# Parte IV — Análise de sobrevivência (seções 4.1 a 4.10).
# Executado por build_rafaelcc_ed2.py (exec): usa md(), code() e interp().

md(r'''
---

# PARTE IV — ANÁLISE DE SOBREVIVÊNCIA

Esta é a parte central do estudo. A pergunta de pesquisa 2 — *a audiência de conciliação (AC) obrigatória, presencial ou remota, altera o tempo até a sentença em relação ao rito atual?* — é uma pergunta sobre **tempo até um evento** observado de forma incompleta: em 07/10/2026, 206 processos ainda não tinham sentença. A análise de sobrevivência é o conjunto de métodos construído exatamente para esse tipo de dado (COLOSIMO; GIOLO, 2006, cap. 1; MORETTIN; SINGER, 2021, cap. 7). O notebook do professor anunciava o Kaplan-Meier como "imprescindível", mas ele nunca era executado por um erro de importação (E1), e todas as comparações de tempo eram feitas com testes que ignoram a censura (E14, E17, E26).

**Roteiro.**

| Seção | Conteúdo | Pergunta respondida |
|---|---|---|
| 4.1 | Conceitos e estrutura dos dados | O que é censura aqui, e ela é "inofensiva"? |
| 4.2 | Kaplan-Meier, Nelson-Aalen, risco suavizado | Como evolui a proporção de processos ainda sem sentença? |
| 4.3 | Testes de comparação de curvas e RMST | As curvas dos três grupos diferem? Onde (no início, no fim)? |
| 4.4 | Diagnóstico de riscos proporcionais | Uma única razão de riscos resume a diferença? |
| 4.5 | Modelos de Cox | Qual o efeito do grupo, ajustado pelo calendário? Ele muda com o tempo? |
| 4.6 | Modelos paramétricos AFT | Em quanto a AC obrigatória alonga ou encurta o tempo (razão de tempos)? |
| 4.7 | Riscos competitivos | O rito muda **o tipo** de sentença (acordo, mérito, sem mérito)? |
| 4.8 | Subconjunto com AC realizada | Presencial × remota, técnica e híbrida entre quem teve audiência |
| 4.9 | Análises de sensibilidade | As conclusões resistem a decisões de curadoria? |
| 4.10 | Síntese | Resposta à pergunta de pesquisa |

**Convenção de sinal (vale para toda a Parte IV).** O "evento" é a **sentença**, que aqui é algo desejável: encerra o conflito. Por isso:

- S(t) = P(processo **ainda sem sentença** após t dias): curva mais alta = rito **mais lento**;
- razão de riscos (HR) > 1 = sentença **mais rápida** que no Controle; **HR < 1 = sentença mais lenta**;
- razão de tempos (AFT) > 1 = tempo **mais longo** que no Controle.
''')

# =====================================================================
md(r'''
## 4.1 Conceitos e estrutura dos dados

### 4.1.1 Tempo, evento, censura e função de risco

**O par (T, δ).** Para cada processo i observa-se o tempo T_i = min(X_i, C_i), em dias desde a distribuição, e o indicador δ_i = 1 se X_i ≤ C_i (a sentença foi observada) ou δ_i = 0 caso contrário. X_i é o tempo até a sentença e C_i é o tempo até a censura (COLOSIMO; GIOLO, 2006, p. 6-12; MORETTIN; SINGER, 2021, p. 243-244). No dataset *tidy*, T é a coluna `tempo` e δ é a coluna `evento`.

**Censura à direita.** Sabe-se apenas que X_i > C_i: o processo ainda estava em curso na data de corte. Colosimo e Giolo (2006, p. 8-11) distinguem três mecanismos:

- **tipo I**: o estudo termina numa data fixa, e todos os não sentenciados são censurados nela;
- **tipo II**: o estudo termina quando se observa um número pré-fixado de eventos;
- **aleatória**: cada unidade tem o seu próprio tempo de censura, por exemplo porque **entrou no estudo em datas diferentes**.

Aqui a censura é **administrativa, do tipo I em calendário** (todos os ativos são censurados em 07/10/2026), mas como a distribuição se estendeu de 01/01 a 03/08/2026 (**entrada escalonada**), na escala do tempo de processo cada unidade tem um tempo potencial de censura diferente: C_i = 07/10/2026 − data de distribuição, de 65 a 279 dias (coluna `followup`). É o caso da figura 1.1 de Colosimo e Giolo (2006, p. 9): na escala do processo, a censura comporta-se como **aleatória**.

**Funções básicas** (COLOSIMO; GIOLO, 2006, p. 18-25):

- função de sobrevivência S(t) = P(X > t): proporção ainda sem sentença após t dias;
- função de risco (*hazard*) h(t) = lim P(t ≤ X < t + Δt | X ≥ t)/Δt: "taxa instantânea de sentenças" entre os processos que ainda estão pendentes no dia t. Não é uma probabilidade, e sim uma taxa por dia;
- risco acumulado Λ(t) = ∫₀ᵗ h(u) du, com S(t) = exp{−Λ(t)}.

**A hipótese de censura não informativa (independente).** Todos os estimadores e testes desta parte supõem que, condicionalmente às covariáveis, o fato de um processo estar censurado não informa sobre o seu tempo restante. Ela é **plausível para a censura administrativa** deste estudo: um processo está ativo em 07/10 porque foi distribuído tarde (data fixada pelo calendário) e não porque seja mais ou menos "difícil". Há duas ressalvas:

1. **Tendência de calendário.** O tempo potencial de censura depende do mês de distribuição. Se o ritmo da vara mudou ao longo de 2026 (férias, pauta de audiências, curva de aprendizado do novo rito), a censura fica associada ao prognóstico pelo calendário. A solução é **condicionar no mês** (estrato ou covariável), como fazem as seções 4.3.4 e 4.5.
2. **Redistribuição não é censura.** Os 24 processos "Decisão" foram remetidos a outro juízo e **nunca** terão sentença no 4º JEC: o evento passou a ser impossível, o que é bem diferente de "ainda não ocorreu". Isso é um **risco competitivo** (PUTTER; FIOCCO; GESKUS, 2007). Tratá-los como censura supõe que eles teriam o mesmo risco de sentença dos que ficaram, e o 1 − KM então superestima a probabilidade acumulada de sentença. Na análise principal (seções 4.2 a 4.6) a redistribuição é censurada em T (é o padrão da literatura para a pergunta "taxa de sentença enquanto o processo está no juízo"); a seção 4.7 a trata como risco competitivo e mostra que, com só 24 casos e quase todos em 0 a 8 dias, o viés é pequeno.

### 4.1.2 Preparação da base de sobrevivência

A célula abaixo cria as colunas numéricas que o `lifelines` e o `statsmodels` exigem (as colunas `Int64`/`boolean` da base *tidy* são convertidas para `float`/`int`) e as variáveis indicadoras do modelo:

- `Presencial`, `Remota`: indicadoras de grupo (referência = Controle);
- `mes`: mês de distribuição, com **agosto unido a julho** (agosto tem só 6 processos e seguimento de 65 dias; um estrato com 1 processo por grupo não teria informação);
- `origem_ext`: processo recebido de outro órgão (12 casos; A9).

Também são definidas funções auxiliares usadas em toda a Parte IV: um Kaplan-Meier/Aalen-Johansen vetorizado na grade de dias inteiros (para *bootstrap* e testes de permutação rápidos), a tabela de razões de risco e o gráfico de floresta. As figuras e tabelas usam a camada de visualização da seção 1.2 (`figura`, `tabela`, `plot_km`).

> **Nota técnica.** A função `lifelines.plotting.add_at_risk_counts` falha com o pandas 3.0.5 deste ambiente (`TypeError: only 0-dimensional arrays...`). A tabela de número em risco sob as curvas de Kaplan-Meier é, por isso, desenhada pela função `plot_km` da seção 1.2, que reproduz a mesma convenção do `lifelines` (em risco em t = processos com T ≥ t).
''')

code(r'''
from lifelines import NelsonAalenFitter, CoxTimeVaryingFitter, WeibullAFTFitter, LogNormalAFTFitter, LogLogisticAFTFitter
from lifelines.statistics import survival_difference_at_fixed_point_in_time_test, proportional_hazard_test
from lifelines.utils import median_survival_times, restricted_mean_survival_time
from statsmodels.duration.survfunc import survdiff, CumIncidenceRight
from statsmodels.stats.multitest import multipletests
from statsmodels.nonparametric.smoothers_lowess import lowess
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

if 'dados' not in globals():
    dados = pd.read_pickle(PROC / 'ed2_tidy.pkl')

MESES_SOB = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul-ago']
COLS_MES = ['mes_fev', 'mes_mar', 'mes_abr', 'mes_mai', 'mes_jun', 'mes_julago']
CAUSAS = {1: 'Homologação', 2: 'Mérito', 3: 'Sem mérito', 4: 'Redistribuição'}
ROTULO_TERMO = {'Presencial': 'AC presencial × Controle', 'Remota': 'AC remota × Controle',
                'origem_ext': 'Origem externa × 4º JEC',
                **{c: f'{m} × jan' for c, m in zip(COLS_MES, MESES_SOB[1:])}}
H_MAX = 280            # grade de dias inteiros 0..H_MAX (tempo máximo observado = 274)
TEMPOS_TAB = [0, 30, 60, 90, 120, 150, 180, 210, 240, 270]


def preparar_sob(df):
    """Base de sobrevivência com colunas numéricas e indicadoras (ver 4.1.2)."""
    s = df.copy()
    s['grupo'] = pd.Categorical(s['grupo'].astype(str), categories=ORDEM_GRUPO)
    s['T'] = s['tempo'].astype(float)
    s['T_pos'] = s['tempo_pos'].astype(float)
    s['E'] = s['evento'].astype(int)
    s['CR'] = s['evento_cr'].astype(int)
    s['K'] = s['causa'].astype(int)
    s['FU'] = s['followup'].astype(float)
    s['Presencial'] = (s['grupo'] == 'Presencial').astype(int)
    s['Remota'] = (s['grupo'] == 'Remota').astype(int)
    mes = s['mes_distribuicao'].astype(str).replace({'jul': 'jul-ago', 'ago': 'jul-ago'})
    s['mes'] = pd.Categorical(mes, categories=MESES_SOB)
    for c, m in zip(COLS_MES, MESES_SOB[1:]):
        s[c] = (s['mes'] == m).astype(int)
    s['mes_cod'] = s['mes'].cat.codes.astype(int)
    s['origem_ext'] = s['origem_externa'].astype(int)
    s['ordem'] = s['ordem_chegada'].astype(float)
    return s


sob = preparar_sob(dados)


# ---------------------------------------------------------------- estimadores vetorizados (grade diária)
def aj_grade(T, K, causas=(1,), H=H_MAX):
    """Kaplan-Meier global S(t) e incidências acumuladas de Aalen-Johansen F_k(t) em t = 0..H.
    T: tempos inteiros; K: código do desfecho (0 = censura). Com uma só causa (K = evento), 1 − S = F."""
    T = np.asarray(T, dtype=int)
    K = np.asarray(K, dtype=int)
    n_sai = np.bincount(T, minlength=H + 1)[:H + 1]
    risco = len(T) - np.concatenate([[0], np.cumsum(n_sai)[:-1]])          # n(t) = #{T >= t}
    d = {k: np.bincount(T[K == k], minlength=H + 1)[:H + 1] for k in causas}
    d_tot = np.sum([d[k] for k in causas], axis=0)
    with np.errstate(divide='ignore', invalid='ignore'):
        haz = np.where(risco > 0, d_tot / risco, 0.0)
        S = np.cumprod(1 - haz)
        S_ant = np.concatenate([[1.0], S[:-1]])
        cif = {k: np.cumsum(S_ant * np.where(risco > 0, d[k] / risco, 0.0)) for k in causas}
    return S, cif


def rmst_grade(T, E, tau):
    """RMST = ∫_0^tau S(t) dt para S em degraus nos dias inteiros."""
    S, _ = aj_grade(T, E)
    return S[:tau].sum()


def km_greenwood(T, E, t0):
    """Ŝ(t0) de Kaplan-Meier e erro-padrão de Greenwood (COLOSIMO; GIOLO, 2006, eq. 2.7)."""
    T = np.asarray(T, float); E = np.asarray(E, int)
    tempos = np.unique(T[(E == 1) & (T <= t0)])
    S, soma = 1.0, 0.0
    for t in tempos:
        n = (T >= t).sum(); d = ((T == t) & (E == 1)).sum()
        S *= 1 - d / n
        soma += d / (n * (n - d)) if n > d else 0.0
    return S, S * np.sqrt(soma)


def quantil_tempo(serie, p):
    """Primeiro t com S(t) <= p (inf se não atingido) — a convenção do lifelines."""
    abaixo = serie[serie <= p]
    return float(abaixo.index[0]) if len(abaixo) else np.inf


# ---------------------------------------------------------------- gráficos e tabelas
def tabela_hr(modelo, termos=None, rotulo='HR'):
    """Razões de risco (ou de tempos) com IC 95% e p-valor de Wald, a partir de um fitter do lifelines."""
    s = modelo.summary.copy()
    if isinstance(s.index, pd.MultiIndex):
        s = s.loc[s.index.get_level_values(0)[0]]
    if termos is not None:
        s = s.loc[[t for t in termos if t in s.index]]
    return pd.DataFrame({rotulo: s['exp(coef)'].values, 'IC 95% inf.': s['exp(coef) lower 95%'].values,
                         'IC 95% sup.': s['exp(coef) upper 95%'].values, 'p (Wald)': s['p'].values},
                        index=[ROTULO_TERMO.get(t, t) for t in s.index])


def floresta(ax, tab, rotulo='HR', cores=None, titulo='', col_p='p (Wald)', cor_de=None, xlabel=None, ticks=None,
             marcadores=None):
    """Gráfico de floresta (escala log) para uma tabela no formato de tabela_hr.

    Cada linha traz, à direita do IC, a estimativa (IC 95%) e o valor-p de Wald. `cor_de` = função nome -> cor
    (padrão: `cores[nome]`); `marcadores` = função nome -> marcador."""
    y = np.arange(len(tab))[::-1]
    for yi, (nome, r) in zip(y, tab.iterrows()):
        cor = cor_de(nome) if cor_de else (cores or {}).get(nome, TINTA)
        mk = marcadores(nome) if marcadores else 'o'
        ax.errorbar(r[rotulo], yi, xerr=[[r[rotulo] - r['IC 95% inf.']], [r['IC 95% sup.'] - r[rotulo]]],
                    fmt=mk, color=cor, capsize=3, ms=6)
        txt = f"{fmt_br(r[rotulo], 2)} [{fmt_br(r['IC 95% inf.'], 2)}; {fmt_br(r['IC 95% sup.'], 2)}]"
        if col_p and col_p in r.index:
            txt += f"; p {'< 0,001' if r[col_p] < 0.001 else '= ' + fmt_p(r[col_p])}"
        ax.annotate(txt, (r['IC 95% sup.'], yi), xytext=(6, 0), textcoords='offset points', va='center',
                    fontsize=8.5, color=TINTA_2, bbox=CAIXA_TXT)
    ax.axvline(1, color=TINTA_2, ls='--', lw=1)
    ax.set_xscale('log')
    ax.set_yticks(y, tab.index)
    ax.set_ylim(-0.6, len(tab) - 0.4)
    ax.grid(axis='y', visible=False)
    ax.grid(axis='x', visible=True)
    ax.set_xlabel(xlabel or rotulo + ' vs. Controle (IC 95%; escala log)')
    if titulo:
        ax.set_title(titulo)
    if ticks is not None:
        ax.set_xticks(ticks)
    ax.xaxis.set_major_formatter(mpl.ticker.FuncFormatter(lambda v, _: fmt_br(v, 2)))
    ax.xaxis.set_minor_formatter(mpl.ticker.NullFormatter())


def sob_tabela(df, id, titulo, secao, casas=3, colunas_p=(), destaque='auto', formatos=None, nota=None, **kw):
    """tabela() da Parte IV: colunas de valor-p em pt-BR e linhas com p < 0,05 em destaque."""
    fmts = {c: 'p' for c in colunas_p if c in df.columns}
    fmts.update(formatos or {})
    if destaque == 'auto':
        destaque = next((c for c in ('p (Holm, 7 testes)', 'p (Holm, 6 testes)', 'p (Holm, 4 testes)', 'p (Holm)',
                                     'p (Wald)', 'p') if c in df.columns), None)
    tabela(df, id, titulo, secao=secao, casas=casas, formatos=fmts, destaque=destaque, nota=nota, **kw)


def p_txt(p):
    """'p < 0,001' ou 'p = 0,034' (para rótulos dentro dos gráficos)."""
    return 'p < 0,001' if p < 0.001 else f'p = {fmt_p(p)}'


CAIXA_TXT = dict(boxstyle='square,pad=0.15', fc='white', ec='none', alpha=0.85)   # fundo de rótulos sobre linhas
COR_TERMO = {'AC presencial × Controle': CORES_GRUPO['Presencial'], 'AC remota × Controle': CORES_GRUPO['Remota']}
GRUPO_TERMO = {'AC presencial × Controle': 'Presencial', 'AC remota × Controle': 'Remota'}
LEG_GRUPO = lambda ordem=ORDEM_GRUPO, longo=False: [Line2D([], [], color=CORES_GRUPO[g], lw=2.2,
                                                           label=ROTULO_GRUPO[g] if longo else g) for g in ordem]

print(f'Base de sobrevivência: {len(sob)} processos | sentenças (δ = 1): {sob.E.sum()} | '
      f'censurados: {(sob.E == 0).sum()} (ativos {(sob.CR == 0).sum()} + redistribuídos {(sob.CR == 2).sum()})')
print('Conferência do estimador vetorizado contra o lifelines (Ŝ em 30/90/180 dias, Controle):')
_c = sob[sob.grupo == 'Controle']
_S, _ = aj_grade(_c['T'], _c['E'])
_k = KaplanMeierFitter().fit(_c['T'], _c['E'])
print('  grade  :', np.round(_S[[30, 90, 180]], 4), '\n  lifelines:', np.round(_k.survival_function_at_times([30, 90, 180]).values, 4))
''')

md(r'''
### 4.1.3 Entrada escalonada e censura administrativa: o diagrama de seguimento

O gráfico abaixo mostra 45 processos sorteados (15 por grupo) em duas escalas. À esquerda, na **escala de calendário**, cada linha vai da distribuição ao desfecho: todas as censuras (círculos vazios) ocorrem na mesma data, 07/10/2026 (censura tipo I). À direita, na **escala do processo** (dias desde a distribuição), todas as linhas começam em zero e as censuras se espalham entre 65 e 279 dias: os processos distribuídos mais tarde têm seguimento mais curto. É por isso que um "tempo médio" calculado tratando os ativos como encerrados (E14) é viesado para baixo, e que o mês de distribuição precisa entrar nos modelos.
''')

code(r'''
_rng = np.random.default_rng(SEMENTE + 4)
amostra = (pd.concat([sob[sob.grupo == g].iloc[_rng.choice((sob.grupo == g).sum(), 15, replace=False)] for g in ORDEM_GRUPO])
           .sort_values('dt_distribuicao').reset_index(drop=True))
fim = amostra['dt_sentenca'].where(amostra['CR'] > 0, DATA_CORTE)
MARCA = {0: dict(marker='o', mfc='white'), 1: dict(marker='o'), 2: dict(marker='X')}

fig, axes = plt.subplots(1, 2, figsize=(13, 7), sharey=True)
for i, r in amostra.iterrows():
    cor = CORES_GRUPO[r['grupo']]
    axes[0].plot([r['dt_distribuicao'], fim[i]], [i, i], color=cor, lw=1.6)
    axes[0].plot(fim[i], i, color=cor, ms=6, ls='', **MARCA[r['CR']])
    axes[1].plot([0, r['T']], [i, i], color=cor, lw=1.6)
    axes[1].plot(r['T'], i, color=cor, ms=6, ls='', **MARCA[r['CR']])
axes[0].axvline(DATA_CORTE, color=DESTAQUE, ls='--', lw=1.2); axes[0].axvline(FIM_RECRUTAMENTO, color=TINTA_2, ls=':', lw=1.2)
axes[0].text(DATA_CORTE, len(amostra) + 0.3, 'corte\n07/10 ', fontsize=8.5, color=DESTAQUE, ha='right', va='bottom')
axes[0].text(FIM_RECRUTAMENTO, len(amostra) + 0.3, 'último sorteio\n03/08 ', fontsize=8.5, color=TINTA_2, ha='right', va='bottom')
axes[0].set_ylim(-1, len(amostra) + 3)
axes[0].set_title('Escala de calendário: censura tipo I (data fixa)')
eixo_meses(axes[0])
axes[0].set_xlabel(ROTULOS['dt_distribuicao'] + ' → desfecho ou corte')
axes[1].set_title('Escala do processo: entrada escalonada, censuras dispersas')
axes[1].set_xlabel(ROTULOS['dias'])
axes[1].set_xticks(np.arange(0, 281, 30))
axes[0].set_yticks([]); axes[0].set_ylabel('Processos sorteados (ordenados pela data de distribuição)')
for ax in axes:
    ax.grid(axis='y', visible=False); ax.grid(axis='x', visible=True)
leg = LEG_GRUPO(longo=True) + [
    Line2D([], [], color=TINTA, marker='o', ls='', label='Sentença'),
    Line2D([], [], color=TINTA, marker='o', mfc='white', ls='', label='Censurado (ativo em 07/10)'),
    Line2D([], [], color=TINTA, marker='X', ls='', label='Redistribuído')]
fig.legend(handles=leg, loc='upper center', ncol=3, bbox_to_anchor=(0.5, 0.0))
figura(fig, 'sob_diagrama_seguimento',
       'Na escala do processo, a censura administrativa de uma data fixa vira censura dispersa entre 65 e 279 dias',
       secao='4.1.3', nota='45 processos sorteados (15 por grupo; semente fixa). Linha = período observado; '
                           'círculo cheio = sentença; círculo vazio = ativo em 07/10/2026 (censurado); X = redistribuição.')
''')

md(r'''
### 4.1.4 Estrutura dos dados por grupo

A tabela resume, por grupo, o que cada processo contribui: sentença (evento), censura administrativa (ativo) ou redistribuição. O **seguimento potencial** é o tempo máximo que cada processo poderia ter sido observado (07/10/2026 − distribuição). O seguimento mediano pelo **KM reverso** (KM com a censura como "evento") é a forma usual de resumir o acompanhamento quando o tempo potencial de censura é desconhecido. Aqui ele é **conhecido exatamente** para todos os processos (07/10/2026 − distribuição), e o seguimento potencial é o resumo preferível; o KM reverso fica na tabela só como conferência.

O gráfico de barras mostra a **proporção censurada por mês de distribuição e grupo**. Ela cresce fortemente com o mês: é a assinatura da entrada escalonada. Se um grupo tivesse mais processos nos meses tardios (julho concentra a Remota: 67 processos, contra 44 na Presencial e 46 no Controle; junho concentra a Presencial: 59, contra 39 no Controle e 34 na Remota), ele teria mais censura por puro calendário, o que é mais um motivo para o ajuste por mês.
''')

