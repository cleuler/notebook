# Parte V — Análise multivariada e modelagem (seções 5.1 a 5.6).
# Executado por build_rafaelcc_ed2.py (exec): usa md(), code() e interp().

md(r'''
# PARTE V — ANÁLISE MULTIVARIADA E MODELAGEM

A Parte IV estimou os efeitos dos grupos sobre o **tempo** com modelos que respeitam a censura (Kaplan-Meier, Cox, AFT e riscos competitivos). Esta parte pergunta o que a **modelagem multivariada** acrescenta: (i) por que a regressão linear sobre o tempo, usada no notebook do professor, não serve (E26); (ii) o que modelos de **classificação** (regressão logística, logit multinomial e árvores de decisão; ARTES; BARROSO, 2023, cap. 10 e 11) dizem sobre o **acordo** e o **tipo de desfecho**; (iii) que estrutura a **análise de correspondência** revela na tabela grupo × desfecho; e (iv) qual modelo de tempo, entre os que tratam a censura, **descreve e prevê** melhor.

### Limitação que condiciona toda a Parte V: quase não há covariáveis

O projeto de pesquisa previa como variáveis de controle o **tipo de ação, o valor da causa e o número de partes** (ver `docs/r1_documentos.md`), e a literatura de duração processual acrescentaria o **advogado constituído** (ou *jus postulandi*), a **pessoa jurídica no polo passivo** e o **litigante habitual**. **Nenhuma dessas variáveis foi coletada.** A planilha só registra o que o próprio experimento produziu:

| Variável disponível | Natureza | Pode entrar como preditora? |
|---|---|---|
| `grupo` (sorteado) | basal, aleatorizada | sim: é o fator de interesse |
| mês de distribuição / ordem de chegada | basal (calendário) | sim; mas determina o seguimento (`followup`), com o qual é quase colinear |
| `origem_externa` (12 processos) | basal | sim, mas rara |
| `ac_realizada`, `hibrida`, técnica | **pós-sorteio** (ocorrem durante o processo; zero estrutural no Controle) | só no subconjunto com audiência, e como mediadores exploratórios |
| `acordo_ac`, `acordo_fora`, `acordo` | **desfechos** intermediários | só como resposta, nunca como preditora do tempo (viés de tempo imortal) |
| `tipo_desfecho` | desfecho | só como resposta |

Consequência: os modelos desta parte têm, no máximo, **três ou quatro preditores**, e todos de baixa variabilidade entre processos. Isso não é defeito do desenho: o sorteio foi feito para uma **comparação causal entre grupos** (que dispensa covariáveis para ser não enviesada), e não para **prever** a duração de um processo individual. Esperam-se, portanto, poder explicativo e preditivo baixos, e a parte é honesta quanto a isso. A seção 5.6 lista as variáveis que permitiriam uma modelagem multivariada de verdade (questão 2.9).

**Codificação comum.** O mês entra como escore ordinal (`mes_num`: jan = 1, …, ago = 8), uma tendência linear de calendário com um único parâmetro; agosto tem só 6 processos, o que desaconselha um parâmetro por mês. Grupo: Controle como referência.
''')

code(r'''
if 'dados' not in globals():
    dados = pd.read_pickle(PROC / 'ed2_tidy.pkl')

from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.multitest import multipletests
from statsmodels.stats.proportion import proportion_confint
from sklearn.metrics import roc_auc_score, roc_curve, confusion_matrix, accuracy_score, balanced_accuracy_score
from sklearn.model_selection import StratifiedKFold, KFold, cross_val_score, cross_val_predict
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor, plot_tree
from lifelines import WeibullAFTFitter, LogNormalAFTFitter, NelsonAalenFitter
from lifelines.utils import k_fold_cross_validation, concordance_index

RNG_MUL = np.random.default_rng(SEMENTE)
mul_res = {}          # resultados guardados para a síntese (5.6)

mul = dados.copy()
mul['grupo'] = pd.Categorical(mul['grupo'].astype(str), categories=ORDEM_GRUPO)
mul['mes_num'] = mul['mes_distribuicao'].cat.codes.astype(int) + 1
mul['presencial'] = (mul['grupo'] == 'Presencial').astype(int)
mul['remota'] = (mul['grupo'] == 'Remota').astype(int)
mul['T'] = mul['tempo'].astype(float)
mul['E'] = mul['evento'].astype(int)
mul['T_pos'] = mul['tempo_pos'].astype(float)
mul['log_T'] = np.log(mul['T_pos'])
mul['followup_f'] = mul['followup'].astype(float)
mul['log_followup'] = np.log(mul['followup_f'])
mul['dia_estudo_f'] = mul['dia_estudo'].astype(float)
mul['encerrado_b'] = mul['encerrado'].astype(bool)
mul['desfecho'] = mul['tipo_desfecho'].astype(str)
mul['homolog'] = (mul['desfecho'] == 'Homologação').astype(int)
mul['hibrida_b'] = mul['hibrida'].fillna(False).astype(bool).astype(int)
mul['origem_ext'] = mul['origem_externa'].astype(bool).astype(int)

NOMES_COEF = {'Intercept': 'Intercepto', 'C(grupo)[T.Presencial]': 'Presencial vs Controle',
              'C(grupo)[T.Remota]': 'Remota vs Controle', 'mes_num': 'Mês de distribuição (+1 mês)',
              'log_followup': 'log(seguimento)', 'hibrida_b': 'Híbrida (sim)', 'remota': 'Remota vs Presencial',
              'presencial': 'Presencial vs Controle', 'origem_ext': 'Origem externa',
              'dia_estudo_f': 'Dia de distribuição'}

def mul_ic_wilson(x, n):
    li, ls = proportion_confint(x, n, method='wilson')
    return li, ls

resumo = pd.DataFrame({
    'Subconjunto': ['Todos', 'Encerrados (sentença ou redistribuição)', 'Sentenciados (evento = 1)',
                    'Com audiência realizada'],
    'n': [len(mul), int(mul['encerrado_b'].sum()), int(mul['E'].sum()),
          int(mul['ac_realizada'].fillna(False).astype(bool).sum())]})
print(f"Correlação entre mês de distribuição e log(seguimento): r = {fmt_br(np.corrcoef(mul['mes_num'], mul['log_followup'])[0, 1], 3)}")
tabela(resumo.rename(columns={'n': 'Processos (n)'}), 'mul_subconjuntos', 'Subconjuntos analíticos usados na Parte V',
       secao='5', nota='encerrados = com sentença ou redistribuição até 07/10/2026; audiência realizada só existe nos grupos '
                       'Presencial e Remota (zero estrutural no Controle).')

# ---------------------------------------------------------------- auxiliares gráficos da Parte V
# Cores de "estimadores/modelos" (entidade própria): nenhuma repete a cor de um grupo.
COR_MODELO = '#2B3A4A'          # modelo de referência / série única
COR_VIES = DESTAQUE             # estimador enviesado ou alternativa em contraste
NOMES_VAR = {'presencial': 'Presencial (1 = sim)', 'remota': 'Remota (1 = sim)', 'dia_estudo': 'Dia de distribuição',
             'origem_ext': 'Origem externa (1 = sim)', 'ac_realizada': 'AC realizada (1 = sim)',
             'hibrida': 'AC híbrida (1 = sim)'}


def mul_peq(p):
    """'< 0,001' ou '= 0,034' (para escrever 'p < 0,001' / 'p = 0,034')."""
    return '< 0,001' if p < 0.001 else '= ' + fmt_p(p)


def mul_ic(v, lo, hi, casas=3):
    return f'{fmt_br(v, casas)} [{fmt_br(lo, casas)}; {fmt_br(hi, casas)}]'


def mul_fmt_razao(v):
    """Rótulo de eixo para razões (escala log): 0,25 · 0,5 · 1 · 1,5 · 2."""
    s = fmt_br(v, 2)
    return s.rstrip('0').rstrip(',') if ',' in s else s


def mul_eixo_razao(ax, valores, eixo='y'):
    """Escala log para razões (RC, RRR, razão de tempos) com marcas legíveis em pt-BR e linha de nulidade em 1."""
    v = np.asarray([x for x in valores if np.isfinite(x) and x > 0], float)
    lo, hi = min(v.min(), 1) / 1.25, max(v.max(), 1) * 1.25
    cand = np.array([0.05, 0.1, 0.2, 0.25, 0.5, 0.75, 1, 1.5, 2, 3, 4, 6, 8, 10, 20, 50, 100])
    marcas = cand[(cand >= lo) & (cand <= hi)]
    alvo = ax.yaxis if eixo == 'y' else ax.xaxis
    (ax.set_yscale if eixo == 'y' else ax.set_xscale)('log')
    alvo.set_major_locator(mpl.ticker.FixedLocator(marcas))
    alvo.set_major_formatter(FuncFormatter(lambda x, _: mul_fmt_razao(x)))
    alvo.set_minor_locator(mpl.ticker.NullLocator())
    (ax.set_ylim if eixo == 'y' else ax.set_xlim)(lo, hi)
    (ax.axhline if eixo == 'y' else ax.axvline)(1, color=TINTA_2, lw=1, zorder=1)


def mul_forest(ax, est, li, ls, x=None, cor=COR_MODELO, textos=None, label=None, marker='o'):
    """Pontos com IC 95% (vertical), um por posição x; `textos` = rótulos seletivos ao lado do ponto."""
    est, li, ls = (np.asarray(a, float) for a in (est, li, ls))
    x = np.arange(len(est)) if x is None else np.asarray(x, float)
    cores = cor if isinstance(cor, (list, tuple)) else [cor] * len(est)
    for i in range(len(est)):
        ax.errorbar(x[i], est[i], yerr=[[est[i] - li[i]], [ls[i] - est[i]]], fmt=marker, ms=7, color=cores[i],
                    ecolor=cores[i], elinewidth=1.6, capsize=4, label=label if i == 0 else None, zorder=3)
        if textos is not None and textos[i]:
            ax.annotate(textos[i], (x[i], est[i]), xytext=(9, 0), textcoords='offset points', va='center',
                        ha='left', fontsize=8.5, color=TINTA)
    ax.grid(axis='x', visible=False)


def mul_rotular_pontos(ax, xs, ys, textos, tamanho=9, negrito=None):
    """Rótulos de pontos sem colisão: testa 8 posições ao redor de cada ponto e fica com a primeira livre."""
    fig = ax.figure
    fig.canvas.draw()
    rend = fig.canvas.get_renderer()
    ocupado = []
    pts = ax.transData.transform(np.column_stack([xs, ys]))
    for (px, py) in pts:
        ocupado.append(mpl.transforms.Bbox.from_extents(px - 6, py - 6, px + 6, py + 6))
    offs = [(8, 6, 'left', 'bottom'), (8, -6, 'left', 'top'), (-8, 6, 'right', 'bottom'), (-8, -6, 'right', 'top'),
            (0, 10, 'center', 'bottom'), (0, -10, 'center', 'top'), (14, 0, 'left', 'center'), (-14, 0, 'right', 'center')]
    for k, (x, y, t) in enumerate(zip(xs, ys, textos)):
        escolhido = None
        for dx, dy, ha, va in offs:
            a = ax.annotate(t, (x, y), xytext=(dx, dy), textcoords='offset points', ha=ha, va=va, fontsize=tamanho,
                            color=TINTA, fontweight='bold' if negrito and negrito[k] else 'normal')
            bb = a.get_window_extent(rend).expanded(1.05, 1.1)
            if not any(bb.overlaps(o) for o in ocupado):
                escolhido = a
                break
            a.remove()
        if escolhido is None:   # nenhuma posição livre: usa a primeira
            dx, dy, ha, va = offs[0]
            escolhido = ax.annotate(t, (x, y), xytext=(dx, dy), textcoords='offset points', ha=ha, va=va,
                                    fontsize=tamanho, color=TINTA)
        ocupado.append(escolhido.get_window_extent(rend))


def mul_arvore(ax, modelo, colunas, classes=None, cores_classe=None, fontsize=9, precisao=2):
    """plot_tree legível: nomes de variáveis em português, vírgula decimal, nós coloridos pela entidade.

    Classificação: cor da classe majoritária (intensidade = pureza). Regressão: escala divergente DIV pelo valor do nó.
    """
    anns = plot_tree(modelo, feature_names=[NOMES_VAR.get(c, c) for c in colunas], class_names=classes,
                     filled=False, rounded=True, impurity=False, proportion=True, fontsize=fontsize, ax=ax,
                     precision=precisao)
    valores = modelo.tree_.value[:, 0, :]
    if classes is None:
        lim = np.abs(valores[:, 0]).max() or 1
    for i, a in enumerate(anns):
        txt = a.get_text()
        txt = re.sub(r'(\d)\.(\d)', r'\1,\2', txt)
        txt = (txt.replace('samples', 'processos').replace('value', 'proporções' if classes is not None else 'resíduo médio')
                  .replace('class', 'classe').replace('<=', '≤').replace('True', 'sim').replace('False', 'não'))
        a.set_text(txt)
        caixa = a.get_bbox_patch()
        if caixa is None or i >= len(valores):
            continue
        if classes is not None:
            v = valores[i] / valores[i].sum()
            k = int(np.argmax(v))
            pureza = (v[k] - 1 / len(v)) / (1 - 1 / len(v))
            caixa.set_facecolor(mpl.colors.to_rgba(cores_classe[classes[k]], 0.12 + 0.43 * pureza))
        else:
            caixa.set_facecolor(DIV(0.5 + 0.5 * valores[i, 0] / lim))
        caixa.set_edgecolor('#8c8c8c')
    return anns
''')

# =====================================================================
md(r'''
## 5.1 Regressão linear (OLS) sobre o tempo: por que não serve

O notebook do professor ajustou `duracao_proc ~ grupo` por mínimos quadrados sobre todos os processos, inclusive os ativos (E14, E26). Há duas versões "corrigidas" que alguém poderia tentar, e ambas falham por razões diferentes:

1. **OLS só com os sentenciados** (n = 708), tirando os censurados. Responde a uma pergunta condicional ("entre os que já tiveram sentença, quanto demoraram?") e é **enviesada para tempos curtos**: um processo distribuído em julho só entra na amostra se for julgado em menos de ~90 dias.
2. **OLS sobre log(tempo)**, que aproxima a regressão de um modelo log-normal (AFT) e tenta corrigir a assimetria; o problema da censura continua.

Ajustam-se as duas versões com `grupo + mês`, examinam-se R² e resíduos e, por fim, comparam-se os coeficientes com os de um **modelo log-normal AFT com censura** (a mesma escala, log T; COLOSIMO; GIOLO, 2006, eq. 4.10, p. 122), que usa todos os 938 processos. A diferença entre eles é o **viés de selecionar só os encerrados**.

### 5.1.1 Ajuste e R²

H0 (teste F global): todos os coeficientes, exceto o intercepto, são nulos. H1: ao menos um não é. Os coeficientes do modelo linear estão em dias; os do modelo em log, exponenciados, são **razões de médias geométricas** (exp(β) = 0,90 significa tempo típico 10% menor).
''')

