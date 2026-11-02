# -*- coding: utf-8 -*-
"""Seção 3: simulação de dados e piloto independente."""

from collections.abc import Callable


def construir(md: Callable[[str], None], code: Callable[[str], None]) -> None:
    """Emite células de simulação, exportação e validação dos dados mock."""
    md(r"""
    ## 3. Simulação de Dados (Mock Data) e Piloto Independente

    Esta seção constrói uma base simulada para um estudo jurídico-institucional
    sobre saúde pública e acesso à justiça em Zircônia. A simulação não pretende
    reproduzir uma instituição real; ela cria um **ambiente controlado de ensino**
    no qual sabemos que a assistência jurídica tem efeito gerador positivo sobre
    o índice de acesso à saúde e altera a distribuição dos desfechos.

    O mecanismo gerador segue quatro ideias metodológicas:

    1. A exposição `assistencia_juridica` é observacional, não randomizada. A
       probabilidade de receber assistência depende de gravidade clínica, renda,
       capilaridade local da Defensoria, completude documental, região, unidade e
       uma variável latente de letramento digital.
    2. O desfecho primário `indice_acesso_saude` recebe um efeito principal
       positivo pré-especificado da assistência jurídica, mas também depende de
       covariáveis prévias, heterogeneidade entre unidades e ruído individual.
    3. O desfecho secundário `desfecho_pedido` é multinomial nominal com cinco
       categorias. A assistência jurídica desloca as probabilidades em direção a
       maior realização de internação/tratamento/medicamento e menor negação ou
       pendência.
    4. Uma variável latente, `letramento_digital_latente`, influencia tanto a
       exposição quanto os resultados, mas não será exportada. Ela ilustra o
       risco de confundimento residual em estudos retrospectivos.

    **Caminhos didáticos do gerador:**  
    `gravidade_clinica -> assistencia_juridica` e `gravidade_clinica -> resultado`;  
    `capilaridade_defensoria -> assistencia_juridica`;  
    `letramento_digital_latente -> assistencia_juridica` e
    `letramento_digital_latente -> resultado`;  
    `assistencia_juridica -> indice_acesso_saude` e
    `assistencia_juridica -> desfecho_pedido`.

    O piloto terá **n = 50** e será gerado por fluxo aleatório independente. Ele
    será usado depois para estimar desvio padrão, proporção de grupos e parâmetros
    preliminares de planejamento amostral. A amostra principal será maior para
    permitir EDA, regressão com erros agrupados por unidade e testes sobre a
    tabela 2x5.
    """)

    code(r"""
    # Definir parâmetros substantivos do mecanismo gerador antes de simular.
    PARAMETROS_GERADORES = {
        "n_amostra_principal": 2500,
        "n_unidades_zus": 80,
        "n_regioes": 20,
        "efeito_assistencia_indice": 7.5,
        "efeito_assistencia_logit_desfecho": 0.75,
        "desvio_ruido_individual": 9.0,
        "desvio_efeito_unidade": 3.0,
        "desvio_efeito_regiao": 2.0,
        "seed_piloto": SEMENTE + 101,
        "seed_principal": SEMENTE + 202,
    }

    # Conferir que o plano de simulação injeta efeito principal não nulo.
    assert PARAMETROS_GERADORES["efeito_assistencia_indice"] != 0
    assert PARAMETROS_GERADORES["efeito_assistencia_logit_desfecho"] != 0
    assert PARAMETROS_GERADORES["n_unidades_zus"] >= 30
    assert PARAMETROS_GERADORES["n_regioes"] == 20

    # Criar rótulos estáveis de regiões e unidades.
    REGIOES_ZIRCONIA = [f"R{i:02d}" for i in range(1, PARAMETROS_GERADORES["n_regioes"] + 1)]
    UNIDADES_ZUS = [f"UZ-{i:03d}" for i in range(1, PARAMETROS_GERADORES["n_unidades_zus"] + 1)]
    MAPA_UNIDADE_REGIAO = {
        unidade: REGIOES_ZIRCONIA[(indice - 1) % len(REGIOES_ZIRCONIA)]
        for indice, unidade in enumerate(UNIDADES_ZUS, start=1)
    }

    def logit_inverso(x):
        # Converter preditor linear em probabilidade no intervalo (0, 1).
        return 1 / (1 + np.exp(-x))

    def softmax_estavel(matriz):
        # Transformar escores multinomiais em probabilidades por linha.
        matriz = np.asarray(matriz, dtype=float)
        deslocada = matriz - matriz.max(axis=1, keepdims=True)
        exposta = np.exp(deslocada)
        probabilidades = exposta / exposta.sum(axis=1, keepdims=True)
        return probabilidades

    def sortear_categorias(probabilidades, categorias, gerador):
        # Sortear uma categoria por linha usando probabilidades já normalizadas.
        acumuladas = np.cumsum(probabilidades, axis=1)
        sorteios = gerador.random(probabilidades.shape[0])
        indices = (sorteios[:, None] > acumuladas).sum(axis=1)
        return np.array(categorias, dtype=object)[indices]

    def gerar_pedidos_simulados(n, prefixo_id, seed):
        # Gerar pedidos simulados com covariáveis, exposição e desfechos.
        # Usar gerador local para tornar cada base reproduzível e independente.
        gerador = np.random.default_rng(seed)

        # Sortear unidades com probabilidades desiguais, aproximando demanda heterogênea.
        pesos_unidades = gerador.gamma(shape=2.5, scale=1.0, size=len(UNIDADES_ZUS))
        pesos_unidades = pesos_unidades / pesos_unidades.sum()
        unidade_zus = gerador.choice(UNIDADES_ZUS, size=n, replace=True, p=pesos_unidades)
        regiao_zirconia = np.array([MAPA_UNIDADE_REGIAO[u] for u in unidade_zus], dtype=object)

        # Gerar efeitos compartilhados por região e por unidade para criar dependência intra-cluster.
        efeito_regiao = {
            regiao: valor
            for regiao, valor in zip(
                REGIOES_ZIRCONIA,
                gerador.normal(0, PARAMETROS_GERADORES["desvio_efeito_regiao"], len(REGIOES_ZIRCONIA)),
                strict=True,
            )
        }
        efeito_unidade = {
            unidade: valor
            for unidade, valor in zip(
                UNIDADES_ZUS,
                gerador.normal(0, PARAMETROS_GERADORES["desvio_efeito_unidade"], len(UNIDADES_ZUS)),
                strict=True,
            )
        }
        ruido_regional = np.array([efeito_regiao[r] for r in regiao_zirconia])
        ruido_unidade = np.array([efeito_unidade[u] for u in unidade_zus])

        # Sortear covariáveis prévias coerentes com o cenário de alta desigualdade.
        ano_pedido = gerador.choice([2023, 2024, 2025], size=n, p=[0.31, 0.34, 0.35])
        idade = np.clip(np.round(gerador.gamma(shape=5.5, scale=9.0, size=n) + 18), 18, 95).astype(int)
        renda_pc_zirc = np.clip(gerador.lognormal(mean=np.log(520), sigma=0.65, size=n), 60, 3500)
        capilaridade_defensoria = gerador.choice([0, 1, 2, 3], size=n, p=[0.24, 0.34, 0.27, 0.15])
        gravidade_clinica = gerador.choice([1, 2, 3, 4], size=n, p=[0.20, 0.36, 0.30, 0.14])

        # Criar variáveis prévias binárias com dependência substantiva.
        prob_doc = logit_inverso(
            -0.15
            + 0.55 * (renda_pc_zirc > 550)
            + 0.28 * capilaridade_defensoria
            - 0.22 * (gravidade_clinica >= 3)
        )
        completude_documental = gerador.binomial(1, prob_doc, size=n)

        # Latente usada apenas no gerador, omitida da base analítica exportada.
        prob_letramento = logit_inverso(
            -0.65
            + 0.75 * (renda_pc_zirc > 700)
            + 0.18 * capilaridade_defensoria
            - 0.012 * np.maximum(idade - 55, 0)
        )
        letramento_digital_latente = gerador.binomial(1, prob_letramento, size=n)

        # Gerar exposição observacional; não há alocação forçada 1:1.
        pred_assistencia = (
            -1.05
            + 0.42 * gravidade_clinica
            - 0.00032 * renda_pc_zirc
            + 0.38 * capilaridade_defensoria
            + 0.45 * (1 - completude_documental)
            + 0.36 * letramento_digital_latente
            + 0.12 * (ano_pedido == 2025)
            + 0.06 * ruido_regional
        )
        prob_assistencia = logit_inverso(pred_assistencia)
        assistencia_binaria = gerador.binomial(1, prob_assistencia, size=n)

        # Injetar o efeito principal da assistência no escore de acesso à saúde.
        indice_latente = (
            43
            + PARAMETROS_GERADORES["efeito_assistencia_indice"] * assistencia_binaria
            + 3.2 * gravidade_clinica
            + 4.4 * completude_documental
            + 1.7 * capilaridade_defensoria
            + 2.8 * letramento_digital_latente
            - 0.0032 * np.maximum(renda_pc_zirc - 900, 0)
            - 0.035 * np.maximum(idade - 70, 0)
            + 0.9 * (ano_pedido == 2025)
            + ruido_regional
            + ruido_unidade
            + gerador.normal(0, PARAMETROS_GERADORES["desvio_ruido_individual"], size=n)
        )
        indice_acesso_saude = np.clip(indice_latente, 0, 100)

        # Gerar tempo de espera como variável de razão; valores positivos em dias.
        media_log_tempo = (
            np.log(54)
            + 0.16 * gravidade_clinica
            - 0.18 * assistencia_binaria
            - 0.10 * completude_documental
            - 0.05 * capilaridade_defensoria
            + 0.06 * ruido_unidade
        )
        tempo_espera_dias = np.clip(gerador.lognormal(media_log_tempo, sigma=0.48), 1, 365)

        # Construir escores multinomiais sem impor ordem ao desfecho.
        base_logits = np.column_stack(
            [
                -0.55 + 0.35 * gravidade_clinica + 0.35 * completude_documental,
                0.20 + 0.18 * gravidade_clinica + 0.25 * completude_documental,
                0.05 + 0.20 * letramento_digital_latente + 0.12 * capilaridade_defensoria,
                0.10 - 0.18 * completude_documental - 0.12 * capilaridade_defensoria,
                -0.10 + 0.18 * (1 - completude_documental) - 0.10 * letramento_digital_latente,
            ]
        )
        efeito_multinomial = PARAMETROS_GERADORES["efeito_assistencia_logit_desfecho"] * assistencia_binaria
        deslocamento_assistencia = np.column_stack(
            [
                0.65 * efeito_multinomial,
                0.30 * efeito_multinomial,
                0.24 * efeito_multinomial,
                -0.55 * efeito_multinomial,
                -0.64 * efeito_multinomial,
            ]
        )
        logits_desfecho = base_logits + deslocamento_assistencia
        probabilidades_desfecho = softmax_estavel(logits_desfecho)
        desfecho_pedido = sortear_categorias(
            probabilidades_desfecho,
            CATEGORIAS_DESFECHO,
            gerador,
        )

        # Montar DataFrame completo para validação, incluindo objetos não exportados.
        dados_completos = pd.DataFrame(
            {
                "id_pedido": [f"{prefixo_id}-{i:06d}" for i in range(1, n + 1)],
                "assistencia_juridica": np.where(assistencia_binaria == 1, "Sim", "Não"),
                "indice_acesso_saude": np.round(indice_acesso_saude, 2),
                "desfecho_pedido": desfecho_pedido,
                "tempo_espera_dias": np.round(tempo_espera_dias, 1),
                "gravidade_clinica": gravidade_clinica,
                "renda_pc_zirc": np.round(renda_pc_zirc, 2),
                "idade": idade,
                "regiao_zirconia": regiao_zirconia,
                "unidade_zus": unidade_zus,
                "capilaridade_defensoria": capilaridade_defensoria,
                "completude_documental": np.where(completude_documental == 1, "Sim", "Não"),
                "ano_pedido": ano_pedido,
                "letramento_digital_latente": letramento_digital_latente,
                "prob_assistencia": prob_assistencia,
            }
        )
        probabilidades = pd.DataFrame(
            probabilidades_desfecho,
            columns=[f"prob_{categoria}" for categoria in CATEGORIAS_DESFECHO],
        )
        dados_completos = pd.concat([dados_completos, probabilidades], axis=1)

        # Criar versão analítica sem latente e sem probabilidades internas.
        dados_analiticos = dados_completos[VARIAVEIS_ANALITICAS].copy()

        # Padronizar tipos categóricos para preservar domínios nas próximas seções.
        dados_analiticos["assistencia_juridica"] = pd.Categorical(
            dados_analiticos["assistencia_juridica"],
            categories=CATEGORIAS_BINARIAS,
        )
        dados_analiticos["completude_documental"] = pd.Categorical(
            dados_analiticos["completude_documental"],
            categories=CATEGORIAS_BINARIAS,
        )
        dados_analiticos["desfecho_pedido"] = pd.Categorical(
            dados_analiticos["desfecho_pedido"],
            categories=CATEGORIAS_DESFECHO,
        )
        dados_analiticos["regiao_zirconia"] = dados_analiticos["regiao_zirconia"].astype("category")
        dados_analiticos["unidade_zus"] = dados_analiticos["unidade_zus"].astype("category")

        return dados_analiticos, dados_completos

    # Gerar piloto e amostra principal por fluxos independentes.
    piloto, piloto_completo = gerar_pedidos_simulados(
        n=tamanho_piloto,
        prefixo_id="PIL",
        seed=PARAMETROS_GERADORES["seed_piloto"],
    )
    dados, dados_completos_validacao = gerar_pedidos_simulados(
        n=PARAMETROS_GERADORES["n_amostra_principal"],
        prefixo_id="ZIR",
        seed=PARAMETROS_GERADORES["seed_principal"],
    )

    # Regerar a amostra principal para confirmar reprodutibilidade exata.
    dados_replicados, _ = gerar_pedidos_simulados(
        n=PARAMETROS_GERADORES["n_amostra_principal"],
        prefixo_id="ZIR",
        seed=PARAMETROS_GERADORES["seed_principal"],
    )
    pd.testing.assert_frame_equal(dados, dados_replicados, check_dtype=True)

    # Conferir dimensões, IDs e independência entre piloto e amostra principal.
    assert len(piloto) == tamanho_piloto, "O piloto deve ter n = 50."
    assert len(dados) == PARAMETROS_GERADORES["n_amostra_principal"]
    assert piloto["id_pedido"].is_unique, "IDs do piloto devem ser únicos."
    assert dados["id_pedido"].is_unique, "IDs da amostra principal devem ser únicos."
    assert set(piloto["id_pedido"]).isdisjoint(set(dados["id_pedido"])), (
        "Piloto e amostra principal não podem compartilhar IDs."
    )

    # Conferir presença dos dois grupos para permitir razão piloto e comparação.
    assert set(piloto["assistencia_juridica"].dropna()) == set(CATEGORIAS_BINARIAS), (
        "O piloto precisa conter casos com e sem assistência jurídica."
    )
    assert set(dados["assistencia_juridica"].dropna()) == set(CATEGORIAS_BINARIAS), (
        "A amostra principal precisa conter casos com e sem assistência jurídica."
    )

    # Conferir domínios, finitude dos valores e cobertura territorial.
    assert set(dados["desfecho_pedido"].cat.categories) == set(CATEGORIAS_DESFECHO)
    assert set(dados["desfecho_pedido"].dropna()).issubset(set(CATEGORIAS_DESFECHO))
    assert np.isfinite(dados["indice_acesso_saude"]).all(), "Escore com valor não finito."
    assert np.isfinite(piloto["indice_acesso_saude"]).all(), "Piloto com escore não finito."
    assert dados["unidade_zus"].nunique() >= 30, "Amostra principal deve ter ao menos 30 unidades."
    assert dados["regiao_zirconia"].nunique() == 20, "As 20 regiões devem aparecer na amostra."

    # Conferir probabilidades internas do gerador antes de descartá-las.
    colunas_prob = [f"prob_{categoria}" for categoria in CATEGORIAS_DESFECHO]
    probs = dados_completos_validacao[colunas_prob]
    assert np.isfinite(probs.to_numpy()).all(), "Probabilidades não finitas."
    assert ((probs >= 0) & (probs <= 1)).all().all(), "Probabilidades fora de [0, 1]."
    assert np.allclose(probs.sum(axis=1), 1.0), "Probabilidades não somam 1 por linha."

    # Garantir que a latente e probabilidades internas não entraram na base analítica.
    colunas_proibidas = {"letramento_digital_latente", "prob_assistencia", *colunas_prob}
    assert colunas_proibidas.isdisjoint(set(dados.columns)), "Coluna interna vazou para dados."
    assert colunas_proibidas.isdisjoint(set(piloto.columns)), "Coluna interna vazou para piloto."

    # Exportar bases analíticas em UTF-8 com BOM para melhor abertura em planilhas.
    caminho_dados = PASTA_SAIDA / "zirconia_pedidos_simulados.csv"
    caminho_piloto = PASTA_SAIDA / "zirconia_piloto_simulado.csv"
    dados.to_csv(caminho_dados, index=False, encoding="utf-8-sig")
    piloto.to_csv(caminho_piloto, index=False, encoding="utf-8-sig")

    # Produzir resumos iniciais para orientar a leitura sem realizar ainda a EDA formal.
    resumo_grupos = (
        dados.groupby("assistencia_juridica", observed=False)
        .agg(
            n=("id_pedido", "size"),
            media_indice=("indice_acesso_saude", "mean"),
            dp_indice=("indice_acesso_saude", "std"),
            mediana_espera=("tempo_espera_dias", "median"),
        )
        .reset_index()
    )
    resumo_piloto = (
        piloto.groupby("assistencia_juridica", observed=False)
        .agg(
            n=("id_pedido", "size"),
            media_indice=("indice_acesso_saude", "mean"),
            dp_indice=("indice_acesso_saude", "std"),
        )
        .reset_index()
    )

    # Exibir parâmetros e primeiras tabelas de sanidade.
    display(pd.DataFrame(PARAMETROS_GERADORES.items(), columns=["parametro", "valor"]))
    display(resumo_grupos)
    display(resumo_piloto)
    print(f"Dados principais gravados em: {caminho_dados}")
    print(f"Piloto gravado em: {caminho_piloto}")
    print("Linhas da amostra principal:", len(dados))
    print("Unidades ZUS observadas:", dados["unidade_zus"].nunique())
    """)

    md(r"""
    ### Interpretação da simulação

    A diferença bruta de médias exibida nesta seção deve ser lida apenas como
    **checagem de sanidade do gerador**. A seção de EDA fará a descrição formal,
    e a seção de modelagem estimará a associação ajustada com erros padrão
    agrupados por unidade. Como a assistência não foi sorteada, parte da diferença
    entre grupos pode decorrer de seleção observacional.

    O piloto n=50 é propositalmente pequeno. Ele será suficiente para demonstrar
    como calcular desvio padrão preliminar e razão entre grupos, mas suas
    estimativas serão instáveis. Por isso, o dimensionamento amostral posterior
    deverá apresentar análise de sensibilidade para proporções de alocação,
    desvio padrão e efeito mínimo relevante.

    A variável latente foi usada para construir um cenário mais realista de
    confundimento residual. Em uma pesquisa real, o estudante deve perguntar:
    quais variáveis não observadas favorecem simultaneamente a procura pela
    Defensoria e a obtenção de cuidado em saúde? O viés tenderia a superestimar
    ou subestimar a associação de interesse? Que desenho alternativo, coleta
    adicional ou análise de sensibilidade poderia enfrentar esse problema?
    """)
