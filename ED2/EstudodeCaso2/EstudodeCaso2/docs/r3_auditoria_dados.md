# R3 — Auditoria dos dados brutos (Estudo de Caso 2)

**Arquivo:** `C:\Users\MPGO\AulaCleuler\EstudodeCaso2\ControleDosProcessos_Mestrado_Atualizacao_07.10.2026.xlsx`
**Aba analisada:** `Processos` (tabela Excel `TAB_DADOS`, intervalo `A2:O946`) — cabeçalho na linha 2, dados nas linhas 3–946 (**944 linhas**, 938 números de processo distintos).
**Ferramentas:** pandas 3 (valores em cache) + openpyxl (`data_only=False` para fórmulas; leitura do XML bruto para validações x14).
**Convenção:** "linha" = número da linha no Excel (`xlrow`). Scripts auxiliares em `...\scratchpad\aud\s1.py`–`s10.py`.

---

## 1. Estrutura do arquivo e metadados

| Item | Achado |
|---|---|
| Abas | `Processos` (dados), `Dash1–3` (dashboards/slicers, sem dados úteis), `Tab_D` (**oculta**, tabelas dinâmicas), `Tabelas` (resumos com fórmulas), `Resumo` (questionário; valores vazios no cache), `Lista` (**oculta**, listas de validação) |
| Última gravação | 2026-10-07 19:57:29 (usuário `pvccr`); criado em 2026-01-28 |
| Colunas ocultas em `Processos` | **J (DURAÇÃO-SENT2), M (DURAÇÃO-PROC)** e P |
| Linhas ocultas | nenhuma em `Processos` |
| Comentários | nenhum em `Processos`; 10 em `Tabelas` (definições de "eficiência") |
| Nomes definidos | segmentações (slicers) de SORTEIO, STATUS, TÉCNICA, SENTENÇA e linha do tempo de DT. DISTRIBUIÇÃO (todos `#N/A` no openpyxl) |
| Linha 1 | totalmente vazia (por isso `header=1`) |
| Coluna 16 (P) | vazia |

### 1.1 Colunas digitadas × calculadas

| Col | Nome (original) | Natureza |
|---|---|---|
| A | NÚMERO DO PROCESSO | digitado |
| B | DT. DISTRIBUIÇÃO | digitado (datetime, todas preenchidas) |
| C | SORTEIO | digitado, validação `Lista!A2:A5` |
| D | HÍBRIDA | digitado, validação `Lista!G2:G4` (`**`/Sim/Não) |
| E | TEVE ACORDO NA AC? | digitado, validação `Lista!G2:G4` |
| F | TÉCNICA | digitado, validação `Lista!C2:C8` (aplicada em faixas com lacunas) |
| G | TEVE ACORDO FORA DA AC? | digitado, validação `Lista!G2:G4` |
| H | SENTENÇA | digitado, validação `Lista!E2:E6` |
| I | DT. SENTENÇA | digitado |
| J–O | durações, texto e STATUS | **fórmulas** (943 linhas; a **linha 920 não tem fórmula nenhuma**) |

### 1.2 Fórmulas (essencial para a data de censura)

```
DURAÇÃO-PROC (M) = ABS( IF(AND(B="",I=""),"", IF(AND(B<>"",I<>""), I-B, TODAY()-B)) )
DURAÇÃO-SENT2 (J) = IF([SENTENÇA]="**","", <mesma expressão>)
DURAÇÃO-TECN  (K) = IF([TÉCNICA]="**","",  <mesma expressão>)
DURAÇÃO-SORT  (L) = IF([SORTEIO]="**","",  <mesma expressão>)
DURAÇÃO DO PROCESSO (N) = IF(M="","", M & " dia(s)")
STATUS (O) = IF(AND(B="",I=""),"", IF(AND(NOT(ISBLANK(B)),NOT(ISBLANK(I))),"Encerrado","Ativo"))
```

Consequências:

1. **A data de referência dos processos Ativos é `TODAY()` (volátil).** Nos valores em cache, `DT.DISTRIBUIÇÃO + DURAÇÃO` = **2026-10-07 para os 209 Ativos** (coerente com o nome do arquivo e a data de gravação). Se o arquivo for aberto e recalculado hoje (2026-11-12), todos os tempos censurados aumentam 36 dias, sem que haja nova informação. → **Fixar a data de censura administrativa em 2026-10-07** e recalcular o tempo em Python a partir das datas; nunca usar as colunas de duração do Excel.
2. `ABS()` mascararia durações negativas (erro de digitação sentença < distribuição). Verificado nas datas brutas: **0 casos** de sentença anterior à distribuição.
3. `STATUS` é derivado exclusivamente do preenchimento de `DT. SENTENÇA` — "Encerrado" inclui a `Decisão` (redistribuição), que não é sentença.
4. As 4 colunas de duração são **idênticas** onde não nulas (verificado célula a célula): SENT2 e SORT = PROC em 943/943 (nunca há `**` em SENTENÇA/SORTEIO); TECN = PROC em 428 linhas (nula onde TÉCNICA = `**`). São apenas filtros para as tabelas dinâmicas. **Atenção:** TECN só exclui `**`; as **76 linhas com TÉCNICA vazia (Ativos sem AC) recebem duração** e entram na média da pesquisadora como "(vazio)" (TAB-03, média 91,2 dias).
5. `DURAÇÃO DO PROCESSO` (texto) = PROC em 943/943 → redundante.

---

## 2. Tipos e ausências por coluna

| Coluna | dtype lido | NaN | `**` | Valores válidos |
|---|---|---|---|---|
| NÚMERO DO PROCESSO | str | 0 | 0 | 944 (938 distintos) |
| DT. DISTRIBUIÇÃO | datetime | 0 | – | 2026-01-01 a 2026-08-03 |
| SORTEIO | str | 0 | 0 | P 316 · R 314 · O 314 |
| HÍBRIDA | str | 72 | 0 | Não 841 · Sim 31 |
| TEVE ACORDO NA AC? | str | 75 | 0 | Não 852 · Sim 17 |
| TÉCNICA | str | 77 | **515** | 352 (6 técnicas) |
| TEVE ACORDO FORA DA AC? | str | 208 | **1** (linha 888) | Não 671 · Sim 64 |
| SENTENÇA | str | 210 | 0 | 734 (5 grafias) |
| DT. SENTENÇA | datetime | 210 | – | 2026-01-07 a 2026-10-06 |
| DURAÇÃO-SENT2/SORT/PROC | float | 1 (linha 920) | – | 0 a 274 |
| DURAÇÃO-TECN | float | 516 | – | 428 |
| DURAÇÃO DO PROCESSO | str | 1 | – | "N dia(s)" |
| STATUS | str | 1 (linha 920) | – | Encerrado 734 · Ativo 209 |

- **Strings vazias / só espaços:** nenhuma (pandas lê células vazias como NaN).
- **`(vazio)`** não existe nos dados: é o rótulo que a tabela dinâmica dá às células em branco (`Tab_D`).
- **Semântica de `**`:** em TÉCNICA significa "AC não realizada / não se aplica" (todos os 314 do Rito Opcional + 112 P + 89 R); NaN significa "ainda não informado" (quase sempre Ativo). **Não fundir `**` com NaN.**

### 2.1 Padrões de ausência (HÍBRIDA, ACORDO_AC, TÉCNICA, ACORDO_FORA, SENTENÇA; 1 = NaN)

| Padrão | Encerrado | Ativo | STATUS NaN | P | R | O | Interpretação |
|---|---|---|---|---|---|---|---|
| 00000 | 733 | 0 | 0 | 240 | 225 | 268 | completo |
| 00011 | 0 | 132 | 0 | 50 | 36 | 46 | AC já ocorreu, aguarda sentença |
| 11111 | 0 | 71 | 1 | 24 | 48 | 0 | AC ainda não realizada (recém-distribuídos) |
| 01111 | 0 | 3 | 0 | 1 | 2 | 0 | linhas 268, 369, 832 |
| 00111 | 0 | 1 | 0 | 0 | 1 | 0 | linha 249 (acordo AC = Não, técnica vazia) |
| 00001 | 0 | 2 | 0 | 0 | 2 | 0 | linhas 566, 607 (acordo fora já marcado, sem sentença — plausível) |
| 00100 | 1 | 0 | 0 | 1 | 0 | 0 | **linha 373**: Encerrado com TÉCNICA vazia |

