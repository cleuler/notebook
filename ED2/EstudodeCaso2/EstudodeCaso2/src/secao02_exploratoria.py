# Parte II — Análise exploratória: o tempo como variável-alvo (seções 2.1 a 2.7).
# Executado por build_rafaelcc_ed2.py (exec): usa md(), code() e interp().
# Testes formais de comparação entre grupos ficam na Parte III; Kaplan-Meier e Cox, na Parte IV.

md(r'''
# PARTE II — ANÁLISE EXPLORATÓRIA: O TEMPO COMO VARIÁVEL-ALVO

A Parte II descreve os dados antes de qualquer inferência sobre o efeito dos ritos. O fio condutor é a **variável-alvo**: o tempo, em dias, da distribuição à sentença. Ela tem uma particularidade que governa tudo o que vem depois: para 230 dos 938 processos (206 ativos e 24 redistribuídos), o tempo até a sentença **não foi observado**; sabe-se apenas que ele é **maior** do que o tempo já decorrido. Por isso, a exploração separa sempre três coisas:

1. o **tempo observado** de cada processo (sentença, redistribuição ou corte em 07/10/2026);
2. o **indicador de evento** (sentença = 1; censura = 0);
3. as estatísticas **condicionais** aos sentenciados, que são legítimas como descrição desse subconjunto, mas enviesadas para tempos curtos como descrição do "tempo de tramitação".

| Seção | Conteúdo | Papel |
|---|---|---|
| 2.1 | A variável-alvo: tempo, evento e censura; por que as médias da pesquisa são enviesadas; entrada escalonada | definir o que se mede |
| 2.2 | Univariada: frequências de todas as categóricas; descritivas, gráficos, *outliers* e tempos zero | conhecer cada variável |
| 2.3 | Normalidade dos tempos dos sentenciados (Shapiro-Wilk, D'Agostino-Pearson, Anderson-Darling, Lilliefors, Jarque-Bera) | justificar métodos não paramétricos |
| 2.4 | Ajuste de distribuições **com censura** (exponencial, Weibull, log-normal, log-logística, gama generalizada, exponencial por partes) | forma do risco; base para os AFT da Parte IV |
| 2.5 | Modelos binomial e multinomial: equilíbrio do sorteio, taxas de acordo, sentenças sem mérito, sorteio das técnicas e sentenças em fim de semana | checar o desenho e as proporções |
| 2.6 | Bivariada: tempo × fatores, tabelas cruzadas, mosaicos, matriz de associação correta e ordem de chegada × tempo | gerar hipóteses para as Partes III a V |
| 2.7 | Síntese exploratória | |

Os testes formais de comparação entre os grupos (qui-quadrado de homogeneidade, Kruskal-Wallis, log-rank etc.) ficam na **Parte III**, e o Kaplan-Meier detalhado, na **Parte IV**. Aqui aparecem apenas os testes que respondem a perguntas **univariadas** (aderência a uma distribuição ou a uma proporção de referência).
''')

code(r'''
if 'dados' not in globals():
    dados = pd.read_pickle(PROC / 'ed2_tidy.pkl')

from scipy.special import gammaln
from statsmodels.stats.diagnostic import lilliefors
from statsmodels.stats.multitest import multipletests
from statsmodels.nonparametric.smoothers_lowess import lowess
from statsmodels.graphics.mosaicplot import mosaic
from lifelines import (ExponentialFitter, WeibullFitter, LogNormalFitter, LogLogisticFitter,
                       GeneralizedGammaFitter, PiecewiseExponentialFitter, NelsonAalenFitter)
from lifelines.plotting import qq_plot

# Base de trabalho da Parte II (dados não é alterado)
d2 = dados.copy()
d2['T'] = d2['tempo'].astype(float)          # dias observados (evento ou censura)
d2['E'] = d2['evento'].astype(int)           # 1 = sentença
d2['status'] = np.select([d2['evento_cr'].eq(1), d2['evento_cr'].eq(2)],
                          ['Sentença', 'Redistribuição'], 'Ativo (censurado)')
# ORDEM_STATUS e CORES_STATUS vêm da camada de visualização (seção 1.2)
sent = d2[d2['E'].eq(1)].copy()              # 708 sentenças: amostra CONDICIONAL
print(f'Processos: {len(d2)} | sentenças: {len(sent)} | redistribuições: {(d2.evento_cr == 2).sum()} | '
      f'ativos: {(d2.evento_cr == 0).sum()}')
''')

# =====================================================================
md(r'''
## 2.1 A variável-alvo: tempo, evento e censura

### 2.1.1 Definição

Para cada processo *i*, o tempo de interesse é **T*ᵢ*** = dias da distribuição até a sentença (homologatória, de mérito ou sem mérito). O que se observa, porém, é o par (**tᵢ**, **δᵢ**) (COLOSIMO; GIOLO, 2006, p. 6-12; MORETTIN; SINGER, 2021, p. 243-244):

| Situação em 07/10/2026 | n | tᵢ (coluna `tempo`) | δᵢ (`evento`) | O que se sabe de T*ᵢ* |
|---|---|---|---|---|
| Sentenciado | 708 | data da sentença − data da distribuição | 1 | T*ᵢ* = tᵢ |
| Ativo | 206 | 07/10/2026 − data da distribuição | 0 | T*ᵢ* > tᵢ (**censura à direita**) |
| Redistribuído ("Decisão") | 24 | data da decisão − data da distribuição | 0 | nunca terá sentença no 4º JEC (**risco competitivo**; tratado como censura nesta parte e modelado na Parte IV) |

A censura é **administrativa**: o processo não terminou porque o estudo parou de olhar. Como a distribuição vai de 01/01 a 03/08/2026 (**entrada escalonada**), o seguimento máximo possível (`followup` = 07/10/2026 − distribuição) vai de 65 a 279 dias: um processo de julho só pode exibir uma sentença de até ~98 dias.

### 2.1.2 Por que as médias da pesquisa e do notebook do professor são enviesadas

As médias divulgadas são: **78,46 dias** (geral, n = 943) e **77,50 / 80,87 / 77,00** (Presencial / Remota / Rito atual), das abas `Tab_D`/`Resumo` da planilha e do notebook do professor (E7, E14); e **75,2 dias** (geral) e **74,22 / 76,67 / 74,72** (Presencial / Remota / Rito atual) no resumo expandido, que não diz como as calculou. A célula abaixo reconstitui as duas séries a partir das datas, com as 944 linhas brutas (o que a pesquisadora tinha) e com a base primária (938), e compara com outros recortes. Há três estimadores em jogo, e **nenhum estima a duração média real**:

- **média de todos os tempos observados** ("mista"): é o que a fórmula da planilha produz, pois a duração dos ativos é `TODAY() − distribuição`. Mistura durações completas com tempos parciais (limites inferiores) e com redistribuições (que não são sentença); cresce todo dia, mesmo sem nenhuma sentença nova;
- **média dos sentenciados**: exclui justamente os processos mais longos, que ainda não terminaram; muda quando a data de corte muda;
- **média dos sentenciados até uma data anterior**: idem, com ainda menos seguimento.
''')

code(r'''
brutas = pd.read_pickle(PROC / 'ed2_todas_linhas.pkl')


def media_mista(df, corte):
    # Média "da planilha": duração até o desfecho se já houve desfecho até o corte; senão, corte − distribuição
    df = df[df['dt_distribuicao'].le(corte)]
    enc = df['encerrado'].fillna(False).astype(bool) & df['dt_sentenca'].le(corte)
    t = np.where(enc, (df['dt_sentenca'] - df['dt_distribuicao']).dt.days, (corte - df['dt_distribuicao']).dt.days)
    return t.mean(), int(enc.sum()), int((~enc).sum())


CORTE_RESUMO = pd.Timestamp('2026-09-23')   # data em que a média mista reproduz o resumo expandido (ver abaixo)
linhas = []
for g in [None] + ORDEM_GRUPO:
    sub = d2 if g is None else d2[d2['grupo'].eq(g)]
    sub_b = brutas if g is None else brutas[brutas['grupo'].eq(g)]
    linhas.append({
        'Grupo': 'Todos' if g is None else g, 'n (938)': len(sub),
        'Mista, 944 linhas, corte 07/10 (planilha: 78,46)': media_mista(sub_b, DATA_CORTE)[0],
        'Mista, 938, corte 07/10': sub['T'].mean(),
        'Mista, 944 linhas, corte 23/09 (resumo: 75,2)': media_mista(sub_b, CORTE_RESUMO)[0],
        'Só sentenciados até 07/10 (938)': sub.loc[sub['E'].eq(1), 'T'].mean(),
        'Só sentenciados até 03/08 (938)': sub.loc[sub['E'].eq(1) & sub['dt_sentenca'].le(FIM_RECRUTAMENTO), 'T'].mean(),
        'Seguimento máximo mediano (dias)': sub['followup'].median(),
    })
tab_medias = pd.DataFrame(linhas).set_index('Grupo')
tabela(tab_medias, 'exp_medias', 'As "médias" de duração reconstituídas a partir das datas, por grupo e critério (dias)',
       secao='2.1.2', casas=2,
       nota='"mista" = média de todos os tempos observados (sentenças + tempos parciais dos ativos), como na fórmula da '
            'planilha; nenhuma das colunas estima a duração média real, porque todas ignoram ou truncam os censurados.')
print('Divulgado na planilha/notebook do professor: 78,46 | Presencial 77,50 | Remota 80,87 | Rito atual 77,00')
print('Divulgado no resumo expandido:               75,2  | Presencial 74,22 | Remota 76,67 | Rito atual 74,72')
_, n_enc, n_atv = media_mista(brutas, CORTE_RESUMO)
print(f'Com corte em {CORTE_RESUMO:%d/%m/%Y} (944 linhas): {n_enc} encerrados e {n_atv} sem desfecho '
      f'(o resumo fala em 668 sentenciados e 275 ativos)')
''')

md(r'''
O gráfico mostra o mecanismo do viés. Para cada data de corte hipotética entre março e 07/10/2026, calcula-se a média que a pesquisa teria divulgado pelos dois critérios (só os sentenciados até aquela data; ou a média mista da planilha) e a proporção de processos ainda sem sentença. **Se essas médias estimassem a duração real, seriam estáveis**; elas crescem com o corte porque cada semana a mais de observação revela processos longos que antes estavam ocultos (e, na média mista, porque os ativos "envelhecem").
''')

code(r'''
cortes = pd.date_range('2026-03-01', DATA_CORTE, freq='7D').append(pd.DatetimeIndex([DATA_CORTE]))
serie_corte = []
for c in cortes:
    distribuidos = d2['dt_distribuicao'].le(c)
    sentenciados = d2['E'].eq(1) & d2['dt_sentenca'].le(c)
    serie_corte.append({'corte': c, 'media_sentenciados': d2.loc[sentenciados, 'T'].mean(),
                        'media_mista': media_mista(brutas, c)[0], 'n_sent': int(sentenciados.sum()),
                        'pct_sem_sentenca': 1 - sentenciados.sum() / distribuidos.sum()})
serie_corte = pd.DataFrame(serie_corte)

fig, ax = plt.subplots(1, 2, figsize=(13, 4.6))
ax[0].plot(serie_corte['corte'], serie_corte['media_sentenciados'], color=TINTA, marker='o', ms=3, label='só sentenciados')
ax[0].plot(serie_corte['corte'], serie_corte['media_mista'], color='#5B7389', marker='s', ms=3,
           label='mista (fórmula da planilha)')
ax[0].axhline(106.8, color=DESTAQUE, ls='--', lw=1)
ax[0].text(serie_corte['corte'].iloc[0], 109, 'média pré-experimento (GPS-Jus): 106,8 dias', color=TINTA_2, fontsize=8.5)
for data, valor, rot, desl in [(CORTE_RESUMO, 75.2, '75,2 (resumo, 23/09)', (-118, -16)),
                               (DATA_CORTE, 78.46, '78,46 (planilha, 07/10)', (-128, 10))]:
    ax[0].scatter([data], [valor], color=DESTAQUE, zorder=5, s=40)
    ax[0].annotate(rot, (data, valor), xytext=desl, textcoords='offset points', fontsize=8.5, color=TINTA)
ax[0].set_ylabel('Média calculada (dias)'); ax[0].legend(loc='lower right')
ax[0].set_title('(a) As "médias" crescem com a data de corte')
ax[0].set_ylim(0, 120)
ax[1].bar(serie_corte['corte'], serie_corte['pct_sem_sentenca'], width=5, color=CORES_STATUS['Ativo (censurado)'],
          edgecolor='#8c8c8c', linewidth=0.5)
eixo_pct(ax[1])
ax[1].set_ylabel('Distribuídos ainda sem sentença (%)')
ax[1].set_title('(b) Fração oculta (censurada) a cada corte')
for a in ax:
    eixo_meses(a)
    a.set_xlabel('Data de corte hipotética (2026)')
figura(fig, 'exp_medias_corte', 'As "médias" divulgadas dependem da data de corte: medem quanto se observou, não a duração',
       secao='2.1.2', nota='cada ponto recalcula a média com os dados disponíveis naquela data; pontos em destaque = valores divulgados.')
tab_corte = serie_corte.iloc[[0, 8, 17, 29, -1]].rename(columns={
    'corte': 'Data de corte', 'media_sentenciados': 'Média só sentenciados (dias)', 'media_mista': 'Média mista (dias)',
    'n_sent': 'Sentenciados até o corte', 'pct_sem_sentenca': 'Ainda sem sentença'})
tabela(tab_corte, 'exp_medias_corte_tab', 'Médias e fração censurada em cinco datas de corte', secao='2.1.2',
       formatos={'Ainda sem sentença': 'pct'})
''')

interp('exp_medias_viesadas')

md(r'''
### 2.1.3 Entrada escalonada e seguimento por mês de distribuição

O seguimento possível depende só da data de distribuição. A primeira figura mostra quantos processos de cada grupo entraram por mês (barras verticais agrupadas); a segunda, a situação de cada mês em 07/10/2026 (sentença, redistribuição ou ainda ativo), com o seguimento máximo possível de cada mês escrito acima da barra. **Como ler:** se algum grupo concentrar entradas em meses tardios, ele terá, por construção, mais censura e tempos observados mais curtos, sem que isso diga nada sobre o rito.
''')

code(r'''
MESES = list(d2['mes_distribuicao'].cat.categories)
cont_mes = pd.crosstab(d2['mes_distribuicao'], d2['grupo']).reindex(columns=ORDEM_GRUPO)
seg_mes = d2.groupby('mes_distribuicao', observed=True)['followup'].agg(['min', 'max'])
cens_mes = pd.crosstab(d2['mes_distribuicao'], d2['status'], normalize='index').reindex(columns=ORDEM_STATUS)

n_mes = d2['mes_distribuicao'].value_counts().reindex(MESES)
ROT_G = {g: rotulo_grupo(g, com_n=True, base=d2) for g in ORDEM_GRUPO}
fig, ax = plt.subplots(figsize=(10, 4.6))
barras_agrupadas(ax, cont_mes.rename(columns=ROT_G), cores={ROT_G[g]: CORES_GRUPO[g] for g in ORDEM_GRUPO},
                 ylabel='Processos distribuídos', xlabel=ROTULOS['mes_distribuicao'])
ax.legend(loc='upper left', ncol=3)
ax.set_ylim(0, cont_mes.to_numpy().max() * 1.25)
figura(fig, 'exp_entradas_mes', 'Entradas por mês e grupo: os grupos não entram no mesmo ritmo ao longo do ano',
       secao='2.1.3')

fig, ax = plt.subplots(figsize=(10, 4.8))
barras_empilhadas(ax, cens_mes, cores=CORES_STATUS, ns=n_mes.to_numpy(), ylabel='Processos do mês (%)')
for xi, mes in enumerate(MESES):
    ax.text(xi, 1.015, f'{seg_mes.loc[mes, "min"]}–{seg_mes.loc[mes, "max"]} d', ha='center', va='bottom',
            fontsize=8, color=TINTA_2, clip_on=False)
ax.set_xlabel(ROTULOS['mes_distribuicao'])
ax.set_title('Acima de cada barra: seguimento máximo possível até 07/10/2026 (dias)', fontsize=9.5,
             fontweight='normal', color=TINTA_2, pad=18)
figura(fig, 'exp_situacao_mes', 'Quanto mais tardia a entrada, maior a fração ainda censurada em 07/10/2026',
       secao='2.1.3', nota='o seguimento é 07/10/2026 menos a data de distribuição; não depende do grupo.')
tab_seg = pd.concat([cont_mes, n_mes.rename('Total'),
                     seg_mes.rename(columns={'min': 'Seguimento mín. (dias)', 'max': 'Seguimento máx. (dias)'}),
                     (100 * cens_mes).add_prefix('% ')], axis=1).rename_axis('Mês')
tabela(tab_seg, 'exp_seguimento_mes', 'Entradas por grupo, seguimento possível e situação em 07/10/2026, por mês de distribuição',
       secao='2.1.3')
''')

interp('exp_seguimento')

md(r'''
### 2.1.4 Trajetórias individuais (gráfico de nadador / diagrama de Lexis simplificado)

Cada linha horizontal é um processo: começa na data de distribuição e termina na sentença (círculo, colorido pelo tipo de desfecho), na redistribuição (losango) ou na data de corte (seta: censurado). Usa-se uma amostra estratificada de 25 processos por grupo (semente fixa), ordenada pela data de distribuição. **Como ler:** as setas se acumulam nos processos de entrada tardia, e a linha vertical de 07/10/2026 é a "parede" que corta as trajetórias; o comprimento de uma seta é um limite inferior, não uma duração.
''')

code(r'''
amostra = (d2.groupby('grupo', observed=True).sample(25, random_state=SEMENTE)
              .sort_values('dt_distribuicao').reset_index(drop=True))
fim = amostra['dt_sentenca'].fillna(DATA_CORTE)
fig, ax = plt.subplots(figsize=(11, 9))
for i, r in amostra.iterrows():
    ax.hlines(i, r['dt_distribuicao'], fim[i], color=CORES_GRUPO[r['grupo']], lw=2)
    if r['evento_cr'] == 1:
        ax.plot(fim[i], i, 'o', color=CORES_DESFECHO[r['tipo_desfecho']], ms=7, mec='white', mew=1)
    elif r['evento_cr'] == 2:
        ax.plot(fim[i], i, 'D', color=CORES_DESFECHO['Redistribuição'], ms=6, mec='white', mew=1)
    else:
        ax.plot(fim[i], i, '>', color=CORES_DESFECHO['Ativo'], ms=7, mec=TINTA_2, mew=0.6)
ax.axvline(DATA_CORTE, color=DESTAQUE, ls='--', lw=1)
ax.axvline(FIM_RECRUTAMENTO, color=TINTA_2, ls=':', lw=1)
ax.text(DATA_CORTE, len(amostra) + 0.5, ' corte 07/10', color=TINTA, fontsize=8.5)
ax.text(FIM_RECRUTAMENTO, len(amostra) + 0.5, 'fim dos sorteios 03/08 ', color=TINTA_2, fontsize=8.5, ha='right')
ax.set_yticks([]); ax.set_ylabel('Processos (amostra de 75, ordenados pela distribuição)')
eixo_meses(ax)
ax.grid(axis='x', visible=True); ax.grid(axis='y', visible=False)
ax.set_xlabel('Calendário (2026)')
leg = ([mpl.lines.Line2D([], [], color=CORES_GRUPO[g], lw=2, label=f'Grupo {g}') for g in ORDEM_GRUPO] +
       [mpl.lines.Line2D([], [], marker='o', ls='', color=CORES_DESFECHO[k], mec='white', ms=7, label=ROTULO_DESFECHO[k])
        for k in ['Homologação', 'Mérito', 'Sem mérito']] +
       [mpl.lines.Line2D([], [], marker='D', ls='', color=CORES_DESFECHO['Redistribuição'], label=ROTULO_DESFECHO['Redistribuição']),
        mpl.lines.Line2D([], [], marker='>', ls='', color=CORES_DESFECHO['Ativo'], mec=TINTA_2, label=ROTULO_DESFECHO['Ativo'])])
legenda_abaixo(ax, ncol=3, dy=-0.08, handles=leg)
figura(fig, 'exp_trajetorias', 'Trajetórias individuais: a data de corte interrompe os processos de entrada tardia',
       secao='2.1.4', nota='amostra estratificada de 25 processos por grupo (semente 2026). A cor da linha é o grupo; '
                           'o marcador final é o desfecho (círculo), a redistribuição (losango) ou a censura (seta).')
print(amostra['status'].value_counts().to_string())
''')

