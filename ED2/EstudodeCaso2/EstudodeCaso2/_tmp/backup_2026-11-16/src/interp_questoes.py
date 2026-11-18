# Interpretações da Parte VI (respostas às questões 2.2 a 2.12).
# Redigidas a partir das saídas reais de _tmp/teste_secao0607.ipynb (execução de 12/11/2026)
# e das saídas das Partes I a V (_tmp/teste_vis02/03, teste_secao04/05).

INTERP_QUESTOES = {

'q_2_2': r'''
**Resposta à questão 2.2.** O diagrama de fluxo mostra o que caracteriza o estudo como **ECA**: os 938 processos da base primária foram repartidos por sorteio em três grupos praticamente iguais (313, 314 e 311), todos acompanhados até a mesma data e todos analisados no grupo sorteado (intenção de tratar), sem perdas. O diagrama mostra também onde o experimento deixa de ser experimento. A partir da segunda linha de caixas, o que acontece depende das partes, e não do sorteio: nos braços com AC, a audiência só foi realizada em 178 de 314 processos (Presencial) e 174 de 311 (Remota); 112 e 88 terminaram sem AC (a técnica ficou registrada como `**`), e 28 audiências presenciais foram híbridas. Comparar "quem teve AC" com "quem não teve" seria, portanto, um estudo observacional embutido no ensaio. Na linha dos desfechos já aparece o achado central: o Controle tem 162 sentenças de mérito e 79 extinções sem mérito; os braços com AC invertem essa proporção (96/109 e 83/98).

Em suma: **ECA** quanto ao rito, porque o pesquisador impôs a exposição por sorteio, com controle contemporâneo; **componentes observacionais** quanto a tudo o que ocorre depois do sorteio; e, quanto à pretensão de avaliar a política nos JECs de Natal, **estudo de caso de uma unidade**. A classificação do próprio projeto como "quase experimental" (TREND) ou "observacional" é imprecisa: o que falta ao experimento não é aleatorização, e sim ocultação da alocação, cegamento e mais de uma unidade.
''',

'q_2_3': r'''
**Resposta à questão 2.3.** As três variáveis basais disponíveis não diferem entre os grupos além do acaso: mês de distribuição χ²(12) = 18,45, p (permutação) = 0,102, V = 0,099; dia da semana χ²(12) = 10,44, p = 0,577, V = 0,075; origem externa χ²(2) = 3,50, p = 0,263 (3, 7 e 2 processos). Após Holm, nenhum p fica abaixo de 0,30. É o que se espera de grupos formados por sorteio a partir de **uma mesma população** disponível. O mês, embora não significativo no global, tem os desvios localizados já vistos na seção 3.5.3 (junho com excesso de Presencial e julho com excesso de Remota), e por isso foi tratado como estrato nas Partes IV e V.

O painel (d) mostra a trajetória que denuncia o **sorteio restrito**: a diferença entre o maior e o menor grupo acumulado cresceu até 31 processos no fim de junho (ordem 757, 25/06) e caiu para 3 ao final, com a compensação concentrada em julho. Num sorteio simples, a amplitude final tem mediana em torno de 28 processos, e uma divisão tão equilibrada quanto a observada tem probabilidade de cerca de 1% (seção 2.5.1). Isso não compromete a independência entre os grupos, mas cria dependência fraca entre alocações sucessivas e uma associação entre período e grupo, o que reforça a análise estratificada por mês.

**Conclusão.** Os grupos são **amostras independentes** (partição aleatória de uma população finita, sem pareamento), comparáveis em expectativa. Isso determina testes para k amostras independentes (χ², Fisher, Kruskal-Wallis, Mann-Whitney, log-rank, Cox), e não testes pareados. As ressalvas (agrupamento por conciliadora e por juiz, litigantes repetidos, sorteio restrito) não mudam a família de testes, mas pedem cautela com valores-p limítrofes e justificam a estratificação.
''',

'q_2_4': r'''
**Resposta à questão 2.4.** As duas variáveis têm em comum o fato de registrarem algo que ocorre **depois do sorteio** e que, por isso, não pode ser tratado como tratamento ou desfecho comuns.

- **Híbrida = Sim** é não adesão parcial: 28 audiências do braço Presencial foram feitas com participação remota de uma parte. Mantidas no grupo sorteado (intenção de tratar), elas não alteram nada; movidas para a Remota ("conforme tratado"), também não (o HR da Remota fica entre 0,79 e 0,82 em todos os cenários da seção 4.9). O acordo na AC híbrida (1/24) não difere do da presencial pura (8/154; Fisher p = 1,000), mas com 9 acordos no total a comparação não tem poder e, sendo observacional, não testaria a hipótese H4 mesmo que tivesse. As 3 híbridas registradas no grupo Remota são erro de registro ou de definição e foram sinalizadas (A12).
- **"Decisão"** é saída do estudo por redistribuição a juízo prevento: 24 processos (5, 10 e 9 por grupo), com mediana de 1 dia e só 3 após 30 dias. Não é sentença: contá-la como evento (E10) faria o processo "terminar" em um dia sem que o conflito tivesse sido resolvido no 4º JEC. Como risco competitivo, ela é igualmente frequente nos três grupos (seção 3.2.4) e distorce pouco o 1 − Kaplan-Meier (no máximo cerca de 3 pontos percentuais aos 180 dias; seção 4.7.1), de modo que nenhuma conclusão depende da forma de tratá-la. Do ponto de vista do desenho, porém, é uma falha de elegibilidade: a prevenção deveria ser verificada **antes** do sorteio, e o processo que retorna não deveria ser sorteado de novo.
''',

'q_2_5': r'''
**Resposta à questão 2.5.** O quadro das populações deixa explícito o salto que a pesquisa precisa dar: da amostrada à disponível, a inferência é **interna e válida** (os 938 processos são praticamente o censo das ações distribuídas ao 4º JEC no período, e o sorteio dá base às comparações); da disponível à de interesse, não há inferência estatística, porque só uma das 14 unidades entrou, e não por sorteio.

O segundo quadro mostra que o DataJud resolve **parte** do problema. Ele traz, para todos os JECs, exatamente o que é preciso para medir o tempo da distribuição à sentença com a mesma regra de censura (datas de ajuizamento e movimentos de julgamento, homologação e redistribuição), e permite conferir, pelo número CNJ, as datas digitadas na planilha (em especial as 18,4% de sentenças em fim de semana). Não traz o que mais falta ao experimento: partes, valor da causa, advogado e magistrado. O DataJud serve, portanto, para **comparar unidades e validar a medida do desfecho**, não para recuperar as covariáveis do processo. Os resultados da coleta (199 de 200 números consultados encontrados até agora no endpoint do TJRN) e as comparações estão na **Parte VIII**.
''',

'q_2_6': r'''
**Resposta à questão 2.6.** O quadro mostra que os problemas do notebook do professor não são independentes: quase todos convergem para a **variável-alvo**. A duração dos ativos calculada até `TODAY()`, a "Decisão" contada como encerramento, as duplicatas que criariam falsos censurados e as colunas redundantes de duração afetam diretamente o par (tempo, evento), do qual dependem todas as análises posteriores. Os demais itens (grafias, CNJ, `**`, híbridas) afetam as variáveis de classificação.

O tratamento adequado não exigiu imputar nada: bastou (i) fixar a data de corte, (ii) recalcular o tempo pelas datas, (iii) definir o evento e o tipo de desfecho com base no significado jurídico de cada registro, (iv) aplicar uma regra única às duplicatas (um processo, uma unidade, o grupo do primeiro sorteio) e (v) registrar cada decisão. O tratamento pode e deve ser complementado com fontes externas: as datas e os motivos de extinção, que a planilha não tem, estão nos movimentos do PJe e, em parte, no DataJud (6.4).
''',

'q_2_7': r'''
**Resposta à questão 2.7.** A figura resolve a aparente contradição entre "há correlação" e "não há correlação" na ordem de chegada. Se os tempos fossem **independentes** da ordem, a censura sozinha produziria um ρ de Spearman em torno de −0,19 quando se usam todos os tempos (intervalo de 95%: −0,25 a −0,13) e de −0,28 quando se usam só os sentenciados (−0,34 a −0,21). Os valores observados (−0,041 e −0,118) são **menos negativos** do que isso e caem **fora** dos intervalos de nulidade. Na janela comum de 65 dias, a única versão do tempo sem censura para todos, o artefato desaparece (ρ médio sob H₀ ≈ 0) e o ρ observado é **positivo** (0,140), acima do intervalo de nulidade (−0,066 a 0,067).

A leitura correta é, portanto, oposta à que a correlação bruta sugere: os processos que chegaram depois **demoraram mais** para ser sentenciados, e o sinal negativo dos dados brutos é produzido pela censura. Isso coincide com os modelos que respeitam a censura (Cox com mês: HR de 0,70 em junho e de 0,58 em julho-agosto contra janeiro; AFT log-normal: cerca de 20% mais tempo por mês de distribuição) e indica **acúmulo de acervo** ao longo do experimento.

Quanto à matriz do professor, a resposta é inequívoca: correlacionar quatro cópias da mesma coluna produz r = 1 por identidade e nada informa. A matriz adequada é de **associação** (V de Cramér entre nominais, η entre nominal e tempo), e a relação de qualquer variável com o tempo deve ser medida num modelo de sobrevivência.
''',

'q_2_8': r'''
**Resposta à questão 2.8.** O quadro separa três situações que costumam ser confundidas sob o nome de "confundimento":

1. **confundidores neutralizados pelo sorteio** (tipo de ação, valor, partes, litigante habitual, advogado): não enviesam a comparação entre grupos, embora a sua ausência na planilha impeça verificar o equilíbrio e reduza a precisão;
2. **confundidores que o sorteio não alcança** porque estão amarrados ao braço ou agem sobre todos os grupos sem cegamento (conciliadora, juiz-pesquisador, reatividade, contaminação): não foram controlados pelo desenho e só podem ser controlados numa replicação (rodízio, cegamento, várias unidades). A conciliadora é o mais grave: torna a comparação Presencial × Remota uma comparação entre **duas pessoas** tanto quanto entre duas modalidades. A contaminação, ao contrário, tende a **reduzir** as diferenças, o que torna mais robustos os efeitos encontrados contra o Controle;
3. **mediadores** (fila da pauta, ausência do autor à AC): não são viés, são o **caminho** pelo qual o rito age, e explicam o resultado. Os dados são compatíveis com o mecanismo da ausência: as extinções sem mérito ocorridas **após 30 dias** de tramitação, período em que a AC costuma ocorrer, somam 26 no Controle, 45 na Presencial e 48 na Remota, enquanto as extinções da primeira semana não mostram excesso consistente (39, 48 e 34). A planilha, porém, não registra o motivo da extinção, e a confirmação depende do PJe.

O mês de distribuição é o único confundidor de calendário **controlado na análise**: o log-rank estratificado por mês (p = 0,045) e o Cox com estrato por mês (HR da Remota 0,80; IC 0,67–0,96) mantêm a conclusão.
''',

'q_2_9': r'''
**Resposta à questão 2.9.** O quadro mostra que a resposta depende de duas perguntas prévias: **quando** a variável é medida (antes ou depois do sorteio) e **se o tempo está censurado**. Variáveis basais (número de partes, valor da causa) são covariáveis legítimas e ajudariam a verificar o sorteio e a ganhar precisão; variáveis de processo (número de atos, remarcações, dias até a AC) são componentes ou mediadores do tempo, e uma correlação delas com a duração é em boa parte mecânica.

Quanto à medida: a correlação de **Pearson** só é apropriada para relação linear com distribuição aproximadamente normal, o que contagens e tempos raramente satisfazem; **Spearman** (relações monotônicas) e **Kendall τ_b** (com muitos empates, típico de contagens pequenas como o número de réus) são as escolhas naturais para dados completos, com teste t para ρ = 0 ou por permutação. Com 24,5% dos tempos censurados, porém, nenhuma correlação simples é válida (6.6): a covariável quantitativa entra num **modelo de Cox** (razão de riscos por unidade, testes de Wald, escore ou razão de verossimilhanças) ou num AFT (razão de tempos), e o C de Harrell faz o papel de um τ de Kendall para dados censurados.
''',

'q_2_10': r'''
**Resposta à questão 2.10.** **Não é possível generalizar estatisticamente** os resultados aos 14 JECs de Natal. O primeiro quadro mostra a assimetria: os pontos que favorecem a validade **interna** são fortes (sorteio, controle contemporâneo, tratamento da censura, robustez em doze cenários de sensibilidade), enquanto a validade **externa** repousa numa única unidade escolhida por conveniência. A distribuição aleatória entre os JECs pelo PJe torna o perfil das **ações** do 4º JEC semelhante, em expectativa, ao das demais unidades; não torna semelhantes o juiz, as conciliadoras, a pauta e o cartório, que são justamente os fatores pelos quais a AC obrigatória age.

O segundo quadro organiza o que se pode fazer. Só o sorteio interno identifica o **efeito do rito**. As duas comparações com o DataJud adotadas como recorte (4º JEC antes × durante e 4º JEC × os outros 13 JECs) respondem a outra pergunta, o **efeito do experimento sobre a unidade**, úteis para avaliar a reatividade e o acúmulo de acervo e para situar os tempos do 4º JEC na capital. A validade externa propriamente dita, para outras comarcas ou estados, exige **replicação** do experimento, não comparação observacional.
''',

'q_2_11': r'''
**Resposta à questão 2.11.** Dos doze procedimentos do quadro, só um era adequado em si, o Kaplan-Meier com log-rank, e foi justamente o que não rodou (E1). O χ² do tipo de sentença tinha a ideia certa, mas precisou ser refeito. Os demais eram tautológicos (Mann-Whitney Encerrado × Ativo, matriz de r = 1), sem sentido substantivo (z com p₀ = 0,5) ou inválidos sob censura (Kruskal-Wallis, OLS, ajuste MLE, χ² de status).

A figura mostra por que isso importa. Com a censura ignorada, as medianas são 77, 83,5 e 81 dias e o Kruskal-Wallis não vê diferença (H = 1,16; p = 0,559 na base primária; p = 0,478 nas 943 linhas do professor). Restrito aos sentenciados, o quadro fica ainda mais "igual" (72, 71 e 77 dias). Com a censura respeitada, as medianas de Kaplan-Meier são 81, 96 e 95 dias, com intervalos de confiança que mal se tocam entre o Controle e os braços com AC, e o log-rank rejeita a igualdade (χ²(2) = 7,52; p = 0,023). O efeito existia; o teste escolhido é que o tornava invisível, porque os processos ainda ativos, mais longos e concentrados nos braços com AC, entravam como se tivessem terminado no dia do corte.

A lição para o TSHN é dupla: o teste deve corresponder à **estrutura dos dados** (censura, zeros estruturais, independência) e à **pergunta** (uma comparação de tempos censurados não é uma comparação de posições), e deve ser relatado com tamanho de efeito, intervalo e controle de multiplicidade. A alegação de "não diferença" do resumo expandido exigiria, ainda, um teste de equivalência e uma análise de poder (7.4.3).
''',

'q_2_12': r'''
**Resposta à questão 2.12.** O quadro de avaliação tem um padrão claro: o item **fidedignidade do registro** é o único avaliado como adequado sem ressalvas, e os itens inadequados concentram-se no **desenho da alocação** (ocultação, unicidade da unidade), na **execução** (cegamento, condutor da intervenção), nas **covariáveis** e no **plano de análise**. É o perfil de uma pesquisa feita com cuidado e boa-fé por quem conhece o processo, mas sem protocolo estatístico prévio: os dados primários são confiáveis naquilo que registram; o problema é o que **não** registram e como foram **analisados**.

A avaliação geral é, por isso, positiva quanto ao potencial e crítica quanto à execução. O experimento respondeu, com validade interna razoável, a uma pergunta relevante de política judiciária, e a resposta (a AC obrigatória alongou o tempo até a sentença e aumentou a extinção sem mérito, sem aumentar o acordo na audiência) é mais informativa do que a conclusão divulgada. Para conferir maior validade a uma replicação, as prioridades são: **interna**, ocultação e documentação do sorteio, rodízio das conciliadoras, cegamento da extração e registro do motivo da extinção; **externa**, várias unidades judiciais sorteadas; **estatística**, pré-registro do desfecho primário e cálculo de poder. O detalhamento está na seção 7.4.
''',

}
