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
- **A hipótese do art. 51, I, da Lei 9.099/1995 é confirmada nos dados.** Entre os sentenciados:
  - **sem mérito:** 30,2% no Controle, contra 47,4% no Presencial e 45,4% na Remota. Presencial × Controle: OR = 2,09 (IC 1,42 a 3,07), diferença de +17,2 p.p. (IC de Newcombe 8,6 a 25,5). Remota × Controle: OR = 1,92 (1,30 a 2,85), +15,2 p.p. (6,5 a 23,7). Ambos com p Holm ≤ 0,005;
  - **mérito:** 61,8% no Controle, contra 41,7% e 38,4%. OR de 0,44 e 0,39, diferenças de −20 e −23 p.p., p Holm < 0,001;
  - os resíduos ajustados apontam as mesmas células: Controle × mérito = +5,6; Controle × sem mérito = −4,3.
- **O mecanismo aparece na tabela descritiva.** Nos braços com AC, quando a audiência **não** foi realizada, 87% (Presencial) e 78% (Remota) das sentenças são **sem mérito**. Quando foi realizada, predominam as de mérito (73% e 60%). A leitura compatível é que a AC obrigatória cria um ponto de "filtragem": o autor que não comparece tem o processo extinto (art. 51, I). Como `ac_realizada` é pós-sorteio, essa tabela mostra **onde** estão as extinções, não prova a causa; parte das AC "não realizadas" pode ser de processos extintos antes da data da audiência.
- **Homologação (acordo).** O global é significativo dentro da família (p Holm = 0,019), e o único par que se sustenta é **Remota × Controle**: 16,2% contra 8,0%, OR = 2,22 (1,21 a 4,15), p Holm = 0,033. Esse par não sobrevive ao Holm global (seção 3.7) e é discutido em horizonte fixo na seção 3.3.
- **A redistribuição não depende do rito**: 5, 10 e 9 casos; Fisher-Freeman-Halton por Monte Carlo, p = 0,393.
- **A conclusão não é um artefato de "quem já encerrou".** Na janela de 65 dias, observada para os 938 processos, a associação persiste e é até mais forte: χ²(8) = 59,19, p < 0,001, V = 0,18 (0,15 a 0,23).
  - **Mérito até o 65º dia:** 35 processos no Controle, contra 5 no Presencial e 2 na Remota (resíduo +7,0). Sem AC inaugural, o Controle consegue julgar o mérito cedo, provavelmente por julgamento antecipado após a contestação.
  - **Sem mérito precoce** se concentra no Presencial (resíduo +2,7).
  - **"Sem desfecho até 65 dias"** se concentra na Remota (+2,4).
- **Leitura jurídica.** A AC obrigatória não se limita a "acrescentar acordos": ela **troca julgamentos de mérito por extinções sem mérito**. Para a política judiciária, isso tem custo. Uma extinção por ausência não resolve o conflito, e o autor pode repropor a ação (art. 51, § 1º). O indicador "processos baixados" melhora sem que a resposta ao jurisdicionado melhore na mesma proporção.
''',

'tst_acordo': r'''
**Leitura. A AC obrigatória não produziu mais acordos *na audiência*. O excedente de acordos da Remota veio de fora dela e só aparece com seguimento maior.**

- **Acordo na AC, presencial × remota (H4).** Foram 9/178 (5,1%) contra 8/174 (4,6%). Fisher p = 1,000; OR = 1,11 (IC exato 0,37 a 3,38); diferença de +0,5 p.p. (IC de Newcombe −4,4 a +5,3).
  - O resultado é **compatível com igualdade**, mas o IC é largo. Com uma taxa-base de 4,8% e cerca de 175 audiências por braço, só uma diferença de **≥ 8,4 p.p.** teria 80% de poder.
  - Ou seja, o estudo **exclui grandes diferenças** entre as modalidades, mas não exclui diferenças de alguns pontos percentuais.
  - Em qualquer modalidade, a taxa de acordo na AC (~5%) é baixa. É coerente com o diagnóstico Ipea/CNJ de baixa efetividade das audiências de conciliação nos JECs.
- **Acordo em qualquer momento (H5), em horizonte fixo:**
  - **até 65 dias** (938 processos): 3,5% no Controle, 4,5% no Presencial e 6,1% na Remota; χ² p = 0,300. Nenhum par difere;
  - **até 120 dias** (688 com seguimento ≥ 120 d): 5,0%, 9,4% e 12,5%; χ²(2) = 8,00, p = 0,018. O par **Remota × Controle** difere: OR = 2,70 (1,28 a 6,01), +7,5 p.p. (2,3 a 13,0), p Holm = 0,020. Presencial × Controle fica no limite (+4,4 p.p., IC −0,3 a 9,3; p Holm = 0,150).
  - Esse sinal é o mesmo da homologação entre os sentenciados (seção 3.2.3). **Não sobrevive à correção global de Holm** sobre os 55 testes da parte, só à de Benjamini-Hochberg (seção 3.7). É um achado **sugestivo**, a confirmar com a função de incidência acumulada do acordo (Parte IV).