code(r'''
sent = mul[mul['E'] == 1].copy()
ols_lin = smf.ols('T ~ C(grupo) + mes_num', data=sent).fit()
ols_log = smf.ols('log_T ~ C(grupo) + mes_num', data=sent).fit()
ols_log_todos = smf.ols('log_T ~ C(grupo) + mes_num', data=mul).fit()   # versão do professor (censurados como completos)

def mul_tab_ols(res, exp=False):
    ic = res.conf_int()
    tab = pd.DataFrame({'coef': res.params, 'li': ic[0], 'ls': ic[1], 'p': res.pvalues})
    if exp:
        tab[['coef', 'li', 'ls']] = np.exp(tab[['coef', 'li', 'ls']])
    rot = 'exp(β) (razão de médias geométricas)' if exp else 'β (dias)'
    return pd.DataFrame({'Termo': [NOMES_COEF.get(i, i) for i in tab.index], rot: tab['coef'].to_numpy(),
                         'IC 95% inf.': tab['li'].to_numpy(), 'IC 95% sup.': tab['ls'].to_numpy(),
                         'p': tab['p'].to_numpy()}), rot

for id_, nome, res, ex in [('mul_ols_lin', 'OLS do tempo (dias) ~ grupo + mês, só sentenciados: o mês tem efeito negativo', ols_lin, False),
                           ('mul_ols_log', 'OLS de log(tempo) ~ grupo + mês, só sentenciados: razões de médias geométricas', ols_log, True)]:
    t_ols, col = mul_tab_ols(res, ex)
    c = 3 if ex else 1
    tabela(t_ols, id_, nome, secao='5.1.1', formatos={col: c, 'IC 95% inf.': c, 'IC 95% sup.': c}, destaque='p',
           nota=f'n = {int(res.nobs)}; R² = {fmt_br(res.rsquared, 3)}; R² ajustado = {fmt_br(res.rsquared_adj, 3)}; '
                f'teste F global = {fmt_br(res.fvalue, 2)} (p {mul_peq(res.f_pvalue)}). '
                'Linhas em destaque: p < 0,05. Referência do grupo: Controle.')
mul_res['ols_r2'] = ols_lin.rsquared
mul_res['olslog_r2'] = ols_log.rsquared
''')

interp('mul_ols_ajuste')

md(r'''
### 5.1.2 Diagnóstico dos resíduos

Os pressupostos do OLS para a inferência são resíduos com **variância constante** e, para amostras pequenas, aproximadamente **normais**. Três gráficos por modelo:

- **resíduos × valores ajustados**: deve ser uma nuvem sem forma. Como só há 3 grupos × 8 meses, os ajustados formam poucas colunas verticais (pontos com leve deslocamento horizontal para visualização);
- **QQ normal** dos resíduos: pontos sobre a reta indicam normalidade;
- **teste de Breusch-Pagan** (H0: variância dos resíduos constante, homocedasticidade; H1: variância depende dos preditores), com o gráfico dos resíduos ao quadrado contra os ajustados, que é exatamente o que o teste regride.
''')

code(r'''
for linha, (nome, res, unid, id_) in enumerate([('tempo (dias)', ols_lin, 'dias', 'mul_ols_diag_lin'),
                                                ('log(tempo)', ols_log, 'log dias', 'mul_ols_diag_log')]):
    resid, ajust = res.resid, res.fittedvalues
    cor = sent['grupo'].map(CORES_GRUPO)
    jit = ajust + RNG_MUL.uniform(-0.3, 0.3, len(ajust)) * (ajust.std() / 10)   # mesma sequência aleatória de antes
    bp_lm, bp_p, _, _ = het_breuschpagan(resid, res.model.exog)
    jb = stats.jarque_bera(resid)
    fig, eixos = plt.subplots(1, 3, figsize=(14, 4.4))
    ax = eixos[0]
    ax.scatter(jit, resid, s=9, alpha=0.5, c=cor, lw=0)
    ax.axhline(0, color=TINTA_2, lw=1)
    ax.set(title='Resíduos × ajustados', xlabel=f'Valor ajustado ({unid})', ylabel=f'Resíduo ({unid})')
    for g in ORDEM_GRUPO:
        ax.scatter([], [], color=CORES_GRUPO[g], label=g, s=20)
    ax.legend(loc='lower left', ncol=3, fontsize=8, handletextpad=0.2, columnspacing=0.8)
    ax = eixos[1]
    sm.qqplot(resid, line='s', ax=ax, markersize=3, alpha=0.6, markerfacecolor=COR_MODELO, markeredgecolor='none')
    ax.get_lines()[1].set_color(DESTAQUE)
    ax.set(title='QQ normal dos resíduos', xlabel='Quantil teórico N(0, 1)', ylabel=f'Quantil dos resíduos ({unid})')
    anotar_teste(ax, texto_teste('Jarque-Bera (H0: normalidade)', f'JB = {fmt_br(jb.statistic, 1)}', jb.pvalue,
                                 f'assimetria = {fmt_br(stats.skew(resid), 2)}; curtose em excesso = {fmt_br(stats.kurtosis(resid), 2)}'),
                 loc='upper left')
    ax = eixos[2]
    ax.scatter(jit, resid ** 2, s=9, alpha=0.5, c=cor, lw=0)
    ax.set(title='Resíduos ao quadrado × ajustados', xlabel=f'Valor ajustado ({unid})', ylabel=f'Resíduo² ({unid}²)')
    anotar_teste(ax, texto_teste('Breusch-Pagan (H0: variância constante)', f'LM = {fmt_br(bp_lm, 2)}', bp_p),
                 loc='upper right')
    figura(fig, id_, f'Diagnóstico do OLS de {nome} entre os sentenciados: '
           + ('variância não constante (heterocedasticidade)' if bp_p < 0.05 else 'variância constante, mas resíduos não normais'),
           secao='5.1.2', nota=f'n = {int(res.nobs)} sentenciados; pontos coloridos pelo grupo, com leve deslocamento horizontal '
                               'aleatório para separar as colunas de valores ajustados (3 grupos × 8 meses).')
    print(f'{nome}: Breusch-Pagan LM = {fmt_br(bp_lm, 2)} (p {p_br(bp_p)}); '
          f'Jarque-Bera = {fmt_br(jb.statistic, 1)} (p {p_br(jb.pvalue)}); '
          f'assimetria = {fmt_br(stats.skew(resid), 2)}; curtose excesso = {fmt_br(stats.kurtosis(resid), 2)}')
    mul_res[f'bp_{linha}'] = bp_p
''')

interp('mul_ols_diag')

md(r'''
### 5.1.3 O viés de descartar os censurados

A comparação decisiva coloca lado a lado, na mesma escala (razão de tempos, exp(β) sobre log T), três estimativas dos efeitos de grupo e de mês:

- **OLS log, todos** (como o professor, censurados tratados como tempos completos: subestima os tempos dos ativos);
- **OLS log, sentenciados** (descarta os censurados: seleciona os rápidos);
- **AFT log-normal com censura** (`LogNormalAFTFitter`, todos os 938, redistribuição tratada como censura; o modelo de referência da Parte IV).

O segundo gráfico mostra o mecanismo do viés pelo calendário: a média de log(tempo) dos sentenciados cai artificialmente com o mês de distribuição, porque os meses finais tiveram menos seguimento; a mediana de Kaplan-Meier, que usa os censurados, não tem esse artefato.
''')

code(r'''
aft_ln = LogNormalAFTFitter().fit(mul[['T_pos', 'E', 'presencial', 'remota', 'mes_num']], 'T_pos', 'E')
termos = [('C(grupo)[T.Presencial]', 'presencial'), ('C(grupo)[T.Remota]', 'remota'), ('mes_num', 'mes_num')]
linhas = []
for rot, res in [('OLS log, todos (censura ignorada)', ols_log_todos), ('OLS log, só sentenciados', ols_log)]:
    ic = res.conf_int()
    for t_ols, t_aft in termos:
        linhas.append({'Modelo': rot, 'Termo': NOMES_COEF[t_ols], 'TR': np.exp(res.params[t_ols]),
                       'li': np.exp(ic.loc[t_ols, 0]), 'ls': np.exp(ic.loc[t_ols, 1])})
s_aft = aft_ln.summary
for t_ols, t_aft in termos:
    lin = s_aft.loc[('mu_', t_aft)]
    linhas.append({'Modelo': 'AFT log-normal com censura (todos)', 'Termo': NOMES_COEF[t_ols],
                   'TR': lin['exp(coef)'], 'li': lin['exp(coef) lower 95%'], 'ls': lin['exp(coef) upper 95%']})
comp_vies = pd.DataFrame(linhas)
tabela(comp_vies.rename(columns={'TR': 'Razão de tempos exp(β)', 'li': 'IC 95% inf.', 'ls': 'IC 95% sup.'}),
       'mul_vies_estimadores', 'Razões de tempos dos mesmos termos por três estimadores: só o AFT com censura usa os ativos',
       secao='5.1.3', casas=3,
       nota='razão de tempos > 1 = tempo típico até a sentença maior. OLS em log(tempo); AFT log-normal ajustado aos 938 processos '
            'com a redistribuição tratada como censura.')
mul_res['vies_mes'] = comp_vies.set_index(['Modelo', 'Termo'])['TR']

fig, ax = plt.subplots(figsize=(10, 5))
cores_mod = {'OLS log, todos (censura ignorada)': CINZA, 'OLS log, só sentenciados': COR_VIES,
             'AFT log-normal com censura (todos)': COR_MODELO}
termos_ord = list(dict.fromkeys(comp_vies['Termo']))
for j, (m, cor_m) in enumerate(cores_mod.items()):
    t = comp_vies[comp_vies['Modelo'] == m].set_index('Termo').reindex(termos_ord)
    mul_forest(ax, t['TR'], t['li'], t['ls'], x=np.arange(3) + (j - 1) * 0.24, cor=cor_m, label=m,
               marker=['s', 'D', 'o'][j],
               textos=[fmt_br(v, 2) for v in t['TR']] if m != 'OLS log, todos (censura ignorada)' else None)
mul_eixo_razao(ax, np.r_[comp_vies['li'], comp_vies['ls']])
ax.set_xticks(range(3), [quebra(t, 18) for t in termos_ord])
ax.set_xlim(-0.6, 2.8)
ax.set(ylabel='Razão de tempos exp(β) (IC 95%; escala log)', title='Mesmos termos, três estimadores')
legenda_abaixo(ax, ncol=3, dy=-0.2, fontsize=8.5)
figura(fig, 'mul_vies_forest', 'Ignorar ou descartar os censurados inverte o efeito do mês: com censura, cada mês a mais '
       'alonga o tempo típico', secao='5.1.3',
       nota='linha horizontal em 1 = nenhum efeito. Rótulos: estimativa pontual dos dois estimadores em contraste.')

meses = list(mul['mes_distribuicao'].cat.categories)
med_sent, med_km, n_mes = [], [], []
for m in meses:
    sub = mul[mul['mes_distribuicao'] == m]
    med_sent.append(sub.loc[sub['E'] == 1, 'T'].median())
    km = KaplanMeierFitter().fit(sub['T'], sub['E'])
    med_km.append(km.median_survival_time_)
    n_mes.append(len(sub))
fig, ax = plt.subplots(figsize=(11, 4.8))
tab_med = pd.DataFrame({'Mediana entre os sentenciados (condicional)': med_sent,
                        'Mediana de Kaplan-Meier (com censura)': [v if np.isfinite(v) else np.nan for v in med_km]},
                       index=[f'{m}\n(n = {n})' for m, n in zip(meses, n_mes)])
barras_agrupadas(ax, tab_med, cores={tab_med.columns[0]: COR_VIES, tab_med.columns[1]: COR_MODELO}, rotular=True,
                 fmt=lambda v: fmt_br(v, 1 if not float(v).is_integer() else 0),
                 ylabel='Tempo mediano até a sentença (dias)', xlabel=ROTULOS['mes_distribuicao'], legenda=False)
for xi, v in enumerate(med_km):
    if not np.isfinite(v):
        ax.annotate('não\natingida', (xi + 0.2, 0), xytext=(0, 4), textcoords='offset points', ha='center',
                    va='bottom', fontsize=8, color=TINTA_2)
legenda_abaixo(ax, ncol=2, dy=-0.22)
figura(fig, 'mul_vies_medianas_mes', 'Por mês de distribuição, a mediana condicional despenca no fim do recrutamento; '
       'a de Kaplan-Meier cresce', secao='5.1.3',
       nota='mediana condicional = só processos já sentenciados (enviesada para tempos curtos nos meses com pouco seguimento); '
            '"não atingida" = menos da metade do mês foi sentenciada até 07/10/2026.')
''')

interp('mul_ols_vies')

# =====================================================================
md(r'''
## 5.2 Regressão logística para o acordo e logit multinomial para o tipo de desfecho

O acordo é um desfecho **binário** e existe nos três grupos (no Controle, só fora de audiência). O modelo logístico é logit π(x) = β₀ + x′β, e exp(βⱼ) é a **razão de chances (RC)** (ARTES; BARROSO, 2023, eq. 10.1-10.3, p. 357-358).

**O problema do seguimento.** A variável `acordo` só está definida para os processos encerrados (nos ativos ainda não se sabe), e entre os encerrados `acordo = 1` coincide exatamente com sentença homologatória. Três definições de resposta, cada uma com sua limitação:

| Definição | Amostra | Limitação |
|---|---|---|
| (A) acordo entre os **encerrados** | 732 | condicional a ter encerrado; mês absorve a diferença de seguimento |
| (B) acordo homologado **até 60 dias** | todos os 938 (seguimento mínimo = 65 dias) | horizonte curto, poucos eventos; sem censura |
| (C) acordo homologado **até 120 dias** | os 688 com seguimento ≥ 120 dias | perde os distribuídos a partir de junho |

O seguimento (`log_followup`) é função determinística da data de distribuição: a correlação com o mês é de cerca de −0,97 (célula inicial). Não é possível pôr os dois no mesmo modelo (ver VIF em 5.2.2); o mês já faz o papel do seguimento. As definições (B) e (C) são as análises sem viés de seguimento, porque todos os incluídos foram observados durante todo o horizonte.

### 5.2.1 Modelo (A): acordo ~ grupo + mês, entre os encerrados

Testes:

- **razão de verossimilhanças (TRV)** do grupo: compara `grupo + mês` com `mês` só. H0: β_Presencial = β_Remota = 0 (os ritos não alteram a chance de acordo, dado o mês); H1: algum é ≠ 0; χ² com 2 g.l.;
- **Wald** de cada contraste (z = β/EP), com correção de Holm para os três pares (Presencial × Controle, Remota × Controle, Remota × Presencial);
- **pseudo-R²** de McFadden (1 − ℓ₁/ℓ₀) e de Nagelkerke (Cox-Snell reescalado para máximo 1).
''')