interp('exp_swimmer')

# =====================================================================
md(r'''
## 2.2 Análise univariada

### 2.2.1 Variáveis categóricas: tabelas de frequência

Para cada variável categórica, a tabela traz a frequência absoluta (n), a relativa (%) e a acumulada (% acum.) sobre os 938 processos, e o % sobre os casos válidos (excluídas as ausências). As ausências **não** são categorias de resposta: são mostradas com o motivo (zero estrutural, "não se aplica", ou processo ativo ainda sem a informação), como determinado na Parte I. A % acumulada só tem leitura substantiva nas variáveis ordinais (mês, dia da semana, ciclo); nas nominais, é a base do gráfico de Pareto.
''')

code(r'''
def para_rotulos(serie, rotulo_na):
    # Converte booleanos em Sim/Não e ausências no rótulo explicativo, preservando a ordem das categorias
    if isinstance(serie.dtype, pd.BooleanDtype) or pd.api.types.is_bool_dtype(serie):
        s = serie.map({True: 'Sim', False: 'Não'})
        ordem = ['Sim', 'Não']
    elif isinstance(serie.dtype, pd.CategoricalDtype):
        s = serie.astype(object)
        ordem = list(serie.cat.categories)
    else:
        s = serie.astype(object)
        ordem = sorted(s.dropna().unique())
    s = s.where(serie.notna(), rotulo_na)
    if serie.isna().any():
        ordem = ordem + [rotulo_na]
    return pd.Categorical(s, categories=ordem, ordered=True)


def tabela_freq(serie, rotulo_na='NA'):
    cat = para_rotulos(serie, rotulo_na)
    n = pd.Series(cat).value_counts(sort=False)
    validos = n.drop(rotulo_na, errors='ignore')
    tab = pd.DataFrame({'n': n, '%': 100 * n / n.sum()})
    tab['% acum.'] = tab['%'].cumsum()
    tab['% válido'] = (100 * validos / validos.sum()).reindex(tab.index)
    return tab


VARS_CAT = {   # variável: (título, rótulo das ausências)
    'grupo': ('Grupo sorteado', None),
    'mes_distribuicao': ('Mês de distribuição', None),
    'ciclo': ('Ciclo (resumo expandido)', None),
    'dia_semana_distribuicao': ('Dia da semana da distribuição', None),
    'tipo_desfecho': ('Tipo de desfecho em 07/10/2026', None),
    'ac_realizada': ('AC realizada', 'não informado (ativo)'),
    'tecnica_curta': ('Técnica de conciliação', 'sem AC (não se aplica)'),
    'hibrida': ('AC híbrida', 'não informado'),
    'acordo_ac': ('Acordo na AC', 'não informado'),
    'acordo_fora': ('Acordo fora da AC', 'ativo (indefinido)'),
    'acordo': ('Acordo (qualquer momento)', 'ativo (indefinido)'),
    'origem_externa': ('Origem externa (redistribuído à vara)', None),
    'tempo_zero': ('Desfecho no dia da distribuição', None),
    'sentenca_fim_semana': ('Desfecho datado em fim de semana', 'ativo (sem desfecho)'),
    'desvio_protocolo': ('Desvio de protocolo (híbrida na Remota ou sem AC)', None),
    'cnj_corrigido': ('Número CNJ corrigido', None),
    'duplicado_removido': ('Número com linha duplicada removida', None),
}
tabelas_freq = {VARS_CAT[v][0]: tabela_freq(d2[v], VARS_CAT[v][1] or 'NA') for v in VARS_CAT}
tab_freq = pd.concat(tabelas_freq, names=['Variável', 'Categoria'])
tabela(tab_freq, 'exp_freq', 'Frequências de todas as variáveis categóricas (938 processos)', secao='2.2.1',
       formatos={'n': 'int'}, casas=1,
       nota='% = sobre os 938 processos; % válido = excluídas as ausências, cujo motivo aparece como categoria própria '
            '(não são respostas). A % acumulada só tem leitura substantiva nas variáveis ordinais.')
''')

md(r'''
**Gráficos de barras verticais.** As variáveis do desenho (grupo e calendário) aparecem primeiro; o rótulo de cada barra é a frequência absoluta. Cada variável tem uma só cor (exceto o grupo, que usa as cores fixas dos grupos), porque a altura da barra já mostra a frequência.
''')

code(r'''
def barras(ax, serie, titulo, rotulo_na='NA', cores=None, quebrar=12):
    tab = tabela_freq(serie, rotulo_na)
    cores_barras = [CORES_DESFECHO['Ativo'] if k == rotulo_na else (cores or {}).get(k, '#5B7389') for k in tab.index]
    barras_verticais(ax, [str(k) for k in tab.index], tab['n'].to_numpy(), cores=cores_barras, quebrar=quebrar,
                     ylabel=ROTULOS['n'])
    ax.set_title(titulo)
    return tab


fig, ax = plt.subplots(2, 2, figsize=(12, 7.5))
barras(ax[0, 0], d2['grupo'], '(a) Grupo sorteado', cores=CORES_GRUPO)
ax[0, 0].axhline(len(d2) / 3, color=TINTA_2, ls='--', lw=1)
ax[0, 0].text(2.32, len(d2) / 3, ' n/3', color=TINTA_2, fontsize=8.5, va='bottom')
barras(ax[0, 1], d2['mes_distribuicao'], '(b) Mês de distribuição (2026)')
barras(ax[1, 0], d2['dia_semana_distribuicao'], '(c) Dia da semana da distribuição')
barras(ax[1, 1], d2['ciclo'], '(d) Ciclo (resumo expandido)', quebrar=10)
figura(fig, 'exp_freq_desenho', 'Variáveis do desenho: grupos de tamanho quase igual; entradas desiguais no calendário',
       secao='2.2.1')
''')

interp('exp_freq_desenho')

md(r'''
**Desfecho e técnica: gráficos de Pareto.** Para as duas variáveis nominais com várias categorias, o Pareto ordena as barras da mais para a menos frequente; a % acumulada é escrita sobre cada barra (em vez de um segundo eixo vertical, que criaria uma escala arbitrária ao lado da contagem). Ele responde a "quais categorias concentram os casos". No tipo de desfecho, "Ativo" é mantido porque é uma situação real em 07/10/2026 (ainda sem desfecho), mas é a censura, não um desfecho.
''')

code(r'''
def pareto(ax, serie, titulo, cores=None, rotulos=None, quebrar=14):
    n = serie.value_counts().sort_values(ascending=False)
    acum = n.cumsum() / n.sum()
    nomes = [(rotulos or {}).get(k, k) for k in n.index]
    barras_verticais(ax, nomes, n.to_numpy(), cores=[(cores or {}).get(k, '#5B7389') for k in n.index],
                     rotular=False, quebrar=quebrar, ylabel=ROTULOS['n'])
    for i, (v, a) in enumerate(zip(n.to_numpy(), acum.to_numpy())):
        ax.annotate(f'{fmt_br(v, 0)}\nacum. {pct_br(a, 0)}', (i, v), xytext=(0, 3), textcoords='offset points',
                    ha='center', va='bottom', fontsize=8.5, color=TINTA)
    ax.set_ylim(0, n.max() * 1.25)
    ax.set_title(titulo)
    return n


fig, ax = plt.subplots(1, 2, figsize=(13, 4.8), gridspec_kw={'width_ratios': [5, 6]})
pareto(ax[0], d2['tipo_desfecho'].astype(str), f'(a) Tipo de desfecho em 07/10/2026 (n = {fmt_br(len(d2), 0)})',
       CORES_DESFECHO, ROTULO_DESFECHO, quebrar=13)
n_ac_real = int(d2['tecnica_curta'].notna().sum())
pareto(ax[1], d2['tecnica_curta'].dropna().astype(str), f'(b) Técnica de conciliação (AC realizadas, n = {n_ac_real})',
       quebrar=12)
ax[1].axhline(n_ac_real / 6, color=TINTA_2, ls='--', lw=1)
ax[1].text(5.45, n_ac_real / 6, 'n/6', fontsize=8.5, color=TINTA_2, va='bottom', ha='right')
figura(fig, 'exp_pareto', 'Pareto do desfecho e da técnica: o mérito lidera os desfechos; as técnicas ficam perto de 1/6 cada',
       secao='2.2.1', nota='sobre cada barra: frequência e % acumulada. "Em tramitação" é censura, não desfecho.')
''')

interp('exp_freq_desfecho')

md(r'''
**Audiência e acordo; indicadores de qualidade.** Barras verticais 100% empilhadas, uma por variável binária (Sim, Não e ausente). A leitura correta de cada uma depende do denominador: `acordo_ac`, `hibrida` e `tecnica` só têm sentido onde houve AC; `acordo` e `acordo_fora` ficam indefinidos nos ativos (o acordo ainda pode acontecer). Os indicadores da segunda linha são *flags* de curadoria (Parte I), úteis para as análises de sensibilidade.
''')

code(r'''
PAINEL_BIN = {'Audiência e acordo': ['ac_realizada', 'hibrida', 'acordo_ac', 'acordo_fora', 'acordo'],
              'Indicadores de curadoria (Parte I)': ['origem_externa', 'tempo_zero', 'sentenca_fim_semana',
                                                    'desvio_protocolo', 'cnj_corrigido']}
CORES_BIN = {'Sim': '#2B3A4A', 'Não': '#A9B8C6', 'Ausente': CORES_DESFECHO['Ativo']}
fig, ax = plt.subplots(1, 2, figsize=(14, 5.2), sharey=True)
for a, (bloco_, vars_) in zip(ax, PAINEL_BIN.items()):
    linhas_bin = {}
    for v in vars_:
        cat = pd.Series(para_rotulos(d2[v], 'Ausente'))
        linhas_bin[VARS_CAT[v][0]] = cat.value_counts(normalize=True).reindex(['Sim', 'Não', 'Ausente']).fillna(0)
    barras_empilhadas(a, pd.DataFrame(linhas_bin).T, cores=CORES_BIN, quebrar=16, legenda=False,
                      fmt=lambda v: pct_br(v, 1) if v < 0.1 else pct_br(v, 0))
    a.set_title(bloco_)
ax[1].set_ylabel('')
ax[1].legend(*[x[::-1] for x in ax[1].get_legend_handles_labels()], loc='center left', bbox_to_anchor=(1.01, 0.5))
figura(fig, 'exp_binarias', 'Variáveis binárias: o denominador muda de variável para variável (938 processos)',
       secao='2.2.1', nota='"Ausente" = não se aplica (sem AC) ou ainda indefinido (processo ativo); ver a tabela de frequências. '
                           'Segmentos menores que 6% ficam sem rótulo.')

# Denominadores corretos das taxas de AC e acordo
ac = d2[d2['ac_realizada'].fillna(False).astype(bool)].copy()
print(f'AC realizadas: {len(ac)} (Presencial {(ac.grupo == "Presencial").sum()}, Remota {(ac.grupo == "Remota").sum()}); '
      f'acordo na AC: {int(ac.acordo_ac.sum())} ({pct_br(ac.acordo_ac.mean())} das AC realizadas)')
print(f'Híbridas: {int(d2.hibrida.sum())}, das quais {int((d2.hibrida.fillna(False) & d2.grupo.eq("Presencial")).sum())} no grupo Presencial')
print(f'Acordo em qualquer momento: {int(d2.acordo.sum())} = homologações ({(d2.tipo_desfecho == "Homologação").sum()})')
print(f'Ativos com o campo de acordo já preenchido na planilha: {int((d2.evento_cr.eq(0) & d2.acordo.notna()).sum())} '
      f'(por isso os indefinidos são {int(d2.acordo.isna().sum())}, e não {int(d2.evento_cr.eq(0).sum())})')
''')

interp('exp_freq_ac')

md(r'''
### 2.2.2 O tempo: medidas descritivas

As medidas são calculadas em quatro recortes, que **não** são intercambiáveis:

- **Sentenças (n = 708)**: durações completas, mas **condicionais** a ter havido sentença até 07/10/2026. Descrevem os processos já sentenciados, não "o tempo de tramitação" do 4º JEC, porque os processos longos estão sub-representados (ainda ativos).
- **Ativos (n = 206)**: tempo já decorrido até o corte; é um **limite inferior** da duração real.
- **Redistribuições (n = 24)**: tempo até a saída da vara; não é tempo até sentença.
- **Todos os tempos observados (n = 938)**: o que a planilha e o notebook do professor resumiam (E7, E14). Apresentado só para mostrar o que estava sendo calculado; **não estima nenhuma quantidade interpretável**.

Medidas: média, mediana, moda (dia mais frequente), desvio-padrão, variância, coeficiente de variação (CV = DP/média), quantis, intervalo interquartil (IIQ), mínimo, máximo, assimetria e curtose em excesso (estimadores sem viés de Fisher; curtose 0 = normal), MAD (desvio absoluto mediano, escala bruta e reescalada por 1,4826 para comparação com o DP), média aparada a 10% e intervalo de confiança *bootstrap* de 95% da mediana (percentil, 5.000 reamostras, semente fixa).
''')

code(r'''
def descritivas(x, b=5000):
    x = np.asarray(x, dtype=float)
    moda = pd.Series(x).mode()
    q = np.percentile(x, [5, 10, 25, 50, 75, 90, 95])
    boot = stats.bootstrap((x,), np.median, n_resamples=b, confidence_level=0.95, method='percentile',
                           rng=np.random.default_rng(SEMENTE))
    return pd.Series({
        'n': len(x), 'média': x.mean(), 'EP da média': x.std(ddof=1) / np.sqrt(len(x)),
        'mediana': q[3], 'IC95% mediana (inf.)': boot.confidence_interval.low,
        'IC95% mediana (sup.)': boot.confidence_interval.high,
        'moda': moda.iloc[0], 'freq. da moda': int((x == moda.iloc[0]).sum()),
        'desvio-padrão': x.std(ddof=1), 'variância': x.var(ddof=1), 'CV (%)': 100 * x.std(ddof=1) / x.mean(),
        'mínimo': x.min(), 'P5': q[0], 'P10': q[1], 'Q1 (P25)': q[2], 'Q3 (P75)': q[4], 'P90': q[5], 'P95': q[6],
        'máximo': x.max(), 'amplitude': x.max() - x.min(), 'IIQ': q[4] - q[2],
        'assimetria': stats.skew(x, bias=False), 'curtose (excesso)': stats.kurtosis(x, bias=False),
        'MAD': stats.median_abs_deviation(x), 'MAD × 1,4826': stats.median_abs_deviation(x, scale='normal'),
        'média aparada 10%': stats.trim_mean(x, 0.10),
    })


recortes = {'Sentenças (condicional)': sent['T'],
            'Ativos (limite inferior)': d2.loc[d2.evento_cr.eq(0), 'T'],
            'Redistribuições': d2.loc[d2.evento_cr.eq(2), 'T'],
            'Todos os observados (inválido)': d2['T']}
tab_desc = pd.DataFrame({k: descritivas(v) for k, v in recortes.items()})
_fmt_desc = lambda v: fmt_br(v, 0) if float(v).is_integer() else fmt_br(v, 2)
tabela(tab_desc.rename_axis('Medida (dias, salvo indicação)'), 'exp_descritivas',
       'Medidas descritivas do tempo em quatro recortes que não são intercambiáveis', secao='2.2.2',
       formatos={c: _fmt_desc for c in tab_desc.columns},
       nota='as sentenças descrevem só os processos já sentenciados (condicional); os ativos dão limites inferiores; '
            'a coluna "todos os observados" mistura os dois e não estima nenhuma quantidade interpretável.')
''')

md(r'''
### 2.2.3 O tempo: gráficos

Quatro gráficos complementares, todos em escala linear:

- **(a) Histograma** dos tempos observados, empilhado pela situação (sentença, redistribuição, ativo). Classes de 10 dias. Mostra onde estão os censurados (à direita, porque só se tornam censurados os processos que chegaram ao corte sem sentença).
- **(b) Boxplot vertical** por recorte. A caixa vai de Q1 a Q3, a linha é a mediana (valor escrito ao lado, "Md"), o losango é a média; os "bigodes" vão até 1,5 IIQ.
- **(c) Violino** das sentenças por tipo de desfecho: a largura é a densidade estimada (núcleo gaussiano), o que revela bimodalidade que o boxplot esconde.
- **(d) ECDF** (função de distribuição empírica) das sentenças e dos ativos. **Atenção:** a ECDF das sentenças **não** é 1 − KM; ela ignora os censurados e por isso sobe depressa demais (o KM correto está na Parte IV).
''')

