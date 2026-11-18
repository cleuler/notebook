# R2 — Leitura crítica do notebook `estcaso_4jec_natal_rn.ipynb` (Estudo de Caso n. 2 — 4º JEC Natal/RN)

Arquivo analisado: `C:\Users\MPGO\AulaCleuler\EstudodeCaso2\estcaso_4jec_natal_rn.ipynb` (56 células, índices 0–55; saídas gravadas em 08/10/2026 numa máquina `e:\DADOS\...`, com `lifelines=False`).
Verificações próprias: a planilha foi relida com o venv (`scripts chk.py/chk2.py` no scratchpad) para confirmar os achados marcados com **[verificado]**.

---

## 1. Estrutura do notebook, seção por seção

| Célula | Seção | O que faz | Variáveis criadas / resultados reportados |
|---|---|---|---|
| 0 | Título/objetivo | Chama de "Estudo de Caso **4**"; afirma que os grupos foram "definidos por **sorteio aleatório** de rito"; promete censura, assimetria, KM. Cita `rafaelcc_ed1.ipynb`/`estcaso_ip.ipynb` como modelos. | — |
| 1 | 1. Tipos de gráficos | Tabela didática (barras/Pareto, histograma+KDE, boxplot, mosaico, dispersão, KM). | — |
| 2–3 | 2. Ambiente | Importa pandas/numpy/scipy/seaborn; `statsmodels` e `lifelines` opcionais; caminhos `BASE/dat/estcaso_4JEC_natal/...`, `BASE/txt/...`, saída `dat/processado`. `warnings.filterwarnings('ignore')`. | `TEM_STATSMODELS=True`, `TEM_LIFELINES=False` (ver erro E1) |
| 4–5 | 3. Leitura DOCX/ODT | Extrai texto via XML (`w:t` no DOCX; `el.text` no ODT) e imprime 1.200 caracteres. | `texto_docx`, `texto_odt` (não são usados depois) |
| 6–7 | 4. Leitura da planilha | `read_excel(header=None)`, cabeçalho = linha índice 1, dados a partir da 2, `dropna(how='all')`. | `raw`, `dados_brutos` (**944 linhas × 15 col.**) |
| 8–9 | 5. Limpeza de rótulos | Dicionário `CORRECOES_COLUNA` p/ *mojibake* (inócuo: os nomes já vêm corretos), `slug_coluna()` → snake_case ASCII; normaliza strings (espaços, `'nan'`→NaN). | `dados`; colunas `numero_do_processo, dt_distribuicao, sorteio, hibrida, teve_acordo_na_ac, tecnica, teve_acordo_fora_da_ac, sentenca, dt_sentenca, duracao_sent2, duracao_tecn, duracao_sort, duracao_proc, duracao_do_processo, status` |
| 10–11 | 6. Categorias | `grupo` = map de `sorteio` → Controle / Tratamento_presencial / Tratamento_remoto; `status_norm`; `sentenca_std = sentenca.str.title()` (unifica "sem julgamento de mérito" em caixa baixa, 11 casos). | grupo 316/314/314; status Encerrado 734, Ativo 209, **NaN 1**; sentença: Mérito 341, Sem mérito 286, NaN 210, Homologação 81, **Decisão 26** |
| 12–13 | 7. Tipagem | datas → datetime; 4 durações → numérico; 7 colunas → `category`; `censura = sentenca_std.isna()`. Cruza censura × status e declara "OK". | `censura` (210 vs. 209 Ativos); describe: as 4 durações com estatísticas **idênticas** (n=943, média 78,5, mediana 80) exceto `duracao_tecn` (n=428, média 105,8) |
| 14–15 | 8. Auditoria | Duplicatas, faltantes, negativas, coerência data×duração (tolerância 2 d). | duplicatas **6**; faltantes `dt_sentenca` 210, `duracao_proc` 1, `status` 1; inconsistência data×duração 0 |
| 16–17 | 9. Exportação | Salva XLSX/CSV "limpos" (944 × 19). | `estcaso_4jec_natal_limpo.xlsx/.csv` |
| 18–19 | 10. Censura/janela | `JANELA_DIAS=218` (do ODT); `evento = (status=='Encerrado')`; proporções por grupo. | censurados 22,2%; "acima_218_dias" 5; % encerrados: Controle 85,4 / Presencial 76,3 / Remota 71,7 |
| 20–22 | 11. Categóricas | `plot_barras_pareto()` para grupo, status, acordo na AC, acordo fora da AC, sentença, técnica, híbrida (inclui NaN e `**` como categorias). | acordo na AC: Sim 17 (1,8%); `tecnica='**'` 515 (54,6%); híbrida Sim 31, NaN 72; acordo fora `**` 1 |
| 23–25 | 12. Quantitativas | `analise_quantitativa()` (dot plot, hist+KDE, boxplot, estatísticas) para as 4 durações. | sent2 = sort = proc: média 78,46, mediana 80, DP 51,2, assimetria 0,30; tecn: média 105,8, mediana 98,5 |
| 26–28 | 13. Comparação por grupo | Boxplots/histogramas de `duracao_proc` por grupo; **Kruskal-Wallis**; post-hoc Mann-Whitney só se p<0,05. | medianas 77 / 84 / 81; **H=1,477, p=0,478** (não rejeita) |
| 29 | 13b. Encerrado × Ativo | Boxplot + **Mann-Whitney**. | Ativo mediana 97 vs Encerrado 72; **U=41437,5, p=3,2e-24** |
| 30–34 | 14. Associação categórica | `analise_associacao()`: crosstab, % por linha, **qui-quadrado**, mosaico. | grupo×status: **χ²=17,55, gl=2, p=0,00015**; grupo×acordo AC: **χ²=9,81, gl=2, p=0,0074**; sentença×grupo: **χ²=36,71, gl=6, p=2,0e-06** |
| 35–38 | 15. Correlação | `matriz_correlacao()` (o texto e o código usam **Spearman**, não Pearson) sobre as 4 durações; dispersões sort×proc e tecn×proc com reta OLS. | todos os pares **r=1,000**; R²=1,000, "p=0" |
| 39–40 | 16. Normalidade | Subamostra aleatória de 500 (seed 42) de `duracao_proc`; Shapiro-Wilk e D'Agostino; Q-Q plot. | SW **W=0,971, p=2,6e-08** (rejeita); D'Agostino **K²=3,09, p=0,213** (não rejeita) |
| 41–42 | 17. Testes de hipótese | Teste z de proporção (H₀: p=0,5 de encerrados); Mann-Whitney duração com × sem acordo na AC. | **z=17,1, p≈0**; MW: n=17 vs 852, medianas 63 vs 81, **U=6477, p=0,456** |
| 43–44 | 18. Ajuste de distribuições | MLE de Log-Normal, Gamma, Weibull, Exponencial em `duracao_proc>0`; AIC/BIC. | Weibull AIC 9585,8 (melhor) < Gamma 9611,6 < LogN 9612,5 < Expon 9753,6 |
| 45–46 | 19. Regressão | OLS `duracao_proc ~ grupo` (dummies, ref. Controle) e Logit `evento ~ grupo`. As durações "intermediárias" anunciadas foram excluídas das preditoras. | OLS: R²=0,001, F p=0,588, coef. presencial +0,51 (p=0,90), remota +3,88 (p=0,34); Durbin-Watson 1,47. Logit: presencial −0,58 (p=0,005), remota −0,83 (p<0,001), pseudo-R² 0,018 |
| 47–48 | 20. Kaplan-Meier | KM por grupo + log-rank par a par — **não executou** (lifelines "indisponível"); fallback: "ECDF" de encerramento por grupo. | só gráfico ECDF (sem IC, sem teste) |
| 49–50 | 21. Janela | Período de distribuição 01/01–03/08/2026 (214 dias), ECDF global com linha em 218, média×mediana por grupo. | mesma tabela 77/84/81 |
| 51–52 | 22. Extensão | Checklist de "prontidão" (todos True exceto lifelines). Comentário sobre merge com DataJud. | — |
| 53–54 | 23. Síntese | Questões norteadoras e resumo automático. | mediana 80, média 78,5, P90 141; % acordos na AC 2,0% |
| 55 | Referências / notas finais | "Lições": censura importa, média≠mediana etc. — as quais o próprio notebook não aplica. | — |

