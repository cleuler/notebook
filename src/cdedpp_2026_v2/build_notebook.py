# -*- coding: utf-8 -*-
"""Monta o notebook autocontido a partir das seções didáticas.

Uso durante a implementação: python src/cdedpp_2026_v2/build_notebook.py --parcial
Uso ao concluir as nove seções: python src/cdedpp_2026_v2/build_notebook.py
"""

from __future__ import annotations

import argparse
import importlib.util
import textwrap
from pathlib import Path

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook


# Localizar a raiz a partir do próprio builder, sem depender do diretório de chamada.
RAIZ = Path(__file__).resolve().parents[2]
PASTA_MODULOS = Path(__file__).resolve().parent
SAIDA_FINAL = RAIZ / "CDEaDPP_2026_Trabalho_Final_Python_v2.ipynb"
SAIDA_PARCIAL = RAIZ / "out" / "cdedpp_2026_v2" / "protocolo_parcial.ipynb"

# Manter a ordem de apresentação e falhar se faltar qualquer seção da entrega final.
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


def construir_notebook(parcial: bool = False) -> nbformat.NotebookNode:
    """Reúne as células dos módulos e valida o arquivo antes de gravá-lo."""
    celulas: list[nbformat.NotebookNode] = []
    selecionados = MODULOS[:2] if parcial else MODULOS

    def md(conteudo: str) -> None:
        """Acrescenta Markdown; junta blocos vizinhos para preservar a alternância."""
        texto = textwrap.dedent(conteudo).strip()
        if not texto:
            raise ValueError("Há um bloco Markdown vazio.")
        if celulas and celulas[-1].cell_type == "markdown":
            celulas[-1].source += "\n\n---\n\n" + texto
        else:
            celulas.append(new_markdown_cell(texto))

    def code(conteudo: str) -> None:
        """Acrescenta código Python completo e verifica sua sintaxe."""
        fonte = textwrap.dedent(conteudo).strip()
        if not fonte:
            raise ValueError("Há uma célula de código vazia.")
        compile(fonte, "<célula do notebook>", "exec")
        celulas.append(new_code_cell(fonte))

    # Carregar cada módulo pelo caminho local e executar somente seu emissor de células.
    for nome_arquivo in selecionados:
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

    # Usar um kernelspec genérico para permitir seleção do ambiente no VS Code/Jupyter.
    notebook = new_notebook(
        cells=celulas,
        metadata={
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python"},
        },
    )
    nbformat.validate(notebook)
    if not any(celula.cell_type == "code" for celula in notebook.cells):
        raise ValueError("O notebook não contém código executável.")
    if not any("| Nome |" in celula.source for celula in notebook.cells):
        raise ValueError("Falta a tabela Markdown do dicionário de dados.")
    if any(celula.cell_type == "code" and celula.outputs for celula in notebook.cells):
        raise ValueError("O notebook gerado não deve conter outputs persistidos.")
    if any(
        atual.cell_type == seguinte.cell_type
        for atual, seguinte in zip(notebook.cells, notebook.cells[1:])
    ):
        raise ValueError("As células Markdown e código não estão alternadas.")
    return notebook


def main() -> None:
    """Processa a opção de etapa e grava um arquivo UTF-8 validado."""
    analisador = argparse.ArgumentParser(description=__doc__)
    analisador.add_argument(
        "--parcial",
        action="store_true",
        help="Monta apenas as seções 1 e 2 durante a primeira iteração.",
    )
    argumentos = analisador.parse_args()
    notebook = construir_notebook(parcial=argumentos.parcial)
    saida = SAIDA_PARCIAL if argumentos.parcial else SAIDA_FINAL
    saida.parent.mkdir(parents=True, exist_ok=True)
    nbformat.write(notebook, saida)
    print(f"Notebook validado: {saida} ({len(notebook.cells)} células)")


if __name__ == "__main__":
    main()
