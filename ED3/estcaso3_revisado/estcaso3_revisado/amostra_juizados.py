"""Diagnóstico da representação dos 14 JEC no sorteio por ano."""

BLOCKS_DESENHO = [
    ("markdown", r"""
### 2.4 Os juizados ficaram proporcionais na amostra?

A pesquisa sorteou processos **por ano**, sem fixar quantos viriam de cada juizado. Isso não é, por si só, um erro: se o sorteio dentro de cada ano for aleatório, a participação de cada JEC oscila em torno de sua participação na moldura. A comparação correta usa os **50.320 processos da Base consolidada**, pois foi dela que saíram os 595 sorteados. Os registros do DataJud são examinados depois, como verificação da cobertura dessa mesma moldura.

Para cada ano e JEC, calculamos a contagem esperada `n_ano × N_ano,jec/N_ano`. Somamos as contagens esperadas dos três anos e confrontamos com as observadas. A simulação repete 20.000 sorteios sem reposição, mantendo os tamanhos de amostra de 2022, 2023 e 2024 e a composição real de cada ano. Ela fornece um teste global dos 14 JEC e outro das 42 combinações ano × JEC. Para localizar desvios individuais sem selecionar um juizado depois de olhar os dados, o valor de p ajustado usa o **maior desvio padronizado** de cada réplica.
"""),
    ("code", r"""
def diagnosticar_juizados(moldura, sorteio, *, semente=20261029, replicas=20000):
    '''Compara JEC de origem, condicionando o sorteio aos tamanhos por ano.'''
    jecs = list(range(1, 15))
    N = moldura.groupby(['ano', 'jec']).size().unstack(fill_value=0).reindex(columns=jecs, fill_value=0)
    O = sorteio.groupby(['ano', 'jec']).size().unstack(fill_value=0).reindex(index=N.index, columns=jecs, fill_value=0)
    Nh, nh = N.sum(axis=1), O.sum(axis=1)
    P = N.div(Nh, axis=0)
    E_ano = P.mul(nh, axis=0)
    E, observado = E_ano.sum(axis=0).to_numpy(), O.sum(axis=0).to_numpy()
    V = (P.mul(1 - P).mul(nh * (Nh - nh) / (Nh - 1), axis=0)).sum(axis=0).to_numpy()
    z = (observado - E) / np.sqrt(V)
    rng = np.random.default_rng(semente)
    sim_total = np.zeros((replicas, 14), dtype=int)
    sim_estratos = np.zeros(replicas)
    anos = []
    for ano in N.index:
        simulados = rng.multivariate_hypergeometric(N.loc[ano].to_numpy(), int(nh.loc[ano]), size=replicas)
        sim_total += simulados
        e_ano = E_ano.loc[ano].to_numpy()
        estat = float(((O.loc[ano].to_numpy() - e_ano) ** 2 / e_ano).sum())
        estat_sim = ((simulados - e_ano) ** 2 / e_ano).sum(axis=1)
        sim_estratos += estat_sim
        anos.append({'ano': int(ano), 'n': int(nh.loc[ano]), 'qui-quadrado': estat,
                     'p por sorteio': (1 + int((estat_sim >= estat).sum())) / (replicas + 1)})
    estat_global = float((((observado - E) ** 2) / E).sum())
    estat_sim_global = ((sim_total - E) ** 2 / E).sum(axis=1)
    estat_estratos = float((((O.to_numpy() - E_ano.to_numpy()) ** 2) / E_ano.to_numpy()).sum())
    max_sim = np.max(np.abs((sim_total - E) / np.sqrt(V)), axis=1)
    tabela = pd.DataFrame({'JEC': jecs, 'N da referência': N.sum(axis=0).to_numpy(),
                           'n da amostra': observado, 'n esperado': E,
                           '% referência': N.sum(axis=0).to_numpy() / Nh.sum(),
                           '% amostra': observado / nh.sum(),
                           'diferença (p.p.)': 100 * (observado / nh.sum() - N.sum(axis=0).to_numpy() / Nh.sum()),
                           'desvio padronizado': z,
                           'p ajustado (14 JEC)': [(1 + int((max_sim >= abs(v)).sum())) / (replicas + 1) for v in z]})
    resumo = {'N': int(Nh.sum()), 'n': int(nh.sum()), 'estatística global': estat_global,
              'p global': (1 + int((estat_sim_global >= estat_global).sum())) / (replicas + 1),
              'estatística ano × JEC': estat_estratos,
              'p ano × JEC': (1 + int((sim_estratos >= estat_estratos).sum())) / (replicas + 1)}
    return tabela, pd.DataFrame(anos), resumo

_base_jec = base.rename(columns={'ano_inicio': 'ano'})[['ano', 'jec']].copy()
_am_jec = am[['ano', 'jec']].copy()
TAB_JEC, ANOS_JEC, RES_JEC = diagnosticar_juizados(_base_jec, _am_jec)
assert (RES_JEC['N'], RES_JEC['n']) == (50320, 595)
assert int(TAB_JEC.loc[TAB_JEC.JEC == 2, 'n da amostra'].iloc[0]) == 55
display(tabela_ptbr(TAB_JEC, casas=3, pct=['% referência', '% amostra'], p=['p ajustado (14 JEC)']))
display(tabela_ptbr(ANOS_JEC, casas=3, p=['p por sorteio']))
display(pd.Series(RES_JEC, name='sorteio por ano, sem cotas por JEC').to_frame())

fig, ax = plt.subplots(figsize=(10, 4.2))
ax.bar(TAB_JEC.JEC - 0.18, 100 * TAB_JEC['% amostra'], width=0.36, label='amostra')
ax.bar(TAB_JEC.JEC + 0.18, 100 * TAB_JEC['% referência'], width=0.36, label='moldura TJRN')
ax.set(xlabel='juizado de origem', ylabel='% de processos', xticks=TAB_JEC.JEC,
       title='Participação dos JEC: amostra × moldura da qual foi sorteada')
ax.legend(); fig.tight_layout()
fig.savefig(FIGURAS / 'amostra_juizados_moldura.png', dpi=150)
plt.show()
"""),
    ("markdown", r"""
**Leitura da moldura.** Os juizados têm participações próximas de 7% na população depurada. O 2º JEC é o maior excesso na amostra: 55 casos, contra aproximadamente 42 esperados; sua participação passa de 7,06% na moldura a 9,24% na amostra. O 5º tem 33 casos, contra aproximadamente 42 esperados. Considerados todos os juizados e os anos do sorteio, as diferenças são compatíveis com a oscilação de uma amostra desse tamanho: o teste global por simulação resulta em **p ≈ 0,79** e o teste das combinações ano × JEC em **p ≈ 0,97**. Nenhum juizado se destaca após considerar as 14 comparações; para o 2º, o p ajustado é aproximadamente 0,40.

Isso **não prova ausência de viés** nem recupera a semente do sorteio original. Mostra que os números realizados não dão evidência de uma distorção por juizado. Sem cotas por JEC, há menos controle da precisão de estimativas **de cada juizado isoladamente**: aqui cada unidade contribuiu com aproximadamente 33 a 55 processos.
"""),
    ("markdown", r"""
### 2.4.1 A interseção entre ano e juizado

Uma distribuição próxima da população no total dos três anos poderia esconder excessos em um ano compensados por faltas em outro. Por isso, a tabela seguinte abre as **42 células**: para cada ano e JEC, mostra quantos processos havia na população elegível, quantos vieram para a amostra, quantos seriam esperados sob sorteio aleatório dentro do ano e as duas participações **dentro daquele mesmo ano**. A diferença em pontos percentuais compara essas participações, sem misturar os tamanhos de 2022, 2023 e 2024.

O mapa facilita localizar excessos e faltas. Para que um destaque visual entre 42 células não seja confundido com evidência de viés, simulamos novamente 20.000 sorteios com os três tamanhos anuais fixos e comparamos cada desvio padronizado com o **maior desvio de todas as 42 células** em cada réplica. O valor de p ajustado responde à busca pelo caso mais discrepante; os testes globais por ano e para as 42 células foram apresentados acima.
"""),
    ("code", r"""
_N_cruzado = _base_jec.groupby(['ano', 'jec']).size().unstack(fill_value=0).reindex(columns=range(1, 15))
_O_cruzado = _am_jec.groupby(['ano', 'jec']).size().unstack(fill_value=0).reindex(
    index=_N_cruzado.index, columns=_N_cruzado.columns, fill_value=0)
_N_anuais = _N_cruzado.sum(axis=1)
_n_anuais = _O_cruzado.sum(axis=1)
_p_cruzado = _N_cruzado.div(_N_anuais, axis=0)
_E_cruzado = _p_cruzado.mul(_n_anuais, axis=0)
_var_cruzado = _p_cruzado.mul(1 - _p_cruzado).mul(
    _n_anuais * (_N_anuais - _n_anuais) / (_N_anuais - 1), axis=0)
_z_cruzado = (_O_cruzado - _E_cruzado) / np.sqrt(_var_cruzado)
_dif_cruzado = 100 * (_O_cruzado.div(_n_anuais, axis=0) - _p_cruzado)
_rng_cruzado = np.random.default_rng(20261030)
_max_desvio_simulado = np.zeros(20000)
for _ano_cruzado in _N_cruzado.index:
    _sorteios = _rng_cruzado.multivariate_hypergeometric(
        _N_cruzado.loc[_ano_cruzado].to_numpy(), int(_n_anuais.loc[_ano_cruzado]), size=20000)
    _z_sorteios = np.abs((_sorteios - _E_cruzado.loc[_ano_cruzado].to_numpy()) /
                        np.sqrt(_var_cruzado.loc[_ano_cruzado].to_numpy()))
    _max_desvio_simulado = np.maximum(_max_desvio_simulado, _z_sorteios.max(axis=1))

_linhas_cruzadas = []
for _ano_cruzado in _N_cruzado.index:
    for _jec_cruzado in _N_cruzado.columns:
        _z = float(_z_cruzado.loc[_ano_cruzado, _jec_cruzado])
        _linhas_cruzadas.append({
            'ano': int(_ano_cruzado), 'JEC': int(_jec_cruzado),
            'N elegível': int(_N_cruzado.loc[_ano_cruzado, _jec_cruzado]),
            'n sorteado': int(_O_cruzado.loc[_ano_cruzado, _jec_cruzado]),
            'n esperado': float(_E_cruzado.loc[_ano_cruzado, _jec_cruzado]),
            '% elegível no ano': float(_p_cruzado.loc[_ano_cruzado, _jec_cruzado]),
            '% amostra no ano': float(_O_cruzado.loc[_ano_cruzado, _jec_cruzado] / _n_anuais.loc[_ano_cruzado]),
            'diferença (p.p.)': float(_dif_cruzado.loc[_ano_cruzado, _jec_cruzado]),
            'desvio padronizado': _z,
            'p ajustado (42 células)': (1 + int((_max_desvio_simulado >= abs(_z)).sum())) / 20001,
        })
TAB_ANO_JEC = pd.DataFrame(_linhas_cruzadas)
assert len(TAB_ANO_JEC) == 42 and TAB_ANO_JEC['n sorteado'].sum() == 595
assert TAB_ANO_JEC['n sorteado'].min() == 10 and TAB_ANO_JEC['n sorteado'].max() == 20
display(tabela_ptbr(TAB_ANO_JEC, casas=3,
                    pct=['% elegível no ano', '% amostra no ano'], p=['p ajustado (42 células)']))

_extremo = TAB_ANO_JEC.loc[TAB_ANO_JEC['desvio padronizado'].abs().idxmax()]
_resumo_cruzado = pd.DataFrame([{
    'ano': int(_extremo['ano']), 'JEC': int(_extremo['JEC']),
    'maior desvio padronizado': float(abs(_extremo['desvio padronizado'])),
    'p ajustado para buscar entre 42': float(_extremo['p ajustado (42 células)']),
    'p global das 42 células': RES_JEC['p ano × JEC'],
}])
display(tabela_ptbr(_resumo_cruzado, casas=3,
                    p=['p ajustado para buscar entre 42', 'p global das 42 células']))

fig, ax = plt.subplots(figsize=(13, 3.8))
_escala = max(3.0, float(np.abs(_dif_cruzado.to_numpy()).max()))
_imagem = ax.imshow(_dif_cruzado.to_numpy(), cmap='RdBu_r', vmin=-_escala, vmax=_escala, aspect='auto')
for _i, _ano_cruzado in enumerate(_N_cruzado.index):
    for _j, _jec_cruzado in enumerate(_N_cruzado.columns):
        ax.text(_j, _i, f'{int(_O_cruzado.loc[_ano_cruzado, _jec_cruzado])}/'
                f'{_E_cruzado.loc[_ano_cruzado, _jec_cruzado]:.1f}',
                ha='center', va='center', fontsize=7)
ax.set(xticks=np.arange(14), xticklabels=list(_N_cruzado.columns),
       yticks=np.arange(len(_N_cruzado)), yticklabels=list(_N_cruzado.index),
       xlabel='juizado', ylabel='ano',
       title='Ano × JEC: diferença de participação (amostra − população elegível)')
fig.colorbar(_imagem, ax=ax, label='diferença em pontos percentuais')
fig.tight_layout()
fig.savefig(FIGURAS / 'amostra_ano_juizado_intersecao.png', dpi=150)
plt.show()
"""),
    ("markdown", r"""
**Leitura da interseção.** A amostra tem **194 processos de 2022, 211 de 2023 e 190 de 2024**. Cada combinação ano × JEC contribui com **10 a 20 processos**. Os testes globais por ano ficam aproximadamente em **p = 0,79 (2022), 0,78 (2023) e 0,92 (2024)**; o teste conjunto das 42 células dá **p ≈ 0,97**. O maior desvio padronizado é o 2º JEC em 2023: **20 sorteados contra 14,5 esperados**. Ao considerar que se procurou o maior desvio entre 42 células, seu p ajustado fica aproximadamente em **0,997**. Assim, não aparece um desequilíbrio escondido em um ano que a tabela agregada tivesse cancelado.

Os valores de p testam compatibilidade com o sorteio aleatório por ano; não provam equivalência exata nem corrigem eventuais falhas da planilha original. Em especial, 10 a 20 casos por célula bastam para inspecionar a distribuição do sorteio, mas são poucos para estimar com precisão a taxa de indício em cada combinação de ano e juizado.
"""),
    ("markdown", r"""
### 2.5 O desbalanceamento observado altera a estimativa de indício?

O teste anterior pergunta se as contagens por juizado são plausíveis sob o sorteio. Para medir o possível efeito sobre o resultado substantivo, ajustamos a amostra às proporções conhecidas das **42 combinações ano × JEC** da moldura. Cada processo recebe peso `N_ano,jec/n_ano,jec`; todas as células têm observações, mas algumas são pequenas. Comparamos a proporção simples, a estimativa estratificada somente por ano e a estimativa pós-estratificada por ano e juizado. Essa é uma análise de sensibilidade da estimativa agregada, não uma substituição automática do desenho original.
"""),
    ("code", r"""
_N_ano_jec = base.groupby(['ano_inicio', 'jec']).size().rename('N_celula')
_n_ano_jec = am.groupby(['ano', 'jec']).size().rename('n_celula')
_pesos_jec = am[['ano', 'jec', 'indicio', 'certeza']].copy()
_pesos_jec = _pesos_jec.join(_N_ano_jec, on=['ano', 'jec']).join(_n_ano_jec, on=['ano', 'jec'])
assert _pesos_jec[['N_celula', 'n_celula']].notna().all().all()
_pesos_jec['peso_ano_jec'] = _pesos_jec.N_celula / _pesos_jec.n_celula
assert np.isclose(_pesos_jec.peso_ano_jec.sum(), len(base))
_N_ano = base.groupby('ano_inicio').size().rename('N_ano')
_n_ano = am.groupby('ano').size().rename('n_ano')
_pesos_jec = _pesos_jec.join(_N_ano, on='ano').join(_n_ano, on='ano')
_pesos_jec['peso_ano'] = _pesos_jec.N_ano / _pesos_jec.n_ano
_linhas_impacto = []
for _rotulo, _coluna in [('indício', 'indicio'), ('certeza', 'certeza')]:
    _y = _pesos_jec[_coluna].astype(int)
    _simples = float(_y.mean())
    _estrat = float(np.average(_y, weights=_pesos_jec.peso_ano))
    _pos = float(np.average(_y, weights=_pesos_jec.peso_ano_jec))
    _linhas_impacto.append({'categoria': _rotulo, 'proporção simples': _simples,
                            'ajuste por ano': _estrat, 'ajuste por ano × JEC': _pos,
                            'mudança ante ajuste por ano (p.p.)': 100 * (_pos - _estrat)})
TAB_IMPACTO_JEC = pd.DataFrame(_linhas_impacto)
display(tabela_ptbr(TAB_IMPACTO_JEC, casas=3,
                    pct=['proporção simples', 'ajuste por ano', 'ajuste por ano × JEC']))
display(pd.Series({'menor n em ano × JEC': int(_n_ano_jec.min()),
                   'maior n em ano × JEC': int(_n_ano_jec.max()),
                   'n efetivo dos pesos ano × JEC': float(_pesos_jec.peso_ano_jec.sum() ** 2 /
                       (_pesos_jec.peso_ano_jec ** 2).sum())}, name='diagnóstico dos pesos').to_frame())
"""),
    ("markdown", r"""
**Leitura do efeito prático.** O indício estimado com os pesos originais por ano é aproximadamente **17,65%**. Ao incorporar também a participação de cada JEC na moldura, fica em aproximadamente **17,47%**, uma diferença de **−0,18 ponto percentual**. Para certeza, a mudança é de aproximadamente **5,04% para 5,09%**. Assim, a falta de cotas por JEC teve efeito pequeno nas **estimativas agregadas observadas**. O tamanho efetivo dos novos pesos é cerca de 571, ante 595 sorteados; esse ajuste não cria informação nova nem melhora a precisão para um JEC isolado.
"""),
]

