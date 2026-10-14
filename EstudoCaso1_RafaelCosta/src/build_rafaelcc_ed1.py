"""Gera EstudodeCaso1/rafaelcc_ed1.ipynb a partir de celulas declaradas aqui.

Uso (na raiz do projeto):
    uv run python EstudodeCaso1/src/build_rafaelcc_ed1.py
    uv run jupyter nbconvert --to notebook --execute --inplace EstudodeCaso1/rafaelcc_ed1.ipynb
"""
import json
import sys
from pathlib import Path

import nbformat as nbf

sys.path.insert(0, str(Path(__file__).parent))
INTERP = {}
try:
    from interp_robustez import INTERP_ROBUSTEZ  # seção 9 (prescrição e regras textuais)
    INTERP.update(INTERP_ROBUSTEZ)
    from interp_exercicios import INTERP_EXERCICIOS  # seções 10 a 14 (exercícios do professor)
    INTERP.update(INTERP_EXERCICIOS)
    from interp_tempo import INTERP_TEMPO  # seções 15 a 20 (tempo de tramitação e DataJud)
    INTERP.update(INTERP_TEMPO)
except ImportError:
    pass

DESTINO = Path(__file__).resolve().parents[1] / "rafaelcc_ed1.ipynb"
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
# Estudo de Caso 1: o Tempo de Tramitação dos Inquéritos Policiais de Homicídio em Goiás

**Autor:** rafaelcc · **Disciplina:** Ciência de Dados e Estatística (CDEDPP) · **Notebook:** `rafaelcc_ed1.ipynb` (gerado por `src/build_rafaelcc_ed1.py`)

## Introdução

O inquérito policial (IP) é o procedimento pelo qual a Polícia Civil apura a materialidade e a autoria de uma infração penal e o encaminha ao Ministério Público, titular da ação penal. Nos crimes dolosos contra a vida, a **duração** do inquérito é um indicador central da capacidade do sistema de justiça criminal de responsabilizar autores. Um IP que se arrasta por anos perde prova testemunhal e pericial, aproxima-se da prescrição e raramente produz denúncia.

**A base.** Este estudo analisa uma **amostra de 218 inquéritos policiais de homicídio e crimes correlatos** (latrocínio, feminicídio, lesão corporal seguida de morte) de **seis comarcas goianas**: Goiânia, Aparecida de Goiânia, Anápolis, Luziânia, Senador Canedo e Águas Lindas de Goiás. Os dados (Apêndice B) vêm dos sistemas Atena (MPGO) e Projudi (TJGO) e do texto dos próprios inquéritos, e são acompanhados de um quadro de variáveis (Apêndice A). Uma segunda base, coletada na **API pública do DataJud (CNJ)**, amplia a análise para todos os inquéritos de CVLI do **Estado de Goiás** registrados no TJGO, o que permite comparar as seis comarcas da amostra com a população.

**Variável-alvo.** O **tempo de tramitação**, em duas definições:

- o **tempo total**, da instauração do IP à conclusão no MP;
- a **fase judicial**, da chegada ao Projudi à conclusão no MP.

**Perguntas de pesquisa.**

1. **Curadoria.** Os dados são coerentes? Que registros são incoerentes e como tratá-los sem inventar informação?
2. **Mensuração.** O que a base realmente mede como "tempo de tramitação"? Que vieses o desenho da amostra introduz (censura, truncamento)?
3. **Distribuição.** O tempo segue uma distribuição normal? Ou se ajusta a alguma família paramétrica, em particular a gama generalizada?
4. **Fatores.** Que variáveis do caso e da investigação se associam a um tempo maior ou menor? Os efeitos resistem ao controle das demais variáveis e à censura?
5. **Complementação.** É necessário e viável complementar a base com o DataJud? O que muda com uma amostra maior?

**Pipeline.**

| Parte | Seções | Conteúdo |
|---|---|---|
| Introdução visual (professor) | 1 | Tipos de gráficos e como lê-los |
| I. Curadoria | 2–9 | Leitura, limpeza, partições, tipagem, auditoria de coerência, prescrição, validação das regras textuais, exportação |
| I-B. Exercícios do professor | 10–14 | Exercícios 1 a 5 do roteiro da disciplina (barras e Pareto, quantitativas, grupos, mosaico e correspondência, correlação), com os desafios |
| **Etapa 1 — a amostra do estudo** | | |
| II. Tempo de tramitação | 15–16 | Definição e descrição do tempo; teste de normalidade e justificativa dos testes não paramétricos |
| III. Testes e modelos | 17–19 | Binomial, qui-quadrado, Fisher e post-hoc; Mann-Whitney, Kruskal-Wallis e Dunn; Spearman; ajuste de distribuições (FDA empírica × teórica); regressões linear e logística |
| IV. Sobrevivência | 20–21 | Kaplan-Meier, log-rank, Cox, AFT; janela de observação, truncamento e teste de Tsai |
| **Etapa 2 — a população do Estado (DataJud)** | | |
| V. DataJud | 22 | CVLI/MVI, coleta, curadoria, linha do tempo do inquérito, e a mesma sequência de análises; comparação com a amostra |
| Síntese | 23 | Respostas, limitações e próximos passos |

> A versão anterior deste notebook está preservada em `versoes/ed1_exercicios_2026-10-01/`.

---
''')

md(r'''
### Métodos: visão geral

| Problema | Método | Por quê |
|---|---|---|
| Distribuição assimétrica, com zeros e cauda longa | Mediana, quartis, testes não paramétricos | Não dependem de normalidade |
| Normalidade | Shapiro-Wilk, D'Agostino-Pearson, Anderson-Darling, Lilliefors; Q-Q | Cada teste é sensível a um aspecto diferente |
| Forma da distribuição | Máxima verossimilhança com censura (e entrada tardia) para exponencial, Weibull, gama, lognormal, log-logística e gama generalizada; AIC/BIC, razão de verossimilhança, Cox-Snell, KS por bootstrap | As famílias são aninhadas na gama generalizada |
| Diferença entre grupos | Mann-Whitney (rank-bisserial), Kruskal-Wallis (ε²), Dunn–Holm, correção BH | Comparação de postos, com tamanho de efeito e controle de falsos positivos |
| Procedimentos não concluídos | Kaplan-Meier, log-rank | Usam a informação parcial (censura) |
| Seleção pela chegada ao Projudi | Entrada tardia (truncamento à esquerda); teste de quase-independência de Tsai | Evita superestimar o tempo |
| Efeito ajustado | Cox (resíduos de Schoenfeld, estratificação) e modelos AFT (razão de tempos) | Controle simultâneo das variáveis; alternativa quando os riscos não são proporcionais |

''')

md(r'''
## 1. Tipos de Gráficos: Uma Introdução Visual

| Gráfico | Tipo de variável | Quando usar | Como ler |
|---|---|---|---|
| **Barras/colunas** | Categórica (nominal ou ordinal) | Distribuição de frequências | Altura = contagem/proporção; compara categorias, identifica a moda e categorias raras |
| **Dot plot** | Quantitativa | Amostras pequenas/médias | Cada ponto é uma observação; mostra repetições (empilhamento), lacunas e valores atípicos |
| **Histograma** | Quantitativa | Amostras médias/grandes | Altura = frequência por intervalo; revela forma (simetria, assimetria), centro, dispersão e multimodalidade. O número de intervalos altera a leitura |
| **Boxplot** | Quantitativa (por grupos) | Comparar grupos | Caixa = Q1–Q3 (IQR), linha = mediana, bigodes até 1,5×IQR, pontos além = possíveis outliers; losango = média |
| **Mosaico** | Duas ou mais categóricas | Associação | Área ∝ frequência conjunta; largura = marginal da 1ª variável; altura = condicional da 2ª. Alturas diferentes entre colunas indicam associação |
| **Dispersão** | Duas quantitativas | Relação | Direção, forma e força da relação; reta de mínimos quadrados = tendência linear média; outliers influentes |

---
''')

# =====================================================================
md(r'''
# PARTE I — CURADORIA DOS DADOS

As seções 2 a 9 leem a base da amostra, limpam, tipam e auditam os dados, e exportam o dataset curado que as partes seguintes usam.

## 2. Preparação do Ambiente

As bibliotecas são as declaradas no `pyproject.toml` do projeto (ambiente `uv`). A paleta categórica é fixa e validada para daltonismo; as cores seguem a entidade (a mesma categoria tem sempre a mesma cor) e nunca são recicladas.
''')

code(r'''
from pathlib import Path
from datetime import datetime
from collections import Counter, defaultdict
import gzip
import json
import re
import textwrap
import unicodedata

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns
import scipy
from scipy import stats
import statsmodels
from statsmodels.graphics.mosaicplot import mosaic
import statsmodels.formula.api as smf
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.duration.survfunc import SurvfuncRight, survdiff
from statsmodels.stats.multitest import multipletests
from statsmodels.stats.proportion import proportion_confint
from statsmodels.stats.diagnostic import lilliefors
from statsmodels.nonparametric.smoothers_lowess import lowess
import scikit_posthocs as sp
import lifelines
from lifelines import (KaplanMeierFitter, NelsonAalenFitter, CoxPHFitter, ExponentialFitter, WeibullFitter,
                       LogNormalFitter, LogLogisticFitter, GeneralizedGammaFitter, WeibullAFTFitter, LogNormalAFTFitter,
                       LogLogisticAFTFitter, GeneralizedGammaRegressionFitter)
from lifelines.fitters import ParametricUnivariateFitter
from lifelines.statistics import logrank_test, multivariate_logrank_test, pairwise_logrank_test, proportional_hazard_test
from lifelines.utils import median_survival_times
from autograd_gamma import gammainccln
import warnings
warnings.filterwarnings('ignore', category=FutureWarning)
from lifelines.exceptions import ApproximationWarning, StatisticalWarning, ConvergenceWarning
for _aviso in (ApproximationWarning, StatisticalWarning, ConvergenceWarning, RuntimeWarning):
    warnings.filterwarnings('ignore', category=_aviso)

pd.set_option('display.max_columns', 80)
pd.set_option('display.width', 220)
pd.set_option('display.max_colwidth', 90)
pd.set_option('display.float_format', lambda v: f'{v:,.2f}')

RNG = np.random.default_rng(2026)  # reprodutibilidade dos testes por permutação

# Paleta categórica validada (ordem fixa) e tintas neutras
CORES = ['#2a78d6', '#eb6834', '#1baf7a', '#eda100', '#e87ba4', '#008300', '#4a3aa7', '#e34948']
COR_PRINCIPAL, COR_DESTAQUE = CORES[0], CORES[1]
COR_SECUNDARIA = '#9ec5f4'
TINTA, TINTA_2, GRADE = '#0b0b0b', '#52514e', '#e4e3df'
MAPA_DIVERGENTE = LinearSegmentedColormap.from_list('div', ['#2a78d6', '#f0efec', '#e34948'])
MAPA_SEQUENCIAL = LinearSegmentedColormap.from_list('seq', ['#f5f9fe', '#86b6ef', '#2a78d6', '#0d366b'])

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

