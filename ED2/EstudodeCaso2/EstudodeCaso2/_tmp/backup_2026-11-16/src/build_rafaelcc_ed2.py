"""Gera EstudodeCaso2/rafaelcc_ed2.ipynb a partir de células declaradas em arquivos de seção.

Uso (na raiz do projeto C:\\Users\\MPGO\\AulaCleuler):
    uv run python EstudodeCaso2/src/build_rafaelcc_ed2.py
    uv run jupyter nbconvert --to notebook --execute --inplace EstudodeCaso2/rafaelcc_ed2.ipynb

Arquitetura (ver CONVENCOES.md):
- md(), code() e interp() acrescentam células à lista `cells`;
- os textos de interpretação ficam em interp_*.py (dicionários INTERP_*), redigidos SOMENTE
  a partir das saídas reais do notebook executado;
- cada parte do pipeline é um arquivo secaoNN_*.py, executado (exec) aqui na ordem de SECOES;
  arquivos ainda inexistentes são simplesmente ignorados.
"""
import importlib
import sys
from pathlib import Path

import nbformat as nbf

PASTA_SRC = Path(__file__).resolve().parent
sys.path.insert(0, str(PASTA_SRC))

# ---------------------------------------------------------------- textos de interpretação
INTERP = {}
for _arquivo in sorted(PASTA_SRC.glob('interp_*.py')):
    try:
        _modulo = importlib.import_module(_arquivo.stem)
        for _nome, _valor in vars(_modulo).items():
            if _nome.startswith('INTERP_') and isinstance(_valor, dict):
                INTERP.update(_valor)
    except Exception as _erro:  # um arquivo com erro não impede os demais
        print(f'Aviso: {_arquivo.name} não carregado ({_erro!r})')

import argparse
_ap = argparse.ArgumentParser()
_ap.add_argument('--somente', nargs='*', default=None,
                 help='gera só a curadoria (secao01) + as seções indicadas, para teste isolado '
                      '(o apêndice secao99_catalogo só entra se indicado)')
_ap.add_argument('--saida', default=None, help='caminho do .ipynb de saída (padrão: rafaelcc_ed2.ipynb)')
_ARGS = _ap.parse_args()
DESTINO = Path(_ARGS.saida).resolve() if _ARGS.saida else PASTA_SRC.parent / 'rafaelcc_ed2.ipynb'
cells = []


def md(texto):
    cells.append(nbf.v4.new_markdown_cell(texto.strip('\n')))


def code(texto):
    cells.append(nbf.v4.new_code_cell(texto.strip('\n')))


def interp(chave):
    texto = INTERP.get(chave, f'*Interpretação `{chave}`: a redigir após a execução.*')
    md(texto)