- **De onde vem o excedente da Remota?** Não vem da AC, já que Presencial e Remota têm a mesma taxa na audiência. O acordo **fora** da AC é de 7,9% no Controle, 6,7% no Presencial e 11,9% na Remota (χ² p = 0,107; nenhum par significativo após Holm). A hipótese plausível, a testar com dados de movimentação, é que a AC remota sem acordo ainda aproxima as partes (contato, proposta registrada), e o acordo se fecha depois, por petição.
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
  - **Mann-Whitney:** todos os deltas de Cliff estão entre −0,03 e +0,03, com ICs dentro de ±0,13 (efeito desprezível);
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

  A Remota já aparece mais lenta, embora sem significância nesse horizonte curto. Usando todo o seguimento com Kaplan-Meier e log-rank (Parte IV), a revisão do notebook do professor encontrou medianas de Controle 80, Presencial 93 e Remota 94 dias (log-rank p ≈ 0,03). **A conclusão muda** de "o rito não importa" (KW ingênuo) para "a AC obrigatória alonga a tramitação", e só um método que respeita a censura consegue mostrar isso.
- **E24 refeito.** Entre as AC realizadas já sentenciadas, os 17 processos com acordo na AC terminaram em 63 dias (mediana), contra 104 dias dos sem acordo (U = 816, p < 0,001, delta de Cliff = −0,61, IC −0,85 a −0,32). O efeito é grande, mas em boa parte é **definicional**: o acordo encerra o processo com a homologação, e quem não fez acordo segue para contestação e julgamento. A pergunta correta ("o acordo na AC antecipa o fim?") é de riscos competitivos (Parte IV).
''',

'tst_ordem': r'''
**Leitura. O sorteio parece aleatório, a vara ficou mais lenta ao longo do ano e a correlação "ingênua" entre a ordem de chegada e o tempo é dominada pela censura.**

- **Aleatoriedade do sorteio (H9).**
  - **Número de corridas:** foram observadas R = 626 corridas, contra 626,3 esperadas sob H₀ (DP de permutação de 14,3; p = 1,000). Não há nem agrupamento nem rodízio regular.
  - **Maior corrida:** tem 8 processos seguidos, comprimento comum sob o acaso (P ≥ 8 = 0,239).
  - **Por grupo:** z = 0,43, 0,75 e −1,24, todos não significativos.

  A sequência é **compatível com sorteio aleatório**, o que reforça a classificação como ECA (questão 2.2). O teste não prova o mecanismo: uma lista pseudoaleatória bem feita e um sorteio físico dariam o mesmo resultado, e a ocultação da alocação continua sem documentação.
- **Composição mensal (H11).** χ²(12) = 18,45, p = 0,103, V = 0,10. No conjunto, o desequilíbrio não excede o acaso, mas os resíduos mostram dois meses atípicos: **junho**, com excesso de Presencial (+2,95), e **julho-agosto**, com excesso de Remota (+3,10; 71 de 163 processos). Como julho é o mês com menos seguimento e mais ativos, a Remota recebe uma parcela maior de processos com pouco seguimento. Por isso o mês entra como estrato e covariável (seção 3.6 e Partes IV e V).
- **Ordem de chegada × tempo (H10, questão 2.7):**
  - **todos (938), censura ignorada:** ρ = −0,04 (p = 0,211), τ = −0,05 (p = 0,024). Spearman e Kendall discordam quanto à significância, um sinal de que a associação é fraca e frágil;
  - **só sentenciados:** ρ = −0,12 (p = 0,002). Este é o "achado" que uma análise ingênua reportaria: "os processos mais recentes são mais rápidos";
  - **janela comum de 65 dias**, sem censura: ρ = **+0,14** (p < 0,001; τ = +0,11). **O sinal se inverte**: os processos que chegaram depois demoram **mais**. A proporção sentenciada até o 65º dia cai de 46% (janeiro) para 21% (julho), o que é compatível com acúmulo de acervo ao longo do experimento (cada processo dos braços com AC exige uma pauta de audiência) ou com sazonalidade de pauta.
- **A simulação explica a inversão.** Em 500 réplicas, os tempos foram gerados **sem nenhuma relação** com a ordem e censurados com o acompanhamento real de cada processo. Sob essa H₀:
  - **só encerrados:** ρ médio = −0,28 (faixa de 95%: −0,34 a −0,21);
  - **todos, com a censura ignorada:** ρ médio = −0,19;
  - **janela de 65 dias:** ρ médio = 0,00.

  A censura sozinha "fabrica" uma correlação negativa forte. Os ρ observados (−0,12 e −0,04) ficam **acima** dessa faixa, ou seja, a associação verdadeira é positiva e parcialmente mascarada pela censura. A magnitude do artefato depende da distribuição simulada (Weibull de forma 1,6), mas o sinal não depende.
- **Resposta à questão 2.7.** Sim, é possível investigar a correlação entre a ordem de chegada e o tempo, com Spearman ou Kendall (a ordem é ordinal; nunca Pearson), **desde que** a censura seja tratada: janela comum de seguimento, como aqui, ou a ordem/data como covariável num modelo de Cox (Parte IV). Sem esse cuidado, a correlação mede o calendário de distribuição e não o ritmo da vara.
''',

'tst_professor': r'''
**Leitura (questão 2.11).**

