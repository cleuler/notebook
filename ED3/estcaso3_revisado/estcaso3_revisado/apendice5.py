"""Comparação retrospectiva entre assunto, trajetória DataJud e combinação."""

BLOCKS = [
    ("markdown", r"""
## 28. O DataJud acrescenta sinal ao assunto da moldura?

A Seção 26 examinou a informação disponível no ajuizamento. Aqui fazemos uma pergunta diferente: **depois de observar a trajetória do processo, os registros do DataJud ajudam a reproduzir o rótulo de indício atribuído pela pesquisa?** Vinculamos, pelo número CNJ, os processos rotulados da Hadja ao assunto da moldura do TJRN e aos dados administrativos do DataJud. Há documento para **593 dos 595**; a comparação usa os **mesmos 593 processos** nas três abordagens para que a ausência dos outros dois não favoreça um modelo.

Comparamos (1) assunto da moldura; (2) trajetória do DataJud — desfecho TPU, recurso, evolução a cumprimento, redistribuição, classe atual, quantidade de movimentos e tempo até desfecho ou censura; e (3) a união desses campos. São variáveis de momentos diferentes. **O segundo e o terceiro modelos são retrospectivos**: não servem para prever risco no ajuizamento, porque conhecem movimentos e situação posteriores. O desfecho TPU continua sendo um proxy administrativo, e o rótulo de indício continua sendo a regra operacional da pesquisa.

A regularização de cada regressão logística é escolhida por perda logarítmica em cinco blocos de **2022–2023**, usando codificação aprendida apenas no respectivo treino. O ano de 2024 recebe somente as previsões dos modelos ajustados no período anterior. As métricas são AUC, precisão média, perda logarítmica e Brier. Usar os mesmos casos permite calcular diferenças pareadas; o bootstrap mantém fixos os números de positivos e negativos de 2024. Essa avaliação é exploratória porque 2024 já foi examinado ao longo do estudo.
"""),
    ("code", r"""
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score, average_precision_score, log_loss, brier_score_loss

_vinculo_28 = l10.merge(
    base[['NÚMERO PROCESSO', 'CÓD ASSUNTO']].rename(columns={'NÚMERO PROCESSO': 'numero',
                                                             'CÓD ASSUNTO': 'assunto_moldura'}),
    on='numero', how='left', validate='one_to_one', indicator=True).reset_index(drop=True)
assert len(_vinculo_28) == 593 and (_vinculo_28['_merge'] == 'both').all()
assert _vinculo_28.numero.is_unique and _vinculo_28.assunto_moldura.notna().all()
_igual_assunto_28 = (_vinculo_28.assunto_moldura.astype(str) ==
                     _vinculo_28.assunto_codigo.astype(str))
assert int((~_igual_assunto_28).sum()) == 86

_X_28 = _vinculo_28.copy()
_cat_dj_28 = ['desfecho', 'houve_recurso', 'evoluiu_cumprimento', 'redistribuido', 'classe_atual']
for _col_28 in ['assunto_moldura'] + _cat_dj_28:
    _X_28[_col_28] = _X_28[_col_28].astype(str)
_X_28['log_movimentos'] = np.log1p(_X_28.n_movimentos.astype(float))
_X_28['log_tempo'] = np.log1p(_X_28.t_desfecho.astype(float))
assert _X_28[['log_movimentos', 'log_tempo']].notna().all().all()
_num_dj_28 = ['log_movimentos', 'log_tempo']
_grupos_28 = {
    'assunto da moldura': (['assunto_moldura'], []),
    'trajetória DataJud': (_cat_dj_28, _num_dj_28),
    'assunto + trajetória DataJud': (['assunto_moldura'] + _cat_dj_28, _num_dj_28),
}
_y_28 = _X_28.indicio.astype(int).to_numpy()
_tr_28 = np.flatnonzero(_X_28.ano.astype(int).to_numpy() < 2024)
_te_28 = np.flatnonzero(_X_28.ano.astype(int).to_numpy() == 2024)
assert (len(_tr_28), len(_te_28), int(_y_28[_tr_28].sum()), int(_y_28[_te_28].sum())) == (403, 190, 77, 28)

def _modelo_28(cat, num, c):
    etapas = [('categorias', OneHotEncoder(handle_unknown='ignore'), cat)]
    if num:
        etapas.append(('numericas', StandardScaler(), num))
    return make_pipeline(ColumnTransformer(etapas), LogisticRegression(C=c, max_iter=3000))

_predicoes_28 = {}
_resultados_28 = []
for _nome_28, (_cat_28, _num_28) in _grupos_28.items():
    _opcoes_28 = []
    for _c_28 in (0.03, 0.3, 3.0):
        _cv_28 = StratifiedKFold(n_splits=5, shuffle=True, random_state=20261030)
        _oof_28 = np.full(len(_tr_28), np.nan)
        for _aj_28, _val_28 in _cv_28.split(_tr_28, _y_28[_tr_28]):
            _m_28 = _modelo_28(_cat_28, _num_28, _c_28)
            _m_28.fit(_X_28.iloc[_tr_28[_aj_28]], _y_28[_tr_28[_aj_28]])
            _oof_28[_val_28] = _m_28.predict_proba(_X_28.iloc[_tr_28[_val_28]])[:, 1]
        _opcoes_28.append((log_loss(_y_28[_tr_28], _oof_28, labels=[0, 1]), _c_28))
    _cv_loss_28, _melhor_c_28 = min(_opcoes_28)
    _m_28 = _modelo_28(_cat_28, _num_28, _melhor_c_28)
    _m_28.fit(_X_28.iloc[_tr_28], _y_28[_tr_28])
    _p_28 = _m_28.predict_proba(_X_28.iloc[_te_28])[:, 1]
    _predicoes_28[_nome_28] = _p_28
    _resultados_28.append({'informação': _nome_28, 'C escolhido': _melhor_c_28,
                           'log-loss CV 2022–2023': _cv_loss_28,
                           'AUC 2024': roc_auc_score(_y_28[_te_28], _p_28),
                           'precisão média 2024': average_precision_score(_y_28[_te_28], _p_28),
                           'log-loss 2024': log_loss(_y_28[_te_28], _p_28, labels=[0, 1]),
                           'Brier 2024': brier_score_loss(_y_28[_te_28], _p_28)})
TAB_COMBINACAO_28 = pd.DataFrame(_resultados_28)
display(tabela_ptbr(TAB_COMBINACAO_28, casas=4))
display(pd.DataFrame([{'comparação de assunto': 'moldura TJRN × primeiro assunto do DataJud',
                       'códigos iguais': int(_igual_assunto_28.sum()),
                       'códigos diferentes': int((~_igual_assunto_28).sum()),
                       'processos vinculados': len(_vinculo_28)}]))

_rng_28 = np.random.default_rng(20261030)
_yb_28 = _y_28[_te_28]
_pos_28 = np.flatnonzero(_yb_28 == 1)
_neg_28 = np.flatnonzero(_yb_28 == 0)
_p_ass_28 = _predicoes_28['assunto da moldura']
_p_comb_28 = _predicoes_28['assunto + trajetória DataJud']
_dif_28 = []
for _ in range(2000):
    _b_28 = np.r_[_rng_28.choice(_pos_28, len(_pos_28), replace=True),
                  _rng_28.choice(_neg_28, len(_neg_28), replace=True)]
    _dif_28.append({
        'AUC combinado − assunto': roc_auc_score(_yb_28[_b_28], _p_comb_28[_b_28]) -
                                  roc_auc_score(_yb_28[_b_28], _p_ass_28[_b_28]),
        'precisão média combinado − assunto': average_precision_score(_yb_28[_b_28], _p_comb_28[_b_28]) -
                                               average_precision_score(_yb_28[_b_28], _p_ass_28[_b_28]),
        'log-loss combinado − assunto': log_loss(_yb_28[_b_28], _p_comb_28[_b_28], labels=[0, 1]) -
                                        log_loss(_yb_28[_b_28], _p_ass_28[_b_28], labels=[0, 1]),
        'Brier combinado − assunto': brier_score_loss(_yb_28[_b_28], _p_comb_28[_b_28]) -
                                     brier_score_loss(_yb_28[_b_28], _p_ass_28[_b_28]),
    })
_dif_28 = pd.DataFrame(_dif_28)
_metricas_dif_28 = [('AUC', 'AUC 2024'), ('precisão média', 'precisão média 2024'),
                    ('log-loss', 'log-loss 2024'), ('Brier', 'Brier 2024')]
TAB_DIF_28 = pd.DataFrame([{'métrica': m,
    'diferença combinado − assunto': float(TAB_COMBINACAO_28.set_index('informação').loc[
        'assunto + trajetória DataJud', coluna] - TAB_COMBINACAO_28.set_index('informação').loc[
        'assunto da moldura', coluna]),
    'limite inferior': _dif_28[f'{m} combinado − assunto'].quantile(.025),
    'limite superior': _dif_28[f'{m} combinado − assunto'].quantile(.975)}
    for m, coluna in _metricas_dif_28])
display(tabela_ptbr(TAB_DIF_28, casas=4))
"""),
    ("markdown", r"""
**Como interpretar.** A regressão com assunto da moldura, a regressão com trajetória e a combinação são avaliadas nos mesmos 190 casos de 2024, após escolha da regularização apenas em 2022–2023. A tabela de diferenças usa a convenção **combinado − assunto**: AUC e precisão média maiores favorecem a combinação; log-loss e Brier menores favorecem a combinação. As faixas bootstrap que cruzam zero indicam que os dados de 2024 não estabelecem uma vantagem estável naquela métrica. A precisão média pode melhorar mesmo quando a qualidade global das probabilidades piora; por isso não escolhemos o modelo olhando apenas uma coluna.

O código de assunto da moldura concorda com o primeiro assunto extraído do DataJud em 507 dos 593 processos vinculados e diverge em 86. Essa divergência pode vir da presença de vários assuntos, da regra de escolha do principal, de atualização cadastral ou de outro detalhe da extração. **Ela não prova, isoladamente, que o assunto tenha mudado depois do ajuizamento.** Para a previsão no ajuizamento, o assunto deve ser obtido de um registro comprovadamente disponível naquele momento; nesta comparação retrospectiva, usamos a moldura para manter a mesma definição nas três abordagens.
"""),
]
