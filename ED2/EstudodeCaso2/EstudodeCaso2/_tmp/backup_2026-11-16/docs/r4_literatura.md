# Revisão de métodos — Análise de sobrevivência da duração de processos no 4º JEC de Natal/RN

**Escopo do caso.** 943 processos distribuídos entre jan. e ago. de 2026, em três grupos procedimentais: (G1) audiência de conciliação presencial obrigatória, (G2) audiência remota e (G3) rito atual com audiência facultativa. Tempo T = dias da distribuição até a sentença. Cerca de 22% dos processos seguiam ativos na data de extração, o que configura censura à direita administrativa. Tipos de desfecho: acordo homologado, julgamento de mérito, extinção sem mérito e "Decisão" (redistribuição a outro juízo). Covariáveis: grupo, audiência híbrida (s/n), acordo em audiência, acordo fora de audiência, técnica de conciliação (6 categorias, só existe quando há audiência) e mês/ordem de distribuição.

**Ambiente verificado** (`C:\Users\MPGO\AulaCleuler\.venv`): lifelines **0.30.0**, statsmodels **0.15.0**, scikit-learn 1.9.0. **O scikit-survival não está instalado.** O módulo `lifelines.statistics` expõe `logrank_test`, `multivariate_logrank_test`, `pairwise_logrank_test`, `survival_difference_at_fixed_point_in_time_test`, `proportional_hazard_test`, `difference_of_restricted_mean_survival_time_test`, `power_under_cph` e `sample_size_necessary_under_cph`. Os fitters disponíveis incluem `KaplanMeierFitter`, `NelsonAalenFitter`, `AalenJohansenFitter`, `CoxPHFitter`, `CoxTimeVaryingFitter`, `WeibullAFTFitter`, `LogNormalAFTFitter`, `LogLogisticAFTFitter`, `GeneralizedGammaFitter`/`GeneralizedGammaRegressionFitter`, `PiecewiseExponential*` e `AalenAdditiveFitter`.

**Observação sobre as fontes.** O PDF de Colosimo e Giolo é digitalização com duas páginas do livro por página do PDF (página do livro ≈ 2 × página do PDF − 20). Os capítulos de Artes e Barroso também são digitalizações. O arquivo "Estatistica-CDados-cap7" é, na verdade, o livro inteiro de Morettin e Singer (versão preliminar de abr. 2021), com página impressa = página do PDF − 10. As páginas citadas abaixo são as **páginas impressas** dos livros.

---

## 0. Decisões de desenho antes de qualquer teste

1. **Origem e evento.** A origem é a data de distribuição. O evento principal é a primeira sentença, de qualquer tipo. A resposta é o par (T, δ), com δ = 1 para falha e δ = 0 para censura (MORETTIN; SINGER, 2021, p. 243-244; COLOSIMO; GIOLO, 2006, p. 6-12). Aqui a "falha" tem conotação positiva, porque é o encerramento. Logo, S(t) = P(processo ainda sem sentença após t dias), e uma razão de riscos (HR) > 1 significa um rito **mais rápido**. Vale deixar isso explícito em todas as tabelas.
2. **Censura.** A censura é administrativa (tipo I com entrada escalonada, ou seja, censura aleatória: COLOSIMO; GIOLO, 2006, p. 8-11, fig. 1.1). Os métodos supõem censura **não informativa**. Essa hipótese é plausível para a data de corte, mas não vale para a redistribuição (ver item 3). Como a entrada vai de janeiro a agosto, o seguimento máximo cai com o mês de distribuição. Por isso, o **mês de distribuição deve entrar como covariável ou estrato**: os grupos podem ter sido implantados em períodos diferentes, e há tendência de calendário (pauta, recesso, férias).
3. **Redistribuição ("Decisão") é risco competitivo, não censura.** O processo sai do 4º JEC e nunca terá sentença ali. Se for tratada como censura, o 1 − KM **superestima** a probabilidade acumulada de sentença. Duas leituras são aceitáveis: (a) evento = sentença, com redistribuição como risco competitivo (Aalen-Johansen ou Cox causa-específico); (b) análise de sensibilidade excluindo os redistribuídos, que costumam ser declinações de competência logo no início. Os livros de referência **não tratam de riscos competitivos**: Colosimo e Giolo cobrem censura, truncamento, censura intervalar e fragilidade, mas não a função de incidência acumulada (FIA). Por isso, cite Fine e Gray (1999), Putter, Fiocco e Geskus (2007) e Aalen e Johansen (1978).
4. **As covariáveis "acordo em audiência" e "acordo fora de audiência" não são basais.** Elas ocorrem durante o seguimento e definem o tipo de desfecho. Usá-las como covariáveis fixas no Cox cria viés de tempo imortal e condiciona no futuro. Há três tratamentos corretos: (i) tratá-las como **tipo de desfecho** (acordo homologado vs. mérito vs. sem mérito, em riscos competitivos); (ii) usar a data da audiência como **covariável dependente do tempo** (`CoxTimeVaryingFitter`; COLOSIMO; GIOLO, 2006, p. 202-204); (iii) deixá-las de fora quando o alvo é o efeito total do grupo.
5. **Técnica de conciliação e audiência híbrida** só existem quando há audiência, ou seja, em G1, em G2 e na parte de G3 que teve audiência. Analise-as **dentro do subconjunto com audiência** (Cox ou logit restritos) ou crie a categoria "sem audiência", sabendo que ela é colinear com o grupo. Não as coloque no mesmo modelo que o grupo sem esse cuidado.
6. **Empates.** Como o tempo é medido em dias, haverá muitos empates. A verossimilhança parcial supõe tempo contínuo (COLOSIMO; GIOLO, 2006, p. 161). A aproximação de Breslow (eq. 5.8) é adequada quando há poucos empates. Efron (1977) é melhor, e com muitos empates usam-se modelos discretos (p. 162; cap. 8, p. 264-270). O `CoxPHFitter` do lifelines usa **Efron**. No statsmodels, use `PHReg(..., ties="efron")`, já que o padrão é "breslow".