---

## 2. Erros, lacunas e incongruências (com correção)

Legenda de gravidade: **[C]** crítico (muda a conclusão), **[M]** moderado, **[L]** leve/operacional.

### A. Leitura, limpeza e tipagem (cél. 3–17)

**E1 [C] — Kaplan-Meier nunca roda por erro de import (cél. 3 e 48).** `from lifelines import KaplanMeierFitter, logrank_test` falha porque `logrank_test` fica em `lifelines.statistics`. O `except ImportError` mascara o erro e faz `TEM_LIFELINES=False` **mesmo com lifelines instalado** [verificado: lifelines 0.30.0 está no venv; o import falha com `ImportError: cannot import name 'logrank_test'`]. Consequência: a única análise adequada a dados censurados — anunciada como "imprescindível" — não é feita. *Correção:* `from lifelines import KaplanMeierFitter; from lifelines.statistics import logrank_test, multivariate_logrank_test`; não silenciar avisos (`warnings.filterwarnings('ignore')`).

**E2 [M] — Linha "fantasma" mantida (cél. 7, 11, 13, 17).** Há 944 linhas, não 943: o processo `0813782-27.2026.8.20.5004` (29/07/2026, Presencial) só tem número, data e sorteio — todas as demais colunas vazias [verificado]. Ele entra nas contagens de grupo (316), recebe `censura=1` (por isso 210 ≠ 209 Ativos) e `evento=0`, e é exportado no dataset "limpo". A célula 13 imprime "OK — censura alinhada ao status" porque o `crosstab` descarta o NaN. *Correção:* identificar e excluir (ou documentar como perda) linhas sem desfecho; N analítico = 943 (ou menos, após duplicatas).

