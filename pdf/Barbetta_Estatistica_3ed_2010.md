Pedro Alberto B arbetta
Marcelo Menezes Reis
Antonio Cezar Bornia
ESTATÍSTICA
PARA CURSOS DE
ENGENHARIA
INFORMÁTICA
3a EDIÇÃO
EditoraAtlas

Estatística

Para alguns livros é disponibilizado Material
Complementar e/ou de Apoio no site da editora.
Verifique se há material disponível para este livro em
atlas.com.br

Pedro Alberto Barbetta
Marcelo Menezes Reis
Antonio Cezar Bornia
Estatística
Para Cursos de Engenharia
e Informática
3* Edição
SÃO PAULO
EDITORA ATLAS S.A. - 2010

© 2004 by Editora Atlas S.A.
1. ed. 2004; 2. ed. 2008; 3. ed. 2010 (4 impressões)
Capa: Roberto de Castro Polisel
Composição: Lino-Jato Editoração Gráfica
Dados Internacionais de Catalogação na Publicação (CIP)
(Câmara Brasileira do Livro, SP, Brasil)
Barbetta, Pedro Alberto
Estatística : para cursos de engenharia e informática / Pedro Alberto Barbetta, Marcelo Me­
nezes Reis, Antonio Cezar Bornia. - 3. ed. - São Paulo : Adas, 2010.
Bibliografia.
ISBN 978-85-224-5994-0
eISBN 978-85-224-6569-9
1. Estatística I. Reis, Marcelo Menezes. II. Bornia, Antonio Cezar. III. Título.
04-0564 CDD-519.5
índice para catálogo sistemático:
1. Estatítica 519.5
TODOS OS DIREITOS RESERVADOS - É proibida a reprodução total ou parcial,
de qualquer forma ou por qualquer meio. A violação dos direitos de autor
(Lei nQ 9.610/98) é crime estabelecido pelo artigo 184 do Código Penal.
atlas
Editora Atlas S.A.
Rua Conselheiro Nébias, 1384 (Campos Elísios)
01203-904 São Paulo (SP)
Tel.: (011) 3357-9144
www.EditoraAtlas.com.br

Sumário
Prefácio, 9
1 INTRODUÇÃO, 11
1.1 A estatística, 11
1.2 Pesquisas, dados, variabilidade e estatística, 12
1.3 A estatística na engenharia, 13
1.4 A estatística e a informática, 14
1.5 Modelos, 15
1.6 Conceitos básicos, 17
2 O PLANEJAMENTO DE UMA PESQUISA, 23
2.1 Aspectos gerais, 23
2.2 Pesquisas de levantamento, 24
2.3 Planejamento de experimentos, 33
3 ANÁLISE EXPLORATÓRIA DE DADOS, 50
3.1 Dados e variáveis, 51
3.2 Análise de variáveis qualitativas, 53
3.3 Análise de variáveis quantitativas, 58
3.4 Medidas descritivas, 68
3.5 Observações ao longo do tempo, 83
3.6 Análise exploratória com apoio do computador, 84
3.7 Orientação geral, 85

6 ESTATÍSTICA
4 PROBABILIDADE, 91
4.1 Espaço amostrai e eventos, 93
4.2 Definições de probabilidade, 96
4.3 Probabilidade condicional e independência, 102
4.4 Teorema da probabilidade total, 110
4.5 Teorema de Bayes, 112
5 VARIÁVEIS ALEATÓRIAS DISCRETAS, 116
5.1 Variável aleatória, 116
5.2 Principais distribuições discretas, 126
6 VARIÁVEIS ALEATÓRIAS CONTÍNUAS, 140
6.1 Caracterização de uma variável aleatória contínua, 140
6.2 Principais modelos contínuos, 147
6.3 A normal como limite de outras distribuições, 159
6.4 Gráfico de probabilidade normal, 164
7 DISTRIBUIÇÕES AMOSTRAIS E ESTIMAÇÃO DE PARÂMETROS, 169
7.1 Parâmetros e estatísticas, 169
7.2 Distribuições amostrais, 174
7.3 Estimação de parâmetros, 179
7.4 Tamanho de amostra, 192
8 TESTES DE HIPÓTESES, 198
8.1 As hipóteses, 198
8.2 Conceitos básicos, 201
8.3 Tipos de erro, 205
8.4 Abordagem clássica, 206
8.5 Testes unilaterais e bilaterais, 208
8.6 Aplicação de testes estatísticos, 211
8.7 Teste para proporção, 212
8.8 Teste para média, 217
8.9 Teste para variância, 222
8.10 Poder de um teste e tamanho da amostra, 224
9 COMPARAÇÃO ENTRE TRATAMENTOS, 232
9.1 Amostras independentes e em blocos, 232
9.2 Teste t para duas amostras pareadas, 235
9.3 Teste t para duas amostras independentes, 238
9.4 Tamanho das amostras, 242

9.5 Teste F para duas variâncias, 247
9.6 Comparação de várias médias, 248
9.7 Anova em projetos fatoriais, 258
9.8 Anova em projetos do tipo 2k, 263
10 TESTES NÃO PARAMÉTRICOS, 273
10.1 Testes de aderência, 274
10.2 Análise de associação, 287
10.3 Testes para duas populações, 293
11 CORRELAÇÃO E REGRESSÃO, 316
11.1 Correlação, 316
11.2 Coeficiente de correlação linear de Pearson, 318
11.3 Regressão linear simples, 324
11.4 Introdução à regressão múltipla, 346
Anexo, 351
Respostas de exercícios, 354
Apêndice: Tabelas estatísticas, 368
Bibliografia, 409

Prefácio
O presente texto é dirigido ao ensino da Estatística, especialmente para es­
tudantes de Engenharia e Informática. Os métodos são apresentados de forma
simples e intuitiva, com exemplos de motivação, aplicações e exercícios típicos
da área de estudo do aluno.
Nossa experiência de vários anos ministrando disciplinas de Estatística,
para diferentes cursos, sugere a conveniência de um texto de Estatística voltado
para a área em que o aluno está cursando, pois isso motiva e melhora o apren­
dizado. Além disso, permite que o aluno aplique mais facilmente os novos con­
ceitos e técnicas em problemas reais de sua área. Muitas aplicações e exemplos
deste livro foram extraídos de dissertações e teses desenvolvidas em programas
de pós-graduação de Engenharia e Ciência da Computação, enfatizando a utili­
zação da Estatística em pesquisas nessas áreas.
O conteúdo do livro pode ser desenvolvido em um ou dois semestres. Nos
cursos com a matéria de Estatística ministrada em dois semestres, recomenda­
mos a realização de trabalhos práticos e o uso de um pacote computacional de
estatística, ou mesmo uma planilha eletrônica. Optamos por não trabalhar um
pacote específico, mas apresentamos várias saídas computacionais (que são
mais ou menos padronizadas nos programas). Essas saídas são comentadas e
interpretadas de acordo com o desenvolvimento dos conceitos. Também descre­
vemos alguns conceitos que facilitam o trabalho do aluno com apoio do compu­
tador.
O livro desenvolve a matéria de Estatística que é usualmente ministrada
em cursos de Engenharia, Ciência da Computação e Sistemas de Informação.
O Capítulo 1 mostra como a Estatística é importante na vida do Engenheiro ou

10 ESTATÍSTICA
do profissional de informática, além de apresentar alguns conceitos básicos. O
Capítulo 2 oferece visão geral do planejamento de uma pesquisa científica. O Ca­
pítulo 3 enfoca a análise exploratória de dados. Os Capítulos 4 a 6 descrevem
uma introdução à probabilidade e os principais modelos probabilísticos. Os Ca­
pítulos 7 e 8 apresentam os princípios da inferência estatística. A matéria de
aplicação mais interessante é tratada nos Capítulos 9 a 11, os quais tratam de
análises estatísticas, como a comparação entre tratamentos e a análise de corre­
lação e regressão.
Não muito comum em outros textos básicos de Estatística, mas que consi­
deramos muito importante, é o planejamento da pesquisa, seja esta um levanta­
mento por amostragem, seja um estudo experimental. Este texto desenvolve o
assunto de forma específica no Capítulo 2. Além disso, apresenta comentários
sobre o planejamento da pesquisa ao longo dos demais capítulos.
Os leitores podem entrar em contato conosco por meio de nossos endere­
ços eletrônicos: < barbetta@ inf.ufsc.br>, < cezar@eps.ufsc.br> e <marce-
lo@inf. ufsc.br >.
Material didático complementar, como slides, arquivos de dados para exer­
cícios e referências de softwares livres de análise estatística, pode ser obtido em:
< www.inf.ufsc.br/~barbetta/livro2.htm>.

1
Introdução
1.1 A ESTATÍSTICA
No desenvolvimento científico e em nosso próprio dia a dia, estamos sem­
pre fazendo observações de fenômenos, gerando dados. Os engenheiros estão
frequentemente analisando dados de propriedades dos materiais; os profissio­
nais da informática estão avaliando dados de desempenho de novos sistemas
computacionais; e todos nós, ao lermos jornais e revistas, estamos vendo resulta­
dos estatísticos provenientes do censo demográfico, de pesquisas eleitorais etc.
Os dados podem provir de estudos observacionais ou de experimentos pla­
nejados. Ao acompanhar o desempenho de um processo produtivo em sua for­
ma natural, estamos fazendo um estudo observacional; ao alterar de forma pro­
posital as variáveis do processo para verificar seus efeitos nos resultados,
estamos realizando um experimento.
A estatística envolve técnicas para coletar, organizar, descrever, analisar e
interpretar dados, ou provenientes de experimentos, ou vindos de estudos
observacionais.
A análise estatística de dados geralmente tem por objetivo tomadas de de­
cisões, resoluções de problemas ou produção de conhecimento. Mas novos co­
nhecimentos normalmente geram novos problemas de pesquisa, resultando em
um processo iterativo (veja a Figura 1.1).

12 ESTATÍSTICA
Figura 1.1 Processo iterativo das pesquisas empíricas.
Neste livro, estudaremos técnicas de amostragens e de planejamento de ex­
perimentos (Capítulo 2), as quais permitem que tenhamos observações - ou da­
dos - capazes de responder a um problema. Mas as informações relevantes, que
devem estar contidas nos dados, normalmente precisam ser realçadas para que
possamos enxergá-las. Isso pode ser feito através da análise exploratória de da­
dos (Capítulo 3).
As observações de um experimento costumam vir acompanhadas de erro
experimental, ou seja, variações aleatórias devidas a uma infinidade de fatores
não controláveis. E a tarefa de verificar se alguma variação é real (devida a al­
gum fator em estudo) ou meramente resultado de flutuações aleatórias não é
fácil. É por isso que estudaremos a probabilidade, parte da matemática preocu­
pada em modelar fenômenos aleatórios (Capítulos 4, 5 e 6).
Inferências estatísticas, ou seja, generalizações de amostras para popula­
ções de onde elas foram extraídas, são fundamentais na resolução de problemas
de engenharia e nos processos de tomada de decisões. É através de inferências
estatísticas que podemos chegar à conclusão de que um material é mais resis­
tente do que outro, que um sistema computacional gera resultados mais preci­
sos do que outro ou, ainda, que um candidato tem intenção de voto no interva­
lo 30% ± 2%, com nível de confiança de 95%.
A essência de uma análise estatística é tirar conclusões sobre uma popula­
ção, ou universo, com base em uma amostra de observações.
Os Capítulos 7 e 8 apresentam as ideias básicas da inferência estatística;
nos Capítulos 9 a 11, são expostos métodos estatísticos propriamente ditos, que
envolvem planejamento da amostragem, análise exploratória, modelos de pro­
babilidade e inferência.
1.2 PESQUISAS, DADOS, VARIABILIDADE E ESTATÍSTICA
As pessoas normalmente associam o termo estatística a números, tabelas e
gráficos, mas a importância da estatística fica melhor representada por dois in­
gredientes comuns em nosso dia a dia: dados e variabilidade.

INTRODUÇÃO 13
Para o engenheiro conhecer as propriedades físicas de um novo material,
ele pode medir algumas de suas características, tais como a dureza, a flexibili­
dade, a densidade, a porosidade etc. Mas se ele medir a dureza em vários cor­
pos de prova do mesmo material com um instrumento de alta precisão, encon­
trará valores diferentes. Subestimar a presença da variabilidade pode pôr a casa
a pique!
Da mesma forma, observações do tempo demandado para transmitir da­
dos através da rede mundial de computadores, ou do número de bytes que pas­
sam por um servidor, variam uma enormidade ao longo do tempo. O conheci­
mento desses dados e de sua variabilidade torna-se imprescindível para se
projetar um sistema de transmissão de dados, ou mesmo para usar o sistema
existente com eficiência.
Em geral, a busca por melhorias na qualidade de um processo produtivo
implica a redução da variabilidade. O que você como consumidor pensa quando
vê refrigerantes de certa marca com grandes variações de conteúdo nas garra­
fas? E quando você resolve medir o peso de pacotes de café de 500 g e verifica
que alguns têm mais de 520 g e outros têm menos que 480 g? A variabilidade
pode ser reduzida com investimentos em pessoal, máquinas e tecnologia, mas
muitas vezes ela pode ser acomodada com o conhecimento de relações entre fa­
tores do processo e características funcionais do produto, o que envolve conhe­
cimentos de engenharia, pesquisas, dados e análises estatísticas.
Com a alta competitividade de hoje, para que uma empresa sobreviva, ela
tem o desafio de adequar o produto ao cliente. Por exemplo, a demanda exige
que certo material tenha um valor específico de dureza. Mas como obter este
valor de dureza, com a menor variabilidade possível, alterando fatores do pro­
cesso, tais como: temperatura do forno, temperatura de têmpera, meio de têm­
pera, alterações nos componentes do material etc.? A resposta pode ser um es­
tudo experimental, em que os fatores do processo são manipulados dentro de
uma região operacional de forma planejada. Observações são obtidas e, através
de uma análise estatística dos dados, podemos chegar à combinação ideal dos
fatores do processo.
Por outro lado, adequar o produto ao cliente envolve saber o que o consu­
midor deseja. Mas os consumidores têm preferências diferentes, o que exige a
realização de pesquisas observacionais (ou de levantamento) com os consumido­
res. Essas pesquisas envolvem planejamento, técnicas de amostragem, constru­
ção de questionários, organização dos dados, análises estatísticas e interpreta­
ção prática dos resultados.
1.3 A ESTATÍSTICA NA ENGENHARIA
Logo após a Revolução Industrial, métodos estatísticos foram incorporados
nos processos industriais para garantir a qualidade dos produtos. Amostras de

14 ESTATÍSTICA
itens produzidos eram avaliadas sistematicamente para inferir se o processo es­
tava sob controle. Mais recentemente, a avaliação da qualidade passou a ser fei­
ta ao longo de todo o processo produtivo como forma de corrigir eventuais fa­
lhas no sistema assim que elas aparecessem. Isso levou a um aumento da
qualidade do produto final e redução de custos, pois se reduziram drasticamen­
te as perdas por defeitos.
Além do acompanhamento estatístico da qualidade, as indústrias costu­
mam fazer experimentos estatisticamente planejados para encontrar a combina­
ção dos níveis dos fatores do processo que levem a melhor qualidade possível.
Na outra ponta, as empresas levantam dados de amostras de consumidores
para realizar pesquisas de marketing direcionadas ou para adequar os produtos
aos clientes. O planejamento dessas amostras e a análise dos dados necessitam
de técnicas estatísticas.
Muitas vezes, a relação entre estatística e engenharia é ainda mais estreita.
Os próprios métodos de engenharia costumam incorporar intrinsecamente pro­
cedimentos probabilísticos ou estatísticos. Assim, para que um aluno possa en­
tender certos métodos de engenharia, é necessário que tenha conhecimentos de
probabilidade e estatística.
1.4 A ESTATÍSTICA E A INFORMÁTICA
Enquanto a Informática é a ciência que trata da informação através de
meios eletrônicos, a Estatística procura obter informações relevantes de massas
de dados e, nos dias de hoje, isso costuma ser feito com auxílio do computador.
A variabilidade está onipresente nos sistemas computacionais atuais. Você
pode observar diferentes tempos de resposta ao carregar um aplicativo num sis­
tema compartilhado, ao transmitir uma mensagem no correio eletrônico etc.
Portanto, a análise do desempenho desses sistemas computacionais exige trata­
mento estatístico.
É comum construir sistemas para simular certas situações reais. Mas, como
no mundo real os acontecimentos nem sempre são previsíveis, toma-se necessá­
rio incluir no modelo de simulação alguma aleatoriedade, que pode ser feita
com base em modelos de probabilidade. Por exemplo, pode ser razoável supor
que em uma fila cheguem, em média, cinco indivíduos por minuto, mas o nú­
mero exato de indivíduos que vão chegar no próximo minuto não é totalmen­
te previsível.
Outra relação importante é o uso conjunto de banco de dados, estatística e
inteligência artificial para extrair informações relevantes e não triviais de gran­
des arquivos de dados, armazenados sob diferentes formatos e em diferentes lo­
cais. Por exemplo, as empresas telefônicas têm dados das ligações telefônicas

INTRODUÇÃO 15
de seus milhares ou até milhões de clientes. Mas é um grande desafio encon­
trar, com base nesses dados, possíveis fraudes, tais como as clonagens de telefo­
nes celulares. Este é um caso típico da necessidade de usar de forma conjunta
técnicas estatísticas e informática.
1.5 MODELOS
Os modelos podem ser considerados como alguma representação da reali­
dade em estudo, destacando aspectos relevantes e desprezando detalhes insig­
nificantes. Em geral, eles servem para simplificar, descrever e facilitar a inter­
pretação daquilo que se está estudando.
Na engenharia, o estudante costuma defrontar com os chamados modelos
determimsticos, isto é, conhecidas as entradas x lf x2, ..., xk> 0 modelo permite
chegar ao resultado y, usando uma função y = f(xi, x2, x j. É o que aconte­
ce, por exemplo, com a Lei de Ohm, em que, dadas a tensão (xO e a resistên­
cia (x2) de um circuito simples, podemos calcular o fluxo da corrente elétrica
(y) por:
y = ^ (1.1)
Muitas vezes, porém, as condições do experimento não permitem deduzir
qual o resultado, mas somente a chance (ou a probabilidade) de possíveis resul­
tados. É o caso da observação da face voltada para cima no lançamento impar­
cial de uma moeda perfeitamente equilibrada. Antes da realização do experi­
mento não se tem como dizer o resultado, mas é razoável atribuir
probabilidade 0,5 para cara e 0,5 para coroa. É um exemplo de modelo probabi-
lístico ou estocástico.
Um exemplo menos trivial de modelo probabilístico é a descrição do nú­
mero de indivíduos que chegam a uma fila, ou do número de pacotes de dados
que chegam a um servidor por segundo. Como veremos no Capítulo 4, sob cer­
tas condições e admitindo que a taxa média de chegadas por segundo é X, (um
valor positivo fixo), a probabilidade de chegar exatamente k pacotes num dado
segundo é de, aproximadamente:
p(fc) = (k = 0, 1, 2, ... e = 2,7183) (1.2)
k\
Esse tipo de modelo pode auxiliar o projetista a planejar a capacidade de
um sistema computacional.
Todo estudante já deve ter-se defrontado com os modelos mecanísticos, ca­
racterizados por serem totalmente deduzidos do conhecimento sobre o fenôme­

16 ESTATÍSTICA
no físico em questão - a Lei de Ohm é um exemplo. De outro lado estão os cha­
mados modelos empíricos, que são construídos com base em observações reais
sobre o problema em estudo. Por exemplo, podemos ter interesse em conhecer
a relação entre a resistência à compressão de um concreto e seu tempo de hi­
dratação. Para isso, podemos realizar um experimento, que resulta em observa­
ções dessas duas variáveis. A Figura 1.2 apresenta os resultados da resistência
(MPa) de 11 corpos de prova, com tempos de hidratação entre 10 e 20 dias.
Corpo Tempo de
Resistência
de hidratação
(MPa)
prova (dias)
1 10 11,3
2 11 12,1
3 12 16,4
4 13 16,3
5 14 20,2
6 15 20,5
10 12 14 16 18 20
7 16 25,0
tempo de hidratação (em dias)
8 17 26,4
9 18 26,2
10 19 28,4
11 20 30,2
Figura 1.2 Resultados de um experimento sobre resistência à compressão de con­
creto, em função do tempo de hidratação - dados e gráfico.
A Figura 1.2 mostra que não se tem uma função matemática simples para
explicar exatamente a relação entre as duas variáveis em questão. Contudo, o
gráfico expõe os pontos em torno de uma reta. Ou seja, podemos admitir que a
resistência esperada do concreto se relaciona linearmente com o tempo de hidra­
tação; e o fato de os pontos observados não estarem exatamente sobre uma reta
é porque existem inúmeros fatores não controláveis que agem sobre o processo -
o erro experimental.
Uma função matemática que explica aproximadamente o relacionamento
entre duas ou mais variáveis, construída com base em dados observados, pode
ser considerada um modelo de regressão, um tipo especial de modelo empírico.
Dado um problema, o conhecimento de engenharia é fundamental para esco­
lher adequadamente as variáveis e, às vezes, a forma funcional (uma reta, uma
parábola etc.), mas a construção completa do modelo é feita através dos dados.
No exemplo em questão, a Figura 1.2 sugere que uma reta (y = a + fix)
descreve aproximadamente o relacionamento. As 11 observações da resistência
(y) para diferentes tempos de hidratação (x) são usadas para obter valores de a

INTRODUÇÃO 17
e P adequados, conforme estudaremos no Capítulo 11. A Figura 1.3 mostra a
equação de regressão analítica e graficamente. O chapéu sobre y é para diferen­
ciar o modelo (a reta) dos valores efetivamente observados (os pontos).
y = 8,01 + 1,95.x 32-
'a 28-
onde x é o tempo de
hidratação e y é o ^
valor de resistência ‘y -
20
c
predito pelo modelo. 16.
•í5
C/D
12
£ -
8
-
8 10 12 14 16 18 20 22
tempo de hidratação (em dias)
Figura 1.3 Exemplo de um modelo empírico para explicar a resistência de um
concreto, em função do tempo de hidratação.
1.6 CONCEITOS BÁSICOS
Apresentaremos alguns conceitos que facilitarão a leitura deste livro. Esses
conceitos serão retomados nos capítulos seguintes com definições mais precisas.
O exemplo seguinte será usado para ilustrar os principais conceitos.
Exemplo 1.1 Considere uma indústria processadora de suco de frutas. Ao re­
ceber um carregamento de laranjas, os técnicos fazem inspeção da qualidade
nas frutas. Examinam uma amostra de cinco caixas, tomadas de forma aleatória
dentre toda a população de caixas do carregamento.
População: conjunto de elementos que formam o universo de nosso estu­
do que são passíveis de ser observados, sob as mesmas condições.
Amostra: parte dos elementos de uma população.
Amostragem: processo de seleção da amostra.
Amostragem aleatória sim ples: o processo de seleção dos elementos
é feito por sorteios, fazendo com que todos os elementos da população te­
nham a mesma chance de ser escolhidos e, além disso, todo subconjunto de
n elementos tenha a mesma chance de fazer parte da amostra.
Algumas características (ou variáveis) podem ser observadas nas cinco cai­
xas de laranjas amostradas, tais como:

18 ESTATÍSTICA
a) uma classificação por um técnico especializado (ótima, boa, regular,
ruim ou péssima);
b) número de laranjas não aproveitáveis por caixa;
c) peso de cada caixa de laranja etc.
O nível de mensuração de uma variável pode ser qualitativo, como no caso
(a), em que o resultado é uma qualidade ou atributo; ou quantitativo, como nos
demais casos, em que o resultado é um valor numa dada escala de medidas. As
variáveis mensuradas ao nível qualitativo serão chamadas de variáveis qualitati­
vas, e as mensuradas ao nível quantitativo, de variáveis quantitativas.
Ao selecionar uma caixa de laranja do carregamento, podemos contar o
número de laranjas não aproveitáveis e medir o peso da caixa. Como o resulta­
do de cada variável depende do processo aleatório de seleção da caixa de laran­
ja, preferimos usar a denominação variável aleatória.
Uma variável aleatória pode ser entendida como uma variável quantita­
tiva, cujo resultado depende de fatores aleatórios.
Ao realizar as observações de certa variável aleatória X, estamos observan­
do uma amostra de n elementos, {jci, x2,..., xrJ , da variável aleatória X. Por
exemplo, ao contar o número de laranjas não aproveitáveis em cada uma das
cinco caixas amostradas, temos um conjunto de cinco valores, digamos {4, 6, 2,
3, 0}, que corresponde à amostra efetivamente observada da variável aleatória
X = número de laranjas não aproveitáveis por caixa.1
Dada uma amostra, é comum calcular medidas descritivas das observa­
ções. Em nosso exemplo, podemos dizer que o número médio de laranjas não
aproveitáveis por caixa é (4 + 6 + 2 + 3 + 0)/5 = 3. Esse valor descreve o que
se observou na amostra, mas também pode ser interpretado como uma estima­
tiva do número médio de laranjas não aproveitáveis por caixa, no carregamen­
to todo.
Parâmetro: uma medida que descreve certa característica dos elementos
da população.
Estatística: uma medida que descreve certa característica dos elementos
da amostra.
Estimativa: valor resultante do cálculo de uma estatística, quando usado
para se ter uma ideia do parâmetro de interesse.
1 Observe que, antes de se fazer a seleção das cinco caixas, temos, na verdade, um con­
junto de cinco variáveis aleatórias {Xu X2,..., X5}, pois o valor de cada uma vai depender das cai­
xas selecionadas.

INTRODUÇÃO 19
Exemplos de parâmetros podem ser:
• média do número de laranjas não aproveitáveis por caixa;
• proporção do número de caixas classificadas como ótima etc.
Uma média ou proporção, quando referente a uma amostra e não a toda a
população, é chamada de estatística. Note que as definições de parâmetro e es­
tatística são muito parecidas, só que parâmetro refere-se à população e estatísti­
ca, à amostra.2 Por sua vez, o termo estimativa refere-se a um resultado numéri­
co, referente à amostra efetivamente observada.
No Capítulo 3, estudaremos várias medidas descritivas da amostra (estatís­
ticas) ou da população (parâmetros). Mas apresentaremos aqui duas medidas
bastante usadas: a média e a variância.
Média
Sejam n observações efetivas de certa variável aleatória X: {x1? x2,..., xn}.
Definimos média aritmética por:
(1.3)
Muitas vezes, vamos nos referir ao cálculo da média aritmética antes da
observação efetiva da amostra. Nesse caso, temos uma estatística, denotada por
X e chamada de média amostrai3
Por outro lado, caso se conheçam todas as possíveis observações de X (por
exemplo, a contagem em todas as caixas de laranja do carregamento), dadas
por x lf x2,..., xN, definimos o parâmetro média aritmética (ou média populacio­
nal) por:4
(1.4)
Às vezes, a população não tem tamanho finito. Imagine, por exemplo, rea­
lizar n observações do tempo de carga T de certo aplicativo, num sistema com-
2 Outra diferença é que os parâmetros são números reais, embora normalmente desco­
nhecidos. Já as estatísticas, antes de efetuar a amostragem, são variáveis aleatórias (dependem
da amostra a ser selecionada).
3 Note que a média amostrai é uma variável aleatória, pois seu valor depende da amos­
tra a ser selecionada.
4 Uma convenção neste livro é denotar as estatísticas por letras latinas e os parâmetros
por letras gregas; também usaremos letras maiúsculas para variáveis aleatórias e letras minúscu­
las para representar observações efetivas.

2 0 ESTATÍSTICA
partilhado, obtendo-se uma amostra {tb t2, ..., tn}. O número de observações
que você poderia fazer é ilimitado, mas mesmo assim pode considerar a popula­
ção como o conjunto (infinito) de possíveis observações de T, sob as mesmas
condições. E, também, considerar a média calculada da amostra, t, como uma
estimativa de uma média populacional fi, que representa o tempo médio ou tem­
po esperado de carga do aplicativo.
Desvios
A média pode ser considerada como um valor central, uma tentativa de
conhecer o valor real daquilo que se está medindo, desconsiderando o erro ex­
perimental. Para uma análise mais rigorosa do problema, toma-se fundamental
incluir alguma medida de variabilidade, como a variância. Esta medida baseia-se
nos desvios de cada valor em relação à média: dt = xt - x (i = 1, 2, ..., rz),
como ilustra a Figura 1.4.
Xj X Xj - x
o
A
4 3 1
<—> ^--->
6 3 3 x ,- x x, - x
<-
2 3 - 1 x ,- x X;-X
3 3 0
0 3 - 3
Figura 1.4 Desvios dos valores em relação à média: elementos básicos no cálculo
da variância.
Graus de liberdade
Podemos identificar uma observação x como um ponto em SR (pode ser
qualquer ponto de um subconjunto de formado pelas restrições da mensura-
ção). Da mesma forma, se são realizadas n observações independentes (xl} x2,
..., xn), podemos identificá-las como um ponto em (pode ser qualquer ponto
de um subconjunto de <Rfí formado pelas restrições da mensuração de cada ob­
servação). Dizemos, então, que uma amostra de n observações tem n graus de li­
berdade. Os desvios, dt = xt - x, embora sejam n resultados numéricos, têm
soma nula, fazendo com que o último desvio fique completamente determinado
pelos demais.5 Assim, os desvios têm (n - 1) graus de liberdade. Desta forma,

INTRODUÇÃO 21
uma amostra de tamanho n tem n graus de liberdade, os quais podem ser de­
compostos da seguinte maneira: 1 grau de liberdade para a média x e (n - 1)
graus de liberdade para os desvios dt = xt - x.
Variancia
Para calcular a variância, devemos considerar os desvios de cada valor em
relação à média aritmética. Depois, construímos uma espécie de média desses
desvios. Para evitar o problema dos desvios negativos, vamos trabalhar com os
desvios quadráticos, df = (x. - x )2. A variância é definida como a média arit­
mética dos desvios quadráticos. Por conveniência, vamos usar como denomina­
dor (n - 1) no lugar de n, ou seja, o número de graus de liberdade associados
aos desvios.6 Assim, definimos a variância de um conjunto de valores por:
(1.4)
Segue o cálculo da variância para os dados relativos ao número de laranjas
não aproveitáveis numa amostra de cinco caixas:
Xi X
-
n - l f t í 4
4 3 1 1
6 3 3 9
2 3 1 1
3 3 0 0
0 3 3 9
O valor da variância sozinho não traz informações relevantes, mas se con­
siderarmos que em uma amostra de outro carregamento a variância foi igual a
10, podemos deduzir que a segunda amostra tem mais variabilidade.
Caso se conheçam todas as possíveis observações de X (por exemplo, a
contagem em todas as caixas de laranja do carregamento), dadas por (xlf x2, ...,
xN), definimos o parâmetro variância (ou variância populacional) por:
(1.5)
onde (j. representa a média da população.
6 Uma justificativa mais formal dessa conveniência será dada no Capítulo 7, seção
7.3.1.

2 2 ESTATÍSTICA
Desvio padrão
A unidade de medida da variância é a unidade dos dados ao quadrado. No
Capítulo 3, são apresentadas formas alternativas para o cálculo da variância e
outras medidas de variabilidade, dentre elas o desvio padrão, que é definido
como a raiz quadrada positiva da variância e, portanto, tem a mesma unidade
de medida dos dados. No exemplo precedente, onde a variância foi de s2 = 5
laranjas2, o desvio padrão é igual a:
s = yj 5 laranjas2 = 2,236 laranjas
EXERCÍCIOS
1. Dê um exemplo de uma situação prática em que é mais razoável um modelo
empírico do que um modelo determinístico.
2. Apresente, em uma situação prática, qual é a população, uma forma de
amostragem e uma possível amostra.
3. Dada a seguinte amostra: {7, 8, 6, 5, 9, 4}, calcule:
a) a média;
b) a variância;
c) o desvio padrão.
4. Para avaliar a qualidade de três empacotadoras (A, B e C) de uma indústria
de torrefação de café, realizou-se uma amostra de dez pacotes de café de
cada empacotadora e mediu-se o peso líquido. O valor declarado é de 500
g. A empacotadora A apresentou peso médio igual a 500,1 g e variância
6,2; a B resultou em peso médio igual a 499,9 g e variância 40,5 e a C, peso
médio igual a 530,3 g e variância 5,8. O que se pode dizer sobre as empaco­
tadoras?
5. Ao calcular a variância de um conjunto de valores, encontrou-se o valor
s2 = 0. O que se pode dizer sobre o conjunto de valores?

2
O Planejamento de uma Pesquisa
2.1 ASPECTOS GERAIS
Para que os resultados de uma análise estatística de dados produzam in­
formações úteis, os dados precisam ser coletados de forma planejada. A Figura
2.1 ilustra as principais etapas de uma pesquisa, enfatizando que os métodos
estatísticos precisam ser pensados ainda na fase do planejamento da pesquisa.
Figura 2.1 Etapas usuais de uma pesquisa empírica.
Embora a Figura 2.1 ilustre as etapas da pesquisa em sequência, na fase do
planejamento é necessário também pensar na forma de análise dos dados, pois,

2 4 ESTATÍSTICA
dependendo da análise estatística que se deseja fazer, o projeto de pesquisa
deve ter suas peculiaridades. Assim, não discutiremos a questão do planejamen­
to de pesquisa somente neste capítulo, mas também quando estivermos discu­
tindo diferentes modelos de análise (Capítulos 7 a 11).
Em função do problema e dos objetivos da pesquisa, devemos decidir entre
uma pesquisa observacional e uma pesquisa experimental. Numa pesquisa ob­
servacional (ou de levantamento) as características de uma população são levan­
tadas (observadas ou medidas), mas sem manipulação. É o caso de um censo
demográfico, pesquisas eleitorais, pesquisas de mercado, inspeção da qualidade
etc. Em todos esses casos, quer-se ter ideia de certa população tal qual ela é na
natureza ou no processo.
Nas pesquisas experimentais, grupos de indivíduos (ou animais, ou objetos)
são manipulados para se avaliar o efeito de diferentes tratamentos. É o caso de
se verificar o rendimento de um processo químico para diferentes temperaturas
de reação, que são manipuladas de acordo com o interesse prático.
A seção 2.2 discute aspectos relacionados com pesquisas de levantamento,
enquanto a seção 2.3 enfatiza o planejamento de pesquisas experimentais.
2.2 PESQUISAS DE LEVANTAMENTO
Delimitação da população
Conforme definimos no capítulo anterior, chamamos de população o conjun­
to de elementos (indivíduos, objetos etc.) que formam o universo de nosso estu­
do e que são passíveis de ser observados, sob as mesmas condições. Num proces­
so de inspeção da qualidade, a população pode ser considerada como o conjunto
de todos os itens que saem da linha de produção; numa pesquisa de mercado, a
população é o conjunto de possíveis consumidores; e assim por diante.
Ao desenvolver uma pesquisa, planejamos fazer com que as conclusões se­
jam válidas para toda a população previamente definida, mesmo que a pesquisa
seja feita por amostragem. Contudo, se, numa pesquisa para estudar a dureza
de um tipo de aço, só tivermos disponibilidade de trabalhar com corpos de pro­
va de certo lote desse aço, tecnicamente as conclusões só valem para esse lote.
Variáveis a serem levantadas
As características que observamos nos elementos da população são chama­
das de variáveis. No exemplo anterior, a dureza é a variável fundamental de
nosso estudo. A cada corpo de prova, temos um e apenas um valor da dureza,
que supostamente é medida sempre sob as mesmas condições.

O PLANEJAMENTO DE UMA PESQUISA 25
A maioria dos estudos envolve mais que uma variável. A seleção adequada
das variáveis é fundamental para o sucesso de uma pesquisa.
Instrumentos para a mensuração de variáveis
Para realizar medidas físicas, normalmente temos instrumentos bem esta­
belecidos e unidades de medidas padrões. Por exemplo, o comprimento pode
ser medido por uma régua, que usa a escala métrica; a temperatura, por um
termômetro, que usa a escala de graus Celsius; e assim por diante. Quando de­
sejamos medir variáveis em seres humanos, geralmente precisamos construir
um questionário. Para variáveis quantitativas, devemos deixar claras as unida­
des de medida; para variáveis qualitativas, devemos especificar as possíveis ca­
tegorias ou atributos. Veja o exemplo seguinte:
Há quanto tempo o Sr. (ou Sra.) trabalha nesta empresa?
_____________ anos completos.
Qual é seu estado civil? ( ) solteiro ( ) casado
( ) viúvo ( ) desquitado ( ) divorciado
Em muitas situações, é comum tentar extrair de um indivíduo o grau de
certa característica (satisfação, conhecimento, aptidão etc.). Veja o exemplo se­
guinte:
Dê uma nota de 1 (um) a 5 (cinco), sendo 1 o grau mínimo e 5 o grau má­
ximo, para as seguintes características relacionadas com você e o curso que está
fazendo.
a) Didática dos professores de seu curso.............................. ( 1 2 3 4 5)
b) Grau de conhecimento dos professores............................( 1 2 3 4 5)
c) Bibliografia disponível......................................................... ( 1 2 3 4 5)
d) Laboratórios e outros recursos m ateriais.........................( 1 2 3 4 5)
e) Conteúdo dos programas das disciplinas oferecidas . . ( 1 2 3 4 5)
f) Encadeamento das disciplinas............................................( 1 2 3 4 5)
É comum o uso de procedimentos típicos de variáveis quantitativas (cálcu­
lo de médias aritméticas, por exemplo) para analisar dados gerados por esse
tipo de instrumento, embora seja um pouco forçoso assumir que essas escalas
sejam realmente quantitativas.

2 6 ESTATÍSTICA
Censo ou amostragem
A palavra censo refere-se à pesquisa de todos os elementos da população.
Geralmente, realizamos um censo quando:
• a população é pequena;
• as variáveis são fáceis de ser medidas ou observadas; ou
• necessitamos de resultados exatos.
Grande parte das pesquisas científicas ou de resoluções de problemas de
engenharia é feita por amostragem, ou seja, observamos apenas um subconjun­
to de elementos da população. A amostragem é particularmente interessante
quando:
• a população é grande ou infinita;
• as observações ou mensurações têm alto custo;
• as medidas exigem testes destrutivos;
• há necessidade de rapidez etc.
Em geral, o uso de amostragem leva à redução de custos e tempo. Mas a
amostragem precisa ser feita com critérios, pois pretendemos ter amostras que
permitam, a partir de uma análise estatística apropriada, obter conclusões satis­
fatórias sobre toda a população (veja a Figura 2.2).
AMOSTRAGEM
POPULAÇAO: todos os
AMOSTRA: um subconjunto
dos consumidores
INFERÊNCIA
Figura 2.2 Ilustração de um levantamento por amostragem para avaliar a pre­
ferência do consumidor.

O PLANEJAMENTO DE UMA PESQUISA 2 7
2.2.1 Técnicas de amostragem
Nesta seção, assumiremos que a população seja finita e composta de N ele­
mentos, salvo quando explicitamos o contrário. O número de elementos que se­
rão amostrados será representado por n.
Daremos ênfase às chamadas amostragens probabilísticas, que se caracteri­
zam por garantir que cada elemento da população tenha certa probabilidade p
conhecida de pertencer à amostra, sendo 0 < p < 1. Nessas amostragens, sem­
pre ocorre algum sorteio.
As amostragens probabilísticas são particularmente importantes nos pro­
cessos de inferência, pois os métodos estatísticos são construídos sob suas pro­
priedades. Descreveremos quatro tipos de amostragens probabilísticas:
• amostragem aleatória simples;
• amostragem sistemática;
• amostragem estratificada;
• amostragem de conglomerados.
Amostragem aleatória simples
Para a seleção de uma amostra aleatória simples, precisamos ter uma lista
completa dos elementos da população. Esse tipo de amostragem consiste em se­
lecionar a amostra através de sorteios, sem restrição.
A amostragem aleatória simples tem a seguinte propriedade:
Qualquer subconjunto da população, com o mesmo número de elementos,
tem a mesma probabilidade de fazer parte da amostra.
Em particular, temos que cada elemento da população tem a mesma pro­
babilidade de pertencer à amostra e esta probabilidade é dada por
A seleção de uma amostra aleatória simples pode ser facilitada com o uso
de números aleatórios, os seja, números resultantes de sucessivos sorteios do
conjunto {0, 1, 2,..., 9}, fazendo com que todo número com a mesma quantida­
de de algarismos tenha a mesma probabilidade de ocorrência. Existem algorit­
mos computacionais capazes de gerar dados que satisfazem aproximadamente
a esta propriedade, resultando nos chamados números pseudo-aleatórios. O
quadro a seguir apresenta alguns números pseudo-aleatórios gerados pelo Mi­
crosoft Excel:

2 8 ESTATÍSTICA
3820 1007 5964 8990 8845 9584 0145 4074 8632 1386 3002 8021 6960 2715 9040
2450 0455 0324 1641 2196 0171 2850 3431 5536 3573 2913 8021 7889 6759 7553
3718 3556 9102 4660 4261 3039 9756 8066 9911 2562 8503 5570 8730 4410 2177
9516 0534 7050 8164 9724 4663 3002 7501 3514 7756 3297 0860 9768 2855 5343
0743 1984 0641 3583 4870 5112 3734 9858 0407 2307 5745 7060 4014 1110 8973
0050 9261 1003 2567 7756 6796 8090 7243 0850 1323 6568 2584 7651 7002 8587
7561 6265 1736 4048 5523 7114 5551 1811 9702 6869 9120 9542 5943 5576 9681
5287 7966 8056 2622 1779 8667 1148 0595 7615 7383 6680 9268 4517 1681 0619
9862 9255 9038 5449 5007 6749 4898 1458 0380 7962 6018 9300 5339 1320 0823
Como ilustração, considere o problema de extrair uma amostra aleatória
simples de tamanho 5 da seguinte população de funcionários de uma empresa,
na qual identificamos cada indivíduo com um número:
01. Aristóteles 02. Anastácia 03. Arnaldo 04. Bartolomeu 05. Bernardino
06. Cardoso 07. Carlito 08. Cláudio 09. Ermüio 10. Ercílio
11. Emestino 12. Endevaldo 13. Francisco 14. Felício 15. Fabrício
16. Geraldo 17. Gabriel 18. Getúlio 19. Hiraldo 20. João da Silva
21. Joana 22. Joaquim 23. Joaquina 24. José da Silva 25. José de Souza
26. Josefa 27. Josefina 28. Maria José 29. Maria Cristina 30. Mauro
31. Paula 32. Paulo César
Para extrairmos uma amostra aleatória simples de tamanho n = 5, basta
tomar cinco números aleatórios do conjunto {01, 02, ..., 32}. Os funcionários
associados aos números selecionados formarão a amostra. Tomando números
da primeira linha e desprezando os valores que estiverem fora do conjunto {01,
02, ..., 32} e os valores que se repetirem, temos:
Números aleatórios: 20 10 07 01 32.
Amostra: {João da Silva, Ercílio, Carlito, Aristóteles, Paulo César}
A dificuldade para fazer uma amostragem desse tipo é ter um arquivo com
todos os elementos da população, pois a geração de números aleatórios e a
identificação dos indivíduos podem ser feitas com auxílio do computador.
A importância da amostragem aleatória simples é que as técnicas estatísti­
cas que serão apresentadas neste livro - e nos livros de estatística em geral -
supõem esse tipo de amostragem.

O PLANEJAMENTO DE UMA PESQUISA 2 9
Amostragem sistemática
Um processo mais simples é sortear o primeiro elemento e extrair os de­
mais sistematicamente. Mais especificamente:
• calcula-se o intervalo de seleção, dado por I = N /, desprezando as
decimais;
• sorteia-se o primeiro elemento do conjunto {1, 2, ..., /}; e
• completa-se a amostra, extraindo um elemento a cada I elementos.
No exemplo precedente, temos o intervalo de seleção 1 = 6. Devemos, en­
tão, sortear um elemento dentre os seis primeiros. Podemos fazer isso extraindo
um número, de um algarismo, do conjunto de números aleatórios apresentado
anteriormente. Tomaremos o primeiro número do conjunto que é “3”. Então, o
primeiro funcionário da amostra é o “Arnaldo”. Os demais são obtidos pelo in­
tervalo de seleção “6”, a partir do Arnaldo, resultando na seguinte amostra:1
(3) (9) (15) (21) (27)
{Arnaldo, Ermílio, Fabrício, Joana, Josefina}
Amostragem estratificada
A técnica da amostragem estratificada consiste em dividir a população em
subgrupos, que denominaremos de estratos. Esses estratos devem ser interna­
mente mais homogêneos do que a população toda, com respeito às variáveis em
estudo. Por exemplo, se para estudar a dureza de certo aço temos corpos de
prova de dois fornecedores, então a população dos corpos de prova pode ser di­
vidida em dois estratos.
Sobre os diversos estratos da população são realizadas seleções aleatórias
de forma independente. A amostra completa é obtida através da agregação das
amostras de cada estrato (veja a Figura 2.3).
Amostragem estratificada proporcional: a proporcionalidade do tamanho de
cada estrato da população é mantida na amostra. Por exemplo, se um estrato
abrange 20% da população, ele também deve abranger 20% da amostra.
Amostragem estratificada uniforme: selecionamos o mesmo número de ele­
mentos em cada estrato. É o processo usual quando se deseja comparar os di­
versos estratos.
1 Devido ao uso da parte inteira do número no cálculo do intervalo de seleção, o núme­
ro n de elementos da amostra pode ficar acima do valor planejado.

3 0 ESTATÍSTICA
POPULAÇAO
variância a* Suposição: a : < o (í = 1, 2 , Jc)
Estrato 1
subgrupo 1 da amostra
variância a/
Estrato 2 seleções r _
amostra
variância o * ^ aleatórias subgrupo 2 da amostra ^
estratificada
subgrupo k da amostra
Figura 2.3 Processo de amostragem estratificada.
Amostragem de conglomerados
Ao contrário da amostragem estratificada, a amostragem de conglomera­
dos tende a produzir uma amostra que gera resultados menos precisos, quando
comparada com uma amostra aleatória simples de mesmo tamanho. Contudo,
seu custo financeiro tende a ser bem menor, especialmente em amostragens de
grandes populações.
Chamamos de conglomerado um grupamento de elementos da população.
Por exemplo, numa população de domicílios de uma cidade, os quarteirões for­
mam conglomerados de domicílios. Ao avaliar a qualidade das laranjas de um
carregamento, as caixas de laranjas são os conglomerados.
Esse tipo de amostragem consiste, num primeiro estágio, em selecionar
conglomerados de elementos. Num segundo estágio, ou se observam todos os
elementos dos conglomerados selecionados no primeiro estágio (amostragem de
conglomerados em um estágio), ou, como é mais comum, se faz nova seleção, to­
mando amostras de elementos dos conglomerados extraídos no primeiro está­
gio (amostragem de conglomerados em dois estágios). Todas as seleções devem
ser aleatórias.
Outras formas de amostragem
Existem situações em que a seleção de uma amostra aleatória propriamen­
te dita é muito difícil ou até mesmo impossível. Mas uma forma muito comum
de extrair amostras em engenharia é através da amostragem acidental ou a
esmo. Exemplos:
a) para avaliar a qualidade em lotes de 1 kg de pregos, podemos exa­
minar n pregos de cada lote, extraídos a esmo;
b) para avaliar a qualidade em um carregamento de laranjas, podemos
examinar n caixas do carregamento, extraídas a esmo. Se a unidade
observacional é a laranja, em cada caixa podemos extrair, a esmo, m
laranjas.

O PLANEJAMENTO DE UMA PESQUISA 31
A seleção acidental nas situações anteriores parece produzir uma amostra
com as mesmas propriedades da amostragem aleatória simples. Contudo, nem
sempre isso acontece. Por exemplo, se numa pesquisa de mercado as pessoas
forem entrevistadas acidentalmente nas ruas mais movimentadas da cidade, en­
tão as pessoas que costumam passar por essas ruas têm maior chance de ser se­
lecionadas e, em consequência, pode haver viés nos resultados da pesquisa. O
conhecimento sobre o problema em estudo é fundamental no planejamento de
uma amostragem acidental.
Em muitas situações, lidamos com populações infinitas. Nesse caso, procu­
ramos realizar as n observações de forma independente e sob as mesmas condi­
ções. Exemplos:
a) para avaliar o desempenho de um sistema computacional em deter­
minada condição, realizam-se n ensaios independentes na condição
preestabelecida;
b) para avaliar a qualidade de itens que saem de uma linha de produ­
ção, observa-se um item a cada 15 minutos.2
Quando examinamos características de um material contínuo, procuramos
sortear - ou escolher a esmo - as posições em que serão coletadas as amostras.
É o caso de se examinar um carregamento de argila que chega em uma fábrica
de cerâmicas. Em materiais líquidos, costumamos homogeneizar a solução an­
tes da amostragem.
2.2.2 Tamanho da Amostra
Quando se fala em amostragem, a pergunta natural é qual deve ser o ta­
manho necessário da amostra. Mas a resposta não é simples. O cálculo do tama­
nho da amostra, para o caso da amostragem aleatória simples, que é a situação
mais fácil, será discutido no Capítulo 7. Contudo, gostaríamos de chamar a
atenção desde já para algumas questões básicas.
Um fator importante na determinação do tamanho da amostra é a variabi­
lidade da população em termos da variável em estudo. Por exemplo, uma amos­
tra de sangue pode ser bem pequena, pois o sangue é razoavelmente homogê­
neo em nosso corpo. Por outro lado, populações com variâncias grandes exigem
amostras maiores.
Outra questão importante é a relação entre tamanho da população (N) e
tamanho da amostra (n). Considerando uma precisão desejada para as estimati­
vas de interesse, a relação entre N e n não é linear (veja a Figura 2.4).
2 Se os itens forem extraídos em sequência, pode haver dependência entre as caracterís­
ticas dos itens.

3 2 ESTATÍSTICA
Figura 2.4 Relação entre tamanho da população e tamanho da amostra.
Como consequência da não linearidade entre N e n, devemos ter um cui­
dado adicional quando temos interesse em estudar separadamente certos sub­
grupos da população. Por exemplo, numa pesquisa eleitoral, podemos estar in­
teressados não só nos resultados de todo o país, mas também em resultados por
região demográfica. Nesse caso, as inferências por região normalmente carre­
gam um erro maior do que as inferências de todo o país.
EXERCÍCIOS
1. Considerando a população apresentada a seguir, extraia uma amostra alea­
tória simples de n = 6 funcionários. Use a segunda linha da tabela de nú­
meros aleatórios.
01. Aristóteles 02. Anastácia 03. Arnaldo 04. Bartolomeu 05. Bernardino
06. Cardoso 07. Carlito 08. Cláudio 09. Ermílio 10. Ercílio
11. Emestino 12. Endevaldo 13. Francisco 14. Felício 15. Fabrício
16. Geraldo 17. Gabriel 18. Getúlio 19. Hiraldo 20. João da Silva
21. Joana 22. Joaquim 23. Joaquina 24. José da Silva 25. José de Souza
26. Josefa 27. Josefina 28. Maria José 29. Maria Cristina 30. Mauro
31. Paula 32. Paulo César
2. Usando a terceira linha da tabela de números aleatórios, extraia uma amos­
tra aleatória simples de quatro letras do alfabeto da língua portuguesa.
3. Os elementos de certa população estão dispostos numa lista, cuja numera­
ção vai de 1.650 a 8.840. Descreva como você usaria uma tabela de núme­
ros aleatórios para obter uma amostra de 100 elementos. Seria necessário
efetuar nova numeração?

O PLANEJAMENTO DE UMA PESQUISA 33
4. Seja um conjunto de 20 corpos de prova numerados de 1 a 20. Usando
uma tabela de números aleatórios, divida aleatoriamente esses corpos de
prova em dois grupos de dez elementos.
5. Selecione uma amostra estratificada uniforme, de tamanho n = 12, da po­
pulação do Exercício 1.
6. Considerando a população de funcionários do exercício 1, faça uma amos­
tragem estratificada proporcional de tamanho n = 8, usando a variável
sexo para a formação dos estratos.
7. Comente os seguintes planos de amostragens, apontando suas incoerências,
quando for o caso.
a) Com a finalidade de estudar o perfil dos consumidores de um super­
mercado, observaram-se os consumidores que compareceram ao su­
permercado no primeiro sábado do mês.
b) Com a finalidade de estudar o perfil dos consumidores de um super­
mercado, fez-se a coleta de dados durante um mês, tomando a cada
dia um consumidor da fila de cada caixa do supermercado, variando
sistematicamente o horário da coleta dos dados.
c) Para avaliar a qualidade dos itens que saem de uma linha de produção,
observaram-se todos os itens das 14 às 14h30min.
d) Para avaliar a qualidade dos itens que saem de uma linha de produção,
observou-se um item a cada meia hora, durante todo o dia.
e) Para estimar a percentagem de empresas que investiram em novas tec­
nologias no último ano, enviou-se um questionário a todas as empre­
sas. A amostra foi formada pelas empresas que responderam ao ques­
tionário.
2.3 PLANEJAMENTO DE EXPERIMENTOS
Na área tecnológica, são muito comuns pesquisas experimentais, nas quais
se manipulam de forma planejada certas variáveis independentes ou fatores (A,
B, C, ...), para verificar o efeito que essa manipulação provoca numa certa va­
riável dependente ou resposta Y.
Exemplos
a) Verificar quais são os fatores que mais interferem na resistência à
compressão (7) de um concreto. Os fatores a serem estudados po­
dem ser:

3 4 ESTATÍSTICA
• tempo de hidratação (A);
• dosagem de cimento (£);
• qualidade do cimento (C);
• uso de aditivos (D).
b) Encontrar a melhor condição de operação de um processo químico.
A resposta Y pode ser o rendimento da reação química e os fatores
podem ser:
• tempo de reação (A);
• temperatura da reação (£).
c) Uma empresa de informática quer verificar o tipo de equipamento
adequado ao usuário. A resposta Y pode ser o tempo de resposta e
os fatores podem ser:
• processador (A);
• quantidade de memória RAM (£);
• quantidade de memória fixa (C);
• tipo de carga de trabalho a ser executada (D).3
Quando se conhece pouco sobre o problema em estudo, é comum buscar a
caracterização do processo, isto é, pesquisar quais são os fatores que provocam
maiores alterações na resposta. Geralmente, esses estudos iniciam com grande
número de fatores e, a partir de um estudo experimental planejado, faz-se uma
triagem de fatores, escolhendo os mais significativos. Em outros casos, já se co­
nhecem os fatores mais significativos e busca-se a combinação de níveis dos fa­
tores que levam à melhor resposta possível. É o que chamamos de otimização
do processo.
Estratégias no planejamento de experimentos
No planejamento de um experimento, devemos:
• reconhecer, estabelecer e delimitar claramente o problema;
• identificar os possíveis fatores que podem afetar o problema em estudo;
• verificar quais fatores poderão ser mantidos fixos e, portanto, não te­
rão seus efeitos avaliados no estudo experimental;
3 Cargas de trabalho são as solicitações feitas pelos usuários de um sistema. Por exem­
plo, as cargas de trabalho de uma CPU são as instruções a serem executadas; as cargas de traba­
lho de um banco de dados são as consultas dos usuários etc.

O PLANEJAMENTO DE UMA PESQUISA 35
• identificar, para cada fator, o intervalo de variação e os níveis que se­
rão estudados;
• escolher um projeto experimental adequado, isto é, saber como com­
binar os níveis dos fatores de forma que se possa resolver o problema
proposto com o menor custo possível;
• escolher a resposta adequada, ou seja, a variável Y que mede adequa­
damente o resultado (a qualidade, o desempenho etc.) do processo;
• planejar como será a análise dos dados do experimento.4
Exemplo 2.1 Considere o problema de operar adequadamente o protótipo de
uma catapulta romana em tamanho reduzido. O objetivo é lançar os projéteis a
uma distância especificada. O operador pode controlar três itens da catapulta:
altura do pivô, comprimento do braço e ângulo de parada. Veja a Figura 2.5.5
Figura 2.5 Protótipo reduzido de uma catapulta romana (Exemplo 2.1).
Um experimento pode ser planejado para verificar as condições de opera­
ção da catapulta que a levam a atingir seu objetivo. Parece natural que os se­
guintes fatores podem alterar o resultado do processo:
• altura do pivô (A);
• comprimento do braço (£);
• ângulo de parada (C).
4 Eventualmente, pode haver mais que uma resposta, mas estudaremos uma por vez.
5 Ilustração extraída do artigo de LUNER, J. J. Quality Engineering, v. 6, n° 4, p.
691-705, 1994.

3 6 ESTATÍSTICA
A região de variação desses fatores deve ser determinada por conhecimen­
to prévio do processo. Se não houver conhecimento suficiente, podemos optar
por uma variação grande e, em experimentos posteriores, reduzir a variação.
Também parece razoável supor que, ao variar cada um desses fatores de seu ní­
vel mínimo até seu nível máximo, o desempenho do processo deve melhorar
até certo ponto e, depois, piorar, caracterizando efeitos não lineares. Assim, é
recomendável usar pelo menos três níveis em cada fator, tais como mostrados
na tabela a seguir:
Fator Nível inferior Nível intermediário Nível superior
A 6,35 cm 10,16 cm 13,97 cm
B 0,81 cm 5,08 cm 9,35 cm
C 300 45° 90°
Poderiam ser identificados outros fatores, tais como pequenas variações no
peso do projétil, variações na banda de borracha, fadiga etc. Como esses fatores
são muito difíceis de ser controlados na operação natural do processo, eles tam­
bém não foram controlados no experimento. Devido à presença de fatores não
controláveis - o que é comum na grande maioria dos experimentos -, toma-se
fundamental usar replicações e aleatorização. Esses procedimentos serão descri­
tos ainda nesta seção.
Um possível projeto experimental para este exemplo é o projeto fatorial,
em que cada nível de um fator é cruzado com todos os níveis dos outros fatores,
conforme será discutido na seção 2.3.4.
A variável dependente, ou resposta, deve avaliar o desempenho ou quali­
dade do processo. No presente exemplo, ela pode ser a distância entre a queda
do projétil e o alvo pretendido.
A Figura 2.6 apresenta um esquema geral de um problema de planejamen­
to de experimento.
fatores controláveis: A B C
r
Y CZD <E>
O O O PROCESSO
^ SlV ^ '■V ^ S"V
O O O ílLn------------------------------- ------------------------------ C£)
O O O A ®
s s s
fatores não controláveis: Z, Z2 Z,...
Figura 2.6 Esquema geral de um problema de planejamento de experimento.

O PLANEJAMENTO DE UMA PESQUISA 3 7
Escolha das unidades experimentais e uso de blocos
As entradas de um processo são as unidades experimentais que serão estu­
dadas. Em engenharia, as entradas costumam ser corpos de prova; em medicina,
são os indivíduos; em informática, são as cargas de trabalho; e assim por diante.
É desejável fazer com que as entradas sejam tão homogêneas quanto possível,
mas, se isso não é possível ou se o estudo quer extrair conclusões para grupos
heterogêneos, devemos tentar construir blocos relativamente homogêneos. Por
exemplo, se os corpos de prova vêm de diferentes lotes, cada lote pode consti­
tuir um bloco. No exemplo da catapulta, se os projéteis têm diferentes formas
ou pesos, podemos tentar formar grupos (blocos) de projéteis similares. Veja a
Figura 2.7.
unidades experimentais
blocos gDi O o o >
relativamente aDl o o o >
homogêneos 0Dt o o o >
Figura 2.7 Formação de blocos para garantir homogeneidade nas entradas.
Em agronomia, costumamos formar blocos de canteiros homogêneos. Na
Ciência da Computação, ao comparar diferentes sistemas computacionais, po­
demos usar o mesmo conjunto de cargas de trabalho em todos os sistemas em
comparação. As observações associadas a uma particular carga de trabalho po­
dem ser consideradas como pertencentes a um mesmo bloco.
Os fatores
Os fatores de um estudo experimental são os fatores controláveis do pro­
cesso que podem afetar seu desempenho. Algumas vezes, incluímos também fa­
tores não controláveis no processo, mas que podem ser controlados em labora­
tório. A inclusão de fatores não controláveis é importante quando se busca
produzir produtos robustos, isto é, produtos pouco sensíveis às variações de fa­
tores ambientais ou de outros ruídos.
Tratamentos
Chamamos de tratamento uma particular combinação de níveis dos fatores
incluídos no modelo do estudo experimental. No exemplo da catapulta, a com­
binação de todos os fatores no primeiro nível (altura do pivô em 6,35 cm, altu­
ra do braço em 0,81 cm e ângulo de parada em 30°) forma um possível trata­
mento. Quando usamos blocos, devemos tentar fazer com que em cada bloco
sejam realizados todos os tratamentos em estudo.

3 8 ESTATÍSTICA
Replicações
Normalmente, realizamos mais de um ensaio em cada condição experi­
mental (tratamento). Ou seja, realizamos replicações. Com as replicações, pode­
mos avaliar o erro experimental, isto é, o efeito provocado pelos possíveis fato­
res que estão agindo no processo, mas que não foram incluídos no estudo.
Aleatorização
Para garantir a validade de um estudo experimental, a alocação dos trata­
mentos nas unidades experimentais deve ser áleatorizada.6 Veja o Exemplo 2.2.
Exemplo 2.2 Desejamos estudar a produção por m2 (Y), de certa cultura,
considerando três níveis de dosagens (a, b e c) de certo fertilizante. Dispomos
de seis canteiros para o experimento, donde podemos fazer duas replicações.
Para aleatorizar o tratamento a ser aplicado em cada canteiro, podemos fazer
uso de números aleatórios. A seguir, é reproduzida uma linha do quadro de nú­
meros aleatórios da seção 2.1:
2450 0455 0324 1641 2196 0171 2850 3431 5536 3573 2913 8021 7889 6759 7553
Excluindo os números fora do conjunto {1, 2, 3, 4, 5, 6} e os que se repe­
tem, temos o seguinte projeto experimental para o problema em questão:
Tratamento: a a b b c c
Canteiro (ordem aleatória): 2 4 5 3 1 6
Se for identificado algum fator de heterogeneidade nos canteiros e se estes
puderem ser agrupados em dois blocos relativamente homogêneos - digamos,
bloco 1 formado pelos canteiros 1, 2 e 3 e bloco 2 pelos canteiros 4, 5 e 6 -, o
esquema do projeto experimental ficaria assim:
Bloco: 1 1 1 2 2 2
Tratamento: a b c a b c
Canteiro: 2 1 3 4 5 6
(ordem aleatória em cada bloco)
6 Quando os ensaios são realizados em tempos diferentes, a ordem dos ensaios também
deve ser aleatorizada.

O PLANEJAMENTO DE UMA PESQUISA 3 9
2.3.1 Projetos com um fator
Embora o objetivo deste capítulo não seja mostrar técnicas de análise de
dados experimentais, faremos algumas considerações, que serão usadas em pro­
jetos mais elaborados.
O Exemplo 2.2 mostrou um problema com apenas um fator (dosagem de
fertilizante). Dois projetos experimentais foram ilustrados: completamente alea-
torizado e com blocos aleatorizados. No momento, estudaremos com mais deta­
lhes somente o primeiro caso, que deve produzir dados da seguinte forma:
Tratamento: a a b b c c
Canteiro (ordem aleatória): 2 4 5 3 1 6
Resposta: y n y 12 y 2\ y22 y3i y32
onde yij representa o valor da produção por m2, considerando a j-ésima replica-
ção do tratamento í (£ = 1, 2, 3;j = 1, 2). O cálculo da média amostrai, calcula­
da para dado tratamento, fornece uma estimativa da produção esperada na con­
dição experimental em questão. Em nosso exemplo:
y _ yn + y n y - y 2i + y 22 e y _ y 3i + y 32
2 9 2 2
Conforme discutimos no Capítulo 1, é fundamental avaliar também a va­
riabilidade do fenômeno em estudo. Assim, podemos calcular a variância amos­
trai da produção em cada tratamento (ver seção 1.6), como segue:
„2 _ ( y n - y . ) 2 + ( y t2 - y J 2 „2 _ ( y 21 - y 2)2 + ( y 22 - y 2)2 .
òl ~ ^ > ò2 — ^ > C
3-y*y - y^y
2 _ (y 1
1
Note que, para avaliar a variabilidade, precisamos ter pelo menos duas ob­
servações em cada tratamento. Com duas observações, temos apenas 1 grau de
liberdade; com n observações, temos n - 1 graus de liberdade. Os graus de liber­
dade são usados no denominador do cálculo das variâncias.
Geralmente, supomos que a variabilidade não se altera com os diferentes
tratamentos. Assim, em nosso exemplo, podemos agregar as três variâncias
amostrais, produzindo uma única medida de variabilidade com três graus de li­
berdade (soma dos graus de liberdade das três variâncias amostrais):

4 0 ESTATÍSTICA
No Capítulo 9, veremos que uma estimativa da variância é fundamental
para avaliar se diferenças observadas entre as médias dos tratamentos são
reais, ou podem ser meramente explicadas por variações casuais associadas ao
erro experimental.
De maneira geral, em um projeto completamente aleatorizado com um fa­
tor, tendo g tratamentos (unidades experimentais divididas aleatoriamente em
g grupos) e n replicações em cada tratamento, temos:
(2.1)
(i = 1, 2, ..., g) (2.2)
E a variância agregada, que mede a variabilidade devida ao erro experi­
mental, é dada por:
2 2
+ 52 +
2 (2.3)
A variância agregada tem g (n - 1) graus de liberdade, pois são agregadas
g variâncias com n - 1 graus de liberdade em cada uma.
Se, na realização do experimento do Exemplo 2.4, obtivermos os seguintes
dados:
Tratamento: a a b b c c
Respostas: y n = 12 y u = 14 y 2l = 16 y 22 = 17 y 3i = 15 y 32 = 15
Temos as seguintes médias e variâncias associadas a essa amostra:
Médias: y j = 13 y 2 = 16,5 y3 = 15
Variâncias: sf =2 sj = 0,5 s 2 = 0
Variância agregada: sjj 0,833.
3
2.3.2 Projetos fatoriais
Os experimentos normalmente envolvem vários fatores. Uma forma efi­
ciente de combinar os níveis dos diversos fatores é cruzando-os, de tal forma que
cada nível de um fator seja combinado com todos os níveis dos outros fatores.

O PLANEJAMENTO DE UMA PESQUISA 41
Exemplo 2.3 Considere um processo químico em que se quer pesquisar a in­
fluência dos fatores:
• o tipo de catalisador (A), com dois níveis (a1? a2) e
• o tempo de reação (£), com quatro níveis (bi, b2, b3, b4),
sobre o rendimento da reação química (Y).
Um projeto fatorial consiste em considerar 2 x 4 = 8 tratamentos, confor­
me mostrado na Figura 2.8.
fatorB
b b — ---------- b, b,
a. ab, ab, ab.
fator A
a ab, a,bA
Figura 2.8 Esquema de um projeto fatorial 2 x 4 .
No exemplo da catapulta (Exemplo 2.1), em que temos três fatores ensaia­
dos a três níveis, o projeto fatorial englobaria 3 x 3 x 3 = 33 = 27 ensaios. Veja
a Figura 2.9.
Figura 2.9 Representação geométrica de um projeto fatorial 33.
Nos projetos fatoriais, podemos avaliar não somente o efeito médio de
cada fator, mas também possíveis interações entre os fatores. Dizemos que exis­
te interação entre dois fatores quando a diferença na resposta entre os níveis de
um fator não é a mesma para todos os níveis do outro fator.
A Figura 2.10 mostra dois possíveis resultados associados ao experimento
descrito no Exemplo 2.3. No primeiro, os fatores tipo de catalisador e tempo de
reação agem aditivamente sobre o rendimento da reação química, permitindo
analisar cada fator separadamente: a mudança no catalisador altera o rendi-

4 2 ESTATÍSTICA
mento em cinco unidades e, a cada variação de nível do tempo de reação, há al­
teração em torno de três unidades no rendimento. Já o gráfico (b) mostra uma
situação com interação. Só é possível analisar o efeito de um fator condicionado
ao outro.
(a) Dois fatores agindo aditivamente (b) Interação entre dois fatores
tempo de reação (min) tempo de reação (min)
Figura 2.10 Dois possíveis perfis de médias para o experimento do Exemplo 2.3.
Na engenharia, era muito comum realizar experimentos, variando um fa­
tor de cada vez. Esse procedimento não permitia verificar possíveis interações
entre os fatores e, muitas vezes, levava a conclusões errôneas.
2.3.3 Projetos com muitos fatores
Em muitos problemas, o número de fatores que possivelmente alteram a
resposta é grande. Por exemplo, para verificar quais são os fatores que mais in­
terferem na resistência à compressão de um concreto (7), podemos citar:
• tempo de hidratação (A);
• a dosagem de cimento (£);
• a qualidade do cimento (C);
• o uso de aditivos (D).
Se forem usados três níveis em cada fator, teremos 34 = 81 ensaios, sem
contar com replicações adicionais, o que tende a encarecer demasiadamente o
experimento.
Projetos fatoriais 2k
Consiste em ensaiar cada um dos k fatores em apenas dois níveis. Além de
evitar grande número de ensaios, esse tipo de projeto é relativamente fácil nos

O PLANEJAMENTO DE UMA PESQUISA 4 3
aspectos computacionais e interpretativos. A Figura 2.11 representa geometri­
camente os 16 pontos a serem ensaiados em um projeto para avaliar quatro fa­
tores.
D
B B
Figura 2.11 Representação geométrica de um projeto fatorial 24.
Projetos do tipo T são largamente utilizados para caracterizar processos,
ou seja, para selecionar fatores que agem significativamente sobre a resposta.
Muitas vezes, quando se deseja otimizar o processo, realiza-se, inicialmente, um
projeto 2k para selecionar os fatores mais significativos e, depois, realizam-se
novos experimentos.
Denotaremos por “+1”, ou simplesmente por “+ ”, o nível superior de um
fator; e por “-1” ou o nível inferior.7 Definimos como efeito principal do fa­
tor a diferença média na resposta quando se passa do nível -1 para o nível +1.
Veja o exemplo a seguir, relativo a um projeto 22, com os resultados de Y em
cada condição experimental:
fator B
15+17 10+12 c
+
e/(A) = — ------------- — = 5
+ C 15
fator A
e/(B) = 12± 1 7 - 10± 1 5 = 2
10
Note que, se o fator B estiver no nível -1, ao variar A de -1 para +1, a va­
riação na resposta é de 5 unidades. Se B estiver no nível +1, ao variar A de -1
para +1, a variação na resposta também é de 5 unidades. Ou seja, o presente
exemplo não tem interação. De modo geral, podemos calcular o efeito da intera­
ção entre dois fatores (A e B) através da diferença da média de quando ambos
estão no mesmo nível (- 1 ou +1) em relação à média de quando eles estão em
níveis trocados. No exemplo em discussão, temos:
7 Para fatores qualitativos, tal como o tipo de catalisador (a, ou a2), os códigos + e - po­
dem ser colocados em quaisquer dos níveis dos fatores.

4 4 ESTATÍSTICA
ef(AB) = 1P —17- - *-2 —15- =0
2 2
Para facilitar o cálculo dos efeitos, podemos organizar os resultados de Y
numa tabela que considera todas as combinações dos fatores, indicando, para
cada fator, seu nível (-o u +). Segue a tabela dos sinais para um projeto 22, in­
cluindo a coluna de elementos unitários I, associada à média global, em que to­
dos os sinais são positivos; e a coluna da interação AB, em que os sinais são ob­
tidos através da multiplicação de elemento a elemento das colunas A e B.
Condição
I A B AB Y
experimental
1 + + ?
— —
•
2 + + ?
— — •
3 + +
— — ■
4 + + + +
■
Ao realizar o experimento, temos os valores para a resposta Y em cada
condição experimental. O cálculo de qualquer efeito (principal ou de interação)
pode ser feito por:
(2.4)
onde:
y+ é a média das observações de Y nas condições experimentais em que
o sinal do fator é positivo e
é a média das observações de Y nas condições experimentais em que
o sinal do fator é negativo.
Exemplo 2.4 Um estudo foi desenvolvido para verificar os fatores que in­
fluenciam a qualidade da transmissão de dados através da porta serial de mi­
crocomputadores. Propositalmente, foram usados cabos com comprimento bas­
tante superior às especificações técnicas. Observou-se a taxa de falhas de
transmissão em função dos fatores: (A) velocidade da transmissão (2.400/9.600
bauds), (£) tamanho do arquivo (100/200 bytes) e (C) comprimento do cabo
serial (15/20 m). Os resultados do experimento, que foi realizado com 2 repli-
cações, foram:8
8 O sinal negativo indica o nível inferior do fator e o sinal positivo indica o nível supe­
rior do fator. Este exemplo é parte de um trabalho de disciplina do acadêmico Maximiliano Pez-
zin, Curso de Pós-Graduação em Ciência da Computação - UFSC, 2001.

O PLANEJAMENTO DE UMA PESQUISA 4 5
Condição Rep. 1 Rep. 2
A B C
experimental
y y
1 32,5 32,3
— — —
2 + 35,7 35,9
— —
3 + 33,1 33,4
— —
4 + + 35,9 36,1
—
5 + 34,1 34,4
— —
6 + + 36,6 36,9
—
7 + + 34,2 34,9
—
8 + + + 37,1 36,9
A tabela seguinte inclui os sinais para o cálculo da média global ffl e de
todas as interações possíveis (AB, AC, BC e ABC). Os sinais de cada interação
correspondem aos sinais da multiplicação de elemento a elemento dos vetores
nela envolvidos.
Condição Rep. 1 Rep. 2
I A B C AB AC BC ABC
experimental
y y
1 + + + + 32,5 32,3
— — — —
2 + + + + 35,7 35,9
— — — —
3 + + + + 33,1 33,4
— — — —
4 + + + + 35,9 36,1
— — — —
5 + + + + 34,1 34,4
— — — —
6 + + + + 36,6 36,9
— — — —
7 + + + + 34,2 34,9
— — — —
8 + + + + + + + + 37,1 36,9
Para calcular o efeito do fator A, ef(A), calculamos a média das observa­
ções em que A tem sinal positivo e a média das observações em que A tem sinal
negativo, ou seja:
34,1 + 34,4 + 36,6 + 36,9 + 34,2 + 34,9 + 37,1 + 36,9 oc
y . = ---------------------------------------------------------------------- = jjjO j /d
8
_ = 32,5 + 32,3 + 35,7 + 35,9 + 33,1 + 33,4 + 35,9 + 36,1 3625
y " " 8 '
Assim,
ef(A) = 35,6375 - 34,3625 = 1,275

4 6 ESTATÍSTICA
ou seja, quando a velocidade de comunicação passa de 2.400 bauds para 9.600
bauds, estimamos que a taxa média de falhas aumenta em 1,275 pontos. De for­
ma análoga, podemos calcular todos os demais efeitos, cujos resultados são
mostrados abaixo:
média global = 35,000
e/CA) = 1,275 e/CAB) = - 0,125
e/(B) = 0,400 e/CAC) = - 0,300
e/CO = 2,775 tf (BC) = - 0,175
ef(ABC) = 0,150
Nesse exemplo, os efeitos das interações são bastante pequenos, o que per­
mite interpretar o efeito de cada fator isoladamente.
Projetos fatoriais fracionados 2k ~p
Quando temos muitos fatores, mesmo que sejam ensaiados em apenas dois
níveis, a quantidade de tratamentos torna-se muito grande. Com oito fatores,
por exemplo, temos 28 = 256 tratamentos. A ideia dos projetos fracionados é
ensaiar apenas parte das possíveis combinações, mas planejado de tal forma
que garanta a possibilidade de estimar os efeitos principais e, às vezes, as inte­
rações entre dois fatores.
Os projetos fracionados são particularmente importantes quando se pre­
tende fazer uma triagem de fatores para serem usados em estudos posteriores.
Um bom fracionamento pode ser feito realizando-se os ensaios cujo sinal
de I é igual ao sinal da interação com todos os k fatores. Ou, equivalentemente,
realizando-se os ensaios do grupo complementar. Nesse caso, temos um projeto
2k com 1 fracionamento, que denotaremos por 2k ~ l. No projeto 23, por exem­
plo, podemos realizar os ensaios em que vale a relação I = ABC ou os ensaios
da relação I = - ABC. Esses dois grupos de condições experimentais são indica­
dos na tabela de sinais, a seguir:

O PLANEJAMENTO DE UMA PESQUISA 4 7
Fazendo somente os ensaios que satisfazem à relação I = ABC, temos:
Condição
I A B C AB AC BC ABC
experimental
1) 2 + + + +
— — — —
2) 3 + + + +
— — — —
3) 5 + + + +
— — — —
4) 8 + + + + + + + +
Note, pela representação geométrica ao lado, que, se os
pontos ensaiados forem projetados em qualquer dos três pia-
A
nos, passamos a ter um projeto 22 completo.
R
Observando a tabela de sinais do projeto 23 " verificamos que algumas
colunas são iguais. Em especial: A = BC, B = AC eC = AB. Logo, com esse pro­
jeto, não é possível distinguir os efeitos principais das interações entre dois fa­
tores - existe confusão entre esses efeitos. Consequentemente, o projeto 23" 1 só
pode ser usado nas situações em que se supõe não haver interações ou que os
efeitos das interações possam ser negligenciados.
Para construir um projeto 23" l, podemos fazer um projeto 22 completo e,
depois, incluir o fator C com sinais equivalentes a AB. Em geral, na construção
de um projeto 2k " l, fazemos um projeto completo com k - 1 fatores e, depois,
incluímos o último fator com os mesmos sinais da interação dos k - 1 fatores
previamente definidos.
Veja, agora, a tabela de sinais de um projeto 24_ l, com a relação I = ABCD.9
Foram incluídas as colunas relativas aos efeitos principais e às interações de se­
gunda ordem, isto é, entre dois fatores. As colunas relativas às interações de or­
dem superior (entre três ou mais fatores) não foram incluídas na tabela.
Condição
I A B C D AB AC AD BC BD CD
experimental
1 + + + + + + +
— — — —
2 + + + + +
— — — — — —
3 + + + + +
— — — — — —
4 + + + + +
— — — — — —
5 + + + + +
— — — — — —
6 + + + + + +
— — — — —
7 + + + +
— — — — — — —
8 + + + + + + + + + + +
9 A construção da tabela dos sinais desse projeto pode ser feita através de todas as com­
binações dos fatores A, B e C, como no projeto 23 completo. Para os sinais de D, faz-se D = ABC.

4 8 ESTATÍSTICA
Observamos que as colunas A, B, C e D não se igualam com colunas de in­
teração de segunda ordem, mas existem algumas igualdades entre estas (por
exemplo, AD = BC).10 Consequentemente, o projeto 24“ 1 é uma boa alternativa
quando se deseja avaliar apenas os efeitos principais.
Em um projeto 25 “ !, não existe confusão entre os efeitos principais nem
entre interações que envolvem dois fatores. Ou seja, cinco fatores podem ser es­
tudados tranquilamente com 25 " 1 = 16 pontos experimentais. Com seis ou
mais fatores, é possível fazer dois fracionamentos (ver o Exercício 11).
EXERCÍCIOS
.
8 Apresente as 32 combinações de sinais em que os fatores A, B, C, D e E de­
vem ser ensaiados em um projeto 25 completo. Anote os ensaios que devem
ser realizados em um projeto 25 “l, considerando a relação I = ABCDE. Repa­
re que você pode construir o mesmo projeto fazendo, inicialmente, um pro­
jeto 24 completo e, depois, inserindo a coluna E com a relação E = ABCD.
9. Calcule a variância agregada do experimento do Exemplo 2.4. Quantos
graus de liberdade estão associados a essa medida?
10. Para avaliar o efeito dos fatores: (A) tempo de hidratação (14 dias/28
dias), (£) relação água/cimento (0,38 e 0,58) e (C) tipo de cimento (co­
mum e pozolânico) na resistência à compressão de um concreto (7), reali­
zou-se um experimento cujos resultados da resistência (em MPá) são apre­
sentados a seguir:11
Tempo de hidratação
Tipo de Relação
cimento água/cimento
14 dias 28 dias
comum 0,38 23,1 42,2
0,58 12,0 27,9
pozolânico 0,38 24,3 39,5
0,58 11,1 24,3
Calcule os efeitos principais e as interações de segunda ordem.
10 No projeto 2' - \ os efeitos principais estão confundidos com interações de terceira or­
dem (entre três fatores), mas os efeitos destas interações geralmente são negligenciáveis.
11 O exercício é parte de um trabalho de disciplina dos acadêmicos F. Pelisser e L. Matos
do Programa de Pós-Graduação em Engenharia Civil - UFSC, 2001. Os dados são hipotéticos,
mas foram baseados em HELENE, P. R. L.; TERZIAN, P. Manual de dosagem e controle do concreto.
São Paulo: PINI, 1995.

O PLANEJAMENTO DE UMA PESQUISA 4 9
11. Em Applied Statistics, v. 42, nQ 4, p. 671-681 (1993), M. G. Tuck e J. I. L.
Cottrell realizaram vários experimentos para obter uma farinha de pão de
melhor qualidade. Misturaram à farinha de trigo pequenas quantidades de
ingredientes permitidos. Os fatores correspondem à quantidade de cada in­
grediente adicionado à farinha, sendo que o nível inferior corresponde à
ausência do ingrediente. Parte de um dos experimentos foi realizada sob
um projeto 26 ~ 2, em que os fatores A, B, C e E formaram um projeto 24
completo. Os sinais do fator D foram obtidos através da relação D = ABC e
os sinais do fator F foram obtidos através da relação F = BCE. A resposta
(y) foi o volume médio dos pães. Em cada condição experimental, realiza­
ram-se quatro ensaios. A tabela, a seguir, apresenta a média y e o desvio
padrão s do volume específico nas quatro replicações em cada combinação
dos níveis dos fatores.
Condição ^
B C D E F y s
experimental
— — — — — —
1 429,25 75,39
2 — + + 433,00 69,40
— — —
3 + + — + 454,25 88,99
— —
4 + + + — 456,75 82,24
— —
5 + + + 446,75 74,09
— — —
6 + + + 447,75 80,93
— — —
7 + + 455,50 89,58
— — — —
8 + + + + 448,25 74,24
— —
9 + + 458,75 79,47
— — — —
10 + + + + 449,50 84,58
— —
11 + + + 463,75 91,67
— — —
12 + + + 466,00 88,99
— — —
13 + + + 449,50 88,88
— — —
14 + + + 452,75 98,27
— — —
15 + + + + 469,00 82,30
— —
16 + + + + + + 471,50 75,11
a) Calcule os efeitos principais dos seis fatores. Quais provocam maiores
variações no nível médio da resposta? Em que níveis eles devem ser fi­
xados para maximizar o volume dos pães?
b)
Calcule os efeitos principais em termos do desvio padrão s. Qual fator
provoca maior alteração na variabilidade da resposta? Se o objetivo é
minimizar a variabilidade, em qual nível este fator deve ser fixado?

3
Análise Exploratória de Dados
Com o advento da informática, o mundo encheu-se de dados. As empresas
têm dados de suas atividades, de seus funcionários, de seus clientes etc. Mas
para que esses dados sejam informativos, necessitamos organizá-los, resumi-los
e apresentá-los de forma adequada. Este é o papel da estatística descritiva.
Como ilustração, considere o problema da pasteurização de leite em um
laticínio, em que os engenheiros estão preocupados com a variação da tempera­
tura do pasteurizador. Para se conhecer o nível dessa variação, foram emprega­
das 1.389 leituras de temperatura, realizadas durante dois meses.1 A Figura 3.1
mostra parte do conjunto das observações e um gráfico que apresenta a distri­
buição de frequências das 1.389 observações.2 Note que o gráfico é mais infor­
mativo do que os dados brutos!
Na análise exploratória de dados, além de descrever os dados, buscamos
conhecer algumas características do processo, com base nos dados. Com o uso
adequado de tabelas, gráficos e medidas, podemos descobrir certas estruturas
que não eram evidentes nos dados brutos. Hoje também se usa a expressão mi­
neração de dados (data mining), que significa a busca por relacionamentos não
triviais, que podem estar escondidos em grandes massas de dados. Em geral,
numa mineração de dados, são aplicadas técnicas estatísticas e computacionais.
1 Extraído da dissertação de mestrado de Luciana S. C. V. da Silva (Programa de
Pós-Graduação em Engenharia de Produção, UFSC, 1999).
2 A construção de distribuições de frequências é objeto de estudo deste capítulo.

ANÁLISE EXPLORATÓRIA DE DADOS 51
Temperatura (°C)
Temperatura do pasteurizador
30'J 1 1 1 —... r i
74,8 74,0 74,7 74,4 75,9
—
73,8 74,4 74,8 76,8 73,6 3 230 —
H
3
75,3 73,4 74,7 73,4 74,2 Aaá 200 - -|
’53
o
76,4 73,2 76,5 75,6 73,5
150 - J
76,3 74,1 75,0 76,0 74,7 e
£
E 1O0
76.8 74,3 74,9 77.0 75.1 •3
z
so -
72.9 72,9 74,6 75.0 75.1
74,9 74,5 77,1 74,6 74,8 0 " k 1
71 72 73 74 75 76 77 78
temperatura C
Figura 3.1 Parte dos dados brutos e um gráfico de distribuição de frequências.
3.1 DADOS E VARIAVEIS
Depois de realizado um levantamento de dados, eles são colocados em ar­
quivos, sob a forma de matrizes. As linhas dessas matrizes correspondem ao
que se observou em cada elemento pesquisado, enquanto as colunas correspon­
dem às características (variáveis) levantadas. Por exemplo, na atualização das
páginas de um site, podemos querer avaliar o perfil dos indivíduos que acessam
esse site. Então, precisamos levantar, junto a cada indivíduo, algumas de suas
características, tais como o sexo, a idade, o nível de instrução e o provedor uti­
lizado. Ao realizar a pesquisa, podemos produzir uma matriz de dados, da se­
guinte forma:
variáveis
nível de
usuário sexo idade provedor
instrução
1 M 35 superior C
indivíduos 2 F 18 fundamental A
dados
ou casos • • • • • • •
• • • ■ • • • •
n F 23 médio C
No controle da qualidade de uma linha de produção de azulejos, podemos
observar algumas características em azulejos extraídos periodicamente da fase
final da linha de produção. Essas características podem ser: empeno, desvio má­
ximo da dimensão ideal, variações na tonalidade da cor etc. Considerando que a
última variável produza uma classificação do tipo A, B e C, a matriz de dados
pode ser apresentada como:

5 2 ESTATÍSTICA
variáveis
empeno desvio
azulejo classificação
(mm) (mm)
1,2 2,1 B
unidades
0,4 1,7 C
dados
ou casos
• • ■
0,3 0,5
Os dados podem ser observações de variáveis qualitativas ou de variáveis
quantitativas. E as técnicas de análise serão diferentes para cada caso. Quando
os possíveis resultados de uma variável são números de certa escala, dizemos
que essa variável é quantitativa. Quando os possíveis resultados são atributos
ou qualidades, a variável é dita qualitativa (veja a Figura 3.2).
Figura 3.2 Classificação das variáveis e dos dados, em termos do nível de mensu-
ração.
No exemplo dos usuários do site, o sexo, o grau de instrução e o provedor
são variáveis qualitativas, enquanto a idade é quantitativa. Nas características
dos azulejos, a classificação é uma variável qualitativa, mas o empeno e o des­
vio são variáveis quantitativas.
Na descrição das variáveis envolvidas na pesquisa, devemos incluir a esca­
la (ou unidade) em que são mensuradas as variáveis quantitativas, e as catego­
rias (possíveis respostas) das variáveis qualitativas. Sempre que uma caracterís­
tica puder ser adequadamente medida sob forma quantitativa, é melhor
usarmos esse tipo de mensuração, porque as medidas quantitativas são, em ge­
ral, mais informativas do que as qualitativas. Por exemplo, dizer que o empeno
é 8,2 mm é mais informativo do que dizer que o empeno é grande.
Distribuição de frequências
Um dos primeiros passos para analisar um arquivo de dados, especialmen­
te quando o número de observações for grande, é a distribuição de frequências
de cada variável.

ANÁLISE EXPLORATÓRIA DE DADOS 53
A distribuição de frequências consiste na organização dos dados de
acordo com as ocorrências dos diferentes resultados observados.
Por exemplo, ao observar a variável sexo, num conjunto de indivíduos, es­
taremos classificando cada indivíduo ou na categoria masculino, ou na catego­
ria feminino. A contagem de quantos elementos existem em cada categoria for­
ma uma distribuição de frequências dos dados dessa variável, que pode ser
apresentada em uma tabela ou em um gráfico. As frequências podem ser apre­
sentadas de forma absoluta (número de homens e número de mulheres) ou de
forma relativa (a porcentagem de homens e a porcentagem de mulheres) ou,
ainda, de ambas as formas. Normalmente, frequências absolutas são preferidas
quando o número de observações é pequeno. Por outro lado, quando queremos
fazer comparações, como estudar as distribuições de homens e mulheres em
duas turmas, as frequências relativas são mais informativas.
As duas seções seguintes mostram a construção e a apresentação de distri­
buições de frequências para variáveis qualitativas e quantitativas, respectiva­
mente.
3.2 ANÁLISE DE VARIÁVEIS QUALITATIVAS
Nesta seção, aprenderemos a descrever e a explorar dados de variáveis
qualitativas, ou seja, aquelas cujos possíveis resultados são observados na forma
de categorias. Para isso, vamos acompanhar o exemplo a seguir:
Exemplo 3.1 Para adequar os produtos às preferências dos clientes, um proje­
tista de páginas de Internet pretende conhecer o perfil dos indivíduos que aces­
sam um de seus sites. Pensando nisso, ele fez uma pesquisa e levantou algumas
características dos visitantes de seu site, tais como o sexo, a idade, o nível de
instrução e o provedor utilizado. Geralmente esse tipo de pesquisa envolve
centenas ou milhares de respondentes, mas aqui consideraremos apenas uma
amostra de 40 pessoas. Os resultados da pesquisa estão apresentados a seguir:

5 4 ESTATÍSTICA
Indiví­ Indiví­ Indiví­ Indiví­
Provedor Provedor Provedor Provedor
duo duo duo duo
1 C 11 C 21 B 31 A
2 A 12 A 22 A 32 A
3 B 13 B 23 A 33 B
4 B 14 D 24 B 34 C
5 C 15 A 25 A 35 B
6 B 16 B 26 A 36 D
7 D 17 B 27 B 37 B
8 B 18 C 28 D 38 B
9 B 19 D 29 D 39 B
10 A 20 B 30 C 40 C
Tabelas de frequência
Para construir a distribuição de frequências com os dados de uma variável
qualitativa, basta contar a quantidade de resultados observados em cada cate­
goria. A Tabela 3.1 mostra a distribuição de frequências da variável provedor.
Tabela 3.1 Distribuição de frequências do provedor usado pelo visitante do site.
Provedor Frequência Porcentagem
A 10 25,0
B 17 42,5
C 7 17,5
D 6 15,0
Total 40 100,0
A primeira coluna da Tabela 3.1 mostra todas as categorias previamente
estabelecidas da variável provedor. A segunda coluna resulta da contagem de
quantas observações se identificam com cada categoria: são as frequências ob­
servadas. Finalmente, a terceira coluna apresenta uma medida relativa da fre­
quência de cada categoria. Essas porcentagens são obtidas dividindo-se a frequên­
cia de cada categoria pelo número total de observações e, em seguida,
multiplicando-se por 100.
As frequências relativas são particularmente importantes para comparar
distribuições de frequências. Por exemplo, poderíamos ter interesse em compa­
rar o perfil de visitantes de dois sites. Como, em geral, as amostras têm

ANÁLISE EXPLORATÓRIA DE DADOS 55
tamanhos diferentes, a comparação através das frequências absolutas fica pre­
judicada, enquanto as frequências relativas sempre apresentam o mesmo total.
Representações gráficas
As representações gráficas fornecem, em geral, visualização mais sugestiva
do que as tabelas. São formas alternativas de apresentar uma distribuição de
frequências.
A Figura 3.3 representa a distribuição de frequências da Tabela 3.1 através
de um gráfico de colunas, onde cada categoria é representada por uma coluna, e
a frequência (absoluta ou relativa) é colocada no eixo vertical.3
B C
provedor
Figura 3.3 Gráfico de colunas para a apresentação da distribuição de frequências
do provedor usado pelo visitante do site.
Alternativamente, o eixo horizontal poderia representar a escala das fre­
quências e o eixo vertical, as categorias. Estaríamos construindo o chamado grá­
fico de barras.
Um gráfico muito comum para representar distribuições de frequências de
variáveis qualitativas é o chamado gráfico de setores, que é particularmente útil
quando o número de categorias não é grande e as categorias não obedecem a
alguma ordem específica. A Figura 3.4 apresenta a distribuição através de um
gráfico de setores.4
3 Da mesma forma que as tabelas, os gráficos devem conter um título, contendo todas as
informações pertinentes. Eles costumam ser referenciados num texto como figuras. A posição do
título de uma figura deve ser embaixo da figura.
4 O gráfico de setores é construído através de uma relação linear (regra de três) entre as
frequências e comprimentos (em graus) de setores de um círculo.

5 6 ESTATÍSTICA
15%
2 5 %
m A
□ B
18%
□
42%
n
□ D
Figura 3.4 Gráfico de setores para a apresentação da distribuição de frequências
do provedor usado pelo visitante do site.
Diagrama de Pareto
Uma das ferramentas dos programas de qualidade é o chamado diagrama
de Pareto. Sua construção em si é bastante simples, pois corresponde ao gráfico
de colunas ou ao gráfico de barras, mas com as categorias ordenadas decres­
centemente pelas frequências observadas.
A importância desse diagrama é que ele é usado nos processos produtivos,
em postos de avaliação da qualidade, colocando hierarquicamente os proble­
mas encontrados pela falta da qualidade. A Figura 3.5 exemplifica um diagra­
ma de Pareto, que mostra os problemas na implantação do controle integrado
de processos. Nesse exemplo, a priorização dos problemas foi feita pela fre­
quência de ocorrências, resultando em uma distribuição de frequências.
Priorização dos problemas da falta de qualidade num posto de avaliação
Espessura
Rebarbas
Falha no desenho
Largura
Peso
Dureza
Falha na raspagem
Rachadura nos gomos
0 5 10 15 20 25
número de ocorrências do problema
Fonte: CATEN; RIBEIRO; FOGLIATTO. Revista Produto & Produção, v. 4, nü 1, 2000.
Figura 3.5 Ilustração de um diagrama de Pareto - priorização em termos das
frequências observadas.

ANÁLISE EXPLORATÓRIA DE DADOS 5 7
Observando a Figura 3.5, verificamos que as principais características que
levam à falta de qualidade no posto de avaliação são a espessura, as rebarbas e
as falhas no desenho. Um programa de melhoria da qualidade deve enfrentar
prioritariamente essas características.
No diagrama de Pareto, é mais comum priorizar os problemas da qualida­
de em termos financeiros. A Figura 3.6 ilustra essa situação, colocando também
uma curva que indica as perdas acumuladas pela falta de qualidade. O eixo ver­
tical da direita informa o percentual acumulado da perda.
Perdas Perdas
Problem as
(R$) acum uladas
Manchas 15.000 15.000
Rachaduras 10.000 25.000
Furos 3.000 28.000
Riscos 2.000 30.000
Problema
Figura 3.6 Ilustração de um diagrama de Pareto - priorização em termos de per­
das financeiras.
EXERCÍCIO
1. Considere o objetivo de verificar a demanda da qualidade no desenvolvi­
mento de um software. Numa pesquisa de mercado, indagou-se aos clientes
potenciais qual dos seguintes itens era considerado mais importante: (a)
interface de fácil acesso, (b) desempenho do sistema, (c) métodos de análi­
se avançados, (d) método de custeio, (e) manutenção e suporte, (f) perso­
nalização, (g) atualização em tempo real, (h) confiabilidade das informa­
ções, (i) segurança dos dados e (j) uso de novas tecnologias de
informática.5 As frequências de resposta foram (a) 8, (b) 7, (c) 7, (d) 12,
(e) 2, (f) 4, (g) 3, (h) 21, (i) 6 e (j) 0, respectivamente.
a) A variável demanda da qualidade no desenvolvimento de um software,
operacionalizada de acordo com a pergunta feita aos clientes, é quali­
tativa ou quantitativa?
5 Os itens foram extraídos de um artigo de SONDA; RIBEIRO; ECHEVESTE. Revista Pro­
dução, v. 10, nü 1, 2000.

5 8 ESTATÍSTICA
b)
Construa um gráfico (ou diagrama) que mostre a distribuição de fre­
quências das respostas, priorizando os itens segundo a frequência de
respostas. Qual o nome que se dá a esse diagrama?
3.3 ANÁLISE DE VARIÁVEIS QUANTITATIVAS
Conforme foi discutido anteriormente, uma variável é dita quantitativa
quando os possíveis resultados são números em certa escala. Por exemplo,
numa fábrica de cerâmicas, podemos contar o número de defeitos e medir o
grau de empeno (em mm), em cada azulejo. O número de defeitos e o grau de
empeno são variáveis quantitativas. As observações dessas variáveis geram
amostras de dados quantitativos.
O número de defeitos, cujos possíveis resultados podem ser listados (0, 1,
2,...), é um exemplo do que chamamos de variável discreta. Enquanto o grau de
empeno, que teoricamente pode assumir qualquer valor num intervalo de núme­
ros reais (no caso, [0,x)), é um exemplo de variável contínua.
3.3.1 Variáveis discretas
A distribuição de frequências de variáveis discretas pode ser feita de forma
análoga à distribuição de frequências de variáveis qualitativas. Porém, como os
valores da variável formam uma escala numérica, temos, graficamente, um par
de eixos cartesianos. Por convenção, o eixo horizontal representa a variável e o
eixo vertical, as frequências.
A análise difere um pouco daquela feita com variáveis qualitativas. Nor­
malmente, três informações principais são procuradas quando estamos explo­
rando uma variável quantitativa:
a) faixa em que os valores ocorrem com maior frequência (faixa de va­
lores típicos);
b) valores discrepantes, que podem ter sido originados de erros de men-
suração ou digitação, mas também podem corresponder a elementos
que apresentam comportamento muito diferente dos demais;
c) forma da distribuição, a fim de compará-la com modelos probabilís-
ticos, o que nos permite usar técnicas mais avançadas de análise.
A Figura 3.7 ilustra um exemplo de gráfico de distribuição de frequências
de uma variável discreta.

ANÁLISE EXPLORATÓRIA DE DADOS 59
Contagem de defeitos em cada unidade de um produto
Amostra de 50 unidades
161------------------------------------------------------------------------------------
14 -
12
-
10
-
8
-
6
-
4 -
2
-
0I----------------------------------------------------- 1---
0 1 2 3 4 5 6 7
número de defeitos encontrados em cada unidade
Figura 3.7 Distribuição de frequências de um conjunto de observações de uma
variável discreta.
Observando o gráfico, notamos que os valores distribuem-se basicamente
na faixa de 0 a 3 defeitos. Também é possível observar que há um valor discre­
pante: um elemento apresentou 7 defeitos. Além disso, vemos maior concentra­
ção de observações na parte inferior da escala.
3.3.2 Variáveis contínuas
Nesta seção, apresentaremos algumas formas de construção de distribui­
ções de frequências de dados contínuos (provenientes de variáveis aleatórias
contínuas). Esses procedimentos também poderão ser usados para variáveis dis­
cretas, quando o número de distintos valores for grande.
Tabela de frequências
Para construir uma tabela de frequências, dividimos a amplitude total dos
dados (diferença entre o maior e o menor valor) em vários intervalos, denomi­
nados classes. Esses intervalos devem ser mutuamente exclusivos, exaustivos e,
de preferência, ter o mesmo tamanho.6
6 Em alguns casos, não é possível usar intervalos com a mesma amplitude. Por exemplo,
se formos analisar os salários em uma empresa, provavelmente encontraremos os valores distri­
buídos em uma grande amplitude e a maioria deles concentrados na parte inferior da escala.
Assim, pode ser conveniente usarmos intervalos menores para os valores iniciais e intervalos
maiores (mais amplos) para valores finais.

6 0 ESTATÍSTICA
Exemplo 3.2 Os dados, a seguir, representam o tempo (em segundos) para
carga de um aplicativo, num sistema compartilhado (50 observações):
5,2 6,4 5,7 8,3 7,0 5,4 4,8 9,1 5,5 6,2 4,9 5,7 6,3
5,1 8,4 6,2 8,9 7,3 5,4 4,8 5,6 6,8 5,0 6,7 8,2 7,1
4,9 5,0 8,2 9,9 5,4 5,6 5,7 6,2 4,9 5,1 6,0 4,7 14,1
5,3 4,9 5,0 5,7 6,3 6,0 6,8 7,3 6,9 6,5 5,9
amplitude dos dados
4,7 14,1
H------ 1---- 1---------------------1-1------1------1------1------1------I - 1 - I-
4 5 6 7 8 9 10 11 12 13 14 15
11 classes de amplitude unitária
O número de classes a ser usado na tabela de frequências é uma escolha
arbitrária. Quanto maior o conjunto de dados, mais classes podem ser usadas.
Uma tabela com poucas classes apresenta a distribuição de forma bastante resu­
mida, podendo deixar de evidenciar algumas características relevantes. Por ou­
tro lado, se usarmos muitas classes, a tabela pode ficar muito grande, não real­
çando aspectos relevantes da distribuição de frequências.
Em geral, são empregadas de 5 a 20 classes, dependendo da quantidade
de dados e dos objetivos. Dentro dessa faixa, uma sugestão é usar, aproximada­
mente, c = \ n classes, onde n é a quantidade de valores observados. Em nosso
exemplo, por facilidade e para melhor apresentação, optamos por usar classes
com amplitude unitária, totalizando 11 classes.
O passo seguinte é contar quantos valores encontram-se em cada classe
previamente estabelecida. Como os dados são arredondados para um número
finito de decimais, podem ocorrer valores exatamente no limite entre duas clas­
ses. Por convenção, consideraremos sempre o intervalo fechado no limite inte­
rior e aberto no limite superior. A primeira classe, por exemplo, é formada pelo
intervalo [4,0, 5,0), ou 4 |— 5, conforme a simbologia comumente usada em
Estatística.
A tabela de frequências é construída através da contagem da frequência de
observações em cada classe, como mostramos a seguir:

ANÁLISE EXPLORATÓRIA DE DADOS 61
Classes Contagem Frequência
4 |- 5 lllll Mill II 7
5 1—6 lllll lllll lllll III 18
6 \ - 7 lllll lllll III 13
7 | - 8 mi 4
8 1-9 mil 5
9 1— 10 ii 2
10 |— 11 0
11 1— 12 0
12 1— 13 0
13 1— 14 0
14 |— 15 i 1
Na apresentação de uma tabela de frequências, é comum colocar também
os pontos médios das classes, isto é, para cada classe, a média de seus limites.
Por exemplo, na classe 4 |— 5, temos o ponto médio 4,5. O ponto médio repre­
senta o valor típico da classe. A Tabela 3.2 apresenta a distribuição de frequên­
cia dos dados em discussão.
Tabela 3.2 Distribuição de frequências do tempo (em segundos) para carga de
um aplicativo, num sistema compartilhado.
Classes Ponto Número de Porcentagem de Porcentagem
de tempo médio observações n, observações 100/j acumulada 100F,
4 | 5 4,5 7 14 14
5 1— 6 5,5 18 36 50
6 h 7 6,5 13 26 76
7 1— 8 7,5 4 8 84
8 [—9 8,5 5 10 94
9 1— 10 9,5 2 4 98
10 1— 11 10,5 0 0 98
11 1— 12 11,5 0 0 98
12 1— 13 12,5 0 0 98
13 [— 14 13,5 0 0 98
14 [— 15 14,5 1 2 100
Total 50 100
— —

6 2 ESTATÍSTICA
As duas últimas colunas da Tabela 3.2 apresentam as frequências relativas
e as frequências relativas acumuladas, que são obtidas, respectivamente, por:
fi = - 0 = (1, 2, c) (3.1)
n
Fi = í f 0 = 1 ,2 , c) (3.2)
i=l
onde n é o número de observações e c, o número de classes.
Muitas vezes, o maior interesse está nas frequências de observações meno­
res ou iguais a determinados valores. A Figura 3.8 mostra o gráfico das fre­
quências relativas acumuladas. A seta ilustra o percentual aproximado de ob­
servações abaixo de 7,0 segundos.7
tempo de carga (s)
Figura 3.8 Distribuição de frequências acumuladas, em %, de 50 observações do
tempo de carga de certo aplicativo.
As frequências acumuladas podem ser definidas de maneira mais rigorosa
com os dados não agrupados em classes, mas somente ordenados. Chamando
de n(x) o número de observações menores ou iguais a x , a frequência de obser­
vações até o valor x é dada por:
F M = ^ (3.3)
n
7 Nesta figura, foi retirado o valor discrepante (14,1). Sempre temos de buscar as cau­
sas de tais valores discrepantes. Se chegarmos à conclusão de que o valor se deve a algum erro
ou alguma situação especial que não deverá ocorrer novamente, esse valor pode ser retirado e as
análises posteriores podem desconsiderá-lo. Na maior parte dos casos, um valor discrepante deve
ser analisado separadamente dos demais.

ANÁLISE EXPLORATÓRIA DE DADOS 63
Por exemplo, para o conjunto de valores {10, 13, 14, 20}, temos:
0 para x < 10 Fíx)
1
1/4 para 10 <x < 13
3/4
F&) = i 2/4 para 13 <x < 14
2/4
3/4 para 14 <x < 20
1/4
1 para x> 20
10 13 14 20
Histograma
O histograma é a forma mais usual de apresentação de distribuições de fre­
quências de variáveis contínuas. A Figura 3.9 mostra um histograma, construí­
do com base na Tabela 3.2. São retângulos justapostos, feitos sobre as classes
da variável em estudo. A área de cada retângulo é igual (ou proporcional) à fre­
quência observada da correspondente classe.8
20 n------1 I------1------v I------1------1------1------r-----1------1------r
LO
18
.8
ü C3 * 16
14
O
C/3
JÛ 12
o
10
o
"O
8
6
o
B 4
'p
c: 2
3 4 5 6 7 8 9 10 11 12 13 14 15
tempo (em segundos) para carga de um aplicativo
Figura 3.9 Distribuição de frequências de 50 observações do tempo de carga de
um certo aplicativo. Apresentação em histograma de frequências.
Note que o histograma (Figura 3.9) permite a mesma análise dos dados
que a tabela de frequências (Tabela 3.2), porém de forma mais clara.
Diagrama de pontos
Uma forma simples de observar como poucas observações se distribuem é
através do diagrama de pontos, onde representamos cada valor como um ponto
8 O histograma também poderia ser feito usando percentagens no eixo vertical, mas a
sua forma não mudaria. A rigor, o eixo vertical de um histograma deve representar as densidades
de frequências, isto é, as frequências relativas, f., divididas pelos correspondentes intervalos das
classes, fazendo com que a soma das áreas dos retângulos se iguale a um. O uso de densidades de
frequências é fundamental quando as classes não têm a mesma amplitude.

6 4 ESTATÍSTICA
na reta de números reais. Por exemplo, considere um estudo experimental so­
bre um processo químico, do qual queremos avaliar o rendimento em dois ní­
veis da temperatura de reação: 60 e 80°C. A Figura 3.10 apresenta os dados e
o diagrama de pontos relativos aos oito ensaios realizados com cada temperatura.
Temperatura Rendimento (%)
60cC 31,0 33,6 32,8 32,2 Temp. 80°C
Temp. 60°C
_____________ 31,9 36,2 34,3 34,0
1----1 i----1----i 1 __ií— 1— i1 . i1----1----iL 1 1
30 32 34 36 38 40 42 44
80CC 37,0 34,4 39,8 38,5
Rendimento
33,9 43,2 35,5 39,0
Figura 3.10 Ilustração de um diagrama de pontos.
Podemos observar na Figura 3.10 que a temperatura de 80°C produziu, em
geral, rendimentos maiores. Mas os pontos apresentaram-se mais dispersos, o
que nos leva a suspeitar que temperaturas mais altas podem provocar maior va­
riabilidade no processo químico.
A estratégia de análise por meio do diagrama de pontos torna-se inadequa­
da quando o número de observações é grande, ao contrário da tabela de fre­
quências e do histograma, que podem ser usados para grandes conjuntos de ob­
servações quantitativas.
Diagrama ramo-e-folhas
O diagrama ramo-e-folhas consiste em apresentar os dados separando os
primeiros dígitos, os quais formarão os ramos, e os demais dígitos, que forma­
rão as folhas. Por exemplo, para os números 10, 15 e 23, as dezenas 1 e 2 fica­
riam do lado esquerdo de uma linha vertical (os ramos 1 e 2) e as unidades 0, 5
e 3, do lado direito (as folhas), como segue:
10, 15, 23 --------- ► 1 0 5
2 3
Para construir um ramo-e-folhas com os dados do Exemplo 3.2, podemos
separar as unidades para formar os ramos e as decimais para formar as folhas,
como ilustrado para os cinco primeiros valores.
5,2 6,4 5,7 8,3 7,0 ► 5 2 7
6 4
7 0 unidade = 0,1
8 3

ANÁLISE EXPLORATÓRIA DE DADOS 65
Repetindo o processo para as 50 observações, chegamos ao diagrama da
Figura 3.11, onde as folhas (decimais dos números) foram ordenadas para faci­
litar a leitura.
Frequência
4 7 8 8 9 9 9 9 7
5 0 0 0 1 1 2 3 4 4 4 5 6 6 7 7 7 7 9 18
6 0 0 2 2 2 3 3 4 5 7 8 8 9 13
7 0 13 3 4
8 2 2 3 4 9 5
9 1 9 2
10 0
11 0
12 0
13 0
14 1 unidade = 0,1 1
Figura 3.11 Diagrama ramo-e-folhas para os dados do Exemplo 3.2.
O diagrama ramo-e-folhas da Figura 3.11 permite observar que, na maioria
das vezes, o tempo de carga fica entre 4 e 7 segundos. O diagrama evidencia
um caso atípico (14,1 segundos). Note que em um ramo-e-folhas observamos as
mesmas características que num histograma (reveja a Figura 3.9).
Muitas vezes, o número de folhas em cada ramo fica muito grande e, em
consequência, o diagrama fica concentrado em poucos ramos. É possível, nesses
casos, dividir cada ramo (composto de 10 folhas) em 2 ou 5 partes (novos ra­
mos compostos de 5 ou 2 folhas, respectivamente). O esquema a seguir ilustra
a divisão do ramo “5” em 2 novos ramos, sendo o primeiro formado pelas fo­
lhas de 0 a 4 e o segundo pelas folhas de 5 a 9. É importante que o número de
folhas possíveis em cada ramo seja o mesmo em todo o diagrama.
0 0 0 1 1 2 3 4 4 4 5 6 6 7 7 7 7 9 -------► 5 0 0 0 1 1 2 3 4 4 4
5 5 6 6 7 7 7 7 9
3.3.3 Características de uma distribuição
Na análise exploratória de dados quantitativos, uma das informações usual­
mente procuradas é a posição central e a forma da distribuição de frequências.
Por exemplo, a Figura 3.12 apresenta um histograma construído com 2.000 ob-

6 6 ESTATÍSTICA
servações do tempo de carga de um aplicativo e uma curva contínua, que repre­
senta a forma aproximada do que se observou.
tempo de carga (s)
Figura 3.12 Histograma de 2.000 observações do tempo de carga de um certo
aplicativo e uma curva simbolizando a forma da distribuição.
Ao confrontarmos a distribuição observada com vários modelos teóricos
existentes, temos uma ideia de qual modelo seria o mais adequado para expli­
car o comportamento da variável estudada. Na investigação sobre a forma da
distribuição, várias características devem ser observadas. As principais são:
a) a posição central, que informa onde se localiza o centro da distri­
buição;
b) a dispersão, que se refere à variabilidade dos dados;
c) a assimetria, que representa a concentração dos valores em um dos
extremos da distribuição;
d) a curtose, que é o grau de achatamento da distribuição.
A Figura 3.13 ilustra diferentes formas de distribuição de frequências, con­
siderando as características comentadas anteriormente.

ANÁLISE EXPLORATÓRIA DE DADOS 67
(a) Distribuições diferentes em (b) Distribuições diferentes
termos da posição central quanto à dispersão
(c) Distribuições diferentes (d) Distribuições diferentes
quanto à assimetria quanto à curtose
Figura 3.13 Diferentes formas de distribuição de frequências.
Na próxima seção, discutiremos algumas medidas que servem para quanti­
ficar a posição central e a dispersão.
EXERCÍCIO
2. Os dados abaixo representam 50 leituras de temperatura (°C) de um pasteu-
rizador de leite
74.8 74,0 74,7 74,4 75,9 76.8 74,3 74,9 77,0 75,1
73.8 74,4 74,8 76,8 73,6 72.9 72,9 74,6 75,0 75,1
75.3 73,4 74,7 73,4 74,2 74.9 74,5 77,1 74,6 74,8
76.4 73,2 76,5 75,6 73,5 76.2 74,7 76,0 75,8 77,3
76,3 74,1 75,0 76,0 74,7 75.2 77,5 74,7 73,3 74,3
a) construa uma tabela de frequências;
b) apresente a distribuição em um histograma;
c) faça um gráfico da distribuição acumulada. Indique no gráfico a
porcentagem aproximada de observações abaixo de 75°C;
d) construa um diagrama ramo-e-folhas.

6 8 ESTATÍSTICA
3.4 MEDIDAS DESCRITIVAS
Quando analisamos uma variável qualitativa, basicamente construímos sua
distribuição de frequências. No entanto, ao explorarmos variáveis quantitativas,
temos condições de empregar algumas medidas descritivas, que sintetizam as
características da distribuição.9 Aqui, vamos desenvolver medidas de posição
central e dispersão.
Muitas vezes um conjunto de observações quantitativas pode ser bem re­
presentado por alguma medida descritiva. Por exemplo, se na primeira avalia­
ção de uma disciplina a média das notas dos alunos foi igual a 8,0 e, na segun­
da avaliação, foi igual a 9,0, podemos concluir que, em geral, os alunos tiveram
melhor aproveitamento na segunda avaliação, mesmo sem nos referirmos às
notas de cada aluno individualmente.
Exemplo 3.3 O rendimento de um processo químico é influenciado pelo tem­
po e pela temperatura de reação. Um experimento é realizado para diferentes
níveis do tempo de reação (20, 25 e 30 minutos) e da temperatura de reação
(60, 70 e 80°C). Como os ensaios são também afetados por fatores não contro­
láveis, as observações agregam um erro experimental. Devido à presença do erro
experimental, foram realizados seis ensaios em cada combinação de níveis do
tempo e da temperatura. Os resultados do experimento (rendimentos em %)
são apresentados a seguir.
Tempo (minutos)
Temperatura
(°C)
20 25 30
60 29,7 28,7 30,2 31,0 30,6 32,8 32.9 32,7 34,8
31,3 31,2 31,7 31,9 31,2 31,2 34.9 33,8 34,9
70 36,6 35,7 35,3 35,7 40,4 41,7 34.8 36,8 37,4
35,1 30,2 37,2 36,9 34,5 40,0 38.9 38,7 42,5
80 40.2 33,6 33,4 37,0 34,4 29,8 36,0 31,3 36,6
35.2 38,1 33,0 33,9 43,2 35,5 32,5 39,2 35,9
Observando os dados brutos, é difícil avaliar qual é a influência do tempo
e da temperatura de reação sobre o rendimento. Porém, calculando a média
aritmética em cada subgrupo da amostra de observações, as relações aparecem
de forma mais nítida. A Figura 3.14 apresenta essas médias em forma tabular e
gráfica.
9 Como vimos na seção anterior, as quatro principais características de uma distribuição
são a tendência central, a dispersão, a assimetria e a curtose.

ANÁLISE EXPLORATÓRIA DE DADOS 69
Rendimento médio cm função da
Tempo (minutos)
Temperatura temperatura c tempo de reação
(°C)
20 25 30
60 30,5 31,4 34,0
70 35,0 38,2 38,2 • 60 graus
- - 70 graus
— 90 fcraus
80 35,6 35,6 35,3 25
tempo (min)
Figura 3.14 Médias aritméticas do rendimento, para diferentes níveis de tempe­
ratura e tempo de reação, num processo químico.
Pela Figura 3.14, é possível observar que, se usarmos a temperatura no ní­
vel intermediário (70°C) e tempo de reação na faixa de 25 a 30 minutos, então
obteremos, em média, melhor rendimento.
3.4.1 Medidas clássicas
A média e o desvio padrão já foram estudadas no Capítulo 1. Aqui as apre­
sentaremos com maiores detalhes.
A média aritmética
O conceito de média aritmética, ou simplesmente média, é bastante fami­
liar. Seja fo, x2,..., xn) uma amostra de n observações de certa variável aleató­
ria X. A média aritmética dessas observações é definida por
(3.4)
No Exemplo 3.3, mostramos como a média aritmética resume os dados de
forma a torná-los mais informativos. Já o Exemplo 3.4 ilustra alguns problemas
ao tentarmos resumir vários valores por uma média.
Exemplo 3.4 Considere as notas finais, relativas aos alunos de três turmas,
representadas em diagramas de pontos (Figura 3.15). As setas apontam para as
posições das médias aritméticas.
Turma Notas dos alunos Média da turma
A 4 5 5 6 6 7 7 8 6,00
B 1 2 4 6 6 9 10 10 6,00
C 0 6 7 7 7 7,5 7,5 6,00

7 0 ESTATÍSTICA
notas
Figura 3.15 Representação das distribuições das notas de três turmas e corres­
pondentes posições das médias aritméticas.
Observando a Figura 3.15, percebemos que, em cada diagrama de pontos,
a média aritmética apresenta-se, de alguma forma, na posição central dos valo­
res observados. Mais precisamente, a média aritmética indica o centro de um
conjunto de valores, considerando o conceito físico de centro de gravidade. Se
imaginarmos os pontos como pesos sobre uma tábua, a média é a posição em
que um suporte equilibraria essa tábua.
Na Figura 3.15, também observamos que os três conjuntos de valores, ape­
sar de estarem distribuídos sob diferentes formas, apontam para uma mesma
média aritmética. Isso mostra que a média aritmética resume o conjunto de da­
dos, em termos de posição central, ou de valor típico, mas não fornece qualquer
informação sobre outros aspectos da distribuição. Comparando, por exemplo,
as notas da turma A com as notas da turma B, verificamos que o segundo con­
junto de notas é bem mais disperso, indicando que a turma B é mais heterogê­
nea em termos de notas obtidas. No conjunto de notas da turma C, observamos
um ponto discrepante dos demais: uma nota extremamente baixa, fazendo com
que a média fique abaixo da maioria das notas da turma.10
Medidas de dispersão
Para melhorar o resumo dos dados, podemos apresentar, ao lado da média
aritmética, uma medida da dispersão desses dados. Uma forma simples de me­
dir a dispersão é através da amplitude, isto é, a diferença entre o maior e o me­
nor valor. Matematicamente:
a = máx.(xly x2i..., x„) - mín.(x1} x2,..., xn) (3.5)
10 Podemos observar no diagrama de pontos referente à turma C que a presença de um
valor discrepante arrasta a média para seu lado. Assim, a média deixa de representar propria­
mente um valor típico do conjunto de dados. Um tratamento mais adequado para dados que con­
tenham valores discrepantes será visto na seção 3.4.2.

ANÁLISE EXPLORATÓRIA DE DADOS 71
Como (3.5) é calculada usando apenas os dois valores mais extremos, ela
pode levar a conclusões errôneas quando existirem valores discrepantes. Medi­
das mais apropriadas são a variância e o desvio padrão.
Tanto a variância quanto o desvio padrão são medidas que fornecem infor­
mações complementares à informação contida na média aritmética. Essas medi­
das avaliam a dispersão do conjunto de valores em análise. Para calcularmos a
variância ou o desvio padrão, devemos considerar os desvios de cada valor em
relação à média aritmética. Depois, construímos uma espécie de média desses
desvios. Ilustramos, a seguir, as etapas de cálculo, usando o conjunto de notas
da turma A (Exemplo 3.4).
Descrição Notação Resultados numéricos
Valores (notas dos alunos) 4 5 5 6 6 7 7 8
Média X 6
Desvios em relação à média Xi - X -2 -1 -1 0 0 1 1 2
Desvios quadráticos (X, - X)2 4 1 1 0 0 1 1 4
Para evitar o problema dos desvios negativos, vamos trabalhar com os des­
vios quadráticos, (xt - x)2 (f = 1, 2,..., n). A variância é definida como a média
aritmética dos desvios quadráticos. Se estivermos trabalhando com uma amos­
tra, devemos calcular essa média usando como denominador (n - 1) no lugar
de n. Assim, definimos a variância de um conjunto de valores pela expressão
(3.6)
Em relação ao conjunto de notas da Turma A, a variância é
2 4 + 1 + 1 + 0 + 0 + 1 + 1 + 4 1 71
s = ------------------------------------ = 1,71
8 - 1
Como a variância de um conjunto de dados é calculada em função dos
desvios quadráticos, sua unidade de medida equivale à unidade de medida dos
dados ao quadrado. Nesse contexto, é mais comum trabalhar com a raiz qua­
drada positiva da variância. Essa medida é conhecida como desvio padrão, o qual
é expresso na mesma unidade de medida dos dados em análise. Então, o desvio
padrão de um conjunto de valores pode ser calculado por:
(3.7)

7 2 ESTATÍSTICA
Em termos do conjunto de notas da turma A (Exemplo 3.4), temos o se­
guinte desvio padrão: s = 1,71 = 1,31.
Ao compararmos os desvios padrões de vários conjuntos de dados, pode­
mos avaliar quais se distribuem de forma mais (ou menos) dispersa. O desvio
padrão será sempre não negativo e será tão maior quanto mais dispersos forem
os valores observados. A Tabela 3.3 mostra o desvio padrão das notas de cada
uma das três turmas de alunos, referente aos dados do Exemplo 3.4.
Tabela 3.3 Medidas descritivas das notas finais dos alunos de três turmas.
Número Desvio
Turma Média
de alunos padrão
A 8 6,00 1,31
B 8 6,00 3,51
C 7 6,00 2,69
Analisando a Tabela 3.3, verificamos, através das médias, que os alunos
das três turmas tenderam a ter as notas em torno de seis, mas, pelos desvios pa­
drões, concluímos que os alunos da turma A obtiveram notas relativamente
próximas umas das outras, quando comparados aos alunos das outras turmas.11
Por outro lado, as notas dos alunos da turma B foram as que se apresentaram
mais heterogêneas.
Retomando o Exemplo 3.3, onde buscávamos verificar o rendimento de
um processo químico para diferentes níveis do tempo de reação (20, 25 e 30
minutos) e da temperatura de reação (60, 70 e 80°C), calculamos a média e o
desvio padrão para cada subconjunto de seis observações realizadas nas dife­
rentes combinações de níveis do tempo e temperatura de reação. Os resultados
são colocados em gráficos, conforme mostramos na Figura 3.16.
Analisando as médias, observamos que, se usarmos a temperatura no nível
intermediário (70°C) e o tempo de reação na faixa de 25 a 30 minutos, então
teremos, em média, maior rendimento. Porém, analisando os desvios padrões, é
possível verificar que, para temperaturas maiores, temos um aumento na varia­
bilidade. Uma das preocupações da engenharia é reduzir a variabilidade de pro­
cessos. Assim, devemos evitar temperaturas superiores a 70°C, pois, além de re­
duzir o rendimento médio, aumenta a variabilidade.
11 Observe, pela Figura 3.15, que as notas da turma C estão mais concentradas do que as
da turma A. Porém, o valor discrepante, além de deslocar a média, aumenta o desvio padrão. Se
o valor discrepante fosse desconsiderado, o desvio padrão das notas da turma C seria o menor de
todos - a média seria 7 e o desvio padrão 0,55.

ANÁLISE EXPLORATÓRIA DE DADOS 73
Rendimento médio em função da Desvio padrão do rendimento em função
temperatura e tempo de reação da temperatura e tempo de reação
t
O
c<V
c
ä
60°C
70°C
20 25 80°C 25
tempo (min) tempo (min)
Figura 3.16 Médias aritméticas e desvios padrões do rendimento (%), para dife­
rentes níveis de temperatura e tempo de reação (Exemplo 3.3).
O cálculo da média e do desvio padrão
Ao calcularmos o desvio padrão nos casos em que a média, x acusar um
valor fracionário, os desvios (x, - x) acumularão erros de arredondamento, que
poderão comprometer o resultado final. Para evitar esse inconveniente, pode­
mos usar a seguinte fórmula alternativa para o cálculo do desvio padrão, que é
matematicamente equivalente à expressão (3.7) :12
(3.8)
Ilustraremos o uso desta nova formulação com as notas obtidas pelos alu­
nos da Turma A (Exemplo 3.4):
Valores xt: 4 5 5 6 6 7 7 8 ^ x , = 48 e x = 6
í=i
Valores ao 2; 16 25 25 36 36 4Ç 4g 64 . y x 2 = 300
quadrado 1 f-f 1
Então:
s= I 300 - 8.(6) _ ; 300 - 288 = 1 2 = 13 1
12 A igualdade no numerador das duas fórmulas de s2 é demonstrada a seguir:
£ (* , - 3c)2 = £(JC? - 2x.x + x2) = £ x ,2 - + £ x 2 =
r=l i= 1 t=l i= 1 i=l
= J x f - 2xnx + nx2 = J x f - 2nx2 + nx2 = J x f - nx2
Í=1 Í=1 1=1

7 4 ESTATÍSTICA
Como era de se esperar, chegamos ao mesmo resultado encontrado ante­
riormente pela Expressão (3.7).
Outro aspecto relativo ao cálculo da média e do desvio padrão refere-se à
soma de valores repetidos. Por exemplo, ao calcularmos a média das notas da
Turma A, fizemos a seguinte soma:
= 4 + 5 + 5 + 6 + 6 + 7 + 7 4 - 8
i=i
que é equivalente a 4(1) + 5(2) + 6(2) + 7(2) + 8(1) =
j=i
onde: x t (j = 1, 2, ..., k) representam os k valores distintos de X;
rij (j = 1, 2, ..., k) são os números de ocorrências desses valores; e
n = nl + n2 + ... + nk é o número total de valores.
Analogamente, podemos calcular a soma quadrática dos valores de X por
£ xfrij = 42 + 52(2) + 62(2) + 72(2) + 82 = 300
;=i
Com essa nova notação, as formulações de média e desvio padrão são
apresentadas a seguir:
= x1n1 + x 22n 2+...+xkn k = 1 ^
_
(3.9)
n j=l
”
(3.10)
A Tabela 3.4 mostra a sequência de cálculos para a obtenção da média e
do desvio padrão, usando as notas finais dos alunos da Turma A.
Tabela 3.4 Cálculos auxiliares para a obtenção de x e s.
Nota Frequência
Xj Tlj Xj2 Tlj
*7 nj
4 1 4 16
5 2 10 50
6 2 12 72
7 2 14 98
8 1 8 64
Total 8 48 300

ANÁLISE EXPLORATÓRIA DE DADOS 75
a • - 48 , ; 300 - 8(6)2 1 01
Assim: x = — =6 e s = . ----------^ - = 1 ,3 1
8
Nas situações em que existem muitas repetições de valores, as expressões
(3.9) e (3.10) não só facilitam o cálculo de x e s, como também reduzem a pos­
sibilidade de erros computacionais.
O coeficiente de variação
Embora o desvio padrão seja a medida de dispersão mais usada, ela mede
a dispersão em termos absolutos. O coeficiente de variação, definido por
(3.11)
mede a variação em termos relativos. Veja, por exemplo, os três conjuntos de
valores apresentados na Tabela 3.5 e seus respectivos desvios padrões.
Tabela 3.5 Média, desvio padrão e coeficiente de variação de três conjuntos de
valores.
Conjunto de valores s cv
X
1) 1 2 3 2 1 0,5
2) 101 102 103 102 1 0,01
3) 100 200 300 200 100 0,5
Os conjuntos (1) e (2) têm o mesmo desvio padrão, pois os intervalos en­
tre os valores são iguais. Por outro lado, os intervalos entre os valores do con­
junto (3) são 100 vezes maiores que nos outros conjuntos. Portanto, o desvio
padrão no conjunto (3) é 100 vezes maior que os dos outros. Note, porém, que
os níveis de variabilidade nos conjuntos (1) e (3) são proporcionalmente iguais;
logo, eles têm o mesmo coeficiente de variação.
Ao dividirmos o desvio padrão pela média, a unidade de medida é cancela­
da. Logo, o coeficiente de variação é adimensional (não tem unidade de medi­
da), tomando-se útil quando queremos comparar a variabilidade de observa­
ções com diferentes unidades de medidas. Cabe observar que o cv não faz
sentido em variáveis que assumem valores com ambos os sinais (positivo e ne­
gativo).

7 6 ESTATÍSTICA
3.4.2 Medidas baseadas na ordenação dos dados
A média e o desvio padrão são as medidas mais usadas para avaliar a posi­
ção central e a dispersão de um conjunto de valores. Contudo, essas medidas
são fortemente influenciadas por valores discrepantes. Por exemplo, nas notas
da turma C (Exemplo 3.4), o valor discrepante 0 (zero) puxa a média para bai­
xo, como ilustra a Figura 3.17. Apesar de a média aritmética ser 6, o diagrama
de pontos sugere que o valor 7 é um valor mais típico para representar as notas
da turma, pois, além de ser o valor mais frequente, ele é o valor do meio, dei­
xando metade das notas abaixo dele, e a outra metade acima dele.
valor
S discrepante
9-------1-------- 1--------1--------1--------h
0 1 2 3 4 S 6 7 8
notas f
média
Figura 3.17 Influência de um valor discrepante no cálculo da média aritmética.
Nesta seção, apresentaremos algumas medidas que são menos afetadas
por valores discrepantes e, em consequência, são mais recomendadas para a
análise de dados que possam conter valores discrepantes.
A mediana
A mediana avalia o centro de um conjunto de valores, sob o critério de ser
o valor que divide a distribuição ao meio, deixando os 50% menores valores de
um lado e os 50% maiores valores do outro lado. Por exemplo, o conjunto de
valores {2, 3, 4, 5, 8} tem como mediana o valor 4, pois a quantidade de valo­
res menores que 4 é igual a 2, a mesma quantidade de valores superiores a 4.
De forma mais precisa, podemos definir a mediana como o valor que ocu­
pa a posição (n + l ) / 2, considerando os dados ordenados crescente ou decres­
centemente. Se (n + l)/2 for fracionário, a mediana é definida como a média
dos dois valores de posições mais próximas a (n + l)/2 . Vamos representar a
mediana por md.
Exemplos:
a) Conjunto de notas da Turma C: {0; 6; 7; 7; 7; 7,5 7,5}
=> posição (n + l)/2 = 4 => md = 7

ANÁLISE EXPLORATÓRIA DE DADOS 7 7
ordenando
b) {5, 3, 2, 8, 4 } -------- > {2, 3, 4, 5, 8}, posição (n + l)/2 = 3 =>
=> md = 4
c) {3, 5, 6, 7, 10, 11} => posição (n + l)/2 = 3,5 => md = (6 + 7)/2 =
= 6,5
Quando os dados estão apresentados num ramo-e-folhas, é muito fácil obter
a mediana, pois, neste caso, os valores já estão ordenados. O esquema seguinte
ilustra a obtenção da mediana no ramo-e-folhas dos dados do Exemplo 3.2.
Frequência
Tempo de carga (s)
acumulada
4 7 8 8 9 9 9 9 7
5 0 0 0 1 1 2 3 4 4 4 5 6 6 7 7 7 7 9 25 n = 50
6 0 0 2 2 2 3 3 4 5 7 8 8 9 38 n + 1
. ~
posição
7 0 1 3 3 42
2
8 2 2 3 4 9 47
5,9+ 6,0
9 19 49 => md = = 5,95
2
10 0
11 0
12 0
13 0
14 1 unidade = 0,1 50
Comparação entre média e mediana
A Figura 3.18 mostra os valores da média e da mediana num histograma.
Note que o valor discrepante da classe 141— 15 puxa mais a média do que a
mediana.
50%
3 4 5 / 6 V 8 9 10 11 12 13 14 15
md = 5,95 x = 6,37
Figura 3.18 Posição da média e da mediana no histograma do tempo de carga de
um aplicativo.

7 8 ESTATÍSTICA
Em distribuições simétricas, a média e a mediana são iguais. Em distribui­
ções assimétricas, a média tende a deslocar-se para o lado da cauda mais longa
(ver Figura 3.19).
distribuição (b) distribuição
(a )
simétrica assimétrica
t
média = mediana
Figura 3.19 Posições da média e mediana, segundo a forma (simétrica ou assi­
métrica) da distribuição.
Em geral, dado um conjunto de valores, a média é a medida de posição
central mais adequada, quando se supõe que esses valores têm uma distribui­
ção razoavelmente simétrica, enquanto a mediana surge como uma alternativa
para representar a posição central em distribuições muito assimétricas.13 Muitas
vezes, calculamos ambas as medidas para avaliar a posição central sob dois en­
foques diferentes, além de obtermos uma primeira avaliação sobre a assimetria
da distribuição.
Quartis e extremos
Na maioria dos casos práticos, o pesquisador tem interesse em conhecer
outros aspectos relativos ao conjunto de valores, além de um valor central, ou
valor típico. Algumas informações relevantes podem ser obtidas através do con­
junto de medidas: mediana, extremos e quartis, como veremos a seguir.
Chamamos de extremo inferior ao menor valor do conjunto de valores, isto
é, mín.Çxi, x2, xn), e de extremo superior ao maior valor, isto é máx.Çxi, x2,
xn). Por exemplo, dado o conjunto de valores {5, 3, 6, 11, 7}, temos min. = 3 e
máx. = 1 1 .
13 Mesmo para variáveis que supostamente tenham distribuições razoavelmente simétri­
cas, a média e a mediana podem não se igualar, já que, em geral, estamos observando apenas al­
guns valores (amostra) dessas variáveis. Para variáveis com distribuições razoavelmente simétri­
cas, a média é a medida de posição central mais adequada, porque usa o máximo da informação
contida nos dados. A média é calculada usando propriamente a magnitude dos valores, enquanto
a mediana utiliza somente a ordenação dos valores.

ANÁLISE EXPLORATÓRIA DE DADOS 79
Chamamos de primeiro quartil ou quartil inferior (qf) o valor que delimita
os 25% menores valores; de terceiro quartil ou quartil superior (qs) o valor que
separa os 25% maiores valores. O segundo quartil, ou quartil do meio, é a pró­
pria mediana, que separa os 50% menores dos 50% maiores valores (ver a Fi­
gura 3.20).
Figura 3.20 Os quartis dividem a distribuição em quatro partes iguais.
Com os dados ordenados crescentemente, temos:
n + 1 n + 1 3 (n + 1)
posição de q,: posição de md: posição de qs:
Quando os resultados das operações acima são fracionários, fazemos uma
interpolação linear com os valores de posições vizinhas ao resultado da fração.
Exemplos:
a) Observações: 15, 18, 5, 7, 9, 11, 3, 5, 6, 8, 12. Ordenando:
3 5 5 6 7 8 9 11 12 15 18
n + 1
n = 11 ------► posição de q;: ------ = 3 ------► q, = 5
71 4" 1
posição de md: ------ = 6 ------► md = 8
. ~ , 3(n +1) n
posição de qs: ---------- = 9 ------- ► qs = 12

8 0 ESTATÍSTICA
b)
Tempo de carga (s)
4 7 8 8 9 n = 50
5 0 00 1
n + 1
6 0 0 2 2 = 25,5 => md = 5,95
2
7 0 1 3 3
8 2 23 4
n + 1
= 12,75 qt = 5,175
9 1 9
4^
10
11 3 (n + 1)
= 38,25 => qs = 6,925
12
13 unidade = 0,1
14 1
Com a mediana, quartis e extremos, podemos ter informações sobre a po­
sição central, dispersão e assimetria da distribuição de frequências, como ilustra
a Figura 3.21.
máx.
— ►
Figura 3.21 Posição dos quartis e extremos em distribuições diferentes quanto à
dispersão e assimetria.
O desvio interquartílico (dq = qs - qt) é muitas vezes usado como uma me­
dida de dispersão. Veja na Figura 3.21 que, quanto mais dispersa a distribuição,

ANÁLISE EXPLORATÓRIA DE DADOS 81
maior será o valor de dq. Em distribuições mais dispersas, os valores dos quartis
(e dos extremos) ficam mais distantes. Em distribuições simétricas, a distância
entre o quartil inferior e a mediana é igual à distância entre a mediana e o
quartil superior, enquanto em distribuições assimétricas essas distâncias são di­
ferentes.
Diagrama em caixas
Uma forma de apresentar graficamente os conceitos discutidos é através
do diagrama em caixas. Trata-se de um retângulo que representa o desvio inter-
quartílico. Esse retângulo representa, portanto, a faixa dos 50% dos valores
mais típicos da distribuição. O retângulo é dividido no valor correspondente à
mediana; assim, ele indica o quartil inferior, a mediana e o quartil superior.
Entre os quartis e os extremos, são traçadas linhas. Caso existam valores discre­
pantes (além de 1,5 dq), a linha é traçada até o último valor não discrepante, e
os valores discrepantes são indicados por pontos. Eventuais pontos muito dis­
tantes (além de 3 dq) normalmente são representados por símbolos diferentes
para serem bem destacados (veja a Figura 3.22).
(a) (b)
max.
14
Qs + l,5dç
13
C/í 12
a h
Qs
S 10
i x 0 ) » 9
o 8
d.
B 7
QJ
min.
6
5 T
4
Figura 3.22 (a) Construção de um diagrama em caixas, (b) Diagrama em caixas
das 50 observações do tempo de carga de um aplicativo (Exemplo 3.2).
A Figura 3.23 mostra a forma do diagrama em caixas para uma distribui­
ção simétrica e para uma distribuição assimétrica. Note as diferenças e imagine
como ficaria um diagrama em caixas se tivéssemos uma distribuição mais dis­
persa.

8 2 ESTATÍSTICA
Figura 3.23 Diagrama em caixas e forma da distribuição.
Exemplo 3.5 Para avaliação da qualidade, foram pesados 228 sacos de leite
tipo C, em cada boca de ensacamento, durante um mês.14 Os diagramas em cai­
xas das amostras são apresentados na Figura 3.24.
boca
Figura 3.24 Representação de distribuições do peso de litros de leite que saem de
um laticínio, por boca de ensacamento.
Através da Figura 3.24, observamos pouca diferença entre as bocas de en­
sacamento. Aparentemente, as bocas B e D apresentam nível de peso e variabi­
lidade levemente menores do que as bocas A e C. A busca por melhoria da
qualidade passa pela redução de variabilidade do processo.
14 A amostra de observações foi extraída da dissertação de mestrado de Luciana S. C. V.
da Silva (Programa de Pós-Graduação em Engenharia de Produção/UFSC, 2001).

ANÁLISE EXPLORATÓRIA DE DADOS 83
3.5 OBSERVAÇÕES AO LONGO DO TEMPO
No acompanhamento da qualidade de um processo, coletamos sistematica­
mente pequenas amostras do produto que está sendo manufaturado, em diver­
sas fases da produção. Retomando o Exemplo 3.5, suponha que em todos os
dias sejam coletadas amostras de dez sacos de leite, os quais têm seu peso me­
dido. Embora diagramas em caixas ou histogramas possam fornecer uma ideia
da variabilidade do processo, eles não permitem avaliar certas tendências do
processo.
Um procedimento mais adequado é calcular medidas descritivas das amos­
tras e apresentá-las ao longo do tempo. No presente exemplo, calculamos a mé­
dia ® e o desvio padrão (s) de amostras de 10 sacos de leite, durante 23 dias,
conforme ilustrado a seguir:
Amostra 1 Amostra 2 Amostra 23
1.034 1.035 1.031
1.029 1.028 1.031
1.032 1.031 1.029
1.030 1.035 1.036
1.032,60 1.033,34 1.030,99
1.032 1.030 1.028 *23 —
> > >
1.033 Si = 2,39 1.035 s2 = 3,79 1.034 2,34
523 =
1.037 1.029 1.031
1.031 1.035 1.030
1.033 1.040 1.030
1.035 1.036 1.031
A Figura 3.25 apresenta as medidas descritivas xt e s, (i = 1, 2, ..., 23) ao
longo do tempo, num gráfico de linhas.
A linha horizontal cheia representa a média aritmética da medida descriti­
va em análise (x no primeiro gráfico e s no segundo) das 23 amostras. Os pon­
tos ligados por linhas tracejadas são os resultados das medidas descritivas. As
linhas horizontais tracejadas podem ser interpretadas como limites das varia­
ções estatisticamente toleráveis. Esses limites baseiam-se na teoria que veremos
no Capítulo 7.
Observando os gráficos da Figura 3.25, verificamos que, apesar de as mé­
dias das amostras estarem sempre dentro dos limites de controle, a amostra 4
apresentou variabilidade acima do tolerado. Além disso, entre as amostras 1 a
4, as médias amostrais apresentaram tendência crescente. Provavelmente, após
termos observado a amostra 4, ocorreu uma intervenção no processo produtivo
para corrigir a tendência aparentemente crescente do peso médio de leite e da
alta variabilidade. A amostra 7 também merece algum cuidado. Embora esteja
dentro dos limites toleráveis, a média amostrai apresenta-se bastante baixa,
próxima do limite inferior.

8 4 ESTATÍSTICA
Gráfico das médias amostrais
amostra
1 5 10 15 20
amostra
Figura 3.25 Gráficos de controle do peso de sacos de leite que saem de um laticí­
nio, numa boca de ensacamento.
3.6 ANÁLISE EXPLORATÓRIA COM APOIO DO COMPUTADOR
Em geral, nos pacotes computacionais de estatística, ou mesmo em plani­
lhas eletrônicas, é bastante simples obter um conjunto de medidas descritivas
dos valores de uma variável quantitativa. A seguir, apresentamos medidas des­
critivas da renda, em salários mínimos, de uma amostra de famílias de um bair­
ro de Florianópolis. As medidas descritivas foram obtidas através da planilha
eletrônica Excel. Ao lado, é apresentado o histograma de frequências para facili­
tar a interpretação.15
15 No Microsoft Excel, várias técnicas estatísticas podem ser feitas acionando no menu
principal “ferramentas”, “suplementos” e solicitando que se instalem as “ferramentas de análise”.
Para obter as medidas descritivas, acionar “ferramentas”, “análise de dados” e “estatísticas descriti­
vas”. O histograma foi construído com o apoio do STATISTICA 5.1. Ver <www.statsoft.com.br>.

ANÁLISE EXPLORATÓRIA DE DADOS 85
Renda
Média 6,34 40 I-----1----r 1----1-----1----r 1----r
Erro padrão 0,37 35
(A
Mediana 5,40 S
3°
Moda 3,90 1
25
Desvio padrão 4,03
■o 20
O
Variância da amostra 16,26
fe 15
E
Curtose 4,55
“3 10
z
Assimetria 1,71 -
5
Intervalo 25,60
0
Mínimo 0,10 6 8 10 12 14 16 18 20 22 24 26
Renda (salários mínimos)
Máximo 25,70
Soma 754,50
Contagem 119
Em termos de posição central, temos a média, a mediana e a moda. Esta úl­
tima medida apresenta o valor mais frequente do conjunto de dados. O fato de
a média apresentar um valor maior que a mediana e a moda sugere uma distri­
buição assimétrica, com cauda mais longa para o lado direito, o que é confirma­
do pelo gráfico. Aliás, na lista de medidas, aparece o chamado coeficiente de as­
simetria, com valor igual a 1,71. Em distribuições simétricas, esse coeficiente
aproxima-se de zero. Coeficiente de assimetria positivo (especialmente quando
superior à unidade) indica cauda mais longa para o lado direito. Por outro lado,
quando negativo (especialmente quando inferior a - 1), indica cauda mais lon­
ga para o lado esquerdo.
A medida erro padrão será apresentada no Capítulo 7. A curtose é pouco
usada e, por isso, não será discutida neste texto. O intervalo é o que definimos,
em (3.5), como amplitude; e a contagem é o número de valores (n) usado no
cálculo das medidas descritivas.
3.7 ORIENTAÇÃO GERAL
Em grandes conjuntos de dados, é comum, inicialmente, construir a distri­
buição de frequências de cada variável e, depois, explorar possíveis associações
entre pares de variáveis. Os procedimentos estatísticos dependem do tipo de va­
riável em estudo (ver Figura 3.26).

8 6 ESTATÍSTICA
Tabela
Distribuição
de frequências
friá v e l
Gráfico de
qualitativa
barras,
colunas ou
Porcentagens
setores
Análise
univariada
Histograma
Distribuição
de frequências
\feriável
Ramo-e-folhas
quantitativa
Medidas descritivas
(média, desvio padrão,
mediana etc.)
Medidas descritivas da
variável quantitativa em cada
Uma variável quantitativa categoria da qualitativa
e outra qualitativa
Diagrama em caixas múltiplas
Análise Duas variáveis
Tabela de contingência (Cap. 10)
bivariada qualitativas
Diagrama de dispersão (Cap. 11)
Duas variaveis
quantitativas
Coeficiente de correlação (Cap. 11)
Figura 3.26 Esquema geral para a análise exploratória de dados.
EXERCÍCIOS
3. Dado o seguinte conjunto de dados: {7, 8, 6, 10, 5, 9, 4, 12, 7, 8}, calcule:
a) a média e
b) o desvio padrão.
4. Calcule a média e o desvio padrão da seguinte distribuição de frequências,
a qual se refere ao número de defeitos encontrados em placas de circuito
integrado.

ANÁLISE EXPLORATÓRIA DE DADOS 8 7
Número de defeitos Frequência
0 30
1 25
2 10
3 5
4 2
5. Considerando o Exercício 2 (seção 3.3), obtenha a mediana e os quartis.
6 . Com o objetivo de direcionar campanhas de marketing, uma livraria virtual
está registrando o número de acessos diários em algumas de suas páginas
da Web, nos últimos três meses. A tabela, a seguir, mostra medidas descriti­
vas desses registros, em páginas de três categorias de livros.
Desvio Quartil Quartil
Livro Média Mediana
padrão inferior superior
Romance 910 690 412 650 1.500
Ficção 220 180 145 398 1.023
Técnico 630 480 115 190 1.500
a) Quais as diferenças das três distribuições em termos de posição central
e dispersão?
b) As medidas sugerem distribuições simétricas?
7. Os dados a seguir são leituras da pressão do homogeneizador de um lati­
cínio.
Leite tipo C Leite UHT
3.0 3,1 3,0 3,0 3,0 2,9 2,9 3,0 2.2 2,2 2,3 2,2 2,2 2,2 2,4 2,4
3.1 2,9 3,0 3,0 3,0 3,0 3,0 3,0 2.2 2,4 2,6 2,6 2,4 2,2 2,2 2,8
3,0 3,0 3,0 3,0 2,9 2,6 2,2 2,6 2,4 2,0
Para cada conjunto de dados, calcule as medidas descritivas que você
conhece. Com base nessas medidas, comente as principais diferenças entre
os dois conjuntos de valores.
EXERCÍCIOS
com plem entares
8. Bernardin (Mestrado Engenharia Mecânica/UFSC, 1994) realizou um expe­
rimento que tinha o objetivo de melhorar a qualidade do processo de

8 8 ESTATÍSTICA
formulação de massa cerâmica para pavimento. Os corpos de prova eram
“biscoitos” que saíam do processo de queima e a qualidade era avaliada por
três variáveis, a saber: Xx = retração linear (%), X2 = resistência mecânica e
X3 = absorção de água (%). O experimento foi realizado sob 8 condições di­
ferentes (no estudo original eram 18). Foram feitos 5 ensaios em cada uma
das 8 condições experimentais. Os dados são apresentados a seguir:
c 1 X, x 2 x 3 C1 X! x 2 x 3 C1 X* x 2 x 3 C1 x. x 2 x 3
1 8,9 41,1 5,5 3 9,4 50,0 0,8 5 13,4 60,6 0,5 7 12,9 41,1 0,2
1 9,2 39,0 4,8 3 9,9 48,3 0,6 5 13,4 60,0 0,5 7 12,4 39,0 0,4
1 8,0 36,9 6,2 3 9,6 50,1 0,6 5 13,6 68,4 0,2 7 12,6 36,9 0,5
1 8,7 39,2 5,7 3 9,2 49,9 0,7 5 13,4 60,8 0,7 7 12,6 39,2 0,4
1 8,7 35,9 5,5 3 9,4 56,2 0,5 5 12,4 51,4 1,0 7 12,9 35,9 0,3
2 12,6 52,7 0,9 4 6,6 31,2 9,0 6 9,6 41,2 3,9 8 8,2 40,8 4,4
2 13,6 53,5 0,4 4 6,4 25,3 10,2 6 10,6 53,0 4,5 8 9,2 43,8 3,9
2 11,6 47,0 1,3 4 5,9 22,8 10,5 6 8,9 37,0 3,3 8 9,2 48,6 4,0
2 10,1 31,1 1,8 4 5,9 27,5 10,6 6 7,5 30,1 3,0 8 8,5 46,9 4,3
2 12,1 50,9 1,1 4 6,8 31,9 9,3 6 8,9 41,6 3,5 8 8,7 46,2 4,1
1 C = condição experimental.
a) Como as variáveis Xl} X2 e X3 podem ser classificadas (qualitativas,
quantitativas discretas ou quantitativas contínuas)?
b) Apresente a distribuição de frequências de XY através de um diagrama
ramo-e-folhas. Comente a forma da distribuição.
c) Apresente as distribuições de frequências de X2 e X3 através de histo­
gramas. Comente as formas das distribuições.
d) Calcule a média e o desvio padrão de X3 para cada condição experi­
mental (por simplicidade, considere apenas as condições 1, 4 e 8).
Quais as informações que podem ser extraídas com estas medidas?
e) Construa diagramas de pontos para X3 nas condições experimentais 1,
4 e 8. As informações fornecidas por esses diagramas são iguais às ob­
tidas no item anterior?
f) Calcule a mediana e quartis de Xi (sugestão: use o diagrama ramo-e-
folhas do item (b)).
g) Construa um diagrama em caixas para Xx.

ANÁLISE EXPLORATÓRIA DE DADOS 89
h) Considere o objetivo de verificar qual das variáveis (Xi, X2 e X3) apre­
senta maior variabilidade. Qual medida de dispersão você deve usar?
9. Com respeito ao exercício anterior, o estudo da variabilidade natural do
processo, em termos das 50 observações de Xly X2 e X3, fica prejudicado,
pois os ensaios foram feitos sob 8 condições experimentais diferentes. Con­
siderando, porém, que, para cada variável, a média Xj corresponde a uma
estimativa da j-ésima condição experimental (j = 1, 2,..., 8), então os des­
vios djj = Xij - Xj (i = 1, 2,..., 5) fornecem informações da variabilidade na­
tural do processo. A tabela seguinte apresenta esses desvios.
d, d2 d3 dx d2 d3 d2 d3 d! d2 d3
0 ,2 0 2 ,6 8 - 0 ,0 4 - 0 ,1 0 - 0 , 9 0 0 , 1 6 0 , 1 6 0 ,3 6 - 0 , 0 8 0 ,2 2 2 ,6 8 - 0 , 1 6
0 ,5 0 0 ,5 8 - 0 ,7 4 0 ,4 0 - 2 ,6 0 - 0 ,0 4 0 , 1 6 - 0 , 2 4 - 0 , 0 8 - 0 , 2 8 0 ,5 8 0 ,0 4
- 0 , 7 0 - 1 , 5 2 0 ,6 6 0 ,1 0 - 0 ,8 0 0 ,0 4 0 ,3 6 8 , 1 6 0 ,3 8 - 0 ,0 8 - 1 , 5 2 0 , 1 4
0 ,0 0 0 ,7 8 0 , 1 6 - 0 ,3 0 - 1 ,0 0 0 ,0 6 0 , 1 6 0 ,5 6 0 , 1 2 - 0 , 0 8 0 ,7 8 0 ,0 4
0 ,0 0 - 2 ,5 2 - 0 ,0 4 - 0 ,1 0 5 ,3 0 - 0 , 1 4 - 0 , 8 4 - 8 , 8 4 0 ,4 2 0 ,2 2 - 2 ,5 2 - 0 ,0 6
0 ,6 0 5 ,6 6 - 0 ,2 0 0 ,2 8 3 ,4 6 - 0 , 9 2 0 ,5 0 0 ,6 2 0 ,2 6 - 0 , 5 6 - 4 , 4 6 0 ,2 6
1 ,6 0 6 ,4 6 - 0 ,7 0 0 ,0 8 - 2 ,4 4 0 ,2 8 1 ,5 0 1 2 ,4 2 0 ,8 6 0 ,4 4 - 1 , 4 6 - 0 ,2 4
- 0 , 4 0 - 0 , 0 4 0 ,2 0 - 0 ,4 2 - 4 ,9 4 0 ,5 8 - 0 , 2 0 - 3 ,5 8 - 0 , 3 4 0 ,4 4 3 ,3 4 - 0 , 1 4
- 1 ,9 0 - 1 5 , 9 4 0 ,7 0 - 0 ,4 2 - 0 ,2 4 0 ,6 8 - 1 ,6 0 - 1 0 ,4 8 - 0 , 6 4 - 0 , 2 6 1 , 6 4 0 , 1 6
0 ,1 0 3 ,8 6 0 ,0 0 0 ,4 8 4 , 1 6 - 0 , 6 2 - 0 , 2 0 1 ,0 2 - 0 , 1 4 - 0 , 0 6 0 ,9 4 - 0 ,0 4
Apresente as distribuições de frequências de dx, d2 e d3 através de his­
togramas ou ramo-e-folhas. O que você pode dizer da dispersão dessas dis­
tribuições comparadas às distribuições construídas no exercício anterior,
itens (b) e (c)?
.
10 Os dados abaixo apresentam a distância (em km) entre a residência e o lo­
cal de trabalho dos funcionários da empresa AAA.
1,8 2,5 0,4 1,9 4,4 2,2 3,5 0,2 0,9 1,4
1.1 1,7 1,2 2,3 1,9 0,8 1,5 1,7 1,4 2,1
3.2 15,1 2,1 1,4 0,5 0,9 1,7 0,5 0,8 3,7
1,4 1,8 2,0 1,1 1,0 0,8
a) Apresente esses dados em ramo-e-folhas.
b) Na empresa BBB, a distância (em km) até a residência de seus 300
funcionários apresenta as seguintes medidas descritivas:
Mediana = 2,8 Quartil inferior = 1,6 Quartil superior = 4,2
Extremo inferior = 0,4 Extremo superior = 8,8

9 0 ESTATÍSTICA
Quais as principais diferenças entre as empresas AAA e BBB, em
termos da distância entre a residência e o local de trabalho dos funcio­
nários?
11. Apresentam-se, abaixo, algumas medidas descritivas da distribuição de sa­
lários, em R$, de três empresas do mesmo ramo.
Desvio Extremo Quartil Quartil Extremo
Empresa Média Mediana
padrão inferior inferior superior superior
A 300 100 100 200 302 400 510
B 400 180 100 250 398 550 720
C 420 350 100 230 300 650 10.000
O que se pode dizer sobre a distribuição dos salários nas três empresas?
Quais as diferenças em termos da posição central, dispersão e assimetria?
12. Cada diagrama em caixas da figura a seguir foi construído com 95 leituras
da pressão do homogeneizador. Discuta as diferenças.
3,4
T
O 3,2
T3
ca
i 3,0
& 2,8
o
O
Z,D
XI
O 2 4
O
‘2 2>2
68
O-, 2,0
1
1,8
C UHT
tipo de leite

4
Probabilidade
No capítulo anterior, procuramos conhecer a variabilidade de algum pro­
cesso com base em observações das variáveis pertinentes. Nestes três próximos
capítulos, continuaremos a estudar os processos que envolvem variabilidade,
aleatoriedade ou incerteza, mas procuraremos construir modelos matemáticos
para facilitar a análise. Esses modelos normalmente são construídos a partir de
suposições sobre o processo, mas podem também basear-se em dados observa­
dos no passado.
O leitor já deve ter ouvido falar de probabilidade ou de modelos probabilís-
ticos. Há dois aspectos a considerar. O primeiro é que intuitivamente as pessoas
procuram tomar decisões em função dos fatos que têm maior probabilidade de
ocorrer. Veja os seguintes exemplos:
a) se o céu está nublado, então há chance considerável de chover.
Deve-se levar um guarda-chuva ao sair de casa!;
b) se um inspetor de qualidade está observando as peças produzidas
por uma máquina, e verifica que elas estão saindo fora do padrão,
então ele pode deduzir que existe alta chance de essa máquina con­
tinuar produzindo peças fora do padrão. Logo, a máquina deverá re­
ceber atenção especial;
c) se em determinada família há muitos casos de doença cardíaca, então
há maior chance de pessoas daquela família serem afetadas; portan­
to, os exames preventivos precisam ser feitos mais frequentemente.
O segundo aspecto é a incerteza inerente às decisões que podem ser toma­
das sobre determinado problema.

9 2 ESTATÍSTICA
a) por mais nublado que o céu esteja, pode não chover, ao menos du­
rante o período de tempo em que a pessoa estiver fora de casa;
b) algumas peças poderiam estar fora do padrão por motivos mera­
mente casuais. O processo pode estar funcionando bem;
c) apesar dos vários precedentes familiares, uma pessoa pode viver a
vida inteira sem ter problemas cardíacos.
Se for possível quantificar a incerteza associada a cada fato, algumas deci­
sões tomam-se mais fáceis. Veja os casos a seguir:
a) Qual deve ser a capacidade instalada de uma usina hidrelétrica, em
função da vazão e da precipitação pluviométrica?
b) Qual deve ser a capacidade do servidor de comércio eletrônico de
uma empresa, em função da demanda prevista?
No caso (a), se for possível prever as variações na quantidade de chuva e,
no caso (b), se houver previsão da demanda, podemos responder melhor às
questões que foram colocadas. A teoria do cálculo de probabilidades permite
obter uma quantificação da incerteza associada a um ou mais fatos e, portanto,
é extremamente útil no auxílio à tomada de decisões.
Os modelos probabilísticos são aplicados em situações que envolvem al­
gum tipo de incerteza ou variabilidade. Mais especificamente, consideraremos a
presença de algum experimento aleatório como princípio para a construção de
modelos probabilísticos.
Exemplo 4.1 São exemplos de experimentos aleatórios:
a) o lançamento de um dado e a observação da face voltada para cima;
não sabemos exatamente qual face vai ocorrer, apenas que será uma
das seis existentes. Além disso, se o dado for não viciado e o lança­
mento imparcial, todas as faces têm a mesma chance de ocorrer;
b) a observação dos diâmetros, em mm, de eixos produzidos em uma
metalúrgica; sabemos que as medidas devem estar próximas de um
valor nominal, mas não sabemos exatamente qual é o diâmetro de
cada eixo antes de efetuar as mensurações;
c) o número de mensagens que são transmitidas corretamente por dia
em uma rede de computadores; sabemos que o mínimo possível é
zero, mas não sabemos nem sequer o número máximo de mensa­
gens que serão transmitidas.
Nos casos em que os possíveis resultados de um experimento aleatório po­
dem ser listados (caso discreto), um modelo probabilístico pode ser entendido
como a listagem desses resultados, acompanhados de suas respectivas probabi-

PROBABILIDADE 93
lidades. A Figura 4.1 ilustra as etapas para a construção de um modelo probabi-
lístico.
Definição dos Definição de uma regra que
Definição do N K
resultados possíveis obtenha a probabilidade de
experimento — I r > i— vw>
do experimento cada resultado ocorrer.
Figura 4.1 Passos para a construção de um modelo probabilístico (caso discreto).
4.1 ESPAÇO AMOSTRAL E EVENTOS
Seja um experimento aleatório qualquer.
O conjunto de todos os possíveis resultados do experimento é chamado de
espaço amostrai e é denotado pela letra grega Q.
Exemplo 4.2 Seguem alguns experimentos aleatórios com os respectivos es­
paços amostrais:
a) lançamento de um dado e observação da face voltada para cima:
Q = {1, 2, 3, 4, 5, 6};
b) retirada de uma carta de um baralho comum (52 cartas) e observa­
ção do naipe: Q = {copas, espadas, ouros, paus};
c) o número de mensagens que são transmitidas corretamente por dia
em uma rede de computadores: Q = {0, 1, 2, 3, ..-};1
d) a observação do diâmetro, em mm, de um eixo produzido em uma
metalúrgica: Q = {d, tal que d > O}.2
O espaço amostrai pode ser:
1. finito, formado por um número limitado de resultados possíveis,
como nos casos (a) e (b);
2. infinito enumerável, formado por um número infinito de resultados,
os quais podem ser listados, como no caso (c); ou
1 Note que não há um limite superior conhecido, mas somente é possível a ocorrência de
valores inteiros.
2 Não há um limite superior e, teoricamente, pode haver uma infinidade de valores.

9 4 ESTATÍSTICA
3. infinito, formado por intervalos de números reais, como no caso (d).
Um espaço amostrai é dito discreto quando for finito ou infinito enumerá-
vel; é dito contínuo quando for infinito, formado por intervalos de núme­
ros reais.
Os elementos para se tomar alguma decisão podem corresponder a um con­
junto de resultados (ou evento) associados ao experimento aleatório. Por exem­
plo, se o diâmetro D de um eixo, em mm, que sai da linha de produção, perten­
cer ao conjunto (ou evento) A = {49,0 < D < 51,0}, então se decide que ele é
adequado.
Chamamos de evento qualquer subconjunto do espaço amostrai:
A é um evento o A ç Q
Exem plo 4.3 Seja o experim ento do lançam ento de um dado. Temos:
Q = {1, 2, 3, 4, 5, 6}. São exemplos de eventos:
A = número par do dado = {2, 4, 6};
B = número maior que 2 do dado = {3, 4, 5, 6};
C = número 6 = {6}.
Dizemos que um evento ocorre quando um dos resultados que o compõem
ocorre. Com respeito ao Exemplo 4.3, se o dado for lançado e ocorrer o número
4, então ocorrem os eventos A e B , mas não ocorre o evento C.
Como um evento é um subconjunto do espaço amostrai, então todos os
conceitos da teoria de conjuntos podem ser aplicados a eventos. Considerando
A e B eventos quaisquer, veja as principais operações na Figura 4.2.
Operação Notação Conjunto Evento
a) união A u B reúne os elementos de ocorre quando ocorrer
ambos os conjuntos pelo menos um deles (A,
B ou ambos)
b) interseção A n B formado somente pelos ocorre quando ocorrer
elementos que estão em ambos os eventos (A e B)
A e B
c) complementar A formado pelos elemen­ ocorre quando não ocor­
tos que não estão em A rer o evento A (não A)

PROBABILIDADE 95
(a) União: A u B (b) interseção: A n B (c) complementar: A
Figura 4.2 Principais operações entre eventos e representações gráficas.
Exemplo 4.3 (continuação). Sejam:
A = número par do dado = {2, 4, 6};
B = número maior que 2 do dado = {3, 4, 5, 6};
C = número 6 = {6}.
Eventos complementares:
A = número ímpar do dado = {1, 3, 5};
B = número menor ou igual a 2 do dado = {1, 2};
C = não 6 = {1, 2, 3, 4, 5}.
Algumas uniões:
A u B = {2,3, 4, 5, 6}; A u C = {2, 4, 6}; A u A = Q
Algumas interseções:
A n B = {4, 6}; A n C = {6}; A n A = {} = 0.
Eventos são ditos m utuam ente exclusivos se e só se eles não puderem
ocorrer simultaneamente. Então, para dois eventos quaisquer, A e B, temos:
A e B são mutuamente exclusivos <=> A n B = 0.
No Exemplo 4.3, os eventos A = {1, 3, 5} e C = {6} são
mutuamente exclusivos, pois eles não podem ocorrer simulta­
neamente (observe que A n C = 0 ) .

9 6 ESTATÍSTICA
EXERCÍCIOS
1. Apresente os espaços amostrais dos seguintes experimentos aleatórios:
a) Lançamento de uma moeda honesta e observação da face voltada para
cima.
b) Observação da qualidade de peças produzidas, registrando o número
de peças defeituosas.
c) Contagem do número de clientes numa fila única de banco, que che­
gam durante uma hora.
d) Medição da velocidade do vento, em km/h, na pista de um aeroporto.
e) Medição da temperatura, em graus Celsius, numa estação meteorológi­
ca da cidade de Florianópolis.
2. Considere que você vai cronometrar o tempo, em segundos, para carregar
uma página da web.
a) Represente, em forma de conjuntos, os seguintes eventos:
A = mais do que 5 e, no máximo, 10 segundos;
B = mais do que 10 segundos;
C = mais do que 8 segundos;
D = A u B ; E = A n B, F = A n C, G = A
b) Represente geometricamente (como intervalos na reta dos reais) os
conjuntos do item anterior.
4.2 DEFINIÇÕES DE PROBABILIDADE
Intuitivamente, as pessoas sabem como calcular algumas probabilidades
para tomar decisões. Observe os seguintes exemplos.
Exemplo 4.4
a) Vamos supor que você fez uma aposta com um amigo. O vencedor
será aquele que acertar a face que ficar para cima, no lançamento de
uma moeda honesta.3 Qual é a probabilidade de você ganhar?
Intuitivamente, você responderia que a probabilidade de ganhar é
igual a 50% (ou Vfe).
3 Usaremos a expressão moeda honesta para referenciar uma moeda perfeitamente equi­
librada e lançamentos imparciais. De forma análoga, usaremos o adjetivo honesto para dado, ba­
ralho etc.

PROBABILIDADE 9 7
b)
Você continua apostando com o mesmo amigo. O vencedor será
aquele que acertar o naipe de uma carta que será retirada, ao acaso,
de um baralho comum de 52 cartas. Qual é a probabilidade de você
ganhar?
Novamente, de forma intuitiva, você responderia que é de 25%
(ou
Va).
O que há em comum entre as situações (a) e (b) do Exemplo 4.4? Refletin­
do um pouco, você observará que em ambas as situações temos experimentos
aleatórios. A cada realização do experimento apenas um dos resultados possí­
veis pode ocorrer. Além disso, como se supõe que a moeda e o baralho são ho­
nestos, cada um dos resultados possíveis tem a mesma probabilidade de ocorrer.
4.2.1 Definição clássica de probabilidade
Se um experimento aleatório tem n resultados igualmente prováveis, e nA
desses resultados pertencem a certo evento A, então a probabilidade de ocor­
rência do evento A será:
(4.1)
Exemplo 4.4 (continuação)
a)
No caso da moeda, há apenas dois resultados possíveis e igualmente
prováveis, resultando que a probabilidade de ocorrência de uma das
faces será igual a V (ou 50%).
2
b)
No caso dos naipes do baralho, há quatro resultados possíveis e
igualmente prováveis, resultando que a probabilidade de ocorrência
de um deles será igual a lA (ou 25%). Analogamente, podemos con­
siderar cada carta do baralho como um resultado. Nesse caso, a pro­
babilidade de ocorrer certo naipe é de % = K-
4.2.2 Definição experimental de probabilidade
Muitas vezes, a alocação de probabilidades baseia-se em observações do
passado. Seja um experimento aleatório com espaço amostrai O e um evento A
de interesse. Suponha que esse experimento seja repetido n vezes e o evento
A ocorreu n(A) vezes. A frequência relativa do evento A é dada por:

9 8 ESTATÍSTICA
/(A ) = ^ (4.2)
Tl
À medida que o experimento é repetido mais e mais vezes, sob as mesmas
condições, a frequência relativa do evento A tenderá a ficar cada vez mais pró­
xima da probabilidade de ocorrência do evento A. Mais especificamente:
P(A) = lim /(A) = lim n(A) (4.3)
n->x n-* oc Yi
Exemplo 4.5 Um fabricante de lâmpadas fluorescentes precisa especificar o
tempo de garantia de um de seus modelos. Embora os projetistas estimem que
o tempo médio de vida do modelo seja de 5.000 horas, não se sabe exatamente
como as lâmpadas irão comportar-se. E sem esse conhecimento seria temerário
especificar o tempo de garantia.
Ao definir o experimento aleatório como ligar a lâmpada e registrar o tem­
po (em horas) que ela funciona, o espaço amostrai é formado pelo conjunto de
todos os valores maiores ou iguais a zero, ou seja:
Q = {t, tal que t > 0}
Seja o evento:
At = a lâmpada funcionar até o tempo t
Podemos repetir o experimento com um número n suficientemente grande
de lâmpadas.4 Com os resultados do experimento, podemos calcular as frequên­
cias relativas:
/(A ,) = (4.4)
n
para diversos valores de t. Essas frequências relativas podem ser usadas como
valores aproximados das probabilidades P(A) e, assim, definir adequadamente
o tempo de garantia, de tal forma que ele não seja demasiadamente longo, pois
aí seria necessário repor muitas lâmpadas (custo financeiro alto), mas também
não seja muito curto, o que pode gerar a suspeita de um produto com baixa
qualidade, acarretando perda de mercado.
Em muitas situações, é impossível realizar o experimento diversas vezes.
Veja o exemplo seguinte.
Exemplo 4.6 Quando estudamos o regime de vazões de um rio, com o objeti­
vo de avaliar a viabilidade da construção de uma usina hidrelétrica, não é pos­
sível replicarmos os diversos meses e anos, fenômenos climáticos e eventual in-
4 Há métodos estatísticos para calcular n (tamanho da amostra), conforme será visto no
Capítulo 7.

PROBABILIDADE 99
tervenção humana. Nesse caso, é bastante comum a utilização de dados
históricos.5 Supondo que as condições atuais e futuras sejam razoavelmente se­
melhantes àquelas nas quais os dados foram obtidos, podemos ter uma ideia so­
bre as probabilidades dos eventos de interesse através das frequências relativas
dos dados históricos.
4.2.3 Axiomas e propriedades da probabilidade
Independentemente de como são obtidas, usando a definição clássica ou a
experimental, as probabilidades atendem a alguns axiomas. Formalmente, seja
um experimento aleatório e um espaço amostrai Q associado a ele. A cada
evento £,- (i = 1, 2, ...) associaremos um número real denominado probabilida­
de de ocorrência de £t, P(£j), que deve satisfazer aos seguintes axiomas:
a) 0 < P(Ed < 1
b) P(Q) = 1 e
c) Se Ei, E2, ..., En são eventos m utuam ente exclusivos, então
P(Ei u E2 u ... u £n) = P(Ei) + P(£2) + ••• + P(£n)*
O axioma (a) afirma que uma probabilidade é sempre um número entre 0
e 1 . O axioma (b) afirma que, ao realizar o experimento, sempre vai ocorrer al­
gum dos resultados possíveis, razão pela qual o espaço amostrai é chamado de
evento certo. Já o axioma (c) é menos intuitivo. Ele afirma que, ao unir eventos
formados por resultados diferentes, a probabilidade de ocorrer essa união é
dada pela soma das probabilidades de cada evento.
Para ilustrar os axiomas, retomemos o experimento de lançar um dado e
observar o lado voltado para cima. Temos Q = {1, 2, 3, 4, 5, 6}. Ao realizar o
experimento, certamente vai ocorrer algum elemento de Q; logo, P(Q) = 1. Va­
mos considerar, por exemplo, os eventos associados a cada resultado, isto é,
Ei = i (i = 1, 2, ..., 6). Se for suposto que o dado é perfeitamente equilibrado e
os lançamentos imparciais (dado honesto), podemos atribuir, pela definição
clássica, as seguintes probabilidades: P(£t) = V6 (i = 1, 2, ..., 6). Note que es­
ses eventos são mutuamente exclusivos (£t n £; = O, Vi * j) e a probabilidade
da união de quaisquer desses eventos é dada pela soma das probabilidades de
cada um. Por exemplo, pela definição clássica, Expressão 4.1, temos:
PCÊ! u E2 u £3) = P({1, 2, 3}) = | = |
O mesmo valor pode ser obtido pelo axioma (c):
5 Alguns rios brasileiros têm dados de vazões coletados desde a década de 1930.

1 00 ESTATÍSTICA
P(Ê! u E2 u £3) = PCEj) + P(E2) + P(£3) = I + I + I = i
6 6 6 2
Seguem algumas propriedades básicas da probabilidade:
1. P(0) = 0
Se o experimento é realizado, algum resultado certamente vai
ocorrer (P(Q) = 1). Portanto, 0 nunca ocorre (P(0) = 0). 0 é co­
nhecido como evento impossível.
2. Para o caso discreto, isto é, quando os resultados possíveis podem
ser listados, então, pelo axioma (c), a probabilidade de qualquer
evento pode ser obtida pela soma das probabilidades dos resultados
individuais, ou seja, s e A ç O = {cdj, co2, co3, ... }, então:
(4.5)
No experimento do dado, por exemplo:
P(número par) = P({2, 4, 6}) = P(2) + P(4) + P(6) = 3/6 = V2
Observe que esse processo de calcular probabilidades pode ser
usado mesmo quando o espaço amostrai não for equiprovável.
3. Sejam A ç O e A o evento complementar de A, então:
PCA) = 1 - P(A)
Note que, ao unir A e A temos o espaço amostrai
Q, que tem probabilidade igual a 1. Pelo axioma (c),
temos a expressão do evento complementar.
No experimento do dado, temos, por exemplo, P(ocorrer seis)
= P({6}) = x/ 6. Pela propriedade do evento complementar: P(não
ocorrer seis) = 1 - V6 = 5/ 6.
4. (Regra da soma das probabilidades). Sejam A e B eventos quaisquer,
então:
PCA u B ) = PCA) + P(fí) - PCA n B) (4.7)
Note, pelo esquema ao lado, que, ao somar
PCA) e P(fí), estamos contando duas vezes os pon­
tos do conjunto A n B . Logo, ao calcular P(A u £),
é necessário excluir uma vez P(A n B).

PROBABILIDADE 101
No experimento do dado, sejam: A = {2, 4, 6} e B = {3, 4, 5, 6}.
Portanto, P(A) = 7 * P(B) = 2/3 e P(A n B) = P({4, 6}) = 7 3. A
probabilidade de ocorrer um número maior do que 1 pode ser calcu­
lada por P(A u B ) = l/ 2 + V3 -
l3
= 5/ó- Note que é o mesmo valor
que obteríamos se calculássemos diretamente por (4.1).
EXERCÍCIOS
3. Retira-se, ao acaso, uma carta de um baralho de 52 cartas. Calcule a proba­
bilidade de:
a) a carta não ser de ouros;
b) ser uma carta de ouros ou uma figura.
4. Depois de um longo período de testes, verificou-se que o procedimento A
de recuperação de informação corre um risco de 2% de não oferecer res­
posta satisfatória. No procedimento £, o risco cai para 1%. O risco de am­
bos os procedimentos apresentarem resposta insatisfatória é de 0,5%. Qual
é a probabilidade de pelo menos um dos procedimentos apresentar respos­
ta insatisfatória?
5. De um conjunto de cinco empresas, deseja-se selecionar, aleatoriamente,
uma empresa, mas com probabilidade proporcional ao número de funcio­
nários. O número de funcionários da Empresa A é 20; de B é 15; de C é 7;
de D é 5 e de E é 3.
a) Qual é a probabilidade de cada uma das empresas ser a selecionada?
b) Qual é a probabilidade de a Empresa A não ser selecionada?
6. Considere que a probabilidade de ocorrer k defeitos ortográficos em uma
página de jornal é dada por:
p(k) = — (e * 2,7183)
e • k\
Tomando-se uma página qualquer, calcule a probabilidade de:
a) não ocorrer erro;
b) ocorrer mais do que dois erros.
7. Mostre que:
P ( A u B u C ) = P(A) + P(fí) + P(C) - P(A n B) - P(A n C) - P(B n C) +
P(A n B n C )

1 02 ESTATÍSTICA
4.3 PROBABILIDADE CONDICIONAL E INDEPENDÊNCIA
Muitas vezes, há interesse em calcular a probabilidade de ocorrência de
um evento A, dada a ocorrência de um evento B. Exemplos:
• Qual é a probabilidade de chover amanhã em Florianópolis, sabendo
que choveu hoje?
• Qual é a probabilidade de um dispositivo eletrônico funcionar sem
problemas por 200 horas consecutivas, sabendo que ele já funcionou
por 100 horas?
• Qual é a probabilidade de que um dos três servidores de correio ele­
trônico fique congestionado, sabendo que um deles está inoperante?
Em outras palavras, queremos calcular a probabilidade de ocorrência de A
condicionada à ocorrência prévia de B. Essa probabilidade é representada por
P(A\B) (lê-se probabilidade de A dado £).
Exemplo 4.7 Os dados, a seguir, representam o sumário de um dia de obser­
vação em um posto de qualidade, em que se avalia o peso dos pacotes de leite
produzidos num laticínio.
Tipo do leite
Condição do peso
b m c (C) UHT (U) Total
Dentro das especificações (D) 500 4.500 1.500 6.500
Fora das especificações CF) 30 270 50 350
Total 530 4.770 1.550 6.850
Retira-se, ao acaso, um pacote de leite da população de 6.850 unidades.
Sejam D e F os eventos que representam se o pacote retirado está dentro ou
fora das especificações, respectivamente. Da mesma forma, B, C eU são eventos
que representam o tipo do leite. Pergunta-se:
a) Qual é a probabilidade de o pacote de leite estar fora das especifica­
ções?
Resp.: Como o espaço amostrai é composto de 6.850 unidades, sen­
do que 350 satisfazem ao evento, então:
350
P(F) = = 0,051
6.850

PROBABILIDADE 103
b) Qual a probabilidade de o pacote de leite retirado estar fora das es­
pecificações, sabendo-se que é do tipo UHT?
Resp.: Nesse caso, o espaço amostrai ficou restrito às 1.550 unidades
de leite UHT. Destas, 50 satisfazem ao evento. Então:
50
P(F\U) = = 0,032
1.550
Note que, se o numerador e o denominador de P(F | L0 forem divididos
pelo número total de unidades, temos:
PlFIlTl - 50 506-850 H F n . U )
L 5 5 ° 1 S 5 0 6 . S 5 O P í m
que é a relação usada na definição formal de probabilidade condicional.
Sejam A e B eventos quaisquer, sendo P(£) > 0. Definimos a probabilidade
condicional de A dado B por:
PÇA nB)
(4.8)
P(B)
Note que no denominador temos a probabilidade do evento que suposta­
mente aconteceu, mas calculada nas condições originais do experimento.
Se houver interesse no oposto, isto é, na probabilidade de ocorrência de B
condicionada à ocorrência prévia de A, sendo P(A) > 0, temos:
P(B |Â) = (4.9)
É importante ressaltar que a operação de intersecção é comutativa, impli­
cando P(A n fí) = P(£ n A).
Exemplo 4.8 Seja o lançamento de 2 dados não viciados e a observação das
faces voltadas para cima. Suponha que haja interesse nas probabilidades dos se­
guintes eventos:
a) Faces iguais, sabendo que a soma é menor ou igual a 5.
b) Soma das faces menor ou igual a 5, sabendo que as faces são iguais.
Inicialmente, vamos explicitar o espaço amostrai desse experimento, que é
formado por todas as 6 x 6 = 36 possíveis combinações de resultados dos dois
dados, ou seja:

1 04 ESTATÍSTICA
(1,1) (1,2) (1,3) (1,4) (1,5) (1,6)
(2,1) (2,2) (2,3) (2,4) (2,5) (2,6)
(3,1) (3,2) (3,3) (3,4) (3,5) (3,6)
(4,1) (4,2) (4,3) (4,4) (4,5) (4,6)
(5,1) (5,2) (5,3) (5,4) (5,5) (5,6)
(6,1) (6,2) (6,3) (6,4) (6,5) (6,6)
Considere os eventos:
El = faces iguais = {(1,1), (2,2), (3,3), (4,4), (5,5), (6,6)} e
E2 = soma das faces é menor ou igual a 5 =
= {(1,1), (1,2), (1,3), (1,4), (2,1), (2,2), (2,3), (3,1), (3,2), (4,1)}.
Portanto, Ei n E2 = {(1,1), (2,2)}. Esquematicamente:
Calculando
a) A probabilidade de as faces serem iguais, sabendo que a soma é me­
nor ou igual a 5. Ou seja:
PÍEJEj) = F,E r ' E l i ----- = A = 0,2
P(E.) 1036 10
Note que, se o espaço amostrai for restringido ao evento conhe­
cido, E2, temos 10 resultados possíveis, sendo que 2 satisfazem tam­
bém ao evento de interesse, Ex, o que torna natural a probabilidade
condicional ser 2/ 10.
b) A probabilidade de a soma das faces ser menor ou igual a 5, saben­
do que as faces são iguais. Ou seja:
PCfclJU = = ^ = 1 =0,333...
3 6

PROBABILIDADE 105
4.3.1 A regra do produto
Uma das consequências da expressão da probabilidade condicional (4.8) é
a regra do produto, obtida ao isolar a probabilidade da interseção. Ou seja:
P(A|B) = P ( A n B ) P ( A n B ) = P(B ).P(A |B ) (4.10)
P(B)
que fornece uma fórmula de calcular a probabilidade de ambos os eventos (A e
£) ocorrerem. Em (4.10), o evento condicionado é B, mas o inverso também é
possível, pois
PÇB n A )
P(B|A) = P(A n B ) = P(A) . P(fí\A) (4.11)
P(A)
Para três eventos, A, B e C, a regra do produto pode ser escrita como
P ( A n B n Q = P(A) . P(B|A) . P(C|A n B) (4.12)
É importante que seja observada a sequência lógica dos eventos para mon­
tar as expressões precedentes.
Exemplo 4.9. Uma caixa contém 4 cartões amarelos e 8 vermelhos. Retira­
mos, ao acaso, 2 cartões, um após o outro, sem reposição, e observamos as co­
res dos dois cartões.
a) Qual é a probabilidade de que ambos sejam amarelos?
Chamando de At o evento que representa cartão amarelo na
i-ésima extração e Vf o evento que representa cartão vermelho na
i-ésima extração (i = 1, 2), temos o seguinte espaço amostrai:
Q = {(Aj, A2), (Aj, V2X (yu AJ, (Vl} V2)}
A probabilidade de interesse é P{(A1? A2)}, que também pode
ser colocada em termos de interseção: P(Ai A2), isto é, a probabi­
lidade de ocorrer amarelo na primeira extração e amarelo na se­
gunda extração. Para a aplicação da regra do produto, P(Ai r\ A2) =
P(Ai) . P(A2\Ai), calculamos:
4 1
P(A- ) = — = - (pois existem 4 amarelos dentre os 12 cartões) e
12 3

1 06 ESTATÍSTICA
3
P(A2\ A l ) = — (pois, supondo que tenha sido extraído cartão amare­
lo na primeira extração, restaram 3 amarelos dentre 11 cartões).
Logo, PCAt n Á2) = PCAJ . PCA^AJ
3 11 11
b) Como alocar probabilidades a todos os elementos do espaço amostrai?
Nesse caso, podemos construir uma árvore, indicando todas as
situações possíveis (arvore de probabilidades). Veja a Figura 4.3.
3 amarelos
8 vermelhos
KA , = - (total = 11)
4 amarelos
8 vermelhos
P(A; | V.) = —
(total = 12)
11
W ) = —
4 amarelos
12 7 vermelhos
(total = 11)
P(V2\V) = —
11
1- extração 2- extração
Figura 4.3 Árvore de probabilidades - retiradas sem reposição (A = amarelo;
V = vermelho).
Com base na Figura 4.1, podemos calcular as probabilidades de
todos os resultados do espaço amostrai, como segue:
P{(A,, Â2)} = P(A, n A2) = P(Ai) • PCAj IAj) = A . A = JL
12 11 11
PÍCAi, V2)} = PÍA1 n Vj) = PCAj) • P(V2|Ai) = ^
X X O J

PROBABILIDADE 1 07
P{(Vu ^ 2)} = P(Vj n A2) = P(V,) ■ P(Â2|VO = 8 4 8
12 11 33
P W i, V2)} = P(Vj n V2) = P(V,) • P(V2|Vj) = A .Z . = 11
1Z 1 1 0 0
Observe que a soma dos quatro resultados possíveis é igual a 1
(axioma (b) da probabilidade).
c) Qual é a probabilidade de ocorrer exatamente 1 cartão amarelo?
Queremos a probabilidade de ocorrer (A1? V2) ou (Vx, A2). Em
termos da linguagem de conjuntos, queremos a união dos dois resul­
tados (eventos). Como esses eventos são mutuamente exclusivos
(não podem ocorrer simultaneamente), então a probabilidade é
dada pela soma, ou seja:
(yu +
PKAu V2) A J } = P(Ai, v2) P(Vh A2) = + ±
u A . g
J J J J 00
d) Considere a retirada de 3 cartões. Qual é a probabilidade de que os
dois primeiros sejam vermelhos e o terceiro seja amarelo?
Desejamos calcular
P(Vx n V2 n A3) = PfVO • P(V2 |Vi) • P(A3 |Vi n V2)
Os dois primeiros fatores já foram calculados anteriormente.
Para calcular P(A31V1 n V2) basta considerar a caixa com 2 cartões
vermelhos a menos, ou seja, com 4 amarelos e 6 vermelhos. Assim:
PW31 Vj n V2) = 4
10
Logo:
nn, T/ - . 8 7 4 28
P(Vi n V2 n A3) --------------------------
12 11 10 165
4.3.2 Eventos independentes
O Exemplo 4.10 é parecido com o exemplo anterior, mas com a amostra­
gem feita com reposição. Verifique que os cálculos tornam-se mais simples, pois
a configuração da urna não se altera na segunda extração.
Exemplo 4.10 Uma caixa contém 4 cartões amarelos e 8 vermelhos. Reti-
ram-se, ao acaso, 2 cartões da caixa, um após o outro, sendo que o primeiro

1 08 ESTATÍSTICA
cartão é reposto antes da retirada do segundo (amostragem com reposição), e
observa-se a cor dos dois cartões.
A Figura 4.4 apresenta a árvore de probabilidades desse experimento.
P(A |A.) = -
12
4 amarelos
8 vermelhos
(total = 12)
A C -'S
4 amarelos
8 vermelhos
(total = 12)
W V < = >
4 amarelos
P(V,) =
8 vermelhos
(total = 12) T
P(V,|VJ = —
12
1- extração 2- extração
Figura 4.4 Arvore de probabilidades - retiradas com reposição (A = amarelo;
V = vermelho).
Note que nessa situação, P(A2 |A2) = P(A21 Vi) = 4/ i 2, ou seja, não importa
se saiu cartão amarelo ou vermelho na primeira extração, a probabilidade de
sair amarelo na segunda extração é de 4/ i 2 - há independência entre os eventos.
Assim, basta escrever P(A2), sem condicionante.
Dois ou mais eventos são independentes quando a ocorrência de um dos
eventos não influencia a probabilidade da ocorrência dos outros.
Se dois eventos A e B são independentes, então:
PCA|B) = P(A) e (4.13)
P(B\A) = P(B) (4.14)

PROBABILIDADE 109
Como consequência de (4.14), a regra do produto pode ser simplificada da
seguinte forma:
P(A n B) = P(A) • P(B|A) = P(A) • P(B) (4.15)
Essa relação é usada para definir formalmente eventos independentes, ou
seja:
A e B são independentes <=> P(A n B ) = P(A) • P(fí)
A definição de independência ainda pode ser ampliada para mais eventos,
como segue:
Elf E2... En são independentes <=> P(El n £2 n ... n £ri) = P(jE2) . P(£2) ••• P(Bn)
Embora a implicação seja dos dois lados, normalmente as condições do ex­
perimento permitem verificar se é razoável supor independência entre os even­
tos e, em caso afirmativo, o cálculo da probabilidade da interseção pode ser fa-
torado nas probabilidades dos eventos independentes.
Quando a população for bastante grande em relação ao tamanho da amos­
tra, mesmo que a amostragem seja feita sem reposição, podemos supor inde­
pendência. Imagine que no experimento do Exemplo 4.9 haja 4.000 cartões
amarelos e 8.000 vermelhos. Ao extrair dois cartões, a probabilidade de sair
amarelo na segunda extração é de aproximadamente 4/ u , independentemente
de ter saído amarelo ou vermelho na primeira extração.
Exemplo 4.11. Considere um sistema composto de n componentes ligados em
série, de tal forma que, se um componente falhar, o sistema todo falha. Esque­
maticamente:
— > © — (§>-............~ © — >
Se os componentes operam independentemente e cada um tem probabilida­
de p de falhar, qual é a probabilidade de o sistema funcionar?
R e s p (1 - p)n (verifique o porquê; use a regra do produto para eventos
independentes).

1 10 ESTATÍSTICA
EXERCÍCIOS
8. Para testar se um sistema especialista responde satisfatoriamente a um
usuário, foram feitas cinco perguntas, cada uma com quatro alternativas de
resposta. Se o sistema escolhe as alternativas aleatoriamente, qual é a pro­
babilidade de ele responder corretamente a todas as cinco perguntas?
9. Com respeito ao Exemplo 4.7, calcule:
P(D); P(B); P(D n fí); P(D|B); P(B|D).
4.4 TEOREMA DA PROBABILIDADE TOTAL
Exemplo 4.12. Imagine que você utiliza peças de quatro fornecedores, que
têm diferentes desempenhos quanto a sua qualidade. As peças são classificadas
como conformes ou não conformes e você conhece a proporção de peças não
conformes de cada fornecedor (px, p2, p3 e p4). Considere a formação de um lote
com peças dos quatro fornecedores, conforme ilustra a Figura 4.5. Se você sele­
cionar, ao acaso, uma das peças do lote, qual é a probabilidade de ela ser não
conforme?
Fornecedor:
(1) (2) (3) (4)
Grupo de peças
extraídas para a
Peças não conformes formação do lote
Figura 4.5 Ilustração da formação de um lote de peças provindas de quatro for­
necedores.
A resposta seria simples se você soubesse de qual fornecedor é a peça sele­
cionada, mas você não sabe. O chamado teorema da probabilidade total permite
solucionar esse problema.
Considere o espaço amostrai particionado em k eventos, Eíf E2, ..., Ek, sa­
tisfazendo às seguintes condições:
a) n Ej = 0 para todo i * j (eventos mutuamente exclusivos);
b) Ex u E2 u ... u Ek = Q (eventos exaustivos) e
c) P(£j) > 0 para i = 1, 2, ..., k. Veja a Figura 4.6.

PROBABILIDADE 111
Figura 4.6 Partição do espaço amostrai em eventos mutuamente exclusivos.
Seja um evento F qualquer, referente ao espaço amostrai Q. Então:
F = (F n £i) u ( F n F2) u ... u (F n F*)
onde os eventos (F n F*) (í = 1, 2, ..., n) são mutuamente exclusivos entre si.
Logo:
P(F) = P[(F n F J u ( F n F2) u ... u (F n F*)] =
= P(F n FO + P(F n F2) + ... + P(F n Fk)
Usando a regra do produto, temos a seguinte equação, conhecida como o
teorema da probabilidade total:
P(F) = P(Fa) • P(F|Fi) + P(F2) • P(F|F2) + ... + P(F,) . P(F|F*)
ou (4.16)
Naturalmente, algumas P(F | F,) poderão assumir valor zero por não haver
interseção entre F e F,. O teorema da probabilidade total pode ser interpretado
fisicamente como uma medida do peso de cada um dos eventos F„ na contribui­
ção para formar o evento F.
Exemplo 4.12 (continuação) Os eventos Ft representam as procedências das
peças (fornecedores 1, 2, 3 e 4), e o evento F representa peça não conforme. Re­
pare que os eventos F, (fornecedores) são mutuamente exclusivos, pois a peça
somente pode ser originária de um dos fornecedores; e que o evento F tem in­
terseção com cada um deles (uma vez que todos os fornecedores produzem pe­
ças não conformes).
Suponha a mesma probabilidade para todos os fornecedores, isto é,
P(F0 = P(F2) = P(F3) = P(F4) = 0,25

1 12 ESTATÍSTICA
e as probabilidades de não conformidade para cada fornecedor sejam:
Pl = P(F I EO = 0,1; p2 = P(F I £2) = 0,1; p3 = P(F I £3) = 0,2;
p4 = P(F I £4) = 0,4
Então, usando (4.16), a probabilidade de não conforme é dada por:
P(F) = (0,25) (0,1) + (0,25)(0,1) + (0,25) (0,2) + (0,25) (0,4) = 0,20.
4.5 TEOREMA DE BAYES
O teorema de Bayes está intimamente relacionado ao teorema da probabi­
lidade total. Supõem-se as mesmas condições (eventos £, mutuamente exclusi­
vos e exaustivos e um evento F qualquer). Basicamente, o teorema de Bayes
permite obter a probabilidade de que um dos eventos £t ocorra, sabendo-se que
o evento F ocorreu. Para o caso das peças dos quatro fornecedores, o Teorema
de Bayes permite responder a questões do tipo: “sabendo-se que a peça é não
conforme, qual é a probabilidade de que tenha vindo do fornecedor 4?”
De maneira geral, usando a expressão (4.8), temos:
P(E P (£ ' n F )
\ F ) =
p m
Usando a regra do produto (4.10), podemos escrever o chamado Teorema
de Bayes:
p ffiin - (4.i7)
onde P(F) é calculado por (4.16).
Exemplo 4.12 (continuação) Sabendo-se que a peça é não conforme, qual é a
probabilidade de que ela tenha vindo do fornecedor 4?
Lembrando que já calculamos P(F) = 0,20, então, aplicando (4.17), temos:
nE,m
= r o ^ - w i E . ) , m a t o , « » , 0 0
P(F) 0,20

PROBABILIDADE 113
EXERCÍCIOS
10. Uma caixa contém três cartões verdes, quatro amarelos, cinco azuis e três
vermelhos. Dois cartões são retirados da caixa, ao acaso, um após o outro,
sem reposição. Anotam-se suas cores. Calcular a probabilidade de que:
a) os dois cartões sejam da mesma cor;
b) os dois cartões sejam verdes, sabendo-se que são da mesma cor.
11. Uma rede local de computadores é composta por um servidor e cinco clien­
tes (A, B, C, D e E). Registros anteriores indicam que dos pedidos de deter­
minado tipo de processamento, realizados através de uma consulta, cerca
de 10% vêm do cliente A, 15% do B, 15% do C, 40% do D e 20% do E. Se
o pedido não for feito de forma adequada, o processamento apresentará
erro. Usualmente, ocorrem os seguintes percentuais de pedidos inadequa­
dos: 1% do cliente A, 2% do cliente B, 0,5% do cliente C, 2% do cliente D e
8% do cliente E.
a) Qual é a probabilidade de o sistema apresentar erro?
b) Qual é a probabilidade de que o processo tenha sido pedido pelo cliente
E, sabendo-se que apresentou erro?
EXERCÍCIOS COMPLEMENTARES
12. A probabilidade de que Joãozinho resolva este problema é 0,5. A probabili­
dade de que Mariazinha resolva este problema é 0,7. Qual é a probabilida­
de de o problema ser resolvido se ambos tentarem independentemente?
13. Um sistema tem dois componentes que operam independentemente. Supo­
nha que as probabilidades de falha dos componentes 1 e 2 sejam 0,1 e 0,2,
respectivamente. Determinar a probabilidade de o sistema funcionar nos
dois casos seguintes:
a) os componentes são ligados em série (isto é, ambos devem funcionar
para que o sistema funcione);
b) os componentes são ligados em paralelo (isto é, basta um funcionar
para que o sistema funcione).
14. Um sistema tem quatro componentes que operam independentemente, sen­
do que cada componente tem probabilidade 0,1 de não funcionar. O siste­
ma é ligado da seguinte forma:
Determinar a probabilidade de o sistema funcionar.

1 14 ESTATÍSTICA
15. De acordo com certa tábua de mortalidade, a probabilidade de José estar
vivo daqui a 20 anos é de 0,6, e a mesma probabilidade para Manuel é de
0,9. Determinar:
a) P (ambos estarem vivos daqui a 20 anos);
b) P (nenhum estar vivo daqui a 20 anos);
c) P (um estar vivo e outro estar morto daqui a 20 anos).
16. Após um longo processo de seleção para preenchimento de duas vagas de
emprego para engenheiro, uma empresa chegou a um conjunto de 9 enge­
nheiros e 6 engenheiras, todos com capacitação bastante semelhante. Inde­
ciso, o setor de recursos humanos decidiu realizar um sorteio para preen­
cher as duas vagas oferecidas.
a) construa o modelo probabilístico, considerando que se esteja observan­
do o sexo (masculino ou feminino) dos sorteados;
b) qual é a probabilidade de que ambos os selecionados sejam do mesmo
sexo?
c) sabendo-se que ambos os selecionados são do mesmo sexo, qual é a
probabilidade de serem homens?
17. Está sendo avaliada a qualidade de um lote de peças numa indústria cerâ­
mica, onde estão misturados 30 pisos e 40 azulejos.
a) retira-se uma peça ao acaso do lote e observa-se o tipo de cerâmica.
Construa o modelo probabilístico para esta situação;
b) retiram-se duas peças ao acaso do lote, uma após a outra, com reposi­
ção, e observa-se o tipo de cerâmica. Construa o modelo probabilístico
para esta situação;
c) repita o item (b), supondo que não haja reposição;
d) registros anteriores da qualidade indicaram que 1,5% dos azulejos e
cerca de 0,7% dos pisos apresentaram defeitos. Retira-se, ao acaso,
uma peça do lote. Qual é a probabilidade de a peça apresentar defeito?
e) para as condições do item (d), qual é a probabilidade de a peça ser
piso, uma vez que apresentou defeito?
18. A caixa I tem 8 peças boas e 2 defeituosas; a caixa II tem 6 peças boas e 4
defeituosas; a caixa III tem 15 peças boas e 5 defeituosas.
a) tira-se, aleatoriamente, uma peça de cada caixa. Determinar a probabi­
lidade de serem todas boas;
b) escolhe-se uma caixa ao acaso e tira-se uma peça. Determinar a proba­
bilidade de ser defeituosa;

PROBABILIDADE 115
c) escolhe-se uma caixa ao acaso e tira-se uma peça. Calcular a probabi­
lidade de ter sido escolhida a caixa I, sabendo-se que a peça é defei­
tuosa.
19. A qualidade de CDs foi avaliada em termos da resistência a arranhão e ade­
quação das trilhas. Os resultados de 1.000 CDs foram:
Adequação das trilhas
Resistência a arranhão
Aprovado Reprovado
Alta 700 140
Baixa 100 60
Se um CD for selecionado ao acaso desse lote de 1.000 CDs, qual é a
probabilidade de ele:
a) ter resistência a arranhão alta e ser aprovado na avaliação das trilhas?
b) ter resistência a arranhão alta ou ser aprovado na avaliação das trilhas?
c) ser aprovado na avaliação das trilhas, dado que tem resistência a arra­
nhão alta?
d) ter resistência a arranhão alta, dado que foi aprovado na avaliação das
trilhas?
20. Certo sistema funciona somente se houver um caminho fechado de A a B,
com componentes que funcionam. Os componentes funcionam indepen­
dentemente um dos outros. O sistema é esquematizado abaixo, assim como
as probabilidades de falha de cada componente:
0,01 0,02
A — ► — ►
0,04 0,03
Calcule a probabilidade de o sistema funcionar.
21. Dois números inteiros são extraídos, aleatoriamente e sem reposição, do in­
tervalo [- 20, 29]. Esses dois números são multiplicados. Qual é a probabi­
lidade de o produto ser positivo?

5
Variáveis Aleatórias Discretas
5.1 VARIÁVEL ALEATÓRIA
Um conceito de fundamental importância para a estatística indutiva é o de
variáveis aleatórias. Para entender esse conceito, imagine que um dado comum
vai ser lançado. Tente dizer qual será o número resultante. É claro que, antes
do lançamento, não podemos dizer qual é o número que ocorrerá, pois o resul­
tado depende do fator sorte e, por isso, é uma variável aleatória.
Uma variável aleatória pode ser entendida como variável quantitativa,
cujo resultado (valor) depende de fatores aleatórios.
Outros exemplos de variáveis aleatórias são:
a) número de coroas obtido no lançamento de duas moedas;
b) número de itens defeituosos em uma amostra retirada, aleatoria­
mente, de um lote;
c) número de defeitos em um azulejo que sai da linha de produção;
d) número de pessoas que visitam um determinado site, num certo pe­
ríodo de tempo;
e) volume de água perdido por dia, num sistema de abastecimento;
f) resistência ao desgaste de um tipo de aço, num teste padrão;

VARIÁVEIS ALEATÓRIAS DISCRETAS 1 1 7
g) tempo de resposta de um sistema computacional;
h) grau de empeno em um azulejo que sai da linha de produção.
Todos os exemplos acima têm uma característica comum: além do resulta­
do ser quantitativo (valor real), não podemos prevê-lo com exatidão, pois ele
depende de experimento aleatório.
Embora no exemplo do dado os valores que a variável aleatória pode assu­
mir coincidam com o espaço amostrai do experimento, este não é um caso ge­
ral. No exemplo (a), lançamento de 2 moedas, o espaço amostrai mais completo
éQ = {(cara, cara), (cara, coroa), {coroa, cara), {coroa, coroa)}, enquanto que a
variável aleatória número de coroas assume valores no conjunto {0, 1, 2}. Mas
existe uma relação (função) entre os dois conjuntos, conforme mostra o esque­
ma a seguir:
Q = {(cara, cara), (cara, coroa), {coroa, cara), {coroa, coroa)}
Formalmente, uma variável aleatória é uma função que associa elemen­
tos do espaço amostrai ao conjunto de números reais.
As variáveis aleatórias podem ser discretas ou contínuas, conforme mostra
a Figura 5.1.
Variável aleatória
Ex. Ex.
0 1 2 3 4 ... 0
número de defeitos em ... tempo de resposta de ...
Figura 5.1 Variáveis aleatórias discretas e contínuas.

1 18 ESTATÍSTICA
Os casos (a) - (d) são exemplos de variáveis aleatórias discretas e os casos
(g) - (h) são exemplos de variáveis aleatórias contínuas. No restante deste capí­
tulo, trataremos apenas do primeiro caso.
Cabe observar que as variáveis qualitativas também podem ser caracteriza­
das como variáveis aleatórias discretas, desde que as representemos como va­
riáveis indicadoras 0 ou 1. Por exemplo, ao avaliar azulejos que saem de uma li­
nha de produção, cada azulejo pode ser classificado como bom (X = 0) ou
defeituoso (X = 1). Nesse caso, a variável aleatória discreta X está definida
como variável indicadora de item defeituoso.1
5.1.1 Distribuição de probabilidades
Definida uma variável aleatória discreta, temos a descrição do que pode
ocorrer no experimento aleatório. Em alguns casos e sob certas suposições, te­
mos duas informações:
• quais resultados podem ocorrer;
• qual é a probabilidade de cada resultado acontecer.
Exemplo 5.1 Seja a variável aleatória X = número obtido no lançamento de
um dado comum. Se assumirmos o dado perfeitamente equilibrado e o lança­
mento imparcial, podemos alocar as seguintes probabilidades aos valores possí­
veis de X:
Valores possíveis Probabilidades
X PM
1
v 6
2 v 6
3
7 ô
4 v 6
5
Vô
6
v 6
Total 1
Ou, mais resumidamente, p(j) = V6 0 = 1, 2, 3, 4, 5, 6).
1 Se houver mais de duas categorias (por exemplo, A,B eC), podemos usar mais de uma
variável indicadora. No caso de três categorias, podem ser empregadas as variáveis aleatórias X e
Y, onde X = 1 se ocorrer B, e X = 0 caso contrário; Y = 1 se ocorrer C, e Y = 0 caso contrário. A
ocorrência de A estaria representada por X = 0 e Y = 0.

VARIÁVEIS ALEATÓRIAS DISCRETAS 1 1 9
A distribuição de probabilidades de uma variável aleatória X é a descri­
ção do conjunto de probabilidades associadas aos possíveis valores de X, con­
forme foi ilustrado no exemplo precedente. Observe que a soma das probabili­
dades dos valores possíveis de X é igual a 1 (um).
Se X for discreta, com possíveis valores {Xj, x2, ...}, então a distribuição de
probabilidades de X pode ser apresentada pela chamada função de pro­
babilidade, que associa a cada valor possível xi a sua probabilidade de
ocorrência p(xt), ou seja:
pbcd = P(X = Xi) (i = 1, 2, ...)
Uma função de probabilidade deve satisfazer:
a) p(xt) > 0;
W X p O O = 1
i
Existe certa similaridade entre as distribuições de probabilidades e as dis­
tribuições de frequências vistas no Capítulo 3. Contudo, na distribuição de pro­
babilidades são mostrados os possíveis valores e não os valores efetivamente ob­
servados. Além disso, as probabilidades são, geralmente, alocadas a partir de
suposições a respeito do experimento aleatório em questão, enquanto as fre­
quências são obtidas com efetivas realizações do experimento.
A Figura 5.2 apresenta gráficos que podem ser usados para representar a
distribuição de probabilidade de uma variável aleatória discreta. O gráfico em
hastes (do lado esquerdo) é típico para variáveis aleatórias discretas. Já o gráfi­
co em forma de histograma (do lado direito) é construído com o cuidado de a
área total ser igual à unidade.
m
área total = 1
1 2 3 4 5 6
Figura 5.2 Representações gráficas da distribuição de probabilidades da variável
aleatória X = número obtido no lançamento de um dado comum.

1 20 ESTATÍSTICA
5.1.2 Função de distribuição acumulada
Outra forma de representar uma distribuição de probabilidades de uma
variável aleatória é através de sua função de distribuição acumulada, que é de­
finida por:
F(x) = PÇX < x), Vx 6 <R (5.1)
Assim, para todo x e 9Í, a função de distribuição acumulada descreve a
probabilidade de ocorrer um valor até x, conforme é ilustrado a seguir:
v—
atéx
A variável aleatória X = número obtido no lançamento de um dado comum
tem a seguinte função de distribuição acumulada:
FM
'0 se x < 1
i
Ve se 1 < x < 2
%- O
2/ 6 se 2 < x < 3
%
FOò = < 3/ 6 se 3 < jc < 4
Vt
v 6 se 4 < x < 5 %
s/ 6 se 5 < x < 6 %
V 1 se x > 6
Observe que os pontos em que a função de probabilidade descreve proba­
bilidades não nulas correspondem a saltos na função de distribuição acumulada
e, também, que a altura de cada salto equivale ao valor da probabilidade na­
quele ponto. Assim, para todo x e 9?, há uma relação direta entre p(x) e F(x).
5.1.3 Valor esperado e variância
Na análise exploratória de dados, discutimos algumas medidas (particular­
mente, a média, a variância e o desvio padrão - Capítulo 3) para sintetizar as
informações sobre distribuições de frequências de variáveis quantitativas. De
forma análoga, essas medidas também podem ser definidas para as variáveis
aleatórias, com o objetivo de sintetizar características relevantes de uma distri­
buição de probabilidades. Considere uma variável aleatória X e sua distribuição
de probabilidades:

VARIÁVEIS ALEATÓRIAS DISCRETAS 121
Valores possíveis Probabilidades
Pi
X2 P2
*3 P3
Xk Pk
Total 1
A média ou valor esperado de uma variável aleatória X é dado por:
(5.2)
E a variância por:
(5.3)
Alternativamente, a variância pode ser calculada por:2
(5.4)
onde: EQC2) = ^ j x 2p j
E o desvio padrão é dado por:
(5.5)
Retomemos o exemplo da variável aleatória X = número obtido no lança­
mento de um dado comum, em que a função de probabilidade é dada por:
P(fi = V6 (j = 1, 2, 3, 4, 5, 6)
A demonstração da equivalência de (5.3) e (5.4) é apresentada a seguir:
= £ ( x 2 - 2xp + \i2)p1 = £ x)pj - 2\i£ xjpj + £ p.u2 =
/-I hi
= 2 > 2P;-2|41 + H2£ p ; = ^*}Pj - 2n2 + |i2 = i£x*pr \i2 =£(X2)-(1:

1 22 ESTATÍSTICA
e calculemos o valor esperado e a variância.
n
+ 2 1 —'j + 3 + 6[ £1=3,5
6 ) /
'1 N
ECX2) = 12[ | j + 22 | N+ 3 + 4 21 -1 + 5 2 ( - I + 6 2 = 15,167
/ /
Assim, VOO = SC*2) - M2 = 15,167 - (3,5)2 = 2,92.
Considerando que as probabilidades podem ser interpretadas como limite
da frequência relativa quando o experimento é executado muitas e muitas ve­
zes, podemos interpretar o valor esperado como a média aritmética dos resulta­
dos da variável aleatória se o experimento pudesse ser repetido infinitas vezes.
Assim, se pudéssemos lançar o dado infinitas vezes, obteríamos, em média, 3,5
pontos por lançamento. Já a variância informa sobre a dispersão dos possíveis
valores.
Observe que, no presente exemplo, o valor esperado = 3,5 é um número
que a variável aleatória não pode assumir. Fisicamente, o valor esperado corres­
ponde ao centro de gravidade da distribuição de probabilidades.
Algumas propriedades
Sendo c uma constante e X e Y variáveis aleatórias, as seguintes relações
podem ser comprovadas:
a) £(c) = c f)
II
o
b) E(X + c) = EVO + c g) VQC + c) = V(X)
c) E{cX) = cEQO h) V(cX) = c2VQ0
d) E(X + Y) = EQ0 + E m i) DP(cX) = \c\DPQO
e) EQC-Y) = EVO - E m
As relações (b) e (g) mostram que ao somar uma constante a uma variável
aleatória, a distribuição de probabilidades é deslocada por esta constante, mas
a variabilidade é preservada. Todavia, ao multiplicar a variável aleatória por
uma constante - relações (c) e (h) -, o centro da distribuição é deslocado na
mesma proporção e a variabilidade também é alterada (ver Figura 5.3).

VARIÁVEIS ALEATÓRIAS DISCRETAS 123
Distribuição de X
pOO
EVO
Figura 5.3 Efeito da soma e da multiplicação de uma constante sobre uma variá­
vel aleatória.
5.1.4 Variáveis aleatórias independentes
Considere que um dado seja lançado duas vezes, sob as mesmas condi­
ções. Seja Xi a variável aleatória que representa o número de pontos obtido no
i-ésimo lançamento (i = 1, 2). Supondo que o dado seja perfeitamente equili­
brado e o lançamento imparcial, então Xi e X2 têm a mesma função de probabi­
lidade, que é dada por:
PO) = Ve Ü = 1, 2, 3, 4, 5, 6)
Considere, também, a variável aleatória S como o número total de pontos
obtidos nos dois lançamentos, isto é,
S = Xl + X2
A função de probabilidade de S pode ser obtida com base em funções de
probabilidades de X: e X2 , resultando em:
2 3 4 5 6 7 8 9 10 11 12
S
p(s) 3 / w 3/
136 /36 36 436 % 6 36 % 6 436 36 236 136

1 24 ESTATÍSTICA
Note que, se o primeiro lançamento for realizado e ocorrer o resultado x if
sendo e {1, 2, 3, 4, 5, 6}, a função de probabilidade de X2 permanece a mes­
ma, pois o segundo lançamento independe do primeiro. Assim, podemos dizer
que Xi e X2 são variáveis aleatórias independentes.
No entanto, a função de probabilidade de S é alterada. Por exemplo, se
ocorrer o valor 1 (Xi = 1), então a distribuição de S passa a ser:
Possíveis valores de S dado que Xx = 1 2 3 4 5 6 7
Probabilidades
y6 % y6 / 6 y6 %
Já se ocorrer X} = 6, passamos a ter:
Possíveis valores de S dado que Xx = 6 7 8 9 10 ii 12
Probabilidades
y6 y6 y6 y6
y 6
Ou seja, Xi e S não são variáveis aleatórias independentes.
Em geral, X lf X2, Xn podem ser consideradas variáveis aleatórias inde­
pendentes se o conhecimento de uma não altera as distribuições de probabili­
dades das demais.
Muitas vezes as características do experimento permitem-nos avaliar se as
variáveis aleatórias envolvidas são independentes. Essa condição é importante,
pois a maioria dos métodos estatísticos é desenvolvida na suposição de que as
observações provêm de variáveis aleatórias independentes.
Considerando a regra do produto, podemos calcular a probabilidade de
sair número par nos dois lançamentos do dado simplesmente multiplicando a
probabilidade de sair par em cada lançamento, ou seja, (Vfc) . (Vfe) = lA. Pode­
mos representar o evento sair número par nos dois lançamentos do dado por:
{X, € (2, 4, 6), X2 G (2, 4, 6)}
E a probabilidade deste evento por:
P{X} e (2, 4, 6), X2 e (2, 4, 6)} = P{X1 e (2, 4, 6)} . P{X2 e (2, 4, 6)} =
= 1 1 - 1
2*2 4 '
Para um conjunto de variáveis aleatórias XXi X2, Xn, definimos:

VARIÁVEIS ALEATÓRIAS DISCRETAS 125
Xlf X2, ..., Xn são variáveis aleatórias independentes se e só se:
P{X1 e Elf X2 e E2, ..., Xn e E J = P(X1 e EJ . P (X2 e E2) . P(Xn e En)
para quaisquer conjuntos El} E2, ..., En.
Se X e Y são variáveis aleatórias independentes, então:
VÇX + Y) = VQO + VÇY) (5.6)
V(X - Y) = V(X) + V(Y) (5.7)
Note, por (5.7), que a variância da diferença de duas variáveis aleatórias
independentes é a soma das variâncias de cada variável aleatória. Isso decorre
da propriedade (h) (Seção 5.1.3).
EXERCÍCIOS
1. Apresente a função de probabilidade para as seguintes variáveis aleatórias:
a) Número de caras obtido com o lançamento de uma moeda honesta;
b) Número de caras obtido no lançamento de duas moedas honestas;
c) Número de peças com defeito em uma amostra de duas peças, sortea­
das aleatoriamente de um grande lote, em que 40% das peças são de­
feituosas;
d) Número de peças com defeito em uma amostra de três peças, sortea­
das aleatoriamente de um grande lote, em que 40% das peças são de­
feituosas.
2. Apresente, sob forma gráfica, a distribuição de probabilidades do Exercí­
cio 1 (d).
3. Apresente a função de probabilidade acumulada do Exercício l(d).
4. Calcule os valores esperados e as variâncias das distribuições de probabili­
dade do Exercício 1.
5. Considere que um produto pode estar perfeito (B), com defeito leve (DL)
ou com defeito grave (DG). Seja a seguinte distribuição do lucro (em R$),
por unidade vendida desse produto:
Produto X Pix)
B 6 0,7
DL 0 0,2
DG -2 0,1

1 26 ESTATÍSTICA
a) Calcule o valor esperado e a variância do lucro.
b)
Se, com a redução de desperdícios, foi possível aumentar uma unidade
no lucro de cada unidade do produto, qual é o novo valor esperado e a
variância do lucro por unidade?
c) E se o lucro duplicou, qual é o novo valor esperado e variância do lu­
cro por unidade?
6 . Certo tipo de conserva tem peso líquido médio de 900 g, com desvio pa­
drão de 10 g. A embalagem tem peso médio de 100 g, com desvio padrão
de 4 g. Suponha que o processo de enchimento das embalagens controla o
peso líquido, de tal forma que se possa supor independência entre o peso
líquido e o peso da embalagem. Qual é a média e o desvio padrão do peso
bruto?
5.2 PRINCIPAIS DISTRIBUIÇÕES DISCRETAS
Na seção anterior, construímos as distribuições de probabilidades de algu­
mas variáveis aleatórias, empregando nosso conhecimento para o cálculo das
probabilidades envolvidas. Nesta seção, estudaremos alguns modelos probabilís-
ticos padrões, que podem ser usados em diversas situações práticas. O problema
passa a ser, então, determinar qual modelo é o mais adequado para a situação
em estudo e como aplicá-lo adequadamente.
Lembremos que, para identificarmos uma variável aleatória discreta, te­
mos de conhecer quais resultados podem ocorrer e quais são as probabilidades
associadas aos resultados. A seguir, vamos ver os principais modelos discretos.
5.2.1 Distribuição de Bernoulli
Talvez os experimentos mais simples são aqueles em que observamos a
presença ou não de alguma característica, que são conhecidos como ensaios de
Bernoulli. Alguns exemplos:
a) lançar uma moeda e observar se ocorre cara ou não;
b) lançar um dado e observar se ocorre seis ou não;
c) numa linha de produção, observar se um item, tomado ao acaso, é
ou não defeituoso;
d) verificar se um servidor de uma intranet está ou não ativo.

VARIÁVEIS ALEATÓRIAS DISCRETAS 1 27
Denominamos sucesso e fracasso os dois eventos possíveis em cada caso.3
O ensaio de Bernoulli é caracterizado por uma variável aleatória X, definida
por X = 1, se sucesso; X = 0, se fracasso. A função de probabilidade de X (Dis­
tribuição de Bernoulli) é dada por
X P M
0 1 - p
1
P
Total 1
onde p = P{sucesso}. A distribuição fica completamente especificada ao
atribuirmos um valor para p. No exemplo (a), se o lançamento for imparcial e a
moeda perfeitamente equilibrada, p = V . Em (b), com suposição análoga, p = y6.
2
Outras características da distribuição de Bernoulli:
E(X) = p (5.8)
VOO = p .( l - p ) (5.9)
0 se x < 0
F(x) = < 1 - p se 0 < * < 1 (5.10)
1 se x > 1
5.2.2 Distribuição Binomial
Na maior parte das vezes, são realizados n ensaios de Bernoulli. O interes­
se está no número X de ocorrências de sucesso, como nos exemplos a seguir:
a) lançar uma moeda cinco vezes e observar o número de caras;
b) numa linha de produção, observar dez itens, tomados ao acaso, e
verificar quantos estão defeituosos;
c) verificar, num dado instante, o número de processadores ativos,
num sistema com multiprocessadores;
d) verificar o número de bits que não estão afetados por ruídos, em um
pacote com n bits.
Nos exemplos precedentes, se for possível supor:
• ensaios independentes;
• P{sucesso} = p, constante para todo ensaio (0 < p < 1).
3 No presente contexto, 0 termo sucesso não significa algo bom, mas simplesmente um
resultado ou evento no qual temos interesse; e fracasso, o outro resultado ou evento possível.

1 28 ESTATÍSTICA
Temos, então, exemplos de experimentos binomiais.
Uma variável aleatória com distribuição binomial de parâmetros n e p
pode ser apresentada por:
X = Xl + X2 + ... + Xn (5.11)
ondeXi, X2)..., Xn são variáveis aleatórias independentes, sendo cada uma delas
com distribuição de Bernoulli de parâmetro p. Como X, será 0 ou 1, dependen­
do da ocorrência ou não de sucesso no i-ésimo ensaio (i = 1, 2, ..., n), então a
soma X corresponderá ao número de sucessos. Para especificarmos a função de
probabilidade de X, considere o seguinte exemplo:
Exemplo 5.1 Uma indústria processadora de suco classifica os carregamentos
de laranja que chegam a suas instalações em A, B ou C. Suponha independência
entre as chegadas dos carregamentos, isto é, a classificação de um não altera a
classificação dos demais. Suponha também que a probabilidade p de classifica­
ção na classe A é a mesma para todos os carregamentos. Para os próximos 4
carregamentos, seja X a variável aleatória que representa o número de carrega­
mentos classificados na classe A. Vamos calcular a probabilidade de que X assu­
ma o valor x, isto é, a probabilidade de que x carregamentos sejam classificados
na classe A (x = 0, 1, 2, 3, 4).
Para cada carregamento, seja S (sucesso) quando este for classificado na
classe A; e seja F (fracasso) quando este for classificado em outra classe. A Figu­
ra 5.4 mostra todas as possíveis sequências de resultados, os possíveis valores
de X e as correspondentes probabilidades.
Resultados possíveis de 4 carregamentos:
SSFF
SFSF
SFFF SFFS SSSF
FSFF FSSF SSFS
FFSF FSFS SFSS
FFFF FFFS FFSS FSSS SSSS
Valores de X: 0 1 2 3 4
I I i i !
Probabilidades: (1 - p)4 4p(l - p)3 6p2(l - p)2 4p3(l - p) p4
Figura 5.4 Construção de uma distribuição binomial com n = 4 e p genérico.
Explicando as probabilidades da Figura 5.4. O evento X = 0 ocorre quando
nenhum carregamento é classificado na classe A (FFFF), cuja probabilidade é

VARIÁVEIS ALEATÓRIAS DISCRETAS 129
(1 - p)( 1 - p)( 1 - p )(l - p) = (1 - p)4. O evento X = 1 ocorre quando um car­
regamento for classificado na classe A (SFFF ou FSFF ou FFSF ou FFFS). Como
cada um desses resultados tem probabilidade p (l - p)3, a probabilidade do
evento X = 1 é igual a 4p(l - p)3. As outras probabilidades podem ser obtidas
de forma análoga.
Coeficientes binomiais
Na Figura 5.4, podemos observar que no cálculo da probabilidade do
evento X = 1, contamos de quantas maneiras poderia aparecer um sucesso en­
tre as quatro possibilidades, assim encontramos a quantidade quatro, corres­
pondente às seguintes sequências de respostas: SFFF, FSFF, FFSF e FFFS.
Em geral, na distribuição binomial, para calcular a probabilidade do even­
to X = x, onde x é um valor possível da variável aleatória X, precisamos conhe­
cer o número de maneiras em que podemos combinar os x sucessos entre os n
ensaios. Esse valor, conhecido como coeficiente binomial, entra no cálculo da
probabilidade como um coeficiente das potências de p e 1 - p, como verifica­
mos na Figura 5.4.
Vamos representar o número de combinações que podemos fazer com x
elementos, numa sequência de n elementos (sendo x < n), por n Esse núme-
ro de combinações pode ser calculado pela seguinte expressão:
(5.12)
onde n! = n(n - 1 )(n - 2)...l (lê-se nfatorial) e, por convenção, 0! = 1. Por
exemplo, para n = 4 temos os seguintes coeficientes binomiais:
'4' 4! 4! 4N 4! 4.3.2.1
x = 0: = 1 x = 3: = 4
4!.0! 4! 1!.3! 1.3.2.1
/
4! 4.3.2.1 4! 4!
x = 1: = 4 x = 4: = 1
/ 3 !.l! 3.2.1.1 0 !.4! 4!
4! 4.3.2.1
x = 2: = 6
2 1.2! 2.1.2.1
Expressão geral da distribuição binomial
SejaX uma variável aleatória com distribuição binomial de parâmetros n e
p (sendo 0 < p < 1). A probabilidade de X assumir um certo valor x, pertencente
ao conjunto {0, 1, 2,..., n}, é dada pela expressão:

1 30 ESTATÍSTICA
(5.13)
Exemplo 5.2 (continuação). Historicamente, 30% dos carregamentos são clas­
sificados na classe A, em que podemos supor que a probabilidade p de um car­
regamento ser classificado na classe A é 0,3. Entre os quatro próximos carrega­
mentos, calculemos a probabilidade de exatamente dois serem classificados na
classe A.
Temos n = 4 e p = 0,3. Assim, a probabilidade de x carregamentos serem
classificados na classe A é dada por:
P0c) = ^ . (0,3y . (0,7)4 -* (x = 0, 1, 2, 3, 4)
Em particular, p (2) = ,* . (0,3)2 . (0,7)4"2 = 6 . (0,09). (0,49) = 0,2646
A Tabela 1 do apêndice apresenta probabilidades da binomial para n < 15
e p múltiplo de 0,05. O Exemplo 5.3 ilustra o uso da tabela.
Exemplo 5.2 Dados históricos mostram que 70% das pessoas que acessam a
página p23 da internet também acessam a página p24. Obteremos, através da
tabela da distribuição binomial, a probabilidade de que, nos dez próximos aces­
sos à p23, a maioria também acesse a p24.
Note que temos um experimento binomial, com
Parte da Tabela 1
n = 10 e p = 0,7 (supondo independência entre os aces­
P
sos). Usando a Tabela da distribuição binomial, podemos
especificar a distribuição de X = número de pessoas que n X 0,70
também acessam a p24. A probabilidade de ocorrer o
10 0 0,0000
evento a maioria também acessar a p24 corresponde, em 1 0,0001
termos da variável aleatória X, ao evento {X > 5}, como 2 0,0014
ilustramos ao lado. A probabilidade deste evento será a 3 0,0090
4 0,0368
soma dos resultados individuais, ou seja:
5 0,1029
PCX > 5) = 0,2001
6
7 0,2668
= p( 6) + p(7) + p(8) + p(9) + p(lO) =
x > 5 8 0,2335
= 0,2001 + 0,2668 + 0,2335 + 0,1211 + 0,0282 =
9 0,1211
= 0,8497. 110 0,0282
Se X tem distribuição binomial de parâmetros n e p , então seu valor espera­
do e sua variância podem ser calculados por:

VARIÁVEIS ALEATÓRIAS DISCRETAS 131
E m = n.p (5.14)
VÍX) = n.p. (1 - p) (5.15)
A Figura 5.5 mostra duas distribuições binomiais com a indicação da posi­
ção dos respectivos valores esperados.
binomial com n = 5 e p = 0,5 binomial com n = 5 e p = 0,25
EQO = 2,5 E(X) = 1,25
Figura 5.5 Representações gráficas de distribuições binomiais.
Distribuições binomiais com p = 0,5 são simétricas, mas são assimétricas
quando p * 0,5. A assimetria aumenta à medida que p aproxima-se de zero (as­
simetria positiva) ou de um (assimetria negativa).
EXERCÍCIOS
7. Dados históricos mostram que 5% dos itens provindos de um fornecedor
apresentam algum tipo de defeito. Considerando um lote com 20 itens, cal­
cular a probabilidade de:
a) haver algum item com defeito;
b) haver exatamente dois itens defeituosos;
c) haver mais de dois itens defeituosos;
d) qual é o número esperado de itens defeituosos no lote?
e) e de itens bons?
.
8 Apresente o gráfico da variável aleatória do Exemplo 5.2 sob a forma de
um histograma, indique a posição do valor esperado e represente P(X > 5)
como uma área na figura.

1 32 ESTATÍSTICA
5.2.3 Distribuição hipergeométrica
Considere o problema básico de inspeção por amostragem, em que obser­
vamos uma amostra de n itens de um lote com N itens, sendo r defeituosos.
Avaliamos o número X de itens defeituosos na amostra. A variável aleatória X
aparenta ser binomial, mas só é realmente binomial se:
• a seleção da amostra for aleatória (para garantir a mesma probabili­
dade p de sair item defeituoso em todos os ensaios);
• com reposição (para garantir independência entre os ensaios).
A segunda condição não costuma ser satisfeita na prática. Se a amostra­
gem for aleatória, mas sem reposição, a distribuição de X é conhecida como hi­
pergeométrica de parâmetros N, n e r (ver Figura 5.6).
Amostra com n itens
Lote com N itens:
{r defeituosos Distribuição
N -r bons Amostragem aleatória binomial
$
com reposição
Amostra com n itens
Distribuição
hipergeométrica
Amostragem aleatória
sem reposição
Figura 5.6 Caso típico de inspeção por amostragem. Variável aleatória em estu­
do: X = número de defeituosos na amostra.
A função de probabilidade de X é expressa por:
' N - r '|
^ n - x j
t )
p(x) = [x = 0, 1, ..., min(r, n)] (5.16)
1
com valor esperado e variância dados por:
E(X) = n.p (5.17)
N - n
VOO = n.p.( 1 - p) . (5.18)
N -1

VARIÁVEIS ALEATÓRIAS DISCRETAS 133
Exemplo 5.3 Placas de vídeo são expedidas em lotes de 30 unidades. Antes
que a remessa seja aprovada, um inspetor escolhe aleatoriamente cinco placas
do lote e as inspeciona. Se nenhuma das placas inspecionadas for defeituosa, o
lote é aprovado. Se uma ou mais forem defeituosas, todo o lote é inspecionado.
Supondo que haja três placas defeituosas no lote, qual é a probabilidade de que
o controle da qualidade aponte para a inspeção total?
Seja X o número de placas defeituosas na amostra. Desejamos calcular:
PCX > í) = i - P(x = o)
Usando o modelo hipergeométrico:
(30 -3^1
í 3^
pC 0) =
• IU 1
o
80.730
/
_ = 0,5665
^30^ 142.506
5
Logo, PCX > 1) = 1 - 0,5665 = 0,4335.
É importante ressaltar que quando N é muito maior do que n, a distribui­
ção hipergeométrica pode ser aproximada pela binomial. Muitos autores pres­
crevem uma relação yN < 0,05 para que seja possível fazer a aproximação.4 Nes­
se caso, a binomial tem parâmetros n = tamanho da amostra e p = r/ ^ .
EXERCÍCIOS
9. Qual é a probabilidade do Exemplo 5.3, se a inspeção completa for feita so­
mente quando forem encontradas mais do que uma placa defeituosa na
amostra?
10. Calcule o valor esperado e a variância da variável aleatória definida no
Exemplo 5.3.
5.2.4 Distribuição de Poisson
Considere as situações em que se avalia o número de ocorrências de um
tipo de evento por unidade de tempo, de comprimento, de área, ou de volume.
Por exemplo:
4 Observe que se N for muito maior que n, as retiradas, mesmo feitas sem reposição, não
irão modificar em demasia as probabilidades condicionais de ocorrências de sucessos (e de fracas­
sos), na sequência de ensaios.

1 34 ESTATÍSTICA
a) número de consultas a uma base de dados em um minuto;
b) número de pedidos a um servidor num intervalo de tempo;
c) número de erros de tipografia em um formulário;
d) número de defeitos em um m2 de piso cerâmico;
e) número de pulsações radioativas em um intervalo de tempo, na de­
sintegração dos núcleos de uma substância radioativa.
Suposições básicas:
• independência entre as ocorrências do evento considerado;
• os eventos ocorrem de forma aleatória, de tal forma que não haja ten­
dência de aumentar ou reduzir as ocorrências do evento, no intervalo
considerado.
Para desenvolvermos a distribuição de Poisson, consideremos a variável
aleatória X = número de consultas a uma base de dados em um minuto. Ou seja,
X é a contagem de ocorrências de consultas no intervalo de tempo [0, 1), como
representado a seguir:
ocorrências do evento
-x— x--------------------------*--------►
0 1 t
Considere o intervalo [0, 1) particionado em n subintervalos de amplitude
yn:
At =
0 1 t
Seja n suficientemente grande para que a probabilidade de ocorrer duas
ou mais consultas, em cada subintervalo de amplitude At, seja desprezível.
Assim, considere que em cada subintervalo só possa ocorrer 0 ou 1 consulta.
Sendo p a probabilidade de ocorrer uma consulta em At, as probabilidades as­
sociadas a X podem ser calculadas, aproximadamente, pela binomial (Expressão
5.13). Então,
p(x) = P(X = x) » ^ . px . (1 - p)n- x, x = 0, 1, ..., n (5.19)
Mas quando n oc e p -» 0, de tal sorte que o valor esperado EQQ = n.p X,
sendo X > 0, é possível mostrar que:

VARIÁVEIS ALEATÓRIAS DISCRETAS 135
\
(5.20)
n->oc
/ p->0 x\
Então, sendo X a taxa média de consultas por unidade de tempo, as proba­
bilidades de X podem ser calculadas pela chamada distribuição de Poisson, cuja
função de probabilidade é dada por:
p(x) = -— x = 0, 1, 2, ... (5.21)
x\
sendo:
EQO = VOO = A, (5.22)
Exemplo 5.4 Supondo que as consultas num banco de dados ocorrem de for­
ma independente e aleatória, com uma taxa média de três consultas por minu­
to, calculemos a probabilidade de que no próximo minuto ocorram menos do
que três consultas.
Seja X o número de consultas por minuto. Então:
e ^3ü e *3~ e 33 2
PCX < 3) = pC0) + pC 1) + pC2) = = 0,4232
0! 1! 2 !
A Tabela 2 do apêndice apresenta as probabilidades acumuladas da Poisson,
isto é:
(5.23)
No Exemplo 5.4, usando a Tabela 2, temos:
PCX < 3) = PCX < 2) = F(2) = 0,4232
Exemplo 5.4 (continuação) Calculemos a probabilidade de que nos próximos
dois minutos ocorram mais do que 5 consultas.
Observe que a unidade de tempo alterou de um para dois minutos. Mas se
a taxa média é de três ocorrências por minuto, então, em dois minutos, a taxa
média é de seis ocorrências. Logo, no presente problema, X = 6 e
PCX > 5) = 1 - PCX < 5) = 1 - F(5) = 1 - 0,4457 = 0,5543

1 36 ESTATÍSTICA
Aproximação da binomial pela Poisson
Justificamos a distribuição de Poisson a partir da binomial, fazendo n -» oc
e p -» 0 (Expressão 5.20). Logo, em experimentos binomiais, quando n for mui­
to grande e p for muito pequeno, podemos usar a distribuição de Poisson com:
X = n.p (5.24)
Observe que se n for grande (acima de 100, por exemplo) as combinações
da binomial ficam difíceis de serem calculadas. Nesse caso, o uso da aproxima­
ção Poisson torna-se imprescindível.
Exemplo 5.5 Seja uma linha de produção em que a taxa de itens defeituosos
é de 0,5%. Calculemos a probabilidade de ocorrer mais do que quatro defeituo­
sos, em uma amostra de 500 itens.
X = n.p = (500) . (0,005) = 2,5
P{X > 4) = 1 - PQC < 4) = 1 - F(4) = 1 - 0,8912 = 0,1088
EXERCÍCIOS
11. Mensagens chegam a um servidor de acordo com uma distribuição de
Poisson, com taxa média de cinco chegadas por minuto.
a) Qual é a probabilidade de que duas chegadas ocorram em um minuto?
b) Qual é a probabilidade de que uma chegada ocorra em 30 segundos?
12. Em um canal de comunicação digital, a probabilidade de se receber um bit
com erro é de 0,0002. Se 10.000 bits forem transmitidos por esse canal,
qual é a probabilidade de que mais de quatro bits sejam recebidos com
erro?
EXERCÍCIOS COMPLEMENTARES
13. Um armazém é abastecido mensalmente, sendo que a taxa média de abas­
tecimento é 30 unidades/dia, com desvio padrão de 3 unidades/dia. A de­
manda média é de 25 unidades/dia, com desvio padrão de 4 unidades/dia.
Suponha que o abastecimento e a demanda sejam independentes e, além
disso, a demanda e o abastecimento num dia não alteram o abastecimento
e a demanda nos dias seguintes. Qual é o valor esperado e o desvio padrão
do excedente de produtos, no período de um mês?

VARIÁVEIS ALEATÓRIAS DISCRETAS 1 3 7
14. Suponha que 10% dos clientes que compram a crédito em uma loja deixam
de pagar regularmente suas contas (prestações). Se num particular dia, a
loja vende a crédito para 10 pessoas, qual é a probabilidade de que mais de
20% delas deixem de pagar regularmente as contas? Suponha que as 10
pessoas que fizeram crediário nesse dia correspondam a uma amostra alea­
tória de clientes potenciais desta loja.
15. Em um sistema de transmissão de dados, existe uma probabilidade igual a
0,05 de um lote de dados ser transmitido erroneamente. Foram transmiti­
dos 20 lotes de dados para a realização de um teste de análise da confiabi­
lidade do sistema.
a) Qual é o modelo teórico mais adequado para esse caso? Por quê?
b) Calcule a probabilidade de haver erro na transmissão.
c) Calcule a probabilidade de que haja erro na transmissão em exatamen­
te 2 dos 20 lotes de dados.
d) Qual é o número esperado de erros no teste realizado?
16. Numa fábrica, 3% dos artigos produzidos são defeituosos. O fabricante
pretende vender 4000 peças e recebeu 2 propostas:
Proposta 1: o comprador A propõe examinar uma amostra de 80 peças.
Se houver 3 ou menos defeituosas, ele paga 60 unidades monetárias (u.m.)
por peça; caso contrário, ele paga 30 u.m. por peça.
Proposta 2: o comprador B propõe examinar 40 peças. Se todas forem
perfeitas, ele está disposto a pagar 65 u.m. por peça; caso contrário, ele
paga 20 u.m. por peça.
Qual é a melhor proposta? (Calcule o valor esperado da venda em
cada proposta.)
17. O departamento de qualidade de uma empresa seleciona, aleatoriamente,
alguns itens que chegam à empresa e submete-os a testes. Para avaliar um
lote de transformadores de pequeno porte, o departamento de qualidade
selecionou, aleatoriamente, 10 transformadores. Ele vai recomendar a acei­
tação do lote se não existir item defeituoso na amostra. Supondo que o
processo produtivo desses transformadores gera um percentual de 3% de
defeituosos, responda:
a) Qual é a probabilidade de que o lote venha a ser aceito?
b) Ao analisar 8 lotes de transformadores, com amostras aleatórias de 10
itens em cada lote, qual é a probabilidade de que, no máximo, um lote
seja rejeitado?
18. Na comunicação entre servidores, uma mensagem é dividida em n pacotes,
os quais são enviados em forma de códigos. Pelo histórico da rede, sabe-se

1 38 ESTATÍSTICA
que cada pacote tem uma pequena probabilidade, igual a 0,01, de não
chegar corretamente a seu destino e, além disso, o fato de um pacote
não chegar ao destino não altera a probabilidade dos demais chegarem
corretamente. Um programa corretivo garante o envio correto da mensa­
gem quando o número de pacotes enviados erroneamente não passar de
10% do total de pacotes da mensagem. Qual é a probabilidade de uma
mensagem composta de 20 pacotes ser enviada corretamente? Responder
usando:
a) a distribuição binomial;
b) a distribuição de Poisson.
19. Uma central telefônica recebe, em média, 300 chamadas na hora de maior
movimento, e pode processar, no máximo, 10 ligações por minuto. Utili­
zando a distribuição de Poisson, calcular a probabilidade de que a capaci­
dade da mesa seja ultrapassada em dado minuto do horário de pico.
20. Um piso cerâmico tem, em média, 0,01 defeito por m2. Em uma área de
10 m x 10 m desse piso, calcule a probabilidade de ocorrer algum defeito.
21. Placas de circuito integrado são avaliadas após serem preenchidas com
chips semicondutores. Considere que foi produzido um lote de 20 placas e
selecionadas 5 para avaliação. Calcule a probabilidade de encontrar pelo
menos uma placa defeituosa, supondo que o lote tenha 4 defeituosas e que
tenha sido realizada:
a) uma amostragem aleatória com reposição;
b) uma amostragem aleatória sem reposição.
22. Suponha que o número de falhas em certo tipo de placa plástica tenha dis­
tribuição de Poisson, com taxa média de 0,05 defeito por m2. Na constru­
ção de um barco, é necessário cobrir uma superfície de 3 m x 2 m com essa
placa.
a) Qual é a probabilidade de que não haja falhas nessa superfície?
b) Qual é a probabilidade de que haja mais que uma falha nessa super­
fície?
c) Na construção de 5 barcos, qual é a probabilidade de que pelo menos 4
não apresentem defeito na superfície plástica?
23. Um item é vendido em lotes de 200 unidades. Normalmente o processo de
fabricação gera 5% de itens defeituosos. Um comprador compra cada lote
por RS 100,00 (alternativa 1). Um outro comprador faz a seguinte propos­
ta: de cada lote, ele escolhe uma amostra de 15 peças; se a amostra tem 0
defeituoso, ele paga RS 200,00; 1 defeituoso, ele paga RS 50,00; mais que
1 defeituoso, ele paga R$ 5,00 (alternativa 2). Em média, qual alternativa

VARIÁVEIS ALEATÓRIAS DISCRETAS 1 3 9
é mais vantajosa para o fabricante? (Calcule os valores esperados das duas
alternativas.)
24. Na produção de rolhas de cortiça, não é possível garantir qualidade homo­
gênea, devido às variações internas nas placas de cortiça. Em função disso,
um equipamento separa as rolhas que saem da linha de produção em duas
categorias: A e B. Os dados históricos mostram que 40% são classificadas
como A e 60% como B. O fabricante vende por RS 100,00 o milhar de ro­
lhas da categoria A; e por RS 60,00 o milhar da categoria B.
Um comprador propõe comprar a produção diária da fábrica. Ele fará
um plano de amostragem, extraindo 8 rolhas aleatoriamente. Se encontrar
mais que 5 rolhas da categoria A, ele paga R$ 200,00; caso contrário, ele
paga RS 50,00. Pede-se:
a) Qual é a probabilidade do comprador encontrar mais que 5 rolhas da
classe A?
b) Qual é o valor esperado da venda do fabricante, por milhar de rolhas
vendidas, se ele aceitar a proposta do comprador? Em termos do valor
esperado da venda, a proposta do comprador é mais vantajosa do que
a venda separada por categoria?
c) Qual é a variância da venda do fabricante, por milhar de rolhas vendi­
das, se ele aceitar a proposta do comprador?
25. Suponha que as requisições a um sistema ocorram de forma independente
e que a taxa média de ocorrências é três requisições por minuto, constante
no período em estudo. Calcule a probabilidade de:
a) ocorrer mais que uma requisição no próximo minuto;
b) ocorrer mais que uma requisição no próximo minuto, sabendo-se que é
certa a ocorrência de pelo menos uma (pois, você mesmo fará uma re­
quisição no próximo minuto).

6
Variáveis Aleatórias Contínuas
6.1 CARACTERIZAÇÃO DE UMA VARIÁVEL ALEATÓRIA
CONTÍNUA
Muitas variáveis aleatórias que surgem na vida de um engenheiro ou de
um profissional da informática têm natureza eminentemente contínua, tais
como:
• tempo de resposta de um sistema computacional;
• rendimento de um processo químico;
• tempo de vida de um componente eletrônico;
• resistência de um material etc.
Outras vezes, há variáveis aleatórias discretas, com grande número de pos­
síveis resultados, em que é preferível usar um modelo aproximado contínuo no
lugar do modelo exato discreto. É o caso de:
• número de transações por segundo de uma CPU;
• número de defeitos numa amostra de 5.000 itens etc.
Para entender as peculiaridades das variáveis aleatórias contínuas, imagi­
ne o seguinte experimento.

VARIÁVEIS ALEATÓRIAS CONTÍNUAS 141
Exemplo 6.1a Um círculo é dividido em dois setores de mes­
mo tamanho (180° cada um), aos quais são atribuídos os nú­
meros 1 e 2. Um ponteiro é preso ao centro do círculo e gira­
do, conforme mostra a figura ao lado. Seja a variável aleatória
discreta X = número do setor apontado quando o ponteiro pára
de girar. A distribuição de probabilidades de X, considerando
que todos os pontos sejam equiprováveis, pode ser especificada
pela função de probabilidade da Figura 6.1.
i
PC*)
P M i ‘ /(*)
X
i
v2 » 1
%
1
1/2 área total 1
=
Vi
2
Total -----------► ------►
1
Figura 6.1 Três formas de apresentação da função de probabilidade do experi­
mento aleatório do Exemplo 6.1a.
A representação com gráfico de hastes é típica para variáveis discretas.
Apresentamos, também, um gráfico em forma de histograma, em que as proba­
bilidades podem ser representadas por área. No caso do exemplo em questão,
as bases dos retângulos são iguais à unidade, o que faz com que a área seja
igual à altura do retângulo.1
Exemplo 6.1b Considere, agora, o círculo dividido em quatro setores de mes­
mo tamanho (90° cada um). A distribuição de probabilidades da variável alea­
tória discreta X = número do setor apontado quando o ponteiro pára de girar é
apresentada na Figura 6.2.
j
rea to ai = 1
Figura 6.2 Representação gráfica da função de probabilidade do experimento
aleatório do Exemplo 6.1b.
1 Ao representarmos probabilidades por áreas, devemos tomar o cuidado para que a
área total seja igual à unidade.

1 42 ESTATÍSTICA
Exemplo 6.1c Imagine que o círculo seja dividido em 8, 16 e 32 setores. A Fi­
gura 6.3 mostra a função de probabilidade de X em cada caso.
m 16 setores
m 32 setores
16
32
8 16 16 32
Figura 6.3 Representações gráficas das funções de probabilidade dos experimen­
tos aleatórios do Exemplo 6.1c.
É fácil verificar que à medida que aumentamos o número de divisões no
círculo, o número de possíveis setores (resultados de uma variável aleatória dis­
creta) vai aumentando, e a probabilidade de cada resultado ocorrer (represen­
tada pela área de um retângulo) vai sendo reduzida. Teoricamente, o círculo
pode ser dividido em infinitos setores, o que toma inviável a representação ta­
bular ou gráfica da distribuição de probabilidades, da forma como fizemos no
Exemplo 6.1. Em termos matemáticos, teríamos:
P(x) = P(X = x) = lim i = 0, Vx = 1, 2, ... (6.1)
n->x> Yi
Uma alternativa melhor é definir uma variável aleatória contínua, como
veremos na seção seguinte.
6.1.1 Função densidade de probabilidade
Exemplo 6.2 Considere um círculo, com medidas de ângulos, em graus, a
partir de determinada origem, como mostra a figura ao lado. Nesse círculo, há
um ponteiro que é colocado a girar.

VARIÁVEIS ALEATÓRIAS CONTÍNUAS 143
Seja a variável aleatória contínua X = ângulo formado entre a posição que o
ponteiro pára e a linha horizontal do lado direito. Considerando que não existe
região de preferência para o ponteiro parar, a distribui­
90
ção de probabilidade de X pode ser representada por
uma função que assume um valor constante e positivo
em todo o intervalo [0o, 360°), de tal forma que as pro­
0
babilidades possam ser representadas por áreas sob a 180
curva dessa função. Como certamente vai ocorrer um re­
sultado em [0o, 360°), então a área sob a função neste
intervalo deve ser igual a 1, e nula fora deste intervalo. 270
A Figura 6.4 ilustra a distribuição de probabilidades de
X, através da chamada função densidade de probabilidade, e mostra a relação en­
tre uma área e um evento.
(a) (b)
i ‘ m
área = P(0<X< 90)
£
0
360 360
—----------------A . ►
90 360
evento {0 < X < 90}
Figura 6.4 (a) Função densidade de probabilidade da variável aleatória do
Exemplo 6.2; e (b) Probabilidade do evento {0 < X < 90}, represen­
tada por uma área.
Note que os eventos associados a uma variá­
vel aleatória contínua são intervalos (ou coleção de
intervalos) dos números reais. Com base na função
densidade de probabilidade, podemos calcular pro- 300
babilidades de eventos desse tipo. Por exemplo,
qual é a probabilidade do ponteiro parar no inter­
valo [30°, 60°]? Tomando a área do retângulo in­
dicado na figura ao lado, temos:
30
P(30 < X < 60) = (6 0 -3 0 ) =
360 360 12
Observe que a inclusão ou exclusão dos extremos não altera a probabilida­
de, pois uma linha tem área nula. Ou seja, para uma variável aleatória contí­
nua, a probabilidade de ocorrer um particular valor é igual a zero.

1 44 ESTATÍSTICA
As probabilidades de eventos associados a uma variável aleatória contínua
X podem ser calculadas através de uma função densidade de probabilida­
de f que deve satisfazer:
k/(x)
a) f(x) > 0, Vx e <R e _
b) J /(x )d x = 1
Se A = [a, b], então P(A) = f fM d x b x
i
Jü
Exemplo 6.3 Seja a variável aleatória T definida como o tempo de resposta
na consulta a um banco de dados, em minutos. Suponha que essa variável alea­
tória tenha a seguinte função densidade de probabilidade:
2e‘2c, para t > 0
m =
0, para t < 0
Vamos calcular a probabilidade de a resposta
demorar mais do que 3 minutos, isto é, P(T > 3).
P(T > 3) = r f(t)dt = r 2e~2'dt = 2 - - e 211 = 0 + e -2(3) = e 6
3 3 L 2 J 3
6.1.2 Função de distribuição acumulada
Como X é uma variável aleatória contínua com função de densidade de
probabilidade /, definimos sua função de distribuição acumulada por:
(6.2)
Considere a função densidade de probabilidade do Exemplo 6.3:
2e'2t, para t > 0
m =
0, para t < 0
Vamos obter a função de distribuição acumulada. Como a expressão mate­
mática se altera no ponto zero, devemos considerar os dois seguintes casos:
para t < 0,
F(t) = f /(s)ds = fo ds = 0
J-30 J-CC

VARIÁVEIS ALEATÓRIAS CONTÍNUAS 145
e para t > 0,
F(t) = J! /(s)ds = J° 0ds + j^2e'2sds = 0 + [~e_25] o = 1 - e~2í
Resumindo, a função de distribuição acumulada da variável aleatória T é
dada por:
prt) = II -e " 2t, para t > 0
0, para t < 0
Cabe observar que é possível obter qualquer probabilidade através da fun­
ção de distribuição acumulada. Para a < b, temos:
P(X < a) = P(X < a) = F(a) (6.3)
PCX > b) = 1 - F(ò) (6.4)
PCa < X < b) = FCb) - FCa) (6.5)
Retomando o Exemplo 6.3, o cálculo de P(T > 3) pode ser feito aplican­
do (6.4):
P(T > 3) = 1 - P(T < 3) = 1 - F(3) = 1 - [1 - e"2(3)] = e~6
Dada a função de distribuição acumulada F, podemos obter a função den­
sidade de probabilidade / por:
/0 0 = f-F O O (6.6)
dx
para todo ponto x em que F é derivável.2 Assim, a função F também caracteriza
a distribuição de probabilidades de uma variável aleatória.
6.1.3 Valor esperado e variância
Uma variável aleatória contínua X, com função densidade de probabilida­
de /, tem valor esperado e variância definidos por:
|i = £(X) = f xf(x)dx (6.7)
J-ao
a 2 = VOO = f Xx - n)7 U )d x (6.8)
J-ao
2 No conjunto finito de pontos em que F não é derivável, podemos arbitrar valores para/.

1 46 ESTATÍSTICA
As interpretações dessas medidas podem ser feitas de forma análoga ao
caso discreto. Além disso, todas as propriedades enunciadas para o caso discre­
to continuam válidas para o caso contínuo, em especial
VOO = EQP) - n2 (6.9)
onde: EÇX2) = J x 2f(x)d x
Retomando o Exemplo 6.3, em que a variável aleatória T era caracteriza­
da por
= Í2e“2t, para t > 0
(0, para t < 0
temos: [i = E(T) = J tf(t)dt = J tOdt + £ t2e~2ldt = 0 + 2£ te'2ldt
Integrando £ t2e 21 dt por partes, obtemos jí = V .
2
Temos, também,
EÇT2) = J t 2/(t)dt = J t20dt+Jo t 22e~2ldt = 0 + 2£ t 22e~2ídt
Com certo esforço matemático, obtemos EÇT2) = V . Então:
2
\2
1 1
02 = V(T) = EiT2) - n2 = - -
2 u / 4
EXERCÍCIOS
1. Seja um ponto escolhido aleatoriamente no intervalo [0, 1].
a) Apresente uma função densidade de probabilidade para este experi­
mento.
b) Obtenha a função de distribuição acumulada.
c) Calcule o valor esperado e a variância.
2. Um profissional de Computação observou que seu sistema gasta entre 20 e
24 segundos para realizar determinada tarefa. Considere a probabilidade
uniforme em [20, 24], isto é, todo subintervalo de mesma amplitude em

VARIÁVEIS ALEATÓRIAS CONTÍNUAS 1 47
[20, 24] tem a mesma probabilidade. Como pode ser descrita, gráfica e al-
gebricamente, a função densidade de probabilidade? Sob essa densidade,
calcule:
a) P(X > 23);
b) EQ0;
c) VCX).
Com respeito ao exercício anterior, mas supondo probabilidades maiores
em tomo de 22 segundos e a densidade decrescendo, simétrica e linear­
mente, até os extremos 20 e 24 segundos. Como pode ser descrita, gráfica
e algebricamente, a função densidade de probabilidade? Sob essa densida­
de, calcule:
a) P(X > 23);
b) EQ0;
c) V(X).
Comparando os gráficos das funções de densidade de probabilidade
dos dois exercícios, você acha razoáveis as diferenças encontradas nos três
itens?
Seja X uma variável aleatória com função de distribuição acumulada
F M = í l - e " , para x > 0
0, para x < 0
Obtenha a função densidade de probabilidade de X.
Seja X com função densidade de probabilidade dada por
x, para 0 < x < 1
fÇx) = <2 - x, para 1 < x < 2
0, para x<£ [0,2)
Calcule:
a) P(0 < X < 5) b) P(0 < X < 1) c) PCV3 < X < 3/ 2)
d) E(X) e) V00
PRINCIPAIS MODELOS CONTÍNUOS
2
Nesta seção serão descritos três modelos contínuos bastante conhecidos.

1 48 ESTATÍSTICA
6.2.1 Distribuição uniforme
Relembremos o Exemplo 6.2, onde tínhamos um cír­
culo e um ponteiro que era colocado a girar. A variável
90°
aleatória de interesse eraX = ângulo formado entre a posi­
ção que o ponteiro pára e a linha horizontal do lado direito.
Supôs-se, também, não existir região de preferência para o 180° 0o
ponteiro parar. Nessas codições, podemos considerar que
todo intervalo de mesma amplitude, contido em [0o, 360°),
tem a mesma probabilidade de ocorrência. É um experi­ 270°
mento típico em que a chamada distribuição uniforme é apropriada.
Uma variável aleatória X tem distribuição uniforme de parâmetros a e p,
sendo p > a, se sua densidade é especificada por:
—-— , para x e [a, p]
f M = ■p - a
0, para x e [a, p] (6.10)
Em consequência, sua distribuição acumulada é dada por (ver Figura 6.5):
0, para x < a
x - a
F M = para a < x < p (6.11)
P - a
1, para x > p
f M iHx)
1 1
P - a
-----------4--- W
0 a p x o a 3
Figura 6.5 Representação gráfica da função densidade de probabilidade e da fun­
ção de distribuição acumulada de uma variável aleatória com dis­
tribuição uniforme em [a, pj.
O valor esperado e a variância de uma distribuição uniforme são:
(6.12)
(6.13)

VARIÁVEIS ALEATÓRIAS CONTÍNUAS 149
Note que o valor esperado da distribuição uniforme é exatamente o ponto
médio do intervalo [a, p], ou seja, nessa distribuição fica evidente que [x repre­
senta o centro de gravidade da massa descrita pela função densidade de proba­
bilidade.
6.2.2 Distribuição exponencial
O modelo exponencial tem forte relação com o modelo discreto de Poisson.
Enquanto a distribuição de Poisson pode ser usada para modelar o número de
ocorrências em um período contínuo (de tempo ou de comprimento), a distribui­
ção exponencial pode modelar a variável aleatória contínua que representa o
intervalo (de tempo ou de comprimento) entre as ocorrências. Exemplos:
a) tempo (em minutos) até a próxima consulta a uma base de dados;
b) tempo (em segundos) entre pedidos a um servidor;
c) distância (em metros) entre defeitos de uma fita.
A distribuição exponencial pode ser usada quando as suposições de Poisson
(independência entre as ocorrências e taxa média de ocorrência constante no
intervalo considerado) estiverem satisfeitas. A Figura 6.6 ilustra a relação entre
as duas distribuições.
Figura 6.6 Relação entre a distribuição de Poisson e a exponencial.
Para chegarmos à formulação matemática da distribuição exponencial, va­
mos considerar a equivalência entre os dois seguintes eventos:
A primeira ocorrência Nenhuma ocorrência
C >>
ser depois do tempo t em [0, t)

1 50 ESTATÍSTICA
Sejam as variáveis aleatórias:
Xt = número de ocorrências no intervalo de tempo [0, t); e
T = tempo entre as ocorrências.
Sendo X a taxa média de ocorrências por unidade de tempo, então, consi­
derando independência entre as ocorrências, Xt tem distribuição de Poisson
com parâmetro At. E a equivalência entre os dois eventos pode ser expressa por:
T > t <C= O Xt = 0
Logo,
0
_-x*
(* )
-fj.
P(T > t) = P(Xf =_ 0) _ = e
aplicação da expressão de Poisson
Usando o evento complementar, podemos definir para todo t > 0 a função
de distribuição acumulada de uma variável aleatória T com distribuição expo­
nencial:
F{t) = P(T < t) = 1 - ér* (6.14)
Em consequência, para t > 0 temos a função densidade de probabilidade
dada por:
(6.15)
Para t < 0, definimos F(t) = /(t) = 0 (ver a Figura 6.7).
Figura 6.7 Representação gráfica da função densidade de probabilidade de uma
variável aleatória com distribuição exponencial.

VARIÁVEIS ALEATÓRIAS CONTÍNUAS 151
Em geral, é mais fácil partir do complemento de F(t) para calcular as pro­
babilidades, ou seja, para t > 0,
P(T > t) = er* (6.16)
E xem plo 6.3 (co n tin u ação ) Dada a variável aleatória T = tempo de
resposta na consulta a um banco de dados (em minutos) com função densidade
de probabilidade
2e 2í para t > 0
m =
0, para t < 0
ou seja, uma exponencial com À= 2, calcular a probabilidade da consulta de­
morar mais que 3 minutos, isto é, PÇT > 3). Podemos partir da função de densi­
dade, fazendo:
-*OC
■f»
P(T > 3) = J f(t)dt = J 2e-2,dt = e'6
Ou podemos usar (6.16), obtendo:
P(T > 3) = e-2(3) = e-6
Considere, agora, o cálculo da probabilidade
P( 2 <T < 3), isto é, a próxima consulta ocorrer no inter­
valo de 2 a 3 minutos. Podemos fazer
P(2 < T< 3) = j2e"2tdt
ou usar (6.5):
P(2 < T < 3) = P(T > 2) - PCT > 3) = e"2(2) - e"2(3) = e“4 - e"6
= 0,0158
Para uma variável aleatória T, com distribuição exponencial de parâmetro
X, temos:
(6.17)
(6.18)

1 52 ESTATÍSTICA
Um exemplo do cálculo do valor esperado e da variância de uma exponen­
cial foi feito na Seção 6.1.3. Observe que podemos obter os mesmos resultados
com (6.17) e (6.18).
EXERCÍCIOS
6. O tempo de vida (em horas) de um transistor é uma variável aleatória T
com distribuição exponencial. O tempo médio de vida do transistor é de
500 horas.
a) Calcule a probabilidade de o transistor durar mais do que 500 horas.
b)
Calcule a probabilidade de o transistor durar entre 300 e 1000 horas.
c) Sabendo-se que o transistor já durou 500 horas, calcule a probabilida­
de de ele durar mais 500 horas.
7. Usando a expressão de probabilidade condicional (Capítulo 4), mostrar que
para s, t > 0, vale a seguinte relação para uma variável aleatória T expo­
nencial:
P(T > s + t\T > s) = P(T > t)
Essa propriedade é conhecida como “falta de memória”, pois não im­
porta o que aconteceu no passado (T < s), mas apenas a partir do momento
em que se inicia a observação, que pode ser considerado como o instante
zero. Nesse contexto, a distribuição exponencial é inadequada para repre­
sentar “tempo de vida” de itens que sofrem efeito de fadiga.
6.2.3 Distribuição normal
A normal é considerada a distribuição de probabilidades mais importante,
pois permite modelar uma infinidade de fenômenos naturais e, além disso, pos­
sibilita realizar aproximações para calcular probabilidades de muitas variáveis
aleatórias que têm outras distribuições. É muito importante também na inferên­
cia estatística, como será observado nos capítulos seguintes.
A distribuição normal é caracterizada por uma função de probabilidade,
cujo gráfico descreve uma curva em forma de sino, como mostra a Figura 6.8.
Essa forma de distribuição evidencia que há maior probabilidade de a variável
aleatória assumir valores próximos do centro.

VARIÁVEIS ALEATÓRIAS CONTÍNUAS 153
Figura 6.8 Representação gráfica da função densidade de probabilidade normal e
a indicação de seus dois parâmetros: jj. e a.
Dados os parâmetros /x g IR e a > 0, a função densidade de probabilidade
da normal é dada por:
(6.19)
Com certo esforço matemático, é possível mostrar que o valor esperado e a
variância da distribuição normal são dados por:
EQQ = (6.20)
VOO = °2 (6.21)
A Figura 6.9 mostra diferentes curvas normais, em função dos valores de
(iea. As distribuições da Figura 6.8 podem representar, por exemplo, medidas
da dureza de aço produzido sob diferentes condições. A distribuição (1) repre­
senta a dureza do aço em uma situação padrão; e a distribuição (2), as medidas
de dureza do aço após um processo de melhoria da qualidade, em que aumen­
tou a dureza média. A distribuição (3) representa as medidas de dureza do aço
quando o processo está sob rígido controle; enquanto a distribuição (4) quando
fora de controle, o que acarreta aumento na variabilidade.
a) Mr ^ M-2 e o-! = a 2 b) |J-3 = m e 03 * a 4
Figura 6.9 Diferentes distribuições normais em função dos parâmetros fieo.

1 54 ESTATÍSTICA
Na sequência, representaremos uma variável aleatória X com distribuição
normal de média [x e variância por X : N(jj, a 2). Seguem outras característi­
g 2
cas do modelo normal:
• a curva é simétrica em torno de ji, em consequência, os valores da
média (}i) e da mediana (md) são iguais, e também P(X < ji - a) =
P(X > |! + a), V a e 9?;
• teoricamente, a curva prolonga-se de - oc a + x, sendo lim f(x) = 0;
a área total sob a curva é igual a 1, ou seja, J fW d x = 1;
-oc
qualquer combinação linear de variáveis aleatórias normais é também
uma variável aleatória normal; em especial, se e X2 são variáveis
aleatórias independentes e X x : N (jii, g 2) eX 2 : N(ji2, g \), então Va, b
e % Y = aXi + bX2 tem distribuição normal com
£(Y) = aji! + b\i 2 (6.22)
V m = a2 G 2 + b2 G (6.23)
afastamentos da média, em unidades de desvio padrão, preservam a
mesma área sob a curva, independentemente dos valores de (i e o
(ver a Figura 6.10).
a a
2 a 2 a
3 a 3 CT
Figura 6.10 Afastamentos da média, em unidades de desvio padrão, preservam a
mesma área sob a curva normal.

VARIÁVEIS ALEATÓRIAS CONTÍNUAS 155
Seja X : N(\i, cr2), então a variável aleatória
(6.24)
tem distribuição normal com média zero e desvio padrão unitário, ou seja, Z :
N(0,1), que também é conhecida como distribuição normal padrão. Qualquer
área (probabilidade) sob a densidade de X pode ser avaliada sob a densidade
de Z, conforme ilustra a Figura 6.11. Dessa forma, qualquer problema relativo a
uma distribuição normal pode ser pensado em termos da distribuição normal
padrão.
Distribuição de X: Distribuição de Z:
normal com jj. = 170 e o = 10 normal padrão
140 150 160 170 180 190 200 x - 3 - 2 - 1 0 1 2 3
= = 180 - 170 = 1
10
Figura 6.11 Transformação do evento {X > 180}, da distribuição normal de pa­
râmetros ji = 170 e g = 10, em um evento da distribuição normal
padrão: {Z > 1}.
Tabela da distribuição norm al padrão
Como vimos, as probabilidades de uma variável com distribuição normal
podem ser representadas por áreas sob a curva da distribuição normal padrão.
No apêndice, apresentamos a Tabela 3, que relaciona valores positivos de z,
com áreas sob a cauda superior da curva. Os valores de z são apresentados com
duas decimais. A primeira decimal fica na coluna da esquerda e a segunda deci­
mal na linha do topo da tabela. A Figura 6.12 mostra como podemos usar a Ta­
bela 3 para encontrar uma área sob a cauda superior da curva.

1 56 ESTATÍSTICA
segunda decimal de z
z
0,00 0,01 0,02 0,09
• ••
0,0 0,4168
(pela
0,1 1f
tabela)
0,2 -* 0,4168
(área na cauda superior)
Figura 6.12 Ilustração do uso da tabela da distribuição normal padrão (Tabela
3 do apêndice) para encontrar P(Z > 0,21).
A área 0,4168 corresponde à probabilidade P(Z > 0,21) = 1 - O (0,21),
onde O representa a função de distribuição acumulada da normal padrão. Ou
seja, a Tabela 3 fornece os valores 1 - O(z), para z = 0,01, 0,02, ..., 3,00.
Exemplo 6.4 Seja Z uma variável aleatória com distribuição normal padrão.
Vamos usar a Tabela 3 para encontrar as seguintes probabilidades:
a) P(Z < 0,42). Esta probabilidade corresponde à
área da distribuição normal padrão indicada ao
lado. Podemos obter esta área, fazendo a seguin­
te operação: 0 0,42
0 0,42 0 0,42
área = 0,3372 área = 0,6628
(pela Tabela 3) (pela subtração)
Mais formalmente,
0(0,42) = P(Z < 0,42) = 1 - P(Z > 0,42) = 1 - 0,3372 = 0,6628
b) P(Z < 0,42). O esquema seguinte mostra esta probabilidade em ter­
mos de área e como podemos usar a simetria da curva para obtê-la
na Tabela 3.

VARIÁVEIS ALEATÓRIAS CONTÍNUAS 1 5 7
Ou seja,
P(Z < - 0,42) = P(Z > 0,41) = 0,3372
c) P (- 0,42 < Z < 0,42).
- 0,42 0 0,42
área pedida área total = 1 2 (0,3372)
Então, P (- 0,42 < Z < 0,42) = 1 - 2 (0,3372) = 0,3256.
Exemplo 6.5 Na distribuição normal padrão, qual é
o valor de z, tal que P(- z < Z < z) = 0,95? (Veja figu­
ra ao lado.)
Considerando a simetria da curva normal e o fato
de a área total sob a curva ser igual a 1 (um), pode­
mos transformar esta pergunta em: Qual é o valor de z
tal que P(Z > z) = 0,025? A figura ao lado ilustra a
equivalência entre as duas perguntas.
Entrando com o valor de área 0,025 na Tabela 3 do apêndice, encontra­
mos o valor de z igual a 1,96. Esse processo é ilustrado a seguir.
0,00 0,01 0,06 0,09
~ T ~
1,9 0,025
Exemplo 6.6 Suponha que a absorção de água (%) em certo tipo de piso ce­
râmico tenha distribuição normal com média 2,5 e desvio padrão 0,6. Selecio­
nando, aleatoriamente, uma unidade desse piso, qual é a probabilidade de ele
acusar absorção de água entre 2% e 3,5%?

1 58 ESTATÍSTICA
Solução: Primeiramente, precisamos transfor­
mar os valores de absorção de água (;c) em valores
padronizados (z), por (6.24), isto é,
x - n _ x - 2,5
z =
a 0,6
2 - 2 5
Para x = 2, temos: z = ------ — = - 0,83
0,6
3 5 - 2 5
e para x = 3,5, temos: z = —------ — = 1,67.
0,6
Usando a Tabela 3 do apêndice, encontramos
para z = 0,83 e z = 1,67 as respectivas áreas nas ex­
tremidades da curva: 0,2033 e 0,0475 (lembrando
que para valores negativos de z, como - 0,83, procu­
ramos na Tabela 3 seu valor absoluto, 0,83). É fácil
observar, pela figura ao lado, que a probabilidade
desejada corresponde ao complemento da soma des­
sas áreas, ou seja:
P(2 < X < 3,5) = P(- 0,83 < Z < 1,67) = 1 - (0,2033 + 0,0475) =
= 0,7492.
EXERCÍCIOS
.
8 Seja Z uma variável aleatória com distribuição normal padrão. Calcule:
a) P(Z > 1,65);
b) P(Z < 1,65);
c) P(- 1 < Z < 1);
d) P(- 2 < Z < 2);
e) P(- 3 < Z < 3);
f) P(Z > 6);
g) o valor de z, tal que P(- z < Z < z) = 0,90;
h) o valor de z, tal que P(- z < Z < z) = 0,99.

VARIÁVEIS ALEATÓRIAS CONTÍNUAS 1 5 9
9. Suponha que o tempo de resposta na execução de um algoritmo é uma va­
riável aleatória com distribuição normal de média 23 segundos e desvio pa­
drão de 4 segundos. Calcule:
a) a probabilidade de o tempo de resposta ser menor do que 25 segundos;
b) a probabilidade de o tempo de resposta ficar entre 20 e 30 segundos.
10. Certo tipo de conserva tem peso líquido (Xx) com média de 900 g e desvio pa­
drão de 10 g. A embalagem tem peso (X2) com média de 100 g e desvio
padrão de 4 g. Suponha X : eX 2 independentes e com distribuições normais.
a) Qual é a probabilidade de o peso bruto ser superior a 1.020 g?
b) Qual é a probabilidade do peso bruto estar entre 980 e 1.020 g?
6.3 A NORMAL COMO LIMITE DE OUTRAS DISTRIBUIÇÕES
Muitas distribuições de probabilidade aproximam-se da distribuição nor­
mal. É o caso da binomial quando n é grande e da Poisson quando X é grande.
6.3.1 Aproximação norm al à binomial
Nos experimentos binomiais, quando n é muito grande, o uso da função de
probabilidade binomial é impraticável, pois os coeficientes binomiais tomam-se
exageradamente grandes. Já vimos que nos casos em que n é grande e p é mui­
to pequeno, podemos usar a distribuição de Poisson para calcular, aproximada­
mente, as probabilidades de uma binomial. Quando n é grande e p não é pró­
ximo de 0 ou de 1, a distribuição normal pode ser usada para calcular,
aproximadamente, as probabilidades de uma binomial.
A Figura 6.13 apresenta gráficos das distribuições de probabilidades bino­
miais com n = 1, 10 e 50 e p = 0,5 e 0,2.
Observando a Figura 6.13, verificamos que quando n = 50, a forma da dis­
tribuição binomial é parecida com a curva de uma distribuição normal. Obser­
ve, ainda, que se p = 0,5, a aproximação já parece razoável para n = 10.
De maneira geral, as condições para fazer uma aproximação da distribui­
ção binomial para a normal são:
1) n g ran d e e
2) p n ão muito próximo de 0 (zero) ou de 1 (um).

1 60 ESTATÍSTICA
Uma regra prática, sugerida por vários autores, considera a aproximação
razoável se as duas seguintes inequações estiverem satisfeitas:
np > 5 e (6.25)
n(l - p) > 5 (6.26)
Os parâmetros |i e a da distribuição normal devem-se identificar ao valor
esperado e ao desvio padrão do modelo binomial, ou seja:
(6.27)
H = nP __________
a = v np( 1 - p) (6.28)
Exemplo 6.7 Historicamente, 10% dos pisos cerâmicos, que saem de uma li­
nha de produção, têm algum defeito leve. Se a produção diária é de 1000 uni­
dades, qual é a probabilidade de ocorrer mais de 120 itens defeituosos?

VARIÁVEIS ALEATÓRIAS CONTÍNUAS 161
Pelas características do experimento, a variável aleatória Y = número de
defeituosos na amostra tem distribuição binomial com parâmetros n = 1000 e
p = 0,1. Verificamos, também, que as condições 6.25 e 6.26 estão satisfeitas, pois
a) np = (1000) (0,1) = 100 > 5 e
b) n (l - p ) = (1000)(0,9) = 900 > 5
Usando (6.27) e (6.28), temos:
[x = np = 1000.(0,1) = 100 e
a = y]nPa - p ) = V1000 (0,1) (0,9) = J9Õ
Considere X uma variável aleatória normal com média [i = 100 e variância
o2 = 90. Então:
P(Y > 120) * P(X > 120)
V
Binomial com Normal com
J ,
n = 1.000 e p = 0,1 p. = 100 e a2 = 90
Valor padronizado: z = —— - = 1^0 _ \ \
2
a V 9 0
Assim, PCX > 120) = P(Z > 2,11) = 0,0174
Correção de continuidade
Ao calcularmos probabilidades de eventos oriundos de experimentos bino­
miais como áreas sob uma curva normal, estamos fazendo uma aproximação de
uma variável aleatória discreta, que só assume valores inteiros, para uma variá­
vel contínua, cujos eventos constituem intervalos de números reais. Nesse con­
texto, devemos fazer alguns ajustes, como ilustra o exemplo seguinte.
Exemplo 6.8 Seja Y o número de caras obtido em dez lançamentos de uma
moeda honesta. Vamos calcular a probabilidade de obter quatro caras usando a
distribuição normal.
Pelas características do experimento, Y tem distribuição binomial com
n = 10 e p = 0,5. Então, a média e o desvio padrão são dados por:
[x = np = 10(0,5) = 5 e
a = V np (1 - p) = v 10 • (0,5) • (1 - 0,5) = v' 2,5

1 62 ESTATÍSTICA
Considere o evento: ocorrer quatro caras, ou seja {Y = 4}. Ao expressar
este evento em termos de uma variável aleatória contínua X : N{5, 2,5), deve­
mos considerar um intervalo em torno do valor 4, pois para variáveis aleatórias
contínuas só faz sentido avaliar probabilidades em intervalos. O intervalo ade­
quado, nesse caso, é construído pela subtração e soma de meia unidade ao valor
quatro, ou seja, {3,5 < X < 4,5}, como ilustra a Figura 6.14.
m
0,3
Pela normal:
Pela binomial:
P (3,5 < X < 4,5) =
P (Y = 4) = 0,2051
= P (- 0,95 < Z < - 0,32)
0,2 = 0,2034
0,1
0
Figura 6.14 Aproximação da probabilidade do evento {Y = 4} (em termos da dis­
tribuição binomial) para a probabilidade do evento {3,5 < X < 4,5}
(em termos da distribuição normal).
O procedimento de subtrair e somar meia unidade para construir um in­
tervalo em torno de valores inteiros é conhecido como correção de continuidade.
Esta correção deve ser usada ao aproximar um evento de uma variável aleató­
ria que só assume valores inteiros para um evento de uma variável aleatória
contínua.
A Figura 6.15 ilustra as diversas situações possíveis de probabilidade asso­
ciada a uma variável aleatória discreta, assumindo valores em {0, 1, 2, ...},
aproximada por probabilidade associada a uma variável aleatória contínua, a
qual pode assumir qualquer valor real.

VARIÁVEIS ALEATÓRIAS CONTÍNUAS 163
P(Y = k:
Y: binomial
X: normal
P(Y < fc) « P(X < k + 0,5)
k k + 0,5
» a, V—' 1 o 5 <X:< k + 0,5)
-----► —►
1c k - 0,5 /c k + 0,5
P([Y>k)*F’(X> k - 0,5)
^ J
...►
.......::::::::
k k--0,5 /k
F'(Y < k) « P(X <: k - 0,5) P( Y> k) « P(X > k + 0,5)
k k - 0,5 k k k + 1 k k + 0,5
Figura 6.15 Correção de continuidade ao aproximar uma variável aleatória dis­
creta por uma variável aleatória contínua.
6.3.2 Aproximação norm al à Poisson
A distribuição de Poisson (Figura 6.16) também se aproxima da normal
quando X é grande. Como o valor esperado e a variância de uma Poisson são
ambos iguais a X, então, na aproximação normal, devemos usar:
(6.29)
(6.30)
X = 1
X = 5 K = 20
••
• •
• •
p(x) p(x) • * 0,08 p(x)
0,4
0,15
0,3
0,10
0,04
0,2
0,05
0,1
-> 0,00* 0,00
0,0
0 1 2 3 4 5 X 0 2 4 6 8 10 12* 10 20 30 X
Figura 6.16 Distribuições de Poisson para diferentes valores de X.

1 64 ESTATÍSTICA
Conforme mostra a Figura 6.16, a aproximação é razoável para X > 5. Para
a aproximação da normal à Poisson, a correção de continuidade, discutida na
Seção 6.4.1, também deve ser usada.
EXERCÍCIOS
11. De um lote de produtos manufaturados, extraímos 100 itens ao acaso. Se
10% dos itens do lote são defeituosos, calcular a probabilidade de:
a) 12 itens serem defeituosos;
b) mais do que 12 itens serem defeituosos.
12. Uma empresa de auxílio à lista telefônica recebe, em média, sete solicita­
ções por minuto, segundo uma distribuição de Poisson. Qual é a probabili­
dade de ocorrer mais de 80 solicitações nos próximos 10 minutos?
6.4 GRÁFICO DE PROBABILIDADE NORMAL
Como veremos nos capítulos posteriores, muitos métodos estatísticos são
desenvolvidos na suposição de que os dados provêm de uma distribuição nor­
mal. Quando o número de observações é grande, podemos construir um histo­
grama e verificar se sua forma segue uma curva em forma de sino, sugerindo o
modelo normal. É o caso da Figura 6.17.
300
250
200
150
100
50
0
71 72 73 74 75 76 77 78
tem peratura (°C)
Figura 6.17 Distribuição de frequências de 1.389 leituras da temperatura de um
pasteurizador.
Podemos, também, calcular a média (x) e o desvio padrão (s) dos dados e
verificar se os intervalos
x ± s, x ± 2s e x ± 3s

VARIÁVEIS ALEATÓRIAS CONTÍNUAS 165
têm percentuais de casos próximos dos esperados por uma distribuição normal
(Figura 6.10).
Quando a quantidade de observações for pequena, o histograma pode
apresentar uma forma muito diferente da real distribuição do processo que ge­
rou os dados. Além disso, o cálculo d e x e s podem ser muito influenciados por
algum valor discrepante. Em geral, o chamado gráfico de probabilidade normal é
mais adequado para verificar a suposição de um modelo normal para os dados.
Algoritmos computacionais para a construção desse gráfico estão implementa­
dos em quase todos pacotes computacionais estatísticos.
Ilustraremos a construção do gráfico de probabilidade normal com apenas
cinco observações (x-, i = 1, 2, ..., 5): 74,8; 74,0; 74,7; 74,4 e 75,9. Sejam x(l)
os valores ordenados, isto é, 74,0; 74,4; 74,7; 74,8; 75,9.
Considere uma distribuição normal com a área dividida em cinco partes
iguais (mesmo número de partes do número de valores, n). E sejam q(0 (£ = 1, 2,
..., 5) os pontos medianos dos intervalos formados pela divisão das cinco áreas
iguais (ver a Figura 6.18).
Cada fatia com 20% de área.
Em cada fatia, o ponto q(0
separa 50% de área para
cada lado.
<3(1) <3(4) x
9(2)Q(3) 9(5)
Figura 6.18 Configuração de cinco pontos com as posições relativas mais verossí­
meis possíveis sob um modelo normal.
Se as cinco observações (74,0; 74,4;
74,7; 74,8; 75,9) provêm de uma distribui­
ção normal, devemos esperar uma relação
aproximadamente linear com os valores teó­
ricos q(l). O gráfico de probabilidade normal
compreende a apresentação dos pontos (x(l),
q(í)), num par de eixos cartesianos, conforme
73,6 74.0 74.4 74,8 75.2 75.6 76.0
o gráfico ao lado. Nesse gráfico, os valores
valor observado
de q(í) foram padronizados (média zero e va­
riância 1).
A Figura 6.19 apresenta dois gráficos de probabilidade normal. O gráfico
da esquerda foi construído com 40 observações que aparentemente seguem

1 6 6 ESTATÍSTICA
uma distribuição normal. No gráfico da direita introduzimos um valor discre­
pante.
73,5 74,5 75,5 76,5 74 76 78 80 82 84
valor observado valor observado
Figura 6.19 Gráfico de probabilidade normal referente a 40 leituras de tempera­
tura de um pasteurizador e o efeito de um valor discrepante.
A Figura 6.20 mostra um gráfico de probabilidade normal construído com
dados gerados por uma distribuição assimétrica, como mostrado do lado es­
querdo da figura. Note que os pontos não estão aleatoriamente em torno de
uma reta.
Figura 6.20 Gráfico de probabilidade normal referente a 40 observações geradas
por uma distribuição assimétrica.
EXERCÍCIOS COMPLEMENTARES
13. O setor de manutenção de uma empresa fez um levantamento das falhas
de um importante equipamento, constatando que há, em média, 0,75 falha
por ano e que o tempo entre falhas segue uma distribuição exponencial.
Qual é a probabilidade de o equipamento não falhar no próximo ano?

VARIÁVEIS ALEATÓRIAS CONTÍNUAS 1 67
14. A vida útil de certo componente eletrônico é, em média, 10.000 horas e
apresenta distribuição exponencial. Qual é a percentagem esperada de
componentes que apresentarão falhas em menos de 10.000 horas?
15. A vida útil de certo componente eletrônico é, em média, 10.000 horas e
apresenta distribuição exponencial. Após quantas horas se espera que 25%
dos componentes tenham falhado?
16. Na manufatura de fios de linha para costura ocorre, em média, um defeito
a cada 100 metros de linha, segundo uma distribuição de Poisson.
a) Qual é a probabilidade de o próximo defeito ocorrer após 120 metros?
b) Quantos metros de linha poderão ser percorridos para que a probabili­
dade de aparecimento de algum defeito seja de 10%?
17. Num laticínio, a temperatura do pasteurizador deve ser de 75°C. Se a tem­
peratura ficar inferior a 70°C, o leite poderá ficar com bactérias maléficas
ao organismo humano. Observações do processo mostram que valores da
temperatura seguem uma distribuição normal com média 75,4°C e desvio
padrão 2,2°C.
a) Qual é a probabilidade da temperatura ficar inferior a 70°C?
b) Qual é a probabilidade de que, em 500 utilizações do pasteurizador,
em mais do que cinco vezes a temperatura não atinja 70°C? Precisa
supor distribuição normal.
18. O tempo para que um sistema computacional execute determinada tarefa é
uma variável aleatória com distribuição normal, com média 320 segundos e
desvio padrão de 7 segundos.
a) Qual é a probabilidade de a tarefa ser executada entre 310 e 330 se­
gundos?
b) Se a tarefa é colocada para execução 200 vezes. Qual é a probabilida­
de de ela demorar mais do que 325 segundos em pelo menos 50 vezes?
19. a) Um exame de múltipla escolha consiste em dez questões, cada uma
com quatro possibilidades de escolha. A aprovação exige, no mínimo,
50% de acertos. Qual é a probabilidade de aprovação se o candidato
comparece ao exame sem saber absolutamente nada, apelando apenas
para o “palpite”?
b) E se o exame tivesse 100 questões?
20. No horário de maior movimento, um sistema de banco de dados recebe, em
média, 100 requisições por minuto, segundo uma distribuição de Poisson.
Qual é a probabilidade de que no próximo minuto ocorram mais de 120 re­
quisições? Use a aproximação normal com correção de continuidade.

1 6 8 ESTATÍSTICA
.
21 Os dados históricos de uma rede de computadores sugerem que as cone­
xões com essa rede, em horário normal, seguem uma distribuição de Poisson
com média de cinco conexões por minuto. Calcule t0, tal que se tenha pro­
babilidade igual a 0,90 de que ocorra pelo menos uma conexão antes do
tempo t0.
.
22 O padrão de qualidade recomenda que os pontos impressos por uma im­
pressora estejam entre 3,7 e 4,3 mm. Uma impressora imprime pontos,
cujo diâmetro médio é igual a 4 mm e o desvio padrão é 0,19 mm. Supo­
nha que o diâmetro dos pontos tenha distribuição normal.
a) Qual é a probabilidade do diâmetro de um ponto dessa impressora es­
tar dentro do padrão?
b) Qual deveria ser o desvio padrão para que a probabilidade do item (a)
atingisse 95%?
23. Certo tipo de cimento tem resistência à compressão com média de 5.800
kg/cm2, e desvio padrão de 180 kg/cm2, segundo uma distribuição normal.
Dada uma amostra desse cimento, calcule as seguintes probabilidades:
a) resistência inferior a 5.600 kg/cm2;
b) resistência entre 5.600 kg/cm2 e 5.950 kg/cm2;
c) resistência superior a 6.000 kg/cm2, sabendo-se que ele já resistiu a
5.600 kg/cm2.
d) se quer a garantia de que haja 95% de probabilidade de o cimento resis­
tir a determinada pressão, qual deve ser o valor máximo dessa pressão?
24. Uma empresa fabrica dois tipos de monitores de vídeo. É suposto que as
durabilidades deles seguem distribuições normais, sendo o monitor Ml
com média de 6 anos e desvio padrão 2,3 anos; e o monitor M2 com média
de 8 anos e desvio padrão 2,8 anos. M l tem 2 anos de garantia e M2 tem 3
anos. A empresa lucra R$ 100,00 a cada M l vendido e RS 200,00 a cada
M2 vendido, mas se deixarem de funcionar no período de garantia, a em­
presa perde RS 300,00 (no caso de M l) e RS 800,00 (no caso de M2). Em
média, qual é o tipo de monitor que gera mais lucro?

7
Distribuições Amostrais e
Estimação de Parâmetros
Este capítulo apresenta a base para aprendermos a estatística indutiva, a
qual fornece procedimentos formais para tirar conclusões sobre uma população,
a partir dos dados de uma amostra. Para isso, veremos como se relacionam es­
tatísticas (características dos elementos de uma amostra) com parâmetros (ca­
racterísticas dos elementos de uma população).
7.1 PARAMETROS E ESTATÍSTICAS
Relembremos alguns conceitos básicos:
População: conjunto de elementos que formam o universo de nosso estu­
do e que são passíveis de ser observados, sob as mesmas condições.
Amostra: uma parte dos elementos de uma população.
Amostragem: o processo de seleção da amostra.
Amostragem aleatória sim ples: o processo de seleção é feito por sor­
teio, fazendo com que todos os elementos da população tenham a mesma
chance de serem escolhidos e, além disso, todo subconjunto de n elementos
tenha a mesma chance de fazer parte da amostra.
Quando a amostragem é aleatória e, em especial, quando é aleatória sim­
ples, podemos fazer inferências sobre a população, com base no estudo de uma
amostra (ver a Figura 7.1).

1 70 ESTATÍSTICA
AMOSTRAGEM
POPULAÇAO:
conjunto de elementos
AMOSTRA: um subconjunto
de n elementos da população
INFERÊNCIA
Figura 7.1 Ilustração de conceitos básicos da estatística.
Em geral, estamos pesquisando uma ou mais variáveis associadas aos ele­
mentos da população ou da amostra. Nesse contexto, também podemos carac­
terizar a população e a amostra em termos da variável em estudo. Por exemplo,
ao verificar se cada consumidor potencial de uma revendedora de automóveis
planeja (X = 1) ou não (X = 0) comprar um carro novo no próximo ano, pode­
mos representar a população pelo conjunto {jcx, x2, x3,..., %}, onde Xj = 0 ou 1,
dependendo se o j-ésimo indivíduo da população pretende ou não comprar um
carro novo no próximo ano. Da mesma forma, a amostra, que será formada por
n indivíduos a serem selecionados da população, pode ser representada por {Xlf
X2) ..., Xn}, onde Xt é a variável aleatória que corresponde ao valor de X (0 ou 1)
na i-ésima observação (i = 1, 2, ...n).
No presente contexto, definimos:
P arâm etro : alguma medida descritiva (média, variância, proporção etc.)
dos valores x lf x2) x3,..., associados à população.
A m ostra a le a tó ria sim ples: conjunto de n variáveis aleatórias inde­
pendentes {Xlf X2, ..., X J, cada uma com a mesma distribuição de probabi­
lidades de certa variável aleatória X. Essa distribuição de probabilidades
deve corresponder à distribuição de frequências dos valores da população
E statística: alguma medida descritiva (média, variância, proporção etc.)
das variáveis aleatórias Xlf X2, ..., Xn, associadas à amostra (ver a Figura 7.2).

DISTRIBUIÇÕES AMOSTRAIS E ESTIMAÇÃO DE PARÂMETROS 171
Parâmetros Estatísticas
Proporção ^ _ rQ de elementos com o atributo - _ nQ de elementos com o atributo
N n
1 n
Média 1 y *
x - ± j : x t
U = — y X:
N t í
Variância a 2 = I f (x,.-^V
N t r }
Figura 7.2 Alguns parâmetros e estatísticas.
Estatísticas e variáveis aleatórias
Vamos considerar uma amostragem aleatória simples, o que faz com que
qualquer medida associada à amostra (estatística) seja uma variável aleatória.
Isso ocorre por causa da aleatoriedade introduzida pelo sorteio, na amostra­
gem. A fim de entender melhor esse conceito, vamos acompanhar os exemplos
seguintes.
Exemplo 7.1 Em um estudo sobre emissões de C02, definiu-se uma popula­
ção como sendo composta por quatro ônibus de uma pequena companhia de
transporte urbano. Dos quatro ônibus, um deles apresentava alto índice de
emissão, enquanto os outros três estavam dentro dos padrões. Assim, a popula­
ção pode ser descrita por {1, 0, 0, 0}. O parâmetro de interesse é a proporção de
veículos fora do padrão. Considere as seguintes questões acerca dessa população:
a) calcular a proporção populacional (p);
b) se for retirada uma amostra aleatória simples, com reposição, de ta­
manho n = 2, qual será a proporção P de veículos fora dos padrões
na amostra?
Solução: Para a questão (a), a resposta é trivial: p = lA. Já a
questão (b) não pode ser respondida, pois a proporção amostrai (P)
é uma variável aleatória. Assim, não podemos dizer o que vai ocor­
rer, mas tão somente o que pode ocorrer.

1 72 ESTATÍSTICA
c) retificando a questão (b), construir a distribuição de probabilidades
da proporção amostrai.
Solução: Seja a variável aleatória X = número de ônibus com alto
índice de emissão entre dois ônibus selecionados ao acaso. Então, X
possui distribuição binomial, já que se trata de dois eventos inde­
pendentes, com duas possibilidades cada (sucesso = ônibus com alto
índice de emissão; fracasso = ônibus dentro dos padrões). Os parâme­
tros da distribuição são n = 2 e p = 0,25. Assim, pela distribuição
binomial (ver a Tabela I do apêndice), temos:
X P(x)
0 0,5625
1 0,3750
2 0,0625
Total 1
A proporção amostrai é dada por:
P = X
n 2
Assim, sua função de probabilidade é dada por:
P A P(P)
0 0,5625
y2 0,3750
i 0,0625
Total 1
A função de probabilidade de P também é chamada de distribuição da pro­
porção amostrai ou distribuição amostrai da proporção, pois apresenta os possí­
veis resultados de uma proporção, que é calculada sobre os elementos de uma
amostra a ser extraída da população em estudo. De maneira geral, temos:
Uma estatística é uma variável aleatória e sua distribuição de probabilida­
des é chamada de distribuição amostrai

DISTRIBUIÇÕES AMOSTRAIS E ESTIMAÇÃO DE PARÂMETROS 173
Exemplo 7.2 Seja a população dos quatro ônibus e ~ pOO
a variável X = número de vezes que o ônibus teve um
defeito grave. Se um ônibus teve dois defeitos graves,
o outro três, o outro quatro e o último cinco defeitos
graves, então a população, em termos da variável X,
pode ser descrita pelo conjunto {2, 3, 4, 5}. A popu- z
lação também pode ser descrita pela função de probabilidade ao lado - a distri­
buição da população. Essa distribuição tem os parâmetros valor esperado (mé­
dia) e variância dados por:
n = — f \ x : = - ( 2 +3 + 4 + 5 ) = 3,5 e
N f t 4
-^)2 = *[(2 - 3’5)2 + (3 - 3>5)2 + (4 - 3’5)2 + (5 - 3’5)2] = i-25
A Tabela 7.1 mostra a construção da distribuição da média amostrai, con­
siderando uma amostragem aleatória simples com n = 2 elementos, extraída
com reposição.
Tabela 7.1 Construção da distribuição de X (Exemplo 7.2).
Amostras possíveis Valor de X Probabilidade
(2, 2) 2,0
Kó
(2, 3), (3, 2) 2,5 Ko
(2, 4), (3, 3), (4, 2) 3,0
Kc
(2, 5), (3, 4), (4, 3), (5, 2) 3,5
(3, 5), (4, 4), (5, 3) 4,0
%6
(4, 5), (5, 4) 4,5
(5, 5) 5,0
Kó
O valor esperado e a variância da distribuição de X são:
' 4 N ' 3 >
+ 31 A + 3,5 + 4 + 4,5| — ^
16 / U 6 / ,16, 16
+ 5 = 3,5
16
V(X) = (2 - 3,5)2 ^ + (2,5 - 3,5)2 A +.. .+ (5 - 3,5)2 = 0,625

1 74 ESTATÍSTICA
A Figura 7.3 mostra a distribuição da população e a distribuição da média
amostrai. Note que ambas têm a mesma média (valor esperado), mas a distri­
buição da média amostrai é mais concentrada (menor variância) e tem forma
mais parecida com a distribuição normal.
Distribuição da
Distribuição da
média amostrai
população p(x)
pM
2 3_A 4 5
Î 4
J= 3,! EQO = 3,5
Figura 7.3 Distribuição da população do Exemplo 7.2 e a distribuição da média
amostrai, considerando amostragem aleatória simples com n = 2 ele­
mentos, extraídos com reposição.
EXERCÍCIOS
1. Refaça o Exemplo 7.1c, considerando que a amostra seja retirada sem re­
posição.
2. Em um estudo sobre consumo de combustível, definiu-se uma população
composta por quatro ônibus de uma pequena companhia de transporte ur­
bano. Os consumos dos ônibus (km/l), em condições padrões de teste,
eram 3,8, 3,9, 4,0 e 4,1. Uma amostra de dois elementos será sorteada,
com reposição. Verifique todas as amostras possíveis e, em seguida, cons­
trua a distribuição amostrai para o consumo médio da amostra e calcule o
valor esperado e a variância.
3. Refaça o exercício anterior considerando amostragem sem reposição.
7.2 DISTRIBUIÇÕES AMOSTRAIS
Quando a amostragem é aleatória simples, várias estatísticas apresentam
distribuições amostrais que se aproximam de distribuições contínuas conheci­
das, à medida que o tamanho da amostra cresce. É o caso da média e da pro­
porção que apresentam distribuições amostrais aproximadamente normal.

DISTRIBUIÇÕES AMOSTRAIS E ESTIMAÇÃO DE PARÂMETROS 175
7.2.1 Distribuição am ostrai da média
Considere o esquema ilustrado na Figura 7.4.
Amostragem
aleatória simples
X pode ser vista como uma variável
aleatória se considerar a distribuição
de frequências da população como
uma distribuição de probabilidades -
a distribuição da população.
Figura 7.4 Esquema geral de uma amostragem aleatória simples na observação
de uma variável quantitativa X.
Seja uma amostra aleatória simples {X1? X2, Xn} e a estatística X. A dis­
tribuição de X (distribuição da média amostrai) apresenta as seguintes proprie­
dades:
a) O valor esperado da média amostrai é igual à média da população,
ou seja:1
EOO (7.1)
b) A variância da média amostrai é inferior à variância populacional
e a relação é dada por
(cj2)
2
(se a amostragem for com reposição, ou N (7.2)
•. i\ o
/ n muito grande ou infinito).2
l
2 Com as condicionantes, podemos supor independência entre Xu ..., Xn, donde:

1 76 ESTATÍSTICA
OU
(se a amostragem for sem reposição e (7.3)
N não muito grande, N < 20n)
c) (Teorema do limite central) Se o tamanho da amostra for razoavel­
mente grande, então a distribuição amostrai da média pode ser apro­
ximada pela distribuição normal. Em geral, para n > 30, a aproxima­
ção já é boa, porém, se a distribuição da população não for muito
distante de uma normal, a aproximação pode ser usada com n menor.
Exemplo 7.2 (continuação) Dada a população {2, 3, 4, 5}, com parâmetros
/z = 3,5 e a 2 = 1,25, e considerando o planejamento de uma amostra aleatória
simples, com reposição, de n = 2 elementos, então podemos obter o valor espe­
rado e a variância da média amostrai usando (7.1) e (7.2):
E(X) = ji = 3,5 e
= —= ^
V(x) = 0,625
^ } n 2
Observe que são os mesmos valores encontrados anteriormente.
7.2.2 Distribuição am ostrai da proporção
Quando o interesse é estudar uma proporção, tal como a proporção dos ele­
mentos que têm certo atributo A, a população pode ser vista como dividida em
dois subgrupos:
1. o subgrupo dos elementos que têm o atributo A; e
2. o subgrupo dos elementos que não têm o atributo A, como mostra a
Figura 7.5.
População: N = NA + NÁ elementos
Parâmetro
p = proporção dos elementos 0 ou 1
que têm o atributo A (0 = Sem o atributo;
1 = com o atributo)
Figura 7.5 Esquema geral de uma amostragem aleatória simples quando se ob­
serva a proporção de certo atributo A.

DISTRIBUIÇÕES AMOSTRAIS E ESTIMAÇÃO DE PARÂMETROS 1 7 7
A distribuição da população pode ser representada por uma variável alea­
tória de Bernoulli (tipo “0-1”), com função de probabilidade:
X PW
0
1 - p
1
P
Como vimos no Capítulo 5, o valor esperado e a variância de uma distribui­
ção desse tipo são dados, respectivamente, por:
= P e (7.4)
a2 = p( 1 - p) (7.5)
Representando as observações amostradas por
'1 se o i- ésimo elemento tem o atributo A
X; =
0 se o i - ésimo elemento não tem o atributo A
verificamos que
número de elementos com o atributo A
X = -^ ---- = P (7.6)
n n
ou seja, a proporção equivale a uma média aritmética para dados de variáveis
do tipo “0-1”. Assim, as propriedades da distribuição amostrai da média tam­
bém são aplicadas à distribuição amostrai da proporção. Usando as notações
próprias da proporção, temos:
a) O valor esperado da proporção amostrai é igual à proporção da po­
pulação:
(7.7)
b) A variância da proporção amostrai é dada por
(se a amostragem for com reposição, ou N (7.8)
muito grande ou infinito).
ou
vcp) - p q - p ) . N - n (se a amostragem for sem reposição (7.9)
n N - l e N não muito grande, N < 20n)

1 7 8 ESTATÍSTICA
c) Se o tamanho da amostra for razoavelmente grande, então a distri­
buição amostrai da proporção pode ser aproximada pela distribuição
normal.3
As aplicações da distribuição da proporção amostrai podem ser feitas no
contexto da aproximação da distribuição normal à binomial, inclusive com a
correção de continuidade (Seção 6.3.1).
EXERCÍCIOS
4. Uma fundição produz blocos para motor de caminhões. Os furos para as
camisas devem ter diâmetro de 100 mm, com tolerância de 5 mm. Para ve­
rificar qual é o diâmetro médio no processo, a empresa vai retirar uma
amostra com 36 blocos e medir os diâmetros de 36 furos ( l a cada bloco).
Suponha que o desvio padrão (populacional) dos diâmetros seja conhecido
e igual a 3 mm.
a) Qual é o desvio padrão da distribuição da média amostrai?
b) Qual é a probabilidade de a média amostrai diferir da média popula­
cional (desconhecida) em mais do que 0,5 mm (para mais ou para
menos)?
c) Qual é a probabilidade de a média amostrai diferir da média populacio­
nal (desconhecida) em mais do que 1 mm (para mais ou para menos)?
d) Se alguém afirmar que a média amostrai não se distanciará da média
populacional em mais do que 0,98 mm, qual é a probabilidade de essa
pessoa acertar?
e) Se alguém afirmar que a média amostrai não se distanciará da média
populacional em mais do que 1,085 mm, qual é a probabilidade de
essa pessoa errar?
5. Uma empresa fabricante de pastilhas para freios efetua um teste para con­
trole de qualidade de seus produtos. Supondo que 1% das pastilhas fabrica­
das pelo processo atual apresenta desempenho deficiente quanto ao nível
de desgaste, qual é a probabilidade, em uma amostra aleatória simples
com 10.000 pastilhas, de serem encontradas 85 ou menos pastilhas com
problemas?
.
6 Sabe-se que 50% dos edifícios construídos em uma grande cidade apresen­
tam problemas estéticos relevantes em menos de cinco anos após a entrega
3 Observamos que a distribuição exata é a binomial (ou a hipergeométrica se a amostra­
gem for feita de população pequena e sem reposição).

DISTRIBUIÇÕES AMOSTRAIS E ESTIMAÇÃO DE PARÂMETROS 179
da obra. Considerando a seleção de uma amostra aleatória simples com
200 edifícios com cinco anos, qual é a probabilidade de menos de 90 deles
apresentarem problemas estéticos relevantes (considerar que não tenha ha­
vido obras de reparo nos edifícios selecionados)?
7. Existem vários algoritmos computacionais que permitem gerar números
aleatórios (ou, mais apropriadamente, pseudo-aleatórios) no intervalo [0, 1],
com distribuição uniforme. Considere a geração de 100 números (Xi, X2i ...,
X100) desta forma e sejaX a média aritmética simples desses 100 números.
a) Qual é o valor esperado e a variância de X J
b) Qual é a probabilidade de Xx assumir um valor no intervalo [0,47, 0,53]?
c) Qual é o valor esperado e a variância de X?
d) Qual é a distribuição de probabilidade de X?
e) Qual é a probabilidade de X assumir um valor no intervalo [0,47, 0,53]?
8. Um profissional de Computação observou que seu sistema gasta entre 20 e
24 segundos para realizar determinada tarefa. Além disso, o tempo gasto,
X, pode ser razoavelmente representado pela seguinte função de densidade:
~ “ 5, para 20 < x < 22
f(x) = < 6 - — para 22 < x < 24
4,
0, para [20,24]
x sé
a) Numa particular rodada, qual é a probabilidade de o sistema gastar
mais que 22,4 segundos?
b) Em 30 rodadas, qual é a probabilidade de o sistema gastar, em média,
mais que 22,4 segundos por rodada?
7.3 ESTIMAÇÃO DE PARÂMETROS
Nesta seção, estudaremos o problema de avaliar parâmetros populacionais,
a partir de operações com os dados de uma amostra. É um raciocínio tipica­
mente indutivo, em que se generalizam resultados da parte (amostra) para o
todo (população), conforme ilustra a Figura 7.6.

18 0 ESTATÍSTICA
POPULAÇÃO (universo do estudo)
O processo de
estimação de parâmetros
AMOSTRA (dados observados)
Figura 7.6 O raciocínio indutivo da estimação.
Por exemplo, podemos ter interesse em avaliar a resistência mecânica X de
um novo material. Contudo, X não é um número, mas uma variável aleatória,
porque há uma infinidade de fatores não controláveis que provocarão variações
nas possíveis medidas de resistência mecânica do material. É até razoável admi­
tir que a distribuição de X seja aproximadamente normal, por se tratar de medi­
das físicas. E o interesse pode estar na avaliação dos parâmetros populacionais
p = EQO e a 2 = V{X).
Medidas de resistência mecânica (Xl} X2, ..., Xn), a serem realizadas de for­
ma independente e sob as mesmas condições, constituem uma amostra aleató­
ria simples de X. Cálculos podem ser feitos sobre essas medidas para estimar os
parâmetros de interesse. Exemplos desses cálculos podem ser
(7.10)
(7.11)
« ■ - i è i S f r - * ) 1
que são estimadores dos parâmetros fi e a 2, respectivamente.
De forma genérica, considere uma população caracterizada pela distribui­
ção de certa variável aleatória X, com parâmetro 0. E seja (Xly X2) Xn) uma
amostra aleatória simples de X.
Uma estatística T é uma função dos elementos da amostra, isto é T = f(Xlf
X2, Xn). Quando ela é usada para avaliar certo parâmetro 0, é também
chamada de estím ador de 6.
Observe que um estimador é uma variável aleatória, pois depende da
amostra a ser selecionada. Realizada a amostragem, o estimador assume deter­
minado valor (o resultado do cálculo), o qual denominamos de estimativa.4
4 Neste texto, as estimativas serão representadas por letras minúsculas, contrastando
com os estimadores, os quais serão representados por letras maiúsculas.

DISTRIBUIÇÕES AMOSTRAIS E ESTIMAÇÃO DE PARÂMETROS 181
Algumas propriedades desejáveis de um estimador serão discutidas, o que
permite, pelo menos em tese, escolher o melhor estimador para cada situação
prática. Usando as distribuições amostrais, é possível avaliar probabilisticamen-
te o erro que se está cometendo por se usar uma amostra e não toda a popula­
ção - o erro amostrai. Isso será feito com estimativas em forma de intervalos de
confiança (Seções 7.3.2 e 7.3.3).
7.3.1 Propriedades de um estim ador
Um estimador, por ser uma variável aleatória, pode assumir valores, se­
gundo uma distribuição de probabilidades. Contudo, é desejável que, em mé­
dia, ele seja igual ao parâmetro que se deseja estimar. Mais formalmente,
T é um estimador n ão -v iesad o (ou n ão ten d en cio so ) de um parâmetro
9 se e só se E(T) = 9.
Por exemplo, X e P são estimadores não viesados dos parâmetros // e p ,
respectivamente, porque E(X) = / i e E(P) = p, conforme foi visto na Seção 7.2.
Já o estimador
â 2 = i f f c - x ) 2 (7.12)
N t r v }
é um estimador viesado do parâmetro a 2, pois E(ô2) - — - a 2. Por isso, defini-
n
mos a variância amostrai, S2, com denominador (n 1) no lugar de n. A dife-
rença
(7.13)
= " - o 2
v J n
é chamada de viés do estimador ô 2.
Na prática, retiramos só uma amostra, produzindo um único valor para o
estimador - uma estimativa. Mesmo que o estimador seja não viesado, o valor
da estimativa pode estar longe do valor do parâmetro. Outra propriedade dese­
jável é que o estimador tenha variância pequena, porque isso reduz a chance de
a estimativa acusar um valor distante do parâmetro.

1 8 2 ESTATÍSTICA
Dados dois estimadores não viesados Tl e T 2, sendo V(Ti) < V(T2), então Tj
é dito mais eficiente do que T2. E a eficiência relativa de Ti em relação a T2é
dada por:
(6.14)
A Figura 7.7 ilustra os conceitos de viés e eficiência, fazendo analogia com
tiros ao alvo, realizados por três rifles. Os rifles T1 e T2 são não viesados, porque,
em média, acertam o alvo; enquanto o rifle T3 é viesado. Embora 7\ e T2 sejam
não viesados, Tl é mais eficiente do que T2, pois a variância entre os tiros é
menor.
Figura 7.7 Tiros ao alvo com três rifles.
Considere a média amostrai (X) e a mediana amostrai (Md) como estima-
ct2
dores do parâmetro /*. Sabemos que V{X) = — . Se supusermos a população
n
com distribuição normal e a amostra grande, é possível mostrar que V(Md) *
7U (J ^ __ —
--------. Como V(X) < V(Md), então X é um estimador mais eficiente do que Md
2 n
na estimação de fx, nas condições estabelecidas. E a eficiência relativa de X em
relação à Md é dada por
7ia
V( M<) _
(7.15)
v ( x ) ~
Assim, em amostras grandes de populações normais, a média amostrai é
cerca de 57% mais eficiente do que a mediana amostrai. Isso significa que se
formos usar Md no lugar de X , precisamos ter uma amostra 57% maior, para
garantir a mesma eficiência na estimação de //.

DISTRIBUIÇÕES AMOSTRAIS E ESTIMAÇÃO DE PARÂMETROS 183
De modo geral, a qualidade de um estimador T, na estimação de um parâ­
metro 6, pode ser avaliada em função de seu erro quadrático médio, o qual é de­
finido por
EQM(T) = E(T - O)2 (7.16)
que pode ser escrito como5
£QM(T) = V(T) + (yiés)2 (7.17)
Então, para um estimador T não viesado, temos EQM(T) = V(T).
Para dois estimadores e T2 quaisquer (não necessariamente não viesa-
dos), definimos a eficiência relativa de Tl em relação à T2 por:
^ r " r ->
- í7 ' 18)
7.3.2 Intervalo de confiança para proporção
Em muitas situações, o principal parâmetro de interesse é alguma propor­
ção p. Por exemplo:
- a proporção de itens defeituosos em uma linha de produção;
- a proporção de consumidores que vão comprar certo produto;
- a proporção de mensagens que chegam adequadamente a seu destino etc.
Seja uma população caracterizada por uma variável aleatória X, que assu­
me o valor 0 ou 1, conforme o elemento tenha ou não certo atributo de interes­
se. Por exemplo, nas peças que saem de uma linha de produção, o código 0
pode identificar peça boa e o código 1 peça defeituosa. Para um elemento to­
mado ao acaso, seja p = P(X = 1 ) . Note que p representa a proporção de ele­
mentos com o atributo, na população.
Já vimos que a proporção amostrai P é um bom estimador da proporção
populacional p. Dada uma amostra aleatória simples de tamanho n, o que se
pode dizer sobre o erro amostrai: |P - p|?
Conforme discutido na Seção 7.2, se n for grande, a distribuição amostrai
de P é aproximadamente normal com6
5 EQMÇO = E{T - £(70 + £(70 - 0}2 = £{7* - £(70 }2 + {£(70 - 6}2 + 2£{7’ - £(70}
{£(70 -6 } = E{T - £(70}2 + {£(70 - O}2 + 0 = V(70 + (.viés)2.
6 Estamos supondo população infinita ou bastante grande. Caso contrário, deveríamos
usar a correção (7.9), como discutido na Seção 7.2.

18 4 ESTATÍSTICA
E( p ) = p e (7.19)
_ P d - P)
Denotaremos por
a * = \
( 7 -2 1 )
o desvio padrão da distribuição amostrai de P> que no presente contexto será
chamado de erro padrão de P.
Seja uma variável aleatória normal padrão, Z. Como vale a relação7
P{- 1,96 < Z < 1,96} = 0,95 (7.22)
podemos escrever
P-j -1,96 < ^ < 1,96 [ = 0,95 (7.23)
° p
OU
p{p - (1,96)0, < p < P + (1,96)0,} = 0,95 (7.24)
ou seja, com probabilidade de 95%, temos:
|P - p\ < (1,96)o . (7.25)
Observada efetivamente a amostra, e chamando de p a proporção obtida
nesta amostra, podemos definir um intervalo de confiança para p, com nível de
confiança de 95%, por
JC(p, 95%) = p ± (1,96 )a - (7.26)
Na prática, a - não pode ser calculado por (7.21), porque depende do pa­
râmetro desconhecido p. Então, usamos em seu lugar a estimativa:
7 Ver Exemplo 6.5 (Capítulo 6).

DISTRIBUIÇÕES AMOSTRAIS E ESTIMAÇÃO DE PARÂMETROS 185
H
_ (7.27)
Tl
Desde que a amostra seja grande (p. ex., n > 50), a diferença entre s- eo -
pode ser considerada desprezível, e um intervalo de confiança para p, com nível
de confiança de 95%, pode ser calculado por:
SL 5
JC(p, 95%) = p ± (1,96) j (7.28)
Esquematicamente,
intervalo de 95% de confiança para p
<-----------------------------------►
O O
p - (l,96)s? A p + (l,96)sp
P
Em suma, embora p seja um parâmetro populacional desconhecido, é pos­
sível, com base em uma amostra aleatória simples, construir um intervalo que
deve conter p com alto nível de confiança. É bastante usual o nível de confiança
de 95%, mas o intervalo pode ser construído com um nível y qualquer, bastan­
do encontrar o valor de zY na distribuição normal padrão, conforme mostra a Fi­
gura 7.8.
0,800 0,900 0,950 0,980 0,990 0,995 0,998
7
1,282 1,645 1,960 2,326 2,576 2,807 3,090
Figura 7.8 Valores de zY para alguns níveis de confiança.
Com zy tomado adequadamente, conforme o esquema da Figura 7.8, calcu­
lamos o intervalo de confiança para p por:

1 8 6 ESTATÍSTICA
Exemplo 7.3 Na avaliação de dois sistemas computacionais, A e B, foram se­
lecionadas 400 cargas de trabalho (tarefas) - supostamente uma amostra alea­
tória da infinidade de cargas de trabalho que poderiam ser submetidas a esses
sistemas. O sistema A foi melhor que o B em 60% dos casos. Construir interva­
los de confiança para p (proporção de vezes que o sistema A é melhor que o sis­
tema B, considerando todas as possíveis cargas de trabalho) usando níveis de
confiança de 95% e 99%.
Para o nível de confiança de 95%, temos zy = 1,96, resultando em
IC(P, 95%) = p ± (1,96)^ p (l^ p) = 0,6 ± ( 1 , 9 6 =
= 0,600 ± 0,048
ou, em porcentagens:
/C(p, 95%) = 60,0% ± 4,8%
Concluímos, então, que o intervalo (55,2%; 64,8%) contém o parâmetro p,
com nível de confiança de 95%.
Para o nível de confiança de 99%, temos zy = 2,576, resultando em
IC(p, 99%) = 0,6 ± (2,576) J ° ’6^ 4 ^ = 0,600 + 0,063
Ou seja, o intervalo (53,7%; 66,2%) contém o parâmetro p, com nível de
confiança de 99%. Esquematicamente:
intervalo de 99% de confiança para p
(60,0 ± 6,3%)
intervalo de 95% de confiança para p
(60,0 ± 4,8%)
■O
53,7% 55,2% 60,0% 64,8% 66,2%
Observe que, ao exigir maior nível de confiança, o intervalo de confiança
aumenta em magnitude. Tente entender o porquê disso! Para dado nível de con­
fiança, dizemos que uma estimativa é tão mais precisa quanto menor for a am-

DISTRIBUIÇÕES AMOSTRAIS E ESTIMAÇÃO DE PARÂMETROS 1 8 7
plitude de seu intervalo de confiança. A forma natural de aumentar a precisão é
aumentando o tamanho da amostra. Voltaremos a esse ponto na Seção 7.4.
7.3.3 Intervalo de confiança para média
Seja uma população caracterizada pela distribuição de uma variável alea-
tória X com os seguintes parâmetros: E(X) = / / e V(X) = a 2. Por exemplo, X
pode representar a mensuração da resistência mecânica de um novo material.
Devido ao erro experimental onipresente, X é uma variável aleatória; assim, o
interesse recai em seu valor esperado /*.
Considere uma amostra aleatória simples {Xu X2, ..., Xn} de X. Supondo X
com distribuição aproximadamente normal, então
(7.30)
é o estimador natural de fx. Vimos na Seção 7.2 que X tem distribuição aproxi­
madamente normal com média e variância dadas por8
E{X) = n (7.31)
(7.32)
n
O desvio padrão da distribuição amostrai de X,
o
(7.33)
será chamado de erro padrão de X.
Escolhendo z.f em função do nível de confiança y desejado, tal que P{- z, <
Z < zy} = y, podemos escrever
n ^ X - // ^
PJ - z < -------— < z = y (7.34)
ou
8 Novamente, estamos supondo a população infinita ou muito grande. Caso contrário,
deveríamos usar a correção (7.3), como visto na Seção 7.2.

1 8 8 ESTATÍSTICA
p \ x - z . , ^ = < n < X + z.,^= L = y (7.35)
[ vn Vn J
Observada efetivamente a amostra, e chamando de x a média aritmética
dos dados, podemos definir um intervalo de confiança para ji, com nível de
confiança y, por:
JC(n, y) = x ± z r -5L (7.36)
Exemplo 7.4 Em uma indústria de cerveja, a quantidade de cerveja inserida
em latas tem-se comportado como uma variável aleatória com média 350 ml e
desvio padrão 3 ml. Após alguns problemas na linha de produção, suspeita-se
que houve alteração na média. Uma amostra de 20 latas acusou média x = 346
ml. Construa um intervalo de confiança para o novo valor da quantidade média
f.i de cerveja inserida em latas, com nível de confiança 95%, supondo que não
tenha ocorrido alteração no desvio padrão do processo.
Solução:
IC(n, 95%) = x ± (1,96)-5= = 346 ± (1,96) -4 = = 346 ±1,31 ml
vn K ' v20
Interpretando: a quantidade m édia// de cerveja inserida em latas, após os
problemas na linha de produção, é 346 ml, tolerando, com 95% de confiança,
uma margem de erro de até 1,31 ml. Assim, o intervalo (344,69; 347,31) con­
tém, com 95% de confiança, o valor //. Isso mostra que estatisticamente houve
alteração na média do processo, pois o valor da média antiga (350 ml) não per­
tence ao intervalo.
Desvio padrão desconhecido
O intervalo de confiança descrito em (7.36) somente poderá ser usado nas
situações em que conhecemos o desvio padrão ct da população, o que não é co­
mum na prática. Caso contrário, o procedimento usual é substituir a pelo des­
vio padrão calculado com os dados da amostra:
Duas situações a considerar:
1. quando a amostra for grande (digamos, n > 50), a diferença entre a
e s pode ser desprezível, permitindo ainda o uso de (7.36);
2. quando a amostra for pequena, é necessário efetuar uma correção,
como veremos a seguir.

DISTRIBUIÇÕES AMOSTRAIS E ESTIMAÇÃO DE PARÂMETROS 189
A distribuição t de Student
Supondo a população com distribuição normal, a estatística
X - i x
T = (7.38)
vn
tem distribuição de probabilidades conhecida como distribuição t de Student,
com gl = n - 1 graus de liberdade.
A distribuição t de Student, como mostra a Figura 7.9, tem forma parecida
com a normal padrão, mas é um pouco mais dispersa. Essa dispersão varia com
o tamanho da amostra. É bastante dispersa para amostras pequenas, mas se
aproxima da normal padrão para amostras grandes.
Figura 7.9 Gráficos de distribuições t de Student e da normal padrão.
Dado um nível de confiança y, podemos obter o valor t.( da distribuição t
de Student, usando a Tabela 4 do apêndice, na linha correspondente a gl = n -
1. A Figura 7.10 ilustra esse processo, com gl = 9 e nível de confiança de 95%.
Distribuição t com gl = 9
Área na cauda superior
gl
0,025
j
o O 0
y 62
ac *95% — 2,262
Figura 7.10 Uso da tabela da distribuição t de Student: ilustração com gl = 9 e
nível de confiança de 95%.

19 0 ESTATÍSTICA
Intervalo de confiança para ^ com uso da distribuição t de Student
Usando a Tabela 4 com gl = n - 1, podemos escolher o valor ty em função
do nível de confiança y desejado, tal que
Pl (7.39)
= y
y / n
ou
P iX - t . 4 = < fi < X +t., s (7.40)
= y
L
'r yjn
Assim, o intervalo de confiança para /*, com a amostra efetivamente obser­
vada, é dado por9
(7.41)
Exemplo 7.5 Deseja-se avaliar a dureza esperada do aço produzido sob um
novo processo de têmpera. Uma amostra de dez corpos de prova do aço produ­
ziu os seguintes resultados de dureza, em HRc:
36,4 35,7 37,2 36,5 34,9 35,2 36,3 35,8 36,6 36,9
Construir um intervalo de confiança para /*, com nível de confiança de 95%.
Calculando as estatísticas para a amostra observada, temos:
s 5 = 4 = = 0,2325
Vn
9 Para amostras pequenas, a validade do ICQi, y) está condicionada à suposição de que
os dados provenham de uma distribuição aproximadamente normal. Para n > 30, o teorema limi­
te central garante a validade de ICQi, y) e, além disso, tem-se para n grande: tr * z..

DISTRIBUIÇÕES AMOSTRAIS E ESTIMAÇÃO DE PARÂMETROS 191
Como vimos na Figura 7.10, usando nível de confiança y = 95%, temos,
pela Tabela 4 com gl = 9, o valor t95% = 2,262, resultando em:
IC(m, 95%) = x ± t 95%-*-= 36,15 ± 0,53
vn
Ou seja, a resistência mecânica esperada do aço produzido pelo novo pro­
cesso de têmpera é 36,15 HRc, tolerando, com 95% de confiança, uma margem
de erro de até 0,53 HRc.
EXERCÍCIOS
9. Sejam Xly X2;, ..., X7 uma amostra aleatória simples de uma população com
média fi e desvio padrão a. Considere os seguintes estimadores de /*:
Ti = % + X2 + X3 +X , + X5 + Xò + X7) / 7
T2 = (X2 + X3 + *4 + *5 + Xe) / 5
r 3 = (X2 + X3 + X4 + X5 + X6) / 7
a) Quais estimadores são não viciados? Justifique.
b) Qual estimador é o mais eficiente entre Ti e T2? Justifique.
10. Em uma amostra aleatória simples com 200 edifícios com cinco anos, em
certa cidade, 55% apresentaram problemas estéticos relevantes após a en­
trega da obra. Construir um intervalo de confiança para a proporção de
edifícios da cidade que apresentam problemas estéticos relevantes nos cin­
co primeiros anos. Use nível de confiança de 95%.
11. Uma empresa fabricante de pastilhas para freios efetua um teste para con­
trole de qualidade de seus produtos. Selecionou-se uma amostra de 600
pastilhas, das quais 18 apresentaram níveis de desgaste acima do tolerado.
Construir um intervalo de confiança para a proporção de pastilhas com
desgaste acima do tolerado, do atual processo industrial, com nível de con­
fiança de 95%. Interpretar o resultado.
12. Uma fundição produz blocos para motor de caminhões. Os blocos têm fu­
ros para as camisas e deseja-se verificar qual é o diâmetro médio no proces­
so do furo. A empresa retirou uma amostra de 36 blocos e mediu os diâme­
tros de 36 furos (1 a cada bloco). A amostra acusou média de 98,0 mm e
desvio padrão de 4,0 mm. Construir um intervalo de confiança para a mé­
dia do processo, com nível de confiança de 99%. Interpretar o resultado. Se
o processo deveria ter média 100 mm, há evidência (com 99% de confian­
ça) de que a média do processo não está no valor ideal? Explique.

19 2 ESTATÍSTICA
7.4 TAMANHO DE AMOSTRA
Na seção anterior, aprendemos como estimar um parâmetro mediante ob­
servação de uma amostra aleatória simples de tamanho n. A estimação é feita
com certa precisão, no sentido de que também avaliamos o erro amostrai que
podemos estar cometendo.
Contudo, ainda na fase do planejamento da pesquisa, muitas vezes preci­
samos calcular o tamanho n da amostra, para garantir certa precisão desejada,
que é descrita em termos do erro amostrai máximo tolerado (£0,) e do nível de
confiança (y) a ser adotado no processo de estimação. No caso de estimação de
//, podemos exigir
\ X - p \ Z E 0 (7.42)
Usando (7.34), temos:
z , ^ < E 0 (7.43)
vn
Isolando n, temos:
n > — ^ C7-44)
K
O tamanho mínimo da amostra é o menor n que satisfaz a inequação pre­
cedente.
A dificuldade operacional para calcularmos o tamanho da amostra é que o
cálculo depende da variância populacional a 2, que em geral é desconhecida.
Em alguns problemas, c2 pode ser avaliada por meio de estudos anteriores ou
pela experiência do engenheiro; em outras situações, a 2 é obtida de uma amos­
tragem piloto, isto é, alguns elementos da população são examinados e a variân­
cia encontrada nesta amostra piloto é usada no lugar de a 2. Nesse caso, é me­
lhor usar a expressão (7.44) com ty no lugar de zy.
Exemplo 7.5 (continuação) Considere que o pesquisador julgou o resultado
encontrado, lC(pi, 95%) = 36,15 ± 0,53, pouco preciso. Ele tolera um erro
amostrai máximo de 0,3 HRc. Além disso, ele quer realizar as estimações com
nível de confiança de 99%. Qual deve ser o tamanho da amostra?
Solução: Para efetuar o cálculo, é necessário o conhecimento da variân­
cia populacional, a 2. Usaremos, em seu lugar, a variância calculada sobre as
dez observações, isto é s2 = (0,7352)2 « 0,54. Logo,

DISTRIBUIÇÕES AMOSTRAIS E ESTIMAÇÃO DE PARÂMETROS 193
, 6 3 i 3 7 5
E l (0,3)-
Portanto, precisamos de n = 64 corpos de prova para satisfazer a precisão
desejada.
O Quadro 7.1 apresenta o formulário para o cálculo do tamanho da amos­
tra, em função do parâmetro desejado. Quando a população é infinita ou muito
grande, n0 já é o tamanho da amostra. Porém, se N é conhecido e, especialmen­
te, se não for muito grande, devemos dar sequência ao cálculo, conforme indica
a última linha do Quadro 7.1.
Quadro 7.1 Tamanho mínimo de uma amostra aleatória simples.
Parâmetro de interesse Valor inicial do tamanho da amostra
_
2 2
a) uma média (u):
Z G
(7.45)
n° =
b) uma proporção (p):
ü fK i-p )
(7.46)
° Ë Ï
c) várias proporções (pj, p2, ...):
(7.47)
° 4
E l
Tamanho da amostra
População infinita: n = n0 (arredondamento para o inteiro superior) (7.48)
População de R _ N.n0 (arredondamento para o inteiro
tamanho N: N + n0 - 1 superior) (7.49)
Quando o objetivo é estimar uma proporção p (0 < p < 1), podemos usar
a seguinte relação (ver a Figura 7.11):
a = p . ( l - p ) < - (7.50)
2
A primeira parte da relação (7.50) foi usada para construir a expressão de
rz0 em (7.46) (Quadro 7.1b); e a segunda em (7.47) (Quadro 7.1c).

19 4 ESTATÍSTICA
Figura 7.11 0 parâmetro c2 em função do valor da proporção p.
A expressão (7.47) (Quadro 7.1c) também é usada com o objetivo de esti­
mar uma única proporção p, quando não temos informação a priori sobre o va­
lor de p. Contudo, deve resultar em um valor de n maior do que o necessário.
No caso de estarmos usando nível de confiança de 95%, temos z.f = 1,96 « 2,
fazendo com que (7.47) resulte em:
n0 = - ± j (7.51)
A expressão (7.51) é muito usada no planejamento de pesquisas de levan­
tamento, com o objetivo de estimar várias proporções, como nos exemplos se­
guintes:
• numa pesquisa eleitoral, em que é comum a necessidade de avaliar a
proporção de cada candidato;
• em pesquisas de mercado, em que normalmente desejam-se avaliar as
proporções de vários atributos nos consumidores;
• no levantamento de arquivos que trafegam em uma rede, em que é
comum o interesse em verificar a proporção de cada tipo de arquivo.
EXERCÍCIOS
13. Um pesquisador precisa determinar o tempo médio gasto para perfurar três
orifícios em uma peça de metal. Qual deve ser o tamanho da amostra para
que a média amostrai esteja a menos de 15 s da média populacional? Por ex­
periência prévia, pode-se supor o desvio padrão em torno de 40 s. Considere
também, que a estimação será realizada com nível de confiança de 95%.
14. Seja a construção de um plano para garantir a qualidade dos parafusos
vendidos em caixas com 100 unidades. Um dos requisitos é controlar o
comprimento médio dos parafusos. Quer-se saber quantos parafusos de-

DISTRIBUIÇÕES AMOSTRAIS E ESTIMAÇÃO DE PARÂMETROS 195
ve-se examinar em cada caixa, para garantir que a média da amostra Gc)
não difira do comprimento médio dos parafusos da caixa {pi) em mais que
0,8 mm. Considere que a estimação seja realizada com nível de confiança
de 95%. Análises feitas na linha de produção indicam variância em torno
de 2 mm2.
15. Considerando o Exercício 14, mas supondo a caixa com 1.000 parafusos,
qual é o tamanho da amostra necessário?
16. Com o objetivo de avaliar a confiabilidade de um novo sistema de trans­
missão de dados, torna-se necessário verificar a proporção de bits transmi­
tidos com erro em cada lote de 100 Mb. Considere que seja tolerável um
erro amostrai máximo de 2% e que em sistemas similares a taxa de erro na
transmissão é de 10%. Qual deve ser o tamanho da amostra?
a) Use y = 0,95.
b) Use y = 0,99.
EXERCÍCIOS COMPLEMENTARES
17. Sob condições normais, realizaram-se dez observações sobre o tempo de
resposta de uma consulta a certo banco de dados. Os resultados, em segun­
dos, foram:
28 35 43 23 62 38 34 27 32 37
Construa um intervalo de confiança para o tempo médio de uma con­
sulta, sob condições normais. Use y = 0,99.
18. Fixados certos parâmetros de entrada, o tempo de execução de um algorit­
mo foi medido 12 vezes, obtendo-se os seguintes resultados, em minutos:
15 12 14 15 16 14 16 13 14 11 15 13
a) Apresente um intervalo de 95% de confiança para o tempo médio de
execução do algoritmo.
b) Considerando as 12 mensurações como uma amostra piloto, avalie o
número de mensurações (tamanho da amostra) necessário para garan­
tir um erro máximo de 15 segundos (0,25 minutos). Use y = 0,95.
19. Uma empresa tem 2.400 empregados. Deseja-se extrair uma amostra de
empregados para verificar o grau de satisfação em relação à qualidade da
comida no refeitório. Em uma amostra piloto, numa escala de 0 a 10, o
grau de satisfação recebeu nota média 6,5 e desvio padrão 2,0.

19 6 ESTATÍSTICA
a) Determine o tamanho mínimo da amostra, supondo amostragem
aleatória simples, com erro máximo de 0,5 unidade e nível de con­
fiança de 99%.
b) Considere que a amostra planejada no item anterior tenha sido realiza­
da e obteve-se média 5,3 e desvio padrão 1,8 ponto. Construa um in­
tervalo de 99% de confiança para o parâmetro p.
c) Considerando o resultado do item anterior, você diria, com nível de
confiança de 99%, que a nota média seria superior a cinco se a pesqui­
sa fosse aplicada a todos os 2.400 funcionários? Justifique.
d) Realizada a amostra planejada no item (a), suponha que 70 atribuíram
notas iguais ou superiores a cinco. Apresente um intervalo de 90% de
confiança para a porcentagem de indivíduos da população que atribui­
riam notas iguais ou superiores a cinco.
20. Com os dados históricos sobre a temperatura do pasteurizador de um laticí­
nio, sabe-se que a variância é aproximadamente 1,8 (°C)2. Planeja-se fazer
uma amostragem para avaliar o valor médio da temperatura do pasteuriza­
dor. Suponha que as observações sejam feitas sob as mesmas condições e
de forma independente. Qual deve ser o tamanho da amostra, para garan­
tir um erro máximo de 0,3°C, com nível de confiança de 95%?
21. Planeja-se extrair uma amostra aleatória simples dos 2.000 funcionários de
uma empresa, para avaliar a satisfação com o trabalho. A satisfação será
avaliada através de um questionário com vários itens numa escala de 1 a 5.
Pretende-se avaliar o valor médio de cada item. Qual deve ser o tamanho
da amostra para garantir um erro máximo de 0,2 unidade, com nível de
confiança de 95%?
N ota: Use como variância o valor teórico que se obtém ao supor probabi­
lidade igual para cada um dos cinco níveis da escala. Observe que dificil­
mente algum item terá variância maior do que esta que você está calculan­
do, pois, na prática, a tendência é que as respostas se concentrem em torno
de algum nível.
22. Numa pesquisa para estudar a preferência do eleitorado a uma semana da
eleição presidencial, qual deve ser o tamanho de uma amostra aleatória
simples para garantir, com nível de confiança de 95%, um erro amostrai
não superior a 2%?
23. Um analista de sistemas está avaliando o desempenho de um novo progra­
ma de análise numérica. Forneceu como entrada do programa 14 opera­
ções similares e obteve os seguintes tempos de processamento (em milisse-
gundos):
12,0 13,5 16,0 15,7 15,8 16,5 15,0 13,1
15,2 18,1 18,5 12,3 17,5 17,0

DISTRIBUIÇÕES AMOSTRAIS E ESTIMAÇÃO DE PARÂMETROS 1 9 7
a) Calcule a média e o desvio padrão da amostra do tempo de processa­
mento.
b) Construir um intervalo de confiança para o tempo médio de processa­
mento, com nível de confiança de 95%.
c) Qual deve ser o tamanho da amostra para garantir um erro amostrai
máximo de 0,5 milissegundo, na estimação do tempo médio de proces­
samento, com nível de confiança de 99%?
24. Uma unidade fabril da Intel produziu 500.000 chips Pentium IV em certo
período. São selecionados, aleatoriamente, 400 chips para testes.
a) Supondo que 20 chips não tenham a velocidade de processamento ade­
quada, construir o intervalo de confiança para a proporção de chips
adequados. Use nível de confiança de 95%.
b) Verificar se essa amostra é suficiente para obter um intervalo de 99%
de confiança, com erro amostrai máximo de 0,5%, para a proporção
de chips adequados. Caso contrário, qual deveria ser o tamanho da
amostra?

8
Testes de Hipóteses
Muitas vezes o pesquisador tem alguma ideia, ou conjetura, sobre o com­
portamento de uma variável, ou de uma possível associação entre variáveis.
Nesses casos, o planejamento da pesquisa deve ser de tal forma que permita,
com os dados amostrais, testar a veracidade de suas ideias sobre a população
(ou as populações) em estudo. Adotamos que a população seja o mundo real e
as ideias sejam as hipóteses de pesquisa, que poderão ser testadas por técnicas
estatísticas denominadas testes de hipóteses ou testes de significância.
8.1 AS HIPÓTESES
Exemplo 8.1 Seguem alguns exemplos de hipóteses:
a) substituindo o processador A pelo processador B, altera-se o tempo
de resposta de um computador;
b) aumentando a dosagem de cimento, aumenta-se a resistência do
concreto;
c) uma campanha publicitária produz efeito positivo nas vendas;
d) a implementação de um programa de melhoria da qualidade em
uma empresa prestadora de serviços melhora a satisfação de seus
clientes.
Para verificar estatisticamente a veracidade de uma hipótese, precisamos
de um conjunto de dados, observados adequadamente em termos do problema

TESTES DE HIPÓTESES 199
em questão. No Exemplo 8.1 (a), podemos realizar um experimento, fazendo
uma amostra de ensaios com o processador A e uma amostra de ensaios com o
processador B, anotando o tempo de resposta em cada ensaio. Em (b), podemos
fazer uma amostra de corpos de prova com a dosagem de cimento e uma
amostra de corpos de prova com a dosagem d2 de cimento (d2 > d j, medindo a
resistência de cada corpo de prova. Em (c), podemos verificar o nível das ven­
das em vários pontos de venda antes do início da campanha publicitária e, tam­
bém, depois desse evento. Em (d), podemos avaliar o percentual de reclama­
ções antes e depois do programa de melhoria da qualidade.
Levando em conta o planejamento da pesquisa, as hipóteses podem ser co­
locadas de forma mais específica, descritas em termos de parâmetros populacio­
nais. Com respeito ao Exemplo 8.1, temos:
a) a média dos tempos de resposta do equipamento com o processador
A é diferente da média dos tempos de resposta com o processador B;
b) a média dos valores de resistência do concreto com a dosagem d2 de
cimento é maior do que a média dos valores de resistência com a do­
sagem dj;
c) a média das vendas depois da campanha publicitária é maior do que
a média das vendas antes da campanha publicitária;
d) a proporção de reclamações após a realização do programa de melho­
ria da qualidade é menor do que antes da realização do programa.
Observe que, nos três primeiros casos, as hipóteses estão descritas em ter­
mos da comparação de duas médias, enquanto no caso (d), a hipótese está des­
crita em termos da comparação de duas proporções. E, também, no caso (a),
queremos verificar se há diferença entre as duas condições em estudo, enquanto
nos demais casos especificamos na hipótese qual parâmetro deve ser o maior.
Essas diferenças dependem do problema e do planejamento do experimento ou
do levantamento da coleta de dados.
Dado um problema de teste de hipóteses, precisamos formular as chama­
das hipótese nula e hipótese alternativa.
A hipótese nula ou hipótese de trabalho (H0) é a hipótese aceita como
verdadeira até prova estatística em contrário. É o ponto de partida para a análi­
se dos dados. Em geral, ela é formulada em termos de igualdade entre parâme­
tros, ou entre um parâmetro e uma constante. Ela geralmente representa o con­
trário do que queremos provar.1
1 Lembre-se de que a prova, na estatística, não é exata, pois existe probabilidade de in­
corrermos em erro, mas é desejável que essa probabilidade seja pequena e conhecida.

2 0 0 ESTATÍSTICA
Quando os dados mostrarem evidência suficiente de que a hipótese nula
(H0) é falsa, o teste rejeita-a, aceitando em seu lugar a chamada hipótese alter­
nativa (Hi). Em geral, a hipótese alternativa (H{) é formulada em termos de
desigualdades O, < ou >). Ela comumente corresponde ao que se quer provar,
ou seja, corresponde à própria hipótese de pesquisa formulada em termos de pa­
râmetros.
Com respeito ao Exemplo 8.1, temos:
a) Ho: /iA = /iB e
onde: é o tempo médio de resposta com o processador A; e
HB é o tempo médio de resposta com o processador B.
b) H0: ju2 = /li e Hj: fi2 >
onde: fi2 é a resistência média do concreto com a dosagem d2 de ci­
mento; e
pL\ é a resistência média do concreto com a dosagem di de ci­
mento.
c) Hq: pi2 = ixY e Hj: ji2 > pil
onde: fii é o valor médio das vendas antes da campanha publicitá­
ria; e
ju2 é o valor médio das vendas depois da campanha publicitária.
d) H0: p2 = p i e Hx: p2 < p^
onde: p l é a proporção de reclamações antes do programa de me­
lhoria da qualidade; e
p2é a proporção de reclamações depois do programa de me­
lhoria da qualidade.
A decisão em aceitar H0 ou Hi é feita a partir de amostras extraídas ade­
quadamente das populações envolvidas. No caso (d), por exemplo, podemos
observar uma amostra aleatória de clientes atendidos antes do programa de
qualidade e outra amostra aleatória de n2 clientes atendidos depois de implanta­
do o programa. É natural que as proporções de reclamações nas duas amostras
(Pi e p 2) sejam diferentes, mesmo que a hipótese nula (H0: p2 = p i) seja verda­
deira, pois sempre existe o efeito aleatório na seleção das amostras.
A aplicação de um teste estatístico (ou teste de significância) serve para ve­
rificar se os dados fornecem evidência suficiente para que possamos aceitar
como verdadeira a hipótese alternativa (Hj), precavendo-nos, com certa segu­
rança, de que as diferenças observadas nos dados não são meramente casuais.

TESTES DE HIPÓTESES 2 0 1
8.2 CONCEITOS BÁSICOS
Apresentaremos as primeiras ideias sobre testes estatísticos usando como
ilustração um experimento binomial. Considere o seguinte problema:
Verificar se uma moeda, usada num jogo de azar, é viciada.
Chamamos de p a probabilidade de cara dessa moeda. Assim, podemos
formular as hipóteses da seguinte maneira:
H0: p = 0,5 (a moeda é honesta) e H^ p * 0,5 (a moeda é viciada)
Suponha, inicialmente, H0 como verdadeira. Ela somente vai ser rejeitada
em favor de Hx se houver evidência suficiente que a contradiga. A existência
dessa possível evidência será verificada com base num conjunto de observa­
ções do problema em estudo. No presente exemplo, o conjunto de observações
(amostra) consistirá nos resultados de uma série de lançamentos imparciais
da moeda.
Em cada lançamento da moeda, observamos um resultado: cara ou coroa.
Ao observar uma amostra de n lançamentos, podemos computar o valor da es­
tatística:
Y = número total de caras nos n lançamentos
A estatística Y poderá ser usada na definição de um critério de decisão:
aceitar H0 ou rejeitar H0 em favor de Nesse contexto, a estatística Y é chama­
da de estatística do teste.
Vamos considerar uma amostra de n = 10 lançamentos e duas situações:
SITUAÇÃO A: Suponha que, nos 10 lançamentos, observamos Y = 10
caras. Podemos rejeitar H0, em favor de H{>
SITUAÇÃO B: E se tivéssemos observado Y = 7 caras?
Na situação A, é intuitivo que exista mais evidência para rejeitar H0. Con­
tudo, em nenhuma das duas situações, podemos rejeitar H0 com plena certeza
de que essa hipótese é realmente falsa, pois estamos trabalhando com um fenô­
meno aleatório, no qual é plenamente possível, em 10 lançamentos de uma moe­
da sabidamente honesta (H0 verdadeira), ocorrerem 7, 8, 9 ou até mesmo 10
caras. Por outro lado, se a ocorrência de um resultado for muito pouco provável
para uma moeda honesta, torna-se natural decidirmos por H1 (moeda viciada).
No presente contexto, é necessário conhecermos a probabilidade de ocor­
rerem resultados como Y = 10 caras (situação A) ou Y = 7 caras (situação B),
em 10 lançamentos de uma moeda honesta. Como se trata de uma variável
aleatória, precisamos da distribuição de probabilidades da estatística do teste Y,

2 0 2 ESTATÍSTICA
admitindo H0 verdadeira. Essa distribuição de probabilidades será a referência
básica para analisarmos o resultado da amostra e decidirmos entre H0 eH j.
A distribuição de probabilidades de Y: distribuição de referência do teste
Pelas características do experimento, podemos afirmar que Y tem distribui­
ção binomial, com parâmetros n = 10 e p = 0,5 (supondo H0 verdadeira). A Fi­
gura 8.1 apresenta essa distribuição sob forma gráfica. As probabilidades p(y)
foram extraídas da Tabela 1 do apêndice, ou seja, são derivadas da expressão
da distribuição binomial, como visto no Capítulo 5. Para facilitar a exposição,
essas probabilidades foram arredondadas para três decimais.
ikp(y) 0.246
0.205 0.205
0.117 0,117
0.044 0,044
o .o o i^í °-010 0,001
0 1 2 3 4 5 6 7 8 9 10
Figura 8.1 Distribuição da estatística Y = número de caras em 10 lançamentos
da moeda, sob H0 (binomial com n = 10 e p = 0,5).
Com a distribuição de probabilidades da estatística do teste, podemos ava­
liar melhor a adequação de H0 com o resultado de Y, calculado com base na
amostra. A Figura 8.1 mostra que, se H0 for verdadeira, os resultados mais pro­
váveis estão em tomo do valor esperado: n = n.p = 5 caras.
A distribuição de referência do teste identifica a variável aleatória, ou seja,
diz quais resultados são mais prováveis e quais são improváveis. Com base nes­
sa informação, devemos, em seguida, comparar o que ocorreu na amostra (re­
sultado da estatística do teste) com o que esperaríamos que tivesse ocorrido,
considerando a hipótese nula verdadeira.
Valor p
Considerando H0 verdadeira, podemos calcular a probabilidade de obter­
mos, por acaso, um resultado tão ou mais longe do esperado do que aquele que
verificamos na amostra efetivamente observada. A essa probabilidade damos o
nome de probabilidade de significância, ou valor p.

TESTES DE HIPÓTESES 20 3
O valor p (ou probabilidade de significância) é definido como a
probabilidade de a estatística do teste acusar um resultado tão ou mais dis­
tante do esperado, como o resultado ocorrido na particular amostra obser­
vada, supondo H0 como a hipótese verdadeira.2
Exemplo 8.2 Retomemos a situação A, em que observamos Y = 10 caras em
n = 10 lançamentos. Considerando o número esperado de caras sob H0 [pi = 5)
como referência, verificamos que tão ou mais distante do que o valor observado
na amostra (7 = 10) encontram-se o valor 0 e o próprio valor 10, como ilustra
a Figura 8.2.
ikp (y )
3.246
D.205 0,205
3,117 0,117
0,044 0.044
0.001
0.001 ^
0 1 2 3 4 5 6 7 8 9 10
î ï Û
Figura 8.2 Distribuição de Y, sob H0. As setas indicam os valores que distam do
esperado Qà = 5) tão ou mais do que o valor Y =10, observado na
amostra da situação A.
Consequentemente, a probabilidade de significância será:
p =
p ( 0 ) + P ( 1 0 ) = 0 , 0 0 1 + 0 , 0 0 1 = 0 , 0 0 2
Assim, para uma moeda honesta (H0 verdadeira), temos a pequena proba­
bilidade p = 0,002 de ocorrer um resultado tão ou mais distante do valor espe­
rado, como o que, de fato, ocorreu na amostra efetivamente observada (Y = 10
caras). Como 0,002 é uma probabilidade muito pequena, toma-se natural rejei­
tar a hipótese de que a moeda é honesta (H0), decidindo-se pela hipótese de
que a moeda é viciada (H J.
Os dados observados mostram evidência suficiente para dizer que a moeda é
viciada!
2 Esta definição é apropriada para distribuições de referênda simétricas e testes bilaterais
(ver seção 8.5).

2 0 4 ESTATÍSTICA
Exemplo 8.3 Vejamos, agora, a situação B, em que observamos 7 = 7 caras
em n = 10 lançamentos. Nesta situação, tão ou mais distante do que o valor
7 = 7 encontram-se os valores: 7, 8, 9,10, 0, 1, 2 e 3, como ilustra a Figura 8.3.
ilp (y ) 3.246
D,205 0,205
0,117 0,117
0.044 0.044
0,010
0.001 °-010
. . 1 .. . - 1 - .—i— L
0 1 2 3 4 5 6 7 8 9 10 y
ü í ü ü « ff ff ü tf
Figura 8.3 Distribuição de Y, sob H0. As setas indicam os valores que distam do
esperado (/j, = 5) tão ou mais do que o valor Y = 7, observado na
amostra da situação B.
Temos, então, a seguinte probabilidade de significância:
p = p( 0) + p( 1) + p(2) + p(3) + p(7) + p( 8) + p( 9) + p(10) =
= 0,001 + 0,010 + 0,044 + 0,117 + 0,117 + 0,044 + 0,010 +
+ 0,001 = 0,344
Esta segunda situação mostra que, para uma moeda honesta (H0 verdadei­
ra), temos a probabilidade p = 0,344 de ocorrer um resultado tão ou mais dis­
tante do valor esperado, como o que, de fato, ocorreu neste caso ( 7 = 7 caras).
Como 0,344 não é uma probabilidade desprezível, torna-se mais prudente não
rejeitar H0.
N ão há evidência suficiente para afirmar que a moeda é viciada\
O valor p aponta o quão improvável foi o resultado da amostra à luz de H0.
Logo, quanto menor for o valor p, maior a evidência para rejeitar H0. O valor p
também pode ser interpretado como o risco de rejeitarmos incorretamente uma
H0 verdadeira, dada a evidência da amostra. Por exemplo, se afirmássemos que
a moeda é viciada com a evidência de 7 = 7 caras em n = 10 lançamentos, es­
taríamos incorrendo numa probabilidade de 34,4% de estarmos fazendo uma
afirmação errada.
Nível de significância
Na realização de uma pesquisa, quando desejamos confirmar ou refutar al­
guma hipótese, é comum estabelecer, ainda na fase do planejamento da pesqui-

TESTES DE HIPÓTESES 20 5
sa, a probabilidade tolerável de incorrer no erro de rejeitar H0, quando H0 é ver­
dadeira. Este valor é conhecido como nível d e sig nificância d o te ste e é
designado pela letra grega a. É comum adotar nível de significância de 5%, isto
é, a = 0,05. Mas, quando desejamos maior segurança ao afirmar Hly podemos
adotar níveis de significância menores, como a = 0,01.
Estabelecido o nível de significância a, temos a seguinte regra geral de de­
cisão de um teste estatístico:
p > a ooi > aceita Hn
p < a UUL -C> rejeita H0
Exemplo 8.2 (continuação) Na amostra da situação A, quando observamos
10 caras em 10 lançamentos, se estivermos usando o nível de significância de
5% (a = 0,05), o teste estatístico rejeita H0 em favor de Hlf pois a probabilidade
de significância, calculada com base na amostra, foi de 0,002, sendo, portanto,
menor do que o valor adotado para a.
Exemplo 8.3 (continuação) Usando a = 0,05 na amostra da situação B,
quando observamos 7 caras em 10 lançamentos, o teste estatístico não rejeita
H0) pois a probabilidade de significância, calculada com base na amostra, foi de
0,344, que não é menor do que o valor adotado para a.
8.3 TIPOS DE ERRO
Para entendermos os erros associados a um teste de hipóteses, precisa fi­
car claro que estamos avaliando uma afirmação (hipótese) sobre a população.
Essa hipótese pode ou não ser verdadeira, mas nunca saberemos com certeza
sobre a realidade da população, já que conhecemos apenas uma amostra. O que
fazemos é tomar uma decisão, considerando evidências na amostra. Antes de
observarmos a amostra, mas estabelecidas as hipóteses e o nível de significân­
cia a, temos as seguintes possibilidades:
Decisão do teste
Realidade
(desconhecida)
Aceita H0 Rejeita H0
H0 verdadeira Decisão correta (probab = 1 - a) Erro tipo I (probab = a)
H0 falsa Erro tipo II (probab = P) Decisão correta (probab = 1 - (3)

2 0 6 ESTATÍSTICA
Conforme o esquema, os erros tipos I e II podem ocorrer segundo as se­
guintes probabilidades condicionais:
P(erro tipo I) = P(rejeitar H0 \ H0 é verdadeira) = a
P(erro tipo II) = P(aceitar H0 \ H0 é falsa) = p
Usando os eventos complementares, temos as probabilidades de decisão
correta:
P(aceitar H0 \ H0 é verdadeira) = 1 - a e
P(rejeitar H0 \ H0 é falsa) = 1 - p
Como a é fixado a priori, se o teste rejeita H0 em favor de Hx (p < a), o ris­
co de estarmos tomando a decisão errada (erro tipo I) fica limitado pelo nível
de significância a adotado. Dessa forma, temos certa garantia da veracidade de
Hi. Em outras palavras, quando o teste rejeita H0, podemos afirmar (conside­
rando o nível de significância do teste) que é verdadeira.
Por outro lado, se o teste aceita H0 (p > a), não temos muito controle do
risco de estarmos tomando a decisão errada (erro tipo II), pois a probabilidade
P, em geral, não é conhecida. Nesse caso, costumamos dizer apenas que os da­
dos estão em conformidade com a hipótese nula. Isso não implica que H0 seja real­
mente a hipótese verdadeira, mas que os dados não estão mostrando evidência
suficiente para rejeitá-la. Sobre isso, R. A. Fisher, considerado o pai da estatísti­
ca experimental, escreveu:
“A hipótese nula pode ou não ser impugnada pelos resultados de um
experimento. Ela nunca pode ser provada, mas pode ser desaprovada no
curso da experimentação.”
Em razão do exposto, usamos uma linguagem mais enfática para descrever
uma situação em que o teste rejeita H0 (por exemplo, os dados provaram estatis­
ticamente que a moeda é viciada) e uma linguagem mais amena quando o teste
aceita H0 (por exemplo, admite-se que a moeda é honesta, pois os dados não mos­
traram evidência suficiente de que ela é viciada).
8.4 ABORDAGEM CLASSICA
Antes de observar a amostra, mas considerando o planejamento do experi­
mento, podemos montar a regra de decisão em termos da estatística do teste,
do nível de significância e da distribuição de probabilidade da estatística do tes­
te sob H0. Depois, observamos a amostra e tomamos a decisão em função da re­
gra previamente construída.

TESTES DE HIPÓTESES 2 0 7
Retomando o experimento de lançar 10 vezes a moeda, a regra de decisão
para a = 0,05 é construída com base na equação:
P(erro tipo I) = P(rejeitar H0 \ H0 é verdadeira) = a
Se H0 é verdadeira, a distribuição para o número de caras Y é binomial
com n = 1 0 e p = 0,5.Ea região de rejeição de H0 deve estar nas extremidades
dessa distribuição, de tal forma que a probabilidade total não ultrapasse o nível
de significância estabelecido: a = 0,05 (Figura 8.4).3
ilp(y)
3.246
0,205 0,205
0,117 0,117
0,044 0.044
0.010 0.001
--L_ -—1—-_—1— ,
0 1 2 3 4 5 6 7 8 9 10 y
aceita Hn
rejeita H0 rejeita H0
Figura 8.4 Regra de decisão em termos de Y = número de caras em 10 lança­
mentos da moeda, com a = 0,05.
Lançamos a moeda 10 vezes e contamos o número Y de caras. Decidimos
por H0 ou Hi, conforme a regra ilustrada na Figura 8.4, ou seja:
• se ocorrer de 2 a 8 caras, então o teste aceita H0;
• se ocorrer menos de 2 caras ou mais de 8 caras, então o teste rejeita
H0 em favor de Ha.
A abordagem clássica é mais fácil quando o trabalho é realizado sem a aju­
da do computador, usando apenas as tabelas estatísticas. Por outro lado, quan­
do usamos algum software estatístico ou uma planilha eletrônica, o sistema já
calcula a estatística do teste e o valor p, de tal forma que a abordagem discuti­
da na seção 8.2 torna-se mais fácil. Contudo, a decisão sempre será a mesma,
independentemente da abordagem utilizada.
3 Como no presente caso a distribuição do teste é discreta, não existe um valor que satis­
faz exatamente à equação P(erro tipo I) = a. Então, a regra é construída com o maior a que sa­
tisfaça a P(erro tipo I) < a.

2 0 8 ESTATÍSTICA
EXERCÍCIOS
1. Seja p a probabilidade de cara de uma moeda. Sejam H0: p = 0,5 e
p * 0,5. Lança-se 12 vezes esta moeda, observando-se o número de caras.
Usando a tabela da distribuição binomial (Tabela 1 do apêndice), obtenha
a probabilidade de significância para cada um dos seguintes resultados:
a) 1 cara; b) 4 caras; e c) 11 caras.
2. Adotando o nível de significância de 5%, qual é a conclusão do teste em
cada item do Exercício 1?
3. Sejam 15 lançamentos de uma moeda. Considerando as hipóteses H0, a
moeda é honesta, e Hl} a moeda é viciada, e o nível de significância de 1%,
apresente a regra de decisão (abordagem clássica) em termos da estatística
Y = número de coroas.
4. É possível, para uma mesma amostra, aceitar H0 ao nível de significância
de 1%, mas rejeitá-la ao nível de 5%? E o inverso? Exemplifique.
5. Para verificar as hipóteses de seu trabalho, um pesquisador fez vários testes
estatísticos (um para cada hipótese de pesquisa), adotando para cada teste
o nível de significância de 5%. Responda os seguintes itens:
a) Num dado teste, o valor p foi 0,0001. Qual deve ser a conclusão (deci-
de-se pela hipótese nula ou pela hipótese alternativa)? Qual é o risco
de o pesquisador estar tomando a decisão errada?
b) Em outro teste, o valor p foi 0,25. Qual deve ser a conclusão? Nesse
caso, você consegue avaliar o risco de o pesquisador estar tomando a
decisão errada?
c) Em outros dois testes, as probabilidades de significância foram de
0,0001 e 0,01, respectivamente. Em qual dos testes o pesquisador deve
estar mais convicto na decisão de qual hipótese deve ser escolhida?
Por quê?
8.5 TESTES UNILATERAIS E BILATERAIS
No exemplo discutido no tópico anterior, rejeita-se H0: p = 0,5, em favor
de Hi'. p * 0,5, tanto quando ocorre um valor muito pequeno, quanto muito
grande de caras. Essa é uma situação típica de teste bilateral.
Existem situações em que pretendemos rejeitar H0 somente em um dos
sentidos. Por exemplo, suspeitamos que a moeda tende a dar mais caras do que
coroas. Nesse caso, sendo p a probabilidade de ocorrer cara, o teste pode ser
formulado da seguinte maneira:

TESTES DE HIPÓTESES 2 0 9
H0: p = 0,5 (a moeda é honesta) e
Hi’. p > 0,5 (a moeda tende a dar mais caras do que coroas).
Com essas hipóteses, só faz sentido rejeitar H0, em favor de Hi, se na
amostra ocorrer um número significativamente maior de caras do que de coroas,
resultando no que chamamos de teste unilateral. Assim, nos testes unilaterais, a
probabilidade de significância é computada em apenas um dos lados da distri­
buição de referência.
Exemplo 8.4 Considere que, para testar H0: p = 0,5 contra H^. p > 0,5, te­
nhamos lançado a moeda n = 10 vezes e observado Y = 7 caras. A probabilida­
de de significância será:
p = p(7) + p ( 8) + p(9) + p(10) = 0,117 + 0,044 + 0,010 + 0,001 =
= 0,172
que corresponde à metade da probabilidade de significância do teste bilateral,
discutido no Exemplo 8.3. Com o nível de significância de 5%, o teste não rejei­
ta H0. A Figura 8.5 ilustra a probabilidade de significância desse teste.
0.246
‘ P(y)
0.205 0,205
0,117 0.117
0.044 0,044
0.010 0.001
0.001 ^ .
L-------►
0 1 2 3 7 8 9 10 y
f l f l f l f l
Figura 8.5 Ilustração do cálculo da probabilidade de significância do teste unila­
teral do Exemplo 8.4.
Uso da abordagem clássica
Se usarmos a abordagem clássica, com a = 0,05, montamos a seguinte re­
gra de decisão antes de observarmos a amostra:4
4 Note que P(Y > 9) = 0,011 < 0,05; já P(Y > 8) = 0,055, superando o nível de signifi­
cância adotado (a = 0,05). Assim, nove caras deve estar na região de rejeição e oito caras na re­
gião de aceitação de H0.

2 1 0 ESTATÍSTICA
• Se ocorrer oito ou menos caras, então o teste aceita H0.
• Se ocorrer mais de oito caras, então o teste rejeita H0 (aceita H J.
Exemplo 8.5 Com o objetivo de testar se a diferença de odor em sorvetes de
morango é percebida por degustadores, efetuou-se um experimento, como des­
crito a seguir.
Para cada um dos oito degustadores selecionados para o experimento, fo­
ram dadas, em ordem aleatória e sem identificação, duas amostras de sorvete:
uma com odor mais forte e outra normal. As amostras de sorvete foram elabo­
radas de forma tão similar quanto possível, com exceção da intensidade de
odor, que é a característica em estudo.
Chamando de p a probabilidade de o degustador acusar corretamente a
amostra de sorvete com odor mais intenso, temos interesse em testar as seguin­
tes hipóteses:
H0: p = 0,5 (o degustador chuta a resposta, isto é, o odor mais intenso
não é detectado) e
Hii p > 0,5 (existe uma tendência de o degustador perceber o sorvete
que tem o odor mais intenso).
Seja Y o número de degustadores que indicam corretamente o sorvete com
odor mais intenso. Pelas características do experimento, podemos deduzir que,
se H0 for correta, a estatística Y tem distribuição binomial com n = 8 e p = 0,5.
Os resultados do experimento mostraram que, dos oito degustadores, seis
indicaram corretamente o sorvete de odor mais intenso (7 = 6). Usando a dis­
tribuição binomial (Tabela 1 do apêndice), podemos computar a probabilidade
de significância:
p = p(6) + p(7) + p(8) = 0,109 + 0,031 + 0,004 = 0,144
Assim, se estamos trabalhando com o nível de significância de 5% (a = 0,05),
a hipótese nula não pode ser rejeitada. Portanto, concluímos que os dados re­
sultantes do experimento são insuficientes para se afirmar que a diferença de
odor em sorvetes de morango seja percebida pelos degustadores.
EXERCÍCIOS
6 . Para cada um dos itens do Exemplo 8.1, descrever qual a abordagem (uni­
lateral ou bilateral) que é mais apropriada.
7. Para cada um dos itens a seguir, apresente as hipóteses nula e alternativa,
indicando qual é a abordagem (unilateral ou bilateral) mais adequada.

TESTES DE HIPÓTESES 2 1 1
a) Um método de treinamento tende a aumentar a produtividade dos fun­
cionários.
b) A velocidade de um veículo num percurso é, em média, menor do que
o valor anunciado.
c) Dois métodos de treinamento tendem a produzir resultados diferentes
na produtividade.
8. Seja p a probabilidade de cara de uma moeda. Sejam H0: p = 0,5 e Hii
p < 0,5. Lança-se 12 vezes essa moeda, observando-se o número de caras.
Usando a tabela da distribuição binomial (Tabela 2 do apêndice), obtenha
a probabilidade de significância para cada um dos seguintes resultados:
a) 1 cara b) 4 caras c) 6 caras
Usando nível de significância de 5%, em quais resultados o teste rejeita H0?
9. Sejam 11 lançamentos de uma moeda. Considerando as hipóteses H0: a
moeda é honesta e Hii a moeda tende a dar mais cara do que coroa e o nível
de significância de 1%, apresente a regra de decisão em termos da estatísti­
ca Y = número de coroas.
10. Para testar se uma criança tem algum conhecimento sobre determinado as­
sunto, elaboraram-se 12 questões do tipo certo-errado. A criança acertou
11. Qual é a conclusão ao nível de significância de 5%?
11. Para testar se uma criança tem algum conhecimento sobre determinado as­
sunto, elaboraram-se 12 questões, cada uma com 4 possibilidades de esco­
lha. A criança acertou 5.
a) Formule as hipóteses em termos do parâmetro p = probabilidade de
acerto de cada questão.
b) Qual é o número esperado de acertos sob H0?
c) Qual é o valor p?
d) Qual é a conclusão ao nível de significância de 5%?
8.6 APLICAÇÃO DE TESTES ESTATÍSTICOS
Formulada uma pergunta ou hipótese, o pesquisador precisa planejar a cole­
ta de dados e um teste estatístico adequado à situação. Os testes diferenciam-se,
basicamente, pelo tipo de problema que pretendemos resolver e pelo tipo de
dados que temos ou que planejamos coletar. Com respeito aos tipos de dados,
existem testes voltados para dados quantitativos, em que normalmente as hipó­
teses são apresentadas em termos de médias; e testes voltados para dados quali-

2 1 2 ESTATÍSTICA
tativos, em que as hipóteses são apresentadas em termos de proporções ou pro­
babilidades de eventos.
Em geral, na aplicação de um teste estatístico, devemos saber:
a) formular H0 e Hi em termos de parâmetros populacionais;
b) como obter a estatística do teste (no exemplo da moeda, Y = núme­
ro de caras);
c) qual é a distribuição de referência adequada para calcular o valor p
(no exemplo da moeda é a distribuição binomial);
d) quais as suposições básicas para o uso do teste escolhido (no exem­
plo da moeda, supusemos que os lançamentos da moeda foram im­
parciais e realizados sob as mesmas condições).
A decisão do teste estatístico é feita pela comparação do valor p com o ní­
vel de significância a preestabelecido, ou seja:
p > a U LI L C > aceita
p < a UUI rejeita H0
----------------
Se for usada a abordagem clássica, no passo (c), ao invés de calcular o va­
lor p, buscamos um valor crítico tabelado, em função do nível de significância
adotado a priori. A decisão é feita comparando o valor da estatística do teste,
calculado com base na amostra observada, com o valor crítico.
A conclusão resultante de um teste estatístico depende da aplicação em
questão. Por exemplo, num estudo experimental, normalmente a decisão do
teste implica uma relação de causa e efeito, mas, num estudo de levantamento,
o resultado do teste usualmente leva apenas a uma conclusão de diferença en­
tre grupos.
Hoje, o cálculo da estatística do teste e a obtenção do valor p tornaram-se
tarefas relativamente fáceis com o auxílio do computador. Ou seja, o pesquisa­
dor não mais precisa ter habilidades em cálculos algébricos para realizar testes
estatísticos. Por outro lado, a análise do problema de pesquisa, o planejamento
da coleta dos dados, a escolha do teste estatístico adequado, a verificação das
suposições e a correta interpretação do resultado estatístico exigem conheci­
mento e raciocínio lógico.
8.7 TESTE PARA PROPORÇÃO
O teste para proporção é aplicado em situações nas quais queremos veri­
ficar se a proporção de algum atributo na população pode ser igual a certo va-

TESTES DE HIPÓTESES 2 1 3
lor p0. No caso de o problema sugerir um teste bilateral, as hipóteses terão a
forma:
H0: p = po e Hi: p * p0
No caso de teste unilateral, a hipótese alternativa seria H /: p > p0 (unila­
teral à direita) ou Hx”: p < p0 (unilateral à esquerda).
Suponha que a amostragem ou o experimento garanta as suposições de
um experimento binomial.5 No caso de a amostra ser pequena, podemos fazer o
teste usando a própria distribuição binomial, conforme ilustrado com o exemplo
da moeda nas seções anteriores. Nessa seção, enfatizaremos o caso em que a
amostra é suficientemente grande para garantir a aproximação normal, ou seja,6
n.po > 5 e (8.1)
71.(1 - Po) > 5 (8.2)
Seja:
y número de elementos com o atributo de interesse
P = - = --------------------------------------------------------------- (8.3)
n n
a proporção do atributo de interesse, na amostra observada. O cálculo da esta­
tística do teste pode ser feito por:
. P - P o - . y ~ n p ° (8.4)
P o - Q - P o ) \ln ' P 0 ( l ~ P 0)
n
onde: p0 é o valor da proporção, segundo H0;
n é tamanho da amostra;
y é o número de elementos com o atributo de interesse, na amostra; e
p é a proporção de elementos com o atributo de interesse, na amostra.
É recomendável o uso da correção de continuidade, fazendo
y = y - 0,5 se y > n-p0; ou (8.5)
y = y + 0,5 sey < n-p0 (8.6)
5 Ver Capítulo 5.
6 Ver seção 6.4.1.

2 1 4 ESTATÍSTICA
Assim, o cálculo da estatística do teste deve ser feito por:
y'2_n 'Po
z = (8.7)
V” ' Po ■ (! - Pü)
Abordagem do valor p. O processo segue o esquema descrito abaixo:
Cálculo de z Obtenção de p pela
AmnçtTP nm------------------ nm------------------
por (8.7) tabela da normal
Com o auxílio de uma tabela da distribuição normal padrão, obtemos a
área acima de \z\. Se o teste for unilateral e a relação entre p e p0 for coerente
com Hi, então esta área já é o valor p.7 Se o teste for bilateral, o valor p corres­
ponde ao dobro da área da cauda superior (veja Figura 8.6).
unilateral à direita unilateral à esquerda bilateral
Figura 8.6 Abordagem do valor p: regra de decisão de testes estatísticos usando o
modelo normal padrão.
A regra de decisão, como em todo teste estatístico feito com a abordagem
do valor p, é dada por:
p > a uui------------- aceita H0
p < a UUL------------- O rejeita H0
Abordagem clássica. O processo segue o esquema descrito abaixo:
Nível de Obtenção do valor Cálculo do valor z
significância ooc c> crítico zc pela tabela da OOC c > com base na amostra
a distribuição normal (Expressão 8.7)
7 Se o teste for unilateral à direita e p < p0, então não é necessário seguir em frente (o
teste aceita H0). O mesmo acontece quando o teste for unilateral à esquerda e p > p0.

TESTES DE HIPÓTESES 2 1 5
Após a formulação das hipóteses e fixado o nível de significância a, pode­
mos construir a regra de decisão, conforme mostra a Figura 8.7 e Tabela 8.1.
unilateral à direita unilateral à esquerda bilateral
0 zc
aceita
Figura 8.7 Abordagem clássica: regra de decisão de testes estatísticos usando o
modelo normal padrão.
Tabela 8.1 Valores usuais de zC) obtidos da distribuição normal padrão.
teste bilateral, a: 0,20 0,10 0,05 0,02 0,01 0,005
teste unilateral, a: 0,10 0,05 0,025 0,01 0,005 0,0025
valor crítico (zc): 1,282 1,645 1,960 2,326 2,576 2,807
Com os dados da amostra, calculamos o valor de z, relativo à estatística do
teste, e tomamos a decisão em termos da regra apropriada, conforme descrito
na Figura 8.7.
Exemplo 8.6 Uma empresa retira periodicamente amostras aleatórias de 500
peças de sua linha de produção para análise da qualidade. As peças da amostra
são classificadas como defeituosas ou não, sendo que a política da empresa exi­
ge que o processo produtivo seja revisto se houver evidência de mais que 1,5%
de peças defeituosas. Na última amostra, foram encontradas nove peças defei­
tuosas. Usando nível de significância de 1%, o processo precisa ser revisto?
Formulação das hipóteses: Como estamos procurando evidência de que a
proporção de peças defeituosas é superior a 1,5%, é natural realizar um teste
unilateral à direita, ou seja:
H0: p = 1,5% (po = 0,015)
Hx:p > 1,5%
Cálculo da estatística do teste: Como foi observada uma amostra de n = 500
peças, donde foram encontradas y = 9 defeituosas, temos a proporção de peças
defeituosas na amostra:

2 1 6 ESTATÍSTICA
p = — = 0,018
500
Os critérios para a aproximação normal são válidos, pois
n.p0 = (500).(0,015) = 7,5 e
n.(l -po) = (500).(0,985) = 492,5
satisfazendo às condições (8.1) e (8.2). Como o valor da proporção amostrai p
é superior ao descrito por H0 (p 0 = 0,015), a correção de continuidade é dada
pory’ = y - 0,5 = 8,5 (ver Expressão 8.5). Logo:
y - n - P o _ 8,5-(500)-(0,015) _ 1 , , 037
\jn Po- a - p 0) v (500) • (0,015) • (1 - 0,015) 2,718 ~
Solução pela abordagem do rnlor p: Usando a
tabela normal padrão (Tabela 3 do apêndice), en­
contramos área na cauda superior igual a 0,3557.
= 0,3557
Como o teste é unilateral, este já é o valor da proba­
(tabela)
bilidade de signifícância (p = 0,3557), o qual é
maior que o nível de signifícância adotado (a = 0,01). 0 z = 0,37
Então, o teste aceita H0. Veja a figura ao lado. Amostra -;/
Solução pela abordagem clássica: O teste é unilateral
à direita e foi adotado o nível de signifícância a = 0,01.
a = 0,01
Pela tabela da distribuição normal padrão, o valor crí­
tico é zc = 2,326 (ver Tabela 8.1). Como a amostra
0 z — 2,326
acusou o valor z = 0,37, o qual está na região de acei­
(tabela)
tação, o teste aceita H0. Veja a figura ao lado.
aceita Hc
rejeita H0
Qualquer que seja a abordagem, o teste mostra
que n ão há evidência de que a verdadeira proporção de peças defeituosas su­
perou 1,5%. Como consequência, chegamos à conclusão de que não há provas
estatísticas suficientes para recomendar a revisão do processo produtivo.
EXERCÍCIOS
12. Refaça os cálculos do Exercício 1, usando a distribuição normal. Compare
os resultados.

TESTES DE HIPÓTESES 2 1 7
13. Seja p a probabilidade de coroa de uma moeda. Com o objetivo de testar
H0: p = 0,5 contra p > 0,5, fizeram-se 50 lançamentos dessa moeda,
obtendo-se 31 coroas.
a) O teste rejeita H0 ao nível de significância de 5%?
b) E se estivéssemos trabalhando com o nível de significância de 1%?
14. Com o objetivo de verificar se uma moeda está viciada, decide-se lançá-la
várias vezes de forma imparcial e sempre sob as mesmas condições.
a) Se em 8 lançamentos obtiverem-se 2 caras (e 6 coroas), qual é a con­
clusão ao nível de significância de 5%?
b) Se em 80 lançamentos obtiverem-se 20 caras (e 60 coroas), qual é a
conclusão ao nível de significância de 5%?
15. Para testar se um sistema computacional “inteligente” adquiriu algum co­
nhecimento sobre determinado assunto, elaboraram-se 60 questões do tipo
certo-errado. O sistema acertou 40. Qual é a conclusão ao nível de signifi­
cância de 5%?
16. Um experimento computacional foi repetido 40 vezes. O sistema A mos-
trou-se superior ao sistema B em 24 das 40 repetições. Há evidência sufi­
ciente para dizer que os sistemas têm desempenhos diferentes? Use a = 5%.
17. Um fabricante garante que 90% de seus itens estão dentro das especifica­
ções. Um comprador examinou uma amostra aleatória de 50 itens e verificou
que apenas 84% estavam dentro das especificações. Há evidência de que o
nível de qualidade é menor do que o alegado pelo fabricante? Use a = 1%.
8.8 TESTE PARA MÉDIA
O teste para média é aplicável nas situações em que queremos verificar se
uma variável na população pode ser considerada, em média, igual a certo valor
yU0. No caso de o problema sugerir um teste bilateral, as hipóteses terão a forma:
H0: /*= fiio e
No caso de teste unilateral, a hipótese alternativa seria H^: fx > /â0 (unila­
teral à direita) ou H /’: ^ < /ã0 (unilateral à esquerda).
Consideraremos duas situações:
• quando existe alguma informação externa aos dados sobre a variância
o2 da variável em estudo, na população (variância conhecida); e
• quando não há essa informação (variância desconhecida).

2 1 8 ESTATÍSTICA
8.8.1 Caso de variância conhecida
Suponha que seja planejada uma amostragem aleatória da população de
interesse. Considere que a amostra seja razoavelmente grande (n > 30) para va­
ler o teorema do limite central; ou que os dados provenham de uma distribui­
ção aproximadamente normal. O cálculo da estatística do teste é realizado por:
z = (8.8)
a
onde: /í0 é o valor da média segundo H0;
n é o tamanho da amostra;
cj é o desvio padrão populacional; e
x é a média da amostra.
Com os dados da amostra, calculamos x ez. Seja \z\ o valor absoluto de z.
Com o auxílio de uma tabela da distribuição normal padrão, obtemos a área
acima de \z\, dada por 1 - 0 ( |z|). Se o teste for unilateral e a relação entre x e
fx0 for coerente com Hlf então essa área já é o valor p.8 Se o teste for bilateral, o
valor p corresponde ao dobro da área da cauda superior (veja a Figura 8.6).
Obtido o valor p, temos a regra de decisão:
Se p < a, então o teste rejeita H0;
caso contrário, o teste aceita H0.
Alternativamente, podemos usar a abordagem clássica. Com os dados da
amostra, calculamos a estatística z e tomamos a decisão em termos da regra
da Figura 8.7.
Exemplo 8.7 Na indústria cerâmica, avalia-se sistematicamente a resistência
de amostras de massas cerâmicas, após o processo de queima. Dessas avalia­
ções, sabe-se que certo tipo de massa tem resistência mecânica aproximada­
mente normal, com média 53 MPa e variância 16 MPa2. Após a troca de alguns
fornecedores de matérias-primas, deseja-se verificar se houve alteração na qua­
lidade. Uma amostra de 15 corpos de prova de massa cerâmica acusou média
igual a 50 MPa. Qual é a conclusão ao nível de significância de 5%?
Realizaremos um teste bilateral, porque antes de a amostra ser observada,
não sabíamos se a resistência deveria ser maior ou menor que 53. Assim,
8 Se o teste for unilateral à direita e x <fi0, então não é necessário seguir em frente (o teste acei­
ta //,j). Da mesma forma, quando o teste for unilateral à esquerda e x > fi0.

TESTES DE HIPÓTESES 2 1 9
H0: ^ = 53 MPa (w0 = 53)
Hii li * 53 MPa
Cálculo da estatística do teste:
_ ( 5 0 - 5 3 ) - ^ 29Q
a -JÍ6
Solução pela abordagem do valor p: Usando a ta­
bela normal padrão, encontramos área na cauda supe­
2.(0,0019)
rior igual a 0,0019. Como o teste é bilateral, a proba­
(tabela)
bilidade de significância é o dobro deste valor [p =
= 2.(0,0019) = 0,0038], que é menor do que a = 0,05.
-2,90 0 2 = 2,90
Portanto, o teste rejeita H0. Veja a figura ao lado.
amostro
Solução pela abordagem clássica: Encontramos,
na tabela normal padrão, o valor crítico zc = 1,96
(ver Tabela 8.1). Como a amostra acusou o valor
z = - 2,90, o qual está na região de rejeição, o
teste rejeita H0. Veja a figura ao lado.
(tabela)
rejeita H„aceita H° rejeita H„
Como consequência do resultado do teste estatístico, chegamos à conclu­
são de que h á evidência de redução na resistência média da massa cerâmica.
8.8.2 Caso de variância desconhecida
Uma situação mais comum ocorre quando não se tem informação sobre a
variância. Nesse caso, a variância é estimada com base nos dados da amostra e
o cálculo da estatística do teste é feito por:
(8.9)
onde: ju0 é o valor da média, segundo H0;
n é o tamanho da amostra;
x é a média da amostra; e
s é o desvio padrão da amostra.

2 2 0 ESTATÍSTICA
Para esse teste, a distribuição de referência é a t de Student com gl = n - 1
graus de liberdade (Tabela 4 do apêndice).9 Para a validade do teste, supõe-se
que os dados provenham de uma distribuição aproximadamente normal, espe­
cialmente quando n < 30.
A realização do teste é feita de forma análoga aos casos anteriores, mas
usando t no lugar de z, para se obter o valor p; ou tc no lugar de zCi para estabe­
lecer a regra clássica de decisão.
Exemplo 8.8 O tempo para transmitir 10 MB em determinada rede de com­
putadores varia segundo um modelo normal, com média 7,4 s e variância 1,3
s2. Depois de algumas mudanças na rede, acredita-se numa redução no tempo
de transmissão de dados, além de uma possível alteração na variabilidade. Fo­
ram realizados 10 ensaios independentes com um arquivo de 10 MB e foram
anotados os tempos de transmissão, em segundos:
6,8 7,1 5,9 7,5 6,3 6,9 7,2 7,6 6,6 6,3
Existe evidência suficiente de que o tempo médio de transmissão foi redu­
zido? Use nível de significância de 1%.
As hipóteses são:
H0: fx = 7,4 s
Hx: fx < 7,4 s
Considerando que a variabilidade possa ter sido alterada, vamos usar a va­
riância da amostra. Fazendo os cálculos com as 10 observações, temos: x = 6,82
e s = 0,551 (ver Expressões 3.4 e 3.8). E o cálculo da estatística do teste:
t (6,82 - 7,4) • y/lÕ
s 0,551
Temos gl = n - 1 = 9 . Como a tabela fornece áreas na cauda superior e a
distribuição t de Student é simétrica, usaremos o valor absoluto de t, ou seja:
| t | = 3,33.
Solução pela abordagem do valor p: Através da
distribuição t de Student com gl = n - 1 = 9, deve­
7
mos encontrar o valor p, como ilustra o esquema ao =
(tabela)
lado. A Tabela 4 do apêndice permite obter este valor
apenas de forma aproximada. Veja o esquema abaixo.
0 kl =3,33
Amostra ^
9 Para n > 50, as distribuições t de Student e normal padrão são bastante parecidas e, portanto,
pode ser usada qualquer das duas.

TESTES DE HIPÓTESES 2 2 1
dados Área na cauda superior
observados
1 gl 0,25 ... 0,01 0,005 0,0025
• ■ •
1 t
m m m
0,703 ... 2,821 3,250 'Ny//3,690
1 t 1 = 3,33
► • ■ •
9
• • •
Ou seja, o valor | t | = 3,33 aponta para uma área na cauda superior en­
p,
tre 0,0025 e 0,005. Como o teste é unilateral, essa área é o próprio valor isto
p p
é, 0,0025 < < 0,005. E como < a = 0,01, o teste rejeita H0 em favor de H\.
Solução pela abordagem clássica: o teste é unila­
teral e foi adotado o nível de significância a = 0,01.
Assim, encontramos, na tabela da distribuição t, o valor
crítico tc = 2,821. Como a amostra acusou | t | = 3,33,
0 íc = 2,821
o qual está na região de rejeição, o teste rejeita H0 em ____________I (tabela)
favor de Hi. Veja a figura ao lado.10
aceitaíí‘ rejeitaít.
Como consequência do resultado do teste estatístico, chegamos à conclu­
são de que houve redução no tempo médio de transmissão com as alterações na
rede de computadores.
EXERCÍCIOS
18. Em certo banco de dados, o tempo para a realização das buscas é aproxi­
madamente normal, com média de 53 s e desvio padrão de 14 s. Depois de
realizadas algumas modificações no sistema, observou-se que, em 30 con­
sultas, o tempo médio caiu para 45 s. Há evidência de melhora? Admita
que as 30 observações possam ser consideradas uma amostra aleatória e
que não houve alteração na variância. Use a = 1%.
19. Certo tipo de pneu dura, em média, 50.000 km. O fabricante investiu em
uma nova composição de borracha para pneus. Vinte pneus, fabricados
com essa nova composição, duraram, em média, 55.000 km, com desvio
padrão de 4.000 km. Supondo que a durabilidade dos pneus segue uma
distribuição aproximadamente normal, verificar se os dados provam que os
novos pneus são mais duráveis. Use a = 1%.
10 Embora o teste seja unilateral à esquerda, usamos o valor de t em módulo, o que permitiu fazer
a comparação do lado direito, em conformidade com a Tabela 4.

2 2 2 ESTATÍSTICA
8.9 TESTE PARA VARIÂNCIA
Muitas vezes, há interesse em verificar possíveis alterações na variabilida­
de. Nesses casos, o teste pode ser feito com as hipóteses:
e a 2 *
H q: g 2 = g [2) H ii
No caso de teste unilateral, a hipótese alternativa seria > c \ (unila­
H^: g 2
teral à direita) ou ”: g 2 < a 2 (unilateral à esquerda).
A estatística do teste é calculada por:
(8.10)
onde:
g I é a variância segundo H0;
n é o tamanho da amostra; e
s2 é a variância da amostra.
Desde que os dados possam ser assumidos com distribuição normal, a dis­
tribuição de referência para o teste é a distribuição qui-quadrado com gl = n - 1
(Tabela 5 do apêndice). Um cuidado adicional é que a distribuição qui-qua-
drado não é simétrica, ou seja, a relação entre área na cauda e valor da abscissa
precisa ser feita em cada lado da distribuição.
Exemplo 8.8 (continuação) Existe evidência suficiente de que as mudanças
na rede de computadores alteraram a variabilidade no tempo de transmissão de
dados? Use nível de significância de 5%.
As hipóteses são:
H0: = 1,3
G2
Hj: a 2 * 1,3
Como uma amostra de 10 observações produziu a variância s2 = 0,304,
temos:
_ ( n - l ) - s 2 _ 9 *(0,304) _
a 2 1,3

TESTES DE HIPÓTESES 2 2 3
Abordagem clássica: para construir a regra de decisão, precisamos obter os
pontos críticos (x í e os quais separam áreas iguais a ^ em cada cauda
da distribuição. Usando a Tabela 5 do apêndice, obtemos %2cl =2,700 e
%]2 =19,023. Veja a Figura 8.8.
rejeita H0 aceita rejeita Hn
Figura 8.8 Regra de decisão de um teste bilateral usando o modelo qui-quadrado
com gl = 9.
Como o resultado da estatística do teste (q2 = 2,10) cai na região de rejei­
ção, o teste rejeita H0 em favor de Hi. Ou seja, as mudanças realizadas na rede
de computadores, além de reduzirem o tempo médio de resposta, também re­
duziram a variabilidade.
Abordagem do valor p: Podemos observar na Tabela 5 que o valor q2 = 2,10
separa cerca de 1% de área na cauda inferior. Considerando que o teste é bila­
teral, temos p * 2%. Como p < a = 5%, o teste rejeita H0.
EXERCÍCIOS
20. Usuários de uma rede de transmissão de energia elétrica têm reclamado da
alta variação na tensão (desvio padrão de 12 V). A empresa encarregada
da transmissão de energia elétrica na região instalou novos transformado­
res. O desvio padrão calculado sobre 30 observações independentes foi de
8 V e a distribuição de frequências dos valores da amostra sugere uma
distribuição normal. Há evidência de redução na variação da tensão? Use
a = 5%.
21. Com respeito ao Exercício 18, suponha que, nas 30 observações, o desvio
padrão do tempo para a realização das buscas no banco de dados foi de 12
s. Há evidência de alteração na variância? Use a = 1%.

2 2 4 ESTATÍSTICA
8.10 PODER DE UM TESTE E TAMANHO DA AMOSTRA
Como discutido anteriormente, em um teste de hipóteses temos as seguin­
tes possibilidades:
Decisão do teste
Realidade
(desconhecida)
Aceita H0 Rejeita H0
H0 verdadeira Decisão correta (probab = 1 - a) Erro tipo I (probab = a)
Hq falsa Erro tipo II (probab = p) Decisão correta (probab = 1 - p)
Fixado o nível de significância a e construída a regra de decisão do teste,
podemos estudar P(erro tipo II) = P(aceitar H0 \ H0 é falsa) = p.
Vamos reconsiderar o Exemplo 8.7, onde tínhamos as hipóteses:
H0: ii = 53 e Hx: fi * 53
e, com base na estatística
_ ( X - ^o) • Æ
z = (8.11)
construímos a regra de decisão ao nível de significância de 5%:
-1,96 0 1,96
aceita Hfí
rejeita H0 rejeita H0
Analogamente, a regra de decisão pode ser colocada em termos da estatís­
tica X. De (8.11), podemos obter os valores críticos por:
=Mo
(8.12)
Vn
Em termos do Exemplo 8.7, onde n = 15, a = 4 e a = 0,05, temos os valo­
res críticos:
x cl = 53 -1,96 • -%= = 50,975 e x c2 = 53 +1,96 ■ = 55,024
•JÏ5 ■JÎ5

TESTES DE HIPÓTESES 22 5
Assim, a regra de decisão para x é dada por:
50,975 53 55,024
rejeita H0 rejeita H0
Vamos considerar que a verdadeira média seja ^ = 56; portanto, H1é a hi­
pótese verdadeira. Nesse caso, a probabilidade de se cometer o erro tipo II é
dada por fí = P(aceitar H0 \ n = 56), ou seja,
p = P{50,975 < X < 55,024 | fi = 56} =
\ (50,975 - 56) -JÍ5 ( X - 5 6 ) • vn ( 5 5 ,0 2 4 - 5 6 ) - ^
4 a 4
= P{- 4,865 < Z < - 0,945} = <D(- 0,945) - <P(- 4,865) * 0,17
Definimos p o d e r de um teste estatístico como a probabilidade de o teste
rejeitar H0 quando H0 é realmente falsa, ou seja, o poder de um teste é igual
a 1 - p.
No Exemplo 8.7, se na realidade = 56, o poder de o teste detectar que
H0 é falsa é dado por
1 _ p * i _ o,17 = 0,83
conforme ilustra a Figura 8.9.
H0 verdadeira H- verdadeira
Üi = 53) ’0a = 56)
rejeita H0 ace*ta rejeita H0
Figura 8.9 Ilustração do poder do teste do Exemplo 8.7, considerando a = 5% e
|A = 56.

2 2 6 ESTATÍSTICA
Mas a hipótese alternativa não é especificamente fx = 56, mas Hx: fx * 53.
E, para cada valor de fx, o poder do teste (1 - ß) terá um valor diferente. Ou
seja, o poder de um teste é, na verdade, uma função do parâmetro fx.n A Figura
8.10 ilustra curvas de poder de um teste bilateral.
1,0
0,01------------------------------------------------- ------
49 50 51 52 53 54 55 56 57
valor verdadeiro do parâmetro média
Figura 8.10 Curvas de poder do teste do Exemplo 8.7 para n = 15 e n = 30,
considerando a = 5%.
Para o teste de média, o poder do teste depende da diferença ^ - / 0, do ta­
1
manho da amostra n, do tipo de teste (se bilateral ou unilateral) e do nível de
significância a adotado. Observamos na Figura 8.10 que o poder do teste au­
menta à medida que o verdadeiro parâmetro se distancia do valor alegado por
H0 e, também, quando se aumenta o tamanho da amostra. Dessa forma, se fi­
xarmos o poder desejado para certo afastamento em relação ao alegado por H0,
podemos calcular o tamanho da amostra necessário.
Teste para m édia com variância conhecida
Seja a distância entre a verdadeira média (a) e o valor alegado por H0, em
unidade de desvio padrão; ou seja:
5 = 1 ^ 0
(8.13)
G
A probabilidade p pode ser calculada, em testes bilaterais, por:
(8.14)
11 Mais diretamente, o poder do teste é uma função da diferença // - pi0.

TESTES DE HIPÓTESES 2 2 7
onde: O é a função de distribuição acumulada normal padrão;
5 definido em (8.13); e
z a é a abscissa da normal padrão que deixa ^ de área na cauda superior.12
O tamanho mínimo da amostra que garante poder igual a (1 - P), em tes­
tes bilaterais, é dado aproximadamente por:
*«/ + V
/2
n « (8.15)
onde é a abscissa da normal padrão que deixa p de área na cauda superior.
Para testes unilaterais,
/ Z„ a + .Z „Ç> \ 2
n « (8.16)
Exemplo 8.9 As especificações de certas lâmpadas eletrônicas afirmam que
elas resistem, em média, à tensão nominal de 127 V, com desvio padrão de 10
V. Um comprador desconfia dessa afirmação e resolve fazer um teste estatístico
para testar as hipóteses H0: [à = 127 e Hx: /x < 127, ao nível de significância de
5%. O comprador considera bastante grave se as lâmpadas resistirem, em mé­
dia, apenas 120 V ou menos. Por isso, se /z = 120, ele quer que o teste detecte
que H0 é falsa com 90% de probabilidade. Mas ele também não quer testar mui­
tas lâmpadas porque o teste é destrutivo, causando perda financeira. Qual é o
tamanho mínimo da amostra?
Solução: 8 = ÜLJiol = ljj Z.._..12Ql = 0 7
a 10
2
a , 645 +1,282 ^
K + V
n «
CO
J = 17,48
1 0,7
Logo, o tamanho mínimo da amostra deve ser n = 18 lâmpadas.
12 Em geral, uma das parcelas de (8.14) é aproximadamente nula.

2 2 8 ESTATÍSTICA
Teste para m édia com variância desconhecida
Podemos calcular, aproximadamente, o tamanho mínimo da amostra atra­
vés das expressões apresentadas no caso anterior, substituindo a abscissa z pela
abscissa t da distribuição t de Student com gl = n - l .13 Contudo, para o cálculo
do tamanho da amostra, não se conhece, a priori, o valor de n para obter gl.
Uma alternativa é fazer a amostragem em dois estágios, ou seja:
• retira-se, primeiramente, uma amostra-piloto de tamanho n0;
• calcula-se o desvio padrão dessa amostra (s0);
• obtém-se 8 com s0 no lugar de ct;
• calcula-se o tamanho n da amostra usando gl = n0 - 1 ; e
• completa-se a amostragem com mais n - n0 observações (supondo
n > n0, pois, em caso contrário, a amostra-piloto já seria suficiente).
Ver Exercício 23.
Teste para proporção
Em testes bilaterais (H0: p = p0 e H^. p * p0), o tamanho da amostra para
garantir poder igual a (1 - P) é dado, em função de p, por:
• %/Po • (1 - Po) + ■ a/p • (1 - p ) '
n = (8.17)
P - P o
Se o teste for unilateral, o cálculo é feito por:
/
Za • \ Po • (! - Po) + • v P C1 - p )
n = (8.18)
P -P o
V
Exemplo 8.10 Uma indústria de cerâmicas admite que até 4% de seus itens
podem conter defeitos leves. Um grande comprador resolve testar a garantia do
fabricante considerando as hipóteses H0: p = 0,04 e H ^ p > 0,04. Qual deve ser
o tamanho mínimo da amostra para garantir um poder de 90% no teste se a
verdadeira proporção for de 8%?
13 Formalmente, nesse caso deveríamos usar a chamada distribuição t não central, mas
isso torna o problema demasiadamente complexo.

TESTES DE HIPÓTESES 2 2 9
* yjPo * O - Po) + • \ P ' C1 - P) '
n =
P -P o
/
(1,645) • v 0,04(0,96) + (1,282) • ^0,08(0,92) 'l
= 280,69
0,08 - 0,04
Logo, o tamanho mínimo da amostra é n = 281.
EXERCÍCIOS
22. Certa rede de computadores transmite dados a uma velocidade média de
200 MB/s, com desvio padrão de 30 MB/s. Algumas alterações estão sendo
realizadas com o objetivo de aumentar a velocidade de transmissão de da­
dos. Qual deve ser o tamanho mínimo da amostra para detectar um au­
mento na média de 0,5 a, com 90% de probabilidade? Use nível de signifí-
cância de 1%.
23. As embalagens de óleo de cozinha devem conter 900 ml de conteúdo líqui­
do. Deseja-se fazer uma pesquisa com determinada marca para verificar se,
em média, o conteúdo líquido não é menor do que o valor estipulado. Com
nível de significância de 5%, qual é o tamanho de amostra necessário para
identificar, com 90% de probabilidade, peso médio inferior a 892 ml? Con­
sidere que já foi realizada uma pesquisa preliminar com 8 unidades, obten­
do desvio padrão igual a 10 ml.
EXERCÍCIOS COMPLEMENTARES
24. Padrões técnicos exigem que o nível de ruído em CPDs seja de, no máximo,
70 dB. Foram analisados 16 CPDs de várias organizações, obtendo-se os se­
guintes valores máximos de ruído:
78 73 68 65 72 64 77 80 82 78 65 72 61 79 58 65
a) Calcule a intensidade de ruído média e o desvio padrão para esses 16
CPDs.
b) Suponha que os 16 CPDs analisados são uma amostra aleatória de
CPDs do país. Para verificar se na média os CPDs atendem aos padrões
técnicos, como você construiria as hipóteses?

2 3 0 ESTATÍSTICA
c) Você pode concluir que a intensidade de ruído média dos CPDs nos ho­
rários críticos é superior ao especificado? Faça o teste adequado ao ní­
vel de significância de 5%.
d) Sob o ponto de vista dos que trabalham nos CPDs, qual é o pior erro?
Explique.
e) Se a verdadeira intensidade média de ruído dos CPDs fosse de 73 dB,
qual é a probabilidade de você tomar uma decisão errada no teste do
item (c)? Suponha que o verdadeiro desvio padrão é 7 dB.
25. Um cliente de uma torrefação de café suspeita que os pesos dos pacotes,
que deveriam ser de 500 g, não estão corretos. Resolveu, então, retirar
uma amostra dos pesos de 16 pacotes (supondo que provenham de uma
distribuição normal):
510, 495, 498, 500, 501, 499, 503, 500, 495, 492, 499, 499, 497,
495, 499, 501
a) Calcule o peso médio e o desvio padrão dos elementos da amostra.
b) O cliente tem razão na suspeita? Use a = 0,05.
c) Pode-se afirmar, com nível de significância de 10%, que a variância do
processo é superior a 10 g2?
26. O tempo médio de vida de um tipo de lâmpada é de 2.000 horas e desvio
padrão de 200 horas, segundo o fabricante. Afirma também que esse tem­
po médio de vida segue uma distribuição normal. Um possível comprador
resolve retirar uma amostra aleatória de 15 lâmpadas. Testando-as, obteve
média de 1.950 horas.
a) A 5% de significância, há evidência de que a afirmação do fornecedor
quanto à média é falsa (prejudicando o comprador)?
b) Assumindo um risco de 5% para o fornecedor, a amostra retirada é su­
ficiente para que o comprador tenha um risco de 10% de que a média
do tempo de vida esteja 50 horas abaixo do especificado? Qual deveria
ser o valor de n?
c) Se o tempo de vida médio real fosse de 1.950 horas, qual é a probabili­
dade de se tomar uma decisão errada no item (a)?
27. O controle estatístico de certo processo estabeleceu que pelo menos 94%
dos produtos têm que estar sem defeitos. Para verificar a validade desta
afirmação, foi coletada uma amostra de 150 produtos, obtendo uma pro­
porção sem defeito igual a 92%.
a) Com 1% de significância, há evidência de que o processo está em desa­
cordo com o esperado?

TESTES DE HIPÓTESES 2 3 1
b) Se o percentual real sem defeito fosse 91%, qual é a probabilidade de
se tomar uma decisão errada no item (a)?
c) Suponha que se queira identificar, com 95% de probabilidade, a falsi­
dade de H0, quando a proporção de sem defeito for, na realidade, igual
a 93%. Considerando que o teste será realizado com 1% de significân­
cia, qual é o tamanho de amostra necessário?
28. O resíduo da queima de carvão mineral (cinza) pode ser usado na composi­
ção do cimento pozolânico. Deseja-se verificar se a substituição da verda­
deira rocha pozolânica por cinza de carvão altera a resistência à compres­
são do cimento, após 28 dias de hidratação. Suponha que esse cimento
com a verdadeira rocha pozolânica tem resistência média de 40 MPa e des­
vio padrão de 4 MPa (após 28 dias de hidratação). Use a = 0,05.
a) Quantos corpos de prova devem ser usados para que seja detectada
uma redução média de 3 MPa, com 95% de probabilidade?
b) Se foi feito um estudo experimental com o tamanho de amostra calcu­
lado no item (a), encontrando x = 39,2 e s = 6 MPa, pode-se dizer
que houve redução na resistência média?
c) Houve aumento na variabilidade? (Suponha que os dados provenham
de distribuição normal.)

9
Comparação Entre Tratamentos
É muito comum o interesse em comparar dois ou mais tratamentos, como,
por exemplo, dois processos de têmpera na produção de aço, três tipos de ci-
mento-e-cola para fixar azulejos, dois sistemas computacionais para a informa­
tização de um processo etc. Para realizar as comparações, podemos planejar ex­
perimentos com amostras submetidas a cada tratamento. Em cada ensaio,
observamos uma resposta adequada. Por exemplo, no caso do aço, a resposta
pode ser a resistência mecânica; no cimento-e-cola, o grau de aderência; no sis­
tema computacional, o tempo de resposta; e assim por diante.
Na comparação dos tratamentos, é natural o interesse em verificar se há
evidência de diferenças entre os efeitos dos tratamentos, o que pode ser feito
através de testes estatísticos. Neste capítulo, apresentaremos testes paramétri­
cos, os quais se caracterizam por suporem certa distribuição de probabilidades
para a variável resposta. Em consequência, a comparação entre os efeitos dos
tratamentos pode ser feita em termos dos parâmetros da distribuição de proba­
bilidades suposta. Nós nos restringiremos à comparação de parâmetros de dis­
tribuições normais, com ênfase em testes de médias.
9.1 AMOSTRAS INDEPENDENTES E EM BLOCOS
Na comparação entre g tratamentos, muitas vezes o experimento pode ser
conduzido dividindo-se aleatoriamente as unidades experimentais em g grupos,
sendo cada grupo submetido a um tratamento - projeto de experimento comple­

COMPARAÇÃO ENTRE TRATAMENTOS 2 3 3
tamente aleatorizado. Como resultado da aplicação desse projeto, temos g amos­
tras independentes.
Alternativamente, podemos construir h blocos de unidades experimentais
relativamente similares. Se em cada bloco temos g unidades experimentais, alo-
camos, por sorteio, todos os g tratamentos em cada bloco - projeto de experi­
mento em blocos aleatorizados. No caso de g = 2, o resultado da aplicação desse
projeto leva a dados pareados.
Exemplo 9.1 Considere o problema de comparar dois materiais (A e B), para
sola de tênis, em termos do grau de desgaste após certo período de uso.1 Se­
guem dois projetos de experimentos alternativos:
Projeto I: Um grupo de indivíduos usa tênis com solas feitas com o
material A; e outro grupo usa tênis com solas feitas com o material B,
conforme ilustra a Figura 9.1.
Material A Material B
divisão aleatória
i s l i IS IS IS l i i s l i l i l). i s l>.
J U H U M M O W
Mensuração do grau de desgaste Mensuração do grau de desgaste
Figura 9.1 Esquema de planejamento de experimento completamente aleatoriza­
do com g = 2 grupos. Em cada grupo é alocado um tratamento.
Projeto II: Fabricam-se, para a realização do experimento, pares de
tênis com os dois tipos de sola, isto é, um dos pés com o material A e o
outro pé com o material B. Em cada par, o material usado em cada pé
(direito ou esquerdo) é decidido por sorteio (ver Figura 9.2).
1 Baseado em exemplo do livro de BOX, G. E. P.; HUNTER, W. G.; HUNTER, J. S. Statis­
tics for experimenters. New York: John Wiley, 1978.

2 3 4 ESTATÍSTICA
alocação aleatória d e A e B e m cada par
L § _ ip - i J O
t s ^ l s
O OJJ 0 0 - a o
jjjj
Mensuração do grau de desgaste
Figura 9.2 Esquema de planejamento de experimento em blocos aleatorizados,
com g = 2 tratamentos e h = 5 blocos.
Para a análise dos resultados do Projeto II, a Figura 9.3 ilustra duas situa­
ções: (a) quando desconsideramos os pares, tratando os dados como se fossem
duas amostras independentes; e (b) quando analisamos os pares.
(a) (b)
desgaste desgaste
t
o
0
• material A
1
o m aterial#
o
1 2 3 4 5
indivíduo (par de unidades experimentais)
Figura 9.3 Ilustração de um conjunto de dados visto de forma pareada (à direi­
ta) e deforma independente (à esquerda).
Analisando a Figura 9.3, fica evidente que, ao olharmos os dados de forma
pareada, temos mais informação sobre uma possível diferença entre os dois ma­
teriais - os pares até o quinto indivíduo mostraram que o material A teve
maior nível de desgaste. Observando as amostras de forma independente, as
diferenças entre os dois materiais ficaram ofuscadas pelas diferenças entre os
indivíduos.
Em suma, para o particular problema, o Projeto II destaca melhor uma
possível diferença entre os materiais. Em geral, quando é possível formar blocos
de unidades relativamente similares, temos um projeto de experimento melhor.
Na prática, porém, muitas vezes não temos total liberdade de escolher o
projeto de experimento mais adequado, seja por questões financeiras, seja por-

COMPARAÇÃO ENTRE TRATAMENTOS 2 3 5
que os grupos já estão naturalmente divididos, como no caso de comparar algu­
ma característica entre homens e mulheres (amostras independentes). Ou, ain­
da, quando queremos comparar o efeito de certo evento, em que é natural
observar as unidades experimentais antes e depois do evento, resultando em
dados pareados.
9.2 TESTE PARA DUAS AMOSTRAS PAREADAS
t
O chamado teste t é apropriado para comparar dois conjuntos de dados
quantitativos, em termos de seus valores médios. Mais especificamente:
H 0: Mi = M-2 e Hi* jij ^ \i2
onde: Mi é o valor esperado da resposta sob o tratamento 1 e
|i2 é o valor esperado da resposta sob o tratamento 2.
Na abordagem unilateral, a hipótese alternativa é do tipo H^: > \i2 ou
Hi”: Mi < \i2.
Nesta seção, trataremos do caso em que os dois conjuntos de dados são
pareados. Contudo, as observações entre os pares devem ser independentes.
Exemplo 9.2 Seja o problema de verificar se um novo algoritmo de busca em
um banco de dados é mais rápido que o algoritmo atualmente usado. Para fazer
a comparação dos dois algoritmos, planeja-se realizar uma amostra aleatória de
dez buscas experimentais (ensaios). Em cada ensaio, uma dada busca é realiza­
da pelos dois algoritmos e o tempo de resposta de cada algoritmo anotado.
Observamos que em cada ensaio os dois algoritmos são usados em condições
idênticas, caracterizando dez pares de observações.
As hipóteses podem ser formuladas da seguinte maneira:
H0: em média, os dois algoritmos são igualmente rápidos e
Hi’. em média, o algoritmo novo é mais rápido do que o algoritmo em uso.
H0: Mi = Hz e Hii < \i2
onde: Mi é o tempo esperado de resposta do algoritmo novo e
M2 é o tempo esperado de resposta do algoritmo atualmente usado.

2 3 6 ESTATÍSTICA
Suponha que o experimento tenha sido realizado, gerando os dados apre­
sentados na Tabela 9.1.
Tabela 9.1 Tempos de resposta dos algoritmos de busca 1 e 2, em dez ensaios pa-
reados.
Tempo de resposta (s)
Ensaio
Xy Antigo X2 Diferença D = X2 - Xy
N O V O
1 22 25 3
2 21 28 7
3 28 26 - 2
4 30 36 6
5 33 32 - 1
6 33 39 6
7 26 28 2
8 24 33 9
9 31 30 - 1
10 22 27 5
Como os dados são pareados, podemos verificar em cada ensaio o quanto
um tratamento (algoritmo) foi melhor do que o outro, ou seja, analisar a va­
riável:
D = X 2 - X j (9.1)
Em termos da variável diferença D, as hipóteses são descritas como:
H0: \iD = 0 e H1:\id > 0
onde é o valor esperado de D. E o problema toma-se semelhante ao teste de
uma média, discutido na seção 8.9. Assim, dada uma amostra, calculamos a es­
tatística do teste por:
d • V n
t = (9.2)
onde: n é o tamanho da amostra (número de pares);
d é a média das diferenças observadas; e
sd é o desvio padrão das diferenças observadas.2
2 Note que estamos considerando o tamanho da amostra (n) como sendo igual ao nú­
mero de pares (h), para evidenciar que esse teste é um caso especial do teste de uma média.

COMPARAÇÃO ENTRE TRATAMENTOS 2 3 7
Supondo que os valores de D provenham de distribuição aproximadamente
normal, o teste pode ser realizado com a distribuição t de Student com gl = n - 1
graus de liberdade.
Exemplo 9.2 (continuação) Valores de D (última coluna da Tabela 9.1):
3, 7, -2, 6, -1, 6, 2, 9, -1, 5
Donde:
n = 10, d. = 3,4 e
sr, = > .3 ,8 1
n - 1
E, portanto:
f _ d -Jn _ 3,4 JÍÕ _ 2 g2
sd 3,81
Abordagem do valor p: Como n = 10, temos gl = 9 graus de liberdade. Tome­
mos, então, a linha de gl = 9 da Tabela 4 do apêndice (tabela da distribuição t
de Student), como mostra a Figura 9.4. Por essa tabela, obtemos a área associa­
da a um valor maior ou igual a t = 2,82. Como o teste é unilateral, essa área
corresponde ao valor p.
dados Área na cauda superior
observados j
0,25 0,10 0,05 0,025 0,010 0,005
t
\
r
0,703 1,383 1,833 2,262 2,821 3,250
t = 2 ,8 2 ---------> 9 - —
Figura 9.4 Uso da distribuição t de Student com gl = 9 para a obtenção do va­
lor p, num teste unilateral, com n = 10 e t = 2,82.
Observando a linha correspondente a gl = 9, verificamos, na tabela, que o
valor t = 2,82 (calculado com base na amostra) está próximo do valor tabulado
2,821. Logo, como ilustra a Figura 9.4, temos p « 0,010.

2 3 8 ESTATÍSTICA
Considerando o nível de significância de 5% (a = 0,05), o teste leva a
conclusão de que os dados mostram evidência suficiente de que H0 é falsa (pois
p < a = 0,05), detectando, então, que o algoritmo novo é, em média, mais rá­
pido do que o algoritmo atualmente em uso. Essa mesma conclusão pode ser
obtida se usarmos a abordagem clássica, conforme descrita a seguir.
Abordagem clássica: Nesse caso, busca-se o valor crítico
tC3 que deixa área a = 0,05 na cauda superior da distribui­
a = 0,05
ção t de student com gl = 9. Pela Tabela 4 do apêndice te­
mos tc = 1,833, levando à regra de decisão apresentada ao
0 t, = 1,833
lado, a qual pode ser construída mesmo antes de se obser­ (tabela)
«------------- \— »
var a amostra. aceita H„
rejeita H„
Como os dados produziram o valor t = 2,82, então o teste rejeita H0 ao ní­
vel de significância de 5%.
9.3 TESTE PARA DUAS AMOSTRAS INDEPENDENTES
t
Nesta seção, apresentaremos como realizar o teste t quando as amostras
são independentes.
Exemplo 9.3 Desejamos verificar se os catalisadores A e B têm efeitos diferen­
tes no rendimento de certa reação química. As hipóteses são:
H0: em média, os dois catalisadores são iguais em termos de rendimento; e
Hii em média, os dois catalisadores são diferentes em termos de rendi­
mento.
Ou, ainda:
H0: Ui = \x2 e H^. ^ * ji*
onde
\iim. rendimento esperado com o catalisador A; e
\i2: rendimento esperado com o catalisador B.
Para testar essas hipóteses, realizamos dez ensaios com cada catalisador,
em ordem aleatória. Como ressaltava R. A. Fisher, que construiu as bases da es­
tatística experimental: a aleatorização dos grupos é fundamental para resguardar
a validade de um teste de significância.
A Tabela 9.2 mostra os resultados do experimento e a Figura 9.5 apresenta
o diagrama de pontos de cada amostra.

COMPARAÇÃO ENTRE TRATAMENTOS 2 3 9
Tabela 9.2 Rendimentos (%) de uma reação química em função do catalisador
utilizado.
Catalisador A Catalisador B
45 51 50 62 43 45 35 43 59 48
42 53 50 48 55 45 41 43 49 39
nn n n Rn n «a n
o catalisador A
<■1 o n fi fi nn o
o catalisador B
-------------------------------- --------------------- ----------------------
30 35 40 45 50 55 60 65
rendimento (%)
Figura 9.5 Diagrama de pontos dos resultados do experimento.
A análise descritiva das amostras sugere que o catalisador A é melhor, mas
precisamos fazer um teste estatístico apropriado para verificar se essa diferença
não pode ser explicada por mero acaso do particular experimento realizado.
Estatística do teste para amostras de tamanhos iguais
Dada as duas amostras, a estatística do teste toma como base a diferença
entre as médias, x. - x 2, mas leva também em consideração o número de ele­
mentos em cada amostra e a variabilidade interna das amostras. Quanto maior
as amostras, maior a evidência de uma possível diferença real. Por outro lado,
se há muita variabilidade entre os elementos de cada amostra, diferenças reais
podem ficar nebulosas (veja a Figura 9.6).
evidência de grupos diferentes evidência de grupos diferentes
n ã o
Q__Û__Q_
Ï >(1) ___CL -►Cl)
>(2) -0-0- Jft__ -**► (2)
*1 *2 *1 *2
Figura 9.6 Importância de se considerar a variância interna dos grupos.
Considerando o mesmo número de elementos, n, em cada amostra, a cha­
mada variância agregada é obtida pela média aritmética das variâncias de cada
grupo, ou seja:
(9.3)

2 4 0 ESTATÍSTICA
E a estatística do teste é calculada por:
(9.4)
onde
n: tamanho da amostra em cada grupo;
x 1: média da amostra 1; x 2: média da amostra 2;
sf: variância da amostra 1; s2: variância da amostra 2; e
s'2: variância agregada das duas amostras.
Estatística do teste para amostras de tamanhos diferentes
No caso de as amostras terem tamanhos diferentes * n2), os cálculos
devem ser feitos por:
„2 _ ( " l + ( n 2 “ 1 > 2
(9.5)
S “
n: + n2 - 2
(9.6)
Suposições básicas para a aplicação do teste:
1. as observações devem ser independentes;
2. as variâncias populacionais devem ser iguais nos dois grupos;
3. os dois conjuntos de dados devem provir de distribuições normais.
A suposição (1) refere-se ao planejamento do experimento, enquanto as
suposições (2) e (3) à variável e às populações em estudo.3 Na prática, não é fá­
cil verificar a veracidade dessas suposições. Aconselhamos, contudo, fazer uma
análise exploratória, tal como um diagrama de pontos para cada amostra. Esses
gráficos permitem avaliar se existem fortes violações das suposições, tais como
3 Observamos que o teste t é razoavelmente robusto às suposições (2) e (3), isto é, o tes­
te somente deixará de ser válido se houver violações fortes dessas suposições, como a presença
de valor discrepante, distribuições muito assimétricas ou uma variância muito superior à outra.

COMPARAÇÃO ENTRE TRATAMENTOS 2 4 1
a presença de pontos discrepantes, distribuições com formas assimétricas ou,
ainda, uma distribuição bem mais dispersa do que a outra.4
Distribuição de referência. Se as médias populacionais forem iguais (H0 ver­
dadeira) e as suposições básicas puderem ser admitidas, então usaremos a dis­
tribuição t de Student, com gl = nl + n2 - 2 graus de liberdade, para a realiza­
ção do teste.
Exemplo 9.3 (continuação)
Amostra 1: n = 10, Xi = 49,900 e s22 = 35,656
Amostra 2: n = 10, x2 = 44,700 e s22 = 42,233
a 2 si + 5ÍÍ 35,656 + 42,233
, , . . . o o n , c
Vanancia agregada: sa = —----- - = —-------------------= 38,945
Resultado da estatística do teste:
f = ~ = ( 4 9 , 9 ° " 4 4 ’ 7 0 ) ' j 2 ( ^ 4 ) = ( 5 ’2 ) ‘ = 1 ) 8 6
Graus de liberdade: gl = 2n - 2 = 2(10) - 2 =18.
Abordagem do valor p: O esquema seguinte ilustra o uso da Tabela 4 do apên­
dice para se obter o valor p associado ao t calculado.
dados Área na cauda superior
observados
gl 0,25 0,10 0,05 0,025 0,010 0,005
t t
. • ■ •
0,688 1,330 1,734 2,101 2,552 2,878
t = 1,86 -> 18
• • •
Os dados observados levaram ao valor t = 1,86, apontando para uma área
na cauda superior da curva entre 0,025 e 0,05. Mas, como o teste é bilateral
(Hii Mi * m2), a área deve ser dobrada para se ter o valor p correto. Veja o es­
quema a seguir:
4 Podemos, ainda, realizar um teste de igualdade de variâncias (seção 9.5) e um teste de
aderência à distribuição normal (Capítulo 10).

2 4 2 ESTATÍSTICA
Pela tabela t:
área entre
e 0,05
1,86 0 1,86
-
Portanto, 0,05 < p < 0,10, o que leva à aceitação de H0 ao nível de signi-
ficância de 5% (pois p > a = 0,05).
Abordagem clássica: Mesmo antes de realizar o experi­
mento, podemos buscar na tabela da distribuição t de stu-
dent com gl = 18 o valor crítico tc, o qual deixa uma área
igual a a = °>0% = 0,025 em cada calda da distribuição
-t. 0 t. = 2,101
(pois o teste é bilateral). Pela Tabela 4, temos tc = 2,101, (tabela)
<----- L eitaJl----- ►
levando à regra de decisão apresentada ao lado.
rejeita H„ aceita 0 rejeita H0
Como os dados produziram o valor t = 1,86, o qual pertence à região de
aceitação, o teste aceita HQ ao nível de significância de 5%.
Concluímos, então, ao nível de significância de 5%, que os dados não com­
provam uma diferença entre os dois catalisadores. Existe uma probabilidade ra­
zoável (superior a 5%) de que as diferenças observadas nos dados experimen­
tais são provenientes de fatores casuais.
9.4 TAMANHO DAS AMOSTRAS
No planejamento de um experimento para comparar dois tratamentos, sur­
ge a questão de qual deve ser o número n de ensaios para cada tratamento.
Para responder a essa questão, vamos relembrar alguns conceitos. Quando o
teste rejeita a hipótese de igualdade entre os tratamentos (H0), concluindo que
existem diferenças significativas entre eles, podemos estar cometendo o chama­
do erro tipo I: rejeitar H0 quando verdadeira. Os testes são construídos com a
probabilidade deste erro fixada num nível bastante baixo, designada por a (ní­
vel de significância do teste) e usualmente a = 0,05. Por outro lado, quando o
teste aceita H0, pode ocorrer o chamado erro tipo II: aceitar H0 quando falsa. A
probabilidade de se cometer este erro é designada por p. É desejável que, quan­
do a diferença entre os tratamentos for grande em termos práticos, a probabili­
dade p seja pequena e, para que isso aconteça, a quantidade n de elementos em
cada grupo deve ser suficientemente grande.

COMPARAÇÃO ENTRE TRATAMENTOS 2 4 3
A discussão que segue restringe-se ao problema de comparar duas amos­
tras independentes em termos de médias. Sejam m e n2 as médias das duas po­
pulações em estudo e seja
g _ Im -H2I
(9.7)
A quantidade 5 é a diferença de magnitude entre as verdadeiras médias
em unidade de desvio padrão (a). Supomos aqui que as duas populações te­
nham o mesmo desvio padrão.
Para avaliar a quantidade n de elementos em cada grupo, o pesquisador
precisa ser capaz de fornecer o valor mínimo de 8 que leva a consequências prá­
ticas. Em geral, o pesquisador tem maior facilidade em raciocinar em termos da
unidade em que se está medindo a variável em análise, mas, nesse caso, tor-
na-se necessário ter uma avaliação de a.
A Figura 9.7 indica o número mínimo n para que uma diferença 8 seja de­
tectada pelo teste estatístico com probabilidade 0,80 (p = 0,20) e com probabi­
lidade 0,90 (p = 0,10).
o
o<
2
bo
Cd
U
6
ÜJ
cd
b
Vi
O
cd
T3
O
XI ------ ß = 0,20
------ p = 0,10
^ 0,5 0,6 0,7 0,8 0,9 1,0 1,1 1,2 1,3 1,4 1,5 1,6 1,7 1,8 1,9 2,0
diferença absoluta entre as médias, por unidade de desvio padrão
Figura 9.7 Tamanho mínimo da amostra, n, em cada grupo, em função da dis­
tância 8 = | jí! - [i2\ : a que se deseja detectar no teste estatístico.
Como exemplo, considere o problema de comparar dois catalisadores,
como no Exemplo 9.7. Sabe-se que os engenheiros consideram relevante uma
diferença de 4 unidades entre as médias e, com base em estudos anteriores, o
desvio padrão do rendimento do processo químico em estudo não deve superar
5 unidades. Logo, 8 = y5 = 0,8. Pelo gráfico da Figura 9.7, o número mínimo

2 4 4 ESTATÍSTICA
de ensaios para cada catalisador deve ser de, aproximadamente, n = 34 para
P = 0,10; ou n = 25 para p = 0,20.
EXERCÍCIOS
1. Uma empresa de cerveja, após uma grande fusão, estuda a possibilidade de
alterar o rótulo de uma de suas marcas, usando formas e cores mais vivas.
Para avaliar se existe vantagem em alterar o rótulo, a empresa levou a cabo
uma pesquisa de marketing. Enlatou a cerveja com o rótulo tradicional e
com o rótulo novo. A pesquisa foi feita em 8 estabelecimentos comerciais.
Em 4 deles, extraídos por sorteio, colocou-se o produto com o rótulo novo
e, nos outros 4, manteve-se o produto com o rótulo tradicional. Após um
mês, avaliou-se a quantidade vendida em cada estabelecimento. Os estabe­
lecimentos que usaram o rótulo tradicional tiveram os seguintes resultados
nas vendas (em milhares de unidades): 6, 5, 2, 2. Os estabelecimentos que
usaram o rótulo novo tiveram os seguintes resultados nas vendas (em mi­
lhares de unidades): 4, 9, 5, 6. Os dados mostram evidência suficiente de
que a média de vendas é superior com o rótulo novo? Responda usando
um teste estatístico apropriado ao nível de significância de 5%.
2. Para o mesmo problema da questão anterior, outro instituto de pesquisa,
que tem uma equipe com melhor preparação em estatística, elaborou um
projeto um pouco diferente. Com seis estabelecimentos comerciais dispos­
tos a colaborar com a pesquisa, colocaram-se as duas embalagens (de rótu­
lo tradicional e de rótulo novo) da mesma cerveja. Tomou-se o cuidado
para que em cada estabelecimento a apresentação das duas embalagens do
produto fosse feita de forma idêntica. Os resultados das vendas mensais
(em milhares de unidades), para cada estabelecimento e cada embalagem,
foram os seguintes:
Estabelecimento: 1 2 3 4 5 6
Rótulo tradicional: 16 12 28 32 19 25
Rótulo novo: 20 11 33 40 21 31
Os dados mostram evidência suficiente de que a média de vendas é su­
perior com o rótulo novo? Responda usando um teste estatístico apropria­
do ao nível de significância de 5%.
3. Para avaliar o efeito de um brinde nas vendas de determinado produto,
planeja-se comparar as vendas em lojas que vendem o produto com o brin­
de, com as vendas em lojas que não oferecem o brinde. Para reduzir o efei­
to de variações devidas a outros fatores, as lojas foram grupadas em pares,
de tal forma que as lojas de um mesmo par são o mais similar possível, em

COMPARAÇÃO ENTRE TRATAMENTOS 24 5
termos, por exemplo, do volume de vendas, localidade, identidade de preços
etc. Em cada par de lojas, uma passou a oferecer o brinde e a outra, não.
a) Apresente as hipóteses nula e alternativa.
b) Os resultados das vendas, em quantidade de unidades vendidas, foram
os seguintes:
Vendas Vendas
Par de loja
sem brinde com brinde
1 33 43
2 43 39
3 26 33
4 19 32
5 37 43
6 27 46
Os dados mostram evidência suficiente para se afirmar que a oferta do
brinde aumenta as vendas? Use nível de significância de 5%.
Para resolver o mesmo problema do exercício anterior, decidiu-se fazer um
planejamento do tipo antes-e-depois. Observou-se a venda mensal do pro­
duto em questão nas 12 lojas. Depois, passou-se a oferecer um brinde e
voltou-se a avaliar a venda mensal desse produto nas 12 lojas. Os incre­
mentos (ou reduções) nas vendas foram os seguintes:
7 10 5 -2 9 0 3 - 4 8 9 1 3
a) Os dados mostram evidência suficiente para se afirmar que a oferta do
brinde aumenta as vendas? Use nível de significância de 5%.
b) Aponte as vantagens e as desvantagens desse planejamento de pesqui­
sa, em relação ao apresentado no Exercício 4, considerando o particu­
lar problema em discussão.
c) Apresente um terceiro planejamento de pesquisa para esse problema,
tentando aproveitar as vantagens dos dois procedimentos apresentados.
Um produto fabricado por injeção de plástico é analisado em dois níveis de
percentual de talco. Os dados seguintes apresentam os resultados da dure­
za (HRc), segundo o percentual de talco utilizado:
Baixo: 51,7 49,4 65,9 60,0 71,1 72,9 71,9 75,1
Alto: 75,2 76,0 63,7 69,6 67,1 69,1 52,8 57,6
Os dados mostram evidência suficiente para afirmar que a dureza média
do produto é diferente nos dois níveis de percentual de talco? Use a = 0,05.

2 4 6 ESTATÍSTICA
6. Deseja-se verificar se há alteração no rendimento médio de um processo de
reação química, ao reduzir a temperatura de 80°C para 70°C. Realiza-
ram-se 12 ensaios em cada temperatura, encontrando os seguintes resulta­
dos de rendimento (%):
Temperatura de 80°C: média 40,61 e variância 12,86.
Temperatura de 70°C: média 36,61 e variância 9,34.
Qual é a conclusão? Use a = 0,01.
.
7 Na comparação de duas topologias de rede de computadores, Cl e C2, ava-
liou-se o tempo de transmissão de pacotes de dados entre duas máquinas.
Foram realizados 32 ensaios em Cl e 24 ensaios em C2, cujos resultados
são apresentados a seguir:
Tempo
Topologia Média Variância
(em décimos de segundo)
Cl 09 12 10 12 11 09 08 12 13
09 13 08 17 09 09 08 09 08 10,625 6,371
14 08 08 08 08 13 10 10 15
13 13 12 14 08
C2 14 15 08 13 16 12 14 17 14 13,458 4,781
10 13 12 13 14 10 15 12 17
16 12 15 13 14 14
Existe diferença significativa entre o tempo médio de transmissão nas
duas topologias?
.
8 Para comparar dois algoritmos de otimização, foi realizado um experimen­
to com seis ensaios. Em cada ensaio, foram usados separadamente os dois
algoritmos em estudo, mas sob as mesmas condições (dados pareados). Os
tempos de resposta ao usuário foram:
Ensaio: 1 2 3 4 5 6
Algoritmo 1: 8,1 8,9 9,3 9,6 8,1 11,2
Algoritmo 2: 9,2 9,8 9,9 10,3 8,9 13,1
Os tempos de resposta dos dois algoritmos são, em média, diferentes?
Use a = 0,05.

COMPARAÇÃO ENTRE TRATAMENTOS 2 4 7
9.
Quantos ensaios devem ser realizados com cada tratamento para garantir
que um teste t para amostras independentes, ao nível de significância de
5%, detecte uma diferença de 1 desvio padrão, com 90% de probabilidade?
Admitindo distribuição normal, a diferença mínima que se quer detectar
está representada na figura a seguir:
9.5 TESTE PARA DUAS VARIÂNCIAS
F
Suponha que queremos comparar se duas populações, supostamente com
distribuições normais, têm a mesma variância. Formulamos as hipóteses por:
H0: a f = a \ e a* * a*
onde:
a.2: variância da população 1; e
variância da população 2
A hipótese alternativa também pode ser H ': v f > a 2. Com as amostras da
população 1 e da população 2, a estatística do teste é calculada por:
(9.8)
onde:
s 2: variância da amostra de elementos; e
s 2: variância da amostra de n2 elementos, considerando s 2 > s 2, ou
seja, a maior variância deve ser colocada no numerador.
A distribuição de referência para este teste é a chamada distribuição F com
gl = rii - 1 no numerador e gl = n2 - 1 no denominador, apresentada na Tabela
6 do apêndice para os níveis de significância de 0,10, 0,05, 0,025 e 0,01. Assim,
estabelecido o nível de significância a, podemos obter o valor f c, que deixa área
igual a a/2 na cauda superior da distribuição (teste bilateral) ou, no caso de

2 4 8 ESTATÍSTICA
teste unilateral, área igual a a. A regra de decisão, na abordagem clássica, é
dada por5
se / < f c, então aceita H0;
se / > f c, então rejeita H0.
Exemplo 9.3 (continuação) Verificamos que não há evidências de que os ca­
talisadores A e B tenham efeitos médios diferentes no rendimento de certa rea­
ção química. Vamos verificar, agora, se eles produzem efeitos diferentes nas va­
riâncias. As hipóteses podem ser:
H0: as variâncias do rendimento são iguais para os dois catalisadores; e
Hi’. as variâncias do rendimento são diferentes para os dois catalisadores.
Dados os resultados do experimento:
Amostra 1: nx = 10, Xi= 49,900 e s 2 = 35,656
Amostra 2: n2 = 10, x2= 44,700 e s 2 = 42,233
No cálculo de /, colocamos a maior variância no numerador, assim:
/ = 4 = 42,233 = 1,18
Sj 35,656
Para obter o valor crítico f c, ao nível de significância de 5%, devemos obter
área igual a 2,5% na cauda superior da distribuição F com gl = 9 no numerador
e gl = 9 no denominador, o que acarreta f c = 4,03. Como / < f c, o teste aceita
H0.
9.6 COMPARAÇÃO DE VÁRIAS MÉDIAS
Nas seções 9.2 e 9.3, aprendemos a testar a significância de duas médias
através de testes t. Nesta seção, aprenderemos um teste para verificar se há di­
ferenças significativas entre as médias de g (g > 2) grupos de observações, sen­
do cada grupo formado pelos resultados de um tratamento. Dessa forma, pode­
mos comparar dois ou mais algoritmos computacionais em termos do tempo
médio de resposta ao usuário; dois ou mais catalisadores em termos do rendi­
mento médio da reação química etc.
5 Estamos usando a abordagem clássica para facilitar o uso da tabela, mas, se o teste for
feito com auxílio do computador, a abordagem do valor p é mais fácil.

COMPARAÇÃO ENTRE TRATAMENTOS 2 4 9
9.6.1 Amostras independentes
A análise estatística para a comparação de g grupos independentes é tradi­
cionalmente feita por uma análise de variância (ANOVA), acompanhada de um
teste F, que, da mesma forma como o teste t, supõe:
1. as observações devem ser independentes;
2. as variâncias populacionais devem ser iguais nos g grupos; e
3. a distribuição das observações em cada grupo deve ser normal.6
Formalmente, temos as seguintes hipóteses:
H0: jii = \i2 = ... = M* e Hii para algum i * j
onde ji; representa o valor esperado da resposta sob o tratamento i (i = 1, 2, ..., g)
(ver Figura 9.8).
Sob H0 Sob Hj
Figura 9.8 Suposições sobre as observações em termos de H0 e Hx.
Considerando n replicações sob cada tratamento (amostra de n elementos
em cada grupo, totalizando N = ng observações), podemos representar os da­
dos pelo seguinte modelo estatístico:
Yy = \x + ij +8ij (i = 1, 2, ..., g ;j = 1, 2, ..., ri) (9.9)
onde: Yy é a variável aleatória associada à;-ésima observação do i-ésimo trata­
mento;
[x é a média global da resposta (independentemente do tratamento);
T; é o efeito do i-ésimo tratamento;
% é o efeito aleatório ou erro experimental, o qual é suposto com distri­
buição aproximadamente normal, média zero e variância constante.
6 Para g = 2, o teste F é equivalente ao teste t bilateral. Observamos que o teste F é ro­
busto com respeito às suposições (2) e (3), ou seja, ele ainda é válido com pequenas violações
destas suposições.

2 5 0 ESTATÍSTICA
Considerando o modelo (9.9), o valor esperado da resposta no i-ésimo tra­
tamento é dado por ^ = [x + t E as hipóteses podem ser escritas por:
H0: Tx = x2 = ... = = 0 e Hii x* * 0, para algum i = 1, 2, ..., g
As observações, as somas e as médias por tratamento são representadas por7
Tratam ento
Kepncaçao
1 2 g
1
yn y2i y«i
2
yi2 y22 y«2
n
ym y2n y?n
Soma yi. y2. • ■ • x*. y.. = 2 > i
!
ÿi. y2. • ■ • x*.
Média X. = -Z X i
5 *
Considere a seguinte soma de quadrados:
SQ™ = È £ ( y , 5 - x ..) 2 (9.10)
i= 1 j=1
Se H0 for verdadeira e, portanto, todas as observações provêm de uma
mesma população, então SQTot é o numerador do cálculo da variância, s2, de to­
das as N = ng observações. Pode-se mostrar que SQTot (soma de quadrados to­
tal) é decomposta na soma de quadrados dos tratamentos e na soma de quadra­
dos do erro dadas, respectivamente, por:
SQ™ = £ J ( y , - y ) 2 = n £ ( y i. - y . y (9.11)
i=l ;=1 t= 1
i= 1 ;=1
Os g diferentes desvios de SQTrat são feitos em relação a uma única média
amostrai (y ). Por isso, dizemos que SQTrat tem g - 1 graus de liberdade. Enquan­
7 Se os tamanhos das amostras forem diferentes, é necessário adequar a formulação
apresentada nesta seção, substituindo n, (tamanho da amostra no grupo i) por n.

COMPARAÇÃO ENTRE TRATAMENTOS 2 5 1
to os N desvios de SQfrro são feitos em relação a g médias amostrais (yi 3 i = 1,
2, g) e, por isso, SQeno tem N - g graus de liberdade. A divisão das somas de
quadrados pelos correspondentes graus de liberdade leva aos chamados qua­
drados médios. Assim:
SQn
Traí _ i= 1 (9.13)
tf] S - 1
Trai
(9.14)
QMtrro =
£m>
onde N = ng.
Observe que QMTrat é uma medida da variância entre as médias dos gru­
pos, enquanto QM£rro é uma medida da variância dentro dos grupos. Define-se
a razão:
(9.15)
que pode ser interpretada como uma medida de discriminação entre os g gru­
pos. Para testar a hipótese H0: m = \jl2 = ... = usamos a distribuição F, com
gl = g - 1 no numerador e gl = N - g no denominador. Assim, estabelecido o
nível de significância a, podemos obter na Tabela 6 do apêndice o valor f c, que
deixa área igual a a na cauda superior da distribuição. A regra de decisão é
dada por:
se / < f c, então aceita H0;
se / > f C) então rejeita H0.
As somas de quadrados são mais facilmente calculadas, conforme as ex­
pressões apresentadas no Quadro 9.1.

2 5 2 ESTATÍSTICA
Quadro 9.1 Cálculos básicos da ANOVA com um fator.
Fonte de Somas de Quadrados
gl Razão
/
variação quadrados médios
r _ QMrrat
Entre g -
1 QMrrat
= ^
tratamentos t f n N & Trat QMetto
Dentro de Erro = SQrot ~ SQ-Trat N - g
•SQ QMlm
= f -
trat. (Erro) S^Erro
N -
1
Total S Q r „ = ± l y l - Ç
i=l j=l iV
Exemplo 9.4 Considere o problema de comparar três tipos de rede de compu­
tadores, Cl, C2 e C3, em termos do tempo médio de transmissão de pacotes de
dados entre duas máquinas. Realizou-se um experimento com oito replicações
com cada tipo de rede, aleatorizando a ordem dos 24 ensaios e mantendo fixos
os demais fatores controláveis (ver resultados na Tabela 9.3). Deseja-se testar
as hipóteses:
H0: os tempos esperados de transmissão são iguais para os três tipos de
rede; e
Hi’. os tempos esperados de transmissão não são todos iguais (depende
do tipo de rede).
Tabela 9.3 Resultados do experimento do Exemplo 9.4.
Tipo de rede
itepiicaçao
Cl C2 C3
1 7,2 7,8 6,3
2 9,3 8,2 6,0
3 8,7 7,1 5,3
4 8,9 8,6 5,1
5 7,6 8,7 6,2
6 7,2 8,2 5,2
7 8,8 7,1 7,2
8 8,0 7,8 6,8
Soma 65,7 63,5 48,1
Média 8,21 7,94 6,01

COMPARAÇÃO ENTRE TRATAMENTOS 2 5 3
Soma global: y.. = 177,3
Soma de quadrados: = (7,2)2 +(9,3Y + ... = 1344,25
i=l j=1
Sn y 2 - (®5,7 )2 + (63,5)2 +(48,1)2 (177,3 )2 _ oo nn
~ N ------------------ 8 24 ’
y>
SQ /brai = £ £ - V = 1 3 4 4 >2 5 - = 3 4 ’4 5
t=l ;=1 iV Z4
SQ£rro = SQTo[aI - SQTrat = 34,45 - 22,29 = 11,46
Resultando no quadro da ANOVA:
Fonte da variação SQ gl QM /
Entre grupos 22,99 2 11,50 21,07
Dentro dos grupos 11,46 21 0,55
Total 34,45 23
Adotando a = 0,05, temos o valor crítico f c = 3,47 (Tabela 6). Como o va­
lor calculado (f = 21,07) é superior ao valor crítico, então o teste rejeita H0,
provando estatisticamente que há diferença entre os três tipos de rede, em ter­
mos do tempo médio de transmissão.8
Análise dos resíduos
Já comentamos que o teste F é válido se os dados provêm de distribuições
normais com variância constante nos diferentes grupos. Essas suposições são
mais fáceis de ser verificadas a partir dos resíduos (diferenças entre valores ob­
servados e médias dos grupos):
eu = yij - y t d = 2, •••> g; j = h 2,..., n) (9.16)
A Figura 9.9 mostra os valores dos resíduos para cada tipo de rede e o grá­
fico de probabilidade normal dos resíduos. O primeiro gráfico indica que é ra-
8 Se a análise for feita com um software estatístico, ou mesmo com uma planilha eletrô­
nica, o sistema apresenta a tabela da ANOVA com o valor p associado à estatística F, bastando,
então, comparar p com o nível de significância estabelecido para decidir entre H0 e H,.

2 5 4 ESTATÍSTICA
zoável a suposição de variância constante nos três grupos; e o segundo mostra
os pontos em torno de uma linha, validando a suposição de normalidade dos
dados (ver seção 6.4).
Resíduos x fator Gráfico de probabilidade normal
CÖ
1,5 3
O 0,99
i,o G 2
CO 0,95
C/3
O 0,5 t O 1
D a 0,75
o
T **•— 3 « 0,0 T3 0 0,55
C/í 03 0,35
Ui
& -0 ,5 a; -1 0,15
Cl
C/i
O) 0,05
1,0 -2
- V-i 0,01
O
3
-1 ,5 ci - -1 o
C2 C3 £
Rede Resíduos
Figura 9.9 Avaliação das suposições da ANOVA através de gráficos dos resíduos.
Estimação das médias
As médias aritméticas de cada grupo servem como uma estimativa pontual
da resposta esperada de cada tratamento. Podemos, também, usar a abordagem
de intervalos de confiança para efetuarmos uma inferência mais completa. O
erro padrão pode ser estimado através da variância conjunta das g amostras.
Daí, o intervalo de confiança para o valor esperado da resposta sob o i-ésimo
tratamento é dado por:
(9.17)
onde £, é obtido na Tabela 4, em função do nível de confiança y estabelecido e
dos graus de liberdade: gl = g(n - 1).
Exemplo 9.4 (continuação) Usando nível de confiança de 95% e gl = N - g =
24 - 3 = 21, temos o valor tabelado t95o/o = 2,08. Então, para a rede Cl, temos:
JCfV, , 95%) = 8,21 ±2,08^ = 8,21+0,55
A Figura 9.10 apresenta graficamente intervalos de confiança para os três
tipos de rede.

COMPARAÇÃO ENTRE TRATAMENTOS 2 5 5
O
«CO
.a
B
g
<u
O
cx
B
£
Rede
Figura 9.10 Estimativas, através de intervalos de 95% de confiança, para o tem­
po esperado de transmissão, em três tipos de rede.
A Figura 9.10 sugere que as redes Cl e C2 podem ser consideradas com o
mesmo tempo esperado de transmissão, pois seus intervalos de confiança se so­
brepõem, indicando que a diferença entre as médias aritméticas pode ser mera­
mente casual. Já a rede C3 parece ser a causa do teste F da ANOVA ter rejeita­
do H0, pois apresenta um intervalo de confiança para a média não sobreposto
com os outros intervalos de confiança, evidenciando produzir tempo esperado
de transmissão menor.9
9.6.2 Amostras em blocos
Considere, agora, que as unidades experimentais são agrupadas em h blo­
cos, de tal forma que todos os g tratamentos sejam realizados em cada bloco,
conforme o esquema a seguir:
Tratam ento
Bloco Soma
1 2
8
1 yn y21 ys i y. i
2
yn y22 y. 2
• • • • ■ ■ •
• • ■ • •
h
yik y2h y.h
Soma yi. y2. y* y.. =X>,-. = 'Z y.i
)
«'
9 Sugerimos que a análise por intervalos de confiança seja feita somente após a ANOVA
rejeitar a hipótese de igualdade entre todas as médias, porque somente o teste F é construído es­
pecificamente para a comparação de vários tratamentos.

2 5 6 ESTATÍSTICA
Nesse projeto, cada observação pode ser influenciada pelo efeito do tra­
tamento, pelo efeito do bloco e pelo efeito aleatório. Assim, consideraremos:
Y9 = \x + %t + pj + 6y (9.18)
onde: jí é a média global da resposta;
Ti é o efeito do i-ésimo tratamento;
P,■ é o efeito do j-ésimo bloco; e
8y é o efeito aleatório (i = 1, 2, ..., g; j = 1, 2, ..., h).
Ao fazer a análise de variância, devemos excluir a variação devida aos blo­
cos da variação do erro experimental. O Quadro 9.2 mostra os cálculos de uma
ANOVA de um projeto em blocos, considerando em cada bloco uma observação
de cada tratamento (blocos completos não replicados), donde o número total de
observações é dado por N = gh.
Quadro 9.2 Cálculos da ANOVA num experimento em blocos completos não re­
plicado.
Fonte de Somas de Quadrados
Razão f
gl
variação quadrados médios
Entre s - i r _ QM-rrot
sq - f z L - £ QMJrat = s f ^
tratamentos t f h N 8 Trat ~ QMErro
h - 1
OM = ^®B!oco
'<IW
Entre blocos Bioco j
~ f í g N &
Bloco
SQ,m = (g-lKh-l)
Dentro (Erro) QM,,rú =
= SQrot - SQjyut - SQbíocc 8
Erro
N - 1
Total SQrc
= È t y J “
t=l
j=l N
Exemplo 9.5 Seja o problema de comparar três algoritmos de busca em um
banco de dados. Realiza-se um experimento com seis buscas experimentais,
sendo que em cada uma é sorteado um número aleatório que indica o registro
do banco de dados a ser localizado. Em cada um dos seis processos de busca,
são usados separadamente os três algoritmos em estudo, mas sob as mesmas
condições, em termos dos fatores controláveis. São anotados os tempos de res­
posta ao usuário.

COMPARAÇÃO ENTRE TRATAMENTOS 2 5 7
Inicialmente, queremos testar as hipóteses:
H0: em média, os três algoritmos são igualmente rápidos; e
Hi'. em média, os três algoritmos não são igualmente rápidos.
Resultados do experimento:
Algoritmo de busca
Ensaio
(bloco)
Al A2 A3
1 8,3 8,1 9,2
2 9,4 8,9 9,8
3 9,1 9,3 9,9
4 9,9 9,6 10,3
5 8,2 8,1 8,9
6 10,9 11,2 13,1
Soma 55,8 55,2 61,2
Média 9,43 9,2 10,2
ANOVA (usando as expressões do Quadro 9.2):
Fonte da variação SQ gl QM /
Algoritmos 3,64 2 1,82 14,29
Blocos 21,95 5 4,39
Erro 1,27 10 0,13
Total 26,86 17
Adotando a = 0,05, temos o valor crítico f c = 4,10 (Tabela 4 do apêndice,
com gl = 2 no numerador e gl = 10 no denominador). Como o valor calculado
(f = 14,29) é superior ao valor crítico, então o teste rejeita H0) provando esta­
tisticamente que há diferença entre os três algoritmos de busca, em termos do
tempo médio de resposta ao usuário.
Usando a mesma abordagem da seção anterior, construímos intervalos de
confiança para o tempo esperado de resposta para cada algoritmo (Figura
9.11). Observamos que os algoritmos Al e A2 são significativamente mais rápi­
dos que A3.

2 5 8 ESTATÍSTICA
Algoritmo
Figura 9.11 Estimativas, através de intervalos de 95% de confiança, para o tem­
po esperado de resposta de três algoritmos de busca em banco de dados.
9.7 ANOVA EM PROJETOS FATORIAIS
Nos estudos experimentais, em geral procuramos avaliar ou testar o efeito
de mais de um fator sobre uma resposta de interesse. Por exemplo, o profissio­
nal de informática pode estar interessado em estudar o tempo de resposta para
o usuário quando se varia a topologia, o protocolo e o número de nós de uma
rede local. O engenheiro civil quer conhecer o quanto o tempo de hidratação, a
dosagem de cimento e o uso de aditivos interferem na resistência à compressão
de um concreto. O engenheiro químico quer saber a influência da temperatura
e do tempo de reação sobre o rendimento de uma reação química.
Um projeto experimental é dito fatorial quando cada nível de um fator é
ensaiado com todos os níveis dos outros fatores, sem restrições. E o primeiro in­
teresse, normalmente, é testar se existe diferença no valor esperado da resposta
entre os níveis de cada fator, além de testar eventuais interações entre os fato­
res.10 Nesta seção, restringiremos o estudo a um projeto fatorial com dois fatores.
Sejam dois fatores, A e B, com g e h níveis, respectivamente. Considere
que em cada cruzamento dos níveis desses fatores sejam realizadas n replicações.
As N = ghn observações podem ser descritas pelo seguinte modelo estatístico:
Yijk = n + t( + Pj + (tPXj + eijk (9.19)
onde: jí é a média global da resposta (independentemente dos efeitos dos fa­
tores);
Tj é o efeito do i-ésimo nível do fator A;
10 Dizemos que existe interação entre dois fatores quando a diferença na resposta entre
os níveis de um fator não é a mesma para todos os níveis do outro fator (ver Capítulo 2).

COMPARAÇÃO ENTRE TRATAMENTOS 2 5 9
P; é o efeito do ;'-ésimo nível do fator B;
(xp)y é o efeito da interação entre x* e p,; e
eijk é o efeito aleatório ou erro experimental (i = 1, 2, ..., g; j = 1, 2, ...,
h; k = 1, 2, ..., n).
Uma única análise de variância permite efetuar três testes estatísticos, as­
sociados às seguintes hipóteses nulas:
H ^ : Ti = t 2 = .... = x* = 0 (não há diferença no valor esperado da
resposta nos g níveis do fator A);
H fp: Pi = p2 = .... = P/j = 0 (não há diferença no valor esperado da
resposta nos h níveis do fator B);
H ^ : (xP)íj = 0, V i,; (não há interação entre os fatores A e B).
Sejam as N = ghn observações e as seguintes notações de somas:
Fator A
Fator B Soma
1 2 8
1 •••> .Xlln 3^211> 3^21n ygn> ygin y. i.
2
y 121» •••> y 12n y221> •••> y
22
n yg2U ^g2n y.2.
• • • • a • • • • • • • • •
m
h
yihi> •••> y i/m y2h\y y2hn y^hl» y ghn y./,.
y\.. y2.. yg... y... = I > i. = 'Ey.).
Soma
i )
A soma das observações em cada caseia é representada por:
n
(9.20)
y,, = X y iik
k=1
E a soma de quadrados entre as caseias é dada por:
s o = f y (9.21)
ot t í h n N
O Quadro 9.3 apresenta os cálculos para a realização de uma ANOVA para
esse tipo de projeto experimental.

2 6 0 ESTATÍSTICA
Quadro 9.3 Cálculos da ANOVA num projeto fatorial com dois fatores.
Fonte de Somas de Quadrados
Razão /
gl
variação quadrados médios
Qm a
Fator A qm a = ^ f _
g~ 1
,-= i hn N QMEno
^ y 2 v 2 f QMb
Fator B SQs = 1 - ^ h - 1
QMb
M — gn N giB
Interação SQaB =
(g-lXh- 1) QM,b =
r
_
QMflB
A*B = SQsubtot ~ SQa ~ SQb QMEno
Erro SQfjto = SQtoí “ SQsuòror hg(n - 1) = SCJ ^
S^Erro
Total s Q r « = H ± y l - Ç N - 1
t=l j=l k=1 iV
Exemplo 9.6 Considere o problema de comparar três topologias de rede de
computadores (Cl, C2 e C3) e dois protocolos (LI e L2), em termos do tempo
de resposta ao usuário. Realizou-se um experimento com quatro replicações em
cada combinação de topologia e protocolo. Deseja-se verificar se há diferenças
entre as topologias, entre os protocolos e eventual interação entre topologia e
protocolo. Então, deseja-se testar as seguintes hipóteses nulas:
H0(a): tempos esperados de resposta são iguais para as três topologias;
os
H0(B): os tempos esperados de resposta são iguais para os dois protocolos;
H0(ab): a mudança de protocolo não altera as diferenças médias do tem­
po de resposta nas três topologias (ausência de interação).
Resultados do experimento:

COMPARAÇÃO ENTRE TRATAMENTOS 2 6 1
Topologia
Protocolo Soma Média
Cl C2 C3
LI 6,2 5,9 5,9 y.i. = 82,8 6,90
7,6 8,4 6,2
7,2 7,1 5,2
8,8 7,1 7,2
L2 9,0 7,1 6,2 y.2. = 95,9 7,99
8,9 8,6 6,1
9,4 9,1 8,9
8,0 7,8 6,8
Soma Yl. = 65,1 y2.. = 6 i,i y3 = 52,5 Y... = 178,7
Média 8,21 7,94 6,01 7,45
Soma das observações em cada caseia (yíf ):
Topologia
Protocolo ----------------------------------
Cl C2 C3
LI 29,8 28,5 24,5
L2 35,3 32,6 28,0
Somas de quadrados:
f ^ - 1 7 , 7 7
h h n N 4 24
SQro, = £ y l - £ = 1365,49 1330,57 34,92
t £ - =
i= 1 ;=1 *=1 JN
SQ — = 10727,47 -1330,57 = 10,36
Ti hn N 8
SQ* = è — - — = 16052,65 -1330,57 = 7,15
B U gn N 12
A ANOVA e os valores críticos, f c, ao nível de significância de 5%, são des­
critos a seguir:

opmeT
2 6 2 ESTATÍSTICA
Fonte da variação SQ gl QM / /c
Topologia 10,36 2 5,18 5,44 3,55
Protocolo 7,15 1 7,15 7,51 4,41
Interação 0,26 2 0,13 0,14 3,55
Erro 17,14 18 0,95
Total 34,92 23
Concluímos que tanto as diferentes topologias, quanto os diferentes proto­
colos utilizados alteram significativamente a média de tempo ao usuário, mas
não há interação entre esses dois fatores.
No projeto fatorial, os valores preditos são as médias dos subgrupos:
h = 1 1 y ,k (9.22)
Tl k
=1
e os resíduos são as diferenças entre os valores observados e a média do respec­
tivo subgrupo:
^ijk = ytjk ~ ytj. (9.23)
A Figura 9.12 (a) ilustra as médias do tempo de resposta para cada topolo­
gia e protocolo; e a Figura 9.12 (b) apresenta o gráfico dos valores preditos
com os resíduos.
(a) Perfil das médias (b) Análise dos resíduos
2.5
2,0
1.5
CO/J 1,0
3
T3 0,5
'»H 0,0
0O0)
ctí -0,5
-1,0
-1,5
2,0
-
5,5 6,0 6,5 7,0 7,5 8,0 8,5 9,0 9,5
Topologia Valores preditos
Figura 9.12 (a) Média do tempo de resposta ao usuário, por topologia e protoco­
lo, e (b) gráfico dos valores preditos com os resíduos.
Na Figura 9.12 (a), podemos observar diferenças entre os níveis dos dois
fatores, mas os perfis são quase paralelos, o que levou o teste F a aceitar que os
dois fatores agem aditivamente (ausência de interação).

COMPARAÇÃO ENTRE TRATAMENTOS 2 6 3
Na Figura 9.12 (b), observamos que os pontos se distribuem aleatoriamen­
te em tomo da linha horizontal, associada ao resíduo nulo. Além disso, os pon­
tos estão em maior intensidade perto da linha horizontal. Isso sugere que as su­
posições de normalidade e variância constante estão razoavelmente satisfeitas,
validando os resultados da ANOVA.
9.8 ANOVA EM PROJETOS DO TIPO 2*
Como discutimos no Capítulo 2, quando se quer analisar muitos fatores, é
comum iniciar com um experimento em que todos os fatores são ensaiados em
apenas dois níveis. Havendo replicações, podemos verificar formalmente a sig-
nificância de cada efeito através do teste F e, nesses projetos, os cálculos da
ANOVA são relativamente simples.11
Sejam:
k o número de fatores;
n o número de observações em cada condição experimental (número de
replicações); e
- 1, se oj-ésimo fator for ensaiado do nível inferior, no
i-ésimo ensaio (; = 2 , N; j =
+ 1, se o;'-ésimo fator for ensaiado no nível superior, = 1, 2, ..., k).
no í-ésimo ensaio12
Em um projeto com k = 3 fatores e n = 2 replicações, temos um total de
N = 2k n = 16 observações. A Tabela 9.4 mostra os Cy associados aos fatores A,
B e C, além dos cí; associados às interações AB, AC, BC e ABC, que são obtidos
pela multiplicação elemento a elemento das colunas dos fatores envolvidos. Em
geral, num projeto 2k, o número total de fatores e interações é igual a 2k - 1.
A soma de quadrados total é obtida por:
<«■»
i=l iV ^ i=i )
11 Para projetos do tipo fracionado 2k~p, pode-se usar o mesmo processo desta seção,
substituindo nas fórmulas k por k - p.
12 Para fatores qualitativos, alocamos, arbitrariamente, o código -1 para uma categoria;
e +1 para a outra categoria.

2 6 4 ESTATÍSTICA
A soma de quadrados do efeito; (j = 1, 2, ..., 2k~ !), associada a um fator
ou a uma interação entre fatores, pode ser calculada por:
S Q ; = ^ ( Í > ^ ) 2 (9.25)
A soma de quadrados do erro pode ser obtida pela diferença:
SQim, = SQT0! - X SQ; (9.26)
j=1
Todas as SQj (j = 1, 2, ..., 2k ~!) têm apenas um grau de liberdade cada
uma, enquanto a SQErro tem N - 2k graus de liberdade.
Exemplo 9.7 Usaremos o problema do Exemplo 2.6, em que descrevemos um
estudo para verificar os fatores que influenciam a qualidade da transmissão de
dados através da porta serial de microcomputadores com cabos longos. Obser-
vou-se a taxa de falhas de transmissão (y) em função dos fatores: 04) velocida­
de da transmissão (2400/9600 bauds), (£) tamanho do arquivo (100/200
bytes) e (C) comprimento do cabo serial (15/20 m). O experimento foi realiza­
do com duas replicações. Os sinais para o cálculo dos efeitos e os resultados do
experimento são apresentados na Tabela 9.4.
Tabela 9.4 Projeto experimental e resultados do experimento do Exemplo 9.7.
Ensaio* Replicação A B C AB AC BC ABC y
1 1 _ j _ J _ J 1 1 1 - 1 32,5
2 2 — 1 — 1 — 1 1 1 1 - 1 32,3
3 1 — 1 — 1 1 1 — 1 — 1 1 35,7
4 2 — 1 — 1 1 1 — 1 — 1 1 35,9
5 1 — 1 1 — 1 — 1 1 — 1 1 33,1
6 2 — 1 1 — 1 — 1 1 — 1 1 33,4
7 1 — 1 1 1 — 1 — 1 1 - 1 35,9
8 2 — 1 1 1 — 1 — 1 1 - 1 36,1
9 1 1 — 1 — 1 — 1 — 1 1 1 34,1
10 2 1 — 1 — 1 — 1 — 1 1 1 34,4
11 1 1 — 1 1 — 1 1 — 1 - 1 36,6
12 2 1 — 1 1 — 1 1 — 1 - 1 36,9
13 1 1 1 — 1 1 — 1 — 1 - 1 34,2
14 2 1 1 — 1 1 — 1 — 1 - 1 34,2
15 1 1 1 1 1 1 1 1 37,1
16 2 1 1 1 1 1 1 1 36,9
* A ordem de realização dos ensaios foi aleatória.

COMPARAÇÃO ENTRE TRATAMENTOS 2 6 5
Aplicando (9.24) e (9.25), temos:
SQro, = 19590,67 - (55y ) = 39,639
t=l N \ i=l ) lv>
2
SQA = — f ! = — (-32,5-...-36,1+ 34,1+ ...+ 36,9 ) 2 =5,641
16
As somas de quadrados dos demais efeitos são calculadas de forma análo­
ga, resultando na seguinte ANOVA:
Fonte da variação QM
SQ gl /
A 5,641 1 5,641 208,9
B 0,391 1 0,391 14,5
C 32,776 1 32,776 1.213,9
A*B 0,181 1 0,181 6,7
A*C 0,181 1 0,181 6,7
B*C 0,031 1 0,031 1,1
A*B*C 0,226 1 0,226 8,4
Erro 0,215 8 0,027
Total 39,639 15
Para testar a significância de cada efeito, comparamos os valores calcu­
lados de/com o valor crítico da distribuição F, com gl = 1 no numerador e gl = 8
no denominador. Pela Tabela 4 do apêndice, o valor crítico é fc = 5,32. Assim,
com exceção da interação B*C, todos os outros efeitos são significativos.
EXERCÍCIOS
10. Com o objetivo de comparar três tipos de cimento em termos da resistência
à compressão do concreto, foi realizado um experimento completamente
aleatorizado, com cinco corpos de prova de cada tipo de cimento. Os resul­
tados foram os seguintes:
Cimento Resistência à compressão
1 9 12 10 8 15
2 20 21 23 17 30
3 10 9 12 20 11

2 6 6 ESTATÍSTICA
a) Faça uma ANOVA e verifique se há evidência de que existe diferença real
entre as resistências médias dos três tipos de cimento. Use a = 0,05.
b) Construa intervalos de 95% de confiança para as médias.
c) Através da análise dos itens anteriores, pode-se dizer que existe um ci­
mento melhor (maior valor esperado de resistência à compressão) que
os outros. E pior?
11. Considerando os dois primeiros tipos de cimento do Exercício 10, verifique
se existe diferença significativa entre as variâncias dos tempos de resposta.
Use a = 0,05.
12. Para comparar a absorção de água de quatro tipos de massa cerâmica, ana-
lisaram-se corpos de prova de três fornadas. Em cada fornada (bloco), era
analisado um corpo de prova de cada tipo de massa cerâmica. Os resulta­
dos (porcentagem de absorção de água) foram:
Massa cerâmica
romaaa
Cl C2 C3 C4
1 1,2 1,5 1,1 2,1
2 2,1 2,1 1,3 2,7
3 1,5 1,9 1,3 2,4
Os dados mostram evidência suficiente para garantir diferença na por­
centagem esperada de absorção de água nos quatro tipos de massa cerâmi­
ca? Use a = 0,05.
13. Considere o problema de estudar os efeitos do tamanho da memória princi­
pal (fator A) e tamanho da memória cache (fator B) no desempenho de um
sistema de arquivos de uma rede local de computadores (LAN). O fator A
foi ensaiado nos níveis 128 e 256 Mbytes e o fator B nos níveis 256 e 512
kbytes, segundo um projeto fatorial com 3 replicações. A medida de desem­
penho do sistema foi o número de operações de transferência de arquivos
por segundo. Os resultados foram os seguintes:
Memória principal
Memória
cache
128 Mbytes 256 Mbytes
256 kbytes 500 1.100
550 1.140
540 1.090
512 kbytes 900 1.900
850 1.950
920 1.910
Baseado em exemplo de FREITAS, P. J. Introdução à modelagem e simula­
ção de sistemas. Visual Books, 2001, p. 277. Com permissão do Autor.

COMPARAÇÃO ENTRE TRATAMENTOS 2 6 7
ANOVA
Fonte da variação SQ gl QM f
Memória cache 1.026.675
Memória principal 1.944.075
Interação 151.875
Erro 6.800
Total 3.129.425
a) Complete a tabela da ANOVA acima.
b) Quais efeitos são significativos?
c) Os efeitos da memória cache e da memória principal podem ser anali­
sados isoladamente? Explique.
14. Para estudar o desempenho, em termos do tempo de resposta (em segun­
dos), de 3 processadores (pro 1, pro 2 e pro 3), sob quatro tipos diferentes
de carga de trabalho (cargas 1, 2, 3 e 4), foi realizado um projeto fatorial
com 2 replicações. Os resultados foram os seguintes:
Tempo de resposta (s)
Processador
Tipo de carga
de trabalho
Pro 1 Pro 2 Pro 3
Carga 1 17 8 28
20 10 27
Carga 2 10 18 27
7 13 31
Carga 3 13 18 30
15 21 23
Carga 4 21 7 32
17 12 26
a) Complete a tabela da ANOVA e descreva as conclusões.
Fonte da variação SQ gl QM f
Processador 1.028
Tipo de carga 18
Interação 286
Erro 102
Total 1.934

2 6 8 ESTATÍSTICA
b) Apresente um gráfico apropriado para observar uma possível interação
entre os dois fatores.
c) Existe um processador que pode ser considerado superior aos outros?
Explique.
EXERCÍCIOS COMPLEMENTARES
15. No desenvolvimento de um sistema de reconhecimento de fala, fez-se um
experimento para avaliar dois tipos de parâmetros acústicos: MFCC (Com­
ponentes Mel Cepstrais) e NMF (Componentes Mel Cepstrais Normaliza­
dos). Foram observadas duas amostras independentes com cada tipo de pa­
râmetro e anotadas as taxas de acerto (em %):13
MFCC: 78,67 81,00 84,67 80,97 81,46
85,12 80,32 80,95 84,76
NMF: 86,67 88,33 92,67 88,05 89,76
93,66 86,03 87,94 91,75
a) Há evidência de diferença entre os dois parâmetros acústicos, em ter­
mos da taxa média de acertos? Use a = 0,01.
b) E em termos de variabilidade? Use a = 0,05.
c) Considere que o experimento tenha sido feito de forma pareada, isto é,
em cada conjunto de ensaios, para reconhecimento de fala, o sistema
rodava com os dois parâmetros (MFCC e NMF) paralelamente. Supo­
nha que os resultados apresentados estão na ordem correta dos pares.
Refaça o item (a).
16. Com respeito ao exercício anterior, também foi avaliado o parâmetro
RNMF (Componentes Mel Cepstrais Normalizados em Tempo Real), com
os seguintes resultados:
RNMF: 77,67 81,67 89,69 80,73 82,43
90,97 77,14 81,27 88,89
13 Os exercícios 15 a 17 foram baseados em trabalho de disciplina dos acadêmicos Ruy
Seara Jr. e Izabel Seara, no Curso de Pós-Graduação em Ciências da Computação/UFSC, 2003.

COMPARAÇÃO ENTRE TRATAMENTOS 2 6 9
a) Analisando como um projeto completamente aleatorizado com um fa­
tor (parâmetro), verifique se há diferenças significativas entre os três
parâmetros. Use a = 0,01.
b) Em cada conjunto de ensaios para reconhecimento de fala, o sistema
rodava com os três parâmetros (MFCC, NMF e RNMF) paralelamente.
Analisando como um projeto em blocos (nove blocos e três tratamen­
tos), verifique se há diferenças significativas entre os três parâmetros.
Use a = 0,01.
17. Ainda com respeito ao Exercício 15, foram avaliados alguns ruídos de
preenchimento (nenhum, uniforme e Rl), que podem melhorar o reconhe­
cimento de fala. O projeto foi o fatorial com dois fatores (parâmetro e ruí­
do), tendo três replicações, e produzindo os resultados:
Ruído de preenchimento
Parâ­
metro
Nenhum Uniforme Rl
MFCC 78,67 81,00 84,67 80,97 81,46 85,12 80,32 80,95 84,76
NMF 86,67 88,33 92,67 88,05 89,76 93,66 86,03 87,94 91,75
RNMF 77,67 81,67 89,69 80,73 82,43 90,97 77,14 81,27 88,89
Realize uma ANOVA para verificar se existe efeito significativo de Pa­
râmetro, Ruído e interação. Use a = 0,01.
18. Um produto usado como piso na “maternidade” da criação de suínos é fa­
bricado por injeção de plástico. Na tentativa de melhorar a qualidade do
produto, realizou-se um experimento, variando os fatores: (A) tempo de
resfriamento, (B) temperatura do fluído, (C) percentual de elastrômetro e
(D) percentual de talco, de acordo com um projeto fatorial 24 com duas re­
plicações. A variável resposta foi a dureza (HRc) do material produzido. Os
resultados foram:14
14 Parte dos dados experimentais do trabalho de dissertação (Engenharia de Produção)
de Morgana Pizzolato. UFRGS, 2002.

2 7 0 ESTATÍSTICA
A B C D Yi y2
_ J _ J ] _ J
_ 51,7 49,4
— 1 — 1 — 1 1 75,2 76,0
— 1 — 1 1 — 1 65,9 60,0
— 1 — 1 1 1 63,7 69,6
— 1 1 — 1 — 1 71,1 72,9
— 1 1 — 1 1 67,1 69,1
— 1 1 1 — 1 71,9 75,1
— 1 1 1 1 52,8 57,6
1 — 1 — 1 — 1 74,5 67,0
1 — 1 — 1 1 54,5 70,3
1 — 1 1 — 1 71,3 70,5
1 — 1 1 1 73,4 74,3
1 1 — 1 — 1 58,5 58,5
1 1 1 1 49,2 50,2
—
1 1 1 1 71,8 71,5
—
1 1 1 1 72,4 66,6
Calcule os efeitos de cada fator isoladamente (efeitos principais). Tes­
te a signifícância de cada efeito principal ao nível de significância de 10%.
19. Estudo do desempenho de uma central de comutação telefônica para servi­
ços especializados, tais como: auxílio à lista, hora certa etc. Fatores em es­
tudo: (A) número de linhas ligadas à rede pública (250 ou 400), (B) núme­
ro de filtros digitais para o reconhecimento de cifras do cliente que disca
(80 ou 120), (C) número de canais de máquinas de mensagem (180 ou
270) e (D) número de atendentes conectadas ao sistema (200 ou 300). A
variável resposta foi o tempo de resposta ao usuário, considerando o mo­
mento do atendimento até o cliente receber a resposta de sua solicitação.
Foram simuladas respostas, segundo um projeto 24 com quatro replicações.
Os resultados estão apresentados a seguir, onde -1 refere-se ao nível infe­
rior do fator e +1 ao nível superior.15
15 Parte da dissertação de mestrado de Marcus Vinícius Silva, Ciência da Computação,
UFSC, 2002.

COMPARAÇÃO ENTRE TRATAMENTOS 2 7 1
A B C D Tempo (s)
J
— J __ J — _ J 51,58 51,33 51,44 51,41
1 1 1 1 42,31 42,22 42,16 42,22
— — —
1 1 1 1 51,58 51,33 51,44 51,41
— — —
1 1 1 1 42,31 42,22 42,16 42,22
— —
1 1 1 1 51,58 51,33 51,44 51,41
— — —
1 1 1 1 42,19 42,21 42,04 42,24
— —
1 1 1 1 51,58 66,59 51,44 51,41
— —
1 1 1 1 42,19 49,95 42,04 42,24
—
1 1 1 1 66,87 66,59 66,81 66,58
— — —
1 1 1 1 50,23 49,95 49,93 49,62
— —
1 1 1 1 66,87 66,59 66,81 66,58
— —
1 1 1 1 50,23 49,95 49,93 49,62
—
1 1 1 1 66,87 66,88 66,54 66,81
— —
1 1 1 1 49,42 49,41 49,40 49,05
—
1 1 1 1 66,87 66,88 66,54 66,81
—
1 1 1 1 49,42 49,41 49,40 49,05
a) Calcule os efeitos de cada fator isoladamente (efeitos principais) e as
interações entre dois fatores.
b)
Teste a significância (a = 0,05) de cada efeito calculado no item (a).
20. Um processo químico é influenciado pelo tempo e pela temperatura de rea­
ção. Um experimento é realizado para diferentes níveis do tempo de reação
(20, 25 e 30 minutos) e da temperatura de reação (60, 70 e 80° C), segundo
um projeto fatorial com seis replicações. A resposta é o rendimento (em %).
Usando a planilha eletrônica Excel, obtiveram-se os seguintes resultados:16
Médias por tratam ento
Tempo (minutos)
(° C)
20 25 30
60 30,5 31,4 34,0
70 35,0 38,2 38,2
80 35,6 35,6 35,3
16 No Excel, acionar “Ferramentas”, “Análise de dados” e “Anova: duplo fator com re­
petição”.

2 7 2 ESTATÍSTICA
ANOVA
Fonte da variação SQ gl QM / Valor-P F crítico
Temperatura 251,25 2 125,62 18,64 l,3E-06 3,20
Tempo 41,84 2 20,92 3,10 0,0546 3,20
Interação 38,77 4 9,69 1,44 0,2370 2,58
Erro 303,27 45 6,74
Total 635,12 53
Interprete os resultados.

10
Testes Não Paramétricos
Os testes descritos no Capítulo 9 são ditos paramétricos, porque supõem
que os dados seguem determinada distribuição de probabilidades - no caso, a
distribuição normal. Imagine que as suposições necessárias para a aplicação dos
testes paramétricos não sejam satisfeitas. Suponha que ocorram alguns dos ca­
sos abaixo:
1. Os dados sob análise têm um nível de mensuração qualitativo: ordi­
nal ou nominal.
2. Os dados sob análise têm nível de mensuração quantitativo, mas há
indícios de que a distribuição populacional não é normal.
3. Há interesse em realizar inferência sobre outras características da
população, além dos parâmetros de sua distribuição, como a própria
forma da distribuição.
Uma alternativa para essas situações é a utilização dos testes não paramé­
tricos, ou testes livres de distribuição. As suposições necessárias para a aplicação
desses testes são menos rígidas que as dos paramétricos, possibilitando uma
aplicação mais generalizada. Obviamente, suposições mais relaxadas significam
que o poder estatístico de um teste não paramétrico é inferior ao teste paramé­
trico equivalente, mas, em muitos casos, é a única alternativa disponível para
análise dos dados e realização da inferência estatística.
Este texto abordará basicamente três tipos de testes não paramétricos: tes­
tes de aderência, testes de independência e testes de comparação de popula­
ções. A Figura 8.1 permite visualizar alguns testes não paramétricos.

2 7 4 ESTATÍSTICA
Figura 10.1 Alguns testes não paramétricos. Os testes marcados com asterisco não
serão abordados neste texto.
As próximas seções irão detalhar alguns dos testes não paramétricos mais
importantes, mostrando as condições para sua aplicação e apresentando
exemplos.
10.1 TESTES DE ADERENCIA
O objetivo de um teste de aderência é verificar se os dados de uma amos­
tra comportam-se de acordo com uma distribuição teórica. Essa distribuição
teórica pode ser uma distribuição de probabilidades clássica (como normal, ex­
ponencial etc.), ou proporções definidas especificamente para o problema (por
exemplo, a Lei de Mendel para ervilhas lisas e rugosas).

TESTES NÃO PARAMÉTRICOS 2 7 5
10.1.1 Teste qui-quadrado de aderência
O teste qui-quadrado de aderência pode ser aplicado quando estamos estu­
dando dados distribuídos em categorias e há interesse em verificar se as fre­
quências observadas nas K diferentes categorias (Ot-, i = 1, 2, K) são signifi­
cativamente distintas de um conjunto de K frequências esperadas (£t, £ = 1, 2,
..., K).1 As hipóteses são:
H0: O, = £, para todo i = 1, 2, K\
Hi’. Oi * Ei para algum £ = 1, 2, ..., K.
A estatística desse teste, chamada de Q2, é uma espécie de medida de dis­
tância entre as frequências observadas e as frequências esperadas de cada cate­
goria. Sua expressão é dada por:
(10.1)
Q2 = £
i= 1 E:
Havendo aderência (H0 verdadeira), as frequências observadas devem ficar
próximas das esperadas, acarretando um valor pequeno para Q2: as variações
encontradas seriam apenas casuais. Contudo, se não houver aderência (Hi ver­
dadeira), diferenças entre frequências observadas e esperadas poderão ser
grandes, resultando em um valor grande para Q2: é pouco provável que as varia­
ções tenham sido casuais.
Supondo amostra grande (digamos, E{ > 5 para todo i = 1, 2,..., K) e su­
pondo a hipótese de aderência (H0 verdadeira), a estatística Q2 segue aproxima­
damente uma distribuição qui-quadrado com K - 1 graus de liberdade. Observada
uma amostra, podemos obter o valor da estatística Q2, o qual representaremos
por q2. Usando a abordagem clássica, obtemos o valor crítico x 2C, em função do
nível de significância a adotado, formando a seguinte regra de decisão:
q2 < x ] => aceita H0 (há aderência à distribuição especificada)
q2 >Xc => rejeita H0 (não há aderência à distribuição especificada)
Exemplo 10.1 Determinado veículo utilitário está sofrendo pesadas críticas
de seus proprietários, com relação à grande frequência de defeitos no pneu tra­
seiro esquerdo. Preocupado com sua imagem, e procurando defender-se de
1 Os dados em categorias podem provir de uma variável qualitativa ou mesmo de uma
variável quantitativa (discreta ou contínua). No caso de dados de variáveis contínuas, torna-se
necessário categorizá-los, formando uma distribuição de frequências com dados grupados (Capí­
tulo 3).

2 7 6 ESTATÍSTICA
eventuais pedidos de indenização, o fabricante do veículo resolveu coletar in­
formações sobre 152 ocorrências de defeitos, classificando-as por posição do
pneu. Os resultados estão na Tabela 10.1. Usando nível de significância de 5%,
há razão para acreditar que a probabilidade de defeito é diferente para alguma
das posições?
Tabela 10.1 Ocorrências de defeitos por posição do pneu de um veículo utilitário.
Posição Dianteiro Dianteiro Traseiro Traseiro
Total
do pneu esquerdo direito esquerdo direito
Frequência 35 32 57 28 152
Para responder à questão colocada, temos as seguintes hipóteses:
H0: as frequências de defeitos nos quatro pneus são iguais;
Hx: pelo menos uma das frequências de defeitos nos pneus é diferente.
Se H0 for verdadeira, as 152 ocorrências devem distribuir-se igualmente
pelas quatro categorias, resultando na frequência esperada de cada categoria
igual a 15% = 38 ocorrências. Calculando q2:
Dianteiro Dianteiro Traseiro Traseiro
esquerdo direito esquerdo direito
(35 - 38)2/38 = (32 - 38)2/38 = (57 - 38)2/38 = (28 - 38)2/38 =
= 0,237 = 0,947 = 9,5 = 2,632
E, portanto:
q2 = 0,237 + 0,947 + 9,5 + 2,632 = 13,316
Abordagem clássica.2 Para construir a regra de decisão, obtemos o valor
crítico % c da distribuição qui-quadrado, com gl = K - 1 = 4 - 1 = 3 graus de li­
berdade, o qual leva à P(Q2 > x c2) = a = 0,05. Usando a Tabela 5 do apêndice,
obtém-se x] = 7,815, tal como mostrado na Figura 10.2.
2 Neste capítulo, adotaremos apenas a abordagem clássica na resolução dos exemplos,
embora o uso da abordagem do valor p possa ser realizado de forma análoga aos capítulos ante­
riores.

TESTES NÃO PARAMÉTRICOS 2 7 7
aceita Hr
rejeita H0
Figura 10.2 Regra de decisão de um teste de aderência usando o modelo qui-qua-
drado com 3 graus de liberdade.
Como q2 = 13,316 cai na região de rejeição, o teste rejeita H0 em favor de
Hi. Assim, há evidência de que as frequências de ocorrência dos defeitos depen­
dem da posição do pneu.
10.1.2 Teste de Kolmogorov-Smirnov
Considere uma situação em que desejamos verificar a aderência de um
conjunto de valores em relação a uma distribuição de probabilidades especifica­
da (discreta ou contínua). Embora seja possível aplicar o teste qui-quadrado
de aderência, geralmente é melhor aplicar o chamado teste de aderência de
Kolmogorov-Smirnov, que é uma alternativa mais poderosa do que o teste
qui-quadrado, nestas situações.
Seja F(x) a função de distribuição acumulada, com parâmetros especificados,
para a qual se quer verificar a aderência dos dados. As hipóteses são:
H0: os dados provêm de F(x) (há aderência);
Hi". os dados não provêm de F(x) ([não há aderência).
Sejam as distribuições de frequências acumuladas: a empírica, S(x), e a
teórica, F(x). Para cada elemento da amostra, obtém-se a diferença absoluta en­
tre essas duas distribuições. A estatística do teste é a diferença absoluta máxi­
ma, D. O procedimento é descrito a seguir.
1. Definimos SQc) para cada valor xt (i = 1, 2, n) como:
çr . _ número de valores < x { n n
n
onde n é o tamanho da amostra e xt é um valor qualquer da amostra.

2 7 8 ESTATÍSTICA
2. Obtemos, para cada valor xt (£ = 1, 2, n), os valores teóricos FQc,),
calculados pela função de distribuição acumulada F(x), especificada
em H0. Observe que, se a amostra realmente provém de uma popu­
lação que segue a distribuição teórica F(;c), a distribuição observada
SOO não deve afastar-se muito de FM .
3. Verificamos a discrepância entre SQc) e F(x) através das diferenças
absolutas entre F(xD e S(jcJ, e entre F(jcf) e SCx^), para i = 1, 2,..., n.
4. Calculamos a estatística de teste, D, em termos da amostra em aná­
lise:
(10.3)
5. Uma vez identificada a distância máxima d (valor de D para a parti­
cular amostra em análise), comparamos seu valor com um valor ta­
belado, d,., de acordo com o nível de signifícância a e do tamanho n
da amostra (ver Tabela 7 do apêndice). Regra de decisão:
d < dc => aceita H0 (há aderência à distribuição especificada);
d> dc => rejeita H0 (jião há aderência à distribuição especificada).
Exemplo 10.2 Um fabricante de autopeças está próximo de fechar um grande
contrato com uma montadora. O ponto-chave é a garantia da qualidade de seus
produtos, especialmente do diâmetro (em mm) dos eixos produzidos, que ele
supõe seguir uma distribuição normal com média 100 e desvio padrão 2. A
montadora selecionou uma amostra aleatória de 15 eixos, para testar as especi­
ficações a 5% de signifícância. Os valores estão descritos a seguir:
93,45 94,46 94,93 96,17 96,74 97,07 97,68 97,93 99,10
99,30 100,73 103,29 103,60 103,83 105,20
O diâmetro é uma variável contínua e desejamos verificar a aderência a
uma distribuição normal com média e desvio padrão fornecidos. Assim, o teste
de aderência de Kolmogorov-Smirnov pode ser empregado. As hipóteses são:
H0: a amostra provém de uma população que segue uma distribuição
normal com f! = 100 e a = 2 mm;
Hi". a amostra não provém de uma população que segue distribuição
normal com |i = 100 e a = 2 mm.

TESTES NÃO PARAMÉTRICOS 2 7 9
1. Construção da distribuição acumulada da amostra, S(jc):
Valores Frequência
S M
ordenados relativa
93,45 1/15 1/15 = 0,067
94,46 1/15 2/15 = 0,133
94,93 1/15 3/15 = 0,200
96,17 1/15 4/15 = 0,267
96,74 1/15 5/15 = 0,333
97,07 1/15 6/15 = 0,400
97,68 1/15 7/15 = 0,467
97,93 1/15 8/15 = 0,533
99,10 1/15 9/15 = 0,600
99,30 1/15 10/15 = 0,667
100,73 1/15 11/15 = 0,733
103,29 1/15 12/15 = 0,800
103,60 1/15 13/15 = 0,867
103,83 1/15 14/15 = 0,933
105,20 1/15 15/15 = 1,000
2. Construção da função de distribuição acumulada F(x), para cada va­
lor xi (i = 1, 2, n). Cada valor de diâmetro x pode ser convertido
em escore padronizado z. Por exemplo, para x Y = 93,45, temos:
= = 93,45 -100 = _3
a 2
A probabilidade acumulada até cada escore z é obtida da Tabe­
la 3, resultando nos seguintes valores F(xt):
*z F M
0
93,45 - 3,28 0,001
94,46 - 2,77 0,003
94,93 - 2,54 0,006
96,17 - 1,92 0,028
96,74 - 1,63 0,052
97,07 - 1,47 0,071
97,68 - 1,16 0,123
97,93 - 1,04 0,150
99,10 - 0,45 0,326
99,30 - 0,35 0,363
100,73 0,37 0,643
103,29 1,64 0,950
103,60 1,80 0,964
103,83 1,91 0,972
105,20 2,60 0,995

2 8 0 ESTATÍSTICA
3. Obtenção das diferenças absolutas entre as distribuições acumuladas
esperadas e observadas, | F(xf) - S(xt) | e | F(Xj) - S(ximl) | :
*i S(*f) F(xf) |F(xf) - S(Xm)| \Fixd - S{xJ\
0 0
93,45 0,067 0,001 0,001 0,066
94,46 0,133 0,003 0,064 0,131
94,93 0,200 0,006 0,128 0,194
96,17 0,267 0,028 0,172 0,239
96,74 0,333 0,052 0,215 0,282
97,07 0,400 0,071 0,262 0,329
97,68 0,467 0,123 0,277 0,344
97,93 0,533 0,150 0,316 C0,383>
99,10 0,600 0,326 0,207 / 0,274
99,30 0,667 0,363 0,237 0,304
100,73 0,733 0,643 0,024 0,090
103,29 0,800 0,950 0,216 f/ 0,150
103,60 0,867 0,964 0,164 0,097
103,83 0,933 0,972 0,106 / 0,039
105,20 1,000 0,995 0,062 0,005
Distância máxima
4. A maior diferença absoluta foi igual a 0,383; logo, d = 0,383.
5. Pela Tabela 7, para n = 15 e a = 0,05, obtemos a distância máxima
admissível, d: = 0,338. Como d > d:, o teste rejeita H0, concluindo
que não há aderência dos dados à distribuição normal com [x = 100
e a = 2. Observe o gráfico das duas distribuições acumuladas na Fi­
gura 10.3.
— F 00
— soo
93 94 95 96 97 98 99 100101102103104 105106
Diâmetro (mm)
Figura 10.3 Distribuições acumuladas F(x) e S(x) para o Exemplo 10.2.

TESTES NÃO PARAMÉTRICOS 2 8 1
Exemplo 10.3 A metodologia usada para calcular os índices de confiabilidade
de um sistema de transmissão de energia elétrica exige que os tempos para a
falha dos componentes sigam distribuições exponenciais. Observações anterio­
res indicaram a validade de tal suposição, mas um engenheiro decidiu verificar
se o tempo para a falha (em horas) de um componente, especialmente crítico,
pode ser admitido com distribuição exponencial de média de 500 horas. Para
testar essa hipótese, utilizando nível de significância de 1%, coletou-se uma
amostra de 20 observações do tempo de falha desse componente:
7,55 25,20 41,00 133,59 146,77 157,55 158,07 206,08 385,09 426,89
555,86 639,43 816,11 847,57 924,63 945,66 968,66 1.130,391.143,931.365,69
As hipóteses são:
H0: a amostra provém de uma população que segue uma distribuição
exponencial com média 500;
Hi'. a amostra não provém de uma população que segue uma distribui­
ção exponencial com média 500.
A distribuição acumulada da amostra, S(x), é construída da mesma forma
que no exemplo anterior. Já para os valores teóricos da distribuição exponencial
de média 500, lembramos que o parâmetro X de uma distribuição exponencial é
o inverso de sua média (ver Expressão 6.17, Capítulo 6). Assim, pela hipótese
nula:
X = —L _ = J _ = 0,002
£(X) 500
Logo, os valores teóricos associados a xt (í = 1, 2, .., n) são obtidos por
(ver Expressão 6.14, Capítulo 6):
F(x.) = P{X < x l) = l - e >Jf‘ = 1 - e~0,002Xi
Os resultados dessa expressão e os demais cálculos para o teste são apre­
sentados a seguir:

2 8 2 ESTATÍSTICA
s w F(xt) |F(*£) -S C ^JI |F(xf) -S (*f)|
0 0
7,55 0,05 0,015 0,015 0,035
25,20 0,10 0,049 0,001 0,051
41,00 0,15 0,079 0,021 0,071
133,59 0,20 0,234 0,084 0,034
146,77 0,25 0,254 0,054 0,004
157,55 0,30 0,270 0,020 0,030
158,07 0,35 0,271 0,029 0,079
206,08 0,40 0,338 0,012 0,062
385,09 0,45 0,537 0,137 0,087
426,89 0,50 0,574 0,124 0,074
555,86 0,55 0,671 0,171 0,121
639,43 0,60 0,722 0J72 0,122
816,11 0,65 0,805 CO,205) 0,155
847,57 0,70 0,816 f 0,166 0,116
924,63 0,75 0,843 / 0,143 0,093
945,66 0,80 0,849 / 0,099 0,049
968,66 0,85 0,856 / 0,056 0,006
1.130,39 0,90 0,896 0,046 0,004
1.143,93 0,95 0,899 0,001 0,051
1.365,69 1,00 0,935 / 0,015 0,065
Distância máxima
A maior diferença absoluta foi igual a d = 0,205. Procurando na Tabela 7,
para n = 20 e a = 0,01, obtemos uma distância máxima admissível, d,- = 0,352.
Como d < dC) o teste aceita H0 ao nível de significância de 1%, indicando ade­
rência dos dados à distribuição exponencial de média 500. Observe o gráfico
das duas distribuições acumuladas na Figura 10.4.
1,00
-4
0,90
CS
0,80 *
I *
p
0,70
B >
3 0,60 • .. wf.
p Dp= '-'j
0,50
.2
‘y
c 0,40
«OV
0,30
cr
0,20
íi-
0,10
0,00
ot o
■
F(x13) >U]2)
/
/ p
/
/
✓
f r
Vt
— FCx)
L.
S(x)
200 400 600 800 1.000 1.200 1.400
Tempo para a falha (horas)
Figura 10.4 Distribuições acumuladas F(x) e S(x) para o Exemplo 10.3.

TESTES NÃO PARAMÉTRICOS 2 8 3
O teste de Kolmogorov-Smirnov pode ser aplicado para avaliar a aderência
a qualquer distribuição, desde que seus parâmetros sejam especificados.
10.1.3 Teste de Lilliefors
O teste de Lilliefors é usado para verificar a aderência dos dados a uma
distribuição normal qualquer, isto é, sem a especificação de seus parâmetros. É
bastante parecido com o teste de aderência de Kolmogorov-Smirnov, pois tam­
bém avaliamos as distribuições acumuladas S(x) e F(x); obtemos a distância
máxima D entre elas; e a comparamos com um valor tabelado, em função do ní­
vel de significância e do tamanho da amostra. As diferenças residem na forma
de obtenção de F(x) (pois a média e o desvio padrão são calculados com base
na amostra) e na tabela utilizada para a decisão do teste (ver lado direito da
Tabela 7, no apêndice).
Exemplo 10.4 No Exemplo 10.2, não houve aderência dos dados à distribui­
ção normal com média 100 e desvio padrão 2. Mas a montadora quer saber se é
possível considerar que os diâmetros dos eixos distribuem-se segundo uma dis­
tribuição normal (qualquer), ao nível de significância de 5%.
As hipóteses são:
H0: a amostra provém de uma população que segue uma distribuição
normal;
Hi’. a amostra não provém de uma população que segue uma distribui­
ção normal.
Calculando a média e o desvio padrão da amostra, que servirão como esti­
mativas dos parâmetros da distribuição normal, na população:
Para cada valor jc* (i = 1, 2, n), calculamos o correspondente escore zb
usando x e s n o lugar de n e a, respectivamente. Por exemplo, para X\ = 93,45,
temos:

2 8 4 ESTATÍSTICA
E os resultados para o cálculo da estatística do teste:
Xi S(xJ F(xJ | F(xJ - S(Xi l) | |F(xJ -S (x J \
0 0
93,45 0,067 -1,47 0,071 0,071 0,004
94,46 0,133 - 1,20 0,115 0,049 0,018
94,93 0,200 - 1,07 0,142 0,009 0,058
96,17 0,267 -0,74 0,230 0,030 0,036
96,74 0,333 - 0,58 0,280 0,013 0,053
97,07 0,400 -0,49 0,311 0,023 0,089
97,68 0,467 -0,33 0,371 0,029 0,096
97,93 0,533 -0,26 0,397 0,070 0,136
99,10 0,600 0,05 0,522 0,012 0,078
99,30 0,667 0,11 0,543 0,057 0,124
100,73 0,733 0,50 0,690 0J023 0,043
103,29 0,800 1,19 0,882 /P , 149) 0,082
103,60 0,867 1,27 0,898 / 0,098 0,031
103,83 0,933 1,33 0,909 / 0,042 0,025
105,20 1,000 1,70 0,956 / 0,022 0,044
Distância máxima
A estatística do teste para esta amostra é d = 0,149. No lado direito da Tabe­
la 7, para a = 0,05 e n = 15 obtemos a distância máxima admissível dc = 0,220.
Como d < dc, o teste aceita H0 ao nível de significância de 5%, concluindo que
há aderência dos dados a uma distribuição normal, embora com parâmetros di­
ferentes dos especificados pela montadora no Exemplo 10.2. Veja o gráfico das
duas distribuições, exposto na Figura 10.5.
1,00
0,90
CO 0,80
TJ
3 0,70
£
a 0,60
CO
0,50
.2
‘D
e
0,40
<o
zr
0,30
o
i-
Ph
0,20
0,10
0,00 — SOO
93 94 95 96 97 98 99 100 101102103104 105106
Diâmetro (mm)
Figura 10.5 Distribuições acumuladas F(x) e S(x) para o Exemplo 10.4.

TESTES NÃO PARAMÉTRICOS 2 8 5
A Figura 10.5 mostra grande proximidade entre as curvas das distribuições
SM e F(x), razão pela qual o teste de Lilliefors aceitou a hipótese de aderência
à distribuição normal.
Rotineiramente, quando estamos estudando uma variável quantitativa, o
teste de Lilliefors é utilizado para avaliar se é possível aplicar um teste paramé­
trico que supõe distribuição normal. Quando não há aderência, pode ser neces­
sário usar uma técnica não paramétrica alternativa, sendo que algumas delas
serão discutidas nas próximas seções.
EXERCÍCIOS
1. Uma empresa possui três laboratórios de pesquisa (A, B, C), cujos computa­
dores estão conectados a um servidor, para onde enviam pacotes de dados
para serem analisados em um programa estatístico (disponível apenas no
servidor). Os usuários do laboratório A pediram prioridade ao gerente de
rede, pois costumam enviar mais pacotes ao servidor. O gerente observou
500 pacotes de dados enviados e classificou-os de acordo com a origem,
conforme a tabela a seguir:
Laboratório A B C Total
Número de pacotes 165 179 156 500
Os dados constituem evidência suficiente para corroborar o pedido do
laboratório A? Utilize nível de significância de 1%.
2. Quatro fábricas de um mesmo grupo produzem peças automotivas. Histori­
camente, cerca de 20% do total de peças defeituosas vêm da fábrica 1, 30%
da fábrica 2, 25% da fábrica 3 e 25% da fábrica 4. Os engenheiros do setor
da qualidade estão suspeitando que essas proporções não são mais válidas,
e observaram o número de peças defeituosas no último lote de produção.
Os dados são apresentados a seguir:
Fábrica 1 2 3 4 Total
Número de peças 120 200 175 134 629
Utilizando nível de significância de 5%, a suspeita dos engenheiros do
setor da qualidade tem fundamento?
3. Você e seu sócio têm um provedor de acesso à Internet. Para auxiliar na
configuração dos equipamentos, o conhecimento do comportamento dos

2 8 6 ESTATÍSTICA
tempos de acesso de seus clientes é importante. Mas vocês têm divergência
a esse respeito: você crê que o tempo de acesso segue uma distribuição nor­
mal com média de 16 minutos e desvio padrão de 4 minutos, enquanto seu
sócio suspeita que o tempo de acesso segue uma distribuição exponencial,
com média de 16 minutos. Para dirimir a dúvida, vocês coletaram uma
amostra de tempos de acesso (em minutos):
6 10 1 11 1 6 27 9 17 1 18 10 5 35 17 41 2 20 16 5
Utilizando nível de significância de 5%, qual de vocês dois está certo
quanto à distribuição dos tempos de acesso?
4. No controle estatístico de processos, uma suposição crucial para a utiliza­
ção de gráficos de controle de média de Shewhart é de que a distribuição
das médias possa ser considerada normal. Um engenheiro quer saber se é
possível aplicar gráficos de controle de médias a um processo produtivo.
Para tanto, quer avaliar a aderência das médias de 25 amostras à distribui­
ção normal. Os valores estão expressos a seguir:
0,19 0,57 0,66 1,41 0,28 0,05 0,63 0,75 0,85 0,99
1,68 3,01 0,31 5,48 0,66 0,76 5,94 0,85 0,03 9,49
2,18 1,23 4,89 0,71 3,52
Com base nos dados apresentados, e supondo nível de significância de
1%, é possível usar gráficos de controle de média de Shewhart para moni­
torar o processo?
5. A empresa “Faça Certo S.A.” produz peças automotivas da melhor qualida­
de, e uma delas tem aspecto crítico na característica dimensão, a qual pre­
cisa seguir uma distribuição normal (aspecto mais importante), com média
de 15 mm e desvio padrão de 0,4 mm. Após receber muitas reclamações, o
departamento de vendas cobrou do departamento de produção um teste
desta suposição. Uma amostra de 40 peças foi aleatoriamente coletada e
suas dimensões críticas medidas, resultando:
11,37 11,38 11,51 11,57 11,58 11,58 11,58 11,65 11,72 11,75
11,78 11,78 11,83 11,90 11,90 11,92 11,93 11,93 11,97 12,00
12,01 12,06 12,06 12,06 12,07 12,09 12,11 12,11 12,14 12,19
12,20 12,21 12,23 12,23 12,25 12,46 12,48 12,52 12,65 12,81
a) A dimensão crítica segue uma distribuição normal com média de 15
mm e desvio padrão de 4 mm? Use a = 0,05.
b) A dimensão crítica segue uma distribuição normal? Use a = 0,05.

TESTES NÃO PARAMÉTRICOS 2 8 7
10.2 ANALISE DE ASSOCIAÇAO
Dizemos que existe associação entre duas variáveis qualitativas quando as
probabilidades de eventos de uma delas são alteradas conforme a categoria da
outra. Por exemplo, a probabilidade de passar na disciplina de Estatística deve
ser maior se você dedicar mais tempo à disciplina. Então, a dedicação (alta ou
baixa) e aprovação (sim ou não) têm associação. O chamado teste qui-quadrado
de independência serve para avaliar a signifícância de uma associação. O mesmo
procedimento que discutiremos para verificar uma possível associação entre
duas variáveis qualitativas também pode ser usado para verificar se diferentes
populações apresentam as mesmas proporções com respeito a uma variável
qualitativa. Nessa situação, o teste é chamado de teste qui-quadrado de homoge­
neidade, mas em termos matemáticos, o teste de homogeneidade é igual ao tes­
te de independência e, por isso, não faremos distinção entre esses dois testes.
10.2.1 Tabelas de contingência
Antes de estudarmos o teste propriamente dito, precisamos conhecer as ta­
belas de contingência, que são a forma usual de apresentar uma distribuição de
frequências conjunta de duas variáveis qualitativas.
Exemplo 10.5 Determinado posto de qualidade de um laticínio retira uma
amostra dos pesos dos litros de leite produzidos em um dia, classificando-os de
acordo com seu tipo (B, C, UHT), e condições de peso (dentro ou fora das especi­
ficações). A Tabela 10.2 mostra a distribuição de frequências conjunta de 6.850
unidades de leite, disposta numa tabela de contingência.
Tabela 10.2 Distribuição de frequências conjunta do tipo de leite e condição do
peso.3
Tipo do leite
Condição
Total
do peso
B C UHT
Dentro das especificações 500 4.500 1.500 6.500
Fora das especificações 30 270 50 350
Total 530 4.770 1.550 6.850
3 Dados extraídos da dissertação de mestrado de Luciana S. C. V. da Silva (Programa de
Pós-Graduação em Engenharia de Produção/UFSC, 2001).

2 8 8 ESTATÍSTICA
Podemos calcular percentuais para cada célula da tabela, seja em relação
ao total das linhas (condições de peso) ou total das colunas (tipo de leite), o
que possibilita uma avaliação da qualidade dos processos. Calculando percen­
tuais em relação aos totais das colunas, obtemos:
Tipo do leite
Condição
Total
do peso
B C UHT
Dentro das especificações 94,34% 94,34% 96,77% 94,89%
Fora das especificações 5,66% 5,66% 3,23% 5,11%
Total 100% 100% 100% 100%
Não obstante as diferentes quantidades produzidas, os tipos de leite têm
proporções semelhantes para produtos dentro das especificações de peso, com
exceção do tipo UHT, que parece estar mais de acordo com as especificações. A
seção seguinte mostra como podemos testar estatisticamente essa possível asso­
ciação entre o tipo de leite e a condição de peso.
10.2.2 Teste qui-quadrado de independência
Usado para verificar se existe associação entre duas variáveis qualitativas
(categóricas), X e 7, com base em uma amostra de observações disposta numa
tabela de contingência com L linhas e C colunas (L, C > 2), correspondentes às
categorias de X e 7, respectivamente. A hipótese nula afirma independência en­
tre X e 7, enquanto a hipótese alternativa aponta para associação entre X e 7.
Vimos, no Capítulo 4, que dois eventos são independentes se e somente se a
probabilidade conjunta (da interseção) for igual ao produto das probabilidades
de cada evento. Denominam-se:
Pij a probabilidade de ocorrência da linha i e coluna; (i = 1, 2, ..., L;j =
= 1, 2, ...C);
Pi a probabilidade de ocorrência da linha i; e
Pj a probabilidade de ocorrência da coluna j.
Podemos escrever as hipóteses de independência e associação por (ver se­
ção 4.3.2):
H0: Pij = Pi pj para todo i = 1, 2, ..., L e j = 1, 2, ..., C;
Hi’. p^ * Pi pj para algum i = 1, 2, ..., L e j = 1, 2, ..., C.

TESTES NÃO PARAMÉTRICOS 2 8 9
Sejam:
0.; a frequência observada na célula (i, j ) da tabela de contingências; e
Etj a frequência esperada na célula (i, ;), supondo H0 verdadeira.
Sob H0, as frequências esperadas podem ser calculadas por:
( total da linha i) x (total da coluna ;)
E» = (10.4)
tota/ gera/
(i = 1, 2 ..., L ;j = 1, 2, ...CV
A estatística do teste é um tipo de distância entre as frequências observa­
das e as frequências esperadas por H0. Ela é dada por:
L C
(10.5)
i= 1 ;=1 E,
Sob H0, a estatística Q2 segue uma distribuição qui-quadrado com graus de
liberdade igual a:
gl = (L - 1) (C - 1) (10.6)
Adotando nível de significância a, podemos obterx,2 na Tabela 5 do apên­
dice e construir a regra de decisão para o valor calculado q2, como segue:
q2 < ^ 2 => aceita H0 (as duas variáveis são independentes);
q2 >% 2c => rejeita H0 (há associação entre as duas variáveis).
Exemplo 10.5 (continuação) Com os dados do laticínio, vamos testar se há
associação entre o tipo do leite (B, C, UHT) e condições de peso (dentro ou fora
das especificações). Temos as hipóteses:
H0: as condições de peso independem do tipo do leite;
Hy. há associação entre condições de peso e tipos de leite.
Os dados amostrais estão na Tabela 10.2, onde observamos que há
94,89% de produtos dentro das especificações e 5,11% fora. Se as condições de
peso forem independentes dos tipos de leite (B, C, UHT), devemos esperar que
4 Representando por n o total geral, observe que E0 = np. p:, onde p, é a proporção ob­
servada na linha i (i = 1, 2,..., L) e p, é a proporção observada na coluna j (j = 1, 2,..., C). Sob
H0, esta quantidade é uma estimativa de nplf.

2 9 0 ESTATÍSTICA
as porcentagens se mantenham para todos os tipos de leite. Assim, como foram
observados 530 produtos leite tipo B, devemos esperar uma frequência em tor­
no de 502,917 (94,89% de 530) dentro das especificações. Note que chegare­
mos ao mesmo resultado se aplicarmos (10.4):
(total da linha 1) x (total da coluna 1) (6500)(530)
E11 — ■ ■ — — 502,917
total geral 6850
Aplicando (10.4) para todos (i,;) da tabela (i = 1, 2;j = 1, 2, 3), temos:
II M j = 2 j = 3 Total
i = 1 (6500)(530) (6500X4770) _ (6500)(1550) 6.500
6850 6850 6850
= 502,917 = 4526,253 1470,795
i = 2 (350)(530) (350)(4770) _ (350)(1550) 350
6850 6850 6850
= 27,083 = 243,747 = 79,205
Total 530 4.770 1.550 6.850
Para aplicar (10.5), podemos calcular a contribuição de cada célula (£, j) :
j = 1 II ot j = 3 Total
i = 1 (500-502,917)' (4500-4526,253)2 (1500-1470,795)2 6.500
502,917 4526,253 1470,795
= 0,017 = 0,152 = 0,580
i = 2 (30 - 27,083)2 (270 - 243,747)2 _ (50-79,205)2 _ 350
27,083 243,747 79,205
= 0,314 = 2,828 = 10,69
Total 530 4.770 1.550 6.850
Donde, para a presente amostra, temos o seguinte valor para a estatísti­
ca Q2:
q2 = 0,017 + 0,152 + 0,58 + 0,314 + 2,828 + 10,769 = 14,66
com
gl = ( L - 1 ) ( C - 1 ) = ( 2 - 1 X 3 - 1 ) = 2

TESTES NÃO PARAMÉTRICOS 2 9 1
Adotando nível de significância de 5%, obtemos, na Tabela 5 do apêndice,
X t = 5,99 (ver Figura 10.6). Como q2 > % 2ci o teste rejeita a hipótese nula, evi­
denciando associação entre a condição de peso e o tipo de leite. Tal resultado de-
ve-se, provavelmente, ao leite tipo UHT, para o qual foram observadas as maio­
res diferenças e, portanto, as maiores contribuições no cálculo da estatística Q2.5
aceita H° rejeita H0
Figura 10.6 Regra de decisão de um teste de independência usando o modelo qui-
quadrado com dois graus de liberdade.
O teste qui-quadrado de independência pode ser usado para o estudo de
associação entre duas variáveis qualitativas nominais, mas também é possível
usá-lo com variáveis ordinais ou quantitativas (discretas ou contínuas), desde
que seus resultados sejam classificados em categorias. Contudo, tal como no tes­
te qui-quadrado de aderência, há uma restrição importante: todos os totais da
tabela de contingência devem ser razoavelmente grandes, de tal forma a garan­
tir Eÿ > 5, para todo i = 1, 2, ..., L e j = 1, 2, ... C.
Para tabelas 2 x 2 , isto é, quando as duas variáveis têm apenas 2 catego­
rias (L = 2 e C = 2), é recomendável fazer uma pequena alteração na Expres­
são (10.5), para que a distribuição da estatística Q2 fique mais próxima do mo­
delo teórico (distribuição qui-quadrado com gl = 1). A alteração consiste em
subtrair 0,5 unidade da diferença absoluta entre cada par O0 e Eij} ou seja:
- É É (10.7)
t=l j=l
A alteração proposta em (10.7) corresponde à correção de continuidade
discutida na seção 6.3, pois a distribuição qui-quadrado com gl = 1 vem de
uma variável aleatória com distribuição normal padrão ao quadrado.
5 Como o tamanho da amostra deste exemplo é bastante grande, é natural o teste rejei­
tar H0, porque as diferenças, mesmo que pequenas, têm pouca chance de ser explicadas pelo acaso.

2 9 2 ESTATÍSTICA
EXERCÍCIOS
.
6 Há dúvidas sobre os desempenhos dos alunos, na disciplina de Estatística,
de alguns cursos de Engenharia. Alguns argumentam que, dependendo do
curso, o percentual de aprovação pode ser diferente, mesmo que a discipli­
na tenha o mesmo programa. Um estudo foi realizado, selecionando alea­
toriamente alunos de três cursos, registrando os aprovados e reprovados na
disciplina. Os resultados estão na tabela a seguir:
Curso
Situação
Eng. Civil Eng. Química Eng. Mecânica Total
Aprovados 44 26 35 105
Reprovados 11 26 15 52
Total 55 52 50 157
Considerando nível de significância de 5%, os percentuais de aprova­
ção podem ser considerados iguais?
7. Uma metalúrgica produz grandes quantidades de parafusos, trabalhando
em três turnos. O setor da qualidade deseja verificar se o desempenho dos
turnos é semelhante, o que poderia ser avaliado através das proporções de
peças aprovadas, direcionadas a retrabalho ou rejeitadas. Como parte do
Controle Estatístico de Processos, amostras aleatórias de parafusos são co­
letadas de cada turno. Uma dessas amostras, com a classificação das peças,
está mostrada na tabela a seguir:
Turno
Situação
Total
das peças
Matutino Vespertino Noturno
Aprovadas 432 456 424 1.312
Retrabalho 185 190 180 555
Rejeitadas 45 48 39 132
Total 662 694 643 1.999
É possível considerar semelhante o desempenho dos turnos? Use nível
de significância de 1%.
.
8 Uma rede local de computadores tem cinco clientes que enviam pacotes de
dados (gerados por um aplicativo) ao servidor. Os pacotes podem ser con-

TESTES NÃO PARAMÉTRICOS 2 9 3
siderados completos, incompletos mas aproveitáveis e inaproveitáveis, de­
pendendo de como são recebidos pelo servidor. Suspeita-se que pode haver
problemas em um ou mais dos clientes, o que poderia ser evidenciado por
diferentes percentuais de pacotes completos, aproveitáveis e inaproveitáveis.
Um estudo foi realizado, fazendo com que cada cliente enviasse certo nú­
mero de pacotes ao servidor, donde os pacotes foram observados. Os resul­
tados foram:
Situação dos pacotes
Cliente Total
Completos Aproveitáveis Inaproveitáveis
1 485 10 5 500
2 768 24 8 800
3 624 20 6 650
4 522 40 18 580
5 650 3 17 670
Total 3.049 97 54 3.200
A suspeita tem fundamento? Use nível de significância de 2,5%.
10.3 TESTES PARA DUAS POPULAÇÕES
Muitas vezes, não é possível aplicar os testes paramétricos para comparar
diferentes tratamentos ou populações (Capítulo 9), porque alguma das suposi­
ções não é satisfeita. Um caso típico ocorre nas situações em que os dados não
podem ser considerados provenientes de uma população com distribuição nor­
mal.6 Já vimos na seção anterior o teste qui-quadrado de independência (ou de
homogeneidade), que permite comparar duas ou mais populações quando a
resposta é proveniente de uma variável nominal. Nesta seção, discutiremos tes­
tes para comparar duas populações com dados ordinais. Na prática, podemos
aplicá-los em dados provenientes de variável quantitativa, usando apenas a or­
denação dos valores.
10.3.1 Teste dos sinais
Trata-se de um teste para casos em que a variável observada tem nível de
mensuração pelo menos ordinal. O teste dos sinais é utilizado para comparar a
6 Podemos aplicar o teste de Lilliefors para verificar essa suposição.

2 9 4 ESTATÍSTICA
posição central ou locação de duas distribuições populacionais, com base em
amostras pareadas. Exemplos:
• comparar as notas de alunos de Engenharia em uma prova padrão de
Estatística, antes e após a realização de um curso de reforço. Observe
que são os mesmos alunos, avaliados em momentos diferentes, que
provocam dados pareados; e o interesse é avaliar se há diferença sig­
nificativa entre o desempenho mediano dos dois grupos;
• verificar se há diferença no tempo gasto por computadores para exe­
cutar uma mesma tarefa, antes e após a atualização de seus sistemas
operacionais (supondo computadores com configurações idênticas).
Novamente, são os mesmos elementos, avaliados em momentos dife­
rentes, gerando dados pareados; e o teste possibilitará verificar se há
diferença significativa entre as posições centrais das distribuições dos
tempos de resposta das duas situações;
• um grupo de consumidores de determinado software recebe uma nova
versão desse produto, e deve opinar se considera o desempenho da
nova versão melhor ou pior que a antiga. Há interesse em verificar se
a nova versão atendeu às expectativas dos clientes, ou seja, se em ge­
ral (ou na mediana) os consumidores consideram o desempenho da
nova versão melhor do que o desempenho da antiga.
Nos dois primeiros exemplos, supondo que a variável resposta siga aproxi­
madamente um modelo normal, pode ser aplicado o teste t para dados pareados
(seção 9.2). Já no último exemplo, o teste t não pode ser usado, porque não são
observadas medidas quantitativas da variável resposta (desempenho do softwa­
re). Este é um caso típico de aplicação do teste dos sinais.
Sejam Xl e X2 as variáveis aleatórias que indicam as duas condições de
medida da variável resposta, no experimento pareado. Em termos de nossos
exemplos, Xj é a medida antes e X2 é a medida depois. Essas variáveis não
precisam ser observadas diretamente, mas supõe-se que sejam contínuas.
Seja D = X2 - X : a diferença num par de medidas e rjD a mediana de D. As hipó­
teses do teste dos sinais podem ser escritas como:7
Ho'- r\D = 0 e Hi: r\D* 0
Na abordagem unilateral, a hipótese alternativa é Hi9: % > 0 ou H ”: r|D < 0.
Pela definição de mediana, temos P(D > r|D) = P(D < r|D) = 0,5. Então, se
H0 for verdadeira,
7 Se for suposto D = X2 - X} com distribuição simétrica, então a mediana é igual à mé­
dia, e as hipóteses tomam-se as mesmas do teste t pareado.

TESTES NÃO PARAMÉTRICOS 29 5
P(D > 0) = 0,5 <=> P(X2 - Xl > 0) = 0,5 <=> P(X2 > X J = 0,5
Assim, definindo p = P(X2 > X J, que, em termos de nossos exemplos, re­
presenta a probabilidade de a avaliação depois ser maior do que a avaliação an­
tes, a hipótese nula pode ser escrita como:
H0: p = 0,5
caracterizando o teste dos sinais como um caso particular do teste de uma pro­
porção (seção 8.7).
Seja n+ o número de pares em que X2 > X: (pares com sinal positivo). Se H0
for verdadeira, por (5.14) temos que o valor esperado de n . é Assim, se for
observado n+ longe de ^ , há indícios para rejeitar H0 (considerando a hipótese
alternativa e o nível de significância do teste).
Amostra pequena
Quando o número n de pares avaliados (tamanho da amostra) for peque­
no, usamos a distribuição binomial (Tabela 1) para obter o valor p e realizar o
teste. A Tabela 1 contempla valores de n não superiores a 15.
Exemplo 10.6 Um sistema de alarme possui um grande número de compo­
nentes. Há interesse em saber se houve ou não aumento no tempo de falha dos
componentes após implementação de um programa de manutenção. Usualmen­
te, o tempo de falha segue aproximadamente uma distribuição exponencial. Foi
observada uma amostra de dez componentes, antes e depois do programa de
manutenção, e os resultados (em horas) estão na tabela a seguir:
Componente Antes Depois Sinal1
1 400 395 _
2 360 350
—
3 450 556 +
4 390 480 +
5 430 405
—
6 386 500 +
7 452 547 +
8 470 462
—
9 400 500 +
10 340 480 +
1 Foi usado sinal positivo quando a medida depois foi maior do que a medida antes (compatível
com a hipótese em estudo).

2 9 6 ESTATÍSTICA
Observe que se trata de uma amostra pareada e pequena (n = 10). Embo­
ra a variável resposta seja contínua e seja observada nas duas condições, as po­
pulações não seguem distribuições normais; assim, não é recomendável utilizar
o teste t para dados pareados. Aplicaremos o teste dos sinais. As hipóteses são:
H0: a mediana do tempo de falha depois é igual à mediana do tempo de
falha antes;
Hi’. a mediana do tempo de falha depois é maior do que a mediana do
tempo de falha antes.
Da amostra de n = 10 casos eram esperados (sob H0) 5 sinais positivos,
mas observamos n+ = 6. O valor de n+ aponta na direção de Hu mas vamos ob­
ter, na Tabela 1 do apêndice, o valor p para verificar se a diferença em relação
ao valor esperado não pode ser explicada pelo acaso. Como o teste é unilateral
à direita, temos:
p = p( 6) + p(7) + p( 8) + p(9) + p(10) =
= 0,2051 + 0,1172 + 0,0439 + 0,0098 + 0,0010 =
= 0,3770
Adotando nível de signifícância a = 0,05, temos p > a, levando à aceita­
ção de H0 (ver Capítulo 8). Concluímos, então, que o teste dos sinais não en­
controu evidências estatísticas de que o plano de manutenção programada te­
nha aumentado o tempo mediano de falhas dos componentes do sistema.
Amostra grande
Para valores de n superiores aos apresentados na Tabela 1, é possível usar
a aproximação da normal à binomial, calculando:8
(10.8)
onde n[ = n 4 -0 ,5 se n. > — (teste bilateral ou unilateral à direita);
2
n[ = n, + 0,5 se n. < — (teste bilateral ou unilateral à esquerda).9
2
8 Observe que (10.8) corresponde à Expressão 8.7, com p0 = 0,5.
9 Note que, se o teste for unilateral e a relação entre n+ e y2 for diferente da apresenta­
da, não podemos rejeitar H0 em favor de Hx.

TESTES NÃO PARAMÉTRICOS 2 9 7
Exemplo 10.7 Uma empresa quer observar a viabilidade de utilizar um novo
tipo de calibrador, eletrônico, ao invés do modelo empregado atualmente, me­
cânico, para medir dimensões de peças automotivas. Após treinamento apropria­
do, 26 operários foram sorteados para realizar as medições das mesmas peças,
com o calibrador eletrônico e o mecânico: os tempos gastos (em segundos) fo­
ram registrados. Somente será viável a introdução dos novos calibradores se o
tempo mediano de medição for menor do que o obtido com os calibradores me­
cânicos ora em uso. Sabe-se que os tempos de medição desses calibradores não
costumam seguir distribuições normais, donde se optou por evitar o tradicional
teste t de médias. Os tempos de medição e os sinais (positivos quando a medi­
ção no calibrador eletrônico foi maior) estão na tabela a seguir:
Operário Eletr. Mec. Sinal Operário Eletr. Mec. Sinal
1 27,0 27,0 0 14 22,0 29,0
—
2 25,0 30,1 15 16,0 16,0 0
—
3 22,0 28,0 16 22,0 20,6 +
—
4 34,0 34,0 0 17 29,5 25,0 +
5 23,0 24,5 18 36,0 33,0 +
—
6 22,0 28,0 19 35,0 41,0
— —
7 25,0 28,0 20 35,0 35,0 0
—
8 32,3 30,0 + 21 27,5 28,0
—
9 34,0 36,0 22 29,0 31,8
— —
10 23,5 29,0 23 27,0 28,0
— —
11 34,2 39,0 24 24,3 29,3
— —
12 31,8 30,0 + 25 30,1 30,8
—
13 28,4 20,0 + 26 29,3 35,6 —
As hipóteses são:
H0: os tempos medianos de medição com o calibrador eletrônico e com
o calibrador mecânico são iguais;
Hi'. o tempo mediano de medição com calibrador eletrônico é menor que
o tempo mediano de medição com calibrador mecânico.
Faremos esse teste, unilateral à esquerda, com nível de significânda a = 0,05.
Embora tenham sido realizadas 26 observações pareadas, vamos excluir as qua­
tro observações em que o nível de precisão das medidas não detectou diferença
entre os dois calibradores. Assim, temos n = 22.
Pela abordagem clássica, é preciso encontrar o valor zc na distribuição nor­
mal padrão (Tabela 3 do Apêndice), que delimita área de a = 0,05 na cauda
direita da distribuição. Como o teste é unilateral à esquerda, o teste rejeita H0
se e somente se o valor calculado z (Expressão 10.8) for menor ou igual a - zc
(Figura 10.7).

2 9 8 ESTATÍSTICA
Figura 10.7 Regra de decisão para um teste unilateral à esquerda, utilizando a
distribuição normal padrão.
Pela tabela da distribuição normal padrão, obtemos zc = 1,645, levando à
regra de decisão:
se z < - 1,645, então rejeita H0 em favor de Hi,
se z > - 1,645, então aceita H0.
As n = 22 observações pareadas válidas acusaram n+ = 6. Aplicando
(10.8), encontramos:
( ,
2 65)-22
* V22
levando à rejeição de H0 em favor de Hi.
O teste dos sinais encontrou evidências estatísticas de que o tempo médio
de medição efetuada pelo calibrador eletrônico foi menor do que pelo calibra­
dor mecânico. Assim, os calibradores eletrônicos podem ser introduzidos na or­
ganização.
10.3.2 Teste dos sinais por postos
Em cada par de observações, o teste dos sinais, discutido na seção 10.3.1,
avalia apenas qual tratamento foi melhor, desconsiderando a magnitude da di­
ferença. Em consequência, o teste dos sinais não costuma detectar diferença en­
tre os dois tratamentos se as amostras não forem grandes, a menos que a dife­
rença real entre os tratamentos seja muito grande.
O teste dos sinais por postos, também chamado de teste de Wilcoxon, é uma
boa alternativa para os casos em que é possível avaliar a magnitude das diferen­
ças (pelo menos a nível ordinal), mas não é possível garantir as suposições para
a aplicação do teste t pareado. A ordenação da magnitude das diferenças pode

TESTES NÃO PARAMÉTRICOS 2 9 9
ser feita por especialistas ou, quando a variável observada for quantitativa,
pode ser feita objetivamente, conforme descreveremos.
Atribuímos postos às diferenças de cada par, independentemente do sinal,
alocando o posto 1 à menor diferença em módulo; o posto 2 à segunda menor
diferença em módulo; ...; o posto n à maior diferença em módulo. Às observa­
ções empatadas atribuímos a média dos postos correspondentes (por exemplo,
considere três diferenças iguais, que, se distintas, corresponderiam aos postos 4,
5 e 6; atribuímos a cada uma delas a média desses postos, ou seja, o posto 5).
É suposto que a variável resposta seja contínua. Embora ela possa não ser
observável diretamente, supõe-se que seja possível atribuir postos às diferenças
de cada par. Adota-se a mesma formulação das hipóteses (H0 e ) do teste dos
sinais (em termos da mediana das diferenças da variável resposta), mas o teste
dos sinais por postos é desenvolvido através da ordenação das diferenças. Sob a
hipótese nula, a soma dos postos das diferenças positivas deve ser aproximada­
mente igual à soma dos postos das diferenças negativas.
Seja a variável aleatória S+ definida como a soma dos postos das diferenças
positivas de uma amostra de n pares a ser observada. Sob H0, é possível mostrar
que seu valor esperado e sua variância são dados, respectivamente, por:
, x n (n + l)
E (S +)= v } (10.9)
, v n (n + l)(2 n + l)
V ( S ) = -±------ A --------------------------------------------- L (10.10)
v +/ 24
Observada uma amostra pareada de n observações (já descontando algum
caso em que a diferença foi nula), definimos s+ como a soma dos postos das dife­
renças positivas da amostra observada. Se s+ estiver longe do valor esperado por
H0 (Expressão 10.9), há indícios para rejeitar H0 (considerando a hipótese alter­
nativa e o nível de significância do teste).
Amostra pequena
Para n <20 (descontando algum caso em que a diferença no par foi nula),
a Tabela 8 fornece o valor crítico sc para s+, permitindo construir a regra de de­
cisão, em função da hipótese alternativa e do nível de significância do teste.
Veja Quadro 10.1.

3 0 0 ESTATÍSTICA
Quadro 10.1 Regra de decisão do teste dos sinais por postos para amostras pe­
quenas, usando a Tabela 8 do Apêndice.
Hipótese H 1 Regra de decisão
Unilateral à direita - Encontrar sc tal que P(S+ < sc) * 1 - a
- Se s+ > sc, então rejeita H0
Unilateral à esquerda - Encontrar sc tal que P(S+ < sc) « a
- Se s+ < sc, então rejeita H0
Bilateral - Encontrar scl tal que P(Sf < scl) a %
- Encontrar sc2 tal que P(Sf < sc2) « l - y 2
- Se s+ < scl ou s+ > sc2, então rejeita H0
N ota. As probabilidades não são exatas, porque S+ é uma variável alea­
tória discreta, mas os valores críticos da Tabela 8 foram calculados de forma
que P(S+ < sc) não supera o nível de significância estabelecido.
Exemplo 10.8 Vamos retomar o Exemplo 10.6. Como há possibilidade de
avaliar tanto a direção quanto a magnitude das diferenças, vamos usar o teste
dos sinais por postos, com a = 0,05. A tabela seguinte apresenta as diferenças e
a atribuição dos postos.
Antes Depois Diferença
Componente Postos
x 1 X2 D = X, - X2
1 400 395 - 5 1
2 360 350 - 10 3
3 450 556 106 8
4 390 480 90 5
5 430 405 - 25 4
6 386 500 114 9
7 452 547 95 6
8 470 462 - 8 2
9 400 500 100 7
10 340 480 140 10
Somando os postos referentes às diferenças positivas, obtemos s+ = 45.
Como o teste é unilateral à direita, o valor crítico sc é obtido na Tabela 8, tal
que P(S+ > sc) = 0,05 ou, equivalentemente, P(S+ < sc) = 0,95. A ilustração, a
seguir, mostra como obter o valor crítico sc através da Tabela 8.

TESTES NÃO PARAMÉTRICOS 3 0 1
P(S+ < sc) aproxim adam ente igual a
n
0,90 0,95 0,975
• • • • • •
• • •
40 46
10 \ ■ • • j • ■ •
Verificamos que sc = 44. Como s+ = 45 > sc, o teste rejeita H0 ao nível de
significância de 5%, mostrando evidência estatística de que o plano de manu­
tenção programada aumentou o tempo mediano de falha dos componentes do
sistema.
Note que a decisão desse teste foi diferente do teste dos sinais (Exemplo
10.6). Isso se deve ao teste dos sinais por postos (Teste de Wilcoxon) usar me­
lhor a informação dos dados, computando, em cada par de observações, não só
a direção da diferença, mas também o posto relativo às demais diferenças.
Assim, esse teste é mais poderoso do que o anterior, isto é, tem maior chance de
detectar a falsidade de H0, quando ela é realmente falsa.
Devemos dar preferência ao Teste de Wilcoxon, em relação ao teste dos si­
nais, sempre que for possível ordenar as diferenças da amostra pareada.
Amostra grande
A Tabela 8 fornece os valores críticos para n < 20. Para n > 20, a distribui­
ção de S+ é aproximadamente igual a uma distribuição normal, com média e
variância especificadas em (10.9) e (10.10). Assim, podemos calcular:
4s+ - n(n +1)
v'24
z ~
+ l)(2n + l) 4
e usar a distribuição normal padrão para obter o valor crítico zc, considerando o
nível de significância a e o tipo de hipótese alternativa.
Exemplo 10.9 Vamos retomar ao Exemplo 10.7, usando o teste dos sinais por
postos, com a = 0,05. As hipóteses e a regra de decisão são as mesmas apre­
sentadas anteriormente. A tabela seguinte apresenta as diferenças entre os cali­
bradores:

3 0 2 ESTATÍSTICA
Operário Eletr. Mec. Dif. Operário Eletr. Mec. Dif.
1 27,0 27,0 0,0 14 22,0 29,0 -7,0
2 25,0 30,1 -5,1 15 16,0 16,0 0,0
3 22,0 28,0 - 6,0 16 22,0 20,6 1,4
4 34,0 34,0 0,0 17 29,5 25,0 4,5
5 23,0 24,5 - 1,5 18 36,0 33,0 3,0
6 22,0 28,0 - 6,0 19 35,0 41,0 - 6,0
7 25,0 28,0 -3,0 20 35,0 35,0 0,0
8 32,3 30,0 2,3 21 27,5 28,0 - 0,5
9 34,0 36,0 -2,0 22 29,0 31,8 -2,8
10 23,5 29,0 - 5,5 23 27,0 28,0 -1,0
11 34,2 39,0 -4,8 24 24,3 29,3 - 5,0
12 31,8 30,0 1,8 25 30,1 30,8 -0 ,7
13 28,4 20,0 8,4 26 29,3 35,6 - 6,3
Como temos n = 22 casos com diferenças não nulas, usaremos a distribui­
ção aproximada normal. Excluímos os casos com diferença nula e fizemos a or­
denação dos casos em termos de diferenças absolutas. A alocação dos postos foi
feita em termos de diferenças absolutas, conforme mostra a tabela seguinte.
Quando houve empate (como nos operários 7 e 18), colocamos, inicialmente,
um posto para cada caso [coluna posto (a)] e, depois, calculamos a média [co­
luna posto (b)]. Nesta última coluna, colocamos o sinal da diferença entre pa­
rêntesis.
Dif. Posto Posto Dif. Posto Posto
Op. Dif. Op. Dif.
abs. (a) (b) abs. (a) (b)
21 - 0,5 0,5 1 1 (-) 17 4,5 4,5 12 12 (+)
25 -0,7 0,7 2 2 (-) 11 -4,8 4,8 13 13 (-)
23 -1,0 1,0 3 3 (-) 24 - 5,0 5,0 14 14 (-)
16 1,4 1,4 4 4 (+) 2 -5,1 5,1 15 15 (-)
5 - 1,5 1,5 5 5 (-) 10 - 5,5 5,5 16 16 (-)
12 1,8 1,8 6 6 (+) 3 - 6,0 6,0 17* 18,0 (-)
9 -2,0 2,0 7 7 (-) 6 - 6,0 6,0 18* 18,0 (-)
8 2,3 2,3 8 8 (+) 19 - 6,0 6,0 19* 18,0 (-)
22 -2,8 2,8 9 9 (-) 26 - 6,3 6,3 20 20 (-)
7 - 3,0 3,0 10* 10,5 (-) 14 -7,0 7,0 21 21 (-)
18 3,0 3,0 11* 10,5 (+) 13 8,4 8,4 22 22 (+)
* Procedimento para postos empatados.
Calculando os postos de diferenças positivas, temos: s+ = 62,5. E o valor
da estatística de teste para a amostra observada:

TESTES NÃO PARAMÉTRICOS 3 0 3
4 ít - n ( n + l ) ^ 4 4 (6 2 ,5 )-2 2 (2 3 ) ^ 4 , n?R
z = = ------- — ----------- —Z,U / o
yjn(n + l)(2n +1) 4 v 22(23)(45) 4
Considerando a regra de decisão baseada em zc = 1,645 (valor da distribui­
ção normal para a = 0,05 e teste unilateral), o teste rejeita H0, levando à mes­
ma decisão do teste dos sinais.
10.3.3 Teste de Mann-Whitney
O teste de Mann-Whitney ou teste de Wilcoxon-Mann-Whitney é usado para
comparar a posição central de duas populações, com base em amostras indepen­
dentes, extraídas aleatoriamente dessas populações. Veja os exemplos a seguir:
• um professor de Estatística quer comparar as médias obtidas em uma
prova padrão do assunto por alunos de dois cursos diferentes;
• com o propósito de avaliar a qualidade de duas máquinas, são compa­
rados os diâmetros das peças produzidas por elas;
• um administrador de rede quer saber se há diferenças significativas
nos tempos de processamento entre computadores tipo PC e Macin­
tosh (com configurações equivalentes).
Supostamente, os dados das duas amostras independentes são gerados por
populações com distribuições contínuas, embora as variáveis não precisem ser
observadas diretamente; pode ser observado apenas uma ordenação dos ele­
mentos. Sejam r\x a mediana da população 1 e r\2 a mediana da população 2. As
hipóteses podem ser colocadas como:
H0: ri! = r|2 e Hx: tu* ti*
sendo que na abordagem unilateral a hipótese alternativa é H^: % > rj2 ou H ”:
fli < ^2, dependendo do que se quer provar.
Sejam n: e n2 os tamanhos das amostras 1 e 2. Os rii + n2 elementos de­
vem ser ordenados em ordem crescente, em termos da variável observada. Atri­
buímos posto 1 à menor observação, posto 2 à segunda menor observação e
assim por diante, até o posto nx + n2 à maior observação. Quando houver em­
pates (valores iguais), adotaremos o mesmo procedimento do teste de sinais por
postos.
Chamamos de WY a soma dos postos da amostra 1 e W2 a soma dos postos
da amostra 2. É possível mostrar a seguinte relação:

3 0 4 ESTATÍSTICA
(n, +n2Y n "t"n2 + l)
W, + W 2 = ^ --------2- ^ ----------}- (10.12)
2
que pode ser usada para verificar os cálculos de Wx e W2.
A estatística do teste é basicamente a soma dos postos da amostra 1. Mas
faremos uma pequena alteração, para facilitar a análise quando as amostras
têm tamanhos diferentes. Consideraremos a estatística:
II 1
1 1 1
n ( n + ) '
I
i
C
N
1
(10.13)
Sob H0, a estatística U tem as seguintes características:
£(£/) = (10.14)
, v n,n2(n , + n 2 + l)
V(U ) = J 1 n 2-----}- (10.15)
A hipótese nula do teste é de que não há diferença entre as posições cen­
trais das duas populações. Sob essa hipótese, as somas dos postos referentes às
duas amostras devem apresentar resultados aproximadamente iguais, com as
devidas correções se as duas amostras tiverem tamanhos diferentes. Assim, se
H0 for verdadeira, observadas amostras independentes das duas populações, o
valor calculado de U, que chamaremos de u, não deve estar distante da grande­
za descrita em (10.14). Se for verificado u distante do valor esperado por H0,
há indícios para rejeitar H0 (considerando a hipótese alternativa e o nível de
significância do teste).
Amostras pequenas
Para nu n2 < 20, a Tabela 9 fornece valores críticos para ií, permitindo
construir a regra de decisão, em função da hipótese alternativa e do nível de
significância a do teste. Veja o Quadro 10.2.

TESTES NÃO PARAMÉTRICOS 3 0 5
Quadro 10.2 Regra de decisão do teste de Mann-Whitney para amostras peque­
nas, usando a Tabela 9 do Apêndice A.
Hipótese alternativa Regra de decisão
Hi’: ru > r\2 - Encontrar uc tal que P{JJ < uc) » 1 - a
- Se u > uc, então rejeita H0
Hi”: Th < r|2 - Encontrar uc tal que P([/ < uc) * a
- Se u < uc, então rejeita H0
Hx: th* ifc - Encontrar ucl tal que P(U < ucl) « a/2
- Encontrar uc2 tal que P(U < u » 1 - %
- Se u < ucl ou u > uc2, então rejeita H0
N ota: As probabilidades não são exatas, porque U é uma variável aleató­
ria discreta, mas os valores críticos da Tabela 9 foram calculados de forma que
P(U < uc) não supera o nível de significância a estabelecido.
Exemplo 10.10 Um fabricante de vergalhões de ferro para estruturas afirma
que seu novo produto apresenta resistência à tração superior ao modelo atual­
mente vendido, o que justificaria um preço maior. Um cliente não muito con­
vencido quer realizar um teste estatístico para avaliar a afirmação do fabrican­
te. Ele analisou 15 vergalhões de cada tipo. Os vergalhões foram submetidos à
tração, em kgf, até o rompimento. Estudos anteriores sugerem que essa variável
não segue uma distribuição normal, o que sugere o uso de teste não paramétri­
co. Os resultados são apresentados na tabela a seguir:
Vergalhão novo (1) Vergalhão atual (2)
276 380 237 119 696 240
231 127 143 461 298 246
144 234 260 473 327 566
151 165 237 380 293 232
195 198 174 287 199 108
As hipóteses são:
H0: a resistência mediana do vergalhão novo é igual à resistência media­
na do vergalhão atual;
Hx: a resistência mediana do vergalhão novo é maior que a resistência
mediana do vergalhão atual.

3 0 6 ESTATÍSTICA
Trata-se de um teste unilateral à direita, porque se espera que o novo ver-
galhão tenha maior resistência à tração que o atual. Adotaremos nível de signi-
ficância de 5%. Primeiramente, ordenamos os valores, sem levar em conta de
qual grupo cada um deles veio. Depois, atribuímos os postos, como é mostrado
a seguir:
Grupo1 Resist. Posto Grupo1 Resist. Posto
2 108 1 1 237 15,5
2 119 2 2 240 17
1 127 3 2 246 18
1 143 4 1 260 19
1 144 5 1 276 20
1 151 6 2 287 21
1 165 7 2 293 22
1 174 8 2 298 23
1 195 9 2 327 24
1 198 10 1 380 25,5
2 199 11 2 380 25,5
1 231 12 2 461 27
2 232 13 2 473 28
1 234 14 2 566 29
1 237 15,5 2 696 30
1 Códigos: 1 = novo; 2 = atual.
Chamando a amostra referente ao novo tipo de vergalhão de amostra 1,
calculamos a soma de postos: wl = 173,5. Logo:
15(15 +1)
u =173,5 - = 53,5
Com base na hipótese alternativa (H/: > ri2) e no nível de significância
a = 0,05, podemos construir a regra de decisão, de acordo com o Quadro 10.2.
É preciso encontrar o valor crítico uc para o qual P(U < uc) « 1 - 0,05 = 0,95.
Procurando na Tabela 9, conforme esquema a seguir, encontramos uc = 152.
Tl, = 15 P(U < uc) aproximadamente igual a
n2 0,90 0,95x 0,975
• ■ • • • •
• • •
144 160
• • • • • •
1 5 J
• • ■

TESTES NÃO PARAMÉTRICOS 3 0 7
Como a amostra produziu o valor u = 53,5, que é menor que o valor críti­
co, o teste aceita H0 ao nível de significância de 5%. Então, o teste de Mann-
Whitney não encontrou evidência estatística de que o novo vergalhão apresenta
resistência à tração superior à do atual.
Amostras grandes
Para nx > 20 ou n2 > 20, a distribuição de U aproxima-se de uma normal,
com média e variância especificadas em (10.14) e (10.15). Assim, podemos cal­
cular:
(10.16)
e usar a distribuição normal padrão (Tabela 3) para obter o valor crítico zc, con­
siderando o nível de significância a e o tipo de hipótese alternativa.
Exemplo 10.11 Um administrador de rede tem recebido insistentes reclama­
ções de usuários de que os tempos de processamento dos dois servidores da
rede são diferentes, no que tange ao acesso às correspondências eletrônicas.
Intrigado, porque se supunha que não haveria razão para diferenças (suas con­
figurações são praticamente iguais), ele coletou dados dos dois servidores, re­
gistrando os tempos de acesso (em segundos) de 30 usuários em cada servidor,
cujos resultados estão na tabela a seguir. Sabe-se que os tempos de acesso não
seguem uma distribuição normal, e não há hipótese a priori sobre qual servidor
é mais rápido.
Servidor 1 Servidor 2
5,83 3,78 6,79 2,27 6,24 2,44
0,99 1,40 2,70 7,41 4,73 4,17
6,07 5,88 3,05 3,21 9,34 5,01
6,53 3,52 2,44 7,76 4,33 16,68
0,04 3,42 3,74 2,24 4,63 2,97
4,96 0,99 2,66 1,93 3,97 13,45
6,86 1,72 3,09 6,07 4,61 5,35
2,55 4,05 2,03 3,80 5,02 1,80
2,63 1,70 4,65 2,93 6,40 2,97
1,97 6,48 4,26 9,04 4,51 10,75

3 0 8 ESTATÍSTICA
As hipóteses são:
H0: “Hi = ^2 e Hx: * ti2
onde rji é a mediana do tempo de acesso do servidor 1 e rj2 é a mediana do
tempo de acesso do servidor 2. Faremos o teste ao nível de significância de 5%.
Assim, a regra de decisão, para uma estatística com distribuição normal padrão,
é apresentada na Figura 10.8.
(tabela)
* . ' aceita H01 . . *
rejeita Hn 0 rejeita Hn
Figura 10.8 Regra de decisão para um teste bilateral, a = 0,05, utilizando a dis­
tribuição normal padrão.
Calculando a soma dos postos da amostra 1, obtemos wx = 754. Resultan­
do no seguinte valor para a estatística U:
30(30+ 1) _
ni(ni +1)
= 7 5 4 - = 289
Aplicando (10.15):
(30)(30)
n.ji2
u - 2 8 9 -
z = = -2,38
;(30)(30)(30 +30 + l)
lnin2(ni + n2 + l)
12 12
Comparando o valor calculado de z com a regra de decisão da Figura 10.8,
verificamos que o teste rejeita H0 ao nível de significância de 5%. O teste de
Mann-Whitney encontrou evidência estatística de que os tempos medianos
de acesso aos dois servidores são diferentes.

TESTES NÃO PARAMÉTRICOS 3 0 9
EXERCÍCIOS
9. Um banco pretende trocar os terminais que seus caixas usam para atender
ao público, com o intuito de conseguir diminuir o tempo de atendimento.
Para avaliar se vale a pena a mudança, foi realizado um estudo em que os
mesmos caixas atendiam a clientes com o terminal atual e com o novo
(após treinamento), e os tempos médios de atendimento (em minutos) de
cada caixa foram:
Caixa Terminal atual Terminal novo
1 1,6 0,5
2 3,5 0,3
3 0,8 5,9
4 1,1 1,6
5 7,1 1,7
6 8,4 2,2
7 4,8 1,0
8 5,9 1,4
9 2,4 1,0
10 5,5 2,1
a) O terminal novo reduz o tempo de atendimento? Use o teste dos sinais
com a = 0,05.
b) Repita o item (a), utilizando o teste dos sinais por postos.
c) O que você conclui com base nos itens (a) e (b)? Por quê?
10. O mesmo banco do Exercício 9 acredita que o terminal novo pode vir a re­
duzir o número de pessoas nas filas. No mesmo estudo descrito anterior­
mente, o número de pessoas na fila foi monitorado:
Caixa Terminal atual Terminal novo
1 5 1
2 3 3
3 2 6
4 6 6
5 3 2
6 6 6
7 2 2
8 5 2
9 3 2
10 4 2

3 1 0 ESTATÍSTICA
a) O terminal novo reduz o tempo de atendimento? Use o teste dos sinais
com a = 0,05.
b) Repita o item (a) utilizando o teste dos sinais por postos.
11. Certa rede local de computadores tem como principal problema a baixa
taxa de transmissão de dados (em kbps). Estuda-se a possibilidade de em­
pregar um novo cabeamento, que supostamente aumentaria a taxa de
transmissão de dados. Devido aos custos envolvidos, o gerente da rede de­
cidiu realizar um experimento: os mesmos conjuntos de instruções foram
executados pelo mesmo cliente, com o cabeamento atual e o proposto, e
suas taxas de transmissão de dados medidas. Os resultados estão na tabela
a seguir:
Instruções Atual Proposto Instruções Atual Proposto
1 15,3 101,7 17 1,0 73,2
2 93,7 47,3 18 54,4 4,0
3 307,6 1.570,6 19 118,3 84,2
4 322,8 342,8 20 1,5 473,5
5 14,8 9,7 21 0,9 474,6
6 15,0 34,0 22 20,5 582,7
7 135,8 31,6 23 119,2 54,0
8 21,3 1.050,9 24 3,9 895,4
9 3,1 282,3 25 10,4 32,2
10 15,2 26,8 26 5,8 3.514,7
11 2,2 2,6 27 304,7 1.522,5
12 39,6 1.406,4 28 182,2 67,4
13 1,6 136,0 29 12,0 176,2
14 58,0 2.264,0 30 16,5 80,3
15 1,6 25,0 31 9,5 9,2
16 27,2 1,0 32 5,2 1,6
a) Pelo teste dos sinais, o cabeamento proposto aumenta a taxa de trans­
missão dos dados? Use nível de significância de 1%.
b) Repita o item (a), utilizando o teste dos sinais por postos.
12. Em um processo de moldagem de peças plásticas, é preciso escolher quais
dos dois métodos atualmente utilizados é o que obtém menor desperdício,
que é mensurado pelo peso, em gramas, do polímero que “escapa” do mol­

TESTES NÃO PARAMÉTRICOS 3 1 1
de. Nem sequer se sabe se os dois métodos (chamados de 1 e 2) são real­
mente diferentes. Para tentar resolver o problema, o engenheiro responsá­
vel selecionou 25 operadores (treinados em ambos os métodos) e mediu os
valores desperdiçados em cada método. Os valores, em gramas, foram:
Operador Método 1 Método 2 Operador Método 1 Método 2
1 0 0,642 14 0,001 0
2 0,247 0,106 15 0,182 19,657
3 0,678 0 16 0,073 0
4 1,577 0,142 17 0,314 8,651
5 0,002 0,001 18 0,001 0
6 0,041 1,025 19 5,890 1,324
7 0,593 0 20 0,016 0
8 0 0,322 21 0,190 8,346
9 4,078 0 22 0,366 0,007
10 0,049 3,635 23 0,010 0
11 1,010 24,113 24 0,002 7,858
12 0,066 0,338 25 2,566 0
13 0 19,746
a) Pelo teste dos sinais, usando um nível de significância de 5%, o que
você conclui?
b) Repita o item (a) pelo teste dos sinais por postos.
c) Qual é sua conclusão? Por quê?
13. Como parte de seu trabalho de conclusão de curso, um aluno de computa­
ção resolveu verificar se dois tipos de arquitetura (chamadas de A e B) dife­
rem quanto à velocidade de processamento, num dado sistema computacio­
nal. Sob a arquitetura A, o aluno executou uma série de instruções e mediu
os tempos de processamento, em milissegundos. Fez o mesmo sob a arqui­
tetura B, com uma série de instruções análoga à que foi usada na arquitetu­
ra A. Os resultados, em milissegundos, foram:
Rede A Rede B
4,56 0,19 0,68 43,88
0,72 0,25 1,90 6,40
5,89 0,68 1,31 1,89
0,12 1,92 0,21 3,44
2,54 12,77 1,78 1,15
0,89 3,36 0,43 11,11

3 1 2 ESTATÍSTICA
Para o nível de significância de 5%, as duas arquiteturas diferem quan­
to ao tempo de processamento?
14. Dois tipos de concreto (X e Y) estão tendo suas resistências à compressão,
em kgf, avaliadas por ensaios. Suspeita-se que o concreto Y seja mais resis­
tente, o que poderia justificar seu maior preço. Sabe-se que as distribuições
das trações, para ambos os tipos, não podem ser aproximadas por uma nor­
mal. Com base nos resultados apresentados a seguir, e considerando um ní­
vel de significância de 1%, a suspeita é confirmada?
Concreto X:
243,37 244,03 249,8 209,84 244,79
233,11 241,34 214,33 200,19 214,55
Concreto Y:
300,53 355,98 305,12 280,34 502,06 250,75 224,65
15. O tempo de rompimento dos elos fusíveis é um fator crucial para a prote­
ção dos sistemas de distribuição de energia elétrica: uma vez ocorrido um
curto circuito, o fusível deve romper-se no menor tempo possível. A conces­
sionária de energia elétrica de um estado brasileiro está estudando a ado­
ção de um novo modelo, que o fabricante declara ter menor tempo de rom­
pimento do que o modelo atual. Como parte do processo de decisão, foram
realizados ensaios com os dois modelos. Eles foram submetidos a correntes
de curto circuito, e seus tempos até o rompimento foram monitorados.
Com base nos resultados (descritos a seguir), e usando um nível de signifi­
cância de 5%, deve-se cogitar a adoção do novo modelo de elo fusível?
Tempos de rompimento (em segundos) - Atual elo fusível:
0,89 3,32 1,20 3,07 1,57 0,15 0,88 0,29 1,59 3,74 4,57
1,17 0,62 6,82 0,28 7,45 1,05 8,48 0,48 0,35 0,60 0,97
Tempo de rompimento (em segundos) - Novo elo fusível:
0,68 3,44 1,69 0,69 0,61 1,31 1,82 0,37 2,72 0,02 1,03
0,03 0,02 1,22 4,88 0,17 1,6 1,91 0,35 4,3 0,82 0,24
1,06 0,17 0,74
16. No processo de produção de papel, a degradação da lignina (uma enzima)
é um aspecto fundamental e precisa ser feito rapidamente, exigindo, usual­
mente, a utilização de cloro, o que pode ser danoso ao meio ambiente. Re­
centemente, foram realizadas pesquisas que procuram avaliar a viabilidade
de degradação da lignina através da ação de fungos, em bio-reatores, redu-

TESTES NÃO PARAMÉTRICOS 3 1 3
zindo os danos ao meio ambiente e os gastos com tratamento de efluentes
das fábricas de papel. Os departamentos de engenharia química e botânica
de uma universidade brasileira resolveram realizar um experimento para
avaliar duas espécies de fungo, medindo o tempo gasto para degradar um
pequeno cubo de madeira de eucalipto. Acredita-se que a espécie 1 consiga
degradar a lignina em menos tempo. Os resultados obtidos (em dias) estão
descritos a seguir:
Espécie 1
6.5 11,0 16,0 13,5 13,0 16,5 28,5 6,0 7,0 10,0
6.0 7,5 17,5 10,5 14,5 15,0 16,0 4,0 10,5 27,5
5.5 8,5 37,0 25,0 19,0
Espécie 2
51.5 22,5 17,5 16,0 46,5 32,0 5,5 14,0 15,5 38,5
36.5 46,0 17,0 13,0 19,0 34,5 20,0 59,5 14,5 20,5
12.0 66,0 29,5 59,0 19,0
A espécie 1 realmente é mais rápida? Use nível de signifícância de 5%.
EXERCÍCIOS COMPLEMENTARES
17. Uma concessionária de energia elétrica pretende calcular intervalos de con­
fiança para o consumo mensal de kWh de pequenos consumidores. Medi­
ções anteriores indicam que o consumo segue uma distribuição normal
com média de 85 kWh e desvio padrão de 15 kWh. Uma amostra aleatória
de 25 consumidores foi selecionada, registrando seu consumo mensal:
82,01 67,62 80,48 77,35 109,02
92,51 70,53 86,35 60,65 82,36
132,11 66,18 88,56 69,53 101,34
99,45 70,00 80,50 74,87 68,96
101,08 87,87 100,2 92,74 97,55
a) Use o teste qui-quadrado de aderência para verificar se a suposição ba­
seada nas medidas anteriores ainda é válida, em nível de signifícância
de 5%. (Sugestão: defina as categorias utilizando os quartis da distri­
buição normal suposta.)
b) Refaça o problema, usando o teste de aderência de Kolmogorov-Smimov.

3 1 4 ESTATÍSTICA
18. Certa empresa tem 3 unidades fabris. Suspeita-se que a existência de defei­
tos nos produtos estaria associada à unidade fabril que os produziu. Para
testar isso, coletou-se uma amostra, obtendo-se:
Fábrica 1: 110 produtos sem defeito e 40 produtos com defeito.
Fábrica 2: 50 produtos sem defeito e 20 produtos com defeito.
Fábrica 3: 85 produtos sem defeito e 15 produtos com defeito.
Teste a suspeita da empresa ao nível de significância de 5%.
19. Um instituto de metrologia está fazendo uma avaliação da qualidade de
certo produto de limpeza, que é produzido por 3 filiais diferentes da mes­
ma empresa. O produto precisa ter uma concentração adequada de desinfe­
tante. Os testes identificaram 3 tipos de concentração: Adequada, Regular
e Inadequada. Os resultados estão na tabela a seguir:
Filial 1 Filial 2 Filial 3
Adequada 350 100 80
Regular 90 30 40
Inadequada 100 10 150
A concentração de desinfetante no produto é homogênea nas 3 filiais?
Use nível de significância de 1%.
.
20 O gerente de produção de um conglomerado industrial quer avaliar se as
mudanças no programa da Qualidade foram aprovadas pelos funcionários.
Uma amostra aleatória de 400 pessoas foi selecionada, e sua opinião sobre
o programa foi registrada, antes e após a introdução das mudanças. Os re­
sultados foram:
Após as mudanças
Antes das mudanças
Aprovam Não aprovam
Aprovavam 170 30
Não aprovavam 190 10
Usando um teste adequado, verifique se as mudanças do programa da
Qualidade foram aprovadas pelos funcionários. Use a = 0,05.
21. Estamos interessados em verificar se há diferenças entre o desempenho es­
colar de homens e o de mulheres no curso de engenharia de produção.
Aplicamos a mesma prova a um grupo de 15 alunas e a um grupo de 13
alunos, que obtiveram os resultados a seguir:

TESTES NÃO PARAMÉTRICOS 3 1 5
Alunas 4,5 8,9 6,8 7,8 5,4 10,0 5,7 8,0
5.0 6,0 7,6 7,5 4,0 6,8 9,0
Alunos 3,5 6,5 8,0 2,0 9,5 5,6 4,5
7.0 8,8 7,5 8,0 1,5 6,5
Testes de aderência concluíram que não é possível usar um teste para­
métrico. Usando nível de significância de 1%, qual é a sua conclusão?
22. Uma olaria de SC estava preocupada com a qualidade dos seus produtos
(pois estava perdendo muitos clientes para a concorrência). Resolveu, então,
implantar um programa de qualidade, objetivando diminuir o número de
tijolos defeituosos produzidos por seus 12 operários. Os números de tijolos
defeituosos produzidos antes e após o programa estão na tabela a seguir:
Operário 1 2 3 4 5 6 7 8 9 10 11 12
Antes 47 56 54 49 36 48 51 38 61 49 56 52
Depois 71 34 45 34 50 24 42 35 53 20 67 50
Testes de aderência indicam a necessidade de utilizar testes não para­
métricos. Usando nível de significância de 2,5%, o programa de qualidade
deu resultados?
23. Há interesse em avaliar o comportamento de um tipo de pneu especial, su­
postamente de grande durabilidade. Há dois fabricantes, e 30 pneus de
cada um foram selecionados, ao acaso, para avaliar sua durabilidade. Os
resultados foram:
101900 40900 170600 151100 92600 91100
281700 113300 78200 141700 244200 129600
Fabricante 1: 36500 72100 49000 227400 103100 72000
58300 128100 132400 34800 165900 94200
113200 87900 92100 97400 99700 87500
218500 108000 46000 106000 49200 144200
153400 59600 82800 94900 235400 91800
Fabricante 2: 204400 211100 114600 173700 195300 144300
493400 586700 59000 235100 137700 102400
40600 240100 145600 128900 328000 65500
Testes de aderência mostraram a inadequação da distribuição normal
para descrever a duração, mas é razoável supor que a distribuição seja si­
métrica. Pode-se dizer que as vidas médias são diferentes nas populações
de onde vieram os pneus, ao nível de significância de 5%?

11
Correlação e Regressão
11.1 CORRELAÇÃO
Numa população de pessoas, podemos dizer que as variáveis peso e altura
são correlacionadas positivamente, pois a maioria dos indivíduos altos também é
pesada, enquanto a maioria dos indivíduos baixos é leve. De forma análoga, o
faturamento de uma empresa e o nível de utilização do seu sistema computacio­
nal devem ter correlação positiva. Já a quantidade de memória RAM e o tempo
de processamento devem ter correlação negativa.
Dizemos que duas variáveis, X e Y, estão positivamente correlacionadas
quando elas caminham num mesmo sentido, ou seja, elementos com valores pe­
quenos de X tendem a ter valores pequenos de Y e elementos com valores gran­
des de X tendem a ter valores grandes de Y. Estão negativamente correlaciona­
das quando elas caminham em sentidos opostos, ou seja, elementos com valores
pequenos de X tendem a ter valores grandes de Y e elementos com valores
grandes de X tendem a ter valores pequenos de Y.
É importante ressaltar que o conceito de correlação refere-se a uma asso­
ciação numérica entre duas variáveis, não implicando, necessariamente, relação
de causa-e-efeito, ou mesmo uma estrutura com interesses práticos. A análise de
dados para verificar correlações é usualmente feita em termos exploratórios;
verificação de uma correlação serve como elemento auxiliar na análise do pro­
blema em estudo. Ou seja, o estudo da correlação numérica entre as observa­
ções de duas variáveis é geralmente um passo intermediário na análise de um
problema.

CORRELAÇÃO E REGRESSÃO 3 1 7
Diagramas de dispersão
Uma forma de visualizarmos se duas variáveis apresentam-se correlaciona­
das é através do diagrama de dispersão, onde os valores das variáveis são repre­
sentados por pontos, num sistema cartesiano.
Exemplo 11.1 No processo de queima de massa cerâmica para pavimento,
corpos de prova foram avaliados por três variáveis: XY = retração linear (%),
X2 = resistência mecânica (MPa) eX 3 = absorção de água (%). Os resultados
de 18 ensaios são apresentados a seguir:
Ensaio X! X x 3 Ensaio X x 2 x 3
2 1
1 8,70 38,42 5,54 10 13,24 60,24 0,58
2 11,68 46,93 2,83 11 9,10 40,58 3,64
3 8,30 38,05 5,58 12 8,33 41,07 5,87
4 12,00 47,04 1,10 13 11,34 41,94 3,32
5 9,50 50,90 0,64 14 7,48 35,53 6,00
6 8,58 34,10 7,25 15 12,68 38,42 0,36
7 10,68 48,23 1,88 16 8,76 45,26 4,14
8 6,32 27,74 9,92 17 9,93 40,70 5,48
9 8,20 39,20 5,63 18 6,50 29,66 8,98
6 7 8 9 10 11 12 13 14 6 7 8 9 10 11 12 13 14
Retração linear (%) Retração linear (%)
25 30 40 45 55 60 65
Resistência mecânica (MPa)
Figura 11.1 Diagramas de dispersão de uma amostra de 18 observações das va­
riáveis retração linear, resistência mecânica e absorção de água, em
massas cerâmicas.

3 1 8 ESTATÍSTICA
A Figura 11.1 sugere que existe correlação positiva entre resistência mecâ­
nica e retração linear. E correlação negativa entre absorção de água e retração
linear; e entre resistência mecânica e absorção de água.
11.2 COEFICIENTE DE CORRELAÇÃO LINEAR DE PEARSON
Nesta seção, apresentaremos o chamado coeficiente de correlação (linear) de
Pearson, que descreve a correlação linear dos dados de duas variáveis aleatórias.
A ideia da construção do coeficiente de correlação
O valor do coeficiente de correlação não deve depender da unidade de me­
dida dos dados. Por exemplo, o coeficiente de correlação entre as variáveis peso
e altura, observadas num certo conjunto de indivíduos, deve acusar o mesmo
valor, independentemente se o peso for medido em gramas ou quilogramas e a
altura em metros ou centímetros.
Para evitar o efeito da unidade de medida, consideramos os dados em ter­
mos da quantidade de desvio padrão que se afastam da média. Assim, a padro­
nização de (*!, y j , (x2, y2), fo , y n) é feita da seguinte forma:
, x ( - x
------ y[ = —— — (i = 1, 2, n)
X : = —
s>
onde: x: média de x ly x2, xn;
sx: desvio padrão de Xi, x2, xn;
y: média de y lt y 2, y n;
sy: desvio padrão de y l9 y 2, ..., y n.
A Figura 11.2 ilustra dois diagramas de dispersão entre as variáveis resis­
tência mecânica e retração linear. O primeiro na escala original e o segundo na
escala padronizada.
i 65 tA
-------.--------------------r—------
O 9
w 60
na Z
KJ
.5 55 •8 ° , (0 , 0)
a 1 i
M 50 o
45 T) Ü •
„
-------- 1 — £ ♦
? 40 •• • •
TO IA
o v - i •
o C 35 •
O
<CJ 30 •
•
'S? 25 _ -2
- 2 - 1 0 1 2
6 7 8 9 10 11 12 13 14
& 5
Retração linear (%) Valores padronizados de resistência
Figura 11.2 Ilustração do efeito da padronização das escalas.

CORRELAÇÃO E REGRESSÃO 3 1 9
Olhando a Figura 11.2, é possível notar que, no caso de correlação positi­
va, os pontos tendem a se localizar nos quadrantes I e III (x’ e / com o mesmo
sinal). De forma análoga, quando houver correlação negativa, os pontos ten­
dem a se localizar nos quadrantes II e IV (x* e y 3 com sinais trocados). Assim, a
soma dos produtos -x^y5, (i = 1, 2, ..., n) deve ter sinal positivo ou negativo, de­
pendendo do sentido da correlação. Baseado nessa ideia, o coeficiente de corre­
lação linear de Pearson, r, é definido pela seguinte expressão, em termos dos
valores padronizados:
r = ---------- (11.2)
n -1
Para ilustrar a obtenção do coeficiente r, considere 3 observações do par
de variáveis aleatórias (X, Y): (3, 6), (4, 4), (5, 2). Temos: x = 3, y = 4, sx = 1
e sy = 2. Daí, decorrem os seguintes pares de valores padronizados: (-1, 1),
(0, 0), (1, -1) A Figura 11.3 mostra os pontos nos dois sistemas de coordenadas.
7
y
6
i
13
c
C b
■5b i
■g< 1
* 3
u
1 ►
■S3 -
0
2 3 4
Escala X original
Figura 11.3 Padronização de três observações de (X, Y).
Calculando o coeficiente de correlação de Pearson:
$(xy:)
r HXiMoXo)+(iX-0
,
n -1
Interpretação do coeficiente de correlação
Para qualquer conjunto de dados, podemos demonstrar que o valor do
coeficiente de correlação de Pearson, r, estará no intervalo de -1 a 1. Será posi-

3 2 0 ESTATÍSTICA
tivo quando os dados apresentarem correlação linear positiva; será negativo
quando os dados apresentarem correlação linear negativa.
O valor de r será tão mais próximo de 1 (ou -1) quanto mais forte for a
correlação nos dados observados. Teremos r = +1 se os pontos estiverem exa­
tamente sobre uma reta ascendente (correlação positiva perfeita). Por outro
lado, teremos r = -1 se os pontos estiverem exatamente sobre uma reta descen­
dente (correlação negativa perfeita). Quando não houver correlação nos dados, r
acusará um valor próximo de 0 (zero).
A Figura 11.4 mostra os possíveis valores de r e a interpretação em termos
do sentido (positivo ou negativo) e da força (fraca, moderada ou forte) da cor­
relação.
4---------------------------------- valor de r ----------------------------------*•
B o -a -o D o -a -o n "
ausência
SENTIDO: negativa negativa negativa positiva positiva positiva
FORÇA: forte moderada fraca fraca moderada forte
Figura 11.4 Sentido e força da correlação, em termos do coeficiente r.
Exemplo 11.1 (continuação) Com as 18 observações das variáveis retração
linear (%), resistência mecânica (MPa) e absorção de água (%), calculamos o
coeficiente de correlação de Pearson para cada par das variáveis, como é mos­
trado a seguir:
Resistência Absorção
Retração linear
mecânica de água
Retração linear 1,00 0,75 - 0,88
Resistência mecânica 0,75 1,00 - 0,84
Absorção de água -0,88 - 0,84 1,00
Observamos que, entre resistência mecânica e retração linear, temos cor­
relação positiva de moderada a forte. Entre retração linear e absorção de
água, e entre resistência mecânica e absorção de água, temos correlações ne­
gativas fortes.

CORRELAÇÃO E REGRESSÃO 3 2 1
Cálculo do coeficiente de correlação de Pearson
Efetuar o cálculo do coeficiente de correlação r através dos valores padro­
nizados, além de ser bastante trabalhoso, tem o inconveniente de incorporar er­
ros de arredondamentos no cálculo dos valores padronizados, podendo com­
prometer o resultado final. Em geral, é conveniente usar a expressão a seguir,
que é matematicamente igual à expressão (11.2)
r = (11.3)
t ò * . 2 - ( Z / . ) '
Ilustraremos o uso de (11.3) com as 3 observações (3, 6), (4, 4), (5, 2):
•
Xi *i2 í2 Xfi
1
y
1 3 6 9 36 18
2 4 4 16 16 16
3 5 2 25 4 10
Soma 12 12 50 56 44
'
w' I
(12)(12)
“ 1 2 -1
V6 • \'24
/s (5 0 ) - ( 1 2 ) 2 • J 3 (5 6 )-(1 2 )2
Coeficiente de correlação populacional
De forma análoga, como definimos a medida descritiva de correlação entre
as observações em (11.2) e (11.3), podemos definir, em termos probabilísticos,
o parâmetro correlação entre duas variáveis aleatórias, X e 7, pelo valor espera­
do do produto destas variáveis padronizadas, ou seja:
X - \ i x Y -V :
p = Corr(X,Y) = E (11.4)
/
onde nx = ECX), Hy = E(Y), ax = J V ( X ) e a r = J v ( Y )
1 Por simplicidade, daqui para frente excluiremos os índices dos somatórios.

3 2 2 ESTATÍSTICA
Inferência sobre p
Dada uma amostra aleatória simples {xl9 y x), {x2, y2), (*r2, yn) de n ob­
servações do par de variáveis aleatórias (X, Y), o coeficiente r, calculado por
(11.2) ou (11.3), pode ser considerado uma estimativa do verdadeiro e desco­
nhecido coeficiente p.
É comum o interesse em verificar as seguintes hipóteses:
H0: p = 0 (as variáveis X e Y são não correlacionadas);
Hj: p * 0 (as variáveis X e Y são correlacionadas).
podendo, ainda, a hipótese alternativa indicar o sentido da correlação (teste
unilateral), tal como H /: p > 0 (Xe Ysão correlacionadas positivamente) ou Hi”:
p < 0 (X e Y são correlacionadas negativamente). O teste unilateral é aplicado
nos casos em que esperamos o coeficiente de correlação com determinado sinal
(+ ou -).
Restringindo-se à verificação de correlação linear e supondo X e Y com dis­
tribuições normais, podemos realizar o teste, calculando
t = r- £ (11.5)
v 1 - r 2
e usando como distribuição de referência a t de Student com gl = n - 2. A Tabe­
la 10 do apêndice apresenta uma forma mais rápida para esse teste. Para cada
n, a Tabela 10 apresenta o valor absoluto mínimo de r para se rejeitar H0.
Exemplo 11.1 (continuação) Calculamos, anteriormente, as seguintes corre­
lações baseadas em n = 18 observações:
Retração Resistência Absorção
linear mecânica de água
Retração linear 1,00 0,75 - 0,88
Resistência mecânica 0,75 1,00 -0,84
Absorção de água - 0,88 - 0,84 1,00
Considerando testes bilaterais ao nível de significância de 5%, verificamos
na Tabela 10 que, para n = 18, o valor absoluto mínimo para a correlação ser
significativa (rejeitar H0) é 0,468. Como os três coeficientes calculados são, em
valor absoluto, superiores a 0,468, concluímos que as três medidas usadas para
avaliar a qualidade da cerâmica são realmente correlacionadas.

CORRELAÇÃO E REGRESSÃO 3 2 3
EXERCÍCIOS
1. Calcule o coeficiente de correlação de Pearson entre retração linear (%) e
resistência mecânica (MPa) para as 5 primeiras observações apresentadas
no Exemplo 11.1. Apenas com estas observações, o teste estatístico detecta
correlação real entre as duas variáveis?
2. Com respeito aos 23 alunos de uma turma de estatística, foram observadas
as variáveis número de faltas e nota final na disciplina. Esses dados acusa­
ram a seguinte correlação, descrita pelo coeficiente de correlação de Pear­
son: r = - 0,56. Comente as seguintes frases relativas à turma em estudo e
ao coeficiente obtido.
a) “Como r = - 0,56 (correlação negativa moderada), nenhum aluno com
grande número de faltas tirou nota alta.”
b) “Como as duas variáveis são correlacionadas, bastaria usar uma delas
como critério de avaliação, pois uma acarreta a outra.”
c) “Os dados observados mostraram uma leve tendência de que a nota fi­
nal se relaciona inversamente com o número de faltas, ou seja, os alu­
nos frequentadores tiveram, em geral, melhor desempenho nas avalia­
ções do que os alunos que faltaram muito.”
3. Sejam X = nota na prova do vestibular de matemática e Y = nota final na
disciplina de cálculo. Estas variáveis foram observadas em 20 alunos, ao fi­
nal do primeiro período letivo de um curso de engenharia. Os dados são
apresentados a seguir:
X Y X y X y X y X y
39 65 43 78 21 52 64 82 65 88
57 92 47 89 28 73 75 98 47 71
34 56 52 75 35 50 30 50 28 52
40 70 70 50 80 90 32 58 67 88
a) Calcule a correlação entre a nota no vestibular de matemática e a nota
na disciplina de cálculo. Interprete o resultado.
b) Construa um diagrama de dispersão e verifique se algum aluno foge ao
comportamento geral dos demais (ponto discrepante).
c) Retire o valor discrepante detectado no item anterior e calcule nova­
mente o coeficiente r. Interprete.
d) Verifique se a correlação encontrada no item anterior é significativa.
Faça o teste ao nível de signifícância de 5% e interprete o resultado.

3 2 4 ESTATÍSTICA
4. No desenvolvimento computacional de um escalonador, foram realizados
alguns testes em 16 condições experimentais diferentes. O desempenho do
escalonador foi observado através da quantidade de trabalho executado,
num certo período de tempo: em processamento de textos (Xj), em proces­
samento interativo de dados (X2) e em processamento de dados em batch
(X3). Os coeficientes de correlação calculados sobre as 16 observações foram:
x, x2 x3
*1 1,00 0,18 0,86
*2 0,18 1,00 0,02
*3 0,86 0,02 1,00
Que informações podem ser extraídas dessa matriz de correlações? Há
evidências de que nas situações em que desempenho é melhor para um atri­
buto (por exemplo, processamento de texto), ele também tende a ser me­
lhor em outro atributo (por exemplo, processamento interativo de dados) ?
11.3 REGRESSÃO LINEAR SIMPLES
O termo regressão surgiu com os trabalhos de Galton no final do século
XIX. Esses trabalhos procuravam explicar certas características de um indivíduo
a partir das características de seus pais, como, por exemplo, predizer a altura
de um indivíduo em função das alturas de seus pais. O modelo matemáti-
co-estatístico foi aperfeiçoado e hoje é utilizado nas mais variadas áreas, em
particular na engenharia e na informática.
Iniciaremos o estudo de regressão com a formulação mais simples, relacio­
nando uma variável 7, chamada de variável resposta ou dependente, com uma
variável X, denominada de variável explicativa ou independente.2 Veja o Qua­
dro 11.1.
2 Dizemos que a regressão é simples, porque estamos considerando apenas uma variável
independente.

CORRELAÇÃO E REGRESSÃO 3 2 5
Quadro 11.1 Exemplos de aplicação da regressão linear simples.
Variável independente, X ----- ► Variável dependente, Y
Temperatura do forno (°C) Resistência mecânica da cerâmica (MPa)
Quantidade de aditivo (%) Octanagem da gasolina
Renda (RS) Consumo (R$)
Memória RAM do computador (Gb) Tempo de resposta do sistema (s)
Área construída do imóvel (m2) Preço do imóvel (RS)
Observe que os exemplos do Quadro 11.1 se distinguem dos exemplos so­
bre correlação por suporem uma relação de causalidade entre X e Y. É esta a di­
ferença básica de um estudo de correlação e uma análise de regressão. A aplica­
ção da análise de regressão é geralmente feita sob um referencial teórico, que
justifique uma relação matemática de causalidade. Além disso, a variável X nor­
malmente é controlada (não aleatória) e Y é uma variável aleatória.
Assim como num estudo de correlação, a análise de regressão também
parte de um conjunto de observações pareadas (x1,y 1), Oc2,y 2), •••> y J , rela­
tivas às variáveis X e Y.
Exemplo 11.2 Considere um experimento em que se analisa a octanagem da
gasolina (Y) em função da adição de um novo aditivo (X). Para isso, foram rea­
lizados ensaios com os percentuais de 1, 2, 3, 4, 5 e 6% de aditivo. Os resulta­
dos são mostrados na Figura 11.5.
X y E 86’°
& 85,0
1 80,5
1 84,0
u
2 81,6 o
83.0
0)
T3
3 82,1 0) 82.0
U
• ■
4 83,7 81,0
e
5 83,9 80,0
0 1 2 3 4 5 6
6 85,0
Quantidade de aditivo (%)
Figura 11.5 Dados experimentais do efeito de um aditivo (X) na octanagem da
gasolina (Y).
Observe que é razoável supor uma relação aproximadamente linear entre
X e 7 para os níveis de aditivo ensaiados (de 1 a 6%). Contudo, os pontos não

3 2 6 ESTATÍSTICA
estão exatamente sobre uma reta, provavelmente por causa da existência de fa­
tores não controláveis no processo. Vamos supor, então, que o valor esperado
de Y varie com X, de acordo com uma equação de primeiro grau, ou seja:
E{Y} = a + PX (11.6)
onde a e p são os parâmetros do modelo.
Seja um conjunto de observações (xb yi), (x2, y 2), •••> (*n, yJ* O chamado
modelo de regressão linear simples para as observações é dado por
Yi = a + p*i + Si (11.7)
onde: Yt é a variável aleatória associada à i-ésima observação de Y; e
e, é o erro aleatório da i-ésima observação, isto é, o efeito de uma infini­
dade de fatores que estão afetando a observação de Y de forma alea­
tória.
Note que é razoável supor £{e,} = 0 (i = 1, 2,..., n). Assim, considerando
X uma variável controlável (não aleatória), temos, pelas propriedades do valor
esperado (Capítulo 5): £{7,} = a + p*t, compatível com (11.6) para a i-ésima
observação.
11.3.1 Método dos mínimos quadrados
Para a construção do modelo descrito em (11.6), precisamos obter estima­
tivas para a e p, a partir de um conjunto de observações (*i,yi), 0c2, y2) , ..., (xn,
yn). Ou seja, queremos encontrar a reta que passe o mais próximo possível dos
pontos observados.
Há vários métodos para estimar os parâmetros do modelo. O mais usual é
o método de mínimos quadrados, que consiste em fazer com que a soma dos er­
ros quadráticos seja a menor possível. Considerando o modelo (11.7), temos
que o erro aleatório da i-ésima observação (i = 1, 2,..., n) é dado por
£i = Yi - (a + pXi) (11.8)

CORRELAÇÃO E REGRESSÃO 3 2 7
conforme ilustramos anteriormente.
O método consiste em obter os valores de a e p que minimizam a expres-
sao:
s = L e? = Z {yi - (a + ^ ) } (11.9)
.3
que pode ser feito igualando as derivadas parciais a zero, ou seja:
(11.10)
da
resultando nas seguintes estimativas para a e p, as quais chamaremos de a e b,
respectivamente:4
b = ( í i .i i )
(11.12)
onde (xi, yi), (x2, y 2), (x ^ y j é a amostra efetivamente observada.
A chamada equação (reta) de regressão é dada por
y = a + bx (11.13)
Para cada valor x, (i = 1, 2,..., n), temos, pela equação de regressão, o va­
lor predito:
y ,. = a + òx, (11.14)
A diferença entre os valores observados e os preditos é chamada de resíduo:
(11.15)
el = y í - y l
3 Pode-se mostrar que a segunda derivada é negativa, acarretando que a solução encon­
trada é realmente um ponto de mínimo da função (11.9).
4 É possível mostrar que os estimadores associados às estimativas a e b são não viciados
e os mais eficientes, dentre as possíveis relações lineares com as observações de Y.

3 2 8 ESTATÍSTICA
e 5[ = a + bx
O resíduo relativo à i-ésima observação (e,) pode ser
considerado uma estimativa do erro aleatório (s,) desta ob­
servação (veja ilustração ao lado).
Exemplo 11.2 (continuação)
Tabela 11.1 Dados do experimento e cálculos intermediários para obter a equa­
ção de regressão.
Cálculos
Dados
interm ediários
Ensaio (i) Xi yi x 2 Xí Yí
1 1 80,5 1 80,5
2 2 81,6 4 163,2
3 3 82,1 9 246,3
4 4 83,7 16 334,8
5 5 83,9 25 419,5
6 6 85,0 36 510,0
Soma 21 496,8 91 1.754,3
b , 6 (1 7 5 4 ,3)-(2 1) (496.8) , 9 ^ , ^
6•(91) - (21)2 105
n 496,8 -(0 ,8 8 6 ) -(21) _
Assim, temos a seguinte reta de regressão:
y = 79,7 + (0,886)*
Para traçar a reta no plano, basta atribuir dois valores para x e calcular os
correspondentes valores de y (veja a Figura 11.6).

CORRELAÇÃO E REGRESSÃO 3 2 9
Quantidade de aditivo (%)
Figura 11.6 Diagrama de dispersão dos dados do Exemplo 11.2 e a reta de re­
gressão ajustada a esses dados.
A partir dos seis ensaios experimentais, construímos um modelo, o qual nos
permite predizer o índice de octanagem da gasolina (y) a partir de uma quanti­
dade do novo aditivo (x).5 Por exemplo, se for adicionado x = 5,5% de aditivo,
esperamos um índice de octanagem de y = 79,7 + (0,886).(5,5) = 84,573. A
Tabela 11.2 mostra que os valores preditos pelo modelo estão bastante próxi­
mos dos valores observados no experimento.
Tabela 11.2 Valores preditos [y. = 79,7 + (0,886)^] e resíduos (e, = y - y.).
A
*i y* 9i
1 80,5 80,586 - 0,086
2 81,6 81,472 0,128
3 82,1 82,358 - 0,258
4 83,7 83,244 0,456
5 83,9 84,130 - 0,230
6 85,0 85,016 - 0,016
O coeficiente b fornece uma estimativa da variação esperada de Y, a partir
da variação de uma unidade em X. O sinal deste coeficiente indica o sentido da
variação. No exemplo, podemos dizer: a cada 1% a mais do novo aditivo, espe­
ramos um aumento de 0,886 no índice de octanagem.
5 Ressaltamos que o modelo só deve ser usado para realizar predições no intervalo de X
ensaiado (de 1 a 6% de aditivo), pois não há informação sobre o relacionamento entre X e Y fora
deste intervalo.

3 3 0 ESTATÍSTICA
11.3.2 Análise de variância do modelo
Se X não influencia 7, então o valor esperado de Y pode ser estimado sim­
plesmente pela média aritmética (y) das observações de Y. Mas se existe in­
fluência de X sobre Y, então deve haver algum ganho em considerar a equação
de regressão (y = a + bx). Este ganho pode ser avaliado ao comparar os resíduos
nas duas situações (Figura 11.7).
Figura 11.7 Ilustração de resíduos em relação à média aritmética (dt = y t -y ) e
à equação de regressão (e, = yt - y j .
Para i = 1, 2, ..., n, sejam:
a)
y, - y (desvios em relação à média aritmética - não levam em consi­
deração a relação entre Y e X);
b) y,
- y, (desvios em relação aos valores preditos pela equação de re­
gressão - consideram uma relação linear entre Y e X);
c)
y, - y (desvios dos valores preditos em relação à média aritmética).
Veja a Figura 11.8.
a ) y - y b) y, -9, c )? i-y
/
A
l x
J
---------------- ►
Figura 11.8 Ilustração dos desvios numa situação hipotética.

CORRELAÇÃO E REGRESSÃO 3 3 1
As somas dos quadrados dos desvios satisfazem à seguinte equação:
Z O . - y ) 2 = Z O i - y ) ' + Z ( ^ - y , ) 2 C11-16)
variação total variação variação não
explicada explicada
pela equação
de regressão
Chamaremos de coeficiente de determinação a seguinte razão:
Z Q . - y ) 2 variação explicada
= -------------------------v = --------------------------------------
“ y ) variação total
O coeficiente de determinação é uma medida descritiva da proporção da
variação de Y que pode ser explicada por variações em X, segundo o modelo es­
pecificado.
Exemplo 11.2 (continuação)
*í Yi y ?,• y*-y Yi - ?i f t - y (Yi - y)2 (y, - í g 2 íft - y)2
1 80,5 82,8 80,59 -2,3 -0,09 -2,21 5,29 0,01 4,90
2 81,6 82,8 81,47 -1,2 0,13 - 1,33 1,44 0,02 1,77
3 82,1 82,8 82,36 -0,7 -0,26 - 0,44 0,49 0,07 0,20
4 83,7 82,8 83,24 0,9 0,46 0,44 0,81 0,21 0,20
5 83,9 82,8 84,13 1,1 -0,23 1,33 1,21 0,05 1,77
6 85,0 82,8 85,01 2,2 - 0,01 2,21 4,84 0,00 4,90
Soma de Quadrados: 14,08 0,35 13,73
Coeficiente de determinação:
R z2 = 13,73 = 0 975 = 9 %
14,08
Em termos dos 6 ensaios realizados, a variância da octanagem da gasoli­
na é explicada, em parte, pela variação da quantidade de aditivo adicionado
(R2 = 97,5% de explicação) e em parte (1 - R2 = 2,5%) devido a outros fatores
intervenientes no processo.

3 3 2 ESTATÍSTICA
No caso do modelo de regressão linear simples, R2 coincide, numericamen­
te, com o quadrado do coeficiente de correlação r de Pearson, estudado na se­
ção 11.2.
Processo simplificado de cálculo
Soma de quadrados totais (corrigida pela média aritmética):
(11.18)
Soma de quadrados do erro ou soma de quadrados dos resíduos:
(11.19)
Soma de quadrados da regressão:
(11.20)
Coeficiente de determinação:
r 2 _ s q k _ 1 _ sqe
(11.21)
SQT SQT
O leitor poderá refazer os cálculos do Exemplo 11.2 com as expressões
(11.18) a (11.21). Os resultados devem ser os mesmos encontrados anterior­
mente.
Cada soma de quadrados está associada a certo número de graus de liber­
dade. Os desvios de cada observação em relação às estimativas de £{Y} têm
graus de liberdade iguais a n subtraído do número de parâmetros estimados em
£{Y}. Assim, os desvios y, - y têm n - 1 graus de liberdade; e os desvios y t - y 2
têm n - 2 graus de liberdade.
A soma de quadrados dividida pelo correspondente grau de liberdade for­
nece o quadrado médio ou variância. E a razão entre o quadrado médio da regres­
são e o quadrado médio do erro resulta na chamada razão F (veja Tabela 11.3).

CORRELAÇÃO E REGRESSÃO 3 3 3
Tabela 11.3 Análise de variância (Anova) da regressão linear simples.
Fonte de _
SQ QM Razão F
variação *
Regressão 1 SQR = E(y< - y Y QMR = SQR x 11 1 l
i
Erro n - 2 SQE = £ ( y , - y , Y QME = SC*E/ n _ 2
Total n - 1 SQT = 'Z ( y i - ? ) 2 QMT = SQ-T/ n _ 1
Exemplo 11.2 (continuação) Tabela da Anova:
Fonte de
gl SQ MQ Razão F
variação
Regressão 1 13,73 13,729 156,26
Erro 4 0,35 0,088
Total 5 14,08
11.3.3 Inferências sobre o modelo de regressão
Com respeito ao Exemplo 11.2, se fizéssemos outro experimento sob as
mesmas condições e com os mesmos valores de X, não deveríamos encontrar
exatamente os mesmos seis valores de Y descritos no Exemplo 11.2, porque o
erro experimental deverá estar presente no processo. Porém, se o experimento
for bem controlado, deveremos encontrar valores bastante próximos e, conse­
quentemente, uma reta de regressão também bastante próxima da encontrada
anteriormente.
Podemos imaginar que existe uma equação de regressão verdadeira, a qual
poderia ser obtida se pudéssemos realizar o experimento com infinitos ensaios.
Possíveis amostras de (X, Y) devem seguir, aproximadamente, o comportamen­
to da equação de regressão verdadeira, de tal forma que a variação dos pontos
em torno desta equação pode ser caracterizada por uma distribuição de proba­
bilidades, conforme mostra a Figura 11.9.

3 3 4 ESTATÍSTICA
Figura 11.9 Ilustração da distribuição de probabilidades em torno da verdadeira
regressão.
Suposições do modelo
Considerando novamente o modelo de regressão linear simples:
Yt = a + + £j (11.22)
vamos supor:
1) os termos de erro (e1? s2, e „ ) são variáveis aleatórias independentes;
2) £{£,} = 0;
3) V{e,} = o2; e
4) e, tem distribuição normal (i = 1, 2, n).
A primeira suposição exige que o i-ésimo ensaio (ou observação) não seja
afetado pelos ensaios (ou observações) anteriores; a segunda exige que a esco­
lha da forma da equação da média do processo - no caso, uma reta - deve ser
correta; a terceira exige que a variação aleatória não se altere ao longo das ob­
servações; e a quarta aponta para uma forma particular de distribuição dos ter­
mos aleatórios. Na Seção 11.3.4, estudaremos como verificar a validade dessas
suposições.
Teste de signifícância do modelo
Com as suposições (1) - (4) é possível testar formalmente se o modelo de
regressão propicia ganhos significativos em relação à utilização da média arit­
mética simples, na estimação de E{Y}. Considerando o modelo
E{Y} = ct + p .X (11.23)
formulamos as hipóteses
H0: p = 0 e Hii p * 0

CORRELAÇÃO E REGRESSÃO 3 3 5
Note que, sob H0, o valor esperado de Y (a média do processo) não é afeta­
do por X. Esse teste pode ser realizado através da razão F, que, sob H0 e as su­
posições (1) - (4), tem distribuição F com gl = 1 no numerador e gl = n - 2 no
denominador.
No Exemplo 11.2, temos gl = 1 no numerador e gl = 4 no denominador.
Para o nível de significância de 5%, a Tabela 6 do Apêndice fornece o valor crí­
tic o / = 7,71. Como / = 156,26 > / c = 7,71, o teste rejeita H0, indicando que o
modelo de regressão propicia ganhos significativos em relação à simples utiliza­
ção da média aritmética dos valores de 7, na avaliação da média do processo.
Inferência sobre o coeficiente angular
A grandeza
sc = VQMÊ = J IÕ L (11.24)
xn - 2
ou, de forma mais operacional,
i X y f
(11.25)
V n - 2
corresponde ao desvio padrão dos resíduos, ou seja, uma estimativa do desvio
padrão do erro aleatório, a. A partir de (11.25), podemos ter uma estimativa do
erro padrão de b por
n
Su = s, (11.26)
e testar as hipóteses do tipo H0: (3 = p0 vs. Him. P * p0 (Po é uma constante es­
pecificada), calculando
(11.27)
e comparando com o valor tabelado tc da distribuição t (Tabela 4 do apêndi­
ce) com gl = - 2. Se Po = 0, este teste é equivalente ao teste F visto anterior­
ti
mente.6
6 O teste também pode ser unilateral, mas alertamos que a maioria dos pacotes compu­
tacionais apresenta o valor p associado a um teste bilateral.

3 3 6 ESTATÍSTICA
Dado certo nível de confiança y, podemos obter na Tabela 4 o valor corres­
pondente de ty, com gl = n - 2, e construir um intervalo de confiança para p por
JC(P, y) = b ± t.r sb (11.28)
Inferência sobre o coeficiente escalar
Uma estimativa do erro padrão de a é dada por
(11.29)
Para testar H0: a = ct0 vs. Hx: a * a 0 (a0 é uma constante especificada),
calcula-se:
(11.30)
e compara com o valor crítico tc, obtido na Tabela 4, com gl = n - 2. Em espe­
cial, se for adotado 0^ = 0, este teste avalia se é razoável supor que a reta de
regressão passe pela origem.
Podemos obter um intervalo de confiança para a por
JC(a, y) = a ± tf • sc (11.31)
onde £, é obtido na Tabela 4, em função do nível de confiança y estabelecido e
dos graus de liberdade (gl = n - 2).
Uso do com putador
Exemplo 11.3 O anexo deste capítulo contém dados relativos à venda de 142
automóveis seminovos, incluindo o modelo, o preço de revenda (RS), o preço
do modelo novo (R$), o tempo de uso (anos completos) e a quilometragem.
O preço de venda de um carro seminovo depende do preço do mesmo mo­
delo 0 km. Assim, procuramos estabelecer um modelo de regressão entre o pre­

CORRELAÇÃO E REGRESSÃO 3 3 7
ço de revenda (Y) e o preço do correspondente modelo 0 km 00- Usando a pla­
nilha Excel, obtivemos os seguintes resultados:7
Estatística de regressão
R múltiplo 0,889
R-quadrado 0,791
R-quadrado ajustado 0,789
Erro padrão 1778,484
Observações 142
ANOVA
SQ gl QM F Valor p
Regressão 1,67E + 09 1 l,67E+09 528,5782 2,22E-49
Resíduo (erro) 4,43E + 08 140 3163004
Total 2,11E + 09 141
Coefi­ Erro Inferior Superior
Estât, t Valor-p
cientes padrão 95,0% 95,0%
Interseção 2654,11 431,22 6,155 7,46E-09 1801,56 3.506,67
Valor novo 0,476 0,021 22,991 2,22E-49 0,43 0,52
A primeira tabela de resultados mostra algumas estatísticas e, em particu­
lar, o R2 CR-quadrado) igual a 0,791. Este resultado indica que, na amostra ob­
servada, cerca de 79% da variação do preço de revenda pode ser explicada por
uma relação linear com o preço do automóvel 0 km. Os demais 21% podem ser
considerados como a variação provocada por outros fatores não considerados
no modelo de regressão.
O R-múltiplo, no caso de regressão linear simples, corresponde ao Coeficien­
te de Correlação de Pearson. O erro padrão (se) já foi apresentado anteriormen­
te e R2 ajustado não será tratado neste texto.
A segunda tabela apresenta a análise de variância (Anova) do modelo. Te­
m os:/ = 528 [valor p = (2,22).IO-49], indicando que o valor do carro novo (X)
é significativo para explicar o preço do carro seminovo (7).
7 Para fazer uma análise de regressão no Excel, é necessário instalar as Ferramentas de
Análise (ferramentas -> suplementos) e, depois, proceder a análise (ferramentas -> análise de da­
dos -> regressão). Nas tabelas de resultados apresentadas neste texto, alguns termos foram ade­
quados de acordo com nossa terminologia.

3 3 8 ESTATÍSTICA
A primeira coluna da terceira tabela apresenta as estimativas dos coeficien­
tes, donde, no presente exemplo, temos a seguinte equação de predição para o
preço de revenda (Y), em função do preço do automóvel novo (X):
y = 2654,11 + (0,476)*
ou seja, tendo o preço de um particular carro novo, x, podemos obter uma pre­
dição para o preço de revenda, y. Por exemplo, um modelo no qual o preço de
novo é R$ 16.000,00 tem preço de revenda, predito pelo modelo, de
y = 2654,11 + (0,476) (16000) = 10270
ou seja, R$ 10.270,00.
Com a equação de regressão, observamos, também, que, a cada real de di­
ferença no carro novo, esperamos uma diferença de 0,476 reais na revenda.8
A última tabela também fornece os resultados de testes estatísticos sobre
cada um dos parâmetros do modelo. As duas últimas colunas desta tabela apre­
sentam um intervalo de 95% de confiança para os dois parâmetros do modelo
(o intercepto a e a inclinação P).
11.3.4 Análise dos resíduos
Na seção anterior, estabelecemos um modelo para um conjunto de obser­
vações (*!, y j , (x2, y2), (*n> y ti), relativo às variáveis X e Y, da forma
Yi = a + px{ + Si (11.32)
onde: Yt é a variável aleatória associada à i-ésima observação de Y;
8- é o erro aleatório da i-ésima observação; e
a e p são parâmetros a serem estimados com os dados.
Assim, estamos assumindo que X causa Y através de uma relação linear, e
toda a variação em torno dessa relação deve-se ao efeito (erro) aleatório. Além
disso, para a validade dos intervalos de confiança e testes estatísticos, é neces­
sário supor que as observações de Y sejam independentes, e o termo de erro te­
nha distribuição normal, com média nula e variância constante. Apresentare­
mos um processo gráfico para verificar se estas suposições podem ser válidas e,
caso contrário, o que pode ser feito para corrigir as distorções.
8 É claro que um bom modelo para o preço de revenda deve levar em conta outros fato­
res, tais como a idade do veículo, estado de conservação etc. Na Seção 11.4 incluiremos novas va­
riáveis no modelo.

CORRELAÇÃO E REGRESSÃO 3 3 9
Um primeiro gráfico pode ser feito antes de se aplicar a análise de regres­
são. É o diagrama de dispersão, conforme discutido na Seção 11.1. Por esse
gráfico, podemos verificar se a função linear é adequada para representar a for­
ma estrutural entre X e Y. Veja o gráfico à esquerda da Figura 11.10.
Após a estimação dos parâmetros a e p, podemos calcular os resíduos, ou
seja,
ei = y i - y l {i= 1,2,..., n) (11.33)
Um gráfico apresentando os pares (x„ e,), que chamaremos de gráfico dos
resíduos, é bastante útil na avaliação do modelo de regressão. Veja o gráfico à
direita da Figura 11.10.
Figura 11.10 Gráficos indicando adequação do modelo.
Os gráficos da Figura 11.10 indicam uma situação onde as suposições do
modelo estão aparentemente satisfeitas, pois os resíduos apresentam-se distri­
buídos de forma aleatória em torno da reta de regressão. No gráfico dos resí­
duos, a reta de regressão corresponde à linha horizontal sobre o valor zero.9 Já
a Figura 11.11 apresenta uma situação onde existe um ponto discrepante. Esse
ponto é visível nos dois gráficos, mas no gráfico dos resíduos ele aparece mais
nitidamente.
'k resíduo (e)
0
• •
Figura 11.11 Gráficos indicando a presença de um valor discrepante.
9 O gráfico de probabilidade normal (Seção 6.5) também poderia ser aplicado aos resí­
duos para verificar a adequação da distribuição normal.

3 4 0 ESTATÍSTICA
A Figura 11.11 mostra como um ponto discrepante pode forçar uma incli­
nação na reta, sugerindo uma tendência não compatível com as demais obser­
vações. Esse problema surge, principalmente, quando se tem uma amostra de
observações pequena e o ponto discrepante estiver numa das extremidades do
intervalo de observação de X. É prudente, nesse caso, buscar a razão da existên­
cia do ponto discrepante. Se sua causa for algum erro, alguma falha no experi­
mento ou, ainda, puder ser considerada como uma situação atípica, devemos
efetuar nova análise sem essa observação discrepante.
11.3.5 Transformações
Quando se trata de um estudo experimental, a variável X costuma ser esta­
belecida. Por exemplo, num estudo para verificar a relação entre o tempo de
cozimento (X) e a maciez (7) de um alimento, podemos estabelecer diferentes
tempos de cozimento e verificar o resultado Y. Nos casos em que temos contro­
le sobre a variável X, podemos variá-la uniformemente sobre o intervalo de es­
tudo. Por exemplo, se pretendemos fazer a análise entre 20 e 30 minutos de co­
zimento, podemos fazer ensaios com os tempos de cozimentos 20, 21, 22, ... e
30 minutos.
Em estudos de levantamento, normalmente X e Y são observadas, sendo
comum ocorrer uma distribuição assimétrica de valores de X. Por exemplo, con­
sidere o problema de se avaliar a relação entre renda (X) e consumo (Y). A
maioria dos indivíduos tem renda baixa e, consequentemente, tende a consumir
pouco, provocando distribuições assimétricas para X e Y. Nesta situação, os da­
dos devem distribuir-se conforme mostra a Figura 11.12.
frequência frequência
Í~ H t~ y
x y
x
X
Figura 11.12 Gráficos indicando distribuições assimétricas de X e Y, além da va­
riância de Y aumentar proporcionalmente com X.

CORRELAÇÃO E REGRESSÃO 3 4 1
Em situações como indicado na Figura 11.12, os valores grandes de X vão
ter mais peso na determinação da inclinação da reta. Neste caso, recomenda­
mos a aplicação da transformação logarítmica tanto nos valores de X como nos
valores de 7, estabelecendo o seguinte modelo:10
logOO = a + p logOq) + St (11.34)
A transformação logarítmica aumenta as distâncias entre os valores peque­
nos e reduz as distâncias entre os valores grandes, tomando distribuições com
assimetria positiva (cauda mais longa à direita) em distribuições aproximada­
mente simétricas. Com isso, temos uma situação mais adequada para estabele­
cer a reta de regressão. Em termos computacionais, devemos:
a) calcular o logaritmo natural de cada valor xt e de cada valor y t;
b) aplicar a análise de regressão linear sobre os dados transformados
[logfo), logC/i)]; e
c) construir novamente o gráfico de resíduos para verificar a adequa­
ção das suposições nesse novo modelo.
Na Equação 11.34, depois de estimados os parâmetros a e p por a e ò, res­
pectivamente, podemos aplicar a transformação inversa, resultando em
y = ea + b' l0*(x) (11.35)
A Figura 11.13 apresenta uma situação que sugere relação não linear, com
Y crescendo rapidamente para valores pequenos de X e crescendo lentamente
para valores grandes de X. É uma situação típica onde se recomenda uma trans­
formação logarítmica somente nos valores da variável X, ou seja, passamos a
considerar o seguinte modelo para os dados:
y = a + p logQc;) + e* (11.36)
Note que o modelo (11.33) pode ser considerado linear em termos das va­
riáveis logOc;) ey, (mas não mais entre xt e y ). Em termos computacionais, de­
vemos:
a) calcular o logaritmo de cada valor
b) aplicar a análise de regressão linear sobre os dados (logfo), y ); e
c) construir novamente o gráfico de resíduos para verificar a adequa­
ção das suposições nesse novo modelo.
10 É comum usar o logaritmo natural ou na base 10. Outra transformação que se presta
ao mesmo propósito é a raiz quadrada. Esta segunda transformação é usada nas situações em que
a inadequação do modelo não aparece de forma tão forte como visto na Figura 11.10. Observa­
mos que estas transformações são possíveis somente quando todos os valores são positivos.

3 4 2 ESTATÍSTICA
0
Figura 11.13 Gráficos indicando uma relação não linear, aparentemente logarít­
mica.
A Figura 11.14 sugere os seguintes problemas: (1) relação não linear e (2)
aumento da variância à medida que X aumenta. Em casos assim, recomenda­
mos uma transformação logarítmica nos valores da variável Y, ajustando o se­
guinte modelo aos dados:
logOi) = a + fbCi + Ei (11.37)
Ou seja,
a) calcula-se o logaritmo de cada valor y t;
b) aplica-se a análise de regressão linear sobre os dados (xt, /og(y£)); e
c) refaz-se novamente o gráfico de resíduos para verificar se o novo
modelo é mais adequado aos dados.
0 • ••
Figura 11.14 Gráficos indicando uma relação não linear - aparentemente expo­
nencial - e variância não constante.
O uso de transformações auxilia o pesquisador a encontrar um modelo
mais adequado para os dados, ainda que utilizando as expressões da regressão
linear. A transformação logarítmica é muito usada por ter uma interpretação
prática interessante, pois transforma variações percentuais de mesma magnitu­
de em variações constantes. Por exemplo, se se considerar um aumento absolu­
to no salário de RS 100,00, seu significado vai ser muito diferente para quem

CORRELAÇÃO E REGRESSÃO 3 4 3
ganha R$ 100,00 do que para quem ganha R$ 1.000,00. Por isso, é mais co­
mum se ouvir falar em aumentos percentuais de salários. Um aumento de 10%
no salário representa um ganho de R$ 10,00 para quem ganha RS 100,00 e um
ganho de R$ 100,00 para quem ganha RS 1.000,00. Na escala logarítmica, es­
ses incrementos são iguais. Por essa razão, é muito comum usar a escala (ou
transformação) logarítmica em variáveis econômicas ou medidas de valor e ta­
manho em geral.
Exemplo 11.3 (continuação) Na seção anterior, construímos uma regressão
entre o preço de revenda de carros seminovos (7) e o preço do correspondente
modelo 0 km (X), considerando uma amostra de 142 automóveis apresentada
no anexo deste capítulo. A Figura 11.15 apresenta o diagrama de dispersão e o
gráfico dos resíduos desse modelo.
4000
3000 ♦
: l *♦ ♦ %
2000
Ü
1000
CO/l 0 i* U.
3
1000
3
2000
S/i
3000 • ♦
&
4000 S
5000
6000
7000
10000 15000 20000 25000 30000 35000
Valor do carro novo Valor do carro novo
Figura 11.15 Gráfico de dispersão com o ajuste da reta de regressão e gráfico dos
resíduos - Exemplo 11.3.
Observamos na Figura 11.15 que X só assume alguns determinados valo­
res. Isto porque os automóveis em estudo são de 7 modelos e, para cada mode­
lo, o preço 0 km é único. Por outro lado, não parece haver fortes violações nas
suposições do modelo de regressão, a não ser a ocorrência maior de valores pe­
quenos com respeito às duas variáveis, o que sugere tentarmos uma transfor­
mação logarítmica em X e em Y.
Realizamos a transformação logarítmica nos valores das duas variáveis e
refizemos a análise de regressão, contudo o R2 reduziu e o gráfico dos resíduos
apontou uma distribuição assimétrica, com cauda mais longa à esquerda. Em
função desses resultados, preferimos manter o modelo original. Na verdade, o
preço de um carro seminovo depende de vários outros fatores, levando a um
modelo de regressão múltipla, o qual discutiremos na próxima seção.

3 4 4 ESTATÍSTICA
EXERCÍCIOS
5. Um administrador de uma grande sorveteria anotou por um longo período
de tempo a temperatura média diária, em °C (X), e o volume de vendas diá­
rias de sorvete, em kg (7). Com os dados, foi ajustada a seguinte equação
de regressão:
y = 0,5 + l,8x, com R2 = 0,80
Pergunta-se:
a) Qual é o consumo esperado de sorvete num dia de 27°C?
b) Qual é o incremento esperado nas vendas de sorvete a cada 1°C de au­
mento da temperatura?
6 . No processo de queima de massa cerâmica, avaliou-se o efeito da tempera­
tura do forno (X) sobre a resistência mecânica da massa queimada (Y). Fo­
ram realizados 6 ensaios com níveis de temperatura equidistantes, os quais
designaremos por 1, 2, 3, 4, 5 e 6. Os valores obtidos de resistência mecâ­
nica (MPa) foram: 41, 42, 50, 53, 54, 60, respectivamente. Pede-se:
a) As estimativas de a e p da equação de regressão E(Y) = a + p*.
b) O coeficiente R2.
c) O desvio padrão dos resíduos, se.
d) O teste estatístico H0: p = 0
7. A tabela a seguir relaciona os pesos (em centenas de kg) e as taxas de
rendimento de combustível em rodovia (km/litro), numa amostra de 10
carros de passeio novos.
Peso 12 13 14 14 16 18 19 22 24 26
Rendimento 16 14 14 13 11 12 09 09 08 06
a) Calcule o coeficiente de correlação de Pearson.
b) Considerando o resultado do item (a), como você avalia o relaciona­
mento entre peso e rendimento, na amostra observada?
c) Para estabelecer uma equação de regressão, qual deve ser a variável
dependente e qual deve ser a variável independente? Justifique a sua
resposta.
d) Estabeleça a equação de regressão, considerando a resposta do item (c).
e) Apresente o diagrama de dispersão e a reta de regressão obtida em (d).

CORRELAÇÃO E REGRESSÃO 3 4 5
f) Você considera adequado o ajuste do modelo de regressão do item
(d)? Dê uma medida dessa adequação, interpretando-a.
g) Qual é o rendimento esperado para um carro de 2.000 kg? Justifique
sua resposta. Lembrete: os dados de peso na tabela estão em centenas
de kg.
h) Você considera seu estudo capaz de predizer o rendimento esperado
de um veículo com peso de 7.000 kg? Justifique sua resposta.
.
8 Para verificar a viabilidade de incluir os resíduos da queima de carvão mi­
neral na composição do cimento, foram feitos ensaios com cimento conten­
do de 0 a 9% de cinza de carvão; e medida a resistência à compressão (em
MPa), após 28 dias. Os resultados foram os seguintes:
Carvão (%): 0 1 2 3 4 5 6 7 8 9
Resistência (MPa): 38,5 40,2 42,1 37,5 41,1 36,9 38,2 36,7 39,5 35,9
a) Estabeleça a equação de regressão.
b) Calcule R2.
c) Teste se o coeficiente angular pode ser zero. Use a = 0,05.
d) Os resultados mostram evidência de que o uso de cinza de carvão mi­
neral na composição do cimento diminui a sua resistência aos 28 dias?
9. Um estudo foi desenvolvido para verificar o quanto o comprimento de um
cabo da porta serial de microcomputadores influencia na qualidade da
transmissão de dados, medida através do número de falhas em 100.000 lo­
tes de dados transmitidos (taxa de falha). Os resultados foram:
Comp. do cabo (m) 8 8 9 9 10 10 11 11 12
Taxa de falha 2,2 2,1 3,0 2,9 4,1 4,5 6,2 5,9 9,8
Comp. do cabo (m) 12 13 13 14 14 15
Taxa de falha 8,7 12,5 13,1 19,3 17,4 28,2
a) Estabeleça a equação (reta) de regressão.
b) Faça a análise dos resíduos e verifique se o modelo linear é adequado.
c) Qual é a transformação sugerida pelo gráfico dos resíduos?
d) Faça uma análise de regressão com os dados transformados.

3 4 6 ESTATÍSTICA
10. A partir de um levantamento de 397 apartamentos em Criciúma-SC, reali-
zou-se uma regressão entre área total (m2) e valor ($).n Como essas variá­
veis apresentavam uma distribuição de frequências muito assimétricas à di­
reita, foram feitas transformações logarítmicas em ambas as variáveis,
antes de proceder à regressão. O modelo ajustado aos dados foi:
logio (yalor) = 1,60 + (1,38) log10 (área) R2 = 0,89
Interprete o valor de R2 e o coeficiente 1,38.
11.4 INTRODUÇÃO À REGRESSÃO MÚLTIPLA
Em geral, uma variável dependente Y depende de várias variáveis indepen­
dentes (Xi, X2, ..., Xk). Na análise de regressão múltipla, procuramos construir
um modelo estatístico-matemático para se estudar, objetivamente, a relação en­
tre as variáveis independentes e a variável dependente e, a partir do modelo,
conhecer a influência de cada variável independente, como também, predizer a
variável dependente em função do conhecimento das variáveis independentes.
Veja o Quadro 11.2.
Quadro 11.2 Exemplos de aplicação da regressão linear múltipla.
Variáveis independentes ____ ^ Variável dependente
{X19 X 2i Xk)_____________________________ Y___________
X-, = renda (RS)
X2 = poupança (R$) - ► Y = consumo (R$)
X3 = taxa de juros (%)
X: = memória RAM (Gb) Y = tempo de resposta do
X2 = sistema operacional ------- ► sistema computacional
(segundos)
X3 = tipo de processador
X: = área construída do imóvel (m2)
X2 = padrão de qualidade (custo do m2, RS) ► ^ — novo°(R$)Um
X3 = localização________________________________________________________
X- = valor do modelo novo (R$)
X2 = quilometragem
Y = valor de revenda de carro
X3 = idade do veículo (anos) ------- 1
seminovo (R$)
X4 = estado de conservação
Xs = opcionais
11 Os exercícios 10 e 12 baseiam-se em dados extraídos da dissertação de mestrado de
Evelise C. Zancan, PPGEP/UFSC, 1995.

CORRELAÇÃO E REGRESSÃO 3 4 7
Para estabelecer o modelo clássico de regressão múltipla, suporemos que Y
seja uma variável quantitativa contínua e Xly X2, ..., Xk sejam variáveis quantita­
tivas ou indicadoras de certos atributos. A variável indicadora deve ter valor 1,
quando o atributo está presente; e 0, quando não está presente. Por exemplo, a
variável X4 = estado de conservação do veículo pode ter valor 1 quando o veículo
for considerado “bom” e 0 quando for considerado “ruim”.
Será suposto que Y é uma variável aleatória, isto é, somente será conheci­
da após a observação do elemento (indivíduo, carro etc.), enquanto Xlf X2, ...,
Xk também podem provir de observações ou serem estabelecidas a priori. Espe­
cificados os valores x lf x2,, ..., xk para as variáveis independentes, suporemos a
seguinte equação para o valor esperado de Y:
E{Y} = a + Pi*! + p2x2 + ... + PfcXjk (11.38)
A análise de regressão múltipla parte de um conjunto de observações (xn,
(xl2>x22,...,xk2, y 2) , ( x ln, x2n, ...,xkn,y n) relativas às variáveis Xu
X2, ..., Xk e Y. Diremos que uma dada observação Y depende, em parte, dos cor­
respondentes valores xv x2,..., xk e de uma infinidade de outros fatores, repre­
sentados pelo termo de erro, e. Mais especificamente, suporemos o seguinte
modelo para as observações:
Y, = a + PjX^- + P2x2í + ... + PfcXfc + 8, (£ = 1, 2, ..., n) (11.39)
onde a, Pj , p2, ... e p* são parâmetros a serem estimados com os dados e e, re­
presenta o efeito (erro) aleatório da i-ésima observação. As demais suposições
são análogas à regressão simples, acrescentando a suposição de que as variáveis
independentes X1} X2, ..., Xk não devem ter correlações altas entre si.
Exemplo 11.5 Considerando os dados de 142 automóveis (anexo), vamos
construir um modelo de regressão para tentar explicar Y = preço de revenda de
automóveis seminovos (em RS), em função de:
Xl = preço do correspondente modelo 0 km (em RS);
X2 = tempo de uso (em anos completos); e
X3 = quilometragem (em milhares de km).
Usando a planilha Excel, obtivemos os seguintes resultados:
Estatística de regressão
R múltiplo 0,961
R-Quadrado 0,923
R-quadrado ajustado 0,921
Erro padrão 1087
Observações 142

3 4 8 ESTATÍSTICA
ANOVA
gl SQ QM F Valor p
Regressão 3 1,95E + 09 6,51E+08 550,27 l,52E-76
Resíduo 138 1,63E + 08 1182186
Total 141 2,llE+09
Coefi­ Erro Inferior Superior
Estât t Valor p
cientes padrão 95,0% 95,0%
Interseção 6240,13 352,11 17,722 2,25E-37 5543,89 6936,36
Valor novo 0,48 0,01 37,448 3,61E-74 0,45 0,50
Tempo uso - 432,92 136,64 - 3,168 0,0019 - 703,10 - 162,75
Quilometragem -45,11 9,00 - 5,014 l,61E-06 - 62,90 - 27,32
Observamos, na primeira tabela, o valor de R2 (R-quadrado) igual a 0,923.
Este resultado indica que, na amostra observada, cerca de 92% da variação do
preço de revenda podem ser explicados por uma relação linear que envolve o
preço do automóvel 0 km (XJ, o tempo de uso (X2) e a quilometragem (X3).
Um resultado razoavelmente maior do que os 79,1%, que foi obtido quando
usamos apenas X} como variável independente (Exemplo 11.3).12
A segunda tabela (Anova) fornece o resultado estatístico da seguinte hipó­
tese nula:
Pi = P = ... = Pk = 0
Ho- 2
Pela hipótese H0, o conjunto de variáveis independentes em estudo não
tem poder de explicação sobre a variável dependente.13 A razão F resultou no
valor / = 550,27, com correspondente valor p = (1,52)10"76. Como o valor p é
extremamente pequeno, o teste estatístico rejeita H0, indicando que as variáveis
independentes escolhidas são significativas para explicar a variância de Y.
A terceira tabela fornece as estimativas dos coeficientes, incluindo interva­
los de confiança e testes estatísticos para cada particular coeficiente. A primeira
coluna apresenta as estimativas dos coeficientes. Assim, no presente exemplo,
temos a seguinte equação:
12 O cálculo do K* na regressão múltipla é análogo ao da regressão simples.
13 Cabe observar que o teste estatístico refere-se à população. Quando se tem uma amos­
tra muito pequena, pode-se obter um valor alto de R2 e o teste aceitar H0: p, = p2 = ... = p* = 0.

CORRELAÇÃO E REGRESSÃO 3 4 9
y = 6240 + 0,48*! - 433*2 - 45,1*3
Com essa equação, tendo para um particular carro usado o preço de novo
(*j), o tempo de uso (x2) e a quilometragem (x3), podemos obter uma predição
para o seu preço de revenda, y. Por exemplo, um modelo, cujo preço do carro
novo é RS 16.000,00, que tenha 2 anos de uso e 50 mil quilômetros rodados,
seu preço de revenda, predito pelo modelo, é
y = 6240 + (0,48) (16000) - (433) (2) - (45,1) (50) = 10779
ou seja, RS 10.779,00.
Com a equação de regressão, observamos, também, que a cada real de di­
ferença no carro novo, esperamos uma diferença de 48 centavos de reais na re­
venda (mantendo-se constantes o tempo de uso e a quilometragem). A cada
ano de envelhecimento do automóvel, esperamos RS 433,00 a menos na reven­
da (mantendo-se constantes o valor do carro novo e a quilometragem). E, tam­
bém, a cada 1.000 quilômetros rodados, esperamos R$ 45,11 a menos na re­
venda (mantendo-se constantes o valor de novo e o tempo de uso).14
A última tabela também fornece os resultados de testes estatísticos indivi­
duais, relativos a cada um dos coeficientes da equação de regressão. Ou seja,
temos os resultados dos quatro seguintes testes:
1. H0: a = 0;
2. H0: = 0;
3. H0: p2 = 0; e
4. tf0: P3 = 0.
Como em todos os quatro casos, os valores p foram inferiores ao nível de
significância usual de 0,05, rejeitamos as quatro hipóteses nulas, concluindo
que nenhuma das variáveis independentes pode ser excluída do modelo.
Assim como na regressão simples, podemos calcular os resíduos para verifi­
car a adequação do modelo de regressão. Calculamos, inicialmente, os valores
preditos, y, associados a cada conjunto de valores (xl} x2, ..., xk) usado na análi­
14 Dois comentários são pertinentes no momento:
a) É sabido que a desvalorização do automóvel não é linear com o tempo de uso. Uma
transformação logarítmica em Y deve tornar o modelo mais realista.
b) As variáveis independentes, nessa aplicação, são correlacionadas. Por exemplo, um auto­
móvel mais velho deve ter maior quilometragem. Logo, a interpretação “mantendo as demais va­
riáveis constantes” pode ficar prejudicada. Além disso, os valores dos coeficientes das variáveis
independentes correlacionadas não são bem estimados (observe a magnitude dos intervalos de
confiança nas duas últimas colunas da terceira tabela).

3 5 0 ESTATÍSTICA
se. No exemplo dos automóveis, os valores preditos são calculados pela equa­
ção y = 6240 + 0,48*! - 433x2 - 45,lx3, com x lf x2 e x3 associados a cada um
dos 142 automóveis avaliados. Os resíduos são obtidos através da diferença en­
tre os valores observados e os valores preditos, isto é
ei = Yi ~ y t 0 = 1,2, n) (11.40)
Os resíduos podem ser apresentados num diagrama de dispersão com cada
variável independente ou com os valores preditos, os quais correspondem a
uma combinação linear das variáveis independentes. A Figura 11.16 apresenta
o diagrama de dispersão dos pares ordenados (y if et).
Valores preditos
Figura 11.16 Gráfico dos resíduos com os valores preditos.
A análise do gráfico de resíduos (Figura 11.16) mostra um certo padrão.
Para valores preditos pequenos, os resíduos tendem a ser positivos, depois eles
tendem a ser negativos e, para valores preditos grandes, eles tendem a ser posi­
tivos de novo. Além disso, observamos que a dispersão aumenta para os valores
preditos maiores. Conforme visto na seção anterior, essas características suge­
rem a aplicação de uma transformação logarítmica na variável dependente.
Raciocinando em termos da relação entre tempo de uso (X2) e o valor do
automóvel (Y), é mais natural considerar que a cada ano de uso, o automóvel
tenha uma redução percentual do seu valor, reforçando a transformação sugeri­
da pelo gráfico dos resíduos. A construção de um modelo mais adequado para
esses dados é deixada para o leitor.

CORRELAÇÃO E REGRESSÃO 3 5 1
EXERCÍCIOS
11. Com o auxílio de um computador, refaça o Exemplo 13.7, mas consideran­
do como variável dependente o log(y), onde Y = valor de revenda do auto­
móvel. Observe o gráfico dos resíduos. Exclua as três observações que apa­
recem como discrepantes. Refaça novamente a análise.
12. Considerando novamente os dados de 397 apartamentos em Criciúma, rea-
lizou-se uma regressão múltipla, onde Y = log10(valor em $), Xx = idade
(em anos), X2 = gasto com energia elétrica dos moradores do apartamento
(kw), X3 = log10(área em m2) e X4 = local (1 = centro e bairros nobres,
0 = outros bairros). A equação ajustada, com R2 = 0,92, foi:
7 = 1,982 - (0,0073)*! - (0,0002)X2 + (1,228)X3 + (0,108)X4
(p < 0,01) (p = 0,30) (p < 0,01) (p < 0,01)
Os valores p abaixo da equação estão associados aos testes de signi-
ficância de cada coeficiente. Esses testes indicam que alguma variável
pode ser excluída do modelo sem prejuízos? Interprete os coeficientes
significativos.
ANEXO
Os dados que seguem foram coletados em 2001, pelo Prof. Manoel R.
Lino, do Departamento de Informática e Estatística - UFSC, e fornecem infor­
mações sobre a venda de 142 automóveis seminovos, incluindo o modelo, o pre­
ço de revenda (R$), o preço do modelo novo (R$), o tempo de uso do automó­
vel (anos completos) e a quilometragem.
Preço Preço Tempo Preço Preço Tempo
Auto Modelo Km Auto Modelo Km
de rev. novo de uso de rev. novo de uso
1 Mille 4.890 12.081 5 98 72 Gol 10.340 15.945 3 39
2 Mille 5.604 12.081 5 88 73 Gol 9.680 15.945 3 39
3 Mille 7.820 12.081 4 73 74 Gol 11.640 15.945 2 39
4 Mille 7.320 12.081 4 65 75 Gol 11.350 15.945 2 36
5 Mille 8.100 12.081 4 62 76 Gol 11.380 15.945 2 36
6 Mille 7.590 12.081 4 59 77 Gol 12.050 15.945 2 32
7 Mille 8.950 12.081 3 61 78 Gol 11.430 15.945 2 18

3 5 2 ESTATÍSTICA
Preço Preço Tempo Preço Preço Tempo
Auto Modelo Km Auto Modelo Km
de rev. novo de uso de rev. novo de uso
8 Mille 8.590 12.081 3 42 79 Gol 12.570 15.945 1 38
9 Mille 8.530 12.081 3 38 80 Gol 12.040 15.945 1 20
10 Mille 9.040 12.081 2 50 81 Gol 12.580 15.945 1 11
11 Mille 8.790 12.081 2 41 82 Fiorino 7.270 16.711 5 92
12 Mille 9.200 12.081 2 38 83 Fiorino 8.790 16.711 5 72
13 Mille 10.240 12.081 1 19 84 Fiorino 9.510 16.711 4 75
14 Mille 10.560 12.081 1 12 85 Fiorino 8.659 16.711 4 69
15 Fiesta 5.500 13.050 5 90 86 Fiorino 9.660 16.711 4 66
16 Fiesta 7.780 13.050 5 75 87 Fiorino 9.870 16.711 3 57
17 Fiesta 7.850 13.050 5 64 88 Fiorino 9.749 16.711 3 50
18 Fiesta 7.900 13.050 5 60 89 Fiorino 9.340 16.711 3 48
19 Fiesta 7.980 13.050 5 60 90 Fiorino 9.643 16.711 3 45
20 Fiesta 9.450 13.050 4 63 91 Fiorino 11.230 16.711 2 46
21 Fiesta 9.040 13.050 4 56 92 Fiorino 9.970 16.711 2 42
22 Fiesta 8.900 13.050 4 45 93 Fiorino 10.900 16.711 2 37
23 Fiesta 8.970 13.050 4 45 94 Fiorino 10.589 16.711 2 30
24 Fiesta 9.990 13.050 3 48 95 Fiorino 12.910 16.711 1 22
25 Fiesta 10.150 13.050 3 44 96 Fiorino 12.830 16.711 1 17
26 Fiesta 9.150 13.050 3 36 97 Parati 12.000 28.137 5 99
27 Fiesta 10.200 13.050 3 33 98 Parati 11.880 28.137 5 85
28 Fiesta 10.530 13.050 2 52 99 Parati 10.590 28.137 4 82
29 Fiesta 10.900 13.050 2 47 100 Parati 12.280 28.137 4 67
30 Fiesta 11.200 13.050 2 45 101 Parati 14.410 28.137 4 60
31 Fiesta 9.680 13.050 2 23 102 Parati 14.580 28.137 4 54
32 Fiesta 10.200 13.050 2 15 103 Parati 15.750 28.137 4 48
33 Fiesta 9.580 13.050 1 27 104 Parati 14.960 28.137 3 53
34 Fiesta 9.980 13.050 1 16 105 Parati 18.340 28.137 3 48
35 Fiesta 10.050 13.050 1 12 106 Parati 14.580 28.137 3 46

CORRELAÇÃO E REGRESSÃO 3 5 3
Preço Preço Tempo Preço Preço Tempo
Auto Modelo Km Auto Modelo Km
de rev. novo de uso de rev. novo de uso
36 Corsa 8.450 15.337 5 75 107 Parati 17.200 28.137 3 39
37 Corsa 8.120 15.337 5 69 108 Parati 12.680 28.137 2 60
38 Corsa 8.680 15.337 5 65 109 Parati 17.020 28.137 2 39
39 Corsa 8.900 15.337 5 56 110 Parati 16.800 28.137 2 37
40 Corsa 9.200 15.337 4 78 111 Parati 16.800 28.137 2 37
41 Corsa 8.960 15.337 4 65 112 Parati 15.680 28.137 2 29
42 Corsa 9.350 15.337 4 62 113 Parati 18.360 28.137 1 32
43 Corsa 9.180 15.337 4 59 114 Parati 18.960 28.137 1 18
44 Corsa 9.260 15.337 4 59 115 Parati 17.090 28.137 1 18
45 Corsa 9.250 15.337 4 56 116 Escort 11.050 28.168 5 94
46 Corsa 9.680 15.337 3 75 117 Escort 10.480 28.168 5 82
47 Corsa 10.100 15.337 3 60 118 Escort 13.650 28.168 5 68
48 Corsa 9.950 15.337 3 59 119 Escort 12.800 28.168 4 85
49 Corsa 9.580 15.337 3 57 120 Escort 16.570 28.168 4 72
50 Corsa 9.460 15.337 3 48 121 Escort 16.400 28.168 4 55
51 Corsa 10.900 15.337 2 49 122 Escort 16.950 28.168 3 60
52 Corsa 11.200 15.337 2 36 123 Escort 16.860 28.168 3 47
53 Corsa 10.750 15.337 2 36 124 Escort 17.050 28.168 3 47
54 Corsa 12.050 15.337 2 33 125 Escort 18.120 28.168 2 44
55 Corsa 12.350 15.337 1 40 126 Escort 18.900 28.168 2 37
56 Corsa 11.640 15.337 1 23 127 Escort 18.280 28.168 1 26
57 Corsa 11.400 15.337 1 22 128 Escort 17.400 28.168 1 25
58 Gol 9.200 15.945 5 75 129 Vectra 18.830 32.995 5 75
59 Gol 9.340 15.945 5 75 130 Vectra 18.120 32.995 5 68
60 Gol 9.000 15.945 5 68 131 Vectra 15.490 32.995 4 80
61 Gol 9.340 15.945 5 45 132 Vectra 17.600 32.995 4 54
62 Gol 9.450 15.945 4 78 133 Vectra 17.050 32.995 4 47
63 Gol 9.680 15.945 4 69 134 Vectra 19.800 32.995 3 63

3 5 4 ESTATÍSTICA
Preço Preço Tempo Preço Preço Tempo
Auto Modelo Km Auto Modelo Km
de rev. novo de uso de rev. novo de uso
64 Gol 9.920 15.945 4 62 135 Vectra 20.300 32.995 3 58
65 Gol 0.320 15.945 4 59 136 Vectra 20.500 32.995 3 49
66 Gol 9.950 15.945 4 58 137 Vectra 19.880 32.995 3 43
67 Gol 9.680 15.945 4 55 138 Vectra 21.050 32.995 2 40
68 Gol 10.500 15.945 3 63 139 Vectra 20.810 32.995 2 36
69 Gol 10.860 15.945 3 50 140 Vectra 19.400 32.995 2 29
70 Gol 10.780 15.945 3 50 141 Vectra 21.500 32.995 1 28
71 Gol 10.560 15.945 3 43 142 Vectra 21.440 32.995 1 19
RESPOSTAS DE EXERCÍCIOS
CAPÍTULO 1
3. a) 6,5 b) 3,5 c) 1,87
4. As empacotadoras A e B aparentam estar calibradas, pois enchem os paco­
tes de café, em média, com o peso declarado; contudo a variância relativa­
mente alta para a empacotadora B sugere que os pacotes de café provindos
desta empacotadora têm pesos muito diferentes entre eles - falta de unifor­
midade no produto. A empacotadora C aparenta estar descalibrada.
5. Os valores são todos iguais.
CAPÍTULO 2
1. {José da Silva, Bartolomeu, Arnaldo, Geraldo, Joana, Aristóteles}
2. {S, B, L, C}
3. Não, basta extrair 100 números da tabela, com quatro algarismos, perten­
centes ao conjunto {1.650, 1.651, ..., 8.840}, sem repetição.
9. sl = 0,02687 com 8 graus de liberdade.
11. a) ef(A) = 13,65, e/(B) = 3,72, e/(C) = 14,72, e/(D) = 7,03, ef(E) =
= - 0,15 e ef(F) = - 2,41.

RESPOSTAS DE EXERCÍCIOS 3 5 5
Os fatores A, C e D são os que alteram mais o nível médio da resposta.
Maior volume específico é obtido com A, C e D em seus níveis superiores.
b) e/(A) = 6,80, e/(B) = 0,33, e/(C) = 2,77, e/CD) = - 3,59, e/(£) = - 2,07
e e/(F) = - 3,78.
O fator A provoca maior alteração na variabilidade da resposta. Menor
variabilidade é obtida no nível inferior de A.
CAPÍTULO 3
3. a) 7,6 b) 2,37
4. 0,944 e 1,047
5. md = 74,8; qt = 74,3; qs = 75,875
8. d) c = 1: x = 5,54 e s = 0,50;
C = 4: x = 9,92 e s = 0,73;
C = 8: x = 4,14 e s = 0,21.
0 má = 9,4; qt = 8,7; qs = 12,55
CAPITULO 4
1. a) Q = {cara, coroa}; b) Q = {0,1,2, ...}; c) Q = {0, 1, 2,...};
d) Q = {v, tal que v > 0};
e) Q = {t, tal que - x < t < + x}. Poderia também desconsiderar resulta­
dos absurdos, como Q = {t, tal que - 5 < t < 40}.
2. a) A = {t, tal que 5 < t < 10}; B = {t, tal que t > 10};
C = {t, tal que t > 8}; D = {t, tal que t > 5};
£ = ()); F = {t, tal que 8 < t < 10};
G = {t, tal que t < 5 ou t > 10}
3. a) 3/4; b) 22/52
4. 2,5%
5. a) 2/5, 15/50, 7/50, 1/10, 3/50 b) 3/5

3 5 6 ESTATÍSTICA
6. a) l/e b) 1 - 5/2e
8. 1/1024
9. 6.500/6.850; 530/6.850; 500/6.850; 500/530; 500/6.500
10. a) 0,2095 b) 0,1364
11. a) 0,02875 b) 0,5565
12. 0,85
13. a) 0,72 b) 0,98
14. 0,9639
15. a) 0,54 b) 0,04 c) 0,42
16. a) HH HM MH MM b) 51/105 c) 36/
36/105 27/105 27/105 15/105
17. a) P A b) PP PA AP AA
3/7 4/7 9/49 12/49 12/49 16/49
c) 29/161 40/161 40/161 52/161 d) 0,01157 e) 0,2593
18. a) 9/25 b) 17/60 c) 4/17
19. a) 0,7 b) 0,94 c) 0,8333 d) 0,875
20. 0,9990
21. 0,4865
CAPITULO 5
1. a) x : 0 1 b) x : 0 1 2 c) x : 0 1 2
p(x): Vi Vi p(x): V* Vz Va p(x): 0,36 0,48 0,16
d) x : 0 1 2 3
p{x): 0,216 0,432 0,288 0,064

RESPOSTAS DE EXERCÍCIOS 3 5 7
3. 0 se x < 0
0,216 se 0 < x < 1
F M = 0,648 se 1 < x < 2
0,936 se 2 < x < 3
1 se x > 3
4. a) 0,5 e 0,25 b) 1 e 0,5 c) 0,8 e 0,48 d) 1,2 e 0,72
5. a) 4 e 9,6 b) 5 e 9,6 c) 8 e 38,4
6. 1.000 g e 10,7703 g
7. a) 0,6415 b) 0,1887 c) 0,0754 d) 1 e) 19
9. 0,0640
10. 0,5 e 0,3879
11. a) 0,0843 b) 0,2052
12. 0,0527
13. 150 e 27,39
14. 0,0702
15. b) 0,6415 c) 0,1886 d) 1 erro
16. proposta 1
17. a) 0,737 b) 0,337
18. a) 0,9990 b) 0,9989
19. 0,0137
20. 0,6321
21. a) 0,6723 b) 0,7183
22. a) 0,7408 b) 0,0369 c) 0,6135
23. Alternativa 2 (|i = RS 111,80)
24. a) 0,0498;
b) Proposta: lucro esperado R$ 57,47; por categoria: RS 76,00 (não);
c) 1064,85
25. a) 0,8009 b) 0,8428

3 5 8 ESTATÍSTICA
CAPITULO 6
1. a) 0, para x < 0
Para0 - X ~ 1
b) F M x, para 0 < x < 1
n J 10, para x e [0,1]
1, para x > 1
y2 yn
c) e
2. 1 /4 , para 20 < x < 24
f W = a) Va b) 22 c) 4/3
0, para x g [20,24]
3.
— - 5 para 20 < x < 22
4
f W = a) % b) 22 c) %
para 22 < x < 24
4 ’
0, para x g [20,24]
4- fíx) = í e~X para X - 0
' 0, para x < 0
5. a) 1 b) y2 c) % d) 1 e) y6
6. a) 0,3679 b) 0,4135 c) 0,3679
8. a) 0,0495 b) -0,9505 c) 0,6826 d) 0,955 e) 0,9974
f) 0,000 g) 1,65 h) 2,58
9. a) 0,6915 b) 0,7333
10. a) 0,0314 b) 0,9372
11. a) 0,1052 b) 0,2033
12. 0,1056
13. 0,4724
14. 0,6321
15. 2.877 horas
17. a) 0,0071 b) 0,15 (usando aproximação normal)
18. a) 0,8472 b) 0,3859

RESPOSTAS DE EXERCÍCIOS 3 5 9
19. a) 0,0781 b) * 0
20. 0,0202
21. 27,63 segundos
22. a) 0,8858 b) 0,153 mm
23. a) 0,1335 b) 0,6632 c) 0,1541 d) 5.504 kg/cm2
24. M2, pois E(M1) = R$ 83,64 e E(M2) = RS 163,30.
CAPÍTULO 7
P A p (p)
0 y2
y2 y2
2. x: 3,80 3,85 3,90 3,95 4,00 4,05 4,10
pU) : %6 Vi6 Vi6 Vi6 Vi6 Vi6 Xe média = 3,95 var. = 0,00625
4. a) 0,5 b) 0,3174 c) 0,0456 d) 0,95 e) 0,03
5. 0,0722 (usando a correção de continuidade)
6. 0,0694 (usando a correção de continuidade)
7. a) 1/2 e 1/12 b) 0,06 c) 1/2 e 1/1200
d) aprox. normal e) 0,7016
8. a) 0,32 b) 0,0037
10. 55% ± 6,9%
11. 3,00% ± 1,36%
12. 98,0 mm ± 1,8 mm
13. 28
14. 11
15. 12

3 6 0 ESTATÍSTICA
16. a) 865 b) 1.494
17. 35,9 ± 11,2
18. a) 14,00 ± 0,98 b) 184
19. a) 102 b) 5,30 ± 0,45
c) Não, pois o intervalo onde deve estar a verdadeira média abrange tam­
bém valores menores que cinco.
d) 68,6% ± 7,4%
20. 77
21. 176
22. 2.500 (adotando z * 2)
23. a) 15,443 e 2,074 b) 15,44 ± 1,20 c) 157
24. a) 95% ± 2,1% b) 12.298
CAPÍTULO 8
1. a) 0,0062 b) 0,3874 c) 0,0062
2. a) Rejeita H0 b) Aceita H0 c) Rejeita H0
3. Rejeita H0 se ocorrer 0, 1, 2,13, 14 ou 15 caras. Caso contrário, aceita H0.
4. É possível. Por exemplo, se no teste para verificar se uma moeda é honesta
ocorrer 7 = 2 caras em n = 12 lançamentos, temos p = 0,0384, que rejeita
H0 ao nível de 5%, mas aceita ao nível de 1%. O inverso nunca acontece.
5. a) Decide-se por Hx, pois o valor p é menor do que o nível de significân-
cia adotado. Dada a evidência da amostra, o risco dele estar tomando
a decisão errada é de 0,0001.
b) Decide-se por H0, pois o valor p é maior do que o nível de significância
adotado. Quando se aceita H0, o valor p não oferece qualquer informa­
ção sobre o risco de se estar tomando a decisão errada.
c) Quanto menor o valor p, existe maior evidência para a rejeição de H0
(e consequente aceitação de Hj).
6. a) bilateral b) unilateral c) unilateral d) unilateral

RESPOSTAS DE EXERCÍCIOS 3 6 1
7. a) H0: Em média, a produtividade com treinamento é igual do que a pro­
dutividade sem treinamento. Hii Em média, a produtividade com trei­
namento é maior do que a produtividade sem treinamento (teste unila­
teral) .
b) H0: Em média, a velocidade é igual ao valor anunciado. H^: Em média,
a velocidade é menor do que o valor anunciado (teste unilateral).
c) H0: As produtividades médias são iguais para os dois métodos de trei­
namento. Hii As produtividades médias são diferentes para os dois mé­
todos de treinamento (teste bilateral).
8. a) 0,0031 b) 0,1937 c) 0,6127
9. Rejeita H0 se ocorrer 10 ou 11 caras. Caso contrário, aceita H0.
10. Hipóteses: H0: p = 0,5 e HL: p > 0,5 (p = probabilidade de a criança acer­
tar uma dada questão). Decisão: rejeita H0, isto é, há evidência de que a
criança tem algum conhecimento sobre o assunto (p = 0,0031).
11. a) H0: p =0,25 e Hx: p > 0,25; b) ji = 3 c) p = 0,1576
d) Aceita H0. Não há evidência de que a criança tem algum conhecimen­
to sobre o assunto.
12. a) 0,0094 b) 0,3844 c) 0,0094
14. a) Aceita H0: a moeda é honesta (p = 0,2892).
b) Rejeita H0, isto é, decide-se que a moeda é viciada (p » 0,0000068,
uso da aproximação normal).
15. Decisão: rejeita H0, isto é, há evidência de que o sistema “inteligente” ad­
quiriu algum conhecimento sobre o assunto (p = 0,0071, uso da aproxima­
ção normal).
16. Não, pois z = 1,11= = > p = 0,267= = > aceita H0.
17. Não, pois um teste unilateral aceita H0: p = 0,90 (z = - 1,18, p = 0,119)
18. Sim (z = -3,13; p < 0,00135)
19. Sim (t = 5,59; p < 0,0005)
20. Sim (q2 = 12,89; p < 0,01)
21. Não (q2 = 21,3; p > 0,20)
22. = 53
ti
23. = 18 (mais 10 unidades)
ti

3 6 2 ESTATÍSTICA
24. a) 71,06 e 7,49; b) H0: \i = 70 e Hx: n > 70
c) Não (t = 0,57; p > 0,25)
d) Aceitar H0 quando falsa e) 0,564
25. a) 498,94 e 4,07 b) Não (t = - 1,04; 0,10 < p < 0,25)
c) Sim (q2 = 24,85; 0,05 < p < 0,10)
26. a) Não (z = - 0,968; p = 0,166) b) Não, n = 138 c) 0,751
27. a) Não (z = - 0,86; p = 0,1949) b) 0,74 c) 9.450
28. a) 20; b) Não (t = - 0,596; p > 0,25)
c) Sim (q2 = 42,75; p < 0,0025)
CAPÍTULO 9
1. Não. Usando teste t unilateral para amostras independentes: t = 1,51
(0,05 < p < 0,10)
2. Sim. Usando teste t unilateral para dados pareados: t = 3,10 (0,01 < p
< 0,025)
3. b) Rejeita H0 ao nível de 5%, pois t = 2,70 = = > 0,01 < p < 0,025 (tes­
te unilateral).
4. a) Rejeita H0 ao nível de 5%, pois, t = 3,04 = = > 0,005 < p < 0,010
(teste unilateral).
5. Não, t = - 0,36, p > 0,25 (teste bilateral).
6. Há diferença significativa (t = 294, p < 0,01).
7. Sim. Teste t bilateral para amostras independentes: t = - 4,40 (p <
0,001).
8. Sim (t = 5,175; 0,002 < p < 0,005).
9. n « 22.
10. a) Rejeita a hipótese de igualdade entre os circuitos (f = 11,27 > fc = 3,89).

RESPOSTAS DE EXERCÍCIOS 3 6 3
11. Não (f = 3,08 < f c = 7,15, então aceita a hipótese nula de igualdade entre
as variâncias).
12. Sim (f = 28,40 > f c = 4,76).
13. a)
Fonte de variação SQ gl QM /
Memória cache 1026675 1 1026675 1207,9
Memória principal 1944075 1 1944075 2287,1
Interações 151875 1 151875 178,7
Erro 6800 8 850
Total 3129425 11
) Todos (memória cache, memória principal e a interação entre e]
Não, devido a presença de interação.
14. a)
Fonte de variação SQ gl QM / fc
Processador 1028 2 514 60,76 3,89
Tipo de carga 18 3 6 0,71 3,49
Interação 286 6 47,67 5,63 3,00
Erro 102 12 8,50
Total 1934 23
A carga de trabalho e a interação são significativas.
15. a) Sim (t = 6,30; p < 0,0005) b) Não (q2 = 11,16; p > 0,10)
16. a) Sim (f = 10,72; p < 0,01) b) Sim (f = 52,17; p < 0,01)
17. Somente parâmetro é significativo, pois:
Ruído:/ = 0,389; p > 0,25; Parâmetro:/ = 8,469; p < 0,01;
Interação: / = 0,043; p > 0,25.

3 6 4 ESTATÍSTICA
18.
Fator Efeito
/
A 0,34 0,019
B - 1,94 0,613
C 4,58 3,419
D - 1,23 0,245
f c = 2,96, então somente o fator C apresenta efeito significativo a 10%.
CAPÍTULO 10
1. Aceita H0. Pedido do laboratório A não é corroborado pelos dados.
2. Rejeita H0. A suspeita dos engenheiros tem fundamento.
3. Rejeita H0 no teste de aderência à normal, e aceita H0 no teste de aderência
à exponencial. O sócio está certo.
4. Rejeita H0 no teste de aderência à normal. Não é possível utilizar os gráfi­
cos de controle de médias de Shewhart para monitorar o processo.
5. a) Aceita H0. Não há evidência suficiente para considerar que a dimensão
não siga uma distribuição normal.
b) Rejeita H0. Há evidência suficiente para considerar que a dimensão
não segue uma distribuição normal com média 15 e desvio padrão 0,4.
6. Rejeita H0. Os percentuais não podem ser considerados iguais.
7. Aceita H0. Não há evidência suficiente para considerar os percentuais dife­
rentes.
8. Rejeita H0. A suspeita tem fundamento, há evidência suficiente para sugerir
que os percentuais são diferentes.
9. a) Aceita H0. Não há evidência suficiente de que os tempos com o novo
terminal sejam menores do que aqueles obtidos com o atual.
b) Rejeita H0. O novo terminal possibilitou tempos de atendimento meno­
res, há evidência suficiente de que os tempos são menores.
c) Rejeita H0, resultado do item (b). Porque o teste dos sinais por postos é
mais sensível (tem maior poder de detectar a falsidade de H0 quando

RESPOSTAS DE EXERCÍCIOS 3 6 5
ela é realmente falsa), pois leva em conta o sinal e a magnitude das di­
ferenças entre os grupos.
10. a) Rejeita H0. O número de pessoas na fila com o novo terminal é menor
do que aquele obtido com o atual. Há evidência estatística suficiente
de que o número de pessoas é menor.
b) Aceita H0. Não há evidência suficiente de que o número de pessoas na
fila com o novo terminal seja menor do que aquele obtido com o atual.
11. a) Aceita H0. Não há evidência suficiente de que as taxas de transmissão
de dados com o novo cabeamento sejam maiores do que aquelas obti­
das com o atual.
b) Rejeita H0. O novo cabeamento possibilitou taxas de transmissão maio­
res, há evidência suficiente de que os taxas de transmissão são maiores.
12. a) Aceita H0. Não há evidência suficiente de que os dois métodos produ­
zam resultados diferentes.
b) Aceita H0. Não há evidência suficiente de que os dois métodos produ­
zam resultados diferentes.
c) Os métodos não produzem resultados diferentes, pois tanto teste dos
sinais quanto o dos sinais por postos aceitaram H0.
13. Aceita H0. Não há evidência suficiente de que as arquiteturas causem dife­
renças nos tempos de processamento.
14. Rejeita H0. A suspeita é confirmada. Há evidência suficiente para conside­
rar o concreto Y mais resistente à compressão do que o X.
15. Aceita H0. Não há evidência suficiente de que os tempos de rompimento
do novo modelo de elo fusível sejam menores, não se deve cogitar sua
aquisição.
16. Rejeita H0. A espécie 1 degrada a lignina mais rapidamente. Há evidência
suficiente para considerar que a espécie 1 degrada a lignina mais rápido do
que a espécie 2.
17. a) Aceita H0. Não há evidência suficiente para considerar que o consumo
de energia elétrica não siga uma distribuição normal com média de 85
kWh e desvio padrão de 15 kWh.
b) Aceita H0. Não há evidência suficiente para considerar que o consumo
de energia elétrica não siga uma distribuição normal com média de 85
kWh e desvio padrão de 15 kWh.

3 6 6 ESTATÍSTICA
18. Aceita H0. Não há evidência suficiente de que haja associação entre os per­
centuais de defeitos e as fábricas onde as peças foram produzidas.
19. Rejeita H0. A concentração de desinfetante não é homogênea nas três filiais.
Há evidência suficiente para considerar que a concentração difere depen­
dendo da filial que produz o produto de limpeza.
20. Rejeita H0. As mudanças no programa da Qualidade foram aprovadas pelos
funcionários. Há evidência suficiente de que aqueles que desaprovavam an­
tes agora aprovam.
21. Aceita H0. Não há evidência suficiente de que haja diferença entre os índi­
ces de alunos e alunas.
22. Aceita H0. Não há evidência suficiente de que o número de defeituosos di­
minuiu, ou seja, que o programa da Qualidade teve resultado.
23. Aceita H0. Não há evidência suficiente para considerar que as médias das
durações dos pneus vendidos pelos dois fabricantes sejam diferentes.
CAPITULO 11
1. 0,64 (Não, a correlação não é significativamente diferente de zero.)
3. a) 0,69 c) 0,86
d) Correlação é positiva forte e significativamente diferente de zero.
5. a) 49,1 kg b) 1,8 kg
6. a) a = 36,6 e b = 3,83 b) R2 = 0,95 c) se = 1,836
d) Rejeita H0, pois / = 76,1 (p < 0,0001) ou t = 8,72 (p < 0,0001).
7. a) r = - 0,96 b) Correlação negativa forte.
c) Variável dependente: consumo; e variável independente: peso.
d) (consumo) = 22,25 - 0,62 (peso).

RESPOSTAS DE EXERCÍCIOS 3 6 7
e)
I
a
Cc/5
o
u
peso (100 kg)
f) Sim, verifica-se pelo gráfico do item (e) que uma relação linear parece
adequar-se bem ao presente problema. Além disso, tem-se um coe­
ficiente de determinação próximo de 1 (R2 = 0,92)
g) 9,85 km/l
h) Não, pois os veículos estudados estavam na faixa de 1200 a 2600 kg e,
portanto, a equação de regressão deve ser usada apenas nesta faixa.
8. a) y = 40,22 - (0,35)* b) 0,27
c) Aceita H0: p = 0 (Teste bilateral: t = - 1,72; 0,10 < p < 0,20).
d) Não.
9. c) Transformação logarítmica em Y.
10. Em termos do modelo estabelecido, 89% da variância de logÇvalor) pode
ser explicada pelos diferentes valores de log(area). A cada unidade a mais
no log(área), sendo área medida em m2, o log(va/or) aumenta 1,38 unida­
de, sendo valor medido em S.

APÊNDICE: Tabelas Estatísticas
Tabela 1 Distribuição binomial: probabilidade de cada valor x em função de n e p.
P
n X
0,05 0,1 0,15 0,2 0,25 0,3 0,35 0,4 0,45 0,5 0,55 0,6 0,65 0,7 0,75 0,8 0,85 0,9 0,95
1 0 0,9500 0,9000 0,8500 0,8000 0,7500 0,7000 0,6500 0,6000 0,5500 0,5000 0,4500 0,4000 0,3500 0,3000 0,2500 0,2000 0,1500 0,1000 0,0500
1 0,0500 0,1000 0,1500 0,2000 0,2500 0,3000 0,3500 0,4000 0,4500 0,5000 0,5500 0,6000 0,6500 0,7000 0,7500 0,8000 0,8500 0,9000 0,9500
2 0 0,9025 0,8100 0,7225 0,6400 0,5625 0,4900 0,4225 0,3600 0,3025 0,2500 0,2025 0,1600 0,1225 0,0900 0,0625 0,0400 0,0225 0,0100 0,0025
1 0,0950 0,1800 0,2550 0,3200 0,3750 0,4200 0,4550 0,4800 0,4950 0,5000 0,4950 0,4800 0,4550 0,4200 0,3750 0,3200 0,2550 0,1800 0,0950
2 0,0025 0,0100 0,0225 0,0400 0,0625 0,0900 0,1225 0,1600 0,2025 0,2500 0,3025 0,3600 0,4225 0,4900 0,5625 0,6400 0,7225 0,8100 0,9025
3 0 0,8574 0,7290 0,6141 0,5120 0,4219 0,3430 0,2746 0,2160 0,1664 0,1250 0,0911 0,0640 0,0429 0,0270 0,0156 0,0080 0,0034 0,0010 0,0001
1 0,1354 0,2430 0,3251 0,3840 0,4219 0,4410 0,4436 0,4320 0,4084 0,3750 0,3341 0,2880 0,2389 0,1890 0,1406 0,0960 0,0574 0,0270 0,0071
2 0,0071 0,0270 0,0574 0,0960 0,1406 0,1890 0,2389 0,2880 0,3341 0,3750 0,4084 0,4320 0,4436 0,4410 0,4219 0,3840 0,3251 0,2430 0,1354
3 0,0001 0,0010 0,0034 0,0080 0,0156 0,0270 0,0429 0,0640 0,0911 0,1250 0,1664 0,2160 0,2746 0,3430 0,4219 0,5120 0,6141 0,7290 0,8574
4 0 0,8145 0,6561 0,5220 0,4096 0,3164 0,2401 0,1785 0,1296 0,0915 0,0625 0,0410 0,0256 0,0150 0,0081 0,0039 0,0016 0,0005 0,0001 0,0000
1 0,1715 0,2916 0,3685 0,4096 0,4219 0,4116 0,3845 0,3456 0,2995 0,2500 0,2005 0,1536 0,1115 0,0756 0,0469 0,0256 0,0115 0,0036 0,0005
2 0,0135 0,0486 0,0975 0,1536 0,2109 0,2646 0,3105 0,3456 0,3675 0,3750 0,3675 0,3456 0,3105 0,2646 0,2109 0,1536 0,0975 0,0486 0,0135
3 0,0005 0,0036 0,0115 0,0256 0,0469 0,0756 0,1115 0,1536 0,2005 0,2500 0,2995 0,3456 0,3845 0,4116 0,4219 0,4096 0,3685 0,2916 0,1715
4 0,0000 0,0001 0,0005 0,0016 0,0039 0,0081 0,0150 0,0256 0,0410 0,0625 0,0915 0,1296 0,1785 0,2401 0,3164 0,4096 0,5220 0,6561 0,8145
5 0 0,7738 0,5905 0,4437 0,3277 0,2373 0,1681 0,1160 0,0778 0,0503 0,0313 0,0185 0,0102 0,0053 0,0024 0,0010 0,0003 0,0001 0,0000 0,0000
1 0,2036 0,3281 0,3915 0,4096 0,3955 0,3602 0,3124 0,2592 0,2059 0,1563 0,1128 0,0768 0,0488 0,0284 0,0146 0,0064 0,0022 0,0005 0,0000
368
ESTATÍSTICA

Tabela 1 (Continuação).
P
n X
0,05 0,1 0,15 0,2 0,25 0,3 0,35 0,4 0,45 0,5 0,55 0,6 0,65 0,7 0,75 0,8 0,85 0,9 0,95
2 0,0214 0,0729 0,1382 0,2048 0,2637 0,3087 0,3364 0,3456 0,3369 0,3125 0,2757 0,2304 0,1811 0,1323 0,0879 0,0512 0,0244 0,0081 0,0011
3 0,0011 0,0081 0,0244 0,0512 0,0879 0,1323 0,1811 0,2304 0,2757 0,3125 0,3369 0,3456 0,3364 0,3087 0,2637 0,2048 0,1382 0,0729 0,0214
4 0,0000 0,0005 0,0022 0,0064 0,0146 0,0284 0,0488 0,0768 0,1128 0,1563 0,2059 0,2592 0,3124 0,3602 0,3955 0,4096 0,3915 0,3281 0,2036
5 0,0000 0,0000 0,0001 0,0003 0,0010 0,0024 0,0053 0,0102 0,0185 0,0313 0,0503 0,0778 0,1160 0,1681 0,2373 0,3277 0,4437 0,5905 0,7738
6 0 0,7351 0,5314 0,3771 0,2621 0,1780 0,1176 0,0754 0,0467 0,0277 0,0156 0,0083 0,0041 0,0018 0,0007 0,0002 0,0001 0,0000 0,0000 0,0000
1 0,2321 0,3543 0,3993 0,3932 0,3560 0,3025 0,2437 0,1866 0,1359 0,0938 0,0609 0,0369 0,0205 0,0102 0,0044 0,0015 0,0004 0,0001 0,0000
2 0,0305 0,0984 0,1762 0,2458 0,2966 0,3241 0,3280 0,3110 0,2780 0,2344 0,1861 0,1382 0,0951 0,0595 0,0330 0,0154 0,0055 0,0012 0,0001
3 0,0021 0,0146 0,0415 0,0819 0,1318 0,1852 0,2355 0,2765 0,3032 0,3125 0,3032 0,2765 0,2355 0,1852 0,1318 0,0819 0,0415 0,0146 0,0021
4 0,0001 0,0012 0,0055 0,0154 0,0330 0,0595 0,0951 0,1382 0,1861 0,2344 0,2780 0,3110 0,3280 0,3241 0,2966 0,2458 0,1762 0,0984 0,0305
5 0,0000 0,0001 0,0004 0,0015 0,0044 0,0102 0,0205 0,0369 0,0609 0,0938 0,1359 0,1866 0,2437 0,3025 0,3560 0,3932 0,3993 0,3543 0,2321
6 0,0000 0,0000 0,0000 0,0001 0,0002 0,0007 0,0018 0,0041 0,0083 0,0156 0,0277 0,0467 0,0754 0,1176 0,1780 0,2621 0,3771 0,5314 0,7351
7 0 0,6983 0,4783 0,3206 0,2097 0,1335 0,0824 0,0490 0,0280 0,0152 0,0078 0,0037 0,0016 0,0006 0,0002 0,0001 0,0000 0,0000 0,0000 0,0000
1 0,2573 0,3720 0,3960 0,3670 0,3115 0,2471 0,1848 0,1306 0,0872 0,0547 0,0320 0,0172 0,0084 0,0036 0,0013 0,0004 0,0001 0,0000 0,0000
2 0,0406 0,1240 0,2097 0,2753 0,3115 0,3177 0,2985 0,2613 0,2140 0,1641 0,1172 0,0774 0,0466 0,0250 0,0115 0,0043 0,0012 0,0002 0,0000
3 0,0036 0,0230 0,0617 0,1147 0,1730 0,2269 0,2679 0,2903 0,2918 0,2734 0,2388 0,1935 0,1442 0,0972 0,0577 0,0287 0,0109 0,0026 0,0002
4 0,0002 0,0026 0,0109 0,0287 0,0577 0,0972 0,1442 0,1935 0,2388 0,2734 0,2918 0,2903 0,2679 0,2269 0,1730 0,1147 0,0617 0,0230 0,0036
5 0,0000 0,0002 0,0012 0,0043 0,0115 0,0250 0,0466 0,0774 0,1172 0,1641 0,2140 0,2613 0,2985 0,3177 0,3115 0,2753 0,2097 0,1240 0,0406
6 0,0000 0,0000 0,0001 0,0004 0,0013 0,0036 0,0084 0,0172 0,0320 0,0547 0,0872 0,1306 0,1848 0,2471 0,3115 0,3670 0,3960 0,3720 0,2573
7 0,0000 0,0000 0,0000 0,0000 0,0001 0,0002 0,0006 0,0016 0,0037 0,0078 0,0152 0,0280 0,0490 0,0824 0,1335 0,2097 0,3206 0,4783 0,6983
APÊNDICE:
TABELAS
ESTATÍSTICAS
369

Tabela 1 (Continuação).
P
n X
0,05 0,1 0,15 0,2 0,25 0,3 0,35 0,4 0,45 0,5 0,55 0,6 0,65 0,7 0,75 0,8 0,85 0,9 0,95
8 0 0,6634 0,4305 0,2725 0,1678 0,1001 0,0576 0,0319 0,0168 0,0084 0,0039 0,0017 0,0007 0,0002 0,0001 0,0000 0,0000 0,0000 0,0000 0,0000
1 0,2793 0,3826 0,3847 0,3355 0,2670 0,1977 0,1373 0,0896 0,0548 0,0313 0,0164 0,0079 0,0033 0,0012 0,0004 0,0001 0,0000 0,0000 0,0000
2 0,0515 0,1488 0,2376 0,2936 0,3115 0,2965 0,2587 0,2090 0,1569 0,1094 0,0703 0,0413 0,0217 0,0100 0,0038 0,0011 0,0002 0,0000 0,0000
3 0,0054 0,0331 0,0839 0,1468 0,2076 0,2541 0,2786 0,2787 0,2568 0,2188 0,1719 0,1239 0,0808 0,0467 0,0231 0,0092 0,0026 0,0004 0,0000
4 0,0004 0,0046 0,0185 0,0459 0,0865 0,1361 0,1875 0,2322 0,2627 0,2734 0,2627 0,2322 0,1875 0,1361 0,0865 0,0459 0,0185 0,0046 0,0004
5 0,0000 0,0004 0,0026 0,0092 0,0231 0,0467 0,0808 0,1239 0,1719 0,2188 0,2568 0,2787 0,2786 0,2541 0,2076 0,1468 0,0839 0,0331 0,0054
6 0,0000 0,0000 0,0002 0,0011 0,0038 0,0100 0,0217 0,0413 0,0703 0,1094 0,1569 0,2090 0,2587 0,2965 0,3115 0,2936 0,2376 0,1488 0,0515
7 0,0000 0,0000 0,0000 0,0001 0,0004 0,0012 0,0033 0,0079 0,0164 0,0313 0,0548 0,0896 0,1373 0,1977 0,2670 0,3355 0,3847 0,3826 0,2793
8 0,0000 0,0000 0,0000 0,0000 0,0000 0,0001 0,0002 0,0007 0,0017 0,0039 0,0084 0,0168 0,0319 0,0576 0,1001 0,1678 0,2725 0,4305 0,6634
9 0 0,6302 0,3874 0,2316 0,1342 0,0751 0,0404 0,0207 0,0101 0,0046 0,0020 0,0008 0,0003 0,0001 0,0000 0,0000 0,0000 0,0000 0,0000 0,0000
1 0,2985 0,3874 0,3679 0,3020 0,2253 0,1556 0,1004 0,0605 0,0339 0,0176 0,0083 0,0035 0,0013 0,0004 0,0001 0,0000 0,0000 0,0000 0,0000
2 0,0629 0,1722 0,2597 0,3020 0,3003 0,2668 0,2162 0,1612 0,1110 0,0703 0,0407 0,0212 0,0098 0,0039 0,0012 0,0003 0,0000 0,0000 0,0000
3 0,0077 0,0446 0,1069 0,1762 0,2336 0,2668 0,2716 0,2508 0,2119 0,1641 0,1160 0,0743 0,0424 0,0210 0,0087 0,0028 0,0006 0,0001 0,0000
4 0,0006 0,0074 0,0283 0,0661 0,1168 0,1715 0,2194 0,2508 0,2600 0,2461 0,2128 0,1672 0,1181 0,0735 0,0389 0,0165 0,0050 0,0008 0,0000
5 0,0000 0,0008 0,0050 0,0165 0,0389 0,0735 0,1181 0,1672 0,2128 0,2461 0,2600 0,2508 0,2194 0,1715 0,1168 0,0661 0,0283 0,0074 0,0006
6 0,0000 0,0001 0,0006 0,0028 0,0087 0,0210 0,0424 0,0743 0,1160 0,1641 0,2119 0,2508 0,2716 0,2668 0,2336 0,1762 0,1069 0,0446 0,0077
7 0,0000 0,0000 0,0000 0,0003 0,0012 0,0039 0,0098 0,0212 0,0407 0,0703 0,1110 0,1612 0,2162 0,2668 0,3003 0,3020 0,2597 0,1722 0,0629
8 0,0000 0,0000 0,0000 0,0000 0,0001 0,0004 0,0013 0,0035 0,0083 0,0176 0,0339 0,0605 0,1004 0,1556 0,2253 0,3020 0,3679 0,3874 0,2985
9 0,0000 0,0000 0,0000 0,0000 0,0000 0,0000 0,0001 0,0003 0,0008 0,0020 0,0046 0,0101 0,0207 0,0404 0,0751 0,1342 0,2316 0,3874 0,6302
10 0 0,5987 0,3487 0,1969 0,1074 0,0563 0,0282 0,0135 0,0060 0,0025 0,0010 0,0003 0,0001 0,0000 0,0000 0,0000 0,0000 0,0000 0,0000 0,0000
1 0,3151 0,3874 0,3474 0,2684 0,1877 0,1211 0,0725 0,0403 0,0207 0,0098 0,0042 0,0016 0,0005 0,0001 0,0000 0,0000 0,0000 0,0000 0,0000
370
ESTATÍSTICA

Tabela 1 (Continuação).
P
n X
0,05 0,1 0,15 0,2 0,25 0,3 0,35 0,4 0,45 0,5 0,55 0,6 0,65 0,7 0,75 0,8 0,85 0,9 0,95
2 0,0746 0,1937 0,2759 0,3020 0,2816 0,2335 0,1757 0,1209 0,0763 0,0439 0,0229 0,0106 0,0043 0,0014 0,0004 0,0001 0,0000 0,0000 0,0000
3 0,0105 0,0574 0,1298 0,2013 0,2503 0,2668 0,2522 0,2150 0,1665 0,1172 0,0746 0,0425 0,0212 0,0090 0,0031 0,0008 0,0001 0,0000 0,0000
4 0,0010 0,0112 0,0401 0,0881 0,1460 0,2001 0,2377 0,2508 0,2384 0,2051 0,1596 0,1115 0,0689 0,0368 0,0162 0,0055 0,0012 0,0001 0,0000
5 0,0001 0,0015 0,0085 0,0264 0,0584 0,1029 0,1536 0,2007 0,2340 0,2461 0,2340 0,2007 0,1536 0,1029 0,0584 0,0264 0,0085 0,0015 0,0001
6 0,0000 0,0001 0,0012 0,0055 0,0162 0,0368 0,0689 0,1115 0,1596 0,2051 0,2384 0,2508 0,2377 0,2001 0,1460 0,0881 0,0401 0,0112 0,0010
7 0,0000 0,0000 0,0001 0,0008 0,0031 0,0090 0,0212 0,0425 0,0746 0,1172 0,1665 0,2150 0,2522 0,2668 0,2503 0,2013 0,1298 0,0574 0,0105
8 0,0000 0,0000 0,0000 0,0001 0,0004 0,0014 0,0043 0,0106 0,0229 0,0439 0,0763 0,1209 0,1757 0,2335 0,2816 0,3020 0,2759 0,1937 0,0746
9 0,0000 0,0000 0,0000 0,0000 0,0000 0,0001 0,0005 0,0016 0,0042 0,0098 0,0207 0,0403 0,0725 0,1211 0,1877 0,2684 0,3474 0,3874 0,3151
10 0,0000 0,0000 0,0000 0,0000 0,0000 0,0000 0,0000 0,0001 0,0003 0,0010 0,0025 0,0060 0,0135 0,0282 0,0563 0,1074 0,1969 0,3487 0,5987
11 0 0,5688 0,3138 0,1673 0,0859 0,0422 0,0198 0,0088 0,0036 0,0014 0,0005 0,0002 0,0000 0,0000 0,0000 0,0000 0,0000 0,0000 0,0000 0,0000
1 0,3293 0,3835 0,3248 0,2362 0,1549 0,0932 0,0518 0,0266 0,0125 0,0054 0,0021 0,0007 0,0002 0,0000 0,0000 0,0000 0,0000 0,0000 0,0000
2 0,0867 0,2131 0,2866 0,2953 0,2581 0,1998 0,1395 0,0887 0,0513 0,0269 0,0126 0,0052 0,0018 0,0005 0,0001 0,0000 0,0000 0,0000 0,0000
3 0,0137 0,0710 0,1517 0,2215 0,2581 0,2568 0,2254 0,1774 0,1259 0,0806 0,0462 0,0234 0,0102 0,0037 0,0011 0,0002 0,0000 0,0000 0,0000
4 0,0014 0,0158 0,0536 0,1107 0,1721 0,2201 0,2428 0,2365 0,2060 0,1611 0,1128 0,0701 0,0379 0,0173 0,0064 0,0017 0,0003 0,0000 0,0000
5 0,0001 0,0025 0,0132 0,0388 0,0803 0,1321 0,1830 0,2207 0,2360 0,2256 0,1931 0,1471 0,0985 0,0566 0,0268 0,0097 0,0023 0,0003 0,0000
6 0,0000 0,0003 0,0023 0,0097 0,0268 0,0566 0,0985 0,1471 0,1931 0,2256 0,2360 0,2207 0,1830 0,1321 0,0803 0,0388 0,0132 0,0025 0,0001
7 0,0000 0,0000 0,0003 0,0017 0,0064 0,0173 0,0379 0,0701 0,1128 0,1611 0,2060 0,2365 0,2428 0,2201 0,1721 0,1107 0,0536 0,0158 0,0014
8 0,0000 0,0000 0,0000 0,0002 0,0011 0,0037 0,0102 0,0234 0,0462 0,0806 0,1259 0,1774 0,2254 0,2568 0,2581 0,2215 0,1517 0,0710 0,0137
9 0,0000 0,0000 0,0000 0,0000 0,0001 0,0005 0,0018 0,0052 0,0126 0,0269 0,0513 0,0887 0,1395 0,1998 0,2581 0,2953 0,2866 0,2131 0,0867
10 0,0000 0,0000 0,0000 0,0000 0,0000 0,0000 0,0002 0,0007 0,0021 0,0054 0,0125 0,0266 0,0518 0,0932 0,1549 0,2362 0,3248 0,3835 0,3293
11 0,0000 0,0000 0,0000 0,0000 0,0000 0,0000 0,0000 0,0000 0,0002 0,0005 0,0014 0,0036 0,0088 0,0198 0,0422 0,0859 0,1673 0,3138 0,5688
APÊNDICE:
TABELAS
ESTATÍSTICAS
371

Tabela 1 (Continuação).
P
n X
0,05 0,1 0,15 0,2 0,25 0,3 0,35 0,4 0,45 0,5 0,55 0,6 0,65 0,7 0,75 0,8 0,85 0,9 0,95
12 0 0,5404 0,2824 0,1422 0,0687 0,0317 0,0138 0,0057 0,0022 0,0008 0,0002 0,0001 0,0000 0,0000 0,0000 0,0000 0,0000 0,0000 0,0000 0,0000
1 0,3413 0,3766 0,3012 0,2062 0,1267 0,0712 0,0368 0,0174 0,0075 0,0029 0,0010 0,0003 0,0001 0,0000 0,0000 0,0000 0,0000 0,0000 0,0000
2 0,0988 0,2301 0,2924 0,2835 0,2323 0,1678 0,1088 0,0639 0,0339 0,0161 0,0068 0,0025 0,0008 0,0002 0,0000 0,0000 0,0000 0,0000 0,0000
3 0,0173 0,0852 0,1720 0,2362 0,2581 0,2397 0,1954 0,1419 0,0923 0,0537 0,0277 0,0125 0,0048 0,0015 0,0004 0,0001 0,0000 0,0000 0,0000
4 0,0021 0,0213 0,0683 0,1329 0,1936 0,2311 0,2367 0,2128 0,1700 0,1208 0,0762 0,0420 0,0199 0,0078 0,0024 0,0005 0,0001 0,0000 0,0000
5 0,0002 0,0038 0,0193 0,0532 0,1032 0,1585 0,2039 0,2270 0,2225 0,1934 0,1489 0,1009 0,0591 0,0291 0,0115 0,0033 0,0006 0,0000 0,0000
6 0,0000 0,0005 0,0040 0,0155 0,0401 0,0792 0,1281 0,1766 0,2124 0,2256 0,2124 0,1766 0,1281 0,0792 0,0401 0,0155 0,0040 0,0005 0,0000
7 0,0000 0,0000 0,0006 0,0033 0,0115 0,0291 0,0591 0,1009 0,1489 0,1934 0,2225 0,2270 0,2039 0,1585 0,1032 0,0532 0,0193 0,0038 0,0002
8 0,0000 0,0000 0,0001 0,0005 0,0024 0,0078 0,0199 0,0420 0,0762 0,1208 0,1700 0,2128 0,2367 0,2311 0,1936 0,1329 0,0683 0,0213 0,0021
9 0,0000 0,0000 0,0000 0,0001 0,0004 0,0015 0,0048 0,0125 0,0277 0,0537 0,0923 0,1419 0,1954 0,2397 0,2581 0,2362 0,1720 0,0852 0,0173
10 0,0000 0,0000 0,0000 0,0000 0,0000 0,0002 0,0008 0,0025 0,0068 0,0161 0,0339 0,0639 0,1088 0,1678 0,2323 0,2835 0,2924 0,2301 0,0988
11 0,0000 0,0000 0,0000 0,0000 0,0000 0,0000 0,0001 0,0003 0,0010 0,0029 0,0075 0,0174 0,0368 0,0712 0,1267 0,2062 0,3012 0,3766 0,3413
12 0,0000 0,0000 0,0000 0,0000 0,0000 0,0000 0,0000 0,0000 0,0001 0,0002 0,0008 0,0022 0,0057 0,0138 0,0317 0,0687 0,1422 0,2824 0,5404
13 0 0,5133 0,2542 0,1209 0,0550 0,0238 0,0097 0,0037 0,0013 0,0004 0,0001 0,0000 0,0000 0,0000 0,0000 0,0000 0,0000 0,0000 0,0000 0,0000
1 0,3512 0,3672 0,2774 0,1787 0,1029 0,0540 0,0259 0,0113 0,0045 0,0016 0,0005 0,0001 0,0000 0,0000 0,0000 0,0000 0,0000 0,0000 0,0000
2 0,1109 0,2448 0,2937 0,2680 0,2059 0,1388 0,0836 0,0453 0,0220 0,0095 0,0036 0,0012 0,0003 0,0001 0,0000 0,0000 0,0000 0,0000 0,0000
3 0,0214 0,0997 0,1900 0,2457 0,2517 0,2181 0,1651 0,1107 0,0660 0,0349 0,0162 0,0065 0,0022 0,0006 0,0001 0,0000 0,0000 0,0000 0,0000
4 0,0028 0,0277 0,0838 0,1535 0,2097 0,2337 0,2222 0,1845 0,1350 0,0873 0,0495 0,0243 0,0101 0,0034 0,0009 0,0001 0,0000 0,0000 0,0000
5 0,0003 0,0055 0,0266 0,0691 0,1258 0,1803 0,2154 0,2214 0,1989 0,1571 0,1089 0,0656 0,0336 0,0142 0,0047 0,0011 0,0001 0,0000 0,0000
6 0,0000 0,0008 0,0063 0,0230 0,0559 0,1030 0,1546 0,1968 0,2169 0,2095 0,1775 0,1312 0,0833 0,0442 0,0186 0,0058 0,0011 0,0001 0,0000
7 0,0000 0,0001 0,0011 0,0058 0,0186 0,0442 0,0833 0,1312 0,1775 0,2095 0,2169 0,1968 0,1546 0,1030 0,0559 0,0230 0,0063 0,0008 0,0000
8 0,0000 0,0000 0,0001 0,0011 0,0047 0,0142 0,0336 0,0656 0,1089 0,1571 0,1989 0,2214 0,2154 0,1803 0,1258 0,0691 0,0266 0,0055 0,0003
372
ESTATÍSTICA

Tabela 1 (Continuação).
P
n X
0,05 0,1 0,15 0,2 0,25 0,3 0,35 0,4 0,45 0,5 0,55 0,6 0,65 0,7 0,75 0,8 0,85 0,9 0,95
9 0,0000 0,0000 0,0000 0,0001 0,0009 0,0034 0,0101 0,0243 0,0495 0,0873 0,1350 0,1845 0,2222 0,2337 0,2097 0,1535 0,0838 0,0277 0,0028
10 0,0000 0,0000 0,0000 0,0000 0,0001 0,0006 0,0022 0,0065 0,0162 0,0349 0,0660 0,1107 0,1651 0,2181 0,2517 0,2457 0,1900 0,0997 0,0214
11 0,0000 0,0000 0,0000 0,0000 0,0000 0,0001 0,0003 0,0012 0,0036 0,0095 0,0220 0,0453 0,0836 0,1388 0,2059 0,2680 0,2937 0,2448 0,1109
12 0,0000 0,0000 0,0000 0,0000 0,0000 0,0000 0,0000 0,0001 0,0005 0,0016 0,0045 0,0113 0,0259 0,0540 0,1029 0,1787 0,2774 0,3672 0,3512
13 0,0000 0,0000 0,0000 0,0000 0,0000 0,0000 0,0000 0,0000 0,0000 0,0001 0,0004 0,0013 0,0037 0,0097 0,0238 0,0550 0,1209 0,2542 0,5133
14 0 0,4877 0,2288 0,1028 0,0440 0,0178 0,0068 0,0024 0,0008 0,0002 0,0001 0,0000 0,0000 0,0000 0,0000 0,0000 0,0000 0,0000 0,0000 0,0000
1 0,3593 0,3559 0,2539 0,1539 0,0832 0,0407 0,0181 0,0073 0,0027 0,0009 0,0002 0,0001 0,0000 0,0000 0,0000 0,0000 0,0000 0,0000 0,0000
2 0,1229 0,2570 0,2912 0,2501 0,1802 0,1134 0,0634 0,0317 0,0141 0,0056 0,0019 0,0005 0,0001 0,0000 0,0000 0,0000 0,0000 0,0000 0,0000
3 0,0259 0,1142 0,2056 0,2501 0,2402 0,1943 0,1366 0,0845 0,0462 0,0222 0,0093 0,0033 0,0010 0,0002 0,0000 0,0000 0,0000 0,0000 0,0000
4 0,0037 0,0349 0,0998 0,1720 0,2202 0,2290 0,2022 0,1549 0,1040 0,0611 0,0312 0,0136 0,0049 0,0014 0,0003 0,0000 0,0000 0,0000 0,0000
5 0,0004 0,0078 0,0352 0,0860 0,1468 0,1963 0,2178 0,2066 0,1701 0,1222 0,0762 0,0408 0,0183 0,0066 0,0018 0,0003 0,0000 0,0000 0,0000
6 0,0000 0,0013 0,0093 0,0322 0,0734 0,1262 0,1759 0,2066 0,2088 0,1833 0,1398 0,0918 0,0510 0,0232 0,0082 0,0020 0,0003 0,0000 0,0000
7 0,0000 0,0002 0,0019 0,0092 0,0280 0,0618 0,1082 0,1574 0,1952 0,2095 0,1952 0,1574 0,1082 0,0618 0,0280 0,0092 0,0019 0,0002 0,0000
8 0,0000 0,0000 0,0003 0,0020 0,0082 0,0232 0,0510 0,0918 0,1398 0,1833 0,2088 0,2066 0,1759 0,1262 0,0734 0,0322 0,0093 0,0013 0,0000
9 0,0000 0,0000 0,0000 0,0003 0,0018 0,0066 0,0183 0,0408 0,0762 0,1222 0,1701 0,2066 0,2178 0,1963 0,1468 0,0860 0,0352 0,0078 0,0004
10 0,0000 0,0000 0,0000 0,0000 0,0003 0,0014 0,0049 0,0136 0,0312 0,0611 0,1040 0,1549 0,2022 0,2290 0,2202 0,1720 0,0998 0,0349 0,0037
11 0,0000 0,0000 0,0000 0,0000 0,0000 0,0002 0,0010 0,0033 0,0093 0,0222 0,0462 0,0845 0,1366 0,1943 0,2402 0,2501 0,2056 0,1142 0,0259
12 0,0000 0,0000 0,0000 0,0000 0,0000 0,0000 0,0001 0,0005 0,0019 0,0056 0,0141 0,0317 0,0634 0,1134 0,1802 0,2501 0,2912 0,2570 0,1229
13 0,0000 0,0000 0,0000 0,0000 0,0000 0,0000 0,0000 0,0001 0,0002 0,0009 0,0027 0,0073 0,0181 0,0407 0,0832 0,1539 0,2539 0,3559 0,3593
14 0,0000 0,0000 0,0000 0,0000 0,0000 0,0000 0,0000 0,0000 0,0000 0,0001 0,0002 0,0008 0,0024 0,0068 0,0178 0,0440 0,1028 0,2288 0,4877
APÊNDICE:
TABELAS
ESTATÍSTICAS
373

Tabela 1 (Continuação).
P
n X
0,05 0,1 0,15 0,2 0,25 0,3 0,35 0,4 0,45 0,5 0,55 0,6 0,65 0,7 0,75 0,8 0,85 0,9 0,95
15 0 0,4633 0,2059 0,0874 0,0352 0,0134 0,0047 0,0016 0,0005 0,0001 0,0000 0,0000 0,0000 0,0000 0,0000 0,0000 0,0000 0,0000 0,0000 0,0000
1 0,3658 0,3432 0,2312 0,1319 0,0668 0,0305 0,0126 0,0047 0,0016 0,0005 0,0001 0,0000 0,0000 0,0000 0,0000 0,0000 0,0000 0,0000 0,0000
2 0,1348 0,2669 0,2856 0,2309 0,1559 0,0916 0,0476 0,0219 0,0090 0,0032 0,0010 0,0003 0,0001 0,0000 0,0000 0,0000 0,0000 0,0000 0,0000
3 0,0307 0,1285 0,2184 0,2501 0,2252 0,1700 0,1110 0,0634 0,0318 0,0139 0,0052 0,0016 0,0004 0,0001 0,0000 0,0000 0,0000 0,0000 0,0000
4 0,0049 0,0428 0,1156 0,1876 0,2252 0,2186 0,1792 0,1268 0,0780 0,0417 0,0191 0,0074 0,0024 0,0006 0,0001 0,0000 0,0000 0,0000 0,0000
5 0,0006 0,0105 0,0449 0,1032 0,1651 0,2061 0,2123 0,1859 0,1404 0,0916 0,0515 0,0245 0,0096 0,0030 0,0007 0,0001 0,0000 0,0000 0,0000
6 0,0000 0,0019 0,0132 0,0430 0,0917 0,1472 0,1906 0,2066 0,1914 0,1527 0,1048 0,0612 0,0298 0,0116 0,0034 0,0007 0,0001 0,0000 0,0000
7 0,0000 0,0003 0,0030 0,0138 0,0393 0,0811 0,1319 0,1771 0,2013 0,1964 0,1647 0,1181 0,0710 0,0348 0,0131 0,0035 0,0005 0,0000 0,0000
8 0,0000 0,0000 0,0005 0,0035 0,0131 0,0348 0,0710 0,1181 0,1647 0,1964 0,2013 0,1771 0,1319 0,0811 0,0393 0,0138 0,0030 0,0003 0,0000
9 0,0000 0,0000 0,0001 0,0007 0,0034 0,0116 0,0298 0,0612 0,1048 0,1527 0,1914 0,2066 0,1906 0,1472 0,0917 0,0430 0,0132 0,0019 0,0000
10 0,0000 0,0000 0,0000 0,0001 0,0007 0,0030 0,0096 0,0245 0,0515 0,0916 0,1404 0,1859 0,2123 0,2061 0,1651 0,1032 0,0449 0,0105 0,0006
11 0,0000 0,0000 0,0000 0,0000 0,0001 0,0006 0,0024 0,0074 0,0191 0,0417 0,0780 0,1268 0,1792 0,2186 0,2252 0,1876 0,1156 0,0428 0,0049
12 0,0000 0,0000 0,0000 0,0000 0,0000 0,0001 0,0004 0,0016 0,0052 0,0139 0,0318 0,0634 0,1110 0,1700 0,2252 0,2501 0,2184 0,1285 0,0307
13 0,0000 0,0000 0,0000 0,0000 0,0000 0,0000 0,0001 0,0003 0,0010 0,0032 0,0090 0,0219 0,0476 0,0916 0,1559 0,2309 0,2856 0,2669 0,1348
14 0,0000 0,0000 0,0000 0,0000 0,0000 0,0000 0,0000 0,0000 0,0001 0,0005 0,0016 0,0047 0,0126 0,0305 0,0668 0,1319 0,2312 0,3432 0,3658
15 0,0000 0,0000 0,0000 0,0000 0,0000 0,0000 0,0000 0,0000 0,0000 0,0000 0,0001 0,0005 0,0016 0,0047 0,0134 0,0352 0,0874 0,2059 0,4633
374
ESTATÍSTICA

APÊNDICE: TABELAS ESTATÍSTICAS 3 7 5
Tabela 2 Distribuição acumulada de Poisson: P(X < x) = Y -------.
; «
X
0,05 0,1 0,15 0,2 0,25 0,3 0,35 0,4 0,45 0,5
0 0 ,9 5 1 2 0 ,9 0 4 8 0 ,8 6 0 7 0 ,8 1 8 7 0 ,7 7 8 8 0 ,7 4 0 8 0 ,7 0 4 7 0 ,6 7 0 3 0 ,6 3 7 6 0 ,6 0 6 5
1 0 ,9 9 8 8 0 ,9 9 5 3 0 ,9 8 9 8 0 ,9 8 2 5 0 ,9 7 3 5 0 ,9 6 3 1 0 ,9 5 1 3 0 ,9 3 8 4 0 ,9 2 4 6 0 ,9 0 9 8
2 1 ,0 0 0 0 0 ,9 9 9 8 0 ,9 9 9 5 0 ,9 9 8 9 0 ,9 9 7 8 0 ,9 9 6 4 0 ,9 9 4 5 0 ,9 9 2 1 0 ,9 8 9 1 0 ,9 8 5 6
3 1 ,0 0 0 0 1 ,0 0 0 0 1 ,0 0 0 0 0 ,9 9 9 9 0 ,9 9 9 9 0 ,9 9 9 7 0 ,9 9 9 5 0 ,9 9 9 2 0 ,9 9 8 8 0 ,9 9 8 2
4 1 ,0 0 0 0 1 ,0 0 0 0 1 ,0 0 0 0 1 ,0 0 0 0 1 ,0 0 0 0 1 ,0 0 0 0 1 ,0 0 0 0 0 ,9 9 9 9 0 ,9 9 9 9 0 ,9 9 9 8
5 1 ,0 0 0 0 1 ,0 0 0 0 1 ,0 0 0 0 1 ,0 0 0 0 1 ,0 0 0 0 1 ,0 0 0 0 1 ,0 0 0 0 1 ,0 0 0 0 1 ,0 0 0 0 1 ,0 0 0 0
X
0,55 0,6 0,65 0,7 0,75 0,8 0,85 0,9 0,95
0 0 ,5 7 6 9 0 ,5 4 8 8 0 ,5 2 2 0 0 ,4 9 6 6 0 ,4 7 2 4 0 ,4 4 9 3 0 ,4 2 7 4 0 ,4 0 6 6 0 ,3 8 6 7
1 0 ,8 9 4 3 0 ,8 7 8 1 0 ,8 6 1 4 0 ,8 4 4 2 0 ,8 2 6 6 0 ,8 0 8 8 0 ,7 9 0 7 0 ,7 7 2 5 0 ,7 5 4 1
2 0 ,9 8 1 5 0 ,9 7 6 9 0 ,9 7 1 7 0 ,9 6 5 9 0 ,9 5 9 5 0 ,9 5 2 6 0 ,9 4 5 1 0 ,9 3 7 1 0 ,9 2 8 7
3 0 ,9 9 7 5 0 ,9 9 6 6 0 ,9 9 5 6 0 ,9 9 4 2 0 ,9 9 2 7 0 ,9 9 0 9 0 ,9 8 8 9 0 ,9 8 6 5 0 ,9 8 3 9
4 0 ,9 9 9 7 0 ,9 9 9 6 0 ,9 9 9 4 0 ,9 9 9 2 0 ,9 9 8 9 0 ,9 9 8 6 0 ,9 9 8 2 0 ,9 9 7 7 0 ,9 9 7 1
5 1 ,0 0 0 0 1 ,0 0 0 0 0 ,9 9 9 9 0 ,9 9 9 9 0 ,9 9 9 9 0 ,9 9 9 8 0 ,9 9 9 7 0 ,9 9 9 7 0 ,9 9 9 5
6 1 ,0 0 0 0 1 ,0 0 0 0 1 ,0 0 0 0 1 ,0 0 0 0 1 ,0 0 0 0 1 ,0 0 0 0 1 ,0 0 0 0 1 ,0 0 0 0 0 ,9 9 9 9
X
X
1 1,1 1,2 1,3 1,4 1,5 1,6 1,7 1,8 1,9
0 0 ,3 6 7 9 0 ,3 3 2 9 0 ,3 0 1 2 0 ,2 7 2 5 0 ,2 4 6 6 0 ,2 2 3 1 0 ,2 0 1 9 0 ,1 8 2 7 0 ,1 6 5 3 0 ,1 4 9 6
1 0 ,7 3 5 8 0 ,6 9 9 0 0 ,6 6 2 6 0 ,6 2 6 8 0 ,5 9 1 8 0 ,5 5 7 8 0 ,5 2 4 9 0 ,4 9 3 2 0 ,4 6 2 8 0 ,4 3 3 7
2 0 ,9 1 9 7 0 ,9 0 0 4 0 ,8 7 9 5 0 ,8 5 7 1 0 ,8 3 3 5 0 ,8 0 8 8 0 ,7 8 3 4 0 ,7 5 7 2 0 ,7 3 0 6 0 ,7 0 3 7
3 0 ,9 8 1 0 0 ,9 7 4 3 0 ,9 6 6 2 0 ,9 5 6 9 0 ,9 4 6 3 0 ,9 3 4 4 0 ,9 2 1 2 0 ,9 0 6 8 0 ,8 9 1 3 0 ,8 7 4 7
4 0 ,9 9 6 3 0 ,9 9 4 6 0 ,9 9 2 3 0 ,9 8 9 3 0 ,9 8 5 7 0 ,9 8 1 4 0 ,9 7 6 3 0 ,9 7 0 4 0 ,9 6 3 6 0 ,9 5 5 9
5 0 ,9 9 9 4 0 ,9 9 9 0 0 ,9 9 8 5 0 ,9 9 7 8 0 ,9 9 6 8 0 ,9 9 5 5 0 ,9 9 4 0 0 ,9 9 2 0 0 ,9 8 9 6 0 ,9 8 6 8
6 0 ,9 9 9 9 0 ,9 9 9 9 0 ,9 9 9 7 0 ,9 9 9 6 0 ,9 9 9 4 0 ,9 9 9 1 0 ,9 9 8 7 0 ,9 9 8 1 0 ,9 9 7 4 0 ,9 9 6 6
7 1 ,0 0 0 0 1 ,0 0 0 0 1 ,0 0 0 0 0 ,9 9 9 9 0 ,9 9 9 9 0 ,9 9 9 8 0 ,9 9 9 7 0 ,9 9 9 6 0 ,9 9 9 4 0 ,9 9 9 2
8 1 ,0 0 0 0 1 ,0 0 0 0 1 ,0 0 0 0 1 ,0 0 0 0 1 ,0 0 0 0 1 ,0 0 0 0 1 ,0 0 0 0 0 ,9 9 9 9 0 ,9 9 9 9 0 ,9 9 9 8

3 7 6 ESTATÍSTICA
Tabela 2 (Continuação).
X
X
2 2,5 3 4 5 6 7 8 9 10
0 0,1353 0,0821 0,0498 0,0183 0,0067 0,0025 0,0009 0,0003 0,0001 0,0000
1 0,4060 0,2873 0,1991 0,0916 0,0404 0,0174 0,0073 0,0030 0,0012 0,0005
2 0,6767 0,5438 0,4232 0,2381 0,1247 0,0620 0,0296 0,0138 0,0062 0,0028
3 0,8571 0,7576 0,6472 0,4335 0,2650 0,1512 0,0818 0,0424 0,0212 0,0103
4 0,9473 0,8912 0,8153 0,6288 0,4405 0,2851 0,1730 0,0996 0,0550 0,0293
5 0,9834 0,9580 0,9161 0,7851 0,6160 0,4457 0,3007 0,1912 0,1157 0,0671
6 0,9955 0,9858 0,9665 0,8893 0,7622 0,6063 0,4497 0,3134 0,2068 0,1301
7 0,9989 0,9958 0,9881 0,9489 0,8666 0,7440 0,5987 0,4530 0,3239 0,2202
8 0,9998 0,9989 0,9962 0,9786 0,9319 0,8472 0,7291 0,5925 0,4557 0,3328
9 1,0000 0,9997 0,9989 0,9919 0,9682 0,9161 0,8305 0,7166 0,5874 0,4579
10 1,0000 0,9999 0,9997 0,9972 0,9863 0,9574 0,9015 0,8159 0,7060 0,5830
11 1,0000 1,0000 0,9999 0,9991 0,9945 0,9799 0,9467 0,8881 0,8030 0,6968
12 1,0000 1,0000 1,0000 0,9997 0,9980 0,9912 0,9730 0,9362 0,8758 0,7916
13 1,0000 1,0000 1,0000 0,9999 0,9993 0,9964 0,9872 0,9658 0,9261 0,8645
14 1,0000 1,0000 1,0000 1,0000 0,9998 0,9986 0,9943 0,9827 0,9585 0,9165
15 1,0000 1,0000 1,0000 1,0000 0,9999 0,9995 0,9976 0,9918 0,9780 0,9513
16 1,0000 1,0000 1,0000 1,0000 1,0000 0,9998 0,9990 0,9963 0,9889 0,9730
17 1,0000 1,0000 1,0000 1,0000 1,0000 0,9999 0,9996 0,9984 0,9947 0,9857
18 1,0000 1,0000 1,0000 1,0000 1,0000 1,0000 0,9999 0,9993 0,9976 0,9928
19 1,0000 1,0000 1,0000 1,0000 1,0000 1,0000 1,0000 0,9997 0,9989 0,9965
20 1,0000 1,0000 1,0000 1,0000 1,0000 1,0000 1,0000 0,9999 0,9996 0,9984

377
APÊNDICE: TABELAS ESTATÍSTICAS
Tabela 3 Distribuição normal padrão.
o z
Segunda decimal de z
z
0 1 2 3 4 5 6 7 8 9
0,0 0,5000 0,4960 0,4920 0,4880 0,4840 0,4801 0,4761 0,4721 0,4681 0,4641
0,1 0,4602 0,4562 0,4522 0,4483 0,4443 0,4404 0,4364 0,4325 0,4286 0,4247
0,2 0,4207 0,4168 0,4129 0,4090 0,4052 0,4013 0,3974 0,3936 0,3897 0,3859
0,3 0,3821 0,3783 0,3745 0,3707 0,3669 0,3632 0,3594 0,3557 0,3520 0,3483
0,4 0,3446 0,3409 0,3372 0,3336 0,3300 0,3264 0,3228 0,3192 0,3156 0,3121
0,5 0,3085 0,3050 0,3015 0,2981 0,2946 0,2912 0,2877 0,2842 0,2810 0,2776
0,6 0,2743 0,2709 0,2676 0,2643 0,2611 0,2578 0,2546 0,2514 0,2483 0,2451
0,7 0,2420 0,2389 0,2358 0,2327 0,2296 0,2266 0,2236 0,2206 0,2177 0,2148
0,8 0,2119 0,2090 0,2061 0,2033 0,2005 0,1977 0,1949 0,1922 0,1894 0,1867
0,9 0,1841 0,1814 0,1788 0,1762 0,1736 0,1711 0,1685 0,1660 0,1635 0,1611
1,0 0,1587 0,1562 0,1539 0,1515 0,1492 0,1469 0,1446 0,1423 0,1401 0,1379
1,1 0,1357 0,1335 0,1314 0,1292 0,1271 0,1251 0,1230 0,1210 0,1190 0,1170
1,2 0,1151 0,1131 0,1112 0,1093 0,1075 0,1056 0,1038 0,1020 0,1003 0,0985
1,3 0,0968 0,0951 0,0934 0,0918 0,0901 0,0885 0,0869 0,0853 0,0838 0,0823
1,4 0,0808 0,0793 0,0778 0,0764 0,0749 0,0735 0,0722 0,0708 0,0694 0,0681
1,5 0,0668 0,0655 0,0643 0,0630 0,0618 0,0606 0,0594 0,0582 0,0571 0,0559
1,6 0,0548 0,0537 0,0526 0,0516 0,0505 0,0495 0,0485 0,0475 0,0465 0,0455
1,7 0,0446 0,0436 0,0427 0,0418 0,0409 0,0401 0,0392 0,0384 0,0375 0,0367
1,8 0,0359 0,0352 0,0344 0,0336 0,0329 0,0322 0,0314 0,0307 0,0301 0,0294
1,9 0,0287 0,0281 0,0274 0,0268 0,0262 0,0256 0,0250 0,0244 0,0239 0,0233
2,0 0,0228 0,0222 0,0217 0,0212 0,0207 0,0202 0,0197 0,0192 0,0188 0,0183
2,1 0,0179 0,0174 0,0170 0,0166 0,0162 0,0158 0,0154 0,0150 0,0146 0,0143
2,2 0,0139 0,0136 0,0132 0,0129 0,0125 0,0122 0,0119 0,0116 0,0113 0,0110
2,3 0,0107 0,0104 0,0102 0,0099 0,0096 0,0094 0,0091 0,0089 0,0087 0,0084
2,4 0,0082 0,0080 0,0078 0,0075 0,0073 0,0071 0,0069 0,0068 0,0066 0,0064

3 7 8 ESTATÍSTICA
Tabela 3 (Continuação).
Segunda decimal de *
z
0 1 2 3 4 5 6 7 8 9
2,5 0,0062 0,0060 0,0059 0,0057 0,0055 0,0054 0,0052 0,0051 0,0049 0,0048
2,6 0,0047 0,0045 0,0044 0,0043 0,0041 0,0040 0,0039 0,0038 0,0037 0,0036
2,7 0,0035 0,0034 0,0033 0,0032 0,0031 0,0030 0,0029 0,0028 0,0027 0,0026
2,8 0,0026 0,0025 0,0024 0,0023 0,0023 0,0022 0,0021 0,0021 0,0020 0,0019
2,9 0,0019 0,0018 0,0017 0,0017 0,0016 0,0016 0,0015 0,0015 0,0014 0,0014
3,0 0,00135
3,5 0,000 233
4,0 0,000 031 7
4,5 0,000 003 40
5,0 0,000 000 287

APÊNDICE: TABELAS ESTATÍSTICAS 3 7 9
Tabela 4 Distribuição t de Student.
/ j \ área
/ \ indicada
7 1
K .
0 t (valor tabulado)
Área na cauda superior
gl
0,25 0,10 0,05 0,025 0,01 0,005 0,0025 0,001 0,0005
1 1,000 3,078 6,314 12,71 31,82 63,66 127,3 318,3 636,6
2 0,816 1,886 2,920 4,303 6,965 9,925 14,09 22,33 31,60
3 0,765 1,638 2,353 3,182 4,541 5,841 7,453 10,21 12,92
4 0,741 1,533 2,132 2,776 3,747 4,604 5,598 7,173 8,610
5 0,727 1,476 2,015 2,571 3,365 4,032 4,773 5,894 6,869
6 0,718 1,440 1,943 2,447 3,143 3,707 4,317 5,208 5,959
7 0,711 1,415 1,895 2,365 2,998 3,499 4,029 4,785 5,408
8 0,706 1,397 1,860 2,306 2,896 3,355 3,833 4,501 5,041
9 0,703 1,383 1,833 2,262 2,821 3,250 3,690 4,297 4,781
10 0,700 1,372 1,812 2,228 2,764 3,169 3,581 4,144 4,587
11 0,697 1,363 1,796 2,201 2,718 3,106 3,497 4,025 4,437
12 0,695 1,356 1,782 2,179 2,681 3,055 3,428 3,930 4,318
13 0,694 1,350 1,771 2,160 2,650 3,012 3,372 3,852 4,221
14 0,692 1,345 1,761 2,145 2,624 2,977 3,326 3,787 4,140
15 0,691 1,341 1,753 2,131 2,602 2,947 3,286 3,733 4,073
16 0,690 1,337 1,746 2,120 2,583 2,921 3,252 3,686 4,015
17 0,689 1,333 1,740 2,110 2,567 2,898 3,222 3,646 3,965
18 0,688 1,330 1,734 2,101 2,552 2,878 3,197 3,610 3,922
19 0,688 1,328 1,729 2,093 2,539 2,861 3,174 3,579 3,883
20 0,687 1,325 1,725 2,086 2,528 2,845 3,153 3,552 3,850
21 0,686 1,323 1,721 2,080 2,518 2,831 3,135 3,527 3,819
22 0,686 1,321 1,717 2,074 2,508 2,819 3,119 3,505 3,792
23 0,685 1,319 1,714 2,069 2,500 2,807 3,104 3,485 3,768
24 0,685 1,318 1,711 2,064 2,492 2,797 3,091 3,467 3,745
25 0,684 1,316 1,708 2,060 2,485 2,787 3,078 3,450 3,725
26 0,684 1,315 1,706 2,056 2,479 2,779 3,067 3,435 3,707
27 0,684 1,314 1,703 2,052 2,473 2,771 3,057 3,421 3,689
28 0,683 1,313 1,701 2,048 2,467 2,763 3,047 3,408 3,674
29 0,683 1,311 1,699 2,045 2,462 2,756 3,038 3,396 3,660
30 0,683 1,310 1,697 2,042 2,457 2,750 3,030 3,385 3,646
35 0,682 1,306 1,690 2,030 2,438 2,724 2,996 3,340 3,591
40 0,681 1,303 1,684 2,021 2,423 2,704 2,971 3,307 3,551
45 0,680 1,301 1,679 2,014 2,412 2,690 2,952 3,281 3,520
50 0,679 1,299 1,676 2,009 2,403 2,678 2,937 3,261 3,496
z 0,674 1,282 1,645 1,960 2,326 2,576 2,807 3,090 3,291

3 8 0 ESTATÍSTICA
Tabela 5 Distribuição qui-quadrado.
área
indicada
—T------ ■ ►
X (valor tabulado)
Area na cauda superior
gl
0,999 0,9975 0,995 0,99 0,975 0,95 0,9 0,75
1 0,00 0,00 0,00 0,00 0,00 0,00 0,02 0,10
2 0,00 0,01 0,01 0,02 0,05 0,10 0,21 0,58
3 0,02 0,04 0,07 0,11 0,22 0,35 0,58 1,21
4 0,09 0,14 0,21 0,30 0,48 0,71 1,06 1,92
5 0,21 0,31 0,41 0,55 0,83 1,15 1,61 2,67
6 0,38 0,53 0,68 0,87 1,24 1,64 2,20 3,45
7 0,60 0,79 0,99 1,24 1,69 2,17 2,83 4,25
8 0,86 1,10 1,34 1,65 2,18 2,73 3,49 5,07
9 1,15 1,45 1,73 2,09 2,70 3,33 4,17 5,90
10 1,48 1,83 2,16 2,56 3,25 3,94 4,87 6,74
11 1,83 2,23 2,60 3,05 3,82 4,57 5,58 7,58
12 2,21 2,66 3,07 3,57 4,40 5,23 6,30 8,44
13 2,62 3,11 3,57 4,11 5,01 5,89 7,04 9,30
14 3,04 3,58 4,07 4,66 5,63 6,57 7,79 10,17
15 3,48 4,07 4,60 5,23 6,26 7,26 8,55 11,04
16 3,94 4,57 5,14 5,81 6,91 7,96 9,31 11,91
17 4,42 5,09 5,70 6,41 7,56 8,67 10,09 12,79
18 4,90 5,62 6,26 7,01 8,23 9,39 10,86 13,68
19 5,41 6,17 6,84 7,63 8,91 10,12 11,65 14,56
20 5,92 6,72 7,43 8,26 9,59 10,85 12,44 15,45
21 6,45 7,29 8,03 8,90 10,28 11,59 13,24 16,34
22 6,98 7,86 8,64 9,54 10,98 12,34 14,04 17,24
23 7,53 8,45 9,26 10,20 11,69 13,09 14,85 18,14
24 8,08 9,04 9,89 10,86 12,40 13,85 15,66 19,04
25 8,65 9,65 10,52 11,52 13,12 14,61 16,47 19,94
26 9,22 10,26 11,16 12,20 13,84 15,38 17,29 20,84
27 9,80 10,87 11,81 12,88 14,57 16,15 18,11 21,75
28 10,39 11,50 12,46 13,56 15,31 16,93 18,94 22,66
29 10,99 12,13 13,12 14,26 16,05 17,71 19,77 23,57
30 11,59 12,76 13,79 14,95 16,79 18,49 20,60 24,48
35 14,69 16,03 17,19 18,51 20,57 22,47 24,80 29,05
40 17,92 19,42 20,71 22,16 24,43 26,51 29,05 33,66
45 21,25 22,90 24,31 25,90 28,37 30,61 33,35 38,29
50 24,67 26,46 27,99 29,71 32,36 34,76 37,69 42,94
100 61,92 64,86 67,33 70,06 74,22 77,93 82,36 90,13

APÊNDICE: TABELAS ESTATÍSTICAS 3 8 1
Tabela 5 (Continuação).
área
indicada
—7------ ‘ ►
X (valor tabulado)
Área na cauda superior
gl
0,25 0,10 0,05 0,025 0,01 0,005 0,0025 0,001
1 1,32 2,71 3,84 5,02 6,63 7,88 9,14 10,83
2 2,77 4,61 5,99 7,38 9,21 10,60 11,98 13,82
3 4,11 6,25 7,81 9,35 11,34 12,84 14,32 16,27
4 5,39 7,78 9,49 11,14 13,28 14,86 16,42 18,47
5 6,63 9,24 11,07 12,83 15,09 16,75 18,39 20,51
6 7,84 10,64 12,59 14,45 16,81 18,55 20,25 22,46
7 9,04 12,02 14,07 16,01 18,48 20,28 22,04 24,32
8 10,22 13,36 15,51 17,53 20,09 21,95 23,77 26,12
9 11,39 14,68 16,92 19,02 21,67 23,59 25,46 27,88
10 12,55 15,99 18,31 20,48 23,21 25,19 27,11 29,59
11 13,70 17,28 19,68 21,92 24,73 26,76 28,73 31,26
12 14,85 18,55 21,03 23,34 26,22 28,30 30,32 32,91
13 15,98 19,81 22,36 24,74 27,69 29,82 31,88 34,53
14 17,12 21,06 23,68 26,12 29,14 31,32 33,43 36,12
15 18,25 22,31 25,00 27,49 30,58 32,80 34,95 37,70
16 19,37 23,54 26,30 28,85 32,00 34,27 36,46 39,25
17 20,49 24,77 27,59 30,19 33,41 35,72 37,95 40,79
18 21,60 25,99 28,87 31,53 34,81 37,16 39,42 42,31
19 22,72 27,20 30,14 32,85 36,19 38,58 40,88 43,82
20 23,83 28,41 31,41 34,17 37,57 40,00 42,34 45,31
21 24,93 29,62 32,67 35,48 38,93 41,40 43,77 46,80
22 26,04 30,81 33,92 36,78 40,29 42,80 45,20 48,27
23 27,14 32,01 35,17 38,08 41,64 44,18 46,62 49,73
24 28,24 33,20 36,42 39,36 42,98 45,56 48,03 51,18
25 29,34 34,38 37,65 40,65 44,31 46,93 49,44 52,62
26 30,43 35,56 38,89 41,92 45,64 48,29 50,83 54,05
27 31,53 36,74 40,11 43,19 46,96 49,65 52,22 55,48
28 32,62 37,92 41,34 44,46 48,28 50,99 53,59 56,89
29 33,71 39,09 42,56 45,72 49,59 52,34 54,97 58,30
30 34,80 40,26 43,77 46,98 50,89 53,67 56,33 59,70
35 40,22 46,06 49,80 53,20 57,34 60,27 63,08 66,62
40 45,62 51,81 55,76 59,34 63,69 66,77 69,70 73,40
45 50,98 57,51 61,66 65,41 69,96 73,17 76,22 80,08
50 56,33 63,17 67,50 71,42 76,15 79,49 82,66 86,66
100 109,1 118,5 124,3 129,6 135,8 140,2 144,3 149,4

3 8 2 ESTATÍSTICA
Tabela 6 Distribuição F de Snedecor.
a = 0,10
F (valor tabulado)
Graus de liberdade no numerador
s*
denom.
1 2 3 4 5 6 7 8 9 10
1 39,86 49,50 53,59 55,83 57,24 58,20 58,91 59,44 59,86 60,19
2 8,53 9,00 9,16 9,24 9,29 9,33 9,35 9,37 9,38 9,39
3 5,54 5,46 5,39 5,34 5,31 5,28 5,27 5,25 5,24 5,23
4 4,54 4,32 4,19 4,11 4,05 4,01 3,98 3,95 3,94 3,92
5 4,06 3,78 3,62 3,52 3,45 3,40 3,37 3,34 3,32 3,30
6 3,78 3,46 3,29 3,18 3,11 3,05 3,01 2,98 2,96 2,94
7 3,59 3,26 3,07 2,96 2,88 2,83 2,78 2,75 2,72 2,70
8 3,46 3,11 2,92 2,81 2,73 2,67 2,62 2,59 2,56 2,54
9 3,36 3,01 2,81 2,69 2,61 2,55 2,51 2,47 2,44 2,42
10 3,29 2,92 2,73 2,61 2,52 2,46 2,41 2,38 2,35 2,32
11 3,23 2,86 2,66 2,54 2,45 2,39 2,34 2,30 2,27 2,25
12 3,18 2,81 2,61 2,48 2,39 2,33 2,28 2,24 2,21 2,19
13 3,14 2,76 2,56 2,43 2,35 2,28 2,23 2,20 2,16 2,14
14 3,10 2,73 2,52 2,39 2,31 2,24 2,19 2,15 2,12 2,10
15 3,07 2,70 2,49 2,36 2,27 2,21 2,16 2,12 2,09 2,06
16 3,05 2,67 2,46 2,33 2,24 2,18 2,13 2,09 2,06 2,03
17 3,03 2,64 2,44 2,31 2,22 2,15 2,10 2,06 2,03 2,00
18 3,01 2,62 2,42 2,29 2,20 2,13 2,08 2,04 2,00 1,98
19 2,99 2,61 2,40 2,27 2,18 2,11 2,06 2,02 1,98 1,96
20 2,97 2,59 2,38 2,25 2,16 2,09 2,04 2,00 1,96 1,94
21 2,96 2,57 2,36 2,23 2,14 2,08 2,02 1,98 1,95 1,92
22 2,95 2,56 2,35 2,22 2,13 2,06 2,01 1,97 1,93 1,90
23 2,94 2,55 2,34 2,21 2,11 2,05 1,99 1,95 1,92 1,89
24 2,93 2,54 2,33 2,19 2,10 2,04 1,98 1,94 1,91 1,88
25 2,92 2,53 2,32 2,18 2,09 2,02 1,97 1,93 1,89 1,87
26 2,91 2,52 2,31 2,17 2,08 2,01 1,96 1,92 1,88 1,86
27 2,90 2,51 2,30 2,17 2,07 2,00 1,95 1,91 1,87 1,85
28 2,89 2,50 2,29 2,16 2,06 2,00 1,94 1,90 1,87 1,84
29 2,89 2,50 2,28 2,15 2,06 1,99 1,93 1,89 1,86 1,83
30 2,88 2,49 2,28 2,14 2,05 1,98 1,93 1,88 1,85 1,82
35 2,85 2,46 2,25 2,11 2,02 1,95 1,90 1,85 1,82 1,79
40 2,84 2,44 2,23 2,09 2,00 1,93 1,87 1,83 1,79 1,76
45 2,82 2,42 2,21 2,07 1,98 1,91 1,85 1,81 1,77 1,74
50 2,81 2,41 2,20 2,06 1,97 1,90 1,84 1,80 1,76 1,73
100 2,76 2,36 2,14 2,00 1,91 1,83 1,78 1,73 1,69 1,66

383
APÊNDICE: TABELAS ESTATÍSTICAS
Tabela 6 (Continuação).
a = 0,05
Graus de liberdade no numerador
8 l
denom.
1 2 3 4 5 6 7 8 9 10
1 161,45 199,50 215,71 224,58 230,16 233,99 236,77 238,88 240,54 241,88
2 18,51 19,00 19,16 19,25 19,30 19,33 19,35 19,37 19,38 19,40
3 10,13 9,55 9,28 9,12 9,01 8,94 8,89 8,85 8,81 8,79
4 7,71 6,94 6,59 6,39 6,26 6,16 6,09 6,04 6,00 5,96
5 6,61 5,79 5,41 5,19 5,05 4,95 4,88 4,82 4,77 4,74
6 5,99 5,14 4,76 4,53 4,39 4,28 4,21 4,15 4,10 4,06
7 5,59 4,74 4,35 4,12 3,97 3,87 3,79 3,73 3,68 3,64
8 5,32 4,46 4,07 3,84 3,69 3,58 3,50 3,44 3,39 3,35
9 5,12 4,26 3,86 3,63 3,48 3,37 3,29 3,23 3,18 3,14
10 4,96 4,10 3,71 3,48 3,33 3,22 3,14 3,07 3,02 2,98
11 4,84 3,98 3,59 3,36 3,20 3,09 3,01 2,95 2,90 2,85
12 4,75 3,89 3,49 3,26 3,11 3,00 2,91 2,85 2,80 2,75
13 4,67 3,81 3,41 3,18 3,03 2,92 2,83 2,77 2,71 2,67
14 4,60 3,74 3,34 3,11 2,96 2,85 2,76 2,70 2,65 2,60
15 4,54 3,68 3,29 3,06 2,90 2,79 2,71 2,64 2,59 2,54
16 4,49 3,63 3,24 3,01 2,85 2,74 2,66 2,59 2,54 2,49
17 4,45 3,59 3,20 2,96 2,81 2,70 2,61 2,55 2,49 2,45
18 4,41 3,55 3,16 2,93 2,77 2,66 2,58 2,51 2,46 2,41
19 4,38 3,52 3,13 2,90 2,74 2,63 2,54 2,48 2,42 2,38
20 4,35 3,49 3,10 2,87 2,71 2,60 2,51 2,45 2,39 2,35
21 4,32 3,47 3,07 2,84 2,68 2,57 2,49 2,42 2,37 2,32
22 4,30 3,44 3,05 2,82 2,66 2,55 2,46 2,40 2,34 2,30
23 4,28 3,42 3,03 2,80 2,64 2,53 2,44 2,37 2,32 2,27
24 4,26 3,40 3,01 2,78 2,62 2,51 2,42 2,36 2,30 2,25
25 4,24 3,39 2,99 2,76 2,60 2,49 2,40 2,34 2,28 2,24
26 4,23 3,37 2,98 2,74 2,59 2,47 2,39 2,32 2,27 2,22
27 4,21 3,35 2,96 2,73 2,57 2,46 2,37 2,31 2,25 2,20
28 4,20 3,34 2,95 2,71 2,56 2,45 2,36 2,29 2,24 2,19
29 4,18 3,33 2,93 2,70 2,55 2,43 2,35 2,28 2,22 2,18
30 4,17 3,32 2,92 2,69 2,53 2,42 2,33 2,27 2,21 2,16
35 4,12 3,27 2,87 2,64 2,49 2,37 2,29 2,22 2,16 2,11
40 4,08 3,23 2,84 2,61 2,45 2,34 2,25 2,18 2,12 2,08
45 4,06 3,20 2,81 2,58 2,42 2,31 2,22 2,15 2,10 2,05
50 4,03 3,18 2,79 2,56 2,40 2,29 2,20 2,13 2,07 2,03
100 3,94 3,09 2,70 2,46 2,31 2,19 2,10 2,03 1,97 1,93

3 8 4 ESTATÍSTICA
Tabela 6 (Continuação).
a = 0,025
Graus de liberdade no numerador
gl
denom.
1 2 3 4 5 6 7 8 9 10
1 647,79 799,48 864,15 899,60 921,83 937,11 948,20 956,64 963,28 968,63
2 38,51 39,00 39,17 39,25 39,30 39,33 39,36 39,37 39,39 39,40
3 17,44 16,04 15,44 15,10 14,88 14,73 14,62 14,54 14,47 14,42
4 12,22 10,65 9,98 9,60 9,36 9,20 9,07 8,98 8,90 8,84
5 10,01 8,43 7,76 7,39 7,15 6,98 6,85 6,76 6,68 6,62
6 8,81 7,26 6,60 6,23 5,99 5,82 5,70 5,60 5,52 5,46
7 8,07 6,54 5,89 5,52 5,29 5,12 4,99 4,90 4,82 4,76
8 7,57 6,06 5,42 5,05 4,82 4,65 4,53 4,43 4,36 4,30
9 7,21 5,71 5,08 4,72 4,48 4,32 4,20 4,10 4,03 3,96
10 6,94 5,46 4,83 4,47 4,24 4,07 3,95 3,85 3,78 3,72
11 6,72 5,26 4,63 4,28 4,04 3,88 3,76 3,66 3,59 3,53
12 6,55 5,10 4,47 4,12 3,89 3,73 3,61 3,51 3,44 3,37
13 6,41 4,97 4,35 4,00 3,77 3,60 3,48 3,39 3,31 3,25
14 6,30 4,86 4,24 3,89 3,66 3,50 3,38 3,29 3,21 3,15
15 6,20 4,77 4,15 3,80 3,58 3,41 3,29 3,20 3,12 3,06
16 6,12 4,69 4,08 3,73 3,50 3,34 3,22 3,12 3,05 2,99
17 6,04 4,62 4,01 3,66 3,44 3,28 3,16 3,06 2,98 2,92
18 5,98 4,56 3,95 3,61 3,38 3,22 3,10 3,01 2,93 2,87
19 5,92 4,51 3,90 3,56 3,33 3,17 3,05 2,96 2,88 2,82
20 5,87 4,46 3,86 3,51 3,29 3,13 3,01 2,91 2,84 2,77
21 5,83 4,42 3,82 3,48 3,25 3,09 2,97 2,87 2,80 2,73
22 5,79 4,38 3,78 3,44 3,22 3,05 2,93 2,84 2,76 2,70
23 5,75 4,35 3,75 3,41 3,18 3,02 2,90 2,81 2,73 2,67
24 5,72 4,32 3,72 3,38 3,15 2,99 2,87 2,78 2,70 2,64
25 5,69 4,29 3,69 3,35 3,13 2,97 2,85 2,75 2,68 2,61
26 5,66 4,27 3,67 3,33 3,10 2,94 2,82 2,73 2,65 2,59
27 5,63 4,24 3,65 3,31 3,08 2,92 2,80 2,71 2,63 2,57
28 5,61 4,22 3,63 3,29 3,06 2,90 2,78 2,69 2,61 2,55
29 5,59 4,20 3,61 3,27 3,04 2,88 2,76 2,67 2,59 2,53
30 5,57 4,18 3,59 3,25 3,03 2,87 2,75 2,65 2,57 2,51
35 5,48 4,11 3,52 3,18 2,96 2,80 2,68 2,58 2,50 2,44
40 5,42 4,05 3,46 3,13 2,90 2,74 2,62 2,53 2,45 2,39
45 5,38 4,01 3,42 3,09 2,86 2,70 2,58 2,49 2,41 2,35
50 5,34 3,97 3,39 3,05 2,83 2,67 2,55 2,46 2,38 2,32
100 5,18 3,83 3,25 2,92 2,70 2,54 2,42 2,32 2,24 2,18

APÊNDICE: TABELAS ESTATÍSTICAS 3 8 5
Tabela 6 (Continuação).
a = 0,01
F (valor tabulado)
Graus de liberdade no numerador
8 l
denom.
1 2 3 4 5 6 7 8 9 10
1 4.052,2 4.999,3 5.403,5 5.624,3 5.764,0 5.859,0 5.928,3 5.981,0 6.022,4 6.055,9
2 98,50 99,00 99,16 99,25 99,30 99,33 99,36 99,38 99,39 99,40
3 34,12 30,82 29,46 28,71 28,24 27,91 27,67 27,49 27,34 7,23
4 21,20 18,00 16,69 15,98 15,52 15,21 14,98 14,80 14,66 14,55
5 16,26 13,27 12,06 11,39 10,97 10,67 10,46 10,29 10,16 10,05
6 13,75 10,92 9,78 9,15 8,75 8,47 8,26 8,10 7,98 7,87
7 12,25 9,55 8,45 7,85 7,46 7,19 6,99 6,84 6,72 6,62
8 11,26 8,65 7,59 7,01 6,63 6,37 6,18 6,03 5,91 5,81
9 10,56 8,02 6,99 6,42 6,06 5,80 5,61 5,47 5,35 5,26
10 10,04 7,56 6,55 5,99 5,64 5,39 5,20 5,06 4,94 4,85
11 9,65 7,21 6,22 5,67 5,32 5,07 4,89 4,74 4,63 4,54
12 9,33 6,93 5,95 5,41 5,06 4,82 4,64 4,50 4,39 4,30
13 9,07 6,70 5,74 5,21 4,86 4,62 4,44 4,30 4,19 4,10
14 8,86 6,51 5,56 5,04 4,69 4,46 4,28 4,14 4,03 3,94
15 8,68 6,36 5,42 4,89 4,56 4,32 4,14 4,00 3,89 3,80
16 8,53 6,23 5,29 4,77 4,44 4,20 4,03 3,89 3,78 3,69
17 8,40 6,11 5,19 4,67 4,34 4,10 3,93 3,79 3,68 3,59
18 8,29 6,01 5,09 4,58 4,25 4,01 3,84 3,71 3,60 3,51
19 8,18 5,93 5,01 4,50 4,17 3,94 3,77 3,63 3,52 3,43
20 8,10 5,85 4,94 4,43 4,10 3,87 3,70 3,56 3,46 3,37
21 8,02 5,78 4,87 4,37 4,04 3,81 3,64 3,51 3,40 3,31
22 7,95 5,72 4,82 4,31 3,99 3,76 3,59 3,45 3,35 3,26
23 7,88 5,66 4,76 4,26 3,94 3,71 3,54 3,41 3,30 3,21
24 7,82 5,61 4,72 4,22 3,90 3,67 3,50 3,36 3,26 3,17
25 7,77 5,57 4,68 4,18 3,85 3,63 3,46 3,32 3,22 3,13
26 7,72 5,53 4,64 4,14 3,82 3,59 3,42 3,29 3,18 3,09
27 7,68 5,49 4,60 4,11 3,78 3,56 3,39 3,26 3,15 3,06
28 7,64 5,45 4,57 4,07 3,75 3,53 3,36 3,23 3,12 3,03
29 7,60 5,42 4,54 4,04 3,73 3,50 3,33 3,20 3,09 3,00
30 7,56 5,39 4,51 4,02 3,70 3,47 3,30 3,17 3,07 2,98
35 7,42 5,27 4,40 3,91 3,59 3,37 3,20 3,07 2,96 2,88
40 7,31 5,18 4,31 3,83 3,51 3,29 3,12 2,99 2,89 2,80
45 7,23 5,11 4,25 3,77 3,45 3,23 3,07 2,94 2,83 2,74
50 7,17 5,06 4,20 3,72 3,41 3,19 3,02 2,89 2,78 2,70
100 6,90 4,82 3,98 3,51 3,21 2,99 2,82 2,69 2,59 2,50

386
ESTATÍSTICA
Tabela 7 Valores críticos (dc) para os testes de Kolmogorov-Smimov e Lilliefors.
Kolmogorov-Smimov: Lilliefors:
parâmetros conhecidos parâmetros estimados
n = 5% a = 1% n a = 5% a = 1%
a
1 0,975 0,995 4 0,381 0,417
2 0,842 0,929 5 0,337 0,405
3 0,708 0,829 6 0,319 0,364
4 0,624 0,734 7 0,300 0,348
5 0,563 0,669 8 0,285 0,331
6 0,519 0,617 9 0,271 0,311
7 0,483 0,576 10 0,258 0,294
8 0,454 0,542 11 0,249 0,284
9 0,430 0,513 12 0,242 0,275
10 0,409 0,490 13 0,234 0,268
11 0,391 0,468 14 0,227 0,261
12 0,375 0,449 15 0,220 0,257
13 0,361 0,432 16 0,213 0,250
14 0,349 0,418 17 0,206 0,245
15 0,338 0,404 18 0,200 0,239
16 0,327 0,392 19 0,179 0,235
17 0,318 0,381 20 0,190 0,231
18 0,309 0,371 25 0,173 0,200
19 0,301 0,361 30 0,161 0,187
20 0,294 0,352 n > 30 dc = 0,886 vn dc = 1,031 /4n
25 0,264 0,317
30 0,242 0,290
35 0,224 0,269
40 0,210 0,252
45 0,198 0,238
50 0,188 0,227
n > 50 dc = 1,36 \ dc = 1,63 <n
ti

Tabela 8 Escores limites para a estatística do teste de sinais por postos (Wilcoxon).
P(S+ < aproximadamente igual a
Sc)
ti
0,005 0,01 0,025 0,05 0,1 0,2 0,3 0,4 0,5 0,6 0,7 0,8 0,9 0,95 0,975 0,99 0,995
4 0 0 0 0 1 3 3 4 5 6 7 7 9 10 10 10 10
5 0 0 0 1 3 4 5 6 7.5 9 10 11 12 14 15 15 15
6 0 0 1 3 4 6 8 9 10.5 12 13 15 17 18 20 21 21
7 0 1 3 4 6 9 11 12 14 16 17 19 22 24 25 27 28
8 1 2 4 6 9 12 14 16 18 20 22 24 27 30 32 34 35
9 2 4 6 9 11 15 18 20 22.5 25 27 30 34 36 39 41 43
10 4 6 9 11 15 19 22 25 27.5 30 33 36 40 44 46 49 51
11 6 8 11 14 18 23 27 30 33 36 39 43 48 52 55 58 60
12 8 10 14 18 22 28 32 36 39 42 46 50 56 60 64 68 70
13 10 13 18 22 27 33 38 42 45.5 49 53 58 64 69 73 78 81
14 13 16 22 26 32 39 44 48 52.5 57 61 66 73 79 83 89 92
15 16 20 26 31 37 45 51 55 60 65 69 75 83 89 94 100 104
16 20 24 30 36 43 51 58 63 68 73 78 85 93 100 106 112 116
17 24 28 35 42 49 58 65 71 76.5 82 88 95 104 111 118 125 129
18 28 33 41 48 56 66 73 80 85.5 91 98 105 115 123 130 138 143
19 33 38 47 54 63 74 82 89 95 101 108 116 127 136 143 152 157
20 38 44 53 61 70 82 91 98 105 112 119 128 140 149 157 166 172
APÊNDICE:
TABELAS
ESTATÍSTICAS
387

3 8 8 ESTATÍSTICA
Tabela 9 Escores limites para a estatística U do teste de Mann-Whitney.
Tlj = 2 < c) aproximadamente igual a
P ( l/ u
«2 0,001 0,005 0,01 0,025 0,05 0,1 0,9 0,95 0,975 0,99 0,995 0,999
2 0 0 0 0 0 0 4 4 4 4 4 4
3 0 0 0 0 0 5 6 6 6 6 6
1
4 0 0 0 0 0 7 8 8 8 8 8
1
5 0 0 0 0 1 2 8 9 10 10 10 10
6 0 0 0 0 1 2 10 11 12 12 12 12
7 0 0 0 0 1 2 12 13 14 14 14 14
8 0 0 0 1 2 3 13 14 15 16 16 16
9 0 0 0 1 2 3 15 16 17 18 18 18
10 0 0 0 1 2 4 16 18 19 20 20 20
11 0 0 0 1 2 4 18 20 21 22 22 22
12 0 0 0 2 3 5 19 21 22 24 24 24
13 0 0 1 2 3 5 21 23 24 25 26 26
14 0 0 1 2 4 5 23 24 26 27 28 28
15 0 0 1 2 4 6 24 26 28 29 30 30
16 0 0 1 2 4 6 26 29 30 31 32 32
17 0 0 1 3 4 7 27 30 31 33 34 34
18 0 0 1 3 5 7 29 31 33 35 36 36
19 0 1 2 3 5 8 30 33 36 36 37 38
20 0 2 3 5 8 32 35 37 38 39 40
1

APÊNDICE: TABELAS ESTATÍSTICAS 3 8 9
Tabela 9 (Continuação).
Tl1 = 3 P(17 < uc) aproximadamente igual a
n2 0,001 0,005 0,01 0,025 0,05 0,1 0,9 0,95 0,975 0,99 0,995 0,999
2 0 0 0 0 0 1 5 6 6 6 6 6
3 0 0 0 0 1 2 7 8 9 9 9 9
4 0 0 0 0 1 2 10 11 12 12 12 12
5 0 0 0 1 2 3 12 13 14 15 15 15
6 0 0 0 2 3 4 14 15 16 18 18 18
7 0 0 1 2 3 5 16 18 19 20 21 21
8 0 0 1 3 4 6 18 20 21 23 24 24
9 0 0 2 3 5 6 21 22 24 25 26 27
10 0 1 2 4 5 7 23 25 26 28 29 30
11 0 1 2 4 6 8 25 27 29 31 32 33
12 0 2 3 5 6 9 27 30 31 33 34 36
13 0 2 3 5 7 10 29 32 34 36 37 39
14 0 2 3 6 8 11 31 34 36 39 40 42
15 0 3 4 6 8 11 34 37 39 41 42 45
16 0 3 4 7 9 12 36 39 41 44 45 48
17 1 3 5 7 10 13 38 41 44 46 48 50
18 1 3 5 8 10 14 40 44 46 49 51 53
19 1 4 5 8 11 15 42 46 49 52 53 55
20 1 4 6 9 12 16 44 48 51 54 56 59

3 9 0 ESTATÍSTICA
Tabela 9 (Continuação).
n, = 4 P(l/ < uc) aproximadamente igual a
«2 0,001 0,005 0,01 0,025 0,05 0,1 0,9 0,95 0,975 0,99 0,995 0,999
2 0 0 0 0 0 1 7 8 8 8 8 8
3 0 0 0 0 1 2 10 11 12 12 12 12
4 0 0 0 1 2 4 12 14 15 16 16 16
5 0 0 1 2 3 5 15 17 18 19 20 20
6 0 1 2 3 4 6 18 20 21 22 23 24
7 0 1 2 4 5 7 21 23 24 26 27 28
8 0 2 3 5 6 8 24 26 27 29 30 32
9 0 2 4 5 7 10 26 29 31 32 34 36
10 1 3 4 6 8 11 29 32 34 36 37 39
11 1 3 5 7 9 12 32 35 37 39 41 43
12 1 4 6 8 10 13 35 38 40 42 44 47
13 2 4 6 9 11 14 38 41 43 46 48 50
14 2 5 7 10 12 16 40 44 46 49 51 54
15 2 6 8 11 13 17 43 47 49 52 54 58
16 3 6 8 12 15 18 46 49 52 56 58 61
17 3 7 9 12 16 19 49 52 56 59 61 65
18 4 7 10 13 17 21 51 55 59 62 65 68
19 4 8 10 14 18 22 54 58 62 66 68 72
20 4 9 11 15 19 23 57 61 65 69 71 76

APÊNDICE: TABELAS ESTATÍSTICAS 3 9 1
Tabela 9 (Continuação).
n 1 = 5 P(U < uc) aproximadamente igual a
n2 0,001 0,005 0,01 0,025 0,05 0,1 0,9 0,95 0,975 0,99 0,995 0,999
2 0 0 0 0 1 2 8 9 10 10 10 10
3 0 0 0 1 2 3 12 13 14 15 15 15
4 0 0 1 2 3 5 15 17 18 19 20 20
5 0 1 2 3 5 6 19 20 22 23 24 25
6 0 2 3 4 6 8 22 24 26 27 28 30
7 0 2 4 6 7 9 26 28 29 31 33 35
8 1 3 5 7 8 11 29 31 33 35 37 39
9 2 4 6 8 10 13 32 35 37 39 41 43
10 2 5 7 9 12 14 36 38 41 43 45 48
11 3 6 8 10 13 16 39 42 45 47 49 52
12 3 7 9 12 14 18 42 46 48 51 53 57
13 4 8 10 13 16 19 46 49 52 55 57 61
14 4 8 11 14 17 21 49 53 56 59 62 66
15 5 9 12 15 19 23 52 56 60 63 66 70
16 6 10 13 16 20 24 56 60 64 67 70 74
17 6 11 14 18 21 26 59 64 67 71 74 79
18 7 12 15 19 23 28 62 67 71 75 78 83
19 8 13 16 20 24 29 66 71 75 79 82 87
20 8 14 17 21 26 31 69 74 79 83 86 92

3 9 2 ESTATÍSTICA
Tabela 9 (Continuação).
tij = 6 P(l/ < uc) aproximadamente igual a
«2 0,001 0,005 0,01 0,025 0,05 0,1 0,9 0,95 0,975 0,99 0,995 0,999
2 0 0 0 0 1 2 10 11 12 12 12 12
3 0 0 0 2 3 4 14 15 16 18 18 18
4 0 1 2 3 4 6 18 20 21 22 23 24
5 0 2 3 4 6 8 22 24 26 27 28 30
6 0 3 4 6 8 10 26 28 30 32 33 36
7 0 4 5 7 9 12 30 33 35 37 38 42
8 2 5 7 9 11 14 34 37 39 41 43 46
9 3 6 8 11 13 16 38 41 43 46 48 51
10 4 7 9 12 15 18 42 45 48 51 53 56
11 5 8 10 14 17 20 46 49 52 56 58 61
12 5 10 12 15 18 22 50 54 57 60 62 67
13 6 11 13 17 20 24 54 58 61 65 67 72
14 7 12 14 18 22 26 58 62 66 70 72 77
15 8 13 16 20 24 28 62 66 70 74 77 82
16 9 14 17 22 26 30 66 70 74 79 82 87
17 10 16 19 23 27 32 70 75 79 83 86 92
18 11 17 20 25 29 35 73 79 83 88 91 97
19 12 18 21 26 31 37 77 83 88 93 96 102
20 13 19 23 28 33 39 81 87 92 97 101 107

APÊNDICE: TABELAS ESTATÍSTICAS 39 3
Tabela 9 (Continuação).
ni = 7 P(U < uc) aproximadamente igual a
n2 0,001 0,005 0,01 0,025 0,05 0,1 0,9 0,95 0,975 0,99 0,995 0,999
2 0 0 0 0 1 2 12 13 14 14 14 14
3 0 0 1 2 3 5 16 18 19 20 21 21
4 0 1 2 4 5 7 21 23 24 26 27 28
5 0 2 4 6 7 9 26 28 29 31 33 35
6 1 4 5 7 9 12 30 33 35 37 38 41
7 2 5 7 9 12 14 35 37 40 42 44 47
8 3 7 8 11 14 17 39 42 45 48 49 53
9 4 8 10 13 16 19 44 47 50 53 55 59
10 6 10 12 15 18 22 48 52 55 58 60 64
11 7 11 13 17 20 24 53 57 60 64 66 70
12 8 13 15 19 22 27 57 62 65 69 71 76
13 9 14 17 21 25 29 62 66 70 74 77 82
14 10 16 18 23 27 32 66 71 75 80 82 88
15 11 17 20 25 29 34 71 76 80 85 88 94
16 12 19 22 27 31 37 75 81 85 90 93 100
17 14 20 24 29 34 39 80 85 90 95 99 105
18 15 22 25 31 36 42 84 90 95 101 104 111
19 16 23 27 33 38 44 89 95 100 106 110 117
20 17 25 29 35 40 47 93 100 105 111 115 123

3 9 4 ESTATÍSTICA
Tabela 9 (Continuação).
Tlj = 8 P(l/ < uc) aproximadamente igual a
«2 0,001 0,005 0,01 0,025 0,05 0,1 0,9 0,95 0,975 0,99 0,995 0,999
2 0 0 0 1 2 3 13 14 15 16 16 16
3 0 0 1 3 4 6 18 20 21 23 24 24
4 0 2 3 5 6 8 24 26 27 29 30 32
5 1 3 5 7 9 11 29 31 33 35 37 39
6 2 5 7 9 11 14 34 37 39 41 43 46
7 3 7 8 11 14 17 39 42 45 48 49 53
8 5 8 10 14 16 20 44 48 50 54 56 59
9 6 10 12 16 19 23 49 53 56 60 62 66
10 7 12 14 18 21 25 55 59 62 66 68 73
11 9 14 16 20 24 28 60 64 68 72 74 79
12 10 16 18 23 27 31 65 69 73 78 80 86
13 12 18 21 25 29 34 70 75 79 83 86 92
14 13 19 23 27 32 37 75 80 85 89 93 99
15 15 21 25 30 34 40 80 86 90 95 99 105
16 16 23 27 32 37 43 85 91 96 101 105 112
17 18 25 29 35 40 46 90 96 101 107 111 118
18 19 27 31 37 42 49 95 102 107 113 117 125
19 21 29 33 39 45 52 100 107 113 119 123 131
20 22 31 35 42 48 55 105 112 118 125 129 138

APÊNDICE: TABELAS ESTATÍSTICAS 39 5
Tabela 9 (Continuação).
n, = 9 P(U < uc) aproximadamente igual a
n2 0,001 0,005 0,01 0,025 0,05 0,1 0,9 0,95 0,975 0,99 0,995 0,999
2 0 0 0 1 2 3 15 16 17 18 18 18
3 0 1 2 3 5 6 21 22 24 25 26 27
4 0 2 4 5 7 10 26 29 31 32 34 36
5 2 4 6 8 10 13 32 35 37 39 41 43
6 3 6 8 11 13 16 38 41 43 46 48 51
7 4 8 10 13 16 19 44 47 50 53 55 59
8 6 10 12 16 19 23 49 53 56 60 62 66
9 8 12 15 18 22 26 55 59 63 66 69 73
10 9 14 17 21 25 29 61 65 69 73 76 81
11 11 17 19 24 28 32 67 71 75 80 82 88
12 13 19 22 27 31 36 72 77 81 86 89 95
13 15 21 24 29 34 39 78 83 88 93 96 102
14 16 23 27 32 37 42 84 89 94 99 103 110
15 18 25 29 35 40 46 89 95 100 106 110 117
16 20 28 32 38 43 49 95 101 106 112 116 124
17 22 30 34 40 46 53 100 107 113 119 123 131
18 24 32 37 43 49 56 106 113 119 125 130 138
19 26 34 39 46 52 59 112 119 125 132 137 145
20 27 37 41 49 55 63 117 125 131 139 143 153

3 9 6 ESTATÍSTICA
Tabela 9 (Continuação).
n 1 = 10 P(LT < uc) aproximadamente igual a
n2 0,001 0,005 0,01 0,025 0,05 0,1 0,9 0,95 0,975 0,99 0,995 0,999
2 0 0 0 1 2 4 16 18 19 20 20 20
3 0 1 2 4 5 7 23 25 26 28 29 30
4 1 3 4 6 8 11 29 32 34 36 37 39
5 2 5 7 9 12 14 36 38 41 43 45 48
6 4 7 9 12 15 18 42 45 48 51 53 56
7 6 10 12 15 18 22 48 52 55 58 60 64
8 7 12 14 18 21 25 55 59 62 66 68 73
9 9 14 17 21 25 29 61 65 69 73 76 81
10 11 17 20 24 28 33 67 72 76 80 83 89
11 13 19 23 27 32 37 73 78 83 87 91 97
12 15 22 25 30 35 40 80 85 90 95 98 105
13 18 25 28 34 38 44 86 92 96 102 105 112
14 20 27 31 37 42 48 92 98 103 109 113 120
15 22 30 34 40 45 52 98 105 110 116 120 128
16 24 32 37 43 49 55 105 111 117 123 128 136
17 26 35 39 46 52 59 111 118 124 131 135 144
18 28 38 42 49 56 63 117 124 131 138 142 152
19 30 40 45 53 59 67 123 131 137 145 150 160
20 33 43 48 56 63 71 129 137 144 15220 157 167

APÊNDICE: TABELAS ESTATÍSTICAS 3 9 7
Tabela 9 (Continuação).
n, = 11 P(U < uc) aproximadamente igual a
n2 0,001 0,005 0,01 0,025 0,05 0,1 0,9 0,95 0,975 0,99 0,995 0,999
2 0 0 0 1 2 4 18 20 21 22 22 22
3 0 1 2 4 6 8 25 27 29 31 32 33
4 1 3 5 7 9 12 32 35 37 39 41 43
5 3 6 8 10 13 16 39 42 45 47 49 52
6 5 8 10 14 17 20 46 49 52 56 58 61
7 7 11 13 17 20 24 53 57 60 64 66 70
8 9 14 16 20 24 28 60 64 68 72 74 79
9 11 17 19 24 28 32 67 71 75 80 82 88
10 13 19 23 27 32 37 73 78 83 87 91 97
11 16 22 26 31 35 41 80 86 90 95 99 105
12 18 25 29 34 39 45 87 93 98 103 107 114
13 21 28 32 38 43 49 94 100 105 111 115 122
14 23 31 35 41 47 53 101 107 113 119 123 131
15 25 34 38 45 51 58 107 114 120 127 131 140
16 28 37 42 48 55 62 114 121 128 134 139 148
17 30 40 45 52 58 66 121 129 135 142 147 157
18 33 43 48 56 62 70 128 136 142 150 155 165
19 35 46 51 59 66 74 135 143 150 158 163 174
20 38 49 54 63 70 79 141 150 157 166 171 182

3 9 8 ESTATÍSTICA
Tabela 9 (Continuação).
rta = 12 P(l/ < uc) aproximadamente igual a
«2 0,001 0,005 0,01 0,025 0,05 0,1 0,9 0,95 0,975 0,99 0,995 0,999
2 0 0 0 2 3 5 19 21 22 24 24 24
3 0 2 3 5 6 9 27 30 31 33 34 36
4 1 4 6 8 10 13 35 38 40 42 44 47
5 3 7 9 12 14 18 42 46 48 51 53 57
6 5 10 12 15 18 22 50 54 57 60 62 67
7 8 13 15 19 22 27 57 62 65 69 71 76
8 10 16 18 23 27 31 65 69 73 78 80 86
9 13 19 22 27 31 36 72 77 81 86 89 95
10 15 22 25 30 35 40 80 85 90 95 98 105
11 18 25 29 34 39 45 87 93 98 103 107 114
12 21 28 32 38 43 50 94 101 106 112 116 123
13 24 32 36 42 48 54 102 108 114 120 124 132
14 26 35 39 46 52 59 109 116 122 129 133 142
15 29 38 43 50 56 64 116 124 130 137 142 151
16 32 42 47 54 61 68 124 131 138 145 150 160
17 35 45 50 58 65 73 131 139 146 154 159 169
18 38 48 54 62 69 78 138 147 154 162 168 178
19 41 52 57 66 73 82 146 155 162 171 176 187
20 43 55 61 70 78 87 153 162 170 179 185 197

APÊNDICE: TABELAS ESTATÍSTICAS 3 9 9
Tabela 9 (Continuação).
tij = 13 P(U < uc) aproximadamente igual a
n2 0,001 0,005 0,01 0,025 0,05 0,1 0,9 0,95 0,975 0,99 0,995 0,999
2 0 0 1 2 3 5 21 23 24 25 26 26
3 0 2 3 5 7 10 29 32 34 36 37 39
4 2 4 6 9 11 14 38 41 43 46 48 50
5 4 8 10 13 16 19 46 49 52 55 57 61
6 6 11 13 17 20 24 54 58 61 65 67 72
7 9 14 17 21 25 29 62 66 70 74 77 82
8 12 18 21 25 29 34 70 75 79 83 86 92
9 15 21 24 29 34 39 78 83 88 93 96 102
10 18 25 28 34 38 44 86 92 96 102 105 112
11 21 28 32 38 43 49 94 100 105 111 115 122
12 24 32 36 42 48 54 102 108 114 120 124 132
13 27 35 40 46 52 59 110 117 123 129 134 142
14 30 39 44 51 57 64 118 125 131 138 143 152
15 33 43 48 55 62 69 126 133 140 147 152 162
16 36 46 52 60 66 75 133 142 148 156 162 172
17 39 50 56 64 71 80 141 150 157 165 171 182
18 43 54 60 68 76 85 149 158 166 174 180 191
19 46 58 64 73 81 90 157 166 174 183 189 201
20 49 61 68 77 85 95 165 175 183 192 199 211

4 0 0 ESTATÍSTICA
Tabela 9 (Continuação).
n 1 = 14 P(l/ < uc) aproximadamente igual a
n2 0,001 0,005 0,01 0,025 0,05 0,1 0,9 0,95 0,975 0,99 0,995 0,999
2 0 0 1 2 4 5 23 24 26 27 28 28
3 0 2 3 6 8 11 31 34 36 39 40 42
4 2 5 7 10 12 16 40 44 46 49 51 54
5 4 8 11 14 17 21 49 53 56 59 62 66
6 7 12 14 18 22 26 58 62 66 70 72 77
7 10 16 18 23 27 32 66 71 75 80 82 88
8 13 19 23 27 32 37 75 80 85 89 93 99
9 16 23 27 32 37 42 84 89 94 99 103 110
10 20 27 31 37 42 48 92 98 103 109 113 120
11 23 31 35 41 47 53 101 107 113 119 123 131
12 26 35 39 46 52 59 109 116 122 129 133 142
13 30 39 44 51 57 64 118 125 131 138 143 152
14 33 43 48 56 62 70 126 134 140 148 153 163
15 37 57 52 60 67 75 135 143 150 158 163 173
16 40 51 57 65 72 81 143 152 159 167 173 184
17 44 55 61 70 78 86 152 160 168 177 183 194
18 47 59 66 75 83 92 160 169 177 186 193 205
19 51 64 70 79 88 98 168 178 187 196 202 215
20 55 68 74 84 93 103 177 187 196 206 212 225

APÊNDICE: TABELAS ESTATÍSTICAS 4 0 1
Tabela 9 (Continuação).
n, = 15 P(U < uc) aproximadamente igual a
n2 0,001 0,005 0,01 0,025 0,05 0,1 0,9 0,95 0,975 0,99 0,995 0,999
2 0 0 1 2 4 6 24 26 28 29 30 30
3 0 3 4 6 8 11 34 37 39 41 42 45
4 2 6 8 11 13 17 43 47 49 52 54 58
5 5 9 12 15 19 23 52 56 60 63 66 70
6 8 13 16 20 24 28 62 66 70 74 77 82
7 11 17 20 25 29 34 71 76 80 85 88 94
8 15 21 25 30 34 40 80 86 90 95 99 105
9 18 25 29 35 40 46 89 95 100 106 110 117
10 22 30 34 40 45 52 98 105 110 116 120 128
11 25 34 38 45 51 58 107 114 120 127 131 140
12 29 38 43 50 56 64 116 124 130 137 142 151
13 33 43 48 55 62 69 126 133 140 147 152 162
14 37 47 52 60 67 75 135 143 150 158 163 173
15 41 521 57 65 73 81 144 152 160 168 173 184
16 44 56 62 71 78 87 153 162 169 178 184 196
17 48 61 67 76 84 93 162 171 179 188 194 207
18 52 65 71 81 89 99 171 181 189 199 205 218
19 56 70 76 86 95 105 180 190 199 209 215 229
20 60 74 81 91 101 111 189 199 209 219 226 240

4 0 2 ESTATÍSTICA
Tabela 9 (Continuação).
rtj = 16 P(l/ < uc) aproximadamente igual a
n2 0,001 0,005 0,01 0,025 0,05 0,1 0,9 0,95 0,975 0,99 0,995 0,999
2 0 0 1 2 4 6 26 28 30 31 32 32
3 0 3 4 7 9 12 36 39 41 44 45 48
4 3 6 8 12 15 18 46 49 52 56 58 61
5 6 10 13 16 20 24 56 60 64 67 70 74
6 9 14 17 22 26 30 66 70 74 79 82 87
7 12 19 22 27 31 37 75 81 85 90 93 100
8 16 23 27 32 37 43 85 91 96 101 105 112
9 20 28 32 38 43 49 95 101 106 112 116 124
10 24 32 37 43 43 55 105 111 117 123 128 136
11 28 37 42 48 55 62 114 121 128 134 139 148
12 32 42 47 54 61 68 124 131 138 145 150 160
13 36 46 52 60 66 75 133 142 148 156 162 172
14 40 51 57 65 72 81 143 152 159 167 173 184
15 44 56 62 71 78 87 153 162 169 178 184 196
16 49 61 67 76 84 94 162 172 180 189 195 207
17 53 66 72 82 90 100 172 182 190 200 206 219
18 57 71 77 87 96 107 181 192 201 211 217 231
19 61 75 83 93 102 113 191 202 211 221 229 243
20 66 80 88 99 108 120 200 212 221 232 240 254

APÊNDICE: TABELAS ESTATÍSTICAS 4 0 3
Tabela 9 (Continuação).
rij = 17 P(U < uc) aproximadamente igual a
n2 0,001 0,005 0,01 0,025 0,05 0,1 0,9 0,95 0,975 0,99 0,995 0,999
2 0 0 1 3 4 7 27 30 31 33 34 34
3 1 3 5 7 10 13 38 41 44 46 48 50
4 3 7 9 12 16 19 49 52 56 59 61 65
5 6 11 14 18 21 26 59 64 67 71 74 79
6 10 16 19 23 27 32 70 75 79 83 86 92
7 14 20 24 29 34 39 80 85 90 95 99 105
8 18 25 29 35 40 46 90 96 101 107 111 118
9 22 30 34 40 46 53 100 107 113 119 123 131
10 26 35 39 46 52 59 111 118 124 131 135 144
11 30 40 45 52 58 66 121 129 135 142 147 157
12 35 45 50 58 65 73 131 139 146 154 159 169
13 39 50 56 64 71 80 141 150 157 165 171 182
14 44 55 61 70 78 86 152 160 168 177 183 194
15 48 61 67 76 84 93 162 171 179 188 194 207
16 53 66 72 82 90 100 172 182 190 200 206 219
17 58 71 78 88 97 107 182 192 201 211 218 231
18 62 76 83 94 103 114 192 114 192 203 230 244
19 67 82 89 100 110 121 202 213 223 234 241 256
20 71 87 94 106 116 128 212 224 234 246 253 269

4 0 4 ESTATÍSTICA
Tabela 9 (Continuação).
n 1 = 1» P(LT < uc) aproximadamente igual a
n2 0,001 0,005 0,01 0,025 0,05 0,1 0,9 0,95 0,975 0,99 0,995 0,999
2 0 0 1 3 5 7 29 31 33 35 36 36
3 1 3 5 8 10 14 40 44 46 49 51 53
4 4 7 10 13 17 21 51 55 59 62 65 68
5 7 12 15 19 23 28 62 67 71 75 78 83
6 11 17 20 25 29 35 73 79 83 88 91 97
7 15 22 25 31 36 42 84 90 95 101 104 111
8 19 27 31 37 42 49 95 102 107 113 117 125
9 24 32 37 43 49 56 106 113 119 125 130 138
10 28 38 42 49 56 63 117 124 131 138 142 152
11 33 43 48 56 62 70 128 136 142 150 155 165
12 38 48 54 62 69 78 138 147 154 162 168 178
13 43 54 60 68 76 85 149 158 166 174 180 191
14 47 59 66 75 83 92 160 169 177 186 193 205
15 52 65 71 81 89 99 171 181 189 199 205 218
16 57 71 77 87 96 107 181 192 210 211 217 231
17 62 76 83 94 103 114 192 203 212 223 230 244
18 67 82 89 100 110 121 203 214 224 235 242 257
19 72 88 95 107 117 129 213 225 235 247 254 270
20 77 93 101 113 124 136 224 236 247 259 267 283

APÊNDICE: TABELAS ESTATÍSTICAS 4 0 5
Tabela 9 (Continuação).
n, = 19 P(17 < uc) aproximadamente igual a
n2 0,001 0,005 0,01 0,025 0,05 0,1 0,9 0,95 0,975 0,99 0,995 0,999
2 0 1 2 3 5 8 30 33 35 36 37 38
3 1 4 5 8 11 15 42 46 49 52 53 56
4 4 8 10 14 18 22 54 58 62 66 68 72
5 8 13 16 20 24 29 66 71 75 79 82 87
6 12 18 21 26 31 37 77 83 88 93 96 102
7 16 23 27 33 38 44 89 95 100 106 110 117
8 21 29 33 39 45 52 100 107 113 119 123 131
9 26 34 39 46 52 59 112 119 125 132 137 145
10 30 40 45 53 59 67 123 131 137 145 150 160
11 35 46 51 59 66 74 135 143 150 158 163 174
12 41 52 57 66 73 82 146 155 162 171 176 187
13 46 58 64 73 81 90 157 166 174 183 189 201
14 51 64 70 79 88 98 168 178 187 196 202 215
15 56 70 76 86 95 105 180 190 199 209 215 229
16 61 75 83 93 102 113 191 202 211 221 229 243
17 67 82 89 100 110 121 202 213 223 234 241 256
18 72 88 95 107 117 129 213 225 235 247 254 270
19 78 94 102 114 124 136 225 237 247 259 267 283
20 83 100 108 120 131 144 236 249 260 272 280 297

4 0 6 ESTATÍSTICA
Tabela 9 (Continuação).
ftj = 20 P(LT < uc) aproximadamente igual a
n2 0,001 0,005 0,01 0,025 0,05 0,1 0,9 0,95 0,975 0,99 0,995 0,999
2 0 1 2 3 5 8 32 35 37 38 39 40
3 1 4 6 9 12 16 44 48 51 54 56 59
4 4 9 11 15 19 23 57 61 65 69 71 76
5 8 14 17 21 26 31 69 74 79 83 86 92
6 13 19 23 28 33 39 81 87 92 97 101 107
7 17 25 29 35 40 47 93 100 105 111 115 123
8 22 31 35 42 48 55 105 112 118 125 129 138
9 27 37 41 49 55 63 117 125 131 139 143 153
10 33 43 48 56 63 71 129 137 144 152 157 167
11 38 49 54 63 70 79 141 150 157 166 171 182
12 43 55 61 70 78 87 153 162 170 179 185 197
13 49 61 68 77 85 95 165 175 183 192 199 211
14 55 68 74 84 93 103 177 187 196 206 212 225
15 60 74 81 91 101 111 189 199 209 219 226 240
16 66 80 88 99 108 120 200 212 221 232 240 254
17 71 87 94 106 116 128 212 224 234 246 253 269
18 77 93 101 113 124 136 224 236 247 259 267 283
19 83 100 108 120 131 144 236 249 260 272 280 297
20 89 106 115 128 139 152 248 261 272 285 294 311

APÊNDICE: TABELAS ESTATÍSTICAS 4 0 7
Tabela 10 Valor absoluto mínimo para o coeficiente de correlação r de Pearson
ser significativo.
Nível de significância, a, num teste unilateral
0,100 0,050 0,025 0,010 0,005 0,001
Nível de significância, a, num teste bilateral
n 0,200 0,100 0,050 0,020 0,010 0,002
5 0,687 0,805 0,878 0,934 0,959 0,986
6 0,608 0,729 0,811 0,882 0,917 0,963
7 0,551 0,669 0,754 0,833 0,875 0,935
8 0,507 0,621 0,707 0,789 0,834 0,905
9 0,472 0,582 0,666 0,750 0,798 0,875
10 0,443 0,549 0,632 0,715 0,765 0,847
11 0,419 0,521 0,602 0,685 0,735 0,820
12 0,398 0,497 0,576 0,658 0,708 0,795
13 0,380 0,476 0,553 0,634 0,684 0,772
14 0,365 0,458 0,532 0,612 0,661 0,750
15 0,351 0,441 0,514 0,592 0,641 0,730
16 0,338 0,426 0,497 0,574 0,623 0,711
17 0,327 0,412 0,482 0,558 0,606 0,694
18 0,317 0,400 0,468 0,543 0,590 0,678
19 0,308 0,389 0,456 0,529 0,575 0,662
20 0,299 0,378 0,444 0,516 0,561 0,648
21 0,291 0,369 0,433 0,503 0,549 0,635
22 0,284 0,360 0,423 0,492 0,537 0,622
23 0,277 0,352 0,413 0,482 0,526 0,610
24 0,271 0,344 0,404 0,472 0,515 0,599
25 0,265 0,337 0,396 0,462 0,505 0,588
26 0,260 0,330 0,388 0,453 0,496 0,578
27 0,255 0,323 0,381 0,445 0,487 0,568
28 0,250 0,317 0,374 0,437 0,479 0,559
29 0,245 0,311 0,367 0,430 0,471 0,550
30 0,241 0,306 0,361 0,423 0,463 0,541

4 0 8 ESTATÍSTICA
Tabela 10 (Continuação).
Nível de significância, a, num teste bilateral
n 0,200 0,100 0,050 0,020 0,010 0,002
35 0,222 0,283 0,334 0,392 0,430 0,504
40 0,207 0,264 0,312 0,367 0,403 0,474
45 0,195 0,248 0,294 0,346 0,380 0,449
50 0,184 0,235 0,279 0,328 0,361 0,427
60 0,168 0,214 0,254 0,300 0,330 0,391
70 0,155 0,198 0,235 0,278 0,306 0,363
80 0,145 0,185 0,220 0,260 0,286 0,340
90 0,136 0,174 0,207 0,245 0,270 0,322
100 0,129 0,165 0,197 0,232 0,256 0,305
Nota: Tabela construída da estatística t - r. v' n - 2 / v l - r 2que tem distribuição t de
Student com gl = n - 2, sob as suposições de os dados terem distribuição normal e a cor­
relação ser linear.

Bibliografia
BARBETTA, P. A. Estatística aplicada às ciências sociais. 5. ed. Florianópolis:
Editora da UFSC, 2002.
BOX, G. E. P.; HUNTER, W. G.; HUNTER, J. S. Statistics for experimenters. New
York: John Wiley, 1978.
BUSSAB, W. O.; MORETTIN, P. A. Estatística básica. 5. ed. São Paulo: Saraiva,
2002.
COCHRAN, W. G. Sampling techniques. 3. ed. New York: John Wiley, 1977.
CONOVER, W. J. Practical nonparametric statistics. 2. ed. New York: John Wi­
ley, 1980.
FISHER, R. A. The design of experiments. 6. ed. Edimburgo: Oliver and Boyd,
1951.
JAIN, R. The art of computer systems performance analysis: techniques for expe­
rimental design, measurement, simulation, and modeling. New York: John Wi­
ley, 1991.
MENDENHALL, N. Probabilidade e estatística. Rio de Janeiro: Campos, 1985. v.
1 e 2.
MAGALHÃES, A. N.; LIMA, A. C. P. Noções de probabilidade e estatística. 2. ed.
São Paulo: IME-USP, 1999.

4 1 0 ESTATÍSTICA
MONTGOMERY, D. C.; RUNGER, G. C. Estatística aplicada e probabilidade para
engenheiros. Rio de Janeiro: LTC, 2003.
MONTGOMERY, D. C. Design and analysis of experiments. 4. ed. New York:
John Wiley, 1997.
SPRENT, P. Applied nonparametric statistical methods. Bristol: Chapman and
Hall, 1989.
STIGLER, S. M. The history of statistics: the mensurement of uncertainty before
1900. Cambridge: Harvard University Press, 1986.

ESTATÍSTICA
para Cursos de
Engenharia e Inform ática
Este livro enfatiza a relação dos métodos estatísticos com o planejamento e
desenvolvimento de pesquisas em Engenharia e Informática, o que diferencia da
maioria dos livros-texto de Estatística, que tem uma preocupação excessiva com os
aspectos matemáticos dos métodos estatísticos. Aqui, os métodos estatísticos são
apresentados com muitas ilustrações, de forma simples e intuitiva. Os exemplos
de motivação e exercícios são usualmente associados a problemas típicos de
Engenharia e Informática, tomando o aprendizado mais agradável e motivador
aos estudantes dessas áreas.
O texto mostra como a estatística é importante na vida do engenheiro ou do
profissional em informática, apresenta alguns conceitos básicos e oferece visão geral
dos planos amostrais e projetos de experimentos. Também desenvolve os tópicos
clássicos da Estatística: análise exploratória de dados, modelos probabilísticos,
teoria da estimação e testes de hipóteses. Os três últimos capítulos descrevem
as análises estatísticas para comparação de tratamentos, procedimentos não
paramétricos e análise de regressão, ilustrando com problemas reais de pesquisa.
Aplicação
Livro-texto para a disdplina Estatística dos cursos de graduação e pós-graduação
em Engenharia (todas as áreas), Ciência da Computação e Sistemas de Informação.
Material de consulta parapós-graduandos, pesquisadores, estatísticos, engenheiros
e profissionais da Informática.
p u b lic n ç c r a n t l n j
www.EditoraAtlas.com.br