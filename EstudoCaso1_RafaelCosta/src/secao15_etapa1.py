# Seções 15 a 21 — Etapa 1: o tempo de tramitação na amostra do estudo, do mais simples ao mais complexo.
# Trecho incluído por build_rafaelcc_ed1.py (usa md, code e interp de lá).

# =====================================================================
md(r'''
---

# ETAPA 1 (PARTES II A IV): O TEMPO DE TRAMITAÇÃO NA AMOSTRA DO ESTUDO

As seções 15 a 21 usam **os mesmos 218 inquéritos** analisados nos exercícios do professor e tomam o **tempo de tramitação** como variável-alvo. A ordem vai do mais simples ao mais complexo:

| Parte | Seção | Pergunta | Ferramentas |
|---|---|---|---|
| II | 15 | O que é o tempo de tramitação e como ele se distribui? | definição, estatísticas descritivas, histograma, boxplot |
| II | 16 | O tempo segue a distribuição normal? | Shapiro-Wilk, D'Agostino, Anderson-Darling, Lilliefors, Q-Q |
| III | 17 | Quais variáveis se associam ao tempo e ao desfecho? | binomial, qui-quadrado, Fisher, Mann-Whitney, Kruskal-Wallis, Dunn, Spearman |
| III | 18 | Que distribuição descreve o tempo? | máxima verossimilhança, AIC/BIC, razão de verossimilhança, FDA empírica × teórica, KS por bootstrap |
| III | 19 | O que explica o tempo, o indiciamento e a denúncia? | regressão linear (R²), logística (AUC), logística de Firth |
| IV | 20 | E os procedimentos ainda não concluídos? | análise de sobrevivência: Kaplan-Meier, log-rank, Cox, AFT |
| IV | 21 | A janela de observação distorce o tempo total? | truncamento à esquerda, teste de Tsai, entrada tardia |
''')

# =====================================================================
md(r'''
## 15. O Tempo de Tramitação: Definição e Descrição

### 15.1 O que se mede

O trajeto de um inquérito na base tem quatro marcos datados:

| Intervalo | Início → fim | Variável | Observação |
|---|---|---|---|
| Fato → instauração | `Data_fato` → `Data_instauracao` | `Tempo_fato_instauracao` | quase sempre poucos dias |
| Fase policial observada | `Data_instauracao` → `Data_recebimento_projudi` | `Tempo_conclusao_ip` | termina na **chegada ao Projudi**, não na conclusão do IP |
| **Fase judicial** | `Data_recebimento_projudi` → `Data_conclusao_mp` | `Tempo_fase_judicial` | do recebimento no Projudi à conclusão no MP |
| **Tempo total** | `Data_instauracao` → `Data_conclusao_mp` | `Tempo_total` | soma das duas fases |

**Conclusão** é a data em que o MP concluiu o procedimento (arquivamento, denúncia ou outro desfecho). **26 procedimentos ainda não estavam concluídos** na data de referência da coleta (12/03/2026). Neles, o tempo observado é só um **limite inferior** do tempo real. Esses casos se chamam **censurados**. As seções 15 a 19 trabalham com os 192 concluídos, e a seção 20 mostra como incluir os censurados.
''')

code(r'''
evento = dados['Concluido_mp'].astype(bool)
fim_observado = dados['Data_conclusao_mp'].where(evento, DATA_REFERENCIA)
dados['Tempo_fase_judicial'] = (fim_observado - dados['Data_recebimento_projudi']).dt.days.astype('Int64')
dados['Tempo_total'] = (fim_observado - dados['Data_instauracao']).dt.days.astype('Int64')
dados['Idade_entrada_anos'] = (dados['Tempo_conclusao_ip'].astype('Float64') / 365.25).round(3)
dados['Multiplas_vitimas'] = dados['N_vitimas'].gt(1).astype('boolean')
dados['Ano_recebimento_projudi'] = pd.Categorical(dados['Data_recebimento_projudi'].dt.year, ordered=True)
dados['Coorte_instauracao'] = pd.cut(dados['Ano_instauracao'].astype(float), [1990, 2014, 2018, 2021, 2030],
                                     labels=['até 2014', '2015–2018', '2019–2021', '2022 em diante'], ordered=True)
ROTULOS_BOOLEANOS.update({'Multiplas_vitimas': ('Uma vítima', 'Mais de uma vítima')})

# Coerência do desfecho: aditividade, sinais e correspondência entre evento, data e situação
assert (dados['Tempo_total'] == dados['Tempo_conclusao_ip'] + dados['Tempo_fase_judicial']).all()
assert (dados['Tempo_fase_judicial'] >= 0).all() and (dados['Tempo_total'] >= 0).all()
assert (dados.loc[evento, 'Tempo_fase_judicial'] == dados.loc[evento, 'Tempo_conclusao_mp']).all()
print('Situação processual × conclusão no MP:')
display(pd.crosstab(dados['Status_macro'], serie_exibicao(dados, 'Concluido_mp'), margins=True, margins_name='Total'))
ativos_concluidos = dados['Status_macro'].isin(['Ativo', 'Suspenso']) & evento
print(f'Ativos/suspensos com data de conclusão no MP: {int(ativos_concluidos.sum())} | '
      f'arquivados sem data de conclusão: {int((dados["Status_macro"].eq("Arquivado") & ~evento).sum())}')

DESFECHOS = {
    'Tempo_fase_judicial': 'Fase judicial (Projudi → conclusão no MP)',
    'Tempo_total': 'Tempo total (instauração → conclusão no MP)',
}
# Durações para modelos (dias + 0,5: as datas não têm hora, e um evento "no mesmo dia" dura entre 0 e 1 dia)
T_TOTAL = dados['Tempo_total'].astype(float) + 0.5
T_JUD = dados['Tempo_fase_judicial'].astype(float) + 0.5
ENTRADA = dados['Tempo_conclusao_ip'].astype(float)
EVENTO = evento.astype(int)
concluidos = dados[evento]
''')

interp('ds_definicao')

md(r'''
### 15.2 Descrição: forma, centro e dispersão

Estatísticas, histograma e boxplot dos **192 concluídos**. O gráfico de pontos à direita também mostra os 26 censurados, que ficam entre os tempos mais longos.
''')

code(r'''
def descrever(serie):
    s = serie.dropna().astype(float)
    q1, q3 = s.quantile([0.25, 0.75])
    return pd.Series({'n': len(s), 'Média': s.mean(), 'Desvio-padrão': s.std(), 'CV (%)': 100 * s.std() / s.mean(),
                      'Mínimo': s.min(), 'Q1': q1, 'Mediana': s.median(), 'Q3': q3, 'Máximo': s.max(), 'IQR': q3 - q1,
                      'Assimetria': stats.skew(s), 'Curtose (excesso)': stats.kurtosis(s), 'Zeros': int((s == 0).sum())})


descricao = pd.DataFrame({rotulo: descrever(concluidos[v]) for v, rotulo in DESFECHOS.items()})
display(descricao.round(2))

fig, axes = plt.subplots(2, 3, figsize=(17, 9), gridspec_kw={'width_ratios': [2.2, 1, 1]})
for linha, (v, rotulo) in enumerate(DESFECHOS.items()):
    valores = concluidos[v].astype(float)
    ax = axes[linha, 0]
    ax.hist(valores, bins=30, color=COR_PRINCIPAL, edgecolor='white')
    ax.axvline(valores.mean(), color=COR_DESTAQUE, linewidth=2, label=f'Média = {valores.mean():,.0f} dias')
    ax.axvline(valores.median(), color=TINTA, linewidth=2, linestyle='--', label=f'Mediana = {valores.median():,.0f} dias')
    ax.set_title(f'{rotulo}: histograma (concluídos)')
    ax.set_xlabel('dias')
    ax.set_ylabel('inquéritos')
    ax.legend()
    ax = axes[linha, 1]
    ax.boxplot(valores, widths=0.5, patch_artist=True, boxprops={'facecolor': COR_SECUNDARIA},
               medianprops={'color': TINTA, 'linewidth': 2}, showmeans=True,
               meanprops={'marker': 'D', 'markerfacecolor': COR_DESTAQUE, 'markeredgecolor': COR_DESTAQUE})
    ax.set_xticks([1], ['concluídos'])
    ax.set_ylabel('dias')
    ax.set_title('boxplot (◆ = média)')
    ax.grid(axis='x', visible=False)
    ax = axes[linha, 2]
    for i, (rotulo_ev, mascara, cor) in enumerate([('Concluídos', evento, COR_PRINCIPAL), ('Censurados', ~evento, COR_DESTAQUE)]):
        y = dados.loc[mascara, v].astype(float)
        ax.scatter(i + RNG.uniform(-0.22, 0.22, len(y)), y, s=12, color=cor, edgecolor='white', linewidth=0.4)
    ax.set_xticks([0, 1], [f'Concluídos\n(n={int(evento.sum())})', f'Censurados\n(n={int((~evento).sum())})'])
    ax.set_ylabel('dias (observados)')
    ax.set_title('gráfico de pontos')
    ax.grid(axis='x', visible=False)
plt.tight_layout()
plt.show()
''')

interp('ds_descricao')

# =====================================================================
md(r'''
---

## 16. O Tempo Segue a Distribuição Normal?

Muitos testes clássicos (t de Student, ANOVA, correlação de Pearson, regressão linear com inferência exata) supõem **normalidade**. Antes de escolher os testes, verifica-se essa hipótese com quatro testes, cada um sensível a um aspecto diferente da distância à normal:

| Teste | O que avalia |
|---|---|
| **Shapiro-Wilk** | correlação entre os dados ordenados e os quantis normais; é o mais poderoso em amostras pequenas e médias |
| **D'Agostino-Pearson** | assimetria e curtose combinadas |
| **Anderson-Darling** | distância na FDA, com peso maior nas caudas |
| **Lilliefors** | Kolmogorov-Smirnov com média e variância estimadas na própria amostra |

H₀ em todos: **os dados vêm de uma normal**. Como transformações às vezes "normalizam" dados assimétricos, os testes também são aplicados às versões raiz quadrada, log e Box-Cox. Só a tabela é mostrada para essas versões.
''')

code(r'''
def testes_normalidade(x):
    x = np.asarray(x, dtype=float)
    ad = stats.anderson(x, dist='norm')
    return {'n': len(x), 'Shapiro-Wilk W': stats.shapiro(x).statistic, 'p Shapiro': stats.shapiro(x).pvalue,
            "p D'Agostino": stats.normaltest(x).pvalue, 'Anderson-Darling A²': ad.statistic,
            'AD rejeita a 5%': bool(ad.statistic > ad.critical_values[2]), 'p Lilliefors': lilliefors(x, dist='norm')[1],
            'Assimetria': stats.skew(x), 'Curtose': stats.kurtosis(x)}


normalidade = []
for v, rotulo in DESFECHOS.items():
    x = concluidos[v].astype(float).to_numpy() + 0.5
    boxcox_x, lambda_bc = stats.boxcox(x)
    for nome, valores in {'original (dias)': x, 'raiz quadrada': np.sqrt(x), 'log': np.log(x),
                          f'Box-Cox (λ = {lambda_bc:.2f})': boxcox_x}.items():
        normalidade.append({'Desfecho': rotulo, 'Escala': nome, **testes_normalidade(valores)})
normalidade = pd.DataFrame(normalidade).set_index(['Desfecho', 'Escala'])
with pd.option_context('display.float_format', lambda v: f'{v:.4g}'):
    display(normalidade)

fig, axes = plt.subplots(2, 2, figsize=(15, 9))
for linha, (v, rotulo) in enumerate(DESFECHOS.items()):
    x = concluidos[v].astype(float).to_numpy()
    media, dp = x.mean(), x.std(ddof=1)
    ax = axes[linha, 0]
    ax.hist(x, bins=30, density=True, color=COR_SECUNDARIA, edgecolor='white', label='dados (concluídos)')
    grade = np.linspace(min(x.min(), media - 3 * dp), x.max(), 400)
    ax.plot(grade, stats.norm.pdf(grade, media, dp), color=COR_DESTAQUE, linewidth=2.2,
            label=f'normal com a mesma média e desvio\n(μ = {media:,.0f}; σ = {dp:,.0f})')
    ax.axvline(0, color=TINTA, linewidth=1)
    ax.set_title(f'{rotulo}\nhistograma × curva normal')
    ax.set_xlabel('dias')
    ax.set_ylabel('densidade')
    ax.legend(fontsize=8.5)
    ax = axes[linha, 1]
    (osm, osr), (inclinacao, intercepto, _) = stats.probplot(x, dist='norm')
    ax.scatter(osm, osr, s=14, color=COR_PRINCIPAL, edgecolor='white', linewidth=0.4)
    ax.plot(osm, inclinacao * osm + intercepto, color=COR_DESTAQUE, linewidth=1.8, label='reta da normal')
    ax.set_xlabel('quantis teóricos da normal padrão')
    ax.set_ylabel('dias (quantis observados)')
    ax.set_title(f'Q-Q normal (Shapiro-Wilk W = {stats.shapiro(x).statistic:.3f}; p = {stats.shapiro(x).pvalue:.1e})')
    ax.legend()
plt.tight_layout()
plt.show()
''')

interp('ds_normalidade')

