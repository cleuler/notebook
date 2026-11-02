# -*- coding: utf-8 -*-
"""Monta o notebook de Zircônia a partir das seções didáticas.

Uso na iteração atual:
    python src/cdedpp_2026_zirconia/build_notebook.py --ate 2

Uso ao concluir todas as seções:
    python src/cdedpp_2026_zirconia/build_notebook.py
"""

from __future__ import annotations

import argparse
import importlib.util
import textwrap
from pathlib import Path

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook


RAIZ = Path(__file__).resolve().parents[2]
PASTA_MODULOS = Path(__file__).resolve().parent
SAIDA = RAIZ / "CDEaDPP_2026_Trabalho_Final_Zirconia.ipynb"

MODULOS = (
    "secao01_protocolo.py",
    "secao02_dicionario.py",
    "secao03_simulacao.py",
    "secao04_curadoria.py",
    "secao05_exploratoria.py",
    "secao06_modelagem.py",
    "secao07_hipoteses.py",
    "secao08_amostragem.py",
    "secao09_sintese.py",
)


def construir_notebook(ate: int | None = None) -> nbformat.NotebookNode:
    """Reúne células dos módulos selecionados e valida o notebook gerado."""
    limite = len(MODULOS) if ate is None else ate
    if not 1 <= limite <= len(MODULOS):
        raise ValueError(f"O argumento --ate deve estar entre 1 e {len(MODULOS)}.")

    celulas: list[nbformat.NotebookNode] = []

    def md(conteudo: str) -> None:
        """Acrescenta Markdown; funde blocos vizinhos para preservar alternância."""
        texto = textwrap.dedent(conteudo).strip()
        if not texto:
            raise ValueError("Bloco Markdown vazio.")
        if celulas and celulas[-1].cell_type == "markdown":
            celulas[-1].source += "\n\n---\n\n" + texto
        else:
            celulas.append(new_markdown_cell(texto))

    def code(conteudo: str) -> None:
        """Acrescenta código Python e compila a célula para antecipar erros."""
        fonte = textwrap.dedent(conteudo).strip()
        if not fonte:
            raise ValueError("Célula de código vazia.")
        compile(fonte, "<celula-zirconia>", "exec")
        celulas.append(new_code_cell(fonte))

    for nome_arquivo in MODULOS[:limite]:
        caminho = PASTA_MODULOS / nome_arquivo
        if not caminho.is_file():
            raise FileNotFoundError(f"Módulo obrigatório ausente: {caminho}")
        especificacao = importlib.util.spec_from_file_location(caminho.stem, caminho)
        if especificacao is None or especificacao.loader is None:
            raise ImportError(f"Não foi possível carregar {caminho}.")
        modulo = importlib.util.module_from_spec(especificacao)
        especificacao.loader.exec_module(modulo)
        if not hasattr(modulo, "construir"):
            raise AttributeError(f"{nome_arquivo} não define construir(md, code).")
        modulo.construir(md, code)

    notebook = new_notebook(
        cells=celulas,
        metadata={
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "name": "python",
                "pygments_lexer": "ipython3",
            },
        },
    )
    nbformat.validate(notebook)

    if any(celula.cell_type == "code" and celula.outputs for celula in notebook.cells):
        raise ValueError("O notebook gerado não deve conter outputs persistidos.")
    if not any("Dicionário de Dados" in celula.source for celula in notebook.cells):
        raise ValueError("Falta a seção de dicionário de dados.")
    if not any(celula.cell_type == "code" for celula in notebook.cells):
        raise ValueError("O notebook não contém código executável.")
    if any(
        atual.cell_type == seguinte.cell_type
        for atual, seguinte in zip(notebook.cells, notebook.cells[1:])
    ):
        raise ValueError("As células devem alternar entre Markdown e código.")

    return notebook


def main() -> None:
    """Lê argumentos, cria a pasta de saída e grava o notebook em UTF-8."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--ate",
        type=int,
        default=None,
        help="Gera apenas as primeiras N seções durante a construção iterativa.",
    )
    args = parser.parse_args()

    notebook = construir_notebook(ate=args.ate)
    nbformat.write(notebook, SAIDA)
    print(f"Notebook validado: {SAIDA} ({len(notebook.cells)} células)")


if __name__ == "__main__":
    main()
