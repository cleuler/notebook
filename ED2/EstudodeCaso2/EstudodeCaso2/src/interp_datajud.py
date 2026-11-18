"""Interpretações da Parte VI (DataJud). Redigidas a partir das saídas reais do notebook executado
(amostra completa: 38 de 38 lotes; população processo a processo só do 4º JEC, conforme o cache em datajud_sondagem/natal/;
os outros 13 JECs só por consultas agregadas)."""

INTERP_DATAJUD = {

    'dj_vinculo': r'''
**Leitura.** Dos 938 números da planilha, **930 (99,1%)** foram encontrados na API e **926 (98,7%)** têm o registro principal (juizado, com passagem pelo 4º JEC). A taxa é praticamente igual nos três grupos (98,1%, 99,0% e 99,0%; teste de permutação sem evidência de diferença), de modo que o vínculo **não introduz viés diferencial** nas comparações das seções seguintes. Os 12 não vinculados são de dois tipos: (i) **oito números não encontrados** em nenhum grau (seis já encerrados na planilha e dois ativos): o índice público não é exaustivo (há processos sob sigilo e registros não enviados pelo tribunal); (ii) **quatro números encontrados só em outro órgão** (justiça comum, G1), dois deles de **origem externa** (numeração 5300, vindos de outro órgão), cuja passagem pelo 4º JEC não aparece no registro daquele número.

O "mesmo número em outra instância" é frequente e foi tratado sem duplicar: 134 processos (14%) têm também um registro na **Turma Recursal** (recurso inominado). Nenhum número tem mais de um registro de juizado no 4º JEC, e o cumprimento de sentença aparece no **mesmo** registro, por evolução de classe (436 → 156), e não como processo novo.
''',

    'dj_datas': r'''
**Leitura.** A **data de distribuição** da planilha é, em 99,9% dos casos, o dia do 1º movimento no 4º JEC; a diferença para `dataAjuizamento` (96,4% iguais) aparece só nos processos que chegaram de outro órgão ou foram redistribuídos para o 4º JEC: a planilha mede, corretamente, a entrada **na unidade**, que é o tempo zero adequado ao experimento. A **data da sentença** coincide em **97,9%** dos 701 processos com sentença nas duas fontes pela R1 (98,1% com diferença de até 1 dia) e em **99,4%** pela R2. A diferença entre as duas regras não é erro de digitação: quando um acordo é homologado **depois** da sentença de mérito (no cumprimento de sentença ou na pendência do recurso), a planilha registra a homologação, com a data dela. Isso tem uma consequência para a Parte IV: nesses poucos processos (11), o "tempo até a sentença" da planilha é, na verdade, o tempo até o **acordo posterior**, maior que o tempo até a primeira sentença. O efeito sobre os resultados é desprezível (a seção 6.5 refaz as análises pela R1), mas a definição do evento deve ser explicitada.
''',

    'dj_desfecho': r'''
**Leitura.** O tipo de desfecho concorda em **97,2%** dos processos pela **R1**, a regra de referência (**κ = 0,961** [0,946; 0,975]): concordância **quase perfeita** (LANDIS; KOCH, 1977). A R2 sobe para 98,4% (κ = 0,977), mas foi ajustada **depois** de ver os dados, para reproduzir uma convenção da planilha, e por isso não é a medida de validação: ela só mostra que 11 "Homologações" da planilha são, no DataJud, sentenças de mérito seguidas de acordo homologado.

**Extinções superadas.** Quatro processos tinham uma extinção sem mérito seguida, na unidade, de sentença de mérito (tabela acima): a extinção foi reconsiderada ou anulada e o processo seguiu. Em dois deles a planilha já registrava a sentença de mérito, com a data exata; nos outros dois a planilha os mantinha, corretamente, como ativos em 07/10 (a sentença de mérito veio em novembro). Sem a regra de 6.2, a R1 tomaria a extinção como desfecho e criaria quatro "divergências" que são, na verdade, erro da regra.

As 15 divergências que restam com a R2 (tabela) são de três naturezas:

1. **Atraso de alimentação da planilha** (11 processos marcados como "Ativo" em 07/10): seis já tinham sentença de mérito no DataJud (quatro de 03/10/2026, um sábado, e duas de 28/08) e cinco já tinham saído da unidade (de julho a outubro). O efeito é censurar como ativos processos já encerrados, corrigido na extensão de 6.4.
2. **Diferença de classificação do mesmo ato**: um "Mérito" da planilha lançado no DataJud, no mesmo dia, como extinção por ausência de pressupostos processuais; e uma "Redistribuição" que, no DataJud, é extinção por inadmissibilidade do rito seguida de envio a outro órgão.
3. Casos isolados: um "Mérito" sem nenhum julgamento lançado no DataJud e uma homologação lançada pela Turma Recursal (fora da unidade).

Nenhuma dessas divergências se concentra num grupo: elas não ameaçam a comparação entre os ritos.
''',

    'dj_concordancia': r'''
**Leitura.** Todas as variáveis concordam em nível **quase perfeito** (κ > 0,80). A **AC realizada** foi avaliada só nos braços com AC obrigatória (n = 547): κ = 0,972 [0,951; 0,992], com 345 audiências realizadas nas duas fontes, cinco só na planilha e duas só no DataJud. Incluir o Controle, que é "Não" por desenho, somaria 307 concordâncias garantidas e inflaria o resultado (κ = 0,983). O **acordo homologado** concorda com κ = 0,993. A **redistribuição** tem o κ mais baixo (0,866, IC 0,745 a 0,957), por ser rara (21 casos na planilha): cinco saídas registradas no DataJud não constavam da planilha em 07/10, de novo pelo atraso de alimentação. A variável "encerrado em 07/10" resume o padrão: **uma** discordância no sentido "encerrado na planilha, ativo no DataJud" (o "Mérito" sem julgamento lançado) e **11** no sentido oposto; a planilha **subestima** levemente os encerramentos perto do corte.

**Conclusão de VI-A.** A planilha é uma medida **válida** das variáveis do experimento (tipo de desfecho, pela regra de referência R1: κ = 0,961). O que ela tem de problema não é de digitação, e sim de **definição** (o acordo posterior à sentença substitui a sentença) e de **defasagem** perto da data de corte. As duas coisas são pequenas e não diferenciais entre os grupos.
''',

    'dj_fim_semana': r'''
**Leitura.** A suspeita da auditoria (A16) **não se confirma**. As **135 sentenças** datadas em sábado ou domingo na planilha estão no DataJud **no mesmo dia** em 98,5% dos casos, e a distribuição dos dias da semana é praticamente idêntica nas duas fontes (72 sábados e 63 domingos no DataJud). O movimento de julgamento é gerado quando o magistrado **assina eletronicamente** a sentença no PJe; a publicação no Diário vem depois, em dia útil. A hora do registro ajuda a ler o padrão: as sentenças de fim de semana concentram-se **de manhã** (7h às 11h), enquanto as de dia útil se dividem entre manhã e tarde, o perfil de quem despacha remotamente fora do expediente. As datas de fim de semana são, portanto, as datas **reais da assinatura**, e não erro de lançamento. O que a planilha registra é a data em que a sentença passou a existir nos autos; a "data de lançamento" e a "data de assinatura" coincidem no PJe.

Para o estudo, isso fecha a questão da seção 2.5.4 e da sensibilidade da seção 4.9: **nenhuma correção** das datas de fim de semana é necessária. Para a gestão, o dado é relevante por si: quase um quinto das sentenças do período foi assinado em fins de semana.
''',

    'dj_corte': r'''
**Leitura.** O volume diário de movimentos dos processos da amostra oscila, nos dias úteis, em torno do nível de referência até a primeira semana de novembro e cai a **zero a partir de 09/11/2026**, embora a coleta tenha terminado em 12/11. Essa queda abrupta não é a de um acervo que se encerra (que seria gradual): é a **defasagem de carga** do índice, cuja última atualização é de 09/11. O corte confiável adotado é **06/11/2026** (sexta-feira), o último dia útil com volume no nível habitual, um mês depois do corte da planilha. O corte é único para todos os processos (não depende da última atualização de cada registro, que estaria ligada ao desfecho).
''',

    'dj_censurados': r'''
**Leitura.** Dos 206 processos censurados em 07/10/2026, o DataJud registra até 06/11/2026: **83 sentenças posteriores a 07/10** (duas delas são as sentenças de mérito que superaram uma extinção anterior, 6.3.2), **6 sentenças anteriores a 07/10 que a planilha não registrou** (o atraso de alimentação de 6.3), 5 saídas da unidade e 109 processos ainda sem sentença; 3 não puderam ser seguidos (sem vínculo).

Descritivamente, o Controle encerrou cerca de dois terços dos seus censurados nesse mês (65%), a AC presencial metade (50%) e a AC remota menos de um terço (31%). Esse contraste **não tem leitura causal**: os censurados de cada grupo são o que sobrou depois de o rito agir (no Controle, sobretudo processos distribuídos em julho e agosto; nos braços com AC, também processos à espera da audiência), e por isso o χ² entre eles (14,7) é apresentado sem p-valor. O que importa é o efeito da extensão sobre **todos** os processos, a seguir.
''',

    'dj_estendido': r'''
**Leitura.** As funções desta seção reproduzem exatamente os números da Parte IV na base original (medianas de 81, 96 e 95 dias; HR 0,87 e 0,81; ΔRMST180 de 6,5 e 10,7 dias), o que garante que a comparação mede só o efeito do seguimento. Com o seguimento estendido até 06/11/2026, o número de sentenças passa de 708 para **797** e o de censurados cai de 230 para 141:

- as **medianas** quase não mudam (81, 99 e 96 dias);
- o **log-rank** passa de χ² = 7,5 (p = 0,023) para χ² = 13,8 (p < 0,001);
- o **HR da AC remota** passa de 0,81 (0,67–0,97) para **0,75 (0,63–0,89; p = 0,001)**, e o da presencial de 0,87 para 0,85 (0,72–1,00; p = 0,054);
- o **ΔRMST180 da AC remota**, que não depende da hipótese de riscos proporcionais, passa de 10,7 para **14,6 dias (5,6 a 22,9)**; o da presencial, de 6,5 para 7,3 dias (−0,7 a 15,9);
- o teste de **riscos proporcionais** (resíduos de Schoenfeld, como em 4.4.2) não indica violação para os termos de grupo em nenhuma das duas bases (p de 0,55 a 0,95), de modo que a mudança do HR não parece ser só efeito de um horizonte mais longo sobre um risco não proporcional; a seção 4.4.2 mostra, porém, um vale de β(t) entre 60 e 110 dias, e o HR deve ser lido junto com o ΔRMST.

**Conclusão de VI-B.** O seguimento curto **não** produzia o efeito: com mais um mês de observação, as estimativas mantêm a direção e a ordem dos grupos e ficam **um pouco maiores e mais precisas**, sobretudo para a AC remota. Isso é coerente com a análise principal, e não uma prova de que ela fosse "conservadora": as estimativas novas estão dentro dos intervalos de confiança da Parte IV. A análise estendida é uma **sensibilidade**: mistura duas fontes (planilha até 07/10; DataJud depois) e usa outro corte, e por isso não substitui a análise principal.
''',

    'dj_regras': r'''
**Leitura.** Construídas **só com os movimentos** (sem nenhuma informação da planilha além do grupo sorteado), as variáveis reproduzem as da pesquisa: o evento concorda com κ = 0,976, o tipo de desfecho com κ = 0,961, e 98,1% dos tempos diferem em no máximo 1 dia (a maioria das diferenças grandes são os acordos posteriores à sentença, em que a planilha é que se afasta da primeira sentença). As curvas de Kaplan-Meier das duas fontes praticamente se sobrepõem em cada grupo, e os efeitos estimados ficam dentro do IC da planilha nos mesmos processos (HR da AC remota 0,81 × 0,82; ΔRMST180 da remota 10,0 × 9,8 dias; da presencial 5,1 × 5,4). **Todos os critérios pré-fixados foram atendidos**: as regras TPU podem ser aplicadas à população dos JECs de Natal, onde não há planilha.
''',

    'dj_populacao': r'''
**Leitura.** A definição de população é validada pelo próprio experimento: dos 883 processos que o DataJud atribui ao 4º JEC entre 01/01 e 03/08/2026 (classe 436, 1º movimento na unidade), **882 estão na planilha**, isto é, o sorteio do pesquisador cobriu praticamente toda a entrada de ações de conhecimento da unidade. No sentido inverso, 882 dos 938 processos da planilha estão na população; os 56 restantes não são falhas da regra, e sim processos que ela exclui por desenho: 36 chegaram ao 4º JEC por redistribuição (o 1º movimento é de outro órgão), 12 não têm registro de juizado com passagem pelo 4º JEC no índice (6.3.1), 7 têm outra classe (despejo, embargos de terceiro, execução de título, procedimento comum ou da Fazenda Pública), que a planilha incluiu e a população de classe 436 não inclui, e 1 foi ajuizado antes de 2026.
''',

    'dj_agregado': r'''
**Leitura.**

- **Volume.** A distribuição é **equitativa**: em 01/01 a 03/08, cada juizado recebeu de 821 a 887 processos em 2025 e de 889 a 920 em 2026 (coeficiente de variação de 1,9% e 0,9%). A dispersão é menor do que a de um sorteio independente processo a processo, o que indica um distribuidor que compensa as diferenças; por isso não cabe um teste de aderência multinomial. O 4º JEC não recebeu menos processos durante o experimento: a pauta extra de audiências não foi compensada por redução da distribuição.
- **O 4º JEC não era um juizado típico antes do experimento.** Em 2025, ele já era o **2º com mais extinções sem mérito** (36,3% dos processos com esse movimento, contra 25,6% na média dos outros 13) e o **2º com menos julgamentos de mérito** (61,1% contra 68,2%); a heterogeneidade entre as 14 unidades é grande (χ² = 185,5 e 93,8; 13 gl; p < 0,001). Como essas proporções de 2025 já estão perto do fim do seguimento, a comparação entre unidades **dentro de 2025** é a parte mais sólida desta seção: o perfil "muita extinção, pouco mérito" é um traço da unidade (juiz, cartório, prática de extinguir pela ausência do autor e pela inadmissibilidade do rito), e não uma criação do experimento. Isso responde em parte à questão 2.10: o 4º JEC é uma unidade **atípica** dentro de Natal, e os efeitos estimados aqui não se transportam automaticamente às demais.
- **Variação 2025 → 2026 (DiD descritivo).** A proporção de processos com sentença de mérito caiu 13,5 pontos no 4º JEC (61,1% → 47,6%) e 1,8 ponto, em média, nos outros 13: um DiD de −11,8 p.p., o de maior valor absoluto entre os 14 (posição 1; p = 1/14 = 0,071, o menor valor que a permutação admite, e acima de 0,05). A proporção com alguma sentença caiu 4,9 p.p. a mais que nos outros (posição 3; p = 0,21), a de extinção sem mérito subiu 2,9 p.p. relativamente (posição 4; p = 0,29) e a de homologação não mudou (p = 0,57).

**Por que esse DiD não identifica o efeito do experimento.** O seguimento desigual (2025 com 15 a 22 meses; 2026 com 3 a 10) não se cancela entre unidades com velocidades diferentes. A decomposição no 4º JEC mostra o tamanho do problema: com o **mesmo seguimento** dos processos de 2026, a proporção de 2025 com sentença de mérito seria 56,9%, e não 61,1%; a queda até 2026 passa de 14,3 para **10,0 p.p.**, ou seja, cerca de **30%** da queda bruta é só seguimento mais curto. Para "alguma sentença", a queda passa de 11,9 para **6,0 p.p.** (cerca de metade). Nos outros 13 juizados a mesma correção não é possível sem os processos, e o seu tamanho varia com a velocidade de cada um. O DiD agregado mistura, portanto, a mudança de 2026 com a diferença de velocidade entre as unidades.

O que se pode dizer: a queda do mérito no 4º JEC continua presente depois da correção pelo seguimento (−10 p.p.) e é coerente com o que o sorteio mostrou dentro da unidade (Partes III e IV: nos braços com AC, o mérito espera a audiência e parte dos processos termina antes, por acordo ou extinção). Mas a posição do 4º JEC entre os 14 é **descritiva**, sem identificação e sem teste de tendências paralelas; não autoriza dizer que a mudança do 4º JEC foi "a maior da capital" no sentido causal.
''',

    'dj_tendencias': r'''
**Leitura.** *(Redigir quando a coleta dos 14 juizados estiver completa e esta subseção for executada.)*
''',

    'dj_did': r'''
**Leitura.** *(Redigir quando a coleta dos 14 juizados estiver completa e esta subseção for executada.)*
''',

    'dj_antes_durante': r'''
**Leitura.** Medido pelas mesmas regras, com o mesmo corte e o mesmo horizonte, o **grupo Controle de 2026 tramitou no mesmo ritmo do 4º JEC de 2025**: medianas de 81 e 79 dias, RMST até 180 dias de 80,7 e 80,2 dias, 62,4% e 61,9% sentenciados até 90 dias (log-rank χ² = 0,01; p = 0,91). Já os dois braços com AC obrigatória ficam abaixo do patamar histórico da unidade: 47,9% (presencial) e 44,4% (remota) sentenciados até 90 dias, e RMST180 de 85,6 e 95,7 dias.

Três consequências:

1. **O Controle parece representar o "rito atual".** Uma ameaça discutida na seção 7.9 era que o experimento, ao ocupar a pauta com audiências obrigatórias e mobilizar cartório e juiz, mudasse a unidade inteira, e que o Controle de 2026 deixasse de representar o rito anterior (contaminação, efeito Hawthorne sobre o juiz-pesquisador). Os dados não mostram isso: o Controle de 2026 tramitou no mesmo ritmo do 4º JEC de 2025.
2. **O atraso dos grupos com AC aparece sobre um patamar estável**, e não como a combinação de um Controle "acelerado" com grupos tratados normais.
3. **Os processos de 2026 do 4º JEC, somados, foram mais lentos que os de 2025**, porque dois terços deles foram sorteados para a AC obrigatória: é o custo de escala da política, que uma adoção geral transferiria a toda a unidade.

**Limites.** É uma comparação antes × depois numa única unidade. Sem os tempos dos outros 13 juizados, não é possível excluir uma mudança comum à capital entre 2025 e 2026 (se a capital inteira tivesse ficado mais lenta, um Controle igual a 2025 seria, relativamente, mais rápido). E é observacional: a semelhança Controle 2026 × 4º JEC 2025 é evidência a favor da validade do grupo de comparação, não uma prova.
''',

    'dj_tipicidade': r'''
**Leitura.** *(Redigir quando a coleta dos 14 juizados estiver completa e esta subseção for executada.)*
''',

    'dj_106': r'''
**Leitura.** Os **106,8 dias** citados no projeto **não são verificáveis com a mesma definição**. A medida mais próxima que o DataJud permite (4º JEC, sentenciados entre 17/12/2024 e 17/12/2025, dias da entrada ao 1º julgamento) dá **93,6 dias** (mediana de 82; n = 1.386), mas ela não inclui os processos ajuizados antes de 2024 (que puxariam a média para cima), e o painel do CNJ pode usar outra definição de evento (baixa, e não a 1ª sentença). A diferença para 106,8 não é, portanto, nem confirmação nem desmentido do número citado.

A mesma medida para os sentenciados de 01/01 a 07/10/2026 dá **96,4 dias** (mediana de 87; n = 954; Mann-Whitney entre as janelas, p = 0,13), e a média ingênua da planilha, 71 dias. As duas janelas do DataJud têm coberturas incompletas em sentidos opostos (a de 2025 sem os processos antigos; a de 2026 sem os ajuizados depois de 03/08/2026, que seriam todos curtos), de modo que a proximidade entre elas **não** demonstra que a unidade tenha mantido o ritmo; a comparação válida entre antes e durante é a de horizonte fixo (6.6.3).

O que esta seção mostra com segurança é o artefato: a planilha só contém processos distribuídos a partir de 01/01/2026, de modo que até 07/10 nenhum deles podia ter mais de 279 dias, e os ainda pendentes (os mais demorados) ficam fora da média. Os ~71 a 75 dias "dos sentenciados de 2026" não medem uma aceleração da unidade; são consequência da janela de observação (seção 2.5; E14, E30).
''',

    'dj_sintese': r'''
| Pergunta | Resposta | Seção |
|---|---|---|
| A planilha confere com o DataJud? | Sim. Vínculo de 98,7% (igual nos grupos); datas de distribuição e sentença coincidem em 99,9% e 97,9% (R1); tipo de desfecho κ = 0,961 pela regra de referência (R1; 0,977 pela R2, ajustada a posteriori); AC realizada κ = 0,972 (só braços com AC); acordo κ = 0,993. Divergências: acordo homologado depois da sentença registrado como desfecho (11) e atraso de alimentação perto de 07/10 (11 processos "ativos" já encerrados); quatro extinções superadas por sentença de mérito, tratadas pela regra | 6.3 |
| As 135 sentenças em fim de semana são erro? | Não: 98,5% estão no mesmo dia no DataJud; são assinaturas eletrônicas feitas no sábado ou no domingo, quase sempre de manhã | 6.3.3 |
| O seguimento curto distorcia o resultado? | Não. Até 06/11/2026, 83 censurados foram sentenciados (mais 6 já sentenciados antes de 07/10). As estimativas mantêm a direção e ficam um pouco maiores: HR da AC remota 0,81 → 0,75; ΔRMST180 10,7 → 14,6 dias; log-rank p = 0,023 → < 0,001; sem sinal de violação de riscos proporcionais | 6.4 |
| O estudo pode ser refeito só com movimentos? | Sim: κ = 0,976 para o evento, 98,1% dos tempos com diferença ≤ 1 dia, mesmos HR e ΔRMST; critérios pré-fixados atendidos | 6.5 |
| O experimento mudou a unidade? | O Controle, aparentemente não: Controle 2026 ≈ 4º JEC 2025 (RMST180 80,7 × 80,2 dias; p = 0,91). Os braços com AC ficaram mais lentos que o patamar da unidade. Entre os 14 JECs, a comparação agregada é só descritiva: a queda do mérito no 4º JEC (DiD −11,8 p.p.; posição 1 de 14, p = 0,071, o mínimo possível) inclui um efeito do seguimento desigual que, no próprio 4º JEC, responde por cerca de 30% da queda | 6.6.2, 6.6.3 |
| O 4º JEC é típico entre os 14? | Não: já em 2025 era o 2º com mais extinções sem mérito (36% × 26%) e menos mérito (61% × 68%). Distribuição de entrada equitativa entre os 14 | 6.6.2 |
| Comparação com horizonte fixo × outros 13 JECs | Não executada: a API não permitiu coletar os processos dos outros 13 JECs; tendências paralelas não testadas; código retomável a partir do cache | 6.6.1 |
| Os 106,8 dias | Não verificáveis com a mesma definição; a medida mais próxima no DataJud dá 93,6 dias (sem os ajuizados antes de 2024). A média de ~71 a 75 dias dos sentenciados de 2026 é artefato da janela da planilha | 6.6.4 |

**Em síntese**, o DataJud **valida** a planilha, **confirma** o achado principal (a AC obrigatória, sobretudo a remota, atrasa a sentença; com mais um mês de seguimento, as estimativas mantêm a direção e ficam um pouco maiores) e **afasta** duas ameaças levantadas nas Partes I e VII: as datas de fim de semana não são erro, e o grupo Controle tramitou no ritmo anterior da unidade. Mostra também que o 4º JEC é uma unidade atípica em Natal, o que limita a validade externa (questão 2.10). As comparações entre anos e entre unidades são observacionais, e a comparação com os outros 13 JECs ficou restrita a contagens agregadas, que não identificam o efeito do experimento; nenhuma delas muda o estatuto da análise principal, que continua sendo a comparação entre grupos sorteados (Parte IV).
''',
}
