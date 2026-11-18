"""Confere a entrega revisada após a execução do notebook."""
from __future__ import annotations

from pathlib import Path

import nbformat
import openpyxl

HERE = Path(__file__).resolve().parent
nb = nbformat.read(HERE / "estcaso3_revisado.ipynb", as_version=4)
nbformat.validate(nb)
errors = [(i, o.get("ename"), o.get("evalue"))
          for i, c in enumerate(nb.cells) for o in c.get("outputs", [])
          if o.get("output_type") == "error"]
assert not errors, errors[:3]
code = [c for c in nb.cells if c.cell_type == "code"]
assert code and all(c.execution_count is not None for c in code), "há células sem execução"
assert sum(c.cell_type == "markdown" for c in nb.cells) >= 65
fontes = "\n".join(c.source for c in nb.cells)
for termo in ("LCA, k-modes e k-means", "intervalo logito", "eventos concorrentes", "Simulação de todo o funil",
              "O desenho de pesquisa e o lugar de cada variável", "Quanto os desfechos novos conseguem distinguir",
              "Quadro de variáveis e dicionário", "A categoria “certeza” fora do ajuste",
              "Escolha do modelo de previsão no ajuizamento dentro do treino",
              "O DataJud acrescenta sinal ao assunto da moldura?",
              "A trajetória detalhada ou suas interações acrescentam algo?",
              "O início e a variedade dos movimentos TPU acrescentam informação?",
              "Prevalência na moldura por regressão hierárquica e pós-estratificação",
              "Bayes por processo com as verossimilhanças estimadas",
              "A prevalência quando a codificação pode errar",
              "Logística bayesiana para a quase separação",
              "Resposta final ao roteiro"):
    assert termo.casefold() in fontes.casefold(), f"seção ausente: {termo}"
assert "conferencia_desfechos_estcaso3.xlsx" not in fontes, "restou tarefa de planilha manual"

# Texto efetivamente exibido (fontes + saídas): sem marcadores vazios e sem as afirmações corrigidas na revisão final
saidas = []
for c in nb.cells:
    for o in c.get("outputs", []):
        dados = o.get("data", {})
        saidas.append(dados.get("text/markdown", "") + dados.get("text/plain", "") + o.get("text", ""))
exibido = fontes + "\n".join(saidas)
assert "{{" not in "\n".join(saidas), "marcador sem valor numa saída"
for proibido in ("discriminam pouco", "margem de equivalência", "o efeito da F2_11 dobra",
                 "não separam nenhuma das duas coisas", "r19_tost", "esses dados não carregam a informação"):
    assert proibido not in exibido, f"afirmação revista ainda presente: {proibido}"
for exigido in ("Sensibilidade D4", "Resposta final ao roteiro", "MRP", "não é comparável"):
    assert exigido in exibido, f"conteúdo da revisão final ausente: {exigido}"
assert (HERE / "figuras" / "mrp_indicio_por_jec.png").exists()
com_refs = [i for i, c in enumerate(nb.cells) if c.cell_type == "markdown" and "Referências" in c.source
            and ("## " in c.source.split("Referências")[0][-8:])]
assert com_refs == [len(nb.cells) - 1], f"referências fora da última célula: {com_refs}"
assert "AGRESTI" in nb.cells[-1].source and "VEHTARI" in nb.cells[-1].source

path = HERE / "tabelas" / "trajetorias_processuais.xlsx"
wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
expected = {"LEIA-ME", "trajetória 1", "trajetória 2", "trajetória 3", "sem documento no DataJud"}
assert set(wb.sheetnames) == expected, wb.sheetnames
total = 0
processos = set()
for name in expected - {"LEIA-ME"}:
    ws = wb[name]
    headers = [c.value for c in next(ws.iter_rows(max_row=1))]
    assert not {"PARTES ATIVAS", "ADVOGADO", "Tipo de parte"} & set(headers)
    assert not any(h and ("predatória" in h or "certeza" in h or "indício" in h) for h in headers)
    total += ws.max_row - 1
    idx = headers.index("processo")
    for row in ws.iter_rows(min_row=2, values_only=True):
        numero = row[idx]
        assert numero and numero not in processos, f"número ausente ou repetido: {numero}"
        processos.add(numero)
assert total == 50320, total
assert len(processos) == total
dic = openpyxl.load_workbook(HERE / "tabelas" / "quadro_dicionario_large_n.xlsx", read_only=True, data_only=True)
assert set(dic.sheetnames) == {"Quadro conceitual", "Dicionário operacional", "Simulação do funil"}
assert dic["Dicionário operacional"].max_row == 42
html = HERE / "estcaso3_revisado.html"
assert html.exists()
assert html.stat().st_mtime >= (HERE / "estcaso3_revisado.ipynb").stat().st_mtime, "HTML mais antigo que o notebook"
texto_html = html.read_text(encoding="utf-8")
for titulo in ("29. A trajetória detalhada", "30. O início e a variedade", "31. Prevalência na moldura",
               "34. Logística bayesiana", "35. Resposta final ao roteiro"):
    assert titulo in texto_html, f"seção ausente do HTML: {titulo}"
print(f"Entrega conferida: {len(nb.cells)} células, {len(code)} executadas; {total} processos nas quatro abas.")