BLOCKS_DATAJUD = [
    ("markdown", r"""
### 11.2 A mesma comparação entre os processos encontrados no DataJud

O DataJud traz registros de processos além da moldura e informa o **órgão atual**, que pode mudar por redistribuição. Para manter a pergunta sobre representatividade do sorteio, ligamos o cache à Base consolidada pelo número do processo e conservamos o **JEC de origem da moldura**. O teste abaixo usa somente os processos da moldura com documento encontrado no DataJud e os sorteados pertencentes a esse subconjunto. A coluna de cobertura mostra quanto da moldura de cada juizado ficou observável nessa fonte; o teste principal continua sendo o da moldura integral, acima.
"""),
    ("code", r"""
_doc_jec = UNIV.desfecho.notna()
_mold_jec_dj = UNIV.loc[_doc_jec, ['numero', 'ano', 'jec']].copy()
_am_jec_dj = am[['numero', 'ano', 'jec']].merge(
    _mold_jec_dj[['numero']], on='numero', how='inner', validate='one_to_one')
TAB_JEC_DJ, ANOS_JEC_DJ, RES_JEC_DJ = diagnosticar_juizados(_mold_jec_dj, _am_jec_dj)
assert (RES_JEC_DJ['N'], RES_JEC_DJ['n']) == (50102, 593)
_cobertura_jec = TAB_JEC_DJ[['JEC', 'N da referência']].rename(columns={'N da referência': 'n no DataJud'})
_cobertura_jec = TAB_JEC[['JEC', 'N da referência']].rename(columns={'N da referência': 'N na moldura'}).merge(
    _cobertura_jec, on='JEC', validate='one_to_one')
_cobertura_jec['cobertura DataJud'] = _cobertura_jec['n no DataJud'] / _cobertura_jec['N na moldura']
_cobertura_jec['% moldura'] = TAB_JEC['% referência'].to_numpy()
_cobertura_jec['% DataJud localizado'] = TAB_JEC_DJ['% referência'].to_numpy()
_cobertura_jec['% amostra localizada'] = TAB_JEC_DJ['% amostra'].to_numpy()
display(tabela_ptbr(_cobertura_jec, casas=3,
                    pct=['cobertura DataJud', '% moldura', '% DataJud localizado', '% amostra localizada']))
display(pd.Series(RES_JEC_DJ, name='subconjunto encontrado no DataJud').to_frame())
"""),
    ("markdown", r"""
**Leitura do DataJud.** Encontramos documentos para **50.102 dos 50.320** processos da moldura (**99,57%**) e para **593 dos 595** sorteados. A cobertura por juizado vai de aproximadamente **99,29% a 99,89%**. Entre os processos encontrados, a distribuição por JEC permanece quase igual à da moldura integral; o teste global condicionado ao ano dá **p ≈ 0,80**. Assim, a pequena perda no DataJud não muda a conclusão sobre o equilíbrio do sorteio.

Esta comparação usa o JEC de origem. Reclassificar os processos pelo órgão **atual** do DataJud responderia a outra pergunta: redistribuições mudam o órgão, e alguns processos hoje estão fora dos 14 JEC. Por fim, uma amostra proporcional em quantidade não garante que as taxas de indício sejam iguais em todos os juizados; isso exige análise do desfecho com a incerteza apropriada.
"""),
    ("markdown", r"""
### 11.3 E se a referência for a íntegra dos processos coletados nos 14 JEC pelo DataJud?

A coleta por órgão do DataJud abrange **todos os 65.472 registros recuperados** nos 14 JEC para ajuizamentos de 2022 a 2024. O cache consolidado possui **73.501** processos porque inclui também 8.029 registros obtidos na busca complementar pela moldura, muitos deles de anos anteriores ou atualmente em outros órgãos. Portanto, 73.501 não é o denominador correto para uma proporção entre os 14 JEC no triênio.

Nesta segunda referência, identificamos o JEC pelo código de **órgão atual** registrado no DataJud e conferimos os totais com o manifesto da coleta. Colocamos lado a lado a composição dessa coleta integral, a moldura depurada do TJRN e a amostra. A coleta por órgão não aplicou todas as exclusões da moldura, como processos repetidos, classes excluídas e ausência de advogado. Também pode diferir pelo órgão após redistribuição. Por isso, esta é uma **comparação descritiva entre universos diferentes**; o teste formal do sorteio deve continuar condicionado à moldura de onde os 595 foram selecionados.
"""),
    ("code", r"""
_orgaos_je = {int(codigo): int(rotulo.split('º')[0])
              for codigo, rotulo in MANIFESTO['populacao']['escopo']['orgaos'].items()}
_dj_integral = POP.loc[POP.via_coleta.eq('orgao_atual')].copy()
_dj_integral['jec_atual'] = pd.to_numeric(_dj_integral.orgao_atual, errors='coerce').map(_orgaos_je)
assert len(_dj_integral) == 65472 and _dj_integral.jec_atual.notna().all()
assert _dj_integral.data_ajuizamento.dt.year.between(2022, 2024).all()
_totais_manifesto = {int(rotulo.split('º')[0]): int(info['n'])
                    for rotulo, info in MANIFESTO['populacao']['resumo'].items()}
_contagem_dj = _dj_integral.jec_atual.value_counts().reindex(range(1, 15), fill_value=0).sort_index()
assert _contagem_dj.to_dict() == _totais_manifesto

TAB_JEC_INTEGRAL = TAB_JEC[['JEC', 'N da referência', '% referência', 'n da amostra', '% amostra']].copy()
TAB_JEC_INTEGRAL = TAB_JEC_INTEGRAL.rename(columns={
    'N da referência': 'N moldura TJRN', '% referência': '% moldura',
    'n da amostra': 'n Hadja', '% amostra': '% Hadja'})
TAB_JEC_INTEGRAL['N DataJud completo'] = _contagem_dj.to_numpy()
TAB_JEC_INTEGRAL['% DataJud completo'] = _contagem_dj.to_numpy() / len(_dj_integral)
TAB_JEC_INTEGRAL['Hadja − DataJud (p.p.)'] = 100 * (
    TAB_JEC_INTEGRAL['% Hadja'] - TAB_JEC_INTEGRAL['% DataJud completo'])
TAB_JEC_INTEGRAL['n esperado se DataJud fosse moldura'] = (
    len(am) * TAB_JEC_INTEGRAL['% DataJud completo'])
display(tabela_ptbr(TAB_JEC_INTEGRAL, casas=3,
                    pct=['% moldura', '% Hadja', '% DataJud completo']))

_intersecao_dj = _dj_integral.numero.isin(base['NÚMERO PROCESSO'])
_amostra_dj = am.numero.isin(_dj_integral.numero)
display(pd.Series({'cache DataJud total': len(POP),
                   'coleta integral 14 JEC, 2022–2024': len(_dj_integral),
                   'da coleta integral também na moldura depurada': int(_intersecao_dj.sum()),
                   'da coleta integral fora da moldura depurada': int((~_intersecao_dj).sum()),
                   'sorteados presentes na coleta integral': int(_amostra_dj.sum())},
                  name='universos e interseções').to_frame())

fig, ax = plt.subplots(figsize=(10, 4.2))
ax.plot(TAB_JEC_INTEGRAL.JEC, 100 * TAB_JEC_INTEGRAL['% Hadja'], 'o-', label='amostra Hadja')
ax.plot(TAB_JEC_INTEGRAL.JEC, 100 * TAB_JEC_INTEGRAL['% moldura'], 's-', label='moldura TJRN')
ax.plot(TAB_JEC_INTEGRAL.JEC, 100 * TAB_JEC_INTEGRAL['% DataJud completo'], '^-', label='DataJud: coleta integral no triênio')
ax.set(xlabel='juizado', ylabel='% de processos em cada universo', xticks=TAB_JEC_INTEGRAL.JEC,
       title='Composição por juizado: amostra, moldura e coleta integral do DataJud')
ax.legend(); fig.tight_layout()
fig.savefig(FIGURAS / 'amostra_juizados_datajud_integral.png', dpi=150)
plt.show()
"""),
    ("markdown", r"""
**Leitura da coleta integral.** Os 65.472 processos do DataJud estão distribuídos quase uniformemente entre os 14 JEC, com aproximadamente 4.656 a 4.704 processos por unidade. A moldura depurada também é próxima da uniformidade. O maior excesso da amostra continua no 2º JEC, com 9,24% dos sorteados contra cerca de 7,14% na coleta integral; o 5º tem 5,55% contra cerca de 7,14%. A proximidade entre as duas referências populacionais reforça a conclusão descritiva de que a amostra não está fortemente deslocada por juizado.

Dos 65.472 processos da coleta integral, **16.175 não estão na moldura depurada** e **49.297 estão nela**; 581 dos 595 sorteados aparecem nessa via direta de coleta. A comparação com o DataJud inteiro não substitui o teste de representatividade do sorteio, porque esses 16.175 processos adicionais não tinham a mesma regra de elegibilidade e o órgão atual não é necessariamente o de origem. Ela mostra, de forma transparente, como a composição da amostra se compara à distribuição geral dos registros disponíveis no triênio.
"""),
]
