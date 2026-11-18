# Parte III — Testes de hipóteses (seções 3.1 a 3.7).
# Executado por build_rafaelcc_ed2.py (exec): usa md(), code() e interp().
# Variáveis e funções desta parte usam o prefixo tst_/t3_ para não colidir com as demais partes.

md(r'''
# PARTE III — TESTES DE HIPÓTESES

A Parte III aplica os **testes de significância contra a hipótese nula (TSHN)** clássicos às perguntas que eles conseguem responder neste desenho, e critica os que o notebook do professor aplicou. Três regras atravessam a parte:

1. **Só se testa o que faz sentido substantivamente.** Cada teste nasce de uma pergunta jurídica ou de desenho (o rito muda o *tipo* de desfecho? a AC remota produz mais acordos que a presencial? o sorteio foi aleatório?). Testes que só "confirmam" uma propriedade da construção dos dados são descartados e explicados (seção 3.1).
2. **O tempo até a sentença é censurado.** Comparações de duração com testes clássicos (Kruskal-Wallis, Mann-Whitney, ANOVA) são feitas **apenas entre processos encerrados**, como estatística *condicional* e enviesada para tempos curtos; a comparação correta dos tempos é a da Parte IV (Kaplan-Meier, log-rank, Cox). Sempre que possível, usa-se uma **janela comum de 65 dias**: como todo processo tem pelo menos 65 dias de acompanhamento (distribuídos até 03/08/2026, corte em 07/10/2026), o que acontece **até o 65º dia** é observado sem censura para os 938 processos.
3. **Todo teste tem hipóteses explícitas, pressupostos verificados, tamanho de efeito com intervalo de confiança, correção de multiplicidade (Holm) dentro de cada família e o seu próprio gráfico.** A seção 3.7 reúne todos os valores-p da parte.
''')

# =====================================================================
md(r'''
## 3.1 Plano de testes

### 3.1.1 Ferramentas comuns

A célula abaixo define as funções reutilizadas na parte:

- **`tst_registra`** guarda cada teste (seção, família, H₀, estatística, p, efeito) num registro único, usado na seção 3.7;
- **resíduos padronizados ajustados** de Haberman, r = (O − E)/√[E(1 − linha/n)(1 − coluna/n)], que seguem aproximadamente N(0, 1) sob H₀: |r| > 2 aponta a célula que se afasta da independência (AGRESTI, 2007);
- **V de Cramér** com IC 95% por *bootstrap* percentil (2.000 reamostragens dos processos);
- **intervalo de Wilson** para proporções e **intervalo de Newcombe** (método híbrido de escores) para a diferença de duas proporções, ambos adequados a proporções pequenas como as de acordo (NEWCOMBE, 1998);
- **teste de permutação de Monte Carlo** para tabelas r × c esparsas: mantém as margens fixas e embaralha os rótulos, com duas estatísticas — o qui-quadrado e a probabilidade hipergeométrica da tabela (esta última é a versão Monte Carlo do teste exato de Fisher-Freeman-Halton);
- **delta de Cliff** (igual à correlação bisserial de postos de Mann-Whitney), com IC por *bootstrap*.
''')

code(r'''
from statsmodels.stats.multitest import multipletests
from statsmodels.stats.proportion import proportion_confint, confint_proportions_2indep
from statsmodels.stats.contingency_tables import StratifiedTable
from statsmodels.stats.oneway import anova_oneway
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize
from scipy.stats.contingency import odds_ratio
from scipy.special import gammaln

if 'dados' not in globals():
    dados = pd.read_pickle(PROC / 'ed2_tidy.pkl')

t3 = dados.copy()
t3['tempo_f'] = t3['tempo'].astype(float)
t3['grupo'] = t3['grupo'].cat.set_categories(ORDEM_GRUPO)
PARES_GRUPO = [('Presencial', 'Controle'), ('Remota', 'Controle'), ('Presencial', 'Remota')]
TST_REGISTRO = []


# Natureza de cada família no registro da seção 3.7:
#   'principal'   = sem censura (938 ou janela fixa com seguimento completo), desenho ou aleatorização;
#   'condicional' = só entre os sentenciados (depende da data de corte) ou estratificado por variável pós-sorteio;
#   'didático'    = contraste/artefato exibido para crítica; não entra na correção global.
TST_NATUREZA = {'H1 pares': 'condicional', 'H2 tipos binários': 'condicional', 'H2 pares (Fisher)': 'condicional',
                'H8 tempo (condicional)': 'condicional', 'H8 pares MW': 'condicional', 'H8 por tipo': 'condicional',
                'H8 acordo': 'condicional', 'H8 didático': 'didático'}


def tst_registra(secao, familia, teste, h0, estatistica, p, efeito='', natureza=None):
    """Guarda um teste no registro da Parte III (seção 3.7), com a sua natureza (principal/condicional/didático)."""
    TST_REGISTRO.append({'Seção': secao, 'Família': familia, 'Teste': teste, 'H0': h0,
                         'Estatística': estatistica, 'p': float(p), 'Efeito (IC 95%)': efeito,
                         'Natureza': natureza or TST_NATUREZA.get(familia, 'principal')})


def tst_holm(pvalores):
    return multipletests(np.asarray(pvalores, dtype=float), method='holm')[1]


def tst_residuos(tab):
    """Resíduos padronizados ajustados de Haberman."""
    O = np.asarray(tab, dtype=float)
    n = O.sum()
    lin, col = O.sum(axis=1, keepdims=True), O.sum(axis=0, keepdims=True)
    E = lin @ col / n
    return pd.DataFrame((O - E) / np.sqrt(E * (1 - lin / n) * (1 - col / n)), index=tab.index, columns=tab.columns)


def tst_cramer(tab):
    O = np.asarray(tab, dtype=float)
    O = O[O.sum(axis=1) > 0][:, O.sum(axis=0) > 0]
    chi2 = stats.chi2_contingency(O, correction=False)[0]
    return np.sqrt(chi2 / (O.sum() * (min(O.shape) - 1)))


def tst_cramer_ic(x, y, B=2000, semente=SEMENTE):
    """V de Cramér e IC 95% bootstrap percentil (reamostra os processos)."""
    x = pd.Categorical(x); y = pd.Categorical(y)
    cx, cy = x.codes, y.codes
    kx, ky = len(x.categories), len(y.categories)
    obs = tst_cramer(np.bincount(cx * ky + cy, minlength=kx * ky).reshape(kx, ky))
    rng = np.random.default_rng(semente)
    n = len(cx)
    boot = np.empty(B)
    for b in range(B):
        i = rng.integers(0, n, n)
        boot[b] = tst_cramer(np.bincount(cx[i] * ky + cy[i], minlength=kx * ky).reshape(kx, ky))
    return obs, np.percentile(boot, 2.5), np.percentile(boot, 97.5)


def tst_wilson(x, n):
    return proportion_confint(x, n, method='wilson')


def tst_newcombe(x1, n1, x2, n2):
    """Diferença p1 − p2 com IC 95% de Newcombe (híbrido de escores)."""
    lo, hi = confint_proportions_2indep(x1, n1, x2, n2, method='newcomb', compare='diff')
    return x1 / n1 - x2 / n2, lo, hi


def tst_fisher(tab2):
    """Fisher exato bilateral + razão de chances (amostral) e IC 95% condicional exato."""
    tab2 = np.asarray(tab2, dtype=int)
    p = stats.fisher_exact(tab2)[1]
    orc = odds_ratio(tab2, kind='conditional')
    ic = orc.confidence_interval(0.95)
    a, b, c, d = tab2.ravel()
    or_amostral = (a * d) / (b * c) if b * c > 0 else np.inf
    return p, or_amostral, orc.statistic, ic.low, ic.high


def tst_perm_rxc(x, y, B=10000, semente=SEMENTE):
    """Permutação de Monte Carlo com margens fixas: p do qui-quadrado e p de Fisher-Freeman-Halton."""
    x = pd.Categorical(x); y = pd.Categorical(y)
    cx, cy = x.codes.copy(), y.codes.copy()
    kx, ky = len(x.categories), len(y.categories)
    tab = lambda a, b: np.bincount(a * ky + b, minlength=kx * ky).reshape(kx, ky)
    O = tab(cx, cy)
    E = O.sum(axis=1, keepdims=True) @ O.sum(axis=0, keepdims=True) / O.sum()
    chi_obs = ((O - E) ** 2 / E).sum()
    lp_obs = -gammaln(O + 1).sum()                       # log P(tabela) + constante (margens fixas)
    rng = np.random.default_rng(semente)
    chi_b, lp_b = np.empty(B), np.empty(B)
    for b in range(B):
        Ob = tab(cx, rng.permutation(cy))
        chi_b[b] = ((Ob - E) ** 2 / E).sum()
        lp_b[b] = -gammaln(Ob + 1).sum()
    p_chi = (1 + (chi_b >= chi_obs - 1e-9).sum()) / (B + 1)
    p_ffh = (1 + (lp_b <= lp_obs + 1e-9).sum()) / (B + 1)
    return chi_obs, p_chi, p_ffh, chi_b


def tst_cliff(x, y, B=2000, semente=SEMENTE):
    """Delta de Cliff d = P(X > Y) − P(X < Y) = 2U/(n1 n2) − 1, com IC bootstrap."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    f = lambda a, b: 2 * stats.mannwhitneyu(a, b).statistic / (len(a) * len(b)) - 1
    rng = np.random.default_rng(semente)
    boot = [f(rng.choice(x, len(x)), rng.choice(y, len(y))) for _ in range(B)]
    return f(x, y), np.percentile(boot, 2.5), np.percentile(boot, 97.5)


def tst_eq(p):
    """'< 0,001' ou '= 0,034' (para escrever 'p < 0,001' / 'p = 0,034')."""
    return p_br(p) if p < 0.001 else '= ' + p_br(p)


def tst_ic_txt(v, lo, hi, casas=2):
    return f'{fmt_br(v, casas)} [{fmt_br(lo, casas)}; {fmt_br(hi, casas)}]'


def tst_tabela_p(df, id, titulo, secao, colunas_p=('p', 'p Holm'), casas=3, destaque='auto', nota=None, formatos=None):
    """Tabela da Parte III via tabela(): valores-p em pt-BR ('< 0,001'), linhas significativas destacadas."""
    fmts = {c: 'p' for c in colunas_p if c in df}
    fmts.update(formatos or {})
    if destaque == 'auto':
        destaque = next((c for c in ('p Holm global', 'p Holm', 'p') if c in df), None)
    tabela(df, id, titulo, secao=secao, casas=casas, formatos=fmts, destaque=destaque, nota=nota)


def tst_tab(df, nome_indice=None, rotulos_col=None):
    """Prepara uma tabela cruzada para exibição: sem nome nas colunas, índice nomeado, rótulos legíveis."""
    saida = df.copy()
    if rotulos_col:
        saida = saida.rename(columns=rotulos_col)
    saida.columns = [str(c) for c in saida.columns]
    if nome_indice is not None:
        saida = saida.rename_axis(nome_indice)
    return saida


def tst_heatmap_res(ax, res, titulo='Resíduos padronizados ajustados', limite=None, quebrar=12, rotulos_col=None):
    """Mapa de calor dos resíduos ajustados: paleta divergente centrada em 0, limites simétricos, valores pt-BR."""
    res = res.copy()
    if rotulos_col:
        res = res.rename(columns=rotulos_col)
    lim = limite or max(4.0, float(np.ceil(np.nanmax(np.abs(res.to_numpy(dtype=float))))))
    anot = res.apply(lambda col: col.map(lambda v: fmt_br(v, 1)))
    sns.heatmap(res.astype(float), annot=anot.to_numpy(), fmt='', cmap=DIV, center=0, vmin=-lim, vmax=lim, ax=ax,
                linewidths=1, linecolor='white', annot_kws={'fontsize': 9},
                cbar_kws={'label': 'Resíduo ajustado (|r| > 2: célula notável)'})
    ax.set_xticks(np.arange(res.shape[1]) + 0.5, [quebra(str(c), quebrar) for c in res.columns], rotation=0)
    ax.set_yticks(np.arange(res.shape[0]) + 0.5, [quebra(str(i), quebrar) for i in res.index], rotation=0)
    ax.tick_params(length=0)
    ax.grid(False)
    ax.set_title(titulo); ax.set_xlabel(''); ax.set_ylabel('')
    cb = ax.collections[0].colorbar
    cb.ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: fmt_br(v, 0)))


def tst_barras_wilson(ax, categorias, xs, ns, cores=None, ylabel='', quebrar=14, ymax=None, rotulo_n=True):
    """Barras verticais de proporção (%) com IC 95% de Wilson e rótulo 'p% (x/n)' acima do IC."""
    xs, ns = np.asarray(xs, dtype=float), np.asarray(ns, dtype=float)
    prop = xs / ns
    lo, hi = tst_wilson(xs, ns)
    barras_verticais(ax, categorias, 100 * prop, cores=cores, erro=(100 * np.asarray(lo), 100 * np.asarray(hi)),
                     rotular=False, quebrar=quebrar, ylabel=ylabel)
    for i, (p_, h, x_, n_) in enumerate(zip(prop, hi, xs, ns)):
        texto = f'{fmt_br(100 * p_, 1)}%' + (f'\n({fmt_br(x_, 0)}/{fmt_br(n_, 0)})' if rotulo_n else '')
        ax.annotate(texto, (i, 100 * h), xytext=(0, 3), textcoords='offset points', ha='center', va='bottom',
                    fontsize=8.5, color=TINTA)
    topo = 100 * np.nanmax(hi)
    ax.set_ylim(0, ymax if ymax is not None else topo * 1.35 + 1)
    eixo_pct(ax, escala=1)


def tst_agrupadas_pct(ax, perc, base, ylabel, rotulos_idx=None, ymax=None, quebrar=14):
    """Barras agrupadas de % (linhas de `perc` = categorias no eixo x; colunas = grupos, com n na legenda)."""
    nomes = {g: rotulo_grupo(g, com_n=True, base=base) for g in perc.columns}
    tab = perc.rename(columns=nomes)
    if rotulos_idx:
        tab = tab.rename(index=rotulos_idx)
    barras_agrupadas(ax, tab, cores={nomes[g]: CORES_GRUPO[g] for g in perc.columns}, rotular=True,
                     fmt=lambda v: fmt_br(v, 0) + '%', ylabel=ylabel, quebrar=quebrar)
    if ymax is not None:
        ax.set_ylim(0, ymax)
    eixo_pct(ax, escala=1)


COR_NEUTRA = '#5B7389'   # séries que não são grupos nem desfechos (comparações, técnicas, versões de teste)


print('Funções da Parte III carregadas; base com', len(t3), 'processos.')
''')

md(r'''
### 3.1.2 Hipóteses que fazem sentido — e as que não fazem

O desenho é um ensaio aleatorizado com três braços independentes (questões 2.2 e 2.3): os testes são, portanto, **para amostras independentes** (qui-quadrado, Fisher, Kruskal-Wallis, Mann-Whitney), nunca pareados (McNemar, Wilcoxon, Friedman).

**Origem das hipóteses.** Não houve pré-registro. H1, H4, H5 e H9 derivam da pergunta de pesquisa e do desenho. **H2, porém, foi gerada pelos próprios dados**: nasceu do achado descritivo da Parte I (mais mérito no Controle, mais extinções sem mérito nos braços com AC) e é testada na mesma amostra. Os seus valores-p são, portanto, otimistas: o resultado é forte e tem explicação jurídica (art. 51, I, da Lei 9.099/1995), mas só se torna confirmatório numa replicação com a hipótese declarada antes da coleta.

| # | Pergunta substantiva | H₀ | Teste | Seção |
|---|---|---|---|---|
| H1 | O rito altera o **tipo de desfecho** (homologação, mérito, sem mérito)? | tipo de desfecho independente do grupo | χ² de independência, resíduos ajustados, V de Cramér; pares 2 × 3 com Holm | 3.2 |
| H2 | A AC obrigatória **aumenta as extinções sem mérito** (ausência do autor, art. 51, I, Lei 9.099/1995) e **reduz o mérito**? | mesma proporção de sem mérito (e de mérito) nos três grupos | χ² 3 × 2 + Fisher par a par com OR e IC, Holm; repetido em horizontes fixos (65 a 150 dias) | 3.2 |
| H3 | O rito altera a **redistribuição** (Decisão)? | proporção de redistribuições igual | permutação / Fisher-Freeman-Halton | 3.2 |
| H4 | A **modalidade** (presencial × remota) altera o **acordo na AC**? | p(acordo na AC) igual, entre AC realizadas | Fisher exato, OR, diferença com IC de Newcombe | 3.3 |
| H5 | O rito altera o **acordo em qualquer momento** (na AC ou fora)? | p(acordo) igual nos três grupos | χ² + Fisher par a par com Holm, em janela comum | 3.3 |
| H6 | O rito altera o **acordo fora da AC**? | p(acordo fora até 120 dias) igual | χ² + Fisher par a par, em janela comum | 3.3 |
| H7 | A AC **híbrida** e a **técnica** de conciliação alteram o acordo na AC? | acordo independente da híbrida / técnica | Fisher; permutação (Fisher-Freeman-Halton Monte Carlo) | 3.3 |
| H8 | Entre os **sentenciados**, o tempo difere entre os grupos? (condicional) | mesma distribuição do tempo | Kruskal-Wallis + Dunn (Holm); Mann-Whitney + Cliff; mediana de Mood; ANOVA/Welch só didático | 3.4 |
| H9 | O **sorteio** seguiu um padrão aleatório na ordem de chegada? | sequência de grupos aleatória | Wald-Wolfowitz (corridas), permutação | 3.5 |
| H10 | A **ordem de chegada** se associa ao tempo? (questão 2.7) | ρ = 0 | Spearman e Kendall, com e sem censura; por grupo | 3.5 |
| H11 | A composição dos grupos é a mesma em todos os **meses**? | grupo independente do mês | χ² de independência | 3.5 |
| H12 | O efeito do grupo sobre o acordo (até 120 dias) resiste ao **ajuste pelo mês**? | OR comum = 1 | Cochran-Mantel-Haenszel + Breslow-Day | 3.6 |

**Testes que não serão feitos, e por quê:**

- **Mann-Whitney Encerrado × Ativo** (notebook do professor, E18): é tautológico. Um processo ativo tem, por construção, pelo menos o seu tempo de acompanhamento (≥ 65 dias); o teste mede o calendário de distribuição, não um efeito.
- **Teste z de uma proporção com p₀ = 0,5** de encerrados (E23): nenhum fundamento jurídico ou de gestão sustenta 50%, e a proporção de encerrados depende só da data de corte.
- **Testes com zeros estruturais**, como Controle × acordo na AC ou Controle × técnica (E20): o Controle não tem AC; "0 acordos na AC" não é um resultado, é a definição do grupo. As comparações de acordo na AC são feitas **só entre Presencial e Remota**, entre AC realizadas.
- **Correlação entre as quatro colunas de duração** (E16): são a mesma variável (r = 1).
- **Testes de grupo × status (encerrado/ativo) sem horizonte fixo** (E19): o status depende do mês de entrada. São substituídos pela comparação em janela comum de 65 dias.
- **Testes pareados** (Wilcoxon, McNemar, Friedman): não há pareamento; cada processo pertence a um só grupo.
- **Testes de tendência entre grupos** (Jonckheere-Terpstra, Cochran-Armitage sobre o grupo): o grupo é nominal; não há ordem *a priori* Controle < Presencial < Remota. Fariam sentido para o **mês** (seção 3.6).
''')

