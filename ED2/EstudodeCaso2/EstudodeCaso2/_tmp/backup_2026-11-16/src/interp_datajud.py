"""Interpretações da Parte VIII (DataJud). Redigidas a partir das saídas reais do notebook executado
(amostra completa: 38 de 38 lotes; população dos JECs de Natal conforme o cache em datajud_sondagem/natal/)."""

INTERP_DATAJUD = {

    'dj_vinculo': r'''
**Leitura.** Dos 938 números da planilha, **930 (99,1%)** foram encontrados na API e **926 (98,7%)** têm o registro principal (juizado, com passagem pelo 4º JEC). A taxa é praticamente igual nos três grupos (98,1%, 99,0% e 99,0%; teste de permutação sem evidência de diferença), de modo que o vínculo **não introduz viés diferencial** nas comparações das seções seguintes. Os 12 não vinculados são de dois tipos: (i) **oito números não encontrados** em nenhum grau (seis já encerrados na planilha e dois ativos): o índice público não é exaustivo (há processos sob sigilo e registros não enviados pelo tribunal); (ii) **quatro números encontrados só em outro órgão** (justiça comum, G1), dois deles de **origem externa** (numeração 5300, vindos de outro órgão), cuja passagem pelo 4º JEC não aparece no registro daquele número.

O "mesmo número em outra instância" é frequente e foi tratado sem duplicar: 134 processos (14%) têm também um registro na **Turma Recursal** (recurso inominado). Nenhum número tem mais de um registro de juizado no 4º JEC, e o cumprimento de sentença aparece no **mesmo** registro, por evolução de classe (436 → 156), e não como processo novo.
''',

    'dj_datas': r'''
**Leitura.** A **data de distribuição** da planilha é, em 99,9% dos casos, o dia do 1º movimento no 4º JEC; a diferença para `dataAjuizamento` (96,4% iguais) aparece só nos processos que chegaram de outro órgão ou foram redistribuídos para o 4º JEC: a planilha mede, corretamente, a entrada **na unidade**, que é o tempo zero adequado ao experimento. A **data da sentença** coincide em **97,6%** dos casos com o 1º julgamento (R1) e em **99,1%** com a regra R2. A diferença entre as duas regras não é erro de digitação: quando um acordo é homologado **depois** da sentença de mérito (no cumprimento de sentença ou na pendência do recurso), a planilha registra a homologação, com a data dela. Isso tem uma consequência para a Parte IV: nesses poucos processos (11), o "tempo até a sentença" da planilha é, na verdade, o tempo até o **acordo posterior**, maior que o tempo até a primeira sentença. O efeito sobre os resultados é desprezível (a seção 8.5 refaz as análises pela R1), mas a definição do evento deve ser explicitada.
''',

    'dj_desfecho': r'''
**Leitura.** O tipo de desfecho concorda em **96,8%** dos processos pela R1 (κ = 0,955) e em **97,9%** pela R2 (κ = 0,971 [0,957; 0,983]): concordância **quase perfeita**. A matriz da R1 mostra onde estão as diferenças: 11 "Homologações" da planilha são, no DataJud, sentenças de mérito seguidas de acordo homologado (a convenção descrita acima); com a R2, resta uma.

As divergências que sobram (tabela acima) são de três naturezas:

1. **Atraso de alimentação da planilha**: 13 processos marcados como "Ativo" em 07/10 já tinham sentença ou saída no DataJud, várias com data muito próxima do corte (quatro sentenças de 03/10/2026, um sábado; outras de maio a agosto; saídas de julho a outubro). A planilha, alimentada à mão, estava alguns dias atrasada; o efeito é censurar como ativos processos já encerrados (corrigido na extensão de 8.4).
2. **Mérito na planilha × extinção sem mérito no DataJud** (três casos: abandono da causa, ausência de pressupostos, inadmissibilidade do rito): diferença de classificação jurídica do mesmo ato, ou lançamento do código TPU errado.
3. Casos isolados: um "Mérito" sem nenhum julgamento lançado no DataJud; uma "Redistribuição" que, no DataJud, é extinção por inadmissibilidade do procedimento seguida de envio a outro órgão; e uma homologação lançada pela Turma Recursal (fora da unidade).

Nenhuma dessas divergências se concentra num grupo: elas não ameaçam a comparação entre os ritos.
''',

    'dj_concordancia': r'''
**Leitura.** Todas as variáveis concordam em nível **quase perfeito** (κ > 0,80), inclusive as que só a planilha distinguia: a **AC realizada** (κ = 0,983; 345 audiências realizadas nas duas fontes, cinco só na planilha e duas só no DataJud) e o **acordo homologado** (κ = 0,993). A **redistribuição** tem o κ mais baixo (0,866), por ser rara (21 casos): cinco saídas registradas no DataJud não constavam da planilha em 07/10, de novo pelo atraso de alimentação. A variável "encerrado em 07/10" resume o padrão: só **uma** discordância no sentido "encerrado na planilha, ativo no DataJud" e **13** no sentido oposto, isto é, a planilha **subestima** levemente os encerramentos perto do corte, mas não inventa nenhum.

**Conclusão de VIII-A.** A planilha é uma medida **válida** das variáveis do experimento. O principal problema que ela tem não é de digitação, e sim de **definição** (o acordo posterior à sentença substitui a sentença) e de **defasagem** perto da data de corte. As duas coisas são pequenas e não diferenciais entre os grupos.
''',

    'dj_fim_semana': r'''
**Leitura.** A suspeita da auditoria (A16) **não se confirma**. As **135 sentenças** datadas em sábado ou domingo na planilha estão no DataJud **no mesmo dia** em 98,5% dos casos, e a distribuição dos dias da semana é praticamente idêntica nas duas fontes (72 sábados e 63 domingos no DataJud). O movimento de julgamento é gerado quando o magistrado **assina eletronicamente** a sentença no PJe; a publicação no Diário vem depois, em dia útil. A hora do registro ajuda a ler o padrão: as sentenças de fim de semana concentram-se **de manhã** (7h às 11h), enquanto as de dia útil se dividem entre manhã e tarde, o perfil de quem despacha remotamente fora do expediente. As datas de fim de semana são, portanto, as datas **reais da assinatura**, e não erro de lançamento. O que a planilha registra é a data em que a sentença passou a existir nos autos; a "data de lançamento" e a "data de assinatura" coincidem no PJe.

Para o estudo, isso fecha a questão da seção 2.5.4 e da sensibilidade da seção 4.9: **nenhuma correção** das datas de fim de semana é necessária. Para a gestão, o dado é relevante por si: quase um quinto das sentenças do período foi assinado em fins de semana.
''',

    'dj_corte': r'''
**Leitura.** O volume diário de movimentos dos processos da amostra oscila, nos dias úteis, em torno do nível de referência até a primeira semana de novembro e cai a **zero a partir de 09/11/2026**, embora a coleta tenha terminado em 12/11. Essa queda abrupta não é a de um acervo que se encerra (que seria gradual): é a **defasagem de carga** do índice, cuja última atualização é de 09/11. O corte confiável adotado é **06/11/2026** (sexta-feira), o último dia útil com volume no nível habitual, um mês depois do corte da planilha.
''',

    'dj_censurados': r'''
**Leitura.** Dos 206 processos censurados em 07/10/2026, o DataJud registra até 06/11/2026: **81 sentenças posteriores a 07/10**, **8 sentenças anteriores a 07/10 que a planilha não registrou** (o atraso de alimentação de 8.3), 5 saídas da unidade e 109 processos ainda sem sentença; 3 não puderam ser seguidos (sem vínculo). A extensão **não é neutra entre os grupos**: o Controle encerrou cerca de dois terços dos seus censurados nesse mês, a AC presencial metade e a AC remota menos de um terço (χ² = 14,7; 2 gl; p < 0,001). Os processos com AC obrigatória que estavam pendentes em outubro continuavam, em sua maioria, pendentes um mês depois, o que é coerente com o atraso causado pela espera da audiência (Parte IV). A censura de 07/10 não escondia, portanto, uma "recuperação" dos grupos com AC; ao contrário, escondia parte da vantagem do Controle.
''',

    'dj_estendido': r'''
**Leitura.** As funções desta seção reproduzem exatamente os números da Parte IV na base original (medianas de 81, 96 e 95 dias; HR 0,87 e 0,81; ΔRMST180 de 6,5 e 10,7 dias), o que garante que a comparação mede só o efeito do seguimento. Com o seguimento estendido até 06/11/2026, o número de sentenças passa de 708 para **797** e o de censurados cai de 230 para 141:

- as **medianas** quase não mudam (81, 97 e 96 dias): a mediana já era bem estimada em 07/10;
- o **log-rank** passa de χ² = 7,5 (p = 0,023) para **χ² = 13,1 (p = 0,001)**;
- o **HR da AC remota** passa de 0,81 (0,67–0,97) para **0,76 (0,64–0,90; p = 0,002)**, e o da presencial de 0,87 para 0,85 (0,72–1,01; p = 0,059);
- o **ΔRMST180 da AC remota** sobe de 10,7 para **14,0 dias (5,0 a 22,1)**; o da presencial fica em 6,9 dias (−1,0 a 15,5).

**Conclusão de VIII-B.** O seguimento curto **não** produzia o efeito; ao contrário, a análise principal era **conservadora**: com mais um mês de observação, a desvantagem de tempo da AC obrigatória, sobretudo da remota, aumenta e fica mais precisa, e a direção e a ordem dos grupos não mudam. A análise estendida é uma **sensibilidade**: usa uma fonte diferente para os censurados e um corte diferente, e por isso não substitui a análise principal, mas reforça a sua conclusão.
''',

    'dj_regras': r'''
**Leitura.** Construídas **só com os movimentos** (sem nenhuma informação da planilha além do grupo sorteado), as variáveis reproduzem as da pesquisa: o evento concorda com κ = 0,970, o tipo de desfecho com κ = 0,955, e 97,9% dos tempos diferem em no máximo 1 dia (a maioria das diferenças grandes são os acordos posteriores à sentença, em que a planilha é que se afasta da primeira sentença). As curvas de Kaplan-Meier das duas fontes praticamente se sobrepõem em cada grupo, e os efeitos estimados ficam dentro do IC da planilha nos mesmos processos (HR da AC remota 0,82 nas duas fontes; ΔRMST180 de 9,6 × 9,8 dias). **Todos os critérios pré-fixados foram atendidos**: as regras TPU podem ser aplicadas à população dos JECs de Natal, onde não há planilha, com a garantia de que medem o mesmo que a pesquisa mediu.
''',

    'dj_populacao': r'''
**Leitura.** A definição de população é validada pelo próprio experimento: dos 883 processos que o DataJud atribui ao 4º JEC entre 01/01 e 03/08/2026 (classe 436, 1º movimento na unidade), **882 estão na planilha**, isto é, o sorteio do pesquisador cobriu praticamente toda a entrada de ações de conhecimento da unidade. No sentido inverso, 882 dos 938 processos da planilha estão na população; os 56 restantes não são falhas da regra, e sim processos que ela exclui por desenho: 36 chegaram ao 4º JEC por redistribuição (o 1º movimento é de outro órgão), 12 não têm registro de juizado com passagem pelo 4º JEC no índice (8.3.1), 7 têm outra classe (despejo, embargos de terceiro, execução de título, procedimento comum ou da Fazenda Pública), que a planilha incluiu e a população de classe 436 não inclui, e 1 foi ajuizado antes de 2026.

**Situação da coleta: a comparação com os outros 13 JECs ficou parcial.** A API do CNJ esteve sobrecarregada durante toda a coleta (HTTP 429, `es_rejected_execution_exception`, erros de gateway): a certa altura, rendia cerca de 100 processos em duas horas. Foram coletados, processo a processo, **todos** os processos do **4º JEC** ajuizados em 2024, 2025 e de 01/01 a 03/08/2026; dos **outros 13 JECs**, nenhuma janela pôde ser concluída. Por isso, as análises com tempos e horizonte fixo entre unidades (8.6.3 tendências, 8.6.4 DiD com 90 dias, 8.6.6 tipicidade) **não foram executadas nesta versão**. O código está pronto: `coleta_natal.py` retoma do cache (`natal/estado.json`) e o notebook passa a executá-las sozinho quando as janelas estiverem completas (só usa fatias concluídas e não acessa a rede). Em substituição, a seção 8.6.2 compara os 14 juizados por **consultas agregadas**, que a API respondeu.
''',

    'dj_agregado': r'''
**Leitura.**

- **Volume.** O distribuidor reparte a entrada de modo praticamente idêntico entre os 14 juizados, mês a mês, em 2025 e em 2026 (χ² de aderência = 1,05 com 13 gl em 2026; p ≈ 1). O 4º JEC não recebeu menos processos durante o experimento: a pauta extra de audiências não foi compensada por redução da distribuição.
- **O 4º JEC não era um juizado típico antes do experimento.** Em 2025, ele já era o **2º com mais extinções sem mérito** (36,3% dos processos com esse movimento, contra 25,6% na média dos outros 13) e o **2º com menos julgamentos de mérito** (61,1% contra 68,2%); a heterogeneidade entre as 14 unidades é grande (χ² = 185,5 e 93,8; 13 gl; p < 0,001). O perfil "muita extinção, pouco mérito" é, portanto, um traço da unidade (juiz, cartório, prática de extinguir pela ausência do autor e pela inadmissibilidade do rito), e não uma criação do experimento. Isso responde em parte à questão 2.10: o 4º JEC é uma unidade **atípica** dentro de Natal, o que reforça que os efeitos estimados aqui não se transportam automaticamente às demais.
- **Diferenças em diferenças.** De 2025 para 2026, a proporção de processos com **sentença de mérito** caiu 13,5 pontos no 4º JEC (61,1% → 47,6%) e só 1,8 ponto, em média, nos outros 13: o DiD de **−11,8 p.p.** é o **maior em valor absoluto entre as 14 unidades** (p de permutação = 1/14 = 0,071, o menor possível com 14 unidades). A proporção com alguma sentença caiu 4,9 p.p. a mais que nos outros (3ª maior queda; p = 0,21), a de extinção sem mérito subiu 2,9 p.p. relativamente (p = 0,36) e a de homologação não mudou (p = 0,57).

A queda do mérito é coerente com o que o sorteio mostrou dentro da unidade (Partes III e IV): nos grupos com AC obrigatória, o julgamento de mérito passa a esperar a audiência, e parte dos processos termina antes, por acordo ou extinção. Como medida, porém, ela mistura duas coisas: menos processos **chegaram** ao mérito **até a coleta** (atraso) e, possivelmente, menos chegarão (mudança de composição); com dados agregados, sem tempos, não é possível separá-las. É uma comparação **observacional**, no nível da unidade, com N = 14, e o p de 0,071 está no limite do que a permutação permite detectar: indica que a mudança do 4º JEC foi a maior da capital, não que ela seja estatisticamente certa.
''',

    'dj_tendencias': r'''
*Não executada nesta versão: exige os processos (com datas de movimento) das janelas dos outros 13 JECs, que a API não permitiu coletar (ver 8.6.1). O volume mensal por juizado, que a API respondeu por agregação, está em 8.6.2 e não mostra mudança na entrada do 4º JEC em 2026.*
''',

    'dj_did': r'''
*Não executada nesta versão (ver 8.6.1): o DiD com horizonte fixo de 90 dias exige os tempos dos processos dos outros 13 JECs. O DiD possível com os dados agregados está em 8.6.2.*
''',

    'dj_antes_durante': r'''
**Leitura.** Medido pelas mesmas regras, com o mesmo corte e o mesmo horizonte, o **grupo Controle de 2026 é indistinguível do 4º JEC de 2025**: medianas de 81 e 78 dias, RMST até 180 dias de 80,4 e 79,7 dias, 62,4% e 62,3% sentenciados até 90 dias (log-rank χ² = 0,06; p = 0,81). Já os dois braços com AC obrigatória ficam abaixo do patamar histórico da unidade: 48,3% (presencial) e 44,8% (remota) sentenciados até 90 dias, e RMST180 de 85,2 e 95,0 dias.

Três consequências:

1. **O Controle representa de fato o "rito atual"**. Uma ameaça discutida na seção 6.9 era que o experimento, ao ocupar a pauta com audiências obrigatórias e mobilizar cartório e juiz, mudasse a unidade inteira, e que o Controle de 2026 deixasse de representar o rito anterior (contaminação, efeito Hawthorne sobre o juiz-pesquisador). Os dados não mostram isso: o Controle de 2026 tramitou no mesmo ritmo do 4º JEC de 2025.
2. **O atraso dos grupos com AC é um efeito do rito sobre um patamar estável**, e não a combinação de um Controle "acelerado" com grupos tratados normais.
3. **A unidade como um todo ficou mais lenta em 2026**, porque dois terços dos processos foram sorteados para a AC obrigatória: é o custo de escala da política, que uma adoção geral transferiria a toda a unidade. É também o que o DiD agregado de 8.6.2 capta (queda do mérito no 4º JEC maior que em qualquer outro juizado).

**Limites.** É uma comparação antes × depois numa única unidade. Os dados agregados de 8.6.2 indicam que, nos outros 13 JECs, a proporção sentenciada também caiu de 2025 para 2026 (menos tempo de observação para os processos de 2026), mas sem os tempos dos outros juizados não é possível excluir, com horizonte fixo, uma mudança comum à capital. E é observacional: a semelhança Controle 2026 × 4º JEC 2025 é evidência a favor da validade do grupo de comparação, não uma prova.
''',

    'dj_tipicidade': r'''
*Não executada nesta versão (ver 8.6.1): a tipicidade com horizonte fixo exige os tempos dos outros 13 JECs. A comparação possível, pelo perfil de desfechos em 2025, está em 8.6.2: o 4º JEC já era, antes do experimento, o 2º juizado com mais extinções sem mérito e menos julgamentos de mérito.*
''',

    'dj_106': r'''
**Leitura.** A medida do GPS-Jus (duração média dos processos sentenciados nos 12 meses anteriores, do ajuizamento à sentença) foi recalculada com todos os processos do 4º JEC ajuizados a partir de 2024: **93,0 dias** (mediana de 82) para os sentenciados entre 17/12/2024 e 17/12/2025. Fica abaixo dos 106,8 dias citados no projeto, o que é esperado: os processos ajuizados **antes de 2024** e sentenciados naquela janela (os mais antigos e demorados) não foram coletados, e o painel do CNJ pode usar outra definição de evento (baixa, e não a 1ª sentença). Os 93 dias são, portanto, um limite inferior da medida citada.

O ponto central é a comparação feita pelo pesquisador (106,8 → ~75 dias). A **mesma medida**, calculada no DataJud para todos os processos do 4º JEC sentenciados de 01/01 a 07/10/2026, dá **93,5 dias**, praticamente igual à de 2025 (Mann-Whitney p = 0,23), e não os 71 dias da média ingênua da planilha. A diferença vem da janela: a planilha só contém processos distribuídos a partir de 01/01/2026, de modo que até 07/10 nenhum deles podia ter mais de 279 dias, e os ainda pendentes (os mais demorados) ficam fora da média. A "queda" é, portanto, **um artefato da janela de observação** (seção 2.5; E14, E30), e não uma aceleração da unidade; a comparação correta é a de horizonte fixo (8.6.5), que mostra o Controle de 2026 igual ao 4º JEC de 2025 e os grupos com AC mais lentos.
''',

    'dj_sintese': r'''
| Pergunta | Resposta | Seção |
|---|---|---|
| A planilha confere com o DataJud? | Sim. Vínculo de 98,7% (igual nos grupos); datas de distribuição e sentença coincidem em 99,9% e 97,6–99,1%; tipo de desfecho κ = 0,971, AC realizada κ = 0,983, acordo κ = 0,993. Divergências: acordo homologado depois da sentença registrado como desfecho (11) e atraso de alimentação perto de 07/10 (13 processos "ativos" já encerrados) | 8.3 |
| As 135 sentenças em fim de semana são erro? | Não: 98,5% estão no mesmo dia no DataJud; são assinaturas eletrônicas feitas no sábado ou no domingo, quase sempre de manhã | 8.3.3 |
| O seguimento curto distorcia o resultado? | Não; era conservador. Até 06/11/2026, 81 censurados foram sentenciados (mais 8 já sentenciados antes de 07/10); o Controle encerrou mais dos seus pendentes. HR da AC remota 0,81 → 0,76; ΔRMST180 10,7 → 14,0 dias; log-rank p = 0,023 → 0,001 | 8.4 |
| O estudo pode ser refeito só com movimentos? | Sim: κ = 0,97 para o evento, 97,9% dos tempos com diferença ≤ 1 dia, mesmos HR e ΔRMST; critérios pré-fixados atendidos | 8.5 |
| O experimento mudou a unidade? | O Controle não: Controle 2026 = 4º JEC 2025 (RMST180 80,4 × 79,7 dias; p = 0,81). A unidade como um todo, sim: os braços com AC ficaram mais lentos e, entre os 14 JECs, a queda da sentença de mérito de 2025 para 2026 foi a maior no 4º JEC (DiD −11,8 p.p.; permutação p = 0,071, o mínimo possível) | 8.6.2, 8.6.5 |
| O 4º JEC é típico entre os 14? | Não: já em 2025 era o 2º com mais extinções sem mérito (36% × 26%) e menos mérito (61% × 68%). Distribuição de entrada igual entre os 14 | 8.6.2 |
| Comparação com horizonte fixo × outros 13 JECs | Parcial: a API não permitiu coletar os processos dos outros 13 JECs; código retomável a partir do cache | 8.6.1, 8.6.3, 8.6.4, 8.6.6 |
| Os 106,8 dias | Limite inferior de 93 dias no DataJud (sem os ajuizados antes de 2024); a mesma medida em 2026 dá 93,5 dias: a queda para ~75 é artefato da janela da planilha | 8.6.7 |

**Em síntese**, o DataJud **valida** a planilha, **confirma e reforça** o achado principal (a AC obrigatória, sobretudo a remota, atrasa a sentença; com mais seguimento, o efeito cresce) e **afasta** duas ameaças levantadas nas Partes I e VI: as datas de fim de semana não são erro, e o grupo Controle não foi alterado pelo experimento. Mostra também que o 4º JEC é uma unidade atípica em Natal, o que limita a validade externa (questão 2.10). As comparações entre anos e entre unidades são observacionais (e a comparação com os outros 13 JECs ficou parcial por indisponibilidade da API); nenhuma delas muda o estatuto da análise principal, que continua sendo a comparação entre grupos sorteados (Parte IV).
''',
}