code(r'''
fig, ax = plt.subplots(2, 2, figsize=(13, 9.5))
classes = np.arange(0, 290, 10)
base = np.zeros(len(classes) - 1)
for s in ORDEM_STATUS:
    h, _ = np.histogram(d2.loc[d2.status.eq(s), 'T'], bins=classes)
    ax[0, 0].bar(classes[:-1], h, width=10, align='edge', bottom=base, color=CORES_STATUS[s],
                 edgecolor='white', linewidth=0.8, label=f'{s} (n = {d2.status.eq(s).sum()})')
    base += h
ax[0, 0].set_xlabel('Tempo observado (dias; classes de 10 dias)'); ax[0, 0].set_ylabel(ROTULOS['n'])
ax[0, 0].legend(loc='upper right')
ax[0, 0].set_ylim(0, base.max() * 1.08)
for corte_ in (150, 190):
    print(f'Tempo observado > {corte_} dias: {int((d2["T"].gt(corte_) & d2.evento_cr.eq(1)).sum())} sentenças e '
          f'{int((d2["T"].gt(corte_) & d2.evento_cr.eq(0)).sum())} ativos')
ax[0, 0].set_title('(a) Histograma dos tempos observados, por situação')

COR_RECORTE = {'Sentenças (condicional)': CORES_STATUS['Sentença'], 'Ativos (limite inferior)': CORES_STATUS['Ativo (censurado)'],
               'Redistribuições': CORES_STATUS['Redistribuição'], 'Todos os observados (inválido)': '#FFFFFF'}
dados_box = [recortes[k].to_numpy(float) for k in recortes]
bp = ax[0, 1].boxplot(dados_box, positions=range(4), showmeans=True, widths=0.5, patch_artist=True,
                      medianprops=dict(color=TINTA, lw=2), flierprops=dict(marker='o', ms=3, mfc='none', mec=TINTA_2),
                      meanprops=dict(marker='D', markerfacecolor='white', markeredgecolor=TINTA, ms=5))
for p_, k in zip(bp['boxes'], recortes):
    p_.set_facecolor(mpl.colors.to_rgba(COR_RECORTE[k], 0.55)); p_.set_edgecolor(TINTA_2)
for i, v in enumerate(dados_box):
    ax[0, 1].annotate(f'Md = {fmt_br(np.median(v), 1 if not float(np.median(v)).is_integer() else 0)}',
                      (i + 0.27, np.median(v)), xytext=(3, 0), textcoords='offset points', va='center', fontsize=8.5)
ax[0, 1].set_xticks(range(4), [f'{quebra(k, 13)}\n(n = {len(v)})' for k, v in recortes.items()], fontsize=8.5)
ax[0, 1].set_xlim(-0.5, 3.9)
ax[0, 1].set_ylabel('Tempo observado (dias)'); ax[0, 1].set_title('(b) Boxplot por recorte (losango = média)')
ax[0, 1].grid(axis='x', visible=False)

tipos = ['Homologação', 'Mérito', 'Sem mérito']
vp = ax[1, 0].violinplot([sent.loc[sent.tipo_desfecho.eq(t), 'T'] for t in tipos], positions=range(3),
                         showmedians=True, widths=0.8)
for corpo, t in zip(vp['bodies'], tipos):
    corpo.set_facecolor(CORES_DESFECHO[t]); corpo.set_edgecolor(CORES_DESFECHO[t]); corpo.set_alpha(0.55)
for parte in ('cbars', 'cmins', 'cmaxes', 'cmedians'):
    vp[parte].set_color(TINTA); vp[parte].set_linewidth(1)
for i, t in enumerate(tipos):
    md_t = sent.loc[sent.tipo_desfecho.eq(t), 'T'].median()
    ax[1, 0].annotate(f'Md = {fmt_br(md_t, 0 if float(md_t).is_integer() else 1)}', (i + 0.1, md_t), xytext=(4, 4),
                      textcoords='offset points', fontsize=8.5)
ax[1, 0].set_xticks(range(3), [f'{quebra(ROTULO_DESFECHO[t], 14)}\n(n = {sent.tipo_desfecho.eq(t).sum()})' for t in tipos])
ax[1, 0].set_ylabel(ROTULOS['tempo_sentenca']); ax[1, 0].set_title('(c) Violino das sentenças por tipo de desfecho')
ax[1, 0].grid(axis='x', visible=False)

for nome, serie, cor in [(f'Sentenças (n = {len(sent)})', sent['T'], TINTA),
                         (f'Ativos: tempo até o corte (n = {int(d2.evento_cr.eq(0).sum())})', d2.loc[d2.evento_cr.eq(0), 'T'], '#8C8C8C')]:
    xs = np.sort(serie.to_numpy(float))
    ax[1, 1].step(xs, np.arange(1, len(xs) + 1) / len(xs), where='post', color=cor, label=nome)
ax[1, 1].set_xlabel('Tempo observado (dias)'); ax[1, 1].set_ylabel('Proporção acumulada (ECDF)')
ax[1, 1].legend(loc='lower right'); ax[1, 1].grid(axis='both', visible=True)
ax[1, 1].set_title('(d) ECDF: não é 1 − Kaplan-Meier')
figura(fig, 'exp_tempo_graficos', 'O tempo até a sentença é bimodal e a censura ocupa a cauda direita', secao='2.2.3',
       nota='todos os eixos em escala linear. A ECDF das sentenças ignora os censurados e por isso sobe depressa demais; '
            'o Kaplan-Meier correto está na Parte IV.')
''')

interp('exp_tempo_graficos')

md(r'''
O **QQ-plot normal** das sentenças compara os quantis observados com os de uma normal de mesma média e desvio-padrão. Pontos sobre a reta indicam normalidade; curvatura em "S" indica caudas diferentes da normal; desvios nas pontas indicam assimetria ou truncamento. Os testes formais de normalidade estão na seção 2.3.
''')

code(r'''
fig, ax = plt.subplots(figsize=(6, 5))
(osm, osr), (incl, inter, r) = stats.probplot(sent['T'], dist='norm')
ax.scatter(osm, osr, s=9, color=TINTA, alpha=0.5, lw=0)
ax.plot(osm, inter + incl * osm, color=DESTAQUE, lw=1.5, label='normal de mesma média e DP')
ax.set_xlabel('Quantis teóricos da normal padrão'); ax.set_ylabel(ROTULOS['tempo_sentenca'])
ax.grid(axis='both', visible=True); ax.legend(loc='lower right')
anotar_teste(ax, f'n = {len(sent)}\nr (QQ) = {fmt_br(r, 3)}', loc='upper left')
figura(fig, 'exp_qq_sentencas', 'QQ-plot normal das sentenças: os pontos se curvam fora da reta (não normalidade)',
       secao='2.2.3', nota='os testes formais de normalidade estão na seção 2.3.')
''')

interp('exp_tempo_desc')

md(r'''
### 2.2.4 Valores atípicos (regra do IIQ)

Pela regra de Tukey, é atípico o valor fora de [Q1 − 1,5·IIQ; Q3 + 1,5·IIQ]. A regra é aplicada às sentenças (durações completas). **Nenhum valor é removido**: um processo de 220 dias não é erro de medida, é uma duração legítima, e justamente a cauda longa é o que interessa à gestão do acervo. Remover "outliers" de uma variável de tempo encurtaria artificialmente as durações. A conferência de datas (Parte I, seção 1.14) já descartou erros de registro (sentença anterior à distribuição etc.).
''')

code(r'''
q1, q3 = sent['T'].quantile([0.25, 0.75])
iiq = q3 - q1
lim_inf, lim_sup = q1 - 1.5 * iiq, q3 + 1.5 * iiq
atipicos = sent[(sent['T'] < lim_inf) | (sent['T'] > lim_sup)]
print(f'Sentenças: Q1 = {fmt_br(q1)}, Q3 = {fmt_br(q3)}, IIQ = {fmt_br(iiq)}; cercas = [{fmt_br(lim_inf)}; {fmt_br(lim_sup)}] dias')
print(f'Atípicos: {len(atipicos)} ({pct_br(len(atipicos) / len(sent))})')
tabela(atipicos[['processo', 'grupo', 'dt_distribuicao', 'dt_sentenca', 'tempo', 'tipo_desfecho', 'mes_distribuicao']]
       .sort_values('tempo', ascending=False).reset_index(drop=True)
       .rename(columns={'processo': 'Processo', 'grupo': 'Grupo', 'dt_distribuicao': 'Distribuição', 'dt_sentenca': 'Sentença',
                        'tempo': 'Tempo (dias)', 'tipo_desfecho': 'Tipo de desfecho', 'mes_distribuicao': 'Mês'}),
       'exp_atipicos', f'Sentenças atípicas pela regra de Tukey (acima de {fmt_br(lim_sup)} dias): duração legítima, não erro',
       secao='2.2.4', nota='nenhum valor é removido da análise.')
# Os mesmos limites aplicados aos tempos dos ativos (só para referência: são limites inferiores)
ativos_acima = d2[d2.evento_cr.eq(0) & (d2['T'] > lim_sup)]
print(f'Ativos com tempo já decorrido acima da cerca superior: {len(ativos_acima)} '
      f'(seriam atípicos certos se sentenciados hoje)')
''')

interp('exp_outliers')

md(r'''
### 2.2.5 Tempos zero

Há processos com desfecho **no próprio dia da distribuição** (`tempo` = 0). Eles não são erro: o juízo pode indeferir a inicial, homologar desistência imediata ou declinar a competência no mesmo dia. A tabela mostra que tipo de desfecho são, em que grupo e se a AC chegou a ocorrer. Nos modelos paramétricos (seção 2.4), que exigem T > 0, esses tempos são substituídos por 0,5 dia (`tempo_pos`); nos não paramétricos, o zero é mantido.
''')

code(r'''
zeros = d2[d2['T'].eq(0)]
print(f'Tempos zero: {len(zeros)} ({pct_br(len(zeros) / len(d2))} dos processos; '
      f'{int(zeros.E.sum())} sentenças = {pct_br(zeros.E.sum() / len(sent))} das sentenças)')
tabela(pd.crosstab(zeros['tipo_desfecho'].astype(str).map(ROTULO_DESFECHO), zeros['grupo'], margins=True,
                   margins_name='Total').rename_axis(index='Tipo de desfecho', columns=None),
       'exp_zeros_tipo', 'Processos com desfecho no dia da distribuição, por tipo de desfecho e grupo', secao='2.2.5')
tabela(pd.crosstab(zeros['origem_externa'].map({True: 'Sim', False: 'Não'}),
                   zeros['ac_realizada'].map({True: 'Sim', False: 'Não'}).fillna('não informado'),
                   margins=True, margins_name='Total').rename_axis(index='Origem externa', columns=None)
       .rename(columns=lambda c: c if c == 'Total' else f'AC realizada: {c}'),
       'exp_zeros_origem', 'Tempos zero por origem do processo e realização da AC', secao='2.2.5')
# Até 7 dias: extinções "imediatas"
ate7 = sent[sent['T'].le(7)]
print(f'Sentenças em até 7 dias: {len(ate7)}; tipo: {ate7.tipo_desfecho.astype(str).value_counts().to_dict()}')
''')

interp('exp_tempo_zero')

# =====================================================================
md(r'''
## 2.3 Normalidade dos tempos dos sentenciados

**A pergunta certa e a pergunta pedida.** Num problema de sobrevivência, a normalidade da amostra *condicional* dos sentenciados **não** é a questão relevante: os métodos da Parte IV (Kaplan-Meier, log-rank, Cox) não supõem nenhuma distribuição, e os paramétricos (seção 2.4) se escolhem pela verossimilhança com censura. O teste é feito porque o roteiro o pede e porque ele **justifica** o uso de testes não paramétricos (Kruskal-Wallis, Mann-Whitney) quando a Parte III comparar os tempos dos sentenciados. O notebook do professor testou uma subamostra arbitrária de 500 casos e misturou censurados com eventos (E22); aqui se usam todas as 708 sentenças, no total e por grupo.

**Hipóteses** (para cada amostra): H0: os tempos até a sentença vêm de uma distribuição normal; H1: não vêm.

| Teste | O que mede | Gráfico correspondente |
|---|---|---|
| Shapiro-Wilk | correlação entre os dados ordenados e os quantis normais esperados | QQ-plot (1ª figura) |
| Anderson-Darling | distância quadrática ponderada entre ECDF e normal, com mais peso nas caudas | QQ-plot (1ª figura) |
| D'Agostino-Pearson (K²) | combina assimetria e curtose padronizadas | histograma com a normal ajustada (2ª figura) |
| Jarque-Bera | idem, pela assimetria e curtose amostrais (assintótico) | histograma com a normal ajustada (2ª figura) |
| Lilliefors | maior distância vertical entre ECDF e normal com parâmetros estimados (KS corrigido) | ECDF × Φ (3ª figura) |

**Pressupostos:** observações independentes (sorteio individual; ver ressalvas na seção 7.2, questão 2.3); variável contínua: o tempo em dias é discreto e tem **empates** (muitos processos com o mesmo número de dias), o que deixa os testes de ECDF (Lilliefors, Anderson-Darling) ligeiramente mais propensos a rejeitar; com amplitude de 0 a 225 dias, porém, esse efeito é pequeno diante do desvio de forma. Com n de 200 a 700, os testes têm poder para detectar desvios pequenos: a decisão deve olhar o gráfico, não só o p-valor. A correção de Holm é aplicada à família de 20 testes (5 testes × 4 amostras).
''')

code(r'''
def testes_normalidade(x):
    x = np.asarray(x, dtype=float)
    sw = stats.shapiro(x)
    dp = stats.normaltest(x)
    ad = stats.anderson(x, 'norm', method=stats.MonteCarloMethod(n_resamples=9999, rng=np.random.default_rng(SEMENTE)))
    li_stat, li_p = lilliefors(x, dist='norm', pvalmethod='approx')
    jb = stats.jarque_bera(x)
    return [('Shapiro-Wilk', 'W', sw.statistic, sw.pvalue),
            ("D'Agostino-Pearson", 'K²', dp.statistic, dp.pvalue),
            ('Anderson-Darling', 'A²', ad.statistic, ad.pvalue),
            ('Lilliefors', 'D', li_stat, li_p),
            ('Jarque-Bera', 'JB', jb.statistic, jb.pvalue)]


AMOSTRAS_NORM = {'Todas as sentenças': sent['T']} | {g: sent.loc[sent.grupo.eq(g), 'T'] for g in ORDEM_GRUPO}
linhas = []
for nome, x in AMOSTRAS_NORM.items():
    for teste, simb, est, p in testes_normalidade(x):
        linhas.append({'Amostra': nome, 'n': len(x), 'Teste': teste, 'Estatística': f'{simb} = {fmt_br(est, 3)}', 'p': p})
tab_norm = pd.DataFrame(linhas)
tab_norm['p (Holm)'] = multipletests(tab_norm['p'], method='holm')[1]
tab_norm['Decisão (5%)'] = np.where(tab_norm['p (Holm)'] < 0.05, 'rejeita H0', 'não rejeita H0')
tabela(tab_norm, 'exp_normalidade', 'Testes de normalidade do tempo até a sentença (H0: distribuição normal)', secao='2.3',
       destaque='p (Holm)', nota='Holm sobre a família de 20 testes (5 testes × 4 amostras); linhas destacadas: H0 rejeitada a 5%.')
print('Anderson-Darling: p-valor por Monte Carlo (9.999 amostras normais com parâmetros estimados; mínimo 0,0001); '
      'Lilliefors: p-valor pela aproximação analítica de Dallal-Wilkinson.')
''')

code(r'''
cores_amostra = {'Todas as sentenças': '#5B7389'} | CORES_GRUPO


def p_norm(amostra, teste):
    linha = tab_norm[(tab_norm['Amostra'] == amostra) & (tab_norm['Teste'] == teste)].iloc[0]
    return f"{teste}: {linha['Estatística']}; p Holm {'< 0,001' if linha['p (Holm)'] < 0.001 else '= ' + fmt_p(linha['p (Holm)'])}"


# (1) QQ-plots: Shapiro-Wilk e Anderson-Darling
fig, ax = plt.subplots(2, 2, figsize=(11, 8.5))
for a, (nome, x) in zip(ax.flat, AMOSTRAS_NORM.items()):
    x = x.to_numpy(float); cor = cores_amostra[nome]
    (osm, osr), (incl, inter, r) = stats.probplot(x, dist='norm')
    a.scatter(osm, osr, s=8, color=cor, alpha=0.6, lw=0)
    a.plot(osm, inter + incl * osm, color=TINTA, lw=1.2)
    a.set_title(f'{nome} (n = {len(x)})')
    a.set_xlabel('Quantil da normal padrão'); a.set_ylabel(ROTULOS['tempo_sentenca'])
    a.grid(axis='both', visible=True)
    anotar_teste(a, p_norm(nome, 'Shapiro-Wilk') + '\n' + p_norm(nome, 'Anderson-Darling'), loc='upper left', tamanho=8)
figura(fig, 'exp_norm_qq', 'QQ-plots: em todos os grupos os tempos se afastam da normal nas duas caudas', secao='2.3',
       nota='linha = normal com a média e o desvio-padrão da amostra.')

# (2) Histogramas com a normal ajustada: D'Agostino-Pearson e Jarque-Bera
fig, ax = plt.subplots(2, 2, figsize=(11, 8.5))
for a, (nome, x) in zip(ax.flat, AMOSTRAS_NORM.items()):
    x = x.to_numpy(float); cor = cores_amostra[nome]
    a.hist(x, bins=np.arange(0, 240, 10), density=True, color=cor, alpha=0.55, edgecolor='white')
    grade = np.linspace(-50, 240, 300)
    a.plot(grade, stats.norm.pdf(grade, x.mean(), x.std(ddof=1)), color=TINTA, lw=1.2, label='normal ajustada')
    a.set_title(f'{nome} (n = {len(x)})')
    a.set_xlabel(ROTULOS['tempo_sentenca']); a.set_ylabel('Densidade')
    a.ticklabel_format(axis='y', style='plain')
    anotar_teste(a, p_norm(nome, "D'Agostino-Pearson") + '\n' + p_norm(nome, 'Jarque-Bera')
                 + f'\nassimetria = {fmt_br(stats.skew(x, bias=False), 2)}; curtose = {fmt_br(stats.kurtosis(x, bias=False), 2)}',
                 loc='upper right', tamanho=8)
    a.set_ylim(0, a.get_ylim()[1] * 1.35)
figura(fig, 'exp_norm_hist', 'Histogramas e normal ajustada: os tempos são bimodais, não em sino', secao='2.3',
       nota='classes de 10 dias; escala linear.')

# (3) ECDF × normal: Lilliefors
fig, ax = plt.subplots(2, 2, figsize=(11, 8.5))
for a, (nome, x) in zip(ax.flat, AMOSTRAS_NORM.items()):
    x = x.to_numpy(float); cor = cores_amostra[nome]
    xs = np.sort(x); ecdf = np.arange(1, len(xs) + 1) / len(xs)
    fi = stats.norm.cdf(xs, x.mean(), x.std(ddof=1))
    k = np.argmax(np.abs(ecdf - fi))
    a.step(xs, ecdf, where='post', color=cor, label='ECDF')
    a.plot(xs, fi, color=TINTA, lw=1.2, label='normal ajustada')
    a.vlines(xs[k], min(ecdf[k], fi[k]), max(ecdf[k], fi[k]), color=DESTAQUE, lw=2.5, label='D máximo')
    a.set_title(f'{nome} (n = {len(x)})')
    a.set_xlabel(ROTULOS['tempo_sentenca']); a.set_ylabel('Proporção acumulada')
    a.grid(axis='both', visible=True); a.legend(loc='lower right')
    anotar_teste(a, p_norm(nome, 'Lilliefors') + f'\nem {fmt_br(xs[k], 0)} dias', loc='upper left', tamanho=8)
figura(fig, 'exp_norm_ecdf', 'ECDF × normal (Lilliefors): a maior distância aparece no início, nas extinções precoces',
       secao='2.3')
''')

interp('exp_normalidade')

# =====================================================================
md(r'''
## 2.4 Ajuste de distribuições ao tempo **com censura**

**Por que com censura.** O notebook do professor ajustou Weibull, gama, log-normal e exponencial por máxima verossimilhança aos 943 tempos como se fossem todos completos, descartou os zeros e deixou o parâmetro de locação livre (E25). Com censura, a verossimilhança correta é (COLOSIMO; GIOLO, 2006, cap. 3):

L(θ) = ∏ f(tᵢ; θ)^δᵢ · S(tᵢ; θ)^(1 − δᵢ),

em que os sentenciados contribuem com a densidade e os censurados, com a probabilidade de durar **mais** do que o tempo observado. Usa-se `tempo_pos` (zeros → 0,5 dia) e `evento` (redistribuição como censura; a alternativa de riscos competitivos fica para a Parte IV).

**Modelos** (COLOSIMO; GIOLO, 2006, p. 70-81; MORETTIN; SINGER, 2021, p. 246):

| Modelo | Parâmetros | Forma do risco h(t) |
|---|---|---|
| Exponencial | 1 | constante |
| Weibull | 2 | monótona (crescente se ρ > 1) |
| Log-normal | 2 | sobe e depois desce |
| Log-logística | 2 | monótona decrescente ou sobe e desce |
| Gama generalizada | 3 | contém as anteriores (exceto a log-logística) como casos particulares |
| Exponencial por partes | 7 | constante em cada janela (0-15, 15-30, 30-60, 60-90, 90-120, 120-150, > 150 dias): estimativa quase não paramétrica da forma do risco |

**Seleção:** (i) AIC e BIC (menor é melhor; o BIC penaliza mais os parâmetros); (ii) **teste da razão de verossimilhanças (TRV)** dos modelos encaixados na gama generalizada: TRV = 2[log L(gama gen.) − log L(modelo)] ~ χ² com g.l. = diferença de parâmetros (COLOSIMO; GIOLO, 2006, p. 93-94, 100-101). H0: o modelo mais simples é suficiente; H1: a gama generalizada ajusta melhor. A log-logística não é encaixada e só se compara por AIC; (iii) gráficos (p. 96-99).
''')