# =====================================================================
md(r'''
# Estudo de Caso 2: Tempo de Tramitação no 4º JEC de Natal/RN — conciliação obrigatória presencial, remota e rito atual

**Autor:** rafaelcc · **Disciplina:** Ciência de Dados e Estatística aplicadas ao Direito e Políticas Públicas (CDEaDPP) — 2026.2 · **Professor:** Cleuler Barbosa das Neves
**Notebook:** `rafaelcc_ed2.ipynb` (gerado por `src/build_rafaelcc_ed2.py`; não editar à mão)

## Introdução

**O experimento.** O juiz titular do 4º Juizado Especial Cível (JEC) de Natal/RN, Paulo Giovani Militão de Alencar, conduziu, como pesquisa de mestrado profissional (PPGDP/UFG, orientação do Prof. Cleuler), um experimento na própria unidade. Cada ação de conhecimento distribuída ao 4º JEC entre **01/01/2026 e 03/08/2026** foi submetida a um sorteio que definia o rito procedimental:

| Grupo (código) | Rótulo neste notebook | Rótulo na planilha | Descrição |
|---|---|---|---|
| `Controle` | Controle (rito atual, AC opcional) | Rito Atual Ac Opcional | Fluxo vigente em Natal desde a pandemia: citação para contestar, sem audiência de conciliação (AC) inaugural, salvo pedido conjunto das partes |
| `Presencial` | AC presencial obrigatória | Ac Obrigatória Presencial | AC inaugural obrigatória (art. 21 da Lei 9.099/1995), no fórum, conduzida por servidora do CEJUSC |
| `Remota` | AC remota obrigatória | Ac Remota | AC inaugural obrigatória por videoconferência (Teams), conduzida por servidora do gabinete |

Nas audiências, a técnica de conciliação também era sorteada (seis técnicas). A planilha de acompanhamento, alimentada diariamente pela unidade, registra **943 processos** sorteados (944 linhas) com o rito, a ocorrência de acordo na audiência ou fora dela, a técnica, o tipo e a data da sentença. A versão analisada foi **atualizada em 07/10/2026**: os processos ainda sem sentença nessa data estão em tramitação e têm, portanto, tempo **censurado à direita**.

**Variável-alvo.** O **tempo de tramitação**, em dias corridos, da distribuição ao 4º JEC até a sentença (de mérito, sem mérito ou homologatória de acordo).

**Perguntas de pesquisa.**

1. **Curadoria.** Os dados brutos são confiáveis? Que anomalias existem e como tratá-las sem inventar informação?
2. **Efeito sobre o tempo.** A audiência de conciliação obrigatória, presencial ou remota, altera o tempo até a sentença em relação ao rito atual?
3. **Efeito sobre o acordo.** A audiência obrigatória aumenta a proporção de acordos? A modalidade (presencial × remota) importa?
4. **Desenho.** O sorteio produziu grupos comparáveis? Que limitações (censura, redistribuições, híbridas, unidade única) afetam a validade interna e a externa?
5. **Questões do professor.** Respostas às questões 2.2 a 2.12 do roteiro.

**Pipeline de ciência de dados.**

| Parte | Seções | Conteúdo |
|---|---|---|
| I. Curadoria | 1 | Ambiente; formação do dataset bruto; fórmulas e data de corte; tipos e tipologia das variáveis; ausências, duplicidades, número CNJ, grafias, recodificações e desvios de protocolo; dataset *tidy* com tempo e evento; verificações; registro de tratamentos; dicionário e exportação |
| II. Exploratória | 2 | Análise univariada e bivariada com o tempo como alvo; normalidade e ajuste de distribuições; modelo binomial para as proporções |
| III. Testes de hipóteses | 3 | Testes adequados a cada pergunta (qui-quadrado, Fisher, Kruskal-Wallis, Mann-Whitney, Dunn, sequências), com tamanho de efeito e correção de multiplicidade |
| IV. Análise de sobrevivência | 4 | Kaplan-Meier, log-rank, Cox, modelos AFT, riscos competitivos (Aalen-Johansen, Fine-Gray) e tempo médio restrito (RMST) |
| V. Multivariada e regressão | 5 | Modelos com covariáveis (mês de distribuição, origem do processo), regressão logística para o acordo e diagnósticos |
| VI. Questões do professor | 6 | Respostas fundamentadas às questões 2.2 a 2.12 |
| VII. Síntese | 7 | Conclusões, limitações e sugestões para a replicação |
| Apêndice | A | Painel-resumo do estudo; catálogo de todas as figuras e tabelas (numeradas por parte: Figura II.3, Tabela III.5) e exportação para `fig/`, `tab/` e `tab/ed2_tabelas.xlsx` |

### O notebook do professor

O notebook inicial `estcaso_4jec_natal_rn.ipynb` foi revisado célula a célula (30 problemas catalogados, E1 a E30). Os principais, corrigidos aqui:

- **E1** — `from lifelines import KaplanMeierFitter, logrank_test` falha (a função fica em `lifelines.statistics`), e o `except ImportError` desliga silenciosamente o Kaplan-Meier: a única análise adequada a dados censurados nunca é executada;
- **E7/E14** — os tempos dos processos em tramitação (censurados) são tratados como tempos completos, e a "janela de 218 dias" não corresponde aos dados; a data de referência real é 07/10/2026, fixada aqui;
- **E3** — duplicidades detectadas e não tratadas (há processos redistribuídos que voltaram e foram **sorteados de novo**, inclusive para outro grupo);
- **E4/E5** — o marcador `**` ("não se aplica") e as ausências estruturais são tratados como categorias ou como "Não";
- **E10** — a "Decisão" (redistribuição por prevenção) é contada como sentença;
- **E6/E16** — quatro colunas de duração são a mesma variável, e a matriz de correlação entre elas é tautológica (r = 1);
- **E17–E27** — Kruskal-Wallis, OLS e ajuste de distribuições aplicados a tempos censurados; testes tautológicos (Encerrado × Ativo) e sem tamanho de efeito nem correção de multiplicidade.

Em cada seção, quando a abordagem difere da do notebook do professor, o erro corrigido é indicado pelo código (E*n*).

---
''')

# =====================================================================
SECOES = ['secao01_curadoria.py', 'secao02_exploratoria.py', 'secao03_testes.py', 'secao04_sobrevivencia.py',
          'secao05_multivariada.py', 'secao06_questoes.py', 'secao07_sintese.py', 'secao08_datajud.py',
          'secao99_catalogo.py']   # apêndice: painel-resumo e catálogo (sempre o último)
if _ARGS.somente:
    SECOES = ['secao01_curadoria.py'] + [x if x.endswith('.py') else x + '.py' for x in _ARGS.somente
                                         if not x.startswith('secao01')]
for _secao in SECOES:
    _caminho = PASTA_SRC / _secao
    if _caminho.exists():
        exec(_caminho.read_text(encoding='utf-8'), globals())

# =====================================================================
nb = nbf.v4.new_notebook()
nb['cells'] = cells
nb['metadata'] = {
    'kernelspec': {'display_name': 'Python 3 (ipykernel)', 'language': 'python', 'name': 'python3'},
    'language_info': {'name': 'python', 'version': '3.12.8'},
}
nbf.write(nb, DESTINO)
print(f'{len(cells)} células escritas em {DESTINO}')