Ausências são **estruturais** (dependem do estágio do processo), não aleatórias. Nenhuma imputação é necessária para a análise de sobrevivência: as covariáveis de processo (HÍBRIDA, TÉCNICA) são pós-randomização e não entram no modelo principal.

---

## 3. Variantes de grafia e categorias

| Coluna | Problema | Contagem | Linhas | Tratamento |
|---|---|---|---|---|
| SENTENÇA | `Extinção do feito sem julgamento de mérito` (minúsculas) vs `Extinção do Feito sem Julgamento de Mérito` | 11 vs 275 → **286** | 3, 13, 16, 34, 35, 36, 42, 46, 63, 68, 69 (todas de jan/2026) | **recodificar** para a forma canônica. A validação de lista do Excel não diferencia maiúsculas — por isso passou. As tabelas dinâmicas já agrupam (TAB-04 mostra 286) |
| NÚMERO | espaço/quebra de linha final | 2 | 692 (`0809702-20…5004␠␠`), 771 (`0811548-72…5004\n`) | `strip()` |
| NÚMERO | hífen final | 2 | 55 (`…5004-`), 377 (`…5004 -`) | remover sufixo; DV confere com 5004 |
| NÚMERO | órgão truncado (3 dígitos) | 2 | 443 (`0806633-77.2026.8.20.500`), 453 (`0806739-39.2026.8.20.500`) | completar para **5004**: o DV só fecha com 5004/5101/5198/5295/5392 entre 5000–5400, e 5004 é a vara do estudo → recodificar e sinalizar `cnj_corrigido=True` |
| TEVE ACORDO FORA DA AC? | valor `**` | 1 | 888 (P, sem mérito, 8 dias) | recodificar para `Não` (desfecho sem mérito, sem homologação) |
| HÍBRIDA | `Lista!I` prevê `**`/`Híbrida`, mas a coluna usa `Sim`/`Não` | – | – | lista `I` está obsoleta; usar Sim/Não → bool |

Demais categorias sem variantes (verificado `strip`/caixa/acentos): SORTEIO (3), TÉCNICA (6 + `**`), STATUS (2), Sim/Não.

---

## 4. Número CNJ (NNNNNNN-DD.AAAA.J.TR.OOOO)

- Fora do padrão regex: **4** (linhas 55, 377, 443, 453 — ver acima). Após `strip`: 940 válidos.
- **Dígito verificador (mod 97, Res. CNJ 65/2008): 940/940 válidos; 0 inválidos.**
- J.TR = **8.20 (TJRN)** em 100%.
- Ano × órgão de origem:

| Ano | Órgão | n | Obs. |
|---|---|---|---|
| 2026 | 5004 | 928 | vara do experimento |
| 2026 | 5300 | 3 | linhas 215, 454, 546 |
| 2026 | 5001 | 2 | linhas 49, 941 |
| 2026 | 5106 / 5124 / 5129 | 1 / 1 / 1 | linhas 699, 184, 438 |
| 2025 | 5004 | 2 | linhas 21, 234 |
| 2025 | 5300 | 1 | linha 5 |
| 2023 | 5004 | 1 | linha 244 |

**16 processos** com numeração de outro órgão ou ano anterior: são processos **redistribuídos para a vara** (a "DT. DISTRIBUIÇÃO" é a data de chegada na unidade, não o ajuizamento). **Manter** (entraram no sorteio na chegada; o relógio do estudo começa ali), criar flag `origem_externa`, e fazer análise de sensibilidade excluindo-os.

---

## 5. Duplicidades de número de processo (6 números, 11 linhas)

