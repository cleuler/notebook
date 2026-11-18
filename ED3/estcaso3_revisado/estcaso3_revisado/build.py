"""Gera a edição didática auditada a partir do notebook executável original.

Execute na raiz de cdedpp: .venv/bin/python estcaso3_revisado/build.py
O estudo original permanece intacto. As saídas desta edição ficam nesta pasta.
"""
from __future__ import annotations

import re
from pathlib import Path

import nbformat

import revisao_final as RF

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
SOURCE = ROOT / "estcaso3_rafael.ipynb"
TARGET = HERE / "estcaso3_revisado.ipynb"

# Cada nota acompanha um bloco de cálculo. A pergunta e a leitura estão no
# texto corrido, de modo que o colega possa seguir o argumento sem abrir o código.
GUIDES = {
 1: "O estudo começa registrando versões, caminhos e sementes. Isso permite identificar o ambiente que produziu as tabelas e repetir a simulação sem que a ordem das células mude seus números. Os dados brutos continuam na pasta do projeto; esta edição grava as saídas em uma pasta própria.",
 3: "A primeira conferência é a identidade dos processos. Números CNJ são identificadores, não quantidades: a leitura como texto preserva zeros à esquerda. A validação do dígito verificador e o mapa de correções evitam que um erro de planilha gere uma falsa ausência no DataJud.",
 5: "As respostas das três fases precisam conservar a diferença entre “não ocorreu” e “não foi avaliado”. O código tipa cada sinal e reconstrói o funil; a tabela seguinte mostra quais denominadores pertencem a cada pergunta. Uma proporção calculada sobre 233 processos não representa automaticamente os 595 sorteados.",
 7: "Depois da padronização, a auditoria procura valores ausentes e contradições entre a conclusão da fase e os campos preenchidos. Registrar essas exceções é parte da análise: uma regra que apenas força consistência esconderia problemas do dado original.",
 10: "A moldura define a população sobre a qual uma estimativa amostral pode ser projetada. A contagem por etapas reconstrói as exclusões da extração do TJRN e permite verificar se os 50.320 processos usados no estudo são realmente os mesmos do denominador final.",
 13: "Uma amostra estratificada deve ser lida segundo o modo como foi sorteada. Aqui se confere a alocação por ano e a correspondência com as faixas da planilha; essa informação orienta os intervalos e impede tratar a distribuição entre juizados como se fosse o estrato de sorteio.",
 16: "O Quadro de Variáveis liga cada coluna à definição substantiva, à escala e à regra de ausência. O conjunto curado é exportado depois dessas verificações, para que as análises usem a mesma versão dos dados e os colegas possam rastrear cada transformação.",
 19: "O DataJud registra movimentos e situação administrativa, não uma leitura integral dos autos. O módulo de TPU traduz códigos em um desfecho operacional. Esta é uma medida indireta, cuja regra precisa ser declarada antes de discutir associação com litigância predatória.",
 20: "Cada processo pode ter vários documentos e graus. A consolidação reduz isso a uma linha por número CNJ, mantendo o grau de entrada e os eventos relevantes. A junção com a amostra é validada como um para um, pois duplicatas alterariam contagens e probabilidades.",
 22: "Comparar duas regras automáticas revela divergências de implementação, mas não substitui a conferência nos autos. A tabela mostra onde a regra TPU completa e a regra simplificada concordam; o resultado deve continuar identificado como proxy até a validação humana.",
 25: "Esta auditoria verifica automaticamente a cronologia dos eventos, a cobertura por ano e a concordância entre duas regras de TPU. Ela encontra incoerências detectáveis sem abrir autos. A concordância entre algoritmos que usam a mesma fonte não mede a validade jurídica do desfecho; esse limite permanece declarado.",
 27: "O conjunto analítico reúne os sinais da pesquisa e os campos derivados do DataJud, preservando um processo por linha. A nova checagem do número CNJ protege as análises posteriores contra perdas silenciosas no cruzamento das fontes.",
 29: "Antes de modelar, é preciso saber a frequência de cada sinal no grupo em que ele pôde ser observado. O intervalo de Wilson descreve a incerteza de cada proporção; para sinais raros, ele é mais informativo que apenas uma porcentagem arredondada.",
 32: "As tabelas de contingência descrevem como a classificação da pesquisa se distribui por ano, juizado, classe e desfecho. Os testes avaliam incompatibilidade com independência, enquanto o tamanho de efeito mostra a força da associação; nenhum dos dois estabelece causalidade.",
 35: "O número de sinais F2 é uma contagem com muitos zeros e dispersão possivelmente maior que a média. Comparar Poisson, binomial negativa e uma forma com zeros adicionais ajuda a escolher uma descrição adequada antes de interpretar coeficientes.",
 38: "O tempo observado depende de encerramento e censura. A análise de sobrevivência separa quem teve desfecho de quem ainda estava em observação; por isso uma média simples dos tempos encerrados responderia a outra pergunta e poderia introduzir viés.",
 41: "Uma probabilidade condicional exige nomear o evento e o grupo usado como denominador. As tabelas por linha e por coluna usam as mesmas contagens, mas respondem a perguntas diferentes: risco de indício entre expostos e frequência da exposição entre os classificados.",
 43: "O mesmo número de indícios produz proporções diferentes entre sorteados, elegíveis e casos que alcançaram a Fase III. O cálculo torna visível esse efeito de seleção e ajuda a evitar a troca indevida entre P(A dado B) e P(B dado A).",
 46: "Os sinais F2 são comparados com o indício apenas onde foram avaliados. A correção para múltiplas comparações reduz falsas descobertas quando se examinam muitos sinais; comparações escolhidas após observar os dados são identificadas como exploratórias.",
 49: "Bayes combina uma crença inicial com a frequência de um desfecho sob hipóteses concorrentes. As verossimilhanças vêm da amostra e o denominador normaliza as possibilidades. A posteriori apresentada é um exemplo condicionado à priori escolhida, não um diagnóstico validado para um processo individual.",
 52: "No nível da prevalência, a hipótese se refere a uma proporção desconhecida da população, e não ao rótulo de um processo. As diferentes distribuições Beta mostram quanto a conclusão depende da força e da média atribuídas à informação anterior.",
 55: "Uma AUC pode permanecer igual quando a prevalência muda, mas o valor preditivo positivo não. Esta conta traduz a taxa-base para a leitura prática de uma classificação e mostra por que o desempenho na Fase III não pode ser transportado diretamente à população.",
 58: "A análise de correspondência resume diferenças entre perfis de categorias em poucos eixos. A proximidade no mapa é descritiva e depende das massas marginais; por isso os gráficos devem ser lidos junto com a tabela de contingência e a inércia.",
 61: "A correspondência múltipla estende a ideia aos vários sinais F2. A correção das inércias ajuda a não superinterpretar eixos fracos, e as variáveis suplementares são projetadas sem determinar o ajuste. O biplot é um mapa de padrões, não um teste de predação.",
 64: "As três categorias jurídicas são exclusivas, mas têm ordem. O multinomial não impõe ordem; o logito ordinal a utiliza e precisa do pressuposto de chances proporcionais. O confronto entre formas permite decidir qual restrição é sustentada pelos dados.",
 66: "A razão contínua decompõe a pergunta em duas: primeiro, há indício? Depois, entre os indícios, há certeza? O segundo passo usa menos processos e pode sofrer separação; a incerteza dos coeficientes deve pesar mais que a aparência de um valor pontual.",
 68: "A logística condicional compara processos dentro de grupos JEC por ano e descarta estratos sem variação do desfecho. Os resultados valem para esse conjunto informativo. A análise de Firth e a auditoria de colinearidade verificam a estabilidade de estimativas em células raras.",
 70: "Repetir os modelos nos 444 elegíveis mostra o efeito de mudar o universo analítico. A recodificação dos processos sem F2 decorre da regra de classificação do estudo; ela não é uma observação independente de que a lide seja juridicamente não predatória.",
 73: "AIC e BIC só comparam modelos ajustados à mesma resposta e aos mesmos casos. A tabela de três classes identifica o compromisso entre ajuste e complexidade; o modelo binário original é mostrado separadamente, pois responde a outra variável-alvo.",
 75: "ROC e Gini avaliam a ordenação dos casos na mesma dicotomia usada pela pesquisa. Aqui todos os modelos recebem os mesmos três sinais F2 e há poucos padrões distintos; AUC igual mostra empate na ordenação, não equivalência geral de ajuste ou calibração.",
 77: "A validação cruzada reserva casos para avaliação e reajusta os modelos nos demais. Ela reduz o otimismo da AUC calculada nos dados de treino. Como as divisões se repetem sobre a mesma amostra, a dispersão entre repetições não deve ser lida como um novo intervalo populacional.",
 79: "A matriz de confusão traduz escores em decisões num corte explícito. Sensibilidade, especificidade e valor preditivo respondem a perguntas distintas; a classe de certeza merece atenção própria porque erros nela têm significado substantivo diferente.",
 82: "Para aplicar o modelo à moldura, categorias e cortes numéricos devem ser idênticos nos dados de treino e nos novos processos. O código guarda essa codificação. Ela representa trajetória administrativa, não contém os sinais da petição nem a massificação que definem o rótulo jurídico.",
 83: "A análise de classes latentes procura perfis de coocorrência sem usar a classificação da pesquisa no ajuste. Fixar três grupos permite cumprir o exercício; BIC e testes de sensibilidade mostram se os próprios registros sustentam essa escolha. A ordenação por desfecho é uma hipótese interpretativa.",
 85: "A matriz confronta grupos de trajetória com os rótulos atribuídos na pesquisa. É uma checagem de significado, mas usa os mesmos processos que ajustaram a mistura e orientaram a regra de ordenação. Portanto, não é uma estimativa independente de desempenho em casos futuros.",
 87: "Comparar agrupamentos nos mesmos 233 processos separa duas questões: os F2 contêm sinais da petição; o DataJud contém a trajetória posterior. Incluir F3 eleva a concordância por construção, pois F3 participa diretamente da definição da classe jurídica.",
 89: "Simular a partir de um modelo ajustado verifica se o algoritmo consegue recuperar classes quando suas próprias hipóteses são verdadeiras. Esse ensaio não valida a existência de três classes jurídicas no mundo real nem elimina a necessidade de conferência externa.",
 91: "Um modelo supervisionado com os mesmos campos do DataJud serve como comparação exploratória: ele pode usar os rótulos no treino, mas continua limitado pela informação disponível. Seu desempenho cruzado não é um teto matemático para todos os modelos possíveis.",
 94: "A aplicação à população parte da moldura de 50.320 números e marca separadamente os registros sem documento. Comparar o desfecho na amostra e no restante da moldura verifica uma variável observável; não demonstra que a amostra e a população sejam equivalentes quanto à predação.",
 96: "O modelo atribui perfis de trajetória aos processos com documento. A planilha desta edição usa nomes neutros e probabilidades de pertença à mistura. Como a concordância com os rótulos da pesquisa é baixa, esses grupos não podem ser apresentados como listas de indício ou certeza.",
 99: "A proporção de perfis na população não mede a prevalência de litigância predatória. A inversão de Rogan–Gladen é exibida apenas como diagnóstico de sensibilidade: quando o índice de Youden se aproxima de zero, pequenas mudanças nos erros dos grupos produzem enormes mudanças na conta. Nenhum teste de equivalência é calculado nesta edição.",
 102: "A simulação fornece dados artificiais com parâmetros conhecidos para que colegas possam executar o procedimento sem expor processos reais. A comparação entre valores geradores e reestimados mostra o que uma amostra deste tamanho consegue recuperar sob as hipóteses do gerador.",
 104: "O quadro transforma cada variável em uma definição operacional: escala, unidade, categorias, ausência, validade e modelo gerador. Ele é um molde de documentação; antes de copiá-lo para outra pesquisa, é preciso redefinir cada linha segundo a pergunta e a fonte daquele projeto.",
 108: "A síntese lista as verificações automáticas e os avisos de execução. Conferir com o gabarito detecta divergência numérica, mas não comprova a validade jurídica do desfecho nem a transportabilidade dos modelos; essas duas questões dependem das evidências e limitações discutidas acima.",
}
GUIDES[1] = "## 1. Ambiente, versões e sementes\n\n" + GUIDES[1]