# =====================================================================
md(r'''
---

## 17. Testes de Hipóteses: do Mais Simples ao Mais Completo

### 17.1 Variáveis explicativas

As variáveis são agrupadas pelo **momento** em que são conhecidas. Uma variável que só existe depois do início do período medido pode ser tanto causa quanto **consequência** da duração. É o caso de "quantas diligências o MP pediu": um procedimento mais longo tem mais ocasiões de receber pedidos. Esse é o **viés do tempo imortal**, e por isso essas comparações não são lidas como efeito.

| Grupo | Variáveis | Conhecidas em |
|---|---|---|
| Caso e investigação | comarca, delegacia, assunto, artigo, forma de instauração, réu preso, arma de fogo, tentativa, qualificadora, múltiplas vítimas, lei especial, intervenção estatal, tramitação direta, indiciamento | antes da chegada ao Projudi |
| Calendário | ano de recebimento no Projudi, idade do IP na chegada, coorte de instauração | na chegada ao Projudi |
| Processo no MP (não causais) | houve manifestação, tipos de diligência | durante a fase judicial |
| Desfecho e registro (descritivas) | tipo de desfecho, situação, coerência da data de prescrição | no fim |

`Validacao` e `Lei_codigo_penal` são constantes e ficam de fora. `Nome_delegacia` (41 unidades) entra pela versão agrupada `Delegacia_top6`.
''')

code(r'''
VARIAVEIS_CASO = ['Comarca', 'Delegacia_top6', 'Tipo_delegacia', 'Assunto_grupo', 'Artigo_principal', 'Forma_instauracao',
                  'Reu_preso', 'Arma_de_fogo', 'Tentativa', 'Qualificadora_capitulada', 'Multiplas_vitimas',
                  'Concurso_lei_especial', 'Indicio_intervencao_estatal', 'Tramitacao_direta', 'Houve_indiciamento']
VARIAVEIS_CALENDARIO = ['Ano_recebimento_projudi', 'Faixa_tempo_ip', 'Coorte_instauracao']
VARIAVEIS_REGISTRO = ['Desfecho', 'Status_macro', 'Coerencia_prescricao']
VARIAVEIS_PROCESSO = ['Houve_manifestacao_mp', 'Dil_prazo_conclusao', 'Dil_pericias', 'Dil_oitivas', 'Dil_midias_dados',
                      'Dil_documentos', 'Dil_controle_externo']
GRUPO_VARIAVEL = {**{v: 'Caso e investigação' for v in VARIAVEIS_CASO}, **{v: 'Calendário' for v in VARIAVEIS_CALENDARIO},
                  **{v: 'Processo no MP (não causal)' for v in VARIAVEIS_PROCESSO},
                  **{v: 'Desfecho e registro (descritivo)' for v in VARIAVEIS_REGISTRO}}
ROTULO_VARIAVEL = {'Faixa_tempo_ip': 'Idade do IP na chegada (Faixa_tempo_ip)'}
display(pd.DataFrame({'Grupo': GRUPO_VARIAVEL, 'Categorias (n)': {
    v: ' | '.join(f'{k} ({n})' for k, n in serie_exibicao(dados, v).value_counts(sort=False).items()) for v in GRUPO_VARIAVEL}}))


def barras_verticais_empilhadas(ax, tabela, cores, rotulo_largura=12):
    """Barras verticais empilhadas a 100% (linhas da tabela = barras; colunas = segmentos)."""
    pct = 100 * tabela.div(tabela.sum(axis=1), axis=0)
    base = np.zeros(len(pct))
    for coluna in pct.columns:
        ax.bar(range(len(pct)), pct[coluna], bottom=base, color=cores.get(coluna, TINTA_2), label=coluna, width=0.65)
        for i, (b, h, n) in enumerate(zip(base, pct[coluna], tabela[coluna])):
            if h >= 6:
                ax.text(i, b + h / 2, f'{h:.0f}%\n({n})', ha='center', va='center', fontsize=8)
        base += pct[coluna].to_numpy()
    ax.set_xticks(range(len(pct)), [f'{quebrar(g, rotulo_largura)}\n(n={n})' for g, n in tabela.sum(axis=1).items()], fontsize=8)
    ax.set_ylim(0, 100)
    ax.set_ylabel('% do grupo')
    ax.grid(axis='x', visible=False)
''')

md(r'''
### 17.2 Uma proporção: teste binomial exato

O teste mais simples verifica se uma **proporção** difere de um valor de referência p₀. Só faz sentido quando p₀ tem significado. Aqui, p₀ = 50% responde à pergunta **"é a maioria?"**.

- O intervalo de **Clopper-Pearson** é exato; o de **Wilson** tem melhor cobertura com proporções extremas.
- Testar a proporção de réus presos contra 50% não faria sentido, porque ninguém supõe que metade dos investigados esteja presa. Para variáveis assim, informa-se só o intervalo. A comparação com a proporção **da população** fica para a Etapa 2 (seção 22).
''')

code(r'''
def binomial(k, n, p0=0.5):
    teste = stats.binomtest(int(k), int(n), p0)
    cp = teste.proportion_ci(confidence_level=0.95, method='exact')
    w = proportion_confint(int(k), int(n), method='wilson')
    return {'k': int(k), 'n': int(n), 'Proporção (%)': 100 * k / n, 'IC 2,5% (exato)': 100 * cp.low, 'IC 97,5% (exato)': 100 * cp.high,
            'IC 95% Wilson': f'{100 * w[0]:.1f}–{100 * w[1]:.1f}', 'p₀ (%)': 100 * p0, 'p-valor (binomial exato)': teste.pvalue}


PERGUNTAS_MAIORIA = {
    'Tramitação direta é a regra?': dados['Tramitacao_direta'],
    'O MP se manifesta na maioria?': dados['Houve_manifestacao_mp'],
    'A maioria fica sem autor identificado?': ~dados['Houve_indiciamento'].astype(bool),
    'A maioria é com arma de fogo?': dados['Arma_de_fogo'],
    'A maioria é arquivada?': dados['Status_macro'].eq('Arquivado'),
}
tabela_binomial = pd.DataFrame({q: binomial(s.astype(bool).sum(), s.notna().sum()) for q, s in PERGUNTAS_MAIORIA.items()}).T
tabela_binomial['Conclusão (5%)'] = np.where(tabela_binomial['p-valor (binomial exato)'].astype(float) < 0.05,
                                            np.where(tabela_binomial['Proporção (%)'].astype(float) > 50, 'maioria', 'minoria'),
                                            'não se distingue de 50%')
with pd.option_context('display.float_format', lambda v: f'{v:.4g}'):
    display(tabela_binomial)
print('Proporções informadas só com intervalo (não há p₀ com significado na amostra isolada):')
display(pd.DataFrame({q: binomial(s.astype(bool).sum(), s.notna().sum()) for q, s in {
    'Réu preso': dados['Reu_preso'], 'Auto de prisão em flagrante': dados['Forma_instauracao'].astype(str).str.startswith('Auto'),
    'Tentativa': dados['Tentativa'], 'Denúncia oferecida': dados['Desfecho'].eq('Denúncia oferecida'),
    'Indício de intervenção estatal': dados['Indicio_intervencao_estatal']}.items()}).T
        [['k', 'n', 'Proporção (%)', 'IC 2,5% (exato)', 'IC 97,5% (exato)', 'IC 95% Wilson']].astype(object))

fig, ax = plt.subplots(figsize=(12, 5))
x = np.arange(len(tabela_binomial))
props = tabela_binomial['Proporção (%)'].astype(float).to_numpy()
inf, sup = tabela_binomial['IC 2,5% (exato)'].astype(float).to_numpy(), tabela_binomial['IC 97,5% (exato)'].astype(float).to_numpy()
pvals = tabela_binomial['p-valor (binomial exato)'].astype(float).to_numpy()
ax.bar(x, props, color=[COR_PRINCIPAL if p < 0.05 else COR_SECUNDARIA for p in pvals], width=0.6)
ax.errorbar(x, props, yerr=[props - inf, sup - props], fmt='none', ecolor=TINTA, capsize=5, linewidth=1.5)
ax.axhline(50, color=COR_DESTAQUE, linestyle='--', linewidth=1.8, label='p₀ = 50%')
for xi, p, pv in zip(x, props, pvals):
    ax.text(xi, 103, f'{p:.1f}%\np = {pv:.2g}', ha='center', va='bottom', fontsize=8.5)
ax.set_xticks(x, [quebrar(q, 18) for q in tabela_binomial.index], fontsize=8.5)
ax.set_ylim(0, 122)
ax.set_ylabel('% (barra) e IC 95% exato (traço)')
ax.set_title('Teste binomial exato contra 50% (azul escuro: rejeita H₀ a 5%)')
ax.legend(loc='upper right')
ax.grid(axis='x', visible=False)
plt.tight_layout()
plt.show()
''')

md(r'''
### 17.3 Duas variáveis categóricas: qui-quadrado, Fisher e post-hoc

O próximo passo é testar a **associação** entre duas variáveis categóricas. Aqui, o par é uma característica do caso e o **tipo de desfecho** (arquivamento, denúncia, em curso). O tipo de desfecho resume a fase judicial sem dicotomizar o tempo, o que seria inadequado com censurados.

- **Qui-quadrado de independência:** H₀ diz que as proporções de desfecho são iguais em todos os grupos. A **regra de Cochran** exige frequência esperada ≥ 5 em pelo menos 80% das caselas e nenhuma abaixo de 1.
- **Quando a regra falha:** usa-se o **exato de Fisher** nas tabelas 2×2 e o **qui-quadrado por permutação** nas maiores.
- **Força da associação:** **V de Cramér**. Em tabelas 2×2, a **razão de chances (OR)**.
- **Post-hoc:** os **resíduos ajustados** apontam as caselas que fogem da independência (|r| > 2), e os pares de grupos são comparados por Fisher com ajuste de Holm.
''')

code(r'''
def teste_associacao(x, y, n_perm=10_000):
    tabela = pd.crosstab(x, y)
    chi2, p_assint, gl, esperada = stats.chi2_contingency(tabela, correction=False)
    pct_baixa = 100 * (esperada < 5).mean()
    if pct_baixa <= 20 and esperada.min() >= 1:
        metodo, p = 'Qui-quadrado (assintótico)', p_assint
    elif tabela.shape == (2, 2):
        metodo, p = 'Exato de Fisher', stats.fisher_exact(tabela)[1]
    else:
        metodo, p = f'Qui-quadrado por permutação ({n_perm:,})', qui_quadrado_permutacao(x, y, n_perm)[1]
    return tabela, {'χ²': chi2, 'gl': gl, '% esperada < 5': pct_baixa, 'Método': metodo, 'p-valor': p, 'V de Cramér': v_de_cramer(tabela)}


def residuos_ajustados(tabela):
    esperada = stats.contingency.expected_freq(tabela)
    n = tabela.values.sum()
    linha, coluna = tabela.sum(axis=1).values[:, None] / n, tabela.sum(axis=0).values[None, :] / n
    return (tabela - esperada) / np.sqrt(esperada * (1 - linha) * (1 - coluna))


dados['Tipo_desfecho'] = pd.Categorical(
    np.select([dados['Desfecho'].eq('Denúncia oferecida'), dados['Status_macro'].eq('Arquivado')], ['Denúncia', 'Arquivamento'],
              'Em curso'), categories=['Arquivamento', 'Denúncia', 'Em curso'])
CORES_DESFECHO = {'Arquivamento': COR_SECUNDARIA, 'Denúncia': COR_DESTAQUE, 'Em curso': CORES[2],
                  'Sem denúncia': COR_SECUNDARIA}
associacoes_desfecho, tabelas_desfecho = [], {}
for v in ['Forma_instauracao', 'Reu_preso', 'Houve_indiciamento', 'Tentativa', 'Arma_de_fogo', 'Assunto_grupo', 'Tramitacao_direta',
          'Comarca', 'Tipo_delegacia', 'Indicio_intervencao_estatal', 'Coorte_instauracao']:
    x = serie_exibicao(dados, v)
    validos = x.notna()
    tabela, resultado = teste_associacao(x[validos].astype(str), dados.loc[validos, 'Tipo_desfecho'])
    tabelas_desfecho[v] = tabela
    associacoes_desfecho.append({'Variável': v, **resultado})
associacoes_desfecho = pd.DataFrame(associacoes_desfecho).set_index('Variável')
associacoes_desfecho['p BH'] = multipletests(associacoes_desfecho['p-valor'], method='fdr_bh')[1]
print('Variável do caso × tipo de desfecho')
with pd.option_context('display.float_format', lambda v: f'{v:.4g}'):
    display(associacoes_desfecho.sort_values('p-valor'))

variaveis_plot = list(associacoes_desfecho.sort_values('p-valor').index[:6])
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
for ax, v in zip(axes.flat, variaveis_plot):
    barras_verticais_empilhadas(ax, tabelas_desfecho[v], CORES_DESFECHO)
    r = associacoes_desfecho.loc[v]
    ax.set_title(f'{v}\n{r["Método"]}: p = {r["p-valor"]:.3g}; V = {r["V de Cramér"]:.2f}', fontsize=9.5)
axes.flat[0].legend(fontsize=8, loc='lower left')
plt.suptitle('Tipo de desfecho por grupo: barras empilhadas a 100%', fontweight='bold')
plt.tight_layout()
plt.show()

for v in associacoes_desfecho.index[associacoes_desfecho['p BH'] < 0.05]:
    tabela = tabelas_desfecho[v]
    print(f'\nPost-hoc — {v}: % na linha e resíduos ajustados (|r| > 2 indica a casela que foge da independência)')
    display(pd.concat({'% na linha': (100 * tabela.div(tabela.sum(axis=1), axis=0)).round(1),
                       'Resíduo ajustado': residuos_ajustados(tabela).round(2)}, axis=1))
''')

