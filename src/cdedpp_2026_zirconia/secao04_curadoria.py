# -*- coding: utf-8 -*-
"""Seção 4: curadoria e auditoria dos dados simulados."""

from collections.abc import Callable


def construir(md: Callable[[str], None], code: Callable[[str], None]) -> None:
    """Emite células de curadoria, auditoria e validação do esquema."""
    md(r"""
    ## 4. Curadoria e Auditoria dos Dados Simulados

    A simulação produziu arquivos CSV, mas o protocolo empírico não deve confiar
    automaticamente em arquivos recém-gerados. Esta seção recarrega as bases como
    se tivessem sido recebidas por outro pesquisador, confere encoding, esquema,
    domínios, duplicidades, valores ausentes, cobertura territorial e coerência
    das frequências.

    Em pesquisa real, esta etapa corresponde ao **controle de qualidade da base**:
    verificar se cada linha representa a unidade de análise definida, se não há
    duplicatas não documentadas, se categorias respeitam o dicionário, se valores
    quantitativos são finitos e se perdas ou exclusões foram registradas. A regra
    deste template é não apagar casos silenciosamente. Qualquer exclusão deve ter
    critério substantivo e rastro reproduzível.

    **Fluxo de elegibilidade nesta simulação:**

    | Etapa | Regra | Resultado esperado |
    |---|---|---|
    | Arquivos recebidos | Ler CSVs em UTF-8 com BOM compatível com planilhas | Amostra principal e piloto carregados |
    | Unidade de análise | Uma linha por pedido | IDs únicos em cada base |
    | Separação das bases | Piloto independente da amostra principal | Sem IDs sobrepostos |
    | Domínios categóricos | Categorias iguais ao dicionário | Nenhuma categoria fora do domínio |
    | Valores ausentes | NA contabilizado por coluna | Nenhum NA estrutural nesta simulação |
    | Curadoria | Sem exclusão quando não houver falha | N preservado |

    A categoria `pendente_ou_sem_execucao` é um **estado substantivo do desfecho**,
    não um valor ausente. Confundir pendência com NA destruiria informação
    empírica importante e enviesaria a descrição da política pública.
    """)

    code(r"""
    # Definir caminhos dos arquivos produzidos pela simulação.
    caminho_dados = PASTA_SAIDA / "zirconia_pedidos_simulados.csv"
    caminho_piloto = PASTA_SAIDA / "zirconia_piloto_simulado.csv"

    # Conferir existência antes da leitura para sinalizar ordem incorreta de execução.
    assert caminho_dados.is_file(), f"Arquivo principal não encontrado: {caminho_dados}"
    assert caminho_piloto.is_file(), f"Arquivo piloto não encontrado: {caminho_piloto}"

    # Ler explicitamente com UTF-8 com BOM, preservando identificadores como texto.
    dados_lidos = pd.read_csv(
        caminho_dados,
        encoding="utf-8-sig",
        dtype={
            "id_pedido": "string",
            "assistencia_juridica": "string",
            "desfecho_pedido": "string",
            "regiao_zirconia": "string",
            "unidade_zus": "string",
            "completude_documental": "string",
        },
    )
    piloto_lido = pd.read_csv(
        caminho_piloto,
        encoding="utf-8-sig",
        dtype={
            "id_pedido": "string",
            "assistencia_juridica": "string",
            "desfecho_pedido": "string",
            "regiao_zirconia": "string",
            "unidade_zus": "string",
            "completude_documental": "string",
        },
    )

    # Conferir se as colunas correspondem exatamente ao esquema analítico.
    colunas_esperadas = list(VARIAVEIS_ANALITICAS)
    assert list(dados_lidos.columns) == colunas_esperadas, "Colunas da base principal fora do esquema."
    assert list(piloto_lido.columns) == colunas_esperadas, "Colunas do piloto fora do esquema."

    # Converter tipos de forma controlada, preservando categorias do dicionário.
    def aplicar_esquema(df):
        # Trabalhar em cópia para não alterar o objeto original sem rastreio.
        curado = df.copy()

        # Converter variáveis categóricas para domínios fechados.
        curado["assistencia_juridica"] = pd.Categorical(
            curado["assistencia_juridica"],
            categories=CATEGORIAS_BINARIAS,
        )
        curado["completude_documental"] = pd.Categorical(
            curado["completude_documental"],
            categories=CATEGORIAS_BINARIAS,
        )
        curado["desfecho_pedido"] = pd.Categorical(
            curado["desfecho_pedido"],
            categories=CATEGORIAS_DESFECHO,
        )
        curado["regiao_zirconia"] = curado["regiao_zirconia"].astype("category")
        curado["unidade_zus"] = curado["unidade_zus"].astype("category")

        # Converter variáveis numéricas para os tipos usados nas análises.
        numericas_float = ["indice_acesso_saude", "tempo_espera_dias", "renda_pc_zirc"]
        numericas_int = ["gravidade_clinica", "idade", "capilaridade_defensoria", "ano_pedido"]
        for coluna in numericas_float:
            curado[coluna] = pd.to_numeric(curado[coluna], errors="coerce").astype("float64")
        for coluna in numericas_int:
            curado[coluna] = pd.to_numeric(curado[coluna], errors="coerce").astype("Int64")

        return curado

    dados_curados = aplicar_esquema(dados_lidos)
    piloto_curado = aplicar_esquema(piloto_lido)

    # Montar tabela de tipos para auditoria visual.
    tabela_tipos = pd.DataFrame(
        {
            "coluna": dados_curados.columns,
            "tipo_principal": [str(dtype) for dtype in dados_curados.dtypes],
            "tipo_piloto": [str(dtype) for dtype in piloto_curado.dtypes],
        }
    )

    # Contabilizar valores ausentes sem removê-los automaticamente.
    auditoria_na = (
        pd.DataFrame(
            {
                "coluna": dados_curados.columns,
                "na_principal": dados_curados.isna().sum().to_numpy(),
                "na_piloto": piloto_curado.isna().sum().to_numpy(),
            }
        )
        .assign(
            pct_na_principal=lambda x: 100 * x["na_principal"] / len(dados_curados),
            pct_na_piloto=lambda x: 100 * x["na_piloto"] / len(piloto_curado),
        )
    )

    # Conferir duplicatas de identificador em cada base.
    duplicatas = pd.DataFrame(
        {
            "base": ["principal", "piloto"],
            "linhas": [len(dados_curados), len(piloto_curado)],
            "ids_unicos": [dados_curados["id_pedido"].nunique(), piloto_curado["id_pedido"].nunique()],
            "ids_duplicados": [
                dados_curados["id_pedido"].duplicated().sum(),
                piloto_curado["id_pedido"].duplicated().sum(),
            ],
        }
    )

    # Conferir domínios categóricos observados contra o dicionário.
    dominios_observados = {
        "assistencia_juridica": sorted(dados_lidos["assistencia_juridica"].dropna().unique().tolist()),
        "completude_documental": sorted(dados_lidos["completude_documental"].dropna().unique().tolist()),
        "desfecho_pedido": sorted(dados_lidos["desfecho_pedido"].dropna().unique().tolist()),
        "gravidade_clinica": sorted(dados_curados["gravidade_clinica"].dropna().unique().tolist()),
        "capilaridade_defensoria": sorted(dados_curados["capilaridade_defensoria"].dropna().unique().tolist()),
        "ano_pedido": sorted(dados_curados["ano_pedido"].dropna().unique().tolist()),
    }
    tabela_dominios = pd.DataFrame(
        {
            "variavel": list(dominios_observados.keys()),
            "valores_observados": [", ".join(map(str, valores)) for valores in dominios_observados.values()],
        }
    )

    # Produzir frequências por unidade e ano para verificar cobertura e estratos.
    frequencia_unidade = (
        dados_curados["unidade_zus"]
        .value_counts(dropna=False)
        .rename_axis("unidade_zus")
        .reset_index(name="n")
        .sort_values("unidade_zus")
    )
    frequencia_ano = (
        dados_curados["ano_pedido"]
        .value_counts(dropna=False)
        .rename_axis("ano_pedido")
        .reset_index(name="n")
        .sort_values("ano_pedido")
    )
    frequencia_regiao = (
        dados_curados["regiao_zirconia"]
        .value_counts(dropna=False)
        .rename_axis("regiao_zirconia")
        .reset_index(name="n")
        .sort_values("regiao_zirconia")
    )

    # Criar fluxo de elegibilidade e curadoria sem exclusões nesta iteração.
    fluxo_curadoria = pd.DataFrame(
        [
            {
                "etapa": "CSV principal lido",
                "n": len(dados_lidos),
                "observacao": "Arquivo gerado pela seção de simulação.",
            },
            {
                "etapa": "Esquema aplicado",
                "n": len(dados_curados),
                "observacao": "Conversão de tipos sem remoção de linhas.",
            },
            {
                "etapa": "Base curada para análise",
                "n": len(dados_curados),
                "observacao": "Nenhuma exclusão substantiva nesta simulação.",
            },
        ]
    )

    # Conferir preservação de linhas e separação entre bases.
    assert len(dados_lidos) == PARAMETROS_GERADORES["n_amostra_principal"]
    assert len(piloto_lido) == tamanho_piloto
    assert len(dados_curados) == len(dados_lidos), "Curadoria removeu linhas sem registro."
    assert len(piloto_curado) == len(piloto_lido), "Curadoria removeu linhas do piloto sem registro."
    assert dados_curados["id_pedido"].is_unique, "Há IDs duplicados na base principal."
    assert piloto_curado["id_pedido"].is_unique, "Há IDs duplicados no piloto."
    assert set(dados_curados["id_pedido"]).isdisjoint(set(piloto_curado["id_pedido"])), (
        "Piloto e principal compartilham IDs."
    )

    # Conferir ausência de NA estrutural depois da conversão de tipos.
    assert auditoria_na["na_principal"].sum() == 0, "Há NA na base principal."
    assert auditoria_na["na_piloto"].sum() == 0, "Há NA no piloto."

    # Conferir domínios admissíveis de variáveis categóricas e ordinais.
    assert set(dados_lidos["assistencia_juridica"].unique()).issubset(set(CATEGORIAS_BINARIAS))
    assert set(dados_lidos["completude_documental"].unique()).issubset(set(CATEGORIAS_BINARIAS))
    assert set(dados_lidos["desfecho_pedido"].unique()).issubset(set(CATEGORIAS_DESFECHO))
    assert set(piloto_lido["desfecho_pedido"].unique()).issubset(set(CATEGORIAS_DESFECHO))
    assert set(dados_curados["gravidade_clinica"].dropna().unique()).issubset({1, 2, 3, 4})
    assert set(dados_curados["capilaridade_defensoria"].dropna().unique()).issubset({0, 1, 2, 3})
    assert set(dados_curados["ano_pedido"].dropna().unique()).issubset({2023, 2024, 2025})

    # Conferir limites substantivos das variáveis quantitativas.
    assert dados_curados["indice_acesso_saude"].between(0, 100).all()
    assert piloto_curado["indice_acesso_saude"].between(0, 100).all()
    assert (dados_curados["tempo_espera_dias"] > 0).all()
    assert (piloto_curado["tempo_espera_dias"] > 0).all()
    assert (dados_curados["renda_pc_zirc"] > 0).all()
    assert dados_curados["idade"].between(18, 95).all()

    # Conferir cobertura territorial, temporal e soma dos estratos.
    assert dados_curados["unidade_zus"].nunique() >= 30
    assert dados_curados["regiao_zirconia"].nunique() == 20
    assert frequencia_unidade["n"].sum() == len(dados_curados)
    assert frequencia_ano["n"].sum() == len(dados_curados)
    assert frequencia_regiao["n"].sum() == len(dados_curados)

    # Conferir que a categoria substantiva pendente não foi tratada como ausente.
    assert "pendente_ou_sem_execucao" in set(dados_curados["desfecho_pedido"].dropna())
    assert dados_curados["desfecho_pedido"].isna().sum() == 0

    # Conferir que colunas internas do gerador seguem ausentes.
    colunas_internas = {
        "letramento_digital_latente",
        "prob_assistencia",
        *[f"prob_{categoria}" for categoria in CATEGORIAS_DESFECHO],
    }
    assert colunas_internas.isdisjoint(set(dados_curados.columns))
    assert colunas_internas.isdisjoint(set(piloto_curado.columns))

    # Exibir quadros de auditoria para leitura pelo estudante.
    display(fluxo_curadoria)
    display(tabela_tipos)
    display(auditoria_na)
    display(duplicatas)
    display(tabela_dominios)
    display(frequencia_ano)
    display(frequencia_regiao.head(10))
    display(frequencia_unidade.head(10))

    # Manter nomes canônicos para as próximas seções do notebook.
    dados = dados_curados.copy()
    piloto = piloto_curado.copy()

    print("Curadoria concluída sem exclusões.")
    print("Base principal curada:", dados.shape)
    print("Piloto curado:", piloto.shape)
    """)

    md(r"""
    ### Interpretação da curadoria

    A auditoria confirmou que a base principal e o piloto preservam o número de
    linhas esperado, não compartilham identificadores, respeitam os domínios do
    dicionário e não contêm valores ausentes estruturais. Em dados reais, raramente
    essa etapa será tão limpa. O ponto pedagógico é que cada decisão de limpeza
    deve ser visível, justificada e reproduzível.

    Observe que `pendente_ou_sem_execucao` permaneceu como categoria legítima do
    desfecho. Ela representa um estado institucional relevante: o pedido ainda não
    produziu atendimento efetivo ou não teve execução observada na janela definida.
    Removê-la como se fosse ausência de informação reduziria artificialmente a
    variabilidade do fenômeno.

    Para uma pesquisa observacional retrospectiva, a curadoria também deve discutir
    validade externa: quais pedidos nunca chegaram ao sistema de referência? Há
    pessoas sem acesso digital ou sem documentação mínima que ficaram invisíveis?
    A cobertura territorial da Defensoria e do ZUS afeta quem aparece na base?
    Essas perguntas importam tanto quanto os asserts computacionais.
    """)
