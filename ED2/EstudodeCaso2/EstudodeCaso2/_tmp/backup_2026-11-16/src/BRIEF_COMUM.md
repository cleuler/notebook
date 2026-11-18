# Brief comum para os agentes das Partes II–VII (rafaelcc_ed2.ipynb)

## Leia primeiro
- `EstudodeCaso2/src/CONVENCOES.md` (obrigatório: ambiente, helpers, paleta, nomes, prefixos de chaves).
- `EstudodeCaso2/src/build_rafaelcc_ed2.py` (gerador) e `secao01_curadoria.py` (Parte I, já pronta — não editar).
- `EstudodeCaso2/dat/processado/dicionario_variaveis.csv` e `ed2_tidy.pkl` (N = 938; base primária).
- `EstudodeCaso2/docs/r1_documentos.md` (objeto, desenho, limitações), `r2_notebook_professor.md` (erros E1–E30 do notebook do professor), `r3_auditoria_dados.md` (auditoria), `r4_literatura.md` (guia de métodos com citações ABNT/páginas — USE as citações).
- `EstudodeCaso2/estudo_de_caso_n_2.md` (questões do professor 2.2–2.12).

## Fatos da base primária (conferidos pelo orquestrador)
- 938 processos: Controle 313, Presencial 314, Remota 311. `evento_cr`: 0 censurado (206), 1 sentença (708), 2 redistribuição/"Decisão" (24).
- `tempo` = dias da distribuição à sentença ou ao corte 07/10/2026; `evento` = 1 se sentença (0 inclui redistribuição); `tempo_pos` = 0,5 nos 38 tempos zero (39 nas 944 linhas brutas) (só paramétricos). Seguimento 65–279 dias (entrada escalonada; `followup`).
- `tipo_desfecho`: Homologação 81, Mérito 341, Sem mérito 286, Redistribuição 24, Ativo 206. Controle tem mais mérito (162) e menos sem mérito (79) que Presencial (96/109) e Remota (83/98) — investigar (hipótese: extinção por ausência do autor à audiência, art. 51, I, Lei 9.099/95).
- `ac_realizada`: Controle sempre False (zero estrutural: não há AC no rito atual); em Presencial/Remota há `<NA>` para ativos sem AC ainda. Técnica/híbrida só fazem sentido no subconjunto com AC.
- Acordos (`acordo_ac`, `acordo_fora`, `acordo`) ocorrem DURANTE o processo: não usar como covariável fixa em Cox (viés de tempo imortal); usar como desfecho/tipo de evento.
- Mês de distribuição está associado ao seguimento e à composição dos grupos (julho concentra Remota) → covariável/estrato.

## Regras
- Escreva SOMENTE os seus arquivos: `src/secaoNN_<nome>.py` e `src/interp_<nome>.py` (dicionário `INTERP_<NOME>`, chaves com o prefixo da parte). Não edite outros arquivos; se precisar de algo no build ou na Parte I, diga no relatório final.
- Teste isolado (não mexa no notebook principal): na raiz `C:\Users\MPGO\AulaCleuler`:
  ```
  uv run python EstudodeCaso2/src/build_rafaelcc_ed2.py --somente secaoNN_<nome> --saida EstudodeCaso2/_tmp/teste_secaoNN.ipynb
  uv run jupyter nbconvert --to notebook --execute --inplace EstudodeCaso2/_tmp/teste_secaoNN.ipynb --ExecutePreprocessor.timeout=1800
  ```
  Itere até rodar sem erro. Leia as saídas reais (dump de texto via json) e SÓ ENTÃO escreva as interpretações; rebuild + re-execute para conferir.
- Preferências do usuário: Kaplan-Meier desce como S(t); sem histograma em escala log; barras verticais e boxplots; **todo teste tem o seu gráfico**; cada passo explicado em markdown (o quê, por quê, como ler); português com acentos; números no texto em pt-BR; teste só o que faz sentido substantivamente (justifique cada teste; diga quando um teste do professor não fazia sentido).
- Sempre: hipóteses H0/H1 explícitas, pressupostos verificados, tamanho de efeito + IC, correção de multiplicidade (Holm) quando houver famílias de testes, leitura jurídica do resultado.
- Censura: nenhuma estatística de "tempo médio" sobre todos os 938 sem aviso; descritivas sobre encerrados são *condicionais* e enviesadas para tempos curtos — diga isso.
- Relatório final ≤ 350 palavras: arquivos, seções criadas, principais números (com p-valores/IC), problemas e pedidos ao orquestrador.
