# Seções 10 a 14 — Exercícios 1 a 5 propostos pelo professor (estcaso_ip.ipynb), resolvidos com os desafios.
# Trecho incluído por build_rafaelcc_ed1.py (usa md, code e interp de lá).

md(r'''
---

# PARTE I-B — A ANÁLISE EXPLORATÓRIA PROPOSTA PELO PROFESSOR

As seções 10 a 14 seguem o roteiro do notebook da disciplina (`estcaso_ip.ipynb`): as funções do professor, aprimoradas, e os Exercícios 1 a 5 resolvidos, com os desafios. Elas usam o dataset já curado na Parte I. A variável de tempo usada aqui, `Tempo_conclusao_ip`, é a do enunciado; a Parte II mostra o que ela realmente mede e define o desfecho com mais rigor.
''')

# =====================================================================
md(r'''
---

## 10. Análise de Variáveis Categóricas (Exercício 1)

### Objetivo
Gráficos de barras/colunas para cada variável categórica (nominal ou ordinal), com contagem acima de cada barra, proporção (%) e tabela de frequências.

### Função auxiliar — com o desafio de Pareto resolvido

A função do professor foi estendida:

- **`pareto='sim'`** (com `decresc='sim'`) acrescenta a curva de frequência relativa acumulada no eixo direito e marca o ponto de corte de 80%. As barras que compõem os primeiros 80% ficam em cor cheia e as demais em tom claro. O eixo esquerdo vai de 0 a *n* e o direito de 0 a 100%: são **a mesma escala** (contagem e percentual do total), de modo que a curva e as barras são diretamente comparáveis — não é um gráfico de dois eixos com escalas independentes;
- `decresc='não'` respeita a ordem das categorias do dtype (essencial para variáveis ordinais como `Faixa_tempo_ip`);
- booleanos recebem rótulos legíveis apenas na exibição; rótulos longos são quebrados em linhas;
- a tabela de frequências (antes comentada) agora é exibida, com a frequência acumulada.
''')

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


def grafico_barras_completo(dados, variavel, decresc='não', titulo=None, rotacao=0, pareto='não', largura_rotulo=16):
    """
    Gráfico de barras com contagens, proporções e tabela de frequências.

    - decresc: 'sim' ordena por frequência decrescente; 'não' mantém a ordem das categorias
    - pareto: 'sim' (exige decresc='sim') adiciona a curva acumulada e o corte de 80%
    """
    serie = serie_exibicao(dados, variavel)
    freq = serie.value_counts(sort=False)
    if decresc.lower() == 'sim':
        freq = freq.sort_values(ascending=False, kind='stable')
    n = int(freq.sum())
    prop = 100 * freq / n
    acumulada = prop.cumsum()
    usar_pareto = pareto.lower() == 'sim' and decresc.lower() == 'sim'

    k = len(freq)
    fig, ax = plt.subplots(figsize=(max(7, 1.05 * k + 3), 5.2))
    posicoes = np.arange(k)
    if usar_pareto:
        corte = int(np.argmax(acumulada.values >= 80)) + 1  # nº de categorias até atingir 80%
        cores = [COR_PRINCIPAL if i < corte else COR_SECUNDARIA for i in range(k)]
    else:
        cores = COR_PRINCIPAL
    barras = ax.bar(posicoes, freq.values, color=cores, width=0.72, edgecolor='white', linewidth=2)

    topo = n if usar_pareto else freq.max()
    for barra, contagem, pct in zip(barras, freq.values, prop.values):
        x = barra.get_x() + barra.get_width() / 2
        ax.text(x, barra.get_height() + topo * 0.012, f'{contagem}', ha='center', va='bottom',
                fontsize=10, fontweight='bold', color=TINTA)
        if barra.get_height() >= topo * 0.09:
            ax.text(x, barra.get_height() / 2, f'{pct:.1f}%', ha='center', va='center', fontsize=9, color='white',
                    fontweight='bold')
        else:
            ax.text(x, barra.get_height() + topo * 0.075, f'{pct:.1f}%', ha='center', va='bottom', fontsize=8.5,
                    color=TINTA_2)

    ax.set_xticks(posicoes)
    ax.set_xticklabels([quebrar(c, largura_rotulo) for c in freq.index], rotation=rotacao,
                       ha='right' if rotacao else 'center')
    ax.set_ylabel('Frequência (nº de inquéritos)')
    ax.set_xlabel(variavel)
    ax.set_title(titulo or f'Distribuição de {variavel}', pad=14)
    ax.grid(axis='x', visible=False)

    if usar_pareto:
        ax.set_ylim(0, n * 1.08)
        ax2 = ax.twinx()
        ax2.set_ylim(0, 108)  # mesma escala do eixo esquerdo: n ↔ 100%
        ax2.plot(posicoes, acumulada.values, color=COR_DESTAQUE, marker='o', markersize=6, linewidth=2)
        ax2.axhline(80, color=TINTA_2, linestyle='--', linewidth=1)
        ax2.axvline(corte - 1, color=TINTA_2, linestyle=':', linewidth=1)
        ax2.annotate(f'80% atingidos com {corte} de {k} categorias ({acumulada.iloc[corte - 1]:.1f}%)',
                     xy=(corte - 1, acumulada.iloc[corte - 1]), xytext=(8, -26), textcoords='offset points',
                     fontsize=9, color=TINTA)
        ax2.yaxis.set_major_formatter(mtick.PercentFormatter())
        ax2.set_ylabel('Frequência relativa acumulada')
        ax2.grid(False)
        ax2.spines['right'].set_visible(True)
    else:
        ax.set_ylim(0, freq.max() * 1.18)

    plt.tight_layout()
    plt.show()

    tabela = pd.DataFrame({'Contagem': freq.values, 'Proporção (%)': prop.values.round(2),
                           'Acumulada (%)': acumulada.values.round(2)}, index=freq.index.astype(str))
    tabela.index.name = variavel
    ausentes = int(serie.isna().sum())
    display(tabela)
    print(f'Total de observações: {n}' + (f'  |  ausentes: {ausentes}' if ausentes else ''))
    return tabela
''')

md(r'''
### Exercício 1: gráficos de barras para cada variável categórica

