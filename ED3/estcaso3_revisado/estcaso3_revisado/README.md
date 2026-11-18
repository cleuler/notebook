# Estudo de Caso 3 — edição didática auditada (versão final para entrega)

Esta edição apresenta, passo a passo, a curadoria, a análise estatística e a simulação propostas no roteiro da disciplina CDEaDPP. O notebook original continua disponível na raiz de `cdedpp`. O gerador desta pasta lê esse notebook, acrescenta explicações, aplica as correções da revisão final e anexa as Partes V e VI.

## Como ler

Abra `estcaso3_revisado.html` para ler o estudo com tabelas e gráficos, ou `estcaso3_revisado.ipynb` para inspecionar e reexecutar os cálculos. A **Seção 35** traz a resposta final, item a item, ao roteiro.

| Parte | Seções | Conteúdo |
|---|---|---|
| I | 1–3 | ambiente, curadoria, moldura, desenho, representação dos JEC, desfechos do DataJud |
| II | 4–7 | descritiva, probabilidade condicional, Bayes, correspondência e biplots |
| III | 8–12 | logitos multinomial, ordinal e condicional; ROC e Gini; LCA; aplicação à moldura; R19 |
| IV | 13–14 | simulação, Quadro de Variáveis e síntese provisória |
| V | 15–30 | sensibilidade dos métodos; previsão no ajuizamento; o DataJud além do assunto |
| VI | 31–35 | modelos bayesianos e resposta final |
| — | 36 | referências de todo o estudo |

## Principais resultados

- **Prevalência de indício (R19).** Amostra estratificada: 17,65% [14,80; 20,91]%, ou 8.881 processos na moldura de 50.320. Sem os 2 não localizados (D4): 17,71%. Com MRP, que usa o assunto conhecido para toda a moldura: **17,74% [15,46; 20,17]%, ou 8.926 [7.777; 10.149] processos**; a mediana fica dentro do intervalo publicado. Certeza: 5,28% [3,78; 7,11]%, ou 2.654 processos.
- **O assunto concentra o indício.** O código 6226 (inclusão indevida em cadastro de inadimplentes) é 17,1% da moldura e reúne 74 dos 105 indícios. A prevalência é de 67,5% [58,5; 75,8]% nesse assunto e de 7,4% nos demais. A razão de verossimilhança do 6226, estimada em 2022–2023, é 9,8 e prevê corretamente os indícios de 2024. Só com o assunto, conhecido no ajuizamento, a AUC é 0,876 em 2024 (modelo escolhido apenas em 2022–2023).
- **O desfecho é evidência fraca.** RV(extinção) = 1,29 [0,91; 1,77]. A trajetória processual do DataJud acrescenta pouco ao assunto (Seções 22 e 28–30).
- **Certeza.** Nenhuma fonte separa a certeza do indício: 0 de 30 acertos fora do ajuste, e o LOO bayesiano prefere o modelo sem sinais no segundo passo.
- **Perfis de trajetória.** Os três grupos da LCA em `tabelas/trajetorias_processuais.xlsx` não concordam com os rótulos (ARI 0,010 em 2024) e não servem para triagem.
- **Medição.** Com uma única codificadora, cenários plausíveis de erro movem a prevalência entre 15,0% e 19,4%: a incerteza de medição pode superar a amostral.
- **Validade.** A força do assunto pode refletir, em parte, como F3_19 e F3_20 foram codificadas. É preciso validar numa coorte posterior antes de qualquer uso em triagem.

## Revisão final (16/11/2026)

O arquivo `revisao_final.py` aplica as correções; cada substituição falha se o trecho original não existir.

- **Seção 10.6.** O texto dizia "as variáveis do DataJud discriminam pouco" com AUC 0,852. Agora decompõe o sinal (0,709 sem o assunto; 0,810 só com o assunto) e explica por que o número não é comparável com os 233 da Fase III.
- **Seções 10.3, 10.4 e 14.** Corrigidas as frases sobre o DataJud: o que não separa é a trajetória; o assunto separa. A Seção 14 virou síntese provisória.
- **Seção 12.** Passa a exibir a sensibilidade com n = 593 (D4) e os totais na moldura para indício e certeza.
- **Seção 8.3.** Retirada a afirmação de que o efeito da F2_11 "dobra" (intervalos sobrepostos; OR não colapsável).
- **Seção 6.3.** Acrescentada a ressalva de comensurabilidade com os 30% da NT CIJMG, que se referem a dois assuntos.
- **Seções 24, 29 e 30.** Indicada a AUC de referência (a da Seção 26). As Seções 29 e 30 ganharam conclusões numéricas e o teste pareado; o primeiro movimento TPU é constante (código 51 em 99,8%).
- **Limpeza.** Retirados a margem de equivalência e o código morto do TOST; acrescentadas D9 e D11, o título da Seção 1, a numeração da Parte I e as limitações 7 e 10.
- **Parte VI (`bayes.py`, `apendice8.py`).** MRP; Bayes por processo com verossimilhanças Dirichlet; validação temporal do assunto; prevalência com erro de codificação; logística com prioris t de Student e LOO; resposta final.
- **Referências.** Reunidas numa única seção no fim (Seção 36), em vez de ficarem na Seção 14.4, no meio do notebook.
- **`validate.py`.** Confere as novas seções, a ausência das frases corrigidas, marcadores sem valor e se o HTML está atualizado em relação ao notebook.