code(r'''
T_pos = d2['tempo_pos'].astype(float).to_numpy()
E_ev = d2['E'].to_numpy()
n_obs = len(T_pos)
MODELOS = {'Exponencial': ExponentialFitter(), 'Weibull': WeibullFitter(), 'Log-normal': LogNormalFitter(),
           'Log-logística': LogLogisticFitter(), 'Gama generalizada': GeneralizedGammaFitter(),
           'Exponencial por partes': PiecewiseExponentialFitter(breakpoints=[15, 30, 60, 90, 120, 150])}
ajustes = {nome: f.fit(T_pos, E_ev, label=nome) for nome, f in MODELOS.items()}


def mediana_modelo(f, p=0.5):
    # Tempo t com S(t) = p (raiz numérica; o median_survival_time_ do lifelines falha com o numpy atual)
    from scipy.optimize import brentq
    return brentq(lambda t: float(f.survival_function_at_times(np.array([t])).iloc[0]) - p, 1e-6, 5000)


linhas = []
for nome, f in ajustes.items():
    k = len(f.params_)
    linhas.append({'Modelo': nome, 'parâmetros': k, 'log L': f.log_likelihood_, 'AIC': f.AIC_,
                   'BIC': k * np.log(n_obs) - 2 * f.log_likelihood_,
                   'mediana S(t)=0,5 (dias)': mediana_modelo(f),
                   'S(90) (prob. sem sentença aos 90 d)': float(f.survival_function_at_times(np.array([90.0])).iloc[0])})
tab_ajuste = pd.DataFrame(linhas).set_index('Modelo')
tab_ajuste['ΔAIC'] = tab_ajuste['AIC'] - tab_ajuste['AIC'].min()
tabela(tab_ajuste, 'exp_ajuste', 'Modelos paramétricos ajustados com censura (938 processos): verossimilhança e critérios',
       secao='2.4', formatos={'S(90) (prob. sem sentença aos 90 d)': 3, 'parâmetros': 'int'}, casas=1,
       destaque=lambda t: t['AIC'].eq(t['AIC'].min()).to_numpy(),
       nota='menor AIC/BIC = melhor; linha destacada = menor AIC.')

gg = ajustes['Gama generalizada']
print('Parâmetros da gama generalizada:', gg.params_.round(4).to_dict())
trv = []
for nome, gl in [('Exponencial', 2), ('Weibull', 1), ('Log-normal', 1)]:
    est = 2 * (gg.log_likelihood_ - ajustes[nome].log_likelihood_)
    trv.append({'H0 (modelo encaixado)': nome, 'TRV': est, 'g.l.': gl, 'p': stats.chi2.sf(est, gl)})
tab_trv = pd.DataFrame(trv)
tab_trv['p (Holm)'] = multipletests(tab_trv['p'], method='holm')[1]
tabela(tab_trv, 'exp_trv', 'Teste da razão de verossimilhanças contra a gama generalizada (H0: o modelo encaixado basta)',
       secao='2.4', casas=2, destaque='p (Holm)')

# Sensibilidade à substituição dos tempos zero (0,5 dia) por 0,1 e 1 dia
sens_zero = {}
for sub_ in (0.1, 0.5, 1.0):
    T_sub = np.where(d2['T'].to_numpy(float) == 0, sub_, d2['T'].to_numpy(float))
    sens_zero[f'zeros → {fmt_br(sub_, 1)} d'] = {nome: type(f)(**({'breakpoints': [15, 30, 60, 90, 120, 150]}
                                                               if nome == 'Exponencial por partes' else {}))
                                                  .fit(T_sub, E_ev).AIC_ for nome, f in MODELOS.items()}
tab_sens_zero = pd.DataFrame(sens_zero)
tabela(tab_sens_zero.rename_axis('Modelo'), 'exp_sens_zero',
       'Sensibilidade do AIC ao valor atribuído aos tempos zero', secao='2.4', casas=1,
       nota='cada coluna reajusta os seis modelos com os tempos zero substituídos pelo valor indicado.')
print('Ordem por AIC em cada substituição:',
      {c: list(tab_sens_zero[c].sort_values().index) for c in tab_sens_zero.columns})
''')

md(r'''
**Gráficos de adequação.** Cada teste ou critério tem o seu gráfico:

1. **QQ-plots para dados censurados** (`lifelines.plotting.qq_plot`): quantis do modelo contra quantis do KM; pontos sobre a diagonal = bom ajuste. Disponível para os quatro modelos de dois parâmetros ou menos.
2. **Ŝ_KM(t) × Ŝ_modelo(t)** (COLOSIMO; GIOLO, 2006, p. 96-97): para cada tempo de evento, a sobrevivência estimada pelo KM contra a do modelo; o modelo adequado fica perto de y = x. É o gráfico que acompanha o TRV.
3. **Sobreposição das curvas S(t)** paramétricas ao Kaplan-Meier (descendente, com IC de 95%), um painel por modelo, para que cada curva seja comparada sozinha com o KM. É só uma verificação visual: a análise do KM, por grupo, está na Parte IV.
''')

code(r'''
kmf_total = KaplanMeierFitter().fit(T_pos, E_ev, label='Kaplan-Meier')
fig, ax = plt.subplots(2, 2, figsize=(10, 9))
for a, nome in zip(ax.flat, ['Exponencial', 'Weibull', 'Log-normal', 'Log-logística']):
    qq_plot(ajustes[nome], ax=a, scatter_color='#5B7389')
    a.set_title(f'{nome} (ΔAIC = {fmt_br(tab_ajuste.loc[nome, "ΔAIC"], 1)})')
    a.grid(axis='both', visible=True)
    if a.get_legend() is not None:
        a.get_legend().remove()
figura(fig, 'exp_qq_censurado', 'QQ-plots com censura: nenhum modelo de dois parâmetros segue a diagonal', secao='2.4',
       nota='quantis do modelo paramétrico (eixo x) contra quantis do Kaplan-Meier (eixo y), em dias.')

t_ev = np.sort(np.unique(T_pos[E_ev == 1]))
s_km = kmf_total.survival_function_at_times(t_ev).to_numpy()
fig, ax = plt.subplots(2, 3, figsize=(13, 8.5))
for a, (nome, f) in zip(ax.flat, ajustes.items()):
    s_mod = f.survival_function_at_times(t_ev).to_numpy()
    a.scatter(s_mod, s_km, s=8, color='#5B7389', lw=0)
    a.plot([0, 1], [0, 1], color=TINTA, lw=1)
    a.set_xlabel(f'Ŝ(t) {nome}'); a.set_ylabel('Ŝ(t) Kaplan-Meier')
    a.set_xlim(0, 1); a.set_ylim(0, 1); a.set_aspect('equal'); a.grid(axis='both', visible=True)
    a.set_title(nome)
    anotar_teste(a, f'máx |ΔS| = {fmt_br(np.max(np.abs(s_mod - s_km)), 3)}', loc='upper left', tamanho=8)
figura(fig, 'exp_skm_smodelo', 'Ŝ do Kaplan-Meier contra Ŝ de cada modelo: o bom ajuste fica sobre a diagonal', secao='2.4',
       nota='um ponto por tempo de sentença distinto; diagonal = concordância perfeita.')

grade = np.linspace(0.5, 275, 400)
ci_km = kmf_total.confidence_interval_survival_function_
fig, ax = plt.subplots(2, 3, figsize=(13, 8), sharex=True, sharey=True)
for a, (nome, f) in zip(ax.flat, ajustes.items()):
    a.fill_between(ci_km.index, ci_km.iloc[:, 0], ci_km.iloc[:, 1], step='post', color=TINTA, alpha=0.12, lw=0)
    a.step(kmf_total.survival_function_.index, kmf_total.survival_function_.iloc[:, 0], where='post', color=TINTA,
           lw=1.8, label='Kaplan-Meier (IC 95%)')
    a.plot(grade, f.survival_function_at_times(grade), color=DESTAQUE, lw=1.8, label='modelo')
    a.set_title(f'{nome} (ΔAIC = {fmt_br(tab_ajuste.loc[nome, "ΔAIC"], 1)})')
    a.set_ylim(0, 1.02); a.grid(axis='both', visible=True)
for a in ax[1]:
    a.set_xlabel(ROTULOS['dias'])
for a in ax[:, 0]:
    a.set_ylabel(ROTULOS['S'])
ax[0, 0].legend(loc='upper right')
figura(fig, 'exp_km_parametricos', 'Kaplan-Meier e curvas paramétricas ajustadas com censura, um modelo por painel',
       secao='2.4', nota=f'todos os 938 processos; tempos zero substituídos por 0,5 dia. Mediana do KM = '
                         f'{fmt_br(kmf_total.median_survival_time_, 0)} dias.')
''')

interp('exp_ajuste_censurado')

md(r'''
### 2.4.1 Forma da função de risco

A função de risco h(t) é a taxa instantânea de sentença entre os processos ainda sem sentença no dia *t*. Comparam-se: o risco estimado por Nelson-Aalen suavizado (núcleo de 15 dias; não paramétrico), o da exponencial por partes (degraus) e os dos modelos paramétricos, um modelo por painel, sempre contra a mesma curva não paramétrica. **Como ler:** um risco crescente significa que, quanto mais antigo o processo, maior a chance de ser sentenciado no dia seguinte (fila que anda); um pico no início indica extinções precoces; um risco que cai na cauda indica processos "travados".
''')

code(r'''
naf = NelsonAalenFitter().fit(T_pos, E_ev)
h_suave = naf.smoothed_hazard_(bandwidth=15)
pwe = ajustes['Exponencial por partes']
h_suave = h_suave[h_suave.index <= 230]   # o núcleo perde suporte na cauda (poucos processos em risco)
cortes_pwe = [0] + [float(b) for b in pwe.breakpoints if np.isfinite(b)] + [275]
taxas = 1 / pwe.summary.loc[[p for p in pwe.summary.index if p.startswith('lambda_')], 'coef'].to_numpy()
fig, ax = plt.subplots(2, 3, figsize=(13, 7.5), sharex=True, sharey=True)
paineis_h = ['Exponencial por partes', 'Exponencial', 'Weibull', 'Log-normal', 'Log-logística', 'Gama generalizada']
for a, nome in zip(ax.flat, paineis_h):
    a.plot(h_suave.index, h_suave.iloc[:, 0], color=TINTA, lw=1.8, label='Nelson-Aalen suavizado (15 d)')
    if nome == 'Exponencial por partes':
        a.step(cortes_pwe, list(taxas) + [taxas[-1]], where='post', color=DESTAQUE, lw=1.8, label='modelo')
    else:
        a.plot(grade, ajustes[nome].hazard_at_times(grade), color=DESTAQUE, lw=1.8, label='modelo')
    a.set_title(nome); a.set_ylim(0, 0.035); a.grid(axis='both', visible=True)
for a in ax[1]:
    a.set_xlabel(ROTULOS['dias'])
for a in ax[:, 0]:
    a.set_ylabel('h(t): sentenças por\nprocesso-dia em risco')
ax[0, 0].legend(loc='upper right')
figura(fig, 'exp_risco', 'Forma do risco de sentença: pico inicial, vale e subida, que nenhum modelo de 2 parâmetros reproduz',
       secao='2.4.1', nota='eixo vertical cortado em 0,035; Nelson-Aalen mostrado até 230 dias (o núcleo perde suporte na cauda).')
tab_pwe = pd.DataFrame({'janela (dias)': [f'{a:g}–{b:g}' for a, b in zip(cortes_pwe[:-1], cortes_pwe[1:])],
                        'risco diário': taxas, 'meia-vida na janela (dias)': np.log(2) / taxas})
tabela(tab_pwe.rename(columns={'janela (dias)': 'Janela (dias)', 'risco diário': 'Risco diário (sentenças/processo-dia)',
                               'meia-vida na janela (dias)': 'Meia-vida na janela (dias)'}),
       'exp_pwe', 'Exponencial por partes: risco diário de sentença em cada janela de tempo', secao='2.4.1',
       formatos={'Risco diário (sentenças/processo-dia)': 4, 'Meia-vida na janela (dias)': 1})
''')

interp('exp_risco')

md(r'''
### 2.4.2 Comparação: ajuste ingênuo só com os sentenciados (`scipy.stats`)

Para mostrar o que muda, ajustam-se as mesmas famílias (exponencial, Weibull, gama, log-normal e log-logística, todas com locação fixa em zero, `floc = 0`) **apenas às 708 sentenças**, como se fossem a população. O teste de Kolmogorov-Smirnov (H0: as sentenças seguem a distribuição ajustada) é exibido com a ressalva de que, com parâmetros estimados nos mesmos dados, o p-valor do KS é conservador (é o problema que o Lilliefors corrige para a normal). O ponto principal é a **mediana implícita**: o ajuste só nos sentenciados descreve a distribuição *condicional* e subestima a duração, porque ignora os 230 processos que ainda não terminaram. O ajuste com censura (seção 2.4) é o correto.
''')

code(r'''
x_sent = sent['tempo_pos'].to_numpy(float)
FAMILIAS = {'Exponencial': stats.expon, 'Weibull': stats.weibull_min, 'Gama': stats.gamma,
            'Log-normal': stats.lognorm, 'Log-logística': stats.fisk}
linhas, dens = [], {}
for nome, dist in FAMILIAS.items():
    par = dist.fit(x_sent, floc=0)
    ll = dist.logpdf(x_sent, *par).sum()
    k = len(par) - 1
    ks = stats.kstest(x_sent, dist.cdf, args=par)
    mediana_cens = mediana_modelo(ajustes[nome]) if nome in ajustes else np.nan
    linhas.append({'Família': nome, 'log L': ll, 'AIC': 2 * k - 2 * ll, 'KS D': ks.statistic, 'KS p': ks.pvalue,
                   'mediana (só sentenças)': dist.median(*par), 'mediana (ajuste com censura)': mediana_cens})
    dens[nome] = (dist, par)
tab_scipy = pd.DataFrame(linhas).set_index('Família')
tab_scipy['ΔAIC'] = tab_scipy['AIC'] - tab_scipy['AIC'].min()
tabela(tab_scipy.rename(columns={'KS p': 'p (KS)', 'mediana (só sentenças)': 'Mediana só sentenças (dias)',
                                 'mediana (ajuste com censura)': 'Mediana com censura (dias)'}),
       'exp_ajuste_ingenuo', 'Ajuste ingênuo só às 708 sentenças (sem censura) e mediana implícita', secao='2.4.2',
       formatos={'KS D': 3}, casas=1, nota='o p do KS com parâmetros estimados nos mesmos dados é conservador.')
print(f'Mediana empírica das sentenças: {fmt_br(np.median(x_sent))} dias | '
      f'mediana do KM (todos, com censura): {fmt_br(kmf_total.median_survival_time_)} dias')

fig, ax = plt.subplots(2, 3, figsize=(13, 8))
grade2 = np.linspace(0.5, 240, 400)
for a, (nome, (dist, par)) in zip(ax.flat, dens.items()):
    a.hist(x_sent, bins=np.arange(0, 240, 10), density=True, color=CINZA, alpha=0.6, edgecolor='white')
    a.plot(grade2, dist.pdf(grade2, *par), lw=1.8, color=DESTAQUE)
    a.set_ylim(0, 0.02); a.set_title(nome)
    a.set_xlabel(ROTULOS['tempo_sentenca']); a.set_ylabel('Densidade')
    anotar_teste(a, texto_teste('Kolmogorov-Smirnov', f'D = {fmt_br(tab_scipy.loc[nome, "KS D"], 3)}',
                                tab_scipy.loc[nome, 'KS p']), loc='upper right', tamanho=8)
med = tab_scipy[['mediana (só sentenças)', 'mediana (ajuste com censura)']].rename(
    columns={'mediana (só sentenças)': 'Só sentenças', 'mediana (ajuste com censura)': 'Com censura'})
barras_agrupadas(ax[1, 2], med.dropna(), cores={'Só sentenças': CINZA, 'Com censura': TINTA}, rotular=True,
                 fmt=lambda v: fmt_br(v, 0), quebrar=9, ylabel='Mediana implícita (dias)')
ax[1, 2].set_title('Mediana: sem × com censura')
ax[1, 2].legend(loc='upper left', fontsize=8)
ax[1, 2].tick_params(axis='x', labelsize=8)
figura(fig, 'exp_ajuste_ingenuo', 'Ajustar só às sentenças subestima a duração: a mediana implícita é menor que a do ajuste com censura',
       secao='2.4.2', nota=f'histograma = 708 sentenças (classes de 10 dias); curva = densidade ajustada. Mediana empírica das '
                         f'sentenças: {fmt_br(np.median(x_sent))} dias; mediana do KM (com censura): '
                         f'{fmt_br(kmf_total.median_survival_time_)} dias.')
''')

interp('exp_scipy_encerrados')

# =====================================================================
md(r'''
## 2.5 Modelos binomial e multinomial: o desenho e as proporções

Esta seção usa o modelo **binomial** (uma proporção) e o **multinomial** (várias categorias com probabilidades fixadas) para responder a perguntas univariadas sobre o desenho e sobre as taxas. Em cada caso: a hipótese, o teste, o IC e o gráfico. Os ICs de proporção são o **exato de Clopper-Pearson** (conservador, cobertura ≥ 95%) e o **de Wilson** (cobertura mais próxima de 95%, recomendado para proporções pequenas); o IC de Wald (p ± 1,96·EP) é evitado porque falha justamente nas taxas de acordo, próximas de zero.

### 2.5.1 (a) O sorteio produziu grupos equilibrados demais?

**Pergunta.** Se cada processo fosse sorteado de forma independente com probabilidade 1/3 para cada grupo (**aleatorização simples**), os tamanhos dos grupos seguiriam uma multinomial(n; 1/3, 1/3, 1/3). Divisões como **314/316/314** (Controle/Presencial/Remota nas 944 linhas brutas) ou **313/314/311** (a base primária de 938) são compatíveis com isso?

- **Teste usual (cauda direita):** qui-quadrado de aderência, H0: p = (1/3, 1/3, 1/3); H1: algum grupo tem probabilidade diferente. Responde "os grupos são desiguais demais?".
- **Teste de "bom demais" (cauda esquerda):** P(X² ≤ X²_obs | H0), calculada **exatamente**, somando a probabilidade multinomial de todas as divisões (a, b, c) com a + b + c = n tão ou mais equilibradas que a observada. Um valor muito pequeno significa que, sob aleatorização simples, uma divisão tão equilibrada seria improvável, o que é indício de **aleatorização restrita** (em blocos, urna sem reposição ou alternância), compatível com a informação de que o sorteio "seguiu rigorosamente a ordem de chegada" (questão 2.7).

A aleatorização restrita não é um defeito: é prática recomendada para equilibrar os grupos. Mas ela precisa ser documentada, porque (i) muda a análise da sequência (teste de corridas, Parte III) e (ii) se os blocos forem pequenos e conhecidos, o próximo grupo fica previsível.
''')

