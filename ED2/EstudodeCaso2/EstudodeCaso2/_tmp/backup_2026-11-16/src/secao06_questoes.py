# Parte VI — Respostas às questões 2.2 a 2.12 do roteiro do professor (seções 6.1 a 6.11).
# Executado por build_rafaelcc_ed2.py (exec): usa md(), code() e interp().
# Não refaz as análises das Partes I–V: remete a elas e só faz pequenos cálculos de apoio.

md(r'''
# PARTE VI — RESPOSTAS ÀS QUESTÕES DO PROFESSOR (2.2 A 2.12)

Esta parte responde, uma a uma, às questões 2.2 a 2.12 do roteiro `estudo_de_caso_n_2.md`. Cada resposta (i) resume o enunciado; (ii) argumenta com base nas evidências produzidas nas Partes I a V, às quais remete pela numeração das seções; e (iii) quando útil, traz um quadro ou uma figura próprios. Os poucos cálculos feitos aqui (fluxo dos processos, equilíbrio das variáveis basais, contraste entre medianas ingênuas e de Kaplan-Meier) são **de apoio**: não substituem nem refazem as análises das partes anteriores.

| Questão | Tema | Seção | Evidência principal |
|---|---|---|---|
| 2.2 | EO ou ECA? | 6.1 | 1.10, 1.12, 2.5.1, 3.5 |
| 2.3 | Amostras independentes de uma mesma população? | 6.2 | 2.5.1, 3.5.1, 3.5.3 |
| 2.4 | "Híbrida" e "Decisão" | 6.3 | 1.11, 1.12, 3.2.4, 3.3.4, 4.7, 4.9 |
| 2.5 | Populações e cruzamento com os 14 JECs (DataJud) | 6.4 | Parte VIII |
| 2.6 | Tratamento dos dados brutos | 6.5 | Parte I inteira |
| 2.7 | Matriz de correlações; ordem de chegada × duração | 6.6 | 2.6.4, 2.6.5, 3.5.2, 4.5 |
| 2.8 | Variáveis de confundimento | 6.7 | 3.5.3, 4.3.4, 4.9 |
| 2.9 | Outras variáveis em escala intervalar | 6.8 | 5 (limitação), 2.6.4 |
| 2.10 | Validade interna e externa; generalização | 6.9 | Partes III a V |
| 2.11 | Adequação dos TSHN do professor | 6.10 | 3.4, 3.6, Parte IV |
| 2.12 | Avaliação geral e sugestões | 6.11 | todas; Parte VII |
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
## 6.1 Questão 2.2 — Estudo observacional (EO) ou ensaio controlado aleatorizado (ECA)?

**Enunciado.** Trata-se de um EO ou de um ECA? Qual a diferença entre eles?

**A diferença.** O critério que separa os dois desenhos é **quem atribui a exposição** e **como**. No **estudo observacional**, o pesquisador apenas registra a exposição que as unidades "escolheram" ou receberam por circunstâncias alheias a ele; a comparação entre expostos e não expostos fica sujeita a **confundimento**, porque os grupos podem diferir em fatores que também afetam o desfecho, e a inferência causal exige controlar esses fatores (por ajuste, pareamento ou estratificação), sempre com o risco de confundidores não medidos. No **experimento** (ensaio controlado aleatorizado), o pesquisador **impõe** o tratamento e o faz **por sorteio**, com um grupo de comparação **contemporâneo**; a aleatorização torna os grupos comparáveis **em expectativa** quanto a todos os fatores anteriores à alocação, medidos ou não, e é isso que autoriza ler a diferença dos desfechos como efeito causal do tratamento (MOORE; NOTZ; FLIGNER, 2023, cap. 9, citados no próprio resumo expandido).

**O caso.** O experimento do 4º JEC é um **ECA**, e não um EO, quanto ao rito: cada processo novo foi alocado pelo pesquisador, por sorteio individual, a um de três ritos (rito atual, AC presencial obrigatória ou AC remota obrigatória), e os três grupos correram em paralelo no mesmo período e na mesma unidade. A Parte III não encontrou sinal de alocação não aleatória: o teste de corridas sobre a ordem de chegada não rejeita a aleatoriedade (seção 3.5.1) e a composição por mês, embora desigual em junho e julho, não difere do acaso ao nível de 5% (seção 3.5.3). Com mais precisão, é um **ECA pragmático, de centro único, aberto (sem cegamento), com aleatorização individual e alocação 1:1:1**, cujo sorteio produziu totais **equilibrados demais** para um sorteio simples (seção 2.5.1), o que indica **sorteio com restrição** (lista balanceada, cotas ou compensação). Isso não descaracteriza a aleatorização, mas exige que o mecanismo seja documentado.

Três ressalvas impedem chamá-lo de ECA "puro" em todos os aspectos:

1. **dentro do ECA há componentes observacionais**: a realização da AC, a audiência "híbrida", o acordo e a ausência das partes ocorrem **depois** do sorteio e dependem de escolhas das partes; comparações por essas variáveis (por exemplo, "processos com AC realizada × sem AC") são observacionais (seções 3.2.3 e 4.8);
2. **a unidade judicial não foi sorteada**: o 4º JEC entrou por conveniência (os outros 13 juízes não aderiram); para a população dos 14 JECs, o estudo é um **estudo de caso único** (um conglomerado), e não um ensaio por conglomerados;
3. **o próprio projeto se classifica de forma incoerente**: o resumo expandido fala em "experimento controlado aleatorizado"; o projeto depositado usa a diretriz TREND, destinada a desenhos **não aleatorizados** ("quase experimental"), e chega a falar em "estudo observacional" (ver `docs/r1_documentos.md`, §5). Pelo critério acima, prevalece a classificação de ECA; a diretriz de relato adequada seria a CONSORT, e não a TREND.

O quadro a seguir resume a comparação; o diagrama de fluxo, no formato CONSORT, mostra o percurso dos 944 registros da planilha até os desfechos observados em 07/10/2026.
''')

