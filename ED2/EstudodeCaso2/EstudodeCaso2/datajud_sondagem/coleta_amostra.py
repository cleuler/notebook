"""Etapa 1 da sondagem: busca na API pública do DataJud (TJRN) os 938 processos da amostra do experimento.
Uso: python coleta_amostra.py   (retoma de onde parou; grava amostra_vinculada.jsonl.gz)"""
import gzip
import json
import re
from pathlib import Path

import pandas as pd

import api

AQUI = Path(__file__).resolve().parent
PKL = AQUI.parent / 'dat' / 'processado' / 'ed2_tidy.pkl'
DESTINO = AQUI / 'amostra_vinculada.jsonl.gz'
ESTADO = AQUI / 'amostra_estado.json'
LOTE = 25


def main():
    d = pd.read_pickle(PKL)
    numeros = sorted({re.sub(r'\D', '', p) for p in d['processo'].astype(str)})
    assert all(len(n) == 20 for n in numeros), 'número CNJ fora do padrão'
    estado = json.loads(ESTADO.read_text()) if ESTADO.exists() else {'lotes_feitos': []}
    lotes = [numeros[i:i + LOTE] for i in range(0, len(numeros), LOTE)]
    for k, lote in enumerate(lotes):
        if k in estado['lotes_feitos']:
            continue
        j = api.consultar({'size': 200, 'track_total_hits': True,
                           'query': {'terms': {'numeroProcesso': lote}}}, tentativas=200)
        hits = j['hits']['hits']
        with gzip.open(DESTINO, 'at', encoding='utf-8') as f:
            for h in hits:
                f.write(json.dumps({'_id': h['_id'], '_index': h['_index'], **h['_source']}, ensure_ascii=False) + '\n')
        estado['lotes_feitos'].append(k)
        ESTADO.write_text(json.dumps(estado))
        print(f'lote {k + 1}/{len(lotes)}: {len(hits)} registros (total {j["hits"]["total"]["value"]}); chamadas {api.CHAMADAS["n"]}', flush=True)


if __name__ == '__main__':
    main()