md(r'''
### 3.1.3 Estratégia de multiplicidade e de tamanho de efeito

- **Famílias.** Cada pergunta (H1 … H12) é uma família; dentro dela, os valores-p das comparações par a par são ajustados por **Holm** (1979), que controla a taxa de erro por família (FWER) sem a perda de poder do Bonferroni simples. O teste global de cada família funciona como "porteiro": os pares só são lidos se o global rejeita, mas são exibidos sempre. A regra vale também na seção 3.7: um par cujo teste global não sobrevive à correção global é lido como **exploratório**, mesmo que o próprio par sobreviva.
- **Visão de conjunto.** A seção 3.7 reúne os valores-p da parte e aplica Holm global (FWER) e **Benjamini-Hochberg** (1995, controle da taxa de falsas descobertas, FDR), para mostrar quais conclusões sobrevivem a qualquer critério. Cada teste é classificado como **principal** (sem censura: os 938 processos ou uma janela fixa com seguimento completo), **condicional** (só entre os sentenciados, ou estratificado por variável pós-sorteio) ou **didático** (contraste ou artefato exibido para crítica). Os didáticos não entram na correção, e os condicionais não sustentam sozinhos uma conclusão.
- **Tamanho de efeito.** Valor-p não mede importância. Cada teste vem com uma medida de efeito e o seu IC 95%: V de Cramér (tabelas), razão de chances (OR) e diferença de proporções (2 × 2), ε² (Kruskal-Wallis), delta de Cliff (Mann-Whitney), ρ de Spearman e τ de Kendall (correlações).

### 3.1.4 Paramétrico ou não paramétrico?

A Parte II mostra que o tempo até a sentença **não é normal** em nenhum grupo (assimetria, massa em zero, tempos discretos em dias, cauda direita cortada pela censura). Com essa forma, a média é instável e os testes F/t perdem a garantia de nível em amostras desequilibradas e heterocedásticas. A escolha segue Siegel e Castellan (2006), para quem os testes baseados em postos são os indicados quando a escala é no máximo ordinal ou a forma da população é desconhecida/não normal; Barbetta, Reis e Bornia (2020) e Becker (2015) apresentam o mesmo critério de escolha entre o teste paramétrico e o seu equivalente não paramétrico (questão 2.11).

| Pergunta | Paramétrico (pressupõe normalidade/variâncias) | Não paramétrico (escolhido) | Por quê |
|---|---|---|---|
| Tempo, 3 grupos (encerrados) | ANOVA de um fator / Welch | **Kruskal-Wallis** + Dunn (Holm) | não normalidade; ANOVA/Welch só como contraste didático |
| Tempo, 2 grupos | t de Student / Welch | **Mann-Whitney** + delta de Cliff | idem |
| Mediana comum | — | **teste da mediana de Mood** | robusto a diferenças de forma, menos poder |
| Proporções, tabelas r × c | teste z de proporções | **χ²** (esperadas ≥ 5) ou **Fisher / permutação** (esparsas) | contagens pequenas (17 acordos na AC) |
| Associação ordinal | Pearson | **Spearman, Kendall** | ordem de chegada é ordinal (E13, E16) |
| Aleatoriedade de sequência | — | **corridas de Wald-Wolfowitz** | sequência nominal |
| Tempo com censura | regressão / AFT paramétrico | **log-rank, Cox** (Parte IV) | únicos que usam os ativos corretamente |
''')

interp('tst_plano')

# =====================================================================
md(r'''
---

## 3.2 Tipo de desfecho × grupo (H1, H2, H3)

### 3.2.1 Tabela de contingência entre os sentenciados

A base são os **708 processos com sentença** (homologação, mérito ou sem mérito). Ficam de fora os 206 ativos (ainda sem desfecho) e as 24 redistribuições, que não são sentença (E10, E21) e são testadas à parte (3.2.4).

- **H₀:** o tipo de sentença é independente do grupo. **H₁:** a distribuição dos tipos difere entre os grupos.
- **Pressuposto do χ²:** todas as frequências esperadas ≥ 5 (regra de Cochran). A tabela das esperadas é exibida.
- **Leitura do gráfico:** à esquerda, a composição percentual de cada grupo; à direita, os resíduos ajustados (vermelho = mais casos do que o esperado sob independência; azul = menos; |r| > 2 é notável).
- **Cautela:** é uma comparação **entre os já sentenciados**. Se um rito encerra mais cedo um tipo de desfecho, a composição entre os sentenciados muda com a data de corte; por isso a seção 3.2.5 repete a análise numa janela de 65 dias observada para todos.
''')

code(r'''
t3_sent = t3[t3['evento'] == 1].copy()
t3_sent['tipo'] = t3_sent['tipo_desfecho'].cat.remove_unused_categories()
t3_tab_tipo = pd.crosstab(t3_sent['grupo'], t3_sent['tipo'])
chi2, p_tipo, gl, esperadas = stats.chi2_contingency(t3_tab_tipo, correction=False)
v_tipo, v_lo, v_hi = tst_cramer_ic(t3_sent['grupo'], t3_sent['tipo'])
res_tipo = tst_residuos(t3_tab_tipo)
perc = 100 * t3_tab_tipo.div(t3_tab_tipo.sum(axis=1), axis=0)

tabela(tst_tab(t3_tab_tipo.assign(Total=t3_tab_tipo.sum(axis=1)), 'Grupo', ROTULO_DESFECHO), 'tst_tipo_obs',
       'Tipo de sentença por grupo: frequências observadas (processos sentenciados)', secao='3.2.1')
tabela(tst_tab(perc, 'Grupo', ROTULO_DESFECHO), 'tst_tipo_pct',
       'Tipo de sentença por grupo: percentual dos sentenciados de cada grupo (%)', secao='3.2.1', casas=1,
       nota='cada linha soma 100%.')
tabela(tst_tab(pd.DataFrame(esperadas, index=t3_tab_tipo.index, columns=t3_tab_tipo.columns), 'Grupo', ROTULO_DESFECHO),
       'tst_tipo_esp', 'Frequências esperadas sob independência (pressuposto do χ²: todas ≥ 5)', secao='3.2.1', casas=1,
       nota=f'menor esperada = {fmt_br(esperadas.min(), 1)}.')
print(f'Qui-quadrado = {fmt_br(chi2, 2)}, gl = {gl}, p {tst_eq(p_tipo)} | V de Cramér = {tst_ic_txt(v_tipo, v_lo, v_hi, 3)}')
tabela(tst_tab(res_tipo, 'Grupo', ROTULO_DESFECHO), 'tst_tipo_res',
       'Resíduos padronizados ajustados (tipo de sentença × grupo)', secao='3.2.1',
       gradiente={'mapa': DIV, 'vmin': -6, 'vmax': 6, 'colunas': [ROTULO_DESFECHO[str(c)] for c in res_tipo.columns]}, nota='|r| > 2 indica célula que se afasta da independência.')
tst_registra('3.2', 'H1 tipo × grupo', 'χ² tipo de sentença × grupo (sentenciados)', 'independência',
             f'χ²({gl}) = {fmt_br(chi2, 2)}', p_tipo, f'V = {tst_ic_txt(v_tipo, v_lo, v_hi, 3)}', natureza='condicional')

fig, ax = plt.subplots(1, 2, figsize=(13, 4.8), gridspec_kw={'width_ratios': [1.35, 1]})
tst_agrupadas_pct(ax[0], perc.T, t3_sent, 'Sentenciados do grupo (%)', rotulos_idx=ROTULO_DESFECHO,
                  ymax=perc.to_numpy().max() * 1.45)
ax[0].set_title('Composição dos tipos de sentença em cada grupo')
ax[0].legend(loc='upper right')
anotar_teste(ax[0], texto_teste('χ² de independência', f'χ²({gl}) = {fmt_br(chi2, 2)}', p_tipo,
                                f'V de Cramér = {tst_ic_txt(v_tipo, v_lo, v_hi, 2)}'), loc='upper left')
tst_heatmap_res(ax[1], res_tipo, limite=6, rotulos_col=ROTULO_DESFECHO)
figura(fig, 'tst_tipo_grupo',
       'O tipo de sentença depende do rito: mais mérito no Controle, mais extinções sem mérito nos braços com AC',
       secao='3.2.1', nota='base: 708 processos sentenciados até 07/10/2026 (análise condicional). À direita, vermelho = '
                           'mais casos do que o esperado sob independência; azul = menos.')
''')

md(r'''
### 3.2.2 Comparações par a par (2 × 3) com Holm

O χ² global diz que *alguma* diferença existe; as tabelas 2 × 3 dizem **entre quais grupos**. São três comparações, ajustadas por Holm. A comparação Presencial × Remota responde se a modalidade da AC importa para o tipo de desfecho.
''')

code(r'''
linhas = []
for a, b in PARES_GRUPO:
    sub = t3_sent[t3_sent['grupo'].isin([a, b])]
    tab = pd.crosstab(sub['grupo'].astype(str), sub['tipo'])
    c2, p, g, _ = stats.chi2_contingency(tab, correction=False)
    linhas.append({'Comparação': f'{a} × {b}', 'n': len(sub), 'χ²': c2, 'gl': g, 'p': p, 'V de Cramér': tst_cramer(tab)})
t3_pares_tipo = pd.DataFrame(linhas)
t3_pares_tipo['p Holm'] = tst_holm(t3_pares_tipo['p'])
tst_tabela_p(t3_pares_tipo, 'tst_tipo_pares', 'Tipo de sentença: comparações par a par (tabelas 2 × 3), com Holm',
             '3.2.2', casas=3)
for _, r in t3_pares_tipo.iterrows():
    tst_registra('3.2', 'H1 pares', f'χ² 2×3 {r["Comparação"]}', 'mesma distribuição de tipos',
                 f'χ²({r["gl"]}) = {fmt_br(r["χ²"], 2)}', r['p'], f'V = {fmt_br(r["V de Cramér"], 3)}')

fig, ax = plt.subplots(figsize=(7.5, 4.2))
barras_verticais(ax, t3_pares_tipo['Comparação'], t3_pares_tipo['V de Cramér'], cores=COR_NEUTRA, rotular=False,
                 ylabel='V de Cramér (0 = nenhuma associação)', ymax=max(0.35, t3_pares_tipo['V de Cramér'].max() * 1.45))
for i, (v, p) in enumerate(zip(t3_pares_tipo['V de Cramér'], t3_pares_tipo['p Holm'])):
    ax.annotate(f'V = {fmt_br(v, 2)}\np Holm {tst_eq(p)}', (i, v), xytext=(0, 3), textcoords='offset points',
                ha='center', va='bottom', fontsize=9, color=TINTA)
ax.set_title('Força da associação tipo de sentença × par de grupos')
figura(fig, 'tst_tipo_pares', 'Quais pares de grupos diferem no tipo de sentença?', secao='3.2.2',
       nota='χ² 2 × 3 entre os sentenciados; valores-p ajustados por Holm na família de três pares.')
''')

md(r'''
### 3.2.3 Hipótese-chave: a AC obrigatória troca mérito por extinção sem mérito?

A Lei 9.099/1995 (art. 51, I) extingue o processo, sem resolução de mérito, quando o **autor deixa de comparecer a qualquer das audiências**. Num rito com AC inaugural obrigatória, cada ausência do autor vira extinção; no rito atual (Controle), sem audiência inaugural, o processo segue para contestação e julgamento. A hipótese substantiva (gerada pelos dados da Parte I; ver 3.1.2) é: **mais "sem mérito" e menos "mérito" nos braços com AC**.

Para cada tipo de sentença, testa-se o desfecho binário (o tipo × os demais) entre os grupos:

- **H₀:** a proporção do tipo é a mesma nos três grupos (χ² 3 × 2); depois, par a par, **Fisher exato** com **razão de chances (OR)** e IC 95% condicional exato, e a **diferença de proporções** com IC de Newcombe. Os nove pares formam uma família ajustada por Holm.
- **Leitura do gráfico:** proporção de cada tipo por grupo, com IC de Wilson.
- A homologação (acordo) aparece aqui por completude; ela é idêntica a "acordo em qualquer momento" entre os sentenciados e é discutida, numa janela sem censura, na seção 3.3.
''')

code(r'''
linhas_glob, linhas_par = [], []
for tipo in ['Sem mérito', 'Mérito', 'Homologação']:
    y = (t3_sent['tipo'] == tipo)
    tab = pd.crosstab(t3_sent['grupo'], y)
    c2, p, g, e = stats.chi2_contingency(tab, correction=False)
    linhas_glob.append({'Tipo': tipo, 'χ²': c2, 'gl': g, 'p': p, 'mín. esperada': e.min(), 'V': tst_cramer(tab)})
    for a, b in PARES_GRUPO:
        xa, na = int(y[t3_sent['grupo'] == a].sum()), int((t3_sent['grupo'] == a).sum())
        xb, nb = int(y[t3_sent['grupo'] == b].sum()), int((t3_sent['grupo'] == b).sum())
        pf, orm, orc, olo, ohi = tst_fisher([[xa, na - xa], [xb, nb - xb]])
        dif, dlo, dhi = tst_newcombe(xa, na, xb, nb)
        linhas_par.append({'Tipo': tipo, 'Comparação': f'{a} × {b}', f'% {a[:4]}.': 100 * xa / na,
                           'x/n (1º)': f'{xa}/{na}', 'x/n (2º)': f'{xb}/{nb}', 'OR': orm, 'OR IC inf': olo,
                           'OR IC sup': ohi, 'Dif. (p.p.)': 100 * dif, 'Dif. IC inf': 100 * dlo,
                           'Dif. IC sup': 100 * dhi, 'p': pf})
t3_glob_bin = pd.DataFrame(linhas_glob); t3_glob_bin['p Holm'] = tst_holm(t3_glob_bin['p'])
t3_par_bin = pd.DataFrame(linhas_par).drop(columns=[c for c in pd.DataFrame(linhas_par) if c.startswith('% ')])
t3_par_bin['p Holm'] = tst_holm(t3_par_bin['p'])
tst_tabela_p(t3_glob_bin.assign(Tipo=t3_glob_bin['Tipo'].map(ROTULO_DESFECHO)), 'tst_tipobin_global',
             'Cada tipo de sentença × grupo: testes globais 3 × 2 (Holm entre os três tipos)', '3.2.3', casas=3,
             formatos={'mín. esperada': 1})
tst_tabela_p(t3_par_bin.assign(Tipo=t3_par_bin['Tipo'].map(ROTULO_DESFECHO)), 'tst_tipobin_pares',
             'Cada tipo de sentença: pares de grupos (Fisher exato, OR e diferença em pontos percentuais)', '3.2.3',
             casas=2, formatos={'Dif. (p.p.)': 1, 'Dif. IC inf': 1, 'Dif. IC sup': 1},
             nota='OR amostral com IC 95% condicional exato; diferença 1º − 2º com IC 95% de Newcombe; Holm na família de nove pares.')
for _, r in t3_glob_bin.iterrows():
    tst_registra('3.2', 'H2 tipos binários', f'χ² 3×2 {r["Tipo"]} × grupo', 'proporção igual nos 3 grupos',
                 f'χ²(2) = {fmt_br(r["χ²"], 2)}', r['p'], f'V = {fmt_br(r["V"], 3)}')
for _, r in t3_par_bin.iterrows():
    tst_registra('3.2', 'H2 pares (Fisher)', f'Fisher {r["Tipo"]}: {r["Comparação"]}', 'OR = 1', f'OR = {fmt_br(r["OR"], 2)}',
                 r['p'], f'dif. = {tst_ic_txt(r["Dif. (p.p.)"], r["Dif. IC inf"], r["Dif. IC sup"], 1)} p.p.')

fig, ax = plt.subplots(1, 3, figsize=(14, 4.6))
for k, tipo in enumerate(['Sem mérito', 'Mérito', 'Homologação']):
    xs = [int((t3_sent.loc[t3_sent['grupo'] == g, 'tipo'] == tipo).sum()) for g in ORDEM_GRUPO]
    ns = [int((t3_sent['grupo'] == g).sum()) for g in ORDEM_GRUPO]
    tst_barras_wilson(ax[k], ORDEM_GRUPO, xs, ns, ylabel='Sentenciados do grupo (%)' if k == 0 else '')
    r = t3_glob_bin.loc[t3_glob_bin['Tipo'] == tipo].iloc[0]
    anotar_teste(ax[k], texto_teste('χ² 3 × 2', f'χ²(2) = {fmt_br(r["χ²"], 1)}', r['p Holm'], f'V = {fmt_br(r["V"], 2)}')
                 .replace('p ', 'p Holm ', 1), loc='upper left', tamanho=8)
    ax[k].set_title(ROTULO_DESFECHO[tipo])
    ax[k].set_ylim(0, ax[k].get_ylim()[1] * 1.25)
figura(fig, 'tst_tipobin', 'A AC obrigatória troca sentenças de mérito por extinções sem mérito?', secao='3.2.3',
       nota='percentual de cada tipo entre os sentenciados do grupo, com IC 95% de Wilson; valor-p do χ² global ajustado por Holm entre os três tipos.')
''')