| Processo | Linhas | Grupo | Dist. | Sentença | Situação | Tratamento recomendado |
|---|---|---|---|---|---|---|
| 0802424-65.2026.8.20.5004 | 162 / **164** | P / P | 13/02 / 13/02 | Decisão 18/02 / — | 164 é Ativo, tudo vazio, mesma data | **excluir 164** (duplicata de digitação; geraria um falso censurado de 236 dias) |
| 0812314-28.2026.8.20.5004 | **819** / 822 | R / R | 08/07 / 08/07 | — / Homologação 16/09 | 819 Ativo vazio | **excluir 819** (registro desatualizado) |
| 0812839-10.2026.8.20.5004 | 851 / **857** | R / R | 15/07 / 16/07 | — / — | ambos Ativos; 851 tem técnica | **excluir 857** (manter o registro mais antigo e mais completo) |
| 0804436-52.2026.8.20.5004 | 290 / 322 / 475 | **P / P / O** | 18/03, 24/03, 27/04 | Decisão (0, 16, 0 dias) | 3 entradas, todas redistribuídas, **re-sorteadas** | primário: **manter só o 1º episódio (290)** (intenção de tratar); sensibilidade: excluir o processo |
| 0808905-44.2026.8.20.5004 | 591 / 607 | R / R | 20/05 / 22/05 | Decisão 21/05 / — | voltou 1 dia depois e segue Ativo | primário: manter 591 (Decisão); sensibilidade: unir os episódios (início 20/05, censurado em 07/10) |

Lição de desenho: um processo que sai por `Decisão` e volta é **sorteado de novo** (0804436 trocou de braço P→O). Recomendar à pesquisadora que a reentrada herde o grupo original.

Após deduplicar por número: P 314 · O 313 · R 311 (938).

---

## 6. Datas e durações

| Verificação | Resultado |
|---|---|
| Faixa de distribuição | 2026-01-01 a **2026-08-03** (ago/26 só tem 6 processos, 1–3/ago → **fim do recrutamento em 03/08/2026**) |
| Faixa de sentença | 2026-01-07 a **2026-10-06** |
| Sentença < distribuição | **0** |
| Sentença ou distribuição após 07/10/2026 | 0 |
| Duração = 0 (mesmo dia) | **39** (30 sem mérito + 3 sem mérito em minúsculas + 6 Decisão) |
| Duração ≤ 1 dia | 94 |
| Encerrado: `DURAÇÃO-PROC` = DT.SENT − DT.DIST | 734/734 |
| Ativo: `DURAÇÃO-PROC` = 07/10/2026 − DT.DIST | 208/209 + linha 920 (sem fórmula) |
| Ativo com data de sentença / Encerrado sem data | 0 / 0 (STATUS é derivado da data) |
| Tipo de sentença sem data ou data sem tipo | 0 / 0 |
| Ordem das linhas | estritamente não decrescente por data de distribuição (0 inversões) |
| Distribuição em sábado/domingo | 56 (PJe aceita peticionamento em fim de semana — plausível) |
| **Sentença em sábado/domingo** | **135 (18,4%)**, com picos em datas únicas: 30/05 (sáb.) 17; 26/04 (dom.) 13; 18/07 (sáb.) 13; 08/08 (sáb.) 12; 19/09 (sáb.) 9+ |

**Alerta sobre DT. SENTENÇA:** a concentração em fins de semana e em poucas datas (16/09: 24; 23/09: 22; 25/08: 20; 30/05: 17) sugere que, em parte, a coluna pode registrar a **data de lançamento/movimentação em lote** (ou mutirão), e não a assinatura da sentença. Não é corrigível internamente → **manter**, documentar como limitação e, se possível, validar uma amostra contra DataJud/PJe (movimento CNJ de julgamento/extinção).

### 6.1 Linha 920 (0813782-27.2026.8.20.5004)
Sem nenhuma fórmula (J–O vazias), STATUS vazio, P, distribuída em 29/07/2026, sem sentença. É a única do `STATUS (vazio)` = 1 em `Tab_D`. → **manter como Ativo, censurado em 07/10/2026 (70 dias)**.

### 6.2 Tempo de acompanhamento (censura administrativa)
- Data de corte: **07/10/2026**. Última distribuição 03/08 → acompanhamento mínimo de **65 dias** para todos.
- Ativos (209): mediana 97 dias (mín. 65, máx. 274); por grupo: O 46 (mediana 111,5), P 74 (102), R 89 (89).
- Proporção encerrada por coorte de distribuição: jan 97% · fev 99% · mar 93% · abr 89% · mai 84% · **jun 63% · jul 36% · ago 17%**. A censura é essencialmente administrativa (fim do estudo), dependente da data de entrada — compatível com censura não informativa *dentro* de cada coorte. Como R recebeu mais processos em julho (ver §7), R tem mais censura; isso **não** viesa KM/Cox, mas invalida as **médias simples** do Excel.
- Ativos antigos (> 230 dias): linhas 4 (274 d, O), 39 (264 d, O), 64 (257 d, R), 164 (duplicata, excluir).