# Localizar os dados ao iniciar o kernel pela raiz do projeto ou por esta pasta
_candidatos = [Path.cwd(), Path.cwd() / 'EstudodeCaso1', Path.cwd().parent / 'EstudodeCaso1']
PASTA_ESTUDO = next((p.resolve() for p in _candidatos if (p / 'dat' / 'estcaso_ip').is_dir()), None)
if PASTA_ESTUDO is None:
    raise FileNotFoundError('Pasta dat/estcaso_ip não encontrada. Inicie o notebook dentro do projeto AulaCleuler.')
PASTA_DADOS = PASTA_ESTUDO / 'dat' / 'estcaso_ip'
PASTA_SAIDA = PASTA_ESTUDO / 'dat' / 'processado'

print(f'pandas {pd.__version__} | numpy {np.__version__} | matplotlib {mpl.__version__} | '
      f'seaborn {sns.__version__} | scipy {scipy.__version__} | statsmodels {statsmodels.__version__} | '
      f'lifelines {lifelines.__version__} | scikit-posthocs {sp.__version__}')
print(f'Dados: {PASTA_DADOS}')
''')

# =====================================================================
md(r'''
---

## 3. Criação do Dataset

### 3.1 Leitura da base e do dicionário de variáveis

A planilha `ApendiceB-BaseDados.xlsx` tem uma única aba (`218.1`). O arquivo-fonte nunca é alterado: `dados_brutos` preserva exatamente a leitura e todas as transformações acontecem em uma cópia.
''')

code(r'''
dicionario = pd.read_excel(PASTA_DADOS / 'ApendiceA-QuadroVariaveis.xlsx')
dados_brutos = pd.read_excel(PASTA_DADOS / 'ApendiceB-BaseDados.xlsx', sheet_name='218.1', engine='openpyxl')

print(f'Dicionário: {dicionario.shape[0]} variáveis descritas')
print(f'Base      : {dados_brutos.shape[0]} inquéritos × {dados_brutos.shape[1]} variáveis')
print(f'Linhas inteiramente duplicadas: {dados_brutos.duplicated().sum()}')
print(f'N_ordem duplicados            : {dados_brutos["N_ordem"].duplicated().sum()}')
assert dados_brutos['N_ordem'].is_unique and not dados_brutos.duplicated().any()

with pd.option_context('display.max_colwidth', 120):
    display(dicionario[['N.', 'Categoria', 'Variável', 'Tipo', 'Descrição']])
''')

md(r'''
### 3.2 Correspondência entre dicionário e base

O dicionário descreve 38 variáveis da coleta completa; a base amostral disponibilizada tem 28. Quatro colunas da base têm nome diferente do dicionário (erros de digitação como `manifstacao` e sufixos `_mp`/`_ip` trocados). A tabela abaixo documenta a correspondência e lista as variáveis do dicionário que **não** vieram na base.
''')

code(r'''
CORRECAO_NOMES_DICIONARIO = {
    '4_data_primeira_manifstação': '4_data_primeira_manifstação_mp',
    '5_data_ultima_manifestacao': '5_data_ultima_manifestacao_mp',
    '6_Data_conclusao_MP': '6_data_conclusao_mp',
    'Quantidade_manifestacao_ip': 'Quantidade_manifstacao_mp',
}
dic = dicionario.assign(Variável=dicionario['Variável'].str.strip()).set_index('Variável')

correspondencia = pd.DataFrame({'Coluna na base': dados_brutos.columns})
correspondencia['Nome no dicionário'] = correspondencia['Coluna na base'].map(
    lambda c: CORRECAO_NOMES_DICIONARIO.get(c, c))
correspondencia['Tipo segundo o dicionário'] = correspondencia['Nome no dicionário'].map(dic['Tipo'])
assert correspondencia['Tipo segundo o dicionário'].notna().all(), 'Coluna da base sem correspondente no dicionário'

fora_da_base = dic.index.difference(correspondencia['Nome no dicionário'], sort=False)
print(f'{len(correspondencia)} colunas da base encontradas no dicionário '
      f'({len(CORRECAO_NOMES_DICIONARIO)} com nome divergente).')
print(f'{len(fora_da_base)} variáveis do dicionário ausentes da base: {", ".join(fora_da_base)}')
display(correspondencia)
''')

md(r'''
### 3.3 Perfil bruto: o que o pandas leu

O `dtype` que o pandas atribui na leitura não é o tipo estatístico. Colunas de data vêm como `object` porque misturam datas com textos (`Nao_houve`, `Não informada`); indicadores 0/1 vêm como `int64`, embora sejam qualitativos; e o dicionário classifica datas e tempos como "Qualitativa nominal". A coluna *tipos Python* mostra o que realmente existe em cada coluna.
''')

code(r'''
def tipos_presentes(serie):
    return ', '.join(sorted(serie.dropna().map(lambda v: type(v).__name__).unique()))

perfil_bruto = pd.DataFrame({
    'dtype lido': dados_brutos.dtypes.astype(str),
    'tipos Python presentes': dados_brutos.apply(tipos_presentes),
    'não nulos': dados_brutos.notna().sum(),
    'distintos': dados_brutos.nunique(),
    'exemplo (1ª linha)': dados_brutos.iloc[0].astype(str).str.slice(0, 45),
})
display(perfil_bruto)
''')

# =====================================================================
md(r'''
---

## 4. Limpeza dos Dados

### 4.1 Nomes das colunas

Regras: nomes válidos como identificador Python (sem começar por dígito, sem acento), grafia corrigida (`manifstação` → `manifestacao`), sufixo `_ip` para o que é da polícia e `_mp` para o que é do Ministério Público, e prefixo `Data_` para todas as datas. Os nomes usados nos exercícios do professor (`Comarca`, `Reu_preso`, `Tempo_conclusao_ip`, `Assunto_resumido`...) foram mantidos. `N_ordem` passa a ser o **índice** do DataFrame: é identificador, não medida.
''')

code(r'''
RENOMEAR = {
    '1_data_fato': 'Data_fato',
    '2_data_instauracao': 'Data_instauracao',
    '3_data_recebimento_projudi': 'Data_recebimento_projudi',
    '4_data_primeira_manifstação': 'Data_primeira_manifestacao_mp',
    '5_data_ultima_manifestacao': 'Data_ultima_manifestacao_mp',
    '6_Data_conclusao_MP': 'Data_conclusao_mp',
    'Prazo_conclusao_IP': 'Prazo_conclusao_ip',
    'Quantidade_manifestacao_ip': 'Quantidade_manifestacao_mp',
}
dados = dados_brutos.rename(columns=RENOMEAR).set_index('N_ordem').sort_index()
assert dados.index.is_unique
assert all(c.isidentifier() and c.isascii() for c in dados.columns)

display(pd.DataFrame({'Nome original': list(RENOMEAR), 'Nome padronizado': list(RENOMEAR.values())}))
''')

md(r'''
### 4.2 Textos: espaços, quebras de linha e caracteres "sósias"

Os campos textuais têm espaços duplicados, quebras de linha internas e — achado relevante — **letras cirílicas visualmente idênticas às latinas** (`СРВ` em vez de `CPB`, `НОМІCÍDIO`), resíduo de OCR sobre os PDFs dos inquéritos. Elas tornam dois textos iguais à vista diferentes para o computador. A limpeza troca esses homóglifos pelas letras latinas, colapsa espaços e converte cadeias vazias em `pd.NA`.
''')

code(r'''
HOMOGLIFOS = str.maketrans({
    'А': 'A', 'В': 'B', 'С': 'C', 'Е': 'E', 'Н': 'H', 'І': 'I', 'К': 'K', 'М': 'M',
    'О': 'O', 'Р': 'P', 'Т': 'T', 'Х': 'X', 'а': 'a', 'с': 'c', 'е': 'e', 'о': 'o',
    'р': 'p', 'х': 'x', 'і': 'i',
})
COLUNAS_TEXTO = ['Comarca', 'Assunto_resumido', 'Status_projudi', 'Nome_delegacia', 'Forma_instauracao',
                 'N_ip_ou_apf', 'Nome_lei', 'Capitulacao', 'Tipo_manifestacao_mp']


def limpar_texto(serie):
    """Troca homóglifos cirílicos, colapsa espaços/quebras de linha e converte vazio em NA."""
    return (serie.astype('string')
            .str.translate(HOMOGLIFOS)
            .str.replace(r'\s+', ' ', regex=True)
            .str.strip()
            .replace('', pd.NA))


def normalizar_chave(texto):
    """Chave de comparação: sem acentos, maiúscula, espaços simples (não altera o dado)."""
    if pd.isna(texto):
        return pd.NA
    texto = unicodedata.normalize('NFKD', str(texto).translate(HOMOGLIFOS))
    texto = ''.join(c for c in texto if not unicodedata.combining(c))
    return re.sub(r'\s+', ' ', texto).strip().upper()


diagnostico_texto = []
for coluna in COLUNAS_TEXTO:
    bruto = dados[coluna].astype('string')
    limpo = limpar_texto(dados[coluna])
    diagnostico_texto.append({
        'Variável': coluna,
        'Com cirílico': int(bruto.str.contains('[\u0400-\u04FF]', regex=True, na=False).sum()),
        'Com quebra de linha': int(bruto.str.contains('\n', regex=False, na=False).sum()),
        'Com espaço sobrando': int((bruto != bruto.str.replace(r'\s+', ' ', regex=True).str.strip()).sum()),
        'Distintos antes': bruto.nunique(),
        'Distintos depois': limpo.nunique(),
    })
    dados[coluna] = limpo

display(pd.DataFrame(diagnostico_texto))
assert not any(dados[c].str.contains('[\u0400-\u04FF]', regex=True, na=False).any() for c in COLUNAS_TEXTO)
''')

md(r'''
### 4.3 Marcadores de ausência

A planilha registra ausências com palavras. Elas não são categorias nem zeros e precisam virar `pd.NA`/`NaT`, mas **não têm todas o mesmo significado**:

- **Ausência informativa** — o dado existe no mundo real, mas não foi localizado (`Não informada`, `Não encontrado`);
- **Ausência estrutural** — o dado não existe porque o evento não ocorreu (`Nao_houve` manifestação, `Não se aplica`, `Prejudicado`);
- **Censura** — o evento ainda não ocorreu até a data da coleta (`Nao_concluido`): o tempo de conclusão é *pelo menos* o tempo decorrido.

