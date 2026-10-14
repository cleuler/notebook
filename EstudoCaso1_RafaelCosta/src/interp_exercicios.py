# Interpretações dos Exercícios 1 a 5 (seções 10 a 14), redigidas a partir dos resultados da execução.
INTERP_EXERCICIOS = {

'ex1_comarca': r'''**Leitura.** A amostra é muito concentrada: Goiânia responde por 46,3% dos inquéritos e, com Aparecida de Goiânia (20,2%) e Anápolis (15,6%), as três maiores comarcas somam 82,1% — o ponto de corte de 80% do Pareto é atingido com 3 das 6 categorias. Águas Lindas de Goiás tem apenas 7 casos (3,2%), o que torna frágil qualquer conclusão específica sobre ela: nas comparações por comarca, suas estatísticas devem ser lidas com cautela.
''',

'ex1_geral': r'''**Síntese do Exercício 1.**

- **Categorias dominantes.** A maioria das variáveis tem uma classe modal com mais de 70% dos casos: homicídio simples (78,9%), réu solto (90,4%), instauração por portaria (89,9%), arma de fogo (69,7%), crime consumado (80,7%), delegacia especializada em homicídios — DIH/GIH (70,5%) e arquivamento (83,0%). O perfil típico é, portanto, um **homicídio simples consumado, com arma de fogo, sem réu preso, investigado por portaria na DIH/GIH e arquivado**.
- **Categorias raras.** Latrocínio, feminicídio, homicídio privilegiado e lesão corporal seguida de morte somam 3,7% dos casos; por isso foram agrupadas em `Assunto_grupo` ("Outros") para os testes.
- **Autoria.** Em 64,7% dos inquéritos ninguém foi indiciado.
- **Desfecho.** O arquivamento por falta de justa causa é o desfecho mais comum (41,3%); com pedido deferido sem motivo especificado (11,9%), "em investigação" (11,0%), extinção da punibilidade (8,7%) e atipicidade (7,8%), cinco classes cobrem 80,7% dos casos. **Só 6 inquéritos (2,8%) resultaram em denúncia.**
- **Tempo.** 36,7% dos inquéritos levaram mais de cinco anos até chegar ao Projudi; a variável ordinal `Faixa_tempo_ip` mostra a forma da distribuição melhor que as médias. O indicador `Excedeu_prazo_ip` (87,2%) **não mede o descumprimento do prazo legal** (art. 10 do CPP). Ele compara o prazo com a chegada ao Projudi, que não é a conclusão do IP: no flagrante, por exemplo, o auto entra no Projudi no primeiro dia. A seção 15 discute o que esse tempo realmente mede.
- **Atuação do MP.** O MP se manifestou em 61,9% dos inquéritos. Entre esses, as diligências mais frequentes são de prazo/conclusão (73 casos), perícias (57) e oitivas (53).
- **Qualidade do registro.** A classificação do assunto (sistema do MP) e a capitulação (texto do IP) divergem: 20 dos 37 homicídios "qualificados" não citam o §2º do art. 121 na capitulação, e 4 "simples" citam. As duas fontes medem momentos diferentes (tipificação provisória da polícia × classificação do MP) e não devem ser tratadas como sinônimas.
''',

'ex2_tempo_ip': r'''**Leitura.** A distribuição é fortemente **assimétrica à direita** (assimetria = 1,50): a média (1.623 dias ≈ 4,4 anos) é bem maior que a mediana (1.107,5 dias ≈ 3 anos), puxada por uma cauda de inquéritos muito antigos, com máximo de 8.914 dias (≈ 24 anos). A dispersão é enorme (dp = 1.815 dias; CV = 112%) e a metade central dos casos vai de 167 a 2.524 dias (IQR = 2.356,5 dias). O dot plot mostra um pico junto de zero — 17 inquéritos com tempo 0, dos quais 13 são autos de prisão em flagrante recebidos no mesmo dia — e uma distribuição quase uniforme entre 1 e 12 anos. Os 9 outliers (acima de ≈ 6.060 dias) não são erros: são inquéritos instaurados entre 1998 e 2005 (ver seção 15). **A mediana é a medida de centro adequada.**
''',

'ex2_geral': r'''**Síntese do Exercício 2.**

| Variável | Forma | Centro (mediana) | Observação |
|---|---|---|---|
| `Tempo_conclusao_ip` | assimétrica à direita | 1.107,5 dias | cauda de IPs antigos; ver seção 15 |
| `Tempo_conclusao_mp` | assimétrica à direita | 80,5 dias | 192 concluídos; 26 censurados. Com a censura, a mediana de Kaplan-Meier é de 110 dias (seção 15.3) |
| `Tempo_entre_manifestacoes_mp` | bimodal: pico em 0 e cauda longa | 95 dias | 38 zeros correspondem a uma única manifestação |
| `Tempo_fato_instauracao` | extremamente concentrada | 2 dias | Q3 = 6 dias, mas máximo de 4.282 dias |
| `Quantidade_manifestacao_mp` | assimétrica, 38% de zeros | 1 | máximo 17 |
| `N_itens_diligencia` | assimétrica, 38% de zeros | 1 | máximo 15 |
| `N_indiciados` | 64,7% de zeros | 0 | máximo 5 |
| `N_vitimas` | 90,4% com 1 vítima | 1 | máximo 7 (Luziânia) |

- **Maior variabilidade relativa (CV):** `Tempo_fato_instauracao` (531%), `N_indiciados` (177%) e `Quantidade_manifestacao_mp` (142%). Em termos absolutos, `Tempo_conclusao_ip` domina (dp = 1.815 dias).
- **Outliers e sua explicação.** Em `Tempo_fato_instauracao`, 10 inquéritos foram instaurados mais de um ano após o fato (até 11,7 anos): 6 deles em delegacias distritais, o que é compatível com descoberta tardia do crime ou reabertura da apuração (hipótese a conferir nos autos). Em `N_vitimas`, o IQR é 0 (Q1 = Q3 = 1), de modo que a regra de 1,5×IQR marca como "outlier" **todo** caso com mais de uma vítima (21): são múltiplos homicídios legítimos, incluindo um com 7 vítimas. Isso mostra que a regra do boxplot é um alerta, não um critério de exclusão.
- **Média × mediana.** Em todas as variáveis de tempo a média supera a mediana — de 47% (tempo do IP) a mais de 3.500% (tempo entre fato e instauração) —, confirmando a assimetria. Nenhuma delas é aproximadamente normal, o que justifica os testes não paramétricos do Exercício 3.
''',

'ex3_comarca': r'''**Leitura.** As medianas vão de 394,5 dias (Senador Canedo) a 3.361,5 dias (Anápolis), exatamente como antecipado no enunciado — uma diferença de 8,5 vezes. O teste de Kruskal-Wallis rejeita a igualdade das distribuições (H = 19,32; p = 0,0017), mas o tamanho de efeito é pequeno (ε² = 0,068: a comarca "explica" cerca de 7% da variação dos postos). Luziânia é a comarca mais variável (IQR = 5.404 dias), com casos de 0 a 8.914 dias. Os histogramas 6 × 1, com os mesmos intervalos, deixam visível o que a sobreposição esconde: Senador Canedo e Aparecida concentram-se no primeiro ano, enquanto Anápolis tem a massa entre 3.000 e 4.500 dias.

⚠️ **Cuidado com a interpretação causal.** A Parte II mostra que `Tempo_conclusao_ip` é, essencialmente, a **idade do inquérito na chegada ao Projudi**. Anápolis parece "lenta" porque o seu estoque migrado era mais antigo (seção 15), e não porque investigue mais devagar. Na coorte instaurada a partir de 2022, o tempo total não difere entre as comarcas (seção 18.2).
''',

'ex3_reu_preso': r'''**Leitura.** É a comparação mais nítida do estudo. Com réu preso, a mediana é **0 dias** (o auto de prisão em flagrante chega ao Projudi no mesmo dia) e o Q3 é 22 dias; com réu solto, a mediana é **1.320 dias** (3,6 anos). O teste de Mann-Whitney é altamente significativo (p < 0,0001) e o efeito é grande (correlação rank-bisserial = −0,75). O grupo "preso" tem 5 outliers — presos cujo IP se arrastou por até 3.662 dias —, que merecem verificação individual. A diferença era esperada: a prisão impõe o prazo de 10 dias e o controle judicial imediato; o investigado solto não gera essa pressão.
''',

'ex3_geral': r'''**Síntese do Exercício 3.** As sete comparações rejeitaram a igualdade de distribuições a 5%, mas com tamanhos de efeito muito diferentes:

- **Efeitos grandes:** forma de instauração (APF com mediana 0 × portaria com 1.393,5 dias; r = −0,82) e réu preso (r = −0,75). As duas variáveis são quase a mesma coisa (86% dos APF têm réu preso — Exercício 4).
- **Efeitos moderados:** o tipo de delegacia (ε² = 0,12) — centrais de flagrante com mediana de 1 dia, especializadas DIH/GIH com 1.122 dias e distritais com 2.903 dias — e a **quantidade de manifestações do MP por comarca** (ε² = 0,135, o maior efeito entre as comparações com mais de dois grupos): Goiânia tem média de 4,6 manifestações por IP, contra 0,7 a 1,6 nas demais.
- **Tempo do MP por comarca** (ε² = 0,085): Aparecida (mediana de 12 dias) e Luziânia (13,5 dias) concluem muito mais depressa que Goiânia (95), Anápolis (129) e Senador Canedo (160).
- **Situação processual** (ε² = 0,05): os arquivados são os mais antigos (mediana de 1.320 dias), o que também é efeito da idade: o estoque antigo é justamente o que foi arquivado.

A comparação mais reveladora é réu preso × solto: ela mostra que, quando há pressão institucional (prisão, flagrante, prazo de 10 dias), o inquérito anda; quando não há, a mediana passa de três anos.
''',

'ex4_comarca_reu': r'''**Leitura.** A proporção de réus presos varia de 0% (Águas Lindas) a 16,7% (Luziânia), mas o teste não rejeita H₀ (χ² = 3,29; gl = 5; p ≈ 0,68 por permutação; V de Cramér = 0,12). Com apenas 21 presos, 42% das caselas têm frequência esperada abaixo de 5 — por isso o p-valor foi obtido por permutação, e não pela aproximação qui-quadrado. No mosaico, as faixas de "Preso" têm alturas parecidas em todas as colunas. **Conclusão:** não há evidência de que a comarca influencie a proporção de réus presos; as diferenças observadas são compatíveis com o acaso.
''',

'ex4_assunto_reu': r'''**Leitura.** Nenhuma associação: com os 7 tipos (χ² = 1,20; gl = 6; 79% das caselas com esperada < 5; p ≈ 0,91; V = 0,07) e com os 3 grupos (χ² = 1,12; gl = 2; p ≈ 0,59; V = 0,07). A proporção de presos é de 10,5% no homicídio simples e de 7,9% no qualificado. Os tipos raros não têm nenhum preso, mas com 1 a 3 casos cada isso não diz nada. O agrupamento em `Assunto_grupo` não mudou a conclusão, mas tornou o teste mais confiável: a porcentagem de caselas problemáticas caiu de 79% para 33%.
''',

'ex4_comarca_desfecho': r'''**Leitura.** Aqui a associação é clara: χ² = 71,15 (gl = 30), p ≈ 0,0001 por permutação e V de Cramér = 0,26 (associação moderada). Os resíduos ajustados apontam onde ela está:

- **Luziânia**: excesso de arquivamento por "pedido deferido" sem motivo especificado (38,9% contra 11,9% no geral; r = +3,68) e falta de "falta de justa causa" (11,1%; r = −2,71). Isso sugere uma **prática de registro** no Projudi local, que lança o arquivamento como genérico — é uma diferença de rotulagem, não necessariamente de decisão;
- **Senador Canedo**: excesso de "outros desfechos" (42,9%; r = +3,69), que inclui litispendência, suspensão e denúncia;
- **Goiânia**: mais atipicidade (11,9%; r = +2,09) e mais "pedido deferido" (r = +2,08), e menos "outros" (r = −2,95);
- **Anápolis**: nenhum "pedido deferido" (r = −2,34) e 55,9% por falta de justa causa;
- **Águas Lindas**: excesso de autoria desconhecida (28,6%; r = +2,19), com n = 7.

O mapa de correspondência resume o mesmo quadro: as duas primeiras dimensões retêm 82% da inércia. Luziânia se isola à direita, junto de "Arq. pedido"; Senador Canedo, no alto, junto de "Outros"; Goiânia, embaixo, próxima de "Em investigação" e "Arq. atípico"; Anápolis, Aparecida e Águas Lindas, à esquerda, com os arquivamentos por falta de justa causa e por autoria desconhecida.
''',

'ex4_geral': r'''**Síntese do Exercício 4.** Das oito associações testadas, quatro são significativas:

| Associação | V de Cramér | Interpretação |
|---|---|---|
| Forma de instauração × réu preso | 0,87 (forte) | 86,4% dos APF têm réu preso, contra 1,0% das portarias: é praticamente a mesma informação |
| Tentativa × réu preso | 0,31 (moderada) | 28,6% de presos nas tentativas contra 5,1% nos consumados: com a vítima viva, o flagrante e a identificação do autor são mais frequentes |
| Comarca × desfecho | 0,26 (moderada) | diferenças de **registro** do motivo de arquivamento entre comarcas |
| Indiciamento × situação | 0,21 (fraca a moderada) | com indiciado, 20,8% continuam ativos e 72,7% foram arquivados; sem indiciado, 88,7% foram arquivados |

Não houve associação da comarca com réu preso nem com arma de fogo (64% a 74% em todas as comarcas), nem do tipo de crime com réu preso. **As associações encontradas fazem sentido teórico:** o flagrante gera prisão por definição; a tentativa deixa uma testemunha-chave viva; sem autor identificado, o destino natural é o arquivamento. A ressalva metodológica é o tamanho da amostra: com 218 casos e categorias raras, quase todos os testes exigiram permutação ou teste exato.
''',

'ex5_matriz': r'''**Leitura.** Os pares com |r| ou |ρ| > 0,5 formam dois blocos:

1. **Ano de instauração × tempo de conclusão do IP: r = −0,98 (ρ = −0,94).** É quase uma relação determinística, e isso revela algo sobre a própria variável: como todos os recebimentos no Projudi estão concentrados entre 2022 e 2025, o "tempo de conclusão" é praticamente a **idade do inquérito** na chegada ao sistema (seção 15). Não é uma descoberta empírica sobre a polícia, e sim uma consequência da janela de observação da amostra;
2. **O bloco da atuação do MP**: quantidade de manifestações, nº de itens de diligência, tempo entre manifestações e tempo de conclusão no MP correlacionam-se de 0,45 a 0,92. Parte é definicional (mais manifestações ⇒ mais itens; ρ = 0,92), e parte é substantiva (mais manifestações ⇒ mais tempo no MP).

Pearson e Spearman divergem quando há assimetria: `N_itens_diligencia × Tempo_conclusao_mp` tem r = 0,59, mas ρ = 0,74, sinal de uma relação monotônica mas não linear, com poucos casos extremos. `N_vitimas` e `Tempo_fato_instauracao` não se relacionam com nada (|r| < 0,2).
''',

'ex5_pares': r'''**Leitura dos pares.**

- **Tempo do IP × nº de indiciados** (exemplo do professor): correlação fraca e negativa (r = −0,26; ρ = −0,42; R² = 6,9%). Parece que "IPs mais rápidos têm mais indiciados", mas há um **confundidor**: o ano de instauração se correlaciona com o nº de indiciados (ρ = 0,43) e com o tempo (ρ = −0,94). Inquéritos recentes — muitos em flagrante — são curtos *e* têm autor identificado. A reta não deve ser lida como efeito do tempo sobre o indiciamento.;
- **Manifestações do MP × tempo de conclusão no MP**: relação forte e positiva (r = 0,74; ρ = 0,77; R² = 54%). Cada manifestação adicional está associada a cerca de **66 dias** a mais no MP. A causalidade é circular: cada requisição devolve o IP à polícia e prolonga o procedimento, e um procedimento longo dá ocasião a novas manifestações;
- **Ano de instauração × tempo do IP**: r = −0,98, R² = 95,9%; a inclinação (−345 dias por ano) está próxima de −365, o que é exatamente o esperado se o recebimento no Projudi ocorre numa data quase fixa;
- **Manifestações × itens de diligência** (ρ = 0,92) e **manifestações × tempo entre manifestações** (ρ = 0,88): relações quase mecânicas. A dispersão aumenta com x (heterocedasticidade), e a reta de mínimos quadrados subestima a variabilidade para quem tem muitas manifestações.

Todas as correlações fortes fazem sentido teórico, mas duas são **artefatos de construção** (ano × tempo; manifestações × itens). A lição é a do lema da seção final: correlação não é causalidade, e às vezes nem sequer é informação nova.
''',
}