code(r'''
enc = mul[mul['encerrado_b']].copy()

def mul_logit(formula, dados_mod, formula_red=None, nome=''):
    res = smf.logit(formula, data=dados_mod).fit(disp=0)
    n = res.nobs
    cs = 1 - np.exp(2 * (res.llnull - res.llf) / n)
    nag = cs / (1 - np.exp(2 * res.llnull / n))
    saida = {'res': res, 'mcfadden': res.prsquared, 'nagelkerke': nag, 'n': int(n), 'eventos': int(res.model.endog.sum())}
    if formula_red is not None:
        red = smf.logit(formula_red, data=dados_mod).fit(disp=0)
        saida['trv'] = 2 * (res.llf - red.llf)
        saida['trv_gl'] = int(res.df_model - red.df_model)
        saida['trv_p'] = stats.chi2.sf(saida['trv'], saida['trv_gl'])
    return saida

def mul_tab_rc(res):
    ic = np.exp(res.conf_int())
    return pd.DataFrame({'Termo': [NOMES_COEF.get(i, i) for i in res.params.index],
                         'RC': np.exp(res.params).to_numpy(), 'IC 95% inf.': ic[0].to_numpy(),
                         'IC 95% sup.': ic[1].to_numpy(), 'z (Wald)': res.tvalues.to_numpy(),
                         'p (Wald)': res.pvalues.to_numpy()})


FMT_RC = {'RC': 3, 'IC 95% inf.': 3, 'IC 95% sup.': 3, 'z (Wald)': 2}

def mul_contrastes_grupo(res):
    # três contrastes de grupo, Wald, com Holm
    b, V = res.params, res.cov_params()
    P, R = 'C(grupo)[T.Presencial]', 'C(grupo)[T.Remota]'
    cont = {'Presencial vs Controle': (b[P], V.loc[P, P]), 'Remota vs Controle': (b[R], V.loc[R, R]),
            'Remota vs Presencial': (b[R] - b[P], V.loc[R, R] + V.loc[P, P] - 2 * V.loc[P, R])}
    lin = []
    for k, (est, var) in cont.items():
        ep = np.sqrt(var)
        lin.append({'Contraste': k, 'RC': np.exp(est), 'li': np.exp(est - 1.96 * ep), 'ls': np.exp(est + 1.96 * ep),
                    'p': 2 * stats.norm.sf(abs(est / ep))})
    t = pd.DataFrame(lin)
    t['p Holm'] = multipletests(t['p'], method='holm')[1]
    return t

def mul_mostra_contrastes(t):
    return pd.DataFrame({'Contraste': t['Contraste'], 'RC': t['RC'], 'IC 95% inf.': t['li'], 'IC 95% sup.': t['ls'],
                         'p (Wald)': t['p'], 'p (Holm)': t['p Holm']})


def mul_barras_prop(ax, tx, ylabel):
    """Proporção por grupo (barras verticais) com IC de Wilson e rótulo 'x,x% (s/n)' acima do IC."""
    p = tx['sum'] / tx['count']
    li, ls = mul_ic_wilson(tx['sum'], tx['count'])
    grupos = [str(g) for g in tx.index]
    barras_verticais(ax, grupos, p, cores=CORES_GRUPO, rotular=False, erro=(li, ls), ylabel=ylabel)
    for i, (s, n, pi, hi) in enumerate(zip(tx['sum'], tx['count'], p, ls)):
        ax.annotate(f'{pct_br(pi)}\n({int(s)}/{int(n)})', (i, hi), xytext=(0, 3), textcoords='offset points',
                    ha='center', va='bottom', fontsize=8.5, color=TINTA)
    ax.set_ylim(0, max(ls) * 1.3)
    eixo_pct(ax)


modA = mul_logit('homolog ~ C(grupo) + mes_num', enc, 'homolog ~ mes_num')
resA = modA['res']
contA = mul_contrastes_grupo(resA)
nota_A = (f"n = {modA['n']} encerrados, {modA['eventos']} acordos; TRV do grupo = {fmt_br(modA['trv'], 2)} "
          f"({modA['trv_gl']} g.l.; p {mul_peq(modA['trv_p'])}); TRV global = {fmt_br(resA.llr, 2)} (p {mul_peq(resA.llr_pvalue)}); "
          f"pseudo-R² de McFadden = {fmt_br(modA['mcfadden'], 3)}, de Nagelkerke = {fmt_br(modA['nagelkerke'], 3)}.")
tabela(mul_tab_rc(resA), 'mul_logit_A', 'Modelo (A): razões de chances de acordo entre os encerrados (logit acordo ~ grupo + mês)',
       secao='5.2.1', formatos=FMT_RC, destaque='p (Wald)', nota=nota_A + ' Referência: Controle. Destaque: p < 0,05.')
tabela(mul_mostra_contrastes(contA), 'mul_logit_A_contrastes',
       'Modelo (A): os três contrastes de grupo (Wald, com correção de Holm)', secao='5.2.1',
       formatos={'RC': 3, 'IC 95% inf.': 3, 'IC 95% sup.': 3}, destaque='p (Holm)',
       nota='RC = razão de chances de acordo, ajustada pelo mês. Destaque: p de Holm < 0,05.')
mul_res['A'] = modA
mul_res['contA'] = contA

fig, eixos = plt.subplots(1, 2, figsize=(13, 4.8), gridspec_kw={'width_ratios': [1.1, 1]})
ax = eixos[0]
mul_forest(ax, contA['RC'], contA['li'], contA['ls'],
           textos=[f"RC = {fmt_br(r['RC'], 2)}\np Holm {mul_peq(r['p Holm'])}" for _, r in contA.iterrows()])
mul_eixo_razao(ax, np.r_[contA['li'], contA['ls']])
ax.set_xticks(range(3), [quebra(c, 12) for c in contA['Contraste']])
ax.set_xlim(-0.5, 2.9)
ax.set(ylabel='Razão de chances de acordo (IC 95%; escala log)', title='Contrastes do modelo (A), ajustados pelo mês')
anotar_teste(ax, texto_teste('TRV do grupo (2 g.l.)', f"χ² = {fmt_br(modA['trv'], 2)}", modA['trv_p']), loc='upper left')
ax = eixos[1]
tx = enc.groupby('grupo', observed=True)['homolog'].agg(['sum', 'count'])
mul_barras_prop(ax, tx, 'Acordos homologados entre os encerrados (%)')
ax.set_title('Proporção bruta de acordo (IC 95% de Wilson)')
figura(fig, 'mul_logit_A_rc', 'Entre os encerrados, a Remota tem cerca do dobro da chance de acordo do Controle; '
       'Presencial não difere', secao='5.2.1', nota=nota_A)
''')

interp('mul_log_coef')

md(r'''
### 5.2.2 Multicolinearidade (VIF)

O fator de inflação da variância, VIFⱼ = 1/(1 − R²ⱼ), mede quanto a variância de β̂ⱼ é inflada pela correlação de xⱼ com os demais preditores. Referências usuais: VIF > 5 merece atenção e VIF > 10 indica colinearidade grave. Calcula-se para o modelo (A) e, para mostrar por que o seguimento não entra junto com o mês, para o modelo (A) acrescido de log(seguimento).
''')

code(r'''
def mul_vif(res):
    X = pd.DataFrame(res.model.exog, columns=res.model.exog_names)
    return pd.Series({NOMES_COEF.get(c, c): variance_inflation_factor(X.values, i)
                      for i, c in enumerate(X.columns) if c != 'Intercept'})

vifA = mul_vif(resA)
resA_fu = smf.logit('homolog ~ C(grupo) + mes_num + log_followup', data=enc).fit(disp=0)
vifA_fu = mul_vif(resA_fu)
tab_vif = pd.DataFrame({'VIF modelo (A)': vifA, 'VIF (A) + log(seguimento)': vifA_fu}).rename_axis('Preditor')
tabela(tab_vif, 'mul_vif', 'Fator de inflação da variância (VIF) dos preditores do modelo (A), sem e com o seguimento',
       secao='5.2.2', casas=2, nota='VIF > 5 merece atenção; VIF > 10 indica colinearidade grave. "–": termo fora do modelo.')
fig, ax = plt.subplots(figsize=(10, 4.6))
nomes = list(vifA_fu.index)
barras_agrupadas(ax, tab_vif.reindex(nomes), cores={'VIF modelo (A)': COR_MODELO, 'VIF (A) + log(seguimento)': COR_VIES},
                 rotular=True, fmt=lambda v: fmt_br(v, 1), quebrar=16, ylabel='VIF', legenda=False)
for lim, txt in [(5, 'VIF = 5 (atenção)'), (10, 'VIF = 10 (colinearidade grave)')]:
    ax.axhline(lim, color=TINTA_2, lw=1, zorder=1)
    ax.annotate(txt, (1, lim), xycoords=('axes fraction', 'data'), xytext=(-2, 3), textcoords='offset points',
                ha='right', va='bottom', fontsize=8.5, color=TINTA_2)
ax.set_title('VIF por preditor')
legenda_abaixo(ax, ncol=2, dy=-0.2, labels=['Modelo (A): grupo + mês', 'Modelo (A) + log(seguimento)'])
figura(fig, 'mul_vif', 'Mês e log(seguimento) são quase colineares (VIF ≈ 17): o mês já faz o papel do seguimento',
       secao='5.2.2', nota='VIF = 1/(1 − R²ⱼ) da regressão de cada preditor sobre os demais; barras ausentes = termo fora do modelo.')
''')

interp('mul_log_vif')

md(r'''
### 5.2.3 Calibração: teste de Hosmer-Lemeshow

Ordenam-se os processos pela probabilidade prevista π̂ e formam-se g = 10 grupos; HL = Σ (Oₖ − nₖπ̄ₖ)² / [nₖπ̄ₖ(1 − π̄ₖ)] segue χ² com g − 2 g.l. (ARTES; BARROSO, 2023, eq. 10.4, p. 358-359). H0: o modelo está calibrado (as frequências observadas de acordo coincidem com as previstas em cada grupo); H1: não está. Como só há 24 padrões de covariáveis (3 grupos × 8 meses), muitos processos têm a mesma π̂; os empates são repartidos pela ordem (rank), o que mantém os 10 grupos. O gráfico de calibração (observado × previsto, com IC de Wilson) é o gráfico do teste.
''')

code(r'''
def hosmer_lemeshow(y, p, g=10):
    t = pd.DataFrame({'y': np.asarray(y, float), 'p': np.asarray(p, float)})
    t['grp'] = pd.qcut(t['p'].rank(method='first'), g, labels=False)
    agg = t.groupby('grp').agg(n=('y', 'size'), O=('y', 'sum'), pbar=('p', 'mean'))
    agg['E'] = agg['n'] * agg['pbar']
    hl = (((agg['O'] - agg['E']) ** 2) / (agg['E'] * (1 - agg['pbar']))).sum()
    return hl, g - 2, stats.chi2.sf(hl, g - 2), agg

def grafico_calibracao(ax, agg, titulo):
    li, ls = mul_ic_wilson(agg['O'], agg['n'])
    obs = agg['O'] / agg['n']
    ax.errorbar(agg['pbar'], obs, yerr=[obs - li, ls - obs], fmt='o', ms=6, color=COR_MODELO, capsize=3, zorder=3)
    lim = max(agg['pbar'].max(), ls.max()) * 1.1
    ax.plot([0, lim], [0, lim], color=TINTA_2, lw=1, zorder=1)
    ax.annotate('calibração perfeita', (lim * 0.97, lim * 0.97), ha='right', va='bottom', fontsize=8.5, color=TINTA_2,
                rotation=45, rotation_mode='anchor', xytext=(0, 3), textcoords='offset points')
    ax.set(xlim=(0, lim), ylim=(0, lim), xlabel='Probabilidade prevista de acordo (média do decil)',
           ylabel='Proporção observada de acordo (IC 95% de Wilson)', title=titulo)
    ax.set_aspect('equal')
    eixo_pct(ax, 'x'); eixo_pct(ax, 'y')
    ax.grid(axis='both', visible=True)

hlA, glA, pA_hl, aggA = hosmer_lemeshow(resA.model.endog, resA.predict())
mul_res['hlA'] = (hlA, pA_hl)
print(f'Hosmer-Lemeshow modelo (A): HL = {fmt_br(hlA, 2)}, {glA} g.l., p {p_br(pA_hl)}')
tab_hl = pd.DataFrame({'Decil de π̂': np.arange(1, len(aggA) + 1), 'Processos (n)': aggA['n'].to_numpy(),
                       'Acordos observados (O)': aggA['O'].to_numpy(), 'π̂ média': aggA['pbar'].to_numpy(),
                       'Acordos esperados (E = n·π̂)': aggA['E'].to_numpy()})
tabela(tab_hl, 'mul_hl', 'Teste de Hosmer-Lemeshow do modelo (A): acordos observados × esperados por decil de probabilidade',
       secao='5.2.3', formatos={'π̂ média': 3, 'Acordos esperados (E = n·π̂)': 1},
       nota=f'HL = {fmt_br(hlA, 2)}, {glA} g.l., p {mul_peq(pA_hl)} (H0: modelo calibrado).')
fig, ax = plt.subplots(figsize=(6, 5.6))
grafico_calibracao(ax, aggA, 'Observado × previsto, por decil')
anotar_teste(ax, texto_teste('Hosmer-Lemeshow (H0: calibrado)', f'HL = {fmt_br(hlA, 2)}; {glA} g.l.', pA_hl),
             loc='upper left')
figura(fig, 'mul_hl', 'O modelo (A) está calibrado: os decis ficam junto da diagonal', secao='5.2.3',
       nota=f'n = {modA["n"]} encerrados em 10 grupos de igual tamanho, ordenados pela probabilidade prevista.')
''')

interp('mul_log_hl')

md(r'''
### 5.2.4 Discriminação: ROC, AUC, Gini e KS

Calibração diz se as probabilidades são corretas *em média*; discriminação diz se o modelo **ordena** bem quem faz e quem não faz acordo.

- **AUC** (área sob a curva ROC): probabilidade de um processo com acordo ter π̂ maior que um sem acordo. Referências de Hosmer, Lemeshow e Sturdivant reproduzidas por Artes e Barroso (2023, tab. 10.3, p. 365): 0,5 sem discriminação; 0,5-0,7 pobre; 0,7-0,8 aceitável; 0,8-0,9 excelente; ≥ 0,9 excepcional. IC 95% por *bootstrap* percentil (2.000 reamostras).
- **Gini** = 2·AUC − 1 (p. 364).
- **KS**: distância máxima entre as funções de distribuição dos escores dos dois grupos (eq. 10.5, p. 365-367). O teste KS de duas amostras tem H0: os escores de quem fez e de quem não fez acordo têm a mesma distribuição.
- **Validação**: a AUC na própria amostra é otimista. Artes e Barroso recomendam separar 20-30% para validação (p. 359); aqui usam-se uma partição 70/30 estratificada e a validação cruzada estratificada em 10 partes.
''')

