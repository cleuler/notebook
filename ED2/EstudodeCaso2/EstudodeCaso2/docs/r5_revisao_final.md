# r5 — Revisão ponta a ponta de `rafaelcc_ed2.ipynb` (15/11/2026)

Revisão somente leitura: 476 células, Partes I–VIII + Apêndice. Os números principais foram recalculados de forma independente a partir da planilha bruta e de `ed2_tidy.pkl`.

## Integridade (OK)
- O notebook entregue é idêntico ao que se obtém ao rodar `src/` hoje (476 células, 0 diferenças de fonte).
- Reexecução do zero numa cópia isolada, sem `fig/`, `tab/` nem `dat/processado`: 0 erros, saídas textuais idênticas (só mudam caminhos absolutos). **É reprodutível.**
- Contagens conferidas contra a planilha:
  - 944 linhas, 938 CNJ distintos;
  - 6 exclusões → 313/314/311;
  - 708 sentenças, 24 redistribuições, 206 censurados;
  - TODAY() = 07/10/2026.
- Números centrais conferidos: KM 81/96/95 dias; log-rank χ² 7,52 (p 0,023); Cox HR 0,87/0,81; RMST180 82,1/88,6/92,9 dias; Fine-Gray; vínculo DataJud 926/938.

## A. Estrutura (decisão do usuário)
- A1. As referências (7.6) ficam no meio do texto; depois delas vêm a Parte VIII e o Apêndice. → Criar a seção final REFERÊNCIAS antes do Apêndice.
- A2. A síntese (VII) e as respostas (VI) foram escritas antes da Parte VIII:
  - 6.4/6.5 dizem "coleta em curso, 199 de 200";
  - 6.5, a Tabela VI.7 e 7.4.1 tratam as sentenças de fim de semana como suspeitas, mas a 8.3.3 mostra que são reais;
  - 6.9 trata a homogeneidade dos JECs como "não testada", mas a 8.6.2 a testou e rejeitou;
  - Hawthorne/contaminação aparece como "não verificável", mas a 8.6.5 mostra Controle 2026 ≈ 2025.
- A3. A introdução omite a Parte VIII (tabela do pipeline e perguntas de pesquisa).
- A4. Faltam na lista de referências obras citadas no texto:
  - Agresti 2007; Newcombe 1998; Dunn 1964; Tomczak & Tomczak 2014; Romano et al. 2006; Bergsma 2013;
  - Therneau, Grambsch & Fleming 1990; LeBlanc & Crowley 1993; Landis & Koch 1977; Cohen 1960;
  - Machado, Oliveira & Fernandes 2009; Okabe & Ito 2008; Graf et al. 1999;
  - Res. CNJ 481/2022; TPU (Res. CNJ 46/2007).

  Conferir também:
  - a edição de Barbetta (o Enajus cita 2025, p. 13);
  - Moore/Notz/Fligner: edição e tradutor (cap. 9, p. 181–201);
  - a entrada ENAJUS, pelo padrão ABNT de evento;
  - a forma "Barbetta et al." × três autores.

## B. Conclusões a corrigir (CRÍTICO)
- B1. **Parte V × Parte IV.**
  - O problema: a 5.1.3 usa o AFT log-normal (pior AIC: 8.273 contra 7.958 da Weibull) como "modelo de referência da Parte IV" e conclui que o rito não tem efeito.
  - A Parte IV conclui que há efeito: Remota HR 0,81. Recalculado: Cox grupo + mês, Remota 0,82 [0,68; 0,98], p 0,03.
  - Correção: refazer com Cox/Weibull e reescrever as células 310, 312, 354 e 359.
- B2. **Efeito do mês.**
  - O problema: "+20% ao mês" (TR log-normal) dá 2,5× de jan a jun, mas as medianas KM sobem só 1,32× (≈ 6% ao mês). O Cox com mês categórico não é monótono.
  - Correção: rever as células 312 e 362.
- B3. **Sem mérito.**
  - Contradição: a síntese da Parte II (células 167/168) diz "excesso nas extinções precoces". A 2.5.2 e os dados mostram o contrário: tardias (> 30 dias: 26/45/48).
  - Base dos sentenciados: o "+15 a 17 p.p., o maior efeito" é condicional aos sentenciados. Sobre os distribuídos: +9,5 p.p. (Presencial, p 0,011) e +6,3 p.p. (Remota, p 0,09).
  - Janela fixa: em 65 dias, Remota 20,6% × Controle 20,8%; o excesso da Remota só aparece com seguimento ≥ 150 dias.
  - Correção: reescrever nas Partes II, III (célula 187), V e VII ("robusto para a Presencial; na Remota, tardio e menor") e remeter à CIF.