As variáveis analisadas são as de uso "Categórica" no esquema (`Validacao` e `Lei_codigo_penal` são constantes e ficam de fora). Variáveis nominais com muitas classes usam ordem decrescente com Pareto; as ordinais e as dicotômicas mantêm a ordem natural. Começamos pela comarca, com o diagrama de Pareto pedido no desafio.
''')

code(r'''
tab_comarca = grafico_barras_completo(dados, 'Comarca', decresc='sim', pareto='sim')
''')

interp('ex1_comarca')

code(r'''
VARS_CATEGORICAS = ESQUEMA.loc[ESQUEMA['Uso analítico'].eq('Categórica'), 'Variável'].tolist()
print(f'{len(VARS_CATEGORICAS)} variáveis categóricas analisadas:', ', '.join(VARS_CATEGORICAS))

CONFIG_BARRAS = {  # variável: parâmetros específicos
    'Delegacia_top6': dict(decresc='sim', pareto='sim', largura_rotulo=14),
    'Tipo_delegacia': dict(decresc='sim', pareto='sim', largura_rotulo=18),
    'Assunto_resumido': dict(decresc='sim', pareto='sim', largura_rotulo=14),
    'Artigo_principal': dict(decresc='sim', largura_rotulo=18),
    'Desfecho': dict(decresc='sim', pareto='sim', rotacao=35, largura_rotulo=22),
}
tabelas_frequencia = {'Comarca': tab_comarca}
for variavel in VARS_CATEGORICAS:
    if variavel == 'Comarca':
        continue
    tabelas_frequencia[variavel] = grafico_barras_completo(dados, variavel, **CONFIG_BARRAS.get(variavel, {}))
''')

md(r'''
O status processual detalhado (15 classes) e a delegacia (36 unidades) são exibidos à parte, em barras horizontais, porque os rótulos são longos demais para o eixo horizontal.
''')

code(r'''
def barras_horizontais(dados, variavel, titulo=None, largura_rotulo=48):
    serie = serie_exibicao(dados, variavel)
    freq = serie.value_counts().sort_values()
    n = int(freq.sum())
    fig, ax = plt.subplots(figsize=(10, 0.32 * len(freq) + 1.4))
    ax.barh([quebrar(c, largura_rotulo) for c in freq.index], freq.values, color=COR_PRINCIPAL, height=0.72,
            edgecolor='white', linewidth=1.5)
    for y, contagem in enumerate(freq.values):
        ax.text(contagem + freq.max() * 0.01, y, f'{contagem} ({100 * contagem / n:.1f}%)', va='center',
                fontsize=8.5, color=TINTA)
    ax.set_xlim(0, freq.max() * 1.2)
    ax.set_xlabel('Frequência (nº de inquéritos)')
    ax.set_title(titulo or f'Distribuição de {variavel}')
    ax.grid(axis='y', visible=False)
    ax.tick_params(axis='y', labelsize=8.5)
    plt.tight_layout()
    plt.show()


barras_horizontais(dados, 'Status_projudi', 'Status processual detalhado (15 classes)')
barras_horizontais(dados, 'Nome_delegacia', 'Delegacia responsável (nomes canônicos)')
''')

md(r'''
**Campo multirresposta.** Nas diligências, a pergunta certa não é "qual a categoria do caso" (um caso pode ter várias), mas "em quantos casos com manifestação do MP aparece cada tipo de diligência". Por isso as porcentagens abaixo somam mais de 100%.
''')

code(r'''
casos_com_manifestacao = int(dados['Houve_manifestacao_mp'].sum())
freq_dil = dados[list(COLUNA_DILIGENCIA.values())].sum().rename(index={v: k for k, v in COLUNA_DILIGENCIA.items()})
freq_dil = freq_dil.sort_values()
fig, ax = plt.subplots(figsize=(10, 4.6))
ax.barh([quebrar(c, 40) for c in freq_dil.index], freq_dil.values, color=COR_PRINCIPAL, height=0.7)
for y, v in enumerate(freq_dil.values):
    ax.text(v + 1, y, f'{v} ({100 * v / casos_com_manifestacao:.0f}%)', va='center', fontsize=9)
ax.set_xlim(0, freq_dil.max() * 1.22)
ax.set_xlabel(f'Inquéritos com a diligência (base: {casos_com_manifestacao} com manifestação do MP)')
ax.set_title('Tipos de diligência requisitados pelo MP (multirresposta)')
ax.grid(axis='y', visible=False)
plt.tight_layout()
plt.show()
''')

code(r'''
perfil_categorico = pd.DataFrame([
    {'Variável': v, 'Níveis': len(t), 'Categoria modal': t['Contagem'].idxmax(),
     'Casos na moda': int(t['Contagem'].max()), '% da moda': round(t['Proporção (%)'].max(), 1),
     'Categorias raras (< 5%)': int((t['Proporção (%)'] < 5).sum())}
    for v, t in tabelas_frequencia.items()
]).set_index('Variável')
print('PERFIL CATEGÓRICO — resumo do Exercício 1')
display(perfil_categorico)
''')

interp('ex1_geral')

# =====================================================================
md(r'''
---

## 11. Análise de Variáveis Quantitativas (Exercício 2)

### Objetivo
Dot plot, histograma e boxplot para cada variável quantitativa, sempre com a unidade de medida.

### Função auxiliar (aprimorada)

- O **dot plot** empilha os pontos de valores iguais (ou do mesmo intervalo, quando há muitos valores distintos), como no dot plot clássico de Moore — na versão original todos os pontos ficavam na mesma linha e se sobrepunham;
- o histograma de variáveis discretas com poucos valores usa um intervalo por inteiro;
- as estatísticas incluem o coeficiente de variação (CV = dp/média), assimetria, curtose e o número de outliers pela regra de 1,5×IQR.
''')

code(r'''
UNIDADES = ESQUEMA.set_index('Variável')['Unidade'].to_dict()


def resumo_quantitativo(serie):
    serie = serie.dropna().astype(float)
    q1, q3 = serie.quantile([0.25, 0.75])
    iqr = q3 - q1
    return pd.Series({
        'N (obs.)': len(serie), 'Média': serie.mean(), 'Mediana': serie.median(), 'Desvio padrão': serie.std(),
        'CV (%)': 100 * serie.std() / serie.mean() if serie.mean() else np.nan,
        'Mínimo': serie.min(), 'Q1 (25%)': q1, 'Q3 (75%)': q3, 'Máximo': serie.max(), 'IQR': iqr,
        'Assimetria': serie.skew(), 'Curtose': serie.kurt(),
        'Outliers (1,5×IQR)': int(((serie < q1 - 1.5 * iqr) | (serie > q3 + 1.5 * iqr)).sum()),
    })