code(r'''
def multinomial_exato(contagens, p=None):
    # Probabilidades exatas, sob multinomial(n; p), de X² <= X²_obs (cauda esquerda) e X² >= X²_obs (direita); k = 3
    contagens = np.asarray(contagens); n = int(contagens.sum())
    p = np.full(3, 1 / 3) if p is None else np.asarray(p)
    esp = n * p
    x2_obs = ((contagens - esp) ** 2 / esp).sum()
    esq = dir_ = 0.0
    for a in range(n + 1):
        b = np.arange(n - a + 1); c = n - a - b
        x2 = (a - esp[0]) ** 2 / esp[0] + (b - esp[1]) ** 2 / esp[1] + (c - esp[2]) ** 2 / esp[2]
        lp = (gammaln(n + 1) - gammaln(a + 1) - gammaln(b + 1) - gammaln(c + 1)
              + a * np.log(p[0]) + b * np.log(p[1]) + c * np.log(p[2]))
        pr = np.exp(lp)
        esq += pr[x2 <= x2_obs + 1e-9].sum()
        dir_ += pr[x2 >= x2_obs - 1e-9].sum()
    return x2_obs, esq, dir_


divisoes = {'944 linhas brutas': brutas['grupo'].value_counts().reindex(ORDEM_GRUPO).to_numpy(),
            '938 processos (base primária)': d2['grupo'].value_counts().reindex(ORDEM_GRUPO).to_numpy()}
linhas = []
for nome, cont in divisoes.items():
    x2, esq, dir_ = multinomial_exato(cont)
    linhas.append({'Base': nome, 'Controle': cont[0], 'Presencial': cont[1], 'Remota': cont[2],
                   'esperado (n/3)': cont.sum() / 3, 'X²': x2, 'p qui-quadrado (dir.)': stats.chi2.sf(x2, 2),
                   'p exato (dir.)': dir_, 'P(divisão tão equilibrada) exata (esq.)': esq,
                   'amplitude máx − mín': cont.max() - cont.min()})
tab_equilibrio = pd.DataFrame(linhas).set_index('Base')
tabela(tab_equilibrio, 'exp_equilibrio', 'Tamanhos dos grupos contra a aleatorização simples (multinomial 1/3, 1/3, 1/3)',
       secao='2.5.1', casas=2,
       formatos={'X²': 4, 'P(divisão tão equilibrada) exata (esq.)': lambda v: fmt_p(v, 4)},
       nota='cauda direita: os grupos são desiguais demais? Cauda esquerda: uma divisão tão equilibrada seria provável '
            'sob sorteio simples?')

# Monte Carlo: distribuição da amplitude (máx − mín) sob aleatorização simples
sim = RNG.multinomial(len(d2), [1 / 3] * 3, size=200_000)
amp_sim = sim.max(axis=1) - sim.min(axis=1)
x2_sim = ((sim - len(d2) / 3) ** 2 / (len(d2) / 3)).sum(axis=1)
amp_obs = tab_equilibrio.loc['938 processos (base primária)', 'amplitude máx − mín']
print(f'Monte Carlo (200.000 sorteios simples de 938): P(amplitude ≤ {amp_obs}) = {fmt_br((amp_sim <= amp_obs).mean(), 4)}; '
      f'amplitude mediana = {np.median(amp_sim):.0f} processos; P90 = {np.percentile(amp_sim, 90):.0f}')
''')

code(r'''
def p_igual(p):
    return 'p < 0,001' if p < 0.001 else f'p = {fmt_p(p)}'


fig, ax = plt.subplots(1, 2, figsize=(13, 4.6))
x2_938 = tab_equilibrio.loc['938 processos (base primária)', 'X²']
p_esq = tab_equilibrio.loc['938 processos (base primária)', 'P(divisão tão equilibrada) exata (esq.)']
ax[0].hist(x2_sim, bins=np.arange(0, 12.5, 0.25), density=True, color=CINZA, alpha=0.7, edgecolor='white',
           label='X² sob aleatorização simples (simulado)')
g = np.linspace(0.001, 12, 300)
ax[0].plot(g, stats.chi2.pdf(g, 2), color=TINTA, lw=1.5, label='χ² com 2 g.l.')
ax[0].axvline(x2_938, color=DESTAQUE, lw=2, label=f'observado (938): X² = {fmt_br(x2_938, 4)}')
ax[0].set_xlabel('X² de aderência a (1/3, 1/3, 1/3)'); ax[0].set_ylabel('Densidade'); ax[0].legend(loc='center right')
ax[0].set_title('(a) O X² observado fica na cauda esquerda')
anotar_teste(ax[0], texto_teste('Multinomial exato', f'X² = {fmt_br(x2_938, 4)}',
                                extra=f'P(divisão tão equilibrada) = {fmt_p(p_esq, 4)}'), loc='upper right')
v, c = np.unique(amp_sim, return_counts=True)
m = v <= 80
ax[1].bar(v[m], c[m] / len(amp_sim), width=1, color=CINZA, edgecolor='white', linewidth=0.3)
ax[1].axvline(amp_obs, color=DESTAQUE, lw=2, label=f'observado: {amp_obs} processos')
ax[1].set_xlabel('Amplitude entre o maior e o menor grupo (processos)'); ax[1].set_ylabel('Probabilidade')
ax[1].set_title('(b) Amplitude sob aleatorização simples (Monte Carlo)'); ax[1].legend(loc='upper right')
anotar_teste(ax[1], f'P(amplitude ≤ {amp_obs}) = {fmt_br((amp_sim <= amp_obs).mean(), 4)}\n200.000 sorteios simulados',
             loc='center right')
figura(fig, 'exp_equilibrio', 'Grupos equilibrados demais para um sorteio simples: indício de aleatorização restrita',
       secao='2.5.1')
''')

md(r'''
**O equilíbrio ao longo da sequência.** Se o equilíbrio vier de blocos pequenos, a diferença entre o número acumulado de processos de cada grupo e k/3 (após os k primeiros processos) fica sempre pequena; numa aleatorização simples, ela oscila como um passeio aleatório (da ordem de √k); numa **urna sem reposição** com totais fixados (permutação aleatória de uma lista equilibrada), ela oscila no meio e volta a zero no fim. Calcula-se D = máx_k máx_g |N_g(k) − k/3| e compara-se com 5.000 simulações de cada mecanismo. Em paralelo, o teste de aderência a 1/3 é aplicado **mês a mês** (p exato multinomial, cauda direita, com Holm para 8 meses): blocos pequenos produziriam equilíbrio também dentro dos meses.
''')

code(r'''
seq = d2.sort_values('ordem_chegada')['grupo'].astype(str).to_numpy()
ind = np.stack([(seq == g) for g in ORDEM_GRUPO], axis=1).astype(float)
k = np.arange(1, len(seq) + 1)[:, None]
desvio_obs = ind.cumsum(axis=0) - k / 3
D_obs = np.abs(desvio_obs).max()

n_sim = 5000
rng_seq = np.random.default_rng(SEMENTE)
sim_simples = rng_seq.integers(0, 3, size=(n_sim, len(seq)))
sim_urna = np.array([rng_seq.permutation(np.repeat([0, 1, 2], [313, 314, 311])) for _ in range(n_sim)])
def estat_D(sims):
    out = np.empty(len(sims))
    for g in range(3):
        dev = np.abs(np.cumsum(sims == g, axis=1) - np.arange(1, sims.shape[1] + 1) / 3).max(axis=1)
        out = dev if g == 0 else np.maximum(out, dev)
    return out
D_simples, D_urna = estat_D(sim_simples), estat_D(sim_urna)
print(f'D observado = {fmt_br(D_obs, 1)} processos')
print(f'Aleatorização simples: D mediano = {fmt_br(np.median(D_simples), 1)}; P(D ≤ D_obs) = {fmt_br((D_simples <= D_obs).mean(), 4)}')
print(f'Urna sem reposição (totais fixos): D mediano = {fmt_br(np.median(D_urna), 1)}; P(D ≤ D_obs) = {fmt_br((D_urna <= D_obs).mean(), 4)}')

linhas = []
for mes in MESES:
    cont = cont_mes.loc[mes].to_numpy()
    x2, _, p_dir = multinomial_exato(cont)
    linhas.append({'Mês': mes, 'Controle': cont[0], 'Presencial': cont[1], 'Remota': cont[2], 'n': cont.sum(),
                   'X²': x2, 'p exato': p_dir})
tab_mes_gof = pd.DataFrame(linhas).set_index('Mês')
tab_mes_gof['p (Holm)'] = multipletests(tab_mes_gof['p exato'], method='holm')[1]
tabela(tab_mes_gof, 'exp_aderencia_mes', 'Aderência a 1/3 dentro de cada mês (multinomial exato, cauda direita)',
       secao='2.5.1', casas=2, destaque='p (Holm)', nota='Holm sobre os 8 meses; linhas destacadas: p < 0,05.')

fig, ax = plt.subplots(1, 2, figsize=(13, 4.6))
env = np.percentile(np.abs(np.cumsum(sim_simples == 0, axis=1) - np.arange(1, len(seq) + 1) / 3), 95, axis=0)
ax[0].fill_between(k[:, 0], -env, env, color='#E8E8E8', lw=0, label='95% sob aleatorização simples')
for j, g in enumerate(ORDEM_GRUPO):
    ax[0].plot(k[:, 0], desvio_obs[:, j], color=CORES_GRUPO[g], lw=1.2, label=g)
ax[0].axhline(0, color=TINTA_2, lw=0.8)
ax[0].set_xlabel(ROTULOS['ordem_chegada']); ax[0].set_ylabel('Desequilíbrio acumulado N_g(k) − k/3 (processos)')
ax[0].legend(loc='lower left', ncol=2)
ax[0].set_title('(a) Desequilíbrio acumulado ao longo da sequência')
ax[1].hist(D_simples, bins=40, color=CINZA, density=True, alpha=0.7, label='aleatorização simples')
ax[1].hist(D_urna, bins=40, color='#5B7389', density=True, alpha=0.6, label='urna (totais fixos)')
ax[1].axvline(D_obs, color=DESTAQUE, lw=2, label=f'observado D = {fmt_br(D_obs, 1)}')
ax[1].set_xlabel('D = maior desequilíbrio acumulado (processos)'); ax[1].set_ylabel('Densidade'); ax[1].legend(loc='upper right')
ax[1].set_title('(b) D observado × mecanismos de sorteio')
anotar_teste(ax[1], f'P(D ≤ D obs.): simples = {fmt_br((D_simples <= D_obs).mean(), 4)}\n'
                    f'urna = {fmt_br((D_urna <= D_obs).mean(), 4)}\n5.000 simulações de cada', loc='center right')
figura(fig, 'exp_sequencia', 'O equilíbrio ao longo da sequência de chegada: compatível com sorteio simples ou com urna?',
       secao='2.5.1')

fig, ax = plt.subplots(figsize=(11, 4.8))
x = np.arange(len(MESES)); w = 0.27
for j, g in enumerate(ORDEM_GRUPO):
    ax.bar(x + (j - 1) * w, tab_mes_gof[g], width=w, color=CORES_GRUPO[g], label=g, edgecolor='white', linewidth=1)
ax.scatter(x, tab_mes_gof['n'] / 3, marker='_', s=500, color=TINTA, linewidths=2, label='esperado (n/3)', zorder=5)
for xi, mes in zip(x, MESES):
    ax.text(xi, tab_mes_gof.loc[mes, ORDEM_GRUPO].max() + 1.5, p_igual(tab_mes_gof.loc[mes, 'p (Holm)']),
            ha='center', fontsize=8, color=TINTA_2)
ax.set_ylim(0, tab_mes_gof[ORDEM_GRUPO].to_numpy().max() * 1.22)
ax.set_xticks(x, [f'{m_}\n(n = {int(tab_mes_gof.loc[m_, "n"])})' for m_ in MESES])
ax.set_xlabel(ROTULOS['mes_distribuicao']); ax.set_ylabel('Processos distribuídos')
ax.grid(axis='x', visible=False); ax.legend(loc='upper left', ncol=4)
figura(fig, 'exp_aderencia_mes', 'Aderência a 1/3 em cada mês: em que meses a divisão entre grupos se afasta do esperado?',
       secao='2.5.1', nota='acima de cada mês: p exato multinomial (cauda direita) com correção de Holm para 8 meses.')
''')

interp('exp_balanco')

md(r'''
### 2.5.2 (b) Taxas de acordo: modelo binomial com referência externa

**Referência documentada.** O resumo expandido informa que o índice de conciliação do 4º JEC no GPS-Jus "sempre oscilou em torno de 13 a 14%, estando atualmente no patamar de **13,3%**", antes do experimento, e que o índice nacional dos JECs era **17,22%** em dez./2025. O índice de conciliação do CNJ é **sentenças homologatórias de acordo ÷ total de sentenças**; portanto, a comparação legítima usa o mesmo denominador: homologações entre as sentenças proferidas (não entre os processos distribuídos, como no resumo expandido, que dava 8,06%).

**Testes** (binomial exato bilateral, um por linha):

1. **Homologações / sentenças**, no total e por grupo. H0: p = 0,133 (patamar histórico da unidade); H1: p ≠ 0,133. Pergunta: o índice de conciliação durante o experimento difere do patamar histórico? Ressalva: só as sentenças até 07/10 entram; como os acordos tendem a encerrar processos mais cedo, o índice pode cair à medida que as sentenças de mérito dos ativos forem proferidas.
2. **Acordos na AC / AC realizadas**, por grupo de tratamento. H0: p = 0,133; H1: p ≠ 0,133. Pergunta: a audiência, sozinha, alcança o patamar histórico de conciliação da unidade? É uma comparação de ordem de grandeza (os denominadores são diferentes: audiências × sentenças), mas é a pergunta que o desenho do experimento implicitamente faz.

Holm dentro de cada família (4 e 3 testes). A comparação **entre** grupos (Fisher, qui-quadrado) é da Parte III.
''')

code(r'''
P0_UNIDADE, P0_NACIONAL = 0.133, 0.1722

def linha_binomial(rotulo, k, n, p0):
    bt = stats.binomtest(int(k), int(n), p0)
    cp = bt.proportion_ci(confidence_level=0.95, method='exact')
    wi = bt.proportion_ci(confidence_level=0.95, method='wilson')
    return {'Proporção': rotulo, 'k': int(k), 'n': int(n), 'p̂': k / n, 'H0: p': p0,
            'IC95% Clopper-Pearson': (cp.low, cp.high), 'IC95% Wilson': (wi.low, wi.high), 'p': bt.pvalue}

fam1 = []
for g in [None] + ORDEM_GRUPO:
    s = sent if g is None else sent[sent.grupo.eq(g)]
    fam1.append(linha_binomial(f'Homologações/sentenças — {"Todos" if g is None else g}',
                               s.tipo_desfecho.eq('Homologação').sum(), len(s), P0_UNIDADE))
fam2 = []
for g in [None, 'Presencial', 'Remota']:
    s = ac if g is None else ac[ac.grupo.eq(g)]
    fam2.append(linha_binomial(f'Acordo na AC/AC realizadas — {"P + R" if g is None else g}',
                               s.acordo_ac.sum(), len(s), P0_UNIDADE))
tab_bin = []
for fam in (fam1, fam2):
    t = pd.DataFrame(fam)
    t['p (Holm)'] = multipletests(t['p'], method='holm')[1]
    tab_bin.append(t)
tab_bin = pd.concat(tab_bin, ignore_index=True)

def fmt_ic(ic):
    return f'{pct_br(ic[0])} a {pct_br(ic[1])}'

def tabela_binomial(t, id_, titulo, secao, nota=None):
    saida = t.assign(**{'IC95% Clopper-Pearson': t['IC95% Clopper-Pearson'].map(fmt_ic),
                        'IC95% Wilson': t['IC95% Wilson'].map(fmt_ic)})
    tabela(saida, id_, titulo, secao=secao, formatos={'p̂': 'pct', 'H0: p': 'pct'}, destaque='p (Holm)', nota=nota)


tabela_binomial(tab_bin, 'exp_binom_acordo', 'Taxas de conciliação contra o patamar histórico de 13,3% (binomial exato)', '2.5.2',
                nota='Holm dentro de cada família (4 e 3 testes); linhas destacadas: p de Holm < 0,05.')
print(f'Para comparação: acordos/processos distribuídos (denominador do resumo expandido) = '
      f'{int(d2.acordo.sum())}/{len(d2)} = {pct_br(d2.acordo.sum() / len(d2))} (inclui ativos no denominador)')

def p_txt(p):
    return 'referência' if pd.isna(p) else ('p < 0,001' if p < 0.001 else f'p = {p_br(p)}')


def forest(ax, tab, refs, titulo, cores):
    y = np.arange(len(tab))[::-1]
    xmax = max(0.3, tab['IC95% Clopper-Pearson'].map(lambda c: c[1]).max() + 0.12) + 0.1
    for yi, (_, r), c in zip(y, tab.iterrows(), cores):
        ax.hlines(yi + 0.12, *r['IC95% Clopper-Pearson'], color=c, lw=2.5)
        ax.hlines(yi - 0.12, *r['IC95% Wilson'], color=c, lw=2.5, alpha=0.45)
        ax.plot(r['p̂'], yi, 'o', color=c, ms=7, mec='white', mew=1)
        ax.text(r['IC95% Clopper-Pearson'][1] + 0.008, yi, f"{r['k']}/{r['n']} = {pct_br(r['p̂'])}; {p_txt(r['p (Holm)'])}",
                va='center', fontsize=8.5, color=TINTA)
    for valor, rot, ls in refs:
        ax.axvline(valor, color=DESTAQUE, ls=ls, lw=1, label=rot)
    ax.legend(loc='lower right')
    ax.set_yticks(y, [s.split('— ')[-1] for s in tab['Proporção']])
    ax.set_ylim(-0.7, len(tab) - 0.3)
    ax.set_xlim(0, xmax)
    eixo_pct(ax, 'x')
    ax.grid(axis='y', visible=False); ax.grid(axis='x', visible=True)
    ax.set_title(titulo)

cores_fam1 = [TINTA] + [CORES_GRUPO[g] for g in ORDEM_GRUPO]
cores_fam2 = [TINTA, CORES_GRUPO['Presencial'], CORES_GRUPO['Remota']]
fig, ax = plt.subplots(1, 2, figsize=(14, 4.4))
forest(ax[0], tab_bin.iloc[:4], [(P0_UNIDADE, '13,3% (4º JEC, histórico)', '--'), (P0_NACIONAL, '17,2% (JECs, nacional)', ':')],
       '(a) Homologações entre as sentenças', cores_fam1)
forest(ax[1], tab_bin.iloc[4:], [(P0_UNIDADE, '13,3% (4º JEC, histórico)', '--')],
       '(b) Acordo na AC entre as AC realizadas', cores_fam2)
ax[0].set_xlabel('Proporção (IC 95%)'); ax[1].set_xlabel('Proporção (IC 95%)')
figura(fig, 'exp_binom_acordo', 'Taxas de conciliação durante o experimento contra o patamar histórico da unidade (13,3%)',
       secao='2.5.2', nota='traço escuro: IC exato de Clopper-Pearson; traço claro: IC de Wilson; p de Holm do teste binomial '
                           'exato bilateral contra 13,3%.')
''')

interp('exp_binom_acordo')

