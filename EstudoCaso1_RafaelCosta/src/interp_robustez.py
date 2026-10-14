INTERP_ROBUSTEZ = {

'rb_ic': r'''
**Leitura.**

- **A raridade da denúncia é robusta.** Mesmo no limite superior do intervalo exato, a taxa de denúncia não passa de 5,9%, e o descumprimento do prazo com réu solto não fica abaixo de 89%. Essas duas conclusões não dependem do acaso amostral.
- **Flagrante e denúncia.** A denúncia é muito mais frequente nos APF (18,2%; IC 7,3–38,5%) que nas portarias (1,0%; IC 0,3–3,6%). Os intervalos não se sobrepõem, apesar de haver apenas 22 APF.
- **Estimativas frágeis.** Com 21 réus presos, a proporção dos que excederam os 10 dias (28,6%) pode estar em qualquer ponto entre 14% e 50%.
- **Medianas por comarca.** Na amostra completa, o IC de Anápolis (1.187–3.905 dias) não se sobrepõe ao de Aparecida (312–681 dias), e a diferença entre as duas é real. Luziânia, com IC de 315 a 5.020 dias, e Águas Lindas, com n = 7, têm medianas pouco informativas. Na coorte recente todos os intervalos se sobrepõem. O de Senador Canedo (14–538 dias) cobre quase toda a faixa das demais comarcas.
''',

'rb_multiplas': r'''
**Leitura.** As conclusões dos Exercícios 3 e 4 **sobrevivem** à correção. Dos 15 testes, 11 eram significativos a 5% e os mesmos 11 continuam significativos por Holm e por BH. O mais frágil é indiciamento × situação processual (p de Holm = 0,032). Os quatro não significativos já tinham p > 0,5. Nenhuma conclusão do estudo dependia de um p-valor limítrofe.

O post-hoc de Dunn mostra que a diferença entre comarcas no tempo do IP se deve **só a Anápolis**. Os três pares significativos após Holm envolvem Anápolis: contra Aparecida (p = 0,003), contra Goiânia (p = 0,019) e contra Senador Canedo (p = 0,049). Nenhum outro par difere. Na coorte recente, **nenhum** dos 15 pares difere (todos com p de Holm = 1). Isso reforça, par a par, o diagnóstico da seção 14.2.
''',

'rb_modelo': r'''
**Leitura.** O controle pela idade corrige e refina a conclusão da seção 14.2.

1. **O efeito da comarca encolhe cerca de 76%.** Sem controle (M1), os efeitos de comarca somam uma amplitude de 1.857 dias: Anápolis fica 1.277 dias acima de Goiânia e Luziânia, 1.479 dias acima. Com o ano de instauração no modelo (M2), a amplitude cai para 450 dias, e Anápolis passa a apenas +187 dias. O R² sobe de 0,13 para 0,96: **o ano de instauração, sozinho, explica quase toda a variação do tempo**. Cada ano a menos de idade reduz o tempo em cerca de 341 dias, perto dos 365 esperados se a data de chegada ao Projudi fosse fixa.
2. **O efeito não desaparece por completo.** O teste de Wald ainda rejeita a igualdade entre comarcas em M2 (χ² = 22,4; p < 0,001) e na mediana (M3; p < 0,001), com Anápolis (+187 a +270 dias) e Senador Canedo (−263 a −274 dias) significativamente diferentes de Goiânia. A afirmação anterior de que a diferença "desaparece" vale para a coorte recente, mas não para o modelo com toda a amostra.
3. **O resíduo mede o calendário da digitalização, não a investigação.** Controlado o ano de instauração, só pode sobrar a data de recebimento. A ordem dos efeitos residuais coincide com a ordem das medianas de recebimento: Senador Canedo recebeu metade dos seus IPs até 12/2022 (efeito −263 dias), e Anápolis só em 05/2024 (efeito +187 dias). **A comarca continua "influenciando" o tempo medido, mas pela data em que migrou seu estoque para o Projudi**, o que não diz nada sobre a velocidade da polícia.

Réu preso deixa de ter efeito relevante depois do controle (M2: +153 dias; p = 0,12). O "preso é mais rápido" do Exercício 3 era, em grande parte, um efeito da idade: dos 21 presos, 19 são APF, e a mediana do ano de instauração é 2024.
''',

'rb_sobrevivencia': r'''
**Leitura.**

- **Descartar os não concluídos subestimava o tempo do MP.** A mediana de Kaplan-Meier é de **113 dias** (IC 78–154), contra 80,5 dias na conta ingênua: 40% a mais. Em Goiânia, onde estão 14 dos 26 procedimentos abertos, a mediana passa de 95 para 147 dias. Em Senador Canedo, de 160 para 232. Nas comarcas sem censura (Anápolis e Águas Lindas), as duas medianas coincidem, como deveria acontecer.
- **As diferenças entre comarcas continuam significativas, mas mais fracas.** O log-rank dá p = 0,038, contra p = 0,0009 no Kruskal-Wallis do Exercício 3. Aparecida (mediana de 25 dias) e Luziânia (22 dias) concluem muito mais depressa. No modelo de Cox, Aparecida tem **1,89 vez a "taxa" de conclusão de Goiânia** (IC 1,28–2,78). Anápolis tende a ser mais rápida (HR 1,47; p = 0,06).
- **Réu preso: conclusão mais lenta no MP** (HR = 0,51; IC 0,29–0,89). Parece paradoxal, mas é coerente com o funil. Uma explicação provável: os casos com preso são os que mais viram denúncia e ação penal, e por isso permanecem "ativos" no Projudi, sem data de conclusão.
- **Pressuposto.** A censura é considerada **não informativa**: supõe-se que os procedimentos abertos não sejam sistematicamente diferentes dos concluídos. A suposição é discutível, porque os abertos concentram-se em Goiânia e têm muitas manifestações (mediana de 9). Por isso as curvas devem ser lidas como descrição, não como previsão.
''',

'rb_prescricao': r'''
**Leitura.**

- **O Projudi aplica a regra dos 20 anos na maioria dos casos.** Dos 145 inquéritos com data de prescrição, 106 (73%) têm exatamente fato + 20 anos (art. 109, I) e outros 3 contam os 20 anos da instauração. Trinta (21%) têm prazo **maior** que 20 anos, até 32,8, o que nenhuma regra do CP justifica antes da denúncia. Parecem datas recalculadas a partir de outro marco, possivelmente o recebimento no Projudi: em 10 dos 30 casos a prescrição cai exatamente 20 anos depois do recebimento. Seis têm prazo menor que 20 anos, e 73 (33%) não têm data. **A data de prescrição do Projudi não é confiável como variável analítica.**
- **Arquivamentos por prescrição.** Dos 10 casos, 5 são coerentes (≥ 20 anos entre o fato e a conclusão) e 3 são compatíveis com a redução pela metade do art. 115 (11,9, 13,4 e 18,5 anos). Dois são **incompatíveis com qualquer prazo legal**: N_ordem 40 (fato em 02/2022, arquivado por "prescrição" dois meses depois) e N_ordem 121 (8,8 anos). Ambos foram incluídos na auditoria, que passa a ter 24 registros. O mais provável é erro de lançamento do motivo, por exemplo extinção por morte do agente registrada como prescrição.
- **Risco nos casos em curso.** Não há prescrição iminente. Dos 37 inquéritos ativos ou suspensos, o mais próximo do prazo (N_ordem 289, Anápolis) ainda tem 10 anos. Mas 16 deles não têm indiciado, e os mais antigos (fatos de 2015 a 2019, sobretudo em Goiânia) já consumiram de um terço a mais da metade do prazo sem autoria definida. É esse grupo que o MP deveria priorizar.
''',

'rb_sensibilidade': r'''
**Leitura.**

1. **Data malformada.** Imputar 12/02/2015 no N_ordem 170 não muda a mediana (2 dias), o Q3 nem o máximo, e a média varia 0,4%. A decisão conservadora de não imputar é **inócua** para os resultados.
2. **Tempo do IP × nº de indiciados.** A suspeita do Exercício 5 se confirma. O ρ = −0,42 da amostra completa (IC −0,53 a −0,30) cai para **ρ parcial = −0,06 (IC −0,20 a 0,09)** quando se controla o ano de instauração. Na coorte recente também não é significativo (ρ = −0,16; IC −0,36 a 0,06). A relação era **inteiramente produzida pelo confundidor**: IPs recentes são mais curtos e mais frequentemente têm autor identificado, sobretudo os flagrantes.
3. **Comarca × desfecho.** Sem o rótulo genérico "pedido deferido", a associação enfraquece de V = 0,26 para 0,22, mas continua significativa (p ≈ 0,01). A prática de registro de Luziânia explica **parte** da associação, não toda. Os resíduos ajustados que restam apontam o excesso de "outros desfechos" (litispendência, suspensão, denúncia) em Senador Canedo (r = +3,33) e em Luziânia (r = +3,19). Goiânia mantém mais atipicidade (r = +2,34) e menos "outros" (r = −2,71).
''',

'rb_validacao': r'''
**Leitura.** Nenhum item ficou sem regra, e só um caiu no resíduo "Outras providências". Mas **17% dos itens (76 de 444) casam com mais de uma regra**, e neles a categoria foi decidida pela ordem das regras. A ambiguidade concentra-se em duas categorias. Em "Controle externo" (86%), itens como "imagens da viatura da PM" também citam mídia; a ordem dá prioridade ao controle externo, que é o aspecto de maior interesse jurídico. Em "Imagens e dados" (63%), os itens também mencionam oitiva ou perícia. Nas categorias grandes (prazo, oitivas, documentos, competência), a ambiguidade é baixa (0–7%).

Isso não invalida a partição, porque cada item continua com exatamente um rótulo. Mas as frequências de "Controle externo" e "Imagens" dependem da ordem das regras. A planilha `rafaelcc_validacao_regras.xlsx` tem 49 itens e os 14 casos de intervenção estatal para conferência.

**Resultado da conferência.** Os 49 itens da amostra foram considerados corretamente classificados (acerto de 100%; IC 95% de Wilson 93–100%). Quatro são limítrofes e estão anotados na tabela de observações: a perícia em celular, as mídias de gravação das oitivas, a suspensão do art. 366 do CPP e a destinação de armas apreendidas. Nos quatro, a categoria atribuída é defensável, mas outra também seria. Os 14 casos marcados como intervenção estatal foram confirmados (precisão de 100%; IC 95% 78–100%). Dois deles são tentativas sem óbito (N_ordem 184 e 210), e em outros dois a evidência é indireta: um ofício à Corregedoria da PM (106) e a menção à existência de um IPM (246).

**Limites.** A conferência mede só a **precisão** das regras: verifica se o que foi rotulado está certo. Ela não mede a **sensibilidade**, porque não se examinaram os casos não marcados em busca de intervenções que as regras deixaram passar. Com 6 itens por categoria, o acerto de cada categoria tem intervalo largo. O parecer registrado na planilha é uma revisão preliminar e deve ser confirmado pelo autor.
''',
}
