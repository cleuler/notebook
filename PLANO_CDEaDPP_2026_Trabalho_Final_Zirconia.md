# Plano de execução - `CDEaDPP_2026_Trabalho_Final_Zirconia.ipynb`

**Disciplina:** CDEaDPP - 2026.2  
**Produto:** template educacional replicável para protocolo de pesquisa empírica com dados simulados  
**Caso didático:** Zircônia, acesso à saúde e acesso à justiça  
**Estratégia:** construção iterativa em módulos Python autocontidos que emitem células Markdown e células de código para um notebook Jupyter.

---

## 0. Fontes e decisões metodológicas

| Fonte local | Uso no notebook de Zircônia |
|---|---|
| `CDEaDPP_2026_Trabalho_Final_Zirconia.ipynb` | Arquivo de saída gerado pelo builder, sem edição manual direta. |
| `md/trabalho_final_simulacao.md` | Contexto substantivo da Zircônia: desigualdade, ZUS, Defensoria Pública, judicialização da saúde, problemas de pesquisa e exigência de simulação realística. |
| `md/SIPAPP-Turma8-Houston-8mar2024-v3.md` | Conceitos de variável, escala de mensuração, erro tipo I, erro tipo II, validade, desenho observacional, experimento, inferência, resíduos e hipóteses. |
| `md/SIPAPP-Turma8-Reflexões-Houston2-12abr-19jul-2024-v1.md` | Checklist de desenho empírico: problema T.E.M.P., população, sistema de referência, quadro de variáveis, instrumento de medida, piloto, variáveis ocultas e replicabilidade. |
| `PLANO_CDEaDPP_2026_Trabalho_Final_Python_v2.md` | Arquitetura modular, asserts por seção, cuidados com ratio, VIF, clusters e fallback para categorias esparsas. |
| `PLANO_estcaso_lide_pred.md` | Modelo arquitetônico: builder central, módulos por seção e inventário de outputs analíticos. |

O notebook será um **template**. Os dados são simulados e não descrevem instituição real. O estudo didático é observacional retrospectivo: cada linha representa um pedido de internação/tratamento no ZUS acompanhado por via administrativa e, em parte, pela Defensoria Pública da Zircônia.

---

## 1. Pergunta, desenho e hipóteses

**Pergunta-modelo:** entre pessoas de baixa renda com pedido de acesso à saúde no ZUS, qual é a associação entre acesso à assistência jurídica institucional e o acesso efetivo à saúde, medido por um escore intervalar assumido e por um desfecho administrativo/judicial multinomial, após ajuste por características prévias do caso, do requerente e da unidade territorial?

**Hipótese primária quantitativa:**  
$H_0: \beta_{\text{assistencia juridica}} = 0$ contra $H_1: \beta_{\text{assistencia juridica}} \ne 0$ no modelo OLS ajustado para `indice_acesso_saude`.

**Hipótese secundária multinomial:**  
$H_0$: a distribuição dos cinco níveis de `desfecho_pedido` é igual entre requerentes com e sem assistência jurídica.  
$H_1$: ao menos uma proporção difere.

O desenho não identifica causalidade por si só. A simulação incluirá efeito gerador conhecido, mas a interpretação didática do notebook exigirá linguagem de **associação ajustada**, validade interna, validade externa e confundimento residual.

---

## 2. Arquitetura de arquivos

```text
./
├── PLANO_CDEaDPP_2026_Trabalho_Final_Zirconia.md
├── CDEaDPP_2026_Trabalho_Final_Zirconia.ipynb
├── src/
│   └── cdedpp_2026_zirconia/
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
    └── cdedpp_2026_zirconia/
        ├── zirconia_pedidos_simulados.csv
        ├── zirconia_piloto_simulado.csv
        └── figuras/
```

O notebook gerado deve ser autocontido: as células de código não importarão os módulos `src`; os módulos apenas constroem o `.ipynb`. O builder validará `nbformat`, sintaxe das células de código, ausência de outputs persistidos e alternância lógica entre Markdown e código.

---

## 3. Inventário de outputs do notebook