---

## 1. Descrição não paramétrica

### 1.1 Kaplan-Meier (KM) e intervalos de confiança
- Estimador: Ŝ(t) = ∏_{j: t_j<t} (1 − d_j/n_j) (COLOSIMO; GIOLO, 2006, eq. 2.6, p. 37; MORETTIN; SINGER, 2021, p. 247-248).
- Variância de Greenwood: Var[Ŝ(t)] = Ŝ(t)² Σ d_j / [n_j(n_j − d_j)] (COLOSIMO; GIOLO, 2006, eq. 2.7, p. 41).
- O IC "plain" Ŝ ± z·EP pode sair de [0,1] nos extremos. O recomendado é o IC pela transformação Û = log[−log Ŝ(t)], que dá [Ŝ(t)]^{exp(±z√Var(Û))} (eq. 2.8, p. 41-42). Esse é o IC log-log, o "exponential Greenwood" que o **lifelines usa por padrão**.
- Propriedades: o estimador é não viciado em amostras grandes, consistente, assintoticamente gaussiano e de máxima verossimilhança (p. 40).
- Python: `KaplanMeierFitter().fit(T, E, label=g)`, com `.plot_survival_function(at_risk_counts=True)` ou `lifelines.plotting.add_at_risk_counts`. Para a curva de "proporção já sentenciada", use `.plot_cumulative_density()`.

### 1.2 Nelson-Aalen
- Λ̃(t) = Σ d_j/n_j, com Var = Σ d_j/n_j² (eq. 2.9-2.10, p. 43). A variância de Aalen é preferível à de Klein por ter menor vício (p. 44).
- S̃(t) = exp{−Λ̃(t)}, com S̃ ≥ Ŝ em todo t (p. 44).
- Uso no caso: gráficos de Λ(t) para diagnosticar a forma do risco e escolher o modelo paramétrico (p. 45; p. 96-99).
- Python: `NelsonAalenFitter`.

### 1.3 Mediana, quantis e tempo médio restrito
- Mediana: t̂_0,5 = inf{t: Ŝ(t) ≤ 0,5} (MORETTIN; SINGER, 2021, p. 248). Colosimo e Giolo recomendam interpolação linear entre os degraus (p. 49).
- Var(t̂_p) = Var(Ŝ(t̂_p))/f(t̂_p)² é inviável por causa de f. A alternativa é o IC de Brookmeyer e Crowley (1982), que inverte um teste (p. 49-50).
- Python: `median_survival_times(kmf)` e `median_survival_times(kmf.confidence_interval_)`. O lifelines obtém o IC da mediana invertendo as bandas pontuais, o que é próximo de Brookmeyer-Crowley. Para outros quantis, use `kmf.percentile(p)`.
- **Tempo médio.** t_m = ∫S(t)dt (p. 24; p. 50). Com censura na cauda, a média fica **subestimada** e "deve ser interpretada com cautela ou evitada" (p. 50). A saída é o **RMST** (tempo médio restrito a τ), μ_τ = ∫_0^τ S(t)dt, estimado pela área sob o KM (MORETTIN; SINGER, 2021, p. 248, com variância na mesma página).
- Python: `restricted_mean_survival_time(kmf, t=τ, return_variance=True)`, `difference_of_restricted_mean_survival_time_test(kmf1, kmf2, t=τ)` e `rmst_plot`.
- **Escolha de τ.** Use o menor dos seguimentos máximos dos grupos, ou um horizonte de gestão (90 ou 120 dias). Interpretação: "em média, nos primeiros τ dias, o processo do grupo A permaneceu X dias a menos sem sentença".
- Vida média residual: vmr(t) = ∫_t^∞ S(u)du / S(t) (p. 24-25; p. 51).

---

## 2. Comparação de curvas (testes de k amostras)

### 2.1 Log-rank e família ponderada
- Teste para dois grupos: T = [Σ(d_2j − w_2j)]² / Σ(V_j)_2, com w_2j = n_2j d_j/n_j e (V_j)_2 = n_2j(n_j − n_2j)d_j(n_j − d_j)/[n_j²(n_j − 1)], distribuído como χ²_1 (COLOSIMO; GIOLO, 2006, eq. 2.12, p. 56-57; MORETTIN; SINGER, 2021, p. 253).
- Para r grupos: T = v′V⁻¹v ~ χ²_{r−1} (eq. 2.13, p. 58-59). No caso são 3 grupos, logo 2 g.l.
- Forma geral ponderada: S = [Σu_j(d_2j − w_2j)]² / Σu_j²(V_j)_2 (eq. 2.14, p. 61). Os pesos:
  - log-rank: u_j = 1;
  - Wilcoxon/Gehan-Breslow: u_j = n_j;
  - Tarone-Ware: u_j = √n_j;
  - Peto-Prentice: u_j = S̃(t_{j−1}) n_j/(n_j + 1);
  - Harrington-Fleming: u_j = [Ŝ(t_{j−1})]^ρ (eq. 2.15, p. 62). Com ρ = 0 obtém-se o log-rank e com ρ = 1 algo próximo do Wilcoxon (p. 63).