code(r'''
def auc_bootstrap(y, p, B=2000, rng=RNG_MUL):
    y, p = np.asarray(y), np.asarray(p)
    vals = []
    for _ in range(B):
        idx = rng.integers(0, len(y), len(y))
        if y[idx].min() == y[idx].max():
            continue
        vals.append(roc_auc_score(y[idx], p[idx]))
    return np.percentile(vals, [2.5, 97.5])

def ks_escores(y, p):
    y, p = np.asarray(y), np.asarray(p)
    r = stats.ks_2samp(p[y == 1], p[y == 0])
    return r.statistic, r.pvalue

def auc_validacao(formula, dados_mod, resposta, k=10, rng_seed=SEMENTE):
    y = dados_mod[resposta].values
    # 70/30 estratificado
    rng = np.random.default_rng(rng_seed)
    idx_val = np.concatenate([rng.choice(np.where(y == c)[0], int(round(0.3 * (y == c).sum())), replace=False) for c in (0, 1)])
    mask = np.zeros(len(y), bool); mask[idx_val] = True
    r = smf.logit(formula, data=dados_mod[~mask]).fit(disp=0)
    auc_7030 = roc_auc_score(y[mask], r.predict(dados_mod[mask]))
    # k-fold estratificado
    prev = np.zeros(len(y))
    for tr, te in StratifiedKFold(k, shuffle=True, random_state=rng_seed).split(np.zeros(len(y)), y):
        r = smf.logit(formula, data=dados_mod.iloc[tr]).fit(disp=0)
        prev[te] = r.predict(dados_mod.iloc[te])
    return auc_7030, roc_auc_score(y, prev)

yA, pA = resA.model.endog, resA.predict()
aucA = roc_auc_score(yA, pA)
icA = auc_bootstrap(yA, pA)
ksA, ksA_p = ks_escores(yA, pA)
auc7030A, auccvA = auc_validacao('homolog ~ C(grupo) + mes_num', enc, 'homolog')
mul_res['aucA'] = (aucA, icA, auccvA, ksA)
print(f'AUC (amostra toda) = {fmt_br(aucA, 3)} (IC 95% bootstrap {fmt_br(icA[0], 3)} a {fmt_br(icA[1], 3)}); '
      f'Gini = {fmt_br(2 * aucA - 1, 3)}')
print(f'AUC validação 70/30 = {fmt_br(auc7030A, 3)}; AUC validação cruzada 10 partes = {fmt_br(auccvA, 3)}')
print(f'KS = {fmt_br(ksA, 3)} (p {p_br(ksA_p)})')

fig, eixos = plt.subplots(1, 2, figsize=(12.5, 5))
fpr, tpr, _ = roc_curve(yA, pA)
ax = eixos[0]
ax.plot(fpr, tpr, color=COR_MODELO, lw=2, label='Modelo (A), na amostra')
ax.plot([0, 1], [0, 1], color=TINTA_2, lw=1, label='Sem discriminação (AUC = 0,5)')
ax.set(xlabel='1 − especificidade (falsos positivos)', ylabel='Sensibilidade (verdadeiros positivos)',
       title='Curva ROC', xlim=(0, 1), ylim=(0, 1.01))
ax.set_aspect('equal')
ax.grid(axis='both', visible=True)
ax.legend(loc='lower right')
anotar_teste(ax, f'AUC = {mul_ic(aucA, *icA)}\nGini = {fmt_br(2 * aucA - 1, 3)}\n'
                 f'AUC validação 70/30 = {fmt_br(auc7030A, 3)}\nAUC validação cruzada = {fmt_br(auccvA, 3)}',
             loc='upper left')
ax = eixos[1]
for c, cor, rot in [(1, CORES_DESFECHO['Homologação'], 'Com acordo'), (0, COR_MODELO, 'Sem acordo')]:
    v = np.sort(pA[yA == c])
    ax.step(v, np.arange(1, len(v) + 1) / len(v), where='post', color=cor, lw=2,
            label=f'{rot} (n = {fmt_br(len(v), 0)})')
ax.set(xlabel='Probabilidade prevista de acordo, π̂', ylabel='Proporção acumulada dos processos (FDA empírica)',
       title='Distribuição dos escores: com × sem acordo')
eixo_pct(ax, 'x'); eixo_pct(ax, 'y')
ax.grid(axis='both', visible=True)
ax.legend(loc='lower right')
anotar_teste(ax, texto_teste('Kolmogorov-Smirnov (H0: mesmos escores)', f'KS = {fmt_br(ksA, 3)}', ksA_p), loc='upper left')
figura(fig, 'mul_roc_A', f'O modelo (A) discrimina mal o acordo: AUC de {fmt_br(aucA, 2)} na amostra e '
       f'{fmt_br(auccvA, 2)} fora dela',
       secao='5.2.4', nota='AUC com IC 95% bootstrap percentil (2.000 reamostras); validação cruzada estratificada em 10 partes. '
                           'Referência: 0,5 = sem discriminação; 0,7-0,8 = aceitável (Artes; Barroso, 2023, p. 365).')
''')

interp('mul_log_roc')

md(r'''
### 5.2.5 Sensibilidade ao seguimento: horizontes fixos de 60 e 120 dias

Repete-se o modelo com as definições (B) e (C), em que todos os processos incluídos foram observados durante todo o horizonte, de modo que "não acordo até τ" é informação completa (não há censura antes de τ). O que importa é se a RC do grupo muda de direção ou de magnitude em relação ao modelo (A).
''')

code(r'''
mul['acordo60'] = ((mul['homolog'] == 1) & (mul['T'] <= 60)).astype(int)
mul['acordo120'] = ((mul['homolog'] == 1) & (mul['T'] <= 120)).astype(int)
base120 = mul[mul['followup_f'] >= 120].copy()
modB = mul_logit('acordo60 ~ C(grupo) + mes_num', mul, 'acordo60 ~ mes_num')
modC = mul_logit('acordo120 ~ C(grupo) + mes_num', base120, 'acordo120 ~ mes_num')
mul_res['B'], mul_res['C'] = modB, modC
cont_h = []
for rot, m in [('(A) encerrados', modA), ('(B) até 60 dias, todos', modB), ('(C) até 120 dias, seguimento ≥ 120', modC)]:
    t = mul_contrastes_grupo(m['res'])
    t.insert(0, 'Definição', rot)
    t['n'], t['acordos'], t['TRV p'] = m['n'], m['eventos'], m['trv_p']
    cont_h.append(t)
cont_h = pd.concat(cont_h, ignore_index=True)
mul_res['cont_h'] = cont_h
tabela(pd.DataFrame({'Definição': cont_h['Definição'], 'n': cont_h['n'], 'Acordos': cont_h['acordos'],
                     'Contraste': cont_h['Contraste'], 'RC': cont_h['RC'], 'IC 95% inf.': cont_h['li'],
                     'IC 95% sup.': cont_h['ls'], 'p (Holm)': cont_h['p Holm'], 'p do TRV do grupo': cont_h['TRV p']}),
       'mul_logit_horizontes', 'Razões de chances de acordo por grupo nas três definições do desfecho (A, B, C)',
       secao='5.2.5', formatos={'RC': 3, 'IC 95% inf.': 3, 'IC 95% sup.': 3}, destaque='p (Holm)',
       nota='modelos logit acordo ~ grupo + mês; contrastes de Wald com Holm dentro de cada definição. Destaque: p de Holm < 0,05.')

defs = list(dict.fromkeys(cont_h['Definição']))
cores_def = dict(zip(defs, [COR_MODELO, '#8FA3B5', COR_VIES]))
fig, ax = plt.subplots(figsize=(11, 5))
for j, d in enumerate(defs):
    t = cont_h[cont_h['Definição'] == d].reset_index(drop=True)
    mul_forest(ax, t['RC'], t['li'], t['ls'], x=np.arange(3) + (j - 1) * 0.25, cor=cores_def[d], label=d,
               marker=['o', 's', 'D'][j])
mul_eixo_razao(ax, np.r_[cont_h['li'], cont_h['ls']])
ax.set_xticks(range(3), list(contA['Contraste']))
ax.set(ylabel='Razão de chances de acordo (IC 95%; escala log)', title='Contrastes de grupo em cada definição')
legenda_abaixo(ax, ncol=3, dy=-0.14)
figura(fig, 'mul_logit_horizontes_rc', 'A vantagem da Remota sobre o Controle no acordo aparece nas três definições '
       '(RC entre 1,8 e 2,7), com IC largo no horizonte de 60 dias', secao='5.2.5',
       nota='(A) acordo entre encerrados; (B) acordo homologado até 60 dias, todos os 938; (C) até 120 dias, os 688 com seguimento ≥ 120 dias.')

tab_def = {}
erros_def = {}
for rot, col, base in [('(A) encerrados', 'homolog', enc), ('(B) até 60 dias', 'acordo60', mul),
                       ('(C) até 120 dias', 'acordo120', base120)]:
    tx = base.groupby('grupo', observed=True)[col].agg(['sum', 'count'])
    tab_def[rot] = tx['sum'] / tx['count']
    erros_def[rot] = mul_ic_wilson(tx['sum'], tx['count'])
tab_def = pd.DataFrame(tab_def).T[ORDEM_GRUPO]
fig, ax = plt.subplots(figsize=(10, 4.8))
barras_agrupadas(ax, tab_def, cores=CORES_GRUPO, rotular=True, fmt=lambda v: pct_br(v, 1), quebrar=18,
                 erro={g: (np.array([erros_def[d][0][g] for d in tab_def.index]),
                           np.array([erros_def[d][1][g] for d in tab_def.index])) for g in ORDEM_GRUPO},
                 ylabel='Processos com acordo homologado (%)', xlabel='Definição do desfecho')
eixo_pct(ax)
ax.set_title('Proporção bruta de acordo por grupo (IC 95% de Wilson)')
figura(fig, 'mul_logit_horizontes_prop', 'Em todas as definições, a Remota tem a maior proporção de acordo e o Controle, a menor',
       secao='5.2.5', nota='rótulo = proporção pontual (o topo da barra de erro é o limite superior do IC).')
''')

interp('mul_log_horiz')

md(r'''
### 5.2.6 Acordo **na audiência**, no subconjunto com audiência realizada

Aqui a resposta é `acordo_ac` e a amostra são os 352 processos com audiência realizada (só Presencial e Remota: no Controle o acordo em audiência é zero estrutural, E20). Preditores: modalidade (Remota × Presencial), audiência **híbrida** (uma parte remota numa pauta presencial, Res. CNJ 481) e mês. A híbrida é **pós-sorteio**: a RC é associação, não efeito causal.

**Cuidado com poucos eventos.** Há só 17 acordos em audiência. A regra prática de ~10 eventos por parâmetro (EPV) admite no máximo 1 ou 2 preditores; com 3, as estimativas por máxima verossimilhança são instáveis e os IC largos. O resultado é exploratório. TRV do modelo: H0: nenhum preditor associa-se ao acordo em audiência.
''')

code(r'''
sub_ac = mul[mul['ac_realizada'].fillna(False).astype(bool)].copy()
sub_ac['y_ac'] = sub_ac['acordo_ac'].astype(int)
tab_ac = pd.crosstab([sub_ac['grupo'].astype(str), sub_ac['hibrida_b'].map({0: 'não híbrida', 1: 'híbrida'})],
                     sub_ac['y_ac'].map({0: 'Sem acordo na AC', 1: 'Acordo na AC'}))
tab_ac = tab_ac.rename_axis(columns=None).reset_index().rename(columns={'grupo': 'Grupo', 'hibrida_b': 'Audiência'})
tab_ac['Total'] = tab_ac['Sem acordo na AC'] + tab_ac['Acordo na AC']
tab_ac['% com acordo'] = 100 * tab_ac['Acordo na AC'] / tab_ac['Total']
tabela(tab_ac[['Grupo', 'Audiência', 'Acordo na AC', 'Sem acordo na AC', 'Total', '% com acordo']], 'mul_ac_hibrida',
       'Acordo na audiência por modalidade e audiência híbrida (processos com AC realizada)', secao='5.2.6',
       nota='só Presencial e Remota: no Controle não há audiência obrigatória (zero estrutural).')
modAC = mul_logit('y_ac ~ remota + hibrida_b + mes_num', sub_ac)
resAC = modAC['res']
epv = modAC['eventos'] / resAC.df_model
aucAC = roc_auc_score(resAC.model.endog, resAC.predict())
icAC = auc_bootstrap(resAC.model.endog, resAC.predict())
mul_res['AC'] = (modAC, aucAC, icAC)
nota_AC = (f"n = {modAC['n']} audiências realizadas, {modAC['eventos']} acordos na AC; eventos por parâmetro (EPV) = {fmt_br(epv, 1)}; "
           f"TRV global = {fmt_br(resAC.llr, 2)} ({int(resAC.df_model)} g.l.; p {mul_peq(resAC.llr_pvalue)}); "
           f"McFadden = {fmt_br(modAC['mcfadden'], 3)}; AUC na amostra = {mul_ic(aucAC, *icAC)}.")
tabela(mul_tab_rc(resAC), 'mul_logit_ac', 'Logit do acordo na audiência ~ modalidade + híbrida + mês (exploratório: 17 eventos)',
       secao='5.2.6', formatos=FMT_RC, destaque='p (Wald)', nota=nota_AC + ' Referência da modalidade: Presencial.')
fig, ax = plt.subplots(figsize=(8.5, 4.8))
ic = np.exp(resAC.conf_int()).iloc[1:]
rc = np.exp(resAC.params).iloc[1:]
mul_forest(ax, rc, ic[0], ic[1], textos=[f'RC = {fmt_br(rc[t], 2)}\np {mul_peq(resAC.pvalues[t])}' for t in rc.index])
mul_eixo_razao(ax, np.r_[ic[0], ic[1]])
ax.set_xticks(range(len(rc)), [quebra(NOMES_COEF[t], 14) for t in rc.index])
ax.set_xlim(-0.5, len(rc) - 0.1)
ax.set(ylabel='Razão de chances de acordo na AC (IC 95%; escala log)', title='Razões de chances ajustadas')
anotar_teste(ax, texto_teste(f'TRV global ({int(resAC.df_model)} g.l.)', f'χ² = {fmt_br(resAC.llr, 2)}', resAC.llr_pvalue),
             loc='lower left')
figura(fig, 'mul_logit_ac', 'No acordo dentro da audiência, nem a modalidade nem a híbrida fazem diferença detectável',
       secao='5.2.6', nota=nota_AC)
''')

interp('mul_log_ac')

md(r'''
### 5.2.7 Logit multinomial para o tipo de sentença

Entre os 708 sentenciados, o tipo de sentença tem três categorias: **mérito** (referência), **homologação** e **sem mérito**. O logit multinomial (`statsmodels` `MNLogit`) estima, para cada categoria k ≠ mérito, log[P(k)/P(mérito)] = β₀ₖ + x′βₖ; exp(βₖ) é a **razão de riscos relativos (RRR)**: quanto a chance de "k em vez de mérito" se multiplica. A Parte III mostrou, na tabela, que os tratados têm mais extinções sem mérito; o modelo verifica se isso se mantém controlando o mês.

TRV do grupo (H0: β_grupo = 0 nas duas equações; 4 g.l.). O seguimento continua sendo uma ameaça: tipos de sentença mais rápidos (homologação, sem mérito por ausência) aparecem mais cedo e estão super-representados entre os distribuídos nos últimos meses; o mês ajusta parcialmente isso, e repete-se o modelo só com os processos de **seguimento ≥ 150 dias** (distribuídos até ~10/05), em que quase todos já foram sentenciados. O pressuposto de independência de alternativas irrelevantes (IIA) é plausível: as três categorias são decisões juridicamente distintas.
''')

