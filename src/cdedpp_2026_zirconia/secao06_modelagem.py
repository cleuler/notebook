# -*- coding: utf-8 -*-
"""Seção 6: modelagem estatística e diagnósticos."""

from collections.abc import Callable


def construir(md: Callable[[str], None], code: Callable[[str], None]) -> None:
    """Emite células de regressão OLS, erros agrupados e diagnóstico."""
    md(r"""
    ## 6. Modelagem Estatística e Diagnósticos

    Esta seção estima a associação entre assistência jurídica e o índice de acesso
    à saúde por regressão linear. O modelo bruto descreve a diferença média entre
    grupos. O modelo ajustado inclui covariáveis medidas antes ou no contexto
    inicial do pedido: gravidade clínica, renda per capita, idade, completude
    documental, ano e efeitos fixos de unidade ZUS.

    **Estimando primário:** coeficiente de `assistencia_binaria`, interpretado
    como diferença média ajustada no `indice_acesso_saude`, em pontos, entre
    pedidos com e sem assistência jurídica, condicional às covariáveis do modelo.

    **Por que erros padrão agrupados?** Pedidos da mesma unidade ZUS podem
    compartilhar rotinas administrativas, filas, disponibilidade local e cultura
    decisória. Isso viola a independência simples dos resíduos. Por isso, o modelo
    ajustado usa erros padrão agrupados por `unidade_zus`, com correção para número
    finito de grupos. Efeitos fixos de unidade e erros agrupados tratam problemas
    diferentes: os efeitos fixos controlam diferenças médias observáveis ou
    estáveis entre unidades; os erros agrupados ajustam a incerteza quando resíduos
    dentro da mesma unidade são dependentes.

    **Limites.** O ajuste não elimina confundimento por variáveis omitidas, como
    letramento digital ou capital social, e não transforma o estudo retrospectivo
    em experimento. Além disso, o OLS resume o desfecho quantitativo; a análise do
    desfecho multinomial será tratada por tabela 2x5 e teste específico na seção
    seguinte.
    """)

    code(r"""
    # Importar a API de fórmulas do statsmodels apenas na seção que a utiliza.
    import statsmodels.formula.api as smf

    # Criar base de modelagem a partir da base curada.
    dados_modelo = dados.copy()

    # Codificar a exposição principal como 0/1, preservando o rótulo original.
    dados_modelo["assistencia_binaria"] = (
        dados_modelo["assistencia_juridica"].astype(str).eq("Sim").astype(int)
    )

    # Garantir que as variáveis categóricas entram no modelo como categorias.
    dados_modelo["unidade_zus"] = dados_modelo["unidade_zus"].astype("category")
    dados_modelo["ano_pedido"] = dados_modelo["ano_pedido"].astype("category")
    dados_modelo["completude_documental"] = dados_modelo["completude_documental"].astype("category")

    # Selecionar variáveis necessárias e remover apenas linhas incompletas do modelo.
    variaveis_modelo = [
        "indice_acesso_saude",
        "assistencia_binaria",
        "gravidade_clinica",
        "renda_pc_zirc",
        "idade",
        "completude_documental",
        "ano_pedido",
        "unidade_zus",
        "desfecho_pedido",
        "assistencia_juridica",
    ]
    dados_modelo = dados_modelo[variaveis_modelo].dropna().copy()

    # Conferir que a seleção do modelo não removeu casos nesta simulação.
    assert len(dados_modelo) == len(dados), "O modelo perdeu linhas por NA."
    assert dados_modelo["unidade_zus"].nunique() >= 30, "Poucos clusters efetivos."
    assert dados_modelo["assistencia_binaria"].nunique() == 2, "Exposição sem variação."

    # Estimar modelo bruto: diferença média sem ajuste.
    formula_bruta = "indice_acesso_saude ~ assistencia_binaria"
    modelo_bruto = smf.ols(formula_bruta, data=dados_modelo).fit()

    # Estimar modelo ajustado com efeitos fixos de unidade e ano.
    formula_ajustada = (
        "indice_acesso_saude ~ assistencia_binaria"
        " + gravidade_clinica + renda_pc_zirc + idade"
        " + C(completude_documental)"
        " + C(ano_pedido)"
        " + C(unidade_zus)"
    )
    modelo_ajustado_ols = smf.ols(formula_ajustada, data=dados_modelo)
    modelo_ajustado = modelo_ajustado_ols.fit(
        cov_type="cluster",
        cov_kwds={
            "groups": dados_modelo["unidade_zus"],
            "use_correction": True,
        },
        use_t=True,
    )

    # Validar que o desenho do modelo não tem colinearidade perfeita.
    matriz_desenho = modelo_ajustado_ols.exog
    posto = np.linalg.matrix_rank(matriz_desenho)
    n_colunas = matriz_desenho.shape[1]
    assert posto == n_colunas, (
        f"Matriz de desenho sem posto completo: posto={posto}, colunas={n_colunas}."
    )

    # Extrair número de clusters e tamanhos de grupos usados pela inferência.
    clusters_modelo = dados_modelo["unidade_zus"]
    tamanhos_clusters = clusters_modelo.value_counts().sort_index()
    n_clusters = int(tamanhos_clusters.shape[0])
    assert n_clusters >= 30, "Inferência agrupada exige ao menos 30 clusters neste template."
    assert len(clusters_modelo) == int(modelo_ajustado.nobs), "Grupos desalinhados com linhas do modelo."

    # Função auxiliar para resumir coeficientes centrais.
    def resumir_coeficiente(resultado, termo, nome_modelo):
        # Extrair estimativa, intervalo, erro padrão e p-valor para o termo indicado.
        intervalo = resultado.conf_int().loc[termo]
        return {
            "modelo": nome_modelo,
            "termo": termo,
            "estimativa": float(resultado.params[termo]),
            "erro_padrao": float(resultado.bse[termo]),
            "ic95_inferior": float(intervalo.iloc[0]),
            "ic95_superior": float(intervalo.iloc[1]),
            "p_valor": float(resultado.pvalues[termo]),
            "n": int(resultado.nobs),
            "r2": float(resultado.rsquared),
        }

    resumo_modelos = pd.DataFrame(
        [
            resumir_coeficiente(modelo_bruto, "assistencia_binaria", "OLS bruto"),
            resumir_coeficiente(modelo_ajustado, "assistencia_binaria", "OLS ajustado + EP cluster"),
        ]
    )
    resumo_modelos = resumo_modelos.round(
        {
            "estimativa": 3,
            "erro_padrao": 3,
            "ic95_inferior": 3,
            "ic95_superior": 3,
            "p_valor": 4,
            "r2": 3,
        }
    )

    # Montar tabela de clusters para transparência sobre a dependência intraunidade.
    resumo_clusters = pd.DataFrame(
        {
            "metrica": [
                "clusters",
                "menor_n_por_unidade",
                "mediana_n_por_unidade",
                "maior_n_por_unidade",
                "n_modelo",
            ],
            "valor": [
                n_clusters,
                int(tamanhos_clusters.min()),
                float(tamanhos_clusters.median()),
                int(tamanhos_clusters.max()),
                int(modelo_ajustado.nobs),
            ],
        }
    )

    # Diagnóstico simples de colinearidade para covariáveis substantivas sem efeitos fixos.
    covariaveis_vif = dados_modelo[
        [
            "assistencia_binaria",
            "gravidade_clinica",
            "renda_pc_zirc",
            "idade",
        ]
    ].astype(float)
    covariaveis_vif = sm.add_constant(covariaveis_vif)
    from statsmodels.stats.outliers_influence import variance_inflation_factor

    tabela_vif = pd.DataFrame(
        {
            "variavel": covariaveis_vif.columns,
            "vif": [
                variance_inflation_factor(covariaveis_vif.to_numpy(), indice)
                for indice in range(covariaveis_vif.shape[1])
            ],
        }
    ).round(3)

    # Produzir tabela 2x5 completa para a próxima seção de NHST.
    tabela_desfecho_2x5 = pd.crosstab(
        dados_modelo["assistencia_juridica"],
        dados_modelo["desfecho_pedido"],
        dropna=False,
    ).reindex(index=CATEGORIAS_BINARIAS, columns=CATEGORIAS_DESFECHO, fill_value=0)
    tabela_desfecho_2x5_prop = tabela_desfecho_2x5.div(tabela_desfecho_2x5.sum(axis=1), axis=0) * 100

    # Validar estimativas centrais e objetos que serão usados depois.
    coef_ajustado = float(modelo_ajustado.params["assistencia_binaria"])
    ic_ajustado = modelo_ajustado.conf_int().loc["assistencia_binaria"].astype(float)
    p_ajustado = float(modelo_ajustado.pvalues["assistencia_binaria"])
    assert np.isfinite(coef_ajustado), "Coeficiente ajustado não finito."
    assert np.isfinite(ic_ajustado.to_numpy()).all(), "IC ajustado não finito."
    assert np.isfinite(p_ajustado) and 0 <= p_ajustado <= 1, "p-valor ajustado inválido."
    assert ic_ajustado.iloc[0] <= coef_ajustado <= ic_ajustado.iloc[1], "IC não contém estimativa."
    assert 0 <= float(modelo_bruto.rsquared) <= 1, "R² bruto fora do intervalo."
    assert 0 <= float(modelo_ajustado.rsquared) <= 1, "R² ajustado fora do intervalo."
    assert tabela_desfecho_2x5.shape == (2, 5), "Tabela 2x5 com dimensão incorreta."
    assert tabela_desfecho_2x5.to_numpy().sum() == len(dados_modelo), "Tabela 2x5 não soma N."
    assert set(tabela_desfecho_2x5.columns) == set(CATEGORIAS_DESFECHO)
    assert np.allclose(tabela_desfecho_2x5_prop.sum(axis=1), 100), "Percentuais 2x5 não somam 100%."

    # Exibir tabelas principais do modelo.
    display(resumo_modelos)
    display(resumo_clusters)
    display(tabela_vif)
    display(tabela_desfecho_2x5)
    display(tabela_desfecho_2x5_prop.round(2))

    # Gráfico diagnóstico 1: resíduos versus valores ajustados.
    residuos = modelo_ajustado.resid
    ajustados = modelo_ajustado.fittedvalues
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.scatterplot(x=ajustados, y=residuos, s=18, alpha=0.45, ax=ax)
    ax.axhline(0, color="black", linestyle="--", linewidth=1)
    ax.set_title("Diagnóstico do OLS ajustado: resíduos versus valores ajustados")
    ax.set_xlabel("Valores ajustados")
    ax.set_ylabel("Resíduos")
    ax.text(
        0.01,
        -0.18,
        f"Fonte: dados simulados de Zircônia. N = {int(modelo_ajustado.nobs)}.",
        transform=ax.transAxes,
        fontsize=9,
    )
    fig.tight_layout()
    fig.savefig(PASTA_FIGURAS / "modelo_residuos_vs_ajustados.png", dpi=150)
    plt.show()

    # Gráfico diagnóstico 2: QQ plot dos resíduos.
    fig = sm.qqplot(residuos, line="45", fit=True)
    fig.set_size_inches(7, 5)
    ax = fig.axes[0]
    ax.set_title("Diagnóstico do OLS ajustado: QQ plot dos resíduos")
    ax.set_xlabel("Quantis teóricos")
    ax.set_ylabel("Quantis observados dos resíduos")
    ax.text(
        0.01,
        -0.18,
        f"Fonte: dados simulados de Zircônia. N = {int(modelo_ajustado.nobs)}.",
        transform=ax.transAxes,
        fontsize=9,
    )
    fig.tight_layout()
    fig.savefig(PASTA_FIGURAS / "modelo_qqplot_residuos.png", dpi=150)
    plt.show()

    # Validar que as figuras diagnósticas foram gravadas.
    for figura in ["modelo_residuos_vs_ajustados.png", "modelo_qqplot_residuos.png"]:
        caminho_figura = PASTA_FIGURAS / figura
        assert caminho_figura.is_file(), f"Figura não encontrada: {caminho_figura}"
        assert caminho_figura.stat().st_size > 0, f"Figura vazia: {caminho_figura}"

    print("Modelagem concluída.")
    print("Coeficiente ajustado de assistência jurídica:", round(coef_ajustado, 3))
    print("p-valor ajustado:", round(p_ajustado, 5))
    print("Clusters efetivos:", n_clusters)
    """)

    md(r"""
    ### Interpretação da modelagem

    O modelo bruto mede a diferença média sem controle. O modelo ajustado estima a
    associação condicional entre assistência jurídica e índice de acesso à saúde,
    mantendo constantes as covariáveis observadas e diferenças médias entre
    unidades ZUS. A comparação entre os dois coeficientes ajuda a avaliar quanto
    da diferença bruta era compatível com desequilíbrio basal observado.

    O p-valor e o intervalo de confiança do modelo ajustado serão formalmente
    interpretados na seção de NHST. Aqui, o foco é verificar se o modelo foi
    estimável, se a matriz de desenho tem posto completo, se o número de clusters
    é suficiente para a aproximação usada e se os resíduos não indicam anomalias
    graves. O QQ plot é diagnóstico visual; não deve ser substituído por uma
    decisão automática baseada apenas em teste de normalidade.

    A tabela 2x5 permanece descritiva nesta seção. Ela informa a composição do
    desfecho nominal por assistência jurídica, mas o teste inferencial será
    escolhido na próxima seção após verificar frequências esperadas. Mesmo quando
    o teste 2x5 for significativo, ele será uma análise marginal, sem ajuste por
    confundidores ou dependência intraunidade.
    """)