- **Recomendações práticas (p. 55; 62-63):**
  - O log-rank é o mais indicado quando a razão de riscos é aproximadamente constante (riscos proporcionais).
  - O Wilcoxon pesa mais o início do seguimento. Use-o se a diferença esperada é precoce, como no efeito imediato de acordo na audiência inicial.
  - O log-rank pesa igualmente todo o eixo, e Tarone-Ware fica no meio-termo.
  - Peto-Prentice e Harrington-Fleming ponderam pela sobrevivência anterior e, ao contrário do Wilcoxon, não dependem do padrão de censura. Isso pesa aqui, porque **a censura difere entre os grupos e entre os meses**: prefira Peto ou FH a Gehan.
  - **Quando as curvas ou os riscos se cruzam** (por exemplo, G1 encerra mais cedo os casos com acordo, mas o restante demora mais), o log-rank perde poder porque diferenças de sinais opostos se cancelam. Reporte também: Wilcoxon/Peto ou FH(1,0) para diferença precoce; FH(0,1) para diferença tardia (Fleming e Harrington, 1991); o teste em ponto fixo; e a **diferença de RMST**, que não exige riscos proporcionais.
  - Pré-especifique o teste principal e trate os demais como sensibilidade.
- **Comparações múltiplas.** Use log-rank par a par com Bonferroni (α/3 = 0,017 para três pares) (COLOSIMO; GIOLO, 2006, p. 59-61).
- Python (lifelines 0.30):
  - `multivariate_logrank_test(T, grupo, E, weightings=None|"wilcoxon"|"tarone-ware"|"peto"|"fleming-harrington", p=..., q=...)`;
  - `pairwise_logrank_test(T, grupo, E, weightings=...)` (aplique Bonferroni à mão);
  - `logrank_test(TA, TB, EA, EB, weightings=...)`;
  - `survival_difference_at_fixed_point_in_time_test(t0, kmfA, kmfB)` (ex.: t0 = 60 ou 90 dias).
- **Log-rank estratificado** (ex.: por mês de distribuição): o lifelines não oferece. Use `statsmodels.duration.survfunc.survdiff(time, status, group, weight_type=None|"gb"|"tw"|"fh", fh_p=..., strata=mes)`, ou um Cox estratificado com o escore como teste.
- **Teste de tendência** (para a ordem ou o mês de distribuição, ou para uma ordenação a priori dos grupos): ajuste um Cox com o escore ordinal como covariável contínua. O teste escore desse modelo é o teste de tendência do log-rank. O log-rank coincide com o teste escore do Cox (COLOSIMO; GIOLO, 2006, p. 56; ex. 1e, p. 199; MORETTIN; SINGER, 2021, p. 255).

---

## 3. Modelos paramétricos e AFT

- **Distribuições** (COLOSIMO; GIOLO, 2006, cap. 3):
  - exponencial (risco constante; p. 70);
  - Weibull (risco monótono; p. 72);
  - log-normal e log-logística (risco que sobe e depois desce; p. 75-79);
  - gama generalizada (p. 79-81), que contém as anteriores como casos particulares.
  - Morettin e Singer (2021, p. 246, fig. 7.4) resumem a correspondência entre forma do risco e modelo.
- **Seleção gráfica** (p. 96-99):
  - (i) Ŝ_KM(t) contra Ŝ_modelo(t): os pontos devem ficar perto da reta y = x;
  - (ii) linearizações: −log Ŝ × t (exponencial, reta pela origem); log[−log Ŝ] × log t (Weibull); Φ⁻¹(1 − Ŝ) × log t (log-normal); log[(1 − Ŝ)/Ŝ] × log t (log-logística).
- **Seleção formal.** Use a razão de verossimilhanças com modelos encaixados na gama generalizada: TRV = 2[log L(θ̂_G) − log L(θ̂_M)] ~ χ² com g.l. igual à diferença de parâmetros (p. 93-94; 100-101). Para modelos não encaixados, como log-normal contra log-logística, use AIC.
- **AFT:** log T = α + x′β + σν; T = exp{x′β}·exp{σν}. As covariáveis aceleram ou desaceleram o tempo, e exp(β) é a **razão de tempos** (COLOSIMO; GIOLO, 2006, eq. 4.10, p. 122; interpretação na seção 4.4, p. 127-129; MORETTIN; SINGER, 2021, p. 254-255, tab. 7.6). Exemplo de leitura: exp(β) = 0,82 significa tempo mediano 18% menor.
  - A Weibull é o único modelo que é ao mesmo tempo AFT e de riscos proporcionais (COLOSIMO; GIOLO, 2006, p. 198).
  - **No caso, o AFT com razão de tempos é provavelmente a apresentação mais intuitiva para gestores** ("o rito X reduz em k% o tempo até a sentença").
