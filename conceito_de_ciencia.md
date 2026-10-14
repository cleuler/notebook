# Um conceito analítico e axiomático de Ciência sob o dogma da irrenunciabilidade dos pontos de partida

## 1 INTRODUÇÃO

## 2 SÍNTESE A PRIORI DO CONCEITO: PEQUENO CONJUNTO DE GRANDE ALCANCE

## 3 DECOMPOSIÇÃO ANALÍTICA DE SEUS ELEMENTOS

### 3.1 CONCEITOS: PODER OU LIBERDADE DE DEFINIR

### 3.2 AXIOMAS/DOGMAS: PODER DE RESSALVAR PONTOS DE PARTIDA

### 3.3 MÉTODOS: SOB A LÓGICA DO 3º EXCLUÍDO

* **3.3.1 DEDUTIVO:**  $28$ inferências válidas $(P_M \wedge p_m \rightarrow C)$
* **3.3.2 INDUTIVO:** Salto maior $(p_m \wedge C \rightarrow P_M)$
* **3.3.3 ABDUTIVO:** Salto menor $(P_M \wedge C \rightarrow p_m)$

---

## 4 HIPÓTESES

* **4.1 ESPAÇO AMOSTRAL** ($\Omega$)
* **4.2 Partição: subconjuntos que formem classes perfeitas de ($\Omega$)**
* **4.3 Possíveis ($P(H) > 0$)  e Impossíveis** ($P(H) = 0$)
* **4.4 Excludentes:** $H_i \cap H_j = \emptyset, \quad i \neq j$
* **4.5 Exaustivas:** $\bigcup H_i = \Omega, \quad i=1, 2, \dots, N \in \mathbb{N}$
* **4.6 Concorrência e Modus Tollens **:** $(Th \rightarrow H_0) \quad e \quad \neg H_0 \quad \therefore \neg T$ (falha teórica)**
  * **4.6.1 Refutação: Teste de Significância contra $H_0$** (TSHN)
  * **4.6.2 Corroboração:** Hipótese Alternativa (Teoria Rival)
  * **4.6.3 Inconclusão:** Tollens não recíproco
  * **4.6.4 Erros Tipo I ($\alpha$) e Tipo II ($\beta$):** Falso Positivo e Falso Negativo
  * **4.6.5 Sensibilidade (s) e Especificidade (e):** VPP / VPN
  * **4.6.6 Curva ROC:** $s \times (1 - e)$ e Índice de Gini

---

### 4.7 Fator de Bayes e Força Relativa contra e a favor de uma Hipótese ($H_1$) em razão de outra concorrente ($H_0$)

* **4.7.1 Probabilidade Condicional:** $P(A|B)$ ou $P(H_1 | \text{dados})$
* **4.7.2 Regra da Multiplicação**
* **4.7.3 Eventos Independentes**
* **4.7.4 Teorema de Bayes: dados como Evidência**
  * **a)** Probabilidade a priori: $P(H_1)$
  * **b)** Verossimilhança de $H_1$: $P(\text{dados} | H_1)$
  * **c)** Padronização pela Probabilidade Total: $P(\text{dados})$
  * **d)** Probabilidade a posteriori: $P(H_1 | \text{dados})$
  * **f)** Formulação:

$$
P(H_1 | \text{dados}) = \frac{P(\text{dados} | H_1) \cdot P(H_1)}{P(\text{dados})}
$$

* **4.7.5 Razão de "Chances" / Likelihood Ratio / Odds Ratio (ODR):**

$$
FB_{10} = \frac{P(H_1 | \text{dados})}{P(H_0 | \text{dados})} = \frac{P(\text{dados} | H_1) \cdot P(H_1)}{P(\text{dados} | H_0) \cdot P(H_0)}
$$

* $P(H_0 | \text{dados}) \in [0, 1]$
* $P(H_1 | \text{dados}) \in [0, 1]$
* $FB_{10} \in [0, +\infty[$
* $FB < 1 \Rightarrow P(H_1 | \text{dados}) < P(H_0 | \text{dados})$
* $FB = 1 \Rightarrow P(H_1 | \text{dados}) = P(H_0 | \text{dados})$
* $FB > 1 \Leftrightarrow P(H_1 | \text{dados}) > P(H_0 | \text{dados})$
* **4.7.6 Escalas nominais para $FB_{10}$:** Fraco, Médio, Forte, Decisivo
* **4.7.7 Escala Intervalar ou métrica:** $FB$ como uma medida calibrada de performance
* **4.7.8 Jurimetria** como uma metódica de calibração de medidas aproximativas de constructos conceituais acerca do Fenômeno Jurídico

---

## 5 MODELOS: uma simplificação explicativa

* **5.1) Aditivos:** $y_i = f(x_i) + \epsilon_i$
* **5.2) Interações:** $Y = \beta_1 X_1 + \beta_2 X_2 + \beta_3 X_1 X_2 + \epsilon_{1,2,1.2}$
* **5.3) Busca pela Normalidade dos Resíduos ("Erros"):** $N(\mu=0, \sigma=cte)$
* **5.4) Comparação**
* **5.5) Seleção**
* **5.6) Espécies:** standards reconhecidos

---

## 6 ASSUNÇÕES: pressupostos a verificar nos dados para uso adequado dos Modelos

---

## 7 DADOS: Válidos, Fidedignos, Replicáveis e Triangularizáveis (atualizáveis)

* **7.1) Coleta:** a origem
* **7.2) Válidos:** contagens ou métricas
  * **7.2.1) Validade Interna: Escalas de Medida**
    * **a) Nominal ou Categórica:**
      * a.1) Binomial / Booleana
      * a.2) Multinomial
    * **b) Ordinal ou por postos**
    * **c) Intervalar**
    * **d) De Razão**
  * **7.2.2) Validade Externa:** Tipos de Amostragem
* **7.3) Fidedignos**
  * **7.3.1** Não Viesados
  * **7.3.2** Precisão
  * **7.3.3** Repetição de Medidas e Consistência
* **7.4) Replicabilidade**
* **7.5) Atualizáveis:** Triangulação ou verificação dos dados por diferentes pesquisadores e diversificados métodos com novos dados.
