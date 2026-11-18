# Convenções do notebook `rafaelcc_ed2.ipynb`

## Geração

- O notebook é **gerado** por `src/build_rafaelcc_ed2.py`. Nunca editar o `.ipynb` à mão.
- Na raiz do projeto (`C:\Users\MPGO\AulaCleuler`):

  ```
  uv run python EstudodeCaso2/src/build_rafaelcc_ed2.py
  uv run jupyter nbconvert --to notebook --execute --inplace EstudodeCaso2/rafaelcc_ed2.ipynb
  ```

- Cada parte é um arquivo `secaoNN_*.py`, executado com `exec` pelo build, na ordem da lista `SECOES`:
  - `secao01_curadoria.py`
  - `secao02_exploratoria.py`
  - `secao03_testes.py`
  - `secao04_sobrevivencia.py`
  - `secao05_multivariada.py`
  - `secao06_questoes.py`
  - `secao07_sintese.py`
  - `secao99_catalogo.py` (apêndice: painel-resumo e catálogo; só no build completo ou se indicado em `--somente`)

  Arquivo inexistente é ignorado.
- Dentro de uma seção, usam-se três funções:
  - `md(r'''...''')` cria uma célula markdown;
  - `code(r'''...''')` cria uma célula de código;
  - `interp('chave')` cria uma célula de interpretação.
- Os textos de interpretação ficam em `interp_<parte>.py`, num dicionário `INTERP_<PARTE>`. O build carrega automaticamente todo `interp_*.py` e todo dicionário cujo nome começa com `INTERP_`; um erro num arquivo não derruba os outros.
- **Os textos de interpretação são escritos somente depois de executar o notebook e ler as saídas reais.** Enquanto não existem, aparece um marcador "a redigir".
- Prefixe as chaves por parte para evitar colisões:
  - `cur_` curadoria;
  - `exp_` exploratória;
  - `tst_` testes;
  - `sob_` sobrevivência;
  - `mul_` multivariada;
  - `q_` questões;
  - `sin_` síntese.

## Numeração

- Parte I = seções 1.x, Parte II = 2.x, e assim por diante; o título de cada parte é `# PARTE N — TÍTULO`.
- Seções `##`, subseções `###`.

## Ambiente (definido na 1ª célula de código, seção 1.1; não redefinir)

- **Importações:**
  - `pandas as pd`, `numpy as np`, `scipy`, `scipy.stats as stats`;
  - `statsmodels`, `statsmodels.api as sm`, `statsmodels.formula.api as smf`;
  - `lifelines` (`KaplanMeierFitter`, `CoxPHFitter`, `AalenJohansenFitter`);
  - `lifelines.statistics` (`logrank_test`, `multivariate_logrank_test`, `pairwise_logrank_test`);
  - `sklearn`, `scikit_posthocs as sp`;
  - `matplotlib as mpl`, `matplotlib.pyplot as plt`, `seaborn as sns`;
  - `display`, `Markdown`.

  Importações adicionais podem ser feitas localmente na seção.
- **Atenção:** `logrank_test` fica em `lifelines.statistics`. O `from lifelines import logrank_test` do notebook do professor falha e desligava o Kaplan-Meier (E1).
- **Caminhos:**
  - `RAIZ` = pasta `EstudodeCaso2` (resolvida quer o kernel rode na raiz, quer na pasta);
  - `BRUTO` = planilha;
  - `PROC = RAIZ/'dat'/'processado'`;
  - `FIG = RAIZ/'fig'`.
- **Constantes:**
  - `DATA_INICIO = 2026-01-01`;
  - `FIM_RECRUTAMENTO = 2026-08-03`;
  - `DATA_CORTE = 2026-10-07` (censura);
  - `SEMENTE = 2026`, `RNG = np.random.default_rng(SEMENTE)`.
- **Grupos:**
  - `ORDEM_GRUPO = ['Controle', 'Presencial', 'Remota']`, com Controle como referência;
  - `ROTULO_GRUPO` (rótulos longos);
  - `CORES_GRUPO = {'Controle': '#0072B2', 'Presencial': '#E69F00', 'Remota': '#009E73'}` (Okabe-Ito, seguro para daltonismo). **Sempre** colorir os grupos por esse dicionário.
- **Desfechos:** `ORDEM_DESFECHO = ['Homologação', 'Mérito', 'Sem mérito', 'Redistribuição', 'Ativo']` e `CORES_DESFECHO = {'Homologação': '#CC79A7', 'Mérito': '#4B3F8F', 'Sem mérito': '#B8461B', 'Redistribuição': '#7F7F7F', 'Ativo': '#C8C8C8'}` (nenhuma cor de desfecho repete a de um grupo).
- **Formatação pt-BR:**
  - `fmt_br(x, casas=1)` → `1.234,5`;
  - `pct_br(p, casas=1)` → `12,3%`;
  - `p_br(p)` → `< 0,001` ou `0,034`.