A informação contida nas ausências estruturais não se perde: ela é preservada em indicadores booleanos derivados (`Concluido_mp`, `Houve_manifestacao_mp`, seção 8).
''')

code(r'''
MARCADORES_AUSENCIA = pd.DataFrame([
    ('Data_prescricao_projudi', 'Não informada', 'Informativa', 'Data de prescrição não registrada no Projudi'),
    ('N_ip_ou_apf', 'Não encontrado', 'Informativa', 'Número do IP/APF não localizado'),
    ('Nome_delegacia', 'NÃO ENCONTRADO', 'Informativa', 'Delegacia não localizada'),
    ('Data_primeira_manifestacao_mp', 'Nao_houve', 'Estrutural', 'O MP não se manifestou no IP'),
    ('Data_ultima_manifestacao_mp', 'Nao_houve', 'Estrutural', 'Não houve (ou não se registrou) última manifestação'),
    ('Tipo_manifestacao_mp', 'Não se aplica', 'Estrutural', 'Sem manifestação, não há tipo'),
    ('Tempo_entre_manifestacoes_mp', 'Prejudicado', 'Estrutural', 'Sem as duas datas, não há intervalo'),
    ('Data_conclusao_mp', 'Nao_concluido', 'Censura', 'Procedimento ainda não concluído no MP'),
], columns=['Variável', 'Marcador na planilha', 'Tipo de ausência', 'Significado'])

MARCADORES_AUSENCIA['Ocorrências'] = [
    int(dados[v].astype('string').str.strip().eq(m).sum()) for v, m in
    zip(MARCADORES_AUSENCIA['Variável'], MARCADORES_AUSENCIA['Marcador na planilha'])
]
display(MARCADORES_AUSENCIA)

# Nas colunas de texto o marcador vira pd.NA; datas e tempos são tratados a seguir
for v, m in zip(MARCADORES_AUSENCIA['Variável'], MARCADORES_AUSENCIA['Marcador na planilha']):
    if v in COLUNAS_TEXTO:
        dados[v] = dados[v].mask(dados[v].eq(m))
''')

md(r'''
### 4.4 Datas

Cada célula de data é classificada em três situações: data válida, marcador de ausência esperado ou **erro de origem** (texto que não é data nem marcador). Os erros de origem viram `NaT` e são registrados na tabela de auditoria com o valor original. Nenhum valor é "adivinhado".
''')

code(r'''
COLUNAS_DATA = ['Data_prescricao_projudi', 'Data_fato', 'Data_instauracao', 'Data_recebimento_projudi',
                'Data_primeira_manifestacao_mp', 'Data_ultima_manifestacao_mp', 'Data_conclusao_mp']
MARCADOR_POR_COLUNA = dict(zip(MARCADORES_AUSENCIA['Variável'], MARCADORES_AUSENCIA['Marcador na planilha']))

registros_auditoria = []


def registrar(n_ordem, variavel, valor, problema, tratamento):
    registros_auditoria.append({'N_ordem': n_ordem, 'Variável': variavel, 'Valor original': str(valor),
                                'Problema': problema, 'Tratamento': tratamento})


resumo_datas = []
for coluna in COLUNAS_DATA:
    original = dados[coluna]
    e_data = original.map(lambda v: isinstance(v, datetime))
    marcador = MARCADOR_POR_COLUNA.get(coluna)
    e_marcador = original.astype('string').str.strip().eq(marcador).fillna(False) if marcador else e_data & False
    erro = original.notna() & ~e_data & ~e_marcador
    for n_ordem in dados.index[erro]:
        registrar(n_ordem, coluna, original[n_ordem], 'Texto que não é data nem marcador de ausência',
                  'Convertido em NaT (não imputado)')
    dados[coluna] = pd.to_datetime(original.where(e_data), errors='coerce').astype('datetime64[ns]')
    resumo_datas.append({'Variável': coluna, 'Datas válidas': int(e_data.sum()),
                         'Marcador de ausência': int(e_marcador.sum()), 'Erro de origem': int(erro.sum()),
                         'Mínimo': dados[coluna].min().date(), 'Máximo': dados[coluna].max().date()})

display(pd.DataFrame(resumo_datas))
display(pd.DataFrame(registros_auditoria))
print('Contexto do erro em Data_fato (N_ordem 170):')
display(dados.loc[[170], ['Data_instauracao', 'Data_recebimento_projudi']])
''')

md(r'''
O valor `12/02/202515` (N_ordem 170) provavelmente corresponde a 12/02/2015, já que a instauração ocorreu em 26/02/2015. Por prudência metodológica ele **não** é imputado: fica `NaT`, e a hipótese fica registrada. Os dois casos em que a data de prescrição contém o texto do status processual indicam deslocamento de colunas no preenchimento.
''')

md(r'''
### 4.5 Contagens e durações

Contagens (pessoas, manifestações) e durações (dias) são **quantitativas discretas**: usam o inteiro anulável `Int64`, que aceita `pd.NA` sem virar `float`. O marcador `Prejudicado` vira ausência.

**Zero estrutural.** Nos 26 procedimentos não concluídos no MP, a planilha registra `Tempo_conclusao_mp = 0`. Esse zero é falso: tratá-lo como duração real puxaria a média para baixo e confundiria "concluído no mesmo dia" com "ainda não concluído". Ele passa a `pd.NA`; os zeros de procedimentos efetivamente concluídos permanecem.
''')

code(r'''
COLUNAS_CONTAGEM = ['N_indiciados', 'N_vitimas', 'Quantidade_manifestacao_mp']
COLUNAS_DIAS = ['Prazo_conclusao_ip', 'Tempo_conclusao_ip', 'Tempo_entre_manifestacoes_mp', 'Tempo_conclusao_mp']

for coluna in COLUNAS_CONTAGEM + COLUNAS_DIAS:
    serie = dados[coluna]
    marcador = MARCADOR_POR_COLUNA.get(coluna)
    if marcador:
        serie = serie.mask(serie.astype('string').str.strip().eq(marcador).fillna(False))
    convertida = pd.to_numeric(serie, errors='coerce')
    assert not (serie.notna() & convertida.isna()).any(), f'Valor não numérico inesperado em {coluna}'
    assert (convertida.dropna() % 1 == 0).all() and (convertida.dropna() >= 0).all(), coluna
    dados[coluna] = convertida.astype('Int64')

nao_concluido = dados['Data_conclusao_mp'].isna()
zeros_falsos = int(dados.loc[nao_concluido, 'Tempo_conclusao_mp'].eq(0).sum())
assert zeros_falsos == nao_concluido.sum(), 'Há não concluídos com tempo diferente de zero'
dados.loc[nao_concluido, 'Tempo_conclusao_mp'] = pd.NA

print(f'Zeros estruturais removidos de Tempo_conclusao_mp: {zeros_falsos}')
print(f'Zeros legítimos mantidos (concluído no mesmo dia): {int(dados["Tempo_conclusao_mp"].eq(0).sum())}')
''')

# =====================================================================
md(r'''
---

## 5. Normalização das Categorias: Partições

Uma variável categórica bem construída é uma **partição** do conjunto de casos:

1. **Exaustiva** — todo caso pertence a alguma categoria (ou é explicitamente ausente);
2. **Disjunta** — nenhum caso pertence a mais de uma categoria, e nenhuma categoria contém conceitualmente outra (ex.: `Homicídio` ⊃ `Homicídio Simples` viola a regra);
3. **Sem classes vazias** — toda categoria declarada tem ao menos um caso;
4. **Sem sinônimos** — a mesma entidade não aparece com duas grafias (`GIH DE LUZIÂNIA` e `GIH GRUPO DE INVESTIGAÇÃO DE HOMICÍDIOS DE LUZIÂNIA`).

A normalização usa **dicionários de mapeamento explícitos** (valor original → rótulo). A função `para_categoria` recusa valores sem mapeamento, e `verificar_particao` confere as quatro propriedades com `assert`, de modo que um erro interrompe a execução em vez de passar despercebido. O conteúdo original continua disponível em `dados_brutos`.
''')

code(r'''
def ordem_por_frequencia(rotulos):
    """Categorias em ordem decrescente de frequência (empates em ordem alfabética)."""
    contagem = rotulos.dropna().value_counts()
    return sorted(contagem.index, key=lambda r: (-contagem[r], str(r)))


def para_categoria(serie, mapa, ordem=None, ordenada=False):
    """Aplica um mapa exaustivo (valor original → rótulo) e devolve dtype category."""
    sem_mapa = sorted(set(serie.dropna().unique()) - set(mapa))
    assert not sem_mapa, f'Valores sem mapeamento: {sem_mapa}'
    rotulos = serie.map(mapa).astype('object').where(lambda s: s.notna(), None)
    ordem = ordem or ordem_por_frequencia(rotulos)
    assert set(rotulos.dropna()) <= set(ordem), 'Há rótulos fora da lista de categorias'
    return rotulos.astype(pd.CategoricalDtype(ordem, ordered=ordenada))


resumo_particoes = []


def verificar_particao(nova, original=None, ausentes_permitidos=0):
    """Confere se uma variável category é partição: exaustiva, disjunta, sem vazias e sem sinônimos."""
    assert isinstance(nova.dtype, pd.CategoricalDtype), f'{nova.name} não é category'
    contagem = nova.value_counts(sort=False)
    chaves = pd.Series(contagem.index.astype(str)).map(normalizar_chave)
    resultado = {
        'Variável': nova.name,
        'Categorias': len(contagem),
        'Categorias vazias': int((contagem == 0).sum()),
        'Casos sem categoria (NA)': int(nova.isna().sum()),
        'Sinônimos (mesma chave)': int(chaves.duplicated().sum()),
        'Soma = n': int(contagem.sum() + nova.isna().sum()) == len(nova),
    }
    if original is not None:
        mapa = pd.crosstab(original.astype('string').fillna('<NA>'), nova.astype('string').fillna('<NA>'))
        resultado['Valor original em >1 categoria'] = int(((mapa > 0).sum(axis=1) > 1).sum())
        resultado['Valores originais'] = original.nunique()
    ok = (resultado['Categorias vazias'] == 0 and resultado['Sinônimos (mesma chave)'] == 0
          and resultado['Casos sem categoria (NA)'] <= ausentes_permitidos and resultado['Soma = n']
          and resultado.get('Valor original em >1 categoria', 0) == 0)
    resultado['Partição válida'] = ok
    assert ok, f'{nova.name} não forma uma partição: {resultado}'
    resumo_particoes.append(resultado)
    return pd.DataFrame(contagem.rename('Casos')).assign(**{'%': lambda t: 100 * t['Casos'] / len(nova)})
''')

md(r'''
### 5.1 Comarca