md(r'''
**Mecanismo (descritivo, não é teste).** Nos braços com AC, cruza-se o tipo de sentença com a realização da AC. `ac_realizada` é uma variável **pós-sorteio** — ser ou não realizada depende do comportamento das partes —, por isso a tabela não estima efeito causal: apenas mostra *onde* estão as extinções sem mérito. Uma AC "não realizada" pode ser ausência do autor (art. 51, I) ou extinção anterior à data da audiência (desistência, indeferimento da inicial).
''')

code(r'''
trat = t3_sent[t3_sent['grupo'] != 'Controle'].copy()
trat['AC'] = trat['ac_realizada'].map({True: 'AC realizada', False: 'AC não realizada'}).fillna('não informado')
t3_mec = pd.crosstab([trat['grupo'].astype(str), trat['AC']], trat['tipo'])
_mec = t3_mec.assign(Total=t3_mec.sum(axis=1)).rename(columns=ROTULO_DESFECHO).reset_index()
_mec.columns = ['Grupo', 'Audiência'] + [str(c) for c in _mec.columns[2:]]
tabela(_mec, 'tst_mecanismo_n', 'Braços com AC: tipo de sentença conforme a AC foi ou não realizada (frequências)', secao='3.2.3',
       nota='ac_realizada é pós-sorteio: a tabela é descritiva, não estima efeito causal.')
_mecp = (100 * t3_mec.div(t3_mec.sum(axis=1), axis=0)).rename(columns=ROTULO_DESFECHO).reset_index()
_mecp.columns = ['Grupo', 'Audiência'] + [str(c) for c in _mecp.columns[2:]]
tabela(_mecp, 'tst_mecanismo_pct', 'Braços com AC: tipo de sentença conforme a AC foi ou não realizada (% da linha)',
       secao='3.2.3', casas=1)

perc = t3_mec.div(t3_mec.sum(axis=1), axis=0)
ns_mec = t3_mec.sum(axis=1).to_numpy()
perc.index = [f'{g}: {a}' for g, a in perc.index]
fig, ax = plt.subplots(figsize=(10, 4.8))
barras_empilhadas(ax, perc, cores=CORES_DESFECHO, ns=ns_mec, rotulos_serie=ROTULO_DESFECHO, quebrar=16,
                  ylabel='Sentenciados (%)')
ax.set_title('Composição dos tipos de sentença por grupo e realização da AC')
figura(fig, 'tst_mecanismo', 'Nos braços com AC, as extinções sem mérito se concentram onde a audiência não se realizou?',
       secao='3.2.3', nota='descritivo: a realização da AC depende do comportamento das partes (variável pós-sorteio).')
''')

md(r'''
### 3.2.4 Redistribuição (Decisão) × grupo

A redistribuição (remessa a outro juízo por prevenção ou incompetência) não é sentença, mas pode depender do rito: uma AC obrigatória dá mais uma oportunidade de alguém perceber a prevenção. A base são os **938 processos** (a redistribuição costuma ocorrer nos primeiros dias, de modo que a censura pouco a afeta).

- **H₀:** a proporção de redistribuições é igual nos três grupos. Com 24 eventos, as esperadas ficam em torno de 8, e o χ² assintótico é conferido pela **permutação de Monte Carlo** (10.000 reamostragens).
''')

code(r'''
y_red = (t3['tipo_desfecho'] == 'Redistribuição')
tab_red = pd.crosstab(t3['grupo'], y_red)
c2_red, p_red, _, e_red = stats.chi2_contingency(tab_red, correction=False)
_, p_red_mc, p_red_ffh, _ = tst_perm_rxc(t3['grupo'], y_red)
_tr = tab_red.rename(columns={False: 'Não redistribuído', True: 'Redistribuído'})
tabela(tst_tab(_tr.assign(**{'Redistribuído (%)': 100 * _tr['Redistribuído'] / _tr.sum(axis=1)}), 'Grupo'),
       'tst_redist', 'Redistribuição (Decisão) por grupo (938 processos)', secao='3.2.4', casas=1)
print(f'Esperadas mínimas = {fmt_br(e_red.min(), 1)} | χ²(2) = {fmt_br(c2_red, 2)}, p assintótico {tst_eq(p_red)}, '
      f'p permutação (χ²) {tst_eq(p_red_mc)}, p Fisher-Freeman-Halton MC {tst_eq(p_red_ffh)} | V = {fmt_br(tst_cramer(tab_red), 3)}')
tst_registra('3.2', 'H3 redistribuição', 'Redistribuição × grupo (FFH Monte Carlo)', 'proporção igual',
             f'χ²(2) = {fmt_br(c2_red, 2)}', p_red_ffh, f'V = {fmt_br(tst_cramer(tab_red), 3)}')

fig, ax = plt.subplots(figsize=(6.5, 4.3))
tst_barras_wilson(ax, ORDEM_GRUPO, [int(tab_red.loc[g, True]) for g in ORDEM_GRUPO],
                  [int(tab_red.loc[g].sum()) for g in ORDEM_GRUPO], ylabel='Processos redistribuídos (%)')
anotar_teste(ax, texto_teste('Fisher-Freeman-Halton (Monte Carlo)', f'χ²(2) = {fmt_br(c2_red, 2)}', p_red_ffh,
                             f'V = {fmt_br(tst_cramer(tab_red), 3)}'), loc='upper left')
figura(fig, 'tst_redist', f'A redistribuição não depende do rito (p {tst_eq(p_red_ffh)})', secao='3.2.4',
       nota='IC 95% de Wilson; 24 redistribuições em 938 processos; valor-p por permutação de Monte Carlo (10.000).')
''')

md(r'''
### 3.2.5 Sensibilidade sem censura: desfecho até o 65º dia

Todo processo tem no mínimo 65 dias de acompanhamento. Logo, a variável "**como o processo estava no 65º dia**" (homologação, mérito, sem mérito, redistribuído ou ainda sem desfecho) é observada **para os 938**, sem censura e sem condicionar a quem já encerrou. É a forma correta de usar um χ² de "status" (o notebook do professor usou o status na data de corte, que mistura seguimentos de 65 a 279 dias — E19).

- **H₀:** a situação no 65º dia é independente do grupo.
''')

code(r'''
t3['sit65'] = np.where(t3['tempo_f'] <= 65, t3['tipo_desfecho'].astype(str), 'Sem desfecho até 65 d')
t3['sit65'] = np.where((t3['sit65'] == 'Ativo'), 'Sem desfecho até 65 d', t3['sit65'])
ORDEM_SIT65 = ['Homologação', 'Mérito', 'Sem mérito', 'Redistribuição', 'Sem desfecho até 65 d']
tab65 = pd.crosstab(t3['grupo'], t3['sit65'])[ORDEM_SIT65]
c2_65, p_65, gl_65, e_65 = stats.chi2_contingency(tab65, correction=False)
v65, v65lo, v65hi = tst_cramer_ic(t3['grupo'], t3['sit65'])
ROT65 = {**ROTULO_DESFECHO, 'Sem desfecho até 65 d': 'Sem desfecho até o 65º dia'}
tabela(tst_tab(tab65.assign(Total=tab65.sum(axis=1)), 'Grupo', ROT65), 'tst_sit65_obs',
       'Situação de cada processo no 65º dia, por grupo (938 processos, sem censura)', secao='3.2.5')
print(f'Esperada mínima = {fmt_br(e_65.min(), 1)} | χ²({gl_65}) = {fmt_br(c2_65, 2)}, p {tst_eq(p_65)} | V = {tst_ic_txt(v65, v65lo, v65hi, 3)}')
_res65 = tst_residuos(tab65)
tabela(tst_tab(_res65, 'Grupo', ROT65), 'tst_sit65_res', 'Resíduos ajustados: situação no 65º dia × grupo', secao='3.2.5',
       gradiente={'mapa': DIV, 'vmin': -6, 'vmax': 6, 'colunas': [ROT65[c] for c in ORDEM_SIT65]})
tst_registra('3.2', 'H1 tipo × grupo', 'χ² situação no 65º dia × grupo (938, sem censura)', 'independência',
             f'χ²({gl_65}) = {fmt_br(c2_65, 2)}', p_65, f'V = {tst_ic_txt(v65, v65lo, v65hi, 3)}')

fig, ax = plt.subplots(1, 2, figsize=(14, 4.8), gridspec_kw={'width_ratios': [1, 1.25]})
perc = tab65.div(tab65.sum(axis=1), axis=0)
cores65 = {**CORES_DESFECHO, 'Sem desfecho até 65 d': CORES_DESFECHO['Ativo']}
barras_empilhadas(ax[0], perc, cores=cores65, ns=tab65.sum(axis=1).to_numpy(), rotulos_serie=ROT65,
                  ylabel='Processos do grupo (%)')
ax[0].set_title('Situação no 65º dia')
tst_heatmap_res(ax[1], _res65, limite=6, rotulos_col=ROT65, quebrar=11,
                titulo='Resíduos ajustados\n' + f'χ²({gl_65}) = {fmt_br(c2_65, 1)}; p {tst_eq(p_65)}; V = {tst_ic_txt(v65, v65lo, v65hi, 2)}')
figura(fig, 'tst_sit65', 'No 65º dia, observado para todos, a situação dos processos difere entre os grupos', secao='3.2.5',
       nota='todo processo tem ao menos 65 dias de acompanhamento: a comparação não depende da censura.')
''')

md(r'''
### 3.2.6 Sem mérito e mérito em horizontes fixos (seguimento completo)

A janela de 65 dias elimina a censura, mas é curta: só capta as extinções e os julgamentos mais rápidos. Para verificar se o excesso de extinções sem mérito e a falta de julgamentos de mérito nos braços com AC **dependem do horizonte**, repete-se a comparação em 90, 120 e 150 dias. Em cada horizonte h, entram só os processos com pelo menos h dias de acompanhamento (distribuídos até 07/10/2026 − h). Para eles, "sentença sem mérito (ou de mérito) até o dia h" é observada **sem censura**. O sorteio vale dentro de cada subconjunto, porque a exclusão depende apenas da data de distribuição.

- **H₀:** a proporção de processos com sentença sem mérito (ou de mérito) até o dia h é a mesma no braço com AC e no Controle. **Teste:** Fisher exato, com a diferença em pontos percentuais e IC de Newcombe. Os oito pares de cada tipo (4 horizontes × 2 braços) formam uma família ajustada por Holm.
- **Cautela:** os horizontes são aninhados, e os testes, correlacionados; a leitura é do **padrão** ao longo do horizonte, não de um p isolado.
''')

code(r'''
H_FIXOS = [65, 90, 120, 150]
linhas = []
for h in H_FIXOS:
    base_h = t3[t3['followup'] >= h]
    for tipo in ['Sem mérito', 'Mérito']:
        y = (base_h['tipo_desfecho'] == tipo) & (base_h['tempo_f'] <= h)
        x = {g: int(y[base_h['grupo'] == g].sum()) for g in ORDEM_GRUPO}
        n_ = {g: int((base_h['grupo'] == g).sum()) for g in ORDEM_GRUPO}
        for g in ['Presencial', 'Remota']:
            pf, orm, _, olo, ohi = tst_fisher([[x[g], n_[g] - x[g]], [x['Controle'], n_['Controle'] - x['Controle']]])
            dif, dlo, dhi = tst_newcombe(x[g], n_[g], x['Controle'], n_['Controle'])
            linhas.append({'Tipo': tipo, 'Horizonte (dias)': h, 'n': len(base_h), 'Comparação': f'{g} × Controle',
                           'Braço': f'{x[g]}/{n_[g]}', 'Controle': f'{x["Controle"]}/{n_["Controle"]}',
                           '% braço': 100 * x[g] / n_[g], '% Controle': 100 * x['Controle'] / n_['Controle'],
                           'Dif. p.p. [IC Newcombe]': tst_ic_txt(100 * dif, 100 * dlo, 100 * dhi, 1), 'OR': orm, 'p': pf})
t3_hfix = pd.DataFrame(linhas)
t3_hfix['p Holm'] = np.nan
for tipo in ['Sem mérito', 'Mérito']:
    m = t3_hfix['Tipo'] == tipo
    t3_hfix.loc[m, 'p Holm'] = tst_holm(t3_hfix.loc[m, 'p'])
tst_tabela_p(t3_hfix.assign(Tipo=t3_hfix['Tipo'].map(ROTULO_DESFECHO)), 'tst_tipo_horizontes',
             'Sentença sem mérito e de mérito até o dia h, braço com AC × Controle (só processos com seguimento ≥ h)',
             '3.2.6', casas=2, formatos={'% braço': 1, '% Controle': 1},
             nota='Fisher exato; diferença braço − Controle com IC 95% de Newcombe; Holm na família de oito pares de cada tipo.')
for _, r in t3_hfix.iterrows():
    tst_registra('3.2', 'H2 horizonte fixo', f'Fisher {r["Tipo"]} até {r["Horizonte (dias)"]} d: {r["Comparação"]}', 'OR = 1',
                 f'OR = {fmt_br(r["OR"], 2)}', r['p'], f'dif. = {r["Dif. p.p. [IC Newcombe]"]} p.p.')

fig, ax = plt.subplots(1, 2, figsize=(13, 4.6), sharex=True)
for k, tipo in enumerate(['Sem mérito', 'Mérito']):
    for j, g in enumerate(ORDEM_GRUPO):
        ps, los, his = [], [], []
        for h in H_FIXOS:
            base_h = t3[t3['followup'] >= h]
            xg = int(((base_h['tipo_desfecho'] == tipo) & (base_h['tempo_f'] <= h) & (base_h['grupo'] == g)).sum())
            ng = int((base_h['grupo'] == g).sum())
            lo, hi = tst_wilson(xg, ng)
            ps.append(100 * xg / ng); los.append(100 * lo); his.append(100 * hi)
        xx = np.array(H_FIXOS) + (j - 1) * 2.5
        ax[k].errorbar(xx, ps, yerr=[np.array(ps) - los, np.array(his) - ps], fmt='-o', color=CORES_GRUPO[g], capsize=3,
                       ms=5, lw=1.5, label=g)
    topo = ax[k].get_ylim()[1] * 1.3
    ax[k].set_ylim(0, topo)
    ax[k].set_xlim(H_FIXOS[0] - 18, H_FIXOS[-1] + 18)
    for h in H_FIXOS:
        sub = t3_hfix[(t3_hfix['Tipo'] == tipo) & (t3_hfix['Horizonte (dias)'] == h)].set_index('Comparação')
        txt = '\n'.join(f'{c[0]}: p Holm {tst_eq(sub.loc[c, "p Holm"])}' for c in sub.index)
        ax[k].annotate(txt, (h, topo), xytext=(0, -4), textcoords='offset points', ha='center', va='top', fontsize=6.5, color=TINTA_2)
    ax[k].set_title(f'{ROTULO_DESFECHO[tipo]} até o dia h')
    ax[k].set_xticks(H_FIXOS, [f'{h} d\n(n = {int((t3["followup"] >= h).sum())})' for h in H_FIXOS])
    ax[k].set_xlabel('Horizonte h (só processos com seguimento ≥ h)')
    eixo_pct(ax[k], escala=1)
ax[0].set_ylabel('Processos do grupo (%)')
ax[1].legend(loc='center left')
figura(fig, 'tst_tipo_horizontes', 'Sem censura, o déficit de mérito nos braços com AC é nítido em todos os horizontes; o excesso de extinções sem mérito é menor e, na Remota, tardio',
       secao='3.2.6', nota='IC 95% de Wilson; P = Presencial, R = Remota: p de Fisher (braço × Controle) ajustado por Holm na família de oito pares de cada tipo.')
''')

interp('tst_desfecho')

# =====================================================================
md(r'''
---

## 3.3 Acordo (H4 a H7)

### 3.3.1 Acordo na AC: presencial × remota (H4)

Só há acordo na AC onde houve AC. A comparação válida é **Presencial × Remota entre as AC realizadas** (o χ² do professor incluía o Controle, com zero estrutural — E20).

- **H₀:** p(acordo na AC | AC presencial) = p(acordo na AC | AC remota). **H₁:** bilateral.
- **Teste:** exato de Fisher. Com 17 acordos ao todo, as esperadas da coluna "acordo" ficam em torno de 8,5; o χ² ainda seria admissível pela regra de Cochran, mas o Fisher é exato e dispensa a aproximação. Efeitos: OR (IC condicional exato) e diferença de proporções (IC de Newcombe).
- **Poder:** com ~175 audiências por braço, calcula-se a menor diferença detectável com 80% de poder a partir da taxa observada — para dizer se um "não significativo" é informativo.
''')

