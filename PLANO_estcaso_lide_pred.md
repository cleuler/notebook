# Plano de Execução — `estcaso_lide_pred.ipynb`

**Estudo de Caso 3: Identificação da Litigância Abusiva Predatória nos 14 Juizados Especiais Cíveis de Natal/RN**

**Autora da monografia:** Hadja Rayanne Holanda de Alencar
**Notebook a ser criado por:** Claude Sonnet 4.6
**Modelo de referência:** `EstudoCaso1_RafaelCosta/rafaelcc_ed1.ipynb` e seus módulos em `EstudoCaso1_RafaelCosta/src/`

---

## 0. Contexto e Fontes

### 0.1 Documentos-fonte da pesquisa

| Arquivo | Conteúdo relevante |
|---|---|
| `txt/ProjetoHadja_FinalCorrigidoBanca_9mar2026.docx` | Projeto de pesquisa aprovado pela banca — hipóteses, variáveis (Apêndice B), exploração piloto (Apêndices C e D), quadro de variáveis original |
| `txt/26_08_MonografiaFinal_Hadja.docx` | Monografia final — **Cap. 3** (Metodologia: desenho amostral, construção das variáveis, fases I-III) e **Cap. 4** (Resultados: gráficos 1-12, tabelas 5-17, testes inferenciais e modelos). **Todos os outputs analíticos a replicar estão nos capítulos 3 e 4.** |

### 0.2 Dados

| Arquivo | Aba | Linhas × Colunas | Descrição |
|---|---|---|---|
| `dat/estcaso_lide_pred/PlanilhaPreenchidaVariaveisCorrigida_CN_JE_S1422934_Mestrado_03_02.xlsx` | **`AMOSTRA`** | 595 × 34 | **Base principal.** Cada linha é um processo amostrado. 34 colunas: identificação (nº processo, unidade, ano, classe), 6 variáveis Fase I (F1_A…F1_F), conclusão Fase I, 17 variáveis Fase II (F2_01…F2_17), conclusão Fase II, 3 variáveis Fase III (F3_18…F3_20), observações. Valores: "Sim"/"Não"/"sim"/"não" (case-insensitive). |
| (mesmo arquivo) | `Base consolidada` | 50.320 × 34 | População após depuração (sem duplicatas, sem execuções extrajudiciais, sem processos sem advogado). |
| (mesmo arquivo) | `TJRN` | 86.964 × 30 | Dados brutos originais fornecidos pelo TJRN. |
| (mesmo arquivo) | `Quadro variáveis` | ~25 × 11 | Dicionário de variáveis. |
| (mesmo arquivo) | `Amostragem (Fórmula)` | ~2.470 × 33 | Fórmulas de amostragem (RANDBETWEEN + VLOOKUP). |
| `dat/estcaso_lide_pred/casos_novos_JEC_Natal_chamado_S1392344_21.05.2025.xlsx` | — | — | Dados complementares (casos novos). |

### 0.3 Variáveis da aba `AMOSTRA` (34 colunas)

```
Col  0: Amostra selecionada (ID numérico)
Col  1: Número do Processo
Col  2: Unidade Judiciária (ex.: "10º JUIZADO ESPECIAL CÍVEL")
Col  3: Ano da distribuição (2022, 2023, 2024)
Col  4: Classe (ex.: "PROCEDIMENTO DO JUIZADO ESPECIAL CÍVEL")
Col  5: F1_A - Ações de pessoa física no polo passivo
Col  6: F1_B - Ausência de grande litigante no polo passivo
Col  7: F1_C - Processo de conhecimento em curso
Col  8: F1_D - Processos suspensos
Col  9: F1_E - Distribuição incorreta
Col 10: F1_F - Parte_PJ
Col 11: Conclusão FASE I (fórmula: "Parou na Fase I" / "Seguiu para Fase II" / ...)
Col 12: F2_01 - Petição vaga/genérica
Col 13: F2_02 - Ausência de documentos essenciais
Col 14: F2_03 - Documentos sem relação com a causa de pedir
Col 15: F2_04 - Pedido de dispensa de audiência
Col 16: F2_05 - Foro inadequado
Col 17: F2_06 - Documentos incompletos/ilegíveis
Col 18: F2_07 - Pedidos vagos/hipotéticos
Col 19: F2_08 - Demanda idêntica não declarada
Col 20: F2_09 - Procuração incompleta
Col 21: F2_10 - Procuração irregular (assinatura digital)
Col 22: F2_11 - Advogado fora da comarca
Col 23: F2_12 - Valor da causa inadequado
Col 24: F2_13 - Classe ou assunto incorreto
Col 25: F2_14 - Desistência/abandono após indeferimento de liminar
Col 26: F2_15 - Desistência/abandono após notificação
Col 27: F2_16 - Desistência/abandono após contestação
Col 28: F2_17 - Contrato de honorários abusivo
Col 29: Conclusão FASE II
Col 30: F3_18 - Multiplicidade de ações
Col 31: F3_19 - Petições idênticas
Col 32: F3_20 - Volume elevado de demandas
Col 33: obs
```