HOLDOUT_NOTE = """### Verificação temporal fora do ajuste

A matriz anterior usa os mesmos processos que serviram para ajustar a mistura. Para examinar se a correspondência entre perfis e rótulos se mantém em casos não vistos, o modelo abaixo é ajustado apenas com processos de 2022 e 2023. Cortes de tempo e assuntos frequentes também são definidos nesse grupo de treino. Os processos de 2024 entram somente na atribuição de perfil e no confronto final com a classificação da pesquisa. A regra de ordenar os perfis continua a mesma, sem usar os rótulos de 2024.

Uma baixa concordância nessa avaliação reforça a limitação de informação do DataJud. Mesmo uma concordância alta ainda precisaria de validação dos desfechos nos autos e de outra amostra para sustentar uso individual.
"""

HOLDOUT_CODE = """# LCA ajustada em 2022–2023 e examinada nos processos de 2024
from sklearn.metrics import cohen_kappa_score, confusion_matrix
treino = (l10.ano.astype(int).to_numpy() < 2024)
teste = ~treino
X_T = XDJ.copy()
for bruto, codificado in [('t_desfecho', 'tempo_tercil'), ('n_movimentos', 'movimentos_tercil')]:
    cortes = np.quantile(l10.loc[treino, bruto].astype(float), [1 / 3, 2 / 3])
    valores = l10[bruto].astype(float)
    X_T[codificado] = np.where(valores.isna(), -1, np.digitize(valores, cortes))
top_assuntos = l10.loc[treino, 'assunto_principal'].value_counts().index[:4].tolist()
X_T['assunto'] = [top_assuntos.index(a) if a in top_assuntos else 4 for a in l10.assunto_principal]
rng_hold = np.random.default_rng(SEMENTES['lca'])
modelo_hold = C.lca_categorica(X_T.loc[treino, IND_DJ].to_numpy(), 3, rng_hold, n_init=20)
modelo_hold = C.lca_reordenar(modelo_hold, np.argsort(escore_ordem(modelo_hold)))
X_2024 = X_T.loc[teste, IND_DJ].to_numpy().copy()
for j, nc in enumerate(modelo_hold['ncat']):
    X_2024[X_2024[:, j] >= nc, j] = -1  # categoria não vista no treino: marginalizar
prev_2024 = C.lca_posteriori(modelo_hold, X_2024).argmax(1)
real_2024 = l10.loc[teste, 'classe3_cod'].astype(int).to_numpy()
cm_2024 = confusion_matrix(real_2024, prev_2024, labels=[0, 1, 2])
rb, pb = real_2024 >= 1, prev_2024 >= 1
se_2024 = (rb & pb).sum() / rb.sum()
es_2024 = (~rb & ~pb).sum() / (~rb).sum()
j_2024 = se_2024 + es_2024 - 1
kp_2024 = cohen_kappa_score(real_2024, prev_2024, weights='linear')
display(pd.DataFrame(cm_2024, index=[f'pesquisa: {n}' for n in NIVEIS_CLASSE3],
                     columns=[f'perfil {i}' for i in (1, 2, 3)]))
display(pd.Series({'treino 2022–2023': int(treino.sum()), 'avaliação 2024': int(teste.sum()),
                   'kappa ponderado 2024': kp_2024, 'sensibilidade indício 2024': se_2024,
                   'especificidade indício 2024': es_2024, 'J de Youden 2024': j_2024},
                  name='avaliação temporal').to_frame())
display(Markdown(f'**Leitura.** Nos {int(teste.sum())} processos de 2024, mantidos fora do ajuste, '
                 f'o kappa ponderado foi {fnum(kp_2024, 3)} e o índice J de Youden foi {fnum(j_2024, 3)}. '
                 'Essa avaliação mede correspondência com a rotulagem da pesquisa em outro ano, '
                 'não valida o desfecho inferido da TPU nem autoriza triagem individual.'))
"""