| Seção | Outputs obrigatórios |
|---|---|
| 1. Protocolo | Quadro T.E.M.P.; hipóteses; parâmetros globais; versões dos pacotes; asserts de ambiente. |
| 2. Dicionário | Tabela Markdown completa; DataFrame `dicionario`; listas de variáveis/categorias; asserts de cobertura. |
| 3. Simulação | Funções geradoras; amostra principal; piloto n=50; CSVs UTF-8; checagens de reprodutibilidade; exclusão da latente. |
| 4. Curadoria | Leitura dos CSVs; auditoria de tipos, duplicatas, NAs, domínios e fluxo de elegibilidade. |
| 5. EDA | Tabelas de frequência; medidas resumo; histogramas/densidades; boxplots; barras proporcionais; exploração de suporte comum. |
| 6. Modelagem | OLS bruto e ajustado; erros padrão agrupados por unidade; diagnóstico de resíduos; tabela 2x5 completa. |
| 7. NHST | Decisão primária com IC e p-valor; qui-quadrado 2x5 ou reamostragem condicional com margens fixas; discussão de erros tipo I/II. |
| 8. Amostragem | Cálculo para variável intervalar com piloto n=50; dimensionamento multinomial de cinco níveis; razão de grupos observada; sensibilidade; aviso sobre VIF, clusters e regressão ajustada. |
| 9. Síntese | Quadro-resumo dos parâmetros e resultados; checklist de replicabilidade; conclusão com limitações do estudo observacional retrospectivo. |

---

## 4. Esquema mínimo de variáveis

| Nome | Significado | Tipo e escala | Papel |
|---|---|---|---|
| `id_pedido` | Identificador artificial do pedido | Texto, identificador | Chave |
| `assistencia_juridica` | Acesso à Defensoria/serviço institucional antes da decisão final | Binária nominal | Independente principal |
| `indice_acesso_saude` | Escore didático de acesso efetivo à saúde | Quantitativa, intervalar assumida | Dependente primária |
| `desfecho_pedido` | Resultado em cinco categorias exaustivas | Multinomial nominal | Dependente secundária |
| `tempo_espera_dias` | Dias entre solicitação e decisão/atendimento | Quantitativa de razão | Covariável/desfecho auxiliar |
| `gravidade_clinica` | Gravidade prévia do caso | Ordinal | Confundidora observada |
| `renda_pc_zirc` | Renda familiar per capita em Z$ | Quantitativa de razão | Confundidora observada |
| `idade` | Idade do requerente | Quantitativa de razão | Confundidora observada |
| `regiao_zirconia` | Uma das 20 regiões do país | Nominal | Estrato/contexto |
| `unidade_zus` | Unidade administrativa/territorial | Nominal | Cluster inferencial |
| `capilaridade_defensoria` | Grau de presença institucional local | Ordinal | Confundidora/contexto |
| `completude_documental` | Documentos adequados no protocolo | Binária nominal | Covariável prévia |
| `ano_pedido` | Ano do pedido | Temporal discreta | Contexto |
| `letramento_digital_latente` | Facilidade não observada de navegar no ZUS | Latente | Confundidora oculta excluída da base analítica |

---

## 5. Regras estatísticas transversais

1. A alocação entre expostos e controles será observacional, sem impor grupos 1:1. O `ratio` observado no piloto n=50 entrará no dimensionamento.
2. O cálculo t para `indice_acesso_saude` será apresentado como aproximação analítica; o texto advertirá que ele ignora a inflação de variância por colinearidade entre exposição e covariáveis, sintetizada pelo VIF, além da dependência dentro de clusters.
3. A modelagem primária usará OLS ajustado com erros padrão agrupados por `unidade_zus`, declarando número de clusters e limitação quando houver poucos grupos efetivos.
4. A análise multinomial 2x5 verificará frequências esperadas antes do teste. Se houver célula esperada pequena, será acionado fallback por reamostragem condicional com margens fixas, sem colapsar categorias depois de ver resultado.
5. Nenhum `assert` exigirá `p < alpha`, pois significância observada é resultado aleatório mesmo com efeito gerador não nulo.
6. A latente usada no gerador não será exportada para o dataset analítico.

---

## 6. Sequência iterativa de implementação