Os seis nomes vieram em maiúsculas e sem acento. Passam à grafia oficial dos municípios.
''')

code(r'''
MAPA_COMARCA = {
    'GOIANIA': 'Goiânia',
    'APARECIDA DE GOIANIA': 'Aparecida de Goiânia',
    'ANAPOLIS': 'Anápolis',
    'LUZIANIA': 'Luziânia',
    'SENADOR CANEDO': 'Senador Canedo',
    'AGUAS LINDAS DE GOIAS': 'Águas Lindas de Goiás',
}
dados['Comarca'] = para_categoria(dados['Comarca'], MAPA_COMARCA)
verificar_particao(dados['Comarca'], dados_brutos.set_index('N_ordem')['Comarca'])
''')

md(r'''
### 5.2 Assunto (tipo de crime)

Problemas no original: o rótulo genérico `Homicídio` (3 casos) **contém** conceitualmente `Homicídio Simples`, `Qualificado` e `Privilegiado` — a partição não seria disjunta; e `Seguida de Morte` é um fragmento de "lesão corporal seguida de morte" (art. 129, §3º do CP).

Regra adotada: o caso genérico cuja capitulação indica **art. 121, *caput*** é, por definição legal, homicídio simples e é reclassificado; os demais genéricos, cuja capitulação diz apenas "art. 121", recebem o rótulo explícito `Homicídio (espécie não especificada)`, que é disjunto dos outros. Para análises com tabelas de contingência cria-se também `Assunto_grupo` com três classes (o feminicídio de 2023 era, à época, qualificadora do art. 121, §2º, VI).
''')

code(r'''
capitulacao_chave = dados['Capitulacao'].map(normalizar_chave).str.replace(r'\b[L1]2[L1]\b', '121', regex=True)

MAPA_ASSUNTO = {
    'Homicídio Simples': 'Homicídio simples',
    'Homicídio Qualificado': 'Homicídio qualificado',
    'Homicídio Privilegiado': 'Homicídio privilegiado',
    'Homicídio': 'Homicídio (espécie não especificada)',
    'Feminicídio': 'Feminicídio',
    'Latrocínio': 'Latrocínio',
    'Seguida de Morte': 'Lesão corporal seguida de morte',
}
ORDEM_ASSUNTO = ['Homicídio simples', 'Homicídio qualificado', 'Homicídio privilegiado',
                 'Homicídio (espécie não especificada)', 'Feminicídio', 'Latrocínio',
                 'Lesão corporal seguida de morte']
assunto = dados['Assunto_resumido'].map(MAPA_ASSUNTO)
generico_caput = dados['Assunto_resumido'].eq('Homicídio') & capitulacao_chave.str.contains(r'\bCAPUT\b')
for n_ordem in dados.index[generico_caput]:
    registrar(n_ordem, 'Assunto_resumido', 'Homicídio', 'Rótulo genérico com capitulação "art. 121, caput"',
              'Reclassificado como Homicídio simples')
dados['Assunto_resumido'] = para_categoria(assunto.mask(generico_caput, 'Homicídio simples'),
                                           {v: v for v in ORDEM_ASSUNTO}, ORDEM_ASSUNTO)

MAPA_ASSUNTO_GRUPO = {
    'Homicídio simples': 'Homicídio simples',
    'Homicídio qualificado': 'Homicídio qualificado',
    'Feminicídio': 'Homicídio qualificado',
    'Homicídio privilegiado': 'Outros',
    'Homicídio (espécie não especificada)': 'Outros',
    'Latrocínio': 'Outros',
    'Lesão corporal seguida de morte': 'Outros',
}
dados['Assunto_grupo'] = para_categoria(dados['Assunto_resumido'].astype('string'), MAPA_ASSUNTO_GRUPO,
                                        ['Homicídio simples', 'Homicídio qualificado', 'Outros'])

display(pd.crosstab(dados_brutos.set_index('N_ordem')['Assunto_resumido'], dados['Assunto_resumido']))
display(verificar_particao(dados['Assunto_resumido']))
display(verificar_particao(dados['Assunto_grupo'], dados['Assunto_resumido']))
''')

md(r'''
### 5.3 Situação processual (`Status_projudi`)

Os 15 status originais misturam duas informações: a **situação** do procedimento (ativo, suspenso, arquivado) e o **motivo** do arquivamento, com abreviações (`EXT. DA PUNIB.`) e grafias irregulares. São criadas três variáveis hierárquicas, cada uma uma partição:

- `Status_projudi` — os 15 status com rótulos legíveis (nível mais detalhado);
- `Desfecho` — 11 classes: os quatro casos de extinção da punibilidade (prescrição, morte do agente, renúncia, cumprimento de ANPP) formam uma classe, e dois motivos únicos (desistência, sentença absolutória) formam "outros motivos";
- `Status_macro` — 3 classes: Ativo, Suspenso, Arquivado.

Cada nível é função do anterior (nenhum status aparece em dois desfechos), o que garante a hierarquia.
''')

code(r'''
MAPA_STATUS = {  # original: (status detalhado, desfecho)
    'Ativo': ('Ativo: em investigação', 'Em investigação'),
    'Ativo (denúncia)': ('Ativo: denúncia oferecida', 'Denúncia oferecida'),
    'Suspenso': ('Suspenso', 'Suspenso'),
    'Arquivado - EXT. DA PUNIB. POR FALTA DE JUSTA CAUSA PARA AÇÃO PENAL':
        ('Arquivado: falta de justa causa', 'Arquivado: falta de justa causa'),
    'Arquivado - DEFERIMENTO DO PEDIDO':
        ('Arquivado: pedido deferido (motivo não especificado)', 'Arquivado: pedido deferido (motivo não especificado)'),
    'Arquivado - NÃO CONSTITUI CRIME (ATIPICIDADE)': ('Arquivado: atipicidade', 'Arquivado: atipicidade'),
    'Arquivado - AGENTE DESCONHECIDO': ('Arquivado: autoria desconhecida', 'Arquivado: autoria desconhecida'),
    'Arquivado - EXTINÇÃO DA PUNIBILIDADE - PRESCRIÇÃO':
        ('Arquivado: extinção da punibilidade (prescrição)', 'Arquivado: extinção da punibilidade'),
    'Arquivado - EXTINÇÃO DA PUNIBILIDADE - MORTE DO AGENTE':
        ('Arquivado: extinção da punibilidade (morte do agente)', 'Arquivado: extinção da punibilidade'),
    'Arquivado - EXTINÇÃO DA PUNIBILIDADE-RENUNCIA AO DIREITO DE REPRESENTAR':
        ('Arquivado: extinção da punibilidade (renúncia à representação)', 'Arquivado: extinção da punibilidade'),
    'Arquivado - EXT. DA PUNIB PELO CUMPRIMENTO DAS CONDIÇÕES IMP. P/ANPP':
        ('Arquivado: extinção da punibilidade (cumprimento de ANPP)', 'Arquivado: extinção da punibilidade'),
    'Arquivado - LITISPENDÊNCIA': ('Arquivado: litispendência', 'Arquivado: litispendência'),
    'Arquivado - INDICIADO NÃO DENUNCIADO': ('Arquivado: indiciado não denunciado', 'Arquivado: indiciado não denunciado'),
    'Arquivado - DESISTÊNCIA DA PARTE': ('Arquivado: desistência da parte', 'Arquivado: outros motivos'),
    'Arquivado - ABSOLUTÓRIA': ('Arquivado: sentença absolutória', 'Arquivado: outros motivos'),
}
ORDEM_DESFECHO = ['Em investigação', 'Denúncia oferecida', 'Suspenso',
                  'Arquivado: falta de justa causa', 'Arquivado: pedido deferido (motivo não especificado)',
                  'Arquivado: extinção da punibilidade', 'Arquivado: atipicidade', 'Arquivado: autoria desconhecida',
                  'Arquivado: litispendência', 'Arquivado: indiciado não denunciado', 'Arquivado: outros motivos']

status_original = dados['Status_projudi']
dados['Status_projudi'] = para_categoria(status_original, {k: v[0] for k, v in MAPA_STATUS.items()})
dados['Desfecho'] = para_categoria(status_original, {k: v[1] for k, v in MAPA_STATUS.items()}, ORDEM_DESFECHO)
dados['Status_macro'] = para_categoria(
    dados['Desfecho'].astype('string'),
    {d: ('Ativo' if d in ('Em investigação', 'Denúncia oferecida') else
         'Suspenso' if d == 'Suspenso' else 'Arquivado') for d in ORDEM_DESFECHO},
    ['Ativo', 'Suspenso', 'Arquivado'])

display(verificar_particao(dados['Status_projudi'], status_original))
display(verificar_particao(dados['Desfecho'], dados['Status_projudi']))
display(verificar_particao(dados['Status_macro'], dados['Desfecho']))
''')

md(r'''
### 5.4 Delegacia

É a variável mais "suja": 42 valores distintos — 41 grafias de delegacias mais o marcador `NÃO ENCONTRADO` —, com nomes truncados (`...HOMICIDIOS DE APARECI`), com e sem acento, com e sem sigla, e a mesma unidade escrita de formas diferentes (`01 DDP DE ANAPOLIS GO` e `1ª DELEGACIA DISTRITAL DE POLÍCIA DE ANÁPOLIS`). O mapeamento explícito leva cada grafia a um **nome canônico** (sigla – município). `NÃO ENCONTRADO` é ausência informativa.