def replace_exact(source: str, old: str, new: str, *, label: str) -> str:
    if old not in source:
        raise RuntimeError(f"Trecho esperado ausente em {label}: {old[:70]}")
    return source.replace(old, new)


def update_code(idx: int, source: str) -> str:
    source = source.replace("proxy por códigos TPU; conferência manual pendente",
                            "proxy por códigos TPU; validade jurídica não aferida")
    if idx == 1:
        source = replace_exact(source,
            "RAIZ = Path.cwd()",
            "RAIZ = Path.cwd()\nif not (RAIZ / 'pyproject.toml').exists():\n    RAIZ = RAIZ.parent",
            label="raiz do notebook")
        source = replace_exact(source,
            "RAIZ = RAIZ.parent",
            "RAIZ = RAIZ.parent\nsys.path.insert(0, str(RAIZ))",
            label="importação dos módulos revisados")
        source = replace_exact(source,
            "BRUTOS, DATAJUD, PROCESSADO = PASTA_DADOS / 'brutos', PASTA_DADOS / 'datajud', PASTA_DADOS / 'processado'",
            "BRUTOS, DATAJUD = PASTA_DADOS / 'brutos', PASTA_DADOS / 'datajud'\nPROCESSADO = RAIZ / 'estcaso3_revisado' / 'processado'",
            label="caminhos")
        source = replace_exact(source,
            "FIGURAS, TABELAS = RAIZ / 'figuras', RAIZ / 'tabelas'",
            "FIGURAS, TABELAS = RAIZ / 'estcaso3_revisado' / 'figuras', RAIZ / 'estcaso3_revisado' / 'tabelas'",
            label="saídas")
        source = replace_exact(source,
            "GAB = json.loads((PROCESSADO / 'exposicao_numeros.json').read_text(encoding='utf-8'))",
            "GAB = json.loads((PASTA_DADOS / 'processado' / 'exposicao_numeros.json').read_text(encoding='utf-8'))",
            label="gabarito")
    if idx == 25:
        source = """# 3.4 Auditoria automática do proxy de desfecho, sem leitura manual de autos
_audit = proc.copy()
_audit['ano'] = pd.to_datetime(_audit.data_ajuizamento).dt.year
_eventos = _audit.e_desfecho.astype(int) == 1
_sem_data = int((_eventos & _audit.desfecho_data.isna()).sum())
_antes = int((_eventos & (_audit.desfecho_data < _audit.data_ajuizamento)).sum())
_sem_doc = int(dj.grau_entrada.isna().sum())
_residuais = int((_audit.desfecho == 'sem sentença registrada').sum())
AUDITORIA_PROXY = pd.DataFrame([
    {'verificação': 'processos com documento', 'casos': len(_audit)},
    {'verificação': 'amostra sem documento JE/G1', 'casos': _sem_doc},
    {'verificação': 'evento sem data', 'casos': _sem_data},
    {'verificação': 'evento anterior ao ajuizamento', 'casos': _antes},
    {'verificação': 'categorias residuais sem sentença', 'casos': _residuais},
    {'verificação': 'decisões de grupos diferentes no mesmo dia', 'casos': int(_audit.conflito_mesmo_dia.sum())},
    {'verificação': 'primeira categoria difere da última', 'casos': int((_audit.primeira_categoria.notna() &
        (_audit.primeira_categoria != _audit.desfecho_categoria)).sum())},
    {'verificação': 'divergência com regra simplificada, grupo amplo', 'casos': len(divergentes)},
])
display(AUDITORIA_PROXY)
display(pd.crosstab(_audit.ano, _audit.desfecho, margins=True))
V.update(conf_n=fint(len(_audit)), conf_estratos=fint(_audit.desfecho.nunique()),
         conf_status='auditoria automatizada; validade jurídica da sentença não observável por esta fonte')
"""
    if idx == 96:
        source = replace_exact(source,
            "NOMES_LISTA = {0: 'não predatória', 1: 'indício de lide predatória', 2: 'certeza de lide predatória'}",
            "NOMES_LISTA = {0: 'trajetória 1', 1: 'trajetória 2', 2: 'trajetória 3'}\nfor k, nome in enumerate(NIVEIS_CLASSE3):\n    UNIV[f'P(trajetória {k + 1})'] = UNIV[f'P({nome})']",
            label="nomes dos grupos")
        source = replace_exact(source,
            "'P(não predatória)', 'P(indício sem certeza)', 'P(certeza)', 'prob_pertenca', 'via_coleta'",
            "'P(trajetória 1)', 'P(trajetória 2)', 'P(trajetória 3)', 'prob_pertenca', 'via_coleta'",
            label="probabilidades")
        source = replace_exact(source,
            "ARQ_LISTAS = TABELAS / 'listas_classificacao.xlsx'",
            "ARQ_LISTAS = TABELAS / 'trajetorias_processuais.xlsx'",
            label="arquivo")
        source = source.replace(
            "Listas geradas pelo classificador não supervisionado (LCA, K = 3) da Seção 10, aplicado à moldura da pesquisa.",
            "Grupos exploratórios de trajetórias processuais da LCA (K = 3). Não são rótulos jurídicos de predação.")
        source = source.replace(
            "As listas NÃO servem para triagem individual: o classificador quase não discrimina (ver Seções 10 e 12).",
            "Uso individual e inferência de litigância predatória são inadequados; ver Seções 10 e 12.")
    if idx == 99:
        source = source.replace(
            "# 12.1 Prevalência aparente, Rogan-Gladen com bootstrap e comparação com os intervalos (indício e certeza)",
            "# 12.1 Diagnóstico exploratório de não identificação: as estimativas corrigidas não são prevalências validadas")
        source = replace_exact(source,
            "pap_b = rng_rg.binomial(len(pred_pop), pap) / len(pred_pop)",
            "pap_b = pap  # moldura observada quase integralmente: fixar proporção aparente neste diagnóstico",
            label="proporção da moldura")
        source = replace_exact(source,
            "dif = (min(max(rg, 0), 1) - ref['p_amostra']) if np.isfinite(rg) else np.nan",
            "dif = np.nan  # não testar igualdade a partir de correção instável e modelo sem validação",
            label="diferença inválida")
        source = replace_exact(source,
            "ep_dif = math.sqrt(np.nanvar(boot) + ref['ep'] ** 2) if ok_b.any() else np.nan",
            "ep_dif = np.nan",
            label="erro da diferença")
        source = replace_exact(source,
            "p_dif=2 * stats.norm.sf(abs(dif / ep_dif)) if np.isfinite(dif) else np.nan,",
            "p_dif=np.nan,",
            label="teste da diferença")
        source = replace_exact(source,
            "tost=bool(np.isfinite(dif) and (dif - 1.645 * ep_dif > -delta) and (dif + 1.645 * ep_dif < delta)),",
            "tost=False,  # não identificado; TOST não aplicável",
            label="TOST inválido")
    if "def biplots(ca, rot_lin" in source:
        source = replace_exact(source,
            "for i, r in enumerate(rot_lin):\n            ax.annotate(r, Fp[i], fontsize=7, color='#0072B2', xytext=(3, 3), textcoords='offset points')",
            "for i, r in enumerate(rot_lin):\n            # Rotular só os pontos que mais definem o plano; todas as coordenadas estão na tabela.\n            if i not in np.argsort(ca['ctr_lin'][:, :2].sum(1))[-5:]:\n                continue\n            ax.annotate(r, Fp[i], fontsize=8, color='#0072B2', xytext=(4, 4), textcoords='offset points')",
            label="legibilidade dos biplots")
    return source