code(r'''
def resumo_estrutura(s):
    kmr = KaplanMeierFitter().fit(s['T'], 1 - s['E'])        # KM reverso (censura como "evento")
    return pd.Series({'n': len(s), 'Sentenças (δ = 1)': int(s['E'].sum()),
                      'Ativos (censura adm.)': int((s['CR'] == 0).sum()),
                      'Redistribuídos': int((s['CR'] == 2).sum()),
                      '% censurado': pct_br(1 - s['E'].mean()),
                      'Seguimento potencial mediano (d)': fmt_br(s['FU'].median(), 0),
                      'Seguimento potencial mín.–máx.': f"{int(s['FU'].min())}–{int(s['FU'].max())}",
                      'Seguimento mediano, KM reverso (d)': fmt_br(kmr.median_survival_time_, 0)})

estrutura = pd.concat({g: resumo_estrutura(sob[sob.grupo == g]) for g in ORDEM_GRUPO} | {'Total': resumo_estrutura(sob)}, axis=1)
tabela(estrutura.rename_axis('Medida'), 'sob_estrutura', 'Contribuição de cada processo à análise: sentença, censura ou redistribuição',
       secao='4.1.4', nota='seguimento potencial = 07/10/2026 − data de distribuição; KM reverso = Kaplan-Meier com a censura '
                           'como "evento".')

cens_mes = (sob.assign(cens=1 - sob['E']).groupby(['mes', 'grupo'], observed=True)['cens'].mean().unstack() * 100)
n_mes = sob.groupby('mes', observed=True).size()
_cm = cens_mes.copy()
_cm.columns = [str(c) for c in _cm.columns]
_cm.index = [f'{m}\n(n = {fmt_br(n_mes[m], 0)})' for m in _cm.index]
fig, ax = plt.subplots(figsize=(10, 4.6))
barras_agrupadas(ax, _cm, cores=CORES_GRUPO, rotular=False, quebrar=20,
                 ylabel='Processos sem sentença em 07/10 (%)', xlabel='Mês de distribuição (2026; julho e agosto unidos)',
                 legenda=False)
eixo_pct(ax, escala=1)
ax.set_ylim(0, 105)
ax.set_title('Proporção censurada por mês de distribuição e grupo')
legenda_abaixo(ax, ncol=3, dy=-0.25, handles=[Patch(color=CORES_GRUPO[g], label=ROTULO_GRUPO[g]) for g in ORDEM_GRUPO])
figura(fig, 'sob_censura_mes', 'A censura cresce com o mês de distribuição: é a assinatura da entrada escalonada',
       secao='4.1.4', nota='censurado = sem sentença em 07/10/2026 (ativo ou redistribuído); n = processos distribuídos no mês.')
''')

md(r'''
### 4.1.5 Tabela de vida: número em risco, eventos e censuras por intervalo

A tabela de vida (atuarial) por intervalos de 30 dias é a forma mais transparente de ver de onde vem a informação: **n em risco** no início do intervalo, **sentenças** e **censuras** dentro dele. Note que, a partir de ~180 dias, o número em risco cai rapidamente, e a censura passa a dominar: as estimativas da cauda direita (> 180 dias) são imprecisas, o que orienta a escolha do horizonte τ do RMST (seção 4.3.6).
''')

code(r'''
def tabela_vida(s, cortes=TEMPOS_TAB):
    linhas = []
    for a, b in zip(cortes, cortes[1:] + [np.inf]):
        no_int = (s['T'] >= a) & (s['T'] < b)
        linhas.append({'intervalo (d)': f'[{a}, {b})' if np.isfinite(b) else f'≥ {a}',
                       'em risco': int((s['T'] >= a).sum()),
                       'sentenças': int((no_int & (s['E'] == 1)).sum()),
                       'censuras': int((no_int & (s['E'] == 0)).sum())})
    return pd.DataFrame(linhas).set_index('intervalo (d)')

vida = pd.concat({g: tabela_vida(sob[sob.grupo == g]) for g in ORDEM_GRUPO}, axis=1)
tabela(vida.rename_axis('Intervalo (dias)'), 'sob_tabela_vida', 'Tabela de vida por grupo: em risco no início, sentenças e censuras '
       'em cada intervalo de 30 dias', secao='4.1.5', indice=True,
       nota='em risco = processos com T ≥ início do intervalo; censuras = ativos em 07/10/2026 ou redistribuídos.')
''')

interp('sob_estrutura')

# =====================================================================
md(r'''
---

## 4.2 Estimação não paramétrica: Kaplan-Meier e Nelson-Aalen

### 4.2.1 O estimador de Kaplan-Meier

O estimador de Kaplan-Meier (KAPLAN; MEIER, 1958) é o produto, sobre os tempos de evento t_j < t, das probabilidades condicionais de "sobreviver" (continuar sem sentença) a cada t_j:

Ŝ(t) = ∏_{j: t_j ≤ t} (1 − d_j / n_j),

em que d_j é o número de sentenças no dia t_j e n_j é o número em risco (ainda pendentes e não censurados) imediatamente antes de t_j (COLOSIMO; GIOLO, 2006, eq. 2.6, p. 37; MORETTIN; SINGER, 2021, p. 247-248). Cada censurado contribui para os denominadores enquanto está em observação, e depois sai do risco: é assim que o KM usa a informação parcial que a média ingênua desperdiça.

- **Variância de Greenwood:** Var[Ŝ(t)] = Ŝ(t)² Σ d_j/[n_j(n_j − d_j)] (eq. 2.7, p. 41).
- **IC 95% log-log** ("Greenwood exponencial"): o IC simples Ŝ ± 1,96·EP pode sair de [0, 1] nos extremos; a transformação Û = log[−log Ŝ(t)] produz [Ŝ(t)]^{exp(±1,96·√Var Û)}, sempre dentro de [0, 1] (eq. 2.8, p. 41-42). É o padrão do `lifelines`.
- **Propriedades:** não viciado em amostras grandes, consistente, assintoticamente normal e estimador de máxima verossimilhança não paramétrico (p. 40).

Como pedido, a curva é sempre a **descendente** S(t). As marcas verticais (|) são as censuras; a tabela sob o gráfico dá o número em risco.
''')

code(r'''
km_total = KaplanMeierFitter(label='Todos os processos').fit(sob['T'], sob['E'])
med_ic = median_survival_times(km_total.confidence_interval_)
print(f'Mediana global: {fmt_br(km_total.median_survival_time_, 0)} dias '
      f'(IC 95%: {fmt_br(med_ic.iloc[0, 0], 0)}–{fmt_br(med_ic.iloc[0, 1], 0)})')

fig, ax = plt.subplots(figsize=(10, 5.2))
plot_km(ax, sob, tempo='T', evento='E', grupo=None, passo=30, rotulos={'Todos': 'Todos os processos'})
ax.axhline(0.5, color=TINTA_2, ls=':', lw=1)
eixo_pct(ax)
ax.set_title('Kaplan-Meier global, S(t) com IC 95% log-log')
figura(fig, 'sob_km_global',
       f'Metade dos processos recebe sentença em até {fmt_br(km_total.median_survival_time_, 0)} dias '
       f'(IC 95%: {fmt_br(med_ic.iloc[0, 0], 0)}–{fmt_br(med_ic.iloc[0, 1], 0)})',
       secao='4.2.1', nota='faixa = IC 95% (Greenwood, transformação log-log); | = censura; linha pontilhada = 50%. '
                           'Redistribuições censuradas no seu tempo.')
''')

md(r'''
### 4.2.2 Kaplan-Meier por grupo

As três curvas com IC 95% (faixas) e marcas de censura. Leitura: a curva mais **alta** em um dado t é a do grupo com mais processos **ainda pendentes** nesse dia, ou seja, o rito mais lento até ali. A distância vertical entre as curvas em t é a diferença na proporção já sentenciada; a distância horizontal na altura 50% é a diferença de medianas.
''')

code(r'''
km_g = {g: KaplanMeierFitter(label=ROTULO_GRUPO[g]).fit(sob.loc[sob.grupo == g, 'T'], sob.loc[sob.grupo == g, 'E'])
        for g in ORDEM_GRUPO}
fig, ax = plt.subplots(figsize=(10.5, 5.8))
plot_km(ax, sob, tempo='T', evento='E', grupo='grupo', passo=30)
ax.axhline(0.5, color=TINTA_2, ls=':', lw=1)
eixo_pct(ax)
ax.set_title('Kaplan-Meier por grupo, S(t) com IC 95% log-log')
_md = {g: km_g[g].median_survival_time_ for g in ORDEM_GRUPO}
figura(fig, 'sob_km_grupos',
       f'Os grupos com AC obrigatória ficam mais tempo sem sentença: medianas de {fmt_br(_md["Controle"], 0)} dias no Controle, '
       f'{fmt_br(_md["Presencial"], 0)} na AC presencial e {fmt_br(_md["Remota"], 0)} na AC remota',
       secao='4.2.2', nota='curva mais alta = mais processos ainda pendentes (rito mais lento até ali). Faixas = IC 95% '
                           '(Greenwood, log-log); | = censura; linha pontilhada = 50%.')
''')

md(r'''
### 4.2.3 Mediana e quartis com IC 95%

A mediana é t̂₀,₅ = inf{t: Ŝ(t) ≤ 0,5} (MORETTIN; SINGER, 2021, p. 248). Os quartis seguem a mesma regra: o **1º quartil** (Q1) é o dia em que 25% dos processos já tiveram sentença (Ŝ ≤ 0,75) e o **3º quartil** (Q3), o dia em que 75% já tiveram (Ŝ ≤ 0,25). A variância da mediana depende da densidade f(t), desconhecida; o IC é obtido **invertendo as bandas** de confiança de Ŝ (o tempo em que cada limite do IC cruza o nível p), procedimento próximo ao de Brookmeyer e Crowley (1982) descrito por Colosimo e Giolo (2006, p. 49-50). É o que faz `median_survival_times(kmf.confidence_interval_)`.

O **tempo médio** ∫S(t)dt não é estimável: com censura na cauda, a média fica subestimada e "deve ser interpretada com cautela ou evitada" (COLOSIMO; GIOLO, 2006, p. 50). O substituto é o RMST (seção 4.3.6).
''')

code(r'''
def quantis_km(kmf):
    ic = kmf.confidence_interval_
    linha = {}
    for nome, p in [('Q1 (25% sentenciados)', 0.75), ('Mediana', 0.5), ('Q3 (75% sentenciados)', 0.25)]:
        est = quantil_tempo(kmf.survival_function_.iloc[:, 0], p)
        inf = quantil_tempo(ic.iloc[:, 0], p)       # limite inferior de S cruza antes
        sup = quantil_tempo(ic.iloc[:, 1], p)
        linha[nome] = f'{fmt_br(est, 0)} ({fmt_br(inf, 0)}–{fmt_br(sup, 0) if np.isfinite(sup) else "∞"})'
    return pd.Series(linha)

quartis = pd.DataFrame({ROTULO_GRUPO[g]: quantis_km(km_g[g]) for g in ORDEM_GRUPO} | {'Todos': quantis_km(km_total)}).T
tabela(quartis.rename_axis('Grupo'), 'sob_quartis', 'Dias até a sentença: quartis de Kaplan-Meier, estimativa (IC 95%)',
       secao='4.2.3', formatos={c: 'texto' for c in quartis.columns},
       nota='IC por inversão das bandas log-log de Ŝ(t); ∞ = o limite do IC não cruza o nível dentro do seguimento.')
MEDIANAS = {g: km_g[g].median_survival_time_ for g in ORDEM_GRUPO}
''')

md(r'''
### 4.2.4 Ŝ(t) em horizontes fixos de gestão

Para o gestor, a pergunta natural é "que fração dos processos ainda está sem sentença depois de 1, 2, 3, 4 e 6 meses?". A tabela traz Ŝ(t) com IC 95% log-log em 30, 60, 90, 120 e 180 dias; o gráfico mostra as mesmas estimativas em barras verticais com o IC. Os testes formais de diferença nesses pontos estão na seção 4.3.5.
''')

code(r'''
HORIZONTES = [30, 60, 90, 120, 180]
linhas = []
for g in ORDEM_GRUPO:
    k = km_g[g]
    S = k.survival_function_at_times(HORIZONTES).values
    ic = k.confidence_interval_
    for t, s_t in zip(HORIZONTES, S):
        li = ic.iloc[:, 0][ic.index <= t].iloc[-1]; ls = ic.iloc[:, 1][ic.index <= t].iloc[-1]
        linhas.append({'grupo': g, 't': t, 'S': s_t, 'inf': li, 'sup': ls, 'em risco': int((sob.loc[sob.grupo == g, 'T'] >= t).sum())})
s_horiz = pd.DataFrame(linhas)
tab = s_horiz.assign(txt=lambda d: [f'{pct_br(a)} ({pct_br(b)}–{pct_br(c)}) [n={n}]' for a, b, c, n in zip(d.S, d['inf'], d['sup'], d['em risco'])]
                     ).pivot(index='t', columns='grupo', values='txt')[ORDEM_GRUPO]
tab.index = [f'{t} dias' for t in tab.index]
tab.columns = [str(c) for c in tab.columns]
tabela(tab.rename_axis('Horizonte'), 'sob_S_horizontes', 'Proporção ainda sem sentença, Ŝ(t), em horizontes fixos: '
       'estimativa (IC 95%) [n em risco]', secao='4.2.4', formatos={c: 'texto' for c in tab.columns},
       nota='IC 95% log-log (Greenwood).')

_sh = s_horiz.pivot(index='t', columns='grupo', values='S')[ORDEM_GRUPO]
_sh.index = [f'{t} dias' for t in _sh.index]
_sh.columns = [str(c) for c in _sh.columns]
_erro = {g: (s_horiz.loc[s_horiz.grupo == g, 'inf'].to_numpy(), s_horiz.loc[s_horiz.grupo == g, 'sup'].to_numpy())
         for g in ORDEM_GRUPO}
fig, ax = plt.subplots(figsize=(10, 4.8))
barras_agrupadas(ax, _sh, cores=CORES_GRUPO, erro=_erro, legenda=False, ylabel='Ŝ(t): processos ainda sem sentença (IC 95%)',
                 xlabel='Dias desde a distribuição')
eixo_pct(ax); ax.set_ylim(0, 1)
for j, g in enumerate(ORDEM_GRUPO):         # rótulo só no horizonte de 90 dias (onde as curvas mais se separam)
    v = _sh.loc['90 dias', g]; hi = _erro[g][1][HORIZONTES.index(90)]
    ax.annotate(pct_br(v, 0), (HORIZONTES.index(90) + (j - 1) * 0.8 / 3, hi), xytext=(0, 3), textcoords='offset points',
                ha='center', va='bottom', fontsize=8.5, color=TINTA)
ax.set_title('Ŝ(t) por grupo em 30, 60, 90, 120 e 180 dias')
ax.legend(handles=[Patch(color=CORES_GRUPO[g], label=ROTULO_GRUPO[g]) for g in ORDEM_GRUPO], loc='upper right')
figura(fig, 'sob_S_horizontes', f'Aos 90 dias, {pct_br(_sh.loc["90 dias", "Presencial"], 0)} (presencial) e '
       f'{pct_br(_sh.loc["90 dias", "Remota"], 0)} (remota) dos processos com AC ainda estão sem sentença, '
       f'contra {pct_br(_sh.loc["90 dias", "Controle"], 0)} no Controle',
       secao='4.2.4', nota='barras = Ŝ(t) de Kaplan-Meier; traços = IC 95% log-log. Os testes formais nesses pontos estão na seção 4.3.5.')
''')

md(r'''
### 4.2.5 Nelson-Aalen e risco suavizado

O estimador de **Nelson-Aalen** do risco acumulado é Λ̃(t) = Σ_{t_j ≤ t} d_j/n_j, com variância de Aalen Σ d_j/n_j² (COLOSIMO; GIOLO, 2006, eq. 2.9-2.10, p. 43-44). Ele dá S̃(t) = exp{−Λ̃(t)} ≥ Ŝ(t) e serve sobretudo para ver a **forma do risco**: Λ(t) reto indica risco constante; côncavo, risco decrescente; convexo, crescente (p. 45; p. 96-99).

A **taxa de sentença por dia** h(t) é a derivada de Λ(t). Estima-se por suavização por núcleo (Ramlau-Hansen) dos incrementos d_j/n_j, com núcleo de Epanechnikov e banda de 20 dias (`NelsonAalenFitter.smoothed_hazard_`). A banda é uma escolha de compromisso: menor deixa a curva ruidosa, maior apaga a estrutura. A curva é cortada em 160 dias: o núcleo usa os dados de t − 20 a t + 20 dias, e depois de ~180 dias há menos de 10 processos em risco por grupo; perto desse limite a estimativa sofre o **efeito de borda** do núcleo e vira ruído (por isso não se interpreta a subida final de nenhuma curva). É a figura que mostra **quando** cada rito sentencia mais.
''')

code(r'''
na_g = {g: NelsonAalenFitter(label=ROTULO_GRUPO[g]).fit(sob.loc[sob.grupo == g, 'T'], sob.loc[sob.grupo == g, 'E'])
        for g in ORDEM_GRUPO}
BANDA = 20
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
for g in ORDEM_GRUPO:
    ch = na_g[g].cumulative_hazard_.iloc[:, 0]
    ci = na_g[g].confidence_interval_
    axes[0].step(ch.index, ch.values, where='post', color=CORES_GRUPO[g], lw=2, label=ROTULO_GRUPO[g])
    axes[0].fill_between(ci.index, ci.iloc[:, 0], ci.iloc[:, 1], step='post', color=CORES_GRUPO[g], alpha=0.13, lw=0)
    hz = na_g[g].smoothed_hazard_(bandwidth=BANDA)
    hz = hz[hz.index <= 160]
    axes[1].plot(hz.index, hz.iloc[:, 0], color=CORES_GRUPO[g], lw=2, label=ROTULO_GRUPO[g])
axes[0].set_xlim(0, 280); axes[0].set_xticks(np.arange(0, 281, 30))
axes[0].set_xlabel(ROTULOS['dias']); axes[0].set_ylabel('Risco acumulado Λ̃(t) (sentenças por processo)')
axes[0].set_title('Risco acumulado de Nelson-Aalen (IC 95%)')
axes[0].legend(loc='upper left')
axes[1].set_xlim(0, 160); axes[1].set_xticks(np.arange(0, 161, 30))
axes[1].set_xlabel(ROTULOS['dias']); axes[1].set_ylabel('Taxa de sentença h(t) (por processo pendente por dia)')
axes[1].set_title(f'Risco suavizado h(t) (Epanechnikov, banda de {BANDA} dias)')
for ax in axes:
    ax.grid(axis='both', visible=True)
figura(fig, 'sob_nelson_aalen_risco', 'O pico da taxa diária de sentenças chega mais tarde nos grupos com AC obrigatória',
       secao='4.2.5', nota=f'Nelson-Aalen com IC 95%; risco suavizado por núcleo de Epanechnikov (banda de {BANDA} dias), '
                           'cortado em 160 dias (a janela do núcleo chega a 180 dias, depois dos quais há menos de 10 processos em risco por grupo).')
''')

interp('sob_km')

# =====================================================================
md(r'''
---

## 4.3 Comparação das curvas de sobrevivência

**Hipóteses (para toda a família de testes de k amostras):**

- H₀: S_Controle(t) = S_Presencial(t) = S_Remota(t) para todo t (equivalentemente, mesmas funções de risco);
- H₁: ao menos uma curva difere em algum t.

**Por que testar.** O desenho é um experimento com sorteio: diferenças sistemáticas entre as curvas, além do acaso, são atribuíveis ao rito. Os grupos são **independentes** (processos distintos, alocação aleatória; questão 2.3), o que justifica testes de k amostras independentes. **Pré-especificação:** o teste principal é o **log-rank** de 3 grupos (2 g.l.); os testes ponderados, os pares, o estratificado, os pontos fixos e o RMST são análises de apoio, cada uma respondendo a uma pergunta mais específica.

### 4.3.1 Teste log-rank

O log-rank compara, em cada tempo de evento t_j, o número observado de sentenças em cada grupo com o esperado sob H₀ (w_gj = n_gj d_j/n_j) e soma as diferenças ao longo do tempo. Com r = 3 grupos, a estatística T = v′V⁻¹v tem distribuição χ² com r − 1 = 2 g.l. (COLOSIMO; GIOLO, 2006, eq. 2.12-2.13, p. 56-59; MORETTIN; SINGER, 2021, p. 253). Ele coincide com o teste escore do modelo de Cox com o grupo como covariável (COLOSIMO; GIOLO, 2006, p. 56) e é o **mais poderoso quando os riscos são proporcionais** (p. 55).

**Pressupostos:** censura não informativa (4.1.1) e independência entre processos. **Gráfico do teste:** barras de sentenças **observadas (O)** e **esperadas sob H₀ (E)** por grupo; O < E significa que o grupo sentenciou menos (foi mais lento) do que sentenciaria se não houvesse diferença.
''')