---

## 7. Sorteio (alocação)

| Mês | O | P | R | Total |
|---|---|---|---|---|
| 2026-01 | 37 | 34 | 32 | 103 |
| 2026-02 | 34 | 36 | 37 | 107 |
| 2026-03 | 57 | 51 | 44 | 152 |
| 2026-04 | 48 | 46 | 44 | 138 |
| 2026-05 | 52 | 45 | 50 | 147 |
| 2026-06 | 39 | **59** | 34 | 132 |
| 2026-07 | 46 | 44 | **69** | 159 |
| 2026-08 | 1 | 1 | 4 | 6 |
| **Total** | **314** | **316** | **314** | 944 |

- Qui-quadrado mês × grupo: χ² = 21,1; p = 0,099 (sem desequilíbrio temporal significativo ao nível de 5%).
- Sequência na ordem das linhas: **não é cíclica** (P,R,O). Transições aproximadamente uniformes (90–122 cada); posições mod 3 sem padrão; só 73/314 trincas consecutivas são permutações (esperado ≈ 22% ao acaso → 70).
- **Teste de sequências (runs, 3 categorias):** 629 sequências vs 630,3 esperadas, z = −0,09 → compatível com aleatoriedade. Sequência máxima: 8 R seguidos. Por mês, |z| ≈ 2 em jan (−2,02), fev (+2,01) e jul (−1,99) — limítrofes, sem padrão sistemático.
- **Equilíbrio final notável:** totais 316/314/314. Sob sorteio simples (1/3 cada), P(máx − mín ≤ 2) ≈ **0,5%** (simulação, 200 mil réplicas). Porém o desequilíbrio acumulado chegou a **32** (linha 763, fim de junho) e foi compensado em julho (R = 69). Padrão compatível com **sorteio restrito** (lista pré-gerada balanceada, sorteio sem reposição ou cotas), não com sorteio simples. Não invalida a randomização, mas **confirmar o mecanismo com a pesquisadora** e descrevê-lo no relatório; se houve compensação deliberada no fim, ajustar por período (estratificar Cox por mês de distribuição como sensibilidade).

---

## 8. Consistência das variáveis de processo

### 8.1 HÍBRIDA × grupo
| | P | R | O |
|---|---|---|---|
| Sim | 28 | **3** | 0 |
| Não | 264 | 263 | 314 |
| NaN | 24 | 48 | 0 |

- **3 audiências híbridas no grupo Remota** (deveria ocorrer só na Presencial): linhas **318** (0804822-82), **456** (0806797-42), **832** (0812493-59, Ativo, técnica vazia). → **manter no grupo sorteado (ITT)**; flag `desvio_protocolo`. Para análise "conforme tratado", reclassificar como híbrida.
- **3 híbridas (P) com TÉCNICA `**`** (AC não realizada?): linhas 433, 455, 712 — contraditório (marcar híbrida implica audiência). → manter; flag; perguntar à pesquisadora.

### 8.2 Acordo na AC, técnica e grupo
| | P | R | O |
|---|---|---|---|
| Acordo na AC = Sim | 9 | 8 | **0** |
| Acordo na AC = Não | 282 | 256 | 314 |
| NaN | 25 | 50 | 0 |
| TÉCNICA ≠ `**` (AC realizada) | 178 | 174 | **0** |
| TÉCNICA = `**` | 112 | 89 | 314 |
| TÉCNICA NaN | 26 | 51 | 0 |

- **Rito Atual Ac Opcional: 0 audiências de conciliação, 0 técnicas, 0 acordos na AC** em 314 → o grupo O é, na prática, "sem AC". Coerente; documentar.
- Acordo na AC = Sim sem técnica: **0**. Técnica no grupo O: **0**.
- Acordos por técnica (AC): Parafraseamento 6/57, Separação 5/60, Análise da Comunicação 2/63, Desconstrução 2/47, Padrões 2/67, Afago 0/58 — total 17 (n pequenos: não sustentam comparação inferencial entre técnicas).
- **Linha 373** (0805675-91, P, Encerrado sem mérito em 1 dia): TÉCNICA vazia → recodificar `**` (AC não realizada; extinção no dia seguinte).
- **Linha 249** (0803708-11, R, Ativo): acordo AC = Não mas técnica vazia → manter NaN (não imputar).