def update_interpretation(source: str) -> str:
    if source.startswith("exibir('dj_proxy'"):
        source = source.replace(
            "A conferência manual (Seção 3.2) mede essa distância.",
            "A auditoria automática da Seção 3.2 detecta erros internos, mas não mede a distância até a sentença nos autos.")
    if source.startswith("exibir('dj_validacao'"):
        source = re.sub(r"exibir\('dj_validacao', r'''[\s\S]*?'''\)",
            """exibir('dj_validacao', r'''
**Leitura da auditoria automática.** O proxy foi calculado para {{conf_n}} processos com documento, distribuídos em {{conf_estratos}} grupos amplos de desfecho. A tabela acima verifica datas, cobertura, decisões concorrentes e divergências entre duas regras de TPU. Situação: {{conf_status}}.

Essas verificações são reproduzíveis sem abrir processos e permitem localizar erros de código ou transmissão. Duas regras que concordam sobre os mesmos movimentos podem, porém, concordar no mesmo erro. Assim, os desfechos permanecem **proxies administrativos**, e nenhuma estimativa de acurácia jurídica é atribuída a eles.
''')""", source, count=1)
    if source.startswith("exibir('ns_confusao_datajud'"):
        source = source.replace("padrão-ouro externo", "referência da pesquisa")
        source = source.replace("o classificador do DataJud praticamente não concorda", "os perfis do DataJud praticamente não concordam")
        source = source.replace("O classificador cumpre o que o roteiro pede", "A análise cobre o exercício do roteiro")
        source = source.replace(
            "mas a resposta honesta é que **esses dados não carregam a informação** necessária para separar as classes.",
            "e **esses dados não carregam a informação** necessária para separar as classes. A matriz é calculada nos mesmos processos usados para ajustar os grupos; não é validação independente.")
    if source.startswith("exibir('ns_recuperacao'"):
        source = source.replace(
            "A baixa concordância da Seção 10.3 não vem, portanto, de um defeito do algoritmo nem de amostra pequena demais para o modelo. Ela vem de as classes latentes do DataJud **não serem** as classes jurídicas.",
            "A recuperação mostra apenas que o algoritmo reencontra grupos gerados pelas hipóteses que ele próprio assume. Ela não prova que o tamanho da amostra seja suficiente em outros cenários. A baixa concordância observada indica que as trajetórias do DataJud **não correspondem**, nesta amostra, às classes jurídicas.")
    if source.startswith("exibir('pop_listas'"):
        source = re.sub(r"exibir\('pop_listas', r'''[\s\S]*?'''\)",
            """exibir('pop_listas', r'''
**A aplicação produz três perfis de trajetória processual.** Entre os {{pop_doc}} processos com documento, os tamanhos são {{lista_0}}, {{lista_1}} e {{lista_2}}. As porcentagens correspondentes são {{lista_0_p}}, {{lista_1_p}} e {{lista_2_p}}. A probabilidade média de pertença ao perfil atribuído é {{prob_media}}.

A planilha `estcaso3_revisado/tabelas/trajetorias_processuais.xlsx` conserva o número CNJ, as variáveis processuais e as probabilidades dos três perfis. Há uma aba adicional para números sem documento. Os nomes neutros são deliberados: a matriz da Seção 10 não sustenta chamar os grupos de “não predatória”, “indício” e “certeza”. A planilha serve para examinar padrões administrativos; **não serve para triagem ou decisão sobre processos individuais**.
''')""", source, count=1)
    if source.startswith("exibir('r19_resposta'"):
        source = re.sub(r"exibir\('r19_resposta', r'''[\s\S]*?'''\)",
            """exibir('r19_resposta', r'''
**O exercício populacional não identifica a prevalência jurídica.** A proporção aparente de perfis que receberiam o antigo nome de indício é {{r19_pap}}, mas a concordância com a classificação da pesquisa é fraca (J de Youden = {{r19_J}}). A inversão de Rogan–Gladen produz {{r19_rg}}, com intervalo exploratório {{r19_ic}}; a amplitude mostra que esse número não tem precisão útil. Para a certeza, J = {{r19c_J}} e a correção é indefinida.

O bootstrap aqui mantém o modelo ajustado e suas atribuições fixos. Ele não incorpora toda a incerteza de ajuste e escolha dos grupos; por isso o intervalo não deve ser usado para afirmar igualdade ou equivalência com a pesquisa. A estimativa sustentada pela amostra probabilística permanece {{p_indicio}}. A aproximação de Wilson por tamanho efetivo é {{ic_des}}; o apêndice também apresenta um intervalo logito baseado no erro-padrão estratificado. O intervalo publicado {{ic_pub}} foi calculado por Wald com correção de população finita, apesar do nome usado no roteiro. Os dados novos do DataJud descrevem trajetórias, mas não refinam de modo confiável a prevalência de litigância predatória.
''')""", source, count=1)
    if source.startswith("exibir('sintese'"):
        source = source.replace(
            "listas em `tabelas/listas_classificacao.xlsx`: {{lista_0}} / {{lista_1}} / {{lista_2}} processos, sem dados pessoais e **sem valor de triagem**",
            "perfis de trajetória em `estcaso3_revisado/tabelas/trajetorias_processuais.xlsx`: {{lista_0}} / {{lista_1}} / {{lista_2}} processos; sem valor de triagem jurídica")
        source = source.replace(
            "o classificador não permite responder: prevalência aparente {{r19_pap}}; Rogan-Gladen {{r19_rg}}, com IC {{r19_ic}}.",
            "os perfis não permitem responder: proporção aparente {{r19_pap}} e correção instável {{r19_rg}} (intervalo exploratório {{r19_ic}}).")
    return source


