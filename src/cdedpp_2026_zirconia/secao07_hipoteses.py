# -*- coding: utf-8 -*-
"""Seção 7: testes de hipóteses e erros de decisão."""

from collections.abc import Callable


def construir(md: Callable[[str], None], code: Callable[[str], None]) -> None:
    """Emite células de NHST para o modelo primário e desfecho multinomial."""
    md(r"""
    ## 7. NHST e Erros de Decisão

    Esta seção formaliza os testes de hipótese pré-especificados. O teste
    primário usa o coeficiente ajustado de `assistencia_binaria` no OLS com erros
    padrão agrupados por unidade ZUS. A regra de decisão foi fixada no início do
    notebook: rejeitar $H_0$ quando `p_valor < alpha`, com `alpha = 0,05`.

    **Hipótese primária bilateral:**

    $H_0: \beta_{\text{assistência jurídica}} = 0$  
    $H_1: \beta_{\text{assistência jurídica}} \ne 0$

    O p-valor não é a probabilidade de $H_0$ ser verdadeira. Ele é a probabilidade,
    sob o modelo e sob $H_0$, de obter estatística tão ou mais incompatível com
    $H_0$ quanto a observada. A decisão `rejeitar` ou `não rejeitar` não substitui
    a interpretação substantiva do intervalo de confiança, do tamanho da associação
    e dos limites do desenho observacional.

    **Hipótese secundária multinomial, marginal:**

    $H_0$: a distribuição dos cinco desfechos é igual entre pedidos com e sem
    assistência jurídica.  
    $H_1$: ao menos uma proporção difere.

    Antes de escolher o método para a tabela 2x5, o notebook calcula frequências
    esperadas. Se todas forem pelo menos 5, aplica-se o qui-quadrado de Pearson.
    Se alguma frequência esperada for menor que 5, aplica-se automaticamente uma
    reamostragem condicional com margens fixas usando a estatística qui-quadrado.
    Categorias não são colapsadas depois de observar o resultado.
    """)

    code(r"""
    # Extrair elementos do teste primário a partir do modelo ajustado.
    termo_primario = "assistencia_binaria"
    estimativa_primaria = float(modelo_ajustado.params[termo_primario])
    erro_padrao_primario = float(modelo_ajustado.bse[termo_primario])
    estatistica_primaria = float(modelo_ajustado.tvalues[termo_primario])
    p_primario = float(modelo_ajustado.pvalues[termo_primario])
    ic_primario = modelo_ajustado.conf_int().loc[termo_primario].astype(float)
    decisao_primaria = "rejeitar H0" if p_primario < alpha else "não rejeitar H0"

    # Montar tabela do teste primário.
    resultado_primario = pd.DataFrame(
        [
            {
                "hipotese": "H0: beta_assistencia = 0",
                "estimativa": estimativa_primaria,
                "erro_padrao_cluster": erro_padrao_primario,
                "estatistica_t": estatistica_primaria,
                "ic95_inferior": float(ic_primario.iloc[0]),
                "ic95_superior": float(ic_primario.iloc[1]),
                "p_valor": p_primario,
                "alpha": alpha,
                "decisao": decisao_primaria,
                "n": int(modelo_ajustado.nobs),
                "clusters": n_clusters,
            }
        ]
    )

    # Validar coerência da decisão primária.
    assert np.isfinite(p_primario) and 0 <= p_primario <= 1, "p primário inválido."
    assert np.isfinite(estimativa_primaria), "Estimativa primária não finita."
    assert np.isfinite(erro_padrao_primario) and erro_padrao_primario > 0
    assert float(ic_primario.iloc[0]) <= estimativa_primaria <= float(ic_primario.iloc[1])
    assert decisao_primaria == ("rejeitar H0" if p_primario < alpha else "não rejeitar H0")

    # Preparar a tabela 2x5 para o teste secundário.
    tabela_observada = tabela_desfecho_2x5.copy()
    tabela_inferencial = tabela_observada.loc[:, tabela_observada.sum(axis=0) > 0].copy()
    categorias_removidas = [
        categoria
        for categoria in tabela_observada.columns
        if tabela_observada[categoria].sum() == 0
    ]

    # Definir função da estatística qui-quadrado de Pearson para tabelas com margens fixas.
    def estatistica_chi2_tabela(tabela):
        # Calcular esperados por produto das margens e somar contribuição de Pearson.
        arr = np.asarray(tabela, dtype=float)
        total = arr.sum()
        linhas = arr.sum(axis=1, keepdims=True)
        colunas = arr.sum(axis=0, keepdims=True)
        esperadas = linhas @ colunas / total
        return float(((arr - esperadas) ** 2 / esperadas).sum())

    # Selecionar o método secundário de acordo com as frequências esperadas.
    status_secundario = "estimável"
    metodo_secundario = None
    chi2_secundario = np.nan
    gl_secundario = np.nan
    p_secundario = np.nan
    menor_esperada = np.nan
    B_reamostragem = 5000
    erro_mc = np.nan
    frequencias_esperadas = None

    if tabela_inferencial.shape[0] < 2 or tabela_inferencial.shape[1] < 2:
        status_secundario = "teste não estimável"
        metodo_secundario = "não estimável: grupos ou categorias insuficientes"
    else:
        chi2_tmp, p_tmp, gl_tmp, esperadas_tmp = stats.chi2_contingency(
            tabela_inferencial,
            correction=False,
        )
        frequencias_esperadas = pd.DataFrame(
            esperadas_tmp,
            index=tabela_inferencial.index,
            columns=tabela_inferencial.columns,
        )
        menor_esperada = float(frequencias_esperadas.to_numpy().min())
        chi2_secundario = float(chi2_tmp)
        gl_secundario = int(gl_tmp)

        if menor_esperada >= 5:
            metodo_secundario = "qui-quadrado de Pearson"
            p_secundario = float(p_tmp)
        else:
            metodo_secundario = "reamostragem condicional com margens fixas"
            rng_teste = np.random.default_rng(SEMENTE + 707)
            margens_linha = tabela_inferencial.sum(axis=1).to_numpy(dtype=int)
            margens_coluna = tabela_inferencial.sum(axis=0).to_numpy(dtype=int)
            estatisticas_simuladas = np.empty(B_reamostragem, dtype=float)

            for indice in range(B_reamostragem):
                tabela_simulada = stats.random_table.rvs(
                    margens_linha,
                    margens_coluna,
                    random_state=rng_teste,
                )
                estatisticas_simuladas[indice] = estatistica_chi2_tabela(tabela_simulada)

            excedencias = int((estatisticas_simuladas >= chi2_secundario).sum())
            p_secundario = (1 + excedencias) / (1 + B_reamostragem)
            erro_mc = float(np.sqrt(p_secundario * (1 - p_secundario) / (B_reamostragem + 1)))

    decisao_secundaria = (
        "não estimável"
        if status_secundario != "estimável"
        else ("rejeitar H0" if p_secundario < alpha else "não rejeitar H0")
    )

    # Montar tabela do teste secundário.
    resultado_secundario = pd.DataFrame(
        [
            {
                "hipotese": "H0: distribuição 2x5 igual entre grupos",
                "status": status_secundario,
                "metodo": metodo_secundario,
                "chi2": chi2_secundario,
                "gl": gl_secundario,
                "menor_frequencia_esperada": menor_esperada,
                "B_reamostragem": B_reamostragem if "reamostragem" in str(metodo_secundario) else 0,
                "erro_monte_carlo": erro_mc,
                "p_valor": p_secundario,
                "alpha": alpha,
                "decisao": decisao_secundaria,
                "categorias_sem_ocorrencia_total": ", ".join(categorias_removidas) if categorias_removidas else "nenhuma",
            }
        ]
    )

    # Quadro didático dos erros de decisão no contexto do estudo.
    quadro_erros_decisao = pd.DataFrame(
        [
            {
                "erro": "Tipo I",
                "probabilidade_planejada": alpha,
                "interpretação_no_estudo": (
                    "Concluir associação estatisticamente significativa entre assistência jurídica "
                    "e acesso à saúde quando, no modelo populacional correspondente, beta fosse zero."
                ),
            },
            {
                "erro": "Tipo II",
                "probabilidade_planejada": beta,
                "interpretação_no_estudo": (
                    "Não detectar associação mínima relevante quando ela existisse no modelo populacional."
                ),
            },
            {
                "erro": "Poder",
                "probabilidade_planejada": poder_alvo,
                "interpretação_no_estudo": (
                    "Probabilidade planejada de rejeitar H0 para o efeito mínimo relevante definido no protocolo."
                ),
            },
        ]
    )

    # Validar coerência do teste secundário.
    assert tabela_observada.shape == (2, 5), "Tabela observada deve ser 2x5."
    assert tabela_observada.to_numpy().sum() == int(modelo_ajustado.nobs), "Soma da tabela 2x5 incoerente."
    assert set(tabela_observada.columns) == set(CATEGORIAS_DESFECHO)
    if status_secundario == "estimável":
        assert np.isfinite(p_secundario) and 0 <= p_secundario <= 1, "p secundário inválido."
        assert np.isfinite(chi2_secundario) and chi2_secundario >= 0
        assert gl_secundario == (tabela_inferencial.shape[0] - 1) * (tabela_inferencial.shape[1] - 1)
        assert np.isfinite(menor_esperada) and menor_esperada > 0
        if menor_esperada >= 5:
            assert metodo_secundario == "qui-quadrado de Pearson"
        else:
            assert metodo_secundario == "reamostragem condicional com margens fixas"
            assert B_reamostragem > 0
            assert np.isfinite(erro_mc) and erro_mc >= 0
        assert decisao_secundaria == ("rejeitar H0" if p_secundario < alpha else "não rejeitar H0")
    else:
        assert decisao_secundaria == "não estimável"

    # Exibir resultados inferenciais.
    display(resultado_primario.round(5))
    display(tabela_observada)
    if frequencias_esperadas is not None:
        display(frequencias_esperadas.round(2))
    display(resultado_secundario.round(5))
    display(quadro_erros_decisao)

    # Visualizar p-valores em relação ao limiar de decisão.
    grafico_pvalores = pd.DataFrame(
        {
            "teste": ["Primário: OLS ajustado", "Secundário: desfecho 2x5"],
            "p_valor": [p_primario, p_secundario if status_secundario == "estimável" else np.nan],
        }
    )
    fig, ax = plt.subplots(figsize=(8, 4.5))
    sns.barplot(
        data=grafico_pvalores,
        x="teste",
        y="p_valor",
        hue="teste",
        palette="Set2",
        legend=False,
        ax=ax,
    )
    ax.axhline(alpha, color="black", linestyle="--", linewidth=1, label=f"alpha = {alpha}")
    ax.set_title("p-valores observados e limiar de decisão pré-fixado")
    ax.set_xlabel("")
    ax.set_ylabel("p-valor")
    ax.set_ylim(0, max(0.10, np.nanmax(grafico_pvalores["p_valor"].to_numpy()) * 1.25))
    ax.tick_params(axis="x", rotation=12)
    ax.legend()
    ax.text(
        0.01,
        -0.25,
        f"Fonte: dados simulados de Zircônia. N = {int(modelo_ajustado.nobs)}.",
        transform=ax.transAxes,
        fontsize=9,
    )
    fig.tight_layout()
    fig.savefig(PASTA_FIGURAS / "nhst_pvalores_alpha.png", dpi=150)
    plt.show()

    # Validar figura da seção.
    caminho_figura = PASTA_FIGURAS / "nhst_pvalores_alpha.png"
    assert caminho_figura.is_file(), f"Figura não encontrada: {caminho_figura}"
    assert caminho_figura.stat().st_size > 0, f"Figura vazia: {caminho_figura}"

    print("NHST concluído.")
    print("Decisão primária:", decisao_primaria, "| p =", round(p_primario, 6))
    print("Decisão secundária:", decisao_secundaria, "| método:", metodo_secundario)
    """)

    md(r"""
    ### Interpretação dos testes

    O teste primário responde à pergunta pré-especificada sobre a associação
    ajustada entre assistência jurídica e índice de acesso à saúde. Se o p-valor
    for menor que `alpha`, rejeita-se $H_0$ no sentido estatístico frequentista:
    os dados seriam pouco compatíveis com coeficiente zero sob o modelo adotado.
    Isso não prova causalidade nem elimina confundimento residual.

    O teste secundário 2x5 é marginal. Ele compara distribuições dos desfechos sem
    ajuste por gravidade, renda, unidade ou ano. Portanto, seu p-valor não substitui
    uma análise categórica ajustada e não corrige dependência intraunidade. Sua
    utilidade pedagógica é demonstrar como respeitar as frequências esperadas e
    como acionar reamostragem quando o qui-quadrado assintótico for inadequado.

    A decisão deve ser comunicada junto com intervalo de confiança, tamanho da
    associação e limitações do desenho. Também se deve evitar a expressão “aceitar
    $H_0$”: quando o p-valor não é menor que `alpha`, a conclusão correta é “não
    rejeitar $H_0$”, reconhecendo a possibilidade de erro tipo II e de poder
    insuficiente para efeitos menores que o planejado.
    """)
