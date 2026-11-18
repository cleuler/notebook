"""Plano B da Parte VIII-D: contagens mensais de processos ajuizados (classe 436/156) por Juizado Especial Cível de
Natal, 01/2025 a 03/08/2026, por consulta leve (size 0 + agregações): não passa pela fase 'fetch' que a API
sobrecarregada rejeita. Dá só o VOLUME de entrada por juizado e mês (não há desfechos nem tempos).
Unidade = órgão julgador ATUAL do registro (as agregações não veem o 1º movimento).
Uso: .venv/Scripts/python.exe EstudodeCaso2/datajud_sondagem/contagens_mensais.py   -> natal_contagens_mensais.json"""
import json
import sys
import time
from pathlib import Path

import api

AQUI = Path(__file__).resolve().parent
SAIDA = AQUI / 'natal_contagens_mensais.json'
JECS = [13282, 13283, 5153, 13285, 13286, 83097, 13288, 13289, 13290, 13291, 13292, 13293, 13284, 77266]


def main(limite_s=1200):
    inicio = time.time()
    corpo = {'size': 0, 'track_total_hits': True,
             'query': {'bool': {'filter': [{'terms': {'orgaoJulgador.codigo': JECS}},
                                           {'terms': {'classe.codigo': [436, 156]}},
                                           {'range': {'dataAjuizamento': {'gte': 20250101000000, 'lt': 20260804000000}}}]}},
             'aggs': {'orgao': {'terms': {'field': 'orgaoJulgador.codigo', 'size': 20},
                                'aggs': {'mes': {'histogram': {'field': 'dataAjuizamento', 'interval': 100000000,
                                                               'min_doc_count': 0}}}}}}
    while time.time() - inicio < limite_s:
        try:
            j = api.consultar(corpo, tentativas=5, pausa=1)
        except RuntimeError as e:
            print('falhou:', e, flush=True)
            continue
        out = {'coletado_em': time.strftime('%Y-%m-%d %H:%M:%S'), 'total': j['hits']['total']['value'], 'orgaos': {}}
        for b in j['aggregations']['orgao']['buckets']:
            meses = {}
            for m in b['mes']['buckets']:
                k = str(int(m['key']))[:6]            # aaaamm (o histograma de passo 10^8 agrupa por aaaamm)
                if m['doc_count']:
                    meses[k] = meses.get(k, 0) + m['doc_count']
            out['orgaos'][str(b['key'])] = meses
        SAIDA.write_text(json.dumps(out, indent=1), encoding='utf-8')
        print('ok', out['total'], len(out['orgaos']), 'órgãos', flush=True)
        return 0
    print('desistência: limite de tempo atingido')
    return 1


if __name__ == '__main__':
    sys.exit(main())