---

## 1. Estrutura de Pastas e Arquivos a Criar

```
./  (raiz do projeto)
├── estcaso_lide_pred.ipynb              ← notebook principal (gerado por build)
├── src/
│   └── estcaso_lide_pred/
│       ├── __init__.py
│       ├── build_notebook.py            ← gera o .ipynb a partir dos módulos
│       ├── secao01_ambiente.py          ← preparação do ambiente e paleta
│       ├── secao02_curadoria.py         ← leitura, limpeza, tipagem, esquema
│       ├── secao03_populacao.py         ← análise da população (Tab. 1)
│       ├── secao04_amostra.py           ← desenho amostral (Tab. 2, Tab. 3)
│       ├── secao05_descritiva.py        ← fluxo funil (Gráf. 1-2), estimativas (Tab. 5),
│       │                                   combinações F3 (Tab. 6, Gráf. 3-4),
│       │                                   incidência por ano (Tab. 7, Gráf. 5),
│       │                                   incidência por unidade (Tab. 8, Gráf. 6)
│       ├── secao06_frequencias.py       ← frequências F1 (Tab. 9), F2 (Gráf. 7, Tab. 10)
│       ├── secao07_inferencial.py       ← qui-quadrado por ano (Tab. 11, Gráf. 8),
│       │                                   qui-quadrado por unidade (Tab. 12),
│       │                                   associação bivariada F2 × classificação
│       │                                   (Tab. 13, Gráf. 9 forest plot)
│       ├── secao08_regressao.py         ← regressão logística (Tab. 14, Gráf. 10 ROC),
│       │                                   frequência F2_14-F2_17 (Tab. 15)
│       ├── secao09_correlacao.py        ← coeficiente phi (Gráf. 11 heatmap,
│       │                                   Gráf. 12 barras, Tab. 16, Tab. 17)
│       └── secao10_sintese.py           ← resumo, limitações, próximos passos
└── dat/
    └── estcaso_lide_pred/               ← já existe
        ├── PlanilhaPreenchida...xlsx     ← já existe
        └── casos_novos...xlsx           ← já existe
```

**Observação sobre a arquitetura:** Seguir o padrão do modelo `EstudoCaso1_RafaelCosta`, onde:
- Cada seção é um arquivo `.py` que usa as funções `md()`, `code()` e `interp()` do builder;
- O `build_notebook.py` importa e executa cada seção para montar o `.ipynb`;
- O notebook gerado é autocontido (pode ser executado standalone).

---

## 2. Inventário Completo dos Outputs a Replicar

### 2.1 Do Capítulo 3 (Metodologia)

| Output | Tipo | Seção | Descrição | Dados-fonte |
|---|---|---|---|---|
| Tabela 1 | Tabela | 3.2.1 | Processos distribuídos nos 14 JEC (2022-2024), por unidade e ano | Aba `TJRN` ou `Base consolidada` |
| Tabela 2 | Tabela | 3.2.2 | Distribuição da amostra por unidade judiciária e ano (n=595) | Aba `AMOSTRA` |
| Tabela 3 | Tabela | 3.2.3 | Distribuição da amostra por classe processual | Aba `AMOSTRA` |
| Quadro 3 | Tabela | 3.2 | Variáveis utilizadas no estudo (25 variáveis, 3 fases) | Aba `Quadro variáveis` |
| Tabela 4 | Tabela | 3.3 | Quadro consolidado das 25 variáveis observacionais | Aba `Quadro variáveis` |

