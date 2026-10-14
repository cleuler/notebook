INTERP_TEMPO = {

# ---------------------------------------------------------------- Etapa 1
'ds_definicao': r'''
**Leitura.**

- **As durações fecham.** Nos 218 casos, o tempo total é exatamente a fase policial observada mais a fase judicial. Nos 192 concluídos, a fase judicial coincide com o `Tempo_conclusao_mp` da planilha.
- **"Conclusão no MP" não é o mesmo que fim do procedimento.** Há 13 procedimentos ativos ou suspensos que já têm data de conclusão:
  - em 6, a conclusão é o oferecimento da denúncia, o que é coerente;
  - nos outros 7, o IP segue em investigação depois de uma conclusão registrada (provavelmente voltou à polícia).

  Há também 2 arquivados sem data de conclusão. São incoerências de registro a conferir nos autos; a definição da base é mantida.
''',

'ds_descricao': r'''
**Leitura.** As duas durações são fortemente **assimétricas à direita**: há muitos casos curtos e uma cauda longa de casos demorados, e a média fica bem acima da mediana.

| Duração (192 concluídos) | Mediana | Média | Q1–Q3 | Máximo | Assimetria |
|---|---|---|---|---|---|
| Fase judicial | 80,5 dias | 209 dias | 11–269 | 1.335 | 1,74 |
| Tempo total | 1.331,5 dias | 1.903 dias | 331–3.031 | 8.925 | 1,25 |

- **Fase judicial:** tem 8 conclusões no mesmo dia, e um quarto dos casos termina em até 11 dias. É o retrato de dois regimes: o arquivamento imediato e o ciclo de diligências.
- **Censurados:** no gráfico de pontos, os 26 censurados estão entre os tempos mais longos. Descartá-los, como fazem as seções 15 a 19, **encurta** a distribuição, e a seção 20 corrige isso.
- **Média × mediana:** a mediana é a medida de centro adequada.
''',

'ds_normalidade': r'''
**Leitura. O tempo não é normal**, e as transformações usuais não resolvem.

- **Tempo original:** os quatro testes rejeitam a normalidade com folga. Shapiro-Wilk W = 0,737 na fase judicial e 0,858 no tempo total (p < 10⁻¹¹).
- **No gráfico:** a curva normal com a mesma média e o mesmo desvio põe massa em **tempos negativos**, que não existem. Os pontos do Q-Q se afastam da reta nas duas caudas.
- **Transformações:** raiz, log e Box-Cox (λ = 0,12 e 0,25) reduzem a assimetria, mas os testes continuam rejeitando. Na melhor versão, Box-Cox, o Shapiro dá p < 0,001, e o Lilliefors, p = 0,03 e 0,001.

**Consequência para o restante da análise.** Os métodos que supõem normalidade não são adequados: t de Student, ANOVA e correlação de Pearson com inferência. Por isso a análise usa **testes de postos** (Mann-Whitney, Kruskal-Wallis, Dunn, Spearman), que comparam ordens e não médias, e **modelos próprios para durações** (seções 18 a 21).
''',

'ef_proporcoes': r'''
**Leitura.**

*Binomial ("é a maioria?").* As cinco perguntas rejeitam H₀: p = 50%. Em todas, a resposta é **sim, é a maioria**:

| Pergunta | Proporção | IC 95% exato | p |
|---|---|---|---|
| Arquivado | 83,0% | 77–88% | < 10⁻²³ |
| Com arma de fogo | 69,7% | 63–76% | < 10⁻⁸ |
| Com tramitação direta | 65,1% | 58–71% | — |
| Sem autor identificado | 64,7% | — | — |
| Com manifestação do MP | 61,9% | 55–68% | 0,0005 |

A denúncia (2,8%; IC 1,0–5,9%) e o réu preso (9,6%) são raros. Contra qual valor compará-los fica para a Etapa 2 (seção 22.11), que traz a proporção da população.

*Qui-quadrado e Fisher (tipo de desfecho).* Como a regra de Cochran falha em quase todas as tabelas, o p-valor vem da permutação. Cinco associações resistem à correção BH:

- **Forma de instauração** (V = 0,48), a mais forte. Com APF, 18% são denunciados e 50% seguem em curso; com portaria, 89% são arquivados, e os resíduos ajustados chegam a ±6,8;
- **Réu preso** (V = 0,39);
- **Indiciamento** (V = 0,23): com indiciado, 6,5% de denúncia; sem indiciado, 0,7%;
- **Coorte de instauração** (V = 0,21): os IPs de até 2014 estão **todos** arquivados;
- **Tipo de delegacia** (V = 0,21): as centrais de flagrante têm 18% de denúncia.

*Tabelas 2×2 (Fisher).* A chance de denúncia é 22 vezes maior com APF (OR = 21,6; IC 2,8–245; p = 0,001) e 10 vezes maior com indiciado (OR = 9,7; p = 0,02). Para réu preso (p = 0,10) e tentativa (p = 0,09), o teste não tem poder com só 6 denúncias.

*Post-hoc.* Na coorte de instauração, os pares com Fisher–Holm mostram que só a coorte de até 2014 difere: ali não há nenhum caso em curso.
''',

'ef_naoparametricos': r'''
**Leitura.**

*Fase judicial (concluídos).* Entre as variáveis do caso, só duas resistem à correção BH:

- **Comarca** (Kruskal-Wallis p < 0,001; ε² = 0,085). No post-hoc de Dunn–Holm, **Aparecida de Goiânia** (mediana de 12 dias) difere de Goiânia (95), de Senador Canedo (160) e, no limite, de Anápolis (129);
- **Indício de intervenção estatal** (Mann-Whitney p = 0,01): 250 × 69 dias; rank-bisserial = −0,44.

Forma de instauração, réu preso, arma de fogo, tentativa, qualificadora e indiciamento **não** diferem. As variáveis do processo no MP separam os grupos com enorme força: sem manifestação do MP, a mediana é de 7 dias; com manifestação, de 211 dias (rank-bisserial = −0,78). Mas isso descreve como os procedimentos terminam, e não é efeito.

*Tempo total (concluídos).* Os maiores efeitos são de **calendário**: coorte de instauração ε² = 0,84 e idade do IP na chegada ε² = 0,87. Pelo Dunn, todas as coortes diferem entre si, com medianas de 4.285 dias (até 2014) a 312 dias (2022 em diante). Os demais efeitos (APF, arma, indiciamento, réu preso, delegacia, comarca) **carregam essa idade**, como mostra a seção 21. Anápolis só difere de Aparecida e de Goiânia porque o seu estoque migrado era mais antigo.
''',

'ef_spearman': r'''
**Leitura.**

- **Tempo total:** é quase uma função do calendário. Ano de instauração ρ = −0,93; idade na chegada ρ = 0,96. Inquéritos mais antigos têm, por construção, tempo total maior. O ρ = −0,35 com o número de indiciados reflete o mesmo confundimento: os IPs recentes têm mais autor identificado.
- **Fase judicial:** o tempo cresce com o número de manifestações do MP (ρ = 0,77) e de itens de diligência (ρ = 0,74), relações monotônicas fortes. São variáveis do processo, e a causalidade é circular: cada pedido devolve o IP à polícia, e um IP mais longo recebe mais pedidos.
- **Idade na chegada × fase judicial:** a correlação é fraca e negativa (ρ = −0,15; p BH = 0,08). Os IPs que chegam mais velhos tendem a encerrar mais depressa, o que o Cox confirma na seção 20.
''',

'ds_distribuicao': r'''
**Leitura: a gama generalizada é adequada?**

*Fase judicial (192 concluídos).*
- **Critérios de informação:** Weibull (forma 0,59; escala 141 dias) e gama (forma 0,47) empatam no AIC (diferença de 0,3). A gama generalizada fica atrás, porque o terceiro parâmetro não melhora a verossimilhança. Lognormal, log-logística e exponencial ficam bem atrás (ΔAIC de 16 a 102).
- **Razão de verossimilhança:** confirma. A gama generalizada não supera a Weibull nem a gama (p > 0,4). A exponencial é rejeitada (p < 10⁻²³): o risco de conclusão **diminui** com o tempo (forma de Weibull < 1).
- **Aderência por bootstrap:** nenhuma família passa a 5%. Para a Weibull, KS p ≈ 0,01; para a gama, p ≈ 0,04. A FDA empírica sobe mais rápido que a teórica nos primeiros dias, por causa do excesso de arquivamentos imediatos, e o gráfico P-P mostra essa curvatura.
- **Mistura de dois regimes:** separados, os dois grupos se ajustam muito melhor que o conjunto (LR = 90; 3 gl; p < 10⁻¹⁸):

  | Grupo | Mediana |
  |---|---|
  | Sem manifestação do MP | 7,5 dias |
  | Com manifestação do MP | 212 dias |

*Tempo total.* Gama, Weibull, gama generalizada e até a exponencial ficam a poucos pontos de AIC. Os dados não distinguem as famílias e, ainda assim, todas são rejeitadas no bootstrap. É o reflexo de uma variável que mede a idade do inquérito (seção 21).

**Veredito.** Na amostra, a suspeita de gama generalizada **não se confirma como necessidade**. A família mais simples que descreve a fase judicial é a **Weibull com risco decrescente**, e a gama generalizada não acrescenta nada significativo. Nenhuma família única é aderente, porque o tempo é uma **mistura de regimes**. Na população (seção 22.8), com milhares de casos, o quadro muda: a gama generalizada vence com folga.
''',

'rg_regressoes': r'''
**Leitura.**

*Regressão linear do log do tempo (fase judicial).* O modelo explica **25% da variação** (R² = 0,253; ajustado 0,180; F p < 10⁻⁹):

| Variável | ΔR² ao retirar | Efeito |
|---|---|---|
| Comarca | 13 pontos | Aparecida leva 0,26 vez o tempo de Goiânia (−74%; p < 0,001); Águas Lindas, 3,3 vezes (p = 0,01) |
| Idade do IP na chegada | 4 pontos | cada ano reduz o tempo em 9% (p < 0,001) |
| Ano de recebimento | 3 pontos | — |

As demais contribuem com menos de 1 ponto. O VIF máximo é de 4,0 (ano de recebimento), sem colinearidade grave. Os resíduos não são normais: o R² é **descritivo**, e a inferência fica com os erros robustos (HC3) e com os modelos de sobrevivência.

*Logística do indiciamento (77 × 141).* O modelo discrimina bem (**AUC = 0,75**; McFadden 0,18; LR p < 10⁻⁷) e é bem calibrado (Hosmer-Lemeshow p = 0,16). Dois fatores aparecem:

- **APF** multiplica por 11 a chance de haver indiciado (OR = 10,9; IC 2,1–56);
- **cada ano mais recente de instauração** a aumenta em 13% (OR = 1,13; IC 1,05–1,23). Isso pode ser efeito de período ou de os IPs antigos sem autor terem ficado no estoque.

Tentativa e arma de fogo dobram a chance, mas sem significância (p = 0,10). Delegacia especializada e comarca não importam. O VIF máximo é de 1,8.

*Firth: denúncia (6 eventos), uma variável por vez.* APF (OR = 42; IC 7–241; p < 0,001), réu preso (OR = 11; p = 0,03), indiciado (OR = 8; p = 0,009) e instauração a partir de 2022 (OR = 22; p = 0,002) aumentam a chance de denúncia. **Todas as seis denúncias** são de IPs recentes.

*Firth: prescrição (10 eventos entre 181 arquivados).* O único fator é o **tempo decorrido**:

- **idade do fato na conclusão:** cada ano a mais multiplica por **1,34** a chance de o arquivamento ser por prescrição (IC 1,18–1,52; p < 10⁻⁸);
- **idade do IP na chegada ao Projudi:** o mesmo efeito (OR 1,34/ano);
- **sem efeito:** indiciamento, comarca e qualificadora.

É o que o art. 109 do CP prevê: a prescrição é função do tempo. O modelo multivariável da extinção da punibilidade fica para a população (seção 22.9).
''',

'sv_km_judicial': r'''
**Leitura.**

- **Censura importa.** Contando só os concluídos, a mediana da fase judicial é de 80 dias. Com os 26 censurados (Kaplan-Meier), sobe para **110 dias** (IC 78–154), quase 40% a mais. O quartil superior passa de 270 para 520 dias.
- **Curvas por grupo:** com os 218 casos, só duas variáveis separam as curvas após a correção BH:
  - a **coorte de instauração** (p BH < 0,001): os IPs de até 2014 se encerram muito depressa (mediana de 28 dias) e diferem de todas as outras coortes no log-rank par a par;
  - a **qualificadora capitulada** (p BH = 0,05): 360 × 100 dias.
- **Diferenças grandes, mas não significativas após BH:**
  - **comarca**, com Aparecida em 26 dias e Goiânia em 148 (log-rank p = 0,04);
  - **réu preso**, 360 × 98 dias;
  - **APF**, 302 × 98 dias, com HR univariado < 1.

  O multivariável da 20.3 as recupera.
- **Sem diferença:** tentativa, tramitação direta, arma de fogo e indiciamento.
''',

'sv_cox': r'''
**Leitura.** O modelo é significativo (razão de verossimilhança p < 0,001), com C = 0,64 e **pseudo-R² de Nagelkerke = 0,20**. Com as demais variáveis constantes:

| Efeito | HR | IC 95% | Leitura |
|---|---|---|---|
| Aparecida de Goiânia × Goiânia | 2,24 | 1,50–3,35 | encerra duas vezes mais depressa |
| APF × portaria | 0,37 | 0,17–0,84 | demora mais |
| Arma de fogo | 0,65 | 0,45–0,93 | demora mais |
| Idade do IP na chegada (por ano) | 1,06 | 1,02–1,10 | quanto mais antigo, mais rápido o arquivamento |

- **O que mais pesa:** retirar cada variável mostra que a **comarca** (LR χ² = 15; p = 0,01) e a **idade na chegada** (LR χ² = 9,6; p = 0,002) são as que mais contribuem.
- **Curvas ajustadas:** as curvas de sobrevivência previstas pelo Cox mostram a escala desses efeitos. Com as demais variáveis na média, o IP de Aparecida cruza 50% muito antes do de Goiânia.
- **Pressuposto de riscos proporcionais:** o teste de Schoenfeld acusa violação em todos os níveis do **ano de recebimento**, um efeito de lote que muda no tempo.
- **Cox estratificado** por esse ano: os efeitos se mantêm. Aparecida HR 1,84 (IC 1,22–2,77), APF 0,36, arma 0,70 (p = 0,05), idade 1,06/ano. O efeito de Aparecida ainda varia no tempo, concentrado nos primeiros dias, e deve ser lido como efeito médio.
''',

'sv_aft': r'''
**Leitura.**

*Famílias com censura.* Gama generalizada, Weibull e lognormal ficam a menos de 1,5 ponto de AIC. O terceiro parâmetro não se paga (razão de verossimilhança × Weibull p = 0,11; × lognormal p = 0,06), e a gama é rejeitada (p = 0,003). As curvas ajustadas acompanham o Kaplan-Meier, e os resíduos de Cox-Snell ficam próximos da diagonal. Com censura, a Weibull e a lognormal são aproximações adequadas.

*Modelos AFT.* As quatro distribuições empatam (ΔAIC ≤ 3,5; pseudo-R² de Nagelkerke de 0,20 a 0,23), e as razões de tempo (TR) confirmam o Cox:

| Efeito | TR | Leitura |
|---|---|---|
| Aparecida de Goiânia | 0,24–0,26 | um quarto do tempo de Goiânia |
| APF | 4,9–5,5 | cinco vezes mais tempo |
| Idade na chegada | 0,89–0,90 por ano | −10% por ano |
| Arma de fogo | 1,6 a 2,2 | significativo só na Weibull |
''',

'ds_truncamento': r'''
**Leitura: o principal resultado metodológico da Etapa 1.**

1. **O estimador muda a resposta em uma ordem de grandeza.** A mediana do tempo total é:
   - 1.332 dias só com os concluídos;
   - 1.764 dias com a censura tratada;
   - **140 dias** com a entrada tardia.
2. **A correção por entrada tardia também falha.** O teste de Tsai rejeita a quase-independência: tau = −0,31 (z = −6,2; p < 0,001) na amostra completa, −0,26 nos instaurados a partir de 2022 e −0,36 nos anteriores. Quem chegou ao Projudi mais velho conclui **antes**. **O relógio que governa a conclusão é o tempo desde a chegada ao Projudi, e não desde a instauração**: os IPs antigos migrados são arquivados pouco depois de chegar.
3. **Consequência:** a amostra não permite estimar o tempo total do inquérito sem viés.
   - 1.764 dias superestima, porque os casos longos têm mais chance de estar na amostra;
   - 140 dias depende de uma hipótese rejeitada.

   O que a base mede bem é a **fase judicial**, e é ela que a Etapa 2 compara com a população.
''',

'sv_total': r'''
**Leitura.** No tempo total, o recorte muda as conclusões:

- **Amostra completa com entrada tardia:** quase tudo é "significativo" no Cox univariado (comarca, APF, réu preso, qualificadora, tramitação direta, indiciamento). Mas essas comparações herdam a quase-independência rejeitada.
- **Coorte instaurada a partir de 2022 (89 IPs, truncamento pequeno):** **nenhuma** variável do caso separa as curvas após BH. A mediana de Kaplan-Meier do tempo total é de **342 dias**, e só o ano de recebimento difere (p BH = 0,01).
- **No multivariável, três efeitos aparecem nos dois recortes:**
  - **homicídio qualificado**: HR 0,60 e 0,28;
  - **APF**: HR 0,33 e 0,38;
  - **indiciado**: HR 0,63 e 0,55.

  São as marcas do caminho da responsabilização, que não termina num arquivamento rápido.
- **Famílias paramétricas com entrada tardia:** a gama generalizada é preferida (× Weibull p = 0,007; × gama p = 0,04), mas sob a mesma hipótese rejeitada.
''',

# ---------------------------------------------------------------- Etapa 2
'dj_janela': r'''
**Leitura.**

- **Volume:** a base estadual tem **cerca de 34 mil processos únicos** de CVLI e correlatos: cerca de 22 mil inquéritos e APFs, e 12 mil ações penais que nasceram de inquérito.
- **Truncamento do estoque antigo:** 95% dos processos antigos convertidos foram digitalizados até 2021, antes da janela da amostra. Por isso não é possível reproduzir a amostra pela data de digitalização: a "chegada ao Projudi" dos IPs antigos da amostra é outro marco.
- **Coorte 2022–2026:**
  - **13.294 inquéritos nativos digitais**, sem truncamento;
  - **89% já com desfecho:** cerca de 5,6 mil denúncias, 5,3 mil arquivamentos e 900 extinções da punibilidade; os demais seguem em curso;
  - nas seis comarcas da amostra são cerca de 5 mil processos, com Goiânia em 2,3 mil.
- **Qualidade:**
  - cerca de 100 processos têm desfecho datado antes do ajuizamento e foram excluídos (incoerência de registro);
  - menos de 200 ações penais evoluídas não têm o marco de denúncia;
  - a manifestação do MP só está registrada como petição tipificada em parte dos casos, por isso o desfecho principal é a **decisão judicial**.
''',

'dj_descricao': r'''
**Leitura.**

| Etapa (encerrados da coorte) | Mediana | Q1–Q3 |
|---|---|---|
| Fase judicial (ajuizamento → decisão) | **51 dias** | 17–167 |
| Até a manifestação do MP (cerca de 5 mil casos com petição tipificada) | 35 dias | — |
| Até o retorno da polícia (proxy, cerca de 6 mil com tramitação direta) | 13 dias | — |

- **Do MP à decisão:** o juízo decide em mediana **5 dias** depois da manifestação do MP. A decisão judicial é, portanto, um bom substituto da conclusão no MP.
- **Forma:** a distribuição é ainda mais assimétrica que na amostra (assimetria 2,5; Shapiro-Wilk W = 0,65; p < 10⁻⁷⁰). Com milhares de casos, a não normalidade é inequívoca, e os testes de postos e os modelos de duração são os adequados também aqui.
''',

'dj_testes': r'''
**Leitura.** Com milhares de casos, todos os testes dão p minúsculo. O que importa é o **tamanho do efeito**.

*Tipo de desfecho (V de Cramér).* As associações mais fortes são:

| Variável | V |
|---|---|
| Indício de prisão | 0,49 |
| Tramitação direta | 0,34 |
| Modalidade | 0,32 |
| Tipo de CVLI | 0,28 |
| Ano de ajuizamento | 0,21 |

Comarca, mesorregião e porte do município têm associação fraca (V ≈ 0,12): **o desfecho depende mais do caso do que do lugar**.

*Fase judicial por grupo (Kruskal-Wallis e Mann-Whitney, encerrados).*
- **Indício de prisão:** mediana de 26 × 69 dias, o maior efeito (rank-bisserial 0,28);
- **Ano de ajuizamento:** ε² = 0,05;
- **Tipo de CVLI:** ε² = 0,04. Feminicídio leva 22 dias e homicídio qualificado 35, contra 98 no homicídio simples;
- **Comarca:** ε² = 0,002. As medianas vão de 36 dias (Aparecida) a 62 (Senador Canedo), mas a comarca explica uma fração ínfima da variação;
- **Processo:** com prorrogação de prazo, 399 × 50 dias; com tramitação direta, 67 × 35 dias. São variáveis descritivas.
''',

'dj_distribuicao': r'''
**Leitura.** Na população, a distribuição se define:

- **Melhor família:** a **gama generalizada** é a melhor por AIC e por BIC, com a **lognormal** a cerca de 24 pontos e as demais muito atrás;
- **Restrições:** Weibull e gama são rejeitadas com folga pela razão de verossimilhança (p < 10⁻¹⁸⁰). Os parâmetros estimados levam a gama generalizada para perto do seu limite lognormal;
- **Aderência:** com mil processos sorteados, o bootstrap ainda rejeita as três melhores (p ≈ 0,01). As distâncias KS são pequenas (0,04 a 0,05), e a lognormal é a mais próxima.

**Por que difere da amostra.** Na amostra, a Weibull bastava. A diferença está na **composição**: a população inclui as denúncias rápidas (feminicídio, presos), que a amostra quase não tem. Isso desloca a forma para a lognormal. Com censura (seção 22.10), lognormal e gama generalizada empatam: **a lognormal é a descrição parcimoniosa da fase judicial na população**.
''',

'dj_logistica': r'''
**Leitura.**

*Denúncia × arquivamento (cerca de 11 mil processos; metade denúncias).* O modelo discrimina muito bem (**AUC ≈ 0,90**; McFadden ≈ 0,41):

| Fator | OR |
|---|---|
| Indício de prisão | **≈ 15** |
| Homicídio qualificado | ≈ 11 |
| Feminicídio | ≈ 11 |
| Latrocínio | ≈ 4 |
| Tentativa | ≈ 4 (a vítima sobrevivente é testemunha) |
| Cada aumento de 10 vezes na população do município | ≈ 0,5 |
| Anápolis × Goiânia | ≈ 0,5 |

As demais comarcas da amostra não diferem de Goiânia.

*Extinção da punibilidade × arquivamento (cerca de 900 extinções).* O modelo é mais fraco (AUC ≈ 0,72):

- **comarca:** a extinção é muito mais frequente fora de Goiânia. Luziânia e os demais municípios têm OR acima de 10. Goiânia arquiva por outros motivos;
- **indício de prisão:** reduz a chance (OR ≈ 0,3);
- **feminicídio:** a aumenta (OR ≈ 2), provavelmente pela morte do agente (feminicídio seguido de suicídio).
''',

'dj_sobrevivencia': r'''
**Leitura.**

- **Kaplan-Meier:** a mediana da fase judicial na população é de cerca de **2 meses**. Todas as variáveis separam as curvas no log-rank, porque com 13 mil casos até diferenças pequenas são significativas. Em dias:

  | Grupo | Mediana |
  |---|---|
  | Feminicídio | 24 |
  | Com indício de prisão | 30 |
  | Homicídio qualificado | 42 |
  | Sem indício de prisão | 90 |
  | Homicídio simples | 98 |
  | Com prorrogação de prazo | 796 |
  | 6 comarcas | 60 (Aparecida) a 88 (Águas Lindas) |
  | Demais municípios | 64 |

- **Cox (C ≈ 0,60; Nagelkerke ≈ 0,08):** os efeitos que aceleram o desfecho são feminicídio (HR ≈ 1,9), indício de prisão (≈ 1,5), homicídio qualificado (≈ 1,4) e latrocínio (≈ 1,35). Municípios maiores são mais lentos. **Nenhuma comarca da amostra difere de Goiânia.**
- **Pressuposto de riscos proporcionais:** é violado em quase todas as variáveis, o que é esperado com esse n. Os HR devem ser lidos como efeitos médios, e o AFT confirma o sentido: TR de 0,37 (feminicídio), 0,54 (qualificado) e 0,58 (prisão).
- **Famílias com censura:** a lognormal é a melhor por AIC e BIC, e a gama generalizada não a supera (λ ≈ 0). Weibull, gama e exponencial são rejeitadas.
''',

'dj_comparacao': r'''
**Leitura: a amostra representa a população?**

*Proporções (binomial exato contra a população, 6 comarcas, 2022+).*

| Indicador | Amostra | População | p BH | Leitura |
|---|---|---|---|---|
| Denúncia (amostra inteira) | 2,8% | 36% | < 10⁻³⁰ | sub-representada |
| Denúncia (recorte ≥ 2022) | 6,7% | 36% | < 10⁻⁹ | sub-representada |
| Homicídio qualificado | 15% | 40% | < 10⁻⁶ | sub-representado |
| Réu preso / indício de prisão (≥ 2022) | 20% | 24% | — | compatível |
| Réu preso (amostra inteira) | 9,6% | — | — | abaixo |
| Tentativa | — | — | — | compatível |
| Tramitação direta | — | — | — | compatível |

A distribuição dos IPs recentes entre as comarcas é compatível com a da população (qui-quadrado de aderência p ≈ 0,17).

*Fase judicial.* A amostra é **mais lenta** que a população: em Goiânia, cerca de 148 dias até o MP, contra cerca de 80 até a decisão e 63 até o MP na população. Nas demais comarcas, as diferenças não são significativas após BH.

*Vínculo individual.* Em cerca de 20% dos IPs recentes houve um único candidato. Neles, a decisão judicial ocorre poucos dias depois da conclusão no MP registrada na amostra (mediana de 4 dias), o que confirma que os marcos são equivalentes.

**Interpretação.** A amostra **sub-representa os inquéritos que terminam em denúncia**, que são os mais rápidos, os qualificados e os com prisão. Uma explicação provável é o desenho da coleta: ao serem denunciados, os IPs mudam de classe e deixam de figurar como inquérito. Isso explica por que, na amostra, APF e qualificadora parecem **alongar** a fase judicial, enquanto na população eles a **encurtam**.
''',

'dj_taxas': r'''
**Leitura.**

- **Estado:** cerca de 31 processos de CVLI consumado por 100 mil habitantes por ano (2022–2025).
- **Seis comarcas:** de cerca de 28 (Anápolis) a 37 (Senador Canedo).
- **Relação com a MVI:** a taxa de processos acompanha a MVI de 2022 da Tabela 01 (Spearman ρ ≈ **0,9**). Senador Canedo, Luziânia e Aparecida, com MVI alta, têm as maiores taxas; Goiânia e Anápolis, com MVI menor, as menores.
- **Sensibilidade:** incluindo as tentativas, a correlação cai para cerca de 0,6. As tentativas não entram no indicador de mortes.

**Cautela.** A taxa de processos supera a MVI em todas as comarcas: há mais processos que mortes. É compatível com as ressalvas da tabela acima: mais de um processo por fato, comarcas que abrangem municípios vizinhos e defasagem do ajuizamento. Com seis pontos, a correlação é descritiva.
''',

'dj_confirmacao': r'''
**Leitura.** A população **confirma** a não normalidade e a forte associação entre prisão/flagrante e denúncia. Mas **contradiz** três achados da amostra:

1. **A denúncia não é rara:** é cerca de 36% na população, contra 2,8% na amostra;
2. **Flagrante/prisão e homicídio qualificado aceleram o desfecho:** na amostra, pareciam alongá-lo;
3. **Aparecida não é mais rápida que Goiânia** depois do ajuizamento: HR ≈ 1.

As três divergências têm a mesma origem: a amostra perdeu os inquéritos que viraram ação penal, justamente os mais rápidos e os qualificados ou com prisão. **A lição metodológica do estudo é que o desenho da amostra determina as conclusões sobre o tempo.**
''',

# ---------------------------------------------------------------- Síntese
'sintese': r'''
### 23.2 Reporte analítico

**1. Curadoria.**
- **Tratamento:** a base foi limpa sem imputação. Foram:
  - corrigidos os homóglifos de OCR;
  - separados os três tipos de ausência;
  - removidos os zeros estruturais;
  - normalizadas as categorias em partições verificadas;
  - aplicados tipos explícitos.
- **Incoerências documentadas:** 24 registros, entre eles data malformada, prescrições impossíveis e status sem indiciado. Somam-se a eles os 13 procedimentos "concluídos no MP" que seguem ativos.
- **No DataJud:** os desfechos anteriores ao ajuizamento e as ações penais sem marco de denúncia, também documentados.

**2. O que é o "tempo de tramitação".**
- **Tempo total:** a variável do professor (`Tempo_conclusao_ip`) é a idade do inquérito na chegada ao Projudi (r = −0,98 com o ano de instauração). O tempo total não é estimável sem viés com esta amostra: 1.764 dias com censura, 140 com entrada tardia, e o teste de Tsai rejeita a hipótese da correção.
- **Fase judicial:** é a medida comparável. Na amostra, mediana de Kaplan-Meier de **110 dias**; na população 2022+, de cerca de **2 meses**.

**3. Distribuição.**
- **Normalidade:** rejeitada em todas as escalas, nas duas bases. Por isso os testes de postos e os modelos de duração.
- **Família:** a gama generalizada não é necessária na amostra (Weibull e gama bastam). Na população, ela vence, com a lognormal como forma limite. Nenhuma família única é aderente, porque o tempo é uma mistura de regimes: o arquivamento imediato e o ciclo de diligências.

**4. Fatores do tempo.**
- **Amostra:** Aparecida de Goiânia (HR 2,2), APF (0,37), arma de fogo (0,65) e idade na chegada (1,06/ano), robustos ao Cox estratificado e aos AFT.
- **População:** o que acelera o desfecho é o **tipo de caso** (feminicídio, qualificado, latrocínio) e a **prisão**, e não a comarca.

**5. Desfechos.**
- **Indiciamento:** associado ao flagrante (OR 11) e à recência (AUC 0,75).
- **Denúncia:** na população, associada à prisão (OR ≈ 15) e à gravidade (qualificado/feminicídio OR ≈ 11), com AUC ≈ 0,90.
- **Extinção da punibilidade:** concentrada fora de Goiânia.

**6. Amostra × população.** A amostra sub-representa as denúncias (2,8% × cerca de 36%), os qualificados e os presos, o que inverte o sentido de alguns efeitos. É o achado mais importante para quem for usar a amostra: **as conclusões sobre tempo dependem de quais inquéritos entram na base**.

**7. Visualização.**
- Os gráficos decisivos foram o dispersograma tempo × ano de instauração, o diagrama de Lexis, as curvas de Kaplan-Meier com e sem censura e a comparação de proporções amostra × população.
- Os testes de postos foram acompanhados de boxplots com letras do post-hoc, e os ajustes de distribuição da FDA empírica × teórica.
''',

'limitacoes': r'''
### 23.3 Limitações e próximos passos

**Limitações.**
- **Amostra:** não tem o número CNJ. O vínculo com o DataJud é aproximado (cerca de 20% dos IPs recentes), e a data de referência da coleta (12/03/2026) foi inferida.
- **Ações penais:** a amostra parece excluir os inquéritos que viraram ação penal. Convém confirmar o critério de seleção com o pesquisador que a coletou.
- **DataJud:**
  - não identifica quem praticou cada ato, e o retorno da polícia e a manifestação do MP são **proxies** baseados em movimentos e tipos de petição;
  - não informa a data de instauração, nem distingue as mortes por intervenção policial (por isso mede CVLI, e não MVI);
  - a classe de origem (APF) se perde nas ações penais.
- **Taxas por habitante:** contam processos, e não mortes, e usam a população da sede da comarca.
- **Validação manual das regras textuais:** é preliminar e precisa ser confirmada pelo autor.

**Próximos passos.**
1. Obter o número CNJ da amostra para um vínculo exato.
2. Coletar a data de instauração (Atena) para os processos do DataJud.
3. Modelar os desfechos concorrentes (denúncia, arquivamento, extinção) com incidência acumulada (Aalen-Johansen, Fine-Gray).
4. Estender a coleta ao estoque antigo para estudar a prescrição.
''',
}
