# Plano de execução — `CDEaDPP_2026_Trabalho_Final_Python_v2.ipynb`

**Disciplina:** CDEaDPP — 2026.2  
**Produto:** template educacional, executável e replicável de protocolo de pesquisa empírica  
**Executor das próximas etapas:** Sol 6.1  
**Estado desta etapa:** planejamento. A implementação será feita em módulos sucessivos.

---

## 0. Fontes e decisões metodológicas

| Fonte local | Uso no novo notebook |
|---|---|
| `CDEaDPP_2026_Trabalho_Final_Python.ipynb` | Preservar a progressão didática entre dicionário, simulação, análise exploratória, inferência e amostragem. Substituir exemplos desconexos, conclusões em branco e dimensionamento inconsistente. Não alterar o original. |
| `md/SIPAPP-Turma8-Reflexões-Houston2-12abr-19jul-2024-v1.md` | Delimitação T.E.M.P., população e unidades, sistema de referência, operacionalização, piloto, variáveis ocultas, replicabilidade, erros amostrais e não amostrais. |
| `md/SIPAPP-Turma8-Houston-8mar2024-v3.md` | Escalas de mensuração, distinção entre estudo observacional e experimento, inferência, validade, erros tipos I e II e caminhos causais. |
| `PLANO_estcaso_lide_pred.md` | Arquitetura: um builder e seções `.py` que emitem células Markdown e código para um `.ipynb` autocontido. Não transportar dados nem resultados do estudo Hadja. |

**Caso didático proposto:** avaliação retrospectiva de um programa **hipotético** de orientação jurídica para pedidos de benefício social em unidades administrativas. Cada linha representa um pedido concluído ou acompanhado em um período definido pelo aluno. A exposição é o atendimento pelo programa, sem sorteio; a adesão depende de características do caso e da unidade. Não mencionar órgão, município, lei ou programa real como se os dados os descrevessem.

**Pergunta-modelo:** entre os pedidos elegíveis, qual é a associação entre o atendimento pelo programa e (a) a pontuação de acesso efetivo ao benefício e (b) o desfecho administrativo, após ajuste por características medidas? O texto explicará que associação ajustada em dados observacionais retrospectivos não identifica automaticamente efeito causal.

**Hipótese quantitativa primária, bilateral:** H₀: β do atendimento = 0, condicional às covariáveis pré-especificadas; H₁: β ≠ 0. **Hipótese categórica secundária:** H₀: as distribuições dos cinco desfechos são iguais entre atendidos e não atendidos; H₁: ao menos uma proporção difere. Testes adicionais serão marcados como exploratórios.

### 0.1 Quadro de variáveis mínimo, a desenvolver na seção 2

| Nome | Significado e exemplos | Tipo e escala | Papel |
|---|---|---|---|
| `id_pedido` | Identificador artificial; `PED-0001` | Texto, identificador sem escala inferencial | Chave |
| `atendimento_programa` | Recebeu orientação: `Sim`, `Não` | Categórica binária, nominal | Independente principal |
| `pontuacao_acesso` | Escore construído, por exemplo 45,3 e 62,1 pontos | Quantitativa, **intervalar assumida**; zero convencional, diferenças interpretáveis | Dependente primária |
| `desfecho_administrativo` | `deferido_integral`, `deferido_parcial`, `indeferido`, `pendente`, `arquivado` | Categórica multinomial **nominal**, cinco níveis exaustivos e exclusivos | Dependente secundária |
| `complexidade_previa` | Índice do caso na entrada; 1, 2, 3 | Ordinal | Confundidora observada |
| `vulnerabilidade_previa` | Índice socioeconômico na entrada; 0, 1 | Binária, nominal | Confundidora observada |
| `unidade` | Unidade administrativa; `U1`, `U2`, `U3` | Categórica nominal | Estrato/contexto |
| `ano_pedido` | Ano da entrada; 2023, 2024, 2025 | Temporal discreta | Contexto e seleção |
| `documentacao_inicial` | Documentos completos na entrada; `Sim`, `Não` | Binária, nominal | Covariável pré-exposição, se mensurada antes |
| `acesso_digital_nao_observado` | Facilidade de uso do portal, gerada apenas para ilustrar viés | Latente; **excluída do dataset analítico** | Confundidora não observada |

O escore é **didaticamente tratado como intervalar**, não validado por mera simulação. O módulo exige que o aluno descreva itens, pesos, consistência e evidências de validade antes de usar uma escala própria em dados reais. Não chamar tempo em dias de escala intervalar: dias transcorridos têm zero substantivo e escala de razão. O desfecho de cinco níveis é nominal; não calcular médias de seus códigos nem impor ordem fictícia.

