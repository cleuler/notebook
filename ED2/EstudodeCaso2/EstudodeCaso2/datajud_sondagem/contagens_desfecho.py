"""Plano B da Parte VIII-D (2): por consulta leve (size 0 + agregações), conta, por Juizado Especial Cível de Natal e
por janela de ajuizamento (01/01 a 03/08 de 2025 e de 2026), os processos (classe 436/156) cujo registro tem ALGUM
movimento de julgamento (sentença), de mérito, sem mérito e de homologação, segundo as regras TPU da Parte VIII
(códigos tirados do cache tpu_movimentos.json). Não há tempo até a sentença: é a situação na data da coleta.
Unidade = órgão julgador ATUAL do registro.
Uso: .venv/Scripts/python.exe EstudodeCaso2/datajud_sondagem/contagens_desfecho.py   -> natal_contagens_desfecho.json"""
import json
import sys
import time
from pathlib import Path

import api

AQUI = Path(__file__).resolve().parent
SAIDA = AQUI / 'natal_contagens_desfecho.json'
JECS = [13282, 13283, 5153, 13285, 13286, 83097, 13288, 13289, 13290, 13291, 13292, 13293, 13284, 77266]
TPU = json.loads((AQUI / 'tpu_movimentos.json').read_text(encoding='utf-8'))


def cadeia(c):
    out, c = [], int(c)
    while c and c not in out and len(out) < 12:
        out.append(c)
        c = (TPU.get(str(c)) or {}).get('pai')
    return out


def tipo(c):
    """Mesma regra de dj_tipo_julgamento (secao08_datajud.py)."""
    c = int(c)
    nome = ((TPU.get(str(c)) or {}).get('nome') or '').lower()
    if 'embargos de declara' in nome:
        return None
    if c in (466, 14099):
        return 'homologacao'
    if 'execução' in nome or 'cumprimento' in nome:
        return None
    ch = cadeia(c)
    if 193 not in ch:
        return None
    if 385 in ch:
        return 'homologacao' if 'homologa' in nome else 'merito'
    if 218 in ch:
        return 'sem_merito'
    return None


def main(limite_s=1200):
    cods = {}
    for k in TPU:
        t = tipo(k)
        if t:
            cods.setdefault(t, []).append(int(k))
    todos = sorted(c for v in cods.values() for c in v)
    filtros = {'sentenca': {'terms': {'movimentos.codigo': todos}}}
    filtros.update({t: {'terms': {'movimentos.codigo': v}} for t, v in cods.items()})
    corpo = {'size': 0, 'track_total_hits': True,
             'query': {'bool': {'filter': [{'terms': {'orgaoJulgador.codigo': JECS}},
                                           {'terms': {'classe.codigo': [436, 156]}}]}},
             'aggs': {'orgao': {'terms': {'field': 'orgaoJulgador.codigo', 'size': 20},
                                'aggs': {'janela': {'range': {'field': 'dataAjuizamento', 'ranges': [
                                    {'key': '2025', 'from': 20250101000000, 'to': 20250804000000},
                                    {'key': '2026', 'from': 20260101000000, 'to': 20260804000000}]},
                                    'aggs': {'f': {'filters': {'filters': filtros}}}}}}}}
    inicio = time.time()
    while time.time() - inicio < limite_s:
        try:
            j = api.consultar(corpo, tentativas=5, pausa=1)
        except RuntimeError as e:
            print('falhou:', e, flush=True)
            continue
        out = {'coletado_em': time.strftime('%Y-%m-%d %H:%M:%S'), 'codigos': cods, 'orgaos': {}}
        for b in j['aggregations']['orgao']['buckets']:
            out['orgaos'][str(b['key'])] = {jb['key']: {'n': jb['doc_count'], **{k: v['doc_count'] for k, v in jb['f']['buckets'].items()}}
                                           for jb in b['janela']['buckets']}
        SAIDA.write_text(json.dumps(out, indent=1), encoding='utf-8')
        print('ok', len(out['orgaos']), 'órgãos', flush=True)
        return 0
    print('desistência: limite de tempo atingido')
    return 1


if __name__ == '__main__':
    sys.exit(main())
