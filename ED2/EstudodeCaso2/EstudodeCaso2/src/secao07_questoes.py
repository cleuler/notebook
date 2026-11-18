# Parte VII — Respostas às questões 2.2 a 2.12 do roteiro do professor (seções 7.1 a 7.11).
# Executado por build_rafaelcc_ed2.py (exec): usa md(), code() e interp().
# Não refaz as análises das Partes I–VI: remete a elas e só faz pequenos cálculos de apoio.

md(r'''
# PARTE VII — RESPOSTAS ÀS QUESTÕES DO PROFESSOR (2.2 A 2.12)

Esta parte responde, uma a uma, às questões 2.2 a 2.12 do roteiro `estudo_de_caso_n_2.md`. Cada resposta argumenta com as evidências das Partes I a VI (remetidas pela numeração das seções) e, quando útil, traz um quadro ou uma figura. Os poucos cálculos feitos aqui (fluxo dos processos, equilíbrio das variáveis basais, medianas ingênuas × Kaplan-Meier) são **de apoio**: não refazem as análises anteriores.

| Questão | Tema | Seção | Evidência principal |
|---|---|---|---|
| 2.2 | EO ou ECA? | 7.1 | 1.10, 1.12, 2.5.1, 3.5 |
| 2.3 | Amostras independentes de uma mesma população? | 7.2 | 2.5.1, 3.5.1, 3.5.3 |
| 2.4 | "Híbrida" e "Decisão" | 7.3 | 1.11, 1.12, 3.2.4, 3.3.4, 4.7, 4.9 |
| 2.5 | Populações e cruzamento com os 14 JECs (DataJud) | 7.4 | 1.9; Parte VI (6.1, 6.3, 6.6) |
| 2.6 | Tratamento dos dados brutos | 7.5 | Parte I; 6.3 |
| 2.7 | Matriz de correlações; ordem de chegada × duração | 7.6 | 2.6.4, 2.6.5, 3.5.2, 4.5, 5.1 |
| 2.8 | Variáveis de confundimento | 7.7 | 3.5.3, 4.3.4, 4.9, 6.3.3, 6.6.3 |
| 2.9 | Outras variáveis em escala intervalar | 7.8 | 2.6.4; Parte V (limitação) |
| 2.10 | Validade interna e externa; generalização | 7.9 | Partes III a V; 6.4, 6.6 |
| 2.11 | Adequação dos TSHN do professor | 7.10 | 3.4, 3.6, 3.7, Parte IV |
| 2.12 | Avaliação geral e sugestões | 7.11 | todas; Parte VIII |
''')

code(r'''
if 'dados' not in globals():
    dados = pd.read_pickle(PROC / 'ed2_tidy.pkl')
from matplotlib.patches import FancyBboxPatch
from scipy.stats import chi2_contingency

q6 = dados.copy()
q6['grupo'] = pd.Categorical(q6['grupo'].astype(str), categories=ORDEM_GRUPO)
q6['desfecho'] = q6['tipo_desfecho'].astype(str)
q6['acr'] = q6['ac_realizada'].astype(object)
n_grupo = q6['grupo'].value_counts().reindex(ORDEM_GRUPO)
todas_q6 = pd.read_pickle(PROC / 'ed2_todas_linhas.pkl')
RNG_Q6 = np.random.default_rng(SEMENTE)


def q6_csv(nome, pasta='tab'):
    """Lê um CSV exportado pelas Partes II–V (';' e vírgula decimal); None se ainda não existir."""
    caminho = RAIZ / pasta / nome
    if not caminho.exists():
        print(f'Aviso: {pasta}/{nome} não encontrado (é gerado pelas Partes II a V).')
        return None
    return pd.read_csv(caminho, sep=';', decimal=',', encoding='utf-8-sig')


def q6_chi2_perm(tab, n_perm=20000, rng=RNG_Q6):
    """χ² de independência com valor-p por permutação (tabelas com esperadas pequenas)."""
    tab = np.asarray(tab)
    chi2_obs, p_ass, gl, esp = chi2_contingency(tab, correction=False)
    linhas = np.repeat(np.arange(tab.shape[0]), tab.sum(axis=1))
    colunas = np.repeat(np.arange(tab.shape[1]), tab.sum(axis=0))
    maiores = 0
    for _ in range(n_perm):
        perm = rng.permutation(colunas)
        t = np.zeros_like(tab)
        np.add.at(t, (linhas, perm), 1)
        maiores += chi2_contingency(t, correction=False)[0] >= chi2_obs - 1e-12
    v = np.sqrt(chi2_obs / (tab.sum() * (min(tab.shape) - 1)))
    return chi2_obs, gl, p_ass, (maiores + 1) / (n_perm + 1), esp.min(), v

print(f'Base primária: {len(q6)} processos; linhas brutas: {len(todas_q6)}; '
      f'grupos: ' + ', '.join(f'{g} {n_grupo[g]}' for g in ORDEM_GRUPO))
''')

# =====================================================================================
md(r'''
## 7.1 Questão 2.2 — Estudo observacional (EO) ou ensaio controlado aleatorizado (ECA)?


**A diferença.** O que separa os dois desenhos é **quem atribui a exposição, e como**.

- No **estudo observacional**, o pesquisador apenas registra uma exposição que não controla. Os grupos podem diferir em fatores que também afetam o desfecho (**confundimento**), e a inferência causal depende de ajustar esses fatores, sempre com o risco dos confundidores não medidos.
- No **ensaio controlado aleatorizado**, o pesquisador **impõe** o tratamento **por sorteio**, com grupo de comparação **contemporâneo**. O sorteio torna os grupos comparáveis **em expectativa** em todos os fatores anteriores à alocação, medidos ou não (MOORE; NOTZ; FLIGNER, 2023, cap. 9).

**O caso.** Quanto ao rito, o experimento do 4º JEC é um **ECA**, e não um EO: cada processo novo foi alocado pelo pesquisador, por sorteio individual, a um de três ritos, e os três grupos correram em paralelo no mesmo período e na mesma unidade. Com mais precisão, é um **ECA pragmático, de centro único, aberto (sem cegamento), com aleatorização individual 1:1:1**.

**A qualidade da aleatorização, porém, não é verificável.** Duas falhas de protocolo pesam aqui:

- **sequência não documentada.** Os totais finais (313/314/311) são equilibrados demais para um sorteio simples (P ≈ 1%; seção 2.5.1). O desequilíbrio acumulado chegou a 31 processos em junho e foi compensado sobretudo em julho (7.2). Isso indica sorteio a partir de totais preestabelecidos ou compensação deliberada no fim do período, e nenhum dos dois foi descrito;
- **alocação não ocultada.** O sorteio era feito no gabinete do juiz-pesquisador (Chefe de Gabinete, sorteio.com.br), processo a processo, na ordem de chegada. Seguir a ordem de chegada impede que se escolha **quais** processos entram, porque todos entram. Não impede, em tese, que um resultado conhecido seja refeito ou ajustado, e, se houve compensação, a alocação de julho foi parcialmente previsível.

Os testes possíveis não acusam irregularidade: corridas na ordem de chegada (3.5.1) e equilíbrio das variáveis basais (7.2). Eles não demonstram, porém, a integridade do sorteio, que é **plausível, mas não verificável**. O desenho continua sendo de ECA; a qualidade da aleatorização é uma limitação a declarar.

Há ainda três ressalvas:

1. **dentro do ECA há componentes observacionais**: a realização da AC, a audiência "híbrida", o acordo e a ausência das partes ocorrem **depois** do sorteio e dependem de escolhas das partes; comparações por essas variáveis (por exemplo, "processos com AC realizada × sem AC") são observacionais (seções 3.2.3 e 4.8);
2. **a unidade judicial não foi sorteada**: o 4º JEC entrou por conveniência (os outros 13 juízes não aderiram); para a população dos 14 JECs, o estudo é um **estudo de caso único** (um conglomerado), e não um ensaio por conglomerados;
3. **o próprio projeto se classifica de forma incoerente**: o resumo expandido fala em "experimento controlado aleatorizado", enquanto o projeto depositado adota a diretriz TREND, própria de desenhos **não aleatorizados** ("quase experimental"), e fala até em "estudo observacional" (`docs/r1_documentos.md`, §5). Pelo critério acima, prevalece a classificação de ECA, e a diretriz de relato adequada é a CONSORT (SCHULZ; ALTMAN; MOHER, 2010).

O quadro a seguir resume a comparação; o diagrama de fluxo, no formato CONSORT, mostra o percurso dos 944 registros da planilha até os desfechos observados em 07/10/2026.
''')

code(r'''
quadro_eo = pd.DataFrame([
    ['Quem atribui a exposição', 'a própria unidade, as circunstâncias ou terceiros; o pesquisador só observa',
     'o pesquisador, por sorteio', 'o juiz-pesquisador, por sorteio individual de cada processo novo (Chefe de Gabinete, sorteio.com.br)'],
    ['Grupo de comparação', 'expostos × não expostos, às vezes históricos', 'contemporâneo, formado pelo mesmo sorteio',
     'contemporâneo: rito atual (Controle), sorteado junto com os dois braços de AC'],
    ['Comparabilidade dos grupos', 'não garantida; depende de ajuste por confundidores medidos',
     'garantida em expectativa para todos os fatores anteriores ao sorteio', 'grupos de 313/314/311; mês e dia da semana compatíveis com o acaso (7.2)'],
    ['Geração e ocultação da sequência', '—', 'sequência gerada e guardada por terceiro; alocação revelada só após a inclusão',
     'sorteio no gabinete do juiz-pesquisador; mecanismo restrito não documentado (P ≈ 1%); integridade não verificável'],
    ['Inferência causal', 'só sob hipóteses fortes (sem confundidores não medidos)', 'direta para o efeito da alocação (ITT)',
     'válida para o efeito do rito dentro do 4º JEC (intenção de tratar)'],
    ['Variáveis pós-alocação', '—', 'não aleatorizadas: comparações por elas são observacionais',
     'AC realizada, híbrida, acordo e ausência das partes: observacionais'],
    ['Cegamento', 'em geral irrelevante', 'desejável (participantes, avaliadores, analistas)',
     'ausente: o juiz que sorteia também julga e analisa'],
    ['Nível da unidade de política', '—', 'várias unidades sorteadas (ensaio por conglomerados)',
     'uma unidade escolhida por conveniência (N = 1 conglomerado)'],
    ['Diretriz de relato', 'STROBE', 'CONSORT', 'CONSORT (o projeto cita TREND, própria de desenhos não aleatorizados)'],
], columns=['Característica', 'Estudo observacional (EO)', 'Ensaio controlado aleatorizado (ECA)', 'Experimento do 4º JEC'])
tabela(quadro_eo, 'q_eo_eca', 'EO × ECA: o experimento do 4º JEC é um ECA quanto ao rito, com componentes observacionais',
       secao='7.1', fonte='Elaboração própria a partir do projeto de pesquisa, do resumo expandido e das Partes I a III.')
''')

