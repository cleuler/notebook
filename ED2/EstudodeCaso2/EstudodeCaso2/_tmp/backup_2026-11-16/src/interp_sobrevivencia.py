# Interpretações da Parte IV — Análise de sobrevivência (chaves sob_*).
# Redigidas a partir das saídas reais de EstudodeCaso2/_tmp/teste_secao04.ipynb.

INTERP_SOBREVIVENCIA = {

    'sob_estrutura': r'''
**Interpretação (estrutura dos dados).**

- **A censura é desigual entre os grupos:** 16,3% no Controle, 26,8% na AC presencial e 30,5% na AC remota. Os três grupos têm seguimento potencial quase igual (mediana de 170, 162 e 161 dias; mínimo de 65 dias em todos), então a diferença **não** vem do calendário de entrada. Ela vem do próprio desfecho: mais processos com AC ainda aguardavam sentença em 07/10. Isso já antecipa que os ritos com AC são mais lentos, e mostra por que comparar médias só dos encerrados (E14) favorece artificialmente os grupos com AC: os processos lentos deles estão justamente entre os censurados.
- O seguimento mediano pelo KM reverso (167, 140 e 147 dias) é menor nos grupos com AC pelo mesmo motivo. Os processos que continuam ativos são os distribuídos mais tarde.
- **A censura cresce com o mês de distribuição** em todos os grupos (gráfico de barras): é a assinatura da entrada escalonada. Em julho e agosto, a maior parte ainda está ativa. A análise precisa, portanto, condicionar no mês (seções 4.3.4 e 4.5).
- **A informação se esgota depois de ~180 dias.** A tabela de vida mostra 9 a 10 processos em risco por grupo aos 180 dias e 1 a 5 aos 210 dias. Estimativas além de 180 dias são frágeis, e por isso τ = 180 dias é o horizonte máximo do RMST.
- **Plausibilidade da censura não informativa.** Todos os 206 censurados estão ativos na data de corte, e o tempo potencial de censura é fixado pela data de distribuição, não pelo andamento do processo. A hipótese é razoável, **desde que o mês entre no modelo**, porque a seção 4.5.4 mostra uma tendência de calendário (processos mais recentes tramitam mais devagar). As 24 redistribuições (5, 10 e 9 por grupo) são outro mecanismo e são tratadas na seção 4.7.
''',

    'sob_km': r'''
**Interpretação (Kaplan-Meier e risco).**

- **Mediana global:** 89 dias (IC 95%: 83–94). Metade dos processos do 4º JEC recebeu sentença em cerca de três meses.
- **Medianas por grupo:**

  | Grupo | Mediana (IC 95%) |
  |---|---|
  | Controle | 81 dias (75–84) |
  | AC presencial | 96 dias (85–106) |
  | AC remota | 95 dias (89–102) |

  Os intervalos do Controle não se sobrepõem aos da AC remota e só tocam os da presencial. A **AC obrigatória atrasou a mediana em cerca de 15 dias**. O notebook do professor, com o Kruskal-Wallis sobre tempos censurados (E17), concluía "sem diferença".
- **O formato das curvas importa mais que as medianas.** Até cerca de 60 dias, as três curvas praticamente coincidem: Ŝ(30) = 80,6%, 77,9% e 82,5%; Ŝ(60) = 68,9%, 66,3% e 73,6%. A separação acontece **entre 60 e 120 dias**:
  - aos 90 dias, 39,6% dos processos do Controle ainda estão sem sentença, contra 52,3% na AC presencial e 53,7% na remota;
  - aos 120 dias, 23,0% contra 31,0% e 31,3%;
  - aos 180 dias as curvas voltam a se aproximar (6,9%, 7,5% e 10,7%), com ICs largos.
- **Quartis.** O 1º quartil da AC presencial é o *menor* (37 dias, contra 48 no Controle): uma parte dos processos presenciais termina **mais cedo**, e a seção 4.7 mostra que são extinções sem mérito. O 3º quartil é 17 a 18 dias maior nos grupos com AC (131–132 contra 114).
- **Risco suavizado.** A taxa diária de sentenças do Controle atinge o pico por volta de 90 dias (≈ 0,021 sentença por processo pendente por dia). Nos grupos com AC, o pico é **deslocado para 120–150 dias**. É o retrato de um rito com uma etapa a mais: o julgamento de mérito espera a audiência, e a "onda" de sentenças chega mais tarde. Nos primeiros 30 dias, a AC presencial tem taxa um pouco maior que a dos outros grupos.
''',

    'sob_testes': r'''
**Interpretação (comparação das curvas).**

**Teste principal.** Log-rank de 3 grupos: χ²₂ = 7,52, **p = 0,023**. Rejeita-se H₀ de curvas iguais a 5%. O gráfico O/E mostra a direção: o Controle teve 14% **mais** sentenças do que o esperado sob H₀ (O/E = 1,14), e os grupos com AC tiveram menos (0,96 presencial; 0,90 remota).

**Família ponderada (sensibilidade).**

| Teste | Peso | χ²₂ | p |
|---|---|---|---|
| Wilcoxon | início | 6,40 | 0,041 |
| Tarone-Ware | meio-termo | 7,82 | 0,020 |
| Peto-Prentice | início | 6,77 | 0,034 |
| FH(0,1) | final | 4,91 | 0,086 |
| **FH(1,1)** | **meio do seguimento** | **13,80** | **0,001** (Holm 0,007) |

O teste mais forte é o que dá mais peso ao **meio** do seguimento. Isso confirma o que o KM mostra: a diferença está concentrada na faixa de 60 a 120 dias, e não no início nem na cauda. O log-rank, que pesa tudo igualmente, perde parte do poder porque nos extremos as curvas quase coincidem.

**Pares (Holm).**

- **Remota × Controle: p = 0,008 (Holm 0,023)**, significativo;
- Presencial × Controle: p = 0,061 (Holm 0,123), não significativo isoladamente, mas na mesma direção;
- Remota × Presencial: p = 0,519. Não há evidência de diferença entre as modalidades.

**Estratificado por mês.** O log-rank estratificado dá χ²₂ = 6,21, **p = 0,045**; o Gehan-Breslow e o Tarone-Ware estratificados dão p = 0,017 e 0,018. O resultado sobrevive à comparação dentro de cada mês: não é artefato da composição mensal (por exemplo, julho com mais Remota).

**Pontos fixos (Holm sobre 6 testes).**

- Aos 60 dias não há diferença (p ≥ 0,2).
- **Aos 90 dias**, a proporção ainda sem sentença é **12,7 p.p. maior** na AC presencial (IC 95%: 4,7 a 20,7; p Holm = 0,010) e **14,0 p.p. maior** na remota (5,9 a 22,1; p Holm = 0,005).
- Aos 120 dias a diferença cai para cerca de 8 p.p. (p = 0,040 e 0,037 sem correção; 0,149 com Holm).

**RMST.** O efeito médio em dias é modesto.

| τ | RMST Controle | Remota − Controle | Presencial − Controle |
|---|---|---|---|
| 180 d | 82,1 dias | **+10,7 dias** (IC bootstrap 1,9 a 19,5; p = 0,016) | +6,5 dias (−2,1 a 15,8; p = 0,16) |
| 150 d | — | +9,6 dias (p = 0,016) | — |
| 90 d | — | +4,2 dias (ns) | −0,1 dia |

A τ = 90 dias, o atraso dos grupos com AC no fim do intervalo é compensado pelos processos presenciais que terminam mais cedo. Em linguagem de gestão: **nos primeiros seis meses, um processo do rito com AC remota passou, em média, cerca de 11 dias a mais sem sentença** do que no rito atual. Na presencial, cerca de 6 dias a mais, sem significância.
''',

    'sob_ph': r'''
**Interpretação (riscos proporcionais).**

- **Gráfico log(−log Ŝ).** As curvas **não são paralelas**:
  - nos primeiros ~30 dias, a AC presencial está *acima* das demais (mais sentenças precoces);
  - entre 30 e 60 dias as curvas se cruzam;
  - entre ~60 e 120 dias o Controle se afasta para cima (mais sentenças);
  - depois de ~150 dias as curvas voltam a se juntar.

  Esse é um padrão de efeito que **muda de sinal e de intensidade com o tempo**.
- **Teste de Grambsch-Therneau.** Não rejeita a proporcionalidade para nenhum termo: p = 0,49, 0,76 e 0,60 para a presencial (posto, km, t) e 0,98, 0,84 e 0,98 para a remota. Os meses também não violam a hipótese (p entre 0,08 e 0,39).
- **Por que o teste não detecta o que o gráfico mostra.** O teste mede a **correlação linear** entre os resíduos e g(t), ou seja, uma tendência *monótona* de β(t). A suavização *lowess* dos resíduos de Schoenfeld mostra outra forma: β(t) perto de zero no início, um **vale** entre ~60 e ~110 dias (β(t) ≈ −0,9, isto é, HR ≈ 0,4 na presencial) e retorno a zero depois. Um desvio em "U" tem correlação quase nula com o tempo, e o teste perde poder. Colosimo e Giolo (2006, p. 167-170) recomendam ler o gráfico junto com o teste.
- **Consequência.** O HR único do Cox (seção 4.5.1) é uma **média** de um efeito que se concentra numa janela. Por isso a seção 4.5.2 estima o efeito por janela de tempo, e o RMST e os pontos fixos (4.3), que não supõem proporcionalidade, são relatados ao lado do HR.
''',

    'sob_cox': r'''
**Interpretação (modelos de Cox).**

**Efeito do rito (HR < 1 = sentença mais lenta).**

| Modelo | AC presencial × Controle | AC remota × Controle |
|---|---|---|
| (a) só grupo | HR = 0,84 (IC 95%: 0,70–1,00; p = 0,053) | **HR = 0,79 (0,66–0,94; p = 0,009)** |
| (b) + mês + origem | 0,87 (0,72–1,04; p = 0,117) | **0,81 (0,68–0,97; p = 0,022)** |
| (b′) estratificado por mês | 0,86 (p = 0,091) | **0,80 (p = 0,017)** |

O ajuste pelo calendário quase não altera os HRs, o que é o esperado num experimento sorteado: o mês melhora a precisão, mas não confunde o efeito. Em linguagem jurídica: **a cada dia, um processo pendente no rito com AC remota tem cerca de 19% menos "chance" de ser sentenciado** do que um processo pendente no rito atual. Na AC presencial, a redução é de cerca de 13%, compatível com zero.

**Calendário.** Os processos distribuídos em junho (HR = 0,70; p = 0,023) e em julho–agosto (HR = 0,58; p = 0,002) tramitam mais devagar que os de janeiro. Possíveis razões: o acúmulo de pauta ao longo do ano e o recesso/férias de julho. O resíduo martingal contra a ordem de chegada (modelo só com grupo) tem tendência decrescente, o que confirma essa tendência de calendário e justifica o mês no modelo. É o "teste de tendência" que faz sentido aqui (o do grupo não faz; ver 4.3.3). A origem externa não tem efeito detectável (HR = 0,78; p = 0,46; só 12 processos).

**Ajuste e discriminação.**

- O TRV do modelo (b) contra o nulo é χ²₉ = 29,9 (p < 0,001); o AIC parcial cai de 8.469,2 em (a) para 8.460,7 em (b).
- A concordância é baixa (C = 0,53 a 0,56). O grupo e o mês **explicam pouco da variação individual** do tempo: o rito desloca a distribuição, mas a duração de cada processo depende sobretudo de fatores não medidos (complexidade, comportamento das partes, pauta).
- O Cox-Snell do modelo (b) fica sobre a reta y = x até ê ≈ 3, o que indica bom ajuste global.
- Há 3 resíduos deviance além de ±2,5, e nenhum processo tem |dfbeta| acima de 2/√n (o maior é 0,006, frente a um β̂ de −0,14 e EP de 0,09). **Nenhum processo isolado sustenta o resultado.**
- As curvas padronizadas do Cox acompanham bem os KMs.

**Efeito por janela de tempo, modelo (c).** O efeito do rito **não é constante**. O TRV contra o modelo (b) dá χ²₄ = 11,04 (p = 0,026), e o AIC parcial cai de 8.460,7 para 8.457,6.

| Janela | AC presencial × Controle | AC remota × Controle |
|---|---|---|
| 0–30 dias | 1,19 (0,84–1,69) | 0,93 (0,65–1,35) |
| **30–90 dias** | **0,62 (0,46–0,82; p < 0,001)** | **0,63 (0,48–0,84; p = 0,002)** |
| > 90 dias | 1,01 (0,74–1,38) | 0,98 (0,72–1,34) |

Entre 30 e 90 dias, o Controle produziu 122 sentenças, contra 75 e 80 nos grupos com AC. Leitura: **no período em que as audiências obrigatórias acontecem, os processos dos grupos com AC são sentenciados a uma taxa cerca de 37% menor**. Antes disso, a taxa é igual (ou ligeiramente maior na presencial). Depois de 90 dias, a taxa volta a ser a mesma do Controle, mas os grupos com AC **não recuperam** o atraso acumulado. O efeito da AC obrigatória é, portanto, uma **etapa adicional que retarda as sentenças por cerca de dois meses**, e não uma lentidão uniforme.
''',

    'sob_aft': r'''
**Interpretação (AFT).**

- **Razões de tempos (TR > 1 = mais lento):**

  | Modelo | AC presencial × Controle | AC remota × Controle |
  |---|---|---|
  | Weibull | 1,11 (0,93–1,34; p = 0,26) | 1,21 (1,00–1,45; p = 0,051) |
  | Log-normal | 1,01 (0,75–1,37) | 1,22 (0,90–1,65; p = 0,20) |
  | Log-logística | 1,10 (0,86–1,41) | 1,25 (0,98–1,59; p = 0,074) |

  A direção é a mesma do Cox e do RMST: a AC remota **alonga o tempo em cerca de 20%**, e a presencial em cerca de 10%. O resultado da log-normal coincide com o da Parte V (TR da remota ≈ 1,2, não significativo).
- **O ajuste dos três modelos é ruim.** A Weibull tem o menor AIC (7.958, contra 8.170 da log-logística e 8.273 da log-normal), mas os gráficos de Cox-Snell se afastam claramente da reta y = x nos três modelos.
- **As medianas previstas mostram o problema.** A Weibull prevê 68, 75 e 82 dias, contra 81, 96 e 95 do KM; a log-normal, 61, 62 e 74. A razão é estrutural: a distribuição do tempo é uma **mistura** de extinções muito precoces (dezenas de processos em 0 a 10 dias; os tempos zero viram 0,5 dia) com julgamentos de mérito concentrados entre 80 e 130 dias. Nenhuma família unimodal de 2 parâmetros acomoda as duas massas.
- **Conclusão.** As razões de tempos servem como **resumo descritivo da direção e da ordem de grandeza** do efeito ("cerca de +10% a +20%"), mas os seus ICs e p-valores dependem de um modelo mal especificado. As medidas não paramétricas (KM, RMST) e semiparamétricas (Cox) são as preferíveis, e a seção 4.7 modela explicitamente os tipos de desfecho que formam a mistura.
''',

    'sob_cr': r'''
**Interpretação (riscos competitivos).**

**(a) Redistribuição.** O 1 − KM que censura a redistribuição superestima a proporção sentenciada em 0,9 a 1,4 p.p. aos 90 dias e em 1,5 a 2,9 p.p. aos 180 dias. O viés é maior nos grupos com AC, que têm o dobro de redistribuições (3,2% na presencial e 3,0% na remota, contra 1,6% no Controle, todas nos primeiros dias). É pequeno e não altera nenhuma conclusão, mas tem sentido conhecido.

**(b) Tipo de sentença: aqui está o mecanismo.** As FIAs aos 90 dias:

| Desfecho | Controle | AC presencial | AC remota |
|---|---|---|---|
| Mérito | 31,1% | 7,8% | 7,5% |
| Sem mérito | 23,5% | 32,0% | 27,3% |
| Homologação | 4,9% | 6,4% | 10,6% |

- **Julgamento de mérito: fortemente atrasado e reduzido pela AC.** Aos 120 dias, 45,5% dos processos do Controle já tinham sentença de mérito, contra 24,2% e 23,5%; aos 180 dias, 58,3% contra 45,0% e 39,0%.
  - Teste tipo Gray (permutação no mês): **p < 0,001** (Holm 0,002).
  - Cox causa-específico: **HR = 0,55 (0,42–0,71)** na presencial e **0,47 (0,36–0,62)** na remota. Entre os processos pendentes, a taxa de julgamento de mérito cai à metade.
  - Fine-Gray: sHR = 0,46 (0,36–0,60) e 0,42 (0,32–0,55). A versão IPCW dá 0,48 e 0,43, o que confirma a implementação.
- **Extinção sem mérito: acelerada e aumentada pela AC, sobretudo a presencial.** Aos 60 dias, 28,0% na presencial contra 19,8% no Controle; aos 180 dias, 36,2% e 34,8% contra 25,7%.
  - Cox causa-específico: presencial **HR = 1,40 (1,05–1,87; p = 0,023)**; remota 1,26 (0,94–1,70; p = 0,13).
  - Fine-Gray: presencial **sHR = 1,46 (1,09–1,95; p = 0,011)**; remota 1,32 (p = 0,07).
  - Teste de permutação: p = 0,020 (Holm 0,061).

  É o padrão previsto pela hipótese da **extinção por ausência do autor à audiência** (art. 51, I, da Lei 9.099/1995): no Controle não há audiência a que faltar.
- **Acordo homologado: aumentado na AC remota.** Aos 90 dias, 10,6% contra 4,9% no Controle e 6,4% na presencial; aos 180 dias, 12,9% contra 7,6%.
  - Fine-Gray da remota: **sHR = 1,87 (1,08–3,24; p = 0,026)**; Cox causa-específico 1,71 (p = 0,053).
  - Teste de permutação: p = 0,055.
  - A AC presencial não difere do Controle (sHR = 1,25; p = 0,46).
  - Com 81 acordos no total, a evidência é moderada, coerente com a razão de chances de acordo de 2,15 (remota × Controle) da Parte V.

**A hipótese se confirma: o tempo total esconde mecanismos opostos.** A AC obrigatória **acelera** dois tipos de encerramento — extinções (presencial) e acordos (remota) —, mas **atrasa fortemente** o julgamento de mérito, que passa a esperar a audiência. Como o mérito é o desfecho mais frequente (341 de 708 sentenças), o efeito líquido sobre o tempo total é de atraso (HR ≈ 0,8 a 0,87). Juridicamente, o rito com AC muda **como** os processos terminam, e não só **quando**:

- menos decisões de mérito;
- mais extinções sem resolução do conflito, que deixam o autor sem solução e podem gerar reajuizamento;
- e, na modalidade remota, mais acordos.

Uma avaliação do rito que olhe só a duração perde a parte mais importante do efeito.
''',

    'sob_ac': r'''
**Interpretação (subconjunto com AC realizada).**

- **Tamanho e composição.** 352 processos tiveram AC realizada (178 presenciais e 174 remotos). Os perfis de desfecho diferem: a remota tem mais extinções sem mérito (35 contra 20) e mais acordos (19 contra 14), e a presencial tem mais mérito (94 contra 81).
- **Modalidade.** Entre quem teve AC, a remota não difere da presencial: HR = 1,13 (0,88–1,44; p = 0,34) ajustado pelo mês; log-rank p = 0,234; medianas de 115 e 107 dias.
- **Tempo imortal.** Essas medianas são **maiores** que as dos grupos inteiros (96 e 95 dias), justamente porque quem teve AC precisou estar pendente até a data da audiência. Comparar esses processos com os que não tiveram AC (ou com o Controle) atribuiria à audiência um atraso que é, em parte, mecânico.
- **Técnica de conciliação.** Nenhuma diferença: log-rank de 6 grupos com χ²₅ = 1,55, p = 0,908; HRs entre 1,04 e 1,28 em relação a Padrões objetivos, todos com IC contendo 1. Com 47 a 67 processos por técnica, o estudo só detectaria diferenças grandes. A conclusão é "sem evidência de efeito da técnica sobre o tempo", não "técnicas equivalentes".
- **Audiência híbrida.** Dentro do grupo Presencial com AC, as 24 híbridas e as 154 presenciais puras têm tempos indistinguíveis (log-rank p = 0,907).
- **Ressalva.** Os três contrastes são **associativos**. Só a técnica foi sorteada, e mesmo ela só existe para quem chegou à audiência. A análise de *landmark* adequada exigiria a data da AC, que a planilha não registra: é um item a coletar numa replicação (via PJe/DataJud).
''',

    'sob_sens': r'''
**Interpretação (sensibilidade).**

- **Robustez geral.** Em 11 dos 12 cenários, os HRs ficam em faixas estreitas e o log-rank continua significativo (p de 0,007 a 0,046):
  - **0,84–0,90 para a AC presencial**, com IC contendo ou tocando 1 em todos os cenários, exceto no Fine-Gray (i-b), em que o sHR é 0,81 (0,67–0,96);
  - **0,77–0,83 para a AC remota**, com IC sempre abaixo de 1.

  Excluir as redistribuições, a origem externa, os desvios de protocolo ou os tempos zero, reincluir as duplicatas, deslocar ou excluir as sentenças de fim de semana: **nenhuma decisão de curadoria muda a conclusão**.
- **(iii-b) Híbridas "como tratadas".** Passar as 28 híbridas para o grupo Remota aproxima a presencial de 1 (HR = 0,90) e fortalece a remota (0,79; log-rank p = 0,013). A conclusão não muda.
- **(i-b) Redistribuição como competidora (Fine-Gray da sentença).** Os sHR (0,81 e 0,77) são um pouco **menores** que os HRs, porque os grupos com AC têm o dobro de redistribuições: menos processos chegam a ter sentença no 4º JEC.
- **(vii) Dados ingênuos ("Decisão" = evento, como o notebook do professor; E10).** O efeito fica atenuado (HR = 0,89 e 0,83; log-rank p = 0,046): contar redistribuições como sentenças "acelera" artificialmente os grupos que mais as têm.
- **(vi) Censura comum em 65 dias: a exceção esperada.** HR = 1,04 (0,80–1,36) na presencial e 0,80 (0,60–1,06) na remota; p = 0,075. Até 65 dias o efeito da AC ainda não apareceu (seção 4.5.2: a diferença está na janela de 30 a 90 dias e sobretudo depois de 60). Esse cenário não refuta o resultado principal; mostra **em que momento** ele surge. Para neutralizar a entrada escalonada sem perder a janela relevante, a estratégia adequada é a estratificação por mês (4.3.4 e modelo b′), que mantém o efeito (p = 0,045 e HR remota = 0,80).
''',

    'sob_sintese': r'''
**Síntese e resposta à pergunta de pesquisa 2.**

**A AC obrigatória altera o tempo até a sentença?** Sim, e no sentido de **alongá-lo**, contra a expectativa que motivou o experimento.

| Medida | Controle | AC presencial | AC remota |
|---|---|---|---|
| Mediana (dias) | 81 | 96 | 95 |
| RMST em 180 dias (dias) | 82,1 | 88,6 | 92,9 |
| HR ajustado (Cox b) | referência | 0,87 (0,72–1,04) | 0,81 (0,67–0,97) |

- O log-rank global dá p = 0,023, e o estratificado por mês, p = 0,045.
- **Remota:** o efeito é estatisticamente sólido. ΔRMST₁₈₀ = +10,7 dias (IC 1,9 a 19,5); HR = 0,81; resultado robusto em 11 de 12 cenários de sensibilidade.
- **Presencial:** a direção é a mesma (+6,5 dias; HR = 0,87), mas o IC inclui o efeito nulo. Os dados não permitem afirmar que a presencial seja mais lenta que o Controle **no tempo total**.

**Quando o atraso acontece.** O atraso não é uniforme: concentra-se entre 30 e 90 dias (HR ≈ 0,62 nos dois grupos com AC), quando as audiências obrigatórias estão em pauta. Aos 90 dias, cerca de 13 a 14 p.p. a mais de processos estão sem sentença. Depois de 90 dias as taxas se igualam, mas o atraso já acumulado não é recuperado.

**A modalidade importa?** Para o **tempo**, não: Remota × Presencial tem log-rank p = 0,52, e entre os processos com AC realizada, HR = 1,13 (p = 0,34). Para **como** o processo termina, há indícios de diferença:

- a presencial produz mais extinções sem mérito (sHR = 1,46);
- a remota produz mais acordos (sHR = 1,87);
- ambas reduzem os julgamentos de mérito à metade (sHR ≈ 0,42–0,46).

**O achado principal é de mecanismo.** A comparação do tempo total **mascara efeitos opostos**: a AC obrigatória acelera extinções e acordos, mas atrasa fortemente o julgamento de mérito. Para a política judiciária, isso desloca a pergunta de "o rito é mais rápido?" para "o rito resolve mais conflitos?". Um ganho de acordos na remota (de 7,6% para 12,9% aos 180 dias) convive com mais extinções sem resolução e com menos e mais tardias decisões de mérito.

**Limitações.**

- O seguimento é curto: a cauda além de 180 dias não é estimável, e a pauta remota se estende até 24/11/2026.
- A data da AC não foi registrada, o que impede *landmark* e covariável tempo-dependente da audiência.
- O motivo da extinção sem mérito (ausência do autor ou outro) não está codificado; a hipótese do art. 51, I, é **compatível** com os dados, mas não verificada diretamente.
- É uma única unidade judiciária (validade externa).
''',
}