### 2.2 Do Capítulo 4 (Resultados)

#### 2.2.1 Resultados descritivos gerais (seção 4.1)

| Output | Tipo | Seção | Descrição | Método |
|---|---|---|---|---|
| **Gráfico 1** | Gráfico de funil | 4.1.1 | Funil de classificação: 595 → 444 → 233 → 105/30 | Barras horizontais/verticais decrescentes |
| **Gráfico 2** | Barras empilhadas | 4.1.1 | Composição percentual da amostra: excluídos F1, sem indicativo F2, demais F3, indício, certeza | Barras empilhadas a 100% |
| **Tabela 5** | Tabela | 4.1.2 | Indicadores estatísticos: proporção, IC 95% (Wilson), projeção para população | Binomial, Wilson CI |
| **Tabela 6** | Tabela | 4.1.3 | Combinações das 3 variáveis F3 (8 combinações possíveis) entre os 233 processos | Crosstab F3_18 × F3_19 × F3_20 |
| **Gráfico 3** | Barras | 4.1.3 | Combinações de variáveis F3 (visualização da Tab. 6) | Barras por combinação |
| **Gráfico 4** | Barras | 4.1.3 | Frequência absoluta das variáveis F3 isoladas | Barras F3_18, F3_19, F3_20 |
| **Tabela 7** | Tabela | 4.1.4 | Distribuição da classificação (indício/certeza) por ano | Crosstab ano × classificação |
| **Gráfico 5** | Barras agrupadas | 4.1.4 | Indício e certeza por ano | Barras agrupadas/empilhadas |
| **Tabela 8** | Tabela | 4.1.5 | Indício e certeza por unidade judiciária (14 JECs) | Crosstab unidade × classificação |
| **Gráfico 6** | Barras | 4.1.5 | Percentual de indício e certeza por unidade, com linha de média | Barras com referência |

#### 2.2.2 Frequência das variáveis (seção 4.2)

| Output | Tipo | Seção | Descrição | Método |
|---|---|---|---|---|
| **Tabela 9** | Tabela | 4.2.1 | Frequência das variáveis da Fase I (n=595) | Contagem Sim/Não por F1 |
| **Gráfico 7** | Barras horizontais | 4.2.2 | Frequência das variáveis da Fase II (n=595) | Barras ordenadas por freq. |
| **Tabela 10** | Tabela | 4.2.2 | Indício e certeza por classe processual | Crosstab classe × classif. |

#### 2.2.3 Testes inferenciais (seção 4.3)

| Output | Tipo | Seção | Descrição | Método estatístico |
|---|---|---|---|---|
| **Tabela 11** | Tabela | 4.3.1 | Indício e certeza por ano com IC de Wilson | IC Wilson, χ² de homogeneidade (χ²=1,87; gl=2; p=0,393), testes z pareados |
| **Gráfico 8** | Barras com IC | 4.3.1 | Proporções por ano com barras de erro (Wilson 95%) | Barras + errorbar |
| **Teste χ² certeza por ano** | Texto | 4.3.1 | χ²=4,36; gl=2; p=0,113 | χ² de homogeneidade |
| **Teste χ² por unidade** | Texto | 4.3.2 | χ²=20,83; gl=13; p=0,076 | χ² de homogeneidade 14×2 |
| **Tabela 12** | Tabela | 4.3.2 | Comparações pareadas entre unidades (teste z de proporções) | z-test de proporções, post-hoc |
| **Tabela 13** | Tabela | 4.3.3 | Associação bivariada F2 × classificação: OR, Fisher, IC 95% | Fisher exato, odds ratio |
| **Gráfico 9** | Forest plot | 4.3.3 | Odds Ratios das variáveis F2 com IC | Forest plot horizontal |
| **Tabela 14** | Tabela | 4.3.4 | Modelo logístico reduzido (F2_01, F2_02, F2_11): OR, IC, p | `statsmodels.Logit`, pseudo-R² McFadden=0,482 |
| **Gráfico 10** | Curva ROC | 4.3.4 | ROC do modelo logístico reduzido (AUC=0,908) | ROC + AUC |
| **Matriz de confusão** | Texto | 4.3.4 | VP=85, VN=117, FP=11, FN=20; acurácia=86,7% | Confusion matrix |
| **Tabela 15** | Tabela | 4.3.4.1 | Frequência das variáveis F2_14 a F2_17 entre classificados | Contagem condicional |
| **Teste χ² F2_14** | Texto | 4.3.4.1 | χ²=23,44; gl=1; p<0,001 | χ² de associação |
| **Gráfico 11** | Heatmap | 4.3.4.4 | Matriz de correlação φ entre 23 variáveis + 2 classificações | Phi (=Pearson para binárias), heatmap |
| **Gráfico 12** | Barras horizontais | 4.3.4.4 | Correlações φ com Indício e Certeza, ordenadas | Barras duplas |
| **Tabela 16** | Tabela | 4.3.4.4 | Coeficientes φ com p-valores do χ² de associação | Phi + χ² |
| **Tabela 17** | Tabela | 4.3.4.4 | Pares de variáveis preditoras com |φ|≥0,4 | Filtro da matriz |