code(r'''
# ---- diagrama de fluxo (CONSORT) com as contagens da base
excl = todas_q6[~todas_q6['base_primaria'].astype(bool)]
n_a3a4 = int(excl['motivo_exclusao'].astype(str).str.startswith(('A3', 'A4')).sum())
n_a5 = int(excl['motivo_exclusao'].astype(str).str.startswith('A5').sum())

def q6_bloco_grupo(g):
    s = q6[q6['grupo'] == g]
    acr = s['acr']
    if g == 'Controle':
        linha_ac = 'AC: não prevista no rito\n(zero estrutural: 0 audiências)'
    else:
        hib = int(s['hibrida'].fillna(False).astype(bool).sum())
        linha_ac = (f'AC realizada: {int((acr == True).sum())}\n'
                    f'AC não realizada: {int((acr == False).sum())}\n'
                    f'ainda sem registro (ativos): {int(acr.isna().sum())}\n'
                    f'híbridas: {hib}' + (' (A12)' if g == 'Remota' else ''))
    cont = s['desfecho'].value_counts()
    sent = int(s['evento'].astype(int).sum())
    linha_desf = (f'Sentença: {sent}\n'
                  f'  mérito {int(cont.get("Mérito", 0))} · sem mérito {int(cont.get("Sem mérito", 0))}\n'
                  f'  homologação {int(cont.get("Homologação", 0))}\n'
                  f'Redistribuição (Decisão): {int(cont.get("Redistribuição", 0))}\n'
                  f'Em tramitação (censurado): {int(cont.get("Ativo", 0))}')
    return linha_ac, linha_desf

fig, ax = plt.subplots(figsize=(13, 10.5))
ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis('off')

def caixa(x, y, w, h, texto, cor='#555555', fundo='white', peso='normal', tam=9.5):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle='round,pad=0.4,rounding_size=1.2',
                                fc=fundo, ec=cor, lw=1.4))
    ax.text(x, y, texto, ha='center', va='center', fontsize=tam, color=TINTA, fontweight=peso, linespacing=1.3)

def seta(x0, y0, x1, y1):
    ax.annotate('', xy=(x1, y1), xytext=(x0, y0), arrowprops=dict(arrowstyle='-|>', color=TINTA_2, lw=1.1))

caixa(50, 95, 46, 6, f'{len(todas_q6)} linhas na planilha de controle (atualização de 07/10/2026)', peso='bold')
caixa(84, 87, 28, 8.5, f'Excluídas {len(excl)} linhas (seção 1.10):\n{n_a3a4} duplicatas de digitação (A3, A4)\n'
                         f'{n_a5} reentradas re-sorteadas (A5)', cor=CINZA, fundo='#f7f7f7', tam=9)
seta(50, 92, 50, 80.5); ax.plot([50, 70], [86.5, 86.5], color=TINTA_2, lw=1.1)
caixa(50, 77.5, 46, 6, f'{len(q6)} processos aleatorizados (base primária, 01/01 a 03/08/2026)', peso='bold')
xs = {'Controle': 17, 'Presencial': 50, 'Remota': 83}
for g, x in xs.items():
    seta(50, 74.5, x, 69.5)
    caixa(x, 66, 27, 6, f'{ROTULO_GRUPO[g]}\nn = {n_grupo[g]}', cor=CORES_GRUPO[g],
          fundo=mpl.colors.to_rgba(CORES_GRUPO[g], 0.10), peso='bold', tam=9.5)
    l_ac, l_desf = q6_bloco_grupo(g)
    seta(x, 63, x, 57.5)
    caixa(x, 50.5, 27, 13, l_ac, cor=CORES_GRUPO[g], tam=9)
    seta(x, 44, x, 39)
    caixa(x, 29.5, 27, 17, 'Situação em 07/10/2026\n' + l_desf, cor=CORES_GRUPO[g], tam=9)
    seta(x, 21, x, 15.5)
    caixa(x, 11, 27, 7, f'Analisados por intenção de tratar\nn = {n_grupo[g]} (Partes III a V)', cor=CORES_GRUPO[g], tam=9)
figura(fig, 'q_fluxo_consort', 'Fluxo dos processos no experimento: do registro na planilha à análise por intenção de tratar',
       secao='7.1', nota='formato CONSORT; "AC não realizada" = técnica registrada como "**" (extinção anterior à audiência, ausência '
                         'ou outro motivo, não registrado na planilha); '
                         'híbrida = AC pautada como presencial com participação remota de uma das partes.')
''')

interp('q_2_2')

# =====================================================================================
md(r'''
## 7.2 Questão 2.3 — Os três grupos são amostras independentes de uma mesma população?


**Resposta.** Sim, com uma precisão de linguagem e três ressalvas.

**Precisão.** Os grupos não são amostras extraídas por amostragem probabilística, e sim uma **partição aleatória** de um único conjunto: as ações distribuídas ao 4º JEC entre 01/01 e 03/08/2026, praticamente um censo (7.4). A "mesma população" é garantida pelo **sorteio**, e a base da inferência é a aleatorização, o que justifica os testes de permutação.

**Independência.** Cada processo pertence a um só grupo (as reentradas voltaram ao 1º sorteio; A5, seção 1.10), sem pareamento nem medidas repetidas. A única verificação empírica possível é o equilíbrio das variáveis **basais de calendário**, feito abaixo.

**Ressalvas.**

1. **agentes comuns.** O mesmo juiz e cartório, e a mesma conciliadora em cada braço, criam correlação intragrupo. No caso da conciliadora, ela não pode ser corrigida, porque coincide com a modalidade (7.7);
2. **litigantes habituais**, presentes nos três grupos e não identificáveis na planilha;
3. **sorteio restrito ou compensado** (7.1). Totais fixados apenas tornam os testes levemente conservadores. Uma compensação deliberada associa período e grupo, o que recomenda estratificar pelo mês (2.5.1, 4.3.4).

**Influência sobre os testes.** É decisiva: valem os testes para **k amostras independentes** (χ², Fisher, Kruskal-Wallis, Mann-Whitney, Dunn, log-rank, Cox), e não os pareados (McNemar, Wilcoxon pareado, Friedman, Q de Cochran; seção 3.6.3). A **censura** pesa tanto quanto a independência: é ela que desloca a escolha do Kruskal-Wallis para o log-rank (7.10).
''')

code(r'''
# ---- equilíbrio das variáveis basais (as únicas disponíveis antes do sorteio)
q6['mes7'] = q6['mes_distribuicao'].astype(str).replace({'ago': 'jul'})
ordem_mes7 = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul']
ordem_dia = ['seg', 'ter', 'qua', 'qui', 'sex', 'sáb', 'dom']
variaveis_basais = {
    'Mês de distribuição (jul + ago)': ('mes7', ordem_mes7),
    'Dia da semana da distribuição': ('dia_semana_distribuicao', ordem_dia),
    'Origem externa (redistribuído à vara)': ('origem_ext_txt', ['Não', 'Sim']),
}
q6['origem_ext_txt'] = np.where(q6['origem_externa'].astype(bool), 'Sim', 'Não')
eq_linhas, eq_tabs = [], {}
for rotulo, (col, ordem) in variaveis_basais.items():
    tab_ = pd.crosstab(q6[col].astype(str), q6['grupo']).reindex(index=ordem, columns=ORDEM_GRUPO).fillna(0).astype(int)
    eq_tabs[rotulo] = tab_
    chi2_, gl_, p_ass_, p_perm_, esp_min_, v_ = q6_chi2_perm(tab_.to_numpy())
    eq_linhas.append({'Variável basal': rotulo, 'Categorias': len(ordem), 'χ²': chi2_, 'gl': gl_,
                      'Menor esperada': esp_min_, 'p (assintótico)': p_ass_, 'p (permutação)': p_perm_, 'V de Cramér': v_})
eq_df = pd.DataFrame(eq_linhas)
from statsmodels.stats.multitest import multipletests
eq_df['p Holm'] = multipletests(eq_df['p (permutação)'], method='holm')[1]
tabela(eq_df, 'q_equilibrio_basal', 'Equilíbrio das variáveis basais entre os grupos: nenhuma diferença além do acaso',
       secao='7.2', formatos={'gl': 'int', 'Categorias': 'int', 'Menor esperada': 1, 'χ²': 2, 'V de Cramér': 3},
       destaque='p Holm', nota='H0: distribuição da variável igual nos três grupos; p por permutação (20.000 réplicas); '
                               'Holm sobre as três variáveis. Agosto (6 processos) unido a julho.')
''')