code(r'''
def obs_esperados(T, E, G, grupos=ORDEM_GRUPO):
    """Sentenças observadas e esperadas sob H0 (log-rank) por grupo."""
    T = np.asarray(T, float); E = np.asarray(E, int); G = np.asarray(G)
    tempos = np.unique(T[E == 1])
    n_tot = np.array([(T >= t).sum() for t in tempos]); d_tot = np.array([((T == t) & (E == 1)).sum() for t in tempos])
    res = {}
    for g in grupos:
        Tg = T[G == g]
        n_g = np.array([(Tg >= t).sum() for t in tempos])
        res[g] = {'Observadas (O)': int(E[G == g].sum()), 'Esperadas sob H₀ (E)': float((n_g * d_tot / n_tot).sum())}
    out = pd.DataFrame(res).T
    out['O/E'] = out.iloc[:, 0] / out.iloc[:, 1]
    return out

lr_global = multivariate_logrank_test(sob['T'], sob['grupo'].astype(str), sob['E'])
oe = obs_esperados(sob['T'], sob['E'], sob['grupo'].astype(str))
print(f"Log-rank (3 grupos): χ² = {fmt_br(lr_global.test_statistic, 2)}, g.l. = {lr_global.degrees_of_freedom}, p = {p_br(lr_global.p_value)}")
sob_tabela(oe.rename_axis('Grupo'), 'sob_logrank_oe', 'Log-rank de 3 grupos: sentenças observadas e esperadas sob H₀',
           secao='4.3.1', casas=2, destaque=None, formatos={'Observadas (O)': 'int'},
           nota=f'log-rank: χ² = {fmt_br(lr_global.test_statistic, 2)} ({lr_global.degrees_of_freedom} g.l.); '
                f'{p_txt(lr_global.p_value)}. O/E < 1 = menos sentenças que o esperado (grupo mais lento).')

fig, ax = plt.subplots(figsize=(8.5, 4.8))
x = np.arange(3)
ax.bar(x - 0.2, oe['Observadas (O)'], 0.4, color=[CORES_GRUPO[g] for g in ORDEM_GRUPO], edgecolor='white', lw=1)
ax.bar(x + 0.2, oe['Esperadas sob H₀ (E)'], 0.4, color='white', edgecolor=[CORES_GRUPO[g] for g in ORDEM_GRUPO],
       hatch='///', lw=1.4)
for xi, (o, e) in zip(x, oe.iloc[:, :2].values):
    ax.annotate(fmt_br(o, 0), (xi - 0.2, o), xytext=(0, 2), textcoords='offset points', ha='center', va='bottom', fontsize=8.5)
    ax.annotate(fmt_br(e, 1), (xi + 0.2, e), xytext=(0, 2), textcoords='offset points', ha='center', va='bottom', fontsize=8.5)
    ax.annotate(f'O/E = {fmt_br(o / e, 2)}', (xi, max(o, e)), xytext=(0, 16), textcoords='offset points', ha='center',
                va='bottom', fontsize=9, fontweight='bold', color=TINTA)
ax.set_xticks(x, [rotulo_grupo(g, com_n=True, base=sob, quebrar=True) for g in ORDEM_GRUPO])
ax.grid(axis='x', visible=False)
ax.set_ylabel('Número de sentenças'); ax.set_ylim(0, oe.iloc[:, :2].to_numpy().max() * 1.45)
ax.set_title('Sentenças observadas (O, cheias) e esperadas sob H₀ (E, hachuradas)')
ax.legend(handles=[Patch(facecolor=TINTA_2, label='Observadas (O)'),
                   Patch(facecolor='white', edgecolor=TINTA_2, hatch='///', label='Esperadas sob H₀ (E)')],
          loc='upper right')
anotar_teste(ax, texto_teste('Log-rank (3 grupos)', f'χ²({lr_global.degrees_of_freedom}) = {fmt_br(lr_global.test_statistic, 2)}',
                             lr_global.p_value), loc='upper left')
figura(fig, 'sob_logrank_oe', 'O Controle teve mais sentenças do que o esperado sob H₀, e os grupos com AC, menos',
       secao='4.3.1', nota='esperadas = Σ_t n_g(t)·d(t)/n(t), o número de sentenças que cada grupo teria se as três curvas fossem iguais.')
''')

md(r'''
### 4.3.2 A família ponderada: Wilcoxon, Tarone-Ware, Peto-Prentice e Fleming-Harrington

Todos os testes da família têm a forma S = [Σ u_j (d_gj − w_gj)]² / Σ u_j² V_gj, e diferem apenas no **peso u_j** dado a cada tempo de evento (COLOSIMO; GIOLO, 2006, eq. 2.14-2.15, p. 61-63):

| Teste | Peso u_j | Onde tem mais poder |
|---|---|---|
| Log-rank | 1 | diferenças constantes (riscos proporcionais) |
| Wilcoxon / Gehan-Breslow | n_j | diferenças **precoces**; mas depende do padrão de censura |
| Tarone-Ware | √n_j | meio-termo |
| Peto-Prentice | S̃(t_{j−1})·n_j/(n_j + 1), com S̃(t) = ∏(1 − d_j/(n_j + 1)) | precoces, sem depender da censura |
| Fleming-Harrington (p, q) | Ŝ(t_{j−1})^p [1 − Ŝ(t_{j−1})]^q | (1, 0) precoce; (0, 1) **tardia**; (1, 1) intermediária |

**Por que fazer todos.** Se o efeito do rito muda ao longo do tempo (por exemplo, a AC obrigatória acelera extinções e acordos no início e atrasa os julgamentos de mérito depois), as diferenças de sinais opostos se cancelam no log-rank e o teste perde poder (p. 62-63). Comparar testes com pesos precoces e tardios mostra **onde** está a diferença. Como a censura aqui varia entre grupos e meses, Colosimo e Giolo recomendam preferir Peto ou FH ao Gehan (p. 63). Os testes são **sensibilidade** do teste principal, não uma família para escolher o menor p. Em particular, o destaque dado adiante ao FH(1, 1) é uma leitura **a posteriori** (é o teste de maior χ²): ele indica *onde* está a diferença, mas a decisão inferencial continua sendo a do log-rank.

**Implementação.** A estatística de k amostras é calculada por uma função própria (`teste_k_ponderado`, fórmulas de Colosimo e Giolo), porque a opção `weightings='fleming-harrington'` do `lifelines` 0.30 falha com o pandas 3. A coluna "χ² lifelines" confere a implementação nos testes em que o `lifelines` funciona; a pequena diferença no Peto-Prentice vem da definição do peso (o `lifelines` usa S̃ no próprio t_j, e aqui se usa S̃(t_{j−1}), como no livro).

**Gráfico do teste:** à esquerda, os pesos relativos u(t)/max u(t) ao longo do tempo (onde cada teste "olha"); à direita, as estatísticas χ²₂ com o valor crítico de 5%.
''')

code(r'''
def teste_k_ponderado(T, E, G, peso='logrank', p=0, q=0, grupos=ORDEM_GRUPO):
    """Teste de k amostras da família ponderada (COLOSIMO; GIOLO, 2006, eq. 2.13-2.15): χ² = Z'V⁻¹Z, k − 1 g.l."""
    T = np.asarray(T, float); E = np.asarray(E, int); G = np.asarray(G)
    tj = np.unique(T[E == 1])
    n = np.array([(T >= t).sum() for t in tj]); d = np.array([((T == t) & (E == 1)).sum() for t in tj])
    S_km = np.cumprod(1 - d / n); S_km_ant = np.concatenate([[1.0], S_km[:-1]])
    S_peto_ant = np.concatenate([[1.0], np.cumprod(1 - d / (n + 1))[:-1]])
    u = {'logrank': np.ones_like(n, float), 'wilcoxon': n.astype(float), 'tarone-ware': np.sqrt(n),
         'peto': S_peto_ant * n / (n + 1), 'fh': S_km_ant ** p * (1 - S_km_ant) ** q}[peso]
    ng = np.array([[(T[G == g] >= t).sum() for t in tj] for g in grupos[:-1]])
    dg = np.array([[((T[G == g] == t) & (E[G == g] == 1)).sum() for t in tj] for g in grupos[:-1]])
    Z = (u * (dg - ng * d / n)).sum(axis=1)
    fator = np.where(n > 1, d * (n - d) / np.maximum(n - 1, 1), 0.0) * u ** 2
    V = np.empty((len(grupos) - 1,) * 2)
    for a in range(len(grupos) - 1):
        for b in range(len(grupos) - 1):
            V[a, b] = (fator * (ng[a] / n) * ((a == b) - ng[b] / n)).sum()
    chi = float(Z @ np.linalg.solve(V, Z))
    return chi, stats.chi2.sf(chi, len(grupos) - 1)

PONDERACOES = [('Log-rank', ('logrank', {}), {}), ('Wilcoxon (Gehan-Breslow)', ('wilcoxon', {}), {'weightings': 'wilcoxon'}),
               ('Tarone-Ware', ('tarone-ware', {}), {'weightings': 'tarone-ware'}), ('Peto-Prentice', ('peto', {}), {'weightings': 'peto'}),
               ('Fleming-Harrington (1, 0)', ('fh', {'p': 1, 'q': 0}), None),
               ('Fleming-Harrington (0, 1)', ('fh', {'p': 0, 'q': 1}), None),
               ('Fleming-Harrington (1, 1)', ('fh', {'p': 1, 'q': 1}), None)]
res_pond = []
Gs = sob['grupo'].astype(str)
for nome, (peso, kwp), kw_ll in PONDERACOES:
    chi, pv = teste_k_ponderado(sob['T'], sob['E'], Gs, peso, **kwp)
    chi_ll = multivariate_logrank_test(sob['T'], Gs, sob['E'], **kw_ll).test_statistic if kw_ll is not None else np.nan
    res_pond.append({'Teste': nome, 'χ² (2 g.l.)': chi, 'p': pv, 'χ² lifelines (conferência)': chi_ll})
res_pond = pd.DataFrame(res_pond).set_index('Teste')
res_pond['p (Holm, 7 testes)'] = multipletests(res_pond['p'], method='holm')[1]
sob_tabela(res_pond, 'sob_testes_ponderados', 'Família ponderada de testes de k amostras (3 grupos, 2 g.l.)', secao='4.3.2',
           casas=2, colunas_p=('p', 'p (Holm, 7 testes)'),
           nota='implementação própria (COLOSIMO; GIOLO, 2006, eq. 2.13-2.15); "χ² lifelines" confere os quatro testes em que o '
                'lifelines 0.30 funciona com o pandas 3 (– = não disponível). Destaque: p de Holm < 0,05.')
print('Fleming-Harrington: o lifelines 0.30 falha com o pandas 3 (ValueError de alinhamento); usa-se a implementação própria,'
      ' conferida contra o lifelines nos quatro testes em que ele funciona.')

# pesos ao longo do tempo (KM combinado)
S_comb, _ = aj_grade(sob['T'], sob['E'])
tt = np.arange(0, 241)
n_t = np.array([(sob['T'] >= t).sum() for t in tt]); S_ant = np.concatenate([[1.0], S_comb[:-1]])[tt]
pesos = {'Log-rank': np.ones_like(tt, float), 'Wilcoxon (Gehan-Breslow)': n_t, 'Tarone-Ware': np.sqrt(n_t),
         'Peto-Prentice': S_ant * n_t / (n_t + 1), 'Fleming-Harrington (1, 0)': S_ant,
         'Fleming-Harrington (0, 1)': 1 - S_ant, 'Fleming-Harrington (1, 1)': S_ant * (1 - S_ant)}
# cor = família do peso (Gehan/Tarone/Peto: azul-céu; Fleming-Harrington: vinho), estilo = variante; sem cores de grupo
ESTILO_TESTE = {'Log-rank': (TINTA, '-'), 'Wilcoxon (Gehan-Breslow)': ('#56B4E9', '-'), 'Tarone-Ware': ('#56B4E9', '--'),
                'Peto-Prentice': ('#56B4E9', ':'), 'Fleming-Harrington (1, 0)': ('#882255', '-'),
                'Fleming-Harrington (0, 1)': ('#882255', '--'), 'Fleming-Harrington (1, 1)': ('#882255', ':')}
fig, axes = plt.subplots(1, 2, figsize=(14, 5.2), gridspec_kw={'width_ratios': [1, 1.15]})
for nome, u in pesos.items():
    cor, ls = ESTILO_TESTE[nome]
    axes[0].plot(tt, u / u.max(), color=cor, ls=ls, lw=2.2, label=nome)
axes[0].set_xlabel(ROTULOS['dias']); axes[0].set_ylabel('Peso relativo u(t) / máx u(t)')
axes[0].set_xticks(np.arange(0, 241, 30)); axes[0].set_ylim(0, 1.08)
axes[0].set_title('Onde cada teste "olha": peso dado a cada tempo')
legenda_abaixo(axes[0], ncol=2, dy=-0.15, fontsize=8.5)
nomes = list(res_pond.index)
xb = np.arange(len(nomes))
cores_b = [ESTILO_TESTE[n][0] for n in nomes]
axes[1].bar(xb, res_pond['χ² (2 g.l.)'], color=cores_b, width=0.62, edgecolor='white')
crit = stats.chi2.ppf(0.95, 2)
axes[1].axhline(crit, color=DESTAQUE, ls='--', lw=1.3, label=f'Valor crítico χ²(2) a 5% = {fmt_br(crit, 2)}')
axes[1].legend(loc='upper left')
for xi, (c, p, ph) in zip(xb, res_pond[['χ² (2 g.l.)', 'p', 'p (Holm, 7 testes)']].values):
    axes[1].annotate(f'{fmt_br(c, 2)}\n{p_txt(p)}\nHolm {fmt_p(ph)}', (xi, c), xytext=(0, 3), textcoords='offset points',
                     ha='center', va='bottom', fontsize=8, color=TINTA)
axes[1].set_xticks(xb, [quebra(n.replace('Fleming-Harrington', 'Fleming-\nHarrington'), 12) for n in nomes], fontsize=8.5)
axes[1].grid(axis='x', visible=False)
axes[1].set_ylim(0, res_pond['χ² (2 g.l.)'].max() * 1.45)
axes[1].set_ylabel('Estatística χ² (2 g.l.)'); axes[1].set_title('Resultado de cada teste (H₀: três curvas iguais)')
figura(fig, 'sob_testes_ponderados', 'Só o FH(0, 1), que pesa a cauda, não rejeita H₀ a 5%; o FH(1, 1), que pesa o meio do seguimento, dá o maior χ² '
       '(leitura a posteriori: a diferença está no meio do período)',
       secao='4.3.2', nota='pesos calculados com o KM combinado dos três grupos. Holm sobre os 7 testes, que são análises de '
                           'sensibilidade do log-rank (não uma família para escolher o menor p).')
''')

md(r'''
### 4.3.3 Comparações par a par (Holm e Bonferroni)

Rejeitado (ou não) o teste global, interessa saber **quais pares** diferem: Presencial × Controle e Remota × Controle respondem à pergunta do efeito da AC obrigatória; Presencial × Remota, à pergunta da modalidade. São 3 testes log-rank de 2 grupos (1 g.l. cada). Colosimo e Giolo (2006, p. 59-61) usam Bonferroni (α/3 = 0,017); aqui reporta-se também **Holm**, que controla a mesma taxa de erro da família e é uniformemente mais poderoso. O gráfico mostra −log₁₀(p) de cada par, com as linhas de corte de 5% (sem correção) e de Bonferroni.

**Teste de tendência: não se aplica.** O teste de tendência do log-rank (Cox com escore ordinal) pressupõe uma **ordenação a priori** dos grupos (dose crescente, por exemplo). Controle, AC presencial e AC remota são categorias **nominais**: não há razão substantiva para supor que a remota esteja "entre" o controle e a presencial, ou além dela. Um teste de tendência aqui dependeria de uma ordenação arbitrária e não responderia a nenhuma pergunta do estudo. (Um teste de tendência faz sentido para o **mês** de distribuição, que é ordinal; isso é avaliado pelos resíduos martingal na seção 4.5.4.)
''')

code(r'''
PARES = [('Controle', 'Presencial'), ('Controle', 'Remota'), ('Presencial', 'Remota')]
res_par = []
for a, b in PARES:
    sa, sb = sob[sob.grupo == a], sob[sob.grupo == b]
    r = logrank_test(sa['T'], sb['T'], sa['E'], sb['E'])
    res_par.append({'Par': f'{b} × {a}', 'χ² (1 g.l.)': r.test_statistic, 'p': r.p_value})
res_par = pd.DataFrame(res_par).set_index('Par')
res_par['p (Bonferroni)'] = multipletests(res_par['p'], method='bonferroni')[1]
res_par['p (Holm)'] = multipletests(res_par['p'], method='holm')[1]
sob_tabela(res_par, 'sob_logrank_pares', 'Log-rank par a par (2 grupos, 1 g.l.), com correção de Bonferroni e de Holm',
           secao='4.3.3', casas=2, colunas_p=('p', 'p (Bonferroni)', 'p (Holm)'), nota='destaque: p de Holm < 0,05.')

fig, ax = plt.subplots(figsize=(8.5, 4.6))
cores_par = [CORES_GRUPO['Presencial'], CORES_GRUPO['Remota'], CINZA]
xp = np.arange(len(res_par))
ax.bar(xp, -np.log10(res_par['p']), color=cores_par, width=0.6, edgecolor='white')
ax.axhline(-np.log10(0.05), color=TINTA_2, ls=':', lw=1.3, label='p = 0,05 (sem correção)')
ax.axhline(-np.log10(0.05 / 3), color=DESTAQUE, ls='--', lw=1.3, label='Bonferroni (0,05/3)')
for i, (c, p, ph) in enumerate(res_par[['χ² (1 g.l.)', 'p', 'p (Holm)']].values):
    ax.annotate(f'χ²(1) = {fmt_br(c, 2)}\n{p_txt(p)}\nHolm {fmt_p(ph)}', (i, -np.log10(p)), xytext=(0, 3),
                textcoords='offset points', ha='center', va='bottom', fontsize=8.5, bbox=CAIXA_TXT)
ax.set_xticks(xp, res_par.index); ax.grid(axis='x', visible=False)
ax.set_ylabel('−log₁₀(p)  (maior = mais evidência contra H₀)'); ax.set_title('Log-rank de cada par de grupos')
ax.legend(loc='upper right')
ax.set_ylim(0, max(-np.log10(res_par['p'])) * 1.55 + 0.3)
figura(fig, 'sob_logrank_pares', 'Só a AC remota difere do Controle após a correção de Holm; as duas modalidades não diferem entre si',
       secao='4.3.3', nota='3 testes log-rank de 2 grupos; Holm e Bonferroni controlam a taxa de erro da família (α = 0,05).')
''')

md(r'''
### 4.3.4 Log-rank estratificado pelo mês de distribuição

O log-rank estratificado calcula O − E e a variância **dentro de cada mês** e só depois soma os estratos. Assim, compara cada grupo apenas com processos distribuídos no mesmo mês, com o mesmo seguimento potencial e o mesmo "momento" da vara. Isso neutraliza (i) a diferença de composição mensal dos grupos (julho com mais Remota) e (ii) qualquer tendência de calendário. Se o resultado estratificado for parecido com o não estratificado, o calendário não confunde a comparação — o esperado num experimento sorteado. O `lifelines` não oferece estratificação; usa-se `statsmodels.duration.survfunc.survdiff(..., strata=mês)`.

**Gráfico do teste:** Kaplan-Meier por grupo **dentro de cada mês** (os estratos que o teste combina).
''')

code(r'''
g_num = sob['grupo'].cat.codes.values
estr = []
for nome, kw in [('Log-rank', {}), ('Gehan-Breslow', {'weight_type': 'gb'}), ('Tarone-Ware', {'weight_type': 'tw'})]:
    chi_ne, p_ne = survdiff(sob['T'].values, sob['E'].values, g_num, **kw)
    chi_e, p_e = survdiff(sob['T'].values, sob['E'].values, g_num, strata=sob['mes_cod'].values, **kw)
    estr.append({'Teste': nome, 'χ² não estratificado': chi_ne, 'p não estratificado': p_ne,
                 'χ² estratificado por mês': chi_e, 'p estratificado por mês': p_e})
estr = pd.DataFrame(estr).set_index('Teste')
sob_tabela(estr, 'sob_logrank_estratificado', 'Testes de 3 grupos sem e com estratificação pelo mês de distribuição (2 g.l.)',
           secao='4.3.4', casas=2, colunas_p=('p não estratificado', 'p estratificado por mês'),
           destaque='p estratificado por mês', nota='statsmodels.duration.survfunc.survdiff; estratos = 7 meses (julho e agosto unidos).')
LR_ESTRAT_P = estr.loc['Log-rank', 'p estratificado por mês']
_ch_e = estr.loc['Log-rank', 'χ² estratificado por mês']

for parte, meses in [(1, MESES_SOB[:4]), (2, MESES_SOB[4:])]:
    fig, axes = plt.subplots(2, 2, figsize=(12, 8.6), sharex=True, sharey=True)
    for ax, m in zip(axes.flat, meses):
        sm_ = sob[sob.mes == m]
        plot_km(ax, sm_, tempo='T', evento='E', grupo='grupo', ic=False, tabela_risco=False, legenda=False,
                passo=60, tmax=275, xlabel=ROTULOS['dias'], ylabel='S(t): ainda sem sentença')
        eixo_pct(ax)
        ax.set_title(f'{m} (n = {len(sm_)}; seguimento ≥ {int(sm_.FU.min())} dias)')
        ax.label_outer()
    if len(meses) < 4:
        for ax in axes.flat[len(meses):]:
            ax.axis('off')
        axes.flat[-1].legend(handles=LEG_GRUPO(longo=True), loc='upper center', bbox_to_anchor=(0.5, 0.95))
        anotar_teste(axes.flat[-1], texto_teste('Log-rank estratificado por mês', f'χ²(2) = {fmt_br(_ch_e, 2)}', LR_ESTRAT_P,
                                                 extra='(combina os 7 meses)'), loc='center', tamanho=9.5)
        axes.flat[1].tick_params(labelbottom=True); axes.flat[1].set_xlabel(ROTULOS['dias'])
    else:
        axes.flat[0].legend(handles=LEG_GRUPO(), loc='upper right')
    titulo_mes = ('De janeiro a abril, a posição relativa das curvas varia de mês para mês: em janeiro o Controle é o mais '
                  'lento; em abril, o mais rápido' if parte == 1 else
                  f'De maio a agosto, com seguimento mais curto, as curvas são mais ruidosas; o log-rank estratificado '
                  f'combina todos os meses ({p_txt(LR_ESTRAT_P)})')
    figura(fig, f'sob_km_por_mes_{parte}', titulo_mes, secao='4.3.4',
           nota=f'Kaplan-Meier por grupo dentro de cada mês de distribuição ({"jan–abr" if parte == 1 else "mai–ago"}; '
                'julho e agosto unidos); | = censura. Estes são os estratos que o log-rank estratificado combina.')
''')

md(r'''
### 4.3.5 Testes em pontos fixos do tempo (60, 90 e 120 dias)

Em vez de comparar as curvas inteiras, compara-se Ŝ(t₀) entre dois grupos num horizonte fixo. H₀: S_A(t₀) = S_B(t₀). A estatística é a diferença padronizada pelas variâncias de Greenwood (qui-quadrado com 1 g.l.; `survival_difference_at_fixed_point_in_time_test`). É um teste **sem hipótese de riscos proporcionais**, com leitura direta para gestão ("aos 90 dias, X% a mais dos processos ainda estão sem sentença"). Os horizontes de 60, 90 e 120 dias cobrem o período em que a AC já ocorreu e em que a maioria das sentenças acontece, e todos os processos da base têm seguimento potencial ≥ 65 dias (os de 90 e 120 dias perdem os distribuídos mais tarde, o que o KM corrige). São 6 testes (2 contrastes com o Controle × 3 horizontes), corrigidos por Holm.

**Gráfico do teste:** diferença Ŝ_tratado(t₀) − Ŝ_Controle(t₀) com IC 95% (Greenwood): valores **positivos** = mais processos pendentes no grupo com AC (mais lento).
''')