- B4. **DiD da Parte VIII não identificado.**
  - O problema: "a diferença de seguimento se cancela" é falso. No 4º JEC, com o mesmo seguimento, o mérito cai 9,7 p.p. (não 13,6) e a sentença cai 5,2 p.p. (não 11,2).
  - A manchete "−11,8 p.p., o maior dos 14" e a frase "a unidade como um todo, sim" precisam ser rebaixadas a descritivas.
  - As tendências paralelas foram anunciadas e não testadas; há células sem saída e a mensagem "faltam 26 de 28 fatias".
  - A permutação com 14 unidades tem p mínimo de 0,071.
- B5. **Generalização para a Presencial** (7.1, 7.3, 6.11, 7.5).
  - O problema: "a AC obrigatória, presencial ou remota, alongou" não vale para a Presencial: HR 0,87 [0,72; 1,04], ΔRMST 6,5 [−2,1; 15,8].
  - Correção: afirmar o efeito só para a Remota; Presencial = mesma direção, não significativa.

## C. IMPORTANTE
- C1. Bug em `_formatador` (secao01 l.421): colunas com "%" no nome ("IC 95% inf.") saem com 1 casa.
  - Exemplo: Cox (b), Remota, aparece como "0,7–1,0", mas o valor real é 0,675–0,970.
  - Tabelas afetadas: IV.9, 14–16, 19, 21, 27, 28, 30, 31 e V.4.
- C2. Fine-Gray por IPCW: o EP sanduíche com pesos fracionários está inflado (0,20 contra bootstrap 0,16). O p de "sem mérito" na Presencial cai de 0,011 para 0,052 e a célula 290 não comenta.
- C3. "Retarda as sentenças por cerca de dois meses" (célula 274): o atraso real é ~15 dias na mediana e ΔRMST180 de 6,5/10,7 dias.
- C4. Modalidade: "a presencial produz mais extinções; a remota, mais acordos" (célula 301, Fig. IV.27) não foi testado diretamente (os IC se sobrepõem). Na Parte V (células 315/330), a modalidade está confundida com a conciliadora; Remota × Presencial tem p Holm 0,198.
- C5. Cortes 0–30/30–90/>90 e destaque ao FH(1,1) escolhidos depois de ver os dados: declarar.
- C6. Robustez:
  - "12 cenários" / "0,79 a 0,82 em todos" (VI) contra 11 de 12 e 0,77–0,83 (IV); no cenário (vi) o IC inclui 1;
  - "Weibull exclui 1" com p 0,051 (célula 407).
- C7. H10 "a vara ficou mais lenta": vale para os braços com AC (ρ 0,14; 0,22), não para o Controle (ρ 0,05; p 0,34).
- C8. H6/CMH (acordo fora da AC) são condicionais aos encerrados sem aviso. O "porteiro" global não é seguido na 3.7. Separar no registro os testes inferenciais dos didáticos. A H2 é gerada pelos dados.
- C9. Parte III, célula 209: as medianas 80/93/94 e o p ≈ 0,03 são da base do professor; os corretos são 81/96/95 e 0,023.
- C10. Hosmer-Lemeshow depende da ordem das linhas (p de 0,06 a 0,98). Usar o Pearson por padrão de covariáveis (p 0,76).
- C11. Árvore `mul_arvore_A.png` quebrada: sem arestas e com cores de classe trocadas. A interpretação (célula 336) diverge da árvore (47 e não 60; corte em ~27/05, não 13/03). Conferir B e C.
- C12. Conclusão da 5.5 × Tabela V.18: o grupo não melhora o Brier. O Weibull é pior que o nulo.
- C13. DataJud:
  - sentenças superadas (4 casos) e a regra "1º julgamento";
  - κ honesto R1 0,955 (não 0,971), e κ da AC só nos braços AC = 0,972;
  - "106,8 não se reproduz" → "não verificável com a mesma definição";
  - "análise principal conservadora" → "coerente, um pouco maior";
  - χ² entre censurados é condicional à sobrevivência.