- **Avisos:** só filtros específicos (openpyxl `UserWarning`, `FutureWarning`). Nunca usar `warnings.filterwarnings('ignore')` global.

## Dados

- Cada seção começa carregando a base, se ainda não estiver no namespace:

  ```python
  if 'dados' not in globals():
      dados = pd.read_pickle(PROC / 'ed2_tidy.pkl')
  ```

- `ed2_tidy.pkl`: **base primária**, com 938 processos e 37 colunas. Os dtypes são preservados (`category`, `boolean`, `Int64`, `datetime64[ns]`).
- `ed2_todas_linhas.pkl`: as 944 linhas, mais `base_primaria`, `motivo_exclusao` e `reentrada`. Serve só para a sensibilidade.
- `dicionario_variaveis.csv`: o dicionário completo.
- `ed2_log_tratamentos.csv`: o log de tratamentos.
- **Variáveis-chave:**
  - **tempo e evento:** `tempo` (Int64, dias) e `evento` (Int64: 1 = sentença; 0 = censurado, isto é, ativo ou redistribuído);
  - **riscos competitivos:** `evento_cr` (0 = censura, 1 = sentença, 2 = redistribuição);
  - **causa específica:** `causa` (0 = censura, 1 = homologação, 2 = mérito, 3 = sem mérito, 4 = redistribuição);
  - **modelos paramétricos/AFT:** `tempo_pos` (float, com 0 → 0,5);
  - **grupo:** `grupo` (category: Controle/Presencial/Remota) e `grupo_rotulo`;
  - **calendário:** `mes_distribuicao` (ordinal jan–ago), `ciclo`, `dia_estudo` e `ordem_chegada` (1..938);
  - **sensibilidade:** `origem_externa`, `desvio_protocolo`, `hibrida_remota`, `hibrida_sem_ac`, `tempo_zero` e `sentenca_fim_semana`;
  - **audiência e acordo:** `ac_realizada` (boolean com NA), `tecnica`/`tecnica_curta` (NA se não houve AC), `hibrida`, `acordo_ac`, `acordo_fora` e `acordo`.

  O Controle não teve nenhuma AC: os acordos na AC e as técnicas são zeros estruturais nesse grupo.
- Lembrete sobre o lifelines: para usar colunas `Int64`/`boolean` no lifelines, statsmodels ou sklearn, converter antes com `.astype(float)` ou `.astype(int)`.

## Estilo e gráficos (preferências do usuário)

- Texto em **português, com acentos**, em tom acadêmico. Cada passo é explicado em markdown antes do código, e cada resultado é interpretado depois.
- Números no texto em pt-BR: vírgula decimal e ponto de milhar.
- Kaplan-Meier: sempre a curva **descendente S(t)**, nunca 1 − S(t), com IC e tabela de número em risco quando possível.
- **Proibido histograma com escala logarítmica.**
- Preferir **barras verticais** e **boxplots**.
- **Cada teste estatístico tem o seu próprio gráfico.**
- Ao corrigir um erro do notebook do professor, citar o código (E1–E30, ver `docs/r2_notebook_professor.md`).
- Anomalias dos dados: códigos A1–A20 (ver `docs/r3_auditoria_dados.md`). Correções a esse documento:
  - `origem_externa` tem **12** processos (não 16);
  - há **5** números repetidos em 11 linhas (6 linhas excedentes).

## Camada de visualização (seção 1.2 — obrigatória para todas as partes)

Toda figura e toda tabela passa por `figura()` / `tabela()`. Não use `display(df)` para resultados, nem `plt.show()`, `plt.tight_layout()` ou `plt.suptitle()` em figuras finais.

### Figuras

```python
fig, ax = plt.subplots(figsize=(9, 5))
...                                    # desenhe; ax.set_title() = o que o painel mostra
figura(fig, 'sob_km_grupos', 'A AC obrigatória atrasa a sentença em cerca de duas semanas',
       secao='4.2.1', nota='IC 95% (Greenwood); marcas = censuras.')
```

- `id` com o prefixo da parte (`cur_`, `exp_`, `tst_`, `sob_`, `mul_`, `q_`, `sin_`, `apx_`); vira `fig/<id>.png` e `.svg`.
- `secao='4.2.1'` define a parte e a numeração (**Figura IV.3**). A numeração é sequencial por parte, na ordem de execução; **não escreva números de figura fixos no markdown/interp** — descreva a figura ("o gráfico de Kaplan-Meier da seção 4.2") ou confira em `CATALOGO` depois de executar. `ref('sob_km_grupos')` devolve 'Figura IV.3' em código.
- `titulo` enuncia o **achado ou a pergunta**, não o tipo de gráfico. `fonte=` tem padrão (planilha do 4º JEC, 07/10/2026); `nota=` para IC, n, cautelas.
- A função converte os eixos numéricos para vírgula decimal e ponto de milhar; textos que você escreve no gráfico usam `fmt_br`, `pct_br`, `fmt_p`.

### Tabelas