def dot_plot(ax, valores, max_colunas=45):
    valores = np.asarray(valores, dtype=float)
    distintos = np.unique(valores)
    if len(distintos) <= max_colunas:
        centros = valores
    else:  # agrupa em intervalos e empilha pelo centro do intervalo
        bordas = np.histogram_bin_edges(valores, bins=max_colunas)
        idx = np.clip(np.digitize(valores, bordas) - 1, 0, len(bordas) - 2)
        centros = (bordas[idx] + bordas[idx + 1]) / 2
    ordem = np.argsort(centros, kind='stable')
    centros = centros[ordem]
    alturas = np.zeros_like(centros)
    for v in np.unique(centros):
        m = centros == v
        alturas[m] = np.arange(1, m.sum() + 1)
    ax.scatter(centros, alturas, s=22, color=COR_PRINCIPAL, edgecolor='white', linewidth=0.6, zorder=3)
    ax.set_ylim(0, alturas.max() + 1)
    ax.set_ylabel('Nº de casos')


def analise_var_quantitativa(dados, variavel, unidade='', bins=20):
    """Dot plot, histograma e boxplot (3 × 1) de uma variável quantitativa, com estatísticas descritivas."""
    serie = dados[variavel].dropna().astype(float)
    unidade = unidade or UNIDADES.get(variavel, '')
    rotulo = f'{variavel} ({unidade})' if unidade else variavel
    resumo = resumo_quantitativo(serie)

    fig, axes = plt.subplots(3, 1, figsize=(11, 10), sharex=True, gridspec_kw={'height_ratios': [1.2, 1.2, 0.7]})
    dot_plot(axes[0], serie)
    axes[0].set_title('Dot plot')

    discreta_curta = serie.nunique() <= 25 and (serie % 1 == 0).all()
    bordas = np.arange(serie.min() - 0.5, serie.max() + 1.5) if discreta_curta else bins
    axes[1].hist(serie, bins=bordas, color=COR_PRINCIPAL, edgecolor='white', linewidth=1.2)
    axes[1].axvline(resumo['Média'], color=COR_DESTAQUE, linestyle='--', linewidth=2,
                    label=f"Média = {resumo['Média']:,.1f}")
    axes[1].axvline(resumo['Mediana'], color=TINTA, linestyle='-', linewidth=2,
                    label=f"Mediana = {resumo['Mediana']:,.1f}")
    axes[1].set_ylabel('Frequência')
    axes[1].set_title('Histograma')
    axes[1].legend()

    axes[2].boxplot(serie, orientation='horizontal', widths=0.55, patch_artist=True,
                    boxprops=dict(facecolor=COR_SECUNDARIA, edgecolor=TINTA_2),
                    medianprops=dict(color=TINTA, linewidth=2), whiskerprops=dict(color=TINTA_2),
                    capprops=dict(color=TINTA_2),
                    flierprops=dict(marker='o', markerfacecolor=COR_DESTAQUE, markeredgecolor='white', markersize=7))
    axes[2].plot(resumo['Média'], 1, marker='D', color=COR_DESTAQUE, markeredgecolor='white', markersize=9, zorder=3)
    axes[2].set_yticks([])
    axes[2].set_xlabel(rotulo)
    axes[2].set_title('Boxplot (◆ = média)')
    for ax in axes:
        ax.tick_params(labelbottom=True)
    fig.suptitle(f'Análise de {variavel}', fontsize=13, fontweight='bold')
    plt.tight_layout()
    plt.show()

    ausentes = int(dados[variavel].isna().sum())
    print(f'Estatísticas descritivas: {variavel} [{unidade}]' + (f' — {ausentes} ausentes' if ausentes else ''))
    display(resumo.to_frame(variavel).T.round(2))
    return resumo
''')

md(r'''
### Exercício 2: análise individual de variáveis quantitativas

Começamos pela variável-chave do estudo, o tempo que a polícia levou para concluir o inquérito.
''')

code(r'''
resumo_tempo_ip = analise_var_quantitativa(dados, 'Tempo_conclusao_ip', unidade='dias')
''')

interp('ex2_tempo_ip')

code(r'''
VARS_QUANTITATIVAS = ESQUEMA.loc[ESQUEMA['Uso analítico'].eq('Quantitativa'), 'Variável'].tolist()
print(f'{len(VARS_QUANTITATIVAS)} variáveis quantitativas:', ', '.join(VARS_QUANTITATIVAS))

resumos_quantitativos = {'Tempo_conclusao_ip': resumo_tempo_ip}
for variavel in VARS_QUANTITATIVAS:
    if variavel != 'Tempo_conclusao_ip':
        resumos_quantitativos[variavel] = analise_var_quantitativa(dados, variavel)
''')

code(r'''
tabela_quantitativas = pd.DataFrame(resumos_quantitativos).T
tabela_quantitativas.insert(0, 'Unidade', [UNIDADES[v] for v in tabela_quantitativas.index])
print('RESUMO DAS VARIÁVEIS QUANTITATIVAS (ordenado pelo coeficiente de variação)')
display(tabela_quantitativas.sort_values('CV (%)', ascending=False).round(2))
''')

interp('ex2_geral')

# =====================================================================
md(r'''
---

## 12. Comparação de Variáveis Quantitativas por Grupos (Exercício 3)

### Funções auxiliares — com os dois desafios resolvidos

1. **`comparacao_grupos_boxplot(..., decresc='não')`** — ordena os boxplots pela mediana: `'não'` = ordem crescente (da menor para a maior mediana), `'sim'` = decrescente, `None` = ordem das categorias. Os pontos individuais são sobrepostos com leve deslocamento (*jitter*), o *n* de cada grupo aparece no rótulo, e é feito um teste não paramétrico (Mann-Whitney para 2 grupos, Kruskal-Wallis para 3 ou mais) com tamanho de efeito;
2. **`comparacao_grupos_histograma(..., sobrepostos='não')`** — `'não'` empilha os histogramas verticalmente (k × 1), com o mesmo eixo x e os **mesmos intervalos** para todos os grupos; `'sim'` sobrepõe. A versão original calculava os intervalos separadamente para cada grupo, o que tornava as barras incomparáveis.

A escolha de testes não paramétricos se justifica pela forte assimetria dos tempos (Exercício 2): comparar medianas/postos é mais robusto que comparar médias.
''')

code(r'''
def cores_para(categorias):
    """Cor fixa por categoria, na ordem da paleta (nunca reciclada: > 8 grupos usam a cor principal)."""
    categorias = list(categorias)
    if len(categorias) > len(CORES):
        return {c: COR_PRINCIPAL for c in categorias}
    return dict(zip(categorias, CORES))