- C14. 13,3% (homologações ÷ sentenças) comparado com o acordo por AC (5%), com denominadores incompatíveis. A medida comparável é 11,4%.
- C15. 2.2/2.3:
  - "não falta aleatorização" é forte demais: sorteio restrito, não documentado e sem ocultação (gabinete do juiz-pesquisador; compensação em julho);
  - "sem perdas" ignora as 24 redistribuições.
- C16. 2.11: atribuições a Becker (Holm, FDR, TOST, poder) e a Barbetta (CMH, FFH) duvidosas e sem página. O TOST é chamado de "indispensável" mas não foi feito.
- C17. 2.12: falta a dimensão ético-jurídica (comitê de ética, Res. CNS 510/2016, consentimento, isonomia, base legal do Controle diante dos arts. 16/21/22 da Lei 9.099). Poder pós-hoc usado como argumento (célula 413).
- C18. Curadoria:
  - reentradas: o 0808905-44 volta no dia seguinte e segue ativo, mas é contado como Redistribuição;
  - unir os episódios na sensibilidade;
  - `acordo_ac`/`hibrida` = False no Controle (zero estrutural não marcado);
  - texto misturando 944 linhas e base primária (26 × 24 redistribuições; 316/314);
  - "censura desigual invalida médias" mal argumentado (célula 67).
- C19. Parte II:
  - "pico inicial… e pelas redistribuições" está errado: a redistribuição é censura nesse ajuste;
  - binomial contra a taxa do Controle tomada como fixa;
  - "ativos dominam > 150 dias" falso (40 × 38);
  - números escritos à mão sem tabela (faixas 39/48/34; 38,1% × 26,5%).

## D. MENOR (agrupado)
- Português/consistência:
  - "o pesquisador" × "a pesquisadora";
  - data fixa "hoje (12/11/2026)";
  - "J a O, três ocultas";
  - 316/314/314 fora de ordem;
  - 3,6% de 28;
  - Monte Carlo 0,567 × 0,566;
  - 0,68 × 0,67;
  - 0,55 × 0,54;
  - ρ 0,140 × 0,138;
  - 209 × 206 ativos.
- Formatação:
  - `cnj_ano` "2.026";
  - "mediana 473.5";
  - "P / R / O" sem legenda;
  - índice espúrio na V.13;
  - "1 folhas";
  - catálogo com 180 × 178 tabelas e "A: 0 tabelas".
- Figuras:
  - título da Fig. II.32 contradiz a leitura;
  - eixo da Fig. III.24 "truncado em 16";
  - nota "laranja" na Fig. VIII.7 sem barras laranja;
  - painel A.1(e) 112 × 112,5;
  - borda do risco suavizado na Presencial;
  - aviso de `tight_layout` (célula 406) visível;
  - caminhos absolutos `C:\Users\MPGO\...` nas saídas.
- Métodos:
  - dfbeta × DFBETAS;
  - KM reverso mal explicado;
  - τ = 150 "> 30% em observação";
  - Gray por permutação (H0 forte);
  - IIA sem teste;
  - AUC/KS;
  - χ² de aderência 0,99999 ("equitativa", não "sorteio").

---
## Status das correções (16/11/2026)
- **Estrutura.** Aplicada a nova ordem: I–V → VI DataJud → VII Questões → VIII Síntese → REFERÊNCIAS (`secao98_referencias.py`) → Apêndice. A introdução foi atualizada e as remissões, renumeradas. Backup do estado anterior em `_tmp/backup_2026-11-16/`.
- **Itens A, B e C.** Todos aplicados pelas partes, cada uma testada isoladamente e depois no build completo (0 erros, 0 avisos).
- **Mudanças de substância nas conclusões:**
  - o efeito significativo sobre o tempo é só da Remota;
  - o déficit de mérito é robusto em horizonte fixo, enquanto o excesso de sem mérito e o de acordo são sugestivos;
  - o DiD da Parte VI é descritivo;
  - o κ R1 é 0,961;
  - o seguimento estendido dá Remota HR 0,75 e ΔRMST180 14,6, ou seja, é "coerente", não "conservador".
- **Referências.** Lista única com 57 obras, conferida nos dois sentidos contra as citações do texto.
- **Pendências do aluno:**
  - edição de Barbetta, Reis e Bornia (o Enajus cita 2025, p. 13);
  - edição e tradutor de Moore, Notz e Fligner (2023);
  - páginas de Becker (2015), Barbetta e Siegel & Castellan (2006) na resposta à 2.11.