---

## 3. Pipeline Detalhado por Seção do Notebook

### Seção 1 — Preparação do Ambiente (`secao01_ambiente.py`)

**Conteúdo:**
- Markdown introdutório (título, autora, pipeline geral)
- Importações: `numpy`, `pandas`, `matplotlib`, `seaborn`, `scipy.stats`, `statsmodels` (Logit, proportion_confint, chi2_contingency, fisher_exact), `sklearn.metrics` (roc_curve, auc, confusion_matrix)
- Paleta de cores fixa (seguir o mesmo esquema do modelo, com validação para daltonismo)
- Configuração de `plt.rcParams` e `pd.set_option`
- Semente aleatória fixa (`RNG = np.random.default_rng(2026)`)
- Localização dos dados (`PASTA_DADOS`)
- Impressão das versões dos pacotes

**Dependências do `pyproject.toml` a verificar/adicionar:**
- `openpyxl`, `scipy`, `statsmodels`, `seaborn`, `scikit-learn`, `matplotlib`

### Seção 2 — Curadoria dos Dados (`secao02_curadoria.py`)

**Conteúdo:**
1. **Leitura** da aba `AMOSTRA` (595 linhas) com `pd.read_excel(..., sheet_name='AMOSTRA')`
2. **Leitura** da aba `Quadro variáveis` → dicionário
3. **Leitura** da aba `Base consolidada` (50.320 linhas) → população
4. **Padronização de nomes** das colunas: remover espaços, criar identificadores Python
5. **Normalização dos valores Sim/Não**: converter "sim"/"Sim"/"SIM" → `True`, "não"/"Não"/"NÃO" → `False`, usando dtype `boolean`
6. **Tratamento da col. 11 (Conclusão FASE I)**: se contém fórmula, recalcular a partir das F1 booleanas
7. **Variáveis derivadas:**
   - `Excluido_F1`: `bool` = qualquer F1 == True
   - `Alguma_F2`: `bool` = qualquer F2 == True (entre F2_01…F2_17)
   - `Avancou_F3`: `bool` = `Alguma_F2` == True (233 processos)
   - `Indicio`: `bool` = `F3_19` & `F3_20` (inclui certeza)
   - `Certeza`: `bool` = `F3_18` & `F3_19` & `F3_20`
   - `Classificacao`: category com 5 níveis = {"Excluído na Fase I", "Sem indicativo na Fase II", "Demais processos na Fase III", "Indício (sem certeza)", "Certeza"}
   - `JEC_numero`: int extraído de "Xº JUIZADO ESPECIAL CÍVEL"
8. **Esquema de tipos** e `assert` de coerência (n=595, variáveis booleanas sem NA, etc.)
9. **Exportação** do DataFrame curado em `dat/estcaso_lide_pred/processado/hadja_amostra_limpa.pkl`
10. **Exibição** do dicionário de variáveis (Quadro 3 / Tabela 4)

**Regras de validação (com `assert`):**
- 595 linhas na amostra
- 151 excluídos na Fase I + 444 seguiram = 595
- 211 sem indicativo + 233 avançaram à Fase III = 444
- 105 com indício (incluindo 30 com certeza)
- Nenhum NA nas variáveis F1/F2/F3