code(r'''
# Tabelas 2×2: denúncia × características do caso (Fisher, razão de chances e barras empilhadas)
PARES_2X2 = ['Forma_instauracao', 'Reu_preso', 'Houve_indiciamento', 'Tentativa']
fig, axes = plt.subplots(1, len(PARES_2X2), figsize=(4.4 * len(PARES_2X2), 5), sharey=True)
resumo_2x2 = []
for ax, v in zip(axes, PARES_2X2):
    grupo = serie_exibicao(dados, v).astype(str)
    alvo = dados['Desfecho'].eq('Denúncia oferecida').map({True: 'Denúncia', False: 'Sem denúncia'})
    tabela = pd.crosstab(grupo, alvo).reindex(columns=['Denúncia', 'Sem denúncia'], fill_value=0)
    razao, p = stats.fisher_exact(tabela.to_numpy())
    ic_or = stats.contingency.odds_ratio(tabela.to_numpy()).confidence_interval()
    barras_verticais_empilhadas(ax, tabela, CORES_DESFECHO, rotulo_largura=14)
    ax.set_title(f'{v}\nFisher p = {p:.3g}; OR = {razao:.1f}', fontsize=9.5)
    resumo_2x2.append({'Variável': v, 'OR': razao, 'IC 2,5%': ic_or.low, 'IC 97,5%': ic_or.high, 'p (Fisher)': p})
axes[-1].legend(loc='lower right', fontsize=8)
plt.suptitle('Tabelas 2×2: proporção de denúncia por grupo (exato de Fisher)', fontweight='bold')
plt.tight_layout()
plt.show()
with pd.option_context('display.float_format', lambda v: f'{v:.4g}'):
    display(pd.DataFrame(resumo_2x2).set_index('Variável'))


def posthoc_pares(x, y, alvo):
    """Post-hoc do qui-quadrado: cada par de grupos comparado por Fisher (alvo × resto), com ajuste de Holm."""
    grupos = list(pd.unique(x.dropna()))
    linhas = []
    for i, a in enumerate(grupos):
        for b in grupos[i + 1:]:
            m = x.isin([a, b])
            tabela = pd.crosstab(x[m], y[m].eq(alvo)).reindex(columns=[True, False], fill_value=0)
            linhas.append({'Grupo A': a, 'Grupo B': b, f'% {alvo} A': 100 * tabela.loc[a, True] / tabela.loc[a].sum(),
                           f'% {alvo} B': 100 * tabela.loc[b, True] / tabela.loc[b].sum(), 'p Fisher': stats.fisher_exact(tabela)[1]})
    pares = pd.DataFrame(linhas)
    pares['p Holm'] = multipletests(pares['p Fisher'], method='holm')[1]
    return pares.sort_values('p Fisher')


for v in [v for v in associacoes_desfecho.index[associacoes_desfecho['p BH'] < 0.05] if tabelas_desfecho[v].shape[0] > 2]:
    x = serie_exibicao(dados, v).astype(str).where(dados[v].notna())
    print(f'Post-hoc par a par — {v}: proporção "em curso" (Fisher, Holm)')
    display(posthoc_pares(x, dados['Tipo_desfecho'].astype(str), 'Em curso').head(8).round(4))
''')

interp('ef_proporcoes')

md(r'''
### 17.4 O tempo entre grupos: Mann-Whitney, Kruskal-Wallis e Dunn

Como o tempo **não é normal** (seção 16), a comparação entre grupos usa **testes de postos**, que não supõem distribuição alguma:

- **Dois grupos:** **Mann-Whitney**. H₀: um tempo sorteado de cada grupo tem a mesma chance de ser o maior. Tamanho de efeito: **correlação rank-bisserial** (−1 a 1);
- **Três ou mais grupos:** **Kruskal-Wallis**. Tamanho de efeito: **ε²**, a proporção da variação dos postos atribuída ao grupo;
- **Post-hoc:** quando o Kruskal-Wallis é significativo, o **teste de Dunn** compara os pares com ajuste de Holm. Nos boxplots, grupos **sem letra em comum** diferem;
- **Muitos testes:** os p-valores de cada desfecho são corrigidos por **Benjamini-Hochberg** (controle da taxa de falsas descobertas).

Os testes usam os **concluídos**. A seção 20 refaz as comparações incluindo os censurados.
''')

code(r'''
def comparar_grupos(df, var_q, var_c):
    sub = df[[var_q, var_c]].dropna()
    grupos = {str(k): g[var_q].astype(float).to_numpy() for k, g in sub.groupby(var_c, observed=True)}
    grupos = {k: v for k, v in grupos.items() if len(v) >= 3}
    nomes = list(grupos)
    medianas = ' | '.join(f'{k}: {np.median(v):.0f} (n={len(v)})' for k, v in grupos.items())
    if len(grupos) < 2:
        return None
    if len(grupos) == 2:
        a, b = grupos[nomes[0]], grupos[nomes[1]]
        res = stats.mannwhitneyu(a, b, alternative='two-sided')
        return {'Teste': 'Mann-Whitney', 'Estatística': res.statistic, 'p-valor': res.pvalue,
                'Medida de efeito': f'rank-bisserial ({nomes[0]} vs {nomes[1]})', 'Efeito': 2 * res.statistic / (len(a) * len(b)) - 1,
                'Medianas': medianas}
    res = stats.kruskal(*grupos.values())
    n, k = sum(map(len, grupos.values())), len(grupos)
    return {'Teste': 'Kruskal-Wallis', 'Estatística': res.statistic, 'p-valor': res.pvalue, 'Medida de efeito': 'ε²',
            'Efeito': max((res.statistic - k + 1) / (n - k), 0), 'Medianas': medianas}


linhas = []
for v_desfecho, rotulo in DESFECHOS.items():
    for v in GRUPO_VARIAVEL:
        resultado = comparar_grupos(concluidos.assign(**{v: serie_exibicao(concluidos, v)}), v_desfecho, v)
        if resultado:
            linhas.append({'Desfecho': rotulo, 'Variável': ROTULO_VARIAVEL.get(v, v), 'Grupo': GRUPO_VARIAVEL[v], **resultado})
testes_np = pd.DataFrame(linhas)
testes_np['p BH'] = testes_np.groupby('Desfecho')['p-valor'].transform(lambda p: multipletests(p, method='fdr_bh')[1])
testes_np['Significativo (BH 5%)'] = testes_np['p BH'] < 0.05
with pd.option_context('display.float_format', lambda v: f'{v:.4g}', 'display.max_colwidth', 120):
    for rotulo, tabela in testes_np.groupby('Desfecho', sort=False):
        print(rotulo)
        display(tabela.drop(columns='Desfecho').set_index('Variável').sort_values('p-valor'))
''')

code(r'''
def letras_compactas(grupos, p_matriz, alfa=0.05):
    """Letras do post-hoc: grupos que compartilham uma letra não diferem (p ajustado ≥ alfa)."""
    conjuntos = []
    for g in grupos:
        colocado = False
        for conj in conjuntos:
            if all(p_matriz.loc[g, h] >= alfa for h in conj):
                conj.append(g)
                colocado = True
        if not colocado:
            conjuntos.append([g])
    return {g: ''.join('abcdefghij'[i] for i, conj in enumerate(conjuntos) if g in conj) for g in grupos}


def boxplot_grupos(ax, df, v_desfecho, v, titulo=None):
    sub = df[[v_desfecho]].assign(G=serie_exibicao(df, v).astype(object)).dropna()
    sub[v_desfecho] = sub[v_desfecho].astype(float)
    ordem = serie_exibicao(df, v).cat.categories if isinstance(serie_exibicao(df, v).dtype, pd.CategoricalDtype) else sorted(sub['G'].unique())
    grupos = [str(g) for g in ordem if (sub['G'].astype(str) == str(g)).sum() >= 3]
    sub['G'] = sub['G'].astype(str)
    valores = [sub.loc[sub['G'] == g, v_desfecho].to_numpy() for g in grupos]
    caixa = ax.boxplot(valores, patch_artist=True, showfliers=False, widths=0.55, medianprops={'color': TINTA, 'linewidth': 2})
    for patch, cor in zip(caixa['boxes'], CORES * 2):
        patch.set(facecolor=cor, alpha=0.35, edgecolor=cor)
    for i, (vals, cor) in enumerate(zip(valores, CORES * 2), start=1):
        ax.scatter(i + RNG.uniform(-0.18, 0.18, len(vals)), vals, s=8, color=cor, alpha=0.7, edgecolor='none')
    if len(grupos) == 2:
        p = stats.mannwhitneyu(*valores).pvalue
        nome_teste = 'Mann-Whitney'
    else:
        p = stats.kruskal(*valores).pvalue
        nome_teste = 'Kruskal-Wallis'
        if p < 0.05:
            dunn = sp.posthoc_dunn(sub[sub['G'].isin(grupos)], val_col=v_desfecho, group_col='G', p_adjust='holm').loc[grupos, grupos]
            letras = letras_compactas(grupos, dunn)
            topo = max(np.max(vv) for vv in valores)
            for i, g in enumerate(grupos, start=1):
                ax.text(i, topo * 1.04, letras[g], ha='center', fontsize=11, fontweight='bold')
    ax.set_xticks(range(1, len(grupos) + 1), [quebrar(g, 11) for g in grupos], fontsize=8)
    ax.set_title(f'{titulo or v}\n{nome_teste} p = {p:.3g}' + (' (letras: Dunn–Holm)' if nome_teste == 'Kruskal-Wallis' and p < 0.05 else ''),
                 fontsize=9.5)
    ax.grid(axis='x', visible=False)


VARIAVEIS_BOXPLOT = ['Comarca', 'Forma_instauracao', 'Reu_preso', 'Arma_de_fogo', 'Assunto_grupo', 'Tramitacao_direta',
                     'Houve_indiciamento', 'Coorte_instauracao', 'Houve_manifestacao_mp']
for v_desfecho, rotulo in DESFECHOS.items():
    fig, axes = plt.subplots(3, 3, figsize=(18, 14))
    for ax, v in zip(axes.flat, VARIAVEIS_BOXPLOT):
        boxplot_grupos(ax, concluidos, v_desfecho, v)
    for ax in axes[:, 0]:
        ax.set_ylabel('dias')
    plt.suptitle(f'{rotulo}: boxplots por variável (concluídos)', fontweight='bold')
    plt.tight_layout()
    plt.show()
''')

code(r'''
# Post-hoc de Dunn em tabela: todas as variáveis com 3+ grupos significativas após BH
multigrupo = testes_np[(testes_np['Teste'] == 'Kruskal-Wallis') & testes_np['Significativo (BH 5%)']]
mapa_rotulo = {ROTULO_VARIAVEL.get(v, v): v for v in GRUPO_VARIAVEL}
for _, linha in multigrupo.iterrows():
    v = mapa_rotulo[linha['Variável']]
    v_desfecho = {r: k for k, r in DESFECHOS.items()}[linha['Desfecho']]
    sub = concluidos.assign(G=serie_exibicao(concluidos, v).astype(str))[[v_desfecho, 'G']].dropna()
    sub[v_desfecho] = sub[v_desfecho].astype(float)
    dunn = sp.posthoc_dunn(sub, val_col=v_desfecho, group_col='G', p_adjust='holm')
    pares = dunn.where(np.triu(np.ones(dunn.shape, dtype=bool), k=1)).stack().rename('p Holm').reset_index()
    pares.columns = ['Grupo A', 'Grupo B', 'p Holm']
    medianas = sub.groupby('G')[v_desfecho].median()
    pares['Mediana A'], pares['Mediana B'] = pares['Grupo A'].map(medianas), pares['Grupo B'].map(medianas)
    print(f'Dunn–Holm — {linha["Variável"]} ({linha["Desfecho"]}): pares com p < 0,05')
    display(pares[pares['p Holm'] < 0.05].sort_values('p Holm').round(4))
''')

interp('ef_naoparametricos')

md(r'''
### 17.5 Duas variáveis quantitativas: correlação de Spearman

O **ρ de Spearman** é a correlação entre os **postos**. Ele mede relações **monotônicas** (sempre crescentes ou sempre decrescentes), não exige normalidade e é robusto a valores extremos. Por isso substitui o r de Pearson aqui. O gráfico mostra a dispersão com uma linha de tendência **LOWESS** (regressão local), que não impõe forma alguma. O intervalo de ρ vem de 1.000 reamostragens bootstrap.
''')

code(r'''
QUANTITATIVAS = ['Idade_entrada_anos', 'Ano_instauracao', 'Tempo_fato_instauracao', 'N_vitimas', 'N_indiciados',
                 'Quantidade_manifestacao_mp', 'N_itens_diligencia']
correl = []
for v_desfecho, rotulo in DESFECHOS.items():
    for v in QUANTITATIVAS:
        par = concluidos[[v_desfecho, v]].astype(float).dropna()
        r = stats.spearmanr(par[v], par[v_desfecho])
        correl.append({'Desfecho': rotulo, 'Variável': v, 'n': len(par), 'ρ de Spearman': r.statistic, 'p-valor': r.pvalue,
                       'Tipo': 'Processo (não causal)' if v in ('Quantidade_manifestacao_mp', 'N_itens_diligencia') else 'Caso/calendário'})
correl = pd.DataFrame(correl)
correl['p BH'] = correl.groupby('Desfecho')['p-valor'].transform(lambda p: multipletests(p, method='fdr_bh')[1])
display(correl.pivot(index=['Variável', 'Tipo'], columns='Desfecho', values=['ρ de Spearman', 'p BH']).round(4))

PARES_SPEARMAN = [('Idade_entrada_anos', 'Tempo_fase_judicial'), ('Quantidade_manifestacao_mp', 'Tempo_fase_judicial'),
                  ('Ano_instauracao', 'Tempo_total'), ('N_indiciados', 'Tempo_total')]
fig, axes = plt.subplots(1, 4, figsize=(19, 4.8))
for ax, (vx, vy) in zip(axes, PARES_SPEARMAN):
    par = concluidos[[vx, vy]].astype(float).dropna()
    rho = stats.spearmanr(par[vx], par[vy]).statistic
    boot = [stats.spearmanr(*par.iloc[RNG.integers(0, len(par), len(par))].T.to_numpy()).statistic for _ in range(1000)]
    ic = np.nanpercentile(boot, [2.5, 97.5])
    ax.scatter(par[vx] + RNG.uniform(-0.15, 0.15, len(par)) * (par[vx].nunique() < 25), par[vy], s=14,
               color=COR_SECUNDARIA, edgecolor='white', linewidth=0.4)
    suave = lowess(par[vy], par[vx], frac=0.6)
    ax.plot(suave[:, 0], suave[:, 1], color=COR_DESTAQUE, linewidth=2.2, label='tendência (LOWESS)')
    ax.set_xlabel(vx)
    ax.set_ylabel(f'{vy} (dias)')
    ax.set_title(f'ρ = {rho:.2f} (IC 95% {ic[0]:.2f} a {ic[1]:.2f}); n = {len(par)}', fontsize=9.5)
    ax.legend(fontsize=8)
plt.tight_layout()
plt.show()
''')