md(r'''
**Sentenças sem mérito.** O Controle tem proporcionalmente mais sentenças de mérito e menos extinções sem mérito que os grupos com AC obrigatória. A hipótese jurídica é a do **art. 51, I, da Lei 9.099/1995**: o processo é extinto sem resolução do mérito quando o autor deixa de comparecer a qualquer das audiências. Com a AC obrigatória, surge uma oportunidade de extinção que o rito atual (sem audiência inaugural) não oferece.

**Denominador.** A proporção entre as **sentenças** é condicional: os grupos tratados têm mais processos ainda ativos, e esses tendem a terminar em mérito (as extinções sem mérito são, em geral, mais precoces). Por isso ela superestima a diferença entre os grupos. A proporção entre os **distribuídos** conta como "não sem mérito" os ativos que ainda podem ser extintos e por isso tende a subestimá-la. As duas bases são apresentadas como limites; a estimativa que respeita a censura e o risco competitivo é a incidência acumulada (CIF) da Parte IV.

**Teste** (binomial exato bilateral, descritivo): tomando a proporção de sentenças sem mérito do Controle como **referência fixa** (o rito atual), H0: p_grupo = p_Controle; H1: p_grupo ≠ p_Controle, para Presencial e Remota (Holm, 2 testes). Ao fixar a taxa do Controle, ignora-se a sua incerteza, e o p-valor fica pequeno demais. Por isso o p é apenas indicativo: o que importa aqui são as proporções e os seus IC. O teste de duas amostras (Fisher/qui-quadrado), com IC da diferença, está na Parte III. As tabelas seguintes mostram as duas bases, as faixas de tempo das extinções e, nos grupos tratados, a relação entre a extinção sem mérito e a realização da AC.
''')

code(r'''
p_ctrl = sent[sent.grupo.eq('Controle')].tipo_desfecho.eq('Sem mérito').mean()
linhas = [linha_binomial(f'Sem mérito/sentenças — Controle (referência)',
                         sent[sent.grupo.eq('Controle')].tipo_desfecho.eq('Sem mérito').sum(),
                         sent.grupo.eq('Controle').sum(), p_ctrl)]
for g in ['Presencial', 'Remota']:
    s = sent[sent.grupo.eq(g)]
    linhas.append(linha_binomial(f'Sem mérito/sentenças — {g}', s.tipo_desfecho.eq('Sem mérito').sum(), len(s), p_ctrl))
tab_sm = pd.DataFrame(linhas)
tab_sm['p (Holm)'] = np.r_[np.nan, multipletests(tab_sm['p'].iloc[1:], method='holm')[1]]
tab_sm.loc[0, 'p'] = np.nan
tabela_binomial(tab_sm, 'exp_binom_semmerito', 'Sentenças sem mérito nos grupos com AC contra a taxa do Controle (binomial exato)',
                '2.5.2', nota='a taxa do Controle é tomada como referência fixa (sem teste na sua linha); Holm para 2 testes. '
                              'Denominador = sentenças: limite superior da diferença entre grupos.')

# Duas bases como limites: sentenciados (superestima a diferença) e distribuídos (subestima)
linhas_b = []
for g in ORDEM_GRUPO:
    dg, sg = d2[d2.grupo.eq(g)], sent[sent.grupo.eq(g)]
    k_ = int(dg.tipo_desfecho.eq('Sem mérito').sum())
    for base_, n_ in [('Sentenciados', len(sg)), ('Distribuídos', len(dg))]:
        ci_ = stats.binomtest(k_, n_).proportion_ci(method='wilson')
        linhas_b.append({'Grupo': g, 'Base': base_, 'k': k_, 'n': n_, 'p̂': k_ / n_,
                         'IC95% Wilson': fmt_ic((ci_.low, ci_.high))})
tab_sm_bases = pd.DataFrame(linhas_b)
ref_ctrl = tab_sm_bases[tab_sm_bases.Grupo.eq('Controle')].set_index('Base')['p̂']
tab_sm_bases['Diferença para o Controle (p.p.)'] = 100 * (tab_sm_bases['p̂'] - tab_sm_bases['Base'].map(ref_ctrl))
tabela(tab_sm_bases.set_index(['Grupo', 'Base']), 'exp_semmerito_bases',
       'Extinções sem mérito sobre duas bases: sentenciados e distribuídos (limites da diferença entre grupos)',
       secao='2.5.2', formatos={'p̂': 'pct', 'k': 'int', 'n': 'int'}, casas=1,
       nota='sobre os sentenciados, a diferença é superestimada (os ativos, mais numerosos nos tratados, tendem a terminar '
            'em mérito); sobre os distribuídos, subestimada (ativos ainda podem ser extintos). A incidência acumulada '
            '(CIF), que trata a censura e os riscos competitivos, está na Parte IV.')

# Faixas de tempo das extinções sem mérito (n e % dos distribuídos de cada grupo)
sm_all = sent[sent.tipo_desfecho.eq('Sem mérito')]
FAIXAS_SM = ['até 7 dias', '8 a 30 dias', 'após 30 dias']
faixa_sm = pd.cut(sm_all['T'], [-0.5, 7, 30, np.inf], labels=FAIXAS_SM)
tab_faixa = pd.crosstab(sm_all['grupo'].astype(str), faixa_sm.astype(str)).reindex(index=ORDEM_GRUPO, columns=FAIXAS_SM)
n_grupo = d2['grupo'].astype(str).value_counts().reindex(ORDEM_GRUPO)
tab_faixa.columns.name = None
tab_faixa_pct = 100 * tab_faixa.div(n_grupo, axis=0)
saida_faixa = pd.concat({'n': tab_faixa, '% dos distribuídos': tab_faixa_pct}, axis=1)
saida_faixa['Distribuídos'] = n_grupo
tabela(saida_faixa.rename_axis('Grupo'), 'exp_semmerito_faixas',
       'Extinções sem mérito por faixa de tempo desde a distribuição, por grupo', secao='2.5.2', casas=1,
       nota='% sobre os distribuídos de cada grupo. A faixa "após 30 dias" coincide com a fase da audiência nos grupos tratados.')

trat = sent[sent.grupo.isin(['Presencial', 'Remota'])].copy()
trat['AC'] = trat['ac_realizada'].map({True: 'AC realizada', False: 'AC não realizada'}).fillna('não informado')
tab_sm_ac = pd.crosstab([trat['grupo'].astype(str), trat['AC']], trat['tipo_desfecho'].astype(str))
tab_sm_ac = tab_sm_ac.reindex(columns=['Homologação', 'Mérito', 'Sem mérito'])
tab_sm_ac['mediana dias (sem mérito)'] = trat[trat.tipo_desfecho.eq('Sem mérito')].groupby(['grupo', 'AC'], observed=True)['T'].median()
tabela(tab_sm_ac.rename_axis(index=['Grupo', 'AC'], columns=None)
       .rename(columns={'mediana dias (sem mérito)': 'Mediana do tempo até a extinção sem mérito (dias)'}),
       'exp_semmerito_ac', 'Tipo de sentença nos grupos tratados, segundo a realização da AC', secao='2.5.2', casas=1)

fig, ax = plt.subplots(1, 2, figsize=(14, 4.6), gridspec_kw={'width_ratios': [1.15, 1]})
forest(ax[0], tab_sm, [(p_ctrl, f'Controle: {pct_br(p_ctrl)}', '--')], '(a) Sentenças sem mérito entre as sentenças',
       [CORES_GRUPO[g] for g in ORDEM_GRUPO])
ax[0].set_xlabel('Proporção (IC 95%)')
rng_sm = np.random.default_rng(SEMENTE)
for g, desloc in [('Presencial', -0.2), ('Remota', 0.2)]:
    s = trat[trat.grupo.eq(g) & trat.tipo_desfecho.eq('Sem mérito')]
    for i, rot in enumerate(['AC não realizada', 'AC realizada']):
        v = s.loc[s.AC.eq(rot), 'T'].to_numpy(float)
        if len(v) == 0:
            continue
        bpx = ax[1].boxplot([v], positions=[i + desloc], widths=0.32, patch_artist=True, showfliers=False,
                            medianprops=dict(color=TINTA, lw=2))
        bpx['boxes'][0].set_facecolor(mpl.colors.to_rgba(CORES_GRUPO[g], 0.25)); bpx['boxes'][0].set_edgecolor(CORES_GRUPO[g])
        ax[1].scatter(i + desloc + rng_sm.uniform(-0.1, 0.1, len(v)), v, s=7, color=CORES_GRUPO[g], alpha=0.5, lw=0)
        ax[1].text(i + desloc, -14, f'n = {len(v)}', ha='center', fontsize=8.5, color=TINTA_2)
ax[1].set_xticks([0, 1], ['AC não realizada', 'AC realizada']); ax[1].set_ylim(-24, None)
ax[1].set_ylabel('Dias até a extinção sem mérito'); ax[1].grid(axis='x', visible=False)
ax[1].legend(handles=[mpl.patches.Patch(facecolor=mpl.colors.to_rgba(CORES_GRUPO[g], 0.25), edgecolor=CORES_GRUPO[g], label=g)
                      for g in ['Presencial', 'Remota']], loc='upper right')
ax[1].set_title('(b) Quando ocorre a extinção sem mérito nos grupos tratados')
figura(fig, 'exp_binom_semmerito', 'Os grupos com AC obrigatória têm mais extinções sem mérito que o Controle; quando elas ocorrem?',
       secao='2.5.2', nota='(a) base = sentenças (limite superior da diferença); p de Holm do binomial exato contra a taxa '
                           'do Controle fixada, apenas indicativo (ver a Parte III); (b) cada ponto é um processo.')
''')

interp('exp_binom_semmerito')

md(r'''
### 2.5.3 (c) O sorteio das técnicas de conciliação

**Pergunta.** O protocolo previa o sorteio da técnica em cada audiência. O resumo expandido lista **5** técnicas e afirma que "padrões objetivos" foi a mais usada, com **53,85%**; o professor anotou: "53,85%??? o esperado era 1/5 = 20,0%". O projeto, os apêndices e a planilha têm **6** técnicas (a sexta é "análise da comunicação verbal e não-verbal das partes"). Logo, sob sorteio uniforme, o esperado é **1/6 ≈ 16,7%** para cada uma.

**Testes:**

1. Qui-quadrado de aderência e p exato multinomial por Monte Carlo (200.000 sorteios, estatística X²). H0: as 6 técnicas têm probabilidade 1/6; H1: alguma difere. No total das AC realizadas e em cada grupo (Holm, 3 testes).
2. Binomial exato para "padrões objetivos": H0: p = 1/6 e H0: p = 0,5385 (o valor do resumo expandido).
3. Uma versão com 5 técnicas (1/5), excluída "comunicação verbal e não-verbal", para mostrar o que acontece com o valor esperado do professor.
''')

code(r'''
TECNICAS = list(d2['tecnica_curta'].cat.categories)
def gof_uniforme(cont, n_mc=200_000, semente=SEMENTE):
    cont = np.asarray(cont); n = cont.sum(); kcat = len(cont); esp = n / kcat
    x2 = ((cont - esp) ** 2 / esp).sum()
    sim = np.random.default_rng(semente).multinomial(n, [1 / kcat] * kcat, size=n_mc)
    x2_sim = ((sim - esp) ** 2 / esp).sum(axis=1)
    return x2, stats.chi2.sf(x2, kcat - 1), (x2_sim >= x2 - 1e-9).mean()

linhas = []
for rot, s in [('AC realizadas (P + R)', ac), ('Presencial', ac[ac.grupo.eq('Presencial')]), ('Remota', ac[ac.grupo.eq('Remota')])]:
    cont = s['tecnica_curta'].value_counts().reindex(TECNICAS).to_numpy()
    x2, p_chi, p_mc = gof_uniforme(cont)
    linhas.append({'Amostra': rot, 'n': cont.sum(), **dict(zip(TECNICAS, cont)), 'X² (5 g.l.)': x2,
                   'p qui-quadrado': p_chi, 'p exato (Monte Carlo)': p_mc})
tab_tec = pd.DataFrame(linhas).set_index('Amostra')
tab_tec['p MC (Holm)'] = multipletests(tab_tec['p exato (Monte Carlo)'], method='holm')[1]
tabela(tab_tec, 'exp_tecnicas', 'Sorteio das técnicas: aderência à distribuição uniforme (1/6 para cada técnica)',
       secao='2.5.3', casas=2, destaque='p MC (Holm)', nota='p exato por Monte Carlo (200.000 sorteios); Holm para 3 testes.')

cont5 = ac.loc[ac.tecnica_curta.ne('Comunicação'), 'tecnica_curta'].value_counts().reindex([t for t in TECNICAS if t != 'Comunicação'])
x2_5, p5, p5_mc = gof_uniforme(cont5.to_numpy())
print(f'Versão com 5 técnicas (sem "Comunicação", n = {cont5.sum()}): X² = {fmt_br(x2_5, 2)} (4 g.l.), p = {p_br(p5)}, p MC = {p_br(p5_mc)}')

k_po, n_ac = int(ac.tecnica_curta.eq('Padrões objetivos').sum()), len(ac)
for p0, rot in [(1 / 6, '1/6'), (1 / 5, '1/5'), (0.5385, '53,85%')]:
    bt = stats.binomtest(k_po, n_ac, p0)
    ci = bt.proportion_ci(method='wilson')
    print(f'Padrões objetivos: {k_po}/{n_ac} = {pct_br(k_po / n_ac)} (Wilson {pct_br(ci.low)} a {pct_br(ci.high)}); '
          f'H0: p = {rot} → p = {p_br(bt.pvalue)}')
''')

code(r'''
fig, ax = plt.subplots(1, 2, figsize=(14, 5))
cont_tot = ac['tecnica_curta'].value_counts().reindex(TECNICAS)
ic = [stats.binomtest(int(c), n_ac).proportion_ci(method='wilson') for c in cont_tot]
barras_verticais(ax[0], TECNICAS, (cont_tot / n_ac).to_numpy(), cores='#5B7389', quebrar=11,
                 erro=([c.low for c in ic], [c.high for c in ic]), fmt=lambda v: pct_br(v, 0), ymax=0.62,
                 ylabel='AC realizadas (%)')
eixo_pct(ax[0])
ax[0].axhline(1 / 6, color=TINTA, ls='--', lw=1); ax[0].text(5.45, 1 / 6, ' 1/6', fontsize=8.5, va='bottom')
ax[0].axhline(1 / 5, color=TINTA_2, ls=':', lw=1); ax[0].text(5.45, 1 / 5, ' 1/5', fontsize=8.5, va='bottom')
ax[0].axhline(0.5385, color=DESTAQUE, ls='--', lw=1)
ax[0].text(-0.3, 0.548, '53,85% (resumo expandido)', color=TINTA, fontsize=8.5)
ax[0].set_title(f'(a) Técnicas nas {n_ac} AC realizadas (IC Wilson 95%)')
anotar_teste(ax[0], texto_teste('Aderência a 1/6 (Monte Carlo)', f'X² = {fmt_br(tab_tec.iloc[0]["X² (5 g.l.)"], 2)}',
                                tab_tec.iloc[0]['p exato (Monte Carlo)']), loc='upper right')
cont_g = pd.DataFrame({g: ac.loc[ac.grupo.eq(g), 'tecnica_curta'].value_counts().reindex(TECNICAS) for g in ['Presencial', 'Remota']})
rot_g = {g: f'{g} (n = {int(cont_g[g].sum())}; p Holm {"< 0,001" if tab_tec.loc[g, "p MC (Holm)"] < 0.001 else "= " + fmt_p(tab_tec.loc[g, "p MC (Holm)"])})'
         for g in cont_g}
barras_agrupadas(ax[1], cont_g.rename(columns=rot_g), cores={rot_g[g]: CORES_GRUPO[g] for g in rot_g}, quebrar=11,
                 ylabel='AC realizadas')
for g in cont_g:
    ax[1].axhline(cont_g[g].sum() / 6, color=CORES_GRUPO[g], ls='--', lw=1)
ax[1].set_ylim(0, cont_g.to_numpy().max() * 1.35)
ax[1].legend(loc='upper left', fontsize=8.5)
ax[1].set_title('(b) Por grupo (tracejado = esperado n/6)')
figura(fig, 'exp_tecnicas', 'Sorteio das técnicas: frequências compatíveis com 1/6, longe dos 53,85% do resumo expandido?',
       secao='2.5.3')
''')

interp('exp_tecnica')

md(r'''
### 2.5.4 (d) Sentenças datadas em fim de semana

**Pergunta.** Se os atos fossem praticados só em dias úteis, nenhuma sentença teria data de sábado ou domingo. A planilha tem desfechos datados em fins de semana (`sentenca_fim_semana`, anomalia A16). Duas referências:

- **"só dias úteis"** (p₀ = 0): basta um caso para refutar; não há teste a fazer, só a contagem;
- **"datas uniformes nos 7 dias"** (p₀ = 2/7 ≈ 28,6%): o que se esperaria se a data da sentença fosse indiferente ao dia da semana (por exemplo, assinatura eletrônica remota no PJe, que funciona todos os dias).

**Teste:** binomial exato bilateral, H0: p = 2/7; H1: p ≠ 2/7, no total dos desfechos e por tipo de desfecho (Holm, 4 tipos). Complemento: a distribuição dos desfechos pelos 7 dias (qui-quadrado de aderência à uniforme). A leitura jurídica: a data registrada é a da **assinatura eletrônica** do ato; sentenças em fim de semana indicam trabalho do magistrado fora do expediente (comum em gabinetes com acervo controlado), não erro de registro, mas a coluna deve ser conferida no PJe.
''')

code(r'''
desf = d2[d2['encerrado']].copy()
desf['dia_sem'] = desf['dt_sentenca'].dt.dayofweek
DIAS = ['seg', 'ter', 'qua', 'qui', 'sex', 'sáb', 'dom']
linhas = [linha_binomial('Fim de semana — todos os desfechos', desf.dia_sem.ge(5).sum(), len(desf), 2 / 7)]
for t in ['Homologação', 'Mérito', 'Sem mérito', 'Redistribuição']:
    s = desf[desf.tipo_desfecho.eq(t)]
    linhas.append(linha_binomial(f'Fim de semana — {t}', s.dia_sem.ge(5).sum(), len(s), 2 / 7))
tab_fds = pd.DataFrame(linhas)
tab_fds['p (Holm)'] = np.r_[tab_fds['p'].iloc[0], multipletests(tab_fds['p'].iloc[1:], method='holm')[1]]
tabela_binomial(tab_fds, 'exp_fimsemana', 'Desfechos datados em fim de semana contra a proporção uniforme de 2/7 (binomial exato)',
                '2.5.4', nota='Holm para os 4 tipos de desfecho; a primeira linha (todos) não entra na família.')
cont_dia = desf['dia_sem'].value_counts().reindex(range(7), fill_value=0)
x2_dia = stats.chisquare(cont_dia)
print(f'Desfechos por dia da semana: {dict(zip(DIAS, cont_dia.tolist()))}; '
      f'aderência à uniforme nos 7 dias: X² = {fmt_br(x2_dia.statistic, 1)} (6 g.l.), p = {p_br(x2_dia.pvalue)}')

fig, ax = plt.subplots(1, 2, figsize=(14, 4.6))
barras_verticais(ax[0], DIAS, cont_dia.to_numpy(), cores=['#5B7389'] * 5 + [DESTAQUE] * 2, ylabel='Desfechos')
ax[0].axhline(len(desf) / 7, color=TINTA, ls='--', lw=1, label='uniforme (n/7)')
ax[0].legend(loc='upper center')
ax[0].set_xlabel('Dia da semana da data do desfecho')
ax[0].set_title(f'(a) Desfechos por dia da semana (n = {len(desf)})')
anotar_teste(ax[0], texto_teste('Aderência à uniforme (7 dias)', f'X² = {fmt_br(x2_dia.statistic, 1)} (6 g.l.)',
                                x2_dia.pvalue), loc='upper right')
forest(ax[1], tab_fds, [(2 / 7, '2/7 (uniforme)', '--')], '(b) Proporção em fim de semana, por tipo',
       [TINTA, CORES_DESFECHO['Homologação'], CORES_DESFECHO['Mérito'], CORES_DESFECHO['Sem mérito'],
        CORES_DESFECHO['Redistribuição']])
ax[1].set_xlabel('Proporção em sábado ou domingo (IC 95%)')
figura(fig, 'exp_fimsemana', 'Há desfechos datados em fins de semana, mas bem abaixo dos 2/7 de uma data indiferente ao dia',
       secao='2.5.4', nota='a data registrada é a da assinatura eletrônica; p de Holm do binomial exato contra 2/7.')
''')