code(r'''
res_fix = []
for t0 in [60, 90, 120]:
    for g in ['Presencial', 'Remota']:
        r = survival_difference_at_fixed_point_in_time_test(t0, km_g[g], km_g['Controle'])
        sg, eg = km_greenwood(sob.loc[sob.grupo == g, 'T'], sob.loc[sob.grupo == g, 'E'], t0)
        sc, ec = km_greenwood(sob.loc[sob.grupo == 'Controle', 'T'], sob.loc[sob.grupo == 'Controle', 'E'], t0)
        dif, ep = sg - sc, np.sqrt(eg ** 2 + ec ** 2)
        res_fix.append({'t₀ (dias)': t0, 'Contraste': f'{g} − Controle', 'Ŝ grupo': sg, 'Ŝ Controle': sc,
                        'Diferença': dif, 'IC 95% inf.': dif - 1.96 * ep, 'IC 95% sup.': dif + 1.96 * ep,
                        'χ² (1 g.l.)': r.test_statistic, 'p': r.p_value})
res_fix = pd.DataFrame(res_fix)
res_fix['p (Holm, 6 testes)'] = multipletests(res_fix['p'], method='holm')[1]
sob_tabela(res_fix, 'sob_pontos_fixos', 'Diferença na proporção ainda sem sentença em 60, 90 e 120 dias (grupo com AC − Controle)',
           secao='4.3.5', casas=3, colunas_p=('p', 'p (Holm, 6 testes)'),
           formatos={'t₀ (dias)': 'int', 'Ŝ grupo': 'pct', 'Ŝ Controle': 'pct', 'χ² (1 g.l.)': 2},
           nota='diferença e IC 95% na escala de proporção (0,127 = 12,7 p.p.), com EP de Greenwood; χ² de '
                'survival_difference_at_fixed_point_in_time_test. Destaque: p de Holm < 0,05.')

fig, ax = plt.subplots(figsize=(9.5, 5))
for j, g in enumerate(['Presencial', 'Remota']):
    d = res_fix[res_fix.Contraste.str.startswith(g)]
    xs = np.arange(3) + (j - 0.5) * 0.3
    ax.errorbar(xs, d['Diferença'], yerr=[d['Diferença'] - d['IC 95% inf.'], d['IC 95% sup.'] - d['Diferença']],
                fmt='o', ms=7, color=CORES_GRUPO[g], capsize=4, label=f'{ROTULO_GRUPO[g]} − Controle')
    for xi, (v, dif, ph) in zip(xs, d[['IC 95% sup.', 'Diferença', 'p (Holm, 6 testes)']].values):
        ax.annotate(f'{100 * dif:+.1f} p.p.'.replace('.', ',', 1).replace('-', '−') + f'\nHolm {fmt_p(ph)}',
                    (xi, v), xytext=(0, 4), textcoords='offset points', ha='center', va='bottom', fontsize=8)
ax.axhline(0, color=TINTA_2, ls='--', lw=1); ax.set_xticks(range(3), ['60 dias', '90 dias', '120 dias'])
ax.grid(axis='x', visible=False)
ax.yaxis.set_major_formatter(mpl.ticker.FuncFormatter(lambda v, _: f'{100 * v:+.0f} p.p.'.replace('-', '−')))
ax.set_ylim(min(-0.08, res_fix['IC 95% inf.'].min() - 0.02), res_fix['IC 95% sup.'].max() + 0.08)
ax.set_xlabel('Horizonte t₀ (dias desde a distribuição)')
ax.set_ylabel('Ŝ_grupo(t₀) − Ŝ_Controle(t₀) (pontos percentuais)')
ax.set_title('Diferença na proporção ainda sem sentença (IC 95% Greenwood)')
legenda_abaixo(ax, ncol=2, dy=-0.17)
figura(fig, 'sob_pontos_fixos', 'Aos 90 dias, os grupos com AC têm 13 a 14 p.p. a mais de processos sem sentença; aos 60 dias, nenhuma diferença',
       secao='4.3.5', nota='valores positivos = mais processos pendentes no grupo com AC (mais lento). Teste qui-quadrado (1 g.l.) '
                           'em cada ponto; Holm sobre os 6 testes.')
''')

md(r'''
### 4.3.6 Tempo médio restrito (RMST)

O **RMST** até o horizonte τ é a área sob a curva de Kaplan-Meier, μ_τ = ∫₀^τ S(t) dt (MORETTIN; SINGER, 2021, p. 248; ROYSTON; PARMAR, 2013). Leitura: "em média, nos primeiros τ dias após a distribuição, o processo permaneceu μ_τ dias sem sentença". A **diferença de RMST** entre grupos é uma medida de efeito em **dias**, que não exige riscos proporcionais e capta diferenças de qualquer forma (inclusive curvas que se cruzam). É o substituto correto do "tempo médio" que o notebook do professor calculava ignorando a censura (E14, E30).

**Escolha de τ.** O τ deve ser no máximo o menor dos seguimentos máximos dos grupos (273 dias), e com gente suficiente em risco para que Ŝ(t) seja estável até ele. Usam-se **τ = 150 dias** (cerca de 5 meses; 55% a 59% de cada grupo têm seguimento potencial ≥ 150 dias, embora só ~8% ainda estejam em risco nesse dia) e **τ = 180 dias** (6 meses, o horizonte de gestão mais longo com informação razoável; ver a tabela de vida em 4.1.5). τ = 90 dias é mostrado como horizonte curto. Os horizontes não foram fixados num protocolo anterior aos dados; τ = 180 dias é tratado como o principal por ser o maior horizonte com informação (escolha declarada aqui para transparência).

**Inferência.** O RMST é calculado com `restricted_mean_survival_time` do `lifelines` (conferido contra a soma da curva na grade diária). O IC de cada RMST **e** das diferenças vem de *bootstrap* (a opção `return_variance=True` do `lifelines` devolve a variância de min(T, τ) na população, e não a variância do estimador, e não serve para IC). As **diferenças** têm IC por *bootstrap* não paramétrico (2.000 reamostras **dentro de cada grupo**, preservando os tamanhos sorteados; IC percentil) e p-valor pela aproximação normal com o erro-padrão bootstrap. H₀: μ_τ,grupo = μ_τ,Controle.

**Gráficos do teste:** no primeiro, a área entre as curvas de cada grupo com AC e a do Controle é a diferença de RMST até 180 dias (com o resultado do teste anotado); no segundo, as diferenças com IC bootstrap para os três horizontes.
''')

code(r'''
TAUS = [90, 150, 180]
B_BOOT = 2000
rng_boot = np.random.default_rng(SEMENTE + 41)
idx_g = {g: np.where(sob.grupo == g)[0] for g in ORDEM_GRUPO}
T_arr, E_arr = sob['T'].values.astype(int), sob['E'].values.astype(int)

linhas_rmst, dif_rmst, boot_rmst = [], [], {}
for tau in TAUS:
    # bootstrap estratificado por grupo
    bs = {g: np.empty(B_BOOT) for g in ORDEM_GRUPO}
    for b in range(B_BOOT):
        for g in ORDEM_GRUPO:
            ii = rng_boot.choice(idx_g[g], len(idx_g[g]), replace=True)
            bs[g][b] = rmst_grade(T_arr[ii], E_arr[ii], tau)
    boot_rmst[tau] = bs
    for g in ORDEM_GRUPO:
        m = restricted_mean_survival_time(km_g[g], t=tau)
        linhas_rmst.append({'τ (dias)': tau, 'Grupo': g, 'RMST (dias)': m, 'EP (bootstrap)': bs[g].std(ddof=1),
                            'IC 95% inf.': np.percentile(bs[g], 2.5), 'IC 95% sup.': np.percentile(bs[g], 97.5)})
    for a, b_ in [('Controle', 'Presencial'), ('Controle', 'Remota'), ('Presencial', 'Remota')]:
        est = rmst_grade(T_arr[idx_g[b_]], E_arr[idx_g[b_]], tau) - rmst_grade(T_arr[idx_g[a]], E_arr[idx_g[a]], tau)
        dist = bs[b_] - bs[a]; ep = dist.std(ddof=1)
        dif_rmst.append({'τ (dias)': tau, 'Contraste': f'{b_} − {a}', 'Diferença (dias)': est,
                         'IC 95% inf. (bootstrap)': np.percentile(dist, 2.5), 'IC 95% sup. (bootstrap)': np.percentile(dist, 97.5),
                         'p (normal, EP bootstrap)': 2 * stats.norm.sf(abs(est / ep))})
rmst_tab = pd.DataFrame(linhas_rmst)
dif_rmst = pd.DataFrame(dif_rmst)
print('Conferência: RMST(180) Controle — lifelines', fmt_br(rmst_tab.query('`τ (dias)` == 180 and Grupo == "Controle"')['RMST (dias)'].iloc[0], 3),
      '| grade diária', fmt_br(rmst_grade(T_arr[idx_g["Controle"]], E_arr[idx_g["Controle"]], 180), 3))
tabela(rmst_tab, 'sob_rmst_grupos', 'RMST por grupo e horizonte τ: dias, em média, sem sentença nos primeiros τ dias',
       secao='4.3.6', casas=1, formatos={'τ (dias)': 'int', 'EP (bootstrap)': 2},
       nota=f'RMST = área sob o Kaplan-Meier até τ (lifelines); EP e IC 95% percentil por bootstrap estratificado por grupo '
            f'({fmt_br(B_BOOT, 0)} reamostras).')
sob_tabela(dif_rmst, 'sob_rmst_diferencas', 'Diferenças de RMST entre grupos (dias; > 0 = mais dias sem sentença no 1º grupo)',
           secao='4.3.6', casas=2, colunas_p=('p (normal, EP bootstrap)',), formatos={'τ (dias)': 'int'},
           nota='IC 95% percentil por bootstrap; p pela aproximação normal com o EP bootstrap. Destaque: p < 0,05.')

# (a) a área entre as curvas é a diferença de RMST até 180 dias
tau = 180
tg = np.arange(0, tau + 1)
Sc, _ = aj_grade(T_arr[idx_g['Controle']], E_arr[idx_g['Controle']])
fig, axes = plt.subplots(1, 2, figsize=(13, 5), sharey=True)
for ax, g in zip(axes, ['Presencial', 'Remota']):
    Sg, _ = aj_grade(T_arr[idx_g[g]], E_arr[idx_g[g]])
    ax.step(tg, Sc[tg], where='post', color=CORES_GRUPO['Controle'], lw=2, label='Controle')
    ax.step(tg, Sg[tg], where='post', color=CORES_GRUPO[g], lw=2, label=g)
    ax.fill_between(tg, Sc[tg], Sg[tg], step='post', where=Sg[tg] >= Sc[tg], color=CORES_GRUPO[g], alpha=0.3, lw=0,
                    label='área: grupo com AC mais lento')
    ax.fill_between(tg, Sc[tg], Sg[tg], step='post', where=Sg[tg] < Sc[tg], color=CORES_GRUPO['Controle'], alpha=0.3, lw=0,
                    label='área: grupo com AC mais rápido')
    d = dif_rmst.query('`τ (dias)` == @tau and Contraste == @g + " − Controle"').iloc[0]
    ax.set_title(f'AC {g.lower()} × Controle')
    ax.set_xlabel(ROTULOS['dias']); ax.set_xlim(0, tau); ax.set_xticks(np.arange(0, tau + 1, 30))
    ax.set_ylim(0, 1.02); eixo_pct(ax); ax.grid(axis='both', visible=True)
    ax.legend(loc='lower left', fontsize=8.5)
    anotar_teste(ax, texto_teste(f'ΔRMST({tau}) = {fmt_br(d["Diferença (dias)"], 1)} dias',
                                 f'IC 95% [{fmt_br(d["IC 95% inf. (bootstrap)"], 1)}; {fmt_br(d["IC 95% sup. (bootstrap)"], 1)}]',
                                 d['p (normal, EP bootstrap)']), loc='upper right')
axes[0].set_ylabel(ROTULOS['S'])
figura(fig, 'sob_rmst_areas', 'Nos primeiros 180 dias, um processo com AC remota fica em média cerca de 11 dias a mais sem sentença',
       secao='4.3.6', nota='Kaplan-Meier até τ = 180 dias; a área sombreada entre as curvas é a diferença de RMST (área '
                           'acima da curva do Controle menos a área abaixo). IC 95% por bootstrap estratificado.')

# (b) diferenças de RMST com IC bootstrap nos três horizontes
fig, ax = plt.subplots(figsize=(10, 5.2))
CONTRASTES_RMST = ['Presencial − Controle', 'Remota − Controle', 'Remota − Presencial']
for j, c in enumerate(CONTRASTES_RMST):
    d = dif_rmst[dif_rmst.Contraste == c]
    cor = [CORES_GRUPO['Presencial'], CORES_GRUPO['Remota'], CINZA][j]
    xs = np.arange(len(TAUS)) + (j - 1) * 0.26
    ax.errorbar(xs, d['Diferença (dias)'], yerr=[d['Diferença (dias)'] - d['IC 95% inf. (bootstrap)'],
                d['IC 95% sup. (bootstrap)'] - d['Diferença (dias)']], fmt='o', ms=7, color=cor, capsize=4, label=c)
    for xi, (hi, pv) in zip(xs, d[['IC 95% sup. (bootstrap)', 'p (normal, EP bootstrap)']].values):
        ax.annotate(fmt_p(pv), (xi, hi), xytext=(0, 3), textcoords='offset points', ha='center', va='bottom',
                    fontsize=8, color=TINTA_2)
ax.axhline(0, color=TINTA_2, ls='--', lw=1)
ax.set_xticks(range(len(TAUS)), [f'τ = {t} dias' for t in TAUS]); ax.grid(axis='x', visible=False)
ax.set_xlabel('Horizonte τ do RMST')
ax.set_ylabel('Diferença de RMST (dias; IC 95% bootstrap)')
ax.set_title('Diferenças de RMST (> 0 = mais dias sem sentença); número sobre cada IC = valor-p')
ax.set_ylim(dif_rmst['IC 95% inf. (bootstrap)'].min() - 2, dif_rmst['IC 95% sup. (bootstrap)'].max() + 4)
legenda_abaixo(ax, ncol=3, dy=-0.17)
figura(fig, 'sob_rmst', 'A diferença de RMST cresce com o horizonte e só é significativa para a AC remota (τ = 150 e 180 dias)',
       secao='4.3.6', nota='H₀: RMST do grupo = RMST da referência; p pela aproximação normal com o EP bootstrap (sem correção '
                           'de multiplicidade; o τ principal é 180 dias).')
''')

interp('sob_testes')

# =====================================================================
md(r'''
---

## 4.4 Diagnóstico da hipótese de riscos proporcionais

O modelo de Cox (seção 4.5) resume o efeito do grupo numa única razão de riscos, **constante no tempo**: λ(t | x) = λ₀(t) exp(x′β). Antes de interpretar esse número, verifica-se se a hipótese é razoável. Se não for, o HR estimado é uma média ponderada de efeitos que mudam ao longo do tempo, e pode até esconder efeitos de sinais opostos.

### 4.4.1 Método gráfico: log[−log Ŝ(t)] × log t

Sob riscos proporcionais, S_g(t) = S₀(t)^{exp(β_g)}, logo log[−log S_g(t)] = log[−log S₀(t)] + β_g: as curvas dos grupos devem ser **paralelas** (distância vertical constante = β_g). Curvas que se cruzam ou convergem indicam violação (COLOSIMO; GIOLO, 2006, p. 167). Se, além de paralelas, forem retas, o modelo de Weibull é indicado (p. 96-99). O método é subjetivo, por isso é complementado pelo teste formal.
''')

code(r'''
fig, ax = plt.subplots(figsize=(9.5, 5.4))
for g in ORDEM_GRUPO:
    sf_ = km_g[g].survival_function_.iloc[:, 0]
    sf_ = sf_[(sf_ > 0) & (sf_ < 1) & (sf_.index > 0)]
    ax.step(np.log(sf_.index), np.log(-np.log(sf_.values)), where='post', color=CORES_GRUPO[g], lw=2, label=ROTULO_GRUPO[g])
ax.set_xlabel('log t (t em dias desde a distribuição)'); ax.set_ylabel('log[−log Ŝ(t)]')
ax.grid(axis='both', visible=True)
sec = ax.secondary_xaxis('top', functions=(np.exp, np.log)); sec.set_xticks([1, 7, 30, 60, 90, 180])
sec.set_xlabel('Dias (escala log)')
sec.xaxis.set_major_formatter(mpl.ticker.FuncFormatter(lambda v, _: fmt_br(v, 0)))
ax.set_title('log[−log Ŝ(t)] × log t por grupo: curvas paralelas ⇔ riscos proporcionais', pad=10)
ax.legend(loc='lower right')
figura(fig, 'sob_loglog', 'As curvas log(−log Ŝ) não são paralelas: cruzam-se até 60 dias e separam-se entre 60 e 120 dias',
       secao='4.4.1', nota='sob riscos proporcionais, a distância vertical entre as curvas seria constante (= β do grupo). '
                           'Curvas retas indicariam o modelo de Weibull.')
''')

md(r'''
### 4.4.2 Resíduos de Schoenfeld e teste de Grambsch-Therneau

Os **resíduos de Schoenfeld** comparam, em cada sentença, a covariável do processo sentenciado com a média ponderada das covariáveis dos que estavam em risco. Grambsch e Therneau (1994) mostraram que os resíduos **padronizados** s*_k somados a β̂ estimam β(t): se o efeito é constante, o gráfico de s*_k + β̂ contra uma função do tempo g(t) é **horizontal** (COLOSIMO; GIOLO, 2006, eq. 5.10, p. 167-169). O **teste** correspondente verifica a correlação entre os resíduos e g(t), por covariável (χ²₁) e globalmente (p. 169-170). As escolhas usuais de g(t) são t, log t, posto (*rank*) e 1 − KM ("na prática há pouca diferença"; o padrão do R é km, p. 170). O teste é aplicado ao modelo de Cox com grupo + mês (o modelo (b) da seção 4.5 sem a origem externa, cujos 12 processos não sustentam um teste próprio), com as transformações posto, km e identidade (log t não é usado porque há sentenças no dia 0, e log 0 não existe).

- H₀: β_q(t) = β_q (efeito constante; riscos proporcionais);
- H₁: β_q(t) varia monotonicamente com g(t).

**Gráfico do teste:** s*_k + β̂ contra o posto do tempo e contra o tempo em dias, com suavização *lowess*; a linha tracejada é o β̂ constante do Cox. O eixo vertical está na escala do log-HR: **acima de 0 = sentença mais rápida que no Controle naquele momento; abaixo = mais lenta**.
''')

code(r'''
X_BASE = ['Presencial', 'Remota']
X_AJ = X_BASE + COLS_MES + ['origem_ext']
cox_ph = CoxPHFitter().fit(sob[['T', 'E'] + X_BASE + COLS_MES], 'T', 'E')
res_ph = []
for tr in ['rank', 'km', 'identity']:
    r = proportional_hazard_test(cox_ph, sob[['T', 'E'] + X_BASE + COLS_MES], time_transform=tr)
    sm_ = r.summary
    for termo in X_BASE:
        res_ph.append({'g(t)': tr, 'Termo': ROTULO_TERMO[termo], 'χ² (1 g.l.)': sm_.loc[termo, 'test_statistic'], 'p': sm_.loc[termo, 'p']})
res_ph = pd.DataFrame(res_ph)
NOME_GT = {'rank': 'posto', 'km': '1 − KM', 'identity': 't (identidade)'}
sob_tabela(res_ph.assign(**{'g(t)': res_ph['g(t)'].map(NOME_GT)}), 'sob_schoenfeld_grupo',
           'Teste de Grambsch-Therneau (resíduos de Schoenfeld) para os termos de grupo, por transformação do tempo',
           secao='4.4.2', casas=2, colunas_p=('p',), nota='modelo de Cox grupo + mês; H₀: efeito constante no tempo (riscos proporcionais).')
_r = proportional_hazard_test(cox_ph, sob[['T', 'E'] + X_BASE + COLS_MES], time_transform='rank').summary
sob_tabela(_r.loc[COLS_MES, ['test_statistic', 'p']].rename(index=ROTULO_TERMO, columns={'test_statistic': 'χ² (1 g.l.)'})
           .rename_axis('Termo'), 'sob_schoenfeld_meses',
           'Teste de Grambsch-Therneau para os termos de mês (transformação posto)', secao='4.4.2', casas=2, colunas_p=('p',))

sch = cox_ph.compute_residuals(sob[['T', 'E'] + X_BASE + COLS_MES], kind='scaled_schoenfeld')
t_ev = sob.loc[sch.index, 'T'].values
ordem_t = stats.rankdata(t_ev)
fig, axes = plt.subplots(2, 2, figsize=(13, 9), sharey='row')
for i, termo in enumerate(X_BASE):
    beta = cox_ph.params_[termo]
    yv = sch[termo].values + beta
    for j, (xv, nome) in enumerate([(ordem_t, 'Posto do tempo de sentença (1 = mais rápida)'), (t_ev, 'Dias até a sentença')]):
        ax = axes[i, j]
        ax.scatter(xv, yv, s=6, color=CORES_GRUPO[termo], alpha=0.25, lw=0)
        lw = lowess(yv, xv, frac=0.3)
        ax.plot(lw[:, 0], lw[:, 1], color=TINTA, lw=2.2, label='β(t) suavizado (lowess)')
        ax.axhline(beta, color=CORES_GRUPO[termo], ls='--', lw=1.5, label=f'β̂ constante do Cox = {fmt_br(beta, 2)}')
        ax.axhline(0, color=TINTA_2, lw=0.8)
        ax.set_ylim(-4, 4); ax.set_xlabel(nome); ax.set_ylabel(f'β(t), log-HR\n{ROTULO_TERMO[termo]}')
        tr = 'rank' if j == 0 else 'identity'
        linha = res_ph[(res_ph['g(t)'] == tr) & (res_ph.Termo == ROTULO_TERMO[termo])].iloc[0]
        ax.set_title(f'{ROTULO_TERMO[termo]}: β(t) contra {"o posto do tempo" if j == 0 else "o tempo em dias"}')
        ax.legend(fontsize=8, loc='lower right', framealpha=0.9, frameon=True)
        anotar_teste(ax, texto_teste(f'Grambsch-Therneau (g(t) = {'posto' if tr == 'rank' else 't'})',
                                     f'χ²(1) = {fmt_br(linha["χ² (1 g.l.)"], 2)}', linha['p']), loc='upper left', tamanho=8)
figura(fig, 'sob_schoenfeld', 'O teste não rejeita riscos proporcionais, mas β(t) tem um vale entre 60 e 110 dias que '
       'uma correlação linear não capta', secao='4.4.2',
       nota='resíduos de Schoenfeld padronizados + β̂ (modelo de Cox grupo + mês). Acima de 0 = sentença mais rápida que no '
            'Controle naquele momento; abaixo = mais lenta. Eixo vertical cortado em ±4.')
''')