### Seção 3 — População de Referência (`secao03_populacao.py`)

**Output: Tabela 1**
- Ler aba `Base consolidada` ou `TJRN`
- Agregar por `UNIDADE` × `Ano de início`
- Produzir tabela com 14 linhas (JECs) × 3 colunas (2022, 2023, 2024) + Total
- Exibir como `display()` estilizado

### Seção 4 — Desenho Amostral (`secao04_amostra.py`)

**Outputs: Tabela 2, Tabela 3**

**Tabela 2:** Distribuição da amostra por unidade e ano
- `pd.crosstab(dados['Unidade'], dados['Ano'], margins=True)`
- Conferir: 194 em 2022, 211 em 2023, 190 em 2024, total 595

**Tabela 3:** Distribuição por classe processual
- `dados['Classe'].value_counts()`
- Quase todos "PROCEDIMENTO DO JUIZADO ESPECIAL CÍVEL"; classes residuais agrupadas

**Cálculo do erro amostral efetivo:**
- Fórmula da correção para população finita: `e = z * sqrt(p*(1-p)/n) * sqrt((N-n)/(N-1))`
- Resultado esperado: ±4,0 p.p.

### Seção 5 — Resultados Descritivos Gerais (`secao05_descritiva.py`)

**Outputs: Gráficos 1-6, Tabelas 5-8**

#### 5.1 Fluxo pelas fases (Gráfico 1 — Funil)
```python
# Dados do funil:
# 595 → 444 (Fase II) → 233 (Fase III) → 105 (Indício) / 30 (Certeza)
# Usar barras horizontais decrescentes ou diagrama de funil
```

#### 5.2 Composição da amostra (Gráfico 2 — Barras empilhadas)
```python
# 5 categorias (sem dupla contagem):
# Excluídos F1: 151
# Sem indicativo F2: 211
# Demais processos F3: 128
# Indício (sem certeza): 75
# Certeza: 30
# Total = 595
```

#### 5.3 Estimativa para a população (Tabela 5)
```python
from statsmodels.stats.proportion import proportion_confint

# Indício (incl. certeza): k=105, n=595
# IC Wilson 95%
# Projeção: proporção × N_populacao (83.139 ou 50.320)
```

#### 5.4 Combinações F3 (Tabela 6, Gráficos 3-4)
```python
# Crosstab das 8 combinações possíveis de (F3_18, F3_19, F3_20)
# entre os 233 processos da Fase III
combos = dados_f3.groupby(['F3_18', 'F3_19', 'F3_20']).size()
```

#### 5.5 Por ano (Tabela 7, Gráfico 5)
```python
pd.crosstab(dados['Ano'], dados['Classificacao_resumida'])
# Classificacao_resumida: {Sem indício, Indício, Certeza}
```

#### 5.6 Por unidade (Tabela 8, Gráfico 6)
```python
# Crosstab JEC × classificação
# Gráfico: barras por JEC + linha tracejada na média (17,6%)
```

### Seção 6 — Frequência das Variáveis (`secao06_frequencias.py`)

**Outputs: Tabela 9, Gráfico 7, Tabela 10**

#### Tabela 9 — Fase I (n=595)
```python
freq_f1 = dados[cols_f1].sum()  # booleanas: sum() = contagem de True
```

#### Gráfico 7 — Fase II (n=595)
```python
# Barras horizontais ordenadas por frequência
# 17 variáveis F2; 4 com zero ocorrências (F2_07, F2_12, F2_15, F2_16)
```

#### Tabela 10 — Indício/certeza por classe processual
```python
pd.crosstab(dados['Classe_resumida'], dados['Classificacao_resumida'])
```

### Seção 7 — Testes Inferenciais: Homogeneidade e Associação Bivariada (`secao07_inferencial.py`)

**Outputs: Tabela 11, Gráfico 8, Tabela 12, Tabela 13, Gráfico 9**

#### 7.1 Homogeneidade entre anos (Tabela 11, Gráfico 8)

```python
from scipy.stats import chi2_contingency
from statsmodels.stats.proportion import proportion_confint, proportions_ztest

# Tabela 3×2: ano × (indício_ou_certeza / demais)
tabela_ano = pd.crosstab(dados['Ano'], dados['Indicio'])
chi2, p, gl, esperada = chi2_contingency(tabela_ano, correction=False)
# Esperado: χ²=1,87; gl=2; p=0,393

# Testes z pareados: 2022 vs 2023, 2022 vs 2024, 2023 vs 2024
# IC Wilson por ano

# Gráfico 8: barras com errorbar (IC Wilson)
```