def teste_grupos(df, var_q, var_c):
    grupos = [g[var_q].astype(float).values for _, g in df.groupby(var_c, observed=True)]
    n = sum(len(g) for g in grupos)
    if len(grupos) == 2:
        u, p = stats.mannwhitneyu(*grupos, alternative='two-sided')
        efeito = 1 - 2 * u / (len(grupos[0]) * len(grupos[1]))  # correlação rank-bisserial
        return {'Teste': 'Mann-Whitney', 'Estatística': u, 'p-valor': p, 'Efeito': efeito, 'Medida de efeito': 'r bisserial'}
    h, p = stats.kruskal(*grupos)
    epsilon2 = (h - len(grupos) + 1) / (n - len(grupos))
    return {'Teste': 'Kruskal-Wallis', 'Estatística': h, 'p-valor': p, 'Efeito': epsilon2, 'Medida de efeito': 'ε²'}


resultados_grupos = []


def comparacao_grupos_boxplot(dados, var_quantitativa, var_categorica, unidade='', decresc='não', log=False):
    """Boxplots lado a lado ordenados pela mediana (decresc='não' crescente, 'sim' decrescente, None = original)."""
    df = pd.DataFrame({var_quantitativa: dados[var_quantitativa].astype(float),
                       var_categorica: serie_exibicao(dados, var_categorica)}).dropna()
    df[var_categorica] = df[var_categorica].cat.remove_unused_categories()
    medianas = df.groupby(var_categorica, observed=True)[var_quantitativa].median()
    if decresc is None:
        ordem = list(df[var_categorica].cat.categories)
    else:
        ordem = list(medianas.sort_values(ascending=(decresc.lower() == 'não'), kind='stable').index)
    unidade = unidade or UNIDADES.get(var_quantitativa, '')
    cores = cores_para(df[var_categorica].cat.categories)

    fig, ax = plt.subplots(figsize=(max(8, 1.6 * len(ordem) + 3), 6))
    grupos = [df.loc[df[var_categorica] == g, var_quantitativa].values for g in ordem]
    caixas = ax.boxplot(grupos, widths=0.55, patch_artist=True, showfliers=False,
                        medianprops=dict(color=TINTA, linewidth=2), whiskerprops=dict(color=TINTA_2),
                        capprops=dict(color=TINTA_2), boxprops=dict(edgecolor=TINTA_2))
    for caixa, g in zip(caixas['boxes'], ordem):
        caixa.set_facecolor(cores[g])
        caixa.set_alpha(0.35)
    for i, (g, valores) in enumerate(zip(ordem, grupos), start=1):
        ax.scatter(i + RNG.uniform(-0.17, 0.17, len(valores)), valores, s=16, color=cores[g], edgecolor='white',
                   linewidth=0.5, zorder=3)
        ax.plot(i, valores.mean(), marker='D', color=TINTA, markeredgecolor='white', markersize=8, zorder=4)
    ax.set_xticks(range(1, len(ordem) + 1))
    ax.set_xticklabels([f'{quebrar(g, 16)}\n(n={len(v)})' for g, v in zip(ordem, grupos)])
    if log:
        ax.set_yscale('symlog', linthresh=10)
    ax.set_xlabel(var_categorica)
    ax.set_ylabel(f'{var_quantitativa} ({unidade})' if unidade else var_quantitativa)
    sentido = {None: '', 'não': ' — ordem crescente da mediana', 'sim': ' — ordem decrescente da mediana'}
    ax.set_title(f'{var_quantitativa} por {var_categorica}{sentido[decresc]}  (◆ = média)')
    ax.grid(axis='x', visible=False)
    plt.tight_layout()
    plt.show()

    estat = df.groupby(var_categorica, observed=True)[var_quantitativa].apply(resumo_quantitativo).unstack()
    estat = estat.loc[ordem, ['N (obs.)', 'Média', 'Mediana', 'Desvio padrão', 'CV (%)', 'Q1 (25%)', 'Q3 (75%)',
                              'IQR', 'Mínimo', 'Máximo', 'Outliers (1,5×IQR)']]
    teste = teste_grupos(df, var_quantitativa, var_categorica)
    resultados_grupos.append({'Quantitativa': var_quantitativa, 'Grupos': var_categorica, 'k': len(ordem), **teste})
    print(f'Estatísticas de {var_quantitativa} por {var_categorica}')
    display(estat.round(1))
    print(f"{teste['Teste']}: estatística = {teste['Estatística']:.2f}; p-valor = {teste['p-valor']:.4f}; "
          f"{teste['Medida de efeito']} = {teste['Efeito']:.3f}")
    return estat


def comparacao_grupos_histograma(dados, var_quantitativa, var_categorica, unidade='', bins=15, sobrepostos='não'):
    """Histogramas por grupo com intervalos comuns: sobrepostos='não' → k × 1; 'sim' → sobrepostos."""
    df = pd.DataFrame({var_quantitativa: dados[var_quantitativa].astype(float),
                       var_categorica: serie_exibicao(dados, var_categorica)}).dropna()
    df[var_categorica] = df[var_categorica].cat.remove_unused_categories()
    grupos = list(df[var_categorica].cat.categories)
    cores = cores_para(grupos)
    bordas = np.histogram_bin_edges(df[var_quantitativa], bins=bins)
    unidade = unidade or UNIDADES.get(var_quantitativa, '')
    rotulo_x = f'{var_quantitativa} ({unidade})' if unidade else var_quantitativa

    if sobrepostos.lower() == 'sim':
        fig, ax = plt.subplots(figsize=(11, 5.5))
        for g in grupos:
            ax.hist(df.loc[df[var_categorica] == g, var_quantitativa], bins=bordas, alpha=0.45, color=cores[g],
                    edgecolor='white', label=f'{g} (n={int((df[var_categorica] == g).sum())})')
        ax.set_xlabel(rotulo_x)
        ax.set_ylabel('Frequência')
        ax.legend(title=var_categorica)
        ax.set_title(f'Distribuição de {var_quantitativa} por {var_categorica} (sobrepostos)')
    else:
        fig, axes = plt.subplots(len(grupos), 1, figsize=(11, 1.9 * len(grupos) + 1), sharex=True, sharey=True)
        axes = np.atleast_1d(axes)
        for ax, g in zip(axes, grupos):
            valores = df.loc[df[var_categorica] == g, var_quantitativa]
            ax.hist(valores, bins=bordas, color=cores[g], edgecolor='white')
            ax.axvline(valores.median(), color=TINTA, linewidth=2)
            ax.set_title(f'{g}  (n={len(valores)}; mediana = {valores.median():,.0f})', loc='left', fontsize=10)
            ax.set_ylabel('Freq.')
        axes[-1].set_xlabel(rotulo_x)
        fig.suptitle(f'Distribuição de {var_quantitativa} por {var_categorica} ({len(grupos)} × 1, intervalos comuns)',
                     fontsize=12, fontweight='bold')
    plt.tight_layout()
    plt.show()