code(r'''
fig, axs = plt.subplots(2, 2, figsize=(13, 9))
for ax, (rotulo, tab_) in zip(axs.ravel()[:3], eq_tabs.items()):
    pct = tab_.div(tab_.sum(axis=0), axis=1) * 100
    if rotulo.startswith('Origem'):          # só a categoria rara, para ser legível
        pct = pct.loc[['Sim']].rename(index={'Sim': 'Processos de outro órgão ou ano'})
        barras_agrupadas(ax, pct, cores=CORES_GRUPO, ylabel='Processos do grupo (%)', legenda=False, rotular=True,
                         fmt=lambda v: fmt_br(v, 1) + '%', quebrar=40)
        pct.index = [f'Processos de outro órgão ou ano\n(' + ' / '.join(str(int(tab_.loc['Sim', g])) for g in ORDEM_GRUPO)
                     + ' processos)']
        ax.set_xticks([0], pct.index)
    else:
        barras_agrupadas(ax, pct, cores=CORES_GRUPO, ylabel='Processos do grupo (%)', legenda=False)
    linha = eq_df.set_index('Variável basal').loc[rotulo]
    ax.set_ylim(0, pct.to_numpy().max() * 1.45)
    anotar_teste(ax, texto_teste('χ² de independência (permutação)', f'χ²({int(linha["gl"])}) = {fmt_br(linha["χ²"], 2)}',
                                 linha['p (permutação)'], f'V = {fmt_br(linha["V de Cramér"], 3)}'), loc='upper right')
    ax.set_title(rotulo)
# (d) desequilíbrio acumulado ao longo da ordem de chegada (descritivo: o sorteio restrito)
ordem = q6.sort_values('ordem_chegada')
acum = pd.get_dummies(ordem['grupo'].astype(str)).reindex(columns=ORDEM_GRUPO).cumsum()
amplitude = acum.max(axis=1) - acum.min(axis=1)
ax = axs[1, 1]
ax.plot(ordem['ordem_chegada'].astype(int).to_numpy(), amplitude.to_numpy(), color=TINTA_2, lw=1.4)
i_max = int(np.argmax(amplitude.to_numpy()))
ax.annotate(f'máximo: {int(amplitude.iloc[i_max])} processos\n(ordem {int(ordem["ordem_chegada"].iloc[i_max])}, '
            f'{ordem["dt_distribuicao"].iloc[i_max].strftime("%d/%m")})',
            (int(ordem['ordem_chegada'].iloc[i_max]), int(amplitude.iloc[i_max])), xytext=(-150, -10),
            textcoords='offset points', fontsize=8.5, arrowprops=dict(arrowstyle='-', color=TINTA_2))
ax.annotate(f'final: {int(amplitude.iloc[-1])}', (len(ordem), int(amplitude.iloc[-1])), xytext=(-40, 18),
            textcoords='offset points', fontsize=8.5, arrowprops=dict(arrowstyle='-', color=TINTA_2))
ax.set_xlabel(ROTULOS['ordem_chegada']); ax.set_ylabel('Maior − menor grupo acumulado (processos)')
ax.set_title('Desequilíbrio acumulado dos grupos na ordem de chegada')
# legenda dentro do painel (a), no canto livre (o figura() aplica tight_layout, que ignora fig.legend)
axs[0, 0].legend(handles=[mpl.patches.Patch(color=CORES_GRUPO[g], label=rotulo_grupo(g, com_n=True)) for g in ORDEM_GRUPO],
                 loc='upper left', ncol=1, frameon=False, fontsize=9)
figura(fig, 'q_equilibrio_basal', 'As variáveis basais estão equilibradas entre os grupos; o desequilíbrio acumulado foi compensado no fim',
       secao='7.2', nota='painéis (a) a (c): % dentro de cada grupo; painel (d): diferença entre o maior e o menor grupo '
                         'acumulado após cada processo (descritivo; o teste do equilíbrio final está na seção 2.5.1).')
''')

interp('q_2_3')

# =====================================================================================
md(r'''
## 7.3 Questão 2.4 — O que significam "híbrida" e "Decisão"?


**"Híbrida".** É uma **AC pautada como presencial** em que uma das partes participou por videoconferência, a pedido próprio deferido pelo juiz (Res. CNJ nº 481/2022). Estatisticamente, é **não adesão parcial** ao rito sorteado, decidida pela parte depois do sorteio. Daí três consequências:

1. a comparação "híbrida × presencial pura" é observacional e não testa causalmente a hipótese H4 do projeto;
2. na análise principal, por intenção de tratar, as híbridas ficam na Presencial; movê-las para a Remota ("conforme tratado") é sensibilidade (4.9);
3. o "Não" tem dois sentidos: no Controle é zero estrutural ("não se aplica"); nos braços com AC, é audiência na modalidade pautada. Há ainda três "Sim" incoerentes na Remota (A12) e três "Sim" na Presencial sem AC realizada (A13), sinalizados como desvio de protocolo (1.12).

**"Decisão".** É a **remessa do processo a outro juízo**, prevento (CPC, arts. 59 e 286): o processo sai do 4º JEC e nunca terá sentença ali. Contá-la como encerramento (E10) mistura um ato administrativo, com mediana de 1 dia, com o tempo até a sentença. Aqui a redistribuição é tratada de três formas:

- como **risco competitivo** (4.7);
- como censura no Cox causa-específico (4.5);
- como exclusão ou evento nas análises de sensibilidade (4.9).

No desenho, é uma inelegibilidade descoberta depois do sorteio, e o processo que voltou foi sorteado de novo (A5).

O quadro resume as duas variáveis, com as contagens da base primária e o efeito de cada tratamento sobre as conclusões.
''')

code(r'''
hib = q6['hibrida'].fillna(False).astype(bool)
red = q6[q6['desfecho'] == 'Redistribuição']
red_t = red['tempo'].astype(float)
n_red = red['grupo'].value_counts().reindex(ORDEM_GRUPO)
quadro_hd = pd.DataFrame([
    ['Híbrida = Sim', 'AC pautada como presencial com participação remota de uma parte (pedido deferido)',
     'pós-sorteio; não adesão parcial ao rito sorteado',
     f'Presencial {int((hib & (q6.grupo == "Presencial")).sum())}; Remota {int((hib & (q6.grupo == "Remota")).sum())} (A12, incoerente); '
     f'Controle {int((hib & (q6.grupo == "Controle")).sum())}',
     'ITT: mantida no grupo sorteado; sensibilidade "conforme tratado" (4.9); acordo na AC híbrida × pura (3.3.4)',
     'não altera: HR da Remota 0,79 com as híbridas "como tratadas" (0,81 no principal; 4.9); acordo 1/24 × 8/154, Fisher p = 1,000'],
    ['Híbrida = Não', 'AC realizada integralmente na modalidade pautada; no Controle, "não se aplica"',
     'zero estrutural no Controle', f'{int((~hib).sum())} registros (Controle: todos)',
     'distinguir "Não" de "não se aplica" (1.7, 1.11)', '—'],
    ['Sentença/decisão = "Decisão"', 'remessa a outro juízo por prevenção (CPC, arts. 59 e 286): o processo sai da vara',
     'saída do estudo antes da sentença; risco competitivo',
     f'{len(red)} na base primária (Controle {n_red["Controle"]}, Presencial {n_red["Presencial"]}, Remota {n_red["Remota"]}); '
     f'mediana {fmt_br(red_t.median(), 0)} dia; {int((red_t > 30).sum())} após 30 dias',
     'evento_cr = 2 (Aalen-Johansen, Fine-Gray, 4.7); censura no Cox causa-específico; exclusão e "evento" como sensibilidade (4.9)',
     'não altera: proporção igual entre grupos (3.2.4); viés do 1 − KM ≤ 3 p.p. aos 180 dias (4.7.1)'],
    ['Reentrada após "Decisão"', 'processo redistribuído que voltou e foi sorteado de novo, às vezes para outro grupo',
     'violação da unicidade da unidade experimental', '3 linhas (A5)', 'excluídas: vale o primeiro sorteio (1.10)',
     'não altera: HR da Remota 0,80 com as duplicatas e 0,805 com as reentradas unidas ao 1º sorteio (4.9)'],
], columns=['Registro', 'Significado', 'Natureza no desenho', 'Contagem (base primária)', 'Tratamento neste notebook',
            'Efeito sobre a conclusão'])
tabela(quadro_hd, 'q_hibrida_decisao', '"Híbrida" é não adesão parcial ao rito; "Decisão" é saída do estudo por redistribuição',
       secao='7.3', fonte='Elaboração própria; contagens da base primária (938 processos); efeitos conforme as Partes III e IV.')
''')

interp('q_2_4')

# =====================================================================================
md(r'''
## 7.4 Questão 2.5 — Populações de interesse, disponível e amostrada; cruzamento com os 14 JECs; há dados no CNJ?


**As três populações.**

- **De interesse** (alvo) é aquela sobre a qual se quer concluir: as ações do procedimento do JEC cível (classe CNJ 436) distribuídas aos **14 JECs de Natal** no período e, no sentido amplo do projeto, os JECs cíveis em geral.
- **Disponível** é a parte acessível: as ações distribuídas ao **4º JEC** entre 01/01 e 03/08/2026, a única unidade cujo juiz aderiu. O primeiro processo é de 01/01/2026, e não de 2/1, como diz o enunciado (seção 1.13).
- **Amostrada** é o que entrou na base: 943 processos sorteados (944 linhas), reduzidos a **938** processos distintos (1.10), observados até 07/10/2026 (708 sentenças, 24 redistribuições, 206 censurados). É praticamente um censo da população disponível e um **conglomerado escolhido por conveniência** em relação à de interesse.

A inferência estatística vai da amostrada à disponível. A passagem à de interesse é **extrapolação**, que depende de argumento substantivo, e não de cálculo.

**Há dados no CNJ: o DataJud.** A API Pública do DataJud traz, por processo, classe, órgão julgador, data de ajuizamento e cada **movimento** codificado pelas Tabelas Processuais Unificadas (TPU), com data e hora: audiência, homologação, julgamento com ou sem mérito, redistribuição. Filtrando o endpoint `api_publica_tjrn` pela classe 436, pelos órgãos julgadores dos 14 JECs (o 4º é o 13285) e pela data de ajuizamento, reconstrói-se o tempo até o primeiro julgamento com a mesma regra de censura. O vínculo com a planilha é exato, pelo número CNJ.

**O que a Parte VI fez com esses dados.**

- validou a planilha: vínculo de 98,7%, κ = 0,961 no tipo de desfecho, datas 97,9% iguais e sentenças de fim de semana reais (6.3);
- estendeu o seguimento até 06/11/2026 (6.4);
- comparou o 4º JEC com os demais (6.6.2). A entrada é repartida de modo equitativo entre os 14 (CPC, art. 285), mas o 4º JEC já era atípico em 2025.

**Limites.** A API não traz partes, valor da causa, advogado nem magistrado. Por sobrecarga, a coleta dos outros 13 JECs não se completou, e a comparação entre unidades ficou em contagens agregadas, sem tempos (6.6.1).
''')