code(r'''
quadro_eo = pd.DataFrame([
    ['Quem atribui a exposição', 'a própria unidade, as circunstâncias ou terceiros; o pesquisador só observa',
     'o pesquisador, por sorteio', 'o juiz-pesquisador, por sorteio individual de cada processo novo (Chefe de Gabinete, sorteio.com.br)'],
    ['Grupo de comparação', 'expostos × não expostos, às vezes históricos', 'contemporâneo, formado pelo mesmo sorteio',
     'contemporâneo: rito atual (Controle), sorteado junto com os dois braços de AC'],
    ['Comparabilidade dos grupos', 'não garantida; depende de ajuste por confundidores medidos',
     'garantida em expectativa para todos os fatores anteriores ao sorteio', 'grupos de 313/314/311; mês e dia da semana compatíveis com o acaso (6.2)'],
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
       secao='6.1', fonte='Elaboração própria a partir do projeto de pesquisa, do resumo expandido e das Partes I a III.')
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
       secao='6.1', nota='formato CONSORT; "AC não realizada" = técnica registrada como "**" (extinção anterior à audiência, ausência '
                         'ou outro motivo, não registrado na planilha); '
                         'híbrida = AC pautada como presencial com participação remota de uma das partes.')
''')

interp('q_2_2')

# =====================================================================================
md(r'''
## 6.2 Questão 2.3 — Os três grupos são amostras independentes de uma mesma população?

**Enunciado.** Decidir, justificadamente, se Controle, AC presencial e AC remota são amostras **independentes** extraídas de uma mesma população, e se isso influi na escolha dos testes.

**Resposta.** Sim, com uma precisão de linguagem e três ressalvas.

*Precisão.* Os grupos não são "amostras extraídas" de uma população por **amostragem probabilística**: são uma **partição aleatória** de um único conjunto, o fluxo de ações distribuídas ao 4º JEC entre 01/01 e 03/08/2026 (praticamente um censo da população disponível; ver 6.4). A "mesma população" é garantida pelo **sorteio**: antes da alocação, cada processo tinha a mesma chance de cair em qualquer grupo, de modo que os três grupos são, em expectativa, idênticos em tudo o que existia antes do sorteio. A base lógica da inferência é, portanto, a **aleatorização** (o que justifica testes de permutação e a interpretação dos testes clássicos como aproximações deles), e não a amostragem de uma população infinita.

*Independência.* Os grupos são **independentes entre si**: cada processo pertence a um só grupo (as reentradas re-sorteadas foram reconduzidas ao primeiro sorteio, A5, seção 1.10), e não há pareamento nem medidas repetidas da mesma unidade em grupos diferentes. A única verificação empírica possível, dado que a planilha não tem covariáveis do processo, é o equilíbrio das variáveis **basais de calendário**: o quadro e a figura abaixo testam mês e dia da semana da distribuição e a origem externa do processo.

*Ressalvas.* (i) **Dependência por agentes comuns**: o mesmo juiz, o mesmo cartório e a **mesma conciliadora em cada braço** atendem todos os processos de um grupo, o que cria correlação intragrupo (agrupamento) que os testes clássicos ignoram e que, no caso da conciliadora, não pode ser corrigida, porque ela coincide com a modalidade (6.7); (ii) **litigantes habituais** (bancos, operadoras) aparecem nos três grupos e podem induzir correlação entre processos, sem que a planilha permita identificá-los; (iii) o **sorteio restrito** (totais fixados ou compensados) cria uma dependência fraca entre as alocações, que torna os testes clássicos levemente conservadores e recomenda estratificar pelo período (seções 2.5.1 e 4.3.4).

*Influência sobre os testes.* Decisiva. Amostras independentes exigem testes para **k amostras independentes**: χ² de independência ou exato de Fisher para proporções; Kruskal-Wallis, Mann-Whitney e Dunn para posições; log-rank e Cox para tempos censurados. Os testes para amostras **dependentes** (McNemar, Wilcoxon pareado, Friedman, Q de Cochran) não se aplicam (seção 3.6.3). Além da independência, a **censura** e a natureza **nominal** de quase todas as variáveis pesam tanto quanto ela: é a censura que desloca a escolha do Kruskal-Wallis para o log-rank (6.10).
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
       secao='6.2', formatos={'gl': 'int', 'Categorias': 'int', 'Menor esperada': 1, 'χ²': 2, 'V de Cramér': 3},
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
fig.legend(handles=[mpl.patches.Patch(color=CORES_GRUPO[g], label=rotulo_grupo(g, com_n=True)) for g in ORDEM_GRUPO],
           loc='lower center', bbox_to_anchor=(0.5, -0.03), ncol=3, frameon=False)
fig.tight_layout(rect=(0, 0.04, 1, 1))
figura(fig, 'q_equilibrio_basal', 'As variáveis basais estão equilibradas entre os grupos; o desequilíbrio acumulado foi compensado no fim',
       secao='6.2', nota='painéis (a) a (c): % dentro de cada grupo; painel (d): diferença entre o maior e o menor grupo '
                         'acumulado após cada processo (descritivo; o teste do equilíbrio final está na seção 2.5.1).')
''')

interp('q_2_3')

# =====================================================================================
md(r'''
## 6.3 Questão 2.4 — O que significam "híbrida" e "Decisão"?

**Enunciado.** O que significa a variável `híbrida` (Sim/Não), à luz da explicação do pesquisador (AC presencial em que uma das partes pediu para participar remotamente, deferida com base na Res. CNJ 481)? E o que significa o registro "Decisão" na coluna `sentença/decisão` (remessa do processo a outro juízo, por prevenção)?

**"Híbrida".** É uma **AC pautada como presencial** em que ao menos uma das partes participou por videoconferência, a pedido próprio, deferido pelo juiz. Estatisticamente, é uma **não adesão parcial ao tratamento sorteado** (*crossover* parcial do braço presencial em direção ao remoto), decidida pela parte **depois** do sorteio. Três consequências:

1. **não é tratamento aleatorizado**: quem pede para participar remotamente pode diferir de quem comparece (distância, trabalho, representação por advogado, interesse em acordo); a comparação "híbrida × presencial pura" é observacional e não testa a hipótese H4 do projeto ("presencial mais efetiva que a híbrida") de forma causal;
2. **na análise principal (intenção de tratar, ITT)** as híbridas permanecem no grupo sorteado (Presencial); a análise "conforme tratado", que as move para a Remota, é **sensibilidade** (seção 4.9);
3. **o "Não" tem dois sentidos**: no Controle, onde não há AC, o "Não" é um **zero estrutural** ("não se aplica"); nos braços com AC, é "audiência integralmente na modalidade pautada". Há, além disso, três "Sim" no grupo **Remota** (A12), incoerentes com a definição (uma audiência pautada como remota não pode ser "híbrida" nesse sentido), e três "Sim" na Presencial com técnica `**`, isto é, sem AC realizada (A13): ambos foram mantidos e sinalizados como desvio de protocolo (seção 1.12).

**"Decisão".** Não é sentença nem resolução do conflito: é a **remessa do processo a outro juízo** para redistribuição, porque um juízo anterior estava **prevento** (CPC, arts. 59 e 286). O processo **sai do 4º JEC** e nunca terá sentença ali. Tratar a "Decisão" como "encerramento" (o notebook do professor a conta como evento, E10) mistura um desfecho administrativo, de mediana de 1 dia, com o tempo até a sentença. Neste notebook, a redistribuição é (i) **risco competitivo** da sentença (Aalen-Johansen e Fine-Gray, seção 4.7), (ii) censura na análise causa-específica (Cox, 4.5) e (iii) excluída ou tratada como evento nas análises de sensibilidade (4.9). Como ela ocorre quase sempre **antes** da AC, é também, na prática, uma **inelegibilidade descoberta depois do sorteio**; e o processo que voltou ao 4º JEC foi **sorteado de novo** (A5), uma falha de protocolo corrigida na curadoria (o processo conserva o grupo do primeiro sorteio).

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
     'não altera: HR da Remota 0,79 a 0,82 em todos os cenários (4.9); acordo 1/24 × 8/154, Fisher p = 1,000'],
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
     'não altera (cenário "com as duplicatas", 4.9)'],
], columns=['Registro', 'Significado', 'Natureza no desenho', 'Contagem (base primária)', 'Tratamento neste notebook',
            'Efeito sobre a conclusão'])
tabela(quadro_hd, 'q_hibrida_decisao', '"Híbrida" é não adesão parcial ao rito; "Decisão" é saída do estudo por redistribuição',
       secao='6.3', fonte='Elaboração própria; contagens da base primária (938 processos); efeitos conforme as Partes III e IV.')
''')