Para análise, cria-se `Tipo_delegacia` (4 classes, pela natureza da unidade) e `Delegacia_top6` (as 6 unidades mais frequentes e "Outras delegacias", como pede o desafio do Exercício 4).
''')

code(r'''
MAPA_DELEGACIA = {
    'DIH DELEGACIA ESTADUAL DE INVESTIGACAO DE HOMICIDI': 'DIH – Goiânia',
    'GIH GRUPO DE INVESTIGACAO DE HOMICIDIOS DE APARECI': 'GIH – Aparecida de Goiânia',
    'GIH GRUPO DE INVESTIGÀÇÃO DE HOMICÍDIOS DE APARECIDA DE GOIÂNIA': 'GIH – Aparecida de Goiânia',
    'GIH GRUPO DE INVESTIGACAO DE HOMICIDIOS DE ANAPOLIS': 'GIH – Anápolis',
    'GRUPO DE INVESTIGACAO DE HOMICIDIOS DE ANÁPOLIS': 'GIH – Anápolis',
    'GIH DE SENADOR CANEDO': 'GIH – Senador Canedo',
    'GIH GRUPO DE INVESTIGAÇÃO DE HOMICÍDIOS DE SENADOR CANEDO': 'GIH – Senador Canedo',
    'GIH DE LUZIÂNIA': 'GIH – Luziânia',
    'GIH GRUPO DE INVESTIGAÇÃO DE HOMICÍDIOS DE LUZIÂNIA': 'GIH – Luziânia',
    'GRUPO DE INVESTIGAÇÃO DE HOMICÍDIOS DE ÁGUAS LINDAS': 'GIH – Águas Lindas de Goiás',
    'CENTRAL GERAL DE FLAGRANTES DE GOIÂNIA': 'Central Geral de Flagrantes – Goiânia',
    'CENTRAL GERAL DE FLAGRANTES DE APARECIDA DE GOIÂNIA': 'Central Geral de Flagrantes – Aparecida de Goiânia',
    '03 DP DE ANÁPOLIS - CENTRAL DE FLAGRANTE': '3ª DP – Anápolis (Central de Flagrantes)',
    '01 DDP DE GOIANIA GO': '1ª DDP – Goiânia',
    '08 DDP DE GOIANIA GO': '8ª DDP – Goiânia',
    '10 DDP DE GOIANIA GO': '10ª DDP – Goiânia',
    '11 DDP DE GOIANIA GO': '11ª DDP – Goiânia',
    '18 DDP DE GOIANIA GO': '18ª DDP – Goiânia',
    '23 DDP DE GOIANIA GO': '23ª DDP – Goiânia',
    '24 DDP DE GOIANIA GO': '24ª DDP – Goiânia',
    '01 DDP DE APARECIDA DE GOIÂNIA': '1ª DDP – Aparecida de Goiânia',
    '04 DDP DE APARECIDA DE GOIÂNIA': '4ª DDP – Aparecida de Goiânia',
    '07 DDP DE APARECIDA DE GOIÂNIA': '7ª DDP – Aparecida de Goiânia',
    '01 DDP DE ANAPOLIS GO': '1ª DDP – Anápolis',
    '1ª DELEGACIA DISTRITAL DE POLÍCIA DE ANÁPOLIS': '1ª DDP – Anápolis',
    '02 DDP DE ANAPOLIS GO': '2ª DDP – Anápolis',
    '04 DDP DE ANAPOLIS GO': '4ª DDP – Anápolis',
    '05 DDP DE ANAPOLIS GO': '5ª DDP – Anápolis',
    '01 DDP DE LUZIANIA GO': '1ª DDP – Luziânia',
    '02 DDP DE LUZIANIA GO': '2ª DDP – Luziânia',
    '17ª DELEGACIA REGIONAL DE POLÍCIA DE LUZIÂNIA': '17ª DRP – Luziânia',
    'DP DE SENADOR CANEDO GO': 'DP – Senador Canedo',
    '01 CIOPS DE AGUAS LINDAS GO': '1º CIOPS – Águas Lindas de Goiás',
    '1ª DEAM - Goiânia centro': '1ª DEAM – Goiânia',
    'DEAM - ANÁPOLIS': 'DEAM – Anápolis',
    'DPCA - Aparecida de Goiânia': 'DPCA – Aparecida de Goiânia',
    'DEAI DE GOIÂNIA': 'DEAI – Goiânia',
    'DEIC DELEGACIA ESTADUAL DE INVESTIGACOES CRIMINAIS': 'DEIC – Goiânia',
    'GEIC/1ª DRP DE GOIÂNIA': 'GEIC/1ª DRP – Goiânia',
    'DIG': 'DIG (município não informado)',
    'GRUPO DE INVESTIGAÇÃO DE DESAPARECIDOS': 'GID – Grupo de Investigação de Desaparecidos',
}
delegacia_original = dados['Nome_delegacia']
dados['Nome_delegacia'] = para_categoria(delegacia_original, MAPA_DELEGACIA)


def tipo_delegacia(nome):
    if nome.startswith(('DIH', 'GIH')):
        return 'Especializada em homicídios (DIH/GIH)'
    if 'Flagrantes' in nome:
        return 'Central de flagrantes'
    if re.match(r'^(\d+[ªº] (DDP|DRP|CIOPS)|DP) ', nome):
        return 'Distrital/regional (DDP, DP, DRP)'
    return 'Outras especializadas (DEAM, DPCA, DEIC...)'


MAPA_TIPO_DELEGACIA = {n: tipo_delegacia(n) for n in dados['Nome_delegacia'].cat.categories}
dados['Tipo_delegacia'] = para_categoria(dados['Nome_delegacia'].astype('string'), MAPA_TIPO_DELEGACIA)

TOP6_DELEGACIAS = list(dados['Nome_delegacia'].cat.categories[:6])  # categorias já em ordem de frequência
dados['Delegacia_top6'] = para_categoria(
    dados['Nome_delegacia'].astype('string'),
    {n: (n if n in TOP6_DELEGACIAS else 'Outras delegacias') for n in dados['Nome_delegacia'].cat.categories},
    TOP6_DELEGACIAS + ['Outras delegacias'])

print(f'Grafias originais: {delegacia_original.nunique()} → unidades canônicas: {dados["Nome_delegacia"].nunique()}')
display(verificar_particao(dados['Nome_delegacia'], delegacia_original, ausentes_permitidos=1).head(10))
display(verificar_particao(dados['Tipo_delegacia'], dados['Nome_delegacia'], ausentes_permitidos=1))
display(verificar_particao(dados['Delegacia_top6'], dados['Nome_delegacia'], ausentes_permitidos=1))
''')

md(r'''
### 5.5 Forma de instauração e indicadores binários

`Forma_instauracao` tem duas classes que não são verdadeiro/falso (portaria × auto de prisão em flagrante), portanto é `category`. Já `Reu_preso`, `Tramitacao_direta`, `Arma_de_fogo` e `Validacao` são proposições sim/não codificadas 0/1: são **qualitativas nominais dicotômicas** e usam o booleano anulável `boolean` do pandas. Os rótulos legíveis ("Preso"/"Solto") são aplicados apenas na exibição, sem alterar o tipo.

`Validacao` é constante (todos os 218 casos = 1): não tem variabilidade, portanto não tem poder explicativo e fica fora das análises.
''')

code(r'''
dados['Forma_instauracao'] = para_categoria(
    dados['Forma_instauracao'], {'Portaria': 'Portaria', 'APF': 'Auto de prisão em flagrante (APF)'})
verificar_particao(dados['Forma_instauracao'], dados_brutos.set_index('N_ordem')['Forma_instauracao'])

COLUNAS_BOOLEANAS_ORIGINAIS = ['Reu_preso', 'Tramitacao_direta', 'Arma_de_fogo', 'Validacao']
for coluna in COLUNAS_BOOLEANAS_ORIGINAIS:
    assert set(dados[coluna].unique()) <= {0, 1}, f'Domínio inválido em {coluna}'
    dados[coluna] = dados[coluna].map({0: False, 1: True}).astype('boolean')

ROTULOS_BOOLEANOS = {
    'Reu_preso': ('Solto', 'Preso'),
    'Tramitacao_direta': ('Não', 'Sim'),
    'Arma_de_fogo': ('Sem arma de fogo', 'Com arma de fogo'),
    'Validacao': ('Não validado', 'Validado'),
}
display(pd.DataFrame({c: dados[c].value_counts() for c in COLUNAS_BOOLEANAS_ORIGINAIS}).fillna(0).astype(int))
''')

md(r'''
### 5.6 Capitulação: atributos jurídicos extraídos do texto livre

`Capitulacao` tem 82 redações diferentes para, essencialmente, meia dúzia de enquadramentos. Em vez de forçar o texto livre a virar categoria, extraem-se dele atributos bem definidos, cada um uma partição:

- `Artigo_principal` — art. 121 (homicídio), 157 §3º (latrocínio), 129 §3º (lesão corporal seguida de morte) ou 122 (induzimento ao suicídio);
- `Tentativa` — há menção ao art. 14, II, ou às palavras tentativa/tentado;
- `Qualificadora_capitulada` — há menção ao §2º do art. 121 ou à palavra "qualificado".

A extração usa a chave normalizada (sem acentos, homóglifos corrigidos e o erro de OCR `l2l` → `121`). O texto original é mantido em `Capitulacao` (`string`).
''')

code(r'''
def artigo_principal(chave):
    if re.search(r'\b157\b', chave):
        return 'Art. 157 §3º (latrocínio)'
    if re.search(r'\b121\b', chave):
        return 'Art. 121 (homicídio)'
    if re.search(r'\b129\b', chave):
        return 'Art. 129 §3º (lesão corporal seguida de morte)'
    if re.search(r'\b122\b', chave):
        return 'Art. 122 (induzimento ao suicídio)'
    return None


artigos = capitulacao_chave.map(artigo_principal)
assert artigos.notna().all(), 'Capitulação sem artigo reconhecido'
dados['Artigo_principal'] = para_categoria(artigos, {a: a for a in artigos.unique()})
dados['Tentativa'] = capitulacao_chave.str.contains(r'TENTA|\b14\b', regex=True).astype('boolean')
dados['Qualificadora_capitulada'] = capitulacao_chave.str.contains(r'§\s*2|QUALIFICAD', regex=True).astype('boolean')

display(verificar_particao(dados['Artigo_principal']))
print('Concordância entre o assunto (sistema do MP) e a capitulação (texto do IP):')
display(pd.crosstab(dados['Assunto_resumido'], [dados['Artigo_principal'], dados['Qualificadora_capitulada']],
                    margins=True, margins_name='Total'))
''')

md(r'''
### 5.7 Campos multirresposta: leis e diligências do MP

`Nome_lei` e `Tipo_manifestacao_mp` guardam **vários itens na mesma célula**, separados por `;`. Tratar cada combinação como uma categoria criaria classes que se sobrepõem (um caso com "CP; Lei de Drogas" teria intersecção com "CP"). A solução correta é:

1. Separar os itens em uma **tabela longa** (uma linha por caso × item);
2. Classificar cada **item** em uma partição de categorias (cada item em exatamente uma);
3. Voltar ao nível do caso com **indicadores booleanos** (um caso pode ter vários — é multirresposta, e isso é declarado, não escondido).

**Leis.** São só quatro leis, todas as combinações incluem o Código Penal.
''')

code(r'''
LEIS = {'Código Penal': 'Lei_codigo_penal', 'Lei de Drogas': 'Lei_drogas',
        'Código de Trânsito Brasileiro': 'Lei_transito', 'Estatuto do Desarmamento': 'Lei_desarmamento'}
itens_lei = dados['Nome_lei'].str.split(';').explode().str.strip()
assert set(itens_lei.dropna()) <= set(LEIS), set(itens_lei.dropna()) - set(LEIS)

for nome, coluna in LEIS.items():
    dados[coluna] = dados['Nome_lei'].str.contains(nome, regex=False).astype('boolean')
dados['Concurso_lei_especial'] = dados[['Lei_drogas', 'Lei_transito', 'Lei_desarmamento']].any(axis=1).astype('boolean')