code(r'''
COD_TIPO = {'Mérito': 0, 'Homologação': 1, 'Sem mérito': 2}
ROT_TIPO = {1: 'Homologação vs Mérito', 2: 'Sem mérito vs Mérito'}
sent['y_tipo'] = sent['desfecho'].map(COD_TIPO)

def mul_mnlogit(base):
    r = smf.mnlogit('y_tipo ~ C(grupo) + mes_num', data=base).fit(disp=0, maxiter=200)
    r0 = smf.mnlogit('y_tipo ~ mes_num', data=base).fit(disp=0, maxiter=200)
    trv = 2 * (r.llf - r0.llf)
    return r, trv, stats.chi2.sf(trv, 4)

def mul_tab_rrr(r):
    ic = r.conf_int()
    eqs = list(dict.fromkeys(ic.index.get_level_values(0)))
    lin = []
    for j, col in enumerate(r.params.columns):
        for termo in r.params.index:
            k = j + 1
            lo, hi = ic.loc[(eqs[j], termo)]
            lin.append({'Equação': ROT_TIPO[k], 'Termo': NOMES_COEF.get(termo, termo),
                        'RRR': np.exp(r.params.loc[termo, col]), 'li': np.exp(lo), 'ls': np.exp(hi),
                        'p': r.pvalues.loc[termo, col]})
    return pd.DataFrame(lin)

mnl, trv_mnl, p_mnl = mul_mnlogit(sent)
sent150 = sent[sent['followup_f'] >= 150]
base150 = mul[mul['followup_f'] >= 150]
mnl150, trv150, p150 = mul_mnlogit(sent150)
rrr = mul_tab_rrr(mnl)
rrr150 = mul_tab_rrr(mnl150)
mul_res['mnl'] = (rrr, trv_mnl, p_mnl, mnl.prsquared, rrr150, p150)
nota_mnl = (f'n = {int(mnl.nobs)} sentenciados; TRV do grupo = {fmt_br(trv_mnl, 2)} (4 g.l.; p {mul_peq(p_mnl)}); '
            f'pseudo-R² de McFadden = {fmt_br(mnl.prsquared, 3)}. Categoria de referência: sentença de mérito; grupo de referência: Controle.')
mostra = lambda t: t.rename(columns={'li': 'IC 95% inf.', 'ls': 'IC 95% sup.'})[['Equação', 'Termo', 'RRR', 'IC 95% inf.', 'IC 95% sup.', 'p']]
FMT_RRR = {'RRR': 3, 'IC 95% inf.': 3, 'IC 95% sup.': 3}
tabela(mostra(rrr), 'mul_mnlogit', 'Logit multinomial do tipo de sentença ~ grupo + mês: razões de riscos relativos (RRR)',
       secao='5.2.7', formatos=FMT_RRR, destaque='p', nota=nota_mnl + ' Destaque: p < 0,05.')
nota_150 = (f'n = {len(sent150)} sentenciados de {len(base150)} distribuídos com seguimento ≥ 150 dias '
            f'({pct_br(len(sent150) / len(base150))} já sentenciados); TRV do grupo = {fmt_br(trv150, 2)} (p {mul_peq(p150)}).')
tabela(mostra(rrr150[rrr150['Termo'].str.contains('vs Controle')]), 'mul_mnlogit_150',
       'Sensibilidade: RRR dos grupos só com processos de seguimento ≥ 150 dias', secao='5.2.7', formatos=FMT_RRR,
       destaque='p', nota=nota_150 + ' Só os termos de grupo; o modelo inclui o mês.')

# (a) probabilidades previstas no mês mediano: barras 100% empilhadas por grupo
grade = pd.DataFrame({'grupo': pd.Categorical(ORDEM_GRUPO, categories=ORDEM_GRUPO), 'mes_num': np.median(sent['mes_num'])})
prev = np.asarray(mnl.predict(grade))
prev_df = pd.DataFrame(prev, index=ORDEM_GRUPO, columns=['Mérito', 'Homologação', 'Sem mérito'])
prev_df = prev_df[[k for k in ORDEM_DESFECHO if k in prev_df.columns]]
fig, ax = plt.subplots(figsize=(8.5, 5))
barras_empilhadas(ax, prev_df, cores=CORES_DESFECHO, fmt=lambda v: pct_br(v, 0), largura=0.55,
                  ylabel='Probabilidade prevista do tipo de sentença (%)', rotulos_serie=ROTULO_DESFECHO,
                  ns=[int((sent['grupo'] == g).sum()) for g in ORDEM_GRUPO])
ax.set_title(f'Mês de distribuição fixado na mediana ({MESES_PT[int(np.median(sent["mes_num"])) - 1]})')
anotar_teste(ax, texto_teste('TRV do grupo (4 g.l.)', f'χ² = {fmt_br(trv_mnl, 2)}', p_mnl), loc='upper left')
ax.set_ylim(0, 1.18)
ax.set_yticks(np.arange(0, 1.01, 0.25))
figura(fig, 'mul_mnlogit_prev', 'Com o mês fixo, o Controle tem quase metade de sentenças de mérito; Presencial e Remota, '
       'mais extinções sem mérito e homologações', secao='5.2.7', nota=nota_mnl)

# (b) RRR dos grupos nas duas equações
t = rrr[rrr['Termo'].str.contains('vs Controle')].reset_index(drop=True)
fig, ax = plt.subplots(figsize=(10, 5))
cores_t = [CORES_GRUPO['Presencial' if 'Presencial' in r['Termo'] else 'Remota'] for _, r in t.iterrows()]
x_pos = np.array([0, 0.45, 1.4, 1.85])[:len(t)]
mul_forest(ax, t['RRR'], t['li'], t['ls'], x=x_pos, cor=cores_t,
           textos=[f"{fmt_br(r['RRR'], 2)}\np {mul_peq(r['p'])}" for _, r in t.iterrows()])
mul_eixo_razao(ax, np.r_[t['li'], t['ls']])
ax.set_xticks(x_pos, [quebra(r['Termo'], 12) for _, r in t.iterrows()])
for xc, eq in zip([0.225, 1.625], list(dict.fromkeys(t['Equação']))):
    ax.annotate(eq.replace(' vs ', ' em vez de ').lower().capitalize(), (xc, 1), xycoords=('data', 'axes fraction'),
                xytext=(0, 4), textcoords='offset points', ha='center', va='bottom', fontsize=9.5, fontweight='bold')
ax.set_xlim(-0.35, 2.45)
ax.set(ylabel='Razão de riscos relativos (IC 95%; escala log)')
figura(fig, 'mul_mnlogit_rrr', 'Os dois ritos com audiência multiplicam por 2 a 3 a chance de homologação ou de extinção '
       'sem mérito, em vez de mérito', secao='5.2.7', nota=nota_mnl + ' Cor do ponto = grupo comparado ao Controle.')
''')

interp('mul_mnl')

# =====================================================================
md(r'''
## 5.3 Árvores de decisão

Uma árvore de classificação (CART) particiona os dados, recursivamente, em grupos cada vez mais homogêneos quanto à resposta (ARTES; BARROSO, 2023, cap. 11, p. 377-382). Para variáveis ordinais, como o dia de distribuição, as partições são monotônicas (p. 390). O tamanho da árvore é escolhido por **poda de custo-complexidade**, C_α(A) = erro(A) + α·|folhas| (p. 395-396), com α escolhido por **validação cruzada** (5 partes estratificadas). Com tão poucos preditores, a árvore serve para (i) mostrar se há **interações** que o modelo logístico aditivo não captou e (ii) medir, fora da amostra, o poder preditivo realista. Compara-se sempre com a **regra trivial** (prever a classe mais frequente). Exige-se no mínimo 20 processos por folha, para evitar folhas espúrias.

### 5.3.1 Tipo de sentença com preditores basais

Preditores basais (anteriores ao sorteio ou o próprio sorteio): grupo (dois indicadores), dia de distribuição (0 a 214) e origem externa.
''')

code(r'''
def arvore_cv(X, y, classificacao=True, min_folha=20, k=5, semente=SEMENTE):
    Est = DecisionTreeClassifier if classificacao else DecisionTreeRegressor
    base = Est(min_samples_leaf=min_folha, random_state=semente)
    alphas = base.cost_complexity_pruning_path(X, y).ccp_alphas
    alphas = np.unique(np.clip(alphas, 0, None))
    cv = (StratifiedKFold if classificacao else KFold)(k, shuffle=True, random_state=semente)
    score = 'accuracy' if classificacao else 'neg_mean_squared_error'
    medias, eps = [], []
    for a in alphas:
        s = cross_val_score(Est(min_samples_leaf=min_folha, ccp_alpha=a, random_state=semente), X, y, cv=cv, scoring=score)
        medias.append(s.mean()); eps.append(s.std(ddof=1) / np.sqrt(k))
    medias, eps = np.array(medias), np.array(eps)
    i_best = int(np.argmax(medias))
    # regra de 1 erro-padrão: a árvore mais simples (maior α) dentro de 1 EP da melhor
    i_1se = int(np.max(np.where(medias >= medias[i_best] - eps[i_best])[0]))
    a_sel = alphas[i_1se]
    modelo = Est(min_samples_leaf=min_folha, ccp_alpha=a_sel, random_state=semente).fit(X, y)
    prev_cv = cross_val_predict(Est(min_samples_leaf=min_folha, ccp_alpha=a_sel, random_state=semente), X, y, cv=cv)
    return {'modelo': modelo, 'alphas': alphas, 'medias': medias, 'eps': eps, 'a_sel': a_sel,
            'i_best': i_best, 'i_1se': i_1se, 'prev_cv': prev_cv, 'score': score}

def figura_arvore(r, X, y, nomes_classe, titulo, id_, secao, achado_arvore, achado_diag, metrica='Acurácia na validação cruzada',
                  nota=None):
    # (1) a árvore, sozinha e grande, com nós coloridos pela classe majoritária (cores dos desfechos)
    folhas = r['modelo'].get_n_leaves()
    fig, ax = plt.subplots(figsize=(max(9, 2.6 * folhas + 3), 2.2 * (r['modelo'].get_depth() + 1) + 1))
    if folhas > 1:
        mul_arvore(ax, r['modelo'], list(X.columns), classes=nomes_classe,
                   cores_classe={c: CORES_DESFECHO.get(c, CINZA) for c in nomes_classe}, fontsize=9)
        for c in nomes_classe:
            ax.scatter([], [], marker='s', s=90, color=CORES_DESFECHO.get(c, CINZA), alpha=0.55, label=ROTULO_DESFECHO.get(c, c))
        ax.legend(loc='upper left', title='Classe majoritária do nó', fontsize=8.5, frameon=False)
    else:
        ax.text(0.5, 0.5, 'A poda escolheu a árvore de um só nó\n(nenhuma partição melhora a previsão fora da amostra)',
                ha='center', va='center', fontsize=12); ax.axis('off')
    ax.set_title(titulo)
    figura(fig, id_, achado_arvore, secao=secao,
           nota=(nota + ' ' if nota else '') + 'Em cada nó: regra de divisão, % dos processos, proporções de cada classe '
                '(na ordem da legenda de classes) e classe prevista; intensidade da cor = pureza do nó.')
    # (2) diagnóstico: poda, importância e matriz de confusão
    fig, eixos = plt.subplots(1, 3, figsize=(15, 4.6), gridspec_kw={'width_ratios': [1.2, 1, 1]})
    ax = eixos[0]
    ax.errorbar(range(len(r['alphas'])), r['medias'], yerr=r['eps'], fmt='o-', ms=3, lw=1.2, color=COR_MODELO, capsize=2)
    ax.axvline(r['i_1se'], color=COR_VIES, lw=1.2, label='α escolhido (regra de 1 erro-padrão)')
    ax.set(xlabel='Índice de α (árvores cada vez mais simples →)', ylabel=metrica, title='Validação cruzada da poda')
    if r['score'] == 'accuracy':
        eixo_pct(ax)
    ax.legend(loc='lower left', fontsize=8.5)
    ax = eixos[1]
    imp = pd.Series(r['modelo'].feature_importances_, index=X.columns)
    barras_verticais(ax, [NOMES_VAR.get(c, c) for c in imp.index], imp.values, cores=COR_MODELO, quebrar=12,
                     fmt=lambda v: fmt_br(v, 2), ylabel='Importância (redução de impureza)',
                     ymax=max(imp.max() * 1.18, 0.05))
    ax.set_title('Importância das variáveis')
    ax = eixos[2]
    if nomes_classe is not None:
        cm = confusion_matrix(y, r['prev_cv'], labels=list(range(len(nomes_classe))))
        rot_c = [quebra(ROTULO_DESFECHO.get(c, c), 12) for c in nomes_classe]
        sns.heatmap(cm, annot=True, fmt='d', cmap=SEQ, cbar=True, xticklabels=rot_c, yticklabels=rot_c, ax=ax,
                    cbar_kws={'label': 'Processos (n)'}, annot_kws={'fontsize': 9})
        ax.set(xlabel='Previsto (fora da amostra)', ylabel='Observado', title='Matriz de confusão (validação cruzada)')
        ax.tick_params(axis='y', rotation=0)
    figura(fig, id_ + '_diag', achado_diag, secao=secao)
    return imp

X_base = pd.DataFrame({'presencial': sent['presencial'], 'remota': sent['remota'],
                       'dia_estudo': sent['dia_estudo_f'], 'origem_ext': sent['origem_ext']})
y_tipo = sent['y_tipo'].values
nomes_tipo = ['Mérito', 'Homologação', 'Sem mérito']
arvA = arvore_cv(X_base, y_tipo)
base_trivial = np.bincount(y_tipo).max() / len(y_tipo)
acc = accuracy_score(y_tipo, arvA['prev_cv']); bacc = balanced_accuracy_score(y_tipo, arvA['prev_cv'])
mul_res['arvA'] = (arvA['modelo'].get_n_leaves(), acc, bacc, base_trivial)
print(f"Árvore A: {arvA['modelo'].get_n_leaves()} folhas, profundidade {arvA['modelo'].get_depth()}, α = {fmt_br(arvA['a_sel'], 4)}")
print(f'Acurácia VC = {pct_br(acc)} (regra trivial "sempre mérito" = {pct_br(base_trivial)}); '
      f'acurácia balanceada VC = {pct_br(bacc)} (trivial = 33,3%)')
impA = figura_arvore(arvA, X_base, y_tipo, nomes_tipo, 'Árvore A: tipo de sentença ~ preditores basais', 'mul_arvore_A', '5.3.1',
                     f'Árvore A: com grupo, dia de distribuição e origem, o tipo de sentença é pouco previsível '
                     f'(acurácia balanceada fora da amostra de {pct_br(bacc)}; regra trivial, 33,3%)',
                     'Árvore A: poda, importância das variáveis e erros de classificação fora da amostra',
                     nota=f'n = {len(y_tipo)} sentenciados; mínimo de 20 processos por folha.')
''')

interp('mul_arv_tipo')

md(r'''
### 5.3.2 Tipo de sentença nos grupos tratados, com variáveis do processo (exploratória)

Nos grupos Presencial e Remota, acrescentam-se duas variáveis **pós-sorteio**: se a audiência foi realizada e se foi híbrida. A hipótese jurídica da Parte III é que a extinção sem mérito nos tratados decorre da **ausência do autor à audiência obrigatória** (art. 51, I, Lei 9.099/1995). Atenção à causalidade reversa: "audiência não realizada" pode ser causa da extinção (ausência do autor) ou consequência dela (o processo foi extinto, por desistência ou indeferimento, antes da data da audiência). A árvore mostra a **associação**, não separa esses caminhos; para isso seria preciso registrar a data e o motivo da não realização.
''')