- **Diagnóstico** (COLOSIMO; GIOLO, 2006, seção 4.3, p. 123-127):
  - Cox-Snell: ê_i = Λ̂(t_i|x_i). O KM de ê deve acompanhar a Exp(1), e Λ̂(ê) × ê deve ser uma reta de inclinação 1 (eq. 4.11, p. 124). Esse resíduo mede o ajuste global, mas não mostra o tipo de falha (p. 125).
  - Padronizados: ν̂ = (log t − x′β̂)/σ̂ (eq. 4.12, p. 125).
  - Martingal: m̂_i = δ_i − ê_i, para a forma funcional (p. 126-127). No caso, a ordem de distribuição.
  - Deviance: d̂_i = sinal(m̂)[−2(m̂ + δ log(δ − m̂))]^{1/2}, mais simétrico e usado para outliers (eq. 4.14, p. 127).
- Python:
  - ajuste univariado e QQ: `WeibullFitter`, `LogNormalFitter`, `LogLogisticFitter`, `ExponentialFitter`, `GeneralizedGammaFitter` + `lifelines.plotting.qq_plot`;
  - comparação: `.log_likelihood_`, `.AIC_`;
  - regressão: `WeibullAFTFitter().fit(df, "T", "E", formula="C(grupo)+C(mes)")`, `LogNormalAFTFitter`, `LogLogisticAFTFitter`, `GeneralizedGammaRegressionFitter`. O `print_summary()` mostra exp(coef) como razão de tempos.

---

## 4. Modelo de Cox

- **Modelo:** λ(t|x) = λ_0(t)exp(x′β) (COLOSIMO; GIOLO, 2006, cap. 5; MORETTIN; SINGER, 2021, p. 255).
  - Verossimilhança parcial: L(β) = ∏[exp(x_i′β)/Σ_{R(t_i)}exp(x_j′β)]^{δ_i} (eq. 5.6, p. 161).
  - Empates: ver item 0.6 (p. 161-162).
  - As propriedades assintóticas permitem os testes de Wald, RV e escore (p. 162).
- **Interpretação** (p. 162-164). exp(β_l) é a razão de riscos constante no tempo. Para um fator de 3 níveis, use indicadoras com uma categoria de referência; o livro traz exemplo de grupo controle e dois tratamentos com IC por método delta (p. 163-164). No caso, sugere-se **G3 (rito atual) como referência**. HR > 1 indica sentença mais rápida.
- **Funções de base:**
  - Breslow: Λ̂_0(t) = Σ d_j / Σ_{R_j} exp(x_l′β̂) (eq. 5.9, p. 165);
  - Ŝ(t|x) = [Ŝ_0(t)]^{exp(x′β̂)} (p. 164-165), útil para curvas ajustadas por grupo e percentis.
- **Adequação (seção 5.6, p. 165-175):**
  - Ajuste global por Cox-Snell (p. 166). **Não** use esse resíduo para avaliar riscos proporcionais.
  - **Riscos proporcionais, método gráfico** (p. 167): curvas de log Λ̂_0j(t) × t ou log t por estrato devem ser paralelas. É o gráfico log(−log Ŝ). Agrupe as covariáveis contínuas. O método é subjetivo.
  - **Resíduos de Schoenfeld padronizados** (eq. 5.10, p. 167-169): o gráfico de s*_iq + β̂_q × g(t) com spline deve ser horizontal (Grambsch e Therneau, 1994).
  - **Teste**, global e por covariável: T_q = d(Σ(g_k − ḡ)s*_qk)² / [I_q⁻¹ Σ(g_k − ḡ)²] ~ χ²_1, e o global ~ χ²_p (p. 169-170). Pode-se usar a correlação ρ entre resíduos e g(t). As opções de g(t) são t, log t, rank e km; "na prática há pouca diferença", e km é o padrão do R (p. 170).
  - **Covariável dependente do tempo** (x·t, Cox, 1979) como teste e como modelo (p. 170-172, fig. 5.3): HR(t) = exp(β_1 + β_2 t).
  - **Martingal** × covariável para a forma funcional (ordem ou mês de distribuição) e **deviance** × preditor linear para outliers (eq. 5.11, p. 172-173). Para influência, use dfbeta/jackknife (p. 173).
- **Quando os riscos proporcionais falham:**
  - (a) **Cox estratificado** por estrato da covariável que viola a hipótese, com β comum (eq. 6.2-6.3, p. 204-206). A homogeneidade dos β entre estratos é testada por TRV com (m − 1)p g.l. (p. 205-206). Estratifique só quando necessário, porque há perda de eficiência (p. 206). Sem estimativa de efeito para a variável estratificadora, essa solução **serve para o mês, não para o grupo**, que é a variável de interesse.
  - (b) **Coeficiente variando no tempo**: termo grupo × g(t) ou partição do eixo em janelas (ex.: 0-60 e >60 dias), com HR por janela. Exige `CoxTimeVaryingFitter` com dados no formato contagem (episódios). Para corte em janelas, use `lifelines.utils.to_episodic_format` ou `add_covariate_to_timeline`.
  - (c) Partições do eixo e modelos por intervalo (MORETTIN; SINGER, 2021, p. 256, nota 2).
  - (d) **AFT ou RMST** como medidas alternativas.