code(r'''
quadro_pop = pd.DataFrame([
    ['De interesse (alvo)', 'ações do procedimento do JEC cível (classe 436) dos 14 JECs de Natal, 01/01 a 03/08/2026; '
     'em sentido amplo, JECs cíveis sob a política de conciliação do CNJ', 'desconhecido na planilha; contagens agregadas no DataJud (6.6.2)',
     'extrapolação: exige argumento substantivo ou replicação (7.9)'],
    ['Disponível (acessível)', 'ações distribuídas ao 4º JEC de Natal, 01/01 a 03/08/2026',
     '943 sorteadas (resumo expandido); 944 linhas na planilha', 'unidade única, escolhida por conveniência'],
    ['Amostrada (analisada)', 'processos distintos da planilha, observados até 07/10/2026',
     f'{len(q6)} processos: {int(q6.evento.astype(int).sum())} sentenças, {int((q6.desfecho == "Redistribuição").sum())} redistribuições, '
     f'{int((q6.desfecho == "Ativo").sum())} censurados', 'censo da disponível; inferência por aleatorização válida para o 4º JEC'],
], columns=['População', 'Definição', 'Tamanho e fonte', 'Alcance da inferência'])
tabela(quadro_pop, 'q_populacoes', 'Populações de interesse, disponível e amostrada', secao='7.4',
       fonte='Elaboração própria a partir do projeto de pesquisa, do resumo expandido e da Parte I.')

quadro_dj = pd.DataFrame([
    ['Número CNJ', 'sim', 'sim', 'vínculo exato: 926 de 938 (98,7%; 6.3.1)'],
    ['Data de distribuição / ajuizamento', 'sim', 'sim (dataAjuizamento; movimento de distribuição)', 'origem do tempo; 99,9% iguais à entrada na unidade (6.3.2)'],
    ['Data e tipo da sentença', 'sim (digitado; 18% em fim de semana, A16)', 'sim (movimentos TPU com data e hora)',
     'datas 97,9% iguais; tipo κ = 0,961; fins de semana reais (6.3.2, 6.3.3)'],
    ['Redistribuição', 'sim ("Decisão")', 'sim (movimento de redistribuição)', 'risco competitivo nos 14 JECs'],
    ['Audiência de conciliação (data, realização)', 'não (só a técnica)', 'sim, quando lançada (movimentos de audiência)',
     'AC realizada κ = 0,972 (6.3.2); decompor o tempo em etapas'],
    ['Grupo do experimento, técnica, híbrida', 'sim', 'não', 'só existem na planilha'],
    ['Partes, polo passivo, litigante habitual', 'não', 'não (dados de partes fora da API pública)', 'covariável faltante (7.8)'],
    ['Valor da causa, assunto', 'não', 'assunto sim (TPU); valor da causa não', 'assunto como covariável basal'],
    ['Magistrado, advogado', 'não', 'não', 'efeito de juiz só por órgão julgador'],
], columns=['Informação', 'Planilha do experimento', 'DataJud (API pública)', 'Uso no estudo'])
tabela(quadro_dj, 'q_datajud', 'O que o DataJud acrescenta à planilha e o que continua faltando', secao='7.4',
       fonte='Elaboração própria a partir da documentação da API Pública do DataJud (CNJ) e das Partes I e VI.')
''')

interp('q_2_5')

# =====================================================================================
md(r'''
## 7.5 Questão 2.6 — O tratamento dos dados brutos no notebook do professor foi adequado?


**Resposta.** **Não foi adequado**. O notebook faz uma auditoria inicial útil, mas não age sobre o que encontra, e o problema central é a **definição da variável-alvo**:

1. **duração dos ativos até `TODAY()`** (fórmula volátil). Os 209 ativos da planilha (206 na base primária) são tratados como tempos completos (E7, E14; A1). Aqui, a censura foi fixada em 07/10/2026 e o tempo foi recalculado pelas datas (1.4);
2. **"Decisão" contada como encerramento** (E10), quando é redistribuição (7.3);
3. **duplicatas e reentradas mantidas** (E3; A3–A5, seção 1.10);
4. **`**` e ausências estruturais** tratados como categoria ou como "Não" (E4, E5; 1.7);
5. **quatro colunas de duração idênticas** (E6, A17), que contaminam a matriz de correlações (7.6);
6. grafias, números CNJ, origem externa e desvios da híbrida não tratados (A2, A6–A9, A12, A13).

**Como complementar.** A Parte I responde a cada item com uma regra explícita, registrada no log e no dicionário (1.15, 1.16), sem imputar nada. O DataJud confirmou datas e desfechos (6.3) e revelou um **atraso de alimentação**: 11 processos ainda "ativos" em 07/10 já estavam encerrados. Só o PJe fornece o que ainda falta: o **motivo da extinção sem mérito**, a **data da AC** e as **covariáveis** previstas no projeto.
''')

code(r'''
quadro_trat = pd.DataFrame([
    ['E7, E14 / A1', 'duração dos ativos até TODAY(); censurados tratados como tempos completos',
     'tempo recalculado das datas; censura fixa em 07/10/2026; par (tempo, evento)', '1.4, 1.13'],
    ['E10 / Decisão', '"Decisão" contada como encerramento', 'tipo "Redistribuição"; evento = 0, evento_cr = 2, causa = 4', '1.11.2, 1.12.1'],
    ['E3 / A3–A5', 'duplicatas detectadas e mantidas', '6 linhas excluídas; 1 processo = 1 unidade, grupo do 1º sorteio', '1.10'],
    ['E2 / A2', 'linha sem fórmulas e STATUS vazio', 'mantida como ativo censurado (data de distribuição válida)', '1.13'],
    ['E4, E5', '"**" e NA como categorias ou como "Não"', 'NA estrutural × NA de registro; ac_realizada; tabela de padrões de ausência', '1.7'],
    ['E6 / A17', 'quatro colunas de duração idênticas tratadas como variáveis distintas', 'descartadas; uma só variável-tempo', '1.4'],
    ['A6', 'grafia variante do tipo de sentença (11 casos)', 'recodificada para a forma canônica', '1.11'],
    ['A7, A8', 'CNJ com espaço, hífen ou órgão truncado', 'normalizado; dígito verificador (mod 97) confere em 100%', '1.9'],
    ['A9', 'processos de outro órgão ou ano (redistribuídos à vara)', 'mantidos; flag origem_externa; sensibilidade', '1.9.1, 4.9'],
    ['E11 / A12, A13', 'híbrida ignorada; híbridas incoerentes', 'flags de desvio de protocolo; ITT e "conforme tratado"', '1.12, 4.9'],
    ['A15', 'desfechos no dia zero descartados no ajuste (x > 0)', 'mantidos; 0,5 dia só nos modelos paramétricos', '1.13, 2.2.5'],
    ['A16', 'não examinado', 'flag sentenca_fim_semana; sensibilidade; datas confirmadas no DataJud (reais)', '2.5.4, 4.9, 6.3.3'],
    ['—', 'sem dicionário nem registro das decisões', 'log de tratamentos e dicionário exportados', '1.15, 1.16'],
], columns=['Código', 'No notebook do professor', 'Tratamento neste notebook', 'Seção'])
tabela(quadro_trat, 'q_tratamento', 'Tratamento dos dados brutos: o que o notebook do professor deixou de fazer e como foi feito aqui',
       secao='7.5', fonte='Elaboração própria; códigos E1–E30 de docs/r2_notebook_professor.md e A1–A20 de docs/r3_auditoria_dados.md.')
''')

interp('q_2_6')

# =====================================================================================
md(r'''
## 7.6 Questão 2.7 — A matriz de correlações é adequada? Ordem de chegada × duração


**A matriz não é adequada**, por três razões, cada uma suficiente:

1. **é tautológica.** As quatro colunas (`DURAÇÃO-SENT2`, `-SORT`, `-PROC`, `-TECN`) são a mesma fórmula da planilha, e r = 1 é identidade aritmética (E6, E16; 2.6.4);
2. **não há outra variável quantitativa.** As demais são nominais e pedem o V de Cramér; entre uma nominal e o tempo, a razão η ou, melhor, um modelo de sobrevivência. A seção 2.6.4 substitui a matriz por uma **matriz de associação**;
3. **ignora a censura.** Um quarto dos tempos é limite inferior.

**A ordem de chegada pode ser investigada, mas não pela correlação bruta.** A ordem é ordinal e admite Spearman ou Kendall. O obstáculo é estrutural: com um corte comum, quanto mais tarde o processo chegou, menor o seguimento possível. Um processo de julho só aparece como sentenciado se for rápido, o que gera uma correlação **negativa artificial**. A seção 3.5.2 mediu esse artefato por simulação, e a figura abaixo compara o ρ observado com o que a censura sozinha produziria.

A pergunta substantiva ("o tempo mudou ao longo do experimento?") pede o mês ou a ordem como **covariável num modelo de sobrevivência**:

- **Cox** (4.5): HR de 0,70 em junho e de 0,58 em julho–agosto, contra janeiro;
- **medianas de Kaplan-Meier por mês** (5.1): de 75 dias em janeiro a 99 em junho, cerca de **5,7% ao mês**. Os AFT paramétricos exageram essa tendência;
- **por grupo**, na janela comum (H10, 3.5.2): ρ = +0,05 no Controle (p = 0,34), +0,14 na Presencial e +0,22 na Remota.

A desaceleração é **dos braços com AC**, e não da vara, o que é compatível com o acúmulo da pauta de audiências. A ordem serviu também para o teste de corridas do sorteio (3.5.1).
''')