code(r'''
trat = sent[sent['grupo'] != 'Controle'].copy()
X_proc = pd.DataFrame({'remota': trat['remota'], 'ac_realizada': trat['ac_realizada'].astype(bool).astype(int),
                       'hibrida': trat['hibrida_b'], 'dia_estudo': trat['dia_estudo_f'], 'origem_ext': trat['origem_ext']})
y_trat = trat['y_tipo'].values
arvB = arvore_cv(X_proc, y_trat)
accB = accuracy_score(y_trat, arvB['prev_cv']); baccB = balanced_accuracy_score(y_trat, arvB['prev_cv'])
trivB = np.bincount(y_trat).max() / len(y_trat)
mul_res['arvB'] = (arvB['modelo'].get_n_leaves(), accB, baccB, trivB)
print(f"Árvore B (tratados, n = {len(trat)}): {arvB['modelo'].get_n_leaves()} folhas; acurácia VC = {pct_br(accB)} "
      f"(trivial = {pct_br(trivB)}); acurácia balanceada VC = {pct_br(baccB)}")
tab_acr = pd.crosstab(X_proc['ac_realizada'].map({1: 'AC realizada', 0: 'AC não realizada'}), trat['desfecho'],
                      normalize='index').reindex(columns=['Homologação', 'Mérito', 'Sem mérito'])
tab_acr = (100 * tab_acr).rename(columns=lambda c: ROTULO_DESFECHO[c] + ' (%)').rename_axis('Audiência de conciliação')
tabela(tab_acr, 'mul_tratados_acr', 'Tipo de sentença nos tratados conforme a audiência foi ou não realizada (% da linha)',
       secao='5.3.2', casas=1, nota=f'n = {len(trat)} sentenciados dos grupos Presencial e Remota.')
impB = figura_arvore(arvB, X_proc, y_trat, nomes_tipo, 'Árvore B: tipo de sentença nos tratados, com variáveis do processo',
                     'mul_arvore_B', '5.3.2',
                     'Árvore B: nos tratados, a audiência não realizada concentra as extinções sem mérito (associação, não causa)',
                     'Árvore B: poda, importância das variáveis e erros de classificação fora da amostra',
                     nota=f'n = {len(y_trat)} sentenciados dos grupos Presencial e Remota; mínimo de 20 processos por folha.')
''')

interp('mul_arv_proc')

md(r'''
### 5.3.3 Acordo entre os encerrados (preditores basais)

A mesma árvore, agora para o acordo (definição A). Como os acordos são só 11% dos encerrados, a acurácia é inútil (a regra trivial "nunca há acordo" acerta 89%); a poda é feita pela acurácia, mas o desempenho é medido pela **AUC fora da amostra** das probabilidades das folhas, comparável à do logit (5.2.4).
''')

code(r'''
X_enc = pd.DataFrame({'presencial': enc['presencial'], 'remota': enc['remota'],
                      'dia_estudo': enc['dia_estudo_f'], 'origem_ext': enc['origem_ext']})
y_enc = enc['homolog'].values
arvC = arvore_cv(X_enc, y_enc)
# a árvore podada por acurácia tende a um nó; para a AUC usa-se a probabilidade de folhas de uma árvore rasa (profundidade 3)
cv5 = StratifiedKFold(5, shuffle=True, random_state=SEMENTE)
prob_cv = cross_val_predict(DecisionTreeClassifier(max_depth=3, min_samples_leaf=20, random_state=SEMENTE),
                            X_enc, y_enc, cv=cv5, method='predict_proba')[:, 1]
auc_arv = roc_auc_score(y_enc, prob_cv)
mul_res['arvC'] = (arvC['modelo'].get_n_leaves(), auc_arv)
print(f"Árvore C (acordo): poda por acurácia escolheu {arvC['modelo'].get_n_leaves()} folha(s); "
      f"AUC VC de uma árvore de profundidade 3 = {fmt_br(auc_arv, 3)} (logit (A), VC: {fmt_br(auccvA, 3)})")
arvC3 = DecisionTreeClassifier(max_depth=3, min_samples_leaf=20, random_state=SEMENTE).fit(X_enc, y_enc)
fig, ax = plt.subplots(figsize=(15, 7))
cls_acordo = ['Sem acordo', 'Acordo']
mul_arvore(ax, arvC3, list(X_enc.columns), classes=cls_acordo,
           cores_classe={'Sem acordo': CINZA, 'Acordo': CORES_DESFECHO['Homologação']}, fontsize=9)
for c, cor in [('Sem acordo', CINZA), ('Acordo (homologação)', CORES_DESFECHO['Homologação'])]:
    ax.scatter([], [], marker='s', s=90, color=cor, alpha=0.55, label=c)
ax.legend(loc='upper left', title='Classe majoritária do nó', fontsize=8.5)
ax.set_title('Árvore de profundidade 3 (exploratória, não podada)')
figura(fig, 'mul_arvore_C', 'Árvore do acordo entre os encerrados: as partições por grupo e calendário quase não separam '
       'quem faz acordo', secao='5.3.3',
       nota=f'n = {len(y_enc)} encerrados ({int(y_enc.sum())} acordos); mínimo de 20 processos por folha. A poda por acurácia '
            f'escolheu {arvC["modelo"].get_n_leaves()} folha(s); esta árvore rasa é só para visualizar a estrutura. '
            'Em cada nó: proporções [sem acordo, acordo].')

fig, ax = plt.subplots(figsize=(6.2, 5.8))
fpr, tpr, _ = roc_curve(y_enc, prob_cv)
ax.plot(fpr, tpr, color=COR_VIES, lw=2, label=f'Árvore (prof. 3), validação cruzada: AUC = {fmt_br(auc_arv, 3)}')
fpr, tpr, _ = roc_curve(yA, pA)
ax.plot(fpr, tpr, color=COR_MODELO, lw=2, label=f'Logit (A), na amostra: AUC = {fmt_br(aucA, 3)}')
ax.plot([0, 1], [0, 1], color=TINTA_2, lw=1, label='Sem discriminação (AUC = 0,5)')
ax.set(xlabel='1 − especificidade (falsos positivos)', ylabel='Sensibilidade (verdadeiros positivos)',
       title='Curvas ROC', xlim=(0, 1), ylim=(0, 1.01))
ax.set_aspect('equal')
ax.grid(axis='both', visible=True)
legenda_abaixo(ax, ncol=1, dy=-0.14)
figura(fig, 'mul_arvore_C_roc', 'Fora da amostra, nem a árvore nem o logit discriminam o acordo muito melhor que o acaso',
       secao='5.3.3', nota=f'AUC do logit (A) em validação cruzada de 10 partes: {fmt_br(auccvA, 3)}.')
''')

interp('mul_arv_acordo')

md(r'''
### 5.3.4 Árvore de sobrevivência (aproximação pelos resíduos martingal)

Árvores de sobrevivência propriamente ditas (LeBlanc e Crowley, 1993) exigem o pacote `scikit-survival`, que não está instalado no ambiente do projeto. A aproximação clássica de Therneau, Grambsch e Fleming (1990) dispensa o pacote: calcula-se o **resíduo martingal de um modelo de Cox nulo**, Mᵢ = δᵢ − Ĥ₀(tᵢ), em que Ĥ₀ é o risco acumulado de Nelson-Aalen. Mᵢ > 0 indica processo sentenciado "antes do esperado" e Mᵢ < 0, processo que demora mais que o esperado (ou censurado tardio). Uma **árvore de regressão** sobre Mᵢ, com poda por validação cruzada (erro quadrático médio), encontra os subgrupos com tempos mais distintos, e as curvas de Kaplan-Meier das folhas mostram o resultado na escala natural. Os 938 processos entram (os censurados contribuem com δ = 0). O log-rank entre folhas é apresentado só como descrição: as partições foram escolhidas para maximizar a diferença, de modo que o valor-p é otimista.
''')

code(r'''
naf = NelsonAalenFitter().fit(mul['T'], mul['E'])
H0 = naf.cumulative_hazard_at_times(mul['T']).values
mul['martingal'] = mul['E'] - H0
X_sob = pd.DataFrame({'presencial': mul['presencial'], 'remota': mul['remota'],
                      'dia_estudo': mul['dia_estudo_f'], 'origem_ext': mul['origem_ext']})
arvS = arvore_cv(X_sob, mul['martingal'].values, classificacao=False, min_folha=40)
mS = arvS['modelo']
r2_cv = 1 - (-arvS['medias'][arvS['i_1se']]) / mul['martingal'].var(ddof=0)
r2_best = 1 - (-arvS['medias'][arvS['i_best']]) / mul['martingal'].var(ddof=0)
print(f"Árvore podada (regra 1 EP): {mS.get_n_leaves()} folha(s); R² VC dos resíduos martingal ≈ {fmt_br(r2_cv, 3)}")
print(f"Melhor α sem a regra 1 EP: R² VC ≈ {fmt_br(r2_best, 3)}")
mS_podada_folhas = mS.get_n_leaves()
if mS.get_n_leaves() == 1:
    # a poda eliminou todas as partições; para visualizar a estrutura, exibe-se uma árvore rasa NÃO validada
    mS = DecisionTreeRegressor(max_depth=2, min_samples_leaf=40, random_state=SEMENTE).fit(X_sob, mul['martingal'])
    print('Exibição: árvore exploratória de profundidade 2 (não sobrevive à validação cruzada).')
mul['folha'] = mS.apply(X_sob)
folhas = sorted(mul['folha'].unique(), key=lambda f: -mul.loc[mul['folha'] == f, 'martingal'].mean())
mul_res['arvS'] = (mS_podada_folhas, r2_cv)
rot_exploratoria = ' (exploratória, profundidade 2: não sobrevive à validação cruzada)' if mS_podada_folhas == 1 else ''
fig, ax = plt.subplots(figsize=(13, 6.2))
if mS.get_n_leaves() > 1:
    mul_arvore(ax, mS, list(X_sob.columns), classes=None, fontsize=9, precisao=3)
    sm_ = mpl.cm.ScalarMappable(cmap=DIV, norm=mpl.colors.Normalize(-np.abs(mS.tree_.value[:, 0, 0]).max(),
                                                                     np.abs(mS.tree_.value[:, 0, 0]).max()))
    cb = fig.colorbar(sm_, ax=ax, fraction=0.025, pad=0.01)
    cb.set_label('Resíduo martingal médio do nó\n(> 0: sentença antes do esperado)')
ax.set_title('Árvore de regressão sobre os resíduos martingal' + rot_exploratoria)
figura(fig, 'mul_arvore_sobrev', 'Árvore de sobrevivência: nenhuma partição por grupo ou calendário melhora a previsão '
       'do tempo fora da amostra', secao='5.3.4',
       nota=f'n = {len(mul)} processos; mínimo de 40 por folha; resíduo martingal de um Cox nulo, Mᵢ = δᵢ − Ĥ₀(tᵢ). '
            f'R² de validação cruzada ≈ {fmt_br(r2_cv, 3)}.')

fig, eixos = plt.subplots(1, 2, figsize=(14, 5.2), gridspec_kw={'width_ratios': [1.5, 1]})
ax = eixos[0]
if len(folhas) > 1:
    cores_folha = {f'Folha {f}': SEQ(v) for f, v in zip(folhas, np.linspace(1.0, 0.45, len(folhas)))}
    mul_km = mul.assign(folha_rot=mul['folha'].map(lambda f: f'Folha {f}'))
    plot_km(ax, mul_km, tempo='T', evento='E', grupo='folha_rot', ordem=list(cores_folha), cores=cores_folha, passo=30,
            tmax=float(mul['T'].max()))
    lr = multivariate_logrank_test(mul['T'], mul['folha'], mul['E'])
    anotar_teste(ax, texto_teste('Log-rank entre folhas (otimista)', f'χ² = {fmt_br(lr.test_statistic, 1)}', lr.p_value),
                 loc='lower left')
    ax.set_title('Kaplan-Meier por folha (da mais rápida à mais lenta)')
    mul_res['arvS_lr'] = lr.p_value
ax = eixos[1]
ax.errorbar(range(len(arvS['alphas'])), -arvS['medias'], yerr=arvS['eps'], fmt='o-', ms=3, lw=1.2, color=COR_MODELO, capsize=2)
ax.axvline(arvS['i_1se'], color=COR_VIES, lw=1.2, label='α escolhido (regra de 1 erro-padrão)')
ax.set(xlabel='Índice de α (árvores cada vez mais simples →)', ylabel='Erro quadrático médio na validação cruzada',
       title='Validação cruzada da poda')
ax.legend(loc='upper right', fontsize=8.5)
figura(fig, 'mul_arvore_sobrev_km', 'As folhas da árvore exploratória separam as curvas (distribuídos no início do ano mais rápidos), '
       'mas a partição não se sustenta fora da amostra',
       secao='5.3.4', nota='o valor-p do log-rank é otimista: as partições foram escolhidas para maximizar a diferença.')
''')

interp('mul_arv_sobrev')

# =====================================================================
md(r'''
## 5.4 Análise de correspondência

A análise de correspondência (AC) decompõe a estatística χ² de uma tabela de contingência em dimensões ortogonais e representa linhas e colunas num mesmo plano: categorias próximas têm perfis parecidos, e uma categoria de linha próxima de uma de coluna indica associação positiva. A **inércia total** é χ²/n; cada dimensão explica uma fração dela. Implementação direta por decomposição em valores singulares (SVD) da matriz de resíduos padronizados S = D_r^(−1/2)(P − rcᵀ)D_c^(−1/2), sem bibliotecas externas: coordenadas principais das linhas F = D_r^(−1/2)UΣ e das colunas G = D_c^(−1/2)VΣ (mapa simétrico).

### 5.4.1 AC simples: grupo × tipo de desfecho

A tabela inclui os cinco desfechos (inclusive ativos e redistribuídos), porque a composição dos ativos também difere entre grupos. Com 3 linhas, há no máximo 2 dimensões, e o plano explica 100% da inércia. O teste χ² de independência (H0: o perfil de desfechos é o mesmo nos três grupos) é o teste associado; o mapa é o seu gráfico.
''')

