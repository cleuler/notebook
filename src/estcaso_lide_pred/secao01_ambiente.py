# -*- coding: utf-8 -*-
"""
Seção 1 — Preparação do Ambiente
=================================
Células de markdown e código incluídas no notebook por build_notebook.py.
Usa as funções md() e code() definidas no builder.

Conteúdo gerado
---------------
- Célula markdown: capa do notebook (título, autora, pipeline)
- Célula de código: importações, paleta, configurações globais, localização dos dados
"""

# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 1 — MARKDOWN: CAPA
# ──────────────────────────────────────────────────────────────────────────────
md(r'''
# Estudo de Caso 3: Identificação da Litigância Abusiva Predatória nos Juizados Especiais Cíveis de Natal/RN

**Autora da pesquisa:** Hadja Rayanne Holanda de Alencar
**Dissertação de Mestrado** — Programa de Pós-Graduação em Direito e Políticas Públicas · UFG · 2026
**Notebook:** `estcaso_lide_pred.ipynb` (gerado por `src/estcaso_lide_pred/build_notebook.py`)

---

## Introdução

Os Juizados Especiais Cíveis (JECs) foram criados pela Lei n.º 9.099/1995 com o objetivo de
ampliar o acesso à justiça para demandas de menor complexidade e valor. Nas últimas décadas,
porém, esses canais passaram a ser alvo de um fenômeno denominado **litigância abusiva
predatória**: o ajuizamento massificado de ações judiciais por parte de advogados que atuam de
forma industrializada, com petições padronizadas, documentação precária e ausência de
personalização da relação processual, frequentemente visando obter vantagens financeiras
independentemente do mérito da causa.

O Conselho Nacional de Justiça (CNJ), por meio da **Recomendação n.º 159, de 23 de outubro
de 2024**, formalizou diretrizes e listou **20 condutas processuais** potencialmente abusivas
(Anexo A), fornecendo, pela primeira vez, um marco normativo estruturado para a identificação
desse fenômeno.

**A pesquisa.** Este estudo analisa uma **amostra probabilística estratificada de 595 processos**
distribuídos nos **14 Juizados Especiais Cíveis de Natal/RN**, no triênio **2022–2024**. A coleta
de dados foi realizada pela pesquisadora entre novembro de 2025 e março de 2026, mediante
consulta direta ao sistema PJe do TJRN, com o registro de **25 variáveis binárias (Sim/Não)**
construídas a partir de 19 dos 20 critérios do Anexo A da Recomendação CNJ n.º 159/2024.

**Hipóteses de trabalho:**

| Hipótese | Enunciado |
|---|---|
| **H1** | A aplicação dos parâmetros da Recomendação CNJ n.º 159/2024 *permite* identificar lides predatórias nos 14 JECs de Natal |
| **H1-0** | A aplicação dos parâmetros da Recomendação CNJ n.º 159/2024 *não permite* identificar lides predatórias nos 14 JECs de Natal |
| **H2** | A estimativa de incidência nos JECs de Natal é *maior* que 30% (referência: NT 01/2022 do CIJMG) |
| **H2-0** | A estimativa de incidência nos JECs de Natal é *menor ou igual* a 30% |

**Pipeline do notebook:**

| Seção | Conteúdo | Outputs |
|---|---|---|
| 1 | Ambiente e configurações | — |
| 2 | Curadoria dos dados | Esquema, dicionário de variáveis (Quadro 3 / Tabela 4) |
| 3 | População de referência | Tabela 1 |
| 4 | Desenho amostral | Tabelas 2–3 |
| 5 | Resultados descritivos gerais | Gráficos 1–6, Tabelas 5–8 |
| 6 | Frequência das variáveis F1 e F2 | Tabela 9, Gráfico 7, Tabela 10 |
| 7 | Testes inferenciais (homogeneidade e associação bivariada) | Tabelas 11–13, Gráficos 8–9 |
| 8 | Regressão logística e curva ROC | Tabelas 14–15, Gráfico 10 |
| 9 | Matriz de correlação phi (φ) | Gráficos 11–12, Tabelas 16–17 |
| 10 | Síntese, limitações e próximos passos | — |

---
''')

# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 2 — MARKDOWN: MÉTODOS ESTATÍSTICOS
# ──────────────────────────────────────────────────────────────────────────────
md(r'''
### Métodos: visão geral

| Problema | Método | Justificativa |
|---|---|---|
| Estimativa da incidência na população | Proporção + IC Wilson 95% | Intervalo mais preciso para proporções com amostras finitas |
| Projeção para a população | Proporção amostral × N populacional | Estudo observacional; projeção conservadora |
| Homogeneidade da incidência entre anos | Qui-quadrado de homogeneidade (3×2) | Três grupos independentes, variável binária |
| Homogeneidade entre os 14 JECs | Qui-quadrado de homogeneidade (14×2) + testes z pareados | Heterogeneidade global + identificação de unidades discrepantes |
| Associação entre variável F2 e classificação | Odds Ratio + Fisher exato + IC 95% | Tabelas 2×2 esparsas; F2 raras têm frequências esperadas < 5 |
| Predição multivariada da classificação | Regressão logística binária (MLE) | Controle simultâneo das variáveis; desfecho binário |
| Desempenho do modelo | Pseudo-R² de McFadden, AUC-ROC, matriz de confusão | Capacidade discriminante e calibração |
| Colinearidade e estrutura das variáveis | Coeficiente phi (φ) = Pearson entre binárias | Ausência de escalas contínuas; variáveis todas dicotômicas |
''')

# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 3 — CÓDIGO: IMPORTAÇÕES E CONFIGURAÇÕES GLOBAIS
# ──────────────────────────────────────────────────────────────────────────────
code(r'''
# ── Biblioteca padrão ────────────────────────────────────────────────────────
import re                      # expressões regulares (extração de JEC_numero)
import textwrap                # quebra de rótulos longos em gráficos
import warnings                # controle de avisos dos pacotes estatísticos
from pathlib import Path       # localização de pastas e arquivos

# ── Computação científica ────────────────────────────────────────────────────
import numpy as np             # operações vetoriais e numéricas
import pandas as pd            # estrutura e manipulação de dados tabulares

# ── Visualização ─────────────────────────────────────────────────────────────
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns          # heatmap da matriz de correlação phi

# ── Estatística ──────────────────────────────────────────────────────────────
import scipy
from scipy import stats        # chi2_contingency, fisher_exact, pearsonr, etc.

import statsmodels
import statsmodels.api as sm                                    # Logit
from statsmodels.stats.proportion import (
    proportion_confint,        # IC Wilson
    proportions_ztest,         # teste z de proporções
)

import sklearn
from sklearn.metrics import (
    roc_curve,                 # curva ROC
    auc,                       # área sob a curva
    confusion_matrix,          # matriz de confusão
    classification_report,     # relatório de desempenho
)

# Silenciar avisos de convergência e de futuras mudanças de API
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=RuntimeWarning)

# ── Reprodutibilidade ────────────────────────────────────────────────────────
# Semente fixa para todos os procedimentos aleatórios (ex.: bootstrap futuro)
RNG = np.random.default_rng(2026)

# ── Opções de exibição do pandas ─────────────────────────────────────────────
pd.set_option('display.max_columns', 50)
pd.set_option('display.width', 200)
pd.set_option('display.max_colwidth', 100)
pd.set_option('display.float_format', lambda v: f'{v:,.4f}')

# ── Paleta categórica validada (mesmo padrão do Estudo de Caso 1) ─────────────
# Cores testadas para acessibilidade (daltonismo tipo Deuteranopia/Protanopia)
CORES = ['#2a78d6', '#eb6834', '#1baf7a', '#eda100', '#e87ba4', '#008300', '#4a3aa7', '#e34948']
COR_PRINCIPAL  = CORES[0]   # azul  — categoria dominante / positivo
COR_DESTAQUE   = CORES[1]   # laranja — destaque / significativo
COR_SECUNDARIA = '#9ec5f4'  # azul claro — barras de fundo / IC
COR_CERTEZA    = CORES[2]   # verde — categoria "Certeza"
COR_INDICIO    = CORES[3]   # amarelo escuro — categoria "Indício (sem certeza)"
COR_EXCLUIDO   = CORES[7]   # vermelho — excluídos / p < 0,001

# Tintas neutras para texto, eixos e grade
TINTA   = '#0b0b0b'         # quase preto — títulos e rótulos primários
TINTA_2 = '#52514e'         # cinza escuro — eixos, ticks e rótulos secundários
GRADE   = '#e4e3df'         # cinza muito claro — linhas de grade

# Mapas de cores para heatmap e gráficos divergentes
MAPA_DIVERGENTE = LinearSegmentedColormap.from_list(
    'div_lide', ['#2a78d6', '#f0efec', '#e34948'])
MAPA_SEQUENCIAL = LinearSegmentedColormap.from_list(
    'seq_lide', ['#f5f9fe', '#86b6ef', '#2a78d6', '#0d366b'])

# ── Configurações globais de matplotlib ──────────────────────────────────────
plt.rcParams.update({
    'figure.dpi': 100,
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.edgecolor': TINTA_2,
    'axes.labelcolor': TINTA,
    'axes.titleweight': 'bold',
    'axes.titlesize': 12,
    'axes.grid': True,
    'grid.color': GRADE,
    'grid.linewidth': 0.8,
    'axes.axisbelow': True,
    'xtick.color': TINTA_2,
    'ytick.color': TINTA_2,
    'axes.prop_cycle': mpl.cycler(color=CORES),
    'font.size': 10,
    'legend.frameon': False,
})

# ── Localização dos dados ─────────────────────────────────────────────────────
# Aceita execução a partir da raiz do projeto ou de dentro da pasta do estudo
_candidatos = [Path.cwd(), Path.cwd().parent]
PASTA_DADOS = next(
    (p / 'dat' / 'estcaso_lide_pred'
     for p in _candidatos
     if (p / 'dat' / 'estcaso_lide_pred').is_dir()),
    None,
)
if PASTA_DADOS is None:
    raise FileNotFoundError(
        'Pasta dat/estcaso_lide_pred não encontrada. '
        'Execute o notebook a partir da raiz do projeto.'
    )

# Pasta de saída para o dataset curado
PASTA_SAIDA = PASTA_DADOS / 'processado'
PASTA_SAIDA.mkdir(parents=True, exist_ok=True)

# Arquivo-fonte principal (planilha Excel com as 5 abas)
ARQUIVO_XLSX = (
    PASTA_DADOS
    / 'PlanilhaPreenchidaVariaveisCorrigida_CN_JE_S1422934_Mestrado_03_02.xlsx'
)
assert ARQUIVO_XLSX.exists(), f'Planilha principal não encontrada: {ARQUIVO_XLSX}'

# ── Impressão de versões ──────────────────────────────────────────────────────
print(
    f'pandas      {pd.__version__}  |  numpy   {np.__version__}  |  '
    f'matplotlib  {mpl.__version__}'
)
print(
    f'seaborn     {sns.__version__}  |  scipy   {scipy.__version__}  |  '
    f'statsmodels {statsmodels.__version__}'
)
print(
    f'scikit-learn {sklearn.__version__}'
)
print(f'\nDados : {PASTA_DADOS}')
print(f'Saída : {PASTA_SAIDA}')
''')

# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 4 — CÓDIGO: FUNÇÕES UTILITÁRIAS GLOBAIS
# ──────────────────────────────────────────────────────────────────────────────
code(r'''
# ── Funções utilitárias compartilhadas por todas as seções ───────────────────

def quebrar(rotulo: str, largura: int = 16) -> str:
    """Quebra um rótulo longo em múltiplas linhas para uso em eixos de gráficos.

    Parâmetros
    ----------
    rotulo  : texto a ser quebrado
    largura : largura máxima por linha (em caracteres)

    Retorna
    -------
    Texto com quebras de linha '\n'.
    """
    return '\n'.join(textwrap.wrap(str(rotulo), largura)) or str(rotulo)


def formatar_pvalor(p: float) -> str:
    """Formata um p-valor para exibição em título de gráfico.

    Exemplos
    --------
    0.0001  → 'p < 0,001'
    0.045   → 'p = 0,045'
    0.393   → 'p = 0,393'
    """
    if p < 0.001:
        return 'p < 0,001'
    return f'p = {p:.3f}'.replace('.', ',')


def ic_wilson(k: int, n: int, alpha: float = 0.05) -> tuple[float, float]:
    """Calcula o intervalo de confiança de Wilson para uma proporção.

    Parâmetros
    ----------
    k     : número de sucessos
    n     : tamanho da amostra
    alpha : nível de significância (padrão 0,05 → IC 95%)

    Retorna
    -------
    (limite_inferior, limite_superior) em escala [0, 1]
    """
    li, ls = proportion_confint(int(k), int(n), alpha=alpha, method='wilson')
    return float(li), float(ls)


def anotar_barras(ax, barras, formato: str = '{:.0f}', posicao: str = 'topo',
                  fontsize: int = 9, cor: str = None) -> None:
    """Adiciona rótulos de valor em cima (ou dentro) de cada barra vertical.

    Parâmetros
    ----------
    ax       : eixo matplotlib
    barras   : container de barras (retorno de ax.bar())
    formato  : string de formatação do valor
    posicao  : 'topo' coloca o rótulo acima da barra; 'centro' no meio
    fontsize : tamanho da fonte
    cor      : cor do texto (padrão: TINTA)
    """
    cor = cor or TINTA
    for barra in barras:
        h = barra.get_height()
        if h == 0:
            continue
        y = h + 0.01 * ax.get_ylim()[1] if posicao == 'topo' else h / 2
        va = 'bottom' if posicao == 'topo' else 'center'
        ax.text(
            barra.get_x() + barra.get_width() / 2,
            y,
            formato.format(h),
            ha='center', va=va, fontsize=fontsize, color=cor,
        )


def grafico_floresta_or(
    tabela: 'pd.DataFrame',
    coluna_or: str = 'OR',
    coluna_ic_inf: str = 'IC 2,5%',
    coluna_ic_sup: str = 'IC 97,5%',
    coluna_pvalor: str = 'p-valor',
    titulo: str = 'Odds Ratios (escala log) — IC 95%',
    limiar_sig: float = 0.001,
) -> None:
    """Gera um forest plot horizontal dos Odds Ratios.

    Parâmetros
    ----------
    tabela        : DataFrame com OR, IC e p-valor; índice = nomes das variáveis
    coluna_or     : nome da coluna com o OR pontual
    coluna_ic_inf : nome da coluna com o limite inferior do IC
    coluna_ic_sup : nome da coluna com o limite superior do IC
    coluna_pvalor : nome da coluna com o p-valor
    titulo        : título do gráfico
    limiar_sig    : p-valor abaixo do qual o marcador é destacado em vermelho
    """
    # Ordenar da maior para a menor OR, invertendo para o plot ficar legível
    tab = tabela.copy().sort_values(coluna_or)
    y = np.arange(len(tab))
    cores_ponto = [
        COR_EXCLUIDO if p < limiar_sig else COR_PRINCIPAL
        for p in tab[coluna_pvalor]
    ]

    fig, ax = plt.subplots(figsize=(10, 0.42 * len(tab) + 1.8))

    # Barras de erro (IC)
    ax.hlines(
        y,
        tab[coluna_ic_inf].clip(lower=0.01),  # evitar log(0)
        tab[coluna_ic_sup],
        color=TINTA_2, linewidth=1.8, zorder=2,
    )
    # Marcadores de OR pontual
    ax.scatter(tab[coluna_or], y, color=cores_ponto, s=55, zorder=3)

    # Linha de referência OR = 1
    ax.axvline(1, color=TINTA, linewidth=1.2, linestyle='--', zorder=1)

    # Escala logarítmica no eixo x
    ax.set_xscale('log')
    ax.set_yticks(y)
    ax.set_yticklabels([quebrar(str(i), 42) for i in tab.index], fontsize=8.5)
    ax.set_xlabel('Odds Ratio (escala log) — IC 95%')
    ax.set_title(titulo)
    ax.grid(axis='y', visible=False)

    # Legenda das cores
    from matplotlib.lines import Line2D
    legenda = [
        Line2D([0], [0], marker='o', color='w',
               markerfacecolor=COR_EXCLUIDO, markersize=8,
               label=f'p < {limiar_sig:.3f} (altamente significativo)'),
        Line2D([0], [0], marker='o', color='w',
               markerfacecolor=COR_PRINCIPAL, markersize=8,
               label='p ≥ 0,001'),
    ]
    ax.legend(handles=legenda, fontsize=8.5, loc='lower right')
    plt.tight_layout()
    plt.show()
''')