cap_menciona_lei_especial = capitulacao_chave.str.contains(r'10\.826|11\.343|LEI DE DROGAS|\bCTB\b|TRANSITO', regex=True)
display(dados[list(LEIS.values())].sum().rename('Casos').to_frame())
print('Concurso com lei especial segundo Nome_lei × segundo o texto da capitulação:')
display(pd.crosstab(dados['Concurso_lei_especial'], cap_menciona_lei_especial.rename('Capitulação cita lei especial')))
''')

md(r'''
**Diligências e manifestações do MP.** São 444 itens com cerca de 300 redações distintas. Cada item é classificado por uma lista **ordenada** de regras (expressões regulares sobre a chave normalizada): a primeira regra que casa define a categoria. Como cada item recebe exatamente um rótulo, o conjunto de categorias é uma partição dos itens por construção; a verificação confirma que nenhuma categoria ficou vazia e que o resíduo "Outras providências" é mínimo.
''')

code(r'''
REGRAS_DILIGENCIA = [  # (categoria, padrão) — a ordem resolve itens que citam dois temas
    ('Outras providências', r'DESTRUICAO'),
    ('Controle externo da atividade policial',
     r'CORREGEDORIA|POLICIA(L|IS)? MILITAR|\bIPM\b|VIATURAS|AGENTES? D[OE]S? ORGAOS D[EO] SEGURANCA|'
     r'AGENTES DE SEGURANCA|ESCALAS DE SERVICO'),
    ('Competência, redistribuição e apensamento',
     r'REDISTRIBU|DECLIN|COMPETEN[CI]|\bVARAS?\b|JUIZADO|APENSAMENTO|HABILITACAO DE SERVENTIA|'
     r'TRIBUNAL DO JURI|COMPARTILHAMENTO'),
    ('Imagens, mídias e dados telemáticos',
     r'CAMERA|IMAGE|VIDEO|MIDIA|QUEBRA DE SIGILO|SIGILO TELEF|TELEFON|TELEMAT|CELULAR|INTERCEPTA|FILMAGE'),
    ('Medidas cautelares, prisão e atos processuais',
     r'PRISAO PREVENTIVA|RELAXAMENTO|PRISAO EM FLAGRANTE|CAUTELA[RE]|TORNOZELEIRA|MONITORAMENTO ELETRONICO|'
     r'MANDADO DE PRISAO|DESCUMPRIMENTO|CUMPRIMENTO DA MEDIDA|MEDIDAS IMPOSTAS|ANPP|EXTINCAO DA PUNIBILIDADE|'
     r'CITADO POR EDITAL|ASSISTENTE DE ACUSACAO|REPRESENTACAO PROCESSUAL'),
    ('Perícias e laudos',
     r'LAUDO|EXAME|PERICI|NECRO|DNA|GENETIC|BALISTIC|REPRODUCAO SIMULADA|CROQUI|RELATORIO MEDICO|PRONTUARIO|'
     r'LEGISTA|\bIML\b|MUNIC|ARMAS? D[EA] FOGO|INSANIDADE|IDENTIFICACAO DE VEICULO|DESCRICAO DE OBJETO'),
    ('Oitivas e identificação de pessoas',
     r'OITIVA|OUVIR|INQUIRI|DEPOIMENTO|INTERROGA|ACAREACAO|TESTEMUNHA|QUALIFICA|LOCALIZ|IDENTIFICA|'
     r'DECLARACO|FAMILIARES|RECONHECIMENTO|INTIMACAO DA VITIMA|PRESTAR'),
    ('Prazo e conclusão do inquérito',
     r'DILACAO|CONCLUS|RELATORIO (CONCLUSIVO|FINAL)|REMESSA (INTEGRAL )?DO INQUERITO|ULTIMAR|REITER|AGUARDAR|'
     r'RETORNO|ANDAMENTO|DILIGENCIAS|AUTORIDADE POLICIAL|PERMANENCIA DOS AUTOS|DEVOLUCAO'),
    ('Documentos, certidões e informações',
     r'CERTIDAO|OBITO|FALECIMENTO|ANTECEDENTES|HISTORICO CRIMINAL|JUNTADA|JUNTAR|DOCUMENTO|DENUNCIAS|'
     r'PROCEDIMENTO INVESTIGATIVO|RECLUSA|PRESO|INFORMA|ESCLARECER|DESAVENCA|ORDEM DE MISSAO|APELIDOS|'
     r'PRESENCA DE PESSOAS|COPIA|CERTIFICAR|OFICI'),
]
CATEGORIAS_DILIGENCIA = [c for c, _ in REGRAS_DILIGENCIA[1:]] + ['Outras providências']


def classificar_diligencia(item):
    chave = normalizar_chave(item)
    for categoria, padrao in REGRAS_DILIGENCIA:
        if re.search(padrao, chave):
            return categoria
    return 'Outras providências'


diligencias_longas = (dados['Tipo_manifestacao_mp'].str.split(';').explode().str.strip()
                      .replace('', pd.NA).dropna().rename('Item').rename_axis('N_ordem').reset_index())
diligencias_longas['Categoria'] = para_categoria(
    diligencias_longas['Item'].map(classificar_diligencia),
    {c: c for c in CATEGORIAS_DILIGENCIA}, ordem_por_frequencia(diligencias_longas['Item'].map(classificar_diligencia)))

print(f'{len(diligencias_longas)} itens em {diligencias_longas["N_ordem"].nunique()} inquéritos; '
      f'{diligencias_longas["Item"].map(normalizar_chave).nunique()} redações distintas')
display(verificar_particao(diligencias_longas['Categoria'].rename('Categoria_diligencia'),
                           diligencias_longas['Item'].map(normalizar_chave)))
with pd.option_context('display.max_colwidth', 110):
    display(diligencias_longas.groupby('Categoria', observed=True)['Item']
            .agg(lambda s: ' | '.join(s.str.upper().value_counts().index[:3])).rename('Exemplos mais frequentes').to_frame())
''')

code(r'''
COLUNA_DILIGENCIA = {
    'Prazo e conclusão do inquérito': 'Dil_prazo_conclusao',
    'Perícias e laudos': 'Dil_pericias',
    'Oitivas e identificação de pessoas': 'Dil_oitivas',
    'Imagens, mídias e dados telemáticos': 'Dil_midias_dados',
    'Documentos, certidões e informações': 'Dil_documentos',
    'Competência, redistribuição e apensamento': 'Dil_competencia',
    'Medidas cautelares, prisão e atos processuais': 'Dil_cautelares',
    'Controle externo da atividade policial': 'Dil_controle_externo',
    'Outras providências': 'Dil_outras',
}
contagem_por_caso = (pd.crosstab(diligencias_longas['N_ordem'], diligencias_longas['Categoria'])
                     .reindex(dados.index, fill_value=0))
for categoria, coluna in COLUNA_DILIGENCIA.items():
    dados[coluna] = contagem_por_caso[categoria].gt(0).astype('boolean')
dados['N_itens_diligencia'] = contagem_por_caso.sum(axis=1).astype('Int64')

# Indício exploratório de morte decorrente de intervenção de agente do Estado
padrao_intervencao = r'INTERVEN|POLICIA(?:L|IS)? MILITAR|\bIPM\b|VIATURAS|AGENTES? D.{0,25}SEGURANCA PUBLICA|AUDITORIA MILITAR'
casos_intervencao = set(diligencias_longas.loc[
    diligencias_longas['Item'].map(normalizar_chave).str.contains(padrao_intervencao, regex=True), 'N_ordem'])
casos_intervencao |= set(dados.index[capitulacao_chave.str.contains('INTERVEN')])
dados['Indicio_intervencao_estatal'] = dados.index.isin(sorted(casos_intervencao))
dados['Indicio_intervencao_estatal'] = dados['Indicio_intervencao_estatal'].astype('boolean')

print(f'Casos com ao menos uma diligência: {int(dados["N_itens_diligencia"].gt(0).sum())}')
print(f'Casos com indício de intervenção estatal: {int(dados["Indicio_intervencao_estatal"].sum())}')
display(dados[list(COLUNA_DILIGENCIA.values())].sum().rename('Casos').to_frame())
''')

# =====================================================================
md(r'''
---

## 6. Tipagem Final do Dataset

### 6.1 Variáveis derivadas

Antes de fixar o esquema, criam-se as variáveis analíticas que as perguntas de pesquisa exigem. Todas são funções determinísticas das variáveis originais:

| Variável | Definição | Tipo |
|---|---|---|
| `Concluido_mp` | há data de conclusão no MP | boolean |
| `Houve_manifestacao_mp` | `Quantidade_manifestacao_mp` > 0 | boolean |
| `Houve_indiciamento` | `N_indiciados` > 0 | boolean |
| `Excedeu_prazo_ip` | `Tempo_conclusao_ip` > `Prazo_conclusao_ip` (10 ou 30 dias). **Indicador aproximado**: compara o prazo legal com a chegada ao Projudi, que não é a conclusão do IP (seção 10) | boolean |
| `Tempo_fato_instauracao` | dias entre o fato e a instauração do IP | Int64 |
| `Tempo_conclusao_ip_anos` | `Tempo_conclusao_ip` / 365,25 | Float64 |
| `Ano_fato`, `Ano_instauracao` | ano calendário | Int64 |
| `Faixa_tempo_ip` | classes de `Tempo_conclusao_ip` (idade do IP na chegada ao Projudi) | category **ordenada** |
''')

code(r'''
dados['Concluido_mp'] = dados['Data_conclusao_mp'].notna().astype('boolean')
dados['Houve_manifestacao_mp'] = dados['Quantidade_manifestacao_mp'].gt(0).astype('boolean')
dados['Houve_indiciamento'] = dados['N_indiciados'].gt(0).astype('boolean')
dados['Excedeu_prazo_ip'] = dados['Tempo_conclusao_ip'].gt(dados['Prazo_conclusao_ip']).astype('boolean')
dados['Tempo_fato_instauracao'] = (dados['Data_instauracao'] - dados['Data_fato']).dt.days.astype('Int64')
dados['Tempo_conclusao_ip_anos'] = (dados['Tempo_conclusao_ip'].astype('Float64') / 365.25).round(2)
dados['Ano_fato'] = dados['Data_fato'].dt.year.astype('Int64')
dados['Ano_instauracao'] = dados['Data_instauracao'].dt.year.astype('Int64')

LIMITES_FAIXA = [-1, 30, 90, 365, 3 * 365, 5 * 365, np.inf]
ROTULOS_FAIXA = ['até 30 dias', '31 a 90 dias', '91 dias a 1 ano', '1 a 3 anos', '3 a 5 anos', 'mais de 5 anos']
dados['Faixa_tempo_ip'] = pd.cut(dados['Tempo_conclusao_ip'].astype(float), LIMITES_FAIXA, labels=ROTULOS_FAIXA,
                                 ordered=True)
display(verificar_particao(dados['Faixa_tempo_ip']))

