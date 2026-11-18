# Interpretações da Parte VII (respostas às questões 2.2 a 2.12).
# Revistas em 16/11/2026 a partir das saídas da execução completa (dumps v2_p1 a v2_p8) e do teste p78.
# Cada interpretação lê o quadro ou a figura que a precede e fecha a resposta, sem repetir o texto anterior.

INTERP_QUESTOES = {

'q_2_2': r'''
**Resposta à questão 2.2.** O diagrama mostra o ECA: 938 processos repartidos por sorteio em 313, 314 e 311, acompanhados até a mesma data e analisados no grupo sorteado. Nenhum processo foi excluído depois do sorteio; as 24 redistribuições são saídas da unidade antes da sentença, tratadas como risco competitivo (7.3).

O diagrama mostra também onde termina o experimento. Daí em diante, o que acontece depende das partes:

- a AC foi realizada em 178 de 314 processos (Presencial) e em 174 de 311 (Remota);
- 28 audiências presenciais foram híbridas.

Comparar "quem teve AC" com "quem não teve" seria, portanto, um estudo observacional embutido no ensaio.

Em suma, o estudo é um **ECA quanto ao rito**, com componentes observacionais depois do sorteio e uma só unidade. O que lhe falta não é o sorteio, e sim a documentação e a ocultação da alocação, o cegamento e mais de uma unidade.
''',

'q_2_3': r'''
**Resposta à questão 2.3.** Nenhuma variável basal difere entre os grupos além do acaso: mês (p = 0,102), dia da semana (p = 0,577) e origem externa (p = 0,263), todos com p de Holm acima de 0,30.

O painel (d) mostra o desequilíbrio acumulado. Ele chegou a 31 processos em 25/06 e caiu para 3 no final; num sorteio simples, a mediana da amplitude final seria de 28 processos (2.5.1).

Os grupos são, portanto, **amostras independentes** de uma mesma população finita. A escolha certa são testes para k amostras independentes, com estratificação pelo mês.
''',

'q_2_4': r'''
**Resposta à questão 2.4.**

- **Híbrida = Sim** é não adesão parcial ao rito sorteado, ocorrida depois do sorteio. Pela intenção de tratar, as híbridas ficam na Presencial; tratá-las como remotas muda pouco (HR da Remota 0,79).
- **"Decisão"** é saída do estudo por redistribuição a juízo prevento, e não sentença. A frequência é igual nos três grupos, de modo que nenhuma conclusão depende de como ela é tratada.

As duas apontam falhas de protocolo: a adesão à modalidade e a triagem de prevenção não foram controladas antes do sorteio.
''',

'q_2_5': r'''
**Resposta à questão 2.5.** Da população amostrada à disponível, a inferência é interna e válida: um censo sorteado das ações do 4º JEC. Da disponível à de interesse, não há inferência estatística, porque só uma das 14 unidades entrou, e não por sorteio.

O CNJ tem os dados (API Pública do DataJud), e a Parte VI os usou: validou a planilha, estendeu o seguimento e comparou o 4º JEC com os demais. A comparação dos **tempos** entre os 14 JECs, porém, ficou pendente de concluir a coleta.
''',

'q_2_6': r'''
**Resposta à questão 2.6.** O tratamento do professor não foi adequado, porque os problemas convergem para a **variável-alvo**: o par (tempo, evento), de que dependem todas as análises.

O tratamento correto não exigiu imputar nada. Bastou fixar a data de corte, recalcular o tempo pelas datas, definir o evento pelo significado jurídico de cada registro, aplicar uma regra única às duplicatas e registrar cada decisão.

O que ainda falta (motivo da extinção, datas intermediárias, covariáveis) está no PJe.
''',

'q_2_7': r'''
**Resposta à questão 2.7.** Se ordem e tempo fossem independentes, só a censura produziria ρ ≈ −0,19 com todos os tempos e ρ ≈ −0,28 só com os sentenciados. Os valores observados (−0,041 e −0,118) são menos negativos que isso. Na janela comum de 65 dias, sem censura, o ρ é **positivo** (0,140) e fica acima do intervalo de nulidade (−0,066 a 0,067).

Os processos que chegaram depois demoraram mais, e essa desaceleração é dos braços com AC. A matriz do professor (r = 1) é tautológica e deve dar lugar a uma matriz de associação e a modelos de sobrevivência.
''',

'q_2_8': r'''
**Resposta à questão 2.8.** O quadro distingue três situações:

1. **confundidores neutralizados pelo sorteio** (características do processo e das partes);
2. **fatores que o sorteio não alcança** (conciliadora, juiz-pesquisador, reatividade, contaminação). O mais grave é a conciliadora, que faz de Presencial × Remota uma comparação entre **duas pessoas**. Para a reatividade e a contaminação, a Parte VI não encontrou sinal no Controle;
3. **mediadores**, que são o caminho do efeito, e não viés. Exemplo: o excesso de extinções sem mérito está nas **tardias**, após 30 dias (26, 45 e 48 processos), e não nas da primeira semana (39, 48 e 34), o que é compatível com a ausência do autor à AC.

O mês, único confundidor de calendário, foi controlado na análise: log-rank estratificado p = 0,045; Cox com estrato por mês, HR da Remota 0,80 (p = 0,017).
''',

'q_2_9': r'''
**Resposta à questão 2.9.** Sim. Variáveis basais (número de partes, valor da causa) servem como covariáveis; variáveis de processo (atos, remarcações, dias até a AC) são componentes ou mediadores do tempo.

Sem censura, a medida é Spearman ou Kendall τ_b, com teste t ou por permutação. Com censura, como aqui (24,5% dos tempos), a covariável entra num Cox ou num AFT, e o C de Harrell faz o papel do τ de Kendall.
''',

'q_2_10': r'''
**Resposta à questão 2.10.** **Não é possível generalizar estatisticamente** aos 14 JECs.

- **Validade interna**: razoável. O efeito resiste a 11 de 12 cenários e ao seguimento estendido; restam a integridade não verificável do sorteio e a conciliadora confundida com a modalidade.
- **Validade externa**: repousa numa só unidade, escolhida por conveniência e **atípica**. Os processos são comparáveis aos dos demais juizados; a unidade, não.

As comparações com o DataJud medem o efeito do experimento sobre a unidade, e não o efeito do rito. A validade externa exige **replicação**.
''',

'q_2_11': r'''
**Resposta à questão 2.11.** Dos doze procedimentos do professor, só o Kaplan-Meier com log-rank era adequado, e foi justamente o que não rodou (E1).

A figura mostra o custo do teste errado:

- com a censura ignorada, as medianas são 77, 83,5 e 81 dias, e o Kruskal-Wallis dá p = 0,559;
- com a censura respeitada, as medianas são 81, 96 e 95 dias, e o log-rank dá p = 0,023.

O efeito existia; o Kruskal-Wallis o escondia, porque tratava como encerrados os processos ainda ativos, que são os mais longos e estão concentrados nos braços com AC.
''',

'q_2_12': r'''
**Resposta à questão 2.12.** Só a **fidedignidade do registro** é adequada sem ressalvas, agora confirmada por fonte independente. Os itens inadequados concentram-se na alocação, na execução (cegamento, condutor), nas covariáveis, no plano de análise e nos aspectos ético-jurídicos.

A avaliação é positiva quanto ao potencial e crítica quanto à execução. Para uma replicação, as prioridades são:

- **validade interna**: sequência de aleatorização gerada e guardada por terceiro, rodízio das conciliadoras, cegamento da extração e registro do motivo da extinção;
- **validade externa**: várias unidades sorteadas;
- **validade estatística**: pré-registro e cálculo de poder;
- **legitimidade**: apreciação ética e fundamentação legal de cada rito.

O detalhamento está na seção 8.4.
''',

}
