"""Coleta de inquéritos de CVLI de todo o Estado (TJGO) na API pública do DataJud (CNJ).

Uso (na raiz do projeto):
    uv run python EstudodeCaso1/src/coleta_datajud.py            # coleta ou retoma
    uv run python EstudodeCaso1/src/coleta_datajud.py --refazer  # apaga o cache e recomeça

A API é instável (HTTP 429, shards que falham, quedas de conexão). Por isso:
- cada página só é aceita se nenhum shard falhar; senão, nova tentativa com espera crescente;
- a paginação usa search_after e o ponto de retomada fica gravado em disco;
- o resultado é um cache local (dat/datajud/*.jsonl.gz) lido pelo notebook, que não depende da API.

A chave é a pública, divulgada pelo CNJ em https://datajud-wiki.cnj.jus.br/api-publica/acesso
"""
import gzip
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

import requests

URL = 'https://api-publica.datajud.cnj.jus.br/api_publica_tjgo/_search'
CHAVE_PUBLICA = 'cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=='
CABECALHO = {'Authorization': f'APIKey {CHAVE_PUBLICA}', 'Content-Type': 'application/json'}

PASTA = Path(__file__).resolve().parents[1] / 'dat' / 'datajud'

# Escopo: TODO o Estado de Goiás (TJGO), crimes violentos letais intencionais (CVLI) e correlatos.
# A comarca/município sai de orgaoJulgador.codigoMunicipioIBGE; as 6 comarcas da amostra são marcadas no notebook.
# Assuntos (TPU/CNJ) consultados — a categorização fina (CVLI, tentado, culposo) é feita no notebook:
ASSUNTOS = {
    3370: 'Homicídio Simples', 9636: 'Homicídio Simples',
    3372: 'Homicídio Qualificado', 9638: 'Homicídio Qualificado',
    3371: 'Homicídio Privilegiado', 9637: 'Homicídio Privilegiado',
    11243: 'Homicídio', 12091: 'Feminicídio',
    5567: 'Latrocínio', 11159: 'Latrocínio',
    3387: 'Seguida de Morte', 9643: 'Seguida de Morte',
}
# Segmentos: (A) inquéritos e autos de prisão em flagrante; (B) ações penais que nasceram de inquérito e
# evoluíram de classe com a denúncia (mesmo número de processo; movimento 14739 "Evolução da Classe Processual").
SEGMENTOS = {
    'ip_apf': {'classes': [279, 280], 'movimento_obrigatorio': None},
    'acao_penal_evoluida': {'classes': [282, 283], 'movimento_obrigatorio': [14739]},
    # (C) ações penais que nasceram de inquérito mas mudaram de classe por "Retificação de Classe Processual" (14738),
    # sem o movimento de evolução: mesmo fenômeno, registro diferente
    'acao_penal_retificada': {'classes': [282, 283], 'movimento_obrigatorio': [14738], 'movimento_excluido': [14739]},
}
CLASSES = {279: 'Inquérito Policial', 280: 'Auto de Prisão em Flagrante',
           282: 'Ação Penal de Competência do Júri', 283: 'Ação Penal - Procedimento Ordinário'}
CAMPOS = ['numeroProcesso', 'classe', 'assuntos', 'dataAjuizamento', 'orgaoJulgador', 'sistema', 'formato', 'grau',
          'nivelSigilo', 'dataHoraUltimaAtualizacao', 'movimentos.codigo', 'movimentos.nome', 'movimentos.dataHora',
          'movimentos.complementosTabelados']
TAMANHO_PAGINA = 100
# Fatias por data de ajuizamento (o campo é numérico, aaaammddhhmmss): a consulta estadual inteira estoura o
# tempo limite do gateway (504), mas cada semestre responde. Uma fatia aberta pega datas fora do intervalo.
FATIAS = ([('ate_2013', None, 20140101000000)]
          + [(f'{a}_{s}', a * 10**10 + (101 if s == 1 else 701) * 10**6, (a if s == 1 else a + 1) * 10**10 + (701 if s == 1 else 101) * 10**6)
             for a in range(2014, 2027) for s in (1, 2)]
          + [('desde_2027', 20270101000000, None)])


def consultar(corpo, tentativas=40):
    """POST com tentativas; só aceita resposta sem falha de shard."""
    ultimo = None
    for i in range(tentativas):
        try:
            r = requests.post(URL, headers=CABECALHO, json=corpo, timeout=180)
            j = r.json()
            if r.status_code == 200 and j.get('_shards', {}).get('failed', 0) == 0:
                return j
            ultimo = f'HTTP {r.status_code}; shards com falha: {j.get("_shards", {}).get("failed")}'
        except (requests.RequestException, ValueError) as erro:
            ultimo = repr(erro)[:160]
        espera = min(5 * (i + 1), 30)
        print(f'    tentativa {i + 1} falhou ({ultimo}); nova tentativa em {espera}s', flush=True)
        time.sleep(espera)
    raise RuntimeError(f'API indisponível após {tentativas} tentativas: {ultimo}')