interp('q_2_4')

# =====================================================================================
md(r'''
## 6.4 Questão 2.5 — Populações de interesse, disponível e amostrada; cruzamento com os 14 JECs

**Enunciado.** Descrever a população de interesse, a disponível e a amostrada; dizer como ampliar o cruzamento do tempo da distribuição até a sentença aos 14 JECs de Natal no mesmo período (2/1/2026 a 3/8/2026) e se há dados disponíveis no CNJ.

**As três populações.** A distinção é a de toda pesquisa por amostragem: a **população de interesse** (ou alvo) é aquela sobre a qual se quer concluir; a **disponível** (acessível) é a parte dela a que o pesquisador tem acesso; a **amostrada** é o que efetivamente entrou na base. A inferência estatística vai da amostrada à disponível; a passagem da disponível à de interesse é **extrapolação**, que depende de argumento substantivo, não de cálculo.

- **De interesse.** As ações de conhecimento do procedimento do Juizado Especial Cível (classe CNJ 436) distribuídas aos **14 JECs cíveis de Natal** no período do experimento, e, num sentido mais amplo e implícito no projeto (que pretende avaliar a política nacional de conciliação), as ações dos JECs cíveis em geral sob a alternativa "AC obrigatória × rito sem AC inaugural".
- **Disponível.** As ações distribuídas ao **4º JEC** de Natal entre 01/01 e 03/08/2026: a única unidade cujo juiz aceitou o experimento. Note-se que o período informado na questão (2/1/2026) difere do observado na planilha: o primeiro processo foi distribuído em **01/01/2026** (seção 1.13).
- **Amostrada.** Os **943** processos sorteados (944 linhas), reduzidos a **938** processos distintos na base primária (seção 1.10), observados até a atualização de **07/10/2026**: 708 com sentença, 24 redistribuídos e 206 ainda em tramitação (censurados). Em relação à disponível, é praticamente um **censo**; em relação à de interesse, é **um conglomerado escolhido por conveniência**, e não uma amostra probabilística dos 14 JECs.

**Como ampliar aos 14 JECs: o DataJud.** Há dados públicos no CNJ. A **API Pública do DataJud** expõe, para cada tribunal, os metadados e os **movimentos processuais** codificados pelas Tabelas Processuais Unificadas (TPU): data de ajuizamento, classe, órgão julgador e cada movimento com data e hora (distribuição, audiência, homologação de acordo, julgamento com ou sem resolução do mérito, redistribuição). Para o TJRN, o endpoint é `api_publica_tjrn`; o filtro natural é **classe 436**, **órgão julgador** (o 4º JEC tem o código **13285**; os demais 13 JECs de Natal têm códigos próprios) e data de ajuizamento entre 01/01 e 03/08/2026. Com isso se reconstrói, para os 14 JECs, o tempo da distribuição até o primeiro julgamento, com a mesma regra de censura usada aqui. O vínculo com a planilha é **exato**, porque o número CNJ é identificador único com dígito verificador (940 de 940 válidos, seção 1.9).

**Limites.** A API pública **não traz as partes, o valor da causa, o advogado nem o magistrado**; os movimentos dependem da qualidade do lançamento em cada vara (códigos genéricos, lançamentos em lote); e o índice é atualizado com defasagem. O DataJud permite, portanto, comparar **tempos e tipos de desfecho** entre unidades, mas não fornece as covariáveis que faltam ao experimento (6.8). A etapa de coleta está em curso: até o momento, 199 de 200 números da planilha consultados foram encontrados na API do TJRN, mas a coleta completa está limitada pela sobrecarga da API do CNJ; os números serão apresentados na **Parte VIII**. O que se pode e o que não se pode concluir com a comparação entre JECs está em 6.9.
''')