### 0.2 Desenho gerador e limites

1. Fixar semente com `np.random.default_rng(2026)` e gerar população fictícia ou amostra principal suficientemente grande para tabelas 2×5 com frequências esperadas adequadas; escolher tamanho e parâmetros em seção própria, sem ajustar parâmetros até obter um p-valor desejado.
2. Gerar covariáveis basais, incluindo uma causa comum latente. Gerar `atendimento_programa` por probabilidade logística dependente das covariáveis; verificar sobreposição de propensões. A latente influenciará exposição e resultados, mas não aparecerá no arquivo analítico.
3. Injetar efeito principal **no mecanismo de simulação**: deslocamento positivo predefinido na média de `pontuacao_acesso` e alteração predefinida nas probabilidades das cinco categorias. Adicionar ruído e diferenças entre unidades. Exibir os parâmetros geradores em Markdown/código, distinguindo-os das estimativas recuperadas.
4. Criar piloto **independente** de 30 observações com a mesma regra geradora. Seu desvio padrão amostral (`ddof=1`) será usado no planejamento quantitativo; não reutilizar a amostra principal para escolher o efeito mínimo relevante ou a potência. Para o desfecho multinomial, usar proporções de referência e alternativas **pré-especificadas**, informadas qualitativamente pelo piloto e por relevância substantiva, sem confundir flutuação do piloto com parâmetro verdadeiro.
5. Declarar alvo, período, elegibilidade, unidade de análise, quadro de referência, mecanismo de seleção e destino de NA. Qualquer generalização além da população simulada será apresentada como exercício condicional, não como evidência sobre instituição real.

---

## 1. Arquitetura de arquivos

```text
./
├── PLANO_CDEaDPP_2026_Trabalho_Final_Python_v2.md
├── CDEaDPP_2026_Trabalho_Final_Python.ipynb      # base, intacto
├── CDEaDPP_2026_Trabalho_Final_Python_v2.ipynb   # gerado pelo builder
├── src/
│   └── cdedpp_2026_v2/
│       ├── __init__.py
│       ├── build_notebook.py
│       ├── secao01_protocolo.py
│       ├── secao02_dicionario.py
│       ├── secao03_simulacao.py
│       ├── secao04_curadoria.py
│       ├── secao05_exploratoria.py
│       ├── secao06_modelagem.py
│       ├── secao07_hipoteses.py
│       ├── secao08_amostragem.py
│       └── secao09_sintese.py
└── out/
    └── cdedpp_2026_v2/                         # criado só durante execução
        ├── pedidos_simulados.csv
        └── piloto_simulado.csv
```

O builder poderá adaptar `md()` e `code()` do projeto existente, mas terá namespace próprio e lista explícita de módulos. Cada módulo terá blocos Markdown **antes e depois** do código: fundamento, decisões, interpretação contextual e perguntas para o aluno. A seção 9 conterá a conclusão final com limitações; as outras terão análises e ressalvas locais. Toda célula de código deverá trazer comentários passo a passo em português. O `.ipynb` gerado deve conter todo o Python necessário, sem importação de `src` em tempo de execução. Usar UTF-8, metadados de kernel portáveis, `nbformat` v4, células de código sem outputs persistidos e caminhos relativos à raiz detectada a partir do diretório de trabalho ou por busca controlada. Preservar as diretivas Quarto apenas quando úteis; a execução no Jupyter/VS Code é o critério principal.

**Dependências já declaradas em `pyproject.toml`:** `numpy`, `pandas`, `matplotlib`, `seaborn`, `scipy`, `statsmodels`, `nbformat`, `ipykernel`. Conferir versões no ambiente na etapa de execução; não adicionar pacotes sem necessidade.

---

## 2. Pipeline, células e critérios por módulo

### Seção 1 — Protocolo e ambiente (`secao01_protocolo.py`)

- Markdown: título, uso como template, delimitação T.E.M.P., problema, população-alvo versus acessível, unidades, período, critérios de inclusão/exclusão, hipóteses, desenho retrospectivo observacional, diagrama causal textual ou Mermaid e campo orientado para o aluno preencher.
- Código: importações completas, versões, semente, nível `alpha=0.05`, poder-alvo `0.85` (`beta=0.15`), apresentação dos parâmetros, configurações de gráficos e diretório de saída.
- Markdown interpretativo: distinção entre randomizar a **simulação** e randomizar o **tratamento**; fontes de viés de seleção, aferição e confundimento.
- Asserts: `0 < alpha < 1`, `0 < beta < 1`, `np.isclose(poder_alvo, 1 - beta)`, semente inteira, diretório de saída contido na raiz do projeto.