code(r'''
def analise_correspondencia(tabela):
    N = np.asarray(tabela, float)
    n = N.sum(); P = N / n
    r, c = P.sum(1), P.sum(0)
    S = (P - np.outer(r, c)) / np.sqrt(np.outer(r, c))
    U, sv, Vt = np.linalg.svd(S, full_matrices=False)
    k = int(np.sum(sv > 1e-12))
    F = (U[:, :k] * sv[:k]) / np.sqrt(r)[:, None]
    G = (Vt.T[:, :k] * sv[:k]) / np.sqrt(c)[:, None]
    inercia = sv[:k] ** 2
    return {'F': F, 'G': G, 'inercia': inercia, 'total': inercia.sum(), 'n': n, 'massa_l': r, 'massa_c': c}

tab_ca = pd.crosstab(mul['grupo'], mul['tipo_desfecho']).reindex(columns=ORDEM_DESFECHO)
ca = analise_correspondencia(tab_ca)
chi2_ca, p_ca, gl_ca, _ = stats.chi2_contingency(tab_ca)
mul_res['ca'] = (ca['inercia'] / ca['total'], chi2_ca, p_ca)
tabela(tab_ca.rename(columns=ROTULO_DESFECHO).rename_axis('Grupo').rename_axis(columns=None), 'mul_ca_tabela',
       'Tabela grupo × tipo de desfecho analisada pela correspondência (processos)', secao='5.4.1',
       nota=f'n = {int(tab_ca.values.sum())} processos (inclui ativos e redistribuídos).')
print(f"Inércia total = {fmt_br(ca['total'], 4)} = χ²/n = {fmt_br(chi2_ca, 2)}/{int(ca['n'])}; χ² ({gl_ca} g.l.) p {p_br(p_ca)}")
for i, v in enumerate(ca['inercia']):
    print(f'  dimensão {i + 1}: inércia {fmt_br(v, 4)} ({pct_br(v / ca["total"])})')

pin = ca['inercia'] / ca['total']
fig, ax = plt.subplots(figsize=(10, 6.5))
for i, g in enumerate(tab_ca.index):
    ax.scatter(ca['F'][i, 0], ca['F'][i, 1], s=170, color=CORES_GRUPO[g], marker='s', zorder=3, edgecolor='white', lw=1.5)
for j, d in enumerate(tab_ca.columns):
    ax.scatter(ca['G'][j, 0], ca['G'][j, 1], s=110, color=CORES_DESFECHO[d], marker='o', zorder=3, edgecolor='white', lw=1.5)
ax.axhline(0, color='#bdbdbd', lw=0.8, zorder=1); ax.axvline(0, color='#bdbdbd', lw=0.8, zorder=1)
ax.grid(axis='both', visible=True)
todos_x = np.r_[ca['F'][:, 0], ca['G'][:, 0]]; todos_y = np.r_[ca['F'][:, 1], ca['G'][:, 1]]
mx, my = np.ptp(todos_x) * 0.15, np.ptp(todos_y) * 0.2
ax.set_xlim(todos_x.min() - mx, todos_x.max() + mx); ax.set_ylim(todos_y.min() - my, todos_y.max() + my)
ax.set(xlabel=f'Dimensão 1 ({pct_br(pin[0])} da inércia)', ylabel=f'Dimensão 2 ({pct_br(pin[1])} da inércia)',
       title='Mapa simétrico (coordenadas principais)')
mul_rotular_pontos(ax, todos_x, todos_y, list(tab_ca.index) + [ROTULO_DESFECHO[d] for d in tab_ca.columns],
                   negrito=[True] * len(tab_ca.index) + [False] * len(tab_ca.columns))
ax.scatter([], [], marker='s', s=80, color='#777777', label='Grupo (quadrado; cor do grupo)')
ax.scatter([], [], marker='o', s=60, color='#777777', label='Tipo de desfecho (círculo; cor do desfecho)')
legenda_abaixo(ax, ncol=2, dy=-0.11)
anotar_teste(ax, texto_teste('χ² de independência', f'χ² = {fmt_br(chi2_ca, 2)}; {gl_ca} g.l.', p_ca,
                             f'inércia total = {fmt_br(ca["total"], 4)}'), loc='lower left')
figura(fig, 'mul_ca_mapa', f'Correspondência grupo × desfecho: o 1º eixo ({pct_br(pin[0], 0)} da inércia) separa o Controle (mérito) '
       'dos ritos com audiência (sem mérito, homologação e ativos)', secao='5.4.1',
       nota='categorias próximas têm perfis parecidos; grupo perto de desfecho = associação positiva. Com 3 grupos, o plano '
            'explica 100% da inércia.')
''')

interp('mul_ac_simples')

md(r'''
### 5.4.2 AC múltipla: grupo × tipo de desfecho × bimestre de distribuição

A AC múltipla (ACM) aplica a mesma decomposição à **matriz indicadora** (uma coluna por categoria de cada variável, 938 linhas). O mês entra agrupado em bimestres (jan-fev, mar-abr, mai-jun, jul-ago) para evitar categorias raras. Na ACM, as inércias brutas subestimam a qualidade da representação; usa-se a **correção de Benzécri**: para Q variáveis, só os autovalores λ > 1/Q contam, e λ* = [Q/(Q − 1)]² (λ − 1/Q)². O objetivo é ver se o eixo "desfecho" e o eixo "calendário" se misturam com o eixo "grupo", ou seja, se o mês confunde a comparação.
''')

code(r'''
bimestre = pd.cut(mul['mes_num'], [0, 2, 4, 6, 8], labels=['jan-fev', 'mar-abr', 'mai-jun', 'jul-ago'])
vars_acm = pd.DataFrame({'grupo': mul['grupo'].astype(str), 'desfecho': mul['desfecho'], 'bimestre': bimestre.astype(str)})
Z = pd.get_dummies(vars_acm, prefix_sep=': ').astype(float)
acm = analise_correspondencia(Z.values)
Q = vars_acm.shape[1]
lam = acm['inercia']
lam_adj = np.where(lam > 1 / Q, (Q / (Q - 1)) ** 2 * (lam - 1 / Q) ** 2, 0)
pct_adj = lam_adj / lam_adj.sum()
mul_res['acm'] = pct_adj[:2]
tabela(pd.DataFrame({'Dimensão': np.arange(1, len(lam) + 1), 'Autovalor bruto': lam,
                     'Inércia bruta (%)': 100 * lam / lam.sum(), 'Inércia corrigida de Benzécri (%)': 100 * pct_adj}).head(6),
       'mul_acm_inercia', 'ACM grupo × desfecho × bimestre: inércia por dimensão, bruta e com a correção de Benzécri',
       secao='5.4.2', formatos={'Autovalor bruto': 4},
       nota=f'Q = {Q} variáveis; só os autovalores λ > 1/Q contam na correção λ* = [Q/(Q − 1)]²(λ − 1/Q)².')
fig, eixos = plt.subplots(1, 2, figsize=(15, 6.5), gridspec_kw={'width_ratios': [1, 2.4]})
ax = eixos[0]
barras_verticais(ax, [str(k) for k in range(1, 7)], pct_adj[:6], cores=COR_MODELO, rotular=True,
                 fmt=lambda v: pct_br(v, 1), xlabel='Dimensão', ylabel='Inércia corrigida (Benzécri, %)', ymax=1.05)
eixo_pct(ax)
ax.set_title('Inércia por dimensão')
ax = eixos[1]
marc = {'grupo': 's', 'desfecho': 'o', 'bimestre': '^'}
xs, ys, rots, negr = [], [], [], []
for j, col in enumerate(Z.columns):
    var, cat = col.split(': ', 1)
    cor = CORES_GRUPO.get(cat) if var == 'grupo' else (CORES_DESFECHO.get(cat) if var == 'desfecho' else '#3D3D3D')
    ax.scatter(acm['G'][j, 0], acm['G'][j, 1], marker=marc[var], s=150 if var == 'grupo' else 90, color=cor, zorder=3,
               edgecolor='white', lw=1.2)
    xs.append(acm['G'][j, 0]); ys.append(acm['G'][j, 1])
    rots.append(ROTULO_DESFECHO.get(cat, cat) if var == 'desfecho' else cat); negr.append(var == 'grupo')
ax.axhline(0, color='#bdbdbd', lw=0.8, zorder=1); ax.axvline(0, color='#bdbdbd', lw=0.8, zorder=1)
ax.grid(axis='both', visible=True)
mx, my = np.ptp(xs) * 0.12, np.ptp(ys) * 0.12
ax.set_xlim(min(xs) - mx, max(xs) + mx * 1.6); ax.set_ylim(min(ys) - my, max(ys) + my)
ax.set(xlabel=f'Dimensão 1 ({pct_br(pct_adj[0])}, Benzécri)', ylabel=f'Dimensão 2 ({pct_br(pct_adj[1])}, Benzécri)',
       title='Mapa das categorias')
mul_rotular_pontos(ax, xs, ys, rots, tamanho=8.5, negrito=negr)
for var, m, rot in [('grupo', 's', 'Grupo (cor do grupo)'), ('desfecho', 'o', 'Tipo de desfecho (cor do desfecho)'),
                    ('bimestre', '^', 'Bimestre de distribuição (cinza-escuro)')]:
    ax.scatter([], [], marker=m, color='#777777', s=60, label=rot)
legenda_abaixo(ax, ncol=3, dy=-0.11, fontsize=8.5)
figura(fig, 'mul_acm', 'ACM: o 1º eixo é de calendário e censura (jul-ago e ativos × início do ano); '
       'o 2º separa o Controle (mérito) dos ritos com audiência', secao='5.4.2',
       nota=f'matriz indicadora de {len(Z)} processos × {Z.shape[1]} categorias; coordenadas principais das categorias.')
''')

interp('mul_ac_multipla')

# =====================================================================
md(r'''
## 5.5 Comparação preditiva dos modelos de tempo com censura

A Parte IV interpretou os coeficientes dos modelos de Cox e AFT. Aqui a pergunta é outra: **quanto esses modelos preveem** o tempo de um processo novo? Comparam-se, com validação cruzada em 10 partes (mesma partição para todos):

| Modelo | Preditores |
|---|---|
| Nulo (Kaplan-Meier marginal) | nenhum; C = 0,5 por definição |
| Cox, só mês | mês |
| Cox, grupo | grupo |
| Cox, grupo + mês | grupo, mês |
| Weibull AFT, grupo + mês | grupo, mês |
| Log-normal AFT, grupo + mês | grupo, mês |

Métricas:

- **índice de concordância de Harrell (C)** fora da amostra (`lifelines.utils.k_fold_cross_validation`, `scoring_method='concordance_index'`): proporção de pares comparáveis em que o processo com menor tempo previsto foi de fato sentenciado antes; 0,5 = acaso, 1 = ordenação perfeita;
- **escore de Brier integrado (IBS)** com pesos pela probabilidade inversa de censura (IPCW, Graf et al., 1999), implementado diretamente: BS(t) = média de Ŝ(t|x)²·1(Tᵢ ≤ t, δᵢ = 1)/Ĝ(Tᵢ⁻) + [1 − Ŝ(t|x)]²·1(Tᵢ > t)/Ĝ(t), em que Ĝ é o Kaplan-Meier da censura estimado no treino **separadamente por mês de distribuição** (a censura administrativa depende do mês: um Ĝ marginal violaria a hipótese de censura independente das covariáveis e penalizaria indevidamente os modelos que usam o mês; agosto unido a julho); IBS = média de BS(t) num intervalo. **Janela identificável:** além do seguimento mínimo (65 dias), os processos dos últimos meses não podem ser observados, e o IPCW não recupera essa massa (Ĝ = 0 nesses estratos). Por isso, calcula-se o IBS em duas janelas em que todos os avaliados foram acompanhados durante todo o intervalo (só a redistribuição censura): **[1, 64] dias com os 938** e **[1, 120] dias com os 688 de seguimento ≥ 120**. Menor é melhor; o nulo é a régua;
- **calibração de Ŝ(90)**: previsões fora da amostra agrupadas em quintis, contra o Kaplan-Meier observado em cada quintil.

Usa-se `tempo_pos` (zeros → 0,5 dia) para que Cox e AFT vejam os mesmos dados; a redistribuição é tratada como censura, como na análise principal da Parte IV.
''')

code(r'''
df_s = mul[['T_pos', 'E', 'presencial', 'remota', 'mes_num']].reset_index(drop=True)
MODELOS = {
    'Cox, só mês': (CoxPHFitter, ['mes_num']),
    'Cox, grupo': (CoxPHFitter, ['presencial', 'remota']),
    'Cox, grupo + mês': (CoxPHFitter, ['presencial', 'remota', 'mes_num']),
    'Weibull AFT, grupo + mês': (WeibullAFTFitter, ['presencial', 'remota', 'mes_num']),
    'Log-normal AFT, grupo + mês': (LogNormalAFTFitter, ['presencial', 'remota', 'mes_num']),
}
# (i) concordância por k_fold_cross_validation do lifelines
conc_cv = {}
for nome, (Fit, cols) in MODELOS.items():
    conc_cv[nome] = k_fold_cross_validation(Fit(), df_s[['T_pos', 'E'] + cols], 'T_pos', 'E', k=10,
                                            scoring_method='concordance_index', seed=SEMENTE)
# na amostra toda
conc_in = {}
for nome, (Fit, cols) in MODELOS.items():
    f = Fit().fit(df_s[['T_pos', 'E'] + cols], 'T_pos', 'E')
    conc_in[nome] = f.concordance_index_
tab_conc = pd.DataFrame({'C na amostra': conc_in, 'C validação cruzada (média)': {k: np.mean(v) for k, v in conc_cv.items()},
                         'DP entre as 10 partes': {k: np.std(v, ddof=1) for k, v in conc_cv.items()}}).rename_axis('Modelo')
tabela(tab_conc, 'mul_concordancia', 'Índice de concordância de Harrell (C) dos modelos de tempo, na amostra e fora dela',
       secao='5.5', casas=3, nota='C = 0,5: ordenação ao acaso; 1: ordenação perfeita. Validação cruzada em 10 partes, mesma partição para todos.')
mul_res['conc_cv'] = {k: np.mean(v) for k, v in conc_cv.items()}

fig, ax = plt.subplots(figsize=(11, 4.8))
bp = ax.boxplot(list(conc_cv.values()), positions=range(len(conc_cv)), widths=0.45, patch_artist=True,
                medianprops=dict(color=TINTA, lw=2), whiskerprops=dict(color=TINTA_2), capprops=dict(color=TINTA_2),
                flierprops=dict(marker='o', ms=3, mfc='none', mec=TINTA_2))
for caixa in bp['boxes']:
    caixa.set_facecolor(mpl.colors.to_rgba(COR_MODELO, 0.18)); caixa.set_edgecolor(COR_MODELO)
for k, v in enumerate(conc_cv.values()):
    ax.scatter(np.full(len(v), k) + np.linspace(-0.12, 0.12, len(v)), v, s=12, color=COR_MODELO, alpha=0.6, zorder=3, lw=0)
    ax.annotate(f'média {fmt_br(np.mean(v), 3)}', (k, max(v)), xytext=(0, 5), textcoords='offset points', ha='center',
                va='bottom', fontsize=8.5, color=TINTA)
ax.set_xticks(range(len(conc_cv)), [quebra(k, 14) for k in conc_cv])
ax.axhline(0.5, color=COR_VIES, lw=1.2)
ax.annotate('acaso (C = 0,5)', (1, 0.5), xycoords=('axes fraction', 'data'), xytext=(-3, 3), textcoords='offset points',
            ha='right', va='bottom', fontsize=8.5, color=TINTA)
ax.grid(axis='x', visible=False)
ax.set(ylabel='Índice C fora da amostra (ponto = parte)', title='Concordância de Harrell na validação cruzada (10 partes)')
figura(fig, 'mul_concordancia', 'Nenhum modelo de tempo ordena bem os processos: C fora da amostra entre '
       f'{fmt_br(min(mul_res["conc_cv"].values()), 2)} e {fmt_br(max(mul_res["conc_cv"].values()), 2)}', secao='5.5',
       nota='redistribuição tratada como censura; tempos zero = 0,5 dia.')
''')

interp('mul_pred_cv')