code(r'''
quadro_pop = pd.DataFrame([
    ['De interesse (alvo)', 'ações do procedimento do JEC cível (classe 436) dos 14 JECs de Natal, 01/01 a 03/08/2026; '
     'em sentido amplo, JECs cíveis sob a política de conciliação do CNJ', 'desconhecido na planilha; estimável pelo DataJud (Parte VIII)',
     'extrapolação: exige argumento substantivo ou replicação (6.9)'],
    ['Disponível (acessível)', 'ações distribuídas ao 4º JEC de Natal, 01/01 a 03/08/2026',
     '943 sorteadas (resumo expandido); 944 linhas na planilha', 'unidade única, escolhida por conveniência'],
    ['Amostrada (analisada)', 'processos distintos da planilha, observados até 07/10/2026',
     f'{len(q6)} processos: {int(q6.evento.astype(int).sum())} sentenças, {int((q6.desfecho == "Redistribuição").sum())} redistribuições, '
     f'{int((q6.desfecho == "Ativo").sum())} censurados', 'censo da disponível; inferência por aleatorização válida para o 4º JEC'],
], columns=['População', 'Definição', 'Tamanho e fonte', 'Alcance da inferência'])
tabela(quadro_pop, 'q_populacoes', 'Populações de interesse, disponível e amostrada', secao='6.4',
       fonte='Elaboração própria a partir do projeto de pesquisa, do resumo expandido e da Parte I.')

quadro_dj = pd.DataFrame([
    ['Número CNJ', 'sim', 'sim', 'vínculo exato planilha × DataJud (validação das datas e desfechos)'],
    ['Data de distribuição / ajuizamento', 'sim', 'sim (dataAjuizamento; movimento de distribuição)', 'origem do tempo'],
    ['Data e tipo da sentença', 'sim (digitado; 18% em fim de semana, A16)', 'sim (movimentos TPU com data e hora)',
     'conferir a data da sentença e o tipo de extinção'],
    ['Redistribuição', 'sim ("Decisão")', 'sim (movimento de redistribuição)', 'risco competitivo nos 14 JECs'],
    ['Audiência de conciliação (data, realização)', 'não (só a técnica)', 'sim, quando lançada (movimentos de audiência)',
     'decompor o tempo em etapas (pauta, AC, sentença)'],
    ['Grupo do experimento, técnica, híbrida', 'sim', 'não', 'só existem na planilha'],
    ['Partes, polo passivo, litigante habitual', 'não', 'não (dados de partes fora da API pública)', 'covariável faltante (6.8)'],
    ['Valor da causa, assunto', 'não', 'assunto sim (TPU); valor da causa não', 'assunto como covariável basal'],
    ['Magistrado, advogado', 'não', 'não', 'efeito de juiz só por órgão julgador'],
], columns=['Informação', 'Planilha do experimento', 'DataJud (API pública)', 'Uso no estudo'])
tabela(quadro_dj, 'q_datajud', 'O que o DataJud acrescenta à planilha e o que continua faltando', secao='6.4',
       fonte='Elaboração própria a partir da documentação da API Pública do DataJud (CNJ) e da Parte I.')
''')

interp('q_2_5')

# =====================================================================================
md(r'''
## 6.5 Questão 2.6 — O tratamento dos dados brutos no notebook do professor foi adequado?

**Enunciado.** O tratamento das variáveis no notebook `estcaso_4jec_natal_rn.ipynb` foi adequado? Pode ser complementado? Como?

**Resposta.** **Não foi adequado**, e o problema central não é de limpeza cosmética, mas de **definição da variável-alvo**. O notebook lê corretamente a planilha e faz uma auditoria inicial útil (duplicatas, faltantes, conferência data × duração), mas não age sobre o que encontra e deixa de tratar o que determina todas as análises seguintes:

1. **a data de referência dos processos ativos é `TODAY()`** (fórmula volátil da planilha): os 209 ativos têm duração calculada até o dia em que o arquivo foi aberto, e o notebook os trata como tempos completos (E7, E14; A1). Aqui, a censura foi fixada em **07/10/2026** e o tempo recalculado a partir das datas (seção 1.4);
2. **a "Decisão" é contada como encerramento** (E10), quando é redistribuição (6.3);
3. **duplicatas e reentradas** são detectadas e mantidas (E3): duas linhas vazias criariam falsos censurados e três reentradas foram re-sorteadas, uma delas para outro grupo (A3–A5, seção 1.10);
4. **o marcador `**` e as ausências estruturais** são tratados como categoria ou como "Não" (E4, E5): no Controle, "acordo na AC = Não" e "técnica = `**`" significam "não se aplica" (seção 1.7);
5. **as quatro colunas de duração são a mesma variável** (E6, A17), o que contamina a matriz de correlações (6.6);
6. a linha sem fórmulas (A2), as grafias variantes (A6), os números CNJ com espaço, hífen ou órgão truncado (A7, A8), os processos vindos de outro órgão (A9) e os desvios de protocolo da híbrida (A12, A13) não são tratados.

**Como complementar.** O tratamento feito na Parte I responde a cada item com uma regra explícita, registrada no **log de tratamentos** (seção 1.15) e no **dicionário de variáveis** (seção 1.16), sem imputar nenhuma data ou duração; o quadro abaixo emparelha cada problema com a solução. Faltam, e só podem vir de fora da planilha: (i) a **validação das datas de sentença** (18,4% caem em sábado ou domingo, A16; seção 2.5.4) contra os movimentos do PJe/DataJud; (ii) o **motivo da extinção sem mérito** (ausência do autor, desistência, indeferimento), que explicaria o principal achado do experimento (6.7); (iii) a **data da AC** e as demais datas intermediárias; e (iv) as **covariáveis previstas no projeto** e não coletadas (tipo de ação, valor da causa, número de partes).
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
    ['A16', 'não examinado', 'flag sentenca_fim_semana; sensibilidade; validar no DataJud', '2.5.4, 4.9'],
    ['—', 'sem dicionário nem registro das decisões', 'log de tratamentos e dicionário exportados', '1.15, 1.16'],
], columns=['Código', 'No notebook do professor', 'Tratamento neste notebook', 'Seção'])
tabela(quadro_trat, 'q_tratamento', 'Tratamento dos dados brutos: o que o notebook do professor deixou de fazer e como foi feito aqui',
       secao='6.5', fonte='Elaboração própria; códigos E1–E30 de docs/r2_notebook_professor.md e A1–A20 de docs/r3_auditoria_dados.md.')
''')

interp('q_2_6')