**E3 [M] — Duplicatas detectadas e não tratadas (cél. 15).** 6 números repetidos (11 linhas) [verificado], p.ex. `0804436-52` aparece 3 vezes (2× Presencial, 1× Controle, todas "Decisão"), `0802424-65` e `0808905-44` aparecem como "Decisão" e depois como "Ativo" — ou seja, o mesmo processo redistribuído/retornado foi **re-sorteado**, às vezes para outro grupo. Isso viola a independência e a unicidade da unidade experimental, e contamina grupos. *Correção:* regra explícita (manter a 1ª entrada / considerar o processo único com o grupo original — intenção de tratar), análise de sensibilidade com e sem duplicatas.

**E4 [M] — Placeholders `**` e "não se aplica" tratados como categoria ou como "Não" (cél. 9, 13, 22, 33).** `tecnica='**'` (515 = todo o Controle + 201 dos tratados), `teve_acordo_fora_da_ac='**'` (1). No Controle, `teve_acordo_na_ac='Não'` em 314/314 e `tecnica='**'` em 314/314 — não houve AC, logo é **"não se aplica" (zero estrutural)**, não "Não". *Correção:* recodificar `**` → NA/"Não se aplica"; distinguir NA estrutural (sem AC) de NA por falta de registro; tabela de faltantes por grupo × variável.

**E5 [L] — Faltantes heterogêneos não diagnosticados.** `hibrida` NA 72 (23 Presencial, 48 Remota, 0 Controle), `teve_acordo_na_ac` NA 75, `teve_acordo_fora_da_ac` NA 207 (quase todos Ativos) [verificado]. Os gráficos de Pareto mostram "NaN" como categoria e os testes simplesmente fazem `dropna()` (análise de casos completos sem justificar MCAR). *Correção:* mapa de faltantes por grupo/status; discutir mecanismo (MAR por status).

**E6 [M] — Quatro colunas de duração são a mesma variável (cél. 13, 25).** `duracao_sent2 == duracao_sort == duracao_proc` em 100% das linhas; `duracao_tecn == duracao_proc` em 100% das 428 linhas em que existe (é a mesma duração, filtrada para processos com técnica/AC registrada — só tratados) [verificado]. `duracao_do_processo` ("65 dia(s)") é a mesma informação em texto e é ignorada. O notebook as descreve como "cálculo 2", "a partir do sorteio", "duração total" — descrições inventadas (cél. 23), sem dicionário de dados. *Correção:* manter uma só variável-tempo, documentar a origem das demais, eliminar redundâncias.

