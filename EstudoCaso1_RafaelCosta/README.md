# Estudo de Caso 1 — O Tempo de Tramitação dos Inquéritos Policiais de Homicídio em Goiás

**Autor:** Rafael Costa (rafaelcc) · **Disciplina:** Ciência de Dados e Estatística (CDEDPP)

Este pacote contém tudo o que é necessário para **ler** e **reproduzir** o estudo: o notebook já executado, os scripts que o geram, a base da amostra, a coleta completa do DataJud/CNJ e o ambiente Python travado.

## 1. Para apenas ler os resultados

Não é preciso instalar nada:

- `rafaelcc_ed1.html`: abra no navegador. Tem todos os textos, tabelas e gráficos.
- `rafaelcc_ed1.ipynb`: o mesmo conteúdo, com os resultados salvos, para o Jupyter, o VS Code ou o Google Colab.

## 2. Conteúdo do pacote

| Caminho | O que é |
|---|---|
| `rafaelcc_ed1.ipynb` / `.html` | Notebook do estudo, executado (seções 1 a 23) |
| `src/build_rafaelcc_ed1.py` | Gera o notebook. Inclui `secao09_auditoria.py`, `secao10_exercicios.py`, `secao15_etapa1.py`, `secao22_datajud.py` e `secao23_sintese.py` |
| `src/interp_*.py` | Textos de interpretação, escritos a partir dos resultados da execução |
| `src/coleta_datajud.py` | Coleta na API pública do DataJud (CNJ), retomável e fatiada por semestre |
| `dat/estcaso_ip/` | Apêndice A (quadro de variáveis) e Apêndice B (base com os 218 inquéritos) |
| `dat/datajud/` | Coleta completa do TJGO: 81 arquivos `.jsonl.gz` (um por segmento e semestre de ajuizamento), os arquivos de controle `.estado.json`, o `manifesto.json` e o log da coleta |
| `dat/ibge/` | Municípios de Goiás e população do Censo 2022 (API do IBGE) |
| `dat/processado/` | Saídas: amostra limpa (`.pkl`/`.xlsx`), população tratada (`.pkl`) e planilhas de validação das regras textuais |
| `pyproject.toml`, `uv.lock`, `.python-version` | Ambiente travado (Python 3.12.8) para o `uv` |
| `requirements.txt` | As mesmas versões, para `pip` |

**A coleta do DataJud** (manifesto em `dat/datajud/manifesto.json`) foi feita em 01/10/2026, na base do TJGO. Ela cobre todo o Estado, com os assuntos de CVLI (homicídio, feminicídio, latrocínio e lesão corporal seguida de morte) em três segmentos:

| Segmento | Classes | Processos |
|---|---|---|
| Inquéritos e APFs | 279 e 280 | 22.189 |
| Ações penais evoluídas de IP (movimento 14739) | 282 e 283 | 13.062 |
| Ações penais retificadas (movimento 14738) | 282 e 283 | 1.297 |

As contagens foram conferidas contra a API. As fatias `desde_2027` estão vazias e por isso não têm `.jsonl.gz`.

## 3. Para reproduzir

O notebook precisa ser aberto **com a pasta do pacote como diretório de trabalho**: ele localiza `dat/` a partir dela.

### Opção A — `uv` (recomendada; reproduz exatamente as versões usadas)

Instale o uv (<https://docs.astral.sh/uv/>). Depois, na pasta do pacote, execute:

```bash
uv sync --frozen
uv run python src/build_rafaelcc_ed1.py
uv run jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=3600 rafaelcc_ed1.ipynb
uv run jupyter nbconvert --to html rafaelcc_ed1.ipynb
```

Também dá para abrir o notebook interativamente com `uv run jupyter lab`.

### Opção B — `pip`

Use o Python 3.12:

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows  (Linux/macOS: source .venv/bin/activate)
pip install -r requirements.txt
python src/build_rafaelcc_ed1.py
jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=3600 rafaelcc_ed1.ipynb
```

A execução completa leva de 10 a 15 minutos. As sementes aleatórias são fixas, então os resultados se repetem. O passo `build` regera o notebook a partir de `src/` e é opcional: para só reexecutar, basta o `nbconvert`.

**Observação:** os arquivos `.pkl` de `dat/processado/` são recriados na execução. Se a sua versão do pandas não conseguir lê-los, basta reexecutar o notebook.

### Refazer a coleta do DataJud (opcional)

```bash
uv run python src/coleta_datajud.py --refazer
```

Isso leva algumas horas, porque a API pública é instável (erros 429 e falhas de shard são tratados com novas tentativas). Uma coleta nova pode ter contagens diferentes, porque a base do CNJ é atualizada continuamente.

## 4. Pontos de atenção

- **Validação das regras textuais:** a planilha `dat/processado/rafaelcc_validacao_regras_parecer.xlsx` contém um parecer preliminar, feito com assistência de IA e identificado como tal na coluna `Revisor`.
- **Data de referência da amostra:** 12/03/2026, inferida a partir dos dados. A base original não informa essa data.
- **Vínculo amostra × DataJud:** a amostra não traz o número CNJ dos processos, então a comparação com a população é feita no mesmo recorte (as seis comarcas, com ajuizamento de 2022 em diante) e não processo a processo.
