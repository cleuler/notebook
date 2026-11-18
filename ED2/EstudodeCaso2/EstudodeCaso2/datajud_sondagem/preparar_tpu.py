"""Completa o cache local da TPU (tpu_movimentos.json) com todos os códigos de movimento presentes nos caches do
DataJud (amostra_vinculada.jsonl.gz e natal/*.jsonl.gz) e com a cadeia de itens-pai de cada um, para que o
notebook (Parte VIII) classifique os movimentos sem acessar a rede.
Uso: .venv/Scripts/python.exe EstudodeCaso2/datajud_sondagem/preparar_tpu.py"""
import gzip
import json
from pathlib import Path

import tpu

AQUI = Path(__file__).resolve().parent


def codigos():
    arqs = [AQUI / 'amostra_vinculada.jsonl.gz'] + sorted((AQUI / 'natal').glob('*.jsonl.gz'))
    out = set()
    for arq in arqs:
        if not arq.exists():
            continue
        with gzip.open(arq, 'rt', encoding='utf-8') as f:
            for linha in f:
                for m in json.loads(linha).get('movimentos') or []:
                    out.add(int(m['codigo']))
    return out


def main():
    cs = sorted(codigos())
    novos = [c for c in cs if str(c) not in tpu._cache]
    print(f'{len(cs)} códigos de movimento; {len(novos)} fora do cache')
    for c in cs:
        tpu.cadeia(c)
    sem_nome = [c for c in cs if not tpu.movimento(c).get('nome')]
    print(f'cache com {len(tpu._cache)} códigos; sem nome na TPU: {sem_nome}')


if __name__ == '__main__':
    main()