interp('exp_fimsemana')

# =====================================================================
md(r'''
## 2.6 Análise bivariada

Esta seção é **descritiva**: mostra como o tempo e as categóricas se associam, com medidas de tamanho de efeito, mas sem testes de hipótese (Parte III) nem modelos (Partes IV e V). Duas cautelas atravessam toda a seção:

1. **Toda comparação de tempos entre sentenciados é condicional.** Um grupo com mais processos ativos tem, entre os sentenciados, uma seleção mais "rápida". A comparação correta é a das curvas de sobrevivência (Parte IV).
2. **Variáveis pós-sorteio** (AC realizada, híbrida, técnica, acordo, tipo de desfecho) não são causas exógenas do tempo: elas acontecem durante o processo e, em parte, *definem* o seu fim.

### 2.6.1 Tempo até a sentença × fatores (sentenciados)

Boxplots verticais com o n de cada caixa e a mediana escrita ao lado ("Md"); cada ponto é um processo. A primeira figura traz os fatores do desenho (grupo, tipo de desfecho, mês) e a segunda, as variáveis pós-sorteio (acordo, híbrida, técnica). Para cada fator, a tabela traz n, mediana, IIQ e média, e a razão de correlação **η²** = SQ entre / SQ total (a fração da variância dos tempos dos sentenciados "explicada" pelo fator; tamanho de efeito descritivo, sem teste).
''')

code(r'''
def eta2(y, g):
    y = pd.Series(np.asarray(y, float)); g = pd.Series(np.asarray(g, object))
    ok = g.notna() & y.notna(); y, g = y[ok], g[ok]
    sqt = ((y - y.mean()) ** 2).sum()
    sqe = y.groupby(g).apply(lambda v: len(v) * (v.mean() - y.mean()) ** 2).sum()
    return sqe / sqt


sent['acordo_txt'] = sent['acordo'].map({True: 'Com acordo', False: 'Sem acordo'})
sent['hibrida_txt'] = sent['hibrida'].map({True: 'Híbrida', False: 'Só presencial'})
FATORES = {   # fator: (coluna, subconjunto, ordem dos níveis, cores, título)
    'Grupo': ('grupo', sent, ORDEM_GRUPO, CORES_GRUPO, 'Grupo (todas as sentenças)'),
    'Tipo de desfecho': ('tipo_desfecho', sent, ['Homologação', 'Mérito', 'Sem mérito'], CORES_DESFECHO, 'Tipo de desfecho'),
    'Mês de distribuição': ('mes_distribuicao', sent, MESES, {m: '#5B7389' for m in MESES}, 'Mês de distribuição (2026)'),
    'Acordo': ('acordo_txt', sent, ['Com acordo', 'Sem acordo'], {'Com acordo': CORES_DESFECHO['Homologação'], 'Sem acordo': CINZA},
               'Acordo (qualquer momento)'),
    'Híbrida': ('hibrida_txt', sent[sent.grupo.eq('Presencial') & sent.ac_realizada.fillna(False).astype(bool)],
                ['Só presencial', 'Híbrida'], {'Só presencial': CORES_GRUPO['Presencial'], 'Híbrida': '#5B7389'},
                'Híbrida (Presencial com AC realizada)'),
    'Técnica': ('tecnica_curta', sent[sent.ac_realizada.fillna(False).astype(bool)], TECNICAS,
                {t: '#5B7389' for t in TECNICAS}, 'Técnica (AC realizadas)'),
}
resumo_fatores, eta_fatores = [], {}
for bloco_fat, nomes_fat, titulo_fig, id_fig in [
        ('desenho', ['Grupo', 'Tipo de desfecho', 'Mês de distribuição'],
         'Tempo dos sentenciados por fator do desenho: o tipo de desfecho pesa mais que o grupo', 'exp_tempo_fatores_desenho'),
        ('pós-sorteio', ['Acordo', 'Híbrida', 'Técnica'],
         'Tempo dos sentenciados por variável pós-sorteio: diferenças pequenas e sem valor causal', 'exp_tempo_fatores_pos')]:
    fig, ax = plt.subplots(1, 3, figsize=(16, 5.2), gridspec_kw={'width_ratios': [3, 3, 5] if bloco_fat == 'desenho' else [2, 2, 5]})
    for a, nome in zip(ax, nomes_fat):
        col, df, niveis, cores, titulo = FATORES[nome]
        df_ = df.assign(_nivel=df[col].astype(object))
        rot_niveis = {t: ROTULO_DESFECHO[t] for t in niveis} if nome == 'Tipo de desfecho' else {}
        grupos = boxplot_grupos(a, df_, 'T', grupo='_nivel', ordem=niveis, cores=cores, ylabel=ROTULOS['tempo_sentenca'],
                                quebrar=10 if len(niveis) > 4 else 14, tam_ponto=5)
        if rot_niveis:
            a.set_xticks(range(len(niveis)), [f'{quebra(rot_niveis[t], 12)}\n(n = {len(gv)})' for t, gv in zip(niveis, grupos)])
        if len(niveis) > 4:
            a.tick_params(axis='x', labelsize=8)
            for txt in a.texts:
                txt.set_fontsize(7.5)
        eta_fatores[nome] = eta2(df['T'], df[col].astype(object))
        a.set_title(f'{titulo}\nη² = {fmt_br(eta_fatores[nome], 3)}')
        for nv, gv in zip(niveis, grupos):
            resumo_fatores.append({'Fator': nome, 'Nível': nv, 'n': len(gv), 'mediana': np.median(gv) if len(gv) else np.nan,
                                   'Q1': np.percentile(gv, 25) if len(gv) else np.nan, 'Q3': np.percentile(gv, 75) if len(gv) else np.nan,
                                   'média': gv.mean() if len(gv) else np.nan})
    for a in ax[1:]:
        a.set_ylabel('')
    figura(fig, id_fig, titulo_fig, secao='2.6.1',
           nota='só os 708 sentenciados (estatística condicional, enviesada para tempos curtos); η² = fração da variância '
                'dos tempos associada ao fator (descritivo, sem teste).')
tabela(pd.DataFrame(resumo_fatores).set_index(['Fator', 'Nível'])
       .rename(columns={'mediana': 'Mediana (dias)', 'Q1': 'Q1 (dias)', 'Q3': 'Q3 (dias)', 'média': 'Média (dias)'}),
       'exp_tempo_fatores', 'Tempo até a sentença por fator (sentenciados): n, mediana, quartis e média', secao='2.6.1', casas=1)
''')

md(r'''
**Tempo × tipo de desfecho dentro de cada grupo.** Como o tipo de desfecho é o principal determinante do tempo, a tabela cruza grupo e tipo: medianas e n de cada célula. Se as medianas por tipo forem parecidas entre os grupos, a diferença global entre grupos vem da **composição** dos desfechos (mais extinções rápidas aqui, mais mérito ali), e não de um rito "mais rápido" para o mesmo tipo de processo.
''')

code(r'''
tab_gt = sent.groupby(['grupo', 'tipo_desfecho'], observed=True)['T'].agg(['count', 'median', 'mean']).unstack('tipo_desfecho')
tab_gt = tab_gt.loc[:, (slice(None), ['Homologação', 'Mérito', 'Sem mérito'])]
tabela(tab_gt.rename(columns={'count': 'n', 'median': 'Mediana (dias)', 'mean': 'Média (dias)'}, level=0)
       .rename_axis(index='Grupo', columns=[None, None]),
       'exp_tempo_grupo_tipo', 'Tempo até a sentença por grupo e tipo de desfecho (sentenciados)', secao='2.6.1', casas=1)
''')

interp('exp_biv_tempo')

md(r'''
### 2.6.2 Proporção acumulada de sentenças por grupo no calendário

Para cada data do calendário, a fração de cada grupo já sentenciada (sentenças acumuladas ÷ tamanho do grupo) e, em tracejado, a fração já distribuída. É uma visão de **gestão** do acervo (quanto do trabalho de cada rito já foi concluído), não uma curva de sobrevivência: mistura processos de idades diferentes e depende do ritmo de entrada de cada grupo (por exemplo, a concentração de Remotas em julho).
''')

code(r'''
dias_cal = pd.date_range(DATA_INICIO, DATA_CORTE, freq='D')
fig, ax = plt.subplots(figsize=(11, 5.2))
for g in ORDEM_GRUPO:
    s = d2[d2.grupo.eq(g)]
    n_g = len(s)
    sent_ac = np.searchsorted(np.sort(s.loc[s.E.eq(1), 'dt_sentenca'].to_numpy()), dias_cal.to_numpy(), side='right') / n_g
    dist_ac = np.searchsorted(np.sort(s['dt_distribuicao'].to_numpy()), dias_cal.to_numpy(), side='right') / n_g
    ax.plot(dias_cal, sent_ac, color=CORES_GRUPO[g], lw=2, label=f'{g} (n = {n_g}): sentenciados')
    ax.plot(dias_cal, dist_ac, color=CORES_GRUPO[g], lw=1, ls='--', label=f'{g}: já distribuídos')
    ax.annotate(pct_br(sent_ac[-1]), (dias_cal[-1], sent_ac[-1]), xytext=(4, 0), textcoords='offset points',
                va='center', fontsize=8.5, color=TINTA)
ax.axvline(FIM_RECRUTAMENTO, color=TINTA_2, ls=':', lw=1)
ax.text(FIM_RECRUTAMENTO, 0.02, 'fim dos sorteios ', ha='right', fontsize=8.5, color=TINTA_2)
ax.set_ylabel('Fração do grupo (%)'); ax.set_xlabel('Calendário (2026)')
eixo_pct(ax); eixo_meses(ax); ax.set_ylim(0, 1.03)
handles, labels = ax.get_legend_handles_labels()
ordem_leg = [0, 2, 4, 1, 3, 5]
ax.legend([handles[i] for i in ordem_leg], [labels[i] for i in ordem_leg], loc='upper left', ncol=2)
figura(fig, 'exp_calendario', 'Sentenças acumuladas por grupo no calendário: o Controle termina mais processos até 07/10',
       secao='2.6.2', nota='linha cheia: fração do grupo já sentenciada; tracejado: fração já distribuída. À direita, '
                           'o percentual sentenciado em 07/10/2026. Visão de gestão, não curva de sobrevivência.')
''')

interp('exp_calendario')

md(r'''
### 2.6.3 Tabelas cruzadas e gráficos de mosaico

Para cada par, três versões: contagens, % na linha (distribuição do desfecho *dentro* de cada grupo: a leitura de interesse quando o grupo é a "causa") e % na coluna (de onde vêm os casos de cada categoria). O **mosaico** representa a tabela por áreas: a largura de cada coluna é proporcional ao tamanho do grupo e a altura de cada retângulo, à % na linha; se não houvesse associação, os retângulos se alinhariam em faixas horizontais. A significância e os resíduos ajustados são da Parte III.

- **grupo × tipo de desfecho** (938; inclui Ativo e Redistribuição como situações em 07/10);
- **grupo × acordo** (acordo em qualquer momento; os ativos ficam numa categoria própria, "indefinido");
- **grupo × mês de distribuição** (o calendário do sorteio);
- **técnica × acordo na AC** (352 AC realizadas).
''')

code(r'''
def cruzada(linha, coluna, titulo, id_):
    ct = pd.crosstab(linha, coluna)
    lin = 100 * ct.div(ct.sum(axis=1), axis=0)
    col = 100 * ct.div(ct.sum(axis=0), axis=1)
    saida = pd.concat({'n': ct, '% na linha': lin, '% na coluna': col}, axis=1)
    saida.index = saida.index.astype(object)
    saida.columns = pd.MultiIndex.from_tuples([(a, str(b)) for a, b in saida.columns])
    tabela(saida.rename_axis(index=ct.index.name), id_, titulo, secao='2.6.3', casas=1,
           nota='% na linha: distribuição da coluna dentro de cada categoria da linha; % na coluna: de onde vêm os casos de cada coluna.')
    return ct

d2['acordo_cat'] = d2['acordo'].map({True: 'Com acordo', False: 'Sem acordo'}).fillna('Indefinido (ativo)')
ac['acordo_ac_txt'] = ac['acordo_ac'].map({True: 'Acordo na AC', False: 'Sem acordo na AC'})
ct_desf = cruzada(d2['grupo'].rename('Grupo'), d2['tipo_desfecho'], 'Grupo × tipo de desfecho (938 processos)', 'exp_ct_desfecho')
ct_acordo = cruzada(d2['grupo'].rename('Grupo'), d2['acordo_cat'], 'Grupo × acordo em qualquer momento', 'exp_ct_acordo')
ct_mes = cruzada(d2['grupo'].rename('Grupo'), d2['mes_distribuicao'], 'Grupo × mês de distribuição', 'exp_ct_mes')
ct_tec = cruzada(ac['tecnica_curta'].cat.remove_unused_categories().rename('Técnica'), ac['acordo_ac_txt'],
                 'Técnica × acordo na AC (AC realizadas)', 'exp_ct_tecnica')
''')

code(r'''
def mosaico(ax, ct, cores_col, titulo, rotulos_col=None, quebrar=12):
    # Mosaico manual: largura = tamanho da linha; altura = % na linha
    tot = ct.to_numpy().sum()
    x0 = 0
    for lin in ct.index:
        larg = ct.loc[lin].sum() / tot
        y0 = 0
        for colu in ct.columns:
            h = ct.loc[lin, colu] / ct.loc[lin].sum()
            ax.add_patch(mpl.patches.Rectangle((x0, y0), larg * 0.98, h, facecolor=cores_col[colu], edgecolor='white', lw=1.2))
            if h > 0.05 and larg > 0.06:
                ax.text(x0 + larg * 0.49, y0 + h / 2, fmt_br(ct.loc[lin, colu], 0), ha='center', va='center', fontsize=8,
                        color=_cor_texto(cores_col[colu]))
            y0 += h
        ax.text(x0 + larg * 0.49, -0.03, f'{quebra(str(lin), quebrar)}\n(n = {int(ct.loc[lin].sum())})', ha='center',
                va='top', fontsize=8.5)
        x0 += larg
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_xticks([]); ax.grid(False)
    eixo_pct(ax)
    ax.set_ylabel('% na linha')
    ax.legend(handles=[mpl.patches.Patch(color=cores_col[c], label=(rotulos_col or {}).get(c, str(c))) for c in ct.columns][::-1],
              loc='center left', bbox_to_anchor=(1.0, 0.5), fontsize=8.5)
    ax.set_title(titulo)

cores_mes = dict(zip(MESES, [mpl.colors.to_hex(SEQ(v)) for v in np.linspace(0.15, 1, len(MESES))]))
cores_acordo = {'Com acordo': CORES_DESFECHO['Homologação'], 'Sem acordo': '#5B7389', 'Indefinido (ativo)': CORES_DESFECHO['Ativo']}
fig, ax = plt.subplots(1, 2, figsize=(14, 5.2))
mosaico(ax[0], ct_desf, CORES_DESFECHO, '(a) Grupo × tipo de desfecho', ROTULO_DESFECHO)
mosaico(ax[1], ct_acordo, cores_acordo, '(b) Grupo × acordo (qualquer momento)')
figura(fig, 'exp_mosaico_desfecho', 'Mosaicos: o Controle tem mais sentenças de mérito; os acordos se distribuem de forma parecida',
       secao='2.6.3', nota='largura = tamanho do grupo; altura = % na linha; números = contagens. A significância e os '
                           'resíduos ajustados estão na Parte III.')
fig, ax = plt.subplots(1, 2, figsize=(14, 5.4))
mosaico(ax[0], ct_mes, cores_mes, '(a) Grupo × mês de distribuição')
mosaico(ax[1], ct_tec, {'Acordo na AC': CORES_DESFECHO['Homologação'], 'Sem acordo na AC': '#5B7389'},
        f'(b) Técnica × acordo na AC ({int(ct_tec.to_numpy().sum())} AC)', quebrar=9)
for t in ax[1].texts:
    if '(n =' in t.get_text():
        t.set_fontsize(7.5)
figura(fig, 'exp_mosaico_mes_tecnica', 'Mosaicos: a composição dos grupos muda com o mês; o acordo na AC é raro em todas as técnicas',
       secao='2.6.3', nota='meses em escala sequencial (mais escuro = mais tardio).')
''')

interp('exp_crosstabs')

md(r'''
### 2.6.4 Matriz de associação: a substituta correta da matriz de correlações do professor

**O problema da matriz original (questão 2.7; E6, E16).** O notebook do professor calculou uma matriz de correlação de Spearman entre as colunas `DURAÇÃO-SENT2`, `DURAÇÃO-SORT`, `DURAÇÃO-PROC` e `DURAÇÃO-TECN`. As três primeiras são **a mesma fórmula** repetida, e a quarta é a mesma duração apagada onde não houve técnica: a matriz dá r = 1 em todos os pares por construção (tautologia), não por achado empírico. Além disso, as demais variáveis do banco são **nominais** (grupo, desfecho, técnica, acordo, híbrida), e o coeficiente de Pearson ou Spearman sobre códigos numéricos de categorias não tem sentido. A célula abaixo reproduz o resultado tautológico a partir dos dados brutos.

**A matriz correta** usa, para cada par, a medida adequada aos níveis de mensuração:

| Par | Medida | Faixa |
|---|---|---|
| nominal × nominal | **V de Cramér com correção de viés** (Bergsma, 2013): corrige a inflação do V em tabelas grandes com n moderado | 0 a 1 |
| tempo (sentenciados) × nominal | **razão de correlação η** = √(SQ entre / SQ total) | 0 a 1 |
| ordinal × tempo | **Spearman ρ** e **Kendall τ_b** (seção 2.6.5) | −1 a 1 |

Cada par usa os casos com as duas variáveis definidas (exclusão aos pares). **Associações estruturais** (por exemplo, grupo × AC realizada: o Controle nunca tem AC) aparecem fortes por definição, e não são achados.
''')

code(r'''
if 'dados_brutos' in globals():
    _brutos = dados_brutos
else:
    _brutos = pd.read_excel(BRUTO, sheet_name='Processos', header=1, engine='openpyxl')
cols_dur = ['DURAÇÃO-SENT2', 'DURAÇÃO-SORT', 'DURAÇÃO-PROC', 'DURAÇÃO-TECN']
matriz_prof = _brutos[cols_dur].apply(pd.to_numeric, errors='coerce').corr(method='spearman')
tabela(matriz_prof.rename_axis('Coluna'), 'exp_matriz_professor',
       'Matriz do notebook do professor (Spearman entre as quatro colunas de duração): tautológica', secao='2.6.4', casas=4)
print('Linhas em que as colunas coincidem com DURAÇÃO-PROC:',
      {c: int((_brutos[c] == _brutos['DURAÇÃO-PROC']).sum()) for c in cols_dur}, '| não nulas:',
      {c: int(_brutos[c].notna().sum()) for c in cols_dur})
''')