''')

md(r'''
### Exercício 3: compare variáveis quantitativas entre grupos

**Tempo de conclusão do IP por comarca.** Desafio 1: boxplots em ordem crescente de mediana (`decresc='não'`). O professor antecipa que a ordem vai de Senador Canedo (mediana 394,5 dias) a Anápolis (3.361,5 dias) — a tabela confirma.
''')

code(r'''
estat_comarca = comparacao_grupos_boxplot(dados, 'Tempo_conclusao_ip', 'Comarca', unidade='dias', decresc='não')
assert estat_comarca['Mediana'].iloc[0] == 394.5 and estat_comarca['Mediana'].iloc[-1] == 3361.5
''')

md(r'''
Desafio 2: histogramas não sobrepostos (6 × 1), com os mesmos intervalos para as seis comarcas. Em seguida, a versão sobreposta, para comparação: com seis grupos ela fica ilegível, o que justifica a opção `sobrepostos='não'`.
''')

code(r'''
comparacao_grupos_histograma(dados, 'Tempo_conclusao_ip', 'Comarca', unidade='dias', bins=20, sobrepostos='não')
comparacao_grupos_histograma(dados, 'Tempo_conclusao_ip', 'Comarca', unidade='dias', bins=20, sobrepostos='sim')
''')

interp('ex3_comarca')

md(r'''
**Tempo de conclusão do IP segundo `Reu_preso`** (comparação proposta pelo professor).
''')

code(r'''
comparacao_grupos_boxplot(dados, 'Tempo_conclusao_ip', 'Reu_preso', unidade='dias', decresc='não')
comparacao_grupos_histograma(dados, 'Tempo_conclusao_ip', 'Reu_preso', unidade='dias', bins=20, sobrepostos='não');
''')

interp('ex3_reu_preso')

md(r'''
**Outras comparações.** Forma de instauração, tipo de delegacia e situação processual para o tempo policial; comarca para o tempo do MP e para a quantidade de manifestações.
''')

code(r'''
comparacao_grupos_boxplot(dados, 'Tempo_conclusao_ip', 'Forma_instauracao', unidade='dias')
comparacao_grupos_boxplot(dados, 'Tempo_conclusao_ip', 'Tipo_delegacia', unidade='dias')
comparacao_grupos_boxplot(dados, 'Tempo_conclusao_ip', 'Status_macro', unidade='dias')
comparacao_grupos_boxplot(dados, 'Tempo_conclusao_mp', 'Comarca', unidade='dias', log=True)
comparacao_grupos_boxplot(dados, 'Quantidade_manifestacao_mp', 'Comarca', unidade='manifestações');
''')

code(r'''
tabela_testes_grupos = pd.DataFrame(resultados_grupos).drop_duplicates(['Quantitativa', 'Grupos'])
tabela_testes_grupos['Significativo (5%)'] = tabela_testes_grupos['p-valor'] < 0.05
print('RESUMO DOS TESTES DE COMPARAÇÃO DE GRUPOS')
display(tabela_testes_grupos.round(4))
''')

interp('ex3_geral')

# =====================================================================
md(r'''
---

## 13. Análise de Associações entre Variáveis Categóricas (Exercício 4)

### Objetivo
Gráficos mosaico para explorar associações entre variáveis categóricas e testes de independência.

### Da amostra para a população

Os 218 inquéritos são uma **amostra**; o interesse está na população de inquéritos das seis comarcas. O teste qui-quadrado de independência responde: *se na população as duas variáveis fossem independentes, qual seria a probabilidade de observarmos, em uma amostra deste tamanho, uma discrepância entre frequências observadas e esperadas tão grande quanto a encontrada?*

- **H₀ (hipótese nula):** as variáveis são independentes na população — a distribuição condicional de uma é a mesma em todas as categorias da outra;
- **H₁ (hipótese alternativa):** as variáveis são associadas — ao menos uma distribuição condicional difere.

Rejeita-se H₀ quando p < 0,05. Três cuidados que a função trata automaticamente:

1. **Frequências esperadas pequenas.** A aproximação qui-quadrado exige que no máximo 20% das caselas tenham frequência esperada < 5 e nenhuma < 1. Quando isso falha, o p-valor é obtido por **permutação** (Monte Carlo, 10.000 reamostragens), e em tabelas 2×2 usa-se o **teste exato de Fisher**;
2. **Significância não é força.** O **V de Cramér** (0 = independência, 1 = associação perfeita) mede a intensidade;
3. **Onde está a associação.** Os **resíduos padronizados ajustados** apontam as caselas responsáveis: |r| > 1,96 indica casela com frequência significativamente acima (+) ou abaixo (−) do esperado sob independência.

No mosaico, a cor identifica a categoria da segunda variável (a mesma cor em todas as colunas); alturas diferentes entre colunas indicam associação.
''')

code(r'''
def v_de_cramer(tabela):
    chi2 = stats.chi2_contingency(tabela, correction=False)[0]
    n = tabela.to_numpy().sum()
    return np.sqrt(chi2 / (n * (min(tabela.shape) - 1)))


def qui_quadrado_permutacao(x, y, n_perm=10_000):
    """p-valor do qui-quadrado por permutação de y (preserva as marginais)."""
    xc, yc = pd.factorize(x)[0], pd.factorize(y)[0]
    kx, ky = xc.max() + 1, yc.max() + 1

    def estatistica(yy):
        tabela = np.zeros((kx, ky))
        np.add.at(tabela, (xc, yy), 1)
        esperada = tabela.sum(1, keepdims=True) * tabela.sum(0, keepdims=True) / tabela.sum()
        return ((tabela - esperada) ** 2 / esperada).sum()

    observada = estatistica(yc)
    permutadas = np.array([estatistica(RNG.permutation(yc)) for _ in range(n_perm)])
    return observada, (1 + (permutadas >= observada - 1e-12).sum()) / (n_perm + 1)


resultados_associacao = []