interp('ef_spearman')

# =====================================================================
md(r'''
---

## 18. Que Distribuição Descreve o Tempo?

O tempo não é normal, mas pode seguir outra distribuição conhecida. Para durações positivas e assimétricas, as candidatas são as famílias clássicas de tempo de vida. A **gama generalizada** contém quase todas como casos particulares. No `scipy`, ela tem dois parâmetros de forma, *a* e *c*:

| Família | Restrição na gama generalizada | Parâmetros (com escala) |
|---|---|---|
| Exponencial | a = 1 e c = 1 | 1 |
| Weibull | a = 1 | 2 |
| Gama | c = 1 | 2 |
| Lognormal | limite a → ∞ | 2 |
| Log-logística | não está aninhada | 2 |
| **Gama generalizada** | livre | 3 |

**Procedimento:**

1. ajuste por **máxima verossimilhança** aos concluídos (dias + 0,5, porque as famílias exigem valores positivos);
2. comparação por **AIC e BIC**. O BIC penaliza mais os parâmetros extras;
3. **teste da razão de verossimilhança** (LR) para as famílias aninhadas na gama generalizada: o terceiro parâmetro "se paga"?
4. **aderência:** o KS e o Cramér-von Mises tabelados não valem quando os parâmetros são estimados na própria amostra. O valor-p vem de um **bootstrap paramétrico** com 200 réplicas: simula-se do modelo ajustado, reajusta-se e compara-se a distância;
5. **gráficos:** a **FDA empírica** contra a **FDA teórica** da distribuição escolhida, com os parâmetros estimados, além do histograma com a densidade ajustada.
''')

code(r'''
FAMILIAS_SCIPY = {
    'Exponencial': (stats.expon, 1), 'Weibull': (stats.weibull_min, 2), 'Gama': (stats.gamma, 2),
    'Lognormal': (stats.lognorm, 2), 'Log-logística': (stats.fisk, 2), 'Gama generalizada': (stats.gengamma, 3),
}


def ajustar_scipy(x):
    ajustes, linhas = {}, []
    for nome, (dist, k) in FAMILIAS_SCIPY.items():
        params = dist.fit(x, floc=0)
        if nome == 'Gama generalizada':
            # vários pontos de partida (gama e Weibull ajustadas): a verossimilhança da gama generalizada é irregular
            k_g = stats.gamma.fit(x, floc=0)[0]
            c_w = stats.weibull_min.fit(x, floc=0)[0]
            candidatos = [params] + [dist.fit(x, a0, c0, floc=0) for a0, c0 in [(k_g, 1.0), (1.0, c_w), (5.0, 0.3)]]
            params = max(candidatos, key=lambda p: dist.logpdf(x, *p).sum())
        ll = dist.logpdf(x, *params).sum()
        ajustes[nome] = (dist, params)
        forma = ', '.join(f'{v:.3g}' for v in params[:-2])
        linhas.append({'Família': nome, 'Parâmetros livres': k, 'log-verossimilhança': ll, 'AIC': 2 * k - 2 * ll,
                       'BIC': k * np.log(len(x)) - 2 * ll, 'Forma': forma or '—', 'Escala': params[-1],
                       'Mediana teórica (dias)': dist.median(*params)})
    tabela = pd.DataFrame(linhas).set_index('Família').sort_values('AIC')
    tabela['ΔAIC'], tabela['ΔBIC'] = tabela['AIC'] - tabela['AIC'].min(), tabela['BIC'] - tabela['BIC'].min()
    return ajustes, tabela


def razao_verossimilhanca_scipy(tabela):
    ll = tabela['log-verossimilhança']
    testes = []
    for restrito, gl, hipotese in [('Weibull', 1, 'a = 1'), ('Gama', 1, 'c = 1'), ('Exponencial', 2, 'a = c = 1')]:
        lr = 2 * (ll['Gama generalizada'] - ll[restrito])
        testes.append({'H₀ (modelo restrito)': f'{restrito} ({hipotese})', 'LR': lr, 'gl': gl, 'p-valor': stats.chi2.sf(max(lr, 0), gl)})
    lr = 2 * (ll['Weibull'] - ll['Exponencial'])
    testes.append({'H₀ (modelo restrito)': 'Exponencial dentro da Weibull', 'LR': lr, 'gl': 1, 'p-valor': stats.chi2.sf(max(lr, 0), 1)})
    return pd.DataFrame(testes).set_index('H₀ (modelo restrito)')


def aderencia_bootstrap(x, nome, n_boot=200):
    dist, params = FAMILIAS_SCIPY[nome][0], FAMILIAS_SCIPY[nome][0].fit(x, floc=0)
    ks_obs = stats.kstest(x, dist.cdf, args=params).statistic
    cvm_obs = stats.cramervonmises(x, dist.cdf, args=params).statistic
    ks_sim, cvm_sim = [], []
    for _ in range(n_boot):
        xs = dist.rvs(*params, size=len(x), random_state=RNG)
        ps = dist.fit(xs, floc=0)
        ks_sim.append(stats.kstest(xs, dist.cdf, args=ps).statistic)
        cvm_sim.append(stats.cramervonmises(xs, dist.cdf, args=ps).statistic)
    return {'KS (D)': ks_obs, 'p KS (bootstrap)': (1 + np.sum(np.array(ks_sim) >= ks_obs)) / (n_boot + 1),
            'Cramér-von Mises (W²)': cvm_obs, 'p CvM (bootstrap)': (1 + np.sum(np.array(cvm_sim) >= cvm_obs)) / (n_boot + 1)}


ajustes_conc, tabelas_conc, aderencias_conc = {}, {}, {}
for v, rotulo in DESFECHOS.items():
    x = concluidos[v].astype(float).to_numpy() + 0.5
    ajustes_conc[v], tabelas_conc[v] = ajustar_scipy(x)
    print(rotulo)
    display(tabelas_conc[v].round(3))
    with pd.option_context('display.float_format', lambda v: f'{v:.4g}'):
        display(razao_verossimilhanca_scipy(tabelas_conc[v]))
    candidatas = list(tabelas_conc[v].index[:3])
    aderencias_conc[v] = pd.DataFrame({n: aderencia_bootstrap(x, n) for n in candidatas}).T
    print('Aderência das três melhores por AIC (bootstrap paramétrico, 200 réplicas):')
    with pd.option_context('display.float_format', lambda v: f'{v:.4g}'):
        display(aderencias_conc[v])
''')

code(r'''
# FDA empírica × FDA teórica (com os parâmetros) e histograma × densidade ajustada
for v, rotulo in DESFECHOS.items():
    x = np.sort(concluidos[v].astype(float).to_numpy() + 0.5)
    ecdf = np.arange(1, len(x) + 1) / len(x)
    melhores = list(tabelas_conc[v].index[:3])
    grade = np.linspace(0.5, x.max(), 600)
    fig, axes = plt.subplots(1, 3, figsize=(19, 5.2))
    axes[0].step(x, ecdf, where='post', color=TINTA, linewidth=2, label='FDA empírica (concluídos)')
    for nome, cor in zip(melhores, [COR_PRINCIPAL, COR_DESTAQUE, CORES[2]]):
        dist, params = ajustes_conc[v][nome]
        forma = ', '.join(f'{p:.2f}' for p in params[:-2])
        axes[0].plot(grade, dist.cdf(grade, *params), color=cor, linewidth=1.8,
                     label=f'{nome} ({"forma " + forma + "; " if forma else ""}escala {params[-1]:,.0f})')
    axes[0].set_xlabel('dias')
    axes[0].set_ylabel('F(t) = P(T ≤ t)')
    axes[0].set_title(f'{rotulo}\nFDA empírica × FDA teórica (3 melhores por AIC)')
    axes[0].legend(fontsize=8, loc='lower right')

    nome = melhores[0]
    dist, params = ajustes_conc[v][nome]
    teorica = dist.cdf(x, *params)
    axes[1].plot(teorica, ecdf, 'o', markersize=3.5, color=COR_PRINCIPAL)
    axes[1].plot([0, 1], [0, 1], color=COR_DESTAQUE, linewidth=1.5)
    d_ks = aderencias_conc[v].loc[nome, 'KS (D)']
    axes[1].set_xlabel(f'probabilidade acumulada teórica ({nome})')
    axes[1].set_ylabel('probabilidade acumulada empírica')
    axes[1].set_title(f'Gráfico P-P: {nome}\nKS D = {d_ks:.3f}; p bootstrap = {aderencias_conc[v].loc[nome, "p KS (bootstrap)"]:.3f}')

    axes[2].hist(x, bins=30, density=True, color=COR_SECUNDARIA, edgecolor='white', label='histograma (densidade)')
    for nome_d, cor in zip(melhores, [COR_PRINCIPAL, COR_DESTAQUE, CORES[2]]):
        dist_d, params_d = ajustes_conc[v][nome_d]
        axes[2].plot(grade, dist_d.pdf(grade, *params_d), color=cor, linewidth=1.8, label=nome_d)
    axes[2].set_xlabel('dias')
    axes[2].set_ylabel('densidade')
    axes[2].set_ylim(0, np.histogram(x, bins=30, density=True)[0].max() * 1.6)
    axes[2].set_title('Histograma × função densidade ajustada')
    axes[2].legend(fontsize=8.5)
    plt.tight_layout()
    plt.show()
''')

md(r'''
**A heterogeneidade explica a forma?** A fase judicial mistura dois processos: os procedimentos em que o MP **pede o arquivamento sem se manifestar antes** e os que passam por **diligências**. Se a distribuição for uma mistura desses dois grupos, cada um deve ser bem descrito por uma família. A verificação ajusta a gama generalizada em cada grupo e compara as FDAs empírica e teórica.
''')

code(r'''
x_jud = concluidos['Tempo_fase_judicial'].astype(float).to_numpy() + 0.5
grupo_manif = concluidos['Houve_manifestacao_mp'].astype(bool).to_numpy()
fig, axes = plt.subplots(1, 2, figsize=(15, 4.8))
mistura, ll_grupos = [], 0.0
for ax, (rotulo, mascara) in zip(axes, [('Sem manifestação do MP', ~grupo_manif), ('Com manifestação do MP', grupo_manif)]):
    xg = np.sort(x_jud[mascara])
    params = stats.gengamma.fit(xg, floc=0)
    ll_grupos += stats.gengamma.logpdf(xg, *params).sum()
    ad = aderencia_bootstrap(xg, 'Gama generalizada', n_boot=100)
    mistura.append({'Grupo': rotulo, 'n': len(xg), 'Mediana (dias)': np.median(xg), 'a': params[0], 'c': params[1],
                    'escala': params[-1], **ad})
    ax.step(xg, np.arange(1, len(xg) + 1) / len(xg), where='post', color=TINTA, linewidth=2, label='FDA empírica')
    grade = np.linspace(0.5, xg.max(), 400)
    ax.plot(grade, stats.gengamma.cdf(grade, *params), color=COR_PRINCIPAL, linewidth=2,
            label=f'gama generalizada (a = {params[0]:.2f}; c = {params[1]:.2f}; escala = {params[-1]:,.0f})')
    ax.set_title(f'{rotulo} (n = {len(xg)}): KS p bootstrap = {ad["p KS (bootstrap)"]:.3f}')
    ax.set_xlabel('dias')
    ax.set_ylabel('F(t)')
    ax.legend(fontsize=8.5, loc='lower right')
plt.tight_layout()
plt.show()
display(pd.DataFrame(mistura).set_index('Grupo').round(4))
lr_mistura = 2 * (ll_grupos - tabelas_conc['Tempo_fase_judicial'].loc['Gama generalizada', 'log-verossimilhança'])
print(f'Razão de verossimilhança (uma gama generalizada por grupo × uma só): LR = {lr_mistura:.1f}; gl = 3; '
      f'p = {stats.chi2.sf(lr_mistura, 3):.2e}')
''')

interp('ds_distribuicao')