- Python:
  - `cph = CoxPHFitter(); cph.fit(df, "T", "E", formula="C(grupo, Treatment('G3')) + mes", strata=[...])`;
  - `cph.print_summary()`, com HR = exp(coef) e IC 95%;
  - `cph.check_assumptions(df, p_value_threshold=0.05, show_plots=True)`, que gera os resíduos de Schoenfeld padronizados com bootstrap e as recomendações;
  - `proportional_hazard_test(cph, df, time_transform=["rank","km","log","identity"])`;
  - `cph.compute_residuals(df, kind="schoenfeld"|"scaled_schoenfeld"|"martingale"|"deviance"|"delta_beta"|"score")`;
  - `cph.plot_partial_effects_on_outcome("grupo", values=[...])`;
  - `kmf.plot_loglogs()` ou `lifelines.plotting.loglogs_plot` para o gráfico log(−log S);
  - `cph.concordance_index_` e `cph.AIC_partial_`.
  - Robustez: `robust=True`. Se houver cluster por conciliador, use `cluster_col`.
  - Equivalente em statsmodels: `PHReg(endog, exog, status, strata=..., ties="efron")`.

---

## 5. Riscos competitivos (desfechos múltiplos e redistribuição)

*Este tema não está nos livros de referência. Use a literatura complementar indicada na seção de referências.*

- **Quantidade descritiva: função de incidência acumulada (FIA)** de cada causa k, F_k(t) = P(T ≤ t, causa = k), estimada por **Aalen-Johansen**: F̂_k(t) = Σ_{t_j≤t} Ŝ(t_{j−1}) d_kj/n_j. A soma das FIA mais Ŝ_global é igual a 1. **Não use 1 − KM** censurando as outras causas, porque isso superestima. No caso, há uma FIA para "acordo homologado", uma para "mérito", uma para "sem mérito" e uma para "redistribuição", por grupo, em gráfico empilhado.
  - Python: `AalenJohansenFitter(seed=0).fit(T, causa, event_of_interest=k)`. O lifelines introduz *jitter* nos tempos empatados (`jitter_level=1e-4`), então fixe o `seed`. Alternativa sem jitter: `statsmodels.duration.survfunc.CumIncidenceRight(time, status)`, com status ∈ {0, 1, …, K}.
- **Teste de Gray (k amostras para FIA):** não existe no lifelines nem no statsmodels. Há três alternativas:
  - pacotes PyPI **`pycmprsk`** (porte do `cmprsk` do R; GPL) ou **`pycrr`** (`gray_test`), que não estão instalados;
  - `rpy2` + `cmprsk::cuminc`;
  - aproximação pragmática: log-rank **causa-específico** (censurando as outras causas) com `multivariate_logrank_test`. Ele testa o risco causa-específico, não a FIA. Diga isso no texto.
- **Regressão:**
  - **Cox causa-específico** (recomendado como análise principal "etiológica"): `CoxPHFitter` com E_k = 1{causa = k}, tratando as outras causas como censura. Interpretação: efeito do grupo sobre a taxa instantânea de, por exemplo, acordos entre os processos ainda em curso.
  - **Fine-Gray (subdistribuição)**, para efeito sobre a FIA (prognóstico ou gestão). Não está no lifelines, no statsmodels nem no scikit-survival (este último faz FIA não paramétrica, mas não regressão). Opções: `pycmprsk`/`pycrr`, o pacote `comprisk` (arXiv 2607.09431, 2026), `rpy2` + `cmprsk::crr` ou `survival::finegray`. Outra via é fazer a ponderação IPCW de Geskus (2011) à mão e passá-la a `CoxPHFitter(weights_col=..., robust=True)` em formato contagem.
  - Recomendação (Putter, Fiocco e Geskus, 2007; Austin, Lee e Fine, 2016): reporte **ambos**, causa-específico para a pergunta "o rito acelera os acordos?" e FIA/Fine-Gray para "que fração dos processos termina em acordo até t?".

---

## 6. Regressão logística (desfecho binário: acordo sim/não)

- **Modelo:** π(x) = exp(β_0 + x′β)/[1 + exp(β_0 + x′β)], ou seja, logit π = β_0 + x′β (ARTES; BARROSO, 2023, eq. 10.1-10.2, p. 357). exp(β_j) é a **razão de chances** para o aumento de uma unidade, com as demais covariáveis fixas; para variável binária, é a RC entre presença e ausência (eq. 10.3, p. 358). Estimação por máxima verossimilhança (p. 358). Ver também Morettin e Singer (2021, seção 6.5, p. 218-224; seção 8.2, p. 264-272).
- **Hosmer-Lemeshow:** ordenar por π̂, formar g grupos (em geral 10) e calcular HL = Σ(O_k − n_k π̄_k)²/[n_k π̄_k(1 − π̄_k)] ~ χ²_{g−2} (eq. 10.4, p. 358-359).
- **Classificação:** separe amostras de desenvolvimento e validação (20-30% para validação, p. 359). Calcule sensibilidade S(τ), especificidade E(τ), taxas de falsos positivos e negativos e VPP/VPN (p. 361-363). A curva ROC dá AUROC = A + 0,5 e o índice de Gini IG = 2·AUROC − 1 (p. 364). **Referências de leitura** (Hosmer, Lemeshow e Sturdivant): AUROC 0,5 = sem discriminação; 0,5-0,7 pobre; 0,7-0,8 aceitável; 0,8-0,9 excelente; ≥ 0,9 excepcional (tab. 10.3, p. 365). A estatística KS é a distância máxima entre as FDAs dos escores dos dois grupos (eq. 10.5, p. 365-367).
- **Cuidado com censura.** Com 22% de processos ativos, um logit de "acordo" sobre todos os processos trata os ativos como "não acordo". Há três saídas:
  - (i) restringir aos processos com seguimento ≥ τ e definir Y = acordo até τ;
  - (ii) restringir aos processos com audiência realizada, com Y = acordo na audiência. Esse é o uso natural do logit para **técnica de conciliação** e **audiência híbrida**;
  - (iii) preferir a FIA ou o Fine-Gray.