### Seção 2 — Dicionário e operacionalização (`secao02_dicionario.py`)

- Markdown: **tabela no próprio Markdown**, com nome, significado, tipo, escala, papel e exemplos na última coluna para **todas** as variáveis analíticas; critérios de construção, momento de aferição e possíveis erros de mensuração. Incluir campo para os alunos substituírem cada definição.
- Código: construir `dicionario` também como `DataFrame` para checagem de esquema e exibição; definir lista de categorias e covariáveis basais sem ordenar a variável multinomial.
- Markdown interpretativo: validade de constructo, confiabilidade do escore, separação entre variável prévia e mediadora; ressalva sobre escore intervalar assumido.
- Asserts: nomes únicos; exatamente cinco categorias distintas; variável dependente quantitativa e exposição presentes; toda variável analítica descrita; papel e escala preenchidos.

### Seção 3 — Simulação e piloto (`secao03_simulacao.py`)

- Markdown: mecanismo gerador, parâmetros pré-especificados, quadro de caminhos `U → X`, `U → Y`, `X → Y`, e justificativa da inclusão de unidades e heterogeneidade. Explicar que um resultado estatisticamente significativo não é garantia em cada realização aleatória.
- Código: funções explícitas para gerar covariáveis, exposição, escore e categorias multinomiais por probabilidades válidas (por exemplo, softmax estável). Gerar piloto n=30 com fluxo aleatório independente e amostra principal. Exportar CSVs UTF-8 com `utf-8-sig` se abertos no Excel, mantendo leitura UTF-8 explícita. Não exportar a latente com os dados analíticos.
- Markdown interpretativo: comparar efeitos geradores e padrões da amostra; explicitar risco de confundimento residual.
- Asserts: piloto com 30 linhas; IDs únicos e sem sobreposição entre bases; probabilidades por linha finitas, entre 0 e 1, somando 1; desfecho apenas nas cinco categorias; escore finito; presença dos dois grupos; semente reproduz o mesmo dataset; efeito gerador registrado diferente de zero; nenhuma coluna latente no arquivo analítico.

### Seção 4 — Curadoria e auditoria (`secao04_curadoria.py`)

- Markdown: fluxograma de elegibilidade e critérios explícitos de completude, duplicidade e coerência; distinguir ausência real de categoria `pendente`.
- Código: recarregar os CSVs, conferir tipos e encoding, tabelas de NA, duplicatas, frequências por unidade e período; produzir dataset curado sem apagar casos silenciosamente.
- Markdown interpretativo: quais perdas ou erros poderiam alterar validade interna/externa; procedimento que o aluno deverá adaptar para dados reais.
- Asserts: número de linhas preservado quando não houver exclusões; IDs não duplicados; nenhuma categoria fora do domínio; códigos de exposição válidos; NA contabilizados; soma dos estratos igual ao total; piloto e amostra principal distintos.

### Seção 5 — Análise exploratória (`secao05_exploratoria.py`)

- Markdown: estimadores, denominadores e finalidade de cada tabela/gráfico. Evitar chamar diferença bruta de efeito causal.
- Código: tabela de frequência absoluta/relativa dos cinco desfechos; resumo de média, mediana, DP, quartis e N do escore por exposição e unidade; histogramas/densidades e boxplots; barras agrupadas com proporções por grupo; gráfico de sobreposição da exposição por covariável; gráficos com títulos, rótulos, N e fonte “dados simulados”.
- Markdown interpretativo: perguntas sobre assimetria, dispersão, desequilíbrio basal, suporte comum, categorias raras, composição da amostra e validade externa.
- Asserts: frequências somam N; percentuais somam aproximadamente 100% dentro de cada grupo; nenhuma categoria desapareceu do domínio exibido; estatísticas descritivas finitas; cada gráfico usa o dataframe curado.

### Seção 6 — Modelagem (`secao06_modelagem.py`)

- Markdown: estimando, forma do modelo, escolha de covariáveis **pré-exposição**, condições do OLS, interpretação de coeficientes e IC 95%; separar modelo bruto e ajustado.
- Código: `statsmodels` OLS do escore contra atendimento, primeiro bruto, depois ajustado por complexidade, vulnerabilidade, documentação, unidade e ano; usar erros padrão robustos HC3 e apresentar coeficiente, IC, p, N e R². Gerar diagnóstico de resíduos versus ajustados e QQ plot; não substituir avaliação gráfica por um teste de normalidade isolado. Para o multinomial, produzir tabela 2×5, qui-quadrado como análise secundária e proporções por grupo; modelo multinomial apenas se convergir de modo estável e com interpretação definida.
- Markdown interpretativo: tamanho e precisão da associação, comparação bruto/ajustado, sinais de violação e confundimento residual; associação de cinco categorias não implica ordenação.
- Asserts: modelos convergentes ou falha explicitamente diagnosticada; coeficiente de atendimento e IC finitos; `0 <= R² <= 1` para OLS com intercepto; N do modelo declarado; tabela 2×5 completa; frequências esperadas inspecionadas antes de interpretar χ².