```python
tabela(df, 'tst_desfecho_grupo', 'Tipo de desfecho por grupo entre os sentenciados', secao='3.2.1',
       formatos={'OR': 2, 'p': 'p', 'Proporção': 'pct'}, destaque='p Holm', nota='Holm dentro da família H2.')
```

- Legenda numerada (Tabela III.4 — …), pt-BR, valor-p como '< 0,001', inteiros sem casas, `casas=2` por padrão; exporta `tab/<id>.csv` (`;`, vírgula decimal, UTF-8 com BOM) e entra na pasta `tab/ed2_tabelas.xlsx` do apêndice.
- `formatos`: `{coluna: casas | 'p' | 'pct' (proporção → %) | '%' (já em %) | 'int' | 'texto' | função}`. Colunas chamadas `p`, `p Holm`, `p (exato)`… são formatadas como valor-p automaticamente.
- `destaque`: coluna de p (linhas com p < 0,05 em destaque), máscara booleana ou função. `gradiente={'mapa': DIV, 'colunas': [...], 'vmin': -4, 'vmax': 4}` para mapas de calor em tabela.
- Índice: um índice simples com nome vira a 1ª coluna; `RangeIndex` é ocultado; `MultiIndex` é mantido. Nomeie as colunas com unidade ('Mediana (dias)', 'Acordos (%)').
- Dtypes anuláveis (`Int64`, `Float64`, `boolean`) são limpos automaticamente (sem ruído como 'Float64'; booleanos → Sim/Não).

### Auxiliares

| Função | Uso |
|---|---|
| `plot_km(ax, df, tempo='tempo', evento='evento', grupo='grupo', passo=30, tabela_risco=True)` | Kaplan-Meier S(t) **descendente**, IC 95%, marcas de censura, legenda com n e mediana, número em risco sob o eixo. Devolve `{grupo: KaplanMeierFitter}`. `grupo=None` → curva única |
| `boxplot_grupos(ax, df, valor, ylabel=...)` | boxplot vertical por grupo, pontos com jitter, mediana rotulada, n no rótulo do eixo |
| `barras_verticais(ax, categorias, valores, erro=(lo, hi), ns=..., fmt=...)` | barras verticais com valor no topo (`rotular=True`/`'max'`/`False`) e IC |
| `barras_agrupadas(ax, tab, cores=CORES_GRUPO)` | linhas de `tab` no eixo x, colunas = séries; `erro={serie: (lo, hi)}` |
| `barras_empilhadas(ax, tab_prop, cores=CORES_DESFECHO, ns=..., rotulos_serie=ROTULO_DESFECHO)` | 100% empilhadas, rótulo dentro do segmento só se couber |
| `anotar_teste(ax, texto_teste('Log-rank', 'χ² = 7,9 (2 gl)', p, 'HR = 0,82 [0,70; 0,96]'))` | caixa com o resultado do teste dentro do gráfico — **todo teste tem o seu gráfico com o resultado anotado** |
| `anotar_n(ax, posicoes, ns)` | 'n = …' no topo de cada barra/caixa |
| `quebra(texto, 14)` | quebra rótulos longos ('Extinção do Feito com Homologação do Acordo') |
| `eixo_pct(ax)`, `eixo_meses(ax)`, `legenda_abaixo(ax, ncol=3)` | eixo em %, meses em português (nunca `DateFormatter('%b')`), legenda abaixo do eixo |
| `rotulo_grupo(g, com_n=True)`, `ROTULOS[...]`, `ROTULO_DESFECHO[...]` | rótulos legíveis com unidade: `ROTULOS['tempo']`, `['S']`, `['dias']`, `['mes_distribuicao']`… |

### Regras

- **Cor = entidade.** Grupos: `CORES_GRUPO`; desfechos: `CORES_DESFECHO`; situação (sentença/redistribuição/ativo): `CORES_STATUS`/`ORDEM_STATUS`; contexto: `CINZA`; referência externa (linha de meta, valor divulgado): `DESTAQUE`. Magnitude em mapa de calor: `SEQ` (um matiz); sinal (resíduos, log-HR, diferenças): `DIV` centrado em 0 com limites simétricos e barra de cores rotulada. Paletas verificadas para daltonismo na seção 1.2.1.
- **Ordem fixa**: `ORDEM_GRUPO`, `ORDEM_DESFECHO`, meses jan→ago.
- Legenda sempre que houver ≥ 2 séries; rótulos diretos seletivos (extremo, final, a série do achado), nunca um número em cada ponto.
- Barras e boxplots **verticais**; sem dois eixos y; sem histograma em escala log; S(t) descendente; eixos com unidade; n visível (rótulo, legenda ou `anotar_n`).
- Figuras com muitos painéis: prefira 2 × 2 ou figuras separadas a fileiras de 3–4 painéis de 15 polegadas; cada painel com título curto.
- Depois de executar, **olhe os PNG** em `fig/` (sobreposição de rótulos, legenda sobre dados, texto cortado).
