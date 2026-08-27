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

## 3. Como esta configuração foi criada

Estes são os comandos usados para adicionar a pilha de ciência de dados:

```powershell
uv add numpy pandas matplotlib seaborn scikit-learn
uv add --dev jupyterlab ipykernel nbconvert
```

Bibliotecas usadas pelo projeto ficam em `dependencies`. Ferramentas de
desenvolvimento, como Jupyter, ficam no grupo `dev`.

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

Abra `Disciplina_CDEDPP.ipynb` e selecione `Python 3 (ipykernel)` se a
interface pedir uma escolha.

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

```text
.python-version
pyproject.toml
uv.lock
Disciplina_CDEDPP.ipynb
```

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