code(r'''
sim_ordem = q6_csv('tst_ordem_simulacao.csv')
if sim_ordem is not None:
    rot_v = {'todos (censura ignorada)': 'Todos os tempos\n(censura ignorada)', 'só encerrados': 'Só os\nsentenciados',
             'min(T, 65)': 'Janela comum\nmin(T, 65)'}
    fig, ax = plt.subplots(figsize=(9.5, 5))
    for i, lin in sim_ordem.reset_index(drop=True).iterrows():
        ax.plot([lin['Percentil 2,5'], lin['Percentil 97,5']], [i, i], color=CINZA, lw=7, solid_capstyle='butt',
                label='Intervalo de 95% sob H₀ (só a censura)' if i == 0 else None)
        ax.plot(lin['ρ médio sob H₀'], i, marker='|', ms=18, color=TINTA_2, mew=2, label='ρ médio sob H₀' if i == 0 else None)
        ax.plot(lin['ρ observado'], i, 'o', ms=9, color=DESTAQUE, label='ρ observado' if i == 0 else None)
        ax.annotate(fmt_br(lin['ρ observado'], 3), (lin['ρ observado'], i), xytext=(0, 10), textcoords='offset points',
                    ha='center', fontsize=9, color=DESTAQUE)
    ax.axvline(0, color=TINTA_2, lw=0.8, ls='--')
    ax.set_yticks(range(len(sim_ordem)), [rot_v.get(v, v) for v in sim_ordem['Versão']])
    ax.invert_yaxis()
    ax.set_xlabel('ρ de Spearman entre ordem de chegada e tempo')
    ax.set_title('O ρ observado contra o que a censura produz sem nenhuma associação')
    legenda_abaixo(ax, ncol=3)
    figura(fig, 'q_ordem_artefato', 'Só a censura tornaria a correlação fortemente negativa; a observada é menos negativa '
           'e, na janela comum, positiva: os processos que chegaram depois demoram mais', secao='7.6',
           nota='simulação da seção 3.5.2: 500 réplicas de tempos Weibull independentes da ordem, censurados pelo seguimento '
                'real de cada processo; janela comum = tempo truncado em 65 dias, sem redistribuídos (por isso ρ = 0,140, '
                'e não os 0,138 da versão com os 938 processos, seção 2.6.5).')
''')

interp('q_2_7')

# =====================================================================================
md(r'''
## 7.7 Questão 2.8 — Variáveis de confundimento


**Conceito.** Um **confundidor** está associado à exposição e ao desfecho sem estar no caminho causal entre eles. Distingue-se do **mediador** (o caminho pelo qual o tratamento age, como a fila da pauta ou a ausência do autor à AC) e do **modificador de efeito** (que muda o tamanho do efeito, como o perfil da unidade).

**O que o sorteio controla.** Controla, **em expectativa**, todos os fatores do processo anteriores ao sorteio: tipo de ação, valor, partes, litigante habitual, advogado. Por isso, a falta dessas variáveis não enviesa a comparação, embora impeça verificar o equilíbrio. O sorteio **não controla** três famílias de fatores:

- **os amarrados ao braço.** A conciliadora é a mesma para todos os processos de cada braço, o que torna modalidade e pessoa indissociáveis (H5 inestimável);
- **os que agem sem cegamento.** O juiz-pesquisador, a reatividade (Hawthorne) e a contaminação entre grupos. Há um teste indireto na Parte VI: o Controle de 2026 tramitou como o 4º JEC de 2025 (RMST180 80,7 × 80,2 dias; p = 0,91; 6.6.3). Isso reduz a suspeita sem eliminá-la;
- **os que variam no tempo.** O mês (junho com excesso de Presencial e julho de Remota; resíduos ajustados de 2,95 e 3,10; 3.5.3) foi **controlado na análise** por estratificação (4.3.4, 4.5).
''')

code(r'''
quadro_conf = pd.DataFrame([
    ['Conciliadora (CEJUSC × gabinete)', 'condutora diferente em cada braço; habilidade e estilo próprios',
     'acordo e tempo do braço refletem a pessoa, não só a modalidade', 'indeterminada (Presencial × Remota)',
     'não: confundida por desenho', 'rodízio das conciliadoras entre modalidades; várias conciliadoras por braço'],
    ['Juiz-pesquisador não cego', 'quem sorteia também pauta, julga e analisa',
     'ritmo de sentença diferente por grupo, consciente ou não', 'indeterminada; os resultados contrariam H1, o que atenua a suspeita',
     'não', 'análise cega ao grupo; desfecho extraído do PJe/DataJud por terceiro'],
    ['Reatividade (Hawthorne)', 'equipe sabe que é observada', 'aceleração geral ou do braço "de interesse"', 'tende a reduzir tempos em todos os grupos',
     'não; sem sinal no Controle (6.6.3)', 'feito: Controle 2026 ≈ 4º JEC 2025 (6.6.3); DiD com tempos dos 13 JECs (não executado)'],
    ['Contaminação entre grupos', 'mesmo cartório, mesma equipe e mesmas práticas nos três ritos',
     'práticas da AC vazam para o Controle', 'para zero (subestima diferenças)', 'não; sem sinal no Controle (6.6.3)', 'ensaio por conglomerados (unidades sorteadas)'],
    ['Mês de distribuição / acúmulo de acervo', 'composição dos grupos varia por mês; medianas de KM +5,7% ao mês, desaceleração nos braços com AC',
     'grupo com mais entradas tardias parece mais lento', 'contra a Remota (mais casos em julho)',
     'parcialmente (sorteio restrito)', 'estratificação por mês (feita: 4.3.4, 4.5); blocos por mês na replicação'],
    ['Tipo de ação, valor da causa, nº de partes', 'complexidade e chance de acordo variam com o caso',
     'tempo e acordo', 'nenhuma em expectativa', 'sim, em expectativa (sorteio)', 'coletar para verificar o equilíbrio e ganhar precisão'],
    ['Litigante habitual, advogado constituído', 'réus repetidos e assistência técnica', 'acordo, ausência, tempo', 'nenhuma em expectativa',
     'sim, em expectativa; dependência entre processos', 'coletar; erros-padrão por agrupamento'],
    ['Audiência híbrida (adesão)', 'pedido da parte após o sorteio', 'acordo e tempo da AC', 'pequena (28 casos)',
     'sim pela análise ITT', 'ITT principal; "conforme tratado" como sensibilidade (feita: 4.9)'],
    ['Ausência do autor à AC (art. 51, I, Lei 9.099/95)', 'mediador: a AC obrigatória cria a ocasião da extinção',
     'mais extinções sem mérito nos braços com AC', 'é parte do efeito do rito (não é viés)', 'não se aplica (mediador)',
     'registrar comparecimento e motivo da extinção'],
    ['Fila da pauta da AC', 'mediador: a AC acrescenta uma etapa ao rito', 'sentenças de mérito mais tardias', 'é parte do efeito do rito',
     'não se aplica (mediador)', 'registrar data da AC; decompor o tempo em etapas'],
    ['Técnica de conciliação', 'sorteada por audiência', 'acordo na AC', 'nenhuma (sorteio uniforme, p = 0,566)',
     'sim (sorteio)', '—'],
    ['Data da sentença registrada', '18,4% em fim de semana; suspeita de data de lançamento', 'erro de medida do tempo',
     'afastada: 98,5% no mesmo dia no DataJud', 'verificada (6.3.3)', 'nenhuma correção necessária'],
    ['Redistribuição por prevenção', 'saída do estudo antes da sentença', 'remove casos do risco', 'nenhuma (igual entre grupos, p = 0,393)',
     'sim, na análise (risco competitivo)', 'triagem de prevenção antes do sorteio'],
], columns=['Variável', 'Mecanismo', 'Efeito provável', 'Direção do viés', 'Controlada pelo desenho?', 'Como controlar'])
tabela(quadro_conf, 'q_confundidores', 'Variáveis de confundimento, mediadores e ameaças: efeito provável e controle pelo desenho',
       secao='7.7', fonte='Elaboração própria a partir do projeto de pesquisa, do texto antagonista (ODT) e das Partes II a IV e VI.')
''')

interp('q_2_8')