ROTULOS_BOOLEANOS.update({
    'Tentativa': ('Consumado', 'Tentado'),
    'Qualificadora_capitulada': ('Sem qualificadora', 'Com qualificadora'),
    'Concurso_lei_especial': ('Só Código Penal', 'Com lei especial'),
    'Concluido_mp': ('Não concluído', 'Concluído'),
    'Houve_manifestacao_mp': ('Sem manifestação', 'Com manifestação'),
    'Houve_indiciamento': ('Sem indiciado', 'Com indiciado'),
    'Excedeu_prazo_ip': ('No prazo', 'Excedeu o prazo'),
    'Indicio_intervencao_estatal': ('Sem indício', 'Com indício'),
})
''')

md(r'''
### 6.2 Esquema definitivo e aplicação dos tipos

O esquema abaixo é a "fonte da verdade" do dataset: para cada variável, o **tipo estatístico** (o que ela mede) e o **dtype do pandas** (como é armazenada). Regras:

| Tipo estatístico | dtype pandas | Por quê |
|---|---|---|
| Identificador | índice / `string` | Não se calcula média de número de processo |
| Qualitativa nominal | `category` | Economia de memória, categorias fixas e ordem de exibição controlada |
| Qualitativa ordinal | `category` (`ordered=True`) | Permite comparar `<`, `>` e ordenar corretamente |
| Qualitativa dicotômica (sim/não) | `boolean` | Booleano anulável (`True`, `False`, `pd.NA`); soma = contagem de "sim" |
| Quantitativa discreta | `Int64` | Inteiro anulável: aceita `pd.NA` sem virar `float` |
| Quantitativa contínua | `Float64` | Real anulável |
| Temporal | `datetime64[ns]` | Aritmética de datas; inválidas = `NaT` |
| Texto livre / multirresposta | `string` | Preservado para consulta; a análise usa os atributos extraídos |

A célula aplica `astype` com o esquema e verifica com `assert` que cada coluna terminou com o dtype declarado.
''')

code(r'''
ESQUEMA = pd.DataFrame([
    # variável, grupo, tipo estatístico, dtype, unidade, origem, uso analítico
    ('Comarca', 'Identificação', 'Qualitativa nominal', 'category', '', 'Original normalizada', 'Categórica'),
    ('Nome_delegacia', 'Identificação', 'Qualitativa nominal (alta cardinalidade)', 'category', '', 'Original normalizada', 'Consulta'),
    ('Tipo_delegacia', 'Identificação', 'Qualitativa nominal', 'category', '', 'Derivada', 'Categórica'),
    ('Delegacia_top6', 'Identificação', 'Qualitativa nominal', 'category', '', 'Derivada', 'Categórica'),
    ('N_ip_ou_apf', 'Identificação', 'Identificador', 'string', '', 'Original', 'Excluir de cálculos'),
    ('Assunto_resumido', 'Caso', 'Qualitativa nominal', 'category', '', 'Original normalizada', 'Categórica'),
    ('Assunto_grupo', 'Caso', 'Qualitativa nominal', 'category', '', 'Derivada', 'Categórica'),
    ('Artigo_principal', 'Caso', 'Qualitativa nominal', 'category', '', 'Derivada (capitulação)', 'Categórica'),
    ('Tentativa', 'Caso', 'Qualitativa dicotômica', 'boolean', '', 'Derivada (capitulação)', 'Categórica'),
    ('Qualificadora_capitulada', 'Caso', 'Qualitativa dicotômica', 'boolean', '', 'Derivada (capitulação)', 'Categórica'),
    ('Capitulacao', 'Caso', 'Texto livre', 'string', '', 'Original limpa', 'Consulta'),
    ('Nome_lei', 'Caso', 'Multirresposta', 'string', '', 'Original limpa', 'Consulta'),
    ('Lei_codigo_penal', 'Caso', 'Qualitativa dicotômica', 'boolean', '', 'Derivada (multirresposta)', 'Constante'),
    ('Lei_drogas', 'Caso', 'Qualitativa dicotômica', 'boolean', '', 'Derivada (multirresposta)', 'Multirresposta'),
    ('Lei_transito', 'Caso', 'Qualitativa dicotômica', 'boolean', '', 'Derivada (multirresposta)', 'Multirresposta'),
    ('Lei_desarmamento', 'Caso', 'Qualitativa dicotômica', 'boolean', '', 'Derivada (multirresposta)', 'Multirresposta'),
    ('Concurso_lei_especial', 'Caso', 'Qualitativa dicotômica', 'boolean', '', 'Derivada', 'Categórica'),
    ('N_indiciados', 'Caso', 'Quantitativa discreta', 'Int64', 'pessoas', 'Original', 'Quantitativa'),
    ('Houve_indiciamento', 'Caso', 'Qualitativa dicotômica', 'boolean', '', 'Derivada', 'Categórica'),
    ('N_vitimas', 'Caso', 'Quantitativa discreta', 'Int64', 'pessoas', 'Original', 'Quantitativa'),
    ('Reu_preso', 'Caso', 'Qualitativa dicotômica', 'boolean', '', 'Original', 'Categórica'),
    ('Tramitacao_direta', 'Caso', 'Qualitativa dicotômica', 'boolean', '', 'Original', 'Categórica'),
    ('Forma_instauracao', 'Caso', 'Qualitativa nominal (2 classes)', 'category', '', 'Original normalizada', 'Categórica'),
    ('Arma_de_fogo', 'Caso', 'Qualitativa dicotômica', 'boolean', '', 'Original', 'Categórica'),
    ('Indicio_intervencao_estatal', 'Caso', 'Qualitativa dicotômica', 'boolean', '', 'Derivada (exploratória)', 'Categórica'),
    ('Validacao', 'Caso', 'Qualitativa dicotômica', 'boolean', '', 'Original', 'Constante'),
    ('Status_projudi', 'Desfecho', 'Qualitativa nominal', 'category', '', 'Original normalizada', 'Consulta'),
    ('Desfecho', 'Desfecho', 'Qualitativa nominal', 'category', '', 'Derivada', 'Categórica'),
    ('Status_macro', 'Desfecho', 'Qualitativa nominal', 'category', '', 'Derivada', 'Categórica'),
    ('Concluido_mp', 'Desfecho', 'Qualitativa dicotômica', 'boolean', '', 'Derivada', 'Categórica'),
    ('Data_fato', 'Tempo', 'Temporal', 'datetime64[ns]', 'data', 'Original', 'Temporal'),
    ('Data_instauracao', 'Tempo', 'Temporal', 'datetime64[ns]', 'data', 'Original', 'Temporal'),
    ('Data_recebimento_projudi', 'Tempo', 'Temporal', 'datetime64[ns]', 'data', 'Original', 'Temporal'),
    ('Data_primeira_manifestacao_mp', 'Tempo', 'Temporal', 'datetime64[ns]', 'data', 'Original', 'Temporal'),
    ('Data_ultima_manifestacao_mp', 'Tempo', 'Temporal', 'datetime64[ns]', 'data', 'Original', 'Temporal'),
    ('Data_conclusao_mp', 'Tempo', 'Temporal', 'datetime64[ns]', 'data', 'Original', 'Temporal'),
    ('Data_prescricao_projudi', 'Tempo', 'Temporal', 'datetime64[ns]', 'data', 'Original', 'Temporal'),
    ('Ano_fato', 'Tempo', 'Quantitativa discreta (temporal)', 'Int64', 'ano', 'Derivada', 'Temporal'),
    ('Ano_instauracao', 'Tempo', 'Quantitativa discreta (temporal)', 'Int64', 'ano', 'Derivada', 'Temporal'),
    ('Prazo_conclusao_ip', 'Tempo', 'Quantitativa discreta', 'Int64', 'dias', 'Original', 'Redundante (= f(Reu_preso))'),
    ('Tempo_fato_instauracao', 'Tempo', 'Quantitativa discreta', 'Int64', 'dias', 'Derivada', 'Quantitativa'),
    ('Tempo_conclusao_ip', 'Tempo', 'Quantitativa discreta', 'Int64', 'dias', 'Original', 'Quantitativa'),
    ('Tempo_conclusao_ip_anos', 'Tempo', 'Quantitativa contínua', 'Float64', 'anos', 'Derivada', 'Apresentação'),
    ('Faixa_tempo_ip', 'Tempo', 'Qualitativa ordinal', 'category', '', 'Derivada', 'Categórica'),
    ('Excedeu_prazo_ip', 'Tempo', 'Qualitativa dicotômica', 'boolean', '', 'Derivada', 'Categórica'),
    ('Tempo_entre_manifestacoes_mp', 'Tempo', 'Quantitativa discreta', 'Int64', 'dias', 'Original', 'Quantitativa'),
    ('Tempo_conclusao_mp', 'Tempo', 'Quantitativa discreta (censurada)', 'Int64', 'dias', 'Original', 'Quantitativa'),
    ('Quantidade_manifestacao_mp', 'Atuação do MP', 'Quantitativa discreta', 'Int64', 'manifestações', 'Original', 'Quantitativa'),
    ('Houve_manifestacao_mp', 'Atuação do MP', 'Qualitativa dicotômica', 'boolean', '', 'Derivada', 'Categórica'),
    ('Tipo_manifestacao_mp', 'Atuação do MP', 'Multirresposta', 'string', '', 'Original limpa', 'Consulta'),
    ('N_itens_diligencia', 'Atuação do MP', 'Quantitativa discreta', 'Int64', 'itens', 'Derivada (multirresposta)', 'Quantitativa'),
] + [(c, 'Atuação do MP', 'Qualitativa dicotômica', 'boolean', '', 'Derivada (multirresposta)', 'Multirresposta')
     for c in COLUNA_DILIGENCIA.values()],
    columns=['Variável', 'Grupo', 'Tipo estatístico', 'dtype pandas', 'Unidade', 'Origem', 'Uso analítico'])

assert ESQUEMA['Variável'].is_unique
assert set(ESQUEMA['Variável']) == set(dados.columns), set(ESQUEMA['Variável']) ^ set(dados.columns)

memoria_antes = dados_brutos.memory_usage(deep=True).sum() / 1024
tipos_simples = {v: t for v, t in zip(ESQUEMA['Variável'], ESQUEMA['dtype pandas']) if t != 'category'}
dados = dados.astype(tipos_simples)[ESQUEMA['Variável'].tolist()]  # category já tem suas categorias fixadas

dtypes_finais = dados.dtypes.astype(str)
divergentes = ESQUEMA.loc[dtypes_finais.loc[ESQUEMA['Variável']].values != ESQUEMA['dtype pandas'].values, 'Variável']
assert divergentes.empty, f'dtype diferente do esquema: {list(divergentes)}'