#### 7.2 Homogeneidade entre unidades (Tabela 12)

```python
# Tabela 14×2: JEC × (indício / não)
# χ²=20,83; gl=13; p=0,076

# Comparações pareadas: 7º JEC vs demais, 7º vs 13º, etc.
# Teste z de proporções com significância
```

#### 7.3 Associação bivariada F2 × classificação final (Tabela 13, Gráfico 9)

```python
from scipy.stats import fisher_exact

# Para cada F2 (com ocorrências > 0), entre os 233 da Fase III:
# - Odds Ratio
# - IC 95% do OR
# - p-valor (Fisher exato)
# - Proporção condicional (% indício|F2=Sim vs % indício|F2=Não)

# Gráfico 9: Forest plot horizontal
# - Eixo x: OR em escala log
# - Cada linha: uma variável F2
# - Marcador: OR pontual; barra: IC 95%
# - Linha tracejada em OR=1
# - Destaque em vermelho para p < 0,001
```

**Referência do modelo:** A função `grafico_floresta()` de `secao15_etapa1.py` (linhas do Cox) deve ser adaptada para os OR.

### Seção 8 — Regressão Logística (`secao08_regressao.py`)

**Outputs: Tabela 14, Gráfico 10, Tabela 15, Matriz de confusão**

#### 8.1 Modelo logístico (Tabela 14)

```python
import statsmodels.api as sm

# Base: 233 processos da Fase III
# Y = Indicio (bool)
# X = F2_01, F2_02, F2_04, F2_06, F2_09, F2_10, F2_11, F2_13
#     (variáveis com ≥ 10 ocorrências na Fase III)

# Modelo completo → pseudo-R² McFadden = 0,496
# Modelo reduzido (F2_01, F2_02, F2_11) → pseudo-R² = 0,482

X_red = sm.add_constant(dados_f3[['F2_01', 'F2_02', 'F2_11']].astype(float))
y = dados_f3['Indicio'].astype(int)
logit = sm.Logit(y, X_red).fit(disp=False)

# Tabela 14: coef, OR=exp(coef), IC 95%, p-valor
# AIC=174,13; log-verossimilhança=-83,06
```

#### 8.2 Curva ROC (Gráfico 10)

```python
from sklearn.metrics import roc_curve, auc, confusion_matrix

prob = logit.predict()
fpr, tpr, _ = roc_curve(y, prob)
roc_auc = auc(fpr, tpr)  # Esperado: 0,908

# Matriz de confusão (corte=0,5):
# VP=85, VN=117, FP=11, FN=20
# Acurácia=86,7%, Sensibilidade=80,9%, Especificidade=91,4%
```

#### 8.3 Variáveis F2_14 a F2_17 (Tabela 15)

```python
# Frequência de F2_14 a F2_17 entre os classificados (indício/certeza)
# F2_15 e F2_16: zero ocorrências em toda a amostra
# F2_14: teste χ² de associação (χ²=23,44; gl=1; p<0,001)
```

### Seção 9 — Análise de Correlação Phi (`secao09_correlacao.py`)

**Outputs: Gráfico 11, Gráfico 12, Tabela 16, Tabela 17**

#### 9.1 Matriz de correlação φ (Gráfico 11)

```python
# 23 variáveis (5 F1 + 13 F2 com ocorrências + 3 F3 + 2 classificações)
# Excluir F2_07, F2_12, F2_15, F2_16 (zero ocorrências)
# φ = correlação de Pearson entre variáveis binárias 0/1

# Heatmap: triangular inferior
# Cores quentes = correlação positiva; cores frias = negativa
# Exibir numericamente apenas |φ| ≥ 0,10

import seaborn as sns
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(corr_matrix, mask=mask, cmap=mapa_divergente,
            center=0, vmin=-1, vmax=1, annot=True, fmt='.2f')
```

#### 9.2 Barras de correlação (Gráfico 12)

