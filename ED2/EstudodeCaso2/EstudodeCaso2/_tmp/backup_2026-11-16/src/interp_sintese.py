# Interpretações da Parte VII (síntese).
# Redigidas a partir das saídas reais de _tmp/teste_secao0607.ipynb (execução de 12/11/2026).

INTERP_SINTESE = {

'sin_resumo': r'''
**Leitura da tabela-resumo.** As estimativas formam um quadro coerente, em três camadas:

- **tempo**: todas as medidas que respeitam a censura apontam na mesma direção. Mediana de Kaplan-Meier de 81 dias no Controle contra 96 e 95 nos braços com AC; RMST em 180 dias de 82,1 contra 88,6 e 92,9 dias (ΔRMST da Remota 10,7 dias, IC 1,9 a 19,5); HR do Cox ajustado de 0,87 (0,72–1,04) e 0,81 (0,67–0,97); razão de tempos do Weibull de 1,11 e 1,21. O efeito é nítido para a Remota e na mesma direção, mas não significativo isoladamente, para a Presencial;
- **tipo de desfecho**: a incidência acumulada de sentença de mérito aos 90 dias cai de 31,1% no Controle para 7,8% e 7,5%, enquanto a de extinção sem mérito sobe de 23,5% para 32,0% e 27,3%. Entre os sentenciados, a extinção sem mérito passa de 30,2% para 47,4% e 45,4% (OR 2,09 e 1,92, ambos significativos após Holm), e as sentenças de mérito, quando ocorrem, chegam mais tarde (medianas condicionais de 83, 112,5 e 106 dias). É essa troca que explica o atraso global;
- **acordo**: o acordo **na audiência** é baixo e igual nas duas modalidades (5,1% e 4,6%; Fisher p = 1,000). O acordo em qualquer momento é maior na Remota: homologações 16,2% contra 8,0% dos sentenciados (OR 2,22; p Holm 0,033 na família de 9 pares), RC 2,15 no logit ajustado pelo mês (p Holm 0,027) e OR 2,70 até 120 dias. Na família completa dos 55 testes da Parte III, porém, o p de Holm global desse último contraste é 0,267: trata-se de um sinal **sugestivo**, não de um resultado robusto, e concentrado em acordos feitos fora da audiência.
''',

'sin_forest': r'''
**Leitura do gráfico.** No painel do tempo, os dois braços com AC ficam do lado "mais lento" da linha de nulidade nos dois modelos; só o intervalo da Remota a exclui (HR 0,81; razão de tempos 1,21, com limite inferior em 1,00). No painel dos desfechos, os efeitos mais fortes e consistentes são os da **troca de tipo de sentença**: as razões de chances de mérito (0,44 e 0,39) e de extinção sem mérito (2,09 e 1,92) excluem 1 com folga nos dois braços, e as duas modalidades praticamente se sobrepõem. Os intervalos do acordo (homologação e acordo até 120 dias) são largos e só excluem 1 para a Remota, o que reflete o pequeno número de acordos (81 homologações no total) e reforça a leitura de que o efeito sobre o acordo é incerto. A semelhança entre Presencial e Remota em todos os desfechos sugere que o que importa é a **obrigatoriedade** da audiência, e não a sua modalidade, com a ressalva de que a modalidade está confundida com a conciliadora.
''',

'sin_poder': r'''
**Leitura do cálculo de poder.** Com 478 sentenças nos braços Controle e Remota, o experimento tinha 63% de poder para detectar o HR efetivamente observado (0,81) e 34% para o da Presencial (0,87, com 492 sentenças); detectar o HR da Remota com 80% de poder exigiria 707 sentenças (856 com a correção de Holm), cerca de 1,5 vez as disponíveis, e o da Presencial, 1.619. Isso tem duas consequências. Primeiro, o resultado significativo da Remota não é artefato de excesso de poder: é um efeito de tamanho moderado, detectado com poder apenas razoável. Segundo, a ausência de significância da Presencial **não** autoriza concluir que ela não atrasa a sentença: o experimento simplesmente não tinha poder para efeitos desse tamanho.

No acordo na AC, com 174 audiências realizadas no menor braço e taxa-base de 4,8%, só diferenças grandes eram detectáveis: o poder seria de 46% para chegar a 10% de acordos e de 81% para atingir o índice histórico da unidade (13,3%). Uma replicação que pretenda comparar técnicas ou modalidades quanto ao acordo na audiência precisa, portanto, de algumas centenas de audiências por braço, e deve definir no protocolo qual diferença é relevante para a política judiciária.
''',

}