### 8.3 Acordo × sentença (coerência perfeita)
| Sentença | Acordo AC=Sim | Acordo fora=Sim | Nenhum |
|---|---|---|---|
| Homologação do Acordo (81) | 17 | 64 | **0** |
| Mérito (341) | 0 | 0 | 341 |
| Sem mérito (286) | 0 | 0 | 286 (1 com `**` em "fora") |
| Decisão (26) | 0 | 0 | 26 |

Nenhum acordo marcado sem homologação; nenhuma homologação sem acordo; nenhum caso com acordo na AC e fora ao mesmo tempo. Total de acordos = 81 (bate com `Tabelas`).

### 8.4 Desfecho × grupo × status
| Sentença | O | P | R | Total |
|---|---|---|---|---|
| Mérito | 162 | 96 | 83 | 341 |
| Sem mérito (unificada) | 79 | 109 | 98 | 286 |
| Homologação | 21 | 25 | 35 | 81 |
| Decisão | 6 | 11 | 9 | 26 |
| Ativo (sem sentença) | 46 | 74+1* | 89 | 210 |
| **Total** | 314 | 316 | 314 | 944 |
\* linha 920 (STATUS vazio).

Tempo (dias) até o desfecho entre encerrados — mediana [média]:

| | O | P | R |
|---|---|---|---|
| Mérito | 83 [91,1] | 112,5 [114,4] | 106 [110,1] |
| Sem mérito | 9 [30,0] | 24 [31,3] | 28,5 [42,1] |
| Homologação | 61 [69,8] | 57 [66,4] | 62 [66,7] |
| Decisão | 1 [4,2] | 1 [3,0] | 8 [25,4] |

Nos grupos P/R, os processos com TÉCNICA `**` (AC não realizada, n = 201) terminam muito cedo (sem mérito: mediana 6 dias; n = 151) — são extinções **antes** de a intervenção poder atuar (desistência, indeferimento etc.).

### 8.5 `Decisão` (redistribuição por prevenção) — 26 linhas
Todas "Encerrado". Duração: mediana **1 dia**, média 11,0; 6 com 0 dia; 2 após a AC (linhas **395**: 84 dias, R, técnica Afago; **571**: 74 dias, R, Padrões). Inclui 3 linhas do processo 0804436-52 e 1 do 0808905-44 (ver §5). Linhas: 14, 77, 93, 162, 168, 290, 295, 304, 312, 322, 329, 344, 395, 418, 431, 475, 503, 540, 546, 571, 591, 664, 695, 799, 823, 916.

---

## 9. Números da própria pesquisadora (abas `Tab_D`/`Tabelas`) — conferência

| Indicador do Excel | Valor | Conferido | Comentário |
|---|---|---|---|
| Encerrado: média / n | 68,85 / 734 | ✔ | |
| Ativo: média / n | 112,18 / 209 | ✔ | tempo até 07/10 (censurado) |
| Média geral | 78,46 / 943 | ✔ | **mistura censurados com eventos → estimador inválido** |
| Média por rito P / R / O | 77,50 / 80,87 / 77,00 | ✔ | idem; "O mais rápido / R mais lento" (`Resumo`) não é inferência válida |
| TAB-03 "(vazio)" | 91,18 / 76 | ✔ | Ativos sem técnica entram na média de técnicas |
| Acordos AC P/R/O | 9 / 8 / 0 | ✔ | |
| Acordos fora P/R/O | 16 / 27 / 21 | ✔ | |
| "Eficiência" | razão acordos/total | – | proporções brutas, sem IC nem tempo |

As médias aritméticas devem ser **substituídas** por Kaplan–Meier (mediana, RMST) e Cox/AFT.

---

## 10. Catálogo de anomalias e tratamento