def analise_associacao_categoricas(dados, var1, var2, abreviar=None, n_perm=10_000):
    """
    Mosaico + teste de independência (qui-quadrado assintótico, por permutação ou exato de Fisher),
    V de Cramér e resíduos padronizados ajustados.
    abreviar: dicionário {rótulo longo: abreviatura} aplicado apenas no gráfico.
    """
    abreviar = abreviar or {}
    df = pd.DataFrame({var1: serie_exibicao(dados, var1), var2: serie_exibicao(dados, var2)}).dropna()
    for v in (var1, var2):
        df[v] = df[v].cat.remove_unused_categories()
    tabela = pd.crosstab(df[var1], df[var2])
    n = int(tabela.to_numpy().sum())
    chi2, p_assint, gl, esperada = stats.chi2_contingency(tabela, correction=False)
    esperada = pd.DataFrame(esperada, index=tabela.index, columns=tabela.columns)
    pct_esperada_baixa = 100 * (esperada < 5).to_numpy().mean()
    aproximacao_ok = pct_esperada_baixa <= 20 and (esperada >= 1).to_numpy().all()

    if tabela.shape == (2, 2):
        metodo, p_valor = 'Exato de Fisher', stats.fisher_exact(tabela)[1]
    elif aproximacao_ok:
        metodo, p_valor = 'Qui-quadrado (assintótico)', p_assint
    else:
        metodo, (_, p_valor) = f'Qui-quadrado por permutação ({n_perm:,} reamostragens)', qui_quadrado_permutacao(
            df[var1], df[var2], n_perm)
    v = v_de_cramer(tabela)

    linha = tabela.sum(axis=1).to_numpy()[:, None] / n
    coluna = tabela.sum(axis=0).to_numpy()[None, :] / n
    residuos = (tabela - esperada) / np.sqrt(esperada * (1 - linha) * (1 - coluna))

    # Mosaico: cor = categoria de var2; rótulos só nas caselas com área suficiente
    cores = cores_para(tabela.columns)
    dados_mosaico = {(abreviar.get(str(a), str(a)), abreviar.get(str(b), str(b))): tabela.loc[a, b]
                     for a in tabela.index for b in tabela.columns}
    cor_por_abrev = {abreviar.get(str(b), str(b)): cores[b] for b in tabela.columns}
    fig, ax = plt.subplots(figsize=(12, 6.5))
    mosaic(dados_mosaico, ax=ax, gap=0.012, axes_label=True,
           properties=lambda chave: {'color': cor_por_abrev[chave[1]], 'alpha': 0.85},
           labelizer=lambda chave: (str(dados_mosaico[chave]) if dados_mosaico[chave] / n >= 0.02 else ''))
    ax.set_title(f'Mosaico: {var1} × {var2}', pad=12)
    ax.grid(False)
    plt.setp(ax.get_xticklabels(), rotation=0, fontsize=9)
    plt.tight_layout()
    plt.show()

    print(f'Tabela de contingência: {var1} × {var2}')
    display(pd.crosstab(df[var1], df[var2], margins=True, margins_name='Total'))
    print(f'Distribuição condicional de {var2} dentro de cada {var1} (% na linha)')
    display((100 * pd.crosstab(df[var1], df[var2], normalize='index')).round(1))
    print('Resíduos padronizados ajustados (|r| > 1,96 ⇒ casela se afasta da independência)')
    display(residuos.round(2).style.background_gradient(cmap=MAPA_DIVERGENTE, vmin=-4, vmax=4).format('{:.2f}'))

    print(f'H₀: {var1} e {var2} são independentes na população  |  H₁: são associadas')
    print(f'χ² = {chi2:.3f}; gl = {gl}; caselas com esperada < 5: {pct_esperada_baixa:.0f}%')
    print(f'Método: {metodo}; p-valor = {p_valor:.4f}; V de Cramér = {v:.3f}')
    decisao = 'Rejeita-se H₀: há evidência de associação' if p_valor < 0.05 else 'Não se rejeita H₀: sem evidência de associação'
    print(f'→ {decisao} (α = 5%).')
    resultados_associacao.append({'Variável 1': var1, 'Variável 2': var2, 'n': n, 'Tabela': f'{tabela.shape[0]}×{tabela.shape[1]}',
                                  'χ²': chi2, 'gl': gl, '% esperada < 5': pct_esperada_baixa, 'Método': metodo,
                                  'p-valor': p_valor, 'V de Cramér': v})
    return tabela, residuos
''')

md(r'''
### Exercício 4: explore associações entre variáveis categóricas

**Comarca × Réu preso** (proposta do professor).

*Hipóteses testadas:* H₀ — a proporção de inquéritos com réu preso é a mesma nas seis comarcas; H₁ — ao menos uma comarca tem proporção diferente.
''')

code(r'''
ABREV_COMARCA = {'Goiânia': 'GYN', 'Aparecida de Goiânia': 'APG', 'Anápolis': 'ANA', 'Luziânia': 'LUZ',
                 'Senador Canedo': 'SCA', 'Águas Lindas de Goiás': 'ALG'}
analise_associacao_categoricas(dados, 'Comarca', 'Reu_preso', abreviar=ABREV_COMARCA);
''')

interp('ex4_comarca_reu')

md(r'''
**Assunto × Réu preso** (proposta do professor).

*Hipóteses testadas:* H₀ — a proporção de réus presos é a mesma para todos os tipos de crime; H₁ — ao menos um tipo de crime tem proporção diferente. Com 7 tipos, vários com 1 a 3 casos, a maioria das caselas tem frequência esperada < 5: a função passa automaticamente ao teste por permutação. Em seguida repete-se o teste com `Assunto_grupo` (3 classes), que é o tratamento recomendado no desafio.
''')

code(r'''
ABREV_ASSUNTO = {'Homicídio simples': 'Simples', 'Homicídio qualificado': 'Qualif.', 'Homicídio privilegiado': 'Privil.',
                 'Homicídio (espécie não especificada)': 'N/esp.', 'Feminicídio': 'Femin.', 'Latrocínio': 'Latroc.',
                 'Lesão corporal seguida de morte': 'LC s/ morte'}
analise_associacao_categoricas(dados, 'Assunto_resumido', 'Reu_preso', abreviar=ABREV_ASSUNTO)
analise_associacao_categoricas(dados, 'Assunto_grupo', 'Reu_preso');
''')

interp('ex4_assunto_reu')

md(r'''
### Desafio do Exercício 4

1. **Hipóteses** — enunciadas acima, antes de cada teste;
2. **Tratar variáveis com muitas categorias** — `Desfecho` tem 11 classes, várias com menos de 10 casos;
3. **Dicionário de abreviaturas** — `ABREV_DESFECHO` encurta os rótulos no mosaico;
4. **Top 6 + "Outros"** — `agrupar_top` mantém as 6 categorias mais frequentes e agrupa as demais. A nova variável continua sendo uma partição (verificada).

