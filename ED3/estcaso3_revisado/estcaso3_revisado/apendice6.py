"""Sensibilidade retrospectiva: desfecho detalhado, interação e não linearidade."""

BLOCKS = [
    ("markdown", r"""
## 29. A trajetória detalhada ou suas interações acrescentam algo?

A categoria ampla de desfecho da seção anterior pode ocultar diferenças entre desistência, ausência do autor e outras decisões. Testamos três extensões **retrospectivas** sobre os mesmos 593 processos vinculados: (1) uma regressão com desfecho detalhado, resultado do recurso e indicadores adicionais; (2) a mesma regressão com uma interação entre o grupo de assunto 6226/outros e o desfecho amplo; e (3) uma floresta aleatória com as variáveis detalhadas. A interação verifica se um mesmo tipo de desfecho se associa de modo diferente ao indício conforme o assunto. O grupo 6226 já se destacou nas análises anteriores, então a escolha desta interação é exploratória.

As alternativas e suas regularizações são comparadas por validação cruzada **apenas em 2022–2023**, com perda logarítmica como critério único de escolha. Depois de escolher a melhor extensão, confrontamos suas previsões com o modelo de assunto da Seção 28 nos 190 casos de 2024. O ano de 2024 continua sendo uma avaliação exploratória, pois já foi consultado durante o desenvolvimento do estudo. O bootstrap pareado descreve a variabilidade do conjunto avaliado, mantendo os modelos treinados fixos; não mede toda a incerteza do processo de modelagem.

Os campos adicionais vêm dos registros administrativos e suas regras TPU. Há diferenças no tempo disponível para observar a trajetória de processos ajuizados em anos distintos; portanto, uma associação útil para reconstruir o rótulo da pesquisa não significa que o movimento cause litigância predatória ou que exista uma regra jurídica de classificação automática.
"""),
    ("code", r"""
from sklearn.ensemble import RandomForestClassifier

_X_29 = _X_28.copy()
_cat_extra_29 = ['desfecho_categoria', 'resultado_recurso', 'classe_origem',
                 'extincao_iniciativa_autor', 'teve_acordo', 'classe_origem_inferida']
for _col_29 in _cat_extra_29:
    _X_29[_col_29] = _X_29[_col_29].astype('string').fillna('ausente').astype(str)
_X_29['assunto_grupo'] = np.where(_X_29['assunto_moldura'] == '6226', '6226', 'outros')
_X_29['assunto_grupo_x_desfecho'] = _X_29['assunto_grupo'] + ' | ' + _X_29['desfecho']
_cat_detalhe_29 = ['assunto_moldura'] + _cat_dj_28 + _cat_extra_29
_modelos_29 = {
    'logito detalhado': (_cat_detalhe_29, _num_dj_28, 'logito'),
    'logito com interação': (_cat_detalhe_29 + ['assunto_grupo_x_desfecho'], _num_dj_28, 'logito'),
    'floresta detalhada': (_cat_detalhe_29, _num_dj_28, 'floresta'),
}

def _fabrica_29(cat, num, familia, parametro):
    if familia == 'logito':
        return _modelo_28(cat, num, parametro)
    pre = ColumnTransformer([('categorias', OneHotEncoder(handle_unknown='ignore'), cat),
                             ('numericas', 'passthrough', num)])
    return make_pipeline(pre, RandomForestClassifier(n_estimators=200,
        min_samples_leaf=int(parametro), max_features='sqrt', random_state=20261030,
        n_jobs=1))

_previsoes_29 = {}
_linhas_29 = []
for _nome_29, (_cat_29, _num_29, _fam_29) in _modelos_29.items():
    _parametros_29 = (0.03, 0.3, 3.0) if _fam_29 == 'logito' else (5, 15, 30)
    _opcoes_29 = []
    for _param_29 in _parametros_29:
        _oof_29 = np.full(len(_tr_28), np.nan)
        _cv_29 = StratifiedKFold(n_splits=5, shuffle=True, random_state=20261030)
        for _aj_29, _val_29 in _cv_29.split(_tr_28, _y_28[_tr_28]):
            _m_29 = _fabrica_29(_cat_29, _num_29, _fam_29, _param_29)
            _m_29.fit(_X_29.iloc[_tr_28[_aj_29]], _y_28[_tr_28[_aj_29]])
            _oof_29[_val_29] = _m_29.predict_proba(_X_29.iloc[_tr_28[_val_29]])[:, 1]
        _opcoes_29.append((log_loss(_y_28[_tr_28], _oof_29, labels=[0, 1]), _param_29))
    _cv_loss_29, _melhor_29 = min(_opcoes_29)
    _m_29 = _fabrica_29(_cat_29, _num_29, _fam_29, _melhor_29)
    _m_29.fit(_X_29.iloc[_tr_28], _y_28[_tr_28])
    _p_29 = _m_29.predict_proba(_X_29.iloc[_te_28])[:, 1]
    _previsoes_29[_nome_29] = _p_29
    _linhas_29.append({'modelo': _nome_29, 'parâmetro escolhido': _melhor_29,
                       'log-loss CV 2022–2023': _cv_loss_29,
                       'AUC 2024': roc_auc_score(_yb_28, _p_29),
                       'precisão média 2024': average_precision_score(_yb_28, _p_29),
                       'log-loss 2024': log_loss(_yb_28, _p_29, labels=[0, 1]),
                       'Brier 2024': brier_score_loss(_yb_28, _p_29)})

TAB_DETALHE_29 = pd.concat([TAB_COMBINACAO_28.loc[
    TAB_COMBINACAO_28['informação'].eq('assunto da moldura'),
    ['informação', 'log-loss CV 2022–2023', 'AUC 2024', 'precisão média 2024',
     'log-loss 2024', 'Brier 2024']].rename(columns={'informação': 'modelo'}),
    pd.DataFrame(_linhas_29).drop(columns='parâmetro escolhido')], ignore_index=True)
display(tabela_ptbr(TAB_DETALHE_29, casas=4))

_escolhido_29 = min(_linhas_29, key=lambda d: d['log-loss CV 2022–2023'])['modelo']
_p_novo_29 = _previsoes_29[_escolhido_29]
_p_base_29 = _predicoes_28['assunto da moldura']
_rng_29 = np.random.default_rng(20261031)
_difs_29 = []
for _ in range(2000):
    _b_29 = np.r_[_rng_29.choice(_pos_28, len(_pos_28), replace=True),
                  _rng_29.choice(_neg_28, len(_neg_28), replace=True)]
    _difs_29.append({
        'AUC': roc_auc_score(_yb_28[_b_29], _p_novo_29[_b_29]) - roc_auc_score(_yb_28[_b_29], _p_base_29[_b_29]),
        'precisão média': average_precision_score(_yb_28[_b_29], _p_novo_29[_b_29]) - average_precision_score(_yb_28[_b_29], _p_base_29[_b_29]),
        'log-loss': log_loss(_yb_28[_b_29], _p_novo_29[_b_29], labels=[0, 1]) - log_loss(_yb_28[_b_29], _p_base_29[_b_29], labels=[0, 1]),
        'Brier': brier_score_loss(_yb_28[_b_29], _p_novo_29[_b_29]) - brier_score_loss(_yb_28[_b_29], _p_base_29[_b_29]),
    })
_difs_29 = pd.DataFrame(_difs_29)
_colunas_29 = {'AUC': 'AUC 2024', 'precisão média': 'precisão média 2024',
                'log-loss': 'log-loss 2024', 'Brier': 'Brier 2024'}
_tab_novo_29 = pd.DataFrame(_linhas_29).set_index('modelo')
_tab_base_29 = TAB_COMBINACAO_28.set_index('informação')
TAB_DIF_29 = pd.DataFrame([{'métrica': m,
    'diferença extensão − assunto': _tab_novo_29.loc[_escolhido_29, col] - _tab_base_29.loc['assunto da moldura', col],
    'limite inferior': _difs_29[m].quantile(.025), 'limite superior': _difs_29[m].quantile(.975)}
    for m, col in _colunas_29.items()])
print('Extensão escolhida apenas no desenvolvimento:', _escolhido_29)
display(tabela_ptbr(TAB_DIF_29, casas=4))

_sg_29 = _X_29.iloc[_te_28]['assunto_grupo'].to_numpy()
_subgrupos_29 = []
for _grupo_29 in ('6226', 'outros'):
    _idx_29 = np.flatnonzero(_sg_29 == _grupo_29)
    for _nome_29, _p_29 in [('assunto da moldura', _p_base_29), (_escolhido_29, _p_novo_29)]:
        _subgrupos_29.append({'assunto': _grupo_29, 'modelo': _nome_29,
            'processos': len(_idx_29), 'indícios': int(_yb_28[_idx_29].sum()),
            'log-loss': log_loss(_yb_28[_idx_29], _p_29[_idx_29], labels=[0, 1]),
            'Brier': brier_score_loss(_yb_28[_idx_29], _p_29[_idx_29])})
TAB_SUBGRUPOS_29 = pd.DataFrame(_subgrupos_29)
display(tabela_ptbr(TAB_SUBGRUPOS_29, casas=4))
"""),
    ("markdown", r"""
**Leitura das tabelas.** O melhor resultado de validação cruzada em 2022–2023 escolhe apenas uma extensão antes de comparar com o assunto em 2024. Na tabela de diferenças, AUC e precisão média maiores favorecem a extensão; perda logarítmica e Brier menores a favorecem. O intervalo bootstrap que inclui zero indica que o conjunto de 2024 não sustenta uma direção estável para a diferença. A tabela por assunto mostra se o eventual ganho está concentrado no código 6226 ou aparece também nos demais; ela é descritiva e tem poucos positivos em cada parte.

Essas comparações procuram **associação retrospectiva com o rótulo operacional da pesquisa**, não um diagnóstico jurídico independente. Variáveis como quantidade de movimentos, desfecho e recurso também refletem o tempo de acompanhamento e práticas de registro. A escolha entre modelos deve considerar simultaneamente discriminação, probabilidades e estabilidade, sem interpretar uma melhoria pontual como validação para uso operacional.
"""),
    ("code", r"""
# 29.1 Conclusão numérica da seção
_ref29 = TAB_DETALHE_29.set_index('modelo').loc['assunto da moldura']
_ext29 = TAB_DETALHE_29.set_index('modelo').loc[_escolhido_29]
_d29 = TAB_DIF_29.set_index('métrica')
_cruza29 = [m for m in _d29.index if _d29.loc[m, 'limite inferior'] < 0 < _d29.loc[m, 'limite superior']]
_melhor_cv29 = TAB_DETALHE_29.loc[TAB_DETALHE_29['log-loss CV 2022–2023'].idxmin(), 'modelo']
display(Markdown(
    f"**Conclusão.** No desenvolvimento (2022–2023), o menor log-loss de validação cruzada é o de **{_melhor_cv29}** "
    f"({fnum(TAB_DETALHE_29['log-loss CV 2022–2023'].min(), 4)}); a melhor extensão, **{_escolhido_29}**, tem "
    f"{fnum(_ext29['log-loss CV 2022–2023'], 4)}, contra {fnum(_ref29['log-loss CV 2022–2023'], 4)} do assunto sozinho. "
    f"Em 2024, a extensão tem AUC {fnum(_ext29['AUC 2024'], 3)} e log-loss {fnum(_ext29['log-loss 2024'], 4)}, "
    f"contra {fnum(_ref29['AUC 2024'], 3)} e {fnum(_ref29['log-loss 2024'], 4)} do assunto. "
    f"Os intervalos bootstrap pareados cruzam zero em {len(_cruza29)} de {len(_d29)} métricas ({', '.join(_cruza29) or 'nenhuma'}). "
    "**O desfecho detalhado, o recurso e a interação com o assunto não acrescentam informação estável ao assunto da moldura.**"))
"""),
]
