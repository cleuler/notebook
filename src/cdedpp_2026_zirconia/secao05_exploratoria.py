# -*- coding: utf-8 -*-
"""Seção 5: análise exploratória dos dados simulados."""

from collections.abc import Callable


def construir(md: Callable[[str], None], code: Callable[[str], None]) -> None:
    """Emite células de EDA, gráficos, tabelas e validações exploratórias."""
    md(r"""
    ## 5. Análise Exploratória dos Dados (EDA)

    A análise exploratória não testa ainda a hipótese principal. Ela verifica se a
    base curada se comporta de modo coerente com o desenho: distribuição dos
    grupos, presença das cinco categorias do desfecho, dispersão do índice de
    acesso à saúde, cobertura por ano/unidade/região e indícios de desequilíbrio
    basal entre pedidos com e sem assistência jurídica.

    Nesta seção, diferenças brutas serão descritas como **padrões observados**.
    Elas não devem ser interpretadas como efeito causal, pois a assistência
    jurídica foi gerada por um mecanismo observacional associado a gravidade,
    documentação, capilaridade e renda. A modelagem ajustada virá depois.

    **Outputs desta seção:**

    | Output | Finalidade |
    |---|---|
    | Frequência absoluta e relativa de `desfecho_pedido` | Conferir composição dos cinco desfechos nominais |
    | Tabela 2x5 de assistência jurídica por desfecho | Preparar a seção de testes sem escolher método pelo resultado |
    | Medidas resumo de `indice_acesso_saude` por grupo | Ver média, mediana, DP, quartis e N |
    | Resumo por unidade ZUS | Identificar heterogeneidade territorial e base para clusters |
    | Histogramas/densidades e boxplots | Avaliar forma, dispersão e sobreposição do escore |
    | Barras proporcionais do desfecho por grupo | Ver composição relativa sem colapsar categorias |
    | Gráficos de covariáveis por exposição | Ver desequilíbrio basal e suporte comum |

    A EDA é também uma auditoria substantiva: se alguma categoria desaparece, se
    um grupo fica raro demais, se uma unidade domina a amostra ou se há ausência
    de sobreposição entre grupos, a inferência posterior fica fragilizada.
    """)

    code(r"""
    # Fixar a pasta de figuras da EDA.
    PASTA_FIGURAS.mkdir(parents=True, exist_ok=True)

    # Criar cópias locais para deixar claro que a EDA usa a base curada.
    df_eda = dados.copy()
    piloto_eda = piloto.copy()

    # Validar que a EDA parte dos objetos curados, com o N esperado.
    assert len(df_eda) == PARAMETROS_GERADORES["n_amostra_principal"]
    assert len(piloto_eda) == tamanho_piloto
    assert list(df_eda.columns) == VARIAVEIS_ANALITICAS

    # Tabela de frequência absoluta e relativa dos cinco desfechos.
    freq_desfecho = (
        df_eda["desfecho_pedido"]
        .value_counts(sort=False, dropna=False)
        .rename_axis("desfecho_pedido")
        .reset_index(name="n")
    )
    freq_desfecho["percentual"] = 100 * freq_desfecho["n"] / len(df_eda)
    freq_desfecho["percentual"] = freq_desfecho["percentual"].round(2)

    # Tabela 2x5 completa, preservando categorias mesmo que alguma frequência seja zero.
    tabela_2x5 = pd.crosstab(
        df_eda["assistencia_juridica"],
        df_eda["desfecho_pedido"],
        dropna=False,
    ).reindex(index=CATEGORIAS_BINARIAS, columns=CATEGORIAS_DESFECHO, fill_value=0)
    tabela_2x5_prop = tabela_2x5.div(tabela_2x5.sum(axis=1), axis=0) * 100

    # Medidas resumo do índice por exposição.
    resumo_indice_grupo = (
        df_eda.groupby("assistencia_juridica", observed=False)["indice_acesso_saude"]
        .agg(
            n="size",
            media="mean",
            desvio_padrao="std",
            mediana="median",
            q1=lambda x: x.quantile(0.25),
            q3=lambda x: x.quantile(0.75),
            minimo="min",
            maximo="max",
        )
        .round(2)
        .reset_index()
    )

    # Medidas resumo por unidade para visualizar heterogeneidade e tamanhos de cluster.
    resumo_unidade = (
        df_eda.groupby("unidade_zus", observed=False)
        .agg(
            n=("id_pedido", "size"),
            media_indice=("indice_acesso_saude", "mean"),
            dp_indice=("indice_acesso_saude", "std"),
            prop_assistencia=("assistencia_juridica", lambda x: 100 * (x == "Sim").mean()),
            mediana_espera=("tempo_espera_dias", "median"),
        )
        .round(2)
        .reset_index()
        .sort_values(["n", "unidade_zus"], ascending=[False, True])
    )

    # Comparar covariáveis basais por exposição sem ainda modelar.
    resumo_covariaveis = (
        df_eda.groupby("assistencia_juridica", observed=False)
        .agg(
            n=("id_pedido", "size"),
            idade_media=("idade", "mean"),
            renda_media=("renda_pc_zirc", "mean"),
            gravidade_media=("gravidade_clinica", "mean"),
            capilaridade_media=("capilaridade_defensoria", "mean"),
            pct_documentacao_completa=("completude_documental", lambda x: 100 * (x == "Sim").mean()),
            espera_mediana=("tempo_espera_dias", "median"),
        )
        .round(2)
        .reset_index()
    )

    # Calcular tabela de exposição por gravidade para avaliar suporte comum.
    exposicao_por_gravidade = pd.crosstab(
        df_eda["gravidade_clinica"],
        df_eda["assistencia_juridica"],
        normalize="index",
        dropna=False,
    ).reindex(columns=CATEGORIAS_BINARIAS, fill_value=0) * 100
    exposicao_por_gravidade = exposicao_por_gravidade.round(2)

    # Calcular tabela de exposição por capilaridade institucional.
    exposicao_por_capilaridade = pd.crosstab(
        df_eda["capilaridade_defensoria"],
        df_eda["assistencia_juridica"],
        normalize="index",
        dropna=False,
    ).reindex(columns=CATEGORIAS_BINARIAS, fill_value=0) * 100
    exposicao_por_capilaridade = exposicao_por_capilaridade.round(2)

    # Validar somas, percentuais e finitude das estatísticas.
    assert freq_desfecho["n"].sum() == len(df_eda), "Frequências do desfecho não somam N."
    assert set(freq_desfecho["desfecho_pedido"].astype(str)) == set(CATEGORIAS_DESFECHO)
    assert tabela_2x5.to_numpy().sum() == len(df_eda), "Tabela 2x5 não soma N."
    assert np.allclose(tabela_2x5_prop.sum(axis=1), 100), "Percentuais 2x5 não somam 100% por grupo."
    assert set(tabela_2x5.columns) == set(CATEGORIAS_DESFECHO)
    matriz_indice = resumo_indice_grupo.select_dtypes(include=[np.number]).to_numpy(dtype=float)
    matriz_unidade = resumo_unidade.select_dtypes(include=[np.number]).fillna(0).to_numpy(dtype=float)
    assert np.isfinite(matriz_indice).all()
    assert np.isfinite(matriz_unidade).all()
    assert resumo_unidade["n"].sum() == len(df_eda), "Tamanhos por unidade não somam N."
    assert (resumo_unidade["n"] > 0).all(), "Há unidade exibida sem observações."
    assert df_eda["indice_acesso_saude"].between(0, 100).all()
    assert df_eda["assistencia_juridica"].notna().all()
    assert df_eda["desfecho_pedido"].notna().all()

    # Exibir tabelas exploratórias principais.
    display(freq_desfecho)
    display(tabela_2x5)
    display(tabela_2x5_prop.round(2))
    display(resumo_indice_grupo)
    display(resumo_covariaveis)
    display(resumo_unidade.head(12))
    display(exposicao_por_gravidade)
    display(exposicao_por_capilaridade)

    # Gráfico 1: distribuição do índice por assistência jurídica.
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.histplot(
        data=df_eda,
        x="indice_acesso_saude",
        hue="assistencia_juridica",
        bins=28,
        stat="density",
        common_norm=False,
        kde=True,
        ax=ax,
    )
    ax.set_title("Distribuição do índice de acesso à saúde por assistência jurídica")
    ax.set_xlabel("Índice de acesso à saúde (pontos)")
    ax.set_ylabel("Densidade")
    ax.text(
        0.01,
        -0.18,
        f"Fonte: dados simulados de Zircônia. N = {len(df_eda)}.",
        transform=ax.transAxes,
        fontsize=9,
    )
    fig.tight_layout()
    fig.savefig(PASTA_FIGURAS / "eda_hist_indice_por_assistencia.png", dpi=150)
    plt.show()

    # Gráfico 2: boxplot do índice por assistência jurídica.
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.boxplot(
        data=df_eda,
        x="assistencia_juridica",
        y="indice_acesso_saude",
        hue="assistencia_juridica",
        palette="Set2",
        legend=False,
        ax=ax,
    )
    ax.set_title("Índice de acesso à saúde por grupo de assistência")
    ax.set_xlabel("Assistência jurídica")
    ax.set_ylabel("Índice de acesso à saúde (pontos)")
    ax.text(
        0.01,
        -0.18,
        f"Fonte: dados simulados de Zircônia. N = {len(df_eda)}.",
        transform=ax.transAxes,
        fontsize=9,
    )
    fig.tight_layout()
    fig.savefig(PASTA_FIGURAS / "eda_boxplot_indice_por_assistencia.png", dpi=150)
    plt.show()

    # Gráfico 3: composição proporcional do desfecho por assistência jurídica.
    proporcoes_plot = (
        tabela_2x5_prop.reset_index()
        .melt(
            id_vars="assistencia_juridica",
            var_name="desfecho_pedido",
            value_name="percentual",
        )
    )
    fig, ax = plt.subplots(figsize=(10, 5))
    base = np.zeros(len(CATEGORIAS_BINARIAS))
    cores = sns.color_palette("Set3", n_colors=len(CATEGORIAS_DESFECHO))
    for cor, categoria in zip(cores, CATEGORIAS_DESFECHO, strict=True):
        valores = proporcoes_plot.loc[
            proporcoes_plot["desfecho_pedido"] == categoria,
            "percentual",
        ].to_numpy()
        ax.bar(CATEGORIAS_BINARIAS, valores, bottom=base, label=categoria, color=cor)
        base = base + valores
    ax.set_title("Composição percentual dos desfechos por assistência jurídica")
    ax.set_xlabel("Assistência jurídica")
    ax.set_ylabel("Percentual dentro do grupo")
    ax.set_ylim(0, 100)
    ax.legend(title="Desfecho", bbox_to_anchor=(1.02, 1), loc="upper left")
    ax.text(
        0.01,
        -0.18,
        f"Fonte: dados simulados de Zircônia. N = {len(df_eda)}.",
        transform=ax.transAxes,
        fontsize=9,
    )
    fig.tight_layout()
    fig.savefig(PASTA_FIGURAS / "eda_barras_desfecho_por_assistencia.png", dpi=150)
    plt.show()

    # Gráfico 4: proporção de assistência por gravidade clínica.
    gravidade_plot = exposicao_por_gravidade.reset_index().melt(
        id_vars="gravidade_clinica",
        var_name="assistencia_juridica",
        value_name="percentual",
    )
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(
        data=gravidade_plot,
        x="gravidade_clinica",
        y="percentual",
        hue="assistencia_juridica",
        palette="Set2",
        ax=ax,
    )
    ax.set_title("Assistência jurídica por gravidade clínica inicial")
    ax.set_xlabel("Gravidade clínica inicial")
    ax.set_ylabel("Percentual dentro do nível de gravidade")
    ax.text(
        0.01,
        -0.18,
        f"Fonte: dados simulados de Zircônia. N = {len(df_eda)}.",
        transform=ax.transAxes,
        fontsize=9,
    )
    fig.tight_layout()
    fig.savefig(PASTA_FIGURAS / "eda_assistencia_por_gravidade.png", dpi=150)
    plt.show()

    # Gráfico 5: renda por assistência jurídica para avaliar sobreposição.
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.kdeplot(
        data=df_eda,
        x="renda_pc_zirc",
        hue="assistencia_juridica",
        common_norm=False,
        fill=True,
        alpha=0.35,
        ax=ax,
    )
    ax.set_title("Sobreposição da renda per capita por assistência jurídica")
    ax.set_xlabel("Renda familiar per capita (Z$/mês)")
    ax.set_ylabel("Densidade")
    ax.text(
        0.01,
        -0.18,
        f"Fonte: dados simulados de Zircônia. N = {len(df_eda)}.",
        transform=ax.transAxes,
        fontsize=9,
    )
    fig.tight_layout()
    fig.savefig(PASTA_FIGURAS / "eda_renda_por_assistencia.png", dpi=150)
    plt.show()

    # Gráfico 6: tamanho dos clusters por unidade ZUS.
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.histplot(resumo_unidade["n"], bins=18, ax=ax, color="#4C78A8")
    ax.set_title("Distribuição do tamanho dos clusters por unidade ZUS")
    ax.set_xlabel("Número de pedidos por unidade ZUS")
    ax.set_ylabel("Número de unidades")
    ax.axvline(resumo_unidade["n"].median(), color="black", linestyle="--", label="Mediana")
    ax.legend()
    ax.text(
        0.01,
        -0.18,
        f"Fonte: dados simulados de Zircônia. Unidades = {resumo_unidade.shape[0]}.",
        transform=ax.transAxes,
        fontsize=9,
    )
    fig.tight_layout()
    fig.savefig(PASTA_FIGURAS / "eda_tamanho_clusters_unidade.png", dpi=150)
    plt.show()

    # Validar que os arquivos de gráficos foram produzidos.
    figuras_eda = [
        "eda_hist_indice_por_assistencia.png",
        "eda_boxplot_indice_por_assistencia.png",
        "eda_barras_desfecho_por_assistencia.png",
        "eda_assistencia_por_gravidade.png",
        "eda_renda_por_assistencia.png",
        "eda_tamanho_clusters_unidade.png",
    ]
    for figura in figuras_eda:
        caminho_figura = PASTA_FIGURAS / figura
        assert caminho_figura.is_file(), f"Figura não encontrada: {caminho_figura}"
        assert caminho_figura.stat().st_size > 0, f"Figura vazia: {caminho_figura}"

    print("EDA concluída com tabelas e gráficos salvos em:", PASTA_FIGURAS)
    """)

    md(r"""
    ### Interpretação exploratória

    A distribuição do índice de acesso à saúde deve ser lida primeiro como
    inspeção do comportamento dos dados simulados. Se o grupo com assistência
    jurídica apresenta maior média ou mediana, isso é compatível com o mecanismo
    gerador, mas ainda não separa efeito principal, seleção observacional e
    confundimento residual.

    A tabela 2x5 antecipa a análise inferencial do desfecho multinomial. O ponto
    importante é preservar todas as cinco categorias, inclusive
    `pendente_ou_sem_execucao`, e verificar contagens antes de escolher o teste.
    A decisão entre qui-quadrado e reamostragem ficará para a seção de NHST.

    Os gráficos de gravidade, renda e capilaridade ajudam a localizar
    desequilíbrios basais. Se os grupos diferem nessas covariáveis, o modelo
    ajustado é necessário, embora não suficiente para eliminar variáveis ocultas.
    A distribuição dos tamanhos por unidade ZUS também justifica tratar a unidade
    como cluster na inferência posterior.

    **Registro do estudante:** quais padrões parecem substantivamente relevantes?
    Há categoria rara que ameaça a estabilidade do teste? A exposição tem suporte
    comum nas covariáveis principais? Alguma unidade, região ou ano domina a base?
    Que diferenças brutas poderiam desaparecer ou mudar de direção após ajuste?
    """)