# =====================================================================================
md(r'''
## 6.6 Questão 2.7 — A matriz de correlações é adequada? Ordem de chegada × duração

**Enunciado.** A matriz de correlações inicial do notebook do professor é adequada? Com a informação de que o sorteio seguiu rigorosamente a ordem de chegada dos processos, é possível investigar a correlação entre essa ordem e `duracao_proc`?

**A matriz não é adequada**, por três razões, cada uma suficiente:

1. **é tautológica**: as quatro colunas correlacionadas (`DURAÇÃO-SENT2`, `-SORT`, `-PROC`, `-TECN`) são **a mesma fórmula** da planilha, apenas filtrada para as tabelas dinâmicas; as três primeiras coincidem em 943 de 943 linhas e a quarta nas 428 em que existe. O r = 1 em todas as células (e o R² = 1 das dispersões) é identidade aritmética, não achado (E6, E16; seção 2.6.4);
2. **não há outra variável quantitativa** na planilha: as demais (grupo, híbrida, acordo, técnica, tipo de sentença) são **nominais**, para as quais a medida de associação adequada é o V de Cramér (ou o φ), e entre uma nominal e o tempo, a razão de correlação η ou, melhor, um modelo de sobrevivência. A seção 2.6.4 substitui a matriz do professor por uma **matriz de associação** com essas medidas;
3. **ignora a censura**: um quarto dos tempos é limite inferior (processos ainda ativos), e qualquer correlação calculada sobre eles mistura duração com tempo de seguimento.

**A ordem de chegada pode ser investigada, mas não pela correlação bruta.** A ordem é uma variável **ordinal** (equivalente à data de distribuição), o que admite Spearman ou Kendall, nunca Pearson sobre códigos. O obstáculo é estrutural: como todos os processos foram observados até a mesma data (07/10/2026), **quanto mais tarde o processo chegou, menor o seguimento máximo possível** (correlação de −1 entre ordem e seguimento). Um processo de julho só aparece como "sentenciado" se for rápido; um de janeiro pode aparecer com 200 dias. Isso produz uma correlação **negativa artificial** entre ordem e tempo, mesmo que não haja nenhuma relação real. A Parte III mediu esse artefato por simulação (tempos gerados independentemente da ordem e censurados pelo seguimento real de cada processo; seção 3.5.2): a figura abaixo compara o ρ observado com o intervalo que a censura sozinha produziria. Na **janela comum** de 65 dias (o seguimento mínimo, observado sem censura para todos), o sinal se **inverte**.

A forma correta de responder à pergunta substantiva ("o tempo até a sentença mudou ao longo do experimento?") é incluir o mês ou a ordem como **covariável num modelo de sobrevivência**. O Cox da seção 4.5 mostra razões de risco decrescentes com o mês (junho 0,70; julho-agosto 0,58, contra janeiro), e o AFT log-normal da seção 5.1.3 estima que o tempo típico até a sentença **aumentou cerca de 20% a cada mês** de distribuição: um **acúmulo de acervo** ao longo do experimento que a correlação bruta apresentava com o sinal trocado. A ordem de chegada serviu, ainda, para testar a aleatoriedade do sorteio (teste de corridas, seção 3.5.1).
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
           'e, na janela comum, positiva: os processos que chegaram depois demoram mais', secao='6.6',
           nota='simulação da seção 3.5.2: 500 réplicas de tempos Weibull independentes da ordem, censurados pelo seguimento '
                'real de cada processo; janela comum = tempo truncado em 65 dias, sem redistribuídos.')
''')

interp('q_2_7')

# =====================================================================================
md(r'''
## 6.7 Questão 2.8 — Variáveis de confundimento

**Enunciado.** Refletir sobre possíveis variáveis de confundimento, apresentá-las em quadro com os seus efeitos possíveis e dizer se foram ou não controladas pelo desenho.

**Conceito.** Um **confundidor** é uma variável associada ao mesmo tempo à exposição e ao desfecho, sem estar no caminho causal entre eles; se não for controlado, a diferença observada entre os grupos mistura o efeito do tratamento com o efeito dele. É preciso distingui-lo do **mediador** (a variável pela qual o tratamento age, como a fila da pauta da AC ou a ausência do autor à audiência) e do **modificador de efeito** (a variável que muda o tamanho do efeito, como o perfil da unidade).

**O que o sorteio controla e o que não controla.** A aleatorização individual controla, **em expectativa**, todos os fatores **do processo** anteriores ao sorteio: tipo de ação, valor da causa, número de partes, litigante habitual, presença de advogado. Esse é o grande mérito do desenho, e é por isso que a falta dessas variáveis na planilha não enviesa a comparação entre grupos (embora impeça verificar o equilíbrio e reduza a precisão). O sorteio **não controla** três famílias de fatores:

- os que estão **amarrados ao braço** pelo próprio protocolo: a conciliadora (CEJUSC na presencial, gabinete na remota) é **a mesma para todos os processos de cada braço**, de modo que o "efeito da modalidade" e o "efeito da conciliadora" são indissociáveis (a hipótese H5 do projeto é inestimável);
- os que **agem sobre todos os grupos** de forma possivelmente diferencial e não são cegos: o juiz-pesquisador que sorteia, julga e analisa; a reatividade da equipe (Hawthorne); a contaminação entre grupos (mesmo cartório e mesma equipe);
- os que **variam no tempo** e se combinam com a composição dos grupos: o mês de distribuição (junho com excesso de Presencial e julho de Remota, resíduos ajustados 2,95 e 3,10; seção 3.5.3), que também determina o seguimento e coincide com um acúmulo de acervo (6.6). Este foi **controlado na análise**, por estratificação (log-rank estratificado, Cox com estrato por mês; seções 4.3.4 e 4.5), e a conclusão se manteve.

O quadro a seguir organiza os candidatos, com o efeito provável, a direção do viés e o que o desenho ou a análise fez a respeito.
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
     'não', 'comparar o 4º JEC antes (2025) e durante (2026) com os outros 13 JECs (6.9)'],
    ['Contaminação entre grupos', 'mesmo cartório, mesma equipe e mesmas práticas nos três ritos',
     'práticas da AC vazam para o Controle', 'para zero (subestima diferenças)', 'não', 'ensaio por conglomerados (unidades sorteadas)'],
    ['Mês de distribuição / acúmulo de acervo', 'composição dos grupos varia por mês; tempo cresce ~20% por mês',
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
    ['Data da sentença registrada', '18,4% em fim de semana; possível data de lançamento', 'erro de medida do tempo',
     'não diferencial (sem efeito na conclusão, 4.9)', 'não', 'conferir no PJe/DataJud (Parte VIII)'],
    ['Redistribuição por prevenção', 'saída do estudo antes da sentença', 'remove casos do risco', 'nenhuma (igual entre grupos, p = 0,393)',
     'sim, na análise (risco competitivo)', 'triagem de prevenção antes do sorteio'],
], columns=['Variável', 'Mecanismo', 'Efeito provável', 'Direção do viés', 'Controlada pelo desenho?', 'Como controlar'])
tabela(quadro_conf, 'q_confundidores', 'Variáveis de confundimento, mediadores e ameaças: efeito provável e controle pelo desenho',
       secao='6.7', fonte='Elaboração própria a partir do projeto de pesquisa, do texto antagonista (ODT) e das Partes II a IV.')
''')