code(r'''
t3_ac = t3[t3['ac_realizada'].fillna(False).astype(bool) & (t3['grupo'] != 'Controle')].copy()
t3_ac['grupo'] = t3_ac['grupo'].cat.remove_unused_categories()
tab_acac = pd.crosstab(t3_ac['grupo'], t3_ac['acordo_ac'].fillna(False).astype(bool)).reindex(columns=[True, False], fill_value=0)
xp, xr = int(tab_acac.loc['Presencial', True]), int(tab_acac.loc['Remota', True])
np_, nr = int(tab_acac.loc['Presencial'].sum()), int(tab_acac.loc['Remota'].sum())
p_acac, or_acac, orc_acac, or_lo, or_hi = tst_fisher(tab_acac.values)
dif_acac, dlo_acac, dhi_acac = tst_newcombe(xp, np_, xr, nr)
_t = tab_acac.rename(columns={True: 'Acordo na AC', False: 'Sem acordo'})
tabela(tst_tab(_t.assign(**{'Acordo (%)': 100 * _t['Acordo na AC'] / _t.sum(axis=1)}), 'Grupo'), 'tst_acordo_ac',
       'Acordo na audiência de conciliação, entre as AC realizadas: Presencial × Remota', secao='3.3.1', casas=1)
print(f'Presencial {fmt_br(100 * xp / np_, 1)}% × Remota {fmt_br(100 * xr / nr, 1)}% | Fisher p {tst_eq(p_acac)}')
print(f'OR = {fmt_br(or_acac, 2)} (condicional {fmt_br(orc_acac, 2)}; IC 95% exato {fmt_br(or_lo, 2)} a {fmt_br(or_hi, 2)})')
print(f'Diferença = {fmt_br(100 * dif_acac, 1)} p.p. (IC 95% Newcombe {fmt_br(100 * dlo_acac, 1)} a {fmt_br(100 * dhi_acac, 1)} p.p.)')
p_base = (xp + xr) / (np_ + nr)
for alvo in np.arange(0.005, 0.30, 0.001):
    poder = NormalIndPower().power(proportion_effectsize(p_base + alvo, p_base), nobs1=np_, ratio=nr / np_, alpha=0.05)
    if poder >= 0.8:
        break
print(f'Com taxa-base de {pct_br(p_base)} e esses n, só um aumento ≥ {fmt_br(100 * alvo, 1)} p.p. (a partir da taxa-base) teria 80% de poder (α = 5%).')
tst_registra('3.3', 'H4 acordo AC modalidade', 'Fisher acordo na AC: Presencial × Remota', 'OR = 1', f'OR = {fmt_br(or_acac, 2)}',
             p_acac, f'dif. = {tst_ic_txt(100 * dif_acac, 100 * dlo_acac, 100 * dhi_acac, 1)} p.p.')

fig, ax = plt.subplots(figsize=(6.5, 4.5))
tst_barras_wilson(ax, ['Presencial', 'Remota'], [xp, xr], [np_, nr], ylabel='Acordo entre as AC realizadas (%)')
ax.set_xticks([0, 1], [f'AC presencial\n(n = {np_})', f'AC remota\n(n = {nr})'])
anotar_teste(ax, texto_teste('Fisher exato', f'OR = {fmt_br(or_acac, 2)} [{fmt_br(or_lo, 2)}; {fmt_br(or_hi, 2)}]', p_acac,
                             f'dif. = {tst_ic_txt(100 * dif_acac, 100 * dlo_acac, 100 * dhi_acac, 1)} p.p.'), loc='upper left')
figura(fig, 'tst_acordo_ac', f'A modalidade da AC não altera a taxa de acordo na audiência '
       f'({fmt_br(100 * xp / np_, 1)}% × {fmt_br(100 * xr / nr, 1)}%)', secao='3.3.1',
       nota=f'IC 95% de Wilson; OR com IC condicional exato; diferença com IC de Newcombe. Com estes n, só um aumento '
            f'≥ {fmt_br(100 * alvo, 1)} p.p. sobre a taxa-base teria 80% de poder.')
''')

md(r'''
### 3.3.2 Acordo em qualquer momento (H5)

"Acordo" (na AC ou fora dela) existe nos três grupos, inclusive no Controle (por petição). Entre os sentenciados, acordo é exatamente a **homologação**, já testada em 3.2.3; aquela comparação, porém, é condicional a quem encerrou. Aqui o acordo é medido **em horizonte fixo**, sem censura:

- **Janela de 65 dias:** homologação até o 65º dia, para os 938 processos (todos acompanhados por ≥ 65 dias);
- **Janela de 120 dias:** homologação até o 120º dia, só entre os processos com ≥ 120 dias de acompanhamento (distribuídos até 09/06/2026).

**H₀:** a proporção de acordos até o horizonte é igual nos três grupos. χ² 3 × 2 (ou permutação, se esparso) e Fisher par a par com Holm.
''')

code(r'''
linhas = []
fig, ax = plt.subplots(1, 2, figsize=(12.5, 4.6))
for k, h in enumerate([65, 120]):
    base_h = t3[t3['followup'] >= h]
    y = (base_h['tipo_desfecho'] == 'Homologação') & (base_h['tempo_f'] <= h)
    tab = pd.crosstab(base_h['grupo'], y)
    c2, p, _, e = stats.chi2_contingency(tab, correction=False)
    _, p_mc, _, _ = tst_perm_rxc(base_h['grupo'], y)
    print(f'Horizonte {h} dias (n = {len(base_h)}): acordos {tab[True].to_dict()} | esperada mín. {fmt_br(e.min(), 1)} | '
          f'χ²(2) = {fmt_br(c2, 2)}, p {tst_eq(p)}, p permutação {tst_eq(p_mc)}')
    tst_registra('3.3', 'H5 acordo total', f'χ² acordo até {h} d × grupo', 'proporção igual', f'χ²(2) = {fmt_br(c2, 2)}', p_mc,
                 f'V = {fmt_br(tst_cramer(tab), 3)}')
    for a, b in PARES_GRUPO:
        xa, na = int(y[base_h['grupo'] == a].sum()), int((base_h['grupo'] == a).sum())
        xb, nb = int(y[base_h['grupo'] == b].sum()), int((base_h['grupo'] == b).sum())
        pf, orm, _, olo, ohi = tst_fisher([[xa, na - xa], [xb, nb - xb]])
        dif, dlo, dhi = tst_newcombe(xa, na, xb, nb)
        linhas.append({'Horizonte': h, 'Comparação': f'{a} × {b}', '1º': f'{xa}/{na}', '2º': f'{xb}/{nb}', 'OR': orm,
                       'OR IC': f'{fmt_br(olo, 2)} a {fmt_br(ohi, 2)}', 'Dif. p.p. [IC Newcombe]':
                       tst_ic_txt(100 * dif, 100 * dlo, 100 * dhi, 1), 'p': pf})
    xs = [int(tab.loc[g, True]) if True in tab else 0 for g in ORDEM_GRUPO]
    ns = [int(tab.loc[g].sum()) for g in ORDEM_GRUPO]
    tst_barras_wilson(ax[k], ORDEM_GRUPO, xs, ns, ylabel='Processos com acordo homologado (%)' if k == 0 else '')
    ax[k].set_title(f'Acordo até o {h}º dia (n = {fmt_br(len(base_h), 0)})')
    ax[k].set_ylim(0, ax[k].get_ylim()[1] * 1.25)
    anotar_teste(ax[k], texto_teste('χ² (permutação)', f'χ²(2) = {fmt_br(c2, 2)}', p_mc, f'V = {fmt_br(tst_cramer(tab), 3)}'),
                 loc='upper left', tamanho=8)
ymax = max(a.get_ylim()[1] for a in ax)
for a in ax:
    a.set_ylim(0, ymax)
figura(fig, 'tst_acordo_horizonte', 'O rito altera a proporção de acordos em horizonte fixo (65 e 120 dias)?', secao='3.3.2',
       nota='65 dias: os 938 processos; 120 dias: só os distribuídos até 09/06/2026 (acompanhamento ≥ 120 dias). IC 95% de Wilson.')
t3_acordo_pares = pd.DataFrame(linhas)
t3_acordo_pares['p Holm'] = np.concatenate([tst_holm(t3_acordo_pares.loc[t3_acordo_pares['Horizonte'] == h, 'p']) for h in [65, 120]])
tst_tabela_p(t3_acordo_pares.rename(columns={'Horizonte': 'Horizonte (dias)'}), 'tst_acordo_horizonte_pares',
             'Acordo em horizonte fixo: pares de grupos (Fisher exato), Holm dentro de cada horizonte', '3.3.2', casas=2)
for _, r in t3_acordo_pares.iterrows():
    tst_registra('3.3', 'H5 pares', f'Fisher acordo até {r["Horizonte"]} d: {r["Comparação"]}', 'OR = 1',
                 f'OR = {fmt_br(r["OR"], 2)}', r['p'], f'dif. = {r["Dif. p.p. [IC Newcombe]"]} p.p.')
''')

md(r'''
### 3.3.3 Acordo fora da AC × grupo (H6)

Acordo por petição das partes, fora da audiência, homologado por sentença. Atenção à leitura: no Controle esse é o **único** caminho de acordo; nos braços com AC, é o acordo que veio **depois** de uma AC sem acordo, ou sem AC realizada.

A variável `acordo_fora` só existe para os processos já encerrados. Compará-la entre os encerrados repetiria o viés da comparação condicional, que depende da data de corte. Por isso, como na H5, o desfecho é medido em **horizonte fixo**: acordo fora da AC homologado até o 120º dia, entre os processos com pelo menos 120 dias de acompanhamento. A versão condicional (encerrados) é mostrada só para comparação e não entra no registro.

- **H₀:** a proporção de acordo fora da AC até o 120º dia é igual nos três grupos.
''')

code(r'''
# versão condicional (só para comparação): encerrados com o registro
_enc_f = t3[t3['acordo_fora'].notna()]
_tab_cond = pd.crosstab(_enc_f['grupo'], _enc_f['acordo_fora'].astype(bool))
p_f_cond = stats.chi2_contingency(_tab_cond, correction=False)[1]
print('Versão condicional (encerrados, ' + str(len(_enc_f)) + '): acordo fora '
      + ', '.join(f'{g} {pct_br(_tab_cond.loc[g, True] / _tab_cond.loc[g].sum())}' for g in ORDEM_GRUPO)
      + f' | χ² p {tst_eq(p_f_cond)} (não entra no registro)')

base_f = t3[t3['followup'] >= 120]
y_f = base_f['acordo_fora'].fillna(False).astype(bool) & (base_f['tempo_f'] <= 120)
tab_f = pd.crosstab(base_f['grupo'], y_f)
c2_f, p_f, _, e_f = stats.chi2_contingency(tab_f, correction=False)
_t = tab_f.rename(columns={True: 'Acordo fora', False: 'Sem acordo fora até 120 d'})[['Acordo fora', 'Sem acordo fora até 120 d']]
tabela(tst_tab(_t.assign(**{'Acordo fora (%)': 100 * _t['Acordo fora'] / _t.sum(axis=1)}), 'Grupo'), 'tst_acordo_fora',
       f'Acordo fora da audiência homologado até o 120º dia, por grupo ({fmt_br(len(base_f), 0)} processos com seguimento ≥ 120 dias)',
       secao='3.3.3', casas=1)
print(f'Horizonte 120 d (n = {len(base_f)}): esperada mín. = {fmt_br(e_f.min(), 1)} | χ²(2) = {fmt_br(c2_f, 2)}, p {tst_eq(p_f)} | '
      f'V = {fmt_br(tst_cramer(tab_f), 3)}')
tst_registra('3.3', 'H6 acordo fora', 'χ² acordo fora da AC até 120 d × grupo', 'proporção igual', f'χ²(2) = {fmt_br(c2_f, 2)}', p_f,
             f'V = {fmt_br(tst_cramer(tab_f), 3)}')
linhas = []
for a, b in PARES_GRUPO:
    xa, na = int(tab_f.loc[a, True]), int(tab_f.loc[a].sum()); xb, nb = int(tab_f.loc[b, True]), int(tab_f.loc[b].sum())
    pf, orm, _, olo, ohi = tst_fisher([[xa, na - xa], [xb, nb - xb]])
    dif, dlo, dhi = tst_newcombe(xa, na, xb, nb)
    linhas.append({'Comparação': f'{a} × {b}', 'OR': orm, 'OR IC': f'{fmt_br(olo, 2)} a {fmt_br(ohi, 2)}',
                   'Dif. p.p. [IC]': tst_ic_txt(100 * dif, 100 * dlo, 100 * dhi, 1), 'p': pf})
t3_fora_pares = pd.DataFrame(linhas); t3_fora_pares['p Holm'] = tst_holm(t3_fora_pares['p'])
tst_tabela_p(t3_fora_pares, 'tst_acordo_fora_pares', 'Acordo fora da AC até o 120º dia: pares de grupos (Fisher exato), com Holm',
             '3.3.3', casas=2)
for _, r in t3_fora_pares.iterrows():
    tst_registra('3.3', 'H6 pares', f'Fisher acordo fora até 120 d: {r["Comparação"]}', 'OR = 1', f'OR = {fmt_br(r["OR"], 2)}', r['p'],
                 f'dif. = {r["Dif. p.p. [IC]"]} p.p.')

fig, ax = plt.subplots(figsize=(6.5, 4.5))
tst_barras_wilson(ax, ORDEM_GRUPO, [int(tab_f.loc[g, True]) for g in ORDEM_GRUPO], [int(tab_f.loc[g].sum()) for g in ORDEM_GRUPO],
                  ylabel='Acordo fora da AC até o 120º dia (%)')
anotar_teste(ax, texto_teste('χ² de independência', f'χ²(2) = {fmt_br(c2_f, 2)}', p_f, f'V = {fmt_br(tst_cramer(tab_f), 3)}'),
             loc='upper left')
figura(fig, 'tst_acordo_fora', 'O acordo fora da audiência (até o 120º dia) varia entre os grupos?', secao='3.3.3',
       nota='base: processos com seguimento ≥ 120 dias (distribuídos até 09/06/2026); IC 95% de Wilson. No Controle, é o único caminho de acordo.')
''')

md(r'''
### 3.3.4 AC híbrida e técnica de conciliação (H7)

**Híbrida.** Dentro do braço Presencial, uma AC é "híbrida" quando uma das partes pediu para participar por vídeo (Res. CNJ 481). É uma característica **pós-sorteio** (escolha da parte), portanto a comparação é observacional. **H₀:** p(acordo na AC) igual entre AC híbridas e totalmente presenciais (Fisher exato).

**Técnica.** A técnica foi sorteada entre as AC realizadas (Presencial e Remota). São 6 técnicas e 17 acordos: tabela 6 × 2 muito esparsa (todas as esperadas da coluna "acordo" abaixo de 5, a maioria abaixo de 3). O χ² assintótico não vale; usa-se a **permutação de Monte Carlo** com margens fixas, com a estatística χ² e com a probabilidade da tabela (Fisher-Freeman-Halton). **H₀:** a probabilidade de acordo na AC é a mesma para as seis técnicas. Com tão poucos eventos, o poder é baixíssimo: um "não significativo" aqui **não** mostra que as técnicas são equivalentes.
''')

code(r'''
pres = t3_ac[t3_ac['grupo'] == 'Presencial']
pres = pres[pres['hibrida'].notna()]
tab_h = pd.crosstab(pres['hibrida'].astype(bool), pres['acordo_ac'].fillna(False).astype(bool)).reindex(index=[True, False], columns=[True, False], fill_value=0)
p_h, or_h, _, orh_lo, orh_hi = tst_fisher(tab_h.values)
_t = tab_h.rename(index={True: 'Híbrida', False: 'Presencial pura'}, columns={True: 'Acordo na AC', False: 'Sem acordo'})
tabela(tst_tab(_t.assign(**{'Acordo (%)': 100 * _t['Acordo na AC'] / _t.sum(axis=1)}), 'Formato da AC'), 'tst_hibrida',
       'Braço Presencial: acordo na AC híbrida × totalmente presencial (AC realizadas)', secao='3.3.4', casas=1)
print(f'Fisher p {tst_eq(p_h)} | OR = {fmt_br(or_h, 2)} (IC exato {fmt_br(orh_lo, 2)} a {fmt_br(orh_hi, 2)})')
tst_registra('3.3', 'H7 híbrida/técnica', 'Fisher híbrida × acordo na AC (Presencial)', 'OR = 1', f'OR = {fmt_br(or_h, 2)}', p_h,
             f'OR IC {fmt_br(orh_lo, 2)} a {fmt_br(orh_hi, 2)}')

tec = t3_ac[t3_ac['tecnica_curta'].notna()].copy()
tec['tecnica_curta'] = tec['tecnica_curta'].cat.remove_unused_categories()
y_tec = tec['acordo_ac'].fillna(False).astype(bool)
tab_tec = pd.crosstab(tec['tecnica_curta'], y_tec)
chi_tec, p_tec_chi, p_tec_ffh, chi_null = tst_perm_rxc(tec['tecnica_curta'], y_tec, B=20000)
e_tec = stats.contingency.expected_freq(tab_tec.values)
_t = tab_tec.rename(columns={True: 'Acordo', False: 'Sem acordo'})[['Acordo', 'Sem acordo']]
tabela(tst_tab(_t.assign(**{'Acordo (%)': 100 * tab_tec[True] / tab_tec.sum(axis=1),
                            'Acordos esperados sob H₀': e_tec[:, 1]}), 'Técnica de conciliação'), 'tst_tecnica',
       'Acordo na AC por técnica de conciliação sorteada (AC realizadas, Presencial e Remota)', secao='3.3.4', casas=1,
       nota='todas as esperadas da coluna "acordo" são menores que 5: o χ² assintótico não vale; usa-se permutação.')
print(f'χ² = {fmt_br(chi_tec, 2)}; p permutação (χ²) {tst_eq(p_tec_chi)}; p Fisher-Freeman-Halton MC {tst_eq(p_tec_ffh)} '
      f'(20.000 permutações)')
print(f'p assintótico (só para comparar, inválido aqui) {tst_eq(stats.chi2.sf(chi_tec, (tab_tec.shape[0] - 1)))}')
tst_registra('3.3', 'H7 híbrida/técnica', 'Técnica × acordo na AC (FFH Monte Carlo)', 'acordo independente da técnica',
             f'χ²(5) = {fmt_br(chi_tec, 2)}', p_tec_ffh, f'V = {fmt_br(tst_cramer(tab_tec), 3)}')

fig, ax = plt.subplots(1, 2, figsize=(13, 4.8), gridspec_kw={'width_ratios': [0.55, 1.45]})
tst_barras_wilson(ax[0], ['Híbrida', 'Presencial pura'], [int(tab_h.loc[True, True]), int(tab_h.loc[False, True])],
                  [int(tab_h.loc[True].sum()), int(tab_h.loc[False].sum())], cores=CORES_GRUPO['Presencial'],
                  ylabel='Acordo na AC (%)', quebrar=10)
ax[0].set_title('AC híbrida (braço Presencial)')
anotar_teste(ax[0], texto_teste('Fisher exato', f'OR = {fmt_br(or_h, 2)}', p_h, f'IC 95%: {fmt_br(orh_lo, 2)} a {fmt_br(orh_hi, 2)}'),
             loc='upper left', tamanho=8)
tst_barras_wilson(ax[1], list(tab_tec.index), tab_tec[True].to_numpy(), tab_tec.sum(axis=1).to_numpy(), cores=COR_NEUTRA,
                  ylabel='', quebrar=13)
ax[1].set_title('Técnica de conciliação sorteada')
anotar_teste(ax[1], texto_teste('Fisher-Freeman-Halton (Monte Carlo)', f'χ²(5) = {fmt_br(chi_tec, 2)}', p_tec_ffh,
                                f'V = {fmt_br(tst_cramer(tab_tec), 3)}'), loc='upper left', tamanho=8)
ymax = max(a.get_ylim()[1] for a in ax)
for a in ax:
    a.set_ylim(0, ymax)
figura(fig, 'tst_hibrida_tecnica', 'A AC híbrida ou a técnica de conciliação alteram a chance de acordo na audiência?',
       secao='3.3.4', nota='IC 95% de Wilson. Com 17 acordos ao todo, o poder é muito baixo: um resultado não significativo não '
                           'demonstra equivalência entre as técnicas.')

fig, ax = plt.subplots(figsize=(8, 4.3))
ax.hist(chi_null, bins=40, color=CINZA, edgecolor='white', density=True, label='χ² sob H₀ (20.000 permutações)')
ax.axvline(chi_tec, color=DESTAQUE, lw=2, label=f'χ² observado = {fmt_br(chi_tec, 1)}')
xs = np.linspace(0, chi_null.max(), 200)
ax.plot(xs, stats.chi2.pdf(xs, 5), color=TINTA, lw=1.2, ls='--', label='densidade χ²(5) teórica')
ax.set_xlabel('Estatística χ² (técnica × acordo na AC)'); ax.set_ylabel('Densidade')
ax.legend(loc='upper right')
anotar_teste(ax, texto_teste('Permutação de Monte Carlo', None, p_tec_chi, f'p FFH {tst_eq(p_tec_ffh)}'), loc='center right')
figura(fig, 'tst_tecnica_permutacao', 'Distribuição de permutação do χ² técnica × acordo: o observado não é raro sob H₀',
       secao='3.3.4', nota='proporção das permutações com χ² ≥ observado = valor-p de permutação.')
''')