interp('sob_ph')

# =====================================================================
md(r'''
---

## 4.5 Modelos de Cox

O modelo de riscos proporcionais de Cox (COX, 1972) é λ(t | x) = λ₀(t) exp(x′β), com λ₀(t) não especificado. β é estimado pela verossimilhança parcial L(β) = ∏ [exp(x_i′β) / Σ_{j ∈ R(t_i)} exp(x_j′β)]^{δ_i} (COLOSIMO; GIOLO, 2006, eq. 5.6, p. 161). Como o tempo é medido em dias, há muitos **empates** (vários processos sentenciados no mesmo dia); usa-se a aproximação de **Efron** (1977), melhor que a de Breslow quando os empates são numerosos (p. 161-162), que é o padrão do `CoxPHFitter`.

**Interpretação.** exp(β_g) é a razão de riscos (HR) do grupo g em relação ao Controle (referência), constante no tempo (p. 162-164). Na linguagem do processo: HR = 0,80 significa que, a cada dia, um processo do grupo com AC que ainda está pendente tem 20% **menos** "chance instantânea" de receber sentença do que um processo do Controle também pendente, ou seja, **tramita mais devagar**.

**Modelos ajustados.**

| Modelo | Covariáveis | Para quê |
|---|---|---|
| (a) | grupo | efeito total do rito (o sorteio dispensa ajuste para não haver viés) |
| (b) | grupo + mês de distribuição + origem externa | precisão e controle do calendário (composição mensal, seguimento) |
| (b′) | grupo + origem externa, **estratificado por mês** | risco basal próprio de cada mês, sem supor efeito proporcional do mês |
| (c) | grupo × janela de tempo + mês + origem | efeito do rito **variando no tempo** (se os riscos não forem proporcionais) |

O **dia da semana** da distribuição não entra: não há mecanismo plausível pelo qual ele altere a duração (é apenas o dia do protocolo) e, com 7 níveis, só gastaria graus de liberdade. Os **acordos** (`acordo_ac`, `acordo_fora`) **não** entram como covariáveis: ocorrem durante o processo e definem o tipo de desfecho; usá-los como covariável fixa criaria viés de tempo imortal (seção 4.7 os trata como desfecho).

### 4.5.1 Modelos (a), (b) e (b′)
''')

code(r'''
cox_a = CoxPHFitter().fit(sob[['T', 'E'] + X_BASE], 'T', 'E')
cox_b = CoxPHFitter().fit(sob[['T', 'E'] + X_AJ], 'T', 'E')
cox_bs = CoxPHFitter().fit(sob[['T', 'E', 'mes_cod'] + X_BASE + ['origem_ext']], 'T', 'E', strata=['mes_cod'])
MODELOS_COX = {'(a) grupo': cox_a, '(b) grupo + mês + origem': cox_b, "(b′) grupo + origem, estrato = mês": cox_bs}

for (nome, m), id_ in zip(MODELOS_COX.items(), ['sob_cox_a', 'sob_cox_b', 'sob_cox_bs']):
    sob_tabela(tabela_hr(m).rename_axis('Termo'), id_, f'Modelo de Cox {nome}: razões de risco de sentença (Efron)',
               secao='4.5.1', casas=3, colunas_p=('p (Wald)',),
               nota='HR < 1 = sentença mais lenta que na referência; IC 95% e p de Wald. Destaque: p < 0,05.')

def resumo_ajuste(m):
    lr = m.log_likelihood_ratio_test()
    return pd.Series({'log-verossimilhança parcial': m.log_likelihood_, 'TRV vs. nulo (χ²)': lr.test_statistic,
                      'g.l.': lr.degrees_freedom, 'p (TRV)': lr.p_value,
                      'AIC parcial': m.AIC_partial_, 'Concordância (C de Harrell)': m.concordance_index_})
ajuste_cox = pd.DataFrame({n: resumo_ajuste(m) for n, m in MODELOS_COX.items()}).T
sob_tabela(ajuste_cox.rename_axis('Modelo'), 'sob_cox_ajuste', 'Ajuste dos modelos de Cox: verossimilhança, TRV contra o nulo, '
           'AIC parcial e concordância', secao='4.5.1', casas=3, colunas_p=('p (TRV)',), destaque=None,
           formatos={'g.l.': 'int', 'log-verossimilhança parcial': 1, 'AIC parcial': 1, 'TRV vs. nulo (χ²)': 2},
           nota='o AIC parcial do modelo estratificado (b′) não é comparável ao dos outros (verossimilhança por estrato).')

_flor = pd.concat({nome: tabela_hr(m, X_BASE) for nome, m in MODELOS_COX.items()})
_flor.index = [f'{nome}: {termo.replace(" × Controle", "")}' for nome, termo in _flor.index]
fig, ax = plt.subplots(figsize=(10, 4.8))
floresta(ax, _flor, cor_de=lambda n: CORES_GRUPO['Presencial'] if 'presencial' in n else CORES_GRUPO['Remota'],
         xlabel='HR de sentença vs. Controle (IC 95%; escala log)', ticks=[0.6, 0.7, 0.8, 0.9, 1, 1.1])
ax.set_xlim(0.6, 1.5)
for yi in (1.5, 3.5):
    ax.axhline(yi, color=GRADE, lw=0.8)
ax.set_title('Efeito do rito nos três modelos de Cox (HR < 1 = sentença mais lenta)')
figura(fig, 'sob_cox_floresta', 'Ajustar ou estratificar pelo mês quase não muda o efeito: HR ≈ 0,8 na AC remota e ≈ 0,85 na presencial',
       secao='4.5.1', nota='Cox (Efron); IC 95% e p de Wald. (a) só grupo; (b) grupo + mês + origem externa; '
                           '(b′) grupo + origem, estratificado por mês.')
HR_B = tabela_hr(cox_b, X_BASE)
''')

md(r'''
**Curvas de sobrevivência ajustadas.** Para mostrar o que o modelo (b) implica em escala de tempo, calcula-se a curva **padronizada** de cada grupo: atribui-se o grupo g a todos os 938 processos (mantidos o mês e a origem de cada um), prevê-se Ŝ(t | x) = Ŝ₀(t)^{exp(x′β̂)} (COLOSIMO; GIOLO, 2006, p. 164-165) e tira-se a média. É a curva que se observaria se toda a amostra tivesse sido alocada ao grupo g. As curvas de KM aparecem tracejadas para comparação: se o Cox é adequado, as duas devem estar próximas.
''')

code(r'''
grade_t = np.arange(0, 275)
fig, ax = plt.subplots(figsize=(10, 5.2))
for g in ORDEM_GRUPO:
    x_g = sob[X_AJ].copy(); x_g['Presencial'] = int(g == 'Presencial'); x_g['Remota'] = int(g == 'Remota')
    S_pad = cox_b.predict_survival_function(x_g, times=grade_t).mean(axis=1)
    ax.plot(grade_t, S_pad, color=CORES_GRUPO[g], lw=2.2)
    sf_ = km_g[g].survival_function_.iloc[:, 0]
    ax.step(sf_.index, sf_.values, where='post', color=CORES_GRUPO[g], ls='--', lw=1.1)
ax.set_xlim(0, 275); ax.set_xticks(np.arange(0, 271, 30)); ax.set_ylim(0, 1.02); eixo_pct(ax)
ax.grid(axis='both', visible=True)
ax.set_xlabel(ROTULOS['dias']); ax.set_ylabel(ROTULOS['S'])
ax.set_title('Curvas padronizadas do Cox (b) e Kaplan-Meier, por grupo')
ax.legend(handles=LEG_GRUPO(longo=True) + [Line2D([], [], color=TINTA, lw=2.2, label='Cox (b), curva padronizada'),
                                           Line2D([], [], color=TINTA, lw=1.1, ls='--', label='Kaplan-Meier')],
          loc='upper right')
figura(fig, 'sob_cox_curvas', 'As curvas implicadas pelo Cox (b) acompanham bem os Kaplan-Meier dos três grupos',
       secao='4.5.1', nota='curva padronizada = média de Ŝ(t | x) sobre os 938 processos com o grupo fixado e o mês e a origem '
                           'observados de cada um.')
''')

md(r'''
### 4.5.2 Efeito do rito variando no tempo: modelo (c) com janelas

Se os resíduos de Schoenfeld (4.4.2) mostram que o efeito do grupo muda com o tempo, um único HR é um resumo enganoso. A solução recomendada é permitir um coeficiente por **janela de tempo** (COLOSIMO; GIOLO, 2006, p. 170-172; MORETTIN; SINGER, 2021, p. 256, nota 2): cada processo é dividido em episódios (0, 30], (30, 90] e (90, ∞) dias, e o grupo entra interagido com a janela. Os cortes têm justificativa substantiva, mas foram fixados **depois** de ver as curvas de Kaplan-Meier e os resíduos de Schoenfeld (escolha *a posteriori*). Por isso o TRV de (c) contra (b) é **otimista** (o p-valor não leva em conta a escolha dos cortes) e deve ser lido como descrição de onde está o efeito, não como teste confirmatório:

- **até 30 dias**: fase anterior à AC na maioria dos casos (citação, intimação e pauta); concentra as extinções imediatas e as redistribuições;
- **30 a 90 dias**: período em que as audiências obrigatórias ocorrem e em que se dão a ausência do autor (extinção, art. 51, I, da Lei 9.099/1995) e os acordos;
- **após 90 dias**: fase de instrução e julgamento de mérito.

O modelo é ajustado em formato de **processo de contagem** (início, fim] com o `CoxTimeVaryingFitter` (Efron). Como o `lifelines` exige início < fim, os tempos são deslocados em +0,5 dia (só a ordem dos tempos importa na verossimilhança parcial, logo o deslocamento não altera nada). A primeira célula confere que o modelo sem interação reproduz exatamente o Cox (b). O TRV compara (c) com (b): H₀: o HR de cada grupo é o mesmo nas três janelas (4 g.l.).
''')

code(r'''
CORTES = [30, 90]
JANELAS = ['0–30 d', '30–90 d', '> 90 d']

def dividir_episodios(df, cortes=CORTES, desloc=0.5):
    """Formato de contagem (start, stop] com uma linha por processo e janela de tempo."""
    lim = [0.0] + [c + desloc for c in cortes] + [np.inf]
    partes = []
    for j in range(len(lim) - 1):
        a, b = lim[j], lim[j + 1]
        T = df['T'] + desloc
        sub = df[T > a].copy()
        Ts = sub['T'] + desloc
        sub['start'] = a; sub['stop'] = np.minimum(Ts, b)
        sub['ev'] = ((sub['E'] == 1) & (Ts <= b)).astype(int)
        sub['janela'] = j
        partes.append(sub)
    ep = pd.concat(partes).reset_index().rename(columns={'index': 'id'})
    for j in range(len(lim) - 1):
        for g in X_BASE:
            ep[f'{g}_j{j}'] = ep[g] * (ep['janela'] == j)
    return ep

ep = dividir_episodios(sob)
COLS_INT = [f'{g}_j{j}' for g in X_BASE for j in range(3)]
ctv_b = CoxTimeVaryingFitter().fit(ep[['id', 'start', 'stop', 'ev'] + X_AJ], id_col='id', event_col='ev', start_col='start', stop_col='stop')
ctv_c = CoxTimeVaryingFitter().fit(ep[['id', 'start', 'stop', 'ev'] + COLS_INT + COLS_MES + ['origem_ext']],
                                   id_col='id', event_col='ev', start_col='start', stop_col='stop')
print(f'Conferência: HR Presencial, Cox (b) = {fmt_br(np.exp(cox_b.params_["Presencial"]), 4)} | '
      f'contagem sem interação = {fmt_br(np.exp(ctv_b.params_["Presencial"]), 4)}')
trv_c = 2 * (ctv_c.log_likelihood_ - ctv_b.log_likelihood_)
P_TRV_C = stats.chi2.sf(trv_c, 4)
print(f'TRV (c) × (b): χ² = {fmt_br(trv_c, 2)}, 4 g.l., p = {p_br(P_TRV_C)}  |  '
      f'AIC parcial (b) = {fmt_br(-2 * ctv_b.log_likelihood_ + 2 * len(ctv_b.params_), 1)}; (c) = {fmt_br(-2 * ctv_c.log_likelihood_ + 2 * len(ctv_c.params_), 1)}')

hr_c = ctv_c.summary.loc[COLS_INT]
HR_C = pd.DataFrame({'HR': hr_c['exp(coef)'], 'IC 95% inf.': hr_c['exp(coef) lower 95%'], 'IC 95% sup.': hr_c['exp(coef) upper 95%'],
                     'p (Wald)': hr_c['p']})
HR_C.index = [f'{ROTULO_TERMO[g]}, {JANELAS[j]}' for g in X_BASE for j in range(3)]
eventos_jan = ep.groupby(['janela', 'grupo'], observed=True)['ev'].sum().unstack()
eventos_jan.index = JANELAS
_ej = eventos_jan.copy(); _ej.columns = [str(c) for c in _ej.columns]
tabela(_ej.rename_axis('Janela de tempo'), 'sob_cox_janelas_eventos', 'Sentenças em cada janela de tempo, por grupo',
       secao='4.5.2', formatos={c: 'int' for c in _ej.columns})
sob_tabela(HR_C.rename_axis('Termo'), 'sob_cox_janelas', 'Modelo (c): razão de risco de sentença por janela de tempo (Cox em '
           'formato de contagem, ajustado por mês e origem)', secao='4.5.2', casas=3, colunas_p=('p (Wald)',),
           nota=f'TRV (c) × (b): χ² = {fmt_br(trv_c, 2)}, 4 g.l., {p_txt(P_TRV_C)}. Destaque: p < 0,05.')

fig, ax = plt.subplots(figsize=(10, 5))
for i, g in enumerate(X_BASE):
    d = HR_C.iloc[3 * i:3 * i + 3]
    xs = np.arange(3) + (i - 0.5) * 0.25
    ax.errorbar(xs, d['HR'], yerr=[d['HR'] - d['IC 95% inf.'], d['IC 95% sup.'] - d['HR']], fmt='o', ms=7,
                color=CORES_GRUPO[g], capsize=4, label=f'{ROTULO_TERMO[g]} (por janela)')
    for xi, (hr, hi, pv) in zip(xs, d[['HR', 'IC 95% sup.', 'p (Wald)']].values):
        ax.annotate(f'{fmt_br(hr, 2)}\n{p_txt(pv)}', (xi, hi), xytext=(0, 3), textcoords='offset points', ha='center',
                    va='bottom', fontsize=8, color=TINTA_2, bbox=CAIXA_TXT)
    ax.axhline(np.exp(cox_b.params_[g]), color=CORES_GRUPO[g], ls=':', lw=1.3,
               label=f'HR constante do modelo (b) = {fmt_br(np.exp(cox_b.params_[g]), 2)}')
ax.axhline(1, color=TINTA_2, ls='--', lw=1); ax.set_yscale('log')
ax.yaxis.set_major_formatter(mpl.ticker.FuncFormatter(lambda v, _: fmt_br(v, 2))); ax.yaxis.set_minor_formatter(mpl.ticker.NullFormatter())
ax.set_yticks([0.4, 0.6, 0.8, 1, 1.25, 1.6, 2.5]); ax.set_ylim(0.35, 3)
ax.set_xticks(range(3), ['0 a 30 dias', '30 a 90 dias', 'mais de 90 dias']); ax.grid(axis='x', visible=False)
ax.set_xlabel('Janela de tempo desde a distribuição')
ax.set_ylabel('HR de sentença vs. Controle (IC 95%; escala log)')
ax.set_title('Modelo (c): razão de risco por janela de tempo')
ax.legend(loc='upper right', fontsize=8.5)
anotar_teste(ax, texto_teste('TRV (c) × (b): HR igual nas 3 janelas?', f'χ²(4) = {fmt_br(trv_c, 2)}', P_TRV_C), loc='upper left')
figura(fig, 'sob_cox_janelas', 'O atraso dos grupos com AC concentra-se entre 30 e 90 dias, quando as audiências acontecem (HR ≈ 0,6)',
       secao='4.5.2', nota='Cox em formato de contagem (início, fim] com o grupo interagido com a janela, ajustado por mês e '
                           'origem; IC 95% e p de Wald.')
''')

md(r'''
### 4.5.3 Adequação global: resíduos de Cox-Snell

Os resíduos de Cox-Snell são ê_i = Λ̂₀(t_i) exp(x_i′β̂) (risco acumulado estimado de cada processo no seu próprio tempo). Se o modelo está bem ajustado, eles se comportam como uma amostra censurada de uma exponencial padrão, e o risco acumulado de Nelson-Aalen **dos próprios resíduos** fica sobre a reta de inclinação 1 (COLOSIMO; GIOLO, 2006, p. 166; eq. 4.11, p. 124). Esse resíduo avalia o ajuste global; **não** serve para testar riscos proporcionais (p. 166). Calcula-se como ê_i = δ_i − m̂_i, sendo m̂_i o resíduo martingal.
''')

code(r'''
def cox_snell_plot(ax, ei, delta, titulo, cor=TINTA):
    na = NelsonAalenFitter().fit(ei, delta)
    ax.step(na.cumulative_hazard_.index, na.cumulative_hazard_.iloc[:, 0], where='post', color=cor, lw=2, label='Λ̂ dos resíduos')
    lim = float(np.nanmax(na.cumulative_hazard_.index[np.isfinite(na.cumulative_hazard_.iloc[:, 0])]))
    ax.plot([0, lim], [0, lim], color=DESTAQUE, ls='--', lw=1.3, label='Reta y = x (Exp(1): ajuste perfeito)')
    ax.set_xlabel('Resíduo de Cox-Snell ê'); ax.set_ylabel('Risco acumulado dos resíduos Λ̂(ê)')
    ax.set_title(titulo); ax.legend(fontsize=8.5, loc='upper left'); ax.grid(axis='both', visible=True)

mart_b = cox_b.compute_residuals(sob[['T', 'E'] + X_AJ], kind='martingale')
cs_b = sob.loc[mart_b.index, 'E'] - mart_b['martingale']
fig, ax = plt.subplots(figsize=(6.5, 5))
cox_snell_plot(ax, cs_b.values, sob.loc[mart_b.index, 'E'].values, 'Cox-Snell do modelo (b)')
figura(fig, 'sob_cox_snell', 'O Cox (b) tem bom ajuste global: os resíduos seguem a reta y = x até ê ≈ 3',
       secao='4.5.3', nota='Nelson-Aalen dos resíduos de Cox-Snell ê = δ − m̂ (m̂ = resíduo martingal). '
                           'O afastamento na cauda (poucos resíduos grandes) é usual.')
''')

md(r'''
### 4.5.4 Resíduos martingal (forma funcional), deviance (atípicos) e dfbeta (influência)

- **Martingal** m̂_i = δ_i − ê_i: diferença entre o número observado de eventos do processo (0 ou 1) e o esperado pelo modelo. Contra uma covariável **não incluída**, a curva suavizada sugere a sua forma funcional (COLOSIMO; GIOLO, 2006, p. 172-173). Aqui, contra a **ordem de chegada** (1 a 938), ajustando um modelo só com o grupo: uma curva plana indica que não há tendência de calendário residual; uma curva inclinada indica que processos mais antigos/recentes têm mais/menos sentenças que o esperado, justificando o mês no modelo. É também o teste de tendência do calendário mencionado em 4.3.3.
- **Deviance** d̂_i = sinal(m̂_i)·√{−2[m̂_i + δ_i log(δ_i − m̂_i)]}: versão simétrica do martingal; valores com |d̂| > 2,5 apontam processos mal ajustados (eq. 5.11, p. 172-173).
- **dfbeta** Δβ̂_(i): variação no coeficiente do grupo quando o processo i é retirado (p. 173). Mede influência. O limite usual 2/√n vale para o dfbeta **padronizado** pelo erro-padrão do coeficiente (DFBETAS = Δβ̂_(i)/EP(β̂)); destacam-se os processos com |DFBETAS| > 2/√n.
''')