Antes da revisão, o estado anterior foi salvo em `../estcaso3_revisado_backup_pre_revisao_20261116.tar.gz`.

## Como reproduzir

Execute na raiz de `cdedpp`, com o ambiente e os dados locais do projeto já disponíveis:

```bash
.venv/bin/python estcaso3_revisado/build.py
.venv/bin/jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=3600 estcaso3_revisado/estcaso3_revisado.ipynb
.venv/bin/jupyter nbconvert --to html --TagRemovePreprocessor.remove_input_tags=interp estcaso3_revisado/estcaso3_revisado.ipynb
.venv/bin/python estcaso3_revisado/validate.py
```

O gerador usa `estcaso3_rafael.ipynb` como base. Alterações futuras na base devem ser revisadas antes de regenerar esta edição. As planilhas brutas e o cache do DataJud são lidos em `dat/estcaso_lide_pred/`; o código estatístico e de TPU permanece em `src/estcaso3/` e `framework/modulos/datajud_tpu/`. As saídas revisadas são gravadas em `estcaso3_revisado/processado/`, `figuras/` e `tabelas/`.

## O que a auditoria mudou

- Acrescentou explicações didáticas antes de 44 blocos analíticos, além das interpretações existentes.
- Separou a leitura dos perfis processuais da classificação jurídica atribuída na pesquisa.
- Renomeou as abas e probabilidades da planilha populacional para trajetórias 1, 2 e 3.
- Expôs o caráter exploratório da matriz de confusão nos processos usados para ajustar a mistura.
- Acrescentou uma avaliação temporal: ajuste da LCA em 2022–2023 e confronto com os rótulos de 2024, mantidos fora do ajuste.
- Expôs a incerteza não capturada pelo bootstrap que mantém o modelo de classes fixo.
- Comparou LCA, k-modes e k-means com codificação one-hot no mesmo conjunto de treino e no mesmo ano de avaliação, usando ARI e AMI sem renomear os grupos.
- Acrescentou diagnóstico de dependência local da LCA e verificação do número de grupos por BIC.
- Acrescentou intervalo logito com erro-padrão do desenho, teste de permutação por ano, avaliação fora do ajuste de probabilidades para três classes e incidência acumulada de eventos concorrentes.
- Simulou todo o funil de classificação em populações finitas, com cenário explícito de erro hipotético de codificação.
- Confrontou o desenho com Toshkov: capítulo 8 para observação Large-N, capítulo 7 para experimentos e capítulo 11 para métodos mistos e aninhados.
- Acrescentou uma avaliação temporal supervisionada com desfechos do DataJud e referência de frequência do treino.
- Exportou `tabelas/quadro_dicionario_large_n.xlsx`, com quadro conceitual, dicionário operacional e simulação do funil.
- Substituiu a planilha de conferência manual por auditoria automática e retirou o teste de equivalência sem base de validade.
- Isolou as saídas desta edição para preservar o notebook e as tabelas originais.
- Auditou a representação dos 14 JEC na amostra com simulação de sorteio sem reposição por ano e verificou a cobertura da moldura no DataJud por juizado de origem.
- Abriu o cruzamento ano × JEC, verificou as 42 células com ajuste para múltiplas comparações e produziu um mapa de calor das diferenças.
- Mediu o efeito da pós-estratificação por ano e JEC nas estimativas agregadas de indício e certeza.
- Comparou a amostra também com a coleta integral de 65.472 processos no DataJud durante 2022–2024, distinguindo órgão atual, juizado de origem e regras de elegibilidade.
- Acrescentou matrizes de três classes fora do ajuste, escolha de modelo dentro de 2022–2023, bootstrap das métricas temporais e atualização Bayesiana sequencial em períodos disjuntos.
- Comparou assunto, trajetória DataJud e combinação nos mesmos processos vinculados, com avaliação temporal e intervalos bootstrap pareados para as diferenças de desempenho.