interp('tst_acordo')

# =====================================================================
md(r'''
---

## 3.4 Tempo entre os sentenciados: testes clássicos e por que não bastam (H8)

### 3.4.1 Kruskal-Wallis, ε² e Dunn

**Atenção — análise condicional.** Aqui só entram os **708 processos sentenciados**. É a distribuição do tempo *dado que a sentença saiu até 07/10/2026*: os processos lentos que ainda estão ativos ficam de fora, e ficam mais de fora nos grupos com mais ativos (Presencial e Remota). O resultado descreve os encerrados, **não** estima o efeito do rito sobre o tempo (isso é feito na Parte IV, com Kaplan-Meier e log-rank).

- **H₀ (Kruskal-Wallis):** as três distribuições do tempo são iguais (nenhum grupo é estocasticamente maior). H₁: ao menos um grupo tende a valores maiores. O KW só se lê como "medianas iguais" se as formas forem iguais (E17).
- **Efeito:** ε² = H/(n − 1) (TOMCZAK; TOMCZAK, 2014); referência grosseira: 0,01 pequeno, 0,08 médio, 0,26 grande.
- **Post-hoc:** teste de Dunn (1964) com ajuste de Holm, que usa os postos conjuntos do KW (o notebook do professor usava Mann-Whitney sem correção).
''')

code(r'''
t3_enc = t3_sent.copy()
amostras = [t3_enc.loc[t3_enc['grupo'] == g, 'tempo_f'].values for g in ORDEM_GRUPO]
H_kw, p_kw = stats.kruskal(*amostras)
eps2 = H_kw / (len(t3_enc) - 1)
desc = t3_enc.groupby('grupo', observed=True)['tempo_f'].describe()[['count', '25%', '50%', '75%', 'mean']]
tabela(desc.rename(columns={'count': 'n', '25%': 'Q1 (dias)', '50%': 'Mediana (dias)', '75%': 'Q3 (dias)',
                            'mean': 'Média (dias)'}).rename_axis('Grupo'), 'tst_tempo_desc',
       'Tempo até a sentença entre os sentenciados, por grupo (estatística condicional)', secao='3.4.1', casas=1,
       nota='só os 708 sentenciados: os processos ainda ativos (mais longos) ficam de fora, de modo desigual entre os grupos.')
print(f'Kruskal-Wallis: H = {fmt_br(H_kw, 2)}, gl = 2, p {tst_eq(p_kw)} | ε² = {fmt_br(eps2, 4)}')
dunn = sp.posthoc_dunn(t3_enc, val_col='tempo_f', group_col='grupo', p_adjust='holm').loc[ORDEM_GRUPO, ORDEM_GRUPO]
tst_tabela_p(dunn.rename_axis('Grupo'), 'tst_dunn', 'Teste de Dunn: valores-p par a par ajustados por Holm (tempo, sentenciados)',
             '3.4.1', colunas_p=tuple(ORDEM_GRUPO), destaque=None)
tst_registra('3.4', 'H8 tempo (condicional)', 'Kruskal-Wallis tempo × grupo (sentenciados)', 'distribuições iguais',
             f'H(2) = {fmt_br(H_kw, 2)}', p_kw, f'ε² = {fmt_br(eps2, 4)}')

fig, ax = plt.subplots(1, 2, figsize=(12.5, 4.8), gridspec_kw={'width_ratios': [1.4, 1]})
boxplot_grupos(ax[0], t3_enc, 'tempo_f', ylabel=ROTULOS['tempo_sentenca'])
ax[0].set_title('Distribuição do tempo, só sentenciados')
ax[0].set_ylim(0, t3_enc['tempo_f'].max() * 1.22)
anotar_teste(ax[0], texto_teste('Kruskal-Wallis', f'H(2) = {fmt_br(H_kw, 2)}', p_kw, f'ε² = {fmt_br(eps2, 4)}'), loc='upper left')
anot = dunn.apply(lambda c: c.map(fmt_p)).to_numpy()
sns.heatmap(dunn.astype(float), annot=anot, fmt='', cmap=SEQ.reversed(), vmin=0, vmax=0.1, ax=ax[1], linewidths=1,
            linecolor='white', cbar_kws={'label': 'p ajustado (Holm)'}, annot_kws={'fontsize': 9})
ax[1].collections[0].colorbar.ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: fmt_br(v, 2)))
ax[1].tick_params(length=0); ax[1].grid(False); ax[1].set_xlabel(''); ax[1].set_ylabel('')
ax[1].set_yticklabels(ax[1].get_yticklabels(), rotation=0)
ax[1].set_title('Dunn: p par a par (Holm)')
figura(fig, 'tst_tempo_kw', 'Entre os sentenciados, o tempo até a sentença é praticamente igual nos três grupos',
       secao='3.4.1', nota='análise condicional aos 708 sentenciados; não estima o efeito do rito sobre o tempo (ver Parte IV). '
                           'Md = mediana. Cores mais escuras no mapa = p menor.')
''')

md(r'''
### 3.4.2 Mann-Whitney par a par com delta de Cliff

O mesmo contraste em pares, com o **delta de Cliff** d = P(X > Y) − P(X < Y), que vai de −1 a 1 e coincide com a correlação bisserial de postos. Referência de Romano et al. (2006): |d| < 0,147 desprezível, < 0,33 pequeno, < 0,474 médio. **H₀:** P(X > Y) = P(X < Y). Holm na família de três pares.
''')

code(r'''
linhas = []
for a, b in PARES_GRUPO:
    xa = t3_enc.loc[t3_enc['grupo'] == a, 'tempo_f']; xb = t3_enc.loc[t3_enc['grupo'] == b, 'tempo_f']
    U, p = stats.mannwhitneyu(xa, xb, alternative='two-sided')
    d, dlo, dhi = tst_cliff(xa, xb)
    linhas.append({'Comparação': f'{a} × {b}', 'n1': len(xa), 'n2': len(xb), 'U': U, 'p': p,
                   'delta de Cliff': d, 'IC inf': dlo, 'IC sup': dhi})
t3_mw = pd.DataFrame(linhas); t3_mw['p Holm'] = tst_holm(t3_mw['p'])
tst_tabela_p(t3_mw, 'tst_mw', 'Mann-Whitney par a par com delta de Cliff (IC 95% bootstrap), tempo entre os sentenciados',
             '3.4.2', casas=3)
for _, r in t3_mw.iterrows():
    tst_registra('3.4', 'H8 pares MW', f'Mann-Whitney {r["Comparação"]} (sentenciados)', 'P(X>Y) = P(X<Y)',
                 f'U = {fmt_br(r["U"], 0)}', r['p'], f'Cliff d = {tst_ic_txt(r["delta de Cliff"], r["IC inf"], r["IC sup"], 3)}')

fig, ax = plt.subplots(figsize=(8, 4.3))
ax.axhspan(-0.147, 0.147, color='#EEF0F3', label='|d| < 0,147 (efeito desprezível)')
ax.axhline(0, color=TINTA_2, lw=1)
for i, r in t3_mw.iterrows():
    ax.errorbar(i, r['delta de Cliff'], yerr=[[r['delta de Cliff'] - r['IC inf']], [r['IC sup'] - r['delta de Cliff']]],
                fmt='o', color=TINTA, capsize=6, ms=8, mec='white', mew=1.5)
    ax.annotate(f'd = {fmt_br(r["delta de Cliff"], 3)}\np Holm {tst_eq(r["p Holm"])}', (i, r['delta de Cliff']),
                xytext=(12, 0), textcoords='offset points', fontsize=8.5, va='center')
ax.set_xticks(range(3), [f'{c}\n(n = {a} e {b})' for c, a, b in zip(t3_mw['Comparação'], t3_mw['n1'], t3_mw['n2'])])
ax.set_xlim(-0.4, 2.8)
ax.set_ylabel('Delta de Cliff (1º − 2º)')
ax.grid(axis='x', visible=False)
legenda_abaixo(ax, ncol=1, dy=-0.22)
desprezivel = bool((t3_mw[['IC inf', 'IC sup']].abs().max(axis=1) < 0.33).all())
figura(fig, 'tst_mw', 'Mann-Whitney par a par: diferenças de tempo entre os sentenciados são '
       + ('no máximo pequenas' if desprezivel else 'relevantes em algum par'), secao='3.4.2',
       nota='delta de Cliff d = P(X > Y) − P(X < Y), com IC 95% bootstrap; referências de Romano et al. (2006).')
''')

md(r'''
### 3.4.3 Teste da mediana de Mood

Teste mais simples e robusto (só usa "acima/abaixo da mediana geral"), com menos poder que o KW. **H₀:** os três grupos têm a mesma mediana populacional. É uma tabela 3 × 2 testada por χ².
''')

code(r'''
stat_m, p_m, med_m, tab_m = stats.median_test(*amostras, ties='below')
tab_m = pd.DataFrame(tab_m, index=['> mediana', '≤ mediana'], columns=ORDEM_GRUPO)
tabela(tab_m.rename_axis(f'Tempo vs. mediana geral ({fmt_br(med_m, 0)} dias)'), 'tst_mood',
       'Teste da mediana de Mood: sentenciados acima e abaixo da mediana geral, por grupo', secao='3.4.3')
print(f'Mediana geral = {fmt_br(med_m, 0)} dias | χ²(2) = {fmt_br(stat_m, 2)}, p {tst_eq(p_m)}')
tst_registra('3.4', 'H8 tempo (condicional)', 'Mediana de Mood (sentenciados)', 'medianas iguais', f'χ²(2) = {fmt_br(stat_m, 2)}', p_m, '')

fig, ax = plt.subplots(figsize=(6.5, 4.5))
tst_barras_wilson(ax, ORDEM_GRUPO, [int(tab_m.loc['> mediana', g]) for g in ORDEM_GRUPO],
                  [int(tab_m[g].sum()) for g in ORDEM_GRUPO], ylabel=f'Acima da mediana geral de {fmt_br(med_m, 0)} dias (%)',
                  ymax=85)
ax.axhline(50, color=TINTA_2, lw=1)
ax.annotate('50% (H₀)', (2.45, 50), xytext=(0, 3), textcoords='offset points', ha='right', fontsize=8.5, color=TINTA_2)
anotar_teste(ax, texto_teste('Mediana de Mood', f'χ²(2) = {fmt_br(stat_m, 2)}', p_m), loc='upper left')
figura(fig, 'tst_mood', 'A proporção de sentenciados acima da mediana geral é a mesma nos três grupos?', secao='3.4.3',
       nota='só sentenciados (condicional); IC 95% de Wilson.')
''')

md(r'''
### 3.4.4 ANOVA e Welch: contraste didático

A ANOVA de um fator pressupõe normalidade dos resíduos e variâncias iguais; a ANOVA de Welch dispensa a igualdade de variâncias. Os pressupostos são verificados com **Levene** (centrado na média) e **Brown-Forsythe** (centrado na mediana, robusto) para a homogeneidade, e **Shapiro-Wilk** nos resíduos por grupo. O objetivo é **didático**: mostrar que, com n grande, a conclusão coincide com a do KW, mas que o teste paramétrico está formalmente fora das suas condições — e que nenhum dos dois resolve a censura.
''')

code(r'''
F_a, p_a = stats.f_oneway(*amostras)
welch = anova_oneway(t3_enc['tempo_f'].values, t3_enc['grupo'].astype(str).values, use_var='unequal')
lev, p_lev = stats.levene(*amostras, center='mean')
bf, p_bf = stats.levene(*amostras, center='median')
residuos = np.concatenate([a - a.mean() for a in amostras])
sw = {g: stats.shapiro(a - a.mean()) for g, a in zip(ORDEM_GRUPO, amostras)}
eta2 = F_a * 2 / (F_a * 2 + len(t3_enc) - 3)
_pres = pd.DataFrame([
    {'Teste': 'ANOVA de um fator', 'H₀': 'médias iguais', 'Estatística': F_a, 'p': p_a},
    {'Teste': 'ANOVA de Welch', 'H₀': 'médias iguais (variâncias livres)', 'Estatística': welch.statistic, 'p': welch.pvalue},
    {'Teste': 'Levene (média)', 'H₀': 'variâncias iguais', 'Estatística': lev, 'p': p_lev},
    {'Teste': 'Brown-Forsythe (mediana)', 'H₀': 'variâncias iguais', 'Estatística': bf, 'p': p_bf},
] + [{'Teste': f'Shapiro-Wilk, resíduos {g}', 'H₀': 'resíduos normais', 'Estatística': r.statistic, 'p': r.pvalue}
     for g, r in sw.items()])
tst_tabela_p(_pres, 'tst_anova', 'ANOVA e Welch (contraste didático) e verificação dos pressupostos', '3.4.4', casas=3,
             destaque='p', nota=f'η² = {fmt_br(eta2, 4)}. Linhas destacadas: p < 0,05 (pressuposto violado nos testes de variância e normalidade).')
tst_registra('3.4', 'H8 didático', 'ANOVA de Welch (sentenciados; didático)', 'médias iguais', f'F = {fmt_br(welch.statistic, 3)}',
             welch.pvalue, f'η² = {fmt_br(eta2, 4)}')

fig, ax = plt.subplots(1, 2, figsize=(12.5, 4.6))
medias = [a.mean() for a in amostras]
ep = [a.std(ddof=1) / np.sqrt(len(a)) for a in amostras]
barras_verticais(ax[0], ORDEM_GRUPO, medias, erro=([m - 1.96 * e for m, e in zip(medias, ep)], [m + 1.96 * e for m, e in zip(medias, ep)]),
                 rotular=False, ns=[len(a) for a in amostras], ylabel='Média do tempo até a sentença (dias), IC 95%')
for i, (m, e, a) in enumerate(zip(medias, ep, amostras)):
    ax[0].annotate(f'{fmt_br(m, 1)}\n(DP {fmt_br(a.std(ddof=1), 0)})', (i, m + 1.96 * e), xytext=(0, 3),
                   textcoords='offset points', ha='center', va='bottom', fontsize=8.5)
ax[0].set_ylim(0, max(medias) * 1.6)
ax[0].set_title('Médias por grupo (só sentenciados)')
anotar_teste(ax[0], texto_teste('ANOVA / Welch', f'F = {fmt_br(F_a, 2)} / {fmt_br(welch.statistic, 2)}', welch.pvalue,
                                f'η² = {fmt_br(eta2, 4)}; Brown-Forsythe p {tst_eq(p_bf)}'), loc='upper left', tamanho=8)
(osm, osr), _ = stats.probplot(residuos, dist='norm')
ax[1].scatter(osm, osr, s=6, color=TINTA_2, alpha=0.6, lw=0)
ax[1].plot(osm, osm * residuos.std(ddof=1), color=DESTAQUE, lw=1.5, label='normal de referência')
ax[1].set_xlabel('Quantis teóricos da N(0, 1)'); ax[1].set_ylabel('Resíduos da ANOVA (dias)')
ax[1].set_title('Q-Q dos resíduos'); ax[1].grid(axis='both', visible=True)
ax[1].legend(loc='lower right')
anotar_teste(ax[1], '\n'.join(['Shapiro-Wilk dos resíduos'] + [f'{g}: W = {fmt_br(r.statistic, 3)}; p {tst_eq(r.pvalue)}'
                                                               for g, r in sw.items()]), loc='upper left', tamanho=8)
figura(fig, 'tst_anova', 'ANOVA e Welch concordam com o Kruskal-Wallis, mas os pressupostos de normalidade e de variâncias iguais falham',
       secao='3.4.4', nota='contraste didático: nenhum dos dois testes resolve a censura.')
''')