- Python:
  - `statsmodels.formula.api.logit("acordo ~ C(grupo) + C(tecnica) + hibrida + mes", df).fit()`;
  - `np.exp(res.params)` e `np.exp(res.conf_int())` para RC e IC;
  - `sklearn.metrics.roc_auc_score` e `roc_curve`;
  - HL feito à mão com `pd.qcut` e `scipy.stats.chi2`;
  - com 6 técnicas e poucos eventos por célula, verifique separação; se necessário, use logit penalizado (Firth) ou agrupe categorias.

---

## 7. Árvores de decisão

- **CART/AID/CHAID:** o objetivo é particionar os dados em grupos homogêneos quanto à resposta (ARTES; BARROSO, 2023, cap. 11, p. 377-378; MORETTIN; SINGER, 2021, cap. 10, p. 319-343). A melhor partição maximiza |p_j1 − p_j0| ou o χ² de homogeneidade (p. 379-382, tab. 11.1-11.2).
  - Partições livres para variáveis nominais (técnica de conciliação) e monotônicas para ordinais (mês ou ordem) (p. 390).
  - **Poda** por custo-complexidade: C_α(A) = SQ(A) + α·n_A, com α como parâmetro de afinação (p. 395-396).
  - Critérios de parada: diferença mínima, SQD, F/χ² com p-valor corrigido por Bonferroni (10%/k no nível k), AIC/BIC para partições politômicas (seção 11.5.2, p. 400-401).
  - Bagging e floresta aleatória, avaliados por EQM, EAM e EAMR na amostra de validação (p. 405-407).
- **Uso no caso:** árvore de classificação para o tipo de desfecho ou para "acordo" no subconjunto com audiência (`sklearn.tree.DecisionTreeClassifier(ccp_alpha=...)`, com `cost_complexity_pruning_path` e validação cruzada). É uma ferramenta **exploratória** de interações (técnica × híbrida × grupo), não inferencial.
- **Árvores de sobrevivência** (LeBlanc e Crowley, 1993; floresta aleatória de sobrevivência de Ishwaran et al., 2008) **não estão nos livros**. Em Python: `sksurv.tree.SurvivalTree` e `sksurv.ensemble.RandomSurvivalForest`, que exigem instalar o scikit-survival (`uv add scikit-survival`). Sem instalar nada, a aproximação é uma árvore de regressão sobre os resíduos martingal de um Cox nulo (Therneau, Grambsch e Fleming, 1990).

---

## 8. Ordem sugerida de análise (roteiro do notebook)

1. Construir (T, δ, causa) e checar: datas inconsistentes, T = 0, sentença antes da distribuição, redistribuições precoces.
2. Descrever o tamanho dos grupos, o % de censura por grupo e por mês e o seguimento mediano. O seguimento mediano se obtém pelo KM reverso: `KaplanMeierFitter().fit(T, 1 - E)`.
3. KM por grupo com IC log-log e tabela de risco. Mediana com IC, quartis e RMST(τ) por grupo.
4. Log-rank para 3 grupos (2 g.l.). Wilcoxon/Peto/FH como sensibilidade. Pares com Bonferroni. Teste em t fixo (60 ou 90 dias). Diferença de RMST. Log-rank estratificado por mês (statsmodels).
5. Gráfico log(−log Ŝ) × log t por grupo. Se as curvas forem paralelas, o Cox está indicado; se forem retas paralelas, Weibull.
6. Cox: grupo (referência G3) + mês, com Efron. `check_assumptions` e teste de Schoenfeld. Martingal para a forma funcional da ordem ou do mês. Deviance e dfbeta. Se faltar proporcionalidade no grupo, use HR por janela de tempo ou grupo × log t. Se faltar no mês, estratifique por mês.
7. Paramétrico e AFT: escolha da distribuição por gráficos e por TRV na gama generalizada ou AIC. Razões de tempos por grupo. Cox-Snell.
8. Riscos competitivos: FIA de Aalen-Johansen por causa e grupo. Cox causa-específico para acordo e para mérito. Fine-Gray e Gray via `pycmprsk`/R, se disponíveis.
9. Subconjunto com audiência: logit (acordo na audiência ~ técnica + híbrida + grupo + mês) com RC, HL, AUC e KS. Árvore exploratória.
10. Sensibilidade: excluir redistribuídos; truncar em τ comum; usar só os meses com seguimento ≥ 90 dias.

---

## 9. Validade externa e extensão aos 14 JECs de Natal