### Seção 7 — NHST e erros de decisão (`secao07_hipoteses.py`)

- Markdown: H₀/H₁, teste bilateral primário, regra pré-fixada, diferença entre p-valor e probabilidade de H₀, IC, relevância substantiva e multiplicidade das análises secundárias.
- Código: extrair do OLS ajustado estatística, p, IC e decisão (`rejeitar`/`não rejeitar`); calcular χ² secundário 2×5 somente quando pressupostos forem adequados, caso contrário relatar limite e uma alternativa explicitamente justificada; tabela contextual de erro tipo I (concluir associação quando H₀ é verdadeira) e tipo II (não detectar associação mínima real).
- Markdown interpretativo: texto de conclusão condicionado ao resultado, sem declarar que H₀ foi “aceita”, sem generalização causal e sem fixar p esperado pela simulação.
- Asserts: p finito em `[0,1]`; decisão coerente com `alpha`; IC contém a estimativa; graus de liberdade e somas da tabela 2×5 coerentes; nenhum teste exploratório apresentado como confirmação da hipótese primária.

### Seção 8 — Tamanho amostral e piloto (`secao08_amostragem.py`)

- Markdown: seção reservada, porém **executável**, para erro tipo I, erro tipo II, poder, efeito mínimo relevante e perdas. Distinguir piloto de n=30, escolha substantiva do efeito e amostra principal. Explicar que poder não corrige viés nem representa probabilidade posterior da hipótese.
- Código quantitativo: obter `s_piloto` com `ddof=1`; definir diferença mínima `delta` antes dos testes principais; calcular `d=delta/s_piloto`; usar `TTestIndPower.solve_power` para dois grupos independentes, alocação 1:1, teste bilateral, α e poder-alvo; arredondar **cada grupo** para cima e somar. Incluir análise de sensibilidade para DP e diferença mínima, com parâmetros didáticos explícitos.
- Código multinomial **do protocolo principal**: declarar dois vetores de cinco probabilidades, um por grupo, sob alternativa relevante; declarar alocação 1:1 e simular repetidamente tabelas 2×5 em uma grade de N crescente. Em cada réplica, aplicar o mesmo teste de associação que será usado na seção 6; estimar poder pela fração de rejeições, com fluxo aleatório separado, número de réplicas e erro Monte Carlo informados. Escolher o menor N com poder estimado e margem de segurança definidos antes da busca. Verificar contagens esperadas; para categorias esparsas, usar uma alternativa de teste e de simulação de poder coerente ou rever o desenho antes de recomendar N.
- Código multinomial **complementar, claramente rotulado**: definir H₀ como vetor de cinco probabilidades de referência e H₁ como vetor alternativo substantivo; calcular `w = sqrt(sum((p1-p0)^2/p0))`; usar `GofChisquarePower` com cinco categorias e quatro graus de liberdade para demonstrar o dimensionamento de **aderência de uma amostra**. Esse N não será usado para a hipótese de associação 2×5.
- Markdown interpretativo: tabela comparando `N_quant` e `N_multinomial_2x5`, recomendar o maior para cobrir as duas hipóteses declaradas, acrescentar perdas por `ceil(N/(1-taxa_perda))`, e discutir incerteza de `s_piloto`, do poder Monte Carlo e das contagens esperadas por categoria. Exibir o N de aderência apenas como exercício distinto.
- Asserts: `len(piloto)==30`; `s_piloto>0`; `delta>0`; α, β e taxa de perdas individualmente em `(0,1)`; probabilidades de todos os vetores positivas e somando 1; `w>0`; amostras calculadas inteiras e positivas; `N_final >= max(N_quant,N_multinomial_2x5)`; contagens esperadas verificadas para o N proposto; estimativa de poder da simulação reprodutível; rótulo de aderência não confundido com associação 2×5.

### Seção 9 — Síntese e protocolo replicável (`secao09_sintese.py`)