md(r'''
### 3.4.5 Estratificado pelo tipo de sentença: o efeito de composição

Os tipos de sentença têm tempos muito diferentes (uma extinção sem mérito por ausência à AC sai rápido; um julgamento de mérito exige contestação e instrução). Como os grupos diferem na **composição** de tipos (seção 3.2), uma diferença no tempo "total" pode vir só da mistura. Testa-se, por isso, o tempo × grupo **dentro de cada tipo** (KW, Holm na família de três estratos).

Ressalva: estratificar por uma variável **pós-sorteio** (o tipo de desfecho é consequência do rito) quebra a comparabilidade garantida pelo sorteio; a análise é descritiva do mecanismo, não estimativa causal.
''')

code(r'''
linhas = []
fig, ax = plt.subplots(1, 3, figsize=(14.5, 4.8), sharey=True)
for k, tipo in enumerate(['Homologação', 'Mérito', 'Sem mérito']):
    sub = t3_enc[t3_enc['tipo'] == tipo]
    a = [sub.loc[sub['grupo'] == g, 'tempo_f'].values for g in ORDEM_GRUPO]
    H, p = stats.kruskal(*a)
    linhas.append({'Tipo': tipo, 'n': len(sub), **{f'Md {g}': np.median(x) for g, x in zip(ORDEM_GRUPO, a)},
                   'H': H, 'p': p, 'ε²': H / (len(sub) - 1)})
    boxplot_grupos(ax[k], sub, 'tempo_f', ylabel=ROTULOS['tempo_sentenca'] if k == 0 else None, tam_ponto=5)
    ax[k].set_title(ROTULO_DESFECHO[tipo])
    anotar_teste(ax[k], texto_teste('Kruskal-Wallis', f'H(2) = {fmt_br(H, 2)}', p, f'ε² = {fmt_br(H / (len(sub) - 1), 3)}'),
                 loc='upper left', tamanho=8)
ax[0].set_ylim(0, t3_enc['tempo_f'].max() * 1.3)
t3_estrato = pd.DataFrame(linhas); t3_estrato['p Holm'] = tst_holm(t3_estrato['p'])
figura(fig, 'tst_tempo_por_tipo', 'Dentro de cada tipo de sentença, o tempo difere entre os grupos?', secao='3.4.5',
       nota='só sentenciados; estratificar por uma variável pós-sorteio é descritivo do mecanismo, não estimativa causal. '
            f'Holm entre os três estratos: p = {", ".join(fmt_p(v) for v in t3_estrato["p Holm"])}.')
tst_tabela_p(t3_estrato.assign(Tipo=t3_estrato['Tipo'].map(ROTULO_DESFECHO))
             .rename(columns={f'Md {g}': f'Mediana {g} (dias)' for g in ORDEM_GRUPO}),
             'tst_tempo_por_tipo', 'Tempo até a sentença × grupo dentro de cada tipo de sentença (Kruskal-Wallis, Holm)',
             '3.4.5', casas=3, formatos={f'Mediana {g} (dias)': 1 for g in ORDEM_GRUPO})
for _, r in t3_estrato.iterrows():
    tst_registra('3.4', 'H8 por tipo', f'Kruskal-Wallis tempo × grupo, só {r["Tipo"]}', 'distribuições iguais',
                 f'H(2) = {fmt_br(r["H"], 2)}', r['p'], f'ε² = {fmt_br(r["ε²"], 4)}')
mediana_tipo = t3_enc.groupby('tipo', observed=True)['tempo_f'].median()
print('Mediana do tempo por tipo (todos os grupos):', {k: fmt_br(v, 0) for k, v in mediana_tipo.items()})
''')

md(r'''
### 3.4.6 O Kruskal-Wallis do professor (p ≈ 0,48) e como ele muda

O notebook do professor aplicou o KW a **todos** os processos, tratando o tempo dos ativos (censurado no corte) como tempo completo e a "Decisão" como sentença (E10, E14, E17), e concluiu "sem diferença" (H = 1,48; p = 0,478). Abaixo, o mesmo teste em quatro versões:

1. **Professor (reproduzido na base de 938):** todos os tempos, censurados como se completos;
2. **Só sentenciados (708):** condicional, seção 3.4.1;
3. **Janela de 65 dias (914, sem redistribuídos):** tempo truncado em 65, min(T, 65). Como todos são acompanhados por ≥ 65 dias, o tempo truncado é **observado** para todos: é a única versão do KW livre de censura (a média de min(T, 65) é o RMST de 65 dias da Parte IV; o KW compara os postos, não as médias, mas responde à mesma pergunta sem censura);
4. **Sentença até 65 dias (indicador):** χ² da proporção sentenciada até o 65º dia.

E também o **Mann-Whitney com × sem acordo na AC** do professor (E24), refeito só entre as AC realizadas que já têm sentença.
''')

code(r'''
def kw_grupos(df, col):
    a = [df.loc[df['grupo'] == g, col].values for g in ORDEM_GRUPO]
    H, p = stats.kruskal(*a)
    resumo = [np.mean(x) for x in a] if col == 'tempo65' else [np.median(x) for x in a]
    return H, p, resumo, len(df)

t3['tempo65'] = t3['tempo_f'].clip(upper=65)
nao_red = t3[t3['tipo_desfecho'] != 'Redistribuição']
versoes = {
    '1. Professor: todos, censura ignorada': kw_grupos(t3, 'tempo_f'),
    '2. Só sentenciados (condicional)': kw_grupos(t3_enc, 'tempo_f'),
    '3. Tempo truncado em 65 d (sem censura)': kw_grupos(nao_red, 'tempo65'),
}
y65 = (nao_red['evento'] == 1) & (nao_red['tempo_f'] <= 65)
tab_s65 = pd.crosstab(nao_red['grupo'], y65)
c2_s65, p_s65, _, _ = stats.chi2_contingency(tab_s65, correction=False)
MEDIDA = ['mediana (dias)', 'mediana (dias)', 'média de min(T, 65) (dias)']
linhas = [{'Versão': k, 'n': v[3], 'H / χ²': v[0], 'p': v[1], 'Medida': med, **{g: m for g, m in zip(ORDEM_GRUPO, v[2])}}
          for (k, v), med in zip(versoes.items(), MEDIDA)]
linhas.append({'Versão': '4. Sentença até 65 d (χ² 3×2)', 'n': len(nao_red), 'H / χ²': c2_s65, 'p': p_s65,
               'Medida': '% sentenciado até 65 d', **{g: 100 * tab_s65.loc[g, True] / tab_s65.loc[g].sum() for g in ORDEM_GRUPO}})
t3_versoes = pd.DataFrame(linhas)
tst_tabela_p(t3_versoes, 'tst_kw_versoes', 'O Kruskal-Wallis do professor em quatro versões: o resultado depende do tratamento da censura',
             '3.4.6', casas=2, formatos={g: 1 for g in ORDEM_GRUPO}, destaque='p')
print('% sentenciados até 65 dias:', {g: pct_br(tab_s65.loc[g, True] / tab_s65.loc[g].sum()) for g in ORDEM_GRUPO})
print('% de ativos (censurados) por grupo:', {g: pct_br((t3.loc[t3['grupo'] == g, 'tipo_desfecho'] == 'Ativo').mean()) for g in ORDEM_GRUPO})
print('Mediana do tempo dos ATIVOS por grupo (seguimento, não duração):',
      {g: fmt_br(t3.loc[(t3['grupo'] == g) & (t3['tipo_desfecho'] == 'Ativo'), 'tempo_f'].median(), 0) for g in ORDEM_GRUPO})
tst_registra('3.4', 'H8 sem censura', 'Kruskal-Wallis min(T, 65) × grupo', 'distribuições iguais',
             f'H(2) = {fmt_br(versoes["3. Tempo truncado em 65 d (sem censura)"][0], 2)}', versoes['3. Tempo truncado em 65 d (sem censura)'][1], '')
tst_registra('3.4', 'H8 sem censura', 'χ² sentença até 65 d × grupo', 'proporção igual', f'χ²(2) = {fmt_br(c2_s65, 2)}', p_s65,
             f'V = {fmt_br(tst_cramer(tab_s65), 3)}')

# E24: Mann-Whitney com × sem acordo na AC, refeito entre AC realizadas já sentenciadas
acs = t3_ac[t3_ac['evento'] == 1]
com, sem = acs.loc[acs['acordo_ac'] == True, 'tempo_f'], acs.loc[acs['acordo_ac'] == False, 'tempo_f']
U24, p24 = stats.mannwhitneyu(com, sem)
d24, d24lo, d24hi = tst_cliff(com, sem)
print(f'E24 refeito (AC realizadas e sentenciadas): com acordo n = {len(com)}, Md = {fmt_br(com.median(), 0)} | '
      f'sem acordo n = {len(sem)}, Md = {fmt_br(sem.median(), 0)} | U = {fmt_br(U24, 0)}, p {tst_eq(p24)}, '
      f'Cliff d = {tst_ic_txt(d24, d24lo, d24hi, 3)}')
tst_registra('3.4', 'H8 acordo', 'Mann-Whitney tempo com × sem acordo na AC (AC realizadas, sentenciados)', 'P(X>Y) = P(X<Y)',
             f'U = {fmt_br(U24, 0)}', p24, f'Cliff d = {tst_ic_txt(d24, d24lo, d24hi, 3)}')

ROT_VERSAO = ['1. Professor:\nmediana, censura\nignorada', '2. Sentenciados:\nmediana', '3. Média de\nmin(T, 65)']
fig, ax = plt.subplots(1, 2, figsize=(13.5, 4.8))
_tv = t3_versoes.iloc[:3][ORDEM_GRUPO].copy()
_tv.index = ROT_VERSAO
barras_agrupadas(ax[0], _tv, cores=CORES_GRUPO, rotular=True, fmt=lambda v: fmt_br(v, 0), ylabel='Dias', quebrar=40)
ax[0].set_title('Resumo do tempo por grupo em cada versão')
ax[0].legend(loc='upper right', fontsize=8)
pv = t3_versoes['p'].to_numpy()
cores_v = [CINZA, CINZA, COR_NEUTRA, COR_NEUTRA]
barras_verticais(ax[1], ['1. Professor', '2. Sentenciados', '3. min(T, 65)', '4. Sentença até 65 d'], pv, cores=cores_v,
                 rotular=False, ylabel='Valor-p do teste entre grupos', ymax=1.08, quebrar=12)
for i, p_ in enumerate(pv):
    ax[1].annotate(fmt_p(p_), (i, p_), xytext=(0, 3), textcoords='offset points', ha='center', va='bottom', fontsize=9)
ax[1].axhline(0.05, color=DESTAQUE, lw=1)
ax[1].annotate('α = 0,05', (3.45, 0.05), xytext=(0, 3), textcoords='offset points', ha='right', fontsize=8.5, color=DESTAQUE)
ax[1].set_title('Valor-p em cada versão (cinza: censura mal tratada)')
figura(fig, 'tst_kw_versoes', 'O "sem diferença" do Kruskal-Wallis do professor depende de como a censura é tratada',
       secao='3.4.6', nota='versões 3 e 4 usam a janela comum de 65 dias, observada para todos os processos (sem censura).')

_e24 = acs[acs['acordo_ac'].notna()].assign(Acordo=np.where(acs['acordo_ac'] == True, 'Com acordo na AC', 'Sem acordo na AC'))
fig, ax = plt.subplots(figsize=(6.5, 4.6))
boxplot_grupos(ax, _e24, 'tempo_f', grupo='Acordo', ordem=['Com acordo na AC', 'Sem acordo na AC'],
               cores={'Com acordo na AC': CORES_DESFECHO['Homologação'], 'Sem acordo na AC': CINZA},
               ylabel=ROTULOS['tempo_sentenca'])
ax.set_ylim(0, _e24['tempo_f'].max() * 1.3)
anotar_teste(ax, texto_teste('Mann-Whitney', f'U = {fmt_br(U24, 0)}', p24, f'Cliff d = {tst_ic_txt(d24, d24lo, d24hi, 2)}'),
             loc='upper left')
figura(fig, 'tst_e24', 'Entre as AC realizadas já sentenciadas, os processos com acordo terminam mais cedo (E24 refeito)',
       secao='3.4.6', nota='condicional aos sentenciados; a análise correta do acordo como desfecho concorrente está na Parte IV.')
''')

interp('tst_tempo')

# =====================================================================
md(r'''
---

## 3.5 Ordem de chegada (questão 2.7; H9 a H11)

### 3.5.1 O sorteio foi aleatório? Teste de corridas de Wald-Wolfowitz

Segundo o pesquisador, o sorteio seguiu a ordem de chegada. Se a alocação foi de fato aleatória, a sequência de grupos na ordem de chegada não deve ter **padrões**: nem corridas longas demais (blocos de um mesmo grupo), nem alternância regular demais (rodízio Controle → Presencial → Remota). O **número de corridas** R (sequências maximais de um mesmo grupo) mede isso.

- **H₀:** a sequência é uma permutação aleatória dos 938 rótulos. **H₁:** bilateral (R pequeno = agrupamento; R grande = alternância).
- **Três categorias:** a distribuição de R sob H₀ é obtida por **permutação** (10.000 embaralhamentos da sequência); também se compara a **maior corrida** observada.
- **Por grupo:** cada grupo × os demais (sequência binária), com a aproximação normal de Wald-Wolfowitz e Holm.
''')

code(r'''
seq = t3.sort_values('ordem_chegada')['grupo'].astype(str).values
def n_corridas(s):
    return 1 + int((s[1:] != s[:-1]).sum())
def maior_corrida(s):
    m = c = 1
    for i in range(1, len(s)):
        c = c + 1 if s[i] == s[i - 1] else 1
        m = max(m, c)
    return m
R_obs, L_obs = n_corridas(seq), maior_corrida(seq)
n = len(seq); cont = pd.Series(seq).value_counts()
E_R = 1 + (n - 1) - (cont * (cont - 1)).sum() / n
rng = np.random.default_rng(SEMENTE)
R_null, L_null = np.empty(10000), np.empty(10000)
for b in range(10000):
    s = rng.permutation(seq)
    R_null[b], L_null[b] = n_corridas(s), maior_corrida(s)
p_R = min(1, 2 * min((R_null <= R_obs).mean(), (R_null >= R_obs).mean()))
p_L = (L_null >= L_obs).mean()
print(f'Corridas observadas R = {R_obs} | esperado sob H0 = {fmt_br(E_R, 1)} | permutação: média {fmt_br(R_null.mean(), 1)}, '
      f'DP {fmt_br(R_null.std(), 1)} | p bilateral {tst_eq(p_R)}')
print(f'Maior corrida = {L_obs} | P(maior corrida ≥ {L_obs} sob H0) {tst_eq(p_L)}')
tst_registra('3.5', 'H9 sorteio', 'Corridas (3 grupos, permutação)', 'sequência aleatória', f'R = {R_obs} (E = {fmt_br(E_R, 1)})', p_R, '')

linhas = []
for g in ORDEM_GRUPO:
    b = (seq == g)
    n1, n2 = b.sum(), (~b).sum()
    R = n_corridas(b)
    mu = 2 * n1 * n2 / n + 1
    var = 2 * n1 * n2 * (2 * n1 * n2 - n) / (n ** 2 * (n - 1))
    z = (R - mu) / np.sqrt(var)
    linhas.append({'Grupo': g, 'n': n1, 'Corridas': R, 'Esperado': mu, 'z': z, 'p': 2 * stats.norm.sf(abs(z))})
t3_runs = pd.DataFrame(linhas); t3_runs['p Holm'] = tst_holm(t3_runs['p'])
tst_tabela_p(t3_runs, 'tst_corridas', 'Teste de corridas de Wald-Wolfowitz: cada grupo × os demais na ordem de chegada',
             '3.5.1', casas=2)
for _, r in t3_runs.iterrows():
    tst_registra('3.5', 'H9 sorteio por grupo', f'Corridas {r["Grupo"]} × demais (Wald-Wolfowitz)', 'sequência aleatória',
                 f'z = {fmt_br(r["z"], 2)}', r['p'], '')

fig, ax = plt.subplots(1, 3, figsize=(15, 4.5))
ax[0].hist(R_null, bins=40, color=CINZA, edgecolor='white')
ax[0].axvline(R_obs, color=DESTAQUE, lw=2)
ax[0].set_title('Número de corridas (3 grupos)'); ax[0].set_xlabel('Número de corridas R'); ax[0].set_ylabel('Permutações sob H₀')
anotar_teste(ax[0], texto_teste('Permutação (10.000)', f'R = {R_obs}; E(R) = {fmt_br(E_R, 1)}', p_R), loc='upper left', tamanho=8)
comp, freq = np.unique(L_null, return_counts=True)
ax[1].bar(comp, freq, color=CINZA, width=0.7)
ax[1].axvline(L_obs, color=DESTAQUE, lw=2)
ax[1].set_title('Maior corrida de um mesmo grupo'); ax[1].set_xlabel('Comprimento da maior corrida (processos)')
ax[1].set_ylabel('Permutações sob H₀'); ax[1].grid(axis='x', visible=False)
anotar_teste(ax[1], texto_teste('Permutação (10.000)', f'observada = {L_obs}', p_L), loc='upper right', tamanho=8)
ax[2].axhspan(-1.96, 1.96, color='#EEF0F3', label='|z| < 1,96 (compatível com H₀)')
barras_verticais(ax[2], ORDEM_GRUPO, t3_runs['z'], rotular=False, ylabel='z de Wald-Wolfowitz', ymax=3)
ax[2].set_ylim(-3, 3); ax[2].axhline(0, color=TINTA_2, lw=1)
for i, (z_, p_) in enumerate(zip(t3_runs['z'], t3_runs['p Holm'])):
    ax[2].annotate(f'z = {fmt_br(z_, 2)}\np Holm {tst_eq(p_)}', (i, z_), xytext=(0, 4 if z_ >= 0 else -4), textcoords='offset points',
                   ha='center', va='bottom' if z_ >= 0 else 'top', fontsize=8)
ax[2].set_title('Cada grupo × os demais'); legenda_abaixo(ax[2], ncol=1, dy=-0.2)
figura(fig, 'tst_corridas', 'A sequência dos grupos na ordem de chegada é compatível com um sorteio aleatório',
       secao='3.5.1', nota='linha vermelha = valor observado; distribuições de referência obtidas embaralhando a sequência real (10.000 vezes).')
''')