```python
# Duas colunas da matriz: correlação com Indício e com Certeza
# Barras horizontais, ordenadas por |φ| com Indício
```

#### 9.3 Tabela de coeficientes (Tabela 16)

```python
# Para cada variável:
# - φ com Indício, p-valor (χ²)
# - φ com Certeza, p-valor (χ²)
# Ordenada por φ com Indício (decrescente)
```

#### 9.4 Pares com correlação forte (Tabela 17)

```python
# Filtrar pares com |φ| ≥ 0,4
# Destaques esperados:
# - F2_01 × F2_02: φ ≈ 0,98
# - F2_02 × F2_11: φ ≈ 0,45
# - F2_01 × F2_06: ...
```

### Seção 10 — Síntese (`secao10_sintese.py`)

**Conteúdo (Markdown):**
1. Resumo dos achados principais (5 padrões da seção 4.3.4.4)
2. Comparação com a Nota Técnica 01/2022 do CIJMG (hipótese H2: >30%)
3. Limitações da pesquisa
4. Próximos passos

---

## 4. Correspondência Modelo ↔ Notebook Hadja

| Recurso do modelo (rafaelcc_ed1) | Equivalente no estudo Hadja |
|---|---|
| Leitura de ApêndiceA/B (xlsx) | Leitura das abas AMOSTRA, Quadro variáveis, Base consolidada |
| Partições e normalização categórica | Normalização Sim/Não → boolean; extração JEC_numero |
| `verificar_particao()` com assert | Verificar contagens: 595=151+444, 444=211+233, etc. |
| Teste binomial exato | Estimativa pontual e IC Wilson (Tabela 5) |
| Qui-quadrado, Fisher, post-hoc | Homogeneidade por ano/unidade (Tab. 11-12), associação bivariada (Tab. 13) |
| Forest plot do Cox | Forest plot dos OR (Gráfico 9) |
| Regressão logística (indiciamento) | Regressão logística (classificação final) (Tab. 14) |
| Curva ROC | Curva ROC (Gráfico 10) |
| — (novo) | Coeficiente phi e heatmap (Gráf. 11-12, Tab. 16-17) |
| Boxplot por grupos | — (variáveis são todas binárias; não há variável contínua) |
| Kaplan-Meier, Cox, AFT | — (não há análise de sobrevivência neste estudo) |

---

## 5. Valores de Referência para Validação

Os `assert` e testes de regressão devem conferir os valores publicados na monografia:

| Verificação | Valor esperado |
|---|---|
| `len(amostra)` | 595 |
| `amostra['Excluido_F1'].sum()` | 151 |
| `amostra['Alguma_F2'].sum()` (entre os 444) | 233 |
| `amostra['Indicio'].sum()` | 105 |
| `amostra['Certeza'].sum()` | 30 |
| Proporção indício (incl. certeza) | 17,65% → IC [14,59%; 20,70%] |
| Proporção certeza | 5,04% → IC [3,29%; 6,79%] |
| χ² homogeneidade por ano | 1,87 (gl=2; p=0,393) |
| χ² homogeneidade por unidade | 20,83 (gl=13; p=0,076) |
| OR F2_02 (bivariada) | 45,2 (p<0,001) |
| OR F2_01 (bivariada) | ~39,8 (p<0,001) |
| OR F2_11 (bivariada) | ~11,4 (p<0,001) |
| Pseudo-R² modelo reduzido | 0,482 |
| AUC ROC | 0,908 |
| Acurácia (corte 0,5) | 86,7% |
| φ(F2_01, F2_02) | ≈ 0,98 |
| φ(F2_02, Indício) | 0,82 |
| χ² F2_14 × classificação | 23,44 (gl=1; p<0,001) |

---

## 6. Observações Técnicas para o Claude Sonnet 4.6

### 6.1 Encoding
- O arquivo `.docx` usa encoding com caracteres CJK/Latin que o Python pode ler com `python-docx`, mas a saída no terminal Windows requer `chcp 65001` ou `sys.stdout` com UTF-8.
- A planilha Excel tem valores "Sim"/"sim"/"Não"/"não" → normalizar com `.str.strip().str.lower()` antes de converter.