- Markdown: conclusão acadêmica estruturada com problema, amostra, estimativas/IC, decisão NHST, efeito substantivo, crítica de validade interna e externa, erro de mensuração, seleção, confundidor latente, limites da simulação e recomendações para coleta real. Campos explícitos para os alunos substituírem pressupostos e resultados pelos próprios dados. Nenhuma frase concluirá que a política real funcionou.
- Código: gerar quadro-resumo reproduzível de parâmetros, N, semente, versões, hipótese primária, estimativa, IC, p e tamanho amostral; checagem final das tabelas essenciais.
- Markdown: checklist de replicação e orientações para citar fontes de dados reais, dicionário, protocolo, critérios de exclusão e scripts.
- Asserts: resumo contém todos os campos; N, IC e p repetem objetos calculados; notebook não depende dos dados dos outros estudos do repositório.

---

## 3. Regras transversais de implementação

1. **Células alternadas:** cada trecho analítico terá Markdown de objetivo/método, código executável e Markdown de interpretação/limitações. Evitar sequência longa de código sem contexto. Não deixar placeholders genéricos como “interpretar aqui” sem perguntas concretas e critérios estatísticos.
2. **Comentários:** comentar cada transformação, cálculo e decisão do Python em português claro. Não abreviar código para caber numa única célula.
3. **Resultados:** não inserir números de saída simulada antes da execução. Texto estático explica como interpretar; resultados específicos são exibidos pelo código ou preenchidos pelo aluno após executar. Não impor `assert p < 0.05`: a amostra pode variar mesmo com efeito real gerador.
4. **Validade:** registrar distinção entre validade de constructo, interna, estatística e externa; nomear variáveis ocultas e direção plausível de viés quando justificável. Exposição observacional não vira experimento porque o dataset foi simulado.
5. **Estatística:** pré-especificar hipótese principal e efeito mínimo; usar IC junto ao p; verificar pressupostos antes do χ²; não misturar `GofChisquarePower` com teste 2×5; explicitar correção por perdas e limitações de piloto pequeno.
6. **Reprodutibilidade:** semente fixa, nomes de variáveis estáveis, caminhos relativos, versões exibidas, execução sequencial sem estado oculto, exportação em UTF-8 e ausência de dependências externas de dados.
7. **Builder:** falhar se faltar módulo ou se uma célula de código não compilar; validar `nbformat`; conferir fontes e alternância lógica; só gerar a saída final depois de todas as seções estarem prontas. Não modificar o notebook base.

## 4. Sequência iterativa para o Sol 6.1

| Iteração | Entrega | Gate de validação antes de avançar |
|---|---|---|
| 1 — presente | Este plano, decisões e arquitetura | Fontes inspecionadas; escopo e critérios fixados |
| 2 | `__init__.py`, builder mínimo, seções 1 e 2 | Markdown do quadro completo; imports e asserts iniciais; UTF-8 |
| 3 | Seção 3 | Piloto de 30, dados simulados válidos e determinísticos; efeitos geradores registrados |
| 4 | Seções 4 e 5 | Curadoria sem perdas ocultas; tabelas fecham; gráficos renderizam |
| 5 | Seções 6 e 7 | OLS ajustado e diagnósticos executam; NHST e χ² interpretados com pressupostos |
| 6 | Seção 8 | Dois dimensionamentos corretos, sensibilidade e asserts de probabilidade/N |
| 7 | Seção 9 e builder final | Notebook completo gerado, validado e executado do início ao fim |

Em cada iteração, executar somente as verificações necessárias para o módulo novo e corrigir seus erros antes de seguir. Na iteração final, executar o `.ipynb` em kernel limpo, conferir que todas as células foram percorridas, que nenhuma exceção ocorreu, que gráficos/tabelas apareceram, que os asserts passaram e que o original permaneceu inalterado.

## 5. Critério de conclusão

- [ ] `CDEaDPP_2026_Trabalho_Final_Python_v2.ipynb` existe na raiz, com metadados válidos e execução integral.
- [ ] Todas as seções obrigatórias aparecem, incluindo tabela Markdown do dicionário e cálculo para escore intervalar e desfecho multinomial de cinco níveis.
- [ ] Piloto n=30 é distinto da amostra principal; α, β, DP e efeito mínimo relevante são explícitos.
- [ ] Simulação contém efeitos pré-definidos e confundimento; saída analítica não revela a latente.
- [ ] Gráficos, tabelas, modelos, testes, IC e interpretações estão coerentes com os dados efetivamente gerados.
- [ ] Todos os asserts listados por seção passam; o notebook base permanece intacto.
- [ ] Markdown acadêmico em português diferencia associação, causalidade, validade interna e externa e explicita as limitações do estudo observacional retrospectivo.
