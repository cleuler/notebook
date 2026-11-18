"""Comparação exploratória da previsão no ajuizamento."""

BLOCKS = [
    ("markdown", r"""
## 24. Previsão de indício no ajuizamento

As análises anteriores descrevem sinais encontrados na leitura dos autos e trajetórias processuais. Aqui a pergunta muda: **quanto se consegue antecipar no ajuizamento, antes de conhecer o desfecho?** A resposta é o indício em sentido amplo, definido na pesquisa por F3_19 e F3_20 e incluindo os casos de certeza. O assunto, o juizado e o mês são os únicos preditores desta comparação. O assunto é lido da moldura do TJRN, vinculada aos mesmos processos da amostra. A classe não entra porque pode mudar. Desfecho, duração e movimentos posteriores também ficam fora.

Os 405 casos de 2022–2023 ajustam os modelos e os 190 de 2024 avaliam as probabilidades. Todas as linhas da tabela usam **a mesma resposta, as mesmas observações e a mesma divisão temporal**. AUC resume a ordenação, precisão média resume a curva precisão–revocação e perda logarítmica avalia as probabilidades. Menor perda é melhor; para as outras duas métricas, maior é melhor. A prevalência de indício no teste é 28/190, de modo que a precisão média precisa ser lida junto com essa frequência.

Esta comparação é exploratória: o ano de 2024 já foi examinado durante o desenvolvimento do estudo, e o rótulo representa a regra operacional da pesquisa, não um diagnóstico jurídico independente. Uma coorte futura, ainda não usada na escolha dos modelos, será necessária para validar o desempenho.
"""),
    ("code", r"""
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, average_precision_score, log_loss, confusion_matrix

_entrada = am[['numero', 'ano', 'jec', 'indicio', 'certeza']].merge(
    base[['NÚMERO PROCESSO', 'CÓD ASSUNTO', 'DATA INÍCIO']].rename(columns={'NÚMERO PROCESSO': 'numero'}),
    on='numero', how='left', validate='one_to_one', indicator=True)
assert len(_entrada) == 595 and (_entrada['_merge'] == 'both').all()
_entrada['assunto'] = _entrada['CÓD ASSUNTO'].fillna('AUSENTE').astype(str)
_entrada['jec_txt'] = _entrada.jec.astype(str)
_entrada['mes'] = pd.to_datetime(_entrada['DATA INÍCIO'], format='%d-%m-%Y %H:%M:%S').dt.month.astype(str)
_entrada['assunto_6226'] = np.where(_entrada.assunto.eq('6226'), 'sim', 'não')
_tr_e = _entrada.ano.astype(int).to_numpy() < 2024
_te_e = ~_tr_e
_y_e = _entrada.indicio.astype(int).to_numpy()
assert (int(_tr_e.sum()), int(_te_e.sum()), int(_y_e.sum()), int(_y_e[_te_e].sum())) == (405, 190, 105, 28)

_alternativas = [
    ('frequência do treino', [], DummyClassifier(strategy='prior')),
    ('juizado + mês', ['jec_txt', 'mes'], LogisticRegression(C=0.3, max_iter=3000)),
    ('assunto 6226', ['assunto_6226'], LogisticRegression(C=0.3, max_iter=3000)),
    ('regressão logística com assunto', ['assunto'], LogisticRegression(C=0.3, max_iter=3000)),
    ('regressão logística com assunto + juizado + mês', ['assunto', 'jec_txt', 'mes'],
     LogisticRegression(C=0.3, max_iter=3000)),
    ('floresta aleatória com assunto', ['assunto'],
     RandomForestClassifier(n_estimators=300, min_samples_leaf=8, max_features=0.7,
                            random_state=43, n_jobs=1)),
]
_resultados_e, _prob_e = [], {}
for _nome, _campos, _estimador in _alternativas:
    if _campos:
        _x_e = _entrada[_campos]
        _modelo_e = make_pipeline(OneHotEncoder(handle_unknown='ignore'), _estimador)
        _modelo_e.fit(_x_e.loc[_tr_e], _y_e[_tr_e])
        _p_e = _modelo_e.predict_proba(_x_e.loc[_te_e])[:, 1]
    else:
        _modelo_e = _estimador.fit(np.zeros((_tr_e.sum(), 1)), _y_e[_tr_e])
        _p_e = _modelo_e.predict_proba(np.zeros((_te_e.sum(), 1)))[:, 1]
    _prob_e[_nome] = _p_e
    _resultados_e.append({'modelo': _nome, 'AUC 2024': roc_auc_score(_y_e[_te_e], _p_e),
                          'precisão média 2024': average_precision_score(_y_e[_te_e], _p_e),
                          'perda logarítmica 2024': log_loss(_y_e[_te_e], _p_e)})
_tabela_e = pd.DataFrame(_resultados_e)
display(tabela_ptbr(_tabela_e, casas=3))

_p_assunto = _prob_e['regressão logística com assunto']
_cm_e = confusion_matrix(_y_e[_te_e], _p_assunto >= 0.5, labels=[0, 1])
_top_e = np.argsort(-_p_assunto)[:38]
_cert_e = _entrada.certeza.astype(int).to_numpy()[_te_e]
display(pd.DataFrame(_cm_e, index=['sem indício na pesquisa', 'indício na pesquisa'],
                     columns=['escore < 0,5', 'escore ≥ 0,5']))
display(pd.DataFrame([{'recorte': '38 maiores escores de 2024',
                       'indícios encontrados': int(_y_e[_te_e][_top_e].sum()),
                       'indícios em 2024': int(_y_e[_te_e].sum()),
                       'certezas encontradas': int(_cert_e[_top_e].sum()),
                       'certezas em 2024': int(_cert_e.sum())}]))
assert (_cm_e == np.array([[153, 9], [11, 17]])).all()
assert int(_y_e[_te_e][_top_e].sum()) == 22
"""),
    ("markdown", r"""
O resultado mais alto da tabela é da **regressão logística com assunto**: AUC 0,859, precisão média 0,563 e perda logarítmica 0,293. Entre os 38 maiores escores de 2024 estão 22 dos 28 indícios e 9 dos 10 casos classificados como certeza. No limiar 0,5, há 17 verdadeiros positivos, 9 falsos positivos, 11 falsos negativos e 153 verdadeiros negativos. Esses números descrevem a reprodução do rótulo da pesquisa; não significam que o modelo tenha examinado a petição ou demonstrado predação.

O ganho depende muito do **assunto 6226**, “Inclusão Indevida em Cadastro de Inadimplentes”: ele concentra 74 dos 105 indícios dos 595 processos. A regra simples baseada somente nesse assunto produz a mesma matriz no limiar 0,5. A regressão com todos os assuntos ordena melhor os casos, mas isso ainda precisa ser confirmado em novos processos. Juizado e mês não melhoraram o resultado de 2024; a floresta aleatória também ficou abaixo da regressão simples. Como havia apenas 20 certezas no treino e 10 em 2024, o bom ranqueamento de alguns desses casos não autoriza classificá-los como “certeza” no ajuizamento.

**Qual número citar.** A regularização C = 0,3 desta tabela foi fixada na exploração, e não escolhida nos dados de desenvolvimento. A Seção 26 refaz a escolha por validação cruzada aninhada apenas em 2022–2023 e congela o modelo antes de olhar 2024. **A AUC de referência do modelo de assunto é a da Seção 26.** A Seção 31 usa a mesma informação de outro modo: o assunto como informação auxiliar para estimar a prevalência na moldura.
"""),
]