# =====================================================================================
md(r'''
## 7.8 Questão 2.9 — Outras variáveis quantitativas em escala intervalar


**Sim, e elas fariam falta.** A planilha não tem nenhuma variável quantitativa além do tempo. Do PJe e, em parte, do DataJud podem ser extraídos dois tipos de variável:

- **basais** (anteriores ao sorteio): número de autores e de réus, valor da causa, número de pedidos. Servem como **covariáveis**, para verificar o equilíbrio e ganhar precisão;
- **de processo** (posteriores ao sorteio): número de atos, remarcações da AC, dias até a citação, até a AC e até a sentença. São **mediadores** ou componentes do próprio tempo. O número de atos cresce com a duração, e a causalidade é reversa: só pode entrar como **covariável dependente do tempo**, ou como taxa (atos por 30 dias).

A rigor, contagens e valores monetários estão em escala de **razão**, que contém a intervalar. O que importa para a escolha da medida é que são quantitativas, assimétricas e, nas contagens, com muitos empates.

**Que correlação e que teste.**

- **Sem censura:**
  - **Pearson** mede associação linear e supõe normalidade bivariada; teste t = r√(n − 2)/√(1 − r²), com n − 2 gl. É pouco indicado para tempos e contagens;
  - **Spearman** (monotônica) e **Kendall τ_b** (preferível com muitos empates) têm teste t, normal, exato ou por permutação (SIEGEL; CASTELLAN, 2006, cap. 9).
- **Com censura**, nenhuma dessas correlações vale. A covariável entra num **Cox** (HR por unidade; testes de Wald, escore ou razão de verossimilhanças; COLOSIMO; GIOLO, 2006, cap. 5), num **AFT** (razão de tempos) ou no **C de Harrell**, que generaliza o τ de Kendall a dados censurados. A forma funcional se verifica pelos resíduos martingal (4.5.4).
''')

code(r'''
quadro_vars = pd.DataFrame([
    ['Número de autores; número de réus', 'razão (contagem discreta)', 'PJe (não está na API pública)', 'basal',
     'Kendall τ_b (empates); com censura: Cox (HR por parte a mais)', 'equilíbrio entre grupos; covariável'],
    ['Valor da causa (R$)', 'razão (contínua, assimétrica)', 'PJe', 'basal', 'Spearman; com censura: Cox com log(valor)',
     'transformar em log; teto de 40 salários mínimos nos JECs'],
    ['Pessoa jurídica / litigante habitual no polo passivo', 'nominal (não quantitativa)', 'PJe', 'basal',
     'V de Cramér; Cox com indicadora', 'agrupamento por réu'],
    ['Dias da distribuição até a citação', 'razão (contínua)', 'PJe; DataJud (movimentos)', 'pós-sorteio (etapa)',
     'decomposição do tempo; Cox por etapa', 'censura em cada etapa'],
    ['Dias da distribuição até a AC (pauta)', 'razão (contínua)', 'PJe; DataJud', 'pós-sorteio (mediador)',
     'decomposição do tempo; covariável dependente do tempo', 'só existe nos braços com AC'],
    ['Dias da AC (ou da contestação) até a sentença', 'razão (contínua)', 'PJe; DataJud', 'pós-sorteio (etapa)',
     'KM/Cox a partir da AC', 'origem do relógio na AC'],
    ['Número de atos da serventia e do juiz', 'razão (contagem)', 'PJe; DataJud (movimentos)', 'pós-sorteio',
     'taxa por 30 dias × grupo (Mann-Whitney/Poisson com offset)', 'cresce mecanicamente com a duração'],
    ['Número de remarcações da AC', 'razão (contagem)', 'PJe', 'pós-sorteio', 'Kendall τ_b; Poisson/binomial negativa',
     'mede atrito do rito'],
], columns=['Variável', 'Escala', 'Fonte', 'Momento', 'Medida e teste adequados', 'Cuidado'])
tabela(quadro_vars, 'q_vars_quantitativas', 'Variáveis quantitativas que poderiam ser extraídas e a medida de associação adequada a cada uma',
       secao='7.8', fonte='Elaboração própria; SIEGEL; CASTELLAN (2006); COLOSIMO; GIOLO (2006).')
''')

interp('q_2_9')

# =====================================================================================
md(r'''
## 7.9 Questão 2.10 — Validade interna e externa; generalização aos 14 JECs


**Validade interna: razoável para o efeito do rito no 4º JEC.**

- **A favor**:
  - sorteio individual, grupos contemporâneos e equilibrados nas variáveis basais (7.2);
  - intenção de tratar, com tratamento da censura e dos riscos competitivos (Parte IV);
  - robustez: em 11 dos 12 cenários alternativos de curadoria, o HR da Remota fica entre 0,77 e 0,83, com IC abaixo de 1 (4.9). A exceção é a censura comum em 65 dias, anterior à janela do efeito;
  - o seguimento estendido mantém a direção (HR da Remota 0,75; 6.4).
- **Contra**:
  - a integridade não verificável do sorteio (7.1);
  - a conciliadora confundida com a modalidade, o que afeta só Presencial × Remota;
  - o juiz-pesquisador não cego;
  - a reatividade e a contaminação, para as quais não há sinal no Controle (6.6.3).

**Validade externa: não há base estatística para generalizar aos 14 JECs.** No nível em que a política seria adotada, a serventia, N = 1, escolhida por conveniência. É preciso separar os processos da unidade:

- **os processos são comparáveis em expectativa.** A distribuição é alternada e aleatória (CPC, art. 285), e a entrada é equitativa entre os 14 (6.6.2);
- **a unidade não é representativa.** A premissa dos autores, de "conglomerados homogêneos", foi **testada e rejeitada**: em 2025, os perfis de desfecho dos 14 eram heterogêneos (χ² = 185,5 e 93,8; 13 gl; p < 0,001), e o 4º JEC era o 2º com mais extinções sem mérito (36% × 26%) e o 2º com menos mérito (61% × 68%).

Como um dos mecanismos envolve justamente a extinção sem mérito, o efeito numa unidade que já extinguia mais pode diferir do de um juizado típico. A generalização possível é **analítica** (o mecanismo), e não estatística.

**O que o DataJud permitiu verificar (Parte VI).** São comparações observacionais, que medem o efeito do experimento **sobre a unidade**, e não o do rito:

1. **antes × durante** (6.6.3): o Controle de 2026 equivale ao 4º JEC de 2025 (RMST180 80,7 × 80,2 dias; p = 0,91), e os braços com AC foram mais lentos que esse patamar (85,6 e 95,7 dias). Sem os tempos dos outros 13 JECs, porém, não se exclui uma mudança comum à capital;
2. **4º JEC × os outros 13** (6.6.2): a proporção com sentença de mérito caiu 11,8 p.p. a mais no 4º JEC, a maior queda entre os 14 (p de permutação 0,071, o mínimo possível). É um resultado **descritivo, não identificado**: cerca de 30% da queda vem do seguimento desigual, e as tendências paralelas não foram testadas (6.6.1).

**Outra comarca ou outro estado** ficam como **trabalhos futuros**: ali a validade externa exige **replicar o experimento** (sortear os ritos em outras unidades), e não comparar tempos observacionalmente, porque unidades diferentes diferem em tudo o que o sorteio interno controlava.
''')

code(r'''
quadro_val = pd.DataFrame([
    ['Alocação por sorteio individual e controle contemporâneo', 'interna', 'favorece', 'efeito causal do rito no 4º JEC (ITT)'],
    ['Censura e riscos competitivos tratados (Parte IV)', 'interna / estatística', 'favorece', 'estimativas não enviesadas pelo seguimento'],
    ['Conciliadora confundida com a modalidade', 'interna', 'ameaça', 'Presencial × Remota não separa modalidade de pessoa'],
    ['Integridade do sorteio (sequência e ocultação)', 'interna', 'ameaça', 'plausível, mas não verificável (7.1)'],
    ['Juiz-pesquisador não cego', 'interna / constructo', 'ameaça', 'possível ritmo diferencial; não verificável'],
    ['Reatividade (Hawthorne) e contaminação', 'interna', 'ameaça atenuada', 'Controle 2026 ≈ 4º JEC 2025 (6.6.3): sem sinal no Controle'],
    ['Seguimento curto (65 a 279 dias) e 24,5% sem desfecho', 'estatística', 'ameaça (tratada)', 'RMST; extensão até 06/11 mantém a direção (6.4)'],
    ['Unidade única, escolhida por conveniência (N = 1)', 'externa', 'ameaça grave', 'sem inferência estatística para os 14 JECs'],
    ['Distribuição aleatória e equitativa entre os 14 JECs (CPC, art. 285; 6.6.2)', 'externa', 'favorece parcialmente', 'perfil dos processos semelhante em expectativa'],
    ['4º JEC atípico já em 2025 (mais extinção sem mérito, menos mérito; 6.6.2)', 'externa', 'ameaça grave', 'efeito pode não se transportar a outra unidade'],
    ['Período de 7 meses de 2026', 'externa (tempo)', 'ameaça', 'sazonalidade e acúmulo de acervo específicos'],
], columns=['Aspecto', 'Tipo de validade', 'Efeito', 'Consequência'])
tabela(quadro_val, 'q_validade', 'Validade interna razoável no 4º JEC; validade externa sem base estatística para os 14 JECs',
       secao='7.9', fonte='Elaboração própria a partir das Partes II a VI e do texto antagonista (ODT).')

quadro_cmp = pd.DataFrame([
    ['Sorteio interno (este notebook)', 'efeito do rito sobre o tempo e o acordo no 4º JEC', 'KM, log-rank, Cox, RMST, riscos competitivos',
     'planilha (938)', 'feito (Partes III a V)'],
    ['4º JEC antes (2025) × durante (2026)', 'o experimento mudou o tempo da unidade?', 'KM/Cox por período (série interrompida)',
     'DataJud', 'feito (6.6.3): Controle 2026 ≈ 2025; braços com AC mais lentos'],
    ['4º JEC × outros 13 JECs de Natal, antes e durante', 'efeito do experimento além da tendência da capital',
     'diferenças em diferenças com Cox estratificado por juizado', 'DataJud',
     'só agregado e descritivo (6.6.2: mérito −11,8 p.p.); com tempos, não executado (6.6.1)'],
    ['Outra comarca ou estado', 'o efeito do rito se transporta?', 'replicação do ECA (multicêntrico, por conglomerados)',
     'nova coleta primária', 'trabalho futuro'],
], columns=['Comparação', 'Pergunta', 'Método', 'Dados', 'Situação'])
tabela(quadro_cmp, 'q_comparacoes', 'Comparações possíveis: só o sorteio interno identifica o efeito do rito',
       secao='7.9', fonte='Elaboração própria.')
''')