interp('q_2_8')

# =====================================================================================
md(r'''
## 6.8 Questão 2.9 — Outras variáveis quantitativas em escala intervalar

**Enunciado.** Seria possível extrair outra variável quantitativa intervalar (discreta ou contínua), como o número de autores e réus ou o número de atos da serventia e do juiz, com datas e durações, para correlacionar com `duracao_proc`? Que correlação e que teste usar?

**Sim, e elas fariam falta.** Nenhuma variável quantitativa além do tempo existe na planilha (a Parte V é limitada por isso). Do PJe e, em parte, do DataJud podem ser extraídas variáveis de dois tipos, que precisam ser separadas porque respondem a perguntas diferentes:

- **basais (anteriores ao sorteio)**: número de autores e de réus, valor da causa, número de pedidos, presença de pessoa jurídica no polo passivo; servem como **covariáveis** (verificar o equilíbrio do sorteio e ganhar precisão nos modelos);
- **de processo (posteriores ao sorteio)**: número de atos da serventia e do juiz, número de petições, número de remarcações da AC, dias até a citação, dias até a AC, dias da AC à conclusão e da conclusão à sentença; são **mediadores** e componentes do próprio tempo. O número de atos, em particular, cresce **mecanicamente** com a duração (processo mais longo acumula mais atos): uma correlação alta entre eles nada diz sobre causa e, se usado como preditor da duração, produz viés de tempo imortal. Para esse tipo de variável, a medida útil é a **taxa** (atos por 30 dias) ou a **decomposição do tempo em etapas**.

Rigorosamente, contagens e valores monetários estão em **escala de razão** (zero absoluto), que contém as propriedades da intervalar; o que importa para a escolha da medida é que são **quantitativas**, em geral **assimétricas** e, nas contagens, com **muitos empates**.

**Que correlação e que teste.** Para duas variáveis quantitativas **sem censura**:

- **Pearson** (r) mede associação **linear** e, para inferência, supõe normalidade bivariada ou n grande; teste de H₀: ρ = 0 por t = r√(n − 2)/√(1 − r²), com n − 2 graus de liberdade. É pouco indicado aqui: tempos e contagens são assimétricos e a relação raramente é linear;
- **Spearman** (ρ_s) mede associação **monotônica** sobre os postos; teste pela mesma aproximação t ou, em amostras pequenas, pela distribuição exata ou por permutação (SIEGEL; CASTELLAN, 2006);
- **Kendall** (τ_b) é preferível com **muitos empates** (contagens pequenas, como número de réus) e tem interpretação direta (diferença entre as probabilidades de pares concordantes e discordantes); teste por aproximação normal ou permutação.

**Com censura**, nenhuma dessas correlações vale para o tempo (6.6). A medida adequada é a **razão de riscos por unidade da covariável** num modelo de Cox (testes de Wald, razão de verossimilhanças ou escore; COLOSIMO; GIOLO, 2006, cap. 5), a **razão de tempos** num AFT, ou o **índice de concordância C de Harrell**, que generaliza o τ de Kendall a dados censurados. A forma funcional da covariável contínua se verifica pelos **resíduos martingal** (seção 4.5.4).
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
       secao='6.8', fonte='Elaboração própria; SIEGEL; CASTELLAN (2006); COLOSIMO; GIOLO (2006).')
''')

interp('q_2_9')

# =====================================================================================
md(r'''
## 6.9 Questão 2.10 — Validade interna e externa; generalização aos 14 JECs

**Enunciado.** Considerando a validade interna e a externa, seria possível generalizar os resultados para toda a população dos 14 JECs de Natal no mesmo período?

**Validade interna: razoável para o efeito do rito no 4º JEC.** A validade interna pergunta se a diferença observada entre os grupos pode ser atribuída ao tratamento. Aqui, os pontos fortes são reais: alocação por sorteio individual, grupos contemporâneos e de mesmo tamanho, equilíbrio das variáveis basais disponíveis (6.2), análise por intenção de tratar, e tratamento correto da censura e dos riscos competitivos (Parte IV). As conclusões principais resistiram a doze cenários de sensibilidade (seção 4.9). As ameaças que permanecem são as do quadro de 6.7: a conciliadora confundida com a modalidade (o que compromete só a comparação Presencial × Remota, não a comparação de cada braço com o Controle), o juiz-pesquisador não cego, a reatividade e a contaminação; e o seguimento curto (mínimo de 65 dias), que deixa um quarto dos processos sem desfecho.

**Validade externa: não há base estatística para generalizar aos 14 JECs.** A validade externa pergunta se o efeito estimado vale para outras unidades, pessoas e momentos. O estudo tem **uma só unidade**, escolhida por conveniência: no nível em que a política seria adotada (a serventia), N = 1. Há aqui uma distinção importante. Como a distribuição entre os 14 JECs é aleatória e alternada pelo PJe (CPC, art. 285), os **processos** que chegam ao 4º JEC são, em expectativa, parecidos com os que chegam aos demais; o que **não** é representativo é a **unidade**: o juiz (que é o pesquisador), as duas conciliadoras, o cartório, a pauta e a cultura conciliatória. Se o efeito da AC obrigatória depende dessas características (e é plausível que dependa: o acordo depende da conciliadora; o tempo, da pauta e do gabinete), o efeito do 4º JEC não se transporta automaticamente aos demais. A premissa de que os 14 JECs são "conglomerados homogêneos" é uma **hipótese não testada**, e mesmo uma homogeneidade de perfil das ações não garantiria homogeneidade de efeito. A generalização possível é **analítica** (o mecanismo encontrado, como a extinção por ausência do autor à AC obrigatória, deve operar em outras unidades), não estatística.

**O que se pode fazer com os dados disponíveis (recorte adotado).** O DataJud (6.4; Parte VIII) permite duas comparações **observacionais** no nível da unidade, que medem o **efeito do experimento sobre o 4º JEC**, e não o efeito do rito (que só o sorteio interno identifica):

1. **4º JEC antes × durante**: processos distribuídos em 2025 (antes do experimento) × 2026 (durante), com o mesmo tratamento da censura;
2. **4º JEC × os outros 13 JECs de Natal**, no mesmo período: um desenho de **diferenças em diferenças** (antes/durante × 4º JEC/demais) que separa a mudança do 4º JEC da tendência comum da capital, e que é a melhor forma disponível de avaliar a reatividade e o acúmulo de acervo observado (6.6).

**Outra comarca ou outro estado** ficam como **trabalhos futuros**: ali a validade externa exige **replicar o experimento** (sortear os ritos em outras unidades), e não comparar tempos observacionalmente, porque unidades diferentes diferem em tudo o que o sorteio interno controlava.
''')

