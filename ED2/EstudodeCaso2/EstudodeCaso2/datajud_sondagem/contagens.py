"""Etapa 2 da sondagem: contagens populacionais (agregações, size=0) dos Juizados de Natal no DataJud/TJRN,
e uma amostra de ~200 processos de outros JECs Cíveis de Natal para comparar padrões de movimentos.
Uso: python contagens.py   -> grava contagens.json e outros_jec.jsonl.gz (retoma o que já foi feito)"""
import gzip
import json
from pathlib import Path

import api

AQUI = Path(__file__).resolve().parent
SAIDA = AQUI / 'contagens.json'
OUTROS = AQUI / 'outros_jec.jsonl.gz'
MUNICIPIO_NATAL = 3201  # valor de orgaoJulgador.codigoMunicipioIBGE dos órgãos de Natal no TJRN (visto no registro do 4º JEC)
COD_4JEC = 13285
PERIODOS = {'2025': (20250101000000, 20260101000000),
            '2026-01-01_a_2026-08-03': (20260101000000, 20260804000000)}
POR_JEC = 15  # processos por JEC na amostra de comparação


def faixa(p):
    ini, fim = PERIODOS[p]
    return {'range': {'dataAjuizamento': {'gte': ini, 'lt': fim}}}


def agrega_orgaos(p):
    corpo = {'size': 0, 'track_total_hits': True,
             'query': {'bool': {'filter': [{'term': {'orgaoJulgador.codigoMunicipioIBGE': MUNICIPIO_NATAL}}, faixa(p)]}},
             'aggs': {'orgao': {'terms': {'field': 'orgaoJulgador.codigo', 'size': 400},
                                'aggs': {'nome': {'top_hits': {'size': 1, '_source': ['orgaoJulgador', 'grau']}},
                                         'classe': {'terms': {'field': 'classe.codigo', 'size': 10}},
                                         'grau': {'terms': {'field': 'grau.keyword', 'size': 5}}}}}}
    return api.consultar(corpo, tentativas=40, pausa=3)


def contar(filtros):
    corpo = {'size': 0, 'track_total_hits': True, 'query': {'bool': {'filter': filtros}}}
    return api.consultar(corpo, tentativas=40, pausa=3)['hits']['total']['value']


def gravar(res):
    SAIDA.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')


def main():
    res = json.loads(SAIDA.read_text(encoding='utf-8')) if SAIDA.exists() else {}
    for p in PERIODOS:
        if p in res:
            continue
        j = agrega_orgaos(p)
        linhas = []
        for b in j['aggregations']['orgao']['buckets']:
            src = b['nome']['hits']['hits'][0]['_source']
            linhas.append({'codigo': b['key'], 'nome': src['orgaoJulgador'].get('nome'), 'n': b['doc_count'],
                           'graus': {g['key']: g['doc_count'] for g in b['grau']['buckets']},
                           'classes': {c['key']: c['doc_count'] for c in b['classe']['buckets']}})
        res[p] = {'total': j['hits']['total']['value'], 'orgaos': linhas}
        gravar(res)
        print(p, j['hits']['total'], len(linhas), 'órgãos; chamadas', api.CHAMADAS['n'], flush=True)
    # 4º JEC: pelo órgão atual do registro × por ter qualquer movimento lançado no 4º JEC (inclui os que saíram)
    p = '2026-01-01_a_2026-08-03'
    extra = res.setdefault('4jec', {})
    for rot, filtro in [('orgao_atual', {'term': {'orgaoJulgador.codigo': COD_4JEC}}),
                        ('algum_movimento_no_4jec', {'term': {'movimentos.orgaoJulgador.codigo': str(COD_4JEC)}})]:
        for per in PERIODOS:
            k = f'{rot}__{per}'
            if k not in extra:
                try:
                    extra[k] = contar([filtro, faixa(per)])
                except RuntimeError as e:
                    extra[k] = f'falhou: {e}'
                gravar(res)
                print(k, extra[k], flush=True)
    # amostra de comparação: outros JECs Cíveis de Natal, ajuizados em mar-abr/2026
    if not OUTROS.exists():
        jecs = [o for o in res[p]['orgaos'] if 'JUIZADO ESPECIAL C' in (o['nome'] or '').upper() and o['codigo'] != COD_4JEC]
        with gzip.open(OUTROS, 'wt', encoding='utf-8') as f:
            for o in jecs:
                corpo = {'size': POR_JEC, 'query': {'bool': {'filter': [
                    {'term': {'orgaoJulgador.codigo': o['codigo']}},
                    {'range': {'dataAjuizamento': {'gte': 20260301000000, 'lt': 20260501000000}}}]}},
                    'sort': [{'@timestamp': {'order': 'asc'}}]}
                hits = api.consultar(corpo, tentativas=40, pausa=3)['hits']['hits']
                for h in hits:
                    f.write(json.dumps({'_id': h['_id'], **h['_source']}, ensure_ascii=False) + '\n')
                print('outros JEC', o['codigo'], o['nome'], len(hits), flush=True)
    print('chamadas', api.CHAMADAS['n'])


if __name__ == '__main__':
    main()