| Iteração | Entrega | Gate de validação |
|---|---|---|
| 1 | Este plano, `__init__.py`, builder, seções 1 e 2, notebook inicial | Builder executa; notebook válido; células de código compilam; asserts iniciais passam. |
| 2 | Seção 3: simulação e piloto n=50 | Dados reproduzíveis; dois grupos no piloto e na amostra; cinco categorias válidas; CSVs criados. |
| 3 | Seções 4 e 5: curadoria e EDA | Frequências fecham; gráficos renderizam; perdas/duplicatas/NAs auditados. |
| 4 | Seções 6 e 7: modelagem e NHST | OLS com clusters executa; fallback 2x5 funciona; decisões coerentes com alpha. |
| 5 | Seção 8: tamanho amostral | Ratio do piloto aplicado; multinomial com cinco níveis; sensibilidade; VIF/clusters discutidos. |
| 6 | Seção 9 e validação final | Notebook completo executa em kernel limpo; síntese e checklist prontos. |

---

## 7. Critério final de conclusão

- [ ] `CDEaDPP_2026_Trabalho_Final_Zirconia.ipynb` existe na raiz e executa integralmente.
- [ ] Todas as seções obrigatórias aparecem com Markdown acadêmico e código funcional.
- [ ] O dicionário de dados tem tabela Markdown completa, com unidade de medida, tipo Python, papel e exemplos.
- [ ] A simulação injeta efeitos principais e confundimento plausível.
- [ ] O piloto tem n=50 e é distinto da amostra principal.
- [ ] OLS ajustado usa erros padrão agrupados por `unidade_zus`.
- [ ] O teste multinomial 2x5 usa qui-quadrado ou fallback por reamostragem conforme frequências esperadas.
- [ ] Os cálculos de amostra incorporam alpha, beta, desvio padrão do piloto, ratio observado, escala intervalar e escala multinomial com mais de três níveis.
- [ ] Todos os asserts previstos passam.
- [ ] O notebook base e os notebooks de estudos de caso existentes permanecem intactos.

---

## 8. Registro de execução

**Iteração 1 - 02/11/2026.** Criados plano específico, pacote `src/cdedpp_2026_zirconia`, builder, seções 1 e 2 e notebook inicial.

**Iteração 2 - 02/11/2026.** Criada a seção 3, com simulação principal, piloto n=50, função `softmax` estável, efeito principal pré-especificado, variável latente excluída da base analítica, exportação dos CSVs e asserts de reprodutibilidade/domínio. A próxima etapa é a **Seção 4 - Curadoria e Auditoria**.

**Iteração 3 - 02/11/2026.** Criada a seção 4, com recarga dos CSVs, aplicação de esquema, auditoria de NAs, duplicatas, domínios, estratos territoriais e temporais, preservação de linhas e distinção entre categoria substantiva `pendente_ou_sem_execucao` e ausência de dados. A próxima etapa é a **Seção 5 - Análise Exploratória**.

**Iteração 4 - 02/11/2026.** Criada a seção 5, com tabelas de frequência, tabela 2x5, estatísticas descritivas por grupo e unidade, avaliação de desequilíbrio basal, gráficos exploratórios e asserts de fechamento de frequências/percentuais/figuras. A próxima etapa é a **Seção 6 - Modelagem**.

**Iteração 5 - 02/11/2026.** Criada a seção 6, com OLS bruto, OLS ajustado por covariáveis prévias, efeitos fixos de unidade/ano, erros padrão agrupados por `unidade_zus`, checagem de posto da matriz de desenho, resumo de clusters, VIF descritivo, diagnóstico de resíduos e tabela 2x5 completa para a etapa inferencial. A próxima etapa é a **Seção 7 - NHST e erros de decisão**.

**Iteração 6 - 02/11/2026.** Criada a seção 7, com teste primário bilateral do coeficiente ajustado, decisão coerente com `alpha`, teste secundário da tabela 2x5, verificação de frequências esperadas antes da escolha do método, fallback por reamostragem condicional com margens fixas e quadro didático de erros tipo I, tipo II e poder. A próxima etapa é a **Seção 8 - Tamanho Amostral e Piloto**.

**Iteração 7 - 02/11/2026.** Criada a seção 8, com uso do piloto n=50 para estimar desvio padrão e razão controle/atendido, cálculo t aproximado para variável intervalar, simulação de poder para desfecho multinomial 2x5, cálculo complementar de aderência, calibração por simulação do OLS ajustado com erros agrupados e N final com perdas. A próxima etapa é a **Seção 9 - Síntese e protocolo replicável**.

**Iteração 8 - 02/11/2026.** Criada a seção 9, com síntese acadêmica, quadro-resumo reproduzível, versões, checklist final, conclusão parametrizada e limitações de validade interna/externa/mensuração para estudo observacional retrospectivo. O notebook completo está pronto para validação integral.