- **Referências empíricas.** O diagnóstico CNJ/Ipea dos JECs (2013) fez campo no AP, no CE e no RJ e descreveu perfis distintos dos juizados e das centrais de conciliação (Res. CNJ 125/2010). O CNJ divulgou um diagnóstico posterior dos juizados (2015 vs. 2019), e há registro de espera média de 168 dias até a primeira audiência e de baixa taxa de acordo. O Justiça em Números 2026 (ano-base 2025) informa tempo médio geral de julgamento de 2 anos e 4 meses, sem recorte de JEC na fonte consultada. **Busque o tempo de JEC estadual 1º grau/conhecimento no painel do CNJ**, que não confirmei. Há trabalhos brasileiros de jurimetria com KM e Cox sobre duração processual: TCC da UEPB (mediana de 521 dias até a sentença), dissertação da UnB (2024) sobre precatórios e estudo da Justiça Militar que combina árvore e duração. Nenhum desses é sobre JEC com Cox, o que é uma **lacuna** que este estudo ocupa.
- **Ameaças à validade externa:**
  - um único juízo (efeito de juiz, servidores e conciliadores);
  - distribuição em período curto (sazonalidade, recesso de julho, curva de aprendizado do rito);
  - alocação dos grupos possivelmente não aleatória: verifique se o grupo dependia da data ou da ordem de distribuição. Se a regra for determinística, por exemplo por paridade do número, é quase experimental; se for por período, há confusão com calendário;
  - seguimento curto (≤ 10 meses): a cauda e a média não são estimáveis, então use RMST(τ).
- **Extensão via DataJud.** O endpoint é `POST https://api-publica.datajud.cnj.jus.br/api_publica_tjrn/_search` com cabeçalho `Authorization: APIKey <chave pública do CNJ>`. É o mesmo padrão do coletor já existente em `C:\Users\MPGO\AulaCleuler\EstudodeCaso1\src\coleta_datajud.py`, que usa TJGO: basta trocar o alias para `tjrn`. A paginação é por `search_after` com `sort` em `@timestamp`. Filtre `classe.codigo = 436` (Procedimento do Juizado Especial Cível, TPU/CNJ), `orgaoJulgador.codigoMunicipioIBGE = 2408102` (Natal) ou o nome/código do órgão dos 14 JECs, e `dataAjuizamento` no período.
  - Os movimentos (`movimentos.codigo`/`nome`/`dataHora`) permitem reconstruir distribuição, audiência de conciliação (movimento 970 / "Audiência ... realizada"), homologação de acordo (466), julgamento com resolução de mérito (procedência 219, improcedência 220, parcial 221) e extinção sem mérito (família 457). **Confirme os códigos na TPU do CNJ.** A redistribuição tem movimento próprio (36).
  - **Modelo multicentro:** Cox **estratificado por juizado** (`strata="juizado"`) ou com fragilidade compartilhada por vara (COLOSIMO; GIOLO, 2006, cap. 9, p. 281-317, fragilidade gama, p. 292-301). Também é possível usar variância robusta com `cluster_col="juizado"`. Isso permite comparar o 4º JEC com os outros 13 e testar heterogeneidade do efeito do rito.

---

## Referências (ABNT)

AALEN, O. O.; JOHANSEN, S. An empirical transition matrix for non-homogeneous Markov chains based on censored observations. **Scandinavian Journal of Statistics**, v. 5, n. 3, p. 141-150, 1978.

ARTES, R.; BARROSO, L. P. **Métodos multivariados de análise estatística**. São Paulo: Blucher, 2023. (Cap. 10, Classificação com regressão logística, p. 355-376; cap. 11, Árvores de decisão, p. 377-420.)

AUSTIN, P. C.; LEE, D. S.; FINE, J. P. Introduction to the analysis of survival data in the presence of competing risks. **Circulation**, v. 133, n. 6, p. 601-609, 2016.

BRASIL. Conselho Nacional de Justiça. **Justiça em Números 2026**: ano-base 2025. Brasília: CNJ, 2026. Disponível em: https://www.cnj.jus.br/pesquisas-judiciarias/justica-em-numeros/. Acesso em: 12 nov. 2026.

BRASIL. Conselho Nacional de Justiça. **API Pública do DataJud**: documentação. Brasília: CNJ, [2023]. Disponível em: https://datajud-wiki.cnj.jus.br/api-publica/. Acesso em: 12 nov. 2026.

BROOKMEYER, R.; CROWLEY, J. A confidence interval for the median survival time. **Biometrics**, v. 38, n. 1, p. 29-41, 1982.

COLOSIMO, E. A.; GIOLO, S. R. **Análise de sobrevivência aplicada**. São Paulo: Blucher, 2006. (Projeto Fisher.)

COX, D. R. Regression models and life-tables. **Journal of the Royal Statistical Society: Series B**, v. 34, n. 2, p. 187-220, 1972.

DAVIDSON-PILON, C. lifelines: survival analysis in Python. **Journal of Open Source Software**, v. 4, n. 40, p. 1317, 2019. (Versão utilizada: 0.30.0.)

EFRON, B. The efficiency of Cox's likelihood function for censored data. **Journal of the American Statistical Association**, v. 72, n. 359, p. 557-565, 1977.