md(r'''
### 3.5.2 Ordem de chegada × tempo: Spearman, Kendall e o artefato da censura (H10)

A ordem de chegada é **ordinal**; o tempo, quantitativo com censura. Pearson não cabe (E13, E16); Spearman (ρ) e Kendall (τ-b, que trata empates) medem associação monótona. **H₀:** ρ = 0 (τ = 0).

O problema é a censura: um processo distribuído em agosto só pode aparecer "encerrado" se tiver sido rápido (no máximo 65 dias), enquanto um de janeiro pode ter encerrado em até 279 dias. Entre os encerrados, a ordem de chegada **tem de** se correlacionar negativamente com o tempo, mesmo que o ritmo da vara não tenha mudado. Quatro versões:

1. **Todos (938)**, tempo censurado como se completo;
2. **Só sentenciados (708)**: o artefato;
3. **Janela comum de 65 dias**: min(T, 65), observado para todos (censura administrativa em 65 dias para todos) — a versão válida;
4. **Simulação sob H₀:** tempos gerados independentemente da ordem e censurados com o acompanhamento real de cada processo; mostra que o artefato aparece mesmo quando não existe associação verdadeira.
''')

code(r'''
def corr_ord(df, col):
    rho, p_rho = stats.spearmanr(df['ordem_chegada'].astype(float), df[col])
    tau, p_tau = stats.kendalltau(df['ordem_chegada'].astype(float), df[col])
    return rho, p_rho, tau, p_tau, len(df)

t3_corr = pd.DataFrame([
    dict(zip(['Versão', 'ρ Spearman', 'p (ρ)', 'τ Kendall', 'p (τ)', 'n'], ['1. Todos, censura ignorada', *corr_ord(t3, 'tempo_f')])),
    dict(zip(['Versão', 'ρ Spearman', 'p (ρ)', 'τ Kendall', 'p (τ)', 'n'], ['2. Só sentenciados', *corr_ord(t3_enc, 'tempo_f')])),
    dict(zip(['Versão', 'ρ Spearman', 'p (ρ)', 'τ Kendall', 'p (τ)', 'n'], ['3. min(T, 65), sem redistribuídos', *corr_ord(nao_red, 'tempo65')])),
])
tst_tabela_p(t3_corr, 'tst_ordem_tempo', 'Ordem de chegada × tempo: Spearman e Kendall em três versões', '3.5.2', casas=3,
             colunas_p=('p (ρ)', 'p (τ)'), destaque='p (ρ)')
for i, r in t3_corr.iterrows():
    tst_registra('3.5', 'H10 ordem × tempo', f'Spearman ordem × tempo: {r["Versão"]}', 'ρ = 0', f'ρ = {fmt_br(r["ρ Spearman"], 3)}', r['p (ρ)'],
                 f'τ = {fmt_br(r["τ Kendall"], 3)}', natureza='principal' if i == 2 else 'didático')

# A tendência na janela sem censura é da vara toda ou dos braços com AC? (ρ dentro de cada grupo, que também
# remove o efeito da composição mensal desigual dos grupos)
t3_corr_g = pd.DataFrame([dict(zip(['Grupo', 'ρ Spearman', 'p (ρ)', 'τ Kendall', 'p (τ)', 'n'],
                                   [g, *corr_ord(nao_red[nao_red['grupo'] == g], 'tempo65')])) for g in ORDEM_GRUPO])
t3_corr_g['p Holm'] = tst_holm(t3_corr_g['p (ρ)'])
tst_tabela_p(t3_corr_g, 'tst_ordem_tempo_grupo', 'Ordem de chegada × min(T, 65) dentro de cada grupo (Spearman e Kendall, Holm entre os grupos)',
             '3.5.2', casas=3, colunas_p=('p (ρ)', 'p (τ)', 'p Holm'), destaque='p Holm')
for _, r in t3_corr_g.iterrows():
    tst_registra('3.5', 'H10 por grupo', f'Spearman ordem × min(T, 65): só {r["Grupo"]}', 'ρ = 0', f'ρ = {fmt_br(r["ρ Spearman"], 3)}',
                 r['p (ρ)'], f'τ = {fmt_br(r["τ Kendall"], 3)}')
_s65 = (nao_red['evento'] == 1) & (nao_red['tempo_f'] <= 65)
_s65m = _s65.groupby(nao_red['mes_distribuicao'].astype(str)).mean().reindex(['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago'])
print('% sentenciado até 65 d por mês de distribuição (todos os grupos):', {m: pct_br(v) for m, v in _s65m.items()})
_s65g = pd.crosstab(nao_red['mes_distribuicao'].astype(str), nao_red['grupo'], values=_s65.astype(float), aggfunc='mean')
_s65g = _s65g.reindex(['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago'])
for g in ORDEM_GRUPO:
    print(f'  {g}: ' + ', '.join(f'{m} {pct_br(v)}' for m, v in _s65g[g].items()))

# Simulação: tempos independentes da ordem, censurados pelo acompanhamento real de cada processo
rng = np.random.default_rng(SEMENTE)
fu = t3['followup'].astype(float).values; ordem = t3['ordem_chegada'].astype(float).values
sim = {'todos (censura ignorada)': [], 'só encerrados': [], 'min(T, 65)': []}
for _ in range(500):
    T = rng.weibull(1.6, len(fu)) * 115            # forma e escala próximas às dos dados; sem relação com a ordem
    obs = np.minimum(T, fu); enc = T <= fu
    sim['todos (censura ignorada)'].append(stats.spearmanr(ordem, obs)[0])
    sim['só encerrados'].append(stats.spearmanr(ordem[enc], obs[enc])[0])
    sim['min(T, 65)'].append(stats.spearmanr(ordem, np.minimum(T, 65))[0])
sim = pd.DataFrame(sim)
tabela(pd.DataFrame({'Versão': sim.columns, 'ρ médio sob H₀': sim.mean().to_numpy(),
                     'Percentil 2,5': sim.quantile(.025).to_numpy(), 'Percentil 97,5': sim.quantile(.975).to_numpy(),
                     'ρ observado': t3_corr['ρ Spearman'].to_numpy()}),
       'tst_ordem_simulacao', 'Simulação sob H₀ (500 réplicas): o ρ que a censura produz sem nenhuma associação real',
       secao='3.5.2', casas=3, nota='tempos Weibull independentes da ordem, censurados pelo acompanhamento real de cada processo.')

fig, ax = plt.subplots(1, 2, figsize=(13.5, 4.8))
ev = t3['evento'] == 1
ax[0].scatter(t3.loc[~ev, 'ordem_chegada'], t3.loc[~ev, 'tempo_f'], color=CORES_STATUS['Ativo (censurado)'], s=7, lw=0,
              label='ativo ou redistribuído (censurado)')
ax[0].scatter(t3.loc[ev, 'ordem_chegada'], t3.loc[ev, 'tempo_f'], color=CORES_STATUS['Sentença'], s=7, lw=0, alpha=0.7,
              label='sentenciado')
srt = t3.sort_values('ordem_chegada')
ax[0].plot(srt['ordem_chegada'], srt['followup'], color=DESTAQUE, lw=1.5, label='acompanhamento máximo (fronteira da censura)')
ax[0].axhline(65, color=TINTA, lw=1, label='janela comum de 65 dias')
ax[0].set_xlabel(ROTULOS['ordem_chegada']); ax[0].set_ylabel(ROTULOS['tempo'])
ax[0].set_title('Os encerrados ficam abaixo da fronteira da censura')
legenda_abaixo(ax[0], ncol=2, dy=-0.17, markerscale=2)
pos = np.arange(3)
bp = ax[1].boxplot([sim[c] for c in sim], positions=pos, widths=0.4, patch_artist=True,
                   boxprops=dict(facecolor='#E6E9ED', edgecolor=TINTA_2), medianprops=dict(color=TINTA),
                   whiskerprops=dict(color=TINTA_2), capprops=dict(color=TINTA_2), flierprops=dict(ms=3, mec=TINTA_2))
obs_rho = [t3_corr['ρ Spearman'].iloc[0], t3_corr['ρ Spearman'].iloc[1], t3_corr['ρ Spearman'].iloc[2]]
ax[1].scatter(pos, obs_rho, color=DESTAQUE, zorder=3, s=50, label='ρ observado nos dados')
for x_, r_ in zip(pos, obs_rho):
    ax[1].annotate(f'ρ = {fmt_br(r_, 3)}', (x_, r_), xytext=(10, 0), textcoords='offset points', va='center', fontsize=8.5)
ax[1].axhline(0, color=TINTA_2, lw=1)
ax[1].set_xticks(pos, ['Todos\n(censura ignorada)', 'Só encerrados', 'min(T, 65)\n(sem censura)'])
ax[1].set_ylabel('ρ de Spearman (ordem × tempo)'); ax[1].set_title('ρ sob H₀ simulada (caixas) × ρ observado')
legenda_abaixo(ax[1], ncol=1, dy=-0.2)
figura(fig, 'tst_ordem_tempo', 'A correlação negativa entre ordem de chegada e tempo é produzida pela censura?',
       secao='3.5.2', nota='simulação: 500 réplicas com tempos independentes da ordem e a censura real; '
                           'se o ρ observado cai dentro da caixa, a correlação é compatível com puro artefato.')
''')

md(r'''
### 3.5.3 Grupo × mês de distribuição (H11)

Mesmo com sorteio aleatório, a composição mensal pode oscilar. Se oscilar além do acaso, o mês (que determina o acompanhamento e a sazonalidade da pauta) vira **confundidor** potencial. Agosto (6 processos, até 03/08) é unido a julho.

- **H₀:** a distribuição dos grupos é a mesma em todos os meses (χ² de independência 7 × 3).
''')

code(r'''
mes = t3['mes_distribuicao'].astype(str).replace({'jul': 'jul–ago', 'ago': 'jul–ago'})
ordem_mes = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul–ago']
t3['mes7'] = pd.Categorical(mes, categories=ordem_mes, ordered=True)
tab_mes = pd.crosstab(t3['mes7'], t3['grupo'])
c2_mes, p_mes, gl_mes, e_mes = stats.chi2_contingency(tab_mes, correction=False)
v_mes, vm_lo, vm_hi = tst_cramer_ic(t3['mes7'], t3['grupo'])
tabela(tst_tab(tab_mes.assign(Total=tab_mes.sum(axis=1)), 'Mês de distribuição'), 'tst_grupo_mes',
       'Processos por mês de distribuição e grupo', secao='3.5.3', nota='agosto (6 processos, até 03/08) foi unido a julho.')
print(f'Esperada mín. = {fmt_br(e_mes.min(), 1)} | χ²({gl_mes}) = {fmt_br(c2_mes, 2)}, p {tst_eq(p_mes)} | V = {tst_ic_txt(v_mes, vm_lo, vm_hi, 3)}')
res_mes = tst_residuos(tab_mes)
tabela(tst_tab(res_mes, 'Mês de distribuição'), 'tst_grupo_mes_res', 'Resíduos ajustados: grupo × mês de distribuição',
       secao='3.5.3', gradiente={'mapa': DIV, 'vmin': -4, 'vmax': 4, 'colunas': ORDEM_GRUPO})
tst_registra('3.5', 'H11 grupo × mês', 'χ² grupo × mês de distribuição', 'independência', f'χ²({gl_mes}) = {fmt_br(c2_mes, 2)}', p_mes,
             f'V = {tst_ic_txt(v_mes, vm_lo, vm_hi, 3)}')

fig, ax = plt.subplots(1, 2, figsize=(14, 4.6), gridspec_kw={'width_ratios': [1.35, 1]})
perc = 100 * tab_mes.div(tab_mes.sum(axis=1), axis=0)
perc.index = [f'{m}\n(n = {int(tab_mes.loc[m].sum())})' for m in perc.index]
barras_agrupadas(ax[0], perc[ORDEM_GRUPO], cores=CORES_GRUPO, ylabel='Processos do mês (%)', xlabel=ROTULOS['mes_distribuicao'])
ax[0].set_ylim(0, 75); eixo_pct(ax[0], escala=1)
ax[0].axhline(100 / 3, color=TINTA_2, lw=1)
ax[0].annotate('1/3 (alocação equilibrada)', (6.45, 100 / 3), xytext=(0, 3), textcoords='offset points', ha='right',
               fontsize=8, color=TINTA_2)
ax[0].legend(loc='upper left', ncol=3)
ax[0].set_title('Composição de cada mês')
anotar_teste(ax[0], texto_teste('χ² de independência', f'χ²({gl_mes}) = {fmt_br(c2_mes, 2)}', p_mes,
                                f'V = {tst_ic_txt(v_mes, vm_lo, vm_hi, 2)}'), loc='upper right', tamanho=8)
tst_heatmap_res(ax[1], res_mes.T, limite=4, titulo='Resíduos ajustados (grupo × mês)')
figura(fig, 'tst_grupo_mes', f'A composição dos grupos varia por mês além do acaso? (p {tst_eq(p_mes)})', secao='3.5.3',
       nota='julho concentra Remota (ver resíduos): o mês entra como covariável/estrato nas Partes IV e V.')
''')

interp('tst_ordem')

# =====================================================================
md(r'''
---

## 3.6 Os testes do notebook do professor × as decisões deste notebook (questão 2.11)

### 3.6.1 Reprodução dos testes problemáticos

Para que a comparação seja concreta, os testes do notebook do professor que dependem da base são reproduzidos na base primária (938). Os números diferem um pouco dos originais (944 linhas, com duplicatas, linha vazia e "Decisão" como sentença), mas a conclusão de cada um é a mesma. **Esses testes não entram no registro da seção 3.7**: são exibidos para crítica, não como achados.
''')

code(r'''
rep = {}
tab = pd.crosstab(t3['grupo'], t3['encerrado'].astype(bool)); rep['χ² grupo × status (E19)'] = stats.chi2_contingency(tab, correction=False)[1]
tab = pd.crosstab(t3['grupo'], t3['acordo_ac'].fillna(False).astype(bool)); rep['χ² grupo × acordo na AC com Controle (E20)'] = stats.chi2_contingency(tab, correction=False)[1]
e20 = stats.chi2_contingency(tab, correction=False)[3]
enc_all = t3[t3['encerrado'].astype(bool)]
tab = pd.crosstab(enc_all['tipo_desfecho'].cat.remove_unused_categories(), enc_all['grupo']); rep['χ² sentença (com Decisão) × grupo (E21)'] = stats.chi2_contingency(tab, correction=False)[1]
ativos = t3.loc[t3['tipo_desfecho'] == 'Ativo', 'tempo_f']; encs = enc_all['tempo_f']
rep['Mann-Whitney Encerrado × Ativo (E18)'] = stats.mannwhitneyu(encs, ativos)[1]
x_enc = int(t3['encerrado'].sum())
z = (x_enc / len(t3) - 0.5) / np.sqrt(0.25 / len(t3)); rep['z de proporção p0 = 0,5 (E23)'] = 2 * stats.norm.sf(abs(z))
com_all = t3.loc[t3['acordo_ac'] == True, 'tempo_f']; sem_all = t3.loc[t3['acordo_ac'] != True, 'tempo_f']
rep['Mann-Whitney com × sem acordo na AC, todos (E24)'] = stats.mannwhitneyu(com_all, sem_all)[1]
rep['Kruskal-Wallis todos, censura ignorada (E17)'] = versoes['1. Professor: todos, censura ignorada'][1]
t3_rep = pd.DataFrame({'Teste reproduzido': rep.keys(), 'p': rep.values()})
tst_tabela_p(t3_rep, 'tst_professor', 'Testes do notebook do professor reproduzidos na base primária (crítica, não achados)',
             '3.6.1', destaque=None)
print('Esperadas da coluna "acordo na AC" no χ² com o Controle (E20):', [fmt_br(v, 1) for v in e20[:, 1]])
print(f'Encerrados: {x_enc}/{len(t3)} = {pct_br(x_enc / len(t3))} (z = {fmt_br(z, 1)})')

fig, ax = plt.subplots(figsize=(11.5, 4.8))
lp = -np.log10(np.clip(t3_rep['p'].to_numpy(dtype=float), 1e-300, 1))
rot = [t.replace(' (E', '\n(E') for t in t3_rep['Teste reproduzido']]
barras_verticais(ax, rot, lp, cores=CINZA, rotular=False, quebrar=18, ylabel='Significância: −log₁₀(p)', ymax=lp.max() * 1.15)
for i, (v, p_) in enumerate(zip(lp, t3_rep['p'])):
    ax.annotate(f'p {tst_eq(p_)}', (i, v), xytext=(0, 3), textcoords='offset points', ha='center', va='bottom', fontsize=8)
ax.axhline(-np.log10(0.05), color=DESTAQUE, lw=1)
ax.annotate('p = 0,05', (len(lp) - 0.55, -np.log10(0.05)), xytext=(0, 3), textcoords='offset points', ha='right',
            fontsize=8.5, color=DESTAQUE)
ax.tick_params(axis='x', labelsize=8)
figura(fig, 'tst_professor', 'Testes do professor reproduzidos: "significância" sem sentido substantivo', secao='3.6.1',
       nota='quanto mais alta a barra, menor o valor-p. Valores-p minúsculos aqui refletem tautologias, zeros estruturais ou '
            'censura ignorada (códigos E entre parênteses), não efeitos do rito.')
''')