ESQUEMA['Não nulos'] = dados.notna().sum().values
ESQUEMA['Ausentes'] = dados.isna().sum().values
ESQUEMA['Distintos'] = dados.nunique().values
print(f'Dataset final: {dados.shape[0]} inquéritos × {dados.shape[1]} variáveis (índice: {dados.index.name})')
print(f'Memória: {memoria_antes:,.0f} KiB na leitura bruta (28 colunas) → '
      f'{dados.memory_usage(deep=True).sum() / 1024:,.0f} KiB tipado ({dados.shape[1]} colunas)')
display(ESQUEMA.groupby('dtype pandas').size().rename('Variáveis').to_frame())
with pd.option_context('display.max_rows', 80):
    display(ESQUEMA)
''')

code(r'''
dados.info()
''')

# =====================================================================
md(r'''
---

## 7. Auditoria de Qualidade e Coerência

Com os tipos corretos é possível verificar regras de negócio que eram impossíveis sobre texto:

1. **Cronologia** — fato ≤ instauração ≤ recebimento no Projudi ≤ 1ª manifestação ≤ última manifestação ≤ conclusão no MP;
2. **Durações** — as colunas de tempo da planilha conferem com a diferença entre as datas;
3. **Manifestações** — quantidade, datas e intervalo são coerentes entre si;
4. **Dependências** — `Prazo_conclusao_ip` é determinado por `Reu_preso`; `Forma_instauracao` e `Reu_preso` são fortemente ligados;
5. **Territorialidade** — a delegacia pertence ao município da comarca.
6. **Status × indiciamento** — um arquivamento por "indiciado não denunciado" pressupõe ao menos um indiciado.
''')

code(r'''
SEQUENCIA_DATAS = ['Data_fato', 'Data_instauracao', 'Data_recebimento_projudi', 'Data_primeira_manifestacao_mp',
                   'Data_ultima_manifestacao_mp', 'Data_conclusao_mp']
violacoes_cronologia = {
    f'{a} ≤ {b}': int((dados[a].notna() & dados[b].notna() & (dados[a] > dados[b])).sum())
    for a, b in zip(SEQUENCIA_DATAS, SEQUENCIA_DATAS[1:])
}

DURACOES = {
    'Tempo_conclusao_ip': ('Data_instauracao', 'Data_recebimento_projudi'),
    'Tempo_entre_manifestacoes_mp': ('Data_primeira_manifestacao_mp', 'Data_ultima_manifestacao_mp'),
    'Tempo_conclusao_mp': ('Data_recebimento_projudi', 'Data_conclusao_mp'),
}
divergencias_duracao = {}
for coluna, (inicio, fim) in DURACOES.items():
    recalculada = (dados[fim] - dados[inicio]).dt.days.astype('Int64')
    comparavel = dados[coluna].notna() & recalculada.notna()
    divergencias_duracao[coluna] = int((dados.loc[comparavel, coluna] != recalculada[comparavel]).sum())

q = dados['Quantidade_manifestacao_mp']
sem_ultima = q.ge(1) & dados['Data_ultima_manifestacao_mp'].isna()
uma_com_intervalo = q.eq(1) & dados['Tempo_entre_manifestacoes_mp'].gt(0)
for n_ordem in dados.index[sem_ultima]:
    registrar(n_ordem, 'Data_ultima_manifestacao_mp', 'Nao_houve',
              f'{q[n_ordem]} manifestação(ões), mas sem data da última', 'Mantido NaT; intervalo ausente')
for n_ordem in dados.index[uma_com_intervalo]:
    registrar(n_ordem, 'Tempo_entre_manifestacoes_mp', dados.at[n_ordem, 'Tempo_entre_manifestacoes_mp'],
              'Uma única manifestação, mas intervalo entre manifestações > 0', 'Mantido; conferir no processo')

indiciado_sem_indiciado = dados['Desfecho'].eq('Arquivado: indiciado não denunciado') & dados['N_indiciados'].eq(0)
for n_ordem in dados.index[indiciado_sem_indiciado]:
    registrar(n_ordem, 'Status_projudi', 'Arquivado - INDICIADO NÃO DENUNCIADO',
              'Status indica indiciado, mas N_indiciados = 0', 'Mantido; conferir no processo')

MUNICIPIOS_POR_TAMANHO = sorted(MAPA_COMARCA.values(), key=len, reverse=True)  # 'Aparecida de Goiânia' antes de 'Goiânia'
MUNICIPIO_DA_DELEGACIA = {n: next((m for m in MUNICIPIOS_POR_TAMANHO if m in n), None)
                          for n in dados['Nome_delegacia'].cat.categories}
municipio_delegacia = dados['Nome_delegacia'].astype('string').map(MUNICIPIO_DA_DELEGACIA)
fora_da_comarca = municipio_delegacia.notna() & municipio_delegacia.ne(dados['Comarca'].astype('string'))

relatorio_validacao = pd.DataFrame([
    ('Identificador único', dados.index.is_unique, f'{dados.index.nunique()} N_ordem distintos'),
    ('Nenhuma linha duplicada', not dados.duplicated().any(), f'{dados.duplicated().sum()} duplicadas'),
    ('Cronologia respeitada', sum(violacoes_cronologia.values()) == 0, f'{sum(violacoes_cronologia.values())} violações'),
    ('Durações conferem com as datas', sum(divergencias_duracao.values()) == 0,
     f'{sum(divergencias_duracao.values())} divergências'),
    ('Sem manifestação ⇔ sem 1ª data', (q.eq(0) == dados['Data_primeira_manifestacao_mp'].isna()).all(),
     f'{int(q.eq(0).sum())} casos sem manifestação'),
    ('Prazo determinado por Reu_preso', pd.crosstab(dados['Reu_preso'], dados['Prazo_conclusao_ip']).gt(0).sum(axis=1).eq(1).all(),
     'preso → 10 dias; solto → 30 dias'),
    ('Nenhum zero estrutural restante', not (dados['Data_conclusao_mp'].isna() & dados['Tempo_conclusao_mp'].notna()).any(),
     'Tempo_conclusao_mp = NA se não concluído'),
    ('Manifestações com data da última ausente', True, f'{int(sem_ultima.sum())} casos (registrados)'),
    ('Uma manifestação com intervalo > 0', True, f'{int(uma_com_intervalo.sum())} casos (registrados)'),
    ('"Indiciado não denunciado" sem indiciado', True, f'{int(indiciado_sem_indiciado.sum())} casos (registrados)'),
    ('Delegacia fora do município da comarca', True, f'{int(fora_da_comarca.sum())} casos (plausível na região metropolitana)'),
], columns=['Regra', 'Aprovado', 'Resultado'])
assert relatorio_validacao['Aprovado'].all()

auditoria = pd.DataFrame(registros_auditoria).sort_values(['Variável', 'N_ordem']).reset_index(drop=True)
display(relatorio_validacao)
print('Reu_preso × Forma_instauracao (dependência forte, não determinística):')
display(pd.crosstab(dados['Reu_preso'].map({False: 'Solto', True: 'Preso'}), dados['Forma_instauracao']))
print('Delegacias de outro município:')
display(dados.loc[fora_da_comarca, ['Comarca', 'Nome_delegacia']])
print(f'TABELA DE AUDITORIA — {len(auditoria)} registros para conferência documental:')
display(auditoria)
''')

md(r'''
### 7.1 Resumo das partições

Todas as variáveis categóricas criadas passaram nas verificações: nenhuma categoria vazia, nenhum sinônimo, nenhum valor original repartido entre duas categorias e soma das frequências igual ao número de casos. A única ausência admitida é a delegacia não encontrada (1 caso).
''')

code(r'''
resumo = pd.DataFrame(resumo_particoes).drop_duplicates('Variável', keep='last').set_index('Variável')
display(resumo.astype({'Valor original em >1 categoria': 'Int64', 'Valores originais': 'Int64'}))
''')

# =====================================================================
md(r'''
---

## 8. Exportação do Dataset Limpo

O dataset é salvo em dois formatos em `dat/processado/`:

- **`.pkl`** (pickle) — preserva exatamente os dtypes (`category` com a ordem das categorias, `boolean`, `Int64`...). É o formato que os próximos notebooks devem ler;
- **`.xlsx`** — para consulta humana, com abas para os dados, o esquema, a auditoria e a tabela longa de diligências.

A leitura de volta é conferida: o pickle reproduz o DataFrame idêntico.
''')

code(r'''
PASTA_SAIDA.mkdir(parents=True, exist_ok=True)
ARQUIVO_PKL = PASTA_SAIDA / 'rafaelcc_ip_limpo.pkl'
ARQUIVO_XLSX = PASTA_SAIDA / 'rafaelcc_ip_limpo.xlsx'

dados.to_pickle(ARQUIVO_PKL)
with pd.ExcelWriter(ARQUIVO_XLSX, engine='openpyxl') as planilha:
    dados.to_excel(planilha, sheet_name='dados')
    ESQUEMA.to_excel(planilha, sheet_name='esquema', index=False)
    auditoria.to_excel(planilha, sheet_name='auditoria', index=False)
    diligencias_longas.to_excel(planilha, sheet_name='diligencias_longas', index=False)

pd.testing.assert_frame_equal(pd.read_pickle(ARQUIVO_PKL), dados)
print(f'Salvo e conferido: {ARQUIVO_PKL.name} ({ARQUIVO_PKL.stat().st_size / 1024:,.0f} KiB) e '
      f'{ARQUIVO_XLSX.name} ({ARQUIVO_XLSX.stat().st_size / 1024:,.0f} KiB)')
''')

# =====================================================================
code(r'''
def serie_exibicao(dados, variavel):
    """Versão para exibição: booleanos viram category com rótulos; categorias mantêm sua ordem."""
    serie = dados[variavel]
    if isinstance(serie.dtype, pd.BooleanDtype):
        falso, verdadeiro = ROTULOS_BOOLEANOS.get(variavel, ('Não', 'Sim'))
        return serie.map({False: falso, True: verdadeiro}).astype(pd.CategoricalDtype([falso, verdadeiro]))
    return serie


def quebrar(rotulo, largura=16):
    return '\n'.join(textwrap.wrap(str(rotulo), largura)) or str(rotulo)
''')

for _secao in ['secao09_auditoria.py', 'secao10_exercicios.py', 'secao15_etapa1.py', 'secao22_datajud.py',
               'secao23_sintese.py']:
    exec((Path(__file__).parent / _secao).read_text(encoding='utf-8'))

# =====================================================================
nb = nbf.v4.new_notebook()
nb['cells'] = cells
nb['metadata'] = {
    'kernelspec': {'display_name': 'Python 3 (ipykernel)', 'language': 'python', 'name': 'python3'},
    'language_info': {'name': 'python', 'version': '3.12.8'},
}
nbf.write(nb, DESTINO)
print(f'{len(cells)} células escritas em {DESTINO}')
