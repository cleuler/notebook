# Interpretações da Parte VIII (síntese).
# Revistas em 16/11/2026 a partir das saídas da execução completa (dumps v2) e do teste p78.

INTERP_SINTESE = {

'sin_resumo': r'''
**Leitura da tabela-resumo.** A tabela organiza as estimativas pelo grau de proteção contra o viés de seguimento.

- **Tempo.** Todas as medidas que respeitam a censura apontam na mesma direção, mas a evidência só é clara na **Remota**. Na Presencial, o HR (0,87; estendido 0,85) tem IC que toca 1, e a razão de tempos do Weibull da Remota (1,21) também toca 1 (p = 0,051).
- **Tipo de sentença.** O **déficit de mérito** aparece nas três medidas: Fine-Gray, horizonte fixo e proporção entre os sentenciados. O **excesso de sem mérito**, ao contrário, só é forte na medida condicional, que é um limite superior. Fica no limite no Fine-Gray e desaparece em horizonte fixo depois de Holm.
- **Acordo.** O acordo na audiência é igual e baixo. O excedente da Remota aparece em todas as definições, mas o contraste mais limpo (até 120 dias) tem p de Holm global de 0,312.
''',

'sin_forest': r'''
**Leitura do gráfico.**

- **Painel do tempo.** Os dois braços com AC ficam do lado "mais lento" da linha de nulidade nos dois modelos. Só o HR da Remota tem intervalo que a exclui (0,81). A razão de tempos da Remota (1,21) tem limite inferior em 1,00 e, portanto, não a exclui.
- **Painel dos desfechos.** O efeito mais forte e consistente é o **déficit de mérito**: sHR de 0,46 e 0,42, com intervalos longe de 1.
  - O excesso de extinção sem mérito só exclui 1 na Presencial (1,46).
  - O acordo só exclui 1 na Remota, no limite (sHR 1,87, IC 1,00–3,47; OR até 120 dias 2,70).
  - Os intervalos das duas modalidades se sobrepõem em todos os desfechos, e o contraste direto Remota × Presencial não é significativo em nenhuma causa.

Os dados sugerem que o que importa é a **obrigatoriedade** da audiência, e não a sua modalidade, com a ressalva de que a modalidade está confundida com a conciliadora.
''',

'sin_poder': r'''
**Leitura do cálculo de poder.**

- **Tempo.** Com 478 sentenças nos braços Controle e Remota, o experimento tinha cerca de 68% de poder para um HR verdadeiro de 0,80 e de 43% para 0,85. Para 80% de poder, uma replicação precisaria de cerca de 630 sentenças por par de braços (HR = 0,80) ou de 1.190 (HR = 0,85), e de 20% a mais com a correção de Holm.
  - O experimento estava, portanto, subdimensionado até para efeitos moderados (HR = 0,80).
  - A ausência de significância da Presencial **não** autoriza concluir que ela não atrasa a sentença: um efeito verdadeiro de HR = 0,85 teria só 43% de chance de ser detectado.
- **Acordo na AC.** Com 174 audiências realizadas no menor braço e taxa-base de 4,8%, o poder era de 46% para detectar uma taxa de 10% no outro braço e de 91% para 15%: só diferenças de cerca de 8 a 10 p.p. eram detectáveis com segurança. Uma replicação que pretenda comparar técnicas ou modalidades quanto ao acordo na audiência precisa de algumas centenas de audiências por braço e deve definir no protocolo qual diferença é relevante para a política judiciária.
''',

}