code(r'''
mart_a = cox_a.compute_residuals(sob[['T', 'E'] + X_BASE], kind='martingale')['martingale']
dev_b = cox_b.compute_residuals(sob[['T', 'E'] + X_AJ], kind='deviance')['deviance']
dfb_bruto = cox_b.compute_residuals(sob[['T', 'E'] + X_AJ], kind='delta_beta')
dfb_b = dfb_bruto / cox_b.standard_errors_[dfb_bruto.columns]          # DFBETAS = dfbeta / EP(β̂)
lp_b = cox_b.predict_log_partial_hazard(sob[X_AJ])

lim_dfb = 2 / np.sqrt(len(sob))
fig, axes = plt.subplots(2, 2, figsize=(13, 9.4))
ax = axes[0, 0]
ordem_m = sob.loc[mart_a.index, 'ordem'].values
ax.scatter(ordem_m, mart_a.values, s=6, alpha=0.3, color=CINZA, lw=0)
lw = lowess(mart_a.values, ordem_m, frac=0.3); ax.plot(lw[:, 0], lw[:, 1], color=TINTA, lw=2.5, label='Tendência (lowess)')
ax.axhline(0, color=TINTA_2, lw=0.8)
for m in MESES_SOB[1:]:
    x0 = sob.loc[sob.mes == m, 'ordem'].min()
    ax.axvline(x0, color=TINTA_2, lw=0.6, ls=':')
    ax.annotate(m, (x0, 1), xycoords=('data', 'axes fraction'), xytext=(2, -2), textcoords='offset points',
                fontsize=8, color=TINTA_2, va='top')
ax.set_xlabel('Ordem de chegada (1 a 938; linhas pontilhadas = início de cada mês)'); ax.set_ylabel('Resíduo martingal (modelo a)')
ax.set_title('Martingal × ordem de chegada (tendência de calendário)'); ax.legend(loc='lower left')

ax = axes[0, 1]
for g in ORDEM_GRUPO:
    ii = sob.loc[dev_b.index, 'grupo'] == g
    ax.scatter(lp_b.loc[dev_b.index][ii.values], dev_b.values[ii.values], s=8, alpha=0.35, color=CORES_GRUPO[g], lw=0, label=g)
ax.axhline(2.5, color=DESTAQUE, ls='--', lw=1.2, label='|d| = 2,5'); ax.axhline(-2.5, color=DESTAQUE, ls='--', lw=1.2)
ax.axhline(0, color=TINTA_2, lw=0.8)
ax.set_xlabel("Preditor linear x′β̂ (modelo b)"); ax.set_ylabel('Resíduo deviance')
ax.set_title(f'Deviance × preditor linear: {(dev_b.abs() > 2.5).sum()} processos com |d| > 2,5')
ax.set_ylim(-4.6, 3.0); ax.legend(loc='lower center', fontsize=8.5, ncol=4)

for ax, termo, mk in [(axes[1, 0], 'Presencial', 'o'), (axes[1, 1], 'Remota', 's')]:
    ax.scatter(sob.loc[dfb_b.index, 'ordem'], dfb_b[termo], s=8, alpha=0.5, marker=mk, color=CORES_GRUPO[termo], lw=0)
    ax.axhline(lim_dfb, color=DESTAQUE, ls='--', lw=1.2, label=f'± 2/√n = ± {fmt_br(lim_dfb, 3)}')
    ax.axhline(-lim_dfb, color=DESTAQUE, ls='--', lw=1.2)
    ax.axhline(0, color=TINTA_2, lw=0.8)
    ax.set_xlabel(ROTULOS['ordem_chegada'])
    ax.set_ylabel(f'DFBETAS de β̂ {termo}\n(variação ao retirar o processo / EP)')
    ax.set_title(f'Influência individual em β̂ ({ROTULO_TERMO[termo]}): '
                 f'{(dfb_b[termo].abs() > lim_dfb).sum()} acima do limite')
    ax.set_ylim(-lim_dfb * 1.6, lim_dfb * 1.6)
    ax.legend(loc='upper right', fontsize=8.5)
figura(fig, 'sob_cox_residuos', 'Resíduos do Cox: tendência de calendário no martingal, poucos atípicos e nenhum processo que mova β̂ mais que 0,1 EP',
       secao='4.5.4', nota='martingal do modelo (a), só com o grupo: curva decrescente = processos mais recentes com menos sentenças '
                           'do que o esperado (justifica o mês no modelo). Deviance e DFBETAS (dfbeta / EP) do modelo (b).')

print(f'Deviance |d| > 2,5: {(dev_b.abs() > 2.5).sum()} processos | |DFBETAS| > 2/√n (= {fmt_br(lim_dfb, 3)}): '
      f'Presencial {(dfb_b["Presencial"].abs() > lim_dfb).sum()}, Remota {(dfb_b["Remota"].abs() > lim_dfb).sum()}')
for _g in X_BASE:
    print(f'Maior |DFBETAS| ({_g}): {fmt_br(dfb_b[_g].abs().max(), 3)} (dfbeta bruto {fmt_br(dfb_bruto[_g].abs().max(), 4)}; '
          f'β̂ = {fmt_br(cox_b.params_[_g], 3)}, EP {fmt_br(cox_b.standard_errors_[_g], 3)})')
top = dfb_b[X_BASE].abs().max(axis=1).sort_values(ascending=False).head(5).index
_top = (sob.loc[top, ['processo', 'grupo', 'mes', 'tipo_desfecho', 'T', 'E']]
        .assign(dfbeta_Presencial=dfb_b.loc[top, 'Presencial'], dfbeta_Remota=dfb_b.loc[top, 'Remota'])
        .rename(columns={'processo': 'Processo', 'grupo': 'Grupo', 'mes': 'Mês', 'tipo_desfecho': 'Desfecho',
                         'T': 'Tempo (dias)', 'E': 'Sentença (δ)', 'dfbeta_Presencial': 'DFBETAS Presencial',
                         'dfbeta_Remota': 'DFBETAS Remota'})
        .reset_index(drop=True))
tabela(_top, 'sob_cox_influentes', 'Os cinco processos de maior influência (|DFBETAS|) nos coeficientes do grupo, modelo (b)',
       secao='4.5.4', formatos={'DFBETAS Presencial': 3, 'DFBETAS Remota': 3, 'Tempo (dias)': 'int', 'Sentença (δ)': 'int'},
       nota=f'DFBETAS = dfbeta / EP(β̂); limite de referência 2/√n = {fmt_br(lim_dfb, 3)}; processos acima dele: '
            f'{int((dfb_b[X_BASE].abs() > lim_dfb).any(axis=1).sum())}.')
''')

interp('sob_cox')

# =====================================================================
md(r'''
---

## 4.6 Modelos paramétricos de tempo de vida acelerado (AFT)

O modelo AFT escreve o **logaritmo do tempo** como uma regressão: log T = α + x′β + σν, isto é, T = exp(x′β)·T₀. As covariáveis **esticam ou encolhem** a escala do tempo, e exp(β) é a **razão de tempos** (TR): TR = 1,20 significa que os quantis do tempo até a sentença (inclusive a mediana) são 20% **maiores** no grupo (COLOSIMO; GIOLO, 2006, eq. 4.10, p. 122; interpretação na seção 4.4, p. 127-129; MORETTIN; SINGER, 2021, p. 254-255). É a apresentação mais intuitiva para gestores, e não depende da hipótese de riscos proporcionais, mas sim de uma **forma distribucional** para ν.

A escolha da distribuição **marginal** do tempo foi feita na Parte II; aqui ajustam-se as três famílias candidatas **condicionalmente** a grupo + mês:

- **Weibull**: risco monótono; é o único modelo que é ao mesmo tempo AFT e de riscos proporcionais (COLOSIMO; GIOLO, 2006, p. 198);
- **log-normal** e **log-logística**: risco que sobe e depois desce (p. 75-79).

Usa-se `tempo_pos` (os 38 tempos zero viram 0,5 dia, pois log 0 não existe). A comparação é pelo **AIC** (modelos não encaixados; p. 100-101), e a adequação pelos **resíduos de Cox-Snell** ê_i = −log Ŝ(t_i | x_i) (seção 4.3, p. 123-125). A mediana prevista por grupo é **padronizada** (média das curvas previstas sobre a distribuição observada dos meses), como em 4.5.1.
''')

code(r'''
X_AFT = X_BASE + COLS_MES
base_aft = sob[['T_pos', 'E'] + X_AFT]
AFTS = {'Weibull': WeibullAFTFitter(), 'Log-normal': LogNormalAFTFitter(), 'Log-logística': LogLogisticAFTFitter()}
for m in AFTS.values():
    m.fit(base_aft, 'T_pos', 'E')

tr_linhas, aic = [], {}
for nome, m in AFTS.items():
    t = tabela_hr(m, X_BASE, rotulo='Razão de tempos')
    t.insert(0, 'Modelo', nome)
    tr_linhas.append(t)
    aic[nome] = {'log-verossimilhança': m.log_likelihood_, 'nº parâmetros': len(m.params_), 'AIC': m.AIC_}
aic = pd.DataFrame(aic).T
aic['ΔAIC'] = aic['AIC'] - aic['AIC'].min()
TR_AFT = pd.concat(tr_linhas)
sob_tabela(TR_AFT.rename_axis('Termo').reset_index()[['Modelo', 'Termo', 'Razão de tempos', 'IC 95% inf.', 'IC 95% sup.', 'p (Wald)']],
           'sob_aft_tr', 'Razões de tempos dos grupos com AC vs. Controle nos três modelos AFT (ajustados por mês)',
           secao='4.6', casas=3, colunas_p=('p (Wald)',),
           nota='razão de tempos > 1 = tempo até a sentença mais longo que no Controle; IC 95% e p de Wald. Destaque: p < 0,05.')
sob_tabela(aic.rename_axis('Modelo'), 'sob_aft_aic', 'Comparação dos modelos AFT pelo AIC', secao='4.6', casas=1, destaque=None,
           formatos={'nº parâmetros': 'int'}, nota='ΔAIC = AIC − menor AIC; modelos não encaixados.')
MELHOR_AFT = aic['AIC'].idxmin()

# mediana padronizada por grupo
med_aft = {}
grade_aft = np.arange(1, 400)
for nome, m in AFTS.items():
    med_aft[nome] = {}
    for g in ORDEM_GRUPO:
        x_g = sob[X_AFT].copy(); x_g['Presencial'] = int(g == 'Presencial'); x_g['Remota'] = int(g == 'Remota')
        S_pad = m.predict_survival_function(x_g, times=grade_aft).mean(axis=1)
        med_aft[nome][g] = float(S_pad.index[np.argmax(S_pad.values <= 0.5)])
med_aft = pd.DataFrame(med_aft).T
med_aft.loc['Kaplan-Meier (não paramétrico)'] = [MEDIANAS[g] for g in ORDEM_GRUPO]
_ma = med_aft.copy(); _ma.columns = [str(c) for c in _ma.columns]
tabela(_ma.rename_axis('Modelo'), 'sob_aft_medianas', 'Mediana prevista do tempo até a sentença (dias), padronizada pela '
       'distribuição dos meses, comparada à do Kaplan-Meier', secao='4.6', casas=0)

fig, axes = plt.subplots(2, 2, figsize=(13, 10))
T_u = np.unique(sob['T_pos'])
for ax, (nome, m) in zip(axes.flat[:3], AFTS.items()):
    ch = m.predict_cumulative_hazard(base_aft[X_AFT], times=T_u)       # (tempos × processos)
    pos = np.searchsorted(T_u, sob['T_pos'].values)
    ei = ch.values[pos, np.arange(len(sob))]
    cox_snell_plot(ax, ei, sob['E'].values, f'Cox-Snell do AFT {nome} (AIC = {fmt_br(m.AIC_, 0)})')
ax = axes.flat[3]
_tr = TR_AFT.copy()
_tr.index = [f'{n}: {t.replace(" × Controle", "")}' for n, t in zip(_tr['Modelo'], _tr.index)]
floresta(ax, _tr, rotulo='Razão de tempos', cor_de=lambda n: CORES_GRUPO['Presencial'] if 'presencial' in n else CORES_GRUPO['Remota'],
         xlabel='Razão de tempos vs. Controle (IC 95%; escala log)', ticks=[0.8, 0.9, 1, 1.2, 1.4, 1.6])
ax.set_xlim(0.72, 2.6)
for yi in (1.5, 3.5):
    ax.axhline(yi, color=GRADE, lw=0.8)
ax.set_title('Razões de tempos (> 1 = mais lento que o Controle)')
figura(fig, 'sob_aft', 'Os três AFT indicam tempos 10% a 25% mais longos com AC, mas nenhum se ajusta bem aos dados',
       secao='4.6', nota='Cox-Snell: ê = −log Ŝ(t | x) de cada modelo (grupo + mês; zeros = 0,5 dia); afastamento da reta y = x = '
                         'falta de ajuste. Painel inferior direito: razões de tempos com IC 95% e p de Wald.')
''')

interp('sob_aft')

# =====================================================================
md(r'''
---

## 4.7 Riscos competitivos

Até aqui, o evento foi "sentença de qualquer tipo". Mas uma sentença homologatória de acordo, um julgamento de mérito e uma extinção sem resolução do mérito são **resultados jurídicos muito diferentes**, produzidos por mecanismos diferentes. Se a AC obrigatória acelera certos desfechos e atrasa outros, a comparação do tempo total pode esconder **mecanismos opostos**. A ferramenta adequada é a de **riscos competitivos**: cada processo termina por exatamente uma de várias causas, e a ocorrência de uma impede as demais (PUTTER; FIOCCO; GESKUS, 2007; AUSTIN; LEE; FINE, 2016). Os livros-texto da disciplina não tratam do tema (COLOSIMO; GIOLO, 2006 cobrem censura, truncamento e fragilidade, mas não a incidência acumulada).

**Duas quantidades, duas perguntas.**

1. **Risco causa-específico** h_k(t): taxa instantânea de desfechos do tipo k entre os processos **ainda pendentes**. Estimado pelo Cox causa-específico (as outras causas são censuradas). Pergunta **etiológica**: "o rito acelera a ocorrência de acordos entre os processos em curso?".
2. **Função de incidência acumulada (FIA)** F_k(t) = P(T ≤ t, causa = k): proporção de **todos** os processos que terminou pela causa k até t. Estimada por **Aalen-Johansen** (AALEN; JOHANSEN, 1978): F̂_k(t) = Σ_{t_j ≤ t} Ŝ(t_{j−1}) d_kj/n_j, em que Ŝ é o KM de "qualquer desfecho". As FIA somadas mais Ŝ(t) dão 1. A regressão correspondente é a de **Fine e Gray** (1999). Pergunta **prognóstica/gestão**: "que fração dos processos do rito X termina em acordo até 90 dias?".

**Por que não usar 1 − KM censurando as outras causas.** O 1 − KM de uma causa trata quem saiu por outra causa como se ainda pudesse sofrer aquela causa no futuro: estima uma probabilidade num mundo hipotético sem os demais desfechos e, por isso, **superestima** a incidência real.

### 4.7.1 Redistribuição como risco competitivo da sentença

Primeiro, o caso simples com duas causas: **sentença** (708) e **redistribuição** (24). Compara-se a FIA de sentença (Aalen-Johansen, redistribuição como competidora) com o 1 − KM da análise principal (redistribuição censurada). A diferença entre as duas curvas é o **viés de censurar a redistribuição**.
''')

code(r'''
def cif_statsmodels(T, K):
    """FIA de Aalen-Johansen com EP (statsmodels, sem jitter). Retorna dict causa -> DataFrame(t, F, inf, sup)."""
    ci = CumIncidenceRight(np.asarray(T, float), np.asarray(K, int))
    out = {}
    for j, k in enumerate(sorted(set(np.asarray(K, int)) - {0})):
        F = ci.cinc[j]; se = ci.cinc_se[j]
        out[k] = pd.DataFrame({'t': ci.times, 'F': F, 'inf': np.clip(F - 1.96 * se, 0, 1), 'sup': np.clip(F + 1.96 * se, 0, 1)})
    return out

def F_em(df_cif, t):
    d = df_cif[df_cif.t <= t]
    return d.iloc[-1] if len(d) else pd.Series({'t': t, 'F': 0.0, 'inf': 0.0, 'sup': 0.0})

fig, axes = plt.subplots(2, 2, figsize=(13, 9.4))
vies = []
for ax, g in zip(axes.flat[:3], ORDEM_GRUPO):
    s = sob[sob.grupo == g]
    S_g, cif_g = aj_grade(s['T'], s['CR'], causas=(1, 2))
    Skm, _ = aj_grade(s['T'], s['E'])
    tg = np.arange(0, 275)
    ax.step(tg, 1 - Skm[tg], where='post', color=TINTA, ls='--', lw=1.6, label='1 − KM (redistribuição censurada)')
    ax.step(tg, cif_g[1][tg], where='post', color=CORES_GRUPO[g], lw=2.2, label='FIA de sentença (Aalen-Johansen)')
    ax.step(tg, cif_g[2][tg], where='post', color=CORES_DESFECHO['Redistribuição'], lw=2, label='FIA de redistribuição')
    ax.set_title(ROTULO_GRUPO[g]); ax.set_xlabel(ROTULOS['dias']); ax.set_xlim(0, 274); ax.set_xticks(np.arange(0, 271, 30))
    ax.set_ylim(0, 1.02); eixo_pct(ax); ax.set_ylabel('Proporção acumulada dos processos')
    ax.grid(axis='both', visible=True)
    ax.legend(fontsize=8.5, loc='center right')
    for t in [90, 180]:
        vies.append({'Grupo': g, 't (dias)': t, '1 − KM': 1 - Skm[t], 'FIA sentença (AJ)': cif_g[1][t],
                     'FIA redistribuição': cif_g[2][t], 'Viés (p.p.)': 100 * ((1 - Skm[t]) - cif_g[1][t])})
VIES_CR = pd.DataFrame(vies)
ax = axes.flat[3]
_vb = VIES_CR.pivot(index='t (dias)', columns='Grupo', values='Viés (p.p.)')[ORDEM_GRUPO]
_vb.index = [f'{t} dias' for t in _vb.index]
barras_agrupadas(ax, _vb, cores=CORES_GRUPO, rotular=True, fmt=lambda v: fmt_br(v, 1), legenda=False,
                 ylabel='Viés do 1 − KM (pontos percentuais)', xlabel='Horizonte')
ax.set_title('Superestimação da sentença pelo 1 − KM')
ax.legend(handles=[Patch(color=CORES_GRUPO[g], label=g) for g in ORDEM_GRUPO], loc='upper left')
figura(fig, 'sob_cr_redistribuicao', 'Censurar a redistribuição superestima a proporção sentenciada em apenas 1 a 3 p.p.',
       secao='4.7.1', nota='FIA = função de incidência acumulada (Aalen-Johansen), com a redistribuição como risco competitivo. '
                           'Viés = (1 − KM) − FIA de sentença.')
sob_tabela(VIES_CR, 'sob_cr_vies', 'Proporção sentenciada aos 90 e 180 dias: 1 − KM × FIA de Aalen-Johansen', secao='4.7.1',
           casas=3, destaque=None, formatos={'t (dias)': 'int', '1 − KM': 'pct', 'FIA sentença (AJ)': 'pct',
                                             'FIA redistribuição': 'pct', 'Viés (p.p.)': 2})
''')

md(r'''
### 4.7.2 O tipo de sentença como desfecho competitivo: FIA por grupo

Agora a análise substantiva principal: quatro causas de saída — **homologação de acordo** (1), **julgamento de mérito** (2), **extinção sem mérito** (3) e **redistribuição** (4) —, mais a censura administrativa. A figura empilhada mostra, para cada grupo, como a massa de processos se distribui ao longo do tempo: a faixa de cada cor é a FIA da causa, e o que sobra no topo (cinza) é Ŝ(t), a proporção ainda pendente. A segunda figura sobrepõe os três grupos em cada causa, com IC 95% (erro-padrão do `statsmodels.CumIncidenceRight`, sem o *jitter* que o `AalenJohansenFitter` do `lifelines` introduz nos empates).

**Hipótese a investigar** (seção 3 e E21): a AC obrigatória **acelera** as extinções sem mérito — a ausência do autor à audiência de conciliação extingue o processo (art. 51, I, da Lei 9.099/1995) — e os acordos, mas **atrasa** os julgamentos de mérito, que passam a esperar a audiência antes da contestação e da conclusão para sentença. Se for assim, a comparação do tempo total mistura um efeito que encurta com outro que alonga.
''')

code(r'''
CAUSAS_SENT = (1, 2, 3, 4)
cif_sm = {g: cif_statsmodels(sob.loc[sob.grupo == g, 'T'], sob.loc[sob.grupo == g, 'K']) for g in ORDEM_GRUPO}
tg = np.arange(0, 275)
ORDEM_PILHA = [3, 1, 2, 4]         # sem mérito (precoce), homologação, mérito, redistribuição
fig, axes = plt.subplots(2, 2, figsize=(13, 9.4))
for ax, g in zip(axes.flat[:3], ORDEM_GRUPO):
    s = sob[sob.grupo == g]
    S_g, cif_g = aj_grade(s['T'], s['K'], causas=CAUSAS_SENT)
    camadas = [cif_g[k][tg] for k in ORDEM_PILHA] + [S_g[tg]]
    ax.stackplot(tg, *camadas, step='post', colors=[CORES_DESFECHO[CAUSAS[k]] for k in ORDEM_PILHA] + [CORES_DESFECHO['Ativo']],
                 alpha=0.9, edgecolor='white', lw=0.3)
    ax.set_title(f'{ROTULO_GRUPO[g]} (n = {len(s)})'); ax.set_xlabel(ROTULOS['dias']); ax.set_xlim(0, 274); ax.set_ylim(0, 1)
    ax.set_xticks(np.arange(0, 271, 30)); eixo_pct(ax); ax.set_ylabel('Processos do grupo (%)')
    ax.grid(visible=False)
axes.flat[3].axis('off')
axes.flat[3].legend(handles=[Patch(color=CORES_DESFECHO['Ativo'], label='Ainda sem sentença, Ŝ(t)')] +
                    [Patch(color=CORES_DESFECHO[CAUSAS[k]], label=ROTULO_DESFECHO[CAUSAS[k]]) for k in ORDEM_PILHA[::-1]],
                    loc='center', title='Faixa (de cima para baixo)', fontsize=10, title_fontsize=10)
figura(fig, 'sob_cif_empilhada', 'Com AC obrigatória, a faixa do julgamento de mérito encolhe e chega mais tarde, e a da extinção '
       'sem mérito cresce', secao='4.7.2', nota='incidência acumulada de cada tipo de desfecho (Aalen-Johansen) empilhada; '
                                                'a soma das faixas com Ŝ(t) é 100% em cada t.')

fig, axes = plt.subplots(2, 2, figsize=(13, 9.4), sharex=True)
for ax, k in zip(axes.flat, CAUSAS_SENT):
    for g in ORDEM_GRUPO:
        d = cif_sm[g][k]
        ax.step(d.t, d.F, where='post', color=CORES_GRUPO[g], lw=2, label=ROTULO_GRUPO[g])
        ax.fill_between(d.t, d['inf'], d['sup'], step='post', color=CORES_GRUPO[g], alpha=0.12, lw=0)
    ax.set_title(f'{ROTULO_DESFECHO[CAUSAS[k]]}'); ax.set_xlim(0, 274); ax.set_xticks(np.arange(0, 271, 30))
    ax.set_ylim(0, None); eixo_pct(ax); ax.grid(axis='both', visible=True)
    ax.set_ylabel('Incidência acumulada F̂_k(t) (IC 95%)')
for ax in axes[1]:
    ax.set_xlabel(ROTULOS['dias'])
axes[0, 0].legend(loc='upper left', fontsize=8.5)
figura(fig, 'sob_cif_causas', 'A AC obrigatória reduz e atrasa o julgamento de mérito, e antecipa extinções sem mérito e acordos',
       secao='4.7.2', nota='FIA de Aalen-Johansen por grupo, com IC 95% (EP do statsmodels CumIncidenceRight). Escalas verticais '
                           'diferentes entre os painéis.')

linhas = []
for k in CAUSAS_SENT:
    for t in [30, 60, 90, 120, 180]:
        linha = {'Desfecho': CAUSAS[k], 't (dias)': t}
        for g in ORDEM_GRUPO:
            r = F_em(cif_sm[g][k], t)
            linha[g] = f"{pct_br(r['F'])} ({pct_br(r['inf'])}–{pct_br(r['sup'])})"
        linhas.append(linha)
CIF_TAB = pd.DataFrame(linhas).set_index(['Desfecho', 't (dias)'])
tabela(CIF_TAB.reset_index(), 'sob_cif_tabela', 'Incidência acumulada de cada tipo de desfecho por grupo, F̂_k(t) (IC 95%)',
       secao='4.7.2', formatos={'t (dias)': 'int', **{g: 'texto' for g in ORDEM_GRUPO}},
       nota='Aalen-Johansen (statsmodels CumIncidenceRight); IC 95% pela aproximação normal, truncado em [0, 1].')
''')

