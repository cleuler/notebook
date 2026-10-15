# -*- coding: utf-8 -*-
"""
Script de validação da Seção 6 — executa o notebook e inspeciona saídas.
Uso: uv run python _validar_secao06.py
"""
import io
import json
import sys

# Forçar UTF-8 no stdout do terminal Windows (evita UnicodeEncodeError com cp1252)
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open('estcaso_lide_pred.ipynb', encoding='utf-8') as f:
    nb = json.load(f)

cells = nb['cells']

# ── 1. Verificar erros em todas as células ────────────────────────────────────
erros = []
for i, cell in enumerate(cells):
    for out in cell.get('outputs', []):
        if out.get('output_type') == 'error':
            erros.append((i, out.get('ename', ''), out.get('evalue', '')))

if erros:
    print(f'ERRO(S) ENCONTRADO(S): {len(erros)}')
    for idx, ename, evalue in erros:
        print(f'  Célula {idx:>3}: {ename}: {evalue}')
    sys.exit(1)
else:
    print('OK — Nenhum erro de execução no notebook.\n')

# ── 2. Localizar e imprimir saídas das células de código da Seção 6 ───────────
palavras_chave = [
    'Asserts Tabela 9',
    'Asserts Tabela 10',
    'Asserts frequencias F2',
    'Asserts frequências F2',
    'F2 com ocorrencias',
    'F2 com ocorrências',
    'Top-4',
    'Zeros',
]

print('=== SAÍDAS DAS CÉLULAS DE CÓDIGO — SEÇÃO 6 ===\n')
code_cells = [c for c in cells if c['cell_type'] == 'code']

for i, cell in enumerate(code_cells):
    src = ''.join(cell.get('source', []))
    # Identificar células da seção 6 pelas palavras-chave nos outputs
    outputs = cell.get('outputs', [])
    stdout = []
    for out in outputs:
        if out.get('output_type') == 'stream':
            stdout += out.get('text', [])
        elif out.get('output_type') == 'execute_result':
            stdout += out.get('data', {}).get('text/plain', [])

    texto_saida = ''.join(stdout)
    if any(kw in texto_saida for kw in palavras_chave):
        print(f'--- Célula de código #{i} ---')
        print(texto_saida[:600])
        print()

# ── 3. Contagem final de células ───────────────────────────────────────────────
n_md   = sum(1 for c in cells if c['cell_type'] == 'markdown')
n_code = sum(1 for c in cells if c['cell_type'] == 'code')
print(f'Total de células: {len(cells)}  (Markdown: {n_md} | Código: {n_code})')
print('Validação concluída com sucesso.')
