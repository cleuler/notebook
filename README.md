# CDEDPP: Ciência de Dados e Estatística para Programação e Processos

Ambiente pronto para uso com Jupyter Notebook, gerenciado inteiramente pelo
[`uv`](https://docs.astral.sh/uv/). O `uv` cuida de baixar o Python correto,
criar o ambiente virtual e instalar todas as dependências nas versões exatas
usadas em aula — sem depender de nada que já esteja instalado no computador.

## 0. Pré-requisitos (uma única vez por computador)

Instale o `uv` e o Git, caso ainda não estejam disponíveis:

```powershell
# Instalar uv
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Verificar instalação
uv --version
git --version
```

Não é necessário instalar Python manualmente: o `uv` baixa a versão exigida
pelo projeto automaticamente.

## 1. Clonar o repositório

```powershell
git clone https://github.com/rafaelcostaf4-afk/cdedpp.git
cd cdedpp
```

## 2. Preparar o ambiente

Este único comando lê o `.python-version`, baixa o Python 3.12.8 se necessário,
cria a pasta `.venv` e instala exatamente as dependências travadas no
`uv.lock`:

```powershell
uv sync --frozen
```

Use `--frozen` para garantir que o ambiente fique idêntico ao usado em aula,
sem recalcular versões novas de bibliotecas.

### Se já existir uma pasta `cdedpp` (clone anterior)

O `git clone` falha se a pasta já existir e não estiver vazia. Apague a pasta
antiga antes de clonar de novo:

```powershell
Remove-Item -Recurse -Force cdedpp
git clone https://github.com/rafaelcostaf4-afk/cdedpp.git
cd cdedpp
uv sync --frozen
```

### Se já existir uma `.venv` dentro da pasta

`uv sync` é idempotente: se a `.venv` já estiver correta, ele não faz nada; se
estiver desatualizada, ele mesmo corrige. Em caso de dúvida ou de um ambiente
bagunçado por instalações manuais anteriores, force a recriação do zero:

```powershell
Remove-Item -Recurse -Force .venv
uv sync --frozen
```

### Se houver outro ambiente Python ativo no terminal (Conda, venv de outra aula, etc.)

Não é necessário desativá-lo. Sempre use os comandos com o prefixo `uv run`
(por exemplo, `uv run jupyter lab`): eles ignoram qualquer ambiente ativado
externamente e usam sempre o Python da `.venv` do projeto. Evite rodar
`python` ou `jupyter` "soltos" sem `uv run`, pois aí sim o ambiente ativo
errado seria usado.

### Se já existir uma venv com outro nome (`venv/`, `env/`, etc.)

O `uv` só reconhece e gerencia a pasta `.venv`. Uma venv com nome diferente é
totalmente ignorada por `uv sync`/`uv run` — não há risco de sobrescrita ou
conflito de arquivos. Ainda assim, dois cuidados evitam confusão em sala:

- Se essa venv antiga estiver **ativada** no terminal (prompt mostrando
  `(venv)` ou similar), o `uv` pode exibir um aviso sobre `VIRTUAL_ENV`
  divergente, mas continua usando a `.venv` do projeto normalmente. Se quiser
  eliminar o aviso, apenas desative antes:
  ```powershell
  deactivate
  ```
- No VS Code, o seletor de kernel lista **todos** os ambientes encontrados na
  pasta, inclusive venvs antigas. Confirme que o kernel escolhido é o que
  aparece como `Python 3.12.8 ('.venv')`, e não `venv` ou `env`.

## 2.1 Atualizar um clone antigo (sem perder o que você já criou)

Se você já clonou o repositório antes e quer apenas receber a versão nova do
ambiente, **não clone de novo**. Atualize no lugar:

```powershell
cd cdedpp
git status
```

O `git status` separa duas coisas:

- **`modified`** — arquivos do repositório que você alterou (tipicamente
  `Disciplina_CDEDPP.ipynb`, se você executou e salvou o notebook em aula);
- **`untracked`** — seus próprios arquivos e pastas. **O Git nunca os toca**:
  seus notebooks, dados e resultados continuam exatamente onde estão.

Se houver algum `modified`, guarde primeiro uma cópia pessoal dele — o `git
pull` se recusa a sobrescrever alterações locais e aborta sem fazer nada:

```powershell
# 1. Preserve sua versão com outro nome (repita para cada arquivo modificado)
Copy-Item Disciplina_CDEDPP.ipynb Disciplina_CDEDPP_meu.ipynb

# 2. Descarte as alterações nos arquivos que pertencem ao repositório
git restore .

# 3. Traga a versão nova
git pull origin main

# 4. Atualize o ambiente para as dependências novas
uv sync --frozen

# 5. Confirme que está tudo funcionando
uv run pytest
```

Detalhes esperados depois da atualização:

- O arquivo `main.py`, que existia na versão anterior, é removido: era um resto
  de template, sem uso.
- Alguns dos seus arquivos podem **desaparecer da lista do `git status`** (por
  exemplo, um `.csv` ou `.xlsx` seu). Eles continuam no disco: o `.gitignore`
  novo apenas deixou de listá-los, para que dados não sejam enviados ao
  repositório por engano.

Se o clone estiver muito bagunçado e você preferir recomeçar do zero, clone em
uma pasta nova e copie seus arquivos para dentro dela — mas, no caso comum, os
cinco passos acima bastam.

## 3. A pilha analítica instalada

As bibliotecas foram escolhidas em função do conjunto de dados do projeto
(`DadosMestrado/`): 275 processos descritos por 78 variáveis, majoritariamente
**categóricas codificadas** (inclusive de múltipla resposta, no formato
`22A; 22C`), com **10 colunas de datas** de marcos processuais e diversas
colunas de **duração** entre marcos.

### Núcleo numérico e de dados

| Biblioteca | Para quê |
| --- | --- |
| `numpy`, `pandas` | estruturas de dados e operações vetorizadas |
| `scipy` | distribuições, testes e otimização |
| `pyarrow` | leitura/escrita de Parquet e dtypes preservados |

### Entrada e saída de arquivos

| Biblioteca | Para quê |
| --- | --- |
| `openpyxl` | ler e escrever `.xlsx` (exigido por `pd.read_excel`) |
| `xlsxwriter` | gerar `.xlsx` formatados (múltiplas abas, estilos) |
| `odfpy` | ler `.ods` (LibreOffice) |
| `python-docx` | extrair as tabelas de dicionário de variáveis dos `.docx` |
| `pdfplumber` | extrair texto e tabelas de peças processuais em PDF |
| `charset-normalizer` | detectar a codificação de CSVs de origem duvidosa |

### Estatística e inferência

| Biblioteca | Para quê |
| --- | --- |
| `statsmodels` | regressão (OLS, logit, probit, Poisson, GLM), ANOVA, séries temporais (ARIMA, STL, testes de estacionariedade), análise fatorial, tabelas de contingência |
| `pingouin` | testes com **tamanho de efeito, IC e poder** no mesmo resultado; correlações parciais e correções para comparações múltiplas |
| `scikit-posthocs` | testes post-hoc não paramétricos (Dunn, Conover) com ajuste de p |
| `lifelines` | **análise de sobrevivência**: Kaplan-Meier e regressão de Cox |
| `prince` | **MCA/CA/FAMD** — o análogo da PCA para variáveis categóricas |

Duas escolhas merecem justificativa explícita:

- **`lifelines`** é o método correto para "tempo até a sentença". Processos
  ainda não julgados são observações *censuradas*; descartá-los ou tratá-los
  como concluídos enviesa qualquer média de duração. Kaplan-Meier e Cox
  incorporam a censura no cálculo.
- **`prince` (MCA)** existe porque a base é quase toda categórica. PCA sobre
  códigos numerados trataria rótulos como quantidades e produziria resultado
  sem sentido.

Para análise fatorial exploratória use `statsmodels.multivariate.factor.Factor`
(com rotação varimax/oblimin). A biblioteca `factor-analyzer` foi deliberadamente
**não incluída**: sua versão atual é incompatível com o `scikit-learn` 1.9.

### Machine learning

| Biblioteca | Para quê |
| --- | --- |
| `scikit-learn` | pipelines, validação cruzada, métricas, modelos clássicos |
| `lightgbm` | gradient boosting para dados tabulares, com suporte nativo a categóricas |
| `shap` | interpretação das contribuições de cada variável |
| `imbalanced-learn` | reamostragem para desfechos raros (ex.: condenação) |

`xgboost` foi omitido de propósito: sobrepõe-se ao `lightgbm` e arrasta
dependências CUDA de centenas de MB no `uv sync` dos alunos.

### Texto em português

| Biblioteca | Para quê |
| --- | --- |
| `spacy` + `pt_core_news_sm` | tokenização, lematização, POS e entidades nomeadas em português |
| `rapidfuzz` | pareamento aproximado (unir grafias divergentes de municípios/partes entre planilhas) |
| `unidecode` | normalizar acentuação antes de comparar textos |

O modelo `pt_core_news_sm` está **declarado no `pyproject.toml`** (via
`[tool.uv.sources]`), portanto vem junto no `uv sync` — não é preciso rodar
`python -m spacy download`. Para tarefas que exijam vetores de palavras,
troque pelo `pt_core_news_lg` (~500 MB).

### Visualização e qualidade dos dados

| Biblioteca | Para quê |
| --- | --- |
| `matplotlib`, `seaborn` | gráficos estáticos para publicação |
| `plotly` | gráficos interativos para exploração |
| `missingno` | visualizar o padrão de valores ausentes |
| `pandera` | declarar e validar o **esquema** dos dados (tipos, domínios, nulos) |

### Extra opcional: inferência bayesiana

Não é instalado por padrão porque é pesado e compila código na primeira
execução. Instale apenas se for usar:

```powershell
uv sync --extra bayes
```

Isso adiciona `pymc` e `arviz` (modelos hierárquicos, diagnóstico de cadeias e
intervalos de credibilidade).

### Ferramentas de desenvolvimento (grupo `dev`)

`jupyterlab`, `ipykernel`, `ipywidgets`, `nbconvert`, `nbstripout` (limpa saídas
antes do commit), `watermark` (registra versões dentro do notebook), `ruff`
(lint e formatação) e `pytest`.

## 3.1 Verificação do ambiente

Duas formas equivalentes de confirmar que tudo está funcionando:

```powershell
# 1. Suíte automatizada: exercita cada biblioteca de fato, não só o import
uv run pytest

# 2. Notebook narrado, com exemplo de cada família de método
uv run jupyter lab 00_Verificacao_do_Ambiente.ipynb
```

Os dois são **autossuficientes**: geram seus próprios dados de exemplo e não
dependem de nenhum arquivo externo. Funcionam imediatamente após o
`uv sync --frozen`.

Rode `uv run pytest` sempre que atualizar dependências: uma incompatibilidade
entre versões aparece ali, e não no meio de uma análise.

## 3.2 O que este repositório contém (e o que não contém)

Este repositório é a **base do ambiente de estudo**. Ele carrega apenas o que é
necessário para recriar o ambiente em qualquer computador:

```text
.python-version                    versão exata do Python
pyproject.toml                     declaração das dependências e ferramentas
uv.lock                            versões travadas de tudo
Notebook_de_Estudos.ipynb          notebook em branco, ponto de partida do aluno
00_Verificacao_do_Ambiente.ipynb   checagem completa da pilha analítica
Disciplina_CDEDPP.ipynb            notebook da aula
tests/test_ambiente.py             verificação automatizada
README.md
```

**Dados e resultados ficam fora do controle de versão.** O `.gitignore` exclui
planilhas, CSVs, PDFs, `.docx`, bases tratadas, figuras, tabelas e modelos
serializados. Isso é intencional por dois motivos:

- dados de processos judiciais não devem ir para um repositório público;
- todo arquivo em `outputs/` ou similar deve ser reproduzível a partir do
  código — se não for, o passo que o gerou precisa virar código.

Crie livremente pastas como `dados/` e `outputs/` na sua cópia local: elas já
estão ignoradas. Para versionar deliberadamente um arquivo de exemplo pequeno,
coloque-o em `exemplos/` (exceção já prevista no `.gitignore`) ou force com
`git add -f`.

## 3.3 Rigor e reprodutibilidade

Convenções adotadas no projeto:

- **Semente única e explícita.** Use `rng = np.random.default_rng(SEMENTE)` e
  passe `rng`/`random_state` a toda função estocástica. Evite
  `np.random.seed()` global.
- **Registre as versões.** `%load_ext watermark` seguido de `%watermark -d -v -iv`
  no topo de cada notebook de análise.
- **Valide antes de analisar.** Declare o esquema com `pandera` logo no
  carregamento: linhas em branco no fim da planilha, códigos digitados fora do
  domínio e colunas com tipo misto aparecem ali, e não depois de já terem
  contaminado uma contagem.
- **Relate tamanho de efeito, não só valor-p.** É o que `pingouin` devolve por
  padrão.
- **Corrija comparações múltiplas.** Numa base com dezenas de variáveis, testar
  tudo contra tudo produz falsos positivos por construção: use `p_adjust`
  (Holm/BH).
- **Notebooks entram limpos no Git.** Ative uma vez por clone:
  ```powershell
  uv run nbstripout --install
  ```
- **Antes do commit:** `uv run ruff format . && uv run ruff check . && uv run pytest`

## 3.4 Como esta configuração foi criada

```powershell
uv add numpy pandas scipy matplotlib seaborn scikit-learn
uv add openpyxl xlsxwriter odfpy pyarrow python-docx pdfplumber charset-normalizer
uv add statsmodels pingouin scikit-posthocs lifelines prince pandera missingno
uv add plotly lightgbm shap imbalanced-learn
uv add spacy rapidfuzz unidecode
uv add "pt-core-news-sm @ https://github.com/explosion/spacy-models/releases/download/pt_core_news_sm-3.8.0/pt_core_news_sm-3.8.0-py3-none-any.whl"
uv add --optional bayes pymc arviz
uv add --dev jupyterlab ipykernel ipywidgets nbconvert nbstripout watermark ruff pytest
```

Bibliotecas usadas pela análise ficam em `dependencies`. Ferramentas de
desenvolvimento ficam no grupo `dev`. O que é pesado e opcional fica em
`optional-dependencies`.

## 4. Como o kernel é ligado ao ambiente

O `ipykernel` é instalado dentro da `.venv` pelo `uv sync`. Quando o Jupyter é
iniciado com `uv run`, seu kernel `python3` usa o Python desse mesmo ambiente.
Confirme com:

```powershell
uv run jupyter kernelspec list
```

Não é necessário registrar um kernel global com `--user`. Isso evita caminhos
específicos de uma máquina e torna o projeto portátil.

## 5. Abrir o notebook

Para usar a interface do JupyterLab:

```powershell
uv run jupyter lab
```

Notebooks disponíveis:

- **`Notebook_de_Estudos.ipynb`** — em branco, para começar seu trabalho.
- **`00_Verificacao_do_Ambiente.ipynb`** — confirma que toda a pilha funciona e
  serve de referência de código para cada família de método.
- **`Disciplina_CDEDPP.ipynb`** — o notebook da aula.

Se a interface pedir uma escolha de kernel, selecione **`Python 3 (ipykernel)`**.
Esse é o kernel instalado dentro da `.venv` do projeto — desde que o JupyterLab
tenha sido iniciado com `uv run jupyter lab`, ele é sempre o correto. Kernels de
outros projetos que apareçam na lista (nomes diferentes desse) não devem ser
usados.

No VS Code, abra esta pasta, abra o `.ipynb` e use o seletor de kernel no canto
superior direito. Escolha o interpretador local do projeto, dentro da pasta
clonada:

```text
<caminho-do-projeto>\.venv\Scripts\python.exe
```

Ele normalmente aparece na lista já identificado como `Python 3.12.8 ('.venv')`
— não é necessário digitar o caminho manualmente na maioria dos casos.

Não é preciso ativar a `.venv` quando os comandos começam com `uv run`.

## 6. Verificações úteis para a aula

Confirme o executável e a versão do Python:

```powershell
uv run python -c "import sys; print(sys.executable); print(sys.version)"
```

Confirme que as bibliotecas vêm do mesmo ambiente:

```powershell
uv run python -c "import numpy, pandas, sklearn; print(numpy.__version__, pandas.__version__, sklearn.__version__)"
```

Execute o notebook inteiro sem abrir a interface gráfica:

```powershell
uv run jupyter nbconvert --to notebook --execute Disciplina_CDEDPP.ipynb --output Disciplina_CDEDPP_executado.ipynb
```

Verifique a pilha analítica inteira de uma vez:

```powershell
uv run pytest
```

## 7. Manutenção do ambiente

```powershell
# Adicionar uma biblioteca e atualizar pyproject.toml/uv.lock
uv add nome-da-biblioteca

# Remover uma biblioteca
uv remove nome-da-biblioteca

# Reinstalar/sincronizar o ambiente com a declaração do projeto
uv sync

# Exibir a árvore de dependências
uv tree
```

Evite instalar pacotes por uma célula com `!pip install`: isso pode modificar o
Python errado e não registra a dependência no projeto. Prefira `uv add` no
terminal e reinicie o kernel quando necessário.

## 8. O que entregar aos alunos / clonar em outro computador

Distribua ou versione estes arquivos (todos já estão no repositório remoto):

Tudo o que precisa ser distribuído já está no repositório (ver seção 3.2). Os
dados de pesquisa não são versionados e, quando necessários, devem ser
transferidos separadamente a quem tenha autorização para acessá-los.

Não distribua a pasta `.venv`: ela contém caminhos e binários locais e será
recriada em cada computador. Na primeira sincronização é necessário acesso à
internet para baixar Python e pacotes; depois o cache do `uv` pode ser reutilizado.

Resumo para rodar em qualquer PC (aluno ou outro professor):

```powershell
git clone https://github.com/rafaelcostaf4-afk/cdedpp.git
cd cdedpp
uv sync --frozen
uv run jupyter lab
```