code(r'''
quadro_val = pd.DataFrame([
    ['Alocação por sorteio individual e controle contemporâneo', 'interna', 'favorece', 'efeito causal do rito no 4º JEC (ITT)'],
    ['Censura e riscos competitivos tratados (Parte IV)', 'interna / estatística', 'favorece', 'estimativas não enviesadas pelo seguimento'],
    ['Conciliadora confundida com a modalidade', 'interna', 'ameaça', 'Presencial × Remota não separa modalidade de pessoa'],
    ['Juiz-pesquisador não cego; reatividade (Hawthorne)', 'interna / constructo', 'ameaça', 'possível ritmo diferencial; não verificável'],
    ['Contaminação entre grupos', 'interna', 'ameaça', 'tende a subestimar diferenças'],
    ['Seguimento curto (65 a 279 dias) e 24,5% sem desfecho', 'estatística', 'ameaça (tratada)', 'cauda da distribuição não estimável; usar RMST'],
    ['Unidade única, escolhida por conveniência (N = 1)', 'externa', 'ameaça grave', 'sem inferência estatística para os 14 JECs'],
    ['Distribuição aleatória entre os 14 JECs (art. 285 do CPC)', 'externa', 'favorece parcialmente', 'perfil dos processos semelhante em expectativa'],
    ['Efeito dependente de juiz, conciliadoras, pauta e cultura', 'externa', 'ameaça', 'efeito pode não se transportar a outra unidade'],
    ['Período de 7 meses de 2026', 'externa (tempo)', 'ameaça', 'sazonalidade e acúmulo de acervo específicos'],
], columns=['Aspecto', 'Tipo de validade', 'Efeito', 'Consequência'])
tabela(quadro_val, 'q_validade', 'Validade interna razoável no 4º JEC; validade externa sem base estatística para os 14 JECs',
       secao='6.9', fonte='Elaboração própria a partir das Partes II a V e do texto antagonista (ODT).')

quadro_cmp = pd.DataFrame([
    ['Sorteio interno (este notebook)', 'efeito do rito sobre o tempo e o acordo no 4º JEC', 'KM, log-rank, Cox, RMST, riscos competitivos',
     'planilha (938)', 'feito (Partes III a V)'],
    ['4º JEC antes (2025) × durante (2026)', 'o experimento mudou o tempo da unidade?', 'KM/Cox por período (série interrompida)',
     'DataJud', 'recorte adotado (Parte VIII)'],
    ['4º JEC × outros 13 JECs de Natal, antes e durante', 'efeito do experimento além da tendência da capital',
     'diferenças em diferenças com Cox estratificado por juizado', 'DataJud', 'recorte adotado (Parte VIII)'],
    ['Outra comarca ou estado', 'o efeito do rito se transporta?', 'replicação do ECA (multicêntrico, por conglomerados)',
     'nova coleta primária', 'trabalho futuro'],
], columns=['Comparação', 'Pergunta', 'Método', 'Dados', 'Situação'])
tabela(quadro_cmp, 'q_comparacoes', 'Comparações possíveis: só o sorteio interno identifica o efeito do rito',
       secao='6.9', fonte='Elaboração própria.')
''')

interp('q_2_10')

# =====================================================================================
md(r'''
## 6.10 Questão 2.11 — Os testes de significância do notebook do professor foram adequados?

**Enunciado.** Todos os testes de significância contra a hipótese nula (TSHN) do notebook foram adequados? Que outros testes poderiam ser aplicados (BECKER, 2015; BARBETTA; REIS; BORNIA, 2020; SIEGEL; CASTELLAN, 2006)?

**Resposta.** **Não.** Um teste é adequado quando (i) a hipótese nula responde a uma pergunta substantiva, (ii) os pressupostos valem para os dados e (iii) o resultado vem acompanhado de tamanho de efeito, intervalo de confiança e controle de multiplicidade. O notebook do professor falha no primeiro critério em quatro testes (tautológicos ou sem sentido), no segundo em quase todos (sobretudo pela **censura**) e no terceiro em todos (E27). O quadro a seguir avalia cada teste; a Parte III reproduziu os testes problemáticos na base primária (seção 3.6.1) e a Parte IV aplicou os métodos adequados a dados censurados.

O caso exemplar é o **Kruskal-Wallis** da duração por grupo (H = 1,48; p = 0,478 nas 943 linhas; p = 0,559 na base primária). Ele trata os 206 processos ainda ativos como se tivessem terminado no dia do corte, e os ativos estão concentrados nos braços com AC (14,7% no Controle, 23,6% na Presencial, 27,7% na Remota). O teste "não vê diferença" porque **trunca justamente a cauda longa dos grupos tratados**. A figura abaixo mostra como a mediana de cada grupo depende do tratamento da censura: as medianas ingênuas são praticamente iguais, e as de Kaplan-Meier revelam que os braços com AC levam cerca de duas semanas a mais até a sentença, diferença confirmada pelo log-rank (seção 4.3.1). O único teste que o professor anunciou como "imprescindível", o Kaplan-Meier com log-rank, **nunca rodou**, por um erro de importação silenciado (E1).

**Outros testes aplicáveis**, segundo as referências indicadas:

- **para proporções e tabelas** (BARBETTA; REIS; BORNIA, 2020; SIEGEL; CASTELLAN, 2006): exato de Fisher e Fisher-Freeman-Halton (acordo na AC, com 17 eventos); qui-quadrado de **aderência** (equilíbrio do sorteio dos grupos e das técnicas, seções 2.5.1 e 2.5.3); binomial exato contra a taxa histórica de 13,3% (2.5.2); **Cochran-Mantel-Haenszel** para o acordo estratificado por mês (3.6.4); intervalos de Wilson e de Newcombe;
- **não paramétricos de posição e de forma** (SIEGEL; CASTELLAN, 2006): teste da mediana de Mood; Dunn com Holm após o Kruskal-Wallis; Kolmogorov-Smirnov para duas amostras; Jonckheere-Terpstra para tendência ordenada ao longo dos meses; **teste de sequências (corridas)** para a aleatoriedade do sorteio (3.5.1); Spearman e Kendall para a ordem de chegada (3.5.2);
- **para tempos censurados**: log-rank e a família ponderada (Wilcoxon-Gehan, Tarone-Ware, Peto-Prentice, Fleming-Harrington), log-rank estratificado, testes em pontos fixos do tempo, diferença de RMST, teste de Grambsch-Therneau para riscos proporcionais e teste tipo Gray para as funções de incidência acumulada (Parte IV);
- **inferência e decisão** (BECKER, 2015): intervalos de confiança como forma principal de relato, correção de **Holm** e controle da **FDR** (seção 3.7), **análise de poder** e **testes de equivalência** (TOST), indispensáveis para sustentar a alegação de "não há diferença" que o resumo expandido faz sem teste algum;
- **não se aplicam**: McNemar, Wilcoxon pareado, Friedman e Q de Cochran, porque os grupos são independentes (6.2).
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
     'Cox/AFT; logit em horizonte fixo', 'razão de tempos Weibull Remota 1,21 (1,00–1,45)', '4.5; 4.6; 5.1; 5.2'],
    ['Kaplan-Meier + log-rank', 'não executado', 'adequado, mas não rodou', 'erro de importação silenciado (E1)',
     'corrigir a importação', 'medianas 81 / 96 / 95 dias', '4.2; 4.3'],
], columns=['Teste do professor', 'Resultado original', 'Adequado?', 'Por quê (código)', 'Alternativa', 'Resultado com a alternativa', 'Seção'])
tabela(quadro_tshn, 'q_testes_professor', 'Avaliação dos testes do notebook do professor: o que muda com o teste adequado',
       secao='6.10', fonte='Elaboração própria; resultados originais do notebook do professor (docs/r2_notebook_professor.md) e das Partes II a V.')
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
       'cerca de duas semanas mais tardias nos braços com AC', secao='6.10',
       nota=f'base primária ({len(q6)} processos); barras de erro: IC 95% da mediana de Kaplan-Meier. O Kruskal-Wallis '
            'original (943 linhas) deu H = 1,48 e p = 0,478.')
''')