**E7 [C] — Data de referência da censura e "janela de 218 dias" errados (cél. 19, 49–50).** Para todos os 209 Ativos, `dt_distribuicao + duracao_proc = 07/10/2026` [verificado] — a data de corte é a **data da atualização da planilha (07/10/2026)**, não 03/08/2026. Sentenças vão até 06/10/2026. O seguimento real varia de **65 dias** (distribuídos em 03/08) a **279 dias** (distribuídos em 01/01) — entrada escalonada. A "janela de 218 dias" do ODT não corresponde aos dados; "acima_218_dias = 5" e a linha vertical em 218 na ECDF não têm significado; a amplitude calculada (214 d) é de **inclusão**, não de seguimento. *Correção:* definir `data_corte = 2026-10-07`, recomputar `tempo = (dt_sentenca or data_corte) − dt_distribuicao`, e reportar o seguimento por coorte de mês.

**E8 [L] — Extração do ODT incompleta (cél. 5).** `el.text` ignora `tail` e spans; o texto sai truncado ("D A seleção...", títulos sem conteúdo). O texto do DOCX/ODT não é usado em nenhuma decisão analítica. *Correção:* `odfpy`/`pandoc` ou `itertext()`.

**E9 [L] — Caminhos e reprodutibilidade.** Caminhos `dat/estcaso_4JEC_natal/` e `txt/` não existem nesta pasta (arquivos estão na raiz); a saída é de outra máquina; `CORRECOES_COLUNA` é código morto; o notebook chama-se "Estudo de Caso 4". *Correção:* caminhos relativos ao notebook; `requirements`/`uv.lock`.

### B. Variáveis de desenho: sorteio, híbrida, Decisão

**E10 [C] — "Decisão" tratada como encerramento/desfecho (cél. 11, 13, 19, 34, 48).** As 26 "Decisão" são remessas por prevenção/incompetência (redistribuição) — não são sentença nem resolução do conflito; mediana 1 dia, 6 com 0 dias [verificado]. Ainda assim contam como `evento=1`, puxam para baixo o tempo dos grupos (6 Controle / 11 Presencial / 9 Remota) e entram no χ² de "tipo de sentença". *Correção:* excluir do experimento (o processo saiu do juízo antes de receber o tratamento — critério de elegibilidade) **ou** tratá-las como censura / risco competitivo (Aalen-Johansen, Fine-Gray). Com Decisão como censura, KM: Controle 81, Presencial 96, Remota 95 dias; log-rank p=0,015 [verificado].

**E11 [M] — "Híbrida" ignorada (cél. 22).** Só aparece como gráfico de barras. Híbrida = AC presencial em que uma parte participou remotamente (Res. CNJ 481) — é **não-adesão/cruzamento de tratamento**: 28 Presencial são híbridas; há também 3 "Sim" na Remota (incongruente com a definição) e 0 no Controle (não se aplica) [verificado]. *Correção:* análise por intenção de tratar (grupo sorteado) como principal + análise por protocolo / tratamento recebido como sensibilidade; checar os 3 casos da Remota.

**E12 [M] — "Sorteio aleatório" × "ordem de chegada" (cél. 0, 10).** O notebook afirma randomização sem verificá-la. Segundo o pesquisador, o sorteio seguiu a ordem de chegada. A sequência parece compatível com aleatoriedade (proporção de repetições consecutivas 0,333 = esperado 0,333; maior sequência 8) [verificado], mas não há registro do mecanismo (tabela de sorteio, ocultação da alocação). Além disso, a composição mensal varia (julho: Remota 69 × Presencial 43 × Controle 46) e julho concentra 101 dos 209 Ativos — grupos com mais entradas tardias têm mais censura. *Correção:* teste de corridas (Wald-Wolfowitz) / qui-quadrado de balanceamento por mês; descrever o procedimento de alocação; estratificar a análise por mês de distribuição.