# =====================================================================
md(r'''
---

## 19. Modelos de Regressão: o que Explica o Tempo, o Indiciamento e a Denúncia

| Pergunta | Desfecho | Modelo | Medida de ajuste |
|---|---|---|---|
| O que se associa a um tempo **maior**? | log(1 + dias) da fase judicial, concluídos | **linear** (MQO, erros HC3) | **R²**, R² ajustado, **R² parcial** de cada variável |
| O que se associa ao **indiciamento**? | autor identificado: 77 sim × 141 não | **logística** | razões de chance (OR), pseudo-R² de McFadden, **AUC (ROC)**, Hosmer-Lemeshow |
| O que se associa à **denúncia**? | denúncia (6) × arquivamento (181) | **logística de Firth** | OR penalizado, uma variável por vez |
| O que se associa à **prescrição**? | extinção por prescrição (10) × demais arquivamentos | **logística de Firth** | OR penalizado, uma variável por vez |

**Por que essas escolhas.**
- **Regressão linear:** a resposta é o **log** do tempo porque o tempo é muito assimétrico e os resíduos na escala original seriam muito heterogêneos. Os coeficientes exponenciados são efeitos **multiplicativos** (1,5 = 50% mais tempo). O modelo ignora os 26 censurados; a seção 20 corrige isso.
- **Regressão logística:** a regra prática é ter cerca de 10 eventos por parâmetro. O indiciamento (77 eventos) comporta uns 7 parâmetros.
- **Logística de Firth:** a denúncia (6 eventos) não comporta um modelo multivariável. A logística comum daria estimativas infinitas por separação; a penalização de Firth corrige o viés de eventos raros. O modelo completo da denúncia fica para a população (seção 22).
- **Comum a todos:** o **VIF** verifica a colinearidade entre as variáveis.
''')

code(r'''
REFERENCIAS = {'Comarca': 'Goiânia', 'Assunto_grupo': 'Homicídio simples', 'Forma_instauracao': 'Portaria',
               'Ano_recebimento_projudi': 2022}


def matriz_desenho(df, categoricas, binarias, continuas):
    partes = []
    for v in categoricas:
        x = pd.get_dummies(df[v].astype(object), prefix=v, prefix_sep='=', dtype=float)
        partes.append(x.drop(columns=f'{v}={REFERENCIAS[v]}'))
    partes += [df[binarias].astype(float), df[continuas].astype(float)]
    return pd.concat(partes, axis=1)


COX_CATEGORICAS = ['Comarca', 'Assunto_grupo', 'Forma_instauracao', 'Ano_recebimento_projudi']
COX_BINARIAS = ['Arma_de_fogo', 'Tentativa', 'Tramitacao_direta', 'Multiplas_vitimas', 'Houve_indiciamento']
COX_CONTINUAS = ['Idade_entrada_anos']
X_cox = matriz_desenho(dados, COX_CATEGORICAS, COX_BINARIAS, COX_CONTINUAS)
GRUPOS_REGRESSAO = {
    'Comarca': [c for c in X_cox.columns if c.startswith('Comarca=')],
    'Assunto': [c for c in X_cox.columns if c.startswith('Assunto_grupo=')],
    'Forma de instauração (APF)': [c for c in X_cox.columns if c.startswith('Forma_instauracao=')],
    'Ano de recebimento': [c for c in X_cox.columns if c.startswith('Ano_recebimento_projudi=')],
    'Arma de fogo': ['Arma_de_fogo'], 'Tentativa': ['Tentativa'], 'Tramitação direta': ['Tramitacao_direta'],
    'Múltiplas vítimas': ['Multiplas_vitimas'], 'Indiciamento': ['Houve_indiciamento'], 'Idade do IP na chegada': ['Idade_entrada_anos'],
}

# 1. Regressão linear do log do tempo (concluídos)
X_lin = sm.add_constant(X_cox.loc[evento.to_numpy()].astype(float))
y_lin = np.log1p(concluidos['Tempo_fase_judicial'].astype(float))
mqo = sm.OLS(y_lin, X_lin).fit(cov_type='HC3')
print(f'MQO de log(1 + dias), n = {int(mqo.nobs)}: R² = {mqo.rsquared:.3f}; R² ajustado = {mqo.rsquared_adj:.3f}; '
      f'teste F (HC3): p = {mqo.f_pvalue:.2e}')
display(pd.DataFrame({'Coef. (log)': mqo.params, 'Efeito multiplicativo no tempo': np.exp(mqo.params),
                      'IC 2,5%': np.exp(mqo.conf_int()[0]), 'IC 97,5%': np.exp(mqo.conf_int()[1]), 'p-valor': mqo.pvalues}).drop('const').round(3))
r2_parcial = []
for grupo, colunas in GRUPOS_REGRESSAO.items():
    reduzido = sm.OLS(y_lin, X_lin.drop(columns=colunas)).fit()
    r2_parcial.append({'Variável': grupo, 'ΔR² (perda ao retirar)': mqo.rsquared - reduzido.rsquared,
                       'R² parcial': (mqo.rsquared - reduzido.rsquared) / (1 - reduzido.rsquared)})
r2_parcial = pd.DataFrame(r2_parcial).set_index('Variável').sort_values('ΔR² (perda ao retirar)', ascending=False)
vif = pd.Series([variance_inflation_factor(X_lin.to_numpy(), i) for i in range(1, X_lin.shape[1])], index=X_lin.columns[1:])
r2_parcial['VIF (máximo do grupo)'] = [vif[GRUPOS_REGRESSAO[g]].max() for g in r2_parcial.index]
display(r2_parcial.round(4))

fig, axes = plt.subplots(1, 3, figsize=(19, 5))
axes[0].bar(range(len(r2_parcial)), 100 * r2_parcial['ΔR² (perda ao retirar)'], color=COR_PRINCIPAL)
axes[0].set_xticks(range(len(r2_parcial)), [quebrar(i, 12) for i in r2_parcial.index], fontsize=8)
axes[0].set_ylabel('pontos de R² perdidos ao retirar (%)')
axes[0].set_title(f'Importância de cada variável (R² total = {mqo.rsquared:.2f})')
axes[0].grid(axis='x', visible=False)
axes[1].scatter(mqo.fittedvalues, mqo.resid, s=14, color=COR_SECUNDARIA, edgecolor='white')
axes[1].axhline(0, color=TINTA, linewidth=1)
suave = lowess(mqo.resid, mqo.fittedvalues, frac=0.5)
axes[1].plot(suave[:, 0], suave[:, 1], color=COR_DESTAQUE, linewidth=2)
axes[1].set_xlabel('valor ajustado')
axes[1].set_ylabel('resíduo')
axes[1].set_title('Resíduos × ajustados')
(osm, osr), (a, b, _) = stats.probplot(mqo.resid, dist='norm')
axes[2].scatter(osm, osr, s=12, color=COR_PRINCIPAL)
axes[2].plot(osm, a * osm + b, color=COR_DESTAQUE)
axes[2].set_xlabel('quantis teóricos da normal')
axes[2].set_ylabel('resíduos')
axes[2].set_title(f'Q-Q dos resíduos (Shapiro p = {stats.shapiro(mqo.resid).pvalue:.2g})')
plt.tight_layout()
plt.show()
''')

code(r'''
# 2. Logística: indiciamento (autor identificado)
X_ind = pd.DataFrame({
    'APF': dados['Forma_instauracao'].astype(str).str.startswith('Auto').astype(float),
    'Tentativa': dados['Tentativa'].astype(float),
    'Arma_de_fogo': dados['Arma_de_fogo'].astype(float),
    'Homicidio_qualificado': dados['Assunto_grupo'].eq('Homicídio qualificado').astype(float),
    'Delegacia_DIH_GIH': dados['Tipo_delegacia'].eq('Especializada em homicídios (DIH/GIH)').astype(float),
    'Goiania': dados['Comarca'].eq('Goiânia').astype(float),
    'Ano_instauracao_c': dados['Ano_instauracao'].astype(float) - 2020,
})
y_ind = dados['Houve_indiciamento'].astype(int)
logit_ind = sm.Logit(y_ind, sm.add_constant(X_ind)).fit(disp=False)
or_ind = pd.DataFrame({'OR': np.exp(logit_ind.params), 'IC 2,5%': np.exp(logit_ind.conf_int()[0]),
                       'IC 97,5%': np.exp(logit_ind.conf_int()[1]), 'p-valor': logit_ind.pvalues}).drop('const')
prob = logit_ind.predict()
auc = stats.mannwhitneyu(prob[y_ind == 1], prob[y_ind == 0]).statistic / ((y_ind == 1).sum() * (y_ind == 0).sum())
decis = pd.qcut(prob, 10, duplicates='drop')
hl = pd.DataFrame({'y': y_ind, 'p': prob}).groupby(decis, observed=True).agg(obs=('y', 'sum'), esp=('p', 'sum'), n=('y', 'size'))
hl_stat = (((hl['obs'] - hl['esp']) ** 2) / (hl['esp'] * (1 - hl['esp'] / hl['n']))).sum()
print(f'Logística do indiciamento: n = {int(logit_ind.nobs)}; eventos = {int(y_ind.sum())}; LR χ² = {logit_ind.llr:.1f} '
      f'(p = {logit_ind.llr_pvalue:.2e}); pseudo-R² de McFadden = {logit_ind.prsquared:.3f}; AUC = {auc:.3f}; '
      f'Hosmer-Lemeshow χ² = {hl_stat:.2f} (gl = {len(hl) - 2}; p = {stats.chi2.sf(hl_stat, len(hl) - 2):.3f})')
display(or_ind.round(3))
display(pd.Series([variance_inflation_factor(sm.add_constant(X_ind).to_numpy(), i) for i in range(1, X_ind.shape[1] + 1)],
                  index=X_ind.columns, name='VIF').round(2).to_frame().T)

fig, axes = plt.subplots(1, 3, figsize=(19, 5))
x = np.arange(len(or_ind))
cores = [COR_PRINCIPAL if p < 0.05 else COR_SECUNDARIA for p in or_ind['p-valor']]
axes[0].bar(x, or_ind['OR'], color=cores, width=0.6)
axes[0].errorbar(x, or_ind['OR'], yerr=[or_ind['OR'] - or_ind['IC 2,5%'], or_ind['IC 97,5%'] - or_ind['OR']], fmt='none',
                 ecolor=TINTA, capsize=4)
axes[0].axhline(1, color=COR_DESTAQUE, linestyle='--')
axes[0].set_yscale('log')
axes[0].set_xticks(x, [quebrar(c, 11) for c in or_ind.index], fontsize=8)
axes[0].set_ylabel('razão de chances (escala log) e IC 95%')
axes[0].set_title('Chance de haver indiciado (azul escuro: p < 0,05)')
axes[0].grid(axis='x', visible=False)
limiares = np.r_[1.01, np.sort(prob)[::-1], -0.01]
axes[1].plot([(prob[y_ind == 0] >= l).mean() for l in limiares], [(prob[y_ind == 1] >= l).mean() for l in limiares],
             color=COR_PRINCIPAL, linewidth=2, label=f'modelo (AUC = {auc:.2f})')
axes[1].plot([0, 1], [0, 1], color=TINTA_2, linestyle='--', label='acaso (AUC = 0,5)')
axes[1].set_xlabel('1 − especificidade')
axes[1].set_ylabel('sensibilidade')
axes[1].set_title('Curva ROC')
axes[1].legend()
axes[2].bar(np.arange(len(hl)) - 0.2, hl['obs'], width=0.4, color=COR_PRINCIPAL, label='observados')
axes[2].bar(np.arange(len(hl)) + 0.2, hl['esp'], width=0.4, color=COR_SECUNDARIA, label='esperados pelo modelo')
axes[2].set_xlabel('decil de probabilidade prevista')
axes[2].set_ylabel('inquéritos com indiciado')
axes[2].set_title('Calibração (Hosmer-Lemeshow)')
axes[2].legend()
axes[2].grid(axis='x', visible=False)
plt.tight_layout()
plt.show()
''')