md(r'''
### 3.6.2 Quadro de decisão

| Cél. | Teste do professor | Resultado original | Problema (código) | Decisão aqui | Onde |
|---|---|---|---|---|---|
| 28 | Kruskal-Wallis da duração × grupo, todos | H = 1,48; p = 0,478 | censurados como completos; "Decisão" como sentença; H₀ como "medianas" (E14, E17) | **Substituído** por log-rank/Cox; KW só condicional aos sentenciados ou em min(T, 65) | 3.4; Parte IV |
| 28 | Mann-Whitney post-hoc sem correção | (não executado: p > 0,05) | sem ajuste de multiplicidade (E17, E27) | **Substituído** por Dunn com Holm; MW com delta de Cliff | 3.4 |
| 29 | Mann-Whitney Encerrado × Ativo | p = 3,2 × 10⁻²⁴ | tautológico (E18) | **Removido** | 3.1 |
| 32 | χ² grupo × status | p = 0,00015 | status depende do mês de entrada (E19) | **Substituído** pela situação no 65º dia e por KM | 3.2.5; Parte IV |
| 33 | χ² grupo × acordo na AC | p = 0,0074 | zero estrutural no Controle; esperadas ~5 (E20) | **Substituído** por Fisher Presencial × Remota entre AC realizadas | 3.3.1 |
| 34 | χ² tipo de sentença × grupo | p = 2,0 × 10⁻⁶ | inclui Decisão; sem resíduos nem V; % no sentido errado (E21) | **Adequado na ideia, refeito**: sem Decisão, resíduos, V com IC, pares com Holm | 3.2 |
| 37–38 | Matriz de Spearman das 4 durações; OLS das dispersões | r = 1; R² = 1 | mesma variável (E6, E16) | **Removido**; Spearman/Kendall ordem × tempo com controle da censura | 3.5.2 |
| 40 | Shapiro-Wilk e D'Agostino (subamostra de 500) | p = 2,6 × 10⁻⁸ / 0,213 | subamostra arbitrária, variável censurada, decisão *a posteriori* (E22) | **Refeito** por grupo na Parte II; aqui, nos resíduos da ANOVA didática | Parte II; 3.4.4 |
| 42 | z de proporção (p₀ = 0,5) | z = 17,1 | hipótese sem sentido (E23) | **Removido** | 3.1 |
| 42 | Mann-Whitney com × sem acordo na AC | p = 0,456 | "sem acordo" inclui o Controle e os ativos (E24) | **Refeito** entre AC realizadas e sentenciadas (condicional); correto: riscos competitivos | 3.4.6; Parte IV |
| 44 | Ajuste MLE de distribuições | Weibull melhor AIC | censura ignorada; `loc` livre; zeros descartados (E25) | **Substituído** por ajuste com censura | Partes II e IV |
| 46 | OLS duração ~ grupo; Logit evento ~ grupo | p = 0,588; p < 0,001 | censura; evento depende do seguimento (E26) | **Substituído** por Cox/AFT e logit em horizonte fixo | Partes IV e V |
| 48 | KM + log-rank | não executou | import errado (E1) | **Feito** | Parte IV |
| — | correção de multiplicidade, tamanhos de efeito | ausentes | E27 | **Holm/BH**, V, OR, ε², delta de Cliff, ρ, τ | 3.7 |

### 3.6.3 Outros testes que poderiam ser aplicados (SIEGEL; CASTELLAN, 2006; BARBETTA; REIS; BORNIA, 2020; BECKER, 2015)

| Teste | Para quê, neste caso | Situação |
|---|---|---|
| **Cochran-Mantel-Haenszel** (+ Breslow-Day) | acordo × grupo ajustado pelo mês (estratos) | **implementado abaixo** |
| **Permutação / Monte Carlo** | tabelas esparsas (técnica, redistribuição), sequência do sorteio | implementado (3.2.4, 3.3, 3.5.1) |
| **Exato de Fisher / Fisher-Freeman-Halton** | acordo na AC (17 eventos) | implementado (3.3) |
| **Jonckheere-Terpstra** | tendência ordenada do tempo (condicional) ao longo dos **meses** | possível; não se aplica ao grupo (nominal) |
| **Cochran-Armitage** | tendência da proporção de acordo/sem mérito ao longo dos meses (curva de aprendizado do rito) | possível, mas exige horizonte fixo por causa do seguimento decrescente |
| **Kolmogorov-Smirnov para 2 amostras** | diferença de forma (não só de posição) das distribuições do tempo | possível; mesmo problema de censura |
| **Brunner-Munzel** | alternativa ao Mann-Whitney sem supor formas iguais | possível |
| **Log-rank, Wilcoxon-Gehan, Peto, Fleming-Harrington; Gray** | tempos censurados; riscos competitivos | Parte IV |
| **McNemar, Wilcoxon pareado, Friedman, Cochran Q** | amostras dependentes | **não se aplicam** (grupos independentes, questão 2.3) |

### 3.6.4 Cochran-Mantel-Haenszel: acordo × grupo estratificado por mês (H12)

O mês de distribuição está associado à composição dos grupos (3.5.3) e ao acompanhamento. O CMH combina as tabelas 2 × 2 de cada mês num **OR comum** de Mantel-Haenszel e testa **H₀: OR comum = 1**; o teste de **Breslow-Day** (Tarone) verifica se o OR é homogêneo entre os meses. O desfecho é o **acordo homologado até o 120º dia**, entre os processos com pelo menos 120 dias de acompanhamento (o mesmo da H5, sem censura); cada braço com AC é comparado ao Controle. Os estratos são os meses de janeiro a junho, porque nenhum processo de julho ou agosto tem 120 dias de seguimento. A versão condicional (acordo entre os encerrados, todos os meses) é impressa só para comparação e não entra no registro. O gráfico mostra o OR de cada mês (com correção de Haldane, +0,5, só para desenhar meses com zero) e o OR combinado.
''')

code(r'''
def tst_tabelas_mes(base, y, g):
    """Tabelas 2 × 2 (braço g × Controle; acordo × não) de cada mês presente na base."""
    saida = []
    for m in [m for m in ordem_mes if (base['mes7'] == m).any()]:
        sm_, ym = base[base['mes7'] == m], y[base['mes7'] == m]
        t = np.array([[((sm_['grupo'] == g) & ym).sum(), ((sm_['grupo'] == g) & ~ym).sum()],
                      [((sm_['grupo'] == 'Controle') & ym).sum(), ((sm_['grupo'] == 'Controle') & ~ym).sum()]])
        saida.append((m, t))
    return saida

# versão condicional (só para comparação): acordo entre os encerrados com o registro, todos os meses
_bc = t3[t3['acordo'].notna()]
for g in ['Presencial', 'Remota']:
    _st = StratifiedTable([t for _, t in tst_tabelas_mes(_bc, _bc['acordo'].astype(bool), g)])
    print(f'Versão condicional (encerrados), {g} × Controle: OR MH = {fmt_br(_st.oddsratio_pooled, 2)}, '
          f'p {tst_eq(_st.test_null_odds(correction=False).pvalue)} (não entra no registro)')

base_cmh = t3[t3['followup'] >= 120].copy()
y_cmh = (base_cmh['tipo_desfecho'] == 'Homologação') & (base_cmh['tempo_f'] <= 120)
linhas, forest = [], {}
for g in ['Presencial', 'Remota']:
    tabelas, ors = [], []
    for m, t in tst_tabelas_mes(base_cmh, y_cmh, g):
        tabelas.append(t)
        a, b, c, d = t.ravel() + 0.5
        lor, se = np.log(a * d / (b * c)), np.sqrt(1 / a + 1 / b + 1 / c + 1 / d)
        ors.append((m, np.exp(lor), np.exp(lor - 1.96 * se), np.exp(lor + 1.96 * se), int(t.sum())))
    st = StratifiedTable(tabelas)
    teste = st.test_null_odds(correction=False)
    bd = st.test_equal_odds(adjust=True)
    lo, hi = st.oddsratio_pooled_confint()
    bruto = np.sum(tabelas, axis=0)
    p_bruto, or_bruto, _, _, _ = tst_fisher(bruto)
    linhas.append({'Comparação': f'{g} × Controle', 'OR bruto': or_bruto, 'p bruto (Fisher)': p_bruto,
                   'OR MH': st.oddsratio_pooled, 'OR MH IC': f'{fmt_br(lo, 2)} a {fmt_br(hi, 2)}',
                   'CMH χ²': teste.statistic, 'p': teste.pvalue, 'Breslow-Day p': bd.pvalue})
    forest[g] = (ors, st.oddsratio_pooled, lo, hi)
t3_cmh = pd.DataFrame(linhas); t3_cmh['p Holm'] = tst_holm(t3_cmh['p'])
tst_tabela_p(t3_cmh, 'tst_cmh', 'Cochran-Mantel-Haenszel: acordo até o 120º dia × grupo, estratificado pelo mês de distribuição', '3.6.4', casas=2,
             colunas_p=('p', 'p Holm', 'p bruto (Fisher)', 'Breslow-Day p'),
             nota='OR MH = razão de chances comum de Mantel-Haenszel; Breslow-Day (Tarone) testa a homogeneidade do OR entre os meses.')
for _, r in t3_cmh.iterrows():
    tst_registra('3.6', 'H12 CMH', f'CMH acordo até 120 d × grupo por mês: {r["Comparação"]}', 'OR comum = 1', f'χ²(1) = {fmt_br(r["CMH χ²"], 2)}',
                 r['p'], f'OR MH = {fmt_br(r["OR MH"], 2)} [{r["OR MH IC"].replace(" a ", "; ")}]')

fig, ax = plt.subplots(1, 2, figsize=(13.5, 4.8), sharey=True)
for k, g in enumerate(['Presencial', 'Remota']):
    ors, orp, lo, hi = forest[g]
    for i, (m, o, l, h, nn) in enumerate(ors):
        ax[k].errorbar(i, o, yerr=[[o - l], [h - o]], fmt='o', color=CORES_GRUPO[g], capsize=4, ms=6)
    ax[k].errorbar(len(ors) + 0.6, orp, yerr=[[orp - lo], [hi - orp]], fmt='D', color=TINTA, capsize=6, ms=8)
    ax[k].annotate(f'OR MH = {fmt_br(orp, 2)}', (len(ors) + 0.6, hi), xytext=(0, 4), textcoords='offset points',
                   ha='center', va='bottom', fontsize=8.5)
    ax[k].axhline(1, color=TINTA_2, lw=1)
    ax[k].set_yscale('log')
    ax[k].yaxis.set_major_locator(mpl.ticker.FixedLocator([0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50]))
    ax[k].yaxis.set_major_formatter(FuncFormatter(lambda v, _: fmt_br(v, 2 if v < 0.1 else (1 if v < 1 else 0))))
    ax[k].yaxis.set_minor_formatter(mpl.ticker.NullFormatter())
    ax[k].set_xticks(list(range(len(ors))) + [len(ors) + 0.6],
                     [f'{o[0]}\n(n = {o[4]})' for o in ors] + ['Combinado\n(MH)'], fontsize=8)
    ax[k].set_xlabel(ROTULOS['mes_distribuicao'])
    ax[k].grid(axis='x', visible=False)
    ax[k].set_title(f'{g} × Controle')
    r = t3_cmh.loc[k]
    anotar_teste(ax[k], texto_teste('Cochran-Mantel-Haenszel', f'χ²(1) = {fmt_br(r["CMH χ²"], 2)}', r['p'],
                                    f'Breslow-Day p {tst_eq(r["Breslow-Day p"])}'), loc='upper left', tamanho=8)
ax[0].set_ylabel('Razão de chances de acordo até 120 d (escala log)')
figura(fig, 'tst_cmh', 'O efeito do rito sobre o acordo até o 120º dia resiste ao ajuste pelo mês de distribuição?', secao='3.6.4',
       nota='OR de cada mês com correção de Haldane (+0,5), só para desenhar meses com zero; losango = OR comum de Mantel-Haenszel '
            'com IC 95%. OR > 1: mais acordos no braço com AC do que no Controle.')
''')

interp('tst_professor')

# =====================================================================
md(r'''
---

## 3.7 Multiplicidade: todos os valores-p da Parte III

Cada família já foi corrigida por Holm nas seções anteriores. Aqui, os testes registrados são reunidos e corrigidos de uma vez:

- **Holm global** controla a probabilidade de ao menos um falso positivo entre todos os testes inferenciais da parte (FWER), o critério mais exigente;
- **Benjamini-Hochberg** controla a proporção esperada de falsos positivos entre os testes declarados significativos (FDR), o critério usual em análises exploratórias com muitos testes.

**Três naturezas de teste** (seção 3.1.3):

- **principal:** sem censura (os 938 processos, ou uma janela fixa com seguimento completo), ou sobre o desenho e o sorteio;
- **condicional:** só entre os sentenciados (depende da data de corte) ou estratificado por variável pós-sorteio. Entra na correção, mas **não sustenta sozinho** uma conclusão: precisa de uma versão principal que concorde;
- **didático:** contrastes e artefatos exibidos para crítica (ANOVA de Welch, Spearman com a censura ignorada ou só entre os sentenciados). **Não entra** na correção global.

**Porteiro.** Um par só é lido quando o teste global da sua família também sobrevive ao mesmo critério. Se o global não sobrevive, o par é **exploratório**, ainda que o próprio p ajustado do par fique abaixo de 0,05.

Leitura do gráfico: cada barra é um teste inferencial; a altura é −log₁₀ do p ajustado. As barras acima da linha horizontal são significativas a 5% após a correção, e o prefixo [C] marca os testes condicionais.
''')

code(r'''
t3_reg = pd.DataFrame(TST_REGISTRO)
inf = t3_reg['Natureza'] != 'didático'
t3_reg['p Holm global'] = np.nan
t3_reg['p BH (FDR)'] = np.nan
t3_reg.loc[inf, 'p Holm global'] = multipletests(t3_reg.loc[inf, 'p'], method='holm')[1]
t3_reg.loc[inf, 'p BH (FDR)'] = multipletests(t3_reg.loc[inf, 'p'], method='fdr_bh')[1]
t3_reg['Holm < 0,05'] = np.where(t3_reg['p Holm global'] < 0.05, 'sim', '')
t3_reg['BH < 0,05'] = np.where(t3_reg['p BH (FDR)'] < 0.05, 'sim', '')
n_inf = int(inf.sum())
n_holm, n_bh = int((t3_reg['p Holm global'] < 0.05).sum()), int((t3_reg['p BH (FDR)'] < 0.05).sum())
print(f'{len(t3_reg)} testes registrados: {n_inf} inferenciais ({int((t3_reg["Natureza"] == "principal").sum())} principais, '
      f'{int((t3_reg["Natureza"] == "condicional").sum())} condicionais) e {len(t3_reg) - n_inf} didáticos (fora da correção)')
print(f'Inferenciais significativos: brutos {int((t3_reg.loc[inf, "p"] < 0.05).sum())}, Holm global {n_holm}, BH {n_bh}')
for nat in ['principal', 'condicional']:
    m = t3_reg['Natureza'] == nat
    print(f'  {nat}: Holm global {int((t3_reg.loc[m, "p Holm global"] < 0.05).sum())} de {int(m.sum())}; '
          f'BH {int((t3_reg.loc[m, "p BH (FDR)"] < 0.05).sum())}')
# porteiro: pares cujo global (mesma pergunta) não sobrevive ao BH
_glob = {'H5 pares': 'H5 acordo total', 'H6 pares': 'H6 acordo fora', 'H1 pares': 'H1 tipo × grupo', 'H2 pares (Fisher)': 'H2 tipos binários'}
for fam_par, fam_glob in _glob.items():
    pares_bh = t3_reg[(t3_reg['Família'] == fam_par) & (t3_reg['p BH (FDR)'] < 0.05)]
    for _, r in pares_bh.iterrows():
        print(f'  porteiro: "{r["Teste"]}" (BH {fmt_p(r["p BH (FDR)"])}) — globais da família {fam_glob}: BH '
              + ', '.join(fmt_p(v) for v in t3_reg.loc[t3_reg['Família'] == fam_glob, 'p BH (FDR)']))
tst_tabela_p(t3_reg, 'tst_registro', 'Todos os testes da Parte III: valores-p brutos, Holm global (FWER) e Benjamini-Hochberg (FDR)',
             '3.7', colunas_p=('p', 'p Holm global', 'p BH (FDR)'), destaque='p Holm global',
             nota='linhas destacadas: significativas a 5% após o Holm global. Os testes didáticos não entram na correção (p ajustado em branco).')
t3_reg.to_csv(PROC / 'ed2_parte3_testes.csv', sep=';', decimal=',', index=False, encoding='utf-8-sig')

ordem_plot = t3_reg[inf].sort_values('p').reset_index(drop=True)
fig, ax = plt.subplots(figsize=(17, 6.6))
xx = np.arange(len(ordem_plot)); w = 0.4
lp = lambda s: -np.log10(np.clip(s.astype(float), 1e-16, 1))
ax.bar(xx - w / 2, lp(ordem_plot['p Holm global']), w, color='#2B3A4A', label='Holm global (FWER)')
ax.bar(xx + w / 2, lp(ordem_plot['p BH (FDR)']), w, color='#A9B8C6', label='Benjamini-Hochberg (FDR)')
ax.scatter(xx, lp(ordem_plot['p']), color=DESTAQUE, s=14, zorder=3, label='p bruto', marker='_', lw=2)
ax.axhline(-np.log10(0.05), color=TINTA, lw=1)
ax.annotate('p = 0,05', (len(xx) - 0.5, -np.log10(0.05)), xytext=(0, 3), textcoords='offset points', ha='right', fontsize=8.5)
rot_plot = [('[C] ' if n == 'condicional' else '') + t for t, n in zip(ordem_plot['Teste'], ordem_plot['Natureza'])]
ax.set_xticks(xx, [t if len(t) <= 50 else t[:48] + '…' for t in rot_plot], rotation=70, ha='right', fontsize=6.5)
ax.set_xlim(-0.8, len(xx) - 0.2)
ax.grid(axis='x', visible=False)
ax.set_ylabel('Significância: −log₁₀(p)' + (' (p < 10⁻¹⁶ truncado)' if (ordem_plot['p'] < 1e-16).any() else ''))
ax.legend(loc='upper right')
figura(fig, 'tst_multiplicidade', f'{n_holm} dos {n_inf} testes inferenciais da Parte III sobrevivem ao Holm global ({n_bh} ao Benjamini-Hochberg)',
       secao='3.7', nota='testes em ordem crescente de p bruto; barras acima da linha horizontal são significativas a 5% após a correção; '
                         '[C] = condicional (só sentenciados ou estrato pós-sorteio). Testes didáticos fora do gráfico e da correção.')
''')

interp('tst_multiplicidade')