**E13 [M] — Pergunta 2.7 (ordem de chegada × `duracao_proc`) não investigada.** Nenhuma célula usa a ordem. Ao fazê-lo: Spearman ordem × duração = −0,04 (p=0,21) em todos; −0,12 (p=0,001) só nos encerrados [verificado] — artefato da censura (processos recentes só aparecem encerrados se forem rápidos). *Correção:* usar a ordem/data como covariável num modelo de sobrevivência (Cox com tempo de entrada), não correlação bruta; "ordem" é ordinal → Spearman/Kendall, nunca Pearson.

### C. Estatística descritiva e correlação (cél. 23–25, 35–38)

**E14 [C] — Durações de processos Ativos usadas como tempos completos (cél. 13, 25, 28, 29, 40, 44, 46, 50, 54).** `duracao_proc` mistura 734 tempos observados com 209 tempos censurados (≥65 d, até 274). Média (78,5), mediana (80), percentis, boxplots, Kruskal, OLS, ajuste de distribuições e síntese final ignoram a censura — o próprio texto (cél. 18, 55) diz que isso "subestima artificialmente" o tempo. *Correção:* KM/log-rank, mediana de KM, RMST (tempo médio restrito), Cox; descrever encerrados e ativos separadamente apenas como descritivo.

**E15 [M] — Interpretação incoerente da forma da distribuição (cél. 25, 39–40, 50).** O texto repete "right-skewed", mas a assimetria observada é **0,30** e a curtose 0,01 (quase simétrica) — exatamente porque a censura corta a cauda direita. Média ≈ mediana aqui não indica normalidade nem ausência de cauda: indica truncamento. Unidades erradas ("Assimetria 0,30 **dias**"). Na cél. 50 diz "a média é influenciada pelos processos longos (maioria censurados)" — mas os censurados estão contados como se completos.

**E16 [C] — Matriz de correlação trivial/inadequada (cél. 37–38).** (i) Correlaciona quatro cópias da mesma variável → r=1,000 em tudo, e as dispersões dão R²=1, "p=0" — tautologia, não achado; (ii) `duracao_tecn` só existe para os tratados com AC (seleção) e é a mesma duração; (iii) não há nenhuma outra variável quantitativa intervalar no banco: as demais (grupo, híbrida, acordo, técnica, sentença) são nominais e não cabem em matriz de Pearson/Spearman (o enunciado 2.7 fala em Pearson; o código usa Spearman, mas o problema é o mesmo); (iv) ignora censura. *Correção:* descartar a matriz; para nominal×nominal usar V de Cramér/φ; nominal×tempo, modelos de sobrevivência; para ordem de chegada (ordinal) × tempo, Spearman/Kendall com cautela ou Cox; para variáveis novas intervalares (nº de autores/réus, nº de atos — Q 2.9), Pearson só com linearidade/normalidade bivariada, senão Spearman, com teste t para ρ=0 / permutação.

### D. Testes de hipótese (cél. 28–46)

**E17 [C] — Kruskal-Wallis em tempos censurados (cél. 28).** H=1,48, p=0,478 → "sem diferença". Com KM corretamente aplicado: medianas Controle 80, Presencial 93, Remota 94 dias; **log-rank multivariado p=0,028** [verificado] — os tratamentos foram **mais lentos**, conclusão oposta à pretendida pela pesquisa e invisível no notebook. Além disso, H₀ formulada como "medianas iguais" só vale sob mesma forma de distribuição (o KW testa dominância estocástica). Post-hoc Mann-Whitney sem correção de multiplicidade (Bonferroni/Holm ou Dunn). *Correção:* log-rank (global + pares com Holm), Cox `tempo ~ grupo (+ mês)`, RMST; tamanho de efeito (HR com IC95%).

**E18 [C] — Mann-Whitney Encerrado × Ativo é tautológico (cél. 29).** Ativos têm, por construção, duração ≥65 dias até a data de corte; a "diferença" (p=3e-24) mede o tempo de seguimento, não um efeito. *Correção:* remover; se necessário, descrever seguimento.