code(r'''
# 3. Denúncia × arquivamento: logística de Firth, uma variável por vez
def logistica_firth(X, y, max_iter=200, tol=1e-8):
    """Regressão logística com penalização de Firth (Jeffreys): estimativas finitas mesmo com separação."""
    X, y = np.asarray(X, float), np.asarray(y, float)
    beta = np.zeros(X.shape[1])
    for _ in range(max_iter):
        p = 1 / (1 + np.exp(-X @ beta))
        W = p * (1 - p)
        info_inv = np.linalg.inv(X.T @ (X * W[:, None]))
        h = W * np.einsum('ij,jk,ik->i', X, info_inv, X)
        passo = info_inv @ (X.T @ (y - p + h * (0.5 - p)))
        beta += passo
        if np.max(np.abs(passo)) < tol:
            break
    p = 1 / (1 + np.exp(-X @ beta))
    info = X.T @ (X * (p * (1 - p))[:, None])
    loglik_pen = (y * np.log(p) + (1 - y) * np.log(1 - p)).sum() + 0.5 * np.linalg.slogdet(info)[1]
    return beta, np.sqrt(np.diag(np.linalg.inv(info))), loglik_pen


concl_denuncia = dados[dados['Tipo_desfecho'].isin(['Denúncia', 'Arquivamento'])]
y_den = concl_denuncia['Tipo_desfecho'].eq('Denúncia').astype(int).to_numpy()
firth = []
for nome, x in {'APF': concl_denuncia['Forma_instauracao'].astype(str).str.startswith('Auto'),
                'Réu preso': concl_denuncia['Reu_preso'], 'Com indiciado': concl_denuncia['Houve_indiciamento'],
                'Tentativa': concl_denuncia['Tentativa'], 'Arma de fogo': concl_denuncia['Arma_de_fogo'],
                'Instaurado a partir de 2022': concl_denuncia['Ano_instauracao'].ge(2022)}.items():
    X = np.c_[np.ones(len(y_den)), x.astype(float).to_numpy()]
    beta, ep, ll = logistica_firth(X, y_den)
    _, _, ll0 = logistica_firth(X[:, :1], y_den)
    firth.append({'Variável': nome, 'Denúncias com o atributo': int(y_den[x.astype(bool).to_numpy()].sum()),
                  'OR (Firth)': np.exp(beta[1]), 'IC 2,5%': np.exp(beta[1] - 1.96 * ep[1]), 'IC 97,5%': np.exp(beta[1] + 1.96 * ep[1]),
                  'p (razão de verossimilhança penalizada)': stats.chi2.sf(max(2 * (ll - ll0), 0), 1)})
print(f'Denúncia × arquivamento: {y_den.sum()} denúncias e {len(y_den) - y_den.sum()} arquivamentos — uma variável por vez')
with pd.option_context('display.float_format', lambda v: f'{v:.4g}'):
    display(pd.DataFrame(firth).set_index('Variável'))

# 4. Prescrição × demais arquivamentos: o mesmo procedimento (10 eventos)
arquivados = dados[dados['Status_macro'].eq('Arquivado')]
y_presc = arquivados['Status_projudi'].eq('Arquivado: extinção da punibilidade (prescrição)').astype(int).to_numpy()
firth_presc = []
for nome, x in {'Idade do fato na conclusão (anos)': (arquivados['Data_conclusao_mp'] - arquivados['Data_fato']).dt.days / 365.25,
                'Idade do IP na chegada (anos)': arquivados['Idade_entrada_anos'].astype(float),
                'Sem indiciado': ~arquivados['Houve_indiciamento'].astype(bool),
                'Comarca de Goiânia': arquivados['Comarca'].eq('Goiânia'),
                'Homicídio qualificado': arquivados['Assunto_grupo'].eq('Homicídio qualificado')}.items():
    x = x.astype(float)
    validos = x.notna().to_numpy()
    X = np.c_[np.ones(validos.sum()), x[validos].to_numpy()]
    beta, ep, ll = logistica_firth(X, y_presc[validos])
    _, _, ll0 = logistica_firth(X[:, :1], y_presc[validos])
    firth_presc.append({'Variável': nome, 'OR (Firth)': np.exp(beta[1]), 'IC 2,5%': np.exp(beta[1] - 1.96 * ep[1]),
                        'IC 97,5%': np.exp(beta[1] + 1.96 * ep[1]), 'p (razão de verossimilhança penalizada)': stats.chi2.sf(max(2 * (ll - ll0), 0), 1)})
print(f'Prescrição × demais arquivamentos: {y_presc.sum()} prescrições entre {len(y_presc)} arquivados — uma variável por vez '
      '(variáveis contínuas: OR por ano)')
with pd.option_context('display.float_format', lambda v: f'{v:.4g}'):
    display(pd.DataFrame(firth_presc).set_index('Variável'))
''')

interp('rg_regressoes')

# =====================================================================
md(r'''
---

## 20. Análise de Sobrevivência: Incluindo os Procedimentos Não Concluídos

### 20.1 Por que outra abordagem

As seções 15 a 19 usaram só os concluídos. Isso **encurta** o tempo, porque os 26 censurados estão justamente entre os mais longos. A **análise de sobrevivência** usa toda a informação: o concluído contribui com o tempo exato, e o censurado contribui com o fato de que seu tempo é **maior** que o observado.

- **Função de sobrevivência** S(t) = P(T > t): a proporção de procedimentos **ainda não concluídos** após t dias. A curva **começa em 1 e desce** à medida que os procedimentos são concluídos.
- **Kaplan-Meier:** estimador de S(t) sem supor distribuição. A **mediana** é o tempo em que a curva cruza 0,5.
- **Log-rank:** compara curvas de dois ou mais grupos. É o equivalente do Mann-Whitney/Kruskal-Wallis para dados censurados.
- **Modelo de Cox:** estima a **razão de riscos** (HR) de cada variável, com as demais constantes. HR > 1 significa conclusão **mais rápida** (a curva desce mais depressa).

Esta seção usa a **fase judicial**, que é observada desde a chegada ao Projudi. O tempo total exige um ajuste a mais, que fica para a seção 21.
''')

code(r'''
def mediana_ic(km):
    ic = median_survival_times(km.confidence_interval_)
    return km.median_survival_time_, float(ic.iloc[0, 0]), float(ic.iloc[0, 1])


km_judicial = KaplanMeierFitter().fit(T_JUD, EVENTO, label='Kaplan-Meier (com os 26 censurados)')
km_ingenuo_jud = KaplanMeierFitter().fit(T_JUD[evento], label='só os concluídos')
fig, ax = plt.subplots(figsize=(12, 5.2))
km_ingenuo_jud.plot_survival_function(ax=ax, color=COR_SECUNDARIA, ci_show=False, linewidth=2)
km_judicial.plot_survival_function(ax=ax, color=COR_PRINCIPAL, linewidth=2.4)
censurados = T_JUD[~evento]
ax.plot(censurados, km_judicial.survival_function_at_times(censurados).to_numpy(), '|', color=COR_DESTAQUE, markersize=13,
        markeredgewidth=2, label=f'censura (n = {len(censurados)})')
m, li, ls = mediana_ic(km_judicial)
ax.axhline(0.5, color=TINTA_2, linestyle='--', linewidth=1)
ax.axvline(m, color=COR_PRINCIPAL, linestyle=':', linewidth=1.5)
ax.axvline(km_ingenuo_jud.median_survival_time_, color=COR_SECUNDARIA, linestyle=':', linewidth=1.5)
ax.set_xlabel('dias desde a chegada ao Projudi')
ax.set_ylabel('S(t): proporção ainda não concluída')
ax.set_title(f'Fase judicial: mediana de Kaplan-Meier = {m:.0f} dias (IC {li:.0f}–{ls:.0f}) × '
             f'{km_ingenuo_jud.median_survival_time_:.0f} dias só com concluídos')
ax.set_ylim(0, 1.02)
ax.legend()
plt.tight_layout()
plt.show()
display(pd.DataFrame([{'Estimador': k.label, 'Mediana (dias)': mediana_ic(k)[0], 'IC 2,5%': mediana_ic(k)[1],
                       'IC 97,5%': mediana_ic(k)[2], 'Q1 (dias)': k.percentile(0.75), 'Q3 (dias)': k.percentile(0.25)}
                      for k in [km_ingenuo_jud, km_judicial]]).set_index('Estimador').round(0))
''')

md(r'''
### 20.2 Curvas por grupo: Kaplan-Meier, log-rank e Cox

Cada painel mostra as curvas de sobrevivência de um grupo e, no título:

- o **log-rank** (H₀: curvas iguais);
- a **razão de riscos** de um modelo de Cox com aquela única variável, quando ela tem dois grupos. HR > 1 indica que o segundo grupo conclui mais depressa.

Os p-valores do log-rank são corrigidos por Benjamini-Hochberg. Nas variáveis com mais de dois grupos, os pares são comparados por log-rank com ajuste de Holm.
''')

code(r'''
def grade_km(df, duracao, ev, variaveis, titulo, colunas=4, x_max=None):
    linhas_tab, n_linhas = [], int(np.ceil(len(variaveis) / colunas))
    fig, axes = plt.subplots(n_linhas, colunas, figsize=(4.6 * colunas, 3.8 * n_linhas), sharey=True, squeeze=False)
    duracao, ev = pd.Series(np.asarray(duracao, float), index=df.index), pd.Series(np.asarray(ev, int), index=df.index)
    for ax, v in zip(axes.flat, variaveis):
        grupos = serie_exibicao(df, v).astype(object).where(df[v].notna(), None)
        validos = grupos.notna()
        teste = multivariate_logrank_test(duracao[validos], grupos[validos].astype(str), ev[validos])
        ordem = [g for g in (serie_exibicao(df, v).cat.categories if isinstance(serie_exibicao(df, v).dtype, pd.CategoricalDtype)
                             else pd.unique(grupos[validos])) if (grupos == g).sum() > 0]
        texto_hr = ''
        if len(ordem) == 2:
            base = pd.DataFrame({'T': duracao[validos], 'E': ev[validos], 'X': grupos[validos].eq(ordem[1]).astype(float)})
            cox_u = CoxPHFitter().fit(base, 'T', 'E')
            texto_hr = f'; HR = {cox_u.hazard_ratios_["X"]:.2f}'
        for g, cor in zip(ordem, CORES * 2):
            idx = grupos.index[grupos == g]
            km = KaplanMeierFitter().fit(duracao[idx], ev[idx])
            ax.step(km.survival_function_.index, km.survival_function_.iloc[:, 0], where='post', color=cor, linewidth=1.8,
                    label=f'{quebrar(str(g), 24)} (n={len(idx)})')
            ic = median_survival_times(km.confidence_interval_)
            linhas_tab.append({'Variável': ROTULO_VARIAVEL.get(v, v), 'Grupo': g, 'n': len(idx), 'Eventos': int(ev[idx].sum()),
                               'Mediana KM': km.median_survival_time_, 'IC 2,5%': float(ic.iloc[0, 0]),
                               'IC 97,5%': float(ic.iloc[0, 1]), 'p log-rank': teste.p_value})
        ax.axhline(0.5, color=TINTA_2, linestyle='--', linewidth=0.8)
        ax.set_ylim(0, 1.02)
        if x_max:
            ax.set_xlim(0, x_max)
        ax.set_title(f'{quebrar(ROTULO_VARIAVEL.get(v, v), 34)}\nlog-rank p = {teste.p_value:.3g}{texto_hr}', fontsize=9.5)
        ax.legend(fontsize=7, loc='upper right')
        ax.set_xlabel('dias', fontsize=8.5)
    for ax in axes[:, 0]:
        ax.set_ylabel('S(t)')
    for ax in list(axes.flat)[len(variaveis):]:
        ax.set_visible(False)
    plt.suptitle(titulo, fontweight='bold', y=1.0)
    plt.tight_layout()
    plt.show()
    return pd.DataFrame(linhas_tab)


km_jud_var = grade_km(dados, T_JUD, EVENTO, VARIAVEIS_CASO + VARIAVEIS_CALENDARIO,
                      'Fase judicial: Kaplan-Meier por variável (proporção ainda não concluída)')
logrank_jud = km_jud_var.groupby('Variável', sort=False)['p log-rank'].first().to_frame()
logrank_jud['p BH'] = multipletests(logrank_jud['p log-rank'], method='fdr_bh')[1]
display(logrank_jud.sort_values('p log-rank').round(4))
with pd.option_context('display.max_rows', 90):
    display(km_jud_var.drop(columns='p log-rank').set_index(['Variável', 'Grupo']).round(0))

print('Comparações par a par (log-rank, Holm) nas variáveis com mais de dois grupos e log-rank significativo após BH:')
for v in VARIAVEIS_CASO + VARIAVEIS_CALENDARIO:
    rotulo = ROTULO_VARIAVEL.get(v, v)
    grupos = serie_exibicao(dados, v)
    if grupos.nunique() <= 2 or logrank_jud.loc[rotulo, 'p BH'] >= 0.05:
        continue
    validos = grupos.notna()
    pares = pairwise_logrank_test(T_JUD[validos], grupos[validos].astype(str), EVENTO[validos]).summary
    pares['p Holm'] = multipletests(pares['p'], method='holm')[1]
    print(f'\n{rotulo}')
    display(pares[['test_statistic', 'p', 'p Holm']].sort_values('p').round(4))

km_proc = grade_km(dados, T_JUD, EVENTO, VARIAVEIS_PROCESSO, 'Variáveis do processo no MP (descritivas, não causais)')
''')

interp('sv_km_judicial')

md(r'''
### 20.3 Modelo de Cox multivariável

O Cox estima o efeito de cada variável **mantendo as outras constantes**:

- **Variáveis:** entram só as conhecidas na chegada ao Projudi. `Reu_preso` fica de fora, porque 19 dos 21 presos vêm de APF e a colinearidade inflaria os erros.
- **Tamanho:** são 192 eventos para 17 parâmetros, o que respeita a regra de pelo menos 10 eventos por parâmetro.
- **Ajuste:** concordância C e pseudo-R² de Nagelkerke.
- **Pressuposto de riscos proporcionais:** verificado pelos **resíduos de Schoenfeld**; as violações são corrigidas por **estratificação**.
- **Gráfico:** as **curvas de sobrevivência previstas pelo Cox** para os efeitos principais, com as demais variáveis na média.
''')