interp('q_2_11')

# =====================================================================================
md(r'''
## 6.11 Questão 2.12 — Avaliação geral da pesquisa e sugestões de validade

**Enunciado.** Concluir com uma avaliação geral da pesquisa empírica com levantamento de dados primários fidedignos, em especial do delineamento da coleta, com sugestões para conferir maior validade interna e externa a uma eventual replicação.

**Avaliação.** A pesquisa tem um mérito raro na pesquisa empírica em Direito no Brasil: é um **experimento de verdade**, com sorteio individual, controle contemporâneo e dados primários coletados diariamente na própria unidade, sobre uma questão de política judiciária relevante (a obrigatoriedade da AC inaugural nos JECs). Os dados são, no essencial, **fidedignos**: o dígito verificador do número CNJ confere em 100% dos casos, nenhuma sentença precede a distribuição, e a coerência entre acordo e tipo de sentença é perfeita (seção 1.14). Os problemas não estão na honestidade do registro, mas no **delineamento da coleta**, que foi pensado para tabelas dinâmicas de acompanhamento e não para análise estatística:

- a **variável-alvo foi mal definida** na própria planilha (duração dos ativos até `TODAY()`, "Decisão" como sentença), o que levou as médias divulgadas (78,46 e 75,2 dias) a misturar processos encerrados com processos ainda em curso (seção 2.1.2);
- **faltam as covariáveis** que o próprio projeto previa (tipo de ação, valor da causa, número de partes) e as **datas intermediárias** (AC, contestação, conclusão), que permitiriam decompor o tempo;
- **falta o motivo da extinção** sem mérito, justamente o desfecho que mais diferencia os grupos;
- o **mecanismo do sorteio** não foi documentado (o equilíbrio final é improvável num sorteio simples), as **reentradas foram re-sorteadas** e a **conciliadora coincide com a modalidade**;
- **não houve plano de análise**: o projeto previa apenas estatística descritiva, e o resumo expandido concluiu "não haver discrepância significativa" com base numa amplitude de 2,45 dias, sem teste, sem intervalo e sem considerar a censura.

**O que os dados, bem analisados, mostram.** Ao contrário da conclusão divulgada, a AC obrigatória **alongou** o tempo até a sentença (mediana de Kaplan-Meier 81 dias no Controle, 96 na Presencial e 95 na Remota), sobretudo porque **trocou sentenças de mérito por extinções sem mérito** e tornou as sentenças de mérito mais tardias, sem aumentar o acordo **na audiência** (5,1% × 4,6%). A Parte VII sintetiza esses achados com as estimativas e os intervalos.

O quadro abaixo avalia o delineamento item a item, no espírito da lista CONSORT, com a sugestão correspondente; as recomendações para a replicação estão consolidadas na seção 7.4.
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
    ['Medida do desfecho', 'parcial', 'datas digitadas; 18,4% de sentenças em fim de semana; TODAY() nos ativos', 'extrair datas dos movimentos do PJe/DataJud'],
    ['Covariáveis basais', 'inadequado', 'só a data de distribuição', 'tipo de ação, valor, nº de partes, litigante habitual, advogado'],
    ['Seguimento', 'parcial', '65 a 279 dias; 24,5% sem desfecho', 'seguimento mínimo comum (por exemplo, 180 dias) e análise de sobrevivência'],
    ['Tamanho da amostra e poder', 'inadequado', 'sem cálculo; poder ≈ 0,6 para o efeito observado (7.4)', 'cálculo de poder prévio para o desfecho primário'],
    ['Análise e relato', 'inadequado', 'amplitude de médias sem teste; sem IC', 'plano de análise ITT pré-registrado; relato CONSORT'],
    ['Fidedignidade do registro', 'adequado', 'CNJ 100% válido; 0 incoerências entre acordo e sentença; 0 datas invertidas', 'manter; acrescentar dicionário de dados'],
], columns=['Item do delineamento', 'Avaliação', 'Evidência', 'Sugestão para a replicação'])
cores_aval = {'adequado': '#E8F1E4', 'parcial': '#FFF4D6', 'inadequado': '#F9E1DC'}
tabela(quadro_aval, 'q_avaliacao', 'Avaliação do delineamento da coleta: registro fidedigno, mas desenho e plano de análise frágeis',
       secao='6.11', destaque=quadro_aval['Avaliação'].eq('inadequado').to_numpy(),
       nota='linhas destacadas: itens avaliados como inadequados.',
       fonte='Elaboração própria a partir das Partes I a V; itens inspirados na lista CONSORT.')
''')

interp('q_2_12')
