# -*- coding: utf-8 -*-
"""Seção 1: delimitação do problema, desenho e ambiente."""

from collections.abc import Callable


def construir(md: Callable[[str], None], code: Callable[[str], None]) -> None:
    """Emite a seção inicial do template didático de Zircônia."""
    md(r"""
    # CDEaDPP 2026.2 - Trabalho Final: Zircônia

    ## 1. Delimitação do Problema e Desenho da Pesquisa

    Este notebook é um **template educacional de protocolo empírico replicável**.
    O caso didático é inteiramente simulado e toma como cenário o país imaginário
    Zircônia: população grande, fortemente desigual, sistema público de saúde
    pressionado por filas e presença territorial incompleta da Defensoria Pública.
    O objetivo é ensinar como passar de um problema empírico delimitado para um
    quadro de variáveis, dados simulados, exploração, modelagem, testes de
    hipóteses e planejamento amostral.

    A unidade de análise será o **pedido individual de acesso à saúde** registrado
    no ZUS. O desenho é **observacional retrospectivo**: a assistência jurídica
    não é sorteada pelo pesquisador; ela ocorre de modo associado a características
    da pessoa, do caso e da unidade territorial. Por isso, mesmo quando a simulação
    injeta um efeito gerador conhecido, a interpretação estatística no notebook
    deve falar em associação ajustada, não em prova causal automática.

    | Elemento T.E.M.P. | Delimitação didática | Decisão que o estudante deve adaptar |
    |---|---|---|
    | Tempo | Pedidos simulados entre 2023 e 2025 | Fixar janela de coleta e seguimento |
    | Espaço | 20 regiões e unidades territoriais do ZUS na Zircônia | Descrever sistema de referência e cobertura |
    | Matéria | Acesso à saúde pública e acesso à justiça | Definir política, direito ou serviço estudado |
    | População | Pessoas de baixa renda com pedido de atendimento/intervenção em saúde | Definir população-alvo, acessível e amostrada |
    | Unidade elementar | Pedido administrativo/judicial de saúde | Verificar múltiplos pedidos por pessoa |
    | Exposição | Assistência jurídica institucional antes da decisão final | Definir momento e critério de exposição |
    | Desfecho primário | Índice de acesso efetivo à saúde | Justificar constructo e escala |
    | Desfecho secundário | Desfecho do pedido em cinco categorias nominais | Fixar categorias exaustivas e exclusivas |

    **Problema de pesquisa modelo:** entre pedidos de saúde da população de baixa
    renda da Zircônia, há associação entre assistência jurídica institucional e
    acesso efetivo à saúde, após ajuste por gravidade clínica, renda, idade,
    completude documental, região, ano e unidade do ZUS?

    **Hipótese primária bilateral:** $H_0: \beta_{\text{assistência jurídica}}=0$
    contra $H_1: \beta_{\text{assistência jurídica}}\ne0$ no modelo de regressão
    linear para `indice_acesso_saude`.

    **Hipótese secundária:** $H_0$: a distribuição de `desfecho_pedido` é igual
    entre pedidos com e sem assistência jurídica. $H_1$: ao menos uma das cinco
    proporções difere.

    **Variáveis ocultas e confundidoras.** Letramento digital, capacidade familiar
    de navegar no ZUS, qualidade prévia dos documentos, distância até a Defensoria
    e capital social podem afetar simultaneamente a chance de receber assistência
    jurídica e o acesso efetivo à saúde. O gerador de dados incluirá uma variável
    latente de letramento digital para ilustrar confundimento residual; ela não
    será exportada para a base analítica.

    **Fontes de apoio usadas na construção do template.** A organização segue os
    guias locais da disciplina sobre formulação de problema T.E.M.P., população,
    sistema de referência, unidade amostral, escalas de medição, erros amostrais
    e não amostrais, hipóteses, erros tipo I e II, validade interna, validade
    externa e variáveis ocultas. Como referências bibliográficas de apoio, o
    estudante deve consultar, entre outras, Bolfarine e Bussab para amostragem,
    Barbetta e Agresti/Finlay para estatística social, Babbie e Bryman para
    desenho de pesquisa social, Pearl/Glymour/Jewell para caminhos causais e
    Bruce/Bruce para práticas de ciência de dados.
    """)

    code(r"""
    # Importar bibliotecas necessárias para todo o notebook.
    import importlib.metadata
    from pathlib import Path

    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import scipy.stats as stats
    import seaborn as sns
    import statsmodels.api as sm
    from IPython.display import display
    from statsmodels.stats.power import GofChisquarePower, TTestIndPower

    # Fixar parâmetros inferenciais antes de observar qualquer resultado.
    SEMENTE = 2026
    alpha = 0.05
    beta = 0.15
    poder_alvo = 1 - beta
    tamanho_piloto = 50

    # Criar gerador principal de números pseudoaleatórios para a simulação.
    rng = np.random.default_rng(SEMENTE)

    # Localizar a raiz do projeto por arquivos estáveis do repositório.
    candidatos_raiz = (Path.cwd(), *Path.cwd().parents)
    raizes_possiveis = [
        pasta
        for pasta in candidatos_raiz
        if (pasta / "pyproject.toml").is_file()
        and (pasta / "md" / "trabalho_final_simulacao.md").is_file()
    ]
    if not raizes_possiveis:
        raise FileNotFoundError(
            "Execute o notebook na raiz do projeto ou em uma subpasta dele."
        )
    RAIZ_PROJETO = raizes_possiveis[0].resolve()

    # Preparar diretórios de saída usados pelas próximas seções.
    PASTA_SAIDA = (RAIZ_PROJETO / "out" / "cdedpp_2026_zirconia").resolve()
    PASTA_FIGURAS = (PASTA_SAIDA / "figuras").resolve()
    PASTA_SAIDA.mkdir(parents=True, exist_ok=True)
    PASTA_FIGURAS.mkdir(parents=True, exist_ok=True)

    # Validar parâmetros que controlam inferência e reprodutibilidade.
    assert isinstance(SEMENTE, int), "A semente precisa ser um inteiro."
    assert 0 < alpha < 1, "alpha deve estar entre 0 e 1."
    assert 0 < beta < 1, "beta deve estar entre 0 e 1."
    assert np.isclose(poder_alvo, 1 - beta), "poder_alvo deve ser igual a 1 - beta."
    assert tamanho_piloto == 50, "Este template exige piloto simulado com n = 50."
    assert PASTA_SAIDA.is_relative_to(RAIZ_PROJETO), "Saída fora da raiz do projeto."
    assert PASTA_FIGURAS.is_relative_to(PASTA_SAIDA), "Figuras fora da pasta da seção."

    # Configurar estilo visual e formato de exibição para tabelas.
    sns.set_theme(style="whitegrid", context="notebook")
    plt.rcParams["figure.figsize"] = (9, 5)
    plt.rcParams["axes.titlesize"] = 12
    plt.rcParams["axes.labelsize"] = 10
    pd.set_option("display.precision", 3)
    pd.set_option("display.max_columns", 80)

    # Registrar versões para reprodutibilidade computacional.
    pacotes = ("numpy", "pandas", "matplotlib", "seaborn", "scipy", "statsmodels")
    versoes = {
        pacote: importlib.metadata.version(pacote)
        for pacote in pacotes
    }
    quadro_ambiente = pd.DataFrame(
        {
            "item": ["raiz", "pasta_saida", "semente", "alpha", "beta", "poder", "piloto_n"],
            "valor": [
                str(RAIZ_PROJETO),
                str(PASTA_SAIDA),
                SEMENTE,
                alpha,
                beta,
                poder_alvo,
                tamanho_piloto,
            ],
        }
    )

    # Exibir o registro do ambiente sem gravar outputs no arquivo-fonte.
    display(quadro_ambiente)
    display(pd.DataFrame(versoes.items(), columns=["pacote", "versao"]))
    """)

    md(r"""
    ### Interpretação metodológica da seção

    A semente garante que os mesmos dados simulados possam ser recuperados por
    outro pesquisador. Ela não transforma o desenho em experimento aleatorizado.
    O grupo com assistência jurídica continuará sendo selecionado por um mecanismo
    observacional, possivelmente relacionado a gravidade, vulnerabilidade, região
    e variáveis não observadas. Essa distinção é central para a validade interna.

    Ao adaptar o template, o estudante deve registrar: população-alvo, população
    acessível, sistema de referência, critério de inclusão, critério de exclusão,
    unidade de análise, janela temporal, instrumento de medição, variáveis ocultas
    plausíveis, direção esperada dos vieses e limites de generalização.
    """)
