"""Etapa 4 (Parte VIII-D): coleta, na API pública do DataJud (TJRN), da POPULAÇÃO de processos dos 14 Juizados
Especiais Cíveis de Natal (classe 436 e a 156, para a qual a 436 evolui no cumprimento de sentença, sob o mesmo
número), ajuizados nas janelas do experimento (01/01 a 03/08) de 2025 e de 2026; depois, o resto de 2025 (para as
tendências mensais) e, só para o 4º JEC, 2024 (para reconstruir a "média anterior" de 106,8 dias).

Uso (na raiz do projeto):
    .venv/Scripts/python.exe EstudodeCaso2/datajud_sondagem/coleta_natal.py     # coleta ou retoma
    .venv/Scripts/python.exe EstudodeCaso2/datajud_sondagem/preparar_tpu.py     # completa o cache da TPU (offline depois)

Desenho da coleta (a API está sobrecarregada: 429 / es_rejected_execution / falhas de shard / quedas de conexão):
- uma consulta por vez (sem paralelismo), pausa entre páginas, tentativas com espera crescente (api.consultar);
- fatias = (juizado, janela de ajuizamento), em ordem de prioridade; cada fatia é paginada com search_after
  (ordem @timestamp + id) e tem o seu estado em disco (natal/estado.json): uma fatia concluída nunca é refeita;
  uma interrompida retoma da última página aceita. Um registro atualizado durante a coleta muda de @timestamp e
  reaparece adiante (a duplicata é descartada pelo _id), de modo que nenhum registro se perde;
- filtro do juizado pelos MOVIMENTOS (movimentos.orgaoJulgador.codigo), e não pelo órgão atual: entram também os
  processos que depois saíram da unidade. A unidade de cada processo é definida no notebook (juizado do 1º movimento);
- _source mínimo (sem complementos nem assuntos) e páginas de 1.000, para reduzir o número de chamadas (com a API
  sobrecarregada, cada resposta aceita custava ~10 a 15 tentativas).
  Uma 1ª versão, com fatias mensais e páginas de 100, levava ~10 min por fatia com a API sobrecarregada; o arquivo
  natal/13285_202501.jsonl.gz é dessa versão (contido na janela de 2025 do 4º JEC; duplicatas descartadas pelo _id).
"""
import gzip
import json
import sys
import time
from pathlib import Path

import api

AQUI = Path(__file__).resolve().parent
PASTA = AQUI / 'natal'
ESTADO = PASTA / 'estado.json'
JECS = {13282: '1º JEC', 13283: '2º JEC', 5153: '3º JEC', 13285: '4º JEC', 13286: '5º JEC', 83097: '6º JEC',
        13288: '7º JEC', 13289: '8º JEC', 13290: '9º JEC', 13291: '10º JEC', 13292: '11º JEC', 13293: '12º JEC',
        13284: '13º JEC', 77266: '14º JEC'}   # códigos de orgaoJulgador no TJRN (contagens.json)
CLASSES = [436, 156]
CAMPOS = ['numeroProcesso', 'classe.codigo', 'dataAjuizamento', 'orgaoJulgador.codigo', 'grau',
          'dataHoraUltimaAtualizacao', 'movimentos.codigo', 'movimentos.dataHora', 'movimentos.orgaoJulgador.codigo']
PAGINA = 1000
JANELAS = {'janela2025': (20250101000000, 20250804000000),   # mesma janela do calendário do experimento
           'janela2026': (20260101000000, 20260804000000),   # 01/01 a 03/08/2026
           'resto2025': (20250804000000, 20260101000000),
           'ano2024': (20240101000000, 20250101000000)}


def tarefas():
    # prioridade: tudo do 4º JEC (antes × durante; 2024 para a "média anterior"); as janelas dos outros 13 (DiD);
    # por fim, o resto de 2025 dos outros (só para o gráfico de tendências)
    quarto = [(13285, j) for j in ('janela2026', 'janela2025', 'resto2025', 'ano2024')]
    outros = [c for c in JECS if c != 13285]
    return quarto + [(c, j) for c in outros for j in ('janela2025', 'janela2026')] + [(c, 'resto2025') for c in outros]


def corpo(codigo, janela, depois=None, tamanho=PAGINA):
    ini, fim = JANELAS[janela]
    c = {'size': tamanho, '_source': CAMPOS, 'track_total_hits': depois is None,
         'query': {'bool': {'filter': [{'term': {'movimentos.orgaoJulgador.codigo': str(codigo)}},
                                       {'terms': {'classe.codigo': CLASSES}},
                                       {'range': {'dataAjuizamento': {'gte': ini, 'lt': fim}}}]}},
         'sort': [{'@timestamp': {'order': 'asc'}}, {'id.keyword': {'order': 'asc'}}]}
    if depois:
        c['search_after'] = depois
    return c


def main():
    PASTA.mkdir(exist_ok=True)
    estado = json.loads(ESTADO.read_text(encoding='utf-8')) if ESTADO.exists() else {}
    lista = tarefas()
    for cod, jan in lista:
        chave = f'{cod}_{jan}'
        st = estado.get(chave, {'depois': None, 'n': 0, 'fim': False})
        if st['fim']:
            continue
        destino = PASTA / f'{chave}.jsonl.gz'
        tamanho = PAGINA
        vistos = set()
        if destino.exists():
            with gzip.open(destino, 'rt', encoding='utf-8') as f:
                vistos = {json.loads(linha)['_id'] for linha in f}
        while True:
            # página adaptativa: se 8 tentativas seguidas falham (o gateway devolve 504/HTML para respostas grandes),
            # a página cai pela metade (até 100) e volta a crescer depois de uma resposta aceita
            while True:
                try:
                    j = api.consultar(corpo(cod, jan, st['depois'], tamanho), tentativas=8, pausa=2.0)
                    break
                except RuntimeError:
                    tamanho = max(100, tamanho // 2)
                    print(f'    página reduzida para {tamanho}', flush=True)
            hits = j['hits']['hits']
            if st['depois'] is None:
                st['total_api'] = j['hits']['total']['value']
            if not hits:
                st['fim'] = True
                break
            with gzip.open(destino, 'at', encoding='utf-8') as f:
                for h in hits:
                    if h['_id'] not in vistos:
                        vistos.add(h['_id'])
                        f.write(json.dumps({'_id': h['_id'], **h['_source']}, ensure_ascii=False) + '\n')
            st['depois'] = hits[-1]['sort']
            st['n'] = len(vistos)
            estado[chave] = st
            ESTADO.write_text(json.dumps(estado), encoding='utf-8')
            print(f'    {time.strftime("%H:%M:%S")} {JECS[cod]} {jan}: {st["n"]} / {st.get("total_api")}', flush=True)
            pedido, tamanho = tamanho, min(PAGINA, tamanho * 2)
            if len(hits) < pedido:
                st['fim'] = True
                break
        st['coletado_em'] = time.strftime('%Y-%m-%d %H:%M:%S')
        estado[chave] = st
        ESTADO.write_text(json.dumps(estado), encoding='utf-8')
        print(f'{time.strftime("%H:%M:%S")} FATIA {JECS[cod]} {jan}: {st["n"]} / {st.get("total_api")} '
              f'(chamadas {api.CHAMADAS["n"]})', flush=True)
    feitos = sum(1 for cod, jan in lista if estado.get(f'{cod}_{jan}', {}).get('fim'))
    print(f'fatias concluídas: {feitos} de {len(lista)}')
    return 0 if feitos == len(lista) else 1


if __name__ == '__main__':
    sys.exit(main())