- **Os testes reproduzidos dão valores-p "fortes" justamente onde a hipótese é vazia:**
  - **Encerrado × Ativo:** p < 0,001, e é tautológico;
  - **z com p₀ = 0,5:** z = 17,2, e 78,0% de encerrados não é comparável a nada;
  - **grupo × status:** p < 0,001, mas o status depende do mês de entrada;
  - **grupo × acordo na AC com o Controle:** p = 0,013. O "efeito" é o zero estrutural do Controle, e as esperadas da coluna "acordo" são 5,6 a 5,7, no limite de Cochran.
- **Testes sobre perguntas reais têm valores-p fracos e precisam de método adequado.** É o caso do KW (p = 0,559) e do Mann-Whitney com × sem acordo (p = 0,448). A significância estatística do notebook do professor está, portanto, **invertida em relação à relevância substantiva**.
- **Dos 14 testes do notebook:**
  - **um é adequado na ideia:** χ² tipo de sentença × grupo, refeito aqui sem a "Decisão", com resíduos e V;
  - **quatro devem ser removidos:** Encerrado × Ativo, z com p₀ = 0,5, matriz de correlação e dispersões tautológicas;
  - **os demais devem ser substituídos** por métodos que respeitem a censura (Parte IV), o zero estrutural (Fisher entre os braços com AC) ou a multiplicidade (Dunn/Holm).
- **CMH estratificado por mês (H12).** O acordo foi comparado entre os processos com o registro de acordo (733).
  - **Remota × Controle:** OR bruto = 2,15 e OR de Mantel-Haenszel = **2,17 (IC 95% 1,22 a 3,86)**, χ²(1) = 7,23, p = 0,007 (p Holm = 0,014 na família). Breslow-Day p = 0,385: o OR é homogêneo entre os meses.
  - **Presencial × Controle:** OR MH = 1,34 (0,73 a 2,47), p = 0,351.
  - **Leitura.** O ajuste pelo mês **não altera** a razão de chances. A concentração de Remota em julho não explica o seu excedente de acordos, ou seja, o mês não confunde essa associação. A ressalva continua: a base é condicional a ter o acordo registrado (encerrados), e o desfecho correto é a incidência acumulada do acordo (Parte IV).
- **Outros testes aplicáveis.** CMH, permutação e exatos foram implementados aqui. Jonckheere-Terpstra e Cochran-Armitage servem para hipóteses de **tendência no mês** (por exemplo, a queda da proporção sentenciada até 65 dias, de 46% para 21%), não para o grupo, que é nominal. Brunner-Munzel e Kolmogorov-Smirnov ampliariam a comparação de distribuições, mas herdam o problema da censura. Testes pareados não se aplicam (questão 2.3).
''',

'tst_multiplicidade': r'''
**Leitura. O que sobrevive a qualquer critério.**

- **Volume de testes.** A parte registrou **55 testes**. São significativos a 5%: **19** sem correção, **17** com Benjamini-Hochberg (FDR) e **13** com Holm global (FWER).
- **Sobrevivem ao Holm global, que é o critério mais exigente:**
  - **H1/H2 (tipo de desfecho).** Associação tipo × grupo (sentenciados e janela de 65 dias); pares Presencial × Controle e Remota × Controle; mais sem mérito e menos mérito nos dois braços com AC. **É o achado mais robusto da Parte III.**
  - **H8 por tipo.** Julgamentos de mérito mais lentos nos braços com AC (KW no estrato mérito).
  - **H10.** Correlação positiva entre ordem de chegada e tempo na janela sem censura (ρ = +0,14): a vara ficou mais lenta ao longo do ano.
  - **E24 refeito.** O acordo na AC encerra o processo mais cedo, o que é em boa parte definicional.
- **Sobrevivem só ao BH (FDR), como evidência sugestiva a confirmar:**
  - mais **acordo** na Remota que no Controle: homologação entre sentenciados, acordo até 120 dias e CMH por mês, com OR entre 2,2 e 2,7 de forma consistente;
  - a correlação negativa ordem × tempo entre os sentenciados, que é o artefato da censura (seção 3.5.2) e, por isso, não deve ser lida como achado.
- **Não rejeitados, com IC que informa o tamanho máximo plausível:**
  - acordo na AC presencial × remota: diferença de +0,5 p.p. (IC −4,4 a +5,3);
  - técnica e híbrida: sem poder;
  - redistribuição;
  - aleatoriedade do sorteio, compatível com H₀;
  - tempo agregado entre os sentenciados: delta de Cliff ≈ 0, um paradoxo de composição.
- **Leitura para a questão 2.11.** Sem correção de multiplicidade e sem tamanho de efeito (E27), o notebook do professor não tinha como separar esses três níveis de evidência. Com 55 testes a 5%, cerca de três "significâncias" seriam esperadas só pelo acaso. Por isso, o achado de acordo da Remota, isolado, não autorizaria uma recomendação de política judiciária. Já a troca de mérito por extinção sem mérito autoriza.
''',

}