code(r'''
GRADE_T = np.arange(1, 121)
JANELAS = {'IBS [1, 64], todos': (64, None), 'IBS [1, 120], seguimento ≥ 120': (120, 120)}

def brier_ipcw(T, E, S_pred, T_tr, E_tr, est_te, est_tr, grade):
    """Brier(t) com IPCW (Graf et al., 1999), com G estimado por estrato de mês. S_pred: (n_teste × len(grade))."""
    G_t = np.zeros((len(T), len(grade)))
    G_Ti = np.zeros(len(T))
    for e in np.unique(est_te):
        kmG = KaplanMeierFitter().fit(T_tr[est_tr == e], 1 - E_tr[est_tr == e])
        i = est_te == e
        G_t[i] = kmG.survival_function_at_times(grade).values
        G_Ti[i] = kmG.survival_function_at_times(np.maximum(T[i] - 1e-6, 0)).values
    G_t, G_Ti = np.clip(G_t, 0.05, 1), np.clip(G_Ti, 0.05, 1)
    bs = np.zeros(len(grade))
    for j, t in enumerate(grade):
        evento_antes = (T <= t) & (E == 1)
        vivo = T > t
        bs[j] = np.mean(np.where(evento_antes, S_pred[:, j] ** 2 / G_Ti, 0) + np.where(vivo, (1 - S_pred[:, j]) ** 2 / G_t[:, j], 0))
    return bs

fu_s = mul['followup_f'].reset_index(drop=True).values
kf = KFold(10, shuffle=True, random_state=SEMENTE)
NOMES_PRED = ['Nulo (KM)'] + list(MODELOS)
bs_curvas = {jan: {nome: [] for nome in NOMES_PRED} for jan in JANELAS}
s90_oof = {nome: np.full(len(df_s), np.nan) for nome in ['Cox, grupo + mês', 'Log-normal AFT, grupo + mês']}
for tr, te in kf.split(df_s):
    d_tr, d_te = df_s.iloc[tr], df_s.iloc[te]
    T_te, E_te = d_te['T_pos'].values, d_te['E'].values
    est_tr, est_te = np.minimum(d_tr['mes_num'].values, 7), np.minimum(d_te['mes_num'].values, 7)   # ago unido a jul
    km = KaplanMeierFitter().fit(d_tr['T_pos'], d_tr['E'])
    previsoes = {'Nulo (KM)': np.tile(km.survival_function_at_times(GRADE_T).values, (len(te), 1))}
    for nome, (Fit, cols) in MODELOS.items():
        f = Fit().fit(d_tr[['T_pos', 'E'] + cols], 'T_pos', 'E')
        previsoes[nome] = f.predict_survival_function(d_te[cols], times=GRADE_T).values.T
        if nome in s90_oof:
            s90_oof[nome][te] = f.predict_survival_function(d_te[cols], times=[90]).values.ravel()
    for jan, (tau, fu_min) in JANELAS.items():
        m = np.ones(len(te), bool) if fu_min is None else fu_s[te] >= fu_min
        for nome, Sp in previsoes.items():
            bs_curvas[jan][nome].append(brier_ipcw(T_te[m], E_te[m], Sp[m, :tau], d_tr['T_pos'].values, d_tr['E'].values,
                                                   est_te[m], est_tr, GRADE_T[:tau]))
integra = lambda c, tau: np.trapezoid(c, GRADE_T[:tau]) / (tau - 1)
ibs, ibs_dp, bs_medio = {}, {}, {}
for jan, (tau, _) in JANELAS.items():
    bs_medio[jan] = {k: np.mean(v, axis=0) for k, v in bs_curvas[jan].items()}
    ibs[jan] = {k: integra(v, tau) for k, v in bs_medio[jan].items()}
    ibs_dp[jan] = {k: np.std([integra(c, tau) for c in v], ddof=1) for k, v in bs_curvas[jan].items()}
mul_res['ibs'] = ibs
tab_ibs = pd.DataFrame(index=NOMES_PRED).rename_axis('Modelo')
for jan, rot in zip(JANELAS, ['[1, 64] (938)', '[1, 120] (688)']):
    tab_ibs[f'IBS {rot}'] = pd.Series(ibs[jan])
    tab_ibs[f'DP {rot}'] = pd.Series(ibs_dp[jan])
    tab_ibs[f'Ganho sobre o nulo {rot} (%)'] = pd.Series({k: 100 * (1 - v / ibs[jan]['Nulo (KM)']) for k, v in ibs[jan].items()})
tabela(tab_ibs, 'mul_brier', 'Escore de Brier integrado (IBS, IPCW) fora da amostra, em duas janelas identificáveis',
       secao='5.5', casas=4, nota='menor = melhor; ganho > 0 = melhor que o Kaplan-Meier marginal (nulo). Entre colchetes, '
                                  'a janela em dias; entre parênteses, os processos avaliados. DP entre as 10 partes.')

PAL_MOD = {'Nulo (KM)': TINTA, 'Cox, só mês': '#A9B8C6', 'Cox, grupo': '#6E8396', 'Cox, grupo + mês': COR_MODELO,
           'Weibull AFT, grupo + mês': '#C9A227', 'Log-normal AFT, grupo + mês': COR_VIES}
jan2 = 'IBS [1, 120], seguimento ≥ 120'
fig, ax = plt.subplots(figsize=(11, 5))
for k, v in bs_medio[jan2].items():
    ax.plot(GRADE_T, v, label=k, color=PAL_MOD[k], lw=2.4 if k == 'Nulo (KM)' else 1.6,
            ls=(0, (4, 2)) if k == 'Nulo (KM)' else '-', zorder=4 if k == 'Nulo (KM)' else 3)
ax.set(xlabel=ROTULOS['dias'], ylabel='Escore de Brier(t), IPCW, fora da amostra',
       title='Brier(t) nos processos com seguimento ≥ 120 dias (n = 688)', xlim=(0, 121))
ax.set_xticks(np.arange(0, 121, 15))
legenda_abaixo(ax, ncol=3, dy=-0.15)
figura(fig, 'mul_brier_t', 'O erro de previsão de S(t) dos modelos praticamente coincide com o do Kaplan-Meier marginal; '
       'os AFT ficam acima', secao='5.5', nota='Brier(t) = erro quadrático da previsão de S(t), com pesos IPCW (Graf et al., 1999) '
                                            'estimados por mês de distribuição. Linha tracejada: modelo nulo (régua).')

fig, eixos = plt.subplots(1, 2, figsize=(13, 5))
titulos_jan = {'IBS [1, 64], todos': 'Janela [1, 64] dias, todos (n = 938)',
               'IBS [1, 120], seguimento ≥ 120': 'Janela [1, 120] dias, seguimento ≥ 120 (n = 688)'}
for ax, jan in zip(eixos, JANELAS):
    v = ibs[jan]
    nomes_m = list(v)
    mul_forest(ax, [v[k] for k in nomes_m], [v[k] - ibs_dp[jan][k] for k in nomes_m],
               [v[k] + ibs_dp[jan][k] for k in nomes_m], cor=[PAL_MOD[k] for k in nomes_m],
               textos=[fmt_br(v[k], 4) for k in nomes_m])
    ax.axhline(v['Nulo (KM)'], color=TINTA_2, lw=1, zorder=1)
    ax.set_xticks(range(len(v)), [quebra(k, 12) for k in nomes_m], fontsize=8)
    ax.set_xlim(-0.5, len(v) - 0.1)
    ax.set(ylabel='IBS (± 1 DP entre partes; menor = melhor)', title=titulos_jan.get(jan, jan))
figura(fig, 'mul_brier_ibs', 'Só os Cox com mês ganham (cerca de 1%) do nulo; os AFT erram mais que o Kaplan-Meier marginal',
       secao='5.5', nota='pontos com ± 1 desvio-padrão entre as 10 partes; linha horizontal = IBS do modelo nulo. '
                         'O eixo vertical não começa em zero: compara pontos, não barras.')
''')

interp('mul_pred_brier')

md(r'''
### 5.5.1 Calibração de Ŝ(90)

Cada processo recebeu, fora da amostra, a probabilidade prevista de **continuar sem sentença aos 90 dias**. Agrupam-se as previsões em quintis (empates fazem alguns quintis coincidirem) e compara-se a média prevista com o Kaplan-Meier observado em cada quintil, com IC 95%. Calibração perfeita: pontos sobre a diagonal.
''')

code(r'''
fig, eixos = plt.subplots(1, 2, figsize=(12, 5))
calib = {}
for ax, (nome, s90) in zip(eixos, s90_oof.items()):
    q = pd.qcut(pd.Series(s90).rank(method='first'), 5, labels=False)
    lin = []
    for b in range(5):
        idx = np.where(q == b)[0]
        km = KaplanMeierFitter().fit(df_s['T_pos'].iloc[idx], df_s['E'].iloc[idx])
        obs = km.survival_function_at_times(90).iloc[0]
        ic = km.confidence_interval_survival_function_
        ic_at = ic[ic.index <= 90].iloc[-1]
        lin.append({'quintil': b + 1, 'previsto': s90[idx].mean(), 'observado': obs,
                    'li': ic_at.iloc[0], 'ls': ic_at.iloc[1], 'n': len(idx)})
    t = pd.DataFrame(lin)
    calib[nome] = t
    ax.errorbar(t['previsto'], t['observado'], yerr=[t['observado'] - t['li'], t['ls'] - t['observado']], fmt='o', ms=6,
                capsize=4, color=COR_MODELO, zorder=3)
    lo = min(t['li'].min(), t['previsto'].min()) - 0.03
    hi = max(t['ls'].max(), t['previsto'].max()) + 0.03
    ax.plot([lo, hi], [lo, hi], color=TINTA_2, lw=1, zorder=1)
    ax.set(xlim=(lo, hi), ylim=(lo, hi), xlabel='Ŝ(90) previsto (média do quintil)',
           ylabel='Ŝ(90) observado (Kaplan-Meier, IC 95%)', title=nome)
    ax.set_aspect('equal'); ax.grid(axis='both', visible=True)
    eixo_pct(ax, 'x'); eixo_pct(ax, 'y')
    anotar_teste(ax, f"Erro absoluto médio = {fmt_br(100 * np.mean(np.abs(t['previsto'] - t['observado'])), 1)} p.p.\n"
                     f"n por quintil ≈ {fmt_br(t['n'].mean(), 0)}", loc='upper left')
    print(f"{nome}: amplitude das previsões Ŝ(90) = {fmt_br(s90.min(), 3)} a {fmt_br(s90.max(), 3)}; "
          f"erro absoluto médio de calibração = {fmt_br(np.mean(np.abs(t['previsto'] - t['observado'])), 3)}")
mul_res['calib'] = calib
figura(fig, 'mul_calib_s90', 'Calibração de Ŝ(90), a proporção sem sentença aos 90 dias: o Cox acompanha a diagonal; '
       'o log-normal erra mais', secao='5.5.1',
       nota='previsões de validação cruzada (10 partes) agrupadas em quintis; diagonal = calibração perfeita.')
''')

interp('mul_pred_calib')

# =====================================================================
md(r'''
## 5.6 Síntese da Parte V

A tabela reúne os modelos ajustados, a métrica de desempenho de cada um e o que dizem sobre a pergunta de pesquisa. Os números são lidos diretamente dos resultados acima.
''')

code(r'''
cA = mul_res['contA'].set_index('Contraste')
rrr_t = mul_res['mnl'][0].set_index(['Equação', 'Termo'])
sint = pd.DataFrame([
    {'Seção': '5.1', 'Modelo': 'OLS tempo ~ grupo + mês (sentenciados)', 'Desempenho': f"R² = {fmt_br(mul_res['ols_r2'], 3)}",
     'Leitura': 'inadequado: ignora censura, resíduos não normais e heterocedásticos'},
    {'Seção': '5.2.1', 'Modelo': 'Logit acordo ~ grupo + mês (encerrados)',
     'Desempenho': f"AUC VC = {fmt_br(mul_res['aucA'][2], 3)}; McFadden = {fmt_br(mul_res['A']['mcfadden'], 3)}",
     'Leitura': f"Remota × Controle RC = {fmt_br(cA.loc['Remota vs Controle', 'RC'], 2)} (p Holm {p_br(cA.loc['Remota vs Controle', 'p Holm'])}); TRV grupo p {p_br(mul_res['A']['trv_p'])}"},
    {'Seção': '5.2.6', 'Modelo': 'Logit acordo na AC ~ modalidade + híbrida + mês',
     'Desempenho': f"AUC = {fmt_br(mul_res['AC'][1], 3)} (na amostra)",
     'Leitura': f"TRV p {p_br(mul_res['AC'][0]['res'].llr_pvalue)}; 17 eventos, exploratório"},
    {'Seção': '5.2.7', 'Modelo': 'MNLogit tipo de sentença ~ grupo + mês',
     'Desempenho': f"McFadden = {fmt_br(mul_res['mnl'][3], 3)}",
     'Leitura': f"TRV grupo p {p_br(mul_res['mnl'][2])}; sem mérito vs mérito: RRR Presencial {fmt_br(rrr_t.loc[('Sem mérito vs Mérito', 'Presencial vs Controle'), 'RRR'], 2)}, Remota {fmt_br(rrr_t.loc[('Sem mérito vs Mérito', 'Remota vs Controle'), 'RRR'], 2)}"},
    {'Seção': '5.3.1', 'Modelo': 'Árvore tipo de sentença (basais)',
     'Desempenho': f"acurácia balanceada VC = {pct_br(mul_res['arvA'][2])} (trivial 33,3%)", 'Leitura': f"{mul_res['arvA'][0]} folhas"},
    {'Seção': '5.3.2', 'Modelo': 'Árvore tipo de sentença (tratados, com AC realizada)',
     'Desempenho': f"acurácia balanceada VC = {pct_br(mul_res['arvB'][2])}", 'Leitura': f"{mul_res['arvB'][0]} folhas; AC realizada é a variável dominante (associação, não causa)"},
    {'Seção': '5.3.4', 'Modelo': 'Árvore de sobrevivência (martingal)',
     'Desempenho': f"R² VC ≈ {fmt_br(mul_res['arvS'][1], 3)}", 'Leitura': f"{mul_res['arvS'][0]} folhas"},
    {'Seção': '5.4', 'Modelo': 'AC grupo × desfecho', 'Desempenho': f"dim. 1 = {pct_br(mul_res['ca'][0][0])} da inércia",
     'Leitura': f"χ² p {p_br(mul_res['ca'][2])}"},
    {'Seção': '5.5', 'Modelo': 'Cox grupo + mês', 'Desempenho': f"C VC = {fmt_br(mul_res['conc_cv']['Cox, grupo + mês'], 3)}; IBS[1,120] = {fmt_br(mul_res['ibs']['IBS [1, 120], seguimento ≥ 120']['Cox, grupo + mês'], 4)} (nulo {fmt_br(mul_res['ibs']['IBS [1, 120], seguimento ≥ 120']['Nulo (KM)'], 4)})",
     'Leitura': 'melhor descrição do efeito de grupo com censura; previsão individual fraca'},
    {'Seção': '5.5', 'Modelo': 'Log-normal AFT grupo + mês', 'Desempenho': f"C VC = {fmt_br(mul_res['conc_cv']['Log-normal AFT, grupo + mês'], 3)}; IBS[1,120] = {fmt_br(mul_res['ibs']['IBS [1, 120], seguimento ≥ 120']['Log-normal AFT, grupo + mês'], 4)}",
     'Leitura': 'mesma ordenação que o Cox, mas forma de S(t) errada: Brier pior que o nulo e Ŝ(90) mal calibrado'},
])
tabela(sint, 'mul_sintese', 'Síntese dos modelos da Parte V: desempenho e o que dizem sobre a pergunta de pesquisa',
       secao='5.6', nota='AUC = área sob a curva ROC; VC = validação cruzada; C = índice de concordância de Harrell; '
                         'IBS = escore de Brier integrado (menor = melhor).')
''')

interp('mul_sintese')