Associação escolhida: **Comarca × Desfecho** — o modo como os inquéritos terminam depende da comarca?
''')

code(r'''
def agrupar_top(serie, k=6, outros='Outros'):
    """Mantém as k categorias mais frequentes e agrupa as demais em `outros` (resultado: category)."""
    top = serie.value_counts().index[:k].tolist()
    mapa = {c: (c if c in top else outros) for c in serie.dropna().unique()}
    return para_categoria(serie.astype('string'), {str(c): str(v) for c, v in mapa.items()},
                          [str(c) for c in top] + [outros])


ABREV_DESFECHO = {
    'Em investigação': 'Em invest.',
    'Denúncia oferecida': 'Denúncia',
    'Suspenso': 'Suspenso',
    'Arquivado: falta de justa causa': 'Arq. just. causa',
    'Arquivado: pedido deferido (motivo não especificado)': 'Arq. pedido',
    'Arquivado: extinção da punibilidade': 'Arq. ext. pun.',
    'Arquivado: atipicidade': 'Arq. atípico',
    'Arquivado: autoria desconhecida': 'Arq. s/ autoria',
    'Arquivado: litispendência': 'Arq. litisp.',
    'Arquivado: indiciado não denunciado': 'Arq. não denunc.',
    'Arquivado: outros motivos': 'Arq. outros',
    'Outros desfechos': 'Outros',
}
dados['Desfecho_top6'] = agrupar_top(dados['Desfecho'], k=6, outros='Outros desfechos')
display(verificar_particao(dados['Desfecho_top6'], dados['Desfecho']))
display(pd.Series(ABREV_DESFECHO, name='Abreviatura').rename_axis('Rótulo').to_frame())
''')

code(r'''
tab_comarca_desfecho, res_comarca_desfecho = analise_associacao_categoricas(
    dados, 'Comarca', 'Desfecho_top6', abreviar={**ABREV_COMARCA, **ABREV_DESFECHO})
''')

interp('ex4_comarca_desfecho')

md(r'''
**Análise de Correspondência (*Correspondence Analysis Plot*).** Para tabelas maiores que 2×2, a análise de correspondência resume a associação em um mapa: a tabela de resíduos de independência é decomposta por valores singulares (SVD), e comarcas e desfechos são projetados nas duas dimensões que retêm a maior parte da **inércia** (χ²/n). Pontos próximos da origem estão perto do perfil médio; uma comarca próxima de um desfecho tem esse desfecho acima do esperado.
''')

code(r'''
def analise_correspondencia(tabela, abreviar=None, titulo=None):
    abreviar = abreviar or {}
    N = tabela.to_numpy(dtype=float)
    P = N / N.sum()
    r, c = P.sum(1), P.sum(0)
    S = (P - np.outer(r, c)) / np.sqrt(np.outer(r, c))
    U, sv, Vt = np.linalg.svd(S, full_matrices=False)
    inercia = sv ** 2
    linhas = (U * sv) / np.sqrt(r)[:, None]
    colunas = (Vt.T * sv) / np.sqrt(c)[:, None]
    pct = 100 * inercia / inercia.sum()

    fig, ax = plt.subplots(figsize=(10, 7))
    ax.axhline(0, color=GRADE, linewidth=1)
    ax.axvline(0, color=GRADE, linewidth=1)
    ax.scatter(linhas[:, 0], linhas[:, 1], s=90, color=COR_PRINCIPAL, edgecolor='white', zorder=3,
               label=tabela.index.name)
    ax.scatter(colunas[:, 0], colunas[:, 1], s=90, marker='^', color=COR_DESTAQUE, edgecolor='white', zorder=3,
               label=tabela.columns.name)
    for (x, y), nome in zip(linhas[:, :2], tabela.index):
        ax.annotate(abreviar.get(str(nome), str(nome)), (x, y), xytext=(6, 5), textcoords='offset points',
                    color=TINTA, fontsize=10, fontweight='bold')
    for (x, y), nome in zip(colunas[:, :2], tabela.columns):
        ax.annotate(abreviar.get(str(nome), str(nome)), (x, y), xytext=(6, -12), textcoords='offset points',
                    color=TINTA_2, fontsize=9)
    ax.set_xlabel(f'Dimensão 1 ({pct[0]:.1f}% da inércia)')
    ax.set_ylabel(f'Dimensão 2 ({pct[1]:.1f}% da inércia)')
    ax.set_title(titulo or f'Análise de correspondência: {tabela.index.name} × {tabela.columns.name}')
    ax.legend(loc='best')
    plt.tight_layout()
    plt.show()
    print(f'Inércia total = {inercia.sum():.4f} (= χ²/n). Dimensões 1 e 2 retêm {pct[:2].sum():.1f}%.')
    return pd.DataFrame({'Inércia': inercia, '% da inércia': pct, '% acumulado': pct.cumsum()},
                        index=[f'Dim {i + 1}' for i in range(len(sv))]).round(3)


analise_correspondencia(tab_comarca_desfecho, {**ABREV_COMARCA, **ABREV_DESFECHO})
''')

md(r'''
**Outras associações de interesse.** Forma de instauração × réu preso (esperada: o flagrante gera prisão), comarca × arma de fogo, indiciamento × situação processual, e tentativa × réu preso.
''')

code(r'''
analise_associacao_categoricas(dados, 'Forma_instauracao', 'Reu_preso')
analise_associacao_categoricas(dados, 'Comarca', 'Arma_de_fogo', abreviar=ABREV_COMARCA)
analise_associacao_categoricas(dados, 'Houve_indiciamento', 'Status_macro')
analise_associacao_categoricas(dados, 'Tentativa', 'Reu_preso');
''')

code(r'''
tabela_associacoes = pd.DataFrame(resultados_associacao).drop_duplicates(['Variável 1', 'Variável 2'])
tabela_associacoes['Significativo (5%)'] = tabela_associacoes['p-valor'] < 0.05
print('RESUMO DOS TESTES DE ASSOCIAÇÃO')
display(tabela_associacoes.round(4))
''')

interp('ex4_geral')

# =====================================================================
md(r'''
---

## 14. Análise de Relações entre Variáveis Quantitativas (Exercício 5)

### Objetivo
Diagramas de dispersão com retas de regressão para explorar relações lineares entre variáveis quantitativas.