interp('q_2_10')

# =====================================================================================
md(r'''
## 7.10 Questão 2.11 — Os testes de significância do notebook do professor foram adequados? Que outros caberiam?


**Resposta.** **Não.** Um teste é adequado quando três condições se cumprem:

1. a hipótese nula responde a uma pergunta substantiva;
2. os pressupostos valem para os dados;
3. o resultado vem com tamanho de efeito, intervalo e controle de multiplicidade.

O notebook do professor falha na primeira condição em quatro testes, na segunda em quase todos (pela **censura**) e na terceira em todos (E27). O quadro avalia cada teste (Parte III, 3.6.1; Parte IV).

O caso exemplar é o **Kruskal-Wallis** da duração por grupo (p = 0,478 nas 943 linhas; 0,559 na base primária). Ele trata os 206 ativos como encerrados no dia do corte, e os ativos se concentram nos braços com AC (14,7%, 23,6% e 27,7%): o teste **trunca a cauda longa dos grupos tratados**. O Kaplan-Meier com log-rank, único teste que o professor chamou de "imprescindível", nunca rodou (E1).

**Outros testes aplicáveis.** A lista abaixo indica, para cada família, o que cada referência sugerida pelo roteiro cobre. Os demais métodos remetem à literatura específica.

- **fundamentos e decisão** (BECKER, 2015): lógica do TSHN (hipóteses, erros dos tipos I e II, poder, valor-p) e intervalo de confiança como forma de relato, testes para médias e proporções e qui-quadrado. Faltava ao notebook do professor relatar IC e tamanho de efeito ao lado de cada p. O controle de multiplicidade usado aqui vem da literatura própria: Holm (HOLM, 1979) e FDR (BENJAMINI; HOCHBERG, 1995), na seção 3.7;
- **proporções e tabelas** (BARBETTA; REIS; BORNIA, 2020): IC e testes para proporções e qui-quadrado de aderência e de independência. São usados aqui no equilíbrio do sorteio e das técnicas (2.5.1, 2.5.3), no binomial contra a taxa histórica (2.5.2) e nas tabelas grupo × desfecho (3.2). Para tabelas esparsas e estratificadas, a literatura categórica (AGRESTI, 2007) acrescenta o exato de Fisher e Fisher-Freeman-Halton (acordo na AC, com 17 eventos), Cochran-Mantel-Haenszel (acordo estratificado por mês, 3.6.4) e os IC de Wilson e de Newcombe (NEWCOMBE, 1998);
- **não paramétricos** (SIEGEL; CASTELLAN, 2006):
  - cap. 4 (uma amostra): binomial, qui-quadrado de aderência e **teste de sequências (corridas)**, este para a aleatoriedade do sorteio (3.5.1);
  - cap. 6 (duas amostras independentes): exato de Fisher, mediana, Mann-Whitney e Kolmogorov-Smirnov;
  - cap. 8 (k amostras independentes): extensão do teste da mediana, Kruskal-Wallis com comparações múltiplas e Jonckheere-Terpstra para tendência ordenada (por exemplo, ao longo dos meses);
  - cap. 9 (associação): coeficiente de Cramér, Spearman e Kendall, usados na ordem de chegada (3.5.2);
- **tempos censurados**, que nenhuma das três obras cobre (COLOSIMO; GIOLO, 2006): log-rank e a família ponderada (Wilcoxon-Gehan, Tarone-Ware, Peto-Prentice, Fleming-Harrington), log-rank estratificado, testes em pontos fixos do tempo, diferença de RMST, teste de Grambsch-Therneau para riscos proporcionais e teste de Gray para as funções de incidência acumulada (Parte IV);
- **equivalência**: a alegação de "não haver discrepância" do resumo expandido só se sustentaria com um teste de equivalência (por exemplo, dois testes unilaterais, TOST) contra uma margem fixada **antes** dos dados. O teste não foi executado porque a pergunta já está respondida pelo intervalo: o IC 95% do ΔRMST180 da Remota (1,9 a 19,5 dias) exclui o zero e se estende a quase três semanas. Só uma margem dessa ordem, larga demais para ter sentido de política judiciária, permitiria declarar equivalência;
- **não se aplicam**: McNemar, Wilcoxon pareado, Friedman e Q de Cochran, porque os grupos são independentes (7.2).
''')

code(r'''
quadro_tshn = pd.DataFrame([
    ['Kruskal-Wallis duração × grupo (+ MW post-hoc)', 'H = 1,48; p = 0,478', 'não', 'censurados como completos; "Decisão" como sentença; sem correção (E14, E17)',
     'KM + log-rank; Cox; RMST', 'log-rank χ² = 7,52; p = 0,023; HR Remota 0,81 (0,67–0,97)', '3.4.6; 4.3; 4.5'],
    ['Mann-Whitney Encerrado × Ativo', 'p = 3,2 × 10⁻²⁴', 'não', 'tautológico: ativos têm, por construção, seguimento ≥ 65 dias (E18)',
     'remover', '—', '3.6.1'],
    ['χ² grupo × status', 'p = 0,00015', 'não', 'estar ativo depende do mês de entrada e do seguimento (E19)',
     'situação em horizonte comum (65º dia); KM', 'χ²(8) = 59,19; p < 0,001; V = 0,178', '3.2.5'],
    ['χ² grupo × acordo na AC', 'p = 0,0074', 'não', 'zero estrutural no Controle; esperadas ≈ 5 (E20)',
     'Fisher Presencial × Remota entre AC realizadas', '5,1% × 4,6%; p = 1,000; OR 1,11 (0,37–3,38)', '3.3.1'],
    ['χ² tipo de sentença × grupo', 'p = 2,0 × 10⁻⁶', 'em parte', 'ideia correta, mas inclui "Decisão"; sem resíduos, V nem pares (E21)',
     'χ² sem Decisão, resíduos ajustados, V, Fisher par a par com Holm', 'χ²(4) = 34,34; V = 0,156; sem mérito OR 2,09 e 1,92', '3.2'],
    ['Matriz de Spearman das 4 durações', 'r = 1', 'não', 'quatro cópias da mesma variável (E6, E16)', 'matriz de associação (V, η)', '—', '2.6.4'],
    ['Shapiro-Wilk e D\'Agostino (subamostra de 500)', 'p = 2,6 × 10⁻⁸ / 0,213', 'não', 'subamostra arbitrária; variável censurada; a posteriori (E22)',
     'normalidade por grupo dos sentenciados; diagnóstico de modelos', '17 de 20 testes rejeitam H₀', '2.3'],
    ['z de proporção (p₀ = 0,5) de encerrados', 'z = 17,1', 'não', 'H₀ sem sentido substantivo; depende da data de corte (E23)', 'remover', '—', '3.6.1'],
    ['Mann-Whitney com × sem acordo na AC', 'p = 0,456', 'não', '"sem acordo" inclui o Controle e os ativos (E24)',
     'restringir às AC realizadas; riscos competitivos', 'Md 63 × 104 dias; Cliff d = −0,61 (condicional)', '3.4.6; 4.7'],
    ['Ajuste MLE de distribuições', 'Weibull melhor AIC', 'não', 'censura ignorada; loc livre; zeros descartados (E25)',
     'ajuste com censura; gama generalizada e exponencial por partes', 'risco não monótono; exponencial por partes', '2.4'],
    ['OLS duração ~ grupo; Logit evento ~ grupo', 'p = 0,588; p < 0,001', 'não', 'censura; o evento depende do seguimento (E26)',
     'Cox/AFT; logit em horizonte fixo', 'razão de tempos Weibull Remota 1,21 (1,00–1,45; p = 0,051)', '4.5; 4.6; 5.1; 5.2'],
    ['Kaplan-Meier + log-rank', 'não executado', 'adequado, mas não rodou', 'erro de importação silenciado (E1)',
     'corrigir a importação', 'medianas 81 / 96 / 95 dias', '4.2; 4.3'],
], columns=['Teste do professor', 'Resultado original', 'Adequado?', 'Por quê (código)', 'Alternativa', 'Resultado com a alternativa', 'Seção'])
tabela(quadro_tshn, 'q_testes_professor', 'Avaliação dos testes do notebook do professor: o que muda com o teste adequado',
       secao='7.10', fonte='Elaboração própria; resultados originais do notebook do professor (docs/r2_notebook_professor.md) e das Partes II a V.')
''')