code(r'''
def cramer_v_corrigido(x, y):
    ok = x.notna() & y.notna()
    ct = pd.crosstab(x[ok].astype(str), y[ok].astype(str))
    if ct.shape[0] < 2 or ct.shape[1] < 2:
        return np.nan
    n = ct.to_numpy().sum()
    chi2 = stats.chi2_contingency(ct, correction=False)[0]
    phi2 = chi2 / n
    r, c = ct.shape
    phi2c = max(0, phi2 - (c - 1) * (r - 1) / (n - 1))
    rc, cc = r - (r - 1) ** 2 / (n - 1), c - (c - 1) ** 2 / (n - 1)
    return np.sqrt(phi2c / min(rc - 1, cc - 1)) if min(rc, cc) > 1 else np.nan

VARS_ASSOC = {'grupo': 'Grupo', 'mes_distribuicao': 'Mês', 'ciclo': 'Ciclo', 'dia_semana_distribuicao': 'Dia sem. distrib.',
              'tipo_desfecho': 'Tipo de desfecho', 'ac_realizada': 'AC realizada', 'hibrida': 'Híbrida',
              'tecnica_curta': 'Técnica', 'acordo_ac': 'Acordo na AC', 'acordo_fora': 'Acordo fora',
              'acordo': 'Acordo', 'origem_externa': 'Origem externa', 'sentenca_fim_semana': 'Desfecho fim sem.'}
nomes = list(VARS_ASSOC.values())
mat_v = pd.DataFrame(np.nan, index=nomes + ['Tempo (η, sentenças)'], columns=nomes + ['Tempo (η, sentenças)'])
for i, (vi, ni) in enumerate(VARS_ASSOC.items()):
    for vj, nj in list(VARS_ASSOC.items())[i:]:
        val = 1.0 if vi == vj else cramer_v_corrigido(d2[vi].astype(object), d2[vj].astype(object))
        mat_v.loc[ni, nj] = mat_v.loc[nj, ni] = val
    eta = np.sqrt(eta2(sent['T'], sent[vi].astype(object))) if sent[vi].astype(object).nunique() > 1 else np.nan
    mat_v.loc[ni, 'Tempo (η, sentenças)'] = mat_v.loc['Tempo (η, sentenças)', ni] = eta
mat_v.loc['Tempo (η, sentenças)', 'Tempo (η, sentenças)'] = 1.0

fig, ax = plt.subplots(figsize=(11.5, 9.5))
mascara = np.triu(np.ones_like(mat_v, dtype=bool), k=1)
anot = mat_v.astype(float).map(lambda v: '' if pd.isna(v) else fmt_br(v, 2))
rot_mat = [quebra(c, 14) for c in mat_v.index]
sns.heatmap(mat_v.astype(float), mask=mascara, annot=anot.to_numpy(), fmt='', cmap=SEQ, vmin=0, vmax=1, ax=ax,
            cbar_kws={'label': 'V de Cramér corrigido (última linha: η)', 'shrink': 0.8}, annot_kws={'fontsize': 8},
            linewidths=0.6, linecolor='white', xticklabels=rot_mat, yticklabels=rot_mat)
ax.tick_params(axis='x', labelsize=8.5, rotation=90); ax.tick_params(axis='y', labelsize=8.5, rotation=0)
ax.set_title('Triângulo inferior; células cinza-escuras = associação forte (muitas são estruturais, por definição)',
             fontsize=9.5, fontweight='normal', color=TINTA_2)
figura(fig, 'exp_matriz_associacao', 'Matriz de associação com a medida adequada a cada par de variáveis', secao='2.6.4',
       nota='nominal × nominal: V de Cramér com correção de viés (Bergsma, 2013); tempo dos sentenciados × nominal: η. '
            'Exclusão aos pares.')
pares = (mat_v.where(~mascara & ~np.eye(len(mat_v), dtype=bool)).stack().sort_values(ascending=False))
tabela(pares.head(15).rename('Associação (V ou η)').rename_axis(['Variável 1', 'Variável 2']).reset_index(),
       'exp_pares_associacao', 'As 15 associações mais fortes entre pares de variáveis', secao='2.6.4', casas=3)
''')

interp('exp_assoc_matriz')

md(r'''
### 2.6.5 Ordem de chegada × tempo (questão 2.7)

**É possível investigar?** Sim: a ordem de chegada é uma variável **ordinal** (1 = primeiro distribuído), equivalente à data de distribuição, e o tempo é quantitativo; o par admite **Spearman ρ** e **Kendall τ_b** (robustos a não normalidade e a empates), nunca Pearson sobre os códigos. **Mas a censura cria uma correlação negativa espúria**: os processos que chegaram tarde têm seguimento curto (65 dias para os de agosto), então só podem aparecer como sentenciados se forem rápidos, e, se ativos, o seu tempo observado é pequeno. O tempo observado é limitado por cima pela "diagonal" `followup` = 07/10/2026 − distribuição.

Três versões, para separar o artefato do efeito:

1. **Todos os tempos observados** (mistura sentenças e censuras): inválida, mostrada para expor o artefato;
2. **Só os sentenciados**: condicional, enviesada pelo mesmo mecanismo;
3. **Janela comum de 65 dias**, observada sem censura para os 938, porque **todos** os processos têm pelo menos 65 dias de seguimento. A medida principal é o **indicador "sentenciado em até 65 dias"** (1 = sim; 0 = não), que não confunde a redistribuição com a sentença. O tempo truncado, min(tempo, 65), é mostrado como complemento, com duas ressalvas: (i) o redistribuído antes de 65 dias conta pelo seu tempo, como se fosse "rápido"; (ii) a variável tem muitos empates em 65, todos os processos ainda sem sentença naquele dia.

Na primeira figura, a curva LOWESS (regressão local, fração de 0,3) mostra a tendência e a cor distingue sentenças de censurados; a linha em destaque é o teto imposto pelo seguimento. Na segunda, a proporção de processos sentenciados em até 65 dias aparece por mês de distribuição e grupo, com o ρ de Spearman do indicador de cada grupo na legenda (ρ negativo = quem chegou depois foi sentenciado com menos frequência na janela). O teste formal (Cox com a ordem ou o mês como covariável) fica para as Partes IV e V.
''')

code(r'''
ordem = d2['ordem_chegada'].astype(float)
d2['T65'] = np.minimum(d2['T'], 65)
versoes = {'Todos os tempos observados (inválido)': (ordem, d2['T']),
           'Só sentenciados (condicional)': (sent['ordem_chegada'].astype(float), sent['T']),
           'min(tempo, 65) — todos, janela comum': (ordem, d2['T65']),
           'Seguimento máximo (followup) — referência': (ordem, d2['followup'].astype(float))}
linhas = []
for nome, (xo, yt) in versoes.items():
    rho = stats.spearmanr(xo, yt); tau = stats.kendalltau(xo, yt)
    linhas.append({'Versão': nome, 'n': len(xo), 'Spearman ρ': rho.statistic, 'p (ρ)': rho.pvalue,
                   'Kendall τ_b': tau.statistic, 'p (τ)': tau.pvalue})
for g in ORDEM_GRUPO:
    m = d2.grupo.eq(g)
    rho = stats.spearmanr(ordem[m], d2.loc[m, 'T65']); tau = stats.kendalltau(ordem[m], d2.loc[m, 'T65'])
    linhas.append({'Versão': f'min(tempo, 65) — {g}', 'n': int(m.sum()), 'Spearman ρ': rho.statistic,
                   'p (ρ)': rho.pvalue, 'Kendall τ_b': tau.statistic, 'p (τ)': tau.pvalue})
# Medida principal: indicador de sentença em até 65 dias (0/1)
d2['sent65'] = d2['T'].le(65) & d2['E'].eq(1)
for rot_, m in [('todos', pd.Series(True, index=d2.index))] + [(g, d2.grupo.eq(g)) for g in ORDEM_GRUPO]:
    y_ = d2.loc[m, 'sent65'].astype(int)
    rho = stats.spearmanr(ordem[m], y_); tau = stats.kendalltau(ordem[m], y_)
    linhas.append({'Versão': f'Sentenciado em até 65 d (0/1) — {rot_}', 'n': int(m.sum()), 'Spearman ρ': rho.statistic,
                   'p (ρ)': rho.pvalue, 'Kendall τ_b': tau.statistic, 'p (τ)': tau.pvalue})
tab_ordem = pd.DataFrame(linhas).set_index('Versão')
tabela(tab_ordem, 'exp_ordem_tempo', 'Ordem de chegada × tempo: correlações de postos em várias versões do tempo', secao='2.6.5',
       casas=3, nota='só as versões na janela de 65 dias são observadas sem censura para todos; as demais carregam o artefato '
                     'da censura. Medida principal: o indicador de sentença em até 65 dias (ρ negativo = quem chegou depois '
                     'foi sentenciado com menos frequência).')
print(f'Empates em min(tempo, 65): {pct_br(d2["T65"].eq(65).mean())} dos 938 processos valem exatamente 65 dias.')

# Proporção sentenciada em até 65 dias por ciclo e grupo (IC de Wilson)
linhas65 = []
for g in ['Todos'] + ORDEM_GRUPO:
    for ciclo_ in sorted(d2['ciclo'].astype(str).unique()):
        m = d2['ciclo'].astype(str).eq(ciclo_) & (d2['grupo'].notna() if g == 'Todos' else d2['grupo'].eq(g))
        k_, n_ = int(d2.loc[m, 'sent65'].sum()), int(m.sum())
        ci_ = stats.binomtest(k_, n_).proportion_ci(method='wilson')
        linhas65.append({'Grupo': g, 'Ciclo': ciclo_, 'k': k_, 'n': n_, 'Sentenciados em até 65 d': k_ / n_,
                         'IC95% Wilson': fmt_ic((ci_.low, ci_.high))})
tab65_ciclo = pd.DataFrame(linhas65).set_index(['Grupo', 'Ciclo'])
tabela(tab65_ciclo, 'exp_janela65_ciclo', 'Processos sentenciados em até 65 dias da distribuição, por grupo e ciclo',
       secao='2.6.5', formatos={'Sentenciados em até 65 d': 'pct', 'k': 'int', 'n': 'int'},
       nota='janela comum observada sem censura para os 938 processos.')

fig, ax = plt.subplots(figsize=(11, 6))
for s, mk in [('Sentença', 'o'), ('Redistribuição', 'D'), ('Ativo (censurado)', '>')]:
    m = d2.status.eq(s)
    ax.scatter(ordem[m], d2.loc[m, 'T'], s=10, color=CORES_STATUS[s], marker=mk, alpha=0.7,
               edgecolors=TINTA_2 if s == 'Ativo (censurado)' else 'none', linewidths=0.3, label=f'{s} (n = {int(m.sum())})')
ax.plot(ordem.sort_values(), d2.loc[ordem.sort_values().index, 'followup'], color=DESTAQUE, lw=1.2,
        label='teto: seguimento máximo (07/10 − distribuição)')
for nome, (xo, yt), cor in [('LOWESS de todos os observados', versoes['Todos os tempos observados (inválido)'], '#5B7389'),
                            ('LOWESS só dos sentenciados', versoes['Só sentenciados (condicional)'], TINTA)]:
    lw_ = lowess(yt.to_numpy(float), xo.to_numpy(float), frac=0.3)
    ax.plot(lw_[:, 0], lw_[:, 1], color=cor, lw=2.5, label=nome)
ax.set_xlabel(ROTULOS['ordem_chegada']); ax.set_ylabel('Tempo observado (dias)')
ax.grid(axis='both', visible=True)
legenda_abaixo(ax, ncol=3, dy=-0.12)
anotar_teste(ax, texto_teste('Spearman (só sentenciados)', f'ρ = {fmt_br(tab_ordem.iloc[1]["Spearman ρ"], 3)}',
                             tab_ordem.iloc[1]['p (ρ)']), loc='upper right')
figura(fig, 'exp_ordem_dispersao', 'Ordem de chegada × tempo: a correlação negativa é um artefato do teto de seguimento',
       secao='2.6.5', nota='os processos de chegada tardia só podem ter tempos curtos, porque o corte os interrompe.')

prop65 = d2.groupby(['mes_distribuicao', 'grupo'], observed=True)['sent65'].mean().unstack().reindex(columns=ORDEM_GRUPO)
prop65 = prop65.drop(index='ago')   # 6 processos
fig, ax = plt.subplots(figsize=(11, 5))
rot65 = {g: f'{g} (ρ = {fmt_br(tab_ordem.loc[f"Sentenciado em até 65 d (0/1) — {g}", "Spearman ρ"], 3)}; '
            f'{p_igual(tab_ordem.loc[f"Sentenciado em até 65 d (0/1) — {g}", "p (ρ)"])})' for g in ORDEM_GRUPO}
barras_agrupadas(ax, prop65.rename(columns=rot65), cores={rot65[g]: CORES_GRUPO[g] for g in ORDEM_GRUPO},
                 xlabel='Mês de distribuição (agosto omitido: 6 processos)', ylabel='Sentenciados em até 65 dias (%)')
eixo_pct(ax); ax.set_ylim(0, max(0.7, prop65.to_numpy().max() * 1.3))
ax.legend(loc='upper left', ncol=1, fontsize=8.5)
LIN65 = 'Sentenciado em até 65 d (0/1) — todos'
anotar_teste(ax, texto_teste('Spearman, ordem × sentença em até 65 d (938)', f'ρ = {fmt_br(tab_ordem.loc[LIN65, "Spearman ρ"], 3)}',
                             tab_ordem.loc[LIN65, 'p (ρ)']), loc='upper right')
figura(fig, 'exp_janela65', 'Janela comum de 65 dias: a fração sentenciada cai ao longo do calendário nos grupos com AC',
       secao='2.6.5', nota='todo processo tem pelo menos 65 dias de seguimento: a sentença em até 65 dias é observada sem censura '
                           'para os 938. ρ = Spearman entre a ordem de chegada e o indicador (negativo = queda).')
''')

interp('exp_ordem_tempo')

# =====================================================================
md(r'''
## 2.7 Síntese exploratória

A tabela reúne os achados da Parte II, a medida que os sustenta e o encaminhamento para as partes seguintes.
''')

code(r'''
melhor_aic = tab_ajuste['AIC'].idxmin()
melhor_param = tab_ajuste.drop(index='Exponencial por partes')['AIC'].idxmin()
sintese = pd.DataFrame([
    ('Variável-alvo', f'{len(sent)} sentenças, {(d2.evento_cr == 0).sum()} ativos e {(d2.evento_cr == 2).sum()} redistribuições; seguimento de 65 a 279 dias',
     'Tempo censurado: análise de sobrevivência (Parte IV)'),
    ('Médias da pesquisa', f'78,46 e 75,2 reproduzidas como médias "mistas" (sentenças + ativos) com corte em 07/10 '
     f'({fmt_br(tab_medias.loc["Todos", "Mista, 944 linhas, corte 07/10 (planilha: 78,46)"], 2)}) e 23/09 '
     f'({fmt_br(tab_medias.loc["Todos", "Mista, 944 linhas, corte 23/09 (resumo: 75,2)"], 2)}); só sentenciados = {fmt_br(sent["T"].mean(), 2)}; '
     f'mediana do KM = {fmt_br(kmf_total.median_survival_time_)}',
     'Nenhuma estima a duração; substituir por mediana do KM e RMST (Parte IV)'),
    ('Distribuição das sentenças', f'mediana {fmt_br(tab_desc.loc["mediana", "Sentenças (condicional)"])} d '
     f'(IC95% {fmt_br(tab_desc.loc["IC95% mediana (inf.)", "Sentenças (condicional)"])}–{fmt_br(tab_desc.loc["IC95% mediana (sup.)", "Sentenças (condicional)"])}); '
     f'assimetria {fmt_br(tab_desc.loc["assimetria", "Sentenças (condicional)"], 2)}; curtose {fmt_br(tab_desc.loc["curtose (excesso)", "Sentenças (condicional)"], 2)}',
     'Bimodal (extinções precoces × mérito)'),
    ('Normalidade', f'{(tab_norm["Decisão (5%)"] == "rejeita H0").sum()} de {len(tab_norm)} testes rejeitam H0 (Holm)',
     'Testes não paramétricos na Parte III'),
    ('Ajuste com censura', f'menor AIC: {melhor_aic}; melhor paramétrico: {melhor_param}',
     'Risco não monótono (pico inicial, vale, subida): nenhum AFT padrão ajusta bem; preferir Cox, KM e RMST'),
    ('Sorteio dos grupos', f'313/314/311: P(divisão tão equilibrada) = {fmt_br(tab_equilibrio.iloc[1]["P(divisão tão equilibrada) exata (esq.)"], 4)}',
     'Aleatorização com totais equilibrados (não blocos pequenos): documentar; corridas na Parte III'),
    ('Índice de conciliação', f'{tab_bin.iloc[0]["k"]}/{tab_bin.iloc[0]["n"]} = {pct_br(tab_bin.iloc[0]["p̂"])} das sentenças '
     f'({p_txt(tab_bin.iloc[0]["p"])} contra 13,3%)', 'Comparação entre grupos na Parte III; riscos competitivos na Parte IV'),
    ('Sem mérito', 'Controle × Presencial × Remota: ' + '; '.join(
        f'{pct_br(tab_sm_bases.loc[tab_sm_bases.Base.eq(b_) & tab_sm_bases.Grupo.eq("Controle"), "p̂"].iloc[0])} × '
        f'{pct_br(tab_sm_bases.loc[tab_sm_bases.Base.eq(b_) & tab_sm_bases.Grupo.eq("Presencial"), "p̂"].iloc[0])} × '
        f'{pct_br(tab_sm_bases.loc[tab_sm_bases.Base.eq(b_) & tab_sm_bases.Grupo.eq("Remota"), "p̂"].iloc[0])} dos {b_.lower()}'
        for b_ in ['Sentenciados', 'Distribuídos']) +
     f'; após 30 dias: {" × ".join(str(int(v)) for v in tab_faixa["após 30 dias"])}',
     'Excesso nas extinções tardias (> 30 dias, fase da audiência); as duas bases são limites: CIF na Parte IV, teste na Parte III'),
    ('Acordo na AC', f'{int(ac.acordo_ac.sum())}/{len(ac)} = {pct_br(ac.acordo_ac.mean())} das AC realizadas',
     'Logit restrito às AC na Parte V'),
    ('Técnicas', f'Padrões objetivos = {pct_br(k_po / n_ac)} (não 53,85%); aderência a 1/6: p = {p_br(tab_tec.iloc[0]["p exato (Monte Carlo)"])}',
     'Sorteio das técnicas compatível com uniforme'),
    ('Fim de semana', f'{pct_br(tab_fds.iloc[0]["p̂"])} dos desfechos ({p_txt(tab_fds.iloc[0]["p"])} contra 2/7)',
     'Data = assinatura eletrônica; conferir no PJe'),
    ('Ordem × tempo', f'ρ sentenciados = {fmt_br(tab_ordem.iloc[1]["Spearman ρ"], 3)}; sentença em até 65 d: '
     f'{pct_br(tab65_ciclo.loc[("Todos", "1º ciclo"), "Sentenciados em até 65 d"])} (1º ciclo) × '
     f'{pct_br(tab65_ciclo.loc[("Todos", "2º ciclo"), "Sentenciados em até 65 d"])} (2º ciclo), '
     f'ρ = {fmt_br(tab_ordem.loc[LIN65, "Spearman ρ"], 3)}',
     'Queda só nos grupos com AC; Cox com mês/ordem (Partes IV e V)'),
], columns=['Tema', 'Resultado', 'Encaminhamento'])
tabela(sintese, 'exp_sintese', 'Síntese da Parte II: achados, medidas e encaminhamentos', secao='2.7')
''')

interp('exp_sintese')
