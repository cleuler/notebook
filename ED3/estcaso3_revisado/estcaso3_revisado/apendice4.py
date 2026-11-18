"""Validação dos modelos após a auditoria metodológica."""

BLOCKS = [
    ("markdown", r"""
## 25. A categoria “certeza” fora do ajuste

A comparação anterior resumiu a perda logarítmica e o Brier dos três modelos de resposta ordinal ou multinomial. Aqui examinamos as **previsões fora do ajuste** que produziram esses números. Cada um dos 233 processos da Fase III recebeu probabilidades de um modelo treinado nos outros quatro blocos da validação cruzada. A matriz mostra a categoria de maior probabilidade; a tabela separa sensibilidade e precisão por classe. Isso é importante porque uma AUC alta para *indício versus demais* não demonstra que a classe mais restrita, “certeza”, foi reconhecida.

Os três sinais F2 e as famílias de modelo foram escolhidos no estudo dos mesmos processos antes desta avaliação. Assim, a validação é **interna e retrospectiva**, mesmo que as probabilidades abaixo sejam fora do ajuste dos coeficientes. Os rótulos representam a regra operacional da pesquisa.
"""),
    ("code", r"""
from sklearn.metrics import confusion_matrix, cohen_kappa_score
from statsmodels.stats.proportion import proportion_confint

_linhas_3 = []
for _nome_3, _pr_3 in _probs.items():
    _cm_3 = confusion_matrix(y3, _pr_3.argmax(axis=1), labels=[0, 1, 2])
    display(pd.DataFrame(_cm_3, index=[f'pesquisa: {x}' for x in NIVEIS_CLASSE3],
                         columns=[f'previsto: {x}' for x in NIVEIS_CLASSE3]).rename_axis(_nome_3))
    for _k_3, _classe_3 in enumerate(NIVEIS_CLASSE3):
        _vp_3 = int(_cm_3[_k_3, _k_3])
        _n_real_3 = int(_cm_3[_k_3].sum())
        _n_prev_3 = int(_cm_3[:, _k_3].sum())
        _lo_3, _hi_3 = proportion_confint(_vp_3, _n_real_3, method='wilson')
        _linhas_3.append({'modelo': _nome_3, 'classe': _classe_3,
                          'n real': _n_real_3, 'n previsto': _n_prev_3,
                          'sensibilidade': _vp_3 / _n_real_3,
                          'IC Wilson inf.': _lo_3, 'IC Wilson sup.': _hi_3,
                          'precisão': _vp_3 / _n_prev_3 if _n_prev_3 else np.nan,
                          'kappa ponderado do modelo': cohen_kappa_score(y3, _pr_3.argmax(axis=1), weights='linear')})
TAB_VALIDACAO_3 = pd.DataFrame(_linhas_3)
display(tabela_ptbr(TAB_VALIDACAO_3, casas=3,
                    pct=['sensibilidade', 'IC Wilson inf.', 'IC Wilson sup.', 'precisão']))
assert set(TAB_VALIDACAO_3.loc[TAB_VALIDACAO_3.classe == 'certeza', 'n real']) == {30}
"""),
    ("markdown", r"""
**Leitura.** Nas previsões fora do ajuste, os três modelos acertam **0 dos 30 casos de certeza**. O multinomial atribui essa categoria a um único processo, que pertence ao grupo “indício sem certeza”; o ordinal PO e a razão contínua não a atribuem a ninguém. A sensibilidade observada de certeza é 0%, com limite superior de Wilson próximo de 11,35%. Esse limite expressa incerteza amostral, não resgata a ausência de acertos. A categoria de maior probabilidade é uma regra de decisão, não uma exigência matemática do modelo probabilístico. Um eventual corte alternativo para certeza teria de ser escolhido nos dados de treino de cada bloco e validado fora dele. A AUC binária de 0,908 não responde a essa pergunta de três classes.
"""),
    ("markdown", r"""
## 26. Escolha do modelo de previsão no ajuizamento dentro do treino

Os 405 processos de 2022–2023 são o conjunto de desenvolvimento e os 190 de 2024 servem a uma verificação temporal **exploratória**. O ano de 2024 já influenciou a exploração registrada na Seção 24; repetir a análise com uma regra explícita de escolha não recupera um teste intocado. Ainda assim, podemos evitar um novo erro: escolher variáveis ou regularização depois de comparar as métricas de 2024.

Dentro de 2022–2023, uma validação cruzada **aninhada** avalia o procedimento completo de escolha. O bloco interno seleciona, pela perda logarítmica, entre frequência de treino, JEC + mês, assunto e assunto + JEC + mês, com três forças de regularização. O bloco externo avalia previsões de casos que não participaram dessa seleção. Em seguida, a escolha é refeita nos 405 e congelada antes da verificação em 2024. A codificação das categorias é ajustada somente em cada treino por meio de uma *pipeline*. O assunto 6226 isolado não é candidato aqui porque foi destacado após examinar o estudo inteiro.

O bootstrap de 2024 abaixo mede a dispersão das métricas **condicional ao modelo já ajustado** e preserva a quantidade observada de positivos e negativos. Ele não incorpora a incerteza da escolha do modelo, nem cria uma coorte externa. Perda logarítmica e Brier avaliam a qualidade das probabilidades como um todo; a média prevista comparada à frequência observada é uma checagem simples de calibração no agregado. Com apenas 28 positivos, uma curva flexível ou um coeficiente de calibração teria grande incerteza.
"""),
    ("code", r"""
from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, average_precision_score, log_loss, brier_score_loss

_cols_25 = {'JEC + mês': ['jec_txt', 'mes'], 'assunto': ['assunto'],
            'assunto + JEC + mês': ['assunto', 'jec_txt', 'mes']}
_candidatos_25 = [('frequência do treino', (), None)] + [
    (f'{nome}; C={c:g}', tuple(cols), c)
    for nome, cols in _cols_25.items() for c in (0.03, 0.3, 3.0)]
_X_25 = _entrada.reset_index(drop=True)
_y_25 = _y_e.copy()
_idx_dev_25 = np.flatnonzero(_tr_e)
_idx_2024_25 = np.flatnonzero(_te_e)

def _ajustar_25(nome, cols, c, treino, teste):
    if c is None:
        return np.full(len(teste), _y_25[treino].mean())
    modelo = make_pipeline(OneHotEncoder(handle_unknown='ignore'),
                          LogisticRegression(C=c, max_iter=3000))
    modelo.fit(_X_25.loc[treino, list(cols)], _y_25[treino])
    return modelo.predict_proba(_X_25.loc[teste, list(cols)])[:, 1]

def _escolher_25(indices, *, semente, partes=4):
    cv_interno = StratifiedKFold(n_splits=partes, shuffle=True, random_state=semente)
    resultados = []
    for nome, cols, c in _candidatos_25:
        pr = np.full(len(indices), np.nan)
        for tr_local, val_local in cv_interno.split(indices, _y_25[indices]):
            pr[val_local] = _ajustar_25(nome, cols, c, indices[tr_local], indices[val_local])
        assert np.isfinite(pr).all()
        resultados.append((log_loss(_y_25[indices], pr, labels=[0, 1]), nome, cols, c))
    return min(resultados, key=lambda r: (r[0], r[1])), resultados

_cv_externo_25 = StratifiedKFold(n_splits=5, shuffle=True, random_state=20261030)
_oof_25 = np.full(len(_idx_dev_25), np.nan)
_escolhas_25 = []
for _tr_l, _te_l in _cv_externo_25.split(_idx_dev_25, _y_25[_idx_dev_25]):
    _id_tr = _idx_dev_25[_tr_l]
    _id_te = _idx_dev_25[_te_l]
    _melhor, _ = _escolher_25(_id_tr, semente=20261030 + int(_te_l[0]))
    _escolhas_25.append(_melhor[1])
    _oof_25[_te_l] = _ajustar_25(*_melhor[1:], _id_tr, _id_te)
assert np.isfinite(_oof_25).all()
_melhor_25, _todos_25 = _escolher_25(_idx_dev_25, semente=20261031, partes=5)
_p_2024_25 = _ajustar_25(*_melhor_25[1:], _idx_dev_25, _idx_2024_25)
_y_2024_25 = _y_25[_idx_2024_25]
_p_base_25 = np.full(len(_idx_2024_25), _y_25[_idx_dev_25].mean())

def _metricas_25(y, p):
    return {'AUC': roc_auc_score(y, p), 'precisão média': average_precision_score(y, p),
            'log-loss': log_loss(y, p, labels=[0, 1]), 'Brier': brier_score_loss(y, p),
            'média prevista': float(np.mean(p)), 'frequência observada': float(np.mean(y))}

TAB_ESCOLHA_25 = pd.DataFrame([{'candidato': r[1], 'log-loss CV no desenvolvimento': r[0]}
                               for r in sorted(_todos_25, key=lambda r: (r[0], r[1]))])
display(tabela_ptbr(TAB_ESCOLHA_25, casas=4))
TAB_AVALIACAO_25 = pd.DataFrame([
    {'avaliação': 'procedimento completo: CV externa, 2022–2023',
     'modelo': 'escolha interna por bloco', **_metricas_25(_y_25[_idx_dev_25], _oof_25)},
    {'avaliação': 'frequência do treino em 2024', 'modelo': 'referência',
     **_metricas_25(_y_2024_25, _p_base_25)},
    {'avaliação': 'modelo congelado em 2024', 'modelo': _melhor_25[1],
     **_metricas_25(_y_2024_25, _p_2024_25)},
])
display(tabela_ptbr(TAB_AVALIACAO_25, casas=4,
                    pct=['média prevista', 'frequência observada']))
display(pd.Series(_escolhas_25).value_counts().rename('escolhas nos 5 blocos externos').to_frame())

_rng_25 = np.random.default_rng(20261031)
_pos_25, _neg_25 = np.flatnonzero(_y_2024_25 == 1), np.flatnonzero(_y_2024_25 == 0)
_boot_25 = []
for _ in range(2000):
    _ind_25 = np.r_[_rng_25.choice(_pos_25, len(_pos_25), replace=True),
                     _rng_25.choice(_neg_25, len(_neg_25), replace=True)]
    _m_25 = _metricas_25(_y_2024_25[_ind_25], _p_2024_25[_ind_25])
    _m_25['ganho log-loss versus frequência'] = (
        log_loss(_y_2024_25[_ind_25], _p_base_25[_ind_25], labels=[0, 1]) - _m_25['log-loss'])
    _boot_25.append(_m_25)
_boot_25 = pd.DataFrame(_boot_25)
display(tabela_ptbr(pd.DataFrame([{'métrica': c, 'estimativa 2024':
    (TAB_AVALIACAO_25.iloc[1]['log-loss'] - TAB_AVALIACAO_25.iloc[2]['log-loss'])
    if c == 'ganho log-loss versus frequência' else TAB_AVALIACAO_25.iloc[2][c],
    'limite inferior': _boot_25[c].quantile(.025), 'limite superior': _boot_25[c].quantile(.975)}
    for c in ('AUC', 'precisão média', 'log-loss', 'Brier', 'ganho log-loss versus frequência')]), casas=4))
"""),
    ("markdown", r"""
**Leitura.** A escolha interna em 2022–2023 foi **assunto, C = 3**, repetida nos cinco blocos externos. A validação aninhada nesse período obteve AUC **0,848** e log-loss **0,308** para o procedimento de escolha completo. Após ajuste nos 405 casos de desenvolvimento, o modelo alcançou em 2024 AUC **0,876**, precisão média **0,572**, log-loss **0,269** e Brier **0,079**; a frequência do treino teve log-loss **0,424**. O bootstrap condicional dá aproximadamente **[0,788; 0,944]** para a AUC e **[0,088; 0,217]** para o ganho de log-loss sobre a frequência. A probabilidade média prevista foi **15,53%**, perto dos **14,74%** observados; isso examina só a calibração média. As faixas não incluem a incerteza da escolha do modelo. A avaliação em 2024 continua exploratória porque os resultados desse ano já eram conhecidos no desenvolvimento do estudo.
"""),
    ("markdown", r"""
## 27. A informação anterior em Bayes e a fonte correta dos rótulos

Uma atualização Bayesiana pode usar os **77 indícios nos 405 processos de 2022–2023** como evidência anterior para os **28 indícios nos 190 de 2024**: são processos distintos. No exemplo Beta-Binomial abaixo, a posteriori do primeiro período vira a priori do segundo. A conta supõe uma prevalência comum entre anos e ignora parte do desenho amostral; por isso é uma ilustração da lógica de atualização, não uma substituição da estimativa estratificada. Para uma regressão logística Bayesiana, a mesma lógica vale para a distribuição conjunta dos coeficientes, com a ressalva de que os efeitos de ano podem mudar.

Os **17,65%** publicados provêm dos mesmos 595 processos; empregá-los como priori e em seguida reapresentar esses 595 na verossimilhança contaria a amostra duas vezes. A priori de 30% da Seção 6 vem de levantamento documental em outra região e com outro recorte; permanece um cenário de sensibilidade. A lista ampla `casos_novos_JEC_Natal_...xlsx` serve à conferência da moldura, enquanto os rótulos dos 595 estão na aba `AMOSTRA` da planilha preenchida. O intervalo [14,59%; 20,70%] do roteiro, embora chamado Wilson, é reproduzido como Wald com correção de população finita; os Wilson e o intervalo aproximado pelo desenho aparecem na Seção 16.
"""),
    ("code", r"""
_k_antigo = int(am.loc[am.ano.astype(int) < 2024, 'indicio'].sum())
_n_antigo = int((am.ano.astype(int) < 2024).sum())
_k_novo = int(am.loc[am.ano.astype(int) == 2024, 'indicio'].sum())
_n_novo = int((am.ano.astype(int) == 2024).sum())
assert (_k_antigo, _n_antigo, _k_novo, _n_novo) == (77, 405, 28, 190)
_a0, _b0 = 1, 1
_etapas_bayes = [
    ('antes dos dados', _a0, _b0),
    ('após 2022–2023', _a0 + _k_antigo, _b0 + _n_antigo - _k_antigo),
    ('após incorporar 2024', _a0 + _k_antigo + _k_novo,
     _b0 + _n_antigo - _k_antigo + _n_novo - _k_novo),
]
TAB_BAYES_SEQ = pd.DataFrame([{'etapa': nome, 'alfa': a, 'beta': b,
    'média posterior': a / (a + b), 'IC créd. 95% inf.': stats.beta.ppf(.025, a, b),
    'IC créd. 95% sup.': stats.beta.ppf(.975, a, b)} for nome, a, b in _etapas_bayes])
display(tabela_ptbr(TAB_BAYES_SEQ, casas=3,
                    pct=['média posterior', 'IC créd. 95% inf.', 'IC créd. 95% sup.']))
"""),
]