md(r'''
### 4.7.3 Teste de igualdade das FIA entre grupos (tipo Gray, por permutação)

O teste de Gray (1988) compara as FIA de uma causa entre k grupos. Ele não existe no `lifelines` nem no `statsmodels` (e os pacotes `pycmprsk`/`pycrr` não estão instalados). Implementa-se um **teste de permutação** com a mesma hipótese nula:

- H₀: F_k,Controle(t) = F_k,Presencial(t) = F_k,Remota(t) para todo t ≤ τ;
- estatística: D_k = Σ_g n_g ∫₀^τ [F̂_k,g(t) − F̂_k(t)]² dt, a distância quadrática integrada entre a FIA de cada grupo e a FIA combinada, com τ = 180 dias;
- distribuição sob H₀: 2.000 permutações dos rótulos de grupo **dentro de cada mês de distribuição**. A permutação estratificada respeita o desenho (o sorteio foi feito ao longo do calendário) e preserva a estrutura de censura de cada mês, que é o que torna a censura comparável entre os rótulos permutados. Sob H₀ de nenhum efeito do rito, os rótulos são permutáveis dentro do mês: o p-valor é exato (a menos do erro de Monte Carlo).

São 4 testes (um por causa), corrigidos por Holm. **Gráfico do teste:** distribuição de permutação de D_k com o valor observado.
''')

code(r'''
def estat_gray_perm(T, K, G, k, tau=180, grupos=(0, 1, 2)):
    _, cif_all = aj_grade(T, K, causas=CAUSAS_SENT)
    Fbar = cif_all[k][:tau]
    D = 0.0
    for g in grupos:
        m = G == g
        _, cg = aj_grade(T[m], K[m], causas=CAUSAS_SENT)
        D += m.sum() * np.sum((cg[k][:tau] - Fbar) ** 2)
    return D

B_PERM = 2000
rng_perm = np.random.default_rng(SEMENTE + 47)
T_i, K_i, G_i, M_i = sob['T'].values.astype(int), sob['K'].values.astype(int), sob['grupo'].cat.codes.values, sob['mes_cod'].values
obs_D = {k: estat_gray_perm(T_i, K_i, G_i, k) for k in CAUSAS_SENT}
perm_D = {k: np.empty(B_PERM) for k in CAUSAS_SENT}
idx_mes = [np.where(M_i == m)[0] for m in np.unique(M_i)]
for b in range(B_PERM):
    Gp = G_i.copy()
    for ii in idx_mes:
        Gp[ii] = rng_perm.permutation(G_i[ii])
    for k in CAUSAS_SENT:
        perm_D[k][b] = estat_gray_perm(T_i, K_i, Gp, k)
gray = pd.DataFrame({'Desfecho': [CAUSAS[k] for k in CAUSAS_SENT],
                     'D observado': [obs_D[k] for k in CAUSAS_SENT],
                     'p (permutação)': [(1 + (perm_D[k] >= obs_D[k]).sum()) / (B_PERM + 1) for k in CAUSAS_SENT]}).set_index('Desfecho')
gray['p (Holm, 4 testes)'] = multipletests(gray['p (permutação)'], method='holm')[1]
sob_tabela(gray, 'sob_gray_permutacao', 'Teste de igualdade das FIA entre os três grupos (tipo Gray, por permutação no mês)',
           secao='4.7.3', casas=2, colunas_p=('p (permutação)', 'p (Holm, 4 testes)'),
           nota=f'D = Σ_g n_g ∫₀^180 [F̂_k,g(t) − F̂_k(t)]² dt; {fmt_br(B_PERM, 0)} permutações dos rótulos de grupo dentro do mês. '
                'Destaque: p de Holm < 0,05.')

fig, axes = plt.subplots(2, 2, figsize=(12, 8.4))
for ax, k in zip(axes.flat, CAUSAS_SENT):
    ax.hist(perm_D[k], bins=40, color=CORES_DESFECHO[CAUSAS[k]], alpha=0.8, edgecolor='white', lw=0.4)
    ax.axvline(obs_D[k], color=DESTAQUE, lw=2.2)
    ax.set_title(ROTULO_DESFECHO[CAUSAS[k]])
    ax.set_xlabel(f'Estatística D (distância entre as FIA; {fmt_br(B_PERM, 0)} permutações)')
    ax.set_ylabel('Número de permutações')
    ax.grid(axis='x', visible=False)
    r = gray.loc[CAUSAS[k]]
    lado = 'upper right' if obs_D[k] < np.percentile(perm_D[k], 60) else 'upper center'
    anotar_teste(ax, texto_teste('Permutação tipo Gray', f'D = {fmt_br(r["D observado"], 2)}', r['p (permutação)'],
                                 f'p Holm = {fmt_p(r["p (Holm, 4 testes)"])}'), loc=lado)
figura(fig, 'sob_gray_permutacao', 'A distribuição do mérito no tempo difere claramente entre os grupos; a da extinção sem mérito, '
       'de forma mais fraca', secao='4.7.3', nota='barras = distribuição de D sob H₀ (permutações); linha laranja = D observado. p = proporção de permutações '
                                     'com D ≥ D observado (com correção +1); Holm sobre as 4 causas.')
''')

md(r'''
### 4.7.4 Cox causa-específico por tipo de desfecho

Para cada causa k, ajusta-se um Cox (grupo + mês, Efron) em que o evento é "desfecho do tipo k" e os desfechos de outros tipos são **censurados** no seu tempo. O HR causa-específico responde: entre os processos ainda pendentes no dia t, quanto maior (HR > 1) ou menor (HR < 1) é a taxa diária de desfechos do tipo k no grupo com AC em relação ao Controle? Censurar as outras causas é correto para o risco causa-específico (não para a FIA): o risco causa-específico é definido justamente entre os que ainda estão em risco de todas as causas.
''')

code(r'''
X_CS = X_BASE + COLS_MES
cs_tabs, cs_modelos = [], {}
for k in CAUSAS_SENT:
    base_k = sob[['T'] + X_CS].assign(Ek=(sob['K'] == k).astype(int))
    m = CoxPHFitter().fit(base_k, 'T', 'Ek')
    cs_modelos[k] = m
    t = tabela_hr(m, X_BASE); t.insert(0, 'Desfecho', CAUSAS[k]); t.insert(1, 'eventos', int(base_k['Ek'].sum()))
    cs_tabs.append(t)
HR_CS = pd.concat(cs_tabs)
sob_tabela(HR_CS.rename_axis('Termo').reset_index()[['Desfecho', 'eventos', 'Termo', 'HR', 'IC 95% inf.', 'IC 95% sup.', 'p (Wald)']]
           .rename(columns={'eventos': 'Eventos'}), 'sob_cox_causa_especifica',
           'Cox causa-específico por tipo de desfecho: razão de risco dos grupos com AC vs. Controle (ajustado por mês)',
           secao='4.7.4', casas=3, colunas_p=('p (Wald)',), formatos={'Eventos': 'int'},
           nota='desfechos de outros tipos censurados no seu tempo; HR > 1 = desfecho mais frequente por dia entre os pendentes. '
                'Destaque: p < 0,05.')
''')

md(r'''
### 4.7.5 Modelo de Fine-Gray (subdistribuição) implementado à mão

O modelo de **Fine e Gray (1999)** modela diretamente a FIA: o risco da **subdistribuição** λ̄_k(t) = −d log[1 − F_k(t)]/dt segue um modelo de riscos proporcionais, λ̄_k(t | x) = λ̄_k0(t) exp(x′γ). O exp(γ) (sHR) > 1 indica **maior incidência acumulada** da causa k (mais processos terminando por k até cada t). A diferença em relação ao Cox causa-específico está no **conjunto de risco**: no Fine-Gray, quem saiu por **outra causa** continua no conjunto de risco da causa k (com peso), porque não pode mais ter a causa k "a tempo".

O modelo não está no `lifelines` nem no `statsmodels`. Duas implementações equivalentes:

1. **Censura completamente conhecida** (FINE; GRAY, 1999, seção 3). Aqui toda censura é administrativa, e o tempo potencial de censura de **todos** os processos é conhecido (C_i = `followup` = 07/10/2026 − distribuição). Nesse caso, o estimador de Fine-Gray é exato e simples: quem teve desfecho competitivo permanece no conjunto de risco **até o seu C_i**, com peso 1. Basta um Cox com o tempo do competidor substituído por C_i e o evento k = 0. Erros-padrão robustos (sanduíche), como recomendam os autores.
2. **Ponderação IPCW** (GESKUS, 2011), a forma geral usada pelo `survival::finegray()` do R. Quem tem desfecho competitivo em T_i é mantido em risco depois de T_i em episódios (início, fim] entre os tempos de censura observados, com peso w_i(t) = Ĝ(t)/Ĝ(T_i), sendo Ĝ o KM da distribuição de censura (censura como "evento"). Cox ponderado em formato de contagem, com variância robusta agrupada por processo (`cluster_col`).

As duas devem dar **estimativas pontuais** muito próximas; a versão 2 é aplicada, como conferência, aos dois desfechos centrais (mérito e sem mérito), porque o ajuste ponderado com variância agrupada sobre ~30 mil episódios é lento. A versão 1 é a principal, porque usa a informação exata do desenho. Covariáveis: grupo + mês (como no Cox causa-específico).

**Erros-padrão.** O EP sanduíche das duas versões ignora a incerteza de estimar Ĝ e, na versão 2, o `lifelines` o calcula sobre pesos fracionários num formato de contagem, caso em que ele não é confiável (ver a conferência logo abaixo). Por isso a inferência final do Fine-Gray usa um **EP por *bootstrap*** não paramétrico da versão 1 (reamostragem de processos dentro de cada grupo), com IC normal na escala do log-sHR.
''')

code(r'''
def fine_gray_censura_conhecida(df, k, X):
    """Fine-Gray com tempos potenciais de censura conhecidos (followup)."""
    b = df[['T', 'K', 'FU'] + X].copy()
    compet = (b['K'] != k) & (b['K'] != 0)
    b['T_fg'] = np.where(compet, b['FU'], b['T'])
    b['E_fg'] = (b['K'] == k).astype(int)
    return CoxPHFitter().fit(b[['T_fg', 'E_fg'] + X], 'T_fg', 'E_fg', robust=True)


def fine_gray_ipcw(df, k, X):
    """Fine-Gray por IPCW (Geskus, 2011), como survival::finegray. Tempos deslocados +1 dia (start < stop)."""
    b = df[['T', 'K'] + X].copy().reset_index(drop=True)
    b['id'] = np.arange(len(b))
    T1 = b['T'].values + 1.0
    kmG = KaplanMeierFitter().fit(T1, (b['K'] == 0).astype(int))     # censura como "evento"
    G = kmG.survival_function_.iloc[:, 0]
    G_t, G_v = G.index.values, G.values
    G_em = lambda t: G_v[np.searchsorted(G_t, t, side='right') - 1]
    cortes = np.unique(T1[b['K'] == 0])
    linhas = [pd.DataFrame({'id': b['id'], 'start': 0.0, 'stop': T1, 'ev': (b['K'] == k).astype(int).values, 'w': 1.0})]
    comp = b.index[(b['K'] != k) & (b['K'] != 0)]
    ext = []
    for i in comp:
        Ti = T1[i]; Gi = G_em(Ti)
        cs = cortes[cortes > Ti]
        inicios = np.concatenate([[Ti], cs[:-1]]) if len(cs) else np.array([])
        for a_, b_ in zip(inicios, cs):
            ext.append((i, a_, b_, 0, G_em(a_) / Gi))
    linhas.append(pd.DataFrame(ext, columns=['id', 'start', 'stop', 'ev', 'w']))
    long = pd.concat(linhas, ignore_index=True).merge(b[['id'] + X], on='id')
    long = long[long['w'] > 0]
    m = CoxPHFitter().fit(long[['start', 'stop', 'ev', 'w', 'id'] + X], 'stop', 'ev', entry_col='start',
                          weights_col='w', cluster_col='id', robust=True)
    return m, len(long)


fg_tabs, FG_MODELOS, FG_IPCW = [], {}, {}
for k in CAUSAS_SENT:
    m1 = fine_gray_censura_conhecida(sob, k, X_CS)
    FG_MODELOS[k] = m1
    versoes = [('censura conhecida', m1)]
    if k in (2, 3):          # conferência IPCW só para os dois desfechos centrais (cada ajuste leva ~1–2 min)
        m2, n_long = fine_gray_ipcw(sob, k, X_CS)
        FG_IPCW[k] = m2
        versoes.append((f'IPCW ({n_long:,} episódios)'.replace(',', '.'), m2))
    for nome, m in versoes:
        t = tabela_hr(m, X_BASE, rotulo='sHR'); t.insert(0, 'Desfecho', CAUSAS[k]); t.insert(1, 'Implementação', nome)
        fg_tabs.append(t)
SHR_FG = pd.concat(fg_tabs)
sob_tabela(SHR_FG.rename_axis('Termo').reset_index()[['Desfecho', 'Implementação', 'Termo', 'sHR', 'IC 95% inf.', 'IC 95% sup.', 'p (Wald)']],
           'sob_fine_gray', 'Modelo de Fine-Gray por tipo de desfecho: razão de riscos da subdistribuição (sHR) vs. Controle',
           secao='4.7.5', casas=3, colunas_p=('p (Wald)',),
           nota='sHR > 1 = maior incidência acumulada do desfecho; EP robusto (sanduíche) do lifelines. Ajustado por mês. '
                'Destaque: p < 0,05. A inferência final usa o EP bootstrap da tabela seguinte.')
''')

md(r'''
**Conferência dos erros-padrão e contraste entre as modalidades.** A tabela seguinte compara, para os três tipos de sentença, o EP de cada log-sHR por três caminhos: o sanduíche da versão 1, o sanduíche da versão 2 (IPCW, só mérito e sem mérito) e o *bootstrap* da versão 1 (reamostragem de processos dentro de cada grupo). Ela traz também o contraste **AC remota × AC presencial** (exp(γ_Remota − γ_Presencial)), que é o teste direto da pergunta "as duas modalidades mudam de forma diferente o tipo de desfecho?". Comparar apenas cada modalidade com o Controle, e concluir pela diferença porque um sHR é significativo e o outro não, seria um erro (a diferença entre "significativo" e "não significativo" não é, ela própria, significativa). IC e p finais: aproximação normal com o EP *bootstrap*.
''')

code(r'''
B_FG = 500
rng_fg = np.random.default_rng(SEMENTE + 75)
CONTRASTES_FG = {'AC presencial × Controle': np.array([1.0, 0.0]), 'AC remota × Controle': np.array([0.0, 1.0]),
                 'AC remota × AC presencial': np.array([-1.0, 1.0])}
idx_grupo = [np.where(sob.grupo == g)[0] for g in ORDEM_GRUPO]
_base_fg = sob[['T', 'K', 'FU'] + X_CS].reset_index(drop=True)
linhas_fg = []
SHR_FG_BOOT = {}
for k in (1, 2, 3):
    m1 = FG_MODELOS[k]
    beta = m1.params_[X_BASE].values
    m2 = FG_IPCW.get(k)
    # EP sanduíche do contraste Remota × Presencial: reajuste com a Presencial como referência (o lifelines não guarda
    # a matriz de covariância robusta, só os EPs robustos de cada termo)
    _ref = sob.assign(Controle_d=(sob.grupo == 'Controle').astype(int))
    m1_ref = fine_gray_censura_conhecida(_ref, k, ['Controle_d', 'Remota'] + COLS_MES)
    ep_rob = {'AC presencial × Controle': m1.standard_errors_['Presencial'], 'AC remota × Controle': m1.standard_errors_['Remota'],
              'AC remota × AC presencial': m1_ref.standard_errors_['Remota']}
    ep_ipcw = ({'AC presencial × Controle': m2.standard_errors_['Presencial'], 'AC remota × Controle': m2.standard_errors_['Remota']}
               if m2 is not None else {})
    boot = np.empty((B_FG, 2))
    for b in range(B_FG):
        ii = np.concatenate([rng_fg.choice(ix, len(ix), replace=True) for ix in idx_grupo])
        bb = _base_fg.iloc[ii]
        compet = (bb['K'] != k) & (bb['K'] != 0)
        dfb = pd.DataFrame({'T_fg': np.where(compet, bb['FU'], bb['T']), 'E_fg': (bb['K'] == k).astype(int).values})
        dfb[X_CS] = bb[X_CS].values
        boot[b] = CoxPHFitter().fit(dfb, 'T_fg', 'E_fg').params_[X_BASE].values
    SHR_FG_BOOT[k] = boot
    for nome_c, c in CONTRASTES_FG.items():
        est = c @ beta
        ep_bs = (boot @ c).std(ddof=1)
        linhas_fg.append({'Desfecho': CAUSAS[k], 'Contraste': nome_c, 'sHR': np.exp(est),
                          'EP robusto (v. 1)': ep_rob[nome_c], 'EP robusto IPCW (v. 2)': ep_ipcw.get(nome_c, np.nan),
                          'EP bootstrap (v. 1)': ep_bs,
                          'IC 95% inf. (bootstrap)': np.exp(est - 1.96 * ep_bs), 'IC 95% sup. (bootstrap)': np.exp(est + 1.96 * ep_bs),
                          'p (bootstrap)': 2 * stats.norm.sf(abs(est / ep_bs))})
FG_FINAL = pd.DataFrame(linhas_fg)
sob_tabela(FG_FINAL, 'sob_fine_gray_bootstrap',
           'Fine-Gray (censura conhecida): erros-padrão do log-sHR por três caminhos e inferência final por bootstrap, '
           'incluindo o contraste AC remota × AC presencial', secao='4.7.5', casas=3, colunas_p=('p (bootstrap)',),
           destaque='p (bootstrap)',
           nota=f'EP na escala do log-sHR. Bootstrap: {fmt_br(B_FG, 0)} reamostras de processos dentro de cada grupo; IC 95% = '
                'exp(log-sHR ± 1,96·EP bootstrap). EP robusto = sanduíche do lifelines (o do contraste remota × presencial vem do '
                'reajuste com a Presencial como referência). – = IPCW não ajustado (homologação) ou contraste não calculado. Destaque: p < 0,05.')
''')

md(r'''
**Gráfico dos dois modelos.** Para cada tipo de desfecho, o HR causa-específico (Cox) e o sHR de Fine-Gray (censura conhecida) dos dois grupos com AC em relação ao Controle. Quando os dois apontam na mesma direção, o rito muda tanto a **velocidade** daquele desfecho entre os pendentes quanto a **fração** de processos que termina por ele.
''')

code(r'''
fig, axes = plt.subplots(2, 2, figsize=(14, 7.6), sharex=True)
for ax, k in zip(axes.flat, CAUSAS_SENT):
    cs = HR_CS[HR_CS.Desfecho == CAUSAS[k]].rename(columns={'HR': 'v'})
    fg = SHR_FG[(SHR_FG.Desfecho == CAUSAS[k]) & (SHR_FG['Implementação'] == 'censura conhecida')].rename(columns={'sHR': 'v'})
    linhas_f, cores_f, mks_f = [], {}, {}
    for termo in cs.index:
        for tab_, nome, mk in [(cs, 'Cox causa-específico', 'o'), (fg, 'Fine-Gray', 's')]:
            rot = f"{termo.split(' ×')[0].replace('AC ', '')}: {nome}"
            linhas_f.append(tab_.loc[termo, ['v', 'IC 95% inf.', 'IC 95% sup.', 'p (Wald)']].rename(rot))
            cores_f[rot] = COR_TERMO[termo]; mks_f[rot] = mk
    floresta(ax, pd.DataFrame(linhas_f), rotulo='v', cor_de=cores_f.get, marcadores=mks_f.get,
             xlabel='HR / sHR vs. Controle (IC 95%; escala log)', ticks=[0.25, 0.5, 1, 2, 4])
    ax.axhline(1.5, color=GRADE, lw=0.8)
    ax.set_xlim(0.22, 12)
    ax.set_title(f'{ROTULO_DESFECHO[CAUSAS[k]]} ({int(cs["eventos"].iloc[0])} eventos)')
for ax in axes[0]:
    ax.set_xlabel('')
figura(fig, 'sob_cr_floresta', 'Com AC obrigatória, menos processos terminam em mérito e mais em extinção sem mérito e em acordo '
       '(sem diferença demonstrada entre as duas modalidades)', secao='4.7.5',
       nota='● = HR causa-específico (Cox, outras causas censuradas); ■ = sHR de Fine-Gray (censura conhecida). Ambos ajustados '
            'por mês; IC 95% e p de Wald. > 1 = mais desfechos desse tipo que no Controle.')
''')

interp('sob_cr')

# =====================================================================
md(r'''
---

## 4.8 Subconjunto com AC realizada: modalidade, técnica e audiência híbrida

**Atenção ao que esta análise pode e não pode dizer.** A AC só ocorre nos grupos com AC obrigatória (no Controle não houve nenhuma: zero estrutural), e mesmo neles só para os processos que **chegaram vivos** até a audiência. Restringir a análise a quem teve AC é **condicionar numa variável posterior ao sorteio**:

- quem teve AC "sobreviveu" (sem sentença, sem redistribuição, sem extinção precoce) até a data da audiência. O tempo entre a distribuição e a AC é **tempo imortal** para esse subconjunto: um processo não pode ter sentença antes de entrar nele. Comparar com processos sem AC daria uma vantagem artificial de sobrevivência a quem teve AC;
- a realização da AC pode depender de características do processo (partes presentes, interesse em conciliar), que diferem entre presencial e remota. A comparação Presencial × Remota dentro do subconjunto **não é mais protegida pelo sorteio**: é observacional.

A solução canônica é a **análise de *landmark***: escolher um tempo L, manter apenas quem ainda está em risco em L e classificar pela situação em L. Ela exige a **data da AC**, que a planilha não registra; o tempo é medido desde a distribuição. Por isso, as comparações abaixo restringem-se a processos que tiveram AC (todos passaram pelo tempo imortal) e se leem como **descritivas/associativas**. A técnica de conciliação, essa sim, foi **sorteada** entre as audiências realizadas: a comparação entre técnicas é a mais próxima de um contraste causal neste subconjunto (com a ressalva de que a técnica só "existe" para quem teve AC).

### 4.8.1 Presencial × Remota entre os processos com AC realizada
''')