**E19 [M] — χ² grupo × status (cél. 32).** p=0,00015, mas "estar Ativo em 07/10" depende do tempo de seguimento e do mês de entrada (julho mais Remota). Não é desfecho comparável entre grupos sem ajustar o tempo. *Correção:* comparar taxa de encerramento em horizonte fixo (p.ex. encerrado em ≤90 dias, apenas entre os com ≥90 dias de seguimento) ou usar KM/Cox.

**E20 [M] — χ² grupo × acordo na AC (cél. 33).** O Controle tem 0/314 por ausência estrutural de AC (zero estrutural): o teste "descobre" que quem não teve audiência não fez acordo na audiência. Frequências esperadas da coluna "Sim" ≈ 5,2–6,1 (no limite da regra de Cochran) [verificado]; n=17 eventos. *Correção:* comparar só Presencial × Remota (9/291 vs 8/264) com **exato de Fisher** e IC da diferença de proporções; considerar "acordo total" (na AC + fora da AC) como desfecho que existe também no Controle.

**E21 [M] — χ² sentença × grupo (cél. 34).** p=2e-06, mas inclui "Decisão" (não é sentença, E10) e não diferencia Homologação de acordo feito na AC × fora da AC; sem resíduos padronizados ajustados nem V de Cramér; proporções exibidas por linha (sentença→grupo) quando o interesse é por coluna (grupo→sentença). *Correção:* excluir Decisão, reportar % por grupo, resíduos ajustados, V de Cramér; e notar que o Controle tem mais "julgamento de mérito" e os tratados mais "sem mérito" (possível efeito de ausência da parte autora à AC obrigatória — art. 51, I, Lei 9.099) — achado jurídico relevante ignorado.

