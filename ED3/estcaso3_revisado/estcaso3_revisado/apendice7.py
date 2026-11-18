"""Sensibilidade retrospectiva com a sequência de movimentos TPU."""

BLOCKS = [
    ("markdown", r"""
## 30. O início e a variedade dos movimentos TPU acrescentam informação?

O DataJud fornece, para cada movimento, **código TPU, nome, data/hora, órgão e complementos tabelados**. O nome é uma descrição do código; usá-los simultaneamente como preditores duplicaria a informação. O arquivo coletado **não contém uma contagem de arquivos anexados**: `n_complementos` conta campos estruturados que detalham o movimento e não deve ser apresentado como número de petições ou documentos.

Para cada processo vinculado, ordenamos os movimentos do documento de entrada e retiramos a distribuição (código 26), comum ao fluxo. Extraímos os códigos dos três movimentos seguintes, o número de tipos distintos na trajetória e a quantidade de complementos nos cinco primeiros movimentos restantes. Assim podemos testar um resumo do começo e outro de toda a sequência, sem inventar uma variável de anexos. O mesmo código pode aparecer repetidas vezes; a posição é calculada depois da normalização que remove repetições idênticas e ordena por data. O DataJud é um retrato da coleta, e esses campos só descrevem a trajetória disponível nesse retrato.

Comparamos assunto sozinho, assunto com os primeiros movimentos, assunto com resumo completo da sequência e assunto com todas as variáveis retrospectivas anteriores mais os movimentos. A regularização é escolhida em 2022–2023; 2024 serve apenas à comparação exploratória já discutida. O teste pergunta se os movimentos **ajudam a reproduzir o rótulo de indício da pesquisa**, não se identificam a condição jurídica independentemente das regras F2/F3.
"""),
    ("code", r"""
_mov_30 = tab_dj['movimentos'].merge(_X_28[['numero', 'grau_entrada']],
    on='numero', how='inner', validate='many_to_one')
_mov_30 = _mov_30.loc[_mov_30['grau'].eq(_mov_30['grau_entrada'])].copy()
_mov_30 = _mov_30.sort_values(['numero', 'data_hora', 'seq'], na_position='last')
_mov_30 = _mov_30.loc[_mov_30['codigo'].ne(26).fillna(False)].copy()
_mov_30['posicao'] = _mov_30.groupby('numero').cumcount()
_primeiros_30 = _mov_30.loc[_mov_30.posicao.lt(3), ['numero', 'posicao', 'codigo']].copy()
_primeiros_30['codigo'] = _primeiros_30.codigo.astype('string')
_primeiros_30 = _primeiros_30.pivot(index='numero', columns='posicao', values='codigo')
_primeiros_30 = _primeiros_30.rename(columns={i: f'codigo_pos_{i+1}' for i in range(3)})
_primeiros_30 = _primeiros_30.reindex(columns=[f'codigo_pos_{i}' for i in (1, 2, 3)])
_resumo_30 = _mov_30.groupby('numero').agg(tipos_movimento=('codigo', 'nunique'),
    movimentos_sem_distribuicao=('codigo', 'size'))
_comp_30 = (_mov_30.loc[_mov_30.posicao.lt(5)].groupby('numero')['n_complementos']
            .sum().rename('complementos_primeiros5'))
_resumo_30 = _resumo_30.join(_comp_30)
_X_30 = _X_29.merge(_primeiros_30, left_on='numero', right_index=True, how='left', validate='one_to_one')
_X_30 = _X_30.merge(_resumo_30, left_on='numero', right_index=True, how='left', validate='one_to_one')
assert len(_X_30) == 593 and _X_30.numero.is_unique
_codigos_30 = [f'codigo_pos_{i}' for i in (1, 2, 3)]
for _col_30 in _codigos_30:
    _X_30[_col_30] = _X_30[_col_30].astype('string').fillna('ausente').astype(str)
_numericos_30 = ['tipos_movimento', 'movimentos_sem_distribuicao', 'complementos_primeiros5']
for _col_30 in _numericos_30:
    _X_30[_col_30] = np.log1p(_X_30[_col_30].fillna(0).astype(float))

_nomes_30 = (_mov_30[['codigo', 'nome_tpu']].dropna().drop_duplicates('codigo')
             .set_index('codigo')['nome_tpu'])
_top_30 = (_mov_30.loc[_mov_30.posicao.eq(0), 'codigo'].value_counts().head(10)
           .rename_axis('código TPU').rename('processos').reset_index())
_top_30['nome TPU'] = _top_30['código TPU'].map(_nomes_30)
display(_top_30[['código TPU', 'nome TPU', 'processos']])
print('Processos sem movimento após a distribuição:',
      int(_X_30['codigo_pos_1'].eq('ausente').sum()))

_modelos_30 = {
    'assunto + primeiros códigos': (['assunto_moldura'] + _codigos_30, []),
    'assunto + sequência resumida': (['assunto_moldura'] + _codigos_30, _numericos_30),
    'assunto + trajetória + sequência': (_cat_detalhe_29 + _codigos_30,
                                         _num_dj_28 + _numericos_30),
}
_linhas_30 = []
_previsoes_30 = {}
for _nome_30, (_cat_30, _num_30) in _modelos_30.items():
    _opcoes_30 = []
    for _c_30 in (0.03, 0.3, 3.0):
        _oof_30 = np.full(len(_tr_28), np.nan)
        _cv_30 = StratifiedKFold(n_splits=5, shuffle=True, random_state=20261030)
        for _aj_30, _val_30 in _cv_30.split(_tr_28, _y_28[_tr_28]):
            _m_30 = _modelo_28(_cat_30, _num_30, _c_30)
            _m_30.fit(_X_30.iloc[_tr_28[_aj_30]], _y_28[_tr_28[_aj_30]])
            _oof_30[_val_30] = _m_30.predict_proba(_X_30.iloc[_tr_28[_val_30]])[:, 1]
        _opcoes_30.append((log_loss(_y_28[_tr_28], _oof_30, labels=[0, 1]), _c_30))
    _cv_loss_30, _melhor_c_30 = min(_opcoes_30)
    _m_30 = _modelo_28(_cat_30, _num_30, _melhor_c_30)
    _m_30.fit(_X_30.iloc[_tr_28], _y_28[_tr_28])
    _p_30 = _m_30.predict_proba(_X_30.iloc[_te_28])[:, 1]
    _previsoes_30[_nome_30] = _p_30
    _linhas_30.append({'modelo': _nome_30, 'C escolhido': _melhor_c_30,
        'log-loss CV 2022–2023': _cv_loss_30,
        'AUC 2024': roc_auc_score(_yb_28, _p_30),
        'precisão média 2024': average_precision_score(_yb_28, _p_30),
        'log-loss 2024': log_loss(_yb_28, _p_30, labels=[0, 1]),
        'Brier 2024': brier_score_loss(_yb_28, _p_30)})
TAB_MOVIMENTOS_30 = pd.DataFrame(_linhas_30)
display(tabela_ptbr(TAB_MOVIMENTOS_30, casas=4))
print('Referência assunto sozinho: log-loss CV 2022–2023 =',
      round(float(_tab_base_29.loc['assunto da moldura', 'log-loss CV 2022–2023']), 4),
      '; log-loss 2024 =', round(float(_tab_base_29.loc['assunto da moldura', 'log-loss 2024']), 4))
"""),
    ("markdown", r"""
**Como interpretar.** Compare primeiro a perda logarítmica da validação cruzada com a referência de assunto sozinho: ela mede se a extensão acrescentou informação no período de desenvolvimento, sem usar 2024 para escolher os parâmetros. As colunas de 2024 mostram se a direção se manteve na avaliação temporal exploratória. Os nomes TPU exibidos são rótulos interpretáveis dos códigos mais frequentes na primeira posição após a distribuição; um código frequente pode ser apenas uma rotina cartorária. A contagem de complementos não mede anexos. Qualquer ganho localizado exige examinar a qualidade do registro e o tempo de acompanhamento antes de receber interpretação substantiva.
"""),
    ("code", r"""
# 30.1 Conclusão numérica: variável degenerada e comparação pareada da melhor extensão com o assunto
_n_pos1 = _X_30['codigo_pos_1'].value_counts()
_frac_pos1 = float(_n_pos1.iloc[0] / len(_X_30))
_ref30 = _tab_base_29.loc['assunto da moldura']
_melhor30 = TAB_MOVIMENTOS_30.loc[TAB_MOVIMENTOS_30['log-loss CV 2022–2023'].idxmin()]
_p_m30 = _previsoes_30[_melhor30['modelo']]
_rng_30 = np.random.default_rng(20261032)
_dif30 = []
for _ in range(2000):
    _b30 = np.r_[_rng_30.choice(_pos_28, len(_pos_28), replace=True), _rng_30.choice(_neg_28, len(_neg_28), replace=True)]
    _dif30.append({'AUC': roc_auc_score(_yb_28[_b30], _p_m30[_b30]) - roc_auc_score(_yb_28[_b30], _p_base_29[_b30]),
                   'log-loss': log_loss(_yb_28[_b30], _p_m30[_b30], labels=[0, 1]) -
                               log_loss(_yb_28[_b30], _p_base_29[_b30], labels=[0, 1])})
_dif30 = pd.DataFrame(_dif30)
TAB_DIF_30 = pd.DataFrame([{'métrica': m, 'diferença melhor extensão − assunto':
                            _melhor30[f'{m} 2024'] - _ref30[f'{m} 2024'],
                            'limite inferior': _dif30[m].quantile(.025), 'limite superior': _dif30[m].quantile(.975)}
                           for m in ('AUC', 'log-loss')])
display(tabela_ptbr(TAB_DIF_30, casas=4))
_ganho_cv30 = _ref30['log-loss CV 2022–2023'] - _melhor30['log-loss CV 2022–2023']
display(Markdown(
    f"**Conclusão.** O primeiro movimento após a distribuição é o código {_n_pos1.index[0]} em "
    f"{fpct(_frac_pos1, 1)} dos processos: essa posição **não carrega informação** e funciona como constante. "
    f"A melhor extensão no desenvolvimento, **{_melhor30['modelo']}**, tem log-loss de validação cruzada "
    f"{fnum(_melhor30['log-loss CV 2022–2023'], 4)}, contra {fnum(_ref30['log-loss CV 2022–2023'], 4)} do assunto sozinho "
    f"({'melhora' if _ganho_cv30 > 0 else 'piora'} de {fnum(abs(_ganho_cv30), 4)}). Em 2024, a diferença de log-loss é "
    f"{fnum(TAB_DIF_30.iloc[1, 1], 4)} {fic(TAB_DIF_30.iloc[1, 2], TAB_DIF_30.iloc[1, 3], casas=4)} e a de AUC, "
    f"{fnum(TAB_DIF_30.iloc[0, 1], 4)} {fic(TAB_DIF_30.iloc[0, 2], TAB_DIF_30.iloc[0, 3], casas=4)}. "
    "**A sequência de movimentos TPU não melhora de forma estável a reprodução do rótulo de indício além do assunto.** "
    "As Seções 22 e 28–30 chegam, portanto, à mesma resposta: depois do assunto, os registros administrativos do DataJud "
    "não acrescentam sinal útil."))
"""),
]