code(r'''
# ---- contraste de apoio: a mediana por grupo depende do tratamento da censura
from lifelines import KaplanMeierFitter
from lifelines.statistics import multivariate_logrank_test
from lifelines.utils import median_survival_times
med = pd.DataFrame(index=ORDEM_GRUPO, dtype=float)
med_ic = {}
for g in ORDEM_GRUPO:
    s = q6[q6['grupo'] == g]
    med.loc[g, 'Ingênua: todos os tempos\n(censura ignorada)'] = s['tempo'].astype(float).median()
    med.loc[g, 'Condicional: só os\nsentenciados'] = s.loc[s['evento'].astype(int) == 1, 'tempo'].astype(float).median()
    kmf = KaplanMeierFitter().fit(s['tempo'].astype(float), s['evento'].astype(int))
    med.loc[g, 'Kaplan-Meier\n(censura respeitada)'] = kmf.median_survival_time_
    med_ic[g] = median_survival_times(kmf.confidence_interval_).to_numpy().ravel()
kw = stats.kruskal(*[q6.loc[q6['grupo'] == g, 'tempo'].astype(float) for g in ORDEM_GRUPO])
lr = multivariate_logrank_test(q6['tempo'].astype(float), q6['grupo'].astype(str), q6['evento'].astype(int))
tab_med = med.T
fig, ax = plt.subplots(figsize=(11, 5.6))
barras_agrupadas(ax, tab_med, cores=CORES_GRUPO, rotular=False, ylabel='Mediana do tempo até a sentença (dias)', legenda=False,
                 quebrar=40)
w_ = 0.8 / 3
for j, g in enumerate(ORDEM_GRUPO):
    for i in range(3):
        xi, vi = i + (j - 1) * w_, tab_med.iloc[i][g]
        topo_ = vi
        if i == 2:
            ax.errorbar(xi, vi, yerr=[[vi - med_ic[g][0]], [med_ic[g][1] - vi]], fmt='none', ecolor=TINTA, elinewidth=1, capsize=4)
            topo_ = med_ic[g][1]
        ax.annotate(fmt_br(vi, 0 if float(vi).is_integer() else 1), (xi, topo_), xytext=(0, 3), textcoords='offset points',
                    ha='center', va='bottom', fontsize=9, color=TINTA)
ax.set_ylim(0, 135)
ax.legend(handles=[mpl.patches.Patch(color=CORES_GRUPO[g], label=rotulo_grupo(g, com_n=True)) for g in ORDEM_GRUPO],
          loc='upper left', frameon=False)
anotar_teste(ax, texto_teste('Kruskal-Wallis do professor (1ª série)', f'H = {fmt_br(kw.statistic, 2)}', kw.pvalue,
                             extra=f'Log-rank (3ª série): χ²(2) = {fmt_br(lr.test_statistic, 2)}; p = {fmt_p(lr.p_value)}'),
             loc='upper right')
ax.set_title('Mediana por grupo em três tratamentos da censura')
figura(fig, 'q_censura_conclusao', 'Ignorar a censura apaga a diferença entre os grupos; respeitá-la revela sentenças '
       'cerca de duas semanas mais tardias nos braços com AC', secao='7.10',
       nota=f'base primária ({len(q6)} processos); barras de erro: IC 95% da mediana de Kaplan-Meier. O Kruskal-Wallis '
            'original (943 linhas) deu H = 1,48 e p = 0,478.')
''')

interp('q_2_11')

# =====================================================================================
md(r'''
## 7.11 Questão 2.12 — Avaliação geral da pesquisa e sugestões de validade


**Avaliação.** A pesquisa tem um mérito raro na pesquisa empírica em Direito no Brasil: é um **experimento**, com sorteio individual, controle contemporâneo e dados primários coletados diariamente na própria unidade, sobre uma questão relevante de política judiciária (a obrigatoriedade da AC inaugural nos JECs). Os dados são **fidedignos**:

- o dígito verificador do número CNJ confere em 100% dos casos, nenhuma sentença precede a distribuição, e acordo e tipo de sentença são coerentes (seção 1.14);
- uma fonte independente, o DataJud, confirma a planilha processo a processo (κ = 0,961 no tipo de desfecho; datas 97,9% iguais; seção 6.3). A ressalva é o atraso de alimentação perto da data de corte.

Os problemas estão no **delineamento da coleta**, pensado para tabelas dinâmicas de acompanhamento, e não para análise estatística:

- a **variável-alvo foi mal definida** (duração dos ativos até `TODAY()`, "Decisão" como sentença), o que fez as médias divulgadas (78,46 e 75,2 dias) misturarem processos encerrados e em curso (seção 2.1.2);
- **faltam as covariáveis** que o próprio projeto previa (tipo de ação, valor da causa, número de partes), as **datas intermediárias** (AC, contestação, conclusão) e o **motivo da extinção** sem mérito;
- o **sorteio** não teve mecanismo documentado nem ocultação (7.1), as **reentradas foram re-sorteadas** e a **conciliadora coincide com a modalidade**;
- **não houve plano de análise**: o projeto previa só estatística descritiva, e o resumo expandido concluiu "não haver discrepância significativa" com base numa amplitude de 2,45 dias, sem teste, sem intervalo e sem considerar a censura.

**A dimensão ético-jurídica não está documentada.** O experimento sorteia o **procedimento** aplicado a partes reais, e não apenas observa autos. Três pontos deveriam constar do projeto:

- **apreciação ética.** Nos documentos analisados não há registro de submissão ao sistema CEP/Conep, de consentimento das partes ou de dispensa justificada do consentimento, como prevê a Resolução CNS nº 510/2016 para pesquisas em ciências humanas e sociais;
- **isonomia.** Partes em situação idêntica receberam ritos diferentes por sorteio. Isso só se justifica se os ritos comparados forem igualmente lícitos e se houver incerteza genuína sobre qual é melhor;
- **base legal do Controle.** A Lei nº 9.099/1995 faz da sessão de conciliação o ato inicial do procedimento (arts. 16 e 21) e admite a forma não presencial (art. 22, § 2º). O "rito atual" do Controle inverte essa regra: não há AC, salvo pedido conjunto das partes. Mesmo o CPC, de aplicação subsidiária, só a dispensa quando ambas as partes manifestam desinteresse (art. 334, § 4º, I). A rigor, o braço que se afasta do modelo legal é o Controle, e não os braços com AC obrigatória, e essa escolha precisava de fundamentação.

**O que os dados, bem analisados, mostram.** A AC obrigatória **não acelerou** os processos:

- **tempo**: a Remota alongou o tempo até a sentença (HR 0,81, IC 0,67–0,97; +10,7 dias de RMST em 180); a Presencial vai na mesma direção, mas sem significância (HR 0,87, IC 0,72–1,04);
- **tipo de sentença**: houve um déficit robusto de julgamentos de mérito e um excesso sugestivo de extinções sem mérito;
- **acordo**: não aumentou **na** audiência (5,1% × 4,6%).

A Parte VIII sintetiza esses achados com as estimativas e os intervalos.

O quadro abaixo avalia o delineamento item a item, no espírito da lista CONSORT, com a sugestão correspondente; as recomendações para a replicação estão consolidadas na seção 8.4.
''')

code(r'''
quadro_aval = pd.DataFrame([
    ['Pergunta e hipóteses', 'parcial', 'hipóteses unilaterais no projeto; nenhum teste previsto; desfecho primário ambíguo',
     'pré-registrar desfecho primário (tempo até a sentença, com censura) e secundários (acordo, tipo de extinção)'],
    ['Geração da sequência de alocação', 'parcial', 'sorteio individual; equilíbrio final improvável (P ≈ 1%) → mecanismo restrito não documentado',
     'lista gerada por terceiro, em blocos permutados estratificados por mês, com semente registrada'],
    ['Ocultação da alocação', 'inadequado', 'sorteio feito no gabinete do juiz-pesquisador, processo a processo', 'central de aleatorização externa ao juízo'],
    ['Unicidade da unidade experimental', 'inadequado', 'reentradas re-sorteadas (A5)', 'regra: reentrada herda o grupo original'],
    ['Elegibilidade', 'parcial', 'redistribuições por prevenção sorteadas (24) e processos de outro órgão (12)', 'triagem de prevenção antes do sorteio'],
    ['Adesão ao tratamento', 'parcial', 'híbridas (28) e AC não realizadas sem motivo registrado', 'registrar comparecimento, formato e motivo da não realização'],
    ['Cegamento', 'inadequado', 'juiz sorteia, julga e analisa', 'análise cega ao grupo; desfecho extraído do PJe por terceiro'],
    ['Condutor da intervenção', 'inadequado', 'uma conciliadora por modalidade', 'rodízio ou várias conciliadoras por braço'],
    ['Medida do desfecho', 'parcial', 'TODAY() nos ativos; datas digitadas, mas confirmadas no DataJud (97,9%; fins de semana reais); 11 ativos já encerrados (atraso de alimentação)', 'extrair datas dos movimentos do PJe/DataJud'],
    ['Covariáveis basais', 'inadequado', 'só a data de distribuição', 'tipo de ação, valor, nº de partes, litigante habitual, advogado'],
    ['Seguimento', 'parcial', '65 a 279 dias; 24,5% sem desfecho', 'seguimento mínimo comum (por exemplo, 180 dias) e análise de sobrevivência'],
    ['Tamanho da amostra e poder', 'inadequado', 'sem cálculo prévio; com as sentenças disponíveis, poder de cerca de 68% para HR = 0,80 (8.4.3)', 'cálculo de poder prévio para o desfecho primário'],
    ['Análise e relato', 'inadequado', 'amplitude de médias sem teste; sem IC', 'plano de análise ITT pré-registrado; relato CONSORT'],
    ['Fidedignidade do registro', 'adequado', 'CNJ 100% válido; 0 incoerências entre acordo e sentença; 0 datas invertidas; DataJud κ = 0,961', 'manter; acrescentar dicionário de dados'],
    ['Aspectos ético-jurídicos', 'inadequado', 'sem registro de CEP, de consentimento ou de dispensa; Controle sem AC inaugural sem fundamentação legal expressa', 'submissão ao sistema CEP/Conep (Res. CNS 510/2016); fundamentar a licitude de cada rito; autorização do tribunal'],
], columns=['Item do delineamento', 'Avaliação', 'Evidência', 'Sugestão para a replicação'])
cores_aval = {'adequado': '#E8F1E4', 'parcial': '#FFF4D6', 'inadequado': '#F9E1DC'}
tabela(quadro_aval, 'q_avaliacao', 'Avaliação do delineamento da coleta: registro fidedigno, mas desenho e plano de análise frágeis',
       secao='7.11', destaque=quadro_aval['Avaliação'].eq('inadequado').to_numpy(),
       nota='linhas destacadas: itens avaliados como inadequados.',
       fonte='Elaboração própria a partir das Partes I a VI; itens inspirados na lista CONSORT (SCHULZ; ALTMAN; MOHER, 2010).')
''')

interp('q_2_12')
