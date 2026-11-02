# -*- coding: utf-8 -*-
"""Seção 9: síntese, limitações e protocolo replicável."""

from collections.abc import Callable


def construir(md: Callable[[str], None], code: Callable[[str], None]) -> None:
    """Emite a síntese final e o quadro reproduzível do protocolo."""
    md(r"""
    ## 9. Síntese e Protocolo Replicável

    Esta seção organiza o que foi produzido pelo notebook em um protocolo
    depositável em repositório: problema, desenho, dicionário, simulação,
    curadoria, EDA, modelagem, testes de hipótese, dimensionamento amostral,
    limitações e checklist de replicação.

    A conclusão deve ser lida como **modelo de escrita científica**. Como os dados
    são simulados, nenhuma frase deve afirmar que uma política real da Zircônia
    funcionou. O resultado é didático: mostra como um estudo observacional
    retrospectivo poderia ser planejado, auditado, analisado e documentado.

    **Estrutura recomendada para o relatório do estudante:**

    | Parte | Conteúdo mínimo |
    |---|---|
    | Problema | Delimitação T.E.M.P., população-alvo, população acessível e unidade de análise |
    | Teoria | Mecanismo esperado, hipótese rival e variáveis ocultas plausíveis |
    | Variáveis | Dicionário, escala, unidade de medida, tipo Python, papel e fonte |
    | Dados | Sistema de referência, critérios de inclusão/exclusão, curadoria e perdas |
    | EDA | Frequências, medidas resumo, gráficos e sinais de desequilíbrio basal |
    | Modelagem | Estimando, covariáveis, clusters, diagnóstico e tamanho da associação |
    | NHST | $H_0$, $H_1$, alpha, p-valor, IC, erro tipo I, erro tipo II e decisão |
    | Amostragem | Piloto, desvio padrão, razão entre grupos, poder, perdas e sensibilidade |
    | Limitações | Validade interna, externa, mensuração, seleção e confundimento residual |
    | Repositório | Notebook, dados simulados, dicionário, plano, ambiente e scripts |
    """)

    code(r"""
    # Reunir elementos centrais calculados nas seções anteriores.
    resumo_reprodutivel = pd.DataFrame(
        [
            {"campo": "notebook", "valor": "CDEaDPP_2026_Trabalho_Final_Zirconia.ipynb"},
            {"campo": "plano", "valor": "PLANO_CDEaDPP_2026_Trabalho_Final_Zirconia.md"},
            {"campo": "caso", "valor": "Zircônia - acesso à saúde e acesso à justiça"},
            {"campo": "desenho", "valor": "estudo observacional retrospectivo com dados simulados"},
            {"campo": "unidade_analise", "valor": "pedido individual de acesso à saúde"},
            {"campo": "semente", "valor": SEMENTE},
            {"campo": "alpha", "valor": alpha},
            {"campo": "beta", "valor": beta},
            {"campo": "poder_alvo", "valor": poder_alvo},
            {"campo": "n_piloto", "valor": len(piloto)},
            {"campo": "n_amostra_principal", "valor": len(dados)},
            {"campo": "n_modelo", "valor": int(modelo_ajustado.nobs)},
            {"campo": "clusters_unidade_zus", "valor": n_clusters},
            {"campo": "efeito_gerador_indice", "valor": PARAMETROS_GERADORES["efeito_assistencia_indice"]},
            {"campo": "estimativa_ols_ajustada", "valor": estimativa_primaria},
            {"campo": "ic95_inferior_ols", "valor": float(ic_primario.iloc[0])},
            {"campo": "ic95_superior_ols", "valor": float(ic_primario.iloc[1])},
            {"campo": "p_valor_ols_ajustado", "valor": p_primario},
            {"campo": "decisao_primaria", "valor": decisao_primaria},
            {"campo": "metodo_teste_2x5", "valor": metodo_secundario},
            {"campo": "p_valor_2x5", "valor": p_secundario},
            {"campo": "decisao_secundaria", "valor": decisao_secundaria},
            {"campo": "s_piloto", "valor": s_piloto},
            {"campo": "ratio_piloto_controle_por_atendido", "valor": ratio_piloto},
            {"campo": "N_quant", "valor": N_quant},
            {"campo": "N_multinomial_2x5", "valor": N_multinomial_2x5},
            {"campo": "N_OLS_calibrado", "valor": N_OLS_calibrado},
            {"campo": "N_final_com_perdas", "valor": N_final},
            {"campo": "csv_principal", "valor": str(PASTA_SAIDA / "zirconia_pedidos_simulados.csv")},
            {"campo": "csv_piloto", "valor": str(PASTA_SAIDA / "zirconia_piloto_simulado.csv")},
            {"campo": "pasta_figuras", "valor": str(PASTA_FIGURAS)},
        ]
    )

    # Registrar versões novamente no encerramento para facilitar auditoria externa.
    versoes_finais = pd.DataFrame(
        {
            "pacote": list(versoes.keys()),
            "versao": list(versoes.values()),
        }
    )

    # Montar checklist objetivo de replicabilidade.
    checklist_replicacao = pd.DataFrame(
        [
            ("Plano metodológico existe", (RAIZ_PROJETO / "PLANO_CDEaDPP_2026_Trabalho_Final_Zirconia.md").is_file()),
            ("Notebook gerado existe", (RAIZ_PROJETO / "CDEaDPP_2026_Trabalho_Final_Zirconia.ipynb").is_file()),
            ("CSV principal existe", (PASTA_SAIDA / "zirconia_pedidos_simulados.csv").is_file()),
            ("CSV piloto existe", (PASTA_SAIDA / "zirconia_piloto_simulado.csv").is_file()),
            ("Dicionário cobre variáveis analíticas", set(VARIAVEIS_ANALITICAS).issubset(set(dicionario["nome"]))),
            ("Latente excluída da base analítica", "letramento_digital_latente" not in dados.columns),
            ("Piloto distinto da amostra principal", set(piloto["id_pedido"]).isdisjoint(set(dados["id_pedido"]))),
            ("Amostra principal sem NA", int(dados.isna().sum().sum()) == 0),
            ("Tabela 2x5 completa", tabela_desfecho_2x5.shape == (2, 5)),
            ("Modelo com ao menos 30 clusters", n_clusters >= 30),
            ("N final cobre objetivos inferenciais", N_final >= max(N_quant, N_multinomial_2x5, N_OLS_calibrado)),
        ],
        columns=["item", "ok"],
    )

    # Preparar texto sintético parametrizado por resultados efetivamente calculados.
    conclusao_parametrizada = pd.DataFrame(
        [
            {
                "elemento": "resultado_primario",
                "texto": (
                    f"No conjunto simulado, a associação ajustada entre assistência jurídica "
                    f"e índice de acesso à saúde foi de {estimativa_primaria:.2f} pontos "
                    f"(IC95% {float(ic_primario.iloc[0]):.2f}; {float(ic_primario.iloc[1]):.2f}; "
                    f"p={p_primario:.3g}), com decisão: {decisao_primaria}."
                ),
            },
            {
                "elemento": "resultado_secundario",
                "texto": (
                    f"Para o desfecho multinomial 2x5, o método aplicado foi "
                    f"{metodo_secundario}, com p={p_secundario:.3g} e decisão: "
                    f"{decisao_secundaria}."
                ),
            },
            {
                "elemento": "amostragem",
                "texto": (
                    f"O dimensionamento indicou N final de {N_final} pedidos após "
                    f"correção por perdas, considerando N_quant={N_quant}, "
                    f"N_multinomial_2x5={N_multinomial_2x5} e "
                    f"N_OLS_calibrado={N_OLS_calibrado}."
                ),
            },
        ]
    )

    # Asserts finais de coerência e rastreabilidade.
    campos_obrigatorios = {
        "notebook",
        "plano",
        "semente",
        "alpha",
        "beta",
        "poder_alvo",
        "n_piloto",
        "n_amostra_principal",
        "estimativa_ols_ajustada",
        "ic95_inferior_ols",
        "ic95_superior_ols",
        "p_valor_ols_ajustado",
        "N_final_com_perdas",
    }
    assert campos_obrigatorios.issubset(set(resumo_reprodutivel["campo"]))
    assert int(resumo_reprodutivel.loc[resumo_reprodutivel["campo"] == "n_piloto", "valor"].iloc[0]) == len(piloto)
    assert int(resumo_reprodutivel.loc[resumo_reprodutivel["campo"] == "n_amostra_principal", "valor"].iloc[0]) == len(dados)
    assert np.isclose(
        float(resumo_reprodutivel.loc[resumo_reprodutivel["campo"] == "estimativa_ols_ajustada", "valor"].iloc[0]),
        estimativa_primaria,
    )
    assert np.isclose(
        float(resumo_reprodutivel.loc[resumo_reprodutivel["campo"] == "ic95_inferior_ols", "valor"].iloc[0]),
        float(ic_primario.iloc[0]),
    )
    assert np.isclose(
        float(resumo_reprodutivel.loc[resumo_reprodutivel["campo"] == "ic95_superior_ols", "valor"].iloc[0]),
        float(ic_primario.iloc[1]),
    )
    assert np.isclose(
        float(resumo_reprodutivel.loc[resumo_reprodutivel["campo"] == "p_valor_ols_ajustado", "valor"].iloc[0]),
        p_primario,
    )
    assert checklist_replicacao["ok"].all(), "Algum item do checklist final falhou."
    assert "estcaso_lide_pred" not in str(PASTA_SAIDA).lower()
    assert "rafael" not in str(PASTA_SAIDA).lower()
    assert not any(col.startswith("prob_") for col in dados.columns)

    # Exibir síntese final.
    display(resumo_reprodutivel)
    display(versoes_finais)
    display(checklist_replicacao)
    display(conclusao_parametrizada)

    print("Síntese final concluída.")
    print(f"Notebook completo: {RAIZ_PROJETO / 'CDEaDPP_2026_Trabalho_Final_Zirconia.ipynb'}")
    print(f"N final recomendado no protocolo didático: {N_final}")
    """)

    md(r"""
    ### Conclusão acadêmica do template

    No caso simulado de Zircônia, o notebook ilustra um protocolo completo para
    investigar a associação entre assistência jurídica institucional e acesso
    efetivo à saúde em pedidos de pessoas de baixa renda. A simulação criou um
    efeito gerador positivo, covariáveis observadas, heterogeneidade territorial e
    uma variável latente omitida, de modo a aproximar o exercício das dificuldades
    de um estudo observacional retrospectivo.

    Os resultados estimados no notebook devem ser interpretados como demonstração
    metodológica. Um coeficiente estatisticamente significativo no OLS ajustado
    indica incompatibilidade dos dados simulados com coeficiente zero sob o modelo
    adotado, mas não demonstra, sozinho, causalidade. A validade interna continua
    ameaçada por seleção observacional, confundimento residual, erro de medida e
    eventual especificação incompleta do modelo. A validade externa depende da
    cobertura do sistema de referência, da capilaridade institucional e da
    comparabilidade entre a população simulada e a população real que o estudante
    venha a estudar.

    O desfecho multinomial 2x5 oferece uma análise secundária e marginal. Mesmo
    quando seu teste rejeita $H_0$, ele não ajusta por gravidade, renda, unidade,
    ano ou dependência intraunidade. Ele deve ser apresentado como evidência
    complementar de associação entre distribuição de desfechos e assistência
    jurídica, não como substituto de modelagem categórica ajustada.

    O dimensionamento amostral mostra que o piloto n=50 é útil para obter uma
    primeira estimativa de desvio padrão e razão entre grupos, mas essas estimativas
    são instáveis. Por isso, o protocolo recomenda análise de sensibilidade,
    explicitação do efeito mínimo relevante e calibração por simulação quando o
    modelo final inclui covariáveis, efeitos fixos e erros agrupados.

    **Checklist para depósito em repositório antes da coleta real:**

    - Problema de pesquisa delimitado em tempo, espaço, matéria e população.
    - Dicionário de dados com nome, significado, escala, unidade, tipo Python,
      papel analítico, fonte e exemplos.
    - Critérios de inclusão, exclusão, tratamento de NA e duplicatas.
    - Plano de simulação ou piloto independente documentado.
    - Hipóteses primária e secundária com alpha, beta e poder pré-definidos.
    - Scripts/notebook executáveis do início ao fim.
    - Ambiente computacional e versões de pacotes registradas.
    - Estratégia para variáveis ocultas, confundimento e validade externa.
    - Plano de análise de resíduos, clusters, categorias esparsas e sensibilidade.

    Ao substituir os dados simulados por dados reais, o estudante deve revisar cada
    pressuposto, declarar perdas e limitações, e evitar qualquer conclusão que vá
    além do desenho efetivamente sustentado pelos dados.
    """)
