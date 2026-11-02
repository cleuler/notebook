# -*- coding: utf-8 -*-
"""Seção 2: dicionário de dados e quadro de variáveis."""

from collections.abc import Callable


def construir(md: Callable[[str], None], code: Callable[[str], None]) -> None:
    """Emite o dicionário em Markdown e em DataFrame validável."""
    md(r"""
    ## 2. Dicionário de Dados e Quadro de Variáveis

    A tabela abaixo é parte do protocolo, não apenas documentação posterior. Em
    uma pesquisa empírica replicável, cada variável deve ter definição operacional,
    domínio admissível, escala de mensuração, unidade de medida, tipo computacional
    e papel analítico definidos antes da coleta ou da simulação principal.

    | Nome abreviado | Significado | Tipo | Escala de medição | Unidade de medida | Tipo Python adequado | Papel | Exemplos |
    |---|---|---|---|---|---|---|---|
    | `id_pedido` | Identificador artificial único do pedido de acesso à saúde | Texto | Identificador sem escala inferencial | Não se aplica | `string` | Chave | `ZIR-000001`, `ZIR-000250` |
    | `assistencia_juridica` | Recebeu assistência jurídica institucional antes da decisão final | Categórica binária | Nominal binária | Categoria Sim/Não | `category` | Independente principal | `Sim`, `Não` |
    | `indice_acesso_saude` | Escore composto de acesso efetivo ao cuidado em saúde | Numérica contínua | Intervalar assumida | Pontos de 0 a 100 | `float64` | Dependente primária | `41.7`, `68.2` |
    | `desfecho_pedido` | Resultado final observado na janela retrospectiva | Categórica multinomial | Nominal com cinco níveis | Categoria | `category` | Dependente secundária | `internacao_realizada`, `negado` |
    | `tempo_espera_dias` | Tempo entre o protocolo do pedido e a decisão ou atendimento | Numérica contínua | Razão | Dias | `float64` | Desfecho auxiliar/covariável descritiva | `12.5`, `83.0` |
    | `gravidade_clinica` | Gravidade clínica registrada antes da assistência | Categórica ordinal | Ordinal | Nível 1 a 4 | `Int64` ou `category` ordenada | Confundidora observada | `1`, `4` |
    | `renda_pc_zirc` | Renda familiar mensal per capita do requerente | Numérica contínua | Razão | Z$ por pessoa/mês | `float64` | Confundidora observada | `180.50`, `940.00` |
    | `idade` | Idade do requerente no protocolo | Numérica discreta | Razão | Anos completos | `Int64` | Confundidora observada | `34`, `72` |
    | `regiao_zirconia` | Região administrativa da Zircônia | Categórica multinomial | Nominal | Região | `category` | Estrato/contexto | `R03`, `R17` |
    | `unidade_zus` | Unidade territorial do ZUS vinculada ao pedido | Categórica multinomial | Nominal | Unidade administrativa | `category` | Cluster inferencial | `UZ-014`, `UZ-087` |
    | `capilaridade_defensoria` | Presença local da Defensoria Pública antes do pedido | Categórica ordinal | Ordinal | Nível 0 a 3 | `Int64` ou `category` ordenada | Confundidora/contexto | `0`, `3` |
    | `completude_documental` | Documentação inicial suficiente para análise do pedido | Categórica binária | Nominal binária | Categoria Sim/Não | `category` | Covariável prévia | `Sim`, `Não` |
    | `ano_pedido` | Ano de protocolo do pedido | Temporal discreta | Calendário | Ano | `Int64` | Contexto temporal | `2023`, `2025` |
    | `letramento_digital_latente` | Facilidade não observada de usar sistemas do ZUS e buscar canais institucionais | Latente binária | Nominal binária | Não observada | Não exportar | Confundidora oculta | `0`, `1` apenas no gerador |

    **Ressalva sobre escala intervalar.** O `indice_acesso_saude` será tratado
    como intervalar porque diferenças de pontos serão interpretadas como
    comparáveis. Isso é uma hipótese substantiva e psicométrica do instrumento,
    não uma consequência automática do uso de números decimais. Em dados reais,
    o estudante deve justificar itens, pesos, consistência e evidências de validade.

    **Ressalva sobre escala multinomial.** `desfecho_pedido` terá cinco categorias
    nominais exaustivas e exclusivas. A ordem de apresentação é didática e não
    autoriza calcular médias dos códigos nem tratar o desfecho como ordinal sem
    argumento teórico independente.
    """)

    code(r"""
    # Definir categorias nominais do desfecho antes da simulação.
    CATEGORIAS_DESFECHO = [
        "internacao_realizada",
        "tratamento_ambulatorial",
        "fornecimento_medicamento",
        "negado",
        "pendente_ou_sem_execucao",
    ]

    # Definir categorias binárias padronizadas para variáveis Sim/Não.
    CATEGORIAS_BINARIAS = ["Não", "Sim"]

    # Listar covariáveis medidas antes da exposição ou no contexto inicial.
    COVARIAVEIS_PREVIAS = [
        "gravidade_clinica",
        "renda_pc_zirc",
        "idade",
        "regiao_zirconia",
        "unidade_zus",
        "capilaridade_defensoria",
        "completude_documental",
        "ano_pedido",
    ]

    # Listar variáveis que devem existir na base analítica exportada.
    VARIAVEIS_ANALITICAS = [
        "id_pedido",
        "assistencia_juridica",
        "indice_acesso_saude",
        "desfecho_pedido",
        "tempo_espera_dias",
        *COVARIAVEIS_PREVIAS,
    ]

    # Registrar o dicionário também como DataFrame para auditoria computacional.
    registros_dicionario = [
        {
            "nome": "id_pedido",
            "significado": "Identificador artificial único do pedido de acesso à saúde",
            "tipo": "texto",
            "escala": "identificador",
            "unidade": "não se aplica",
            "tipo_python": "string",
            "papel": "chave",
            "exemplos": "ZIR-000001; ZIR-000250",
        },
        {
            "nome": "assistencia_juridica",
            "significado": "Recebeu assistência jurídica institucional antes da decisão final",
            "tipo": "categórica binária",
            "escala": "nominal binária",
            "unidade": "Sim/Não",
            "tipo_python": "category",
            "papel": "independente principal",
            "exemplos": "Sim; Não",
        },
        {
            "nome": "indice_acesso_saude",
            "significado": "Escore composto de acesso efetivo ao cuidado em saúde",
            "tipo": "numérica contínua",
            "escala": "intervalar assumida",
            "unidade": "pontos de 0 a 100",
            "tipo_python": "float64",
            "papel": "dependente primária",
            "exemplos": "41.7; 68.2",
        },
        {
            "nome": "desfecho_pedido",
            "significado": "Resultado final observado na janela retrospectiva",
            "tipo": "categórica multinomial",
            "escala": "nominal com cinco níveis",
            "unidade": "categoria",
            "tipo_python": "category",
            "papel": "dependente secundária",
            "exemplos": "internacao_realizada; negado",
        },
        {
            "nome": "tempo_espera_dias",
            "significado": "Tempo entre protocolo e decisão ou atendimento",
            "tipo": "numérica contínua",
            "escala": "razão",
            "unidade": "dias",
            "tipo_python": "float64",
            "papel": "desfecho auxiliar/covariável descritiva",
            "exemplos": "12.5; 83.0",
        },
        {
            "nome": "gravidade_clinica",
            "significado": "Gravidade clínica registrada antes da assistência",
            "tipo": "categórica ordinal",
            "escala": "ordinal",
            "unidade": "nível 1 a 4",
            "tipo_python": "Int64 ou category ordenada",
            "papel": "confundidora observada",
            "exemplos": "1; 4",
        },
        {
            "nome": "renda_pc_zirc",
            "significado": "Renda familiar mensal per capita do requerente",
            "tipo": "numérica contínua",
            "escala": "razão",
            "unidade": "Z$ por pessoa/mês",
            "tipo_python": "float64",
            "papel": "confundidora observada",
            "exemplos": "180.50; 940.00",
        },
        {
            "nome": "idade",
            "significado": "Idade do requerente no protocolo",
            "tipo": "numérica discreta",
            "escala": "razão",
            "unidade": "anos completos",
            "tipo_python": "Int64",
            "papel": "confundidora observada",
            "exemplos": "34; 72",
        },
        {
            "nome": "regiao_zirconia",
            "significado": "Região administrativa da Zircônia",
            "tipo": "categórica multinomial",
            "escala": "nominal",
            "unidade": "região",
            "tipo_python": "category",
            "papel": "estrato/contexto",
            "exemplos": "R03; R17",
        },
        {
            "nome": "unidade_zus",
            "significado": "Unidade territorial do ZUS vinculada ao pedido",
            "tipo": "categórica multinomial",
            "escala": "nominal",
            "unidade": "unidade administrativa",
            "tipo_python": "category",
            "papel": "cluster inferencial",
            "exemplos": "UZ-014; UZ-087",
        },
        {
            "nome": "capilaridade_defensoria",
            "significado": "Presença local da Defensoria Pública antes do pedido",
            "tipo": "categórica ordinal",
            "escala": "ordinal",
            "unidade": "nível 0 a 3",
            "tipo_python": "Int64 ou category ordenada",
            "papel": "confundidora/contexto",
            "exemplos": "0; 3",
        },
        {
            "nome": "completude_documental",
            "significado": "Documentação inicial suficiente para análise do pedido",
            "tipo": "categórica binária",
            "escala": "nominal binária",
            "unidade": "Sim/Não",
            "tipo_python": "category",
            "papel": "covariável prévia",
            "exemplos": "Sim; Não",
        },
        {
            "nome": "ano_pedido",
            "significado": "Ano de protocolo do pedido",
            "tipo": "temporal discreta",
            "escala": "calendário",
            "unidade": "ano",
            "tipo_python": "Int64",
            "papel": "contexto temporal",
            "exemplos": "2023; 2025",
        },
        {
            "nome": "letramento_digital_latente",
            "significado": "Facilidade não observada de usar sistemas do ZUS e buscar canais institucionais",
            "tipo": "latente binária",
            "escala": "nominal binária",
            "unidade": "não observada",
            "tipo_python": "não exportar",
            "papel": "confundidora oculta",
            "exemplos": "0; 1 apenas no gerador",
        },
    ]
    dicionario = pd.DataFrame(registros_dicionario)

    # Validar unicidade e completude do dicionário.
    assert dicionario["nome"].is_unique, "O dicionário contém nomes duplicados."
    assert len(CATEGORIAS_DESFECHO) == 5, "O desfecho multinomial deve ter cinco níveis."
    assert len(set(CATEGORIAS_DESFECHO)) == 5, "As categorias do desfecho devem ser distintas."
    assert set(VARIAVEIS_ANALITICAS).issubset(set(dicionario["nome"])), (
        "Há variável analítica sem descrição no dicionário."
    )
    assert "assistencia_juridica" in VARIAVEIS_ANALITICAS, "Exposição ausente."
    assert "indice_acesso_saude" in VARIAVEIS_ANALITICAS, "Dependente primária ausente."
    assert "desfecho_pedido" in VARIAVEIS_ANALITICAS, "Dependente secundária ausente."
    assert "letramento_digital_latente" not in VARIAVEIS_ANALITICAS, (
        "A latente não deve constar da base analítica."
    )
    assert set(COVARIAVEIS_PREVIAS).issubset(set(VARIAVEIS_ANALITICAS)), (
        "Covariáveis prévias devem estar no esquema analítico."
    )

    # Exigir preenchimento em todos os campos do quadro.
    for coluna in dicionario.columns:
        valores = dicionario[coluna].astype(str).str.strip()
        assert valores.ne("").all(), f"Campo vazio encontrado em {coluna}."

    # Exibir a versão computacional do dicionário.
    display(dicionario)
    print("Total de variáveis analíticas:", len(VARIAVEIS_ANALITICAS))
    print("Categorias do desfecho:", ", ".join(CATEGORIAS_DESFECHO))
    """)

    md(r"""
    ### Interpretação metodológica da seção

    O dicionário explicita quais variáveis são observadas e quais pertencem apenas
    ao mecanismo didático de simulação. Essa separação evita uma falha comum:
    ajustar o modelo por uma variável que, na pesquisa real, não estaria disponível
    ou seria medida depois da exposição.

    Em uma adaptação com dados reais, o estudante deve acrescentar: fonte de cada
    variável, responsável pela codificação, regras para valores ausentes, tratamento
    de duplicidades, janela de aferição e justificativa para o papel analítico
    assumido. O quadro também deve ser depositado no repositório antes da coleta,
    para reduzir graus de liberdade analíticos e aumentar replicabilidade.
    """)
