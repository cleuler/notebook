# -*- coding: utf-8 -*-
"""Seção 2: dicionário de dados e operacionalização dos constructos."""

from collections.abc import Callable


def construir(md: Callable[[str], None], code: Callable[[str], None]) -> None:
    """Emite a tabela Markdown e o quadro verificável em pandas."""
    md(r"""
    ## 2. Dicionário de dados e quadro de variáveis

    A unidade de observação é um pedido. Cada variável deve ser definida **antes**
    de examinar os resultados. Os exemplos abaixo são valores possíveis em uma
    base fictícia e não observações reais. As covariáveis de ajuste são aferidas
    na entrada do pedido, antes da exposição, para reduzir o risco de controlar
    uma consequência do próprio atendimento.

    | Nome | Significado | Tipo | Escala | Papel | Exemplos |
    |---|---|---|---|---|---|
    | `id_pedido` | Código artificial único do pedido | Texto | Identificador, sem escala inferencial | Chave | `PED-0001`, `PED-0002` |
    | `atendimento_programa` | Recebeu orientação jurídica do programa | Categórica binária | Nominal binária | Independente principal | `Sim`, `Não` |
    | `pontuacao_acesso` | Escore construído de acesso efetivo, em pontos | Quantitativa contínua | Intervalar assumida | Dependente primária | `45,3`, `62,1` |
    | `desfecho_administrativo` | Estado do pedido na janela de observação | Categórica multinomial | Nominal, cinco níveis | Dependente secundária | `deferido_integral`, `pendente` |
    | `complexidade_previa` | Complexidade registrada na entrada | Categórica de três níveis | Ordinal | Confundidora observada | `1`, `2`, `3` |
    | `vulnerabilidade_previa` | Indicador de vulnerabilidade antes do atendimento | Categórica binária | Nominal binária | Confundidora observada | `0`, `1` |
    | `unidade` | Unidade administrativa de registro | Categórica multinomial | Nominal | Contexto e cluster | `U01`, `U30` |
    | `ano_pedido` | Ano de protocolo do pedido | Temporal discreta | Calendário | Contexto temporal | `2023`, `2025` |
    | `documentacao_inicial` | Documentos completos na entrada | Categórica binária | Nominal binária | Covariável pré-exposição | `Sim`, `Não` |
    | `acesso_digital_nao_observado` | Facilidade de usar o portal, gerada apenas para ilustrar confundimento | Latente binária | Nominal binária | Confundidora oculta, excluída da base analítica | `0`, `1` no gerador |

    **Regra de mensuração do escore.** O zero da pontuação será convencional e
    diferenças iguais serão tratadas como comparáveis. Isso é uma **hipótese de
    mensuração**; um escore produzido em pesquisa real exigirá descrição de itens,
    pesos, consistência, estabilidade temporal e evidências de validade. A escala
    não se torna intervalar apenas porque o código armazena valores decimais.

    **Regra do desfecho.** Cada pedido terá uma única categoria entre
    `deferido_integral`, `deferido_parcial`, `indeferido`, `pendente` e
    `arquivado`, segundo uma janela de acompanhamento previamente delimitada.
    Esses estados são tratados como **nominais**: sua ordem de exibição não
    autoriza médias, distâncias numéricas nem interpretação ordinal.

    **Para adaptar:** substitua cada linha por definição operacional, fonte,
    momento de aferição, códigos admitidos, regra de ausências e ao menos dois
    exemplos. Registre quem codificou as informações e como divergências de
    classificação foram resolvidas.
    """)

    code(r"""
    # Fixar os cinco rótulos nominais antes de simular o desfecho.
    CATEGORIAS_DESFECHO = [
        "deferido_integral",
        "deferido_parcial",
        "indeferido",
        "pendente",
        "arquivado",
    ]

    # Listar apenas variáveis observáveis que poderão entrar no ajuste.
    COVARIAVEIS_PREVIAS = [
        "complexidade_previa",
        "vulnerabilidade_previa",
        "documentacao_inicial",
        "unidade",
        "ano_pedido",
    ]
    VARIAVEIS_ANALITICAS = [
        "id_pedido",
        "atendimento_programa",
        "pontuacao_acesso",
        "desfecho_administrativo",
        *COVARIAVEIS_PREVIAS,
    ]

    # Construir o mesmo quadro em pandas para validar o esquema em código.
    registros_dicionario = [
        ("id_pedido", "Código artificial único do pedido", "Texto", "Identificador", "Chave", "PED-0001; PED-0002"),
        ("atendimento_programa", "Orientação jurídica recebida", "Categórica binária", "Nominal binária", "Independente principal", "Sim; Não"),
        ("pontuacao_acesso", "Escore construído de acesso efetivo", "Quantitativa contínua", "Intervalar assumida", "Dependente primária", "45,3; 62,1"),
        ("desfecho_administrativo", "Estado do pedido na janela definida", "Categórica multinomial", "Nominal, cinco níveis", "Dependente secundária", "deferido_integral; pendente"),
        ("complexidade_previa", "Complexidade registrada na entrada", "Categórica de três níveis", "Ordinal", "Confundidora observada", "1; 2; 3"),
        ("vulnerabilidade_previa", "Vulnerabilidade anterior ao atendimento", "Categórica binária", "Nominal binária", "Confundidora observada", "0; 1"),
        ("unidade", "Unidade administrativa de registro", "Categórica multinomial", "Nominal", "Contexto e cluster", "U01; U30"),
        ("ano_pedido", "Ano de protocolo do pedido", "Temporal discreta", "Calendário", "Contexto temporal", "2023; 2025"),
        ("documentacao_inicial", "Documentos completos na entrada", "Categórica binária", "Nominal binária", "Covariável pré-exposição", "Sim; Não"),
        ("acesso_digital_nao_observado", "Facilidade de uso do portal; apenas no gerador", "Latente binária", "Nominal binária", "Confundidora oculta", "0; 1 no gerador"),
    ]
    dicionario = pd.DataFrame(
        registros_dicionario,
        columns=["nome", "significado", "tipo", "escala", "papel", "exemplos"],
    )

    # Confirmar unicidade, cobertura do esquema e preenchimento das definições.
    assert dicionario["nome"].is_unique, "Há nomes de variáveis duplicados."
    assert len(CATEGORIAS_DESFECHO) == 5, "O desfecho deve ter cinco níveis."
    assert len(set(CATEGORIAS_DESFECHO)) == 5, "Os níveis devem ser distintos."
    assert "pontuacao_acesso" in VARIAVEIS_ANALITICAS
    assert "atendimento_programa" in VARIAVEIS_ANALITICAS
    assert set(VARIAVEIS_ANALITICAS).issubset(set(dicionario["nome"]))
    assert set(COVARIAVEIS_PREVIAS).issubset(set(VARIAVEIS_ANALITICAS))
    assert "acesso_digital_nao_observado" not in VARIAVEIS_ANALITICAS
    for coluna in dicionario.columns:
        assert dicionario[coluna].notna().all(), f"Campo vazio em {coluna}."
        assert dicionario[coluna].astype(str).str.strip().ne("").all(), (
            f"Campo sem conteúdo em {coluna}."
        )

    # Exibir a versão verificável; a tabela Markdown acima permanece legível sem execução.
    display(dicionario)
    print("Variáveis analíticas documentadas:", len(VARIAVEIS_ANALITICAS))
    print("Categorias nominais do desfecho:", ", ".join(CATEGORIAS_DESFECHO))
    """)

    md(r"""
    ### Validade das medidas e papel das variáveis

    O quadro separa o que foi observado do que é apenas parte do mecanismo
    gerador. `acesso_digital_nao_observado` será omitida da base analítica para
    ilustrar que um coeficiente ajustado ainda pode sofrer confundimento. Não se
    deve afirmar que a variável foi medida no estudo observacional.

    Documentação **inicial** pode ser um controle prévio; documentação corrigida
    **após** o atendimento poderia ser mediadora. Controlar esta última mudaria a
    pergunta estimada e poderia remover parte da associação de interesse. O mesmo
    cuidado vale para qualquer variável registrada durante a tramitação.

    **Registro do estudante:** qual é a evidência de que o escore mede acesso
    efetivo? Duas pessoas poderiam codificar o mesmo desfecho da mesma forma?
    Quais categorias estão sujeitas a erro ou censura pela janela retrospectiva?
    Que variável oculta plausível alteraria a direção da associação observada?
    """)