def corpo_busca(segmento, fatia, depois=None):
    _, inicio, fim = fatia
    intervalo = {k: v for k, v in (('gte', inicio), ('lt', fim)) if v is not None}
    filtros = [{'terms': {'classe.codigo': SEGMENTOS[segmento]['classes']}},
               {'terms': {'assuntos.codigo': list(ASSUNTOS)}},
               {'range': {'dataAjuizamento': intervalo}}]
    if SEGMENTOS[segmento]['movimento_obrigatorio']:
        filtros.append({'terms': {'movimentos.codigo': SEGMENTOS[segmento]['movimento_obrigatorio']}})
    consulta = {'filter': filtros}
    if SEGMENTOS[segmento].get('movimento_excluido'):
        consulta['must_not'] = [{'terms': {'movimentos.codigo': SEGMENTOS[segmento]['movimento_excluido']}}]
    corpo = {
        'size': TAMANHO_PAGINA,
        '_source': CAMPOS,
        'track_total_hits': depois is None,
        'query': {'bool': consulta},
        'sort': [{'@timestamp': {'order': 'asc'}}, {'id.keyword': {'order': 'asc'}}],
    }
    if depois:
        corpo['search_after'] = depois
    return corpo


PARALELISMO = 6  # fatias consultadas ao mesmo tempo


def coletar_tudo():
    # Prioridade: anos recentes primeiro (coorte nativa digital, núcleo da Etapa 2), alternando os dois segmentos;
    # o estoque antigo (convertido) vem por último. A ordem não afeta o resultado final, só o que fica pronto antes.
    tarefas = [(s, f) for f in reversed(FATIAS) for s in SEGMENTOS]
    with ThreadPoolExecutor(max_workers=PARALELISMO) as executor:
        resultados = list(executor.map(lambda par: (par[0], coletar_fatia(*par)), tarefas))
    resumo = {s: {'n': 0, 'total_api': 0} for s in SEGMENTOS}
    for segmento, situacao in resultados:
        resumo[segmento]['n'] += situacao['n']
        resumo[segmento]['total_api'] += situacao.get('total_api') or 0
    for segmento, r in resumo.items():
        print(f'== {segmento}: {r["n"]} processos (API: {r["total_api"]})', flush=True)
    return resumo


def coletar_fatia(segmento, fatia):
    rotulo = f'{segmento}__{fatia[0]}'
    destino = PASTA / f'{rotulo}.jsonl.gz'
    estado = PASTA / f'{rotulo}.estado.json'
    situacao = json.loads(estado.read_text(encoding='utf-8')) if estado.exists() else {'depois': None, 'n': 0, 'fim': False}
    if situacao['fim']:
        print(f'{rotulo}: já coletada ({situacao["n"]} processos)')
        return situacao
    vistos = set()
    if destino.exists():
        with gzip.open(destino, 'rt', encoding='utf-8') as f:
            vistos = {json.loads(linha)['_id'] for linha in f}
    print(f'{rotulo}: retomando com {len(vistos)} processos', flush=True)
    while True:
        j = consultar(corpo_busca(segmento, fatia, situacao['depois']))
        hits = j['hits']['hits']
        if situacao['depois'] is None:
            situacao['total_api'] = j['hits']['total']['value']
        if not hits:
            situacao['fim'] = True
            break
        with gzip.open(destino, 'at', encoding='utf-8') as f:
            for h in hits:
                if h['_id'] not in vistos:
                    vistos.add(h['_id'])
                    f.write(json.dumps({'_id': h['_id'], **h['_source']}, ensure_ascii=False) + '\n')
        situacao['depois'] = hits[-1]['sort']
        situacao['n'] = len(vistos)
        estado.write_text(json.dumps(situacao), encoding='utf-8')
        print(f'    {rotulo}: {situacao["n"]} / {situacao.get("total_api")}', flush=True)
    estado.write_text(json.dumps(situacao), encoding='utf-8')
    print(f'{rotulo}: {situacao["n"]} processos (API: {situacao.get("total_api")})', flush=True)
    return situacao


def main():
    PASTA.mkdir(parents=True, exist_ok=True)
    if '--refazer' in sys.argv:
        for arq in PASTA.glob('*'):
            arq.unlink()
    inicio = datetime.now(timezone.utc)
    resumo = coletar_tudo()
    # Conferência: total sem fatiar (consulta de contagem, leve) × soma das fatias
    for s in SEGMENTOS:
        corpo = corpo_busca(s, ('todas', None, None))
        corpo.update({'size': 0, 'track_total_hits': True})
        corpo.pop('sort')
        corpo['query']['bool']['filter'] = [f for f in corpo['query']['bool']['filter'] if 'range' not in f]
        resumo[s]['total_sem_fatiar'] = consultar(corpo)['hits']['total']['value']
        print(f'Conferência {s}: coletados {resumo[s]["n"]} | soma das fatias na API {resumo[s]["total_api"]} | '
              f'total sem fatiar {resumo[s]["total_sem_fatiar"]}', flush=True)
    manifesto = PASTA / 'manifesto.json'
    anterior = json.loads(manifesto.read_text(encoding='utf-8')) if manifesto.exists() else {}
    manifesto.write_text(json.dumps({
        'fonte': URL,
        'inicio_coleta_utc': anterior.get('inicio_coleta_utc', inicio.isoformat()),
        'fim_coleta_utc': datetime.now(timezone.utc).isoformat(),
        'escopo': 'TJGO — todo o Estado', 'segmentos': SEGMENTOS, 'classes': CLASSES, 'assuntos': ASSUNTOS,
        'processos': {c: s['n'] for c, s in resumo.items()},
        'total_api_fatias': {c: s.get('total_api') for c, s in resumo.items()},
        'total_api_sem_fatiar': {c: s.get('total_sem_fatiar') for c, s in resumo.items()},
    }, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'Manifesto gravado em {manifesto}')


if __name__ == '__main__':
    main()
