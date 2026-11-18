# Textos de interpretação da Parte II (exploratória).
# Redigidos a partir das saídas reais do notebook executado; atualizar se os dados mudarem.

INTERP_EXPLORATORIA = {

'exp_medias_viesadas': r'''
**Leitura. As médias divulgadas foram reconstituídas, e nenhuma mede a duração dos processos.**

- **78,46 é uma média "mista".** Com as 944 linhas e a fórmula da planilha (sentenciados pela data da sentença, ativos até 07/10/2026), obtém-se 78,45 dias no geral e 77,00 / 77,48 / 80,87 em Controle / Presencial / Remota, contra 77,00 / 77,50 / 80,87 divulgados. É a média de durações completas com tempos parciais de 206 processos ainda ativos.
- **75,2 também é uma média mista, só que com corte anterior.** O resumo expandido não explica o cálculo. A mesma fórmula com corte em **23/09/2026** (véspera da data do arquivo do resumo, 24/09) dá 75,15 dias, e 74,10 / 76,61 / 74,74 por grupo, contra 74,22 / 76,67 / 74,72 publicados. As contagens do resumo (668 sentenciados e 275 ativos) não batem com essa data (712 e 232 na planilha atual), o que sugere que parte das sentenças foi lançada depois, com data retroativa. Logo, a "queda de 106,8 para 75,2 dias" compara a média histórica do GPS-Jus com uma média que mistura processos ainda em curso, e não é evidência de aceleração.
- **A média dos sentenciados é ainda menor e instável.** Em 07/10 ela vale 70,98 dias; até 03/08 eram só 499 sentenças, com média de 55,95 dias. No gráfico, as duas médias sobem quase linearmente com a data de corte: de 9,0 dias (só sentenciados, corte em 01/03) para 70,98 (07/10), enquanto a fração ainda sem sentença cai de 76% para 25%. Um estimador que depende tanto do dia em que se olha não mede uma propriedade dos processos; mede o tempo de observação.
- **A diferença entre os grupos também é artefato.** A Remota parece "mais lenta" na média mista (80,87) porque concentra entradas em julho (seção 2.1.3), e tem mais ativos com tempo parcial. A comparação válida é a das curvas de sobrevivência: a mediana do Kaplan-Meier de todos os processos é de **89 dias** (seção 2.4.2), acima de todas as médias divulgadas.
''',

'exp_seguimento': r'''
**Leitura. A entrada escalonada faz do mês de distribuição um determinante da censura.**

- O seguimento possível vai de 249 a 279 dias para os processos de janeiro e de só 68 a 98 dias para os de julho. Por isso a fração ainda ativa em 07/10 cresce com o mês: 2,9% (jan.), 0% (fev.), 7,3% (mar.), 10,9% (abr.), 15,8% (mai.), **37,1% (jun.)**, **63,7% (jul.)** e 83,3% dos 6 processos de agosto.
- **Os grupos não entraram no mesmo ritmo.** Em junho, a Presencial recebeu 59 processos, contra 39 do Controle e 34 da Remota; em julho, a **Remota recebeu 67**, contra 46 e 44. Como esses meses têm seguimento curto, a Presencial e, sobretudo, a Remota carregam mais censura por razões de calendário, e não de rito. A aderência mês a mês é testada na seção 2.5.1.
- **Consequência para a análise:** qualquer comparação ingênua entre grupos (médias, proporção de encerrados, χ² de grupo × situação, como no notebook do professor, E19) confunde o rito com o mês de entrada. O mês entra como covariável ou estrato nas Partes IV e V.
''',

'exp_swimmer': r'''
**Leitura.** Na amostra de 75 processos (25 por grupo), 56 terminaram em sentença, 3 em redistribuição e 16 seguem ativos. O gráfico deixa visíveis três padrões que as médias escondem:

- **As setas (censurados) se concentram em junho e julho.** Todas encostam na linha de 07/10, e o seu comprimento varia de pouco mais de 60 dias a cerca de 4 meses: são limites inferiores, não durações.
- **Há dois "relógios" nos desfechos.** As extinções sem mérito (círculos vermelho-tijolo) aparecem muitas vezes poucos dias após a distribuição, com segmentos curtíssimos; as sentenças de mérito (roxo-escuro) aparecem de 2 a 7 meses depois. Essa bimodalidade reaparece no histograma (seção 2.2.3) e na forma do risco (seção 2.4.1).
- **Processos distribuídos no mesmo dia podem ter destinos muito diferentes**, o que mostra a variabilidade individual que os testes e modelos precisam acomodar.
''',

'exp_freq_desenho': r'''
**Leitura. O desenho está equilibrado nos grupos, mas não no calendário.**

- **Grupos:** 313 (33,4%), 314 (33,5%) e 311 (33,2%), praticamente 1/3 cada. É um equilíbrio notável, analisado como evidência sobre o mecanismo do sorteio na seção 2.5.1.
- **Mês:** a distribuição não é uniforme. Janeiro e fevereiro têm cerca de 105 processos (recesso forense até 20/01 e mês curto); março a julho, de 132 a 157; agosto, só 6 (o sorteio terminou em 03/08). A % acumulada mostra que metade dos processos entrou até abril (53,0%) e o 2º ciclo (29/04 a 03/08) tem 453 processos (48,3%), contra 485 no 1º.
- **Dia da semana da distribuição:** segunda a quinta têm de 181 a 182 processos cada, sexta tem 157 e sábado e domingo têm 28 cada (3,0%). A distribuição eletrônica do PJe ocorre também nos fins de semana, de modo que essas datas são legítimas.
''',

'exp_freq_desfecho': r'''
**Leitura.**

- **Desfecho.** O Pareto mostra que mérito (341; 36,4%) e sem mérito (286; 30,5%) somam dois terços dos processos; com os 206 ativos (22,0%), chegam a 88,9%. Homologação de acordo (81; 8,6%) e redistribuição (24; 2,6%) são minoritárias. A taxa de 8,6% de homologações tem como denominador os distribuídos, inclusive os ativos; o índice de conciliação com o denominador correto (sentenças) está na seção 2.5.2.
- **Técnica.** Entre as 352 AC realizadas, as seis técnicas aparecem com frequências próximas, de 47 (Desconstrução; 13,4%) a 67 (Padrões objetivos; 19,0%), todas em torno da linha de 1/6 (58,7 audiências). O Pareto é quase plano: são necessárias cinco das seis técnicas para chegar a 80% dos casos. Não há sinal da hegemonia de "padrões objetivos" com 53,85% afirmada no resumo expandido; o teste está na seção 2.5.3.
''',

'exp_freq_ac': r'''
**Leitura. As taxas só têm sentido com o denominador certo.**

- **AC realizada:** 352 audiências (178 na Presencial e 174 na Remota). Os 513 "Não" incluem os 313 processos do Controle, em que a AC não existe no rito (zero estrutural), e 200 processos tratados em que a AC não ocorreu, em geral porque o processo foi extinto antes (seção 2.5.2). Os 73 sem informação são tratados ativos ainda sem audiência.
- **Acordo na AC:** 17 acordos, isto é, **4,8% das AC realizadas**. Os 1,8% sobre os 938 processos (como no notebook do professor, E30) diluem a taxa com o Controle, que não tem audiência.
- **Acordo fora da AC:** 64, quase quatro vezes os obtidos em audiência; o **acordo em qualquer momento** soma 81, exatamente o número de homologações. Os 205 "ativo (indefinido)" não são "sem acordo": o acordo ainda pode ocorrer. São 205, e não 206, porque um processo ativo já tem o campo de acordo preenchido ("Não") na planilha.
- **Híbrida:** 31 casos (3,6% dos válidos), 28 na Presencial e 3 na Remota, estes incongruentes com o protocolo (`desvio_protocolo`, 6 casos ao todo).
- **Indicadores de curadoria:** 12 processos de origem externa (1,3%), 38 desfechos no dia da distribuição (4,1%; seção 2.2.5), 135 desfechos datados em fim de semana (18,4% dos desfechos; seção 2.5.4), 4 números CNJ corrigidos e 5 números com linha duplicada removida. Todos são raros o bastante para análises de sensibilidade sem perda de poder.
''',

'exp_tempo_graficos': r'''
**Leitura. A distribuição dos tempos é bimodal, e a censura ocupa a cauda direita.**

- **(a) Histograma.** Há um primeiro pico na classe de 0 a 10 dias (cerca de 130 sentenças e a maior parte das redistribuições), formado por extinções sem mérito e declinações de competência; um vale entre 10 e 50 dias; e uma segunda moda entre 70 e 100 dias. Os ativos (cinza-claro) começam em 65 dias e pesam cada vez mais na cauda: acima de 150 dias já são quase metade dos tempos observados (38 ativos contra 40 sentenças) e, acima de 190 dias, a maioria (13 contra 6). A cauda direita da duração real está **escondida** na censura.
- **(b) Boxplots.** A mediana das sentenças (73,5 dias) fica abaixo da dos ativos (97 dias, que ainda vai crescer). A caixa "todos os observados" (mediana 80) parece uma distribuição comportada, mas é uma mistura sem significado. As redistribuições são quase todas imediatas (mediana de 1 dia).
- **(c) Violinos.** Cada tipo de desfecho tem a sua própria distribuição: mérito centrado perto de 100 dias, homologação perto de 60 e sem mérito com massa concentrada junto de zero e uma cauda até 200 dias. A distribuição global é a soma dessas três.
- **(d) ECDF.** A ECDF das sentenças sobe rapidamente até cerca de 20% nos primeiros dias (as extinções imediatas) e atinge 50% por volta de 73 dias. Por ignorar os 230 censurados, ela superestima a velocidade de encerramento: com censura, a mediana é de 89 dias (Kaplan-Meier, seção 2.4.2).
''',

'exp_tempo_desc': r'''
**Leitura das medidas descritivas (tabela da seção 2.2.2) e do QQ-plot.**

- **Sentenças (n = 708, condicional):** média 70,98 dias (EP 1,83), mediana 73,5 (IC95% *bootstrap* 70,0 a 78,0), moda 1 dia (47 sentenças), desvio-padrão 48,7, CV 68,7%, IIQ 76,25 (Q1 = 29, Q3 = 105,25), P90 = 133, máximo 225. A assimetria (0,21) e a curtose em excesso (−0,56) são próximas de zero, mas isso **não** indica normalidade: a distribuição é bimodal e truncada pela janela de observação, e a cauda direita foi cortada pela censura (exatamente o equívoco de leitura do notebook do professor, E15). O MAD reescalado (54,1) é maior que o desvio-padrão (48,7), sinal de distribuição "achatada" (platicúrtica), e não de caudas pesadas; a média aparada a 10% (68,9) fica perto da média.
- **Ativos (n = 206):** o tempo já decorrido vai de 65 a 274 dias (mediana 97). São limites inferiores: a duração final será maior.
- **Redistribuições (n = 24):** mediana de 1 dia e média de 11,3; quase todas são declinações imediatas.
- **Todos os observados (n = 938):** média 78,35 e mediana 80. Não estimam nada (mistura de durações completas, parciais e de saídas da vara).
- **QQ-plot.** Os pontos formam um "patamar" horizontal na cauda esquerda (os tempos próximos de zero, muito mais frequentes do que uma normal admitiria, e sem valores negativos possíveis) e, no centro e na cauda direita, acompanham a reta com curvatura leve. O desvio é de forma (bimodalidade e limite inferior em zero), e é testado formalmente na seção 2.3.
''',

'exp_outliers': r'''
**Leitura.** Com Q1 = 29,0 e Q3 = 105,2 dias, as cercas de Tukey são −85,4 e 219,6 dias. Há **um único valor atípico** entre as 708 sentenças: um processo do Controle distribuído em 12/01/2026 e julgado no mérito em 25/08/2026, após 225 dias. Ele é mantido: é uma duração plausível para um processo contencioso, e não um erro de data. Três processos ativos já ultrapassaram a cerca superior; quando forem sentenciados, serão atípicos "certos". Isso mostra que a raridade de atípicos entre os sentenciados é, em parte, produto da censura: os processos longos ainda não terminaram. Remover atípicos numa variável de tempo seria eliminar justamente a informação de maior interesse para a gestão.
''',

'exp_tempo_zero': r'''
**Leitura.** Há **38 processos com desfecho no próprio dia da distribuição** (4,1%): 33 sentenças sem mérito (4,7% das sentenças; 7 no Controle, 13 na Presencial e 13 na Remota) e 5 redistribuições. Em nenhum deles houve AC, e só um tem origem externa. São atos imediatos do juízo, típicos de indeferimento da inicial, desistência ou extinção por incompetência, e não erros de registro. Somando os primeiros 7 dias, são 123 sentenças, 121 delas sem mérito. Esse bloco de extinções precoces explica o pico inicial do histograma e do risco (seção 2.4.1) e tem tamanho parecido nos três grupos (39, 48 e 34 extinções sem mérito até 7 dias; tabela por faixa de tempo na seção 2.5.2). Nos modelos paramétricos, os zeros recebem 0,5 dia; a seção 2.4 mostra que trocar esse valor por 0,1 ou 1 dia não muda a escolha do modelo.
''',

'exp_normalidade': r'''
**Leitura. A normalidade é rejeitada, como se esperava, e a rejeição se deve à forma da distribuição, não a um detalhe.**

- **Total das sentenças (n = 708):** os cinco testes rejeitam H0 após Holm (Shapiro-Wilk W = 0,960; D'Agostino K² = 23,2; Anderson-Darling A² = 6,42; Lilliefors D = 0,083; Jarque-Bera JB = 14,7; todos com p ajustado ≤ 0,005).
- **Por grupo:** de 20 testes, 17 rejeitam. Os únicos que não rejeitam são os baseados em momentos (D'Agostino e Jarque-Bera) no Controle e o Jarque-Bera na Remota. Isso é coerente com os gráficos: a assimetria e a curtose desses grupos estão perto de zero (Controle: 0,38 e 0,07; Remota: 0,06 e −0,69), e os testes de momentos não "veem" a bimodalidade. Shapiro-Wilk, Anderson-Darling e Lilliefors, que comparam a forma inteira, rejeitam em todos os grupos.
- **Gráficos.** Os QQ-plots mostram o mesmo patamar junto de zero em todos os grupos (a massa de extinções precoces); os histogramas mostram o pico em 0 a 10 dias separado da moda principal; e a maior distância entre a ECDF e a normal (Lilliefors) está sempre entre 9 e 12 dias, exatamente na transição entre os dois "relógios".
- **Consequências.** (i) A comparação dos tempos dos sentenciados na Parte III deve usar testes não paramétricos (Kruskal-Wallis, Mann-Whitney), e não ANOVA ou teste t; (ii) mais importante, a pergunta relevante para os dados censurados não é a normalidade, mas a forma da função de sobrevivência e do risco, examinada na seção 2.4; (iii) o teste do notebook do professor em uma subamostra de 500 casos com censurados misturados (E22), com Shapiro-Wilk rejeitando e D'Agostino não, refletia essa mesma diferença entre testes de forma e testes de momentos, e não uma ambiguidade dos dados.
''',

'exp_ajuste_censurado': r'''
**Leitura. Nenhuma distribuição paramétrica usual descreve bem o tempo até a sentença; a forma do risco é não monótona.**

- **Critérios de informação.** A exponencial por partes (7 parâmetros) tem o menor AIC (7.782,5) e o menor BIC (7.816,4). Entre os paramétricos, a gama generalizada é a melhor (AIC 7.839,7; ΔAIC = 57), seguida de longe pela exponencial (7.992,1) e pela Weibull (7.993,9), que são praticamente o mesmo modelo (o parâmetro de forma da Weibull é ≈ 1). A log-logística (8.194,7) e a log-normal (8.303,6) são as piores.
- **TRV.** A gama generalizada rejeita os três modelos encaixados: contra a exponencial, TRV = 156,5 com 2 g.l.; contra a Weibull, 156,3 com 1 g.l.; contra a log-normal, 465,9 com 1 g.l. (todos p < 0,001, também após Holm). O parâmetro λ estimado (2,45) está longe tanto de 1 (Weibull) quanto de 0 (log-normal) (COLOSIMO; GIOLO, 2006, p. 93-94).
- **Gráficos.** Os QQ-plots com censura e os gráficos Ŝ_KM × Ŝ_modelo têm a forma de "S" em todos os modelos de 2 parâmetros: o maior afastamento entre o KM e o modelo é de 0,135 (exponencial), 0,138 (Weibull), 0,196 (log-logística) e 0,207 (log-normal). A gama generalizada reduz para 0,117, e só a exponencial por partes acompanha o KM de perto (0,074). Na sobreposição de curvas, os modelos de 2 parâmetros cruzam o KM: subestimam S(t) entre 20 e 100 dias e a superestimam depois de 120 dias.
- **Sensibilidade aos tempos zero.** Com os zeros substituídos por 0,1, 0,5 ou 1 dia, a exponencial por partes continua com o menor AIC (7.782,1 a 7.783,0) e a gama generalizada continua em segundo (7.809,6 a 7.851,3). Só a ordem entre a exponencial e a Weibull, praticamente empatadas, se inverte com 0,1 dia. As famílias em escala logarítmica (log-normal, log-logística, gama generalizada) são as mais sensíveis ao valor escolhido, como se esperava, mas nenhuma conclusão muda.
- **Medianas implícitas.** A exponencial por partes dá 88,2 dias, próxima da mediana do KM (89); os demais modelos dão de 62,6 (log-normal) a 76,2 (log-logística). Um modelo mal especificado erra, portanto, a quantidade mais importante para a gestão.
- **Consequência.** Os modelos AFT da Parte IV devem ser lidos com cautela e acompanhados de diagnóstico (Cox-Snell); as conclusões principais devem vir de métodos que não impõem forma ao risco (Kaplan-Meier, log-rank, Cox, RMST).
''',

'exp_risco': r'''
**Leitura. O risco de sentença tem três fases.**

1. **0 a 15 dias: pico inicial** (≈ 0,0117 sentença por processo-dia), produzido pelas extinções imediatas sem mérito (as redistribuições não entram: nesta análise são censuras, e não eventos);
2. **15 a 60 dias: vale** (0,0035 a 0,0047), o período em que o processo "espera" a citação, a contestação ou a pauta da audiência; quase ninguém é sentenciado;
3. **depois de 60 dias: subida e platô** (0,0114 entre 60 e 90 dias; 0,018 a 0,020 após 90 dias), quando os processos chegam à conclusão para sentença. Nesse platô, a meia-vida é de 35 a 39 dias: metade dos processos ainda sem sentença aos 90 dias é sentenciada em pouco mais de um mês.

Essa forma em "banheira invertida e depois subida" não pertence a nenhuma família padrão: a exponencial e a Weibull impõem um risco constante (≈ 0,0097); a log-normal e a log-logística, um risco que cai depois do início (o oposto do observado); e a gama generalizada capta a subida, mas a extrapola sem limite após 150 dias. Juridicamente, o vale entre 15 e 60 dias é o tempo processual mínimo do contraditório (citação, prazo de defesa e, nos tratados, a audiência). É nesse trecho que a AC obrigatória pode alongar o rito, o que se verifica na seção 2.6.1 e na Parte IV. Quando os riscos de dois grupos mudam de ordem ao longo do tempo, o log-rank perde poder, o que justifica testes ponderados e o RMST na Parte IV.
''',

'exp_scipy_encerrados': r'''
**Leitura. Ajustar só os sentenciados produz distribuições "mais rápidas" do que a realidade.**

- Entre os ajustes ingênuos, a gama tem o menor AIC (7.448,8), com a exponencial e a Weibull a menos de 6 pontos; a log-normal e a log-logística ficam muito atrás. Mas **todas** são rejeitadas pelo KS (p < 0,001; D de 0,175 a 0,247), mesmo sendo esse p-valor conservador: nenhuma família unimodal acomoda o pico em zero e a moda em 80 a 100 dias.
- **O viés de seleção aparece nas medianas.** As medianas implícitas dos ajustes só com sentenças vão de 36,6 (log-normal) a 51,5 dias (log-logística); com censura, as mesmas famílias dão de 62,6 a 76,2 dias, e a mediana do KM é de 89 dias. Desprezar os 230 processos não sentenciados subestima a mediana em 15 a 52 dias.
- É por isso que o ajuste do notebook do professor (E25), feito como se todos os tempos fossem completos e sem os zeros, não serve para descrever a duração: ele descreve, no máximo, a distribuição condicional dos processos que já terminaram.
''',

'exp_balanco': r'''
**Leitura. A divisão dos grupos é equilibrada demais para um sorteio simples, mas a sequência não tem a regularidade de blocos pequenos.**

- **Cauda direita (o teste usual):** X² = 0,0085 (944 linhas) e 0,0149 (938) com p ≈ 0,99: nenhum sinal de desequilíbrio.
- **Cauda esquerda ("bom demais"):** sob aleatorização simples, a probabilidade exata de uma divisão tão equilibrada quanto 314/316/314 é de **0,52%**, e quanto 313/314/311, de **1,05%**. Por Monte Carlo, a diferença entre o maior e o menor grupo seria ≤ 3 processos em só 1,06% dos sorteios; a diferença típica seria de 28 processos (P90 = 51). Isso é **indício** de aleatorização restrita (algum mecanismo garantiu totais iguais). A cautela é necessária porque a cauda esquerda foi escolhida depois de ver o equilíbrio, e não planejada de antemão.
- **Mas não blocos pequenos.** O desequilíbrio acumulado ao longo da ordem de chegada chega a D = 20 processos. Esse valor é típico tanto da aleatorização simples (mediana 21,7; P(D ≤ 20) = 0,42) quanto de uma urna com totais fixos (mediana 14,7; P(D ≤ 20) = 0,90). Com blocos de 3 ou 6, D nunca passaria de 2 a 4. O gráfico mostra a Remota acumulando um déficit de quase 20 processos até a posição 800 e **recuperando-o de uma vez no fim** (julho: 67 Remotas contra 46 e 44).
- **Mês a mês:** a aderência a 1/3 só é marginal em junho (Presencial 59; p exato = 0,018) e julho (Remota 67; p = 0,044), e nenhuma resiste à correção de Holm (0,146 e 0,311).
- **Leitura conjunta.** O padrão é compatível com um sorteio sem reposição a partir de totais preestabelecidos (por exemplo, uma lista equilibrada embaralhada no sorteio.com.br) ou com uma compensação deliberada no fim do período. As duas hipóteses preservam a validade da comparação, mas precisam ser **documentadas**: a segunda tornaria a alocação de julho parcialmente previsível. Como julho também é o mês de seguimento mais curto, a concentração de Remotas nele reforça a necessidade de ajustar pelo mês (Partes IV e V). O teste de corridas da sequência é feito na Parte III.
''',

'exp_binom_acordo': r'''
**Leitura. O índice de conciliação durante o experimento não difere do patamar histórico; a audiência, sozinha, fica muito abaixo dele.**

- **Índice de conciliação (homologações ÷ sentenças).** No total, 81 de 708 sentenças, ou **11,4%** (IC95% de Clopper-Pearson: 9,2% a 14,0%), compatível com os 13,3% históricos da unidade (p = 0,150; Holm 0,451). Por grupo: Controle **8,0%** (5,0% a 12,0%), abaixo do patamar (p = 0,011; Holm 0,042); Presencial 10,9% (7,2% a 15,6%) e Remota **16,2%** (11,6% a 21,8%), ambas compatíveis com 13,3% (Holm 0,456). Nenhum grupo atinge com segurança o índice nacional dos JECs (17,2%). O IC de Wilson é praticamente igual ao exato em todos os casos.
- **Acordo na AC (acordos ÷ AC realizadas):** 17 de 352, ou **4,8%** (2,8% a 7,6%); Presencial 5,1% (9/178) e Remota 4,6% (8/174), todos muito abaixo de 13,3% (p < 0,001). A comparação de denominadores (audiências × sentenças) é imperfeita, mas a ordem de grandeza é inequívoca: **a audiência inaugural produz cerca de um acordo a cada 20 sessões**.
- **Leitura jurídica.** O que distingue a Remota é o acordo **fora** da audiência (27 dos 35), e não a AC. A hipótese do projeto ("a audiência obrigatória aumenta os índices de conciliação") tem, por ora, apoio fraco e indireto: os grupos tratados têm índice nominalmente maior que o Controle, mas a diferença entre grupos é testada na Parte III, e, como os acordos encerram os processos mais cedo, o índice entre as sentenças já proferidas tende a cair quando as sentenças de mérito dos ativos chegarem. A taxa de 8,06% do resumo expandido (acordos ÷ distribuídos) mistura essa questão com a censura.
''',

'exp_binom_semmerito': r'''
**Leitura. Os grupos com AC obrigatória têm mais extinções sem mérito, e o excesso está nas extinções tardias (após 30 dias), não nas precoces. O tamanho da diferença depende do denominador.**

- **Sobre as sentenças (limite superior).** Controle **30,2%** (79/262; IC95% exato 24,7% a 36,1%), Presencial **47,4%** (109/230; 40,8% a 54,1%) e Remota **45,4%** (98/216; 38,6% a 52,3%): 17,2 e 15,2 pontos percentuais a mais. Essa base exagera a diferença, porque os tratados têm mais processos ainda ativos, e esses tendem a terminar em mérito. O binomial contra a taxa do Controle fixada dá p < 0,001, mas ignora a incerteza do próprio Controle e serve só como indicação; o teste de duas amostras está na Parte III.
- **Sobre os distribuídos (limite inferior).** Controle **25,2%** (20,7% a 30,3%), Presencial **34,7%** (29,7% a 40,1%) e Remota **31,5%** (26,6% a 36,9%): 9,5 e 6,3 pontos a mais. Nessa base, os IC da Remota e do Controle se sobrepõem. A diferença real fica entre os dois limites; a estimativa que respeita a censura e o risco competitivo é a incidência acumulada de extinção sem mérito (CIF) da Parte IV.
- **Quando ocorrem.** Nos tratados, a maioria das extinções sem mérito acontece **sem que a AC tenha ocorrido**: 89 na Presencial e 63 na Remota, com mediana de **5 e 6 dias**. Nos processos com AC realizada, as extinções sem mérito são 20 e 35, com mediana de 75,5 e 81 dias, compatíveis com a extinção na própria audiência ou depois dela.
- **Onde está o excesso** (tabela por faixa de tempo). Até 7 dias: 39 (Controle), 48 (Presencial) e 34 (Remota), ou 12,5%, 15,3% e 10,9% dos distribuídos. De 8 a 30 dias: 14, 16 e 16 (4,5%, 5,1% e 5,1%). Após 30 dias: **26, 45 e 48** (**8,3%, 14,3% e 15,4%**). O bloco precoce existe nos três grupos e difere pouco: só a Presencial fica cerca de 3 pontos acima do Controle. A diferença principal, de 6 a 7 pontos, está nas extinções tardias, que coincidem com a fase da audiência.
- **Leitura jurídica.** A hipótese do art. 51, I, da Lei 9.099/1995 (ausência do autor à audiência) explica bem o excesso tardio (os 55 casos com AC realizada e as extinções após 30 dias). As extinções com 5 a 6 dias de distribuição ocorrem **antes** de qualquer audiência e aparecem em volume semelhante no Controle; não são, portanto, efeito principal da AC obrigatória: são atos iniciais do juízo (indeferimento, desistência, incompetência) comuns aos três ritos. Isso altera a composição dos desfechos e, com ela, o tempo médio (seção 2.6.1). O motivo de cada extinção precisa ser conferido no PJe; o teste de duas amostras está na Parte III, e a análise por tipo de desfecho (riscos competitivos), na Parte IV.
''',

'exp_tecnica': r'''
**Leitura. O sorteio das técnicas é compatível com um sorteio uniforme entre seis técnicas; o "53,85%" do resumo expandido não se confirma.**

- **Aderência a 1/6:** nas 352 AC realizadas, X² = 3,91 com 5 g.l., p = 0,563 (Monte Carlo 0,566). Por grupo: Presencial p = 0,54 e Remota p = 0,55 (Holm = 1,0). As frequências vão de 47 a 67, dentro da variação esperada.
- **"Padrões objetivos":** 67/352 = **19,0%** (IC de Wilson 15,3% a 23,5%), compatível com 1/6 (p = 0,225) e também com 1/5 (p = 0,690), mas incompatível com 53,85% (p < 0,001). O valor do resumo não pode ser reproduzido com nenhum recorte da planilha atual: pode ter vindo de uma tabela dinâmica com outro denominador ou de uma versão anterior dos dados.
- **5 ou 6 técnicas?** A planilha registra seis técnicas, inclusive "Análise da comunicação verbal e não-verbal" (63 audiências; 17,9%). A anotação do professor ("o esperado era 1/5 = 20,0%") parte da lista de cinco técnicas do resumo expandido; o protocolo efetivamente executado usou seis, e o esperado é 1/6 ≈ 16,7%. Excluída a sexta técnica, o teste com 5 categorias também não rejeita (p = 0,466). O texto do resumo deve ser corrigido para seis técnicas.
- **Consequência.** Como o sorteio parece ter funcionado, a comparação de técnicas dentro das AC é um experimento aninhado legítimo; mas com 17 acordos distribuídos em seis técnicas (de 0 a 6 por técnica) o poder é muito baixo (Parte V).
''',

'exp_fimsemana': r'''
**Leitura.**

- **Há desfechos em fins de semana: 135 de 732 (18,4%; IC95% 15,7% a 21,4%).** Se a regra fosse "só dias úteis", qualquer caso a refutaria. A proporção é, porém, menor que a de uma data indiferente ao dia da semana (2/7 = 28,6%; p < 0,001).
- **Depende do tipo de ato.** As sentenças de **mérito** são assinadas em fins de semana na proporção de uma data uniforme (26,4%; p = 0,402): o magistrado redige e assina os julgamentos também aos sábados e domingos. Homologações (11,1%), extinções sem mérito (12,6%) e redistribuições (0 de 24) concentram-se nos dias úteis (p < 0,001 após Holm), o que é coerente com atos de rotina preparados pela secretaria.
- **Dias da semana:** a distribuição dos desfechos está longe da uniforme (X² = 117,4; 6 g.l.; p < 0,001), com um pico na terça-feira (186) e menos atos na segunda (90).
- **Leitura jurídica.** A data registrada é a da **assinatura eletrônica** no PJe, que funciona todos os dias. As sentenças de fim de semana não indicam erro de registro; indicam o ritmo de trabalho do gabinete e confirmam que o momento da sentença está sob controle direto do juiz-pesquisador, limitação de validade interna já apontada (ausência de cegamento). Uma conferência por amostragem no PJe é recomendável.
''',

'exp_biv_tempo': r'''
**Leitura. Entre os sentenciados, o grupo quase não explica o tempo; o tipo de desfecho explica muito, e ele difere entre os grupos.**

- **Grupo:** medianas de 72 (Controle), 71 (Presencial) e 77 dias (Remota); η² = 0,000. Comparar os tempos dos sentenciados por grupo não mostra diferença, mas essa comparação é condicional e enviesada (os tratados têm mais ativos ainda sem sentença).
- **Tipo de desfecho:** η² = 0,424. Mérito tem mediana de 97 dias; homologação, 61; sem mérito, 20,5.
- **Dentro de cada tipo, os tratados são mais lentos.** A mediana das sentenças de mérito é de **83 dias no Controle**, contra **112,5 na Presencial** e **106 na Remota** (médias 91,1 / 114,4 / 110,1); a das extinções sem mérito é de 9, 24 e 28,5 dias. Nas homologações, as medianas são próximas (61, 57 e 62). Como os tratados têm mais extinções sem mérito (sobretudo após 30 dias; seção 2.5.2), a mistura dos tipos "compensa" o atraso dos julgamentos de mérito, e as medianas globais ficam iguais: é um **efeito de composição**. O tempo "a mais" de 23 a 30 dias no mérito é compatível com a etapa adicional da audiência, mas também é **condicional** aos sentenciados. Os tratados têm mais ativos, que serão justamente os méritos mais demorados, e por isso a diferença entre os sentenciados tende a **subestimar** o atraso. Como o tipo de desfecho é posterior ao sorteio, a comparação dentro do tipo descreve o mecanismo, e não um efeito causal; a estimativa com censura está na Parte IV.
- **Mês:** η² = 0,047; as medianas caem nos meses tardios (jul.: 52,5 dias), por puro efeito de censura (só os rápidos já terminaram).
- **Acordo:** os processos com acordo terminam em 61 dias (mediana), contra 76 sem acordo; η² = 0,001, porque o grupo "sem acordo" mistura extinções imediatas e méritos longos.
- **Híbrida** (Presencial com AC): 113 contra 105 dias (n = 21 e 107; η² = 0,010). **Técnica** (AC realizadas): medianas de 95 a 118 dias, η² = 0,018. Ambas são variáveis pós-sorteio com poucos casos: diferenças descritivas, sem valor causal.
''',

'exp_calendario': r'''
**Leitura.** Em 07/10/2026, o Controle tinha 83,7% dos seus processos sentenciados (262/313), contra 73,2% da Presencial (230/314) e 69,5% da Remota (216/311). As curvas de sentenças acumuladas andam juntas até maio e se separam a partir de junho, com o Controle à frente. Parte dessa distância é calendário: as linhas tracejadas mostram que a Remota recebeu mais processos no fim (julho), que ainda não tiveram tempo de terminar. Outra parte pode ser efeito do rito (a etapa da audiência). Separar as duas coisas exige comparar processos **da mesma idade**, que é o que fazem o Kaplan-Meier e o Cox com o mês como covariável (Parte IV). A proporção de encerrados por grupo em uma data fixa, usada no notebook do professor (χ² de grupo × situação, E19), não faz essa separação.
''',

'exp_crosstabs': r'''
**Leitura (as associações são testadas na Parte III).**

- **Grupo × tipo de desfecho.** Na % na linha, o Controle tem 51,8% de sentenças de mérito, contra 30,6% (Presencial) e 26,7% (Remota); e menos extinções sem mérito (25,2% contra 34,7% e 31,5%). Os ativos são 14,7%, 23,6% e 27,7%. Na % na coluna, 47,5% de todas as sentenças de mérito vêm do Controle, e 43,2% das homologações vêm da Remota. No mosaico, as faixas não se alinham: a estrutura de desfechos muda com o rito.
- **Grupo × acordo.** Com acordo: 6,7% (Controle), 8,0% (Presencial) e 11,3% (Remota) dos processos; a categoria "indefinido" (ativos) cresce na mesma ordem, o que torna qualquer comparação de taxas de acordo sobre os distribuídos sensível à censura.
- **Grupo × mês.** A composição é parecida de janeiro a maio (cada grupo entre 29% e 38% de cada mês). As exceções são junho, com 44,7% de Presencial, e julho, com 42,7% de Remota (seção 2.5.1).
- **Técnica × acordo na AC.** As taxas de acordo vão de 0% (Afago, 0/58) a 10,5% (Parafraseamento, 6/57) e 8,3% (Separação, 5/60). As demais ficam entre 3,0% e 4,3%. Com 17 acordos no total, as diferenças são frágeis (células com 0 a 6 eventos).
''',

'exp_assoc_matriz': r'''
**Leitura. A matriz do professor era tautológica; a matriz correta separa associações estruturais de associações empíricas.**

- **Reprodução do erro (E6, E16).** As quatro colunas de duração da planilha coincidem em todas as linhas em que existem (943, 943, 943 e 428), e a matriz de Spearman entre elas dá 1,0 em todas as células: é a mesma variável, não uma correlação. Por isso a resposta à questão 2.7 é **não**: a matriz inicial não é adequada.
- **Associações estruturais (fortes por definição):** acordo × tipo de desfecho (V = 1,00: acordo ⇔ homologação); ciclo × mês (0,97); acordo × acordo fora (0,88); grupo × AC realizada (0,62: o Controle não tem AC); grupo × híbrida (0,23). A célula técnica × AC realizada fica vazia porque a técnica só existe quando há AC. Nenhuma delas é achado.
- **Associações empíricas relevantes:**
  - **grupo × tipo de desfecho, V = 0,16** (fraca a moderada): a composição dos desfechos muda com o rito, inclusive porque a categoria "Ativo" é maior nos tratados (seções 2.5.2 e 2.6.3);
  - **tipo de desfecho × ciclo (0,41) e × mês (0,27):** efeito da censura (os meses tardios ainda não têm sentenças de mérito);
  - **tempo × tipo de desfecho, η = 0,65**, e **tempo × AC realizada, η = 0,52:** a etapa processual define o tempo;
  - **tempo × mês, η = 0,22:** censura de novo;
  - **tempo × grupo, η = 0,02:** desprezível entre os sentenciados (mas ver o efeito de composição na seção 2.6.1);
  - **grupo × mês, V = 0,06:** fraca, mas com as concentrações de junho e julho vistas acima;
  - **desfecho em fim de semana × tipo, V = 0,19** (seção 2.5.4).
- **Leitura geral.** As variáveis pós-sorteio (AC, acordo, tipo de desfecho) estão fortemente associadas ao tempo, e o grupo se associa ao tempo **através** delas. Isso orienta a modelagem: o efeito total do rito se estima sem essas variáveis (Parte IV); os mecanismos, com riscos competitivos e análises restritas às AC.
''',

'exp_ordem_tempo': r'''
**Leitura (questão 2.7). A correlação negativa entre ordem de chegada e tempo é artefato; na janela comum, ela se inverte: quem chegou depois demorou mais.**

- **Versões ingênuas.** Só com os sentenciados, ρ = **−0,118** (p = 0,002; τ_b = −0,082, p = 0,001). Com todos os tempos observados, ρ = −0,041 (p = 0,211), mas τ_b = −0,050 (p = 0,024). A discordância entre os dois coeficientes indica uma relação muito fraca, que eles ponderam de forma diferente (τ_b conta pares concordantes; ρ, distâncias entre postos), e não um achado. Em ambas as versões, o sinal negativo é o esperado pelo mecanismo da censura: no primeiro gráfico, os pontos ficam sob o "teto" do seguimento máximo (ρ = −1 entre ordem e seguimento, por construção), e a curva LOWESS dos sentenciados cai depois da posição 600, porque os processos de junho e julho só aparecem como sentenciados se forem rápidos.
- **Versão justa: sentença em até 65 dias.** Como todos os processos têm pelo menos 65 dias de seguimento, esse indicador é observado para todos, sem censura. Quem chegou depois foi sentenciado com **menos** frequência na janela: ρ = **−0,156** (p < 0,001; τ_b = −0,127). Foram sentenciados em até 65 dias 38,1% dos processos do 1º ciclo (IC95% 33,9% a 42,5%), contra 26,5% dos do 2º ciclo (22,6% a 30,7%). O tempo truncado, min(tempo, 65), aponta na mesma direção (ρ = +0,138; tempo maior = mais lento), mas 65,2% dos processos valem exatamente 65 dias (empates) e as redistribuições precoces contam como "rápidas". Por isso ele é só um complemento.
- **E isso só nos tratados.** No Controle, ρ = −0,058 (p = 0,304), e a fração sentenciada em até 65 dias passa de 37,8% (1º ciclo) para 32,6% (2º ciclo). Na Presencial, ρ = −0,176 (p = 0,002), de 40,0% para 29,2%. Na Remota, ρ = −0,224 (p < 0,001), de 36,6% para 18,4%. O segundo gráfico mostra a queda mês a mês: de janeiro (44% na Remota, 56% na Presencial) para julho (13% e 20%), enquanto o Controle oscila entre 28% e 44% sem tendência. A leitura mais provável é o **congestionamento da pauta de audiências**: à medida que o experimento avançou, a fila de AC (presenciais até 22/10 e remotas até 24/11) alongou o início dos processos tratados, o que não aconteceu no rito sem audiência.
- **Resposta à questão 2.7.** É possível investigar a relação entre a ordem de chegada e a duração, com Spearman ou Kendall (a ordem é ordinal), mas não sobre `duracao_proc` bruta, que mistura censurados; é preciso uma janela comum (como aqui) ou um modelo de sobrevivência com a ordem ou o mês como covariável (Partes IV e V). O resultado aponta uma **interação entre rito e calendário**, relevante para a validade interna: o efeito da AC obrigatória sobre o tempo parece ter crescido ao longo do experimento.
''',

'exp_sintese': r'''
**Síntese da Parte II.**

1. **A variável-alvo é censurada.** São 708 sentenças, 206 ativos e 24 redistribuições, com seguimento de 65 a 279 dias que depende do mês de entrada. Todas as médias divulgadas (78,46 e 75,2) foram reconstituídas como médias "mistas" de durações completas e tempos parciais, e crescem com a data de corte; a mediana com censura (Kaplan-Meier) é de 89 dias.
2. **A distribuição é bimodal** (extinções imediatas × julgamentos de mérito por volta de 100 dias), não normal (17 de 20 testes rejeitam após Holm) e com risco não monótono: pico inicial, vale entre 15 e 60 dias e platô depois de 90. Nenhuma distribuição paramétrica usual se ajusta bem; a gama generalizada é a melhor delas e a exponencial por partes, a melhor de todas. Isso favorece métodos não paramétricos e semiparamétricos.
3. **O sorteio dos grupos** produziu totais equilibrados demais para uma aleatorização simples (P = 1,05%, num teste de cauda escolhido a posteriori: indício, não prova), sem a regularidade de blocos pequenos, e com concentrações em junho (Presencial) e julho (Remota). Isso deve ser documentado, e o mês deve entrar nos modelos. **O sorteio das técnicas** é compatível com o uniforme entre seis técnicas; o "53,85%" do resumo expandido não se confirma.
4. **Proporções.** O índice de conciliação (homologações ÷ sentenças) é de 11,4%, compatível com o histórico de 13,3%; o acordo na AC é de 4,8% das audiências. Os tratados têm mais extinções sem mérito: de 15 a 17 pontos percentuais a mais sobre as sentenças (limite superior) e de 6 a 10 pontos sobre os distribuídos (limite inferior). O excesso está nas extinções **tardias**, após 30 dias, na fase da audiência (8,3% dos distribuídos no Controle, contra 14,3% e 15,4%). O bloco de extinções imediatas existe nos três ritos. A estimativa com censura (CIF) está na Parte IV.
5. **Relações bivariadas.** Entre os sentenciados, o grupo não explica o tempo (η² = 0,000), mas, dentro de cada tipo de desfecho, os tratados são mais lentos (mérito: 83 dias no Controle, contra 106 a 112,5 nos tratados; comparação condicional, que tende a subestimar o atraso). Na janela comum de 65 dias, observada sem censura, a fração sentenciada caiu do 1º para o 2º ciclo nos tratados (Presencial: 40,0% para 29,2%; Remota: 36,6% para 18,4%), e quase não mudou no Controle (37,8% para 32,6%).

**Hipóteses levadas às Partes III a V:** (i) a AC obrigatória alonga o tempo até a sentença de mérito e muda a composição dos desfechos; (ii) o efeito cresce com o calendário (pauta); (iii) o efeito sobre o acordo, se existe, vem dos acordos fora da audiência. As três exigem comparar processos da mesma idade, com censura, o que só a análise de sobrevivência faz.
''',

}