| # | Anomalia | n | Linhas / processos | Tratamento | Justificativa |
|---|---|---|---|---|---|
| A1 | Data de censura = `TODAY()` volátil | 209 | todos os Ativos | **censurar em 07/10/2026 (fixa)**; recalcular tempo pelas datas | reprodutibilidade; cache = 07/10 |
| A2 | Linha sem fórmulas / STATUS vazio | 1 | 920 | manter; Ativo censurado (70 d) | data de distribuição válida |
| A3 | Duplicata espúria (mesma data, vazia) | 2 | 164, 819 | **excluir** | registros duplicados criariam censurados falsos |
| A4 | Duplicata em dias consecutivos | 1 | 857 | **excluir** (manter 851) | mesmo processo, mesmo grupo |
| A5 | Reentrada após Decisão, re-sorteada | 3 | 322, 475 (0804436-52); 607 (0808905-44) | primário: manter só 1º episódio; sensibilidade: unir/excluir | ITT: 1 unidade = 1 processo, grupo do 1º sorteio |
| A6 | Variante de caixa em SENTENÇA | 11 | 3, 13, 16, 34, 35, 36, 42, 46, 63, 68, 69 | **recodificar** | mesma categoria jurídica |
| A7 | Espaço/quebra/hífen no CNJ | 4 | 55, 377, 692, 771 | `strip` + remover sufixo | DV válido |
| A8 | CNJ truncado (órgão "500") | 2 | 443, 453 | completar 5004; flag | DV fecha com 5004 |
| A9 | Origem/ano externos | 16 | §4 | manter; flag `origem_externa`; sensibilidade | redistribuídos para a vara |
| A10 | `**` em ACORDO FORA | 1 | 888 | recodificar `Não` | sentença sem mérito |
| A11 | TÉCNICA vazia em Encerrado | 1 | 373 | recodificar `**` | extinto em 1 dia, sem AC |
| A12 | Híbrida no grupo Remota | 3 | 318, 456, 832 | manter grupo (ITT); flag desvio | protocolo prevê híbrida só na presencial |
| A13 | Híbrida com TÉCNICA `**` | 3 | 433, 455, 712 | manter; flag; consultar | possível erro de digitação |
| A14 | Ativo com acordo AC preenchido e técnica vazia | 1 | 249 | manter NaN | não imputar |
| A15 | Duração 0 dia | 39 | §6 | manter; para modelos paramétricos usar t = 0,5 dia (convenção documentada, não imputação) | evento real no dia da distribuição |
| A16 | Sentenças em fim de semana / em lote | 135 | §6 | manter; limitação; validar amostra no DataJud | possível data de lançamento |
| A17 | Colunas de duração redundantes, com ABS | – | J–N | **descartar** | recalculadas a partir das datas |
| A18 | Grupo O sem nenhuma AC | 314 | – | documentar | define o contraste real "com AC × sem AC" |
| A19 | Sorteio quase perfeitamente balanceado (P ≈ 0,5% sob sorteio simples) e desequilíbrio de 32 compensado em julho | – | – | confirmar mecanismo; sensibilidade estratificando por mês | validade da randomização |
| A20 | Lista de validação HÍBRIDA (`Lista!I`) obsoleta; validação de TÉCNICA aplicada com lacunas | – | – | ignorar (valores observados são válidos) | – |

**Nunca imputar datas ou durações.** Ativos são **censurados à direita** em 07/10/2026.

Base analítica primária esperada: 944 − 3 (A3/A4) − 3 (A5) = **938 processos** (P 314 · R 311 · O 313).

---

## 11. Esquema *tidy* proposto