def main() -> None:
    from amostra_juizados import BLOCKS_DESENHO, BLOCKS_DATAJUD
    nb = nbformat.read(SOURCE, as_version=4)
    cells = []
    intro = """# Estudo de Caso 3 — edição didática auditada

Este caderno percorre a amostra de 595 processos e os registros do DataJud para responder ao roteiro da disciplina. Ele preserva as contas do estudo original e torna explícitas as decisões de curadoria, os denominadores e os limites de cada resultado. A sequência acompanha a lógica do Estudo de Caso 1: entender as fontes, limpar e auditar, descrever, modelar e só então considerar aplicação.

**Distinção que orienta a leitura:** a pesquisa atribuiu rótulos jurídicos mediante leitura de petições e verificação de massificação. O DataJud registra sobretudo a trajetória processual. Os grupos que uma análise não supervisionada encontra nesses registros são descritos como *perfis de trajetória*. A matriz de confusão permite confrontá-los com os rótulos da pesquisa, mas não autoriza rebatizá-los como certeza ou indício de predação.

As saídas desta edição são gravadas em `estcaso3_revisado/`; os dados e o gabarito numérico são lidos do projeto original. Os desfechos inferidos por TPU passam por auditoria automática e seguem identificados como proxies. Os dados simulados no final servem ao ensino e à avaliação do método; não são novos casos observados.

**Versão final para entrega.** As Partes I a IV respondem ao roteiro. A Parte V testa a sensibilidade dos métodos e a previsão no ajuizamento; ali aparece o achado que reorganiza a leitura: o **assunto** do processo (código 6226) concentra o indício. A Parte VI usa modelos bayesianos para estimar a prevalência com o assunto de toda a moldura, propagar a incerteza das verossimilhanças e da codificação e estabilizar os coeficientes. **A resposta final, item a item, está na Seção 35.**
"""
    cells.append(nbformat.v4.new_markdown_cell(intro))
    for idx, cell in enumerate(nb.cells):
        source = cell.source
        if cell.cell_type == "markdown":
            if idx == 24:
                source = """### 3.2 Auditoria automatizada dos desfechos

Sem abrir autos, é possível verificar se as datas dos eventos são possíveis, quantos processos ficaram sem documento, quais categorias ficaram sem sentença registrada e onde duas regras de TPU divergem. A auditoria abaixo executa essas verificações em todos os processos disponíveis. Ela é uma **sensibilidade entre codificações administrativas**: não calcula sensibilidade ou especificidade em relação à sentença jurídica, que a API pública não contém.
"""
            if idx == 98:
                source = """## 12. O resultado cai no intervalo de 17,65%? (R19)

O intervalo [14,59%; 20,70%] citado no roteiro reproduz Wald com correção de população finita para N = 83.139, apesar do nome Wilson empregado ali. O Wilson simples e a aproximação por tamanho efetivo do desenho são mostrados para comparação. O apêndice final acrescenta um intervalo na escala logito com o erro-padrão estratificado.

A proporção dos perfis de trajetória na moldura não mede a prevalência de indício da pesquisa. A fórmula de Rogan–Gladen é apresentada apenas como diagnóstico: divide pela soma sensibilidade + especificidade − 1, que aqui fica próxima de zero ou negativa. Como os grupos não validaram a classificação jurídica, **não se calcula teste de igualdade nem de equivalência** entre essa correção e a estimativa amostral. A resposta sustentada pelo desenho vem da amostra sorteada.
"""
            source = source.replace(
                "**Notebook:** `estcaso3_rafael.ipynb`, gerado por `src/estcaso3/build_estcaso3_rafael.py`",
                "**Edição:** `estcaso3_revisado/estcaso3_revisado.ipynb`, gerada por `estcaso3_revisado/build.py`")
            source = source.replace("### 2.4 Quadro de Variáveis e Dicionário de Dados",
                                    "### 2.6 Quadro de Variáveis e Dicionário de Dados")
            source = source.replace(
                "A rotulagem da Hadja é o padrão-ouro **externo**: entra só na matriz de confusão, nunca no treino.",
                "A rotulagem da Hadja é uma referência substantiva: entra na matriz, mas os mesmos processos participaram do ajuste da mistura; a avaliação é exploratória.")
            source = source.replace(
                "As classes saem sem ordem (*label switching*). Elas são ordenadas por um escore definido a priori:",
                "As classes saem sem ordem (*label switching*). Elas são ordenadas por um escore analítico:")
            source = source.replace(
                "as três listas", "os três perfis")
            source = source.replace("Wilson com o desenho", "Wilson aproximado por n efetivo")
            source = source.replace("**antes** dos resultados", "como escolhas analíticas declaradas no notebook")
            source = source.replace("**antes** de rodar os modelos", "no plano analítico desta edição")
            source = source.replace(
                "| D10 | validação manual dos desfechos | planilha de conferência gerada aqui; o parecer é humano (no PJe) |",
                "| D10 | auditoria dos desfechos | comparação automática de regras TPU e consistência temporal; validade jurídica externa não observável |")
            source = source.replace(
                "1. **Conferir os desfechos no PJe** com a planilha da Seção 3.2 e reexecutar o notebook.",
                "1. **Manter o desfecho como proxy TPU** e conferir automaticamente cronologia, categorias residuais e diferenças entre regras em cada nova coleta.")
            source = source.replace(
                "4. **Segunda codificação** de uma subamostra dos autos, para medir o kappa entre codificadores das F2/F3.",
                "4. **Relatar o limite dos rótulos existentes**: foram atribuídos por uma codificadora; não há medida independente de concordância entre codificadores.")
            cell.source = RF.markdown(idx, source)
        elif cell.cell_type == "code":
            if idx in GUIDES:
                cells.append(nbformat.v4.new_markdown_cell(GUIDES[idx]))
            cell.source = RF.interpretacao(update_interpretation(RF.code(idx, update_code(idx, source))))
            cell.outputs = []
            cell.execution_count = None
        cells.append(cell)
        if idx in (14, 95):
            blocos = BLOCKS_DESENHO if idx == 14 else BLOCKS_DATAJUD
            for kind, trecho in blocos:
                cells.append(nbformat.v4.new_markdown_cell(trecho.strip()) if kind == "markdown"
                             else nbformat.v4.new_code_cell(trecho.strip()))
        if idx == 86:
            cells.append(nbformat.v4.new_markdown_cell(HOLDOUT_NOTE))
            cells.append(nbformat.v4.new_code_cell(HOLDOUT_CODE))
    from apendice import BLOCKS
    for kind, source in BLOCKS:
        cells.append(nbformat.v4.new_markdown_cell(source.strip()) if kind == "markdown"
                     else nbformat.v4.new_code_cell(source.strip()))
    from apendice2 import BLOCKS as BLOCKS2
    for kind, source in BLOCKS2:
        cells.append(nbformat.v4.new_markdown_cell(source.strip()) if kind == "markdown"
                     else nbformat.v4.new_code_cell(source.strip()))
    from apendice3 import BLOCKS as BLOCKS3
    for kind, source in BLOCKS3:
        cells.append(nbformat.v4.new_markdown_cell(source.strip()) if kind == "markdown"
                     else nbformat.v4.new_code_cell(source.strip()))
    from apendice4 import BLOCKS as BLOCKS4
    for kind, source in BLOCKS4:
        cells.append(nbformat.v4.new_markdown_cell(source.strip()) if kind == "markdown"
                     else nbformat.v4.new_code_cell(source.strip()))
    from apendice5 import BLOCKS as BLOCKS5
    for kind, source in BLOCKS5:
        cells.append(nbformat.v4.new_markdown_cell(source.strip()) if kind == "markdown"
                     else nbformat.v4.new_code_cell(source.strip()))
    from apendice6 import BLOCKS as BLOCKS6
    for kind, source in BLOCKS6:
        cells.append(nbformat.v4.new_markdown_cell(source.strip()) if kind == "markdown"
                     else nbformat.v4.new_code_cell(source.strip()))
    from apendice7 import BLOCKS as BLOCKS7
    for kind, source in BLOCKS7:
        cells.append(nbformat.v4.new_markdown_cell(source.strip()) if kind == "markdown"
                     else nbformat.v4.new_code_cell(source.strip()))
    from apendice8 import BLOCKS as BLOCKS8
    for kind, source in BLOCKS8:
        cells.append(nbformat.v4.new_markdown_cell(source.strip()) if kind == "markdown"
                     else nbformat.v4.new_code_cell(source.strip()))
    if not RF.REFERENCIAS:
        raise RuntimeError("referências não extraídas da Seção 14")
    cells.append(nbformat.v4.new_markdown_cell(
        "---\n\n## 36. Referências\n\nReferências de todo o estudo, inclusive das Partes V e VI.\n\n" + RF.REFERENCIAS))
    nb.cells = cells
    nb.metadata["auditoria"] = {"origem": str(SOURCE.relative_to(ROOT)),
                                "edicao": "didatica", "grupos": "trajetorias processuais"}
    nbformat.validate(nb)
    nbformat.write(nb, TARGET)
    print(f"{TARGET}: {len(nb.cells)} células, {len(GUIDES)} explicações analíticas")


if __name__ == "__main__":
    main()
