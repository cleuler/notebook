# Textos de interpretação da Parte III (testes de hipóteses).
# Redigidos a partir das saídas reais do notebook executado (base primária, N = 938); atualizar se os dados mudarem.

INTERP_TESTES = {

'tst_plano': r'''
**Síntese do plano.** São doze perguntas (H1 a H12), cada uma com uma razão jurídica ou de desenho para existir. Três escolhas organizam o restante da parte:

- **O desfecho principal da pesquisa (tempo até a sentença) não é testado aqui com testes clássicos de forma conclusiva.** Ele é censurado em 22% dos processos, e a resposta válida está na Parte IV. Na seção 3.4, os testes clássicos de tempo aparecem só para mostrar o que eles dizem e o que deixam de dizer.
- **O que os testes clássicos respondem bem neste desenho** são perguntas sobre **proporções e tipos de desfecho** (H1 a H7), sobre a **aleatorização** (H9, H11) e sobre a **associação com a ordem de chegada** (H10), desde que a censura seja neutralizada pela janela comum de 65 dias.
- **Os testes descartados** (Encerrado × Ativo, z com p₀ = 0,5, Controle × acordo na AC, correlação entre cópias da mesma variável) eram os que davam ao notebook do professor os valores-p mais "impressionantes". São justamente os que não informam nada sobre o rito.
''',

'tst_desfecho': r'''
**Leitura. O rito muda o tipo de sentença, e a mudança tem uma explicação jurídica clara.**

- **Há associação entre tipo de sentença e grupo** (χ²(4) = 34,34; p < 0,001; esperadas ≥ 24,7). O efeito é **pequeno a moderado**: V de Cramér = 0,16 (IC 95% 0,11 a 0,21).
- **A diferença está entre o Controle e os braços com AC, e não entre as duas modalidades:**
  - Presencial × Controle: V = 0,20, p Holm < 0,001;
  - Remota × Controle: V = 0,24, p Holm < 0,001;
  - Presencial × Remota: V = 0,08, p = 0,252.

  Para o tipo de desfecho, **"ter AC obrigatória" importa; a modalidade, não**.
- **A hipótese do art. 51, I, da Lei 9.099/1995 é compatível com os dados.** Ela foi gerada pela própria descrição da Parte I (seção 3.1.2), então os valores-p abaixo são otimistas. Entre os sentenciados (análise condicional):
  - **sem mérito:** 30,2% no Controle, contra 47,4% no Presencial e 45,4% na Remota. Presencial × Controle: OR = 2,09 (IC 1,42 a 3,07), diferença de +17,2 p.p. (IC de Newcombe 8,6 a 25,5). Remota × Controle: OR = 1,92 (1,30 a 2,85), +15,2 p.p. (6,5 a 23,7). Ambos com p Holm ≤ 0,005;
  - **mérito:** 61,8% no Controle, contra 41,7% e 38,4%. OR de 0,44 e 0,39, diferenças de −20 e −23 p.p., p Holm < 0,001;
  - os resíduos ajustados apontam as mesmas células: Controle × mérito = +5,6; Controle × sem mérito = −4,3.
- **O mecanismo aparece na tabela descritiva.** Nos braços com AC, quando a audiência **não** foi realizada, 87% (Presencial) e 78% (Remota) das sentenças são **sem mérito**. Quando foi realizada, predominam as de mérito (73% e 60%). A leitura compatível é que a AC obrigatória cria um ponto de "filtragem": o autor que não comparece tem o processo extinto (art. 51, I). Como `ac_realizada` é pós-sorteio, essa tabela mostra **onde** estão as extinções, não prova a causa; parte das AC "não realizadas" pode ser de processos extintos antes da data da audiência.
- **Homologação (acordo).** O global é significativo dentro da família (p Holm = 0,019), e o único par que se sustenta é **Remota × Controle**: 16,2% contra 8,0%, OR = 2,22 (1,21 a 4,15), p Holm = 0,033. Esse par não sobrevive ao Holm global (seção 3.7) e é discutido em horizonte fixo na seção 3.3.
- **A redistribuição não depende do rito**: 5, 10 e 9 casos; Fisher-Freeman-Halton por Monte Carlo, p = 0,393.
- **Sem censura, o que se mantém e o que não se mantém.** A comparação entre os sentenciados depende da data de corte, e por isso é repetida em horizontes fixos, com seguimento completo.
  - **Situação no 65º dia (938 processos):** a associação persiste: χ²(8) = 59,19, p < 0,001, V = 0,18 (0,15 a 0,23). Mérito até o 65º dia: 35 processos no Controle, contra 5 no Presencial e 2 na Remota (resíduo +7,0). Sem AC inaugural, o Controle consegue julgar o mérito cedo, provavelmente por julgamento antecipado após a contestação. "Sem desfecho até 65 dias" se concentra na Remota (+2,4).
  - **O déficit de mérito é robusto.** Ele aparece em todos os horizontes, com p Holm < 0,001 nos oito pares:
    - 90 dias: 8,0% (Presencial) e 7,8% (Remota), contra 30,6% (Controle);
    - 120 dias: 24,5% e 22,2%, contra 45,6%;
    - 150 dias: 35,0% e 30,2%, contra 53,5%;
    - de 90 a 150 dias, a diferença fica entre −18,5 e −23,4 p.p. (no 65º dia, cerca de −10 p.p.).
  - **O excesso de extinções sem mérito é menor e não sobrevive ao Holm em horizonte fixo.**
    - **Presencial:** +7,9 a +11,3 p.p. em todos os horizontes, com p bruto entre 0,02 e 0,04 e p Holm = 0,164 na família;
    - **Remota:** a diferença é nula até o 65º dia (20,6% contra 20,8%, p = 1,000) e cresce com o seguimento: +4,4 p.p. em 90 dias, +7,4 em 120 e +11,7 em 150 (p = 0,021; p Holm = 0,164).

    O "+15,2 p.p." da Remota entre os sentenciados mistura, portanto, efeito e calendário. A direção é a mesma, mas a magnitude depende de quanto seguimento cada braço teve.
- **Leitura jurídica.** A AC obrigatória não se limita a "acrescentar acordos": ela **adia e reduz os julgamentos de mérito** (achado robusto, sem censura) e **tende a aumentar as extinções sem mérito** (consistente na direção, mas sem significância após a correção nos horizontes fixos). Para a política judiciária, isso tem custo. Uma extinção por ausência não resolve o conflito, e o autor pode repropor a ação (art. 51, § 1º). O indicador "processos baixados" melhora sem que a resposta ao jurisdicionado melhore na mesma proporção.
''',

'tst_acordo': r'''
**Leitura. A AC obrigatória não produziu mais acordos *na audiência*. O excedente de acordos da Remota veio de fora dela e só aparece com seguimento maior.**

- **Acordo na AC, presencial × remota (H4).** Foram 9/178 (5,1%) contra 8/174 (4,6%). Fisher p = 1,000; OR = 1,11 (IC exato 0,37 a 3,38); diferença de +0,5 p.p. (IC de Newcombe −4,4 a +5,3).
  - O resultado é **compatível com igualdade**, mas o IC é largo. Com uma taxa-base de 4,8% e cerca de 175 audiências por braço, só um aumento de **≥ 8,4 p.p.** sobre a taxa-base teria 80% de poder.
  - Ou seja, o estudo **exclui grandes diferenças** entre as modalidades, mas não exclui diferenças de alguns pontos percentuais.
  - Em qualquer modalidade, a taxa de acordo na AC (~5%) é baixa. É coerente com o diagnóstico do Ipea e do CNJ sobre a baixa efetividade das audiências de conciliação nos JECs (INSTITUTO DE PESQUISA ECONÔMICA APLICADA, 2013).
- **Acordo em qualquer momento (H5), em horizonte fixo:**
  - **até 65 dias** (938 processos): 3,5% no Controle, 4,5% no Presencial e 6,1% na Remota; χ² p = 0,300. Nenhum par difere;
  - **até 120 dias** (688 com seguimento ≥ 120 d): 5,0%, 9,4% e 12,5%; χ²(2) = 8,00, p = 0,018. O par **Remota × Controle** difere: OR = 2,70 (1,28 a 6,01), +7,5 p.p. (2,3 a 13,0), p Holm = 0,020. Presencial × Controle fica no limite (+4,4 p.p., IC −0,3 a 9,3; p Holm = 0,150).
  - Esse sinal é o mesmo da homologação entre os sentenciados (seção 3.2.3). **Não sobrevive à correção global de Holm** sobre os 71 testes inferenciais da parte, só à de Benjamini-Hochberg (seção 3.7), e o próprio global da família passa no BH por pouco (0,047). É um achado **sugestivo**, a confirmar com a função de incidência acumulada do acordo (Parte IV).
- **De onde vem o excedente da Remota?** Não vem da AC, já que Presencial e Remota têm a mesma taxa na audiência. O acordo **fora** da AC até o 120º dia (688 processos com seguimento completo) é de 5,0% no Controle (12/239), 5,6% no Presencial (13/233) e 9,7% na Remota (21/216). O χ² dá p = 0,095, e o par Remota × Controle, +4,7 p.p. (IC −0,1 a 9,8), p Holm = 0,208. A versão condicional aos encerrados (7,9%, 6,7% e 11,9%; p = 0,107) aponta na mesma direção. A hipótese plausível, a testar com dados de movimentação, é que a AC remota sem acordo ainda aproxima as partes (contato, proposta registrada), e o acordo se fecha depois, por petição.
- **AC híbrida (H7):** 1/24 contra 8/154; Fisher p = 1,000, OR = 0,79 (0,02 a 6,41). Com 24 híbridas e 9 acordos, o teste é **não informativo**: o IC vai de "quase nunca" a "seis vezes mais". A híbrida também é escolha da parte (pós-sorteio).
- **Técnica (H7).** As taxas vão de 0/58 (Afago) a 6/57 (Parafraseamento).
  - O χ² observado é 9,48. A permutação de Monte Carlo dá p = 0,088 (estatística χ²), e o Fisher-Freeman-Halton por Monte Carlo dá **p = 0,080**. O p assintótico (0,092) é parecido, mas não é confiável aqui: todas as esperadas da coluna "acordo" estão entre 2,3 e 3,2.
  - **Não há evidência de que a técnica importe**, e com 17 acordos distribuídos por seis técnicas o teste tem poder muito baixo. A pergunta exigiria centenas de audiências por técnica.
  - O histograma de permutação mostra que, neste caso, a distribuição de referência fica próxima de um χ²(5). A permutação confirma o resultado, mas não o altera.
''',

'tst_tempo': r'''
**Leitura. Entre os sentenciados, os três grupos "levam o mesmo tempo". Esse resultado esconde dois efeitos opostos e é enviesado pela censura.**

- **Testes clássicos, só entre os sentenciados (708):**
  - **Kruskal-Wallis:** H = 0,33, p = 0,847, ε² = 0,0005, praticamente zero. Medianas: Controle 72, Presencial 71 e Remota 77 dias. O Dunn com Holm dá p = 1 em todos os pares;
  - **Mann-Whitney:** todos os deltas de Cliff estão entre −0,03 e +0,03, com ICs dentro de ±0,14 (efeito desprezível);
  - **mediana de Mood:** p = 0,520.
- **ANOVA e Welch (didático).** F = 0,13, p = 0,875; Welch p = 0,880. A conclusão é a mesma, mas os pressupostos falham:
  - **homocedasticidade:** Levene p = 0,005 e Brown-Forsythe p = 0,005 rejeitam a igualdade de variâncias. O Presencial é o mais disperso (P75 = 110 dias);
  - **normalidade:** Shapiro-Wilk rejeita nos resíduos dos três grupos (p < 0,001), e o Q-Q mostra caudas curtas, cortadas pela censura, e massa perto de zero.

  Com n ≈ 230 por grupo, o F é robusto o bastante para não errar a conclusão, mas não há razão para preferi-lo ao KW.
- **O efeito de composição.** Estratificando pelo tipo de sentença:
  - **mérito:** os braços com AC são **muito mais lentos**. Medianas: Controle 83, Presencial 112,5 e Remota 106 dias. KW H = 45,7, p Holm < 0,001, ε² = 0,13 (efeito médio). A AC inaugural acrescenta uma etapa antes da contestação, e o julgamento de mérito chega cerca de um mês depois;
  - **sem mérito:** as extinções saem cedo nos três grupos (medianas 9, 24 e 28,5 dias; p Holm = 0,465);
  - **homologação:** 61, 57 e 62 dias (p = 0,892).

  Os braços com AC têm **mais** extinções rápidas (sem mérito, mediana geral de 20 dias) e **menos** julgamentos de mérito (mediana geral de 97 dias). No agregado, a lentidão do mérito é compensada pela rapidez das extinções. O "nenhuma diferença" do agregado é um **paradoxo de composição**, não ausência de efeito. Ressalva: o tipo de sentença é pós-sorteio, então a estratificação descreve o mecanismo, mas não estima o efeito causal.
- **Por que o KW do professor dá p ≈ 0,5, e como isso muda (E14, E17).** Na base primária, a reprodução dá H = 1,16, p = 0,559 (no original, p = 0,478, com 944 linhas, duplicatas e "Decisão" como sentença). O teste mistura dois tipos de número:
  - durações reais dos encerrados;
  - **tempos de seguimento** dos ativos, que são 14,7% do Controle, 23,6% do Presencial e 27,7% da Remota. Os ativos não têm duração, e sim um piso: estão em tramitação há pelo menos 112, 100 e 89 dias (medianas).

  O grupo com mais ativos tem mais tempos "cortados", e o teste compara grandezas diferentes. Retirar os ativos (versão 2) não resolve: a comparação passa a ser entre os que encerraram rápido o bastante, e o p sobe para 0,847.
- **Versões sem censura.** Com a janela comum de 65 dias, observada para todos:
  - média de min(T, 65): 51,8, 49,9 e 53,1 dias (KW p = 0,135);
  - sentença até o 65º dia: 36,0%, 35,9% e 28,1% (χ² p = 0,063).

  A Remota já aparece mais lenta, embora sem significância nesse horizonte curto. Usando todo o seguimento com Kaplan-Meier e log-rank, a Parte IV encontra medianas de 81 dias no Controle, 96 no Presencial e 95 na Remota (log-rank de 3 grupos p = 0,023). **A conclusão muda** de "o rito não importa" (KW ingênuo) para "a AC obrigatória alonga a tramitação", e só um método que respeita a censura consegue mostrar isso.
- **E24 refeito (condicional).** Entre as AC realizadas já sentenciadas, os 17 processos com acordo na AC terminaram em 63 dias (mediana), contra 104 dias dos sem acordo (U = 816, p < 0,001, delta de Cliff = −0,61, IC −0,85 a −0,32). O efeito é grande, mas em boa parte é **definicional**: o acordo encerra o processo com a homologação, e quem não fez acordo segue para contestação e julgamento. A pergunta correta ("o acordo na AC antecipa o fim?") é de riscos competitivos (Parte IV).
''',

'tst_ordem': r'''
**Leitura. O sorteio parece aleatório, os braços com AC (não o Controle) ficaram mais lentos ao longo do ano e a correlação "ingênua" entre a ordem de chegada e o tempo é dominada pela censura.**

- **Aleatoriedade do sorteio (H9).**
  - **Número de corridas:** foram observadas R = 626 corridas, contra 626,3 esperadas sob H₀ (DP de permutação de 14,3; p = 1,000). Não há nem agrupamento nem rodízio regular.
  - **Maior corrida:** tem 8 processos seguidos, comprimento comum sob o acaso (P ≥ 8 = 0,239).
  - **Por grupo:** z = 0,43, 0,75 e −1,24, todos não significativos.

  A sequência é **compatível com sorteio aleatório**, o que reforça a classificação como ECA (questão 2.2). O teste não prova o mecanismo: uma lista pseudoaleatória bem feita e um sorteio físico dariam o mesmo resultado, e a ocultação da alocação continua sem documentação.
- **Composição mensal (H11).** χ²(12) = 18,45, p = 0,103, V = 0,10. No conjunto, o desequilíbrio não excede o acaso, mas os resíduos mostram dois meses atípicos: **junho**, com excesso de Presencial (+2,95), e **julho-agosto**, com excesso de Remota (+3,10; 71 de 163 processos). Como julho-agosto é o período com menos seguimento e mais ativos, a Remota recebe uma parcela maior de processos com pouco seguimento. Por isso o mês entra como estrato e covariável (seção 3.6 e Partes IV e V).
- **Ordem de chegada × tempo (H10, questão 2.7):**
  - **todos (938), censura ignorada:** ρ = −0,04 (p = 0,211), τ = −0,05 (p = 0,024). Spearman e Kendall discordam quanto à significância, um sinal de que a associação é fraca e frágil;
  - **só sentenciados:** ρ = −0,12 (p = 0,002). Este é o "achado" que uma análise ingênua reportaria: "os processos mais recentes são mais rápidos";
  - **janela comum de 65 dias**, sem censura: ρ = **+0,14** (p < 0,001; τ = +0,11). **O sinal se inverte**: os processos que chegaram depois demoram **mais**. A proporção sentenciada até o 65º dia cai de 46,0% (janeiro) para 20,8% (julho; agosto tem só 6 processos).
  - **Dentro de cada grupo**, o que também elimina a composição mensal desigual: Controle ρ = +0,05 (p = 0,342), Presencial ρ = +0,14 (p = 0,015) e Remota ρ = +0,22 (p < 0,001). A tendência é **dos braços com AC**, e não da vara como um todo; só a da Remota sobrevive ao Holm global. No Controle, a proporção sentenciada até 65 dias oscila entre 29% e 44% sem tendência; na Remota, cai de 46,7% (janeiro) para 13,6% (julho).
  - A leitura compatível é o **acúmulo da pauta de audiências**: cada processo dos braços com AC precisa de uma data de AC, e a fila cresce ao longo do experimento. É uma hipótese a confirmar com as datas de designação das audiências.
- **A simulação explica a inversão.** Em 500 réplicas, os tempos foram gerados **sem nenhuma relação** com a ordem e censurados com o acompanhamento real de cada processo. Sob essa H₀:
  - **só encerrados:** ρ médio = −0,28 (faixa de 95%: −0,34 a −0,21);
  - **todos, com a censura ignorada:** ρ médio = −0,19;
  - **janela de 65 dias:** ρ médio = 0,00.

  A censura sozinha "fabrica" uma correlação negativa forte. Os ρ observados (−0,12 e −0,04) ficam **acima** dessa faixa, ou seja, a associação verdadeira é positiva e parcialmente mascarada pela censura. A magnitude do artefato depende da distribuição simulada (Weibull de forma 1,6), mas o sinal não depende.
- **Resposta à questão 2.7 (seção 7.6).** Sim, é possível investigar a correlação entre a ordem de chegada e o tempo, com Spearman ou Kendall (a ordem é ordinal; nunca Pearson), **desde que** a censura seja tratada: janela comum de seguimento, como aqui, ou a ordem/data como covariável num modelo de Cox (Parte IV). Sem esse cuidado, a correlação mede o calendário de distribuição e não o ritmo da vara.
''',

'tst_professor': r'''
**Leitura (questão 2.11).**

- **Os testes reproduzidos dão valores-p "fortes" justamente onde a hipótese é vazia:**
  - **Encerrado × Ativo:** p < 0,001, e é tautológico;
  - **z com p₀ = 0,5:** z = 17,2, e 78,0% de encerrados não é comparável a nada;
  - **grupo × status:** p < 0,001, mas o status depende do mês de entrada;
  - **grupo × acordo na AC com o Controle:** p = 0,013. O "efeito" é o zero estrutural do Controle, e as esperadas da coluna "acordo" são 5,6 a 5,7, no limite de Cochran.
- **Testes sobre o tempo, a pergunta central, dão valores-p fracos porque o método é inadequado.** É o caso do KW (p = 0,559) e do Mann-Whitney com × sem acordo (p = 0,448). A exceção é o χ² tipo de sentença × grupo (E21), que trata de uma pergunta real e tem p forte. No restante, a significância estatística do notebook do professor anda **na contramão da relevância substantiva**.
- **Dos 14 testes do notebook:**
  - **um é adequado na ideia:** χ² tipo de sentença × grupo, refeito aqui sem a "Decisão", com resíduos e V;
  - **quatro devem ser removidos:** Encerrado × Ativo, z com p₀ = 0,5, matriz de correlação e dispersões tautológicas;
  - **os demais devem ser substituídos** por métodos que respeitem a censura (Parte IV), o zero estrutural (Fisher entre os braços com AC) ou a multiplicidade (Dunn/Holm).
- **CMH estratificado por mês (H12).** O desfecho é o acordo homologado até o 120º dia, entre os 688 processos com seguimento completo (meses de janeiro a junho).
  - **Remota × Controle:** OR bruto = 2,70 e OR de Mantel-Haenszel = **2,72 (IC 95% 1,34 a 5,51)**, χ²(1) = 8,30, p = 0,004 (p Holm = 0,008 na família). Breslow-Day p = 0,367: o OR é homogêneo entre os meses.
  - **Presencial × Controle:** OR MH = 1,98 (0,96 a 4,09), p = 0,060.
  - **Leitura.** O ajuste pelo mês **não altera** a razão de chances: o mês não confunde essa associação. A versão condicional aos encerrados dá o mesmo quadro (OR MH 2,17, p = 0,007, para a Remota). O resultado sobrevive ao BH, mas não ao Holm global (seção 3.7); a análise completa do acordo como desfecho concorrente está na Parte IV.
- **Outros testes aplicáveis (questão 2.11, seção 7.10).** CMH, permutação e exatos foram implementados aqui. Jonckheere-Terpstra e Cochran-Armitage servem para hipóteses de **tendência no mês** (por exemplo, a queda da proporção sentenciada até 65 dias, de 46% em janeiro para 21% em julho), não para o grupo, que é nominal. Brunner-Munzel e Kolmogorov-Smirnov ampliariam a comparação de distribuições, mas herdam o problema da censura. Testes pareados não se aplicam (questão 2.3).
''',

'tst_multiplicidade': r'''
**Leitura. O que sobrevive a qualquer critério, e o que é só condicional.**

- **Volume de testes.** A parte registrou **74 testes**. Três são **didáticos** e ficam fora da correção: a ANOVA de Welch e o Spearman com a censura ignorada ou só entre os sentenciados. Restam **71 inferenciais**, sendo 46 principais (sem censura) e 25 condicionais (só sentenciados ou estrato pós-sorteio). Dos inferenciais, são significativos a 5%: **33** sem correção, **28** com Benjamini-Hochberg (FDR) e **22** com Holm global (FWER).
- **Achados principais (sem censura) que sobrevivem ao Holm global, o critério mais exigente:**
  - **H1/H2 (tipo de desfecho).** A situação no 65º dia difere entre os grupos. O **déficit de julgamentos de mérito** nos dois braços com AC aparece em todos os horizontes fixos (65 a 150 dias), com diferenças de cerca de −10 p.p. no 65º dia e de −18 a −23 p.p. de 90 a 150 dias. **É o achado mais robusto da Parte III.**
  - **H10.** Correlação positiva entre ordem de chegada e tempo na janela sem censura (ρ = +0,14), concentrada nos braços com AC: só a da Remota (ρ = +0,22) sobrevive ao Holm global; a do Controle é nula (ρ = +0,05).
- **Sobrevivem ao Holm global, mas são condicionais** e não sustentam sozinhos uma conclusão:
  - associação tipo × grupo entre os sentenciados e os pares com OR (inclusive o excesso de sem mérito). O déficit de mérito é confirmado sem censura; o excesso de sem mérito, não: em horizonte fixo ele tem a mesma direção, mas p Holm = 0,164;
  - julgamentos de mérito mais lentos nos braços com AC (KW no estrato mérito, que é pós-sorteio);
  - E24 refeito: o acordo na AC encerra o processo mais cedo, o que é em boa parte definicional.
- **Sobrevivem só ao BH (FDR), como evidência sugestiva a confirmar:**
  - mais **acordo** na Remota que no Controle: acordo até 120 dias (OR 2,70) e CMH por mês na mesma janela (OR MH 2,72), ambos sem censura, mais a homologação entre os sentenciados (OR 2,22, condicional). Pela regra do porteiro, os globais dessas famílias também passam no BH, mas por pouco (0,047 e 0,048), e nenhum passa no Holm global;
  - a tendência ordem × tempo dentro do Presencial (ρ = +0,14).
- **Não rejeitados, com IC que informa o tamanho máximo plausível:**
  - acordo na AC presencial × remota: diferença de +0,5 p.p. (IC −4,4 a +5,3);
  - acordo fora da AC até 120 dias;
  - técnica e híbrida: sem poder;
  - redistribuição;
  - aleatoriedade do sorteio, compatível com H₀;
  - tempo agregado entre os sentenciados: delta de Cliff ≈ 0, um paradoxo de composição.
- **Leitura para a questão 2.11 (seção 7.10).** Sem correção de multiplicidade, sem tamanho de efeito (E27) e sem separar o condicional do sem censura, o notebook do professor não tinha como distinguir esses níveis de evidência. Com 71 testes a 5%, cerca de três ou quatro "significâncias" seriam esperadas só pelo acaso, se todas as H₀ fossem verdadeiras. Por isso, o achado de acordo da Remota, isolado, não autorizaria uma recomendação de política judiciária. Já a redução e o adiamento dos julgamentos de mérito autorizam.
''',

}