### 6.2 Fórmulas na planilha
- A coluna 11 (Conclusão FASE I) e coluna 29 (Conclusão FASE II) podem conter **fórmulas Excel** em vez de valores. Usar `openpyxl` com `data_only=True` ou, preferencialmente, **recalcular** as conclusões a partir das variáveis F1/F2/F3 booleanas.

### 6.3 Escala do problema
- A amostra tem apenas 595 processos e 25 variáveis binárias → cabe inteiramente na memória.
- A população (`Base consolidada`, 50.320 linhas) é usada apenas para a Tabela 1 e para projeções.
- A aba `TJRN` (86.964 linhas) é a base bruta original e pode ser usada para conferência.

### 6.4 Testes estatísticos — cuidados
- **Fisher exato** é preferível ao χ² quando há caselas com frequência esperada < 5 (especialmente nas variáveis F2 raras).
- **IC Wilson** para proporções (não o de Wald), conforme adotado na monografia.
- **Regressão logística:** atentar para separação perfeita ou quasi-perfeita em variáveis com OR muito alto (F2_02, OR=30+). Se `statsmodels.Logit` falhar na convergência, usar penalização (Firth) ou regularização (`method='bfgs'`, `maxiter=1000`).
- **Coeficiente phi (φ):** é o Pearson entre binárias; pode ser calculado como `np.corrcoef()` ou via `scipy.stats.pearsonr()`. Excluir variáveis constantes (zero ocorrências).

### 6.5 Gráficos — padrão visual
- Seguir a paleta e o estilo do modelo (`COR_PRINCIPAL`, `COR_DESTAQUE`, `TINTA`, `GRADE`).
- Funções utilitárias do modelo a replicar/adaptar:
  - `quebrar(rotulo, largura)` — quebra rótulos longos em múltiplas linhas
  - `serie_exibicao()` — converte booleanos para rótulos legíveis
  - `barras_verticais_empilhadas()` — barras a 100%
  - `grafico_floresta()` — forest plot dos OR/HR
- Cada gráfico deve ter título com o nome do teste e o p-valor.

### 6.6 Ordem de execução
1. Ler `secao01_ambiente.py` → `secao02_curadoria.py` → demais seções.
2. Cada seção depende do DataFrame `dados` criado na seção 2.
3. A seção 7 (inferencial) depende do subconjunto `dados_f3` (233 processos) criado na seção 5.
4. Todas as seções usam as constantes e funções utilitárias definidas na seção 1.

---

## 7. Sequência de Prompts Sugerida para o Claude Sonnet 4.6

| Prompt | Ação | Validação |
|---|---|---|
| 1 | Criar `src/estcaso_lide_pred/__init__.py` e `secao01_ambiente.py` | Executar célula de imports sem erro |
| 2 | Criar `secao02_curadoria.py` | `assert len(dados)==595`, variáveis booleanas, contagens batem |
| 3 | Criar `secao03_populacao.py` + `secao04_amostra.py` | Tabelas 1-4 reproduzidas |
| 4 | Criar `secao05_descritiva.py` | Gráficos 1-6, Tabelas 5-8 reproduzidas, contagens conferem |
| 5 | Criar `secao06_frequencias.py` | Tabela 9, Gráfico 7, Tabela 10 |
| 6 | Criar `secao07_inferencial.py` | χ²=1,87; χ²=20,83; OR de F2_02=45,2; forest plot |
| 7 | Criar `secao08_regressao.py` | pseudo-R²=0,482; AUC=0,908; matriz de confusão |
| 8 | Criar `secao09_correlacao.py` | Heatmap phi; φ(F2_01,F2_02)≈0,98 |
| 9 | Criar `secao10_sintese.py` + `build_notebook.py` | Gerar `estcaso_lide_pred.ipynb` e executar end-to-end |

---

## 8. Checklist Final

- [ ] Notebook executa do início ao fim sem erro
- [ ] 12 gráficos reproduzidos (Gráficos 1–12)
- [ ] 17 tabelas reproduzidas (Tabelas 1–4, 5–17 + Quadro 3)
- [ ] Todos os testes estatísticos conferem com os valores publicados
- [ ] Nenhum dado é inventado: tudo vem da planilha ou é calculado
- [ ] Paleta visual consistente e acessível
- [ ] Células de markdown com interpretação dos resultados
- [ ] README do estudo de caso (análogo ao modelo)