code(r'''
def nagelkerke(ll_modelo, ll_nulo, n):
    cox_snell = 1 - np.exp(2 * (ll_nulo - ll_modelo) / n)
    return cox_snell, cox_snell / (1 - np.exp(2 * ll_nulo / n))


def grafico_floresta(tabela, titulo, coluna='HR', referencia=1, rotulo_x='HR (escala log) — IC 95%'):
    tabela = tabela.iloc[::-1]
    fig, ax = plt.subplots(figsize=(9.5, 0.36 * len(tabela) + 1.4))
    y = np.arange(len(tabela))
    cores = np.where(tabela['p-valor'] < 0.05, COR_PRINCIPAL, TINTA_2)
    ax.hlines(y, tabela['IC 2,5%'], tabela['IC 97,5%'], color=cores, linewidth=2.2)
    ax.scatter(tabela[coluna], y, color=cores, s=40, zorder=3)
    ax.axvline(referencia, color=TINTA, linewidth=1)
    ax.set_xscale('log')
    ax.set_yticks(y, [quebrar(str(i), 42) for i in tabela.index], fontsize=8.5)
    ax.set_xlabel(rotulo_x)
    ax.set_title(titulo)
    ax.grid(axis='y', visible=False)
    plt.tight_layout()
    plt.show()


base_cox = X_cox.assign(T=T_JUD, E=EVENTO)
cox_jud = CoxPHFitter().fit(base_cox, 'T', 'E')
resumo_cox = cox_jud.summary[['exp(coef)', 'exp(coef) lower 95%', 'exp(coef) upper 95%', 'p']].set_axis(
    ['HR', 'IC 2,5%', 'IC 97,5%', 'p-valor'], axis=1)
ll_nulo_cox = cox_jud.log_likelihood_ - cox_jud.log_likelihood_ratio_test().test_statistic / 2
cs, nk = nagelkerke(cox_jud.log_likelihood_, ll_nulo_cox, len(base_cox))
print(f'n = {len(base_cox)}; eventos = {int(EVENTO.sum())}; C = {cox_jud.concordance_index_:.3f}; pseudo-R² de Nagelkerke = {nk:.3f}; '
      f'razão de verossimilhança: p = {cox_jud.log_likelihood_ratio_test().p_value:.2e}')
display(resumo_cox.round(3))
grafico_floresta(resumo_cox, 'Cox — fase judicial (azul: p < 0,05; HR > 1 = conclusão mais rápida)')

importancia_cox = []
for grupo, colunas in GRUPOS_REGRESSAO.items():
    reduzido = CoxPHFitter().fit(base_cox.drop(columns=colunas), 'T', 'E')
    lr = 2 * (cox_jud.log_likelihood_ - reduzido.log_likelihood_)
    importancia_cox.append({'Variável': grupo, 'LR χ² (perda ao retirar)': lr, 'gl': len(colunas),
                            'p-valor': stats.chi2.sf(lr, len(colunas)), 'ΔC': cox_jud.concordance_index_ - reduzido.concordance_index_})
display(pd.DataFrame(importancia_cox).set_index('Variável').sort_values('LR χ² (perda ao retirar)', ascending=False).round(4))
''')

code(r'''
# Curvas de sobrevivência previstas pelo Cox (demais variáveis na média)
EFEITOS_CURVA = [('Forma_instauracao=Auto de prisão em flagrante (APF)', [0, 1], ['Portaria', 'APF']),
                 ('Comarca=Aparecida de Goiânia', [0, 1], ['Goiânia (ref.) e demais', 'Aparecida de Goiânia']),
                 ('Arma_de_fogo', [0, 1], ['Sem arma de fogo', 'Com arma de fogo']),
                 ('Idade_entrada_anos', [0, 5, 15], ['0 ano', '5 anos', '15 anos'])]
fig, axes = plt.subplots(1, 4, figsize=(20, 4.8), sharey=True)
for ax, (coluna, valores, rotulos) in zip(axes, EFEITOS_CURVA):
    perfil = base_cox.drop(columns=['T', 'E']).mean().to_frame().T
    perfis = pd.concat([perfil.assign(**{coluna: v}) for v in valores], ignore_index=True)
    curvas = cox_jud.predict_survival_function(perfis, times=np.linspace(0, T_JUD.max(), 300))
    for (_, curva), rotulo, cor in zip(curvas.items(), rotulos, CORES):
        ax.plot(curvas.index, curva, color=cor, linewidth=2.2, label=rotulo)
    hr = resumo_cox.loc[coluna]
    ax.set_title(f'{quebrar(coluna, 34)}\nHR = {hr["HR"]:.2f} (IC {hr["IC 2,5%"]:.2f}–{hr["IC 97,5%"]:.2f}); p = {hr["p-valor"]:.3g}',
                 fontsize=9.5)
    ax.axhline(0.5, color=TINTA_2, linestyle='--', linewidth=0.8)
    ax.set_xlabel('dias desde a chegada ao Projudi')
    ax.legend(fontsize=8)
axes[0].set_ylabel('S(t) prevista pelo Cox')
plt.suptitle('Curvas de sobrevivência ajustadas pelo modelo de Cox', fontweight='bold')
plt.tight_layout()
plt.show()
''')

code(r'''
# Pressuposto de riscos proporcionais (resíduos de Schoenfeld) e Cox estratificado
ph = proportional_hazard_test(cox_jud, base_cox, time_transform='rank').summary[['test_statistic', 'p']].set_axis(['χ² (1 gl)', 'p-valor'], axis=1)
ph['Viola (p < 0,05)'] = ph['p-valor'] < 0.05
display(ph.round(4))
violadoras = list(ph.index[ph['Viola (p < 0,05)']])
residuos = cox_jud.compute_residuals(base_cox, 'scaled_schoenfeld')
postos = stats.rankdata(base_cox.loc[residuos.index, 'T'])
if violadoras:
    fig, axes = plt.subplots(1, len(violadoras), figsize=(4.4 * len(violadoras), 3.8), squeeze=False)
    for ax, v in zip(axes[0], violadoras):
        ax.scatter(postos, residuos[v], s=10, color=COR_SECUNDARIA)
        suave = lowess(residuos[v], postos, frac=0.4)
        ax.plot(suave[:, 0], suave[:, 1], color=COR_DESTAQUE, linewidth=2)
        ax.axhline(cox_jud.params_[v], color=TINTA, linestyle='--', linewidth=1)
        ax.set_title(quebrar(v, 30), fontsize=9.5)
        ax.set_xlabel('posto do tempo')
    axes[0][0].set_ylabel('resíduo de Schoenfeld escalonado')
    plt.suptitle('Efeitos que mudam no tempo (tracejado = efeito médio do Cox)', fontweight='bold')
    plt.tight_layout()
    plt.show()

VARIAVEIS_ESTRATO = [v for v in COX_CATEGORICAS if ph.loc[[c for c in ph.index if c.startswith(f'{v}=')], 'Viola (p < 0,05)'].mean() > 0.5]
print(f'Estratificação pela variável cuja maioria dos níveis viola o pressuposto: {VARIAVEIS_ESTRATO or "nenhuma"}')
if VARIAVEIS_ESTRATO:
    X_estr = matriz_desenho(dados, [v for v in COX_CATEGORICAS if v not in VARIAVEIS_ESTRATO], COX_BINARIAS, COX_CONTINUAS)
    base_estr = X_estr.assign(T=T_JUD, E=EVENTO, **{v: dados[v].astype(str) for v in VARIAVEIS_ESTRATO})
    cox_estr = CoxPHFitter().fit(base_estr, 'T', 'E', strata=VARIAVEIS_ESTRATO)
    resumo_estr = cox_estr.summary[['exp(coef)', 'exp(coef) lower 95%', 'exp(coef) upper 95%', 'p']].set_axis(
        ['HR', 'IC 2,5%', 'IC 97,5%', 'p-valor'], axis=1)
    ph_estr = proportional_hazard_test(cox_estr, base_estr, time_transform='rank').summary['p']
    display(pd.concat({'Cox simples': resumo_cox, 'Cox estratificado': resumo_estr.assign(**{'p PH': ph_estr})}, axis=1).round(3))
''')

interp('sv_cox')

md(r'''
### 20.4 Distribuições paramétricas com censura e modelos AFT

A seção 18 ajustou as famílias aos concluídos. Agora o ajuste usa a **verossimilhança com censura**: os concluídos contribuem com a densidade f(t), e os censurados com a sobrevivência S(t).

- **Diagnóstico visual:** as curvas de sobrevivência ajustadas são comparadas com o Kaplan-Meier.
- **Resíduos de Cox-Snell:** se o modelo está certo, eles se comportam como uma exponencial(1), e o risco acumulado estimado fica sobre a diagonal.
- **Modelos AFT:** modelam o tempo diretamente, sem supor riscos proporcionais. O coeficiente exponenciado é uma **razão de tempos** (TR): 1,5 significa 50% mais tempo.
''')

code(r'''
class GamaFitter(ParametricUnivariateFitter):
    """Gama (forma k, escala θ) com censura e entrada tardia; S(t) = Q(k, t/θ)."""
    _fitted_parameter_names = ['k_', 'theta_']
    _bounds = [(1e-6, None), (1e-6, None)]
    label = 'Gama'

    def _cumulative_hazard(self, params, times):
        k, theta = params
        return -gammainccln(k, times / theta)

    def percentile(self, p):
        return float(stats.gamma.isf(p, self.k_, scale=self.theta_))

    @property
    def median_survival_time_(self):
        return self.percentile(0.5)


FAMILIAS = {
    'Exponencial': (ExponentialFitter, 1), 'Weibull': (WeibullFitter, 2), 'Gama': (GamaFitter, 2),
    'Lognormal': (LogNormalFitter, 2), 'Log-logística': (LogLogisticFitter, 2), 'Gama generalizada': (GeneralizedGammaFitter, 3),
}


def ajustar_familias(t, e, entrada=None):
    ajustes, linhas = {}, []
    for nome, (classe, k) in FAMILIAS.items():
        modelo = classe().fit(t, e, entry=entrada)
        ajustes[nome] = modelo
        linhas.append({'Família': nome, 'Parâmetros': k, 'log-verossimilhança': modelo.log_likelihood_,
                       'AIC': -2 * modelo.log_likelihood_ + 2 * k, 'BIC': -2 * modelo.log_likelihood_ + k * np.log(len(t)),
                       'Mediana (dias)': float(modelo.median_survival_time_),
                       'Estimativas': ', '.join(f'{p.rstrip("_")} = {v:.3g}' for p, v in modelo.params_.items())})
    tabela = pd.DataFrame(linhas).set_index('Família').sort_values('AIC')
    tabela['ΔAIC'], tabela['ΔBIC'] = tabela['AIC'] - tabela['AIC'].min(), tabela['BIC'] - tabela['BIC'].min()
    return ajustes, tabela


def razao_verossimilhanca(ajustes):
    gg = ajustes['Gama generalizada'].log_likelihood_
    testes = []
    for restrito, gl, hipotese in [('Weibull', 1, 'λ = 1'), ('Lognormal', 1, 'λ = 0'), ('Gama', 1, 'λ = σ'),
                                   ('Exponencial', 2, 'λ = 1 e σ = 1')]:
        lr = 2 * (gg - ajustes[restrito].log_likelihood_)
        testes.append({'H₀ (modelo restrito)': f'{restrito} ({hipotese})', 'LR': lr, 'gl': gl, 'p-valor': stats.chi2.sf(max(lr, 0), gl)})
    return pd.DataFrame(testes).set_index('H₀ (modelo restrito)')


def diagnostico_sobrevivencia(t, e, ajustes, km, titulo, entrada=None, familias=('Gama generalizada', 'Weibull', 'Lognormal', 'Gama')):
    fig, axes = plt.subplots(1, 2, figsize=(16, 5))
    grade = np.linspace(0.5, np.asarray(t).max(), 500)
    km.plot_survival_function(ax=axes[0], color=TINTA, ci_show=True, linewidth=2.2, label='Kaplan-Meier')
    for nome, cor in zip(familias, CORES):
        axes[0].plot(grade, ajustes[nome].survival_function_at_times(grade), color=cor, linewidth=1.7, label=nome)
    axes[0].set_xlabel('dias')
    axes[0].set_ylabel('S(t)')
    axes[0].set_ylim(0, 1.02)
    axes[0].set_title(f'{titulo}: Kaplan-Meier × sobrevivência ajustada')
    axes[0].legend(fontsize=8.5)
    for nome, cor in zip(familias[:3], CORES):
        modelo = ajustes[nome]
        r = modelo.cumulative_hazard_at_times(np.asarray(t)).to_numpy()
        r0 = None if entrada is None else modelo.cumulative_hazard_at_times(np.maximum(np.asarray(entrada), 1e-9)).to_numpy()
        na = NelsonAalenFitter().fit(r, e, entry=r0)
        axes[1].step(na.cumulative_hazard_.index, na.cumulative_hazard_.iloc[:, 0], where='post', color=cor, label=nome)
    lim = axes[1].get_xlim()[1]
    axes[1].plot([0, lim], [0, lim], color=TINTA, linestyle='--', linewidth=1)
    axes[1].set_xlabel('resíduo de Cox-Snell')
    axes[1].set_ylabel('risco acumulado (Nelson-Aalen)')
    axes[1].set_title('Resíduos de Cox-Snell (ideal: diagonal)')
    axes[1].legend(fontsize=8.5)
    plt.tight_layout()
    plt.show()


ajustes_jud, tabela_jud = ajustar_familias(T_JUD, EVENTO)
display(tabela_jud.round(2))
with pd.option_context('display.float_format', lambda v: f'{v:.4g}'):
    display(razao_verossimilhanca(ajustes_jud))
diagnostico_sobrevivencia(T_JUD, EVENTO, ajustes_jud, km_judicial, 'Fase judicial (com censura)')
''')