**Pearson × Spearman.** O r de Pearson mede relação **linear** e é sensível a valores extremos; o ρ de Spearman mede relação **monotônica** (sobre postos) e é robusto. Com distribuições muito assimétricas, como os tempos deste estudo, divergências entre os dois indicam que poucos casos extremos dirigem o r de Pearson. As matrizes usam, para cada par, os casos com ambos os valores presentes.
''')

code(r'''
VARS_CORRELACAO = ['N_indiciados', 'N_vitimas', 'Ano_instauracao', 'Tempo_fato_instauracao', 'Tempo_conclusao_ip',
                   'Quantidade_manifestacao_mp', 'N_itens_diligencia', 'Tempo_entre_manifestacoes_mp',
                   'Tempo_conclusao_mp']


def matriz_correlacao(dados, variaveis=None):
    """Matrizes de Pearson e de Spearman lado a lado, com a mesma escala divergente (−1 a 1)."""
    variaveis = variaveis or VARS_CORRELACAO
    df = dados[variaveis].astype(float)
    matrizes = {'Pearson': df.corr(method='pearson'), 'Spearman': df.corr(method='spearman')}
    fig, axes = plt.subplots(1, 2, figsize=(17, 7.2))
    mascara = np.triu(np.ones((len(variaveis), len(variaveis)), dtype=bool), k=1)
    for ax, (nome, m) in zip(axes, matrizes.items()):
        sns.heatmap(m, mask=mascara, annot=True, fmt='.2f', cmap=MAPA_DIVERGENTE, vmin=-1, vmax=1, center=0,
                    square=True, linewidths=1, linecolor='white', cbar_kws={'shrink': 0.7}, ax=ax,
                    annot_kws={'fontsize': 8.5})
        ax.set_title(f'Correlação de {nome}')
        ax.tick_params(axis='x', rotation=45)
        plt.setp(ax.get_xticklabels(), ha='right')
    plt.tight_layout()
    plt.show()

    pares = []
    for i, a in enumerate(variaveis):
        for b in variaveis[i + 1:]:
            par = df[[a, b]].dropna()
            pares.append({'X': a, 'Y': b, 'n': len(par), 'Pearson r': matrizes['Pearson'].loc[a, b],
                          'Spearman ρ': matrizes['Spearman'].loc[a, b],
                          'p (Spearman)': stats.spearmanr(par[a], par[b]).pvalue})
    pares = pd.DataFrame(pares)
    fortes = pares.loc[pares[['Pearson r', 'Spearman ρ']].abs().max(axis=1) > 0.5]
    print('Pares com |r| ou |ρ| > 0,5:')
    display(fortes.sort_values('Spearman ρ', key=abs, ascending=False).round(3))
    return pares
''')

code(r'''
def analise_correlacao(dados, var_x, var_y, unidade_x='', unidade_y='', log=False):
    """Dispersão com reta de mínimos quadrados, Pearson, Spearman, R² e interpretação."""
    df = dados[[var_x, var_y]].astype(float).dropna()
    unidade_x = unidade_x or UNIDADES.get(var_x, '')
    unidade_y = unidade_y or UNIDADES.get(var_y, '')
    pearson = stats.pearsonr(df[var_x], df[var_y])
    spearman = stats.spearmanr(df[var_x], df[var_y])
    reg = stats.linregress(df[var_x], df[var_y])

    fig, ax = plt.subplots(figsize=(11, 6.5))
    ax.scatter(df[var_x], df[var_y], s=40, color=COR_PRINCIPAL, alpha=0.75, edgecolor='white', linewidth=0.8, zorder=3)
    xs = np.linspace(df[var_x].min(), df[var_x].max(), 100)
    ax.plot(xs, reg.intercept + reg.slope * xs, color=COR_DESTAQUE, linewidth=2,
            label=f'Reta de MQ: ŷ = {reg.slope:.4f}·x + {reg.intercept:.2f}')
    if log:
        ax.set_yscale('symlog', linthresh=10)
    ax.set_xlabel(f'{var_x} ({unidade_x})' if unidade_x else var_x)
    ax.set_ylabel(f'{var_y} ({unidade_y})' if unidade_y else var_y)
    ax.set_title(f'Relação entre {var_x} e {var_y}  (n = {len(df)})')
    texto = (f'Pearson r = {pearson.statistic:.3f} (p = {pearson.pvalue:.4f})\n'
             f'Spearman ρ = {spearman.statistic:.3f} (p = {spearman.pvalue:.4f})\nR² = {reg.rvalue ** 2:.3f}')
    ax.text(0.02, 0.97, texto, transform=ax.transAxes, va='top', fontsize=9.5,
            bbox=dict(boxstyle='round', facecolor='white', edgecolor=GRADE))
    ax.legend(loc='upper right')
    plt.tight_layout()
    plt.show()

    forca = lambda r: 'fraca' if abs(r) < 0.3 else 'moderada' if abs(r) < 0.7 else 'forte'
    direcao = 'positiva' if pearson.statistic > 0 else 'negativa'
    print(f'Equação: {var_y} = {reg.slope:.5f} × {var_x} + {reg.intercept:.3f}')
    print(f'→ Correlação linear {forca(pearson.statistic)} e {direcao} (r = {pearson.statistic:.3f}); '
          f'monotônica {forca(spearman.statistic)} (ρ = {spearman.statistic:.3f}).')
    print(f'→ {"Significativa" if pearson.pvalue < 0.05 else "Não significativa"} a 5% (Pearson); '
          f'R² = {100 * reg.rvalue ** 2:.1f}% da variação de {var_y} associada linearmente a {var_x}.')
''')

md(r'''
### Exercício 5: explore relações entre variáveis quantitativas

Primeiro, as matrizes de correlação para uma visão geral.
''')

code(r'''
pares_correlacao = matriz_correlacao(dados)
''')

interp('ex5_matriz')

md(r'''
Depois, pares específicos: o exemplo do professor (tempo do IP × nº de indiciados) e os pares que a matriz destacou ou que têm interesse teórico.
''')

code(r'''
analise_correlacao(dados, 'Tempo_conclusao_ip', 'N_indiciados', unidade_x='dias', unidade_y='pessoas')
analise_correlacao(dados, 'Quantidade_manifestacao_mp', 'Tempo_conclusao_mp')
analise_correlacao(dados, 'Ano_instauracao', 'Tempo_conclusao_ip')
analise_correlacao(dados, 'Quantidade_manifestacao_mp', 'N_itens_diligencia')
analise_correlacao(dados, 'Quantidade_manifestacao_mp', 'Tempo_entre_manifestacoes_mp')
''')

interp('ex5_pares')