**E22 [M] — Normalidade (cél. 40).** Subamostra arbitrária de 500 de 943 (descarta dados para "evitar" poder estatístico); testes discordantes (SW rejeita, D'Agostino não) sem interpretação; testa a variável agregada, e não por grupo / resíduos; e a distribuição é de tempos censurados, então a pergunta é mal posta. A escolha não paramétrica já havia sido feita antes (cél. 28) — teste a posteriori. *Correção:* Q-Q por grupo / resíduos; para dados de sobrevivência, testar adequação do modelo (resíduos de Cox-Snell, riscos proporcionais — Schoenfeld).

**E23 [L] — Teste z de proporção p₀=0,5 (cél. 42).** Hipótese sem sentido substantivo (por que 50%?); a proporção de encerrados depende da data de corte. *Correção:* remover ou substituir por IC da proporção por grupo em horizonte fixo.

**E24 [M] — Mann-Whitney com × sem acordo na AC (cél. 42).** "Sem acordo" inclui os 314 do Controle (que não tiveram AC) e os Ativos (censurados); n=17 vs 852; nenhum ajuste. *Correção:* restringir aos tratados que tiveram AC realizada; tempo censurado → log-rank; ou tempo desde a AC.

**E25 [M] — Ajuste de distribuições (cél. 44).** Ajusta MLE a dados censurados como se completos; descarta silenciosamente os 39 zeros (`x>0`); `weibull_min/gamma/lognorm` com `loc` livre (3 parâmetros, `loc` sem sentido físico). *Correção:* ajuste paramétrico com censura (`lifelines.WeibullFitter`, `LogNormalFitter`, AFT `WeibullAFTFitter`), `floc=0`, tratar zeros (somar 0,5 dia ou modelo discreto).

**E26 [M] — Regressões (cél. 46).** OLS `duracao_proc ~ grupo` com censurados (viés para zero; Durbin-Watson 1,47 sinaliza dependência temporal pela ordem); Logit `evento ~ grupo` mistura efeito do tratamento com tempo de seguimento e Decisão como "evento". O markdown promete "durações intermediárias e indicadores de acordo" como preditoras, mas o código as exclui (incoerência texto×código; incluí-las seria tautológico/colinear). *Correção:* Cox PH (`tempo, evento_merito ~ grupo + mês_distribuição`), AFT Weibull; HR e IC95%.

**E27 [M] — Multiplicidade e efeito.** ~10 testes a α=0,05 sem correção (Bonferroni/Holm/FDR); nenhum tamanho de efeito (ε², r de Rosenbaum, V de Cramér, HR) nem IC; nenhuma análise de poder.

**E28 [M] — Independência das observações (2.3).** Grupos são amostras independentes **entre si** (alocação de processos distintos), mas: duplicatas re-sorteadas (E3), mesmo juiz/conciliadores/servidores, litigantes habituais (bancos, telefônicas, mesmos advogados) em vários grupos → agrupamento (*clustering*) e possível contaminação. Não são "amostras de uma mesma população" no sentido de amostragem probabilística: é uma única população disponível (processos distribuídos ao 4º JEC) particionada por sorteio. *Correção:* mencionar; se houver dado de parte/advogado, erros-padrão robustos por cluster ou efeitos aleatórios.

**E29 [L] — Fallback "ECDF" (cél. 48).** Divide encerrados por `len(sub)` (inclui censurados no denominador e nunca os remove do risco): é uma curva de incidência acumulada ingênua, não KM; sem IC e sem teste — apresentado como "substituto do Kaplan-Meier".

**E30 [L] — Síntese (cél. 54) e notas (cél. 55)** reportam média/mediana ingênuas e "prop. acordos na AC 2,0%" (denominador inclui o Controle — real ≈ 3,1% entre tratados). As "lições" (censura, mediana, causalidade) contradizem o que o notebook efetivamente fez. A comparação pré × pós do ODT (106,8 vs 75,2 dias) não é reproduzida nem criticada.

---

## 3. Mapeamento para as questões 2.2–2.12

| Questão | Itens relevantes | Comentário |
|---|---|---|
| **2.2** EO × ECA | E12, E28, cél. 0 | Há alocação por sorteio controlada pelo pesquisador → é um **ECA** (ensaio controlado aleatorizado, pragmático, de um único centro, não cego). Fragilidades: mecanismo de aleatorização não documentado ("ordem de chegada"), cruzamento (híbridas), re-sorteio de duplicatas. Se o "sorteio" for na verdade alternância/ordem, vira quase-experimento. |
| **2.3** Amostras independentes? | E3, E12, E28 | Independentes entre grupos (processos distintos, alocação aleatória) — salvo duplicatas e agentes comuns. Implica testes para amostras independentes (KW, MW, log-rank, χ²/Fisher), não pareados (Friedman/Wilcoxon). |
| **2.4** Híbrida / Decisão | E10, E11 | Híbrida = não-adesão parcial ao rito presencial (ITT × per-protocol). Decisão = redistribuição: excluir (inelegível pós-randomização, com transparência) ou censurar/risco competitivo; nunca "sentença". |
| **2.5** Populações / CNJ | E7, E9, cél. 52 | O notebook não discute. Pop. de interesse: ações dos JECs (Natal/RN ou Brasil); disponível: processos distribuídos ao 4º JEC 01/01–03/08/2026; amostrada: os 943 (+duplicatas). DataJud/CNJ (API pública, classe/órgão julgador/movimentos) permite cruzar os 14 JECs — o checklist da cél. 52 é apenas um placeholder. |
| **2.6** Tratamento dos dados | **E1–E11, E14** | Não adequado: linha fantasma, duplicatas, `**`, NA estrutural, colunas redundantes, data de corte errada, Decisão como evento, híbrida ignorada, censura ignorada. Complementar com dicionário de dados, regras de exclusão, `data_corte`, `tempo`/`evento_merito`, `mes_dist`, `ordem`, `acordo_total`. |
| **2.7** Matriz de correlações / ordem | **E6, E13, E16** | Inadequada: correlaciona 4 cópias da mesma variável (r=1 trivial), sem outras quantitativas intervalares; categóricas exigem outras medidas. A ordem de chegada é ordinal → Spearman/Kendall possível, mas confundida com tempo de seguimento (censura) — usar Cox com data/ordem como covariável. |
| **2.8** Confundimento | E11, E12, E19, E28 | Mês/coorte de entrada (seguimento e sazonalidade), carga do cartório, conciliador, tipo de réu (litigante habitual), assunto/valor da causa, presença de advogado, ausência do autor (extinção sem mérito), Hawthorne. Randomização controla em média os fatores pré-alocação, mas não os pós-alocação (híbrida, ausências, redistribuições). |
| **2.9** Outras quantitativas intervalares | E16 | Nº de autores/réus, nº de atos/movimentos, dias até a AC, dias da AC até a sentença, valor da causa → Pearson (se linearidade/normalidade) ou Spearman/Kendall; teste t para ρ, ou permutação; com censura, Cox. |
| **2.10** Validade externa | E7, cél. 53 | Um único JEC, um único juiz-pesquisador, 7 meses → generalização para os 14 JECs não autorizada sem replicação multicêntrica / comparação com DataJud. |
| **2.11** TSHN adequados? | **E14, E17–E27, E29** | Inadequados: KW e OLS em censurados; MW Encerrado×Ativo tautológico; χ² com zero estrutural e esperadas no limite; z p₀=0,5 sem sentido; normalidade mal aplicada; sem correção múltipla nem tamanhos de efeito. Usar: KM + log-rank (global e par a par com Holm), Cox/AFT, RMST, Aalen-Johansen/Fine-Gray (Decisão, acordo), Fisher exato, V de Cramér, Dunn (se KW em encerrados), testes de permutação, teste de corridas para o sorteio. |
| **2.12** Avaliação geral | todos | Delineamento promissor (randomizado, dados primários com datas), mas registro com placeholders, sem dicionário, alocação não documentada, desfechos contaminados (Decisão), adesão não registrada sistematicamente, seguimento curto e escalonado. Sugestões: protocolo pré-registrado, lista de aleatorização em blocos estratificada por mês, ocultação da alocação, registro de adesão e motivo de extinção, seguimento mínimo igual para todos, multicêntrico, linkage com DataJud. |

---

## 4. O que reaproveitar × o que refazer

**Reaproveitar (boas ideias / código útil)**
- Leitura com `header=None` + cabeçalho na linha índice 1; `slug_coluna()` (snake_case ASCII); `MAPA_GRUPO`; `sentenca_std` com `.str.title()` (unifica variantes de caixa).
- Auditoria da cél. 15 (duplicatas, faltantes, negativas, conferência data × duração — confirma 0 inconsistências entre `dt_sentenca − dt_distribuicao` e `duracao_proc` nos encerrados).
- Criação de indicador de evento/censura e a verificação cruzada com `status` (ajustando o caso NaN).
- Funções gráficas `plot_barras_pareto`, `comparacao_grupos_boxplot`, `analise_associacao` (acrescentar Fisher, resíduos e V de Cramér).
- Esqueleto da cél. 48 de KM por grupo (depois de corrigir o import) e a ideia de checklist para linkage com DataJud.
- Escolha declarada de métodos não paramétricos e a preocupação textual com censura, assimetria e validade externa (só falta aplicá-las).

**Refazer**
- Import de lifelines; remoção do `warnings.filterwarnings('ignore')`.
- Base analítica: excluir linha fantasma, tratar duplicatas, recodificar `**`/NA estrutural, criar `tempo` com `data_corte=2026-10-07`, `evento_merito` (Decisão censurada ou excluída), `mes_dist`, `ordem`, `hibrida` (ITT/per-protocol), `acordo_total`.
- Toda inferência sobre tempo: KM, log-rank, RMST, Cox/AFT (com mês de distribuição), riscos competitivos; substituir KW/OLS/ajuste MLE ingênuos.
- Remover: matriz de correlação das durações, dispersões tautológicas, MW Encerrado×Ativo, teste z p₀=0,5, normalidade em subamostra.
- Testes categóricos: Fisher Presencial×Remota para acordo na AC; sentença × grupo sem Decisão com resíduos; correção de multiplicidade e tamanhos de efeito em tudo.
- Correção da narrativa: "Estudo de Caso 2", janela real de seguimento (65–279 dias), afirmação sobre sorteio, descrição das colunas de duração.

**Resultado-chave que muda a conclusão** [verificado]: ingênuo (notebook) KW p=0,48 "sem diferença"; correto (KM) medianas Controle 80 × Presencial 93 × Remota 94 dias, log-rank p=0,028 (p=0,015 com Decisão censurada) — conciliação obrigatória associada a tramitação **mais longa**, não mais curta.