| Coluna | dtype | Origem / regra |
|---|---|---|
| `id_linha_excel` | Int64 | linha no Excel (rastreabilidade) |
| `numero_cnj` | string | `strip`, sufixos removidos, órgão completado |
| `cnj_corrigido` | bool | True nas linhas 55, 377, 443, 453 (692 e 771: só `strip`) |
| `cnj_ano` | Int64 | AAAA |
| `cnj_orgao` | category | OOOO |
| `origem_externa` | bool | órgão ≠ 5004 ou ano < 2026 |
| `dt_distribuicao` | datetime64[ns] | B |
| `mes_distribuicao` | period[M] / ordered category | derivado |
| `grupo` | category (ordered: `opcional` < `remota` < `presencial`; referência = `opcional`, rito atual) | C → {Rito Atual Ac Opcional: opcional, Ac Remota: remota, Ac Obrigatória Presencial: presencial} |
| `hibrida` | boolean (pandas `BooleanDtype`, com NA) | D |
| `ac_realizada` | boolean | TÉCNICA ≠ `**` e não NaN → True; `**` → False; NaN → NA |
| `tecnica` | category (6 níveis + NA) | F, `**` → NA com `ac_realizada=False` |
| `acordo_ac` | boolean | E |
| `acordo_fora_ac` | boolean | G (`**` → False) |
| `tipo_desfecho` | category: `merito`, `sem_merito`, `homologacao`, `redistribuicao`, `ativo` | H unificado |
| `dt_desfecho` | datetime64[ns] | I |
| `dt_censura` | datetime64[ns] | constante 2026-10-07 |
| `tempo_dias` | Int64 | `dt_desfecho − dt_distribuicao` se houver; senão `dt_censura − dt_distribuicao` |
| `evento` | Int64 (0/1) | 1 se mérito, sem mérito ou homologação; 0 caso contrário (primário) |
| `evento_cr` | Int64 (0 = censura, 1 = sentença, 2 = redistribuição) | riscos competitivos |
| `causa` | Int64 (0 censura, 1 mérito, 2 sem mérito, 3 homologação, 4 redistribuição) | multiestado / causa específica |
| `flag_desvio_protocolo` | bool | A12, A13 |
| `flag_duplicata` / `episodio` | bool / Int64 | A3–A5 |

Colunas descartadas: DURAÇÃO-SENT2, -TECN, -SORT, -PROC, DURAÇÃO DO PROCESSO, STATUS (recalculável: `status = 'encerrado' if dt_desfecho.notna()`).

---

## 12. Definição de tempo e evento para a análise de sobrevivência

- **Origem do tempo:** `dt_distribuicao` (= momento do sorteio; a unidade entra em risco no dia da distribuição na vara).
- **Escala:** dias corridos (opcionalmente meses = dias/30,44 para gráficos).
- **Censura:** administrativa em **07/10/2026** para todos os processos sem desfecho (incl. linha 920). Censura não informativa plausível (depende só da data de entrada); verificar com KM reverso por grupo.
- **Evento principal:** *sentença de extinção* — com julgamento de mérito, sem julgamento de mérito ou homologação de acordo (**708 eventos** na base primária de 938: 341 mérito, 286 sem mérito, 81 homologação; 24 redistribuições; 206 censurados).
- **`Decisão` (redistribuição por prevenção, 26; 24 após dedup):** o processo sai da vara e o desfecho deixa de ser observável — **não é sentença** e **não é censura não informativa** pura (ocorre por característica do processo: conexão/prevenção). Recomendação:
  1. **Primária:** riscos de causa específica — Cox para "sentença" tratando a redistribuição como censura no seu dia (estima o efeito sobre a taxa de sentença entre os que permanecem na vara; válido para a causa específica).
  2. **Complementar:** função de incidência cumulativa (Aalen–Johansen) com redistribuição como **risco competitivo** e Fine–Gray para a probabilidade de sentença até t.
  3. **Sensibilidade:** excluir as redistribuições — mediana de 1 dia, ocorrem antes de qualquer AC (exceto linhas 395 e 571) e, portanto, são quase "inelegíveis" pós-sorteio; a exclusão afeta pouco a comparabilidade (6/11/9 por grupo).
- **Riscos competitivos entre tipos de sentença:** homologação × mérito × sem mérito são desfechos de natureza distinta (a intervenção atua pelo acordo). Reportar CIF por causa e Cox de causa específica para **homologação** (efeito direto da conciliação) e para **mérito**; o evento composto responde à pergunta de "duração do processo".
- **Sensibilidades adicionais:** (a) landmark/exclusão das extinções sem mérito em ≤ 7 dias (antes da AC); (b) exclusão de `origem_externa`; (c) Cox estratificado por mês de distribuição (A19); (d) "conforme tratado" para A12.
- **Empates e zeros:** 39 eventos em t = 0 — KM/Cox (Efron) aceitam; modelos AFT/Weibull exigem t > 0 → usar t = 0,5 dia com nota metodológica.
