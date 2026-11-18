"""Blocos adicionais do notebook revisado, sem nova leitura manual de autos."""

BLOCKS = [
    ("markdown", r"""
---

# PARTE V — SENSIBILIDADE DOS MÉTODOS E LIMITES DA INFERÊNCIA

## 15. LCA, k-modes e k-means nos mesmos dados

O exercício do professor pede agrupamento não supervisionado em três níveis. Há mais de um algoritmo possível, mas eles respondem a perguntas matemáticas diferentes. **K-means** minimiza distâncias quadráticas a médias; códigos numéricos arbitrários para assunto ou desfecho criariam distâncias fictícias. Por isso, nesta comparação ele recebe uma codificação *one-hot* aprendida apenas nos processos de treino. **K-modes** conta diferenças entre categorias e descreve cada grupo por uma combinação modal. **LCA** estima probabilidades das categorias em cada classe e probabilidades de pertença, assumindo independência local dos indicadores dentro de cada grupo.

Todos recebem os mesmos sete indicadores do DataJud, a mesma divisão 2022–2023/2024 e **K = 3**, exigido pelo roteiro. K-means entra apenas como **controle de sensibilidade** após one-hot: não será o método principal para variáveis nominais. Os rótulos jurídicos existentes são usados somente depois do ajuste, como referência externa imperfeita. ARI e AMI dispensam ordenar os nomes dos grupos: por isso são mais apropriados para esta comparação do que atribuir a cada grupo o nome da classe jurídica que mais se parece com ele. A estabilidade e a interpretação substantiva também importam. Nenhum algoritmo pode inferir da trajetória processual um sinal que não foi observado.
"""),
    ("code", r"""
from estcaso3_revisado.metodos import benchmark_agrupamentos, dependencia_local

BENCH, PARES_METODOS, ATRIB = benchmark_agrupamentos(
    X_T.loc[treino, IND_DJ].to_numpy(), X_T.loc[teste, IND_DJ].to_numpy(),
    real_2024, prev_2024, seed=C.inteiro_semente(SEMENTES['kmodes']))
display(BENCH.round(3))
display(PARES_METODOS.round(3))
for metodo, rotulos in ATRIB.items():
    display(pd.crosstab(pd.Series(real_2024, name='rótulo existente'),
                        pd.Series(rotulos, name=f'grupo: {metodo}')).rename_axis(metodo))

DEP_LOCAL = dependencia_local(XDJ.to_numpy(), LCA_DJ[3], IND_DJ)
display(DEP_LOCAL.head(10).round(2))
display(pd.DataFrame({'K': SEL_DJ.index.astype(int), 'BIC': SEL_DJ.BIC.to_numpy()}).round(2))
display(Markdown('O menor BIC nesta amostra é K = **' + str(int(SEL_DJ.BIC.idxmin())) +
                 '**. A diferença de BIC entre K = 3 e K = 4 é **' +
                 fnum(abs(SEL_DJ.loc[3, 'BIC'] - SEL_DJ.loc[4, 'BIC']), 2) +
                 '**; K = 3 é mantido como exercício didático. Resíduos bivariados grandes indicam '
                 'que a independência local da LCA deve ser tratada como hipótese aproximada.'))
"""),
    ("markdown", r"""
**Como ler a comparação.** ARI e AMI próximos de zero indicam que a partição pouco coincide com os rótulos já disponíveis, independentemente da numeração dos grupos. A tabela entre métodos mostra se eles encontram trajetórias semelhantes entre si; concordância entre algoritmos não provaria validade jurídica. A LCA é a principal descrição probabilística e k-modes oferece uma referência categórica simples. K-means é mostrado apenas para verificar se essa escolha alteraria a conclusão. A interpretação da LCA depende também dos diagnósticos da independência local.

## 16. Prevalência com o desenho amostral

A estimativa principal de indício vem da amostra estratificada por ano. Um Wilson simples para 105/595 e a aproximação por tamanho efetivo são úteis como comparação, mas o segundo não é um Wilson exato para amostragem estratificada. Abaixo, o erro-padrão já calculado com pesos de estrato e correção de população finita é transformado na escala do logito. Esse intervalo respeita os limites de 0 a 1 e explicita o desenho. A diferença entre intervalos é informativa; nenhum deles corrige erro de classificação dos rótulos operacionais.

Para a pergunta sobre juizados, a permutação mantém cada ano separado. Assim, o teste verifica se a distribuição de indício por JEC poderia surgir ao acaso **condicionada ao ano de sorteio**, em vez de embaralhar os 595 processos como se fossem uma amostra simples indiferenciada.
"""),
    ("code", r"""
from estcaso3_revisado.metodos import intervalo_logit_desenho

IC_LOGIT = intervalo_logit_desenho(est_ind['p_st'], est_ind['ep'])
TAB_IC = pd.DataFrame([
    {'método': 'publicado: Wald + FPC (N = 83.139)', 'inferior': IC_REF['indício']['publicado (Wald + FPC, N = 83.139)'][0],
     'superior': IC_REF['indício']['publicado (Wald + FPC, N = 83.139)'][1]},
    {'método': 'Wilson simples (595)', 'inferior': IC_REF['indício']['Wilson'][0],
     'superior': IC_REF['indício']['Wilson'][1]},
    {'método': 'Wilson aproximado por n efetivo', 'inferior': est_ind['wilson_desenho'][0],
     'superior': est_ind['wilson_desenho'][1]},
    {'método': 'logito com EP do desenho', 'inferior': IC_LOGIT[0], 'superior': IC_LOGIT[1]},
])
display(tabela_ptbr(TAB_IC, pct=['inferior', 'superior']))
display(Markdown(f'Pela estimativa estratificada, a proporção operacional é **{fpct(est_ind["p_st"])}**. '
                 f'O intervalo logito com o erro-padrão do desenho é **{fic(*IC_LOGIT, pct=True)}**; '
                 'é uma aproximação assintótica, não um intervalo exato.'))

def _chi_jec(indicadores, jecs):
    tab = np.zeros((14, 2), dtype=int)
    np.add.at(tab, (jecs - 1, indicadores.astype(int)), 1)
    return stats.chi2_contingency(tab, correction=False)[0]

_jec = am.jec.astype(int).to_numpy()
_ano = am.ano.astype(int).to_numpy()
_ind = am.indicio.astype(int).to_numpy()
_obs = _chi_jec(_ind, _jec)
_rng = np.random.default_rng(SEMENTES['permutacao'])
_B = 1999
_ge = 0
for _ in range(_B):
    _perm = _ind.copy()
    for _a in (2022, 2023, 2024):
        _m = np.flatnonzero(_ano == _a)
        _perm[_m] = _rng.permutation(_perm[_m])
    _ge += _chi_jec(_perm, _jec) >= _obs
_p_perm = (_ge + 1) / (_B + 1)
display(pd.DataFrame([{'pergunta': 'indício × JEC, condicionado ao ano',
                       'qui-quadrado observado': _obs, 'permutações': _B,
                       'p de permutação': _p_perm}]).round(4))
"""),
    ("markdown", r"""
## 17. Comparação preditiva das três categorias

A ROC binária empata entre os modelos porque todos ordenam igualmente os sete padrões dos três sinais F2. Para comparar probabilidades das **três respostas** — demais, indício sem certeza e certeza — cada processo abaixo recebe uma previsão produzida por um modelo que não foi ajustado com ele. A perda logarítmica pune probabilidades muito confiantes e erradas; o Brier multiclasses mede a distância entre probabilidades e categorias observadas. Também se compara a frequência de certeza prevista à observada. São diagnósticos de calibração da **regra operacional da pesquisa**, não de verdade jurídica independente.

A escolha do modelo e dos três preditores ocorreu no estudo completo; esta validação cruzada mede desempenho interno e não é uma nova validação externa. Diferenças pequenas entre perdas devem ser tratadas como empate prático.
"""),
    ("code", r"""
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import log_loss
from statsmodels.miscmodels.ordinal_model import OrderedModel

_folds = StratifiedKFold(n_splits=5, shuffle=True,
                         random_state=C.inteiro_semente(SEMENTES['validacao_cruzada']))
_probs = {k: np.zeros((n233, 3)) for k in ('multinomial', 'ordinal PO', 'razão contínua', 'frequência no treino')}
_xc = sm.add_constant(X3, has_constant='add')
with C.capturar_avisos('comparação preditiva fora do ajuste', AVISOS):
    for _tr, _te in _folds.split(X3, y3):
        _mn = sm.MNLogit(y3[_tr], _xc.iloc[_tr]).fit(disp=0, method='bfgs', maxiter=1000)
        _po = OrderedModel(y3[_tr], X3.iloc[_tr], distr='logit').fit(disp=0, method='bfgs', maxiter=1000)
        _b1 = sm.Logit((y3[_tr] >= 1).astype(int), _xc.iloc[_tr]).fit(disp=0, method='bfgs', maxiter=1000)
        _tr2 = _tr[y3[_tr] >= 1]
        _b2 = sm.Logit((y3[_tr2] == 2).astype(int),
                       _xc.iloc[_tr2][['const', 'F2_02', 'F2_11']]).fit(disp=0, method='bfgs', maxiter=1000)
        _p1 = np.asarray(_b1.predict(_xc.iloc[_te]))
        _p2 = np.asarray(_b2.predict(_xc.iloc[_te][['const', 'F2_02', 'F2_11']]))
        _probs['multinomial'][_te] = np.asarray(_mn.predict(_xc.iloc[_te]))
        _probs['ordinal PO'][_te] = np.asarray(_po.predict(X3.iloc[_te]))
        _probs['razão contínua'][_te] = np.column_stack([1 - _p1, _p1 * (1 - _p2), _p1 * _p2])
        _probs['frequência no treino'][_te] = np.bincount(y3[_tr], minlength=3) / len(_tr)
_yhot = np.eye(3)[y3]
_score = pd.DataFrame([
    {'modelo': k, 'log-loss': log_loss(y3, p, labels=[0, 1, 2]),
     'Brier multiclasses': np.mean(np.sum((p - _yhot) ** 2, axis=1)),
     'certeza prevista média': p[:, 2].mean(), 'certeza observada': (y3 == 2).mean()}
    for k, p in _probs.items()
])
display(tabela_ptbr(_score, casas=4, pct=['certeza prevista média', 'certeza observada']))

_loss = {k: -np.log(np.clip(p[np.arange(n233), y3], 1e-12, 1)) for k, p in _probs.items()}
_rng = np.random.default_rng(SEMENTES['bootstrap'])
_dif = _loss['ordinal PO'] - _loss['razão contínua']
_boot = np.array([_dif[_rng.integers(0, n233, n233)].mean() for _ in range(1000)])
display(Markdown('Diferença média de log-loss (PO − razão contínua): **' + fnum(_dif.mean(), 4) +
                 '**; faixa bootstrap condicional aos modelos ajustados: **' +
                 fic(*np.quantile(_boot, [0.025, 0.975]), casas=4) + '**.'))
"""),
    ("markdown", r"""
## 18. Acordo, mérito e extinção como eventos distintos

Kaplan–Meier da Seção 4 responde pelo tempo até **qualquer** desfecho. Quando a pergunta muda para “qual a incidência de acordo?” ou “qual a incidência de extinção?”, mérito e os outros desfechos impedem que aquele primeiro desfecho ainda ocorra. Eles competem entre si. A incidência acumulada de Aalen–Johansen permite olhar essas categorias sem tratar as outras como simples perdas de acompanhamento. Continua sendo uma análise dos **eventos inferidos da TPU**, sujeita a seus erros e à diferença de tempo de observação entre coortes.
"""),
    ("code", r"""
from lifelines import AalenJohansenFitter
_evento = np.select([td.desfecho.astype(str) == 'acordo',
                      td.desfecho.astype(str) == 'mérito',
                      td.desfecho.astype(str) == 'extinção sem mérito'], [1, 2, 3], default=0)
assert np.array_equal((_evento > 0).astype(int), td.e.astype(int).to_numpy())
_aj = {}
fig, ax = plt.subplots(figsize=(8, 4.3))
for _k, _nome in [(1, 'acordo'), (2, 'mérito'), (3, 'extinção sem mérito')]:
    _f = AalenJohansenFitter(calculate_variance=False, seed=2026).fit(td.t, _evento,
                                                                        event_of_interest=_k, label=_nome)
    _aj[_nome] = _f
    _f.plot(ax=ax)
ax.set_xlabel('dias desde o ajuizamento')
ax.set_ylabel('incidência acumulada do primeiro desfecho')
ax.set_title('Eventos concorrentes segundo o proxy TPU')
fig.tight_layout()
fig.savefig(FIGURAS / 'incidencia_eventos_concorrentes.png', dpi=150)
plt.show()
_linhas = []
for _nome, _f in _aj.items():
    _tab = _f.cumulative_density_.iloc[:, 0]
    _linhas.append({'desfecho': _nome,
                    'até 365 dias': float(_tab.loc[_tab.index <= 365].iloc[-1]) if (_tab.index <= 365).any() else 0.0,
                    'até 730 dias': float(_tab.loc[_tab.index <= 730].iloc[-1]) if (_tab.index <= 730).any() else 0.0})
display(tabela_ptbr(pd.DataFrame(_linhas), pct=['até 365 dias', 'até 730 dias']))
"""),
    ("markdown", r"""
## 19. Simulação de todo o funil

A simulação anterior cobre principalmente os 233 processos da Fase III e demonstra a recuperação de coeficientes sob um modelo gerador favorável. Para servir de exemplo de desenho de pesquisa, esta extensão simula uma **população finita por ano**, com exclusão na Fase I, passagem pela Fase II, indício na Fase III e certeza entre os indícios. Ela sorteia a mesma quantidade de processos por estrato que a amostra real. Os parâmetros são estimados do caso observado; os dados produzidos são artificiais.

Um segundo cenário introduz taxas **hipotéticas** de 1% de falso positivo e 10% de falso negativo no registro do indício. Esses valores não foram medidos na pesquisa. Eles mostram quanto a conclusão dependeria da confiabilidade da codificação, sem exigir nova leitura de processos nem fingir que a simulação valida o rótulo original.
"""),
    ("code", r"""
from estcaso3_revisado.metodos import simulacao_funil
_taxas = {}
for _ano in (2022, 2023, 2024):
    _g = am.loc[am.ano == _ano]
    _e = _g.loc[~_g.excluido_f1.astype(bool)]
    _f = _e.loc[_e.alguma_f2.astype(bool)]
    _i = _f.loc[_f.indicio.astype(bool)]
    _taxas[_ano] = (float(_g.excluido_f1.mean()), float(_e.alguma_f2.mean()),
                    float(_f.indicio.mean()), float(_i.certeza.mean()))
_nh = estratos[['N_h', 'n_h']].copy()
_sim = simulacao_funil(_nh, _taxas, repeticoes=300,
                       seed=C.inteiro_semente(SEMENTES['simulacao']))
_sim['erro amostral'] = _sim['estimativa estratificada sem erro'] - _sim['prevalência na população simulada']
_sim['erro com codificação hipotética'] = _sim['estimativa com erro hipotético'] - _sim['prevalência na população simulada']
display(_sim[['erro amostral', 'erro com codificação hipotética']].agg(['mean', 'std',
                lambda x: x.quantile(0.025), lambda x: x.quantile(0.975)]).rename(index={'<lambda>': 'quantil'}).round(4))
display(Markdown('Em 300 populações artificiais, a simulação permite separar a variabilidade do sorteio '
                 'do deslocamento produzido pelo erro de codificação hipotético. Nenhuma taxa de erro '
                 'jurídico real foi estimada aqui.'))
"""),
    ("markdown", r"""
## 20. O que estas análises permitem concluir

Os modelos multinomial, ordinal e condicional do roteiro continuam úteis para ensinar perguntas distintas sobre os mesmos dados. ROC e Gini cumprem o pedido do professor, mas empatam porque os escores preservam a mesma ordenação. A comparação de probabilidades fora do ajuste é mais informativa para os três níveis. O agrupamento descreve trajetórias administrativas; o confronto com rótulos existentes decide se essas trajetórias se aproximam da regra da pesquisa. A prevalência populacional operacional continua vindo do sorteio estratificado, não das proporções de grupos do DataJud.

Os testes já apresentados nas seções anteriores são lidos à luz de suas populações de referência e do desenho. Correções de Holm limitam erros de múltiplas comparações, mas uma hipótese escrita no notebook depois de ver os dados não vira, por isso, um pré-registro. A priori bayesiana de 30% também permanece um cenário transferido de outro contexto; as análises de sensibilidade são parte necessária da interpretação. As probabilidades da LCA são de **pertença a perfis estatísticos**, não de certeza jurídica.
"""),
]