code(r'''
ac = sob[(sob.grupo != 'Controle') & (sob['ac_realizada'] == True)].copy()
ac['grupo2'] = ac['grupo'].astype(str)
print(f'Processos com AC realizada: {len(ac)} (Presencial {(ac.grupo2 == "Presencial").sum()}, Remota {(ac.grupo2 == "Remota").sum()}); '
      f'sentenças {ac.E.sum()}')
_ct = pd.crosstab(ac['grupo2'], ac['tipo_desfecho'].astype(str))
_ct = _ct[[c for c in ORDEM_DESFECHO if c in _ct.columns]].rename(columns=ROTULO_DESFECHO)
_ct.columns.name = None
tabela(_ct.assign(Total=_ct.sum(axis=1)).rename_axis('Grupo'), 'sob_ac_desfechos',
       'Processos com AC realizada: tipo de desfecho por modalidade (frequências)', secao='4.8.1',
       formatos={c: 'int' for c in list(_ct.columns) + ['Total']})
km_ac = {g: KaplanMeierFitter(label=ROTULO_GRUPO[g]).fit(ac.loc[ac.grupo2 == g, 'T'], ac.loc[ac.grupo2 == g, 'E']) for g in ['Presencial', 'Remota']}
lr_ac = logrank_test(ac.loc[ac.grupo2 == 'Presencial', 'T'], ac.loc[ac.grupo2 == 'Remota', 'T'],
                     ac.loc[ac.grupo2 == 'Presencial', 'E'], ac.loc[ac.grupo2 == 'Remota', 'E'])
cox_ac = CoxPHFitter().fit(ac[['T', 'E', 'Remota'] + COLS_MES], 'T', 'E')
hr_ac = tabela_hr(cox_ac, ['Remota']); hr_ac.index = ['AC remota × AC presencial (com AC realizada)']
sob_tabela(hr_ac.rename_axis('Termo'), 'sob_ac_cox', 'Cox entre os processos com AC realizada: AC remota × AC presencial '
           '(ajustado por mês)', secao='4.8.1', casas=3, colunas_p=('p (Wald)',),
           nota='comparação observacional (condiciona na realização da AC, posterior ao sorteio).')
print(f"Log-rank Presencial × Remota (com AC): χ² = {fmt_br(lr_ac.test_statistic, 2)}, p = {p_br(lr_ac.p_value)}")
print('Medianas (dias): ' + '; '.join(f'{g} {fmt_br(km_ac[g].median_survival_time_, 0)}' for g in km_ac))

fig, ax = plt.subplots(figsize=(10, 5.4))
plot_km(ax, ac, tempo='T', evento='E', grupo='grupo2', ordem=['Presencial', 'Remota'], passo=30)
eixo_pct(ax)
ax.set_title('Somente processos com AC realizada: AC presencial × AC remota')
_h = hr_ac.iloc[0]
anotar_teste(ax, texto_teste('Log-rank (2 grupos)', f'χ²(1) = {fmt_br(lr_ac.test_statistic, 2)}', lr_ac.p_value,
                             f'HR remota × presencial = {fmt_br(_h["HR"], 2)} [{fmt_br(_h["IC 95% inf."], 2)}; '
                             f'{fmt_br(_h["IC 95% sup."], 2)}] (Cox + mês)'), loc='lower left')
figura(fig, 'sob_ac_modalidade', 'Entre os processos que tiveram audiência, a modalidade (presencial ou remota) não altera o tempo',
       secao='4.8.1', nota='subconjunto condicionado na realização da AC (posterior ao sorteio): leitura associativa, com tempo '
                           'imortal até a audiência. IC 95% log-log; | = censura.')
''')

md(r'''
### 4.8.2 Técnica de conciliação e audiência híbrida

**Técnica.** Seis técnicas sorteadas entre as audiências. H₀: o tempo até a sentença não depende da técnica. Teste: log-rank de 6 grupos (5 g.l.) e Cox com a técnica (referência = Padrões objetivos, a mais frequente) ajustado por modalidade e mês. Com ~47 a 67 processos por técnica, o poder para diferenças moderadas é baixo: um resultado não significativo **não** demonstra equivalência.

**Híbrida.** Audiência pautada como presencial em que uma parte participou remotamente (Res. CNJ 481/2022). É uma decisão posterior ao sorteio, tomada a pedido da parte: comparar híbridas com presenciais puras é observacional (o pedido pode estar associado ao perfil da parte). Restringe-se ao grupo Presencial com AC realizada.
''')

code(r'''
ac['tec'] = ac['tecnica_curta'].astype(str)
ORDEM_TEC = ac['tec'].value_counts().index.tolist()
lr_tec = multivariate_logrank_test(ac['T'], ac['tec'], ac['E'])
for t in ORDEM_TEC[1:]:
    ac[f'tec_{t}'] = (ac['tec'] == t).astype(int)
cols_tec = [f'tec_{t}' for t in ORDEM_TEC[1:]]
cox_tec = CoxPHFitter().fit(ac[['T', 'E', 'Remota'] + COLS_MES + cols_tec], 'T', 'E')
hr_tec = tabela_hr(cox_tec, cols_tec); hr_tec.index = [f'{t} × {ORDEM_TEC[0]}' for t in ORDEM_TEC[1:]]
print(f'Log-rank entre as 6 técnicas: χ² = {fmt_br(lr_tec.test_statistic, 2)}, {lr_tec.degrees_of_freedom} g.l., p = {p_br(lr_tec.p_value)}')
sob_tabela(hr_tec.rename_axis('Técnica (vs. referência)'), 'sob_ac_tecnica_cox',
           f'Cox da técnica de conciliação (referência = {ORDEM_TEC[0]}), ajustado por modalidade e mês', secao='4.8.2',
           casas=3, colunas_p=('p (Wald)',),
           nota=f'log-rank entre as 6 técnicas: χ² = {fmt_br(lr_tec.test_statistic, 2)} ({lr_tec.degrees_of_freedom} g.l.); '
                f'{p_txt(lr_tec.p_value)}.')

pres_ac = ac[ac.grupo2 == 'Presencial'].copy()
pres_ac['hib'] = pres_ac['hibrida'].fillna(False).astype(int)
lr_hib = logrank_test(pres_ac.loc[pres_ac.hib == 1, 'T'], pres_ac.loc[pres_ac.hib == 0, 'T'],
                      pres_ac.loc[pres_ac.hib == 1, 'E'], pres_ac.loc[pres_ac.hib == 0, 'E'])
print(f'Presencial com AC: híbridas {pres_ac.hib.sum()}, presenciais puras {(pres_ac.hib == 0).sum()} | '
      f'log-rank p = {p_br(lr_hib.p_value)}')

# técnicas: paleta própria (nenhuma cor de grupo, de desfecho ou de destaque)
CORES_TEC = dict(zip(ORDEM_TEC, ['#1a1a1a', '#56B4E9', '#882255', '#44AA99', '#DDAA33', '#8C8C8C']))
fig, ax = plt.subplots(figsize=(10.5, 6))
plot_km(ax, ac, tempo='T', evento='E', grupo='tec', ordem=ORDEM_TEC, cores=CORES_TEC, ic=False, passo=30, legenda=False)
eixo_pct(ax)
ax.legend(loc='upper right', fontsize=8.5)
ax.set_title('Processos com AC realizada, por técnica de conciliação sorteada')
anotar_teste(ax, texto_teste(f'Log-rank ({len(ORDEM_TEC)} técnicas)',
                             f'χ²({lr_tec.degrees_of_freedom}) = {fmt_br(lr_tec.test_statistic, 2)}', lr_tec.p_value,
                             f'HR vs. {ORDEM_TEC[0]}: {fmt_br(hr_tec["HR"].min(), 2)} a {fmt_br(hr_tec["HR"].max(), 2)}'),
             loc='lower left')
figura(fig, 'sob_ac_tecnica', 'Nenhuma técnica de conciliação acelera ou retarda a sentença de forma detectável',
       secao='4.8.2', nota='Kaplan-Meier sem IC (6 curvas); | = censura. Com 47 a 67 processos por técnica, só diferenças grandes '
                           'seriam detectadas: ausência de evidência não é equivalência.')

pres_ac['hib_txt'] = np.where(pres_ac['hib'] == 1, 'Híbrida', 'Presencial pura')
fig, ax = plt.subplots(figsize=(10, 5.4))
plot_km(ax, pres_ac, tempo='T', evento='E', grupo='hib_txt', ordem=['Presencial pura', 'Híbrida'],
        cores={'Presencial pura': CORES_GRUPO['Presencial'], 'Híbrida': CORES_GRUPO['Remota']}, passo=30)
eixo_pct(ax)
ax.set_title('Grupo Presencial com AC realizada: audiência híbrida × presencial pura')
anotar_teste(ax, texto_teste('Log-rank (2 grupos)', f'χ²(1) = {fmt_br(lr_hib.test_statistic, 2)}', lr_hib.p_value),
             loc='lower left')
figura(fig, 'sob_ac_hibrida', 'A audiência híbrida não se associa a tempo diferente do da presencial pura',
       secao='4.8.2', nota='híbrida = audiência pautada como presencial com uma parte participando remotamente (decisão posterior '
                           'ao sorteio; comparação observacional). Cor da híbrida = a da modalidade remota. IC 95% log-log.')
''')

interp('sob_ac')

# =====================================================================
md(r'''
---

## 4.9 Análises de sensibilidade

Cada decisão de curadoria da Parte I (o que é evento, quem fica na base, como tratar datas suspeitas) poderia, em tese, mudar a conclusão. A tabela abaixo refaz a análise principal — **Cox grupo + mês (Efron)** e **log-rank de 3 grupos** — sob cenários alternativos. A conclusão é robusta se o HR e o p-valor mudarem pouco. (O cenário "Principal" usa grupo + mês, **sem** a origem externa, para que o mesmo modelo caiba em todos os cenários, inclusive o que exclui a origem externa; por isso o seu HR difere na terceira casa do modelo (b) da seção 4.5.)

| Cenário | O que muda | Por quê |
|---|---|---|
| Principal | redistribuição censurada em T | análise de referência |
| (i-a) Redistribuição excluída | retira os 24 processos "Decisão" | eles saíram do juízo antes de receber o tratamento (inelegíveis pós-sorteio) |
| (i-b) Redistribuição competitiva | Fine-Gray da sentença (redistribuição competidora; log-rank → teste de permutação tipo Gray não repetido) | efeito sobre a incidência acumulada de sentença |
| (ii) Sem origem externa | retira os 12 processos vindos de outro órgão | chegaram com tramitação anterior |
| (iii-a) Sem desvio de protocolo | retira os 6 casos de híbrida incongruente (A12/A13) | registro duvidoso |
| (iii-b) Híbridas "como tratadas" | as 28 híbridas do grupo Presencial passam ao grupo Remota | parte participou remotamente (*as-treated*, não ITT) |
| (iv) Com as duplicatas | inclui as 6 linhas excluídas (reentradas e duplicatas) | E3: checar se a regra de exclusão importa |
| (iv-b) Reentradas unidas | cada processo reentrante fica no grupo do **1º sorteio** e é seguido até o desfecho do **último episódio**: `0808905-44` (Remota, distribuído em 20/05, redistribuído e de volta à vara em 22/05, ativo) passa a censurado em 07/10; `0804436-52` (Presencial, 18/03) segue até a última redistribuição, em 27/04 | ITT por processo: a redistribuição seguida de retorno não encerra o caso |
| (v-a) Fim de semana deslocado | desfechos datados em sábado/domingo passam para a segunda-feira | A16: data de assinatura × data útil |
| (v-b) Fim de semana excluído | retira os 135 processos com desfecho em fim de semana | caso extremo (viesado: retira só eventos) |
| (vi) Censura comum em 65 dias | todos censurados em 65 dias (o menor seguimento) | neutraliza a entrada escalonada por completo |
| (vii) Dados ingênuos | "Decisão" contada como evento (como no notebook do professor, E10) | mostra o efeito do erro |
| (viii) Sem tempos zero | retira os 38 desfechos no dia da distribuição | A15: possíveis erros de data |
''')

code(r'''
def cenario(df, nome, fine_gray=False):
    df = df[df['T'].notna()]
    if fine_gray:
        m = fine_gray_censura_conhecida(df, 1, X_CS)  # causa 1 aqui = sentença (K redefinido)
    else:
        m = CoxPHFitter().fit(df[['T', 'E'] + X_CS], 'T', 'E')
    t = tabela_hr(m, X_BASE, rotulo='HR')
    lr = multivariate_logrank_test(df['T'], df['grupo'].astype(str), df['E'])
    return {'Cenário': nome, 'n': len(df), 'sentenças': int(df['E'].sum()),
            'HR Presencial': t.iloc[0, 0], 'IC P inf.': t.iloc[0, 1], 'IC P sup.': t.iloc[0, 2],
            'HR Remota': t.iloc[1, 0], 'IC R inf.': t.iloc[1, 1], 'IC R sup.': t.iloc[1, 2],
            'p log-rank': lr.p_value if not fine_gray else np.nan}

sens = [cenario(sob, 'Principal')]
sens.append(cenario(sob[sob.CR != 2], '(i-a) Redistribuição excluída'))
sens.append(cenario(sob.assign(K=sob['CR']), '(i-b) Redistribuição competitiva (Fine-Gray)', fine_gray=True))
sens.append(cenario(sob[sob.origem_ext == 0], '(ii) Sem origem externa'))
sens.append(cenario(sob[~sob['desvio_protocolo'].astype(bool)], '(iii-a) Sem desvio de protocolo'))
_as = sob.copy()
_hib = (_as.grupo == 'Presencial') & (_as['hibrida'].fillna(False).astype(bool))
_as.loc[_hib, 'grupo'] = 'Remota'; _as['Presencial'] = (_as.grupo == 'Presencial').astype(int); _as['Remota'] = (_as.grupo == 'Remota').astype(int)
sens.append(cenario(_as, f'(iii-b) Híbridas como tratadas ({_hib.sum()} → Remota)'))
todas = pd.read_pickle(PROC / 'ed2_todas_linhas.pkl')
todas = todas[todas['tempo'].notna() & todas['evento'].notna()]
sens.append(cenario(preparar_sob(todas), f'(iv) Com as duplicatas (n = {len(todas)})'))
_ru = sob.copy()                                     # (iv-b) reentradas unidas: 1º sorteio, desfecho do último episódio
REENTRADAS_UNIDAS = []
for _proc in ['0808905-44', '0804436-52']:
    _eps = todas[todas['processo'].astype(str).str.startswith(_proc)].sort_values('dt_distribuicao')
    _i = _ru.index[_ru['processo'].astype(str).str.startswith(_proc)][0]
    _ult = _eps.iloc[-1]
    _fim = _ult['dt_sentenca'] if pd.notna(_ult['dt_sentenca']) else DATA_CORTE
    _ru.loc[_i, 'T'] = float((pd.Timestamp(_fim) - pd.Timestamp(_ru.loc[_i, 'dt_distribuicao'])).days)
    _ru.loc[_i, 'CR'] = int(_ult['evento_cr']); _ru.loc[_i, 'K'] = int(_ult['causa']); _ru.loc[_i, 'E'] = int(_ult['evento'])
    REENTRADAS_UNIDAS.append(f"{_proc}: {_ru.loc[_i, 'grupo']}, T = {int(sob.loc[_i, 'T'])} → {int(_ru.loc[_i, 'T'])} dias, "
                             f"desfecho {['ativo', 'sentença', 'redistribuição'][int(_ru.loc[_i, 'CR'])]}")
print('Reentradas unidas:', ' | '.join(REENTRADAS_UNIDAS))
sens.append(cenario(_ru, '(iv-b) Reentradas unidas (1º sorteio)'))
_fs = sob.copy()
_dow = _fs['dt_sentenca'].dt.dayofweek
_fs['T'] = _fs['T'] + np.where((_fs.CR > 0) & (_dow == 5), 2, 0) + np.where((_fs.CR > 0) & (_dow == 6), 1, 0)
sens.append(cenario(_fs, '(v-a) Fim de semana → segunda-feira'))
sens.append(cenario(sob[~sob['sentenca_fim_semana'].fillna(False).astype(bool)], '(v-b) Fim de semana excluído'))
_65 = sob.copy(); _65['E'] = ((_65.E == 1) & (_65['T'] <= 65)).astype(int); _65['T'] = _65['T'].clip(upper=65)
sens.append(cenario(_65, '(vi) Censura comum em 65 dias'))
sens.append(cenario(sob.assign(E=(sob.CR > 0).astype(int)), '(vii) Ingênuo: Decisão = evento'))
sens.append(cenario(sob[~sob['tempo_zero'].astype(bool)], '(viii) Sem tempos zero'))
SENS = pd.DataFrame(sens).set_index('Cenário')
sob_tabela(SENS, 'sob_sensibilidade', 'Sensibilidade do efeito do rito às decisões de curadoria (Cox grupo + mês e log-rank)',
           secao='4.9', casas=3, colunas_p=('p log-rank',), formatos={'n': 'int', 'sentenças': 'int'},
           nota='HR < 1 = sentença mais lenta que no Controle; IC 95% de Wald. No cenário (i-b), sHR de Fine-Gray e log-rank não '
                'aplicável (–). Destaque: log-rank p < 0,05.')

fig, ax = plt.subplots(figsize=(11, 7.5))
y = np.arange(len(SENS))[::-1]
for desl, g, col in [(0.15, 'Presencial', 'P'), (-0.15, 'Remota', 'R')]:
    hr = SENS[f'HR {g}']; li = SENS[f'IC {col} inf.']; ls = SENS[f'IC {col} sup.']
    ax.errorbar(hr, y + desl, xerr=[hr - li, ls - hr], fmt='o', ms=6, color=CORES_GRUPO[g], capsize=3, label=ROTULO_TERMO[g])
ax.axvline(1, color=TINTA_2, ls='--', lw=1)
ax.axvline(SENS.loc['Principal', 'HR Presencial'], color=CORES_GRUPO['Presencial'], ls=':', lw=1.2)
ax.axvline(SENS.loc['Principal', 'HR Remota'], color=CORES_GRUPO['Remota'], ls=':', lw=1.2)
for yi, pv in zip(y, SENS['p log-rank']):
    ax.annotate('log-rank: –' if pd.isna(pv) else f'log-rank: {p_txt(pv)}', (1, yi), xycoords=('axes fraction', 'data'),
                xytext=(6, 0), textcoords='offset points', va='center', fontsize=8.5, color=TINTA_2)
ax.set_yticks(y, SENS.index, fontsize=9); ax.set_ylim(-0.7, len(SENS) - 0.3)
ax.grid(axis='y', visible=False); ax.grid(axis='x', visible=True)
ax.set_xlabel('HR de sentença vs. Controle (Cox grupo + mês; IC 95%)')
ax.set_title('HR de cada grupo com AC em cada cenário (pontilhado = análise principal)')
legenda_abaixo(ax, ncol=2, dy=-0.09)
figura(fig, 'sob_sensibilidade', 'Nenhuma decisão de curadoria muda a conclusão; só a censura comum em 65 dias, que corta '
       'a janela do efeito, o atenua', secao='4.9',
       nota='em (i-b), sHR de Fine-Gray da sentença com a redistribuição como competidora (sem log-rank).')
''')

interp('sob_sens')

# =====================================================================
md(r'''
---

## 4.10 Síntese da análise de sobrevivência

A tabela reúne as medidas de efeito principais. Elas respondem a perguntas complementares: a **mediana** e o **RMST** em dias (escala de tempo), o **HR** em taxa diária (escala de risco), a **razão de tempos** do AFT e a **FIA a 90 dias** por tipo de desfecho (o que acontece com os processos).
''')

code(r'''
sint = {}
for g in ORDEM_GRUPO:
    q = quartis.loc[ROTULO_GRUPO[g], 'Mediana']
    r180 = rmst_tab.query('`τ (dias)` == 180 and Grupo == @g').iloc[0]
    linha = {'n': int((sob.grupo == g).sum()), 'Sentenças': int(sob.loc[sob.grupo == g, 'E'].sum()),
             'Mediana KM, dias (IC 95%)': q,
             'RMST 180 d, dias (IC 95%)': f"{fmt_br(r180['RMST (dias)'], 1)} ({fmt_br(r180['IC 95% inf.'], 1)}–{fmt_br(r180['IC 95% sup.'], 1)})"}
    if g == 'Controle':
        linha |= {'ΔRMST 180 d vs. Controle (IC bootstrap)': 'referência', 'HR Cox (b) (IC 95%)': 'referência',
                  f'Razão de tempos {MELHOR_AFT} (IC 95%)': 'referência'}
    else:
        d = dif_rmst.query('`τ (dias)` == 180 and Contraste == @g + " − Controle"').iloc[0]
        h = HR_B.loc[ROTULO_TERMO[g]]
        tr = TR_AFT[(TR_AFT.Modelo == MELHOR_AFT)].loc[ROTULO_TERMO[g]]
        linha |= {'ΔRMST 180 d vs. Controle (IC bootstrap)': f"{fmt_br(d['Diferença (dias)'], 1)} ({fmt_br(d['IC 95% inf. (bootstrap)'], 1)} a {fmt_br(d['IC 95% sup. (bootstrap)'], 1)})",
                  'HR Cox (b) (IC 95%)': f"{fmt_br(h['HR'], 2)} ({fmt_br(h['IC 95% inf.'], 2)}–{fmt_br(h['IC 95% sup.'], 2)})",
                  f'Razão de tempos {MELHOR_AFT} (IC 95%)': f"{fmt_br(tr['Razão de tempos'], 2)} ({fmt_br(tr['IC 95% inf.'], 2)}–{fmt_br(tr['IC 95% sup.'], 2)})"}
    for k in (1, 2, 3):
        linha[f'FIA 90 d: {CAUSAS[k]}'] = CIF_TAB.loc[(CAUSAS[k], 90), g]
    sint[ROTULO_GRUPO[g]] = linha
SINTESE_SOB = pd.DataFrame(sint)
tabela(SINTESE_SOB.rename_axis('Medida'), 'sob_sintese', 'Síntese das medidas de efeito da análise de sobrevivência',
       secao='4.10', formatos={c: 'texto' for c in SINTESE_SOB.columns},
       nota='IC 95% entre parênteses. Mediana e RMST em dias; HR < 1 e razão de tempos > 1 = sentença mais lenta que no '
            'Controle; FIA = incidência acumulada (Aalen-Johansen).')
print(f"Testes globais: log-rank p = {p_br(lr_global.p_value)}; estratificado por mês p = {p_br(LR_ESTRAT_P)}; "
      f"riscos proporcionais violados? TRV janelas p = {p_br(P_TRV_C)}")
SINTESE_SOB.to_csv(PROC / 'ed2_sintese_sobrevivencia.csv', sep=';', encoding='utf-8-sig')
''')

interp('sob_sintese')