code(r'''
base_aft = X_cox.copy()
base_aft.columns = [re.sub(r'\W+', '_', unicodedata.normalize('NFKD', c).encode('ascii', 'ignore').decode()).strip('_') for c in base_aft.columns]
NOMES_AFT = dict(zip(base_aft.columns, X_cox.columns))
base_aft = base_aft.assign(T=T_JUD.to_numpy(), E=EVENTO.to_numpy())
modelos_aft = {
    'Weibull AFT': WeibullAFTFitter().fit(base_aft, 'T', 'E'),
    'Lognormal AFT': LogNormalAFTFitter().fit(base_aft, 'T', 'E'),
    'Log-logística AFT': LogLogisticAFTFitter().fit(base_aft, 'T', 'E'),
    'Gama generalizada AFT': GeneralizedGammaRegressionFitter(penalizer=1e-4).fit(
        base_aft, 'T', 'E', regressors={'mu_': ' + '.join(NOMES_AFT), 'sigma_': '1', 'lambda_': '1'}),
}
NULOS_AFT = {'Weibull AFT': WeibullFitter, 'Lognormal AFT': LogNormalFitter, 'Log-logística AFT': LogLogisticFitter,
             'Gama generalizada AFT': GeneralizedGammaFitter}
comparacao_aft = pd.DataFrame({nome: {'log-verossimilhança': m.log_likelihood_, 'AIC': m.AIC_, 'Parâmetros': len(m.params_),
                                      'pseudo-R² de Nagelkerke': nagelkerke(m.log_likelihood_, NULOS_AFT[nome]().fit(T_JUD, EVENTO).log_likelihood_,
                                                                           len(T_JUD))[1]}
                               for nome, m in modelos_aft.items()}).T.sort_values('AIC')
comparacao_aft['ΔAIC'] = comparacao_aft['AIC'] - comparacao_aft['AIC'].min()
display(comparacao_aft.round(3))
melhor_aft = comparacao_aft.index[0]
parametro_local = {'Weibull AFT': 'lambda_', 'Lognormal AFT': 'mu_', 'Log-logística AFT': 'alpha_', 'Gama generalizada AFT': 'mu_'}
tabelas_tr = {}
for nome in [melhor_aft, 'Weibull AFT']:
    s = modelos_aft[nome].summary.loc[parametro_local[nome]].drop(index='Intercept', errors='ignore')
    tabelas_tr[nome] = pd.DataFrame({'TR': np.exp(s['coef']), 'IC 2,5%': np.exp(s['coef lower 95%']),
                                     'IC 97,5%': np.exp(s['coef upper 95%']), 'p-valor': s['p']}).rename(index=NOMES_AFT)
display(pd.concat(tabelas_tr, axis=1).round(3))
grafico_floresta(tabelas_tr[melhor_aft], f'{melhor_aft} — razão de tempos (TR > 1 = mais demorado)', coluna='TR',
                 rotulo_x='razão de tempos (escala log) — IC 95%')
''')

interp('sv_aft')

# =====================================================================
md(r'''
---

## 21. Tópico Avançado: a Janela de Observação e o Tempo Total

### 21.1 Diagrama de Lexis

A fase judicial é observada desde o início. O **tempo total** não. A base reúne os procedimentos que **chegaram ao Projudi** entre 2022 e 2025: um IP instaurado em 2005 só está na amostra porque ainda não tinha terminado em 2022, e os de 2005 que terminaram antes **nunca poderiam** ter sido amostrados. O diagrama de Lexis mostra cada inquérito como um segmento:

- o trecho pontilhado vai da instauração à chegada ao Projudi e fica **fora** da observação;
- o trecho cheio é o período efetivamente observado.
''')

code(r'''
fig, ax = plt.subplots(figsize=(13, 6.2))
for i, linha in dados.sort_values('Data_instauracao').iterrows():
    x0, x1, x2 = linha['Data_instauracao'], linha['Data_recebimento_projudi'], fim_observado[i]
    y1, y2 = linha['Tempo_conclusao_ip'] / 365.25, linha['Tempo_total'] / 365.25
    cor = COR_PRINCIPAL if linha['Concluido_mp'] else COR_DESTAQUE
    ax.plot([x0, x1], [0, y1], color=GRADE, linewidth=0.7, linestyle=':', zorder=1)
    ax.plot([x1, x2], [y1, y2], color=cor, linewidth=1.3, zorder=2)
    ax.plot(x2, y2, marker='o' if linha['Concluido_mp'] else '>', markersize=3.2, color=cor, zorder=3)
inicio_janela = dados['Data_recebimento_projudi'].min()
ax.axvspan(inicio_janela, DATA_REFERENCIA, color=COR_SECUNDARIA, alpha=0.18, zorder=0)
ax.plot([], [], color=COR_PRINCIPAL, marker='o', label='Concluído no MP (evento)')
ax.plot([], [], color=COR_DESTAQUE, marker='>', label='Em curso na coleta (censurado)')
ax.plot([], [], color=GRADE, linestyle=':', label='Instauração → Projudi (não observado)')
ax.set_xlabel('data do calendário')
ax.set_ylabel('anos desde a instauração')
ax.set_title('Diagrama de Lexis: o inquérito só entra na amostra quando chega ao Projudi (faixa azul = janela)')
ax.legend(loc='upper left')
plt.tight_layout()
plt.show()
''')

md(r'''
### 21.2 Censura e truncamento: três estimativas do tempo total

A seleção pela chegada ao Projudi cria **truncamento à esquerda** (*entrada tardia*): um inquérito só pode ser observado se a duração total superar o tempo até a chegada ao Projudi. O Kaplan-Meier corrige isso quando cada caso entra no conjunto de risco só a partir da sua idade na chegada. Três estimativas, da mais ingênua à mais completa:

1. só os concluídos;
2. Kaplan-Meier com censura;
3. Kaplan-Meier com censura e **entrada tardia**. Esta só vale se a idade na chegada não alterar o risco de conclusão dali em diante, a chamada **quase-independência**, testada na 21.3.
''')

code(r'''
assert (ENTRADA < T_TOTAL).all()
km_ingenuo = KaplanMeierFitter().fit(T_TOTAL[evento], label='1. Só concluídos')
km_censura = KaplanMeierFitter().fit(T_TOTAL, EVENTO, label='2. Com censura')
km_truncado = KaplanMeierFitter().fit(T_TOTAL, EVENTO, entry=ENTRADA, label='3. Com censura e entrada tardia')
display(pd.DataFrame([(k.label, *mediana_ic(k)) for k in [km_ingenuo, km_censura, km_truncado]],
                     columns=['Estimador', 'Mediana (dias)', 'IC 2,5%', 'IC 97,5%']).set_index('Estimador').round(0))
fig, axes = plt.subplots(1, 2, figsize=(16, 5))
for km, cor in zip([km_ingenuo, km_censura, km_truncado], CORES):
    km.plot_survival_function(ax=axes[0], color=cor, ci_show=km is not km_ingenuo, linewidth=2)
axes[0].axhline(0.5, color=TINTA_2, linestyle='--', linewidth=1)
axes[0].set_xlabel('dias desde a instauração')
axes[0].set_ylabel('S(t)')
axes[0].set_ylim(0, 1.02)
axes[0].set_title('Tempo total: o estimador muda a resposta')
risco = pd.Series({t: int(((ENTRADA <= t) & (T_TOTAL >= t)).sum()) for t in np.arange(0, 9001, 15)})
axes[1].plot(risco.index / 365.25, risco.values, color=COR_PRINCIPAL, linewidth=2)
axes[1].set_xlabel('anos desde a instauração')
axes[1].set_ylabel('inquéritos em risco')
axes[1].set_title('Conjunto de risco com entrada tardia (já no Projudi e não concluídos)')
plt.tight_layout()
plt.show()
''')

md(r'''
### 21.3 Teste de quase-independência (Tsai, 1990)

A cada conclusão observada, o teste compara a idade na chegada de quem concluiu com a dos demais inquéritos em risco naquele instante. A estatística é um tau de Kendall condicional:

- **perto de zero:** compatível com quase-independência;
- **negativo:** quem chegou ao Projudi mais velho conclui **antes**, e a correção por entrada tardia deixa de valer.
''')

code(r'''
def teste_tsai(entrada, saida, evento):
    entrada, saida, evento = map(np.asarray, (entrada, saida, evento))
    k_total, variancia, pares = 0.0, 0.0, 0
    for i in np.flatnonzero(evento):
        risco = (entrada <= saida[i]) & (saida >= saida[i])
        r = risco.sum()
        k_total += np.sign(entrada[risco] - entrada[i]).sum()
        variancia += (r ** 2 - 1) / 3
        pares += r - 1
    z = k_total / np.sqrt(variancia)
    return {'K': k_total, 'Pares comparáveis': pares, 'tau condicional': k_total / pares, 'z': z, 'p-valor': 2 * stats.norm.sf(abs(z))}


coorte_2022 = dados['Ano_instauracao'].ge(2022).to_numpy()
display(pd.DataFrame({
    'Amostra completa': teste_tsai(ENTRADA, T_TOTAL, EVENTO),
    'Instaurados a partir de 2022': teste_tsai(ENTRADA[coorte_2022], T_TOTAL[coorte_2022], EVENTO[coorte_2022]),
    'Instaurados antes de 2022': teste_tsai(ENTRADA[~coorte_2022], T_TOTAL[~coorte_2022], EVENTO[~coorte_2022]),
}).T.round(4))
fig, ax = plt.subplots(figsize=(11, 4.8))
ax.scatter(ENTRADA / 365.25, T_TOTAL - ENTRADA, c=np.where(evento, COR_PRINCIPAL, COR_DESTAQUE), s=20, edgecolor='white')
suave = lowess((T_TOTAL - ENTRADA)[evento], (ENTRADA / 365.25)[evento], frac=0.5)
ax.plot(suave[:, 0], suave[:, 1], color=TINTA, linewidth=2, label='tendência (LOWESS, concluídos)')
ax.set_xlabel('idade do IP na chegada ao Projudi (anos)')
ax.set_ylabel('dias da chegada à conclusão')
ax.set_title('Depois da chegada ao Projudi, a idade do inquérito importa? (azul: concluído; laranja: censurado)')
ax.legend()
plt.tight_layout()
plt.show()
''')

interp('ds_truncamento')

md(r'''
### 21.4 Tempo total: comparações com entrada tardia e na coorte recente

Como a quase-independência é rejeitada, o tempo total é lido de duas formas:

1. **amostra completa com entrada tardia:** cada variável é testada por um Cox univariado com entrada tardia, porque o log-rank não admite truncamento;
2. **coorte instaurada a partir de 2022:** o truncamento é pequeno, e usam-se Kaplan-Meier e log-rank.

O modelo de Cox multivariável com entrada tardia fecha a seção.
''')

code(r'''
def cox_univariado(df, duracao, ev, v, entrada=None):
    x = pd.get_dummies(serie_exibicao(df, v).astype(object).where(df[v].notna(), None), drop_first=True, dtype=float)
    validos = df[v].notna().to_numpy()
    base = x[validos].assign(T=duracao[validos], E=ev[validos])
    if entrada is not None:
        base['Entrada'] = entrada[validos]
    if x.shape[1] == 0 or base['E'].sum() < 5:
        return np.nan
    try:
        modelo = CoxPHFitter(penalizer=1e-4).fit(base, 'T', 'E', entry_col='Entrada' if entrada is not None else None)
    except Exception:
        return np.nan
    return modelo.log_likelihood_ratio_test().p_value


testes_total = pd.DataFrame({
    'p Cox com entrada tardia (amostra completa)': {ROTULO_VARIAVEL.get(v, v): cox_univariado(dados, T_TOTAL, EVENTO, v, ENTRADA)
                                                   for v in VARIAVEIS_CASO + ['Ano_recebimento_projudi']},
    'p log-rank (coorte ≥ 2022)': {
        ROTULO_VARIAVEL.get(v, v): (multivariate_logrank_test(T_TOTAL[coorte_2022 & dados[v].notna().to_numpy()],
                                                              serie_exibicao(dados, v)[coorte_2022 & dados[v].notna().to_numpy()].astype(str),
                                                              EVENTO[coorte_2022 & dados[v].notna().to_numpy()]).p_value
                                    if serie_exibicao(dados, v)[coorte_2022].nunique() > 1 else np.nan)
        for v in VARIAVEIS_CASO + ['Ano_recebimento_projudi']},
})
for coluna in list(testes_total.columns):
    validos = testes_total[coluna].notna()
    testes_total.loc[validos, coluna + ' — BH'] = multipletests(testes_total.loc[validos, coluna], method='fdr_bh')[1]
display(testes_total.round(4))

print(f'Coorte instaurada a partir de 2022: {int(coorte_2022.sum())} inquéritos; mediana KM do tempo total = '
      f'{KaplanMeierFitter().fit(T_TOTAL[coorte_2022], EVENTO[coorte_2022]).median_survival_time_:.0f} dias')
km_tot_coorte = grade_km(dados[coorte_2022], T_TOTAL[coorte_2022], EVENTO[coorte_2022],
                         ['Comarca', 'Forma_instauracao', 'Arma_de_fogo', 'Assunto_grupo', 'Tramitacao_direta', 'Houve_indiciamento',
                          'Tentativa', 'Tipo_delegacia'],
                         'Tempo total na coorte instaurada a partir de 2022 (instauração → conclusão no MP)')

cov_total = matriz_desenho(dados, ['Comarca', 'Assunto_grupo', 'Forma_instauracao'], COX_BINARIAS, [])
resultados_total = {}
for rotulo, mascara in [('Amostra completa (entrada tardia)', np.ones(len(dados), dtype=bool)), ('Coorte ≥ 2022 (entrada tardia)', coorte_2022)]:
    base = cov_total[mascara].assign(T=T_TOTAL[mascara], E=EVENTO[mascara], Entrada=ENTRADA[mascara])
    base = base.loc[:, base.std() > 0]
    modelo = CoxPHFitter(penalizer=0.01).fit(base, 'T', 'E', entry_col='Entrada')
    resultados_total[rotulo] = modelo.summary[['exp(coef)', 'p']].set_axis(['HR', 'p-valor'], axis=1)
    print(f'{rotulo}: n = {int(mascara.sum())}; eventos = {int(EVENTO[mascara].sum())}; '
          f'razão de verossimilhança: p = {modelo.log_likelihood_ratio_test().p_value:.2e}')
display(pd.concat(resultados_total, axis=1).round(3))

ajustes_tot_tr, tabela_tot_tr = ajustar_familias(T_TOTAL, EVENTO, entrada=ENTRADA)
print('Distribuições com censura e entrada tardia (tempo total):')
display(tabela_tot_tr.round(2))
with pd.option_context('display.float_format', lambda v: f'{v:.4g}'):
    display(razao_verossimilhanca(ajustes_tot_tr))
''')

interp('sv_total')