FINE, J. P.; GRAY, R. J. A proportional hazards model for the subdistribution of a competing risk. **Journal of the American Statistical Association**, v. 94, n. 446, p. 496-509, 1999.

FLEMING, T. R.; HARRINGTON, D. P. **Counting processes and survival analysis**. New York: Wiley, 1991.

GESKUS, R. B. Cause-specific cumulative incidence estimation and the Fine and Gray model under both left truncation and right censoring. **Biometrics**, v. 67, n. 1, p. 39-49, 2011.

GRAMBSCH, P. M.; THERNEAU, T. M. Proportional hazards tests and diagnostics based on weighted residuals. **Biometrika**, v. 81, n. 3, p. 515-526, 1994.

GRAY, R. J. A class of K-sample tests for comparing the cumulative incidence of a competing risk. **The Annals of Statistics**, v. 16, n. 3, p. 1141-1154, 1988.

HOSMER, D. W.; LEMESHOW, S.; STURDIVANT, R. X. **Applied logistic regression**. 3. ed. Hoboken: Wiley, 2013.

INSTITUTO DE PESQUISA ECONÔMICA APLICADA (IPEA). **Diagnóstico sobre os Juizados Especiais Cíveis**: relatório de pesquisa. Brasília: Ipea; CNJ, 2013. Disponível em: https://repositorio.ipea.gov.br/bitstream/11058/7533/1/RP_Diagn%c3%b3stico_2013.pdf. Acesso em: 12 nov. 2026.

KAPLAN, E. L.; MEIER, P. Nonparametric estimation from incomplete observations. **Journal of the American Statistical Association**, v. 53, n. 282, p. 457-481, 1958.

MORETTIN, P. A.; SINGER, J. M. **Estatística e ciência de dados**. Versão preliminar. São Paulo: IME-USP, abr. 2021. (Cap. 6.5, regressão logística, p. 218-224; cap. 7, análise de sobrevivência, p. 243-260; cap. 10, árvores e florestas, p. 319-343.) Publicado em versão final por LTC, Rio de Janeiro, 2022.

PUTTER, H.; FIOCCO, M.; GESKUS, R. B. Tutorial in biostatistics: competing risks and multi-state models. **Statistics in Medicine**, v. 26, n. 11, p. 2389-2430, 2007.

ROYSTON, P.; PARMAR, M. K. B. Restricted mean survival time: an alternative to the hazard ratio for the design and analysis of randomized trials with a time-to-event outcome. **BMC Medical Research Methodology**, v. 13, art. 152, 2013.

SEABOLD, S.; PERKTOLD, J. statsmodels: econometric and statistical modeling with Python. In: PYTHON IN SCIENCE CONFERENCE, 9., 2010, Austin. **Proceedings** [...]. Austin: SciPy, 2010. p. 92-96. (Versão utilizada: 0.15.0.)

THERNEAU, T. M.; GRAMBSCH, P. M. **Modeling survival data**: extending the Cox model. New York: Springer, 2000.

### Fontes web consultadas (busca de 12 nov. 2026)
- pycmprsk (Gray + Fine-Gray em Python): https://pypi.org/project/pycmprsk/
- pycrr (Fine-Gray + gray_test): https://pypi.org/project/pycrr/
- comprisk (arXiv 2607.09431): https://arxiv.org/abs/2607.09431
- insurance-competing-risks (afirma que o lifelines não tem Fine-Gray): https://pypi.org/project/insurance-competing-risks/
- Ipea/CNJ, Diagnóstico JEC 2013: https://repositorio.ipea.gov.br/bitstream/11058/7533/1/RP_Diagn%c3%b3stico_2013.pdf
- CNJ, "Estudo revela realidade e desafios dos Juizados Especiais": https://www.cnj.jus.br/estudo-revela-realidade-e-desafios-dos-juizados-especiais/
- CNJ, "Ipea mostra diferentes perfis de JECs": https://www.cnj.jus.br/ipea-mostra-diferentes-perfis-de-juizados-especiais-civeis/
- Senado, "espera de 168 dias até 1ª audiência": https://www2.senado.leg.br/jspui/bitstream/id/512361/1/noticia.html
- Justiça em Números 2026 (notícia): https://www.correiodamanha.com.br/economia/justica/2026/06/297188-judiciario-encerrou-2025-com-755-milhoes-de-processos-e-recorde-de-acoes.html
- TCC UEPB (KM, mediana de 521 dias): https://dspace.bc.uepb.edu.br/jspui/bitstream/123456789/28013/6/TCC%20-%20Jancer%20Gomes.pdf
- Dissertação UnB (precatórios, sobrevivência): https://www.repositorio.unb.br/bitstream/10482/52609/1/RafaelMonteiroDeCastroNascimento_DISSERT.pdf
- Revista do MPM (árvore + duração, Justiça Militar): https://revista.mpm.mp.br/rmpm/article/download/467/449/1185
- TJAC, edital com "436-Procedimento do Juizado Especial Cível": https://www.tjac.jus.br/wp-content/uploads/2024/05/Edital-Eliminacao-02-2024-2.pdf

*Limitações desta revisão.* A wiki do DataJud retornou HTTP 403, e o endpoint foi inferido do coletor já existente no Estudo de Caso 1. O tempo médio específico de JEC no Justiça em Números não foi localizado. Os códigos de movimento da TPU citados na seção 9 devem ser conferidos.
