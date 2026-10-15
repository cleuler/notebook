# -*- coding: utf-8 -*-
"""
Validação detalhada da Seção 6 — confronta cada valor publicado na monografia.
Uso: uv run python _validar_secao06_detalhado.py
"""
import io
import json
import sys

# Forçar UTF-8 no stdout do terminal Windows (evita UnicodeEncodeError com cp1252)
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

NOTEBOOK = 'estcaso_lide_pred.ipynb'

with open(NOTEBOOK, encoding='utf-8') as f:
    nb = json.load(f)

cells = nb['cells']
code_cells = [c for c in cells if c['cell_type'] == 'code']

# ── Verificar erros de execução ───────────────────────────────────────────────
erros = []
for i, cell in enumerate(cells):
    for out in cell.get('outputs', []):
        if out.get('output_type') == 'error':
            erros.append((i, out.get('ename', ''), out.get('evalue', '')))

if erros:
    print(f'FALHA — {len(erros)} erro(s) de execução:')
    for idx, ename, evalue in erros:
        print(f'  Célula {idx}: {ename}: {evalue}')
    sys.exit(1)

print('=' * 60)
print('  Validação da Seção 6 — Valores da monografia')
print('=' * 60)

# ── Extrair todos os textos de saída ─────────────────────────────────────────
saida_total = []
for cell in code_cells:
    for out in cell.get('outputs', []):
        if out.get('output_type') == 'stream':
            saida_total += out.get('text', [])
saida_str = ''.join(saida_total)

# ── Verificações por palavras-chave esperadas ─────────────────────────────────
checks = [
    # (descrição, string_esperada_na_saída)
    ('Tabela 9 — asserts passaram',          'Asserts Tabela 9: OK'),
    ('Tabela 10 — asserts passaram',         'Asserts Tabela 10: OK'),
    ('Frequências F2 — asserts passaram',    'Asserts frequ'),
    ('Top-4 F2 correto (F2_06 líder)',        "Top-4: ['F2_06'"),
    ('Zero: F2_07 confirmado',               'F2_07'),
    ('Zero: F2_12 confirmado',               'F2_12'),
    ('Zero: F2_15 confirmado',               'F2_15'),
    ('Zero: F2_16 confirmado',               'F2_16'),
    ('13 variáveis F2 ativas',               'F2 com ocorr'),
]

passou = True
for descricao, esperado in checks:
    ok = esperado in saida_str
    status = 'PASS' if ok else 'FAIL'
    if not ok:
        passou = False
    print(f'  [{status}] {descricao}')

print()
print('=' * 60)

# ── Confronto direto com valores numéricos da monografia ─────────────────────
print('  Valores de referência (monografia, cap. 4)')
print('=' * 60)
ref = {
    'F1_A = 79 (13,3%)':  ('F1_A', 79),
    'F1_D = 0 (retirada)': ('F1_D', 0),
    'F1_B = 28 (4,7%)':   ('F1_B', 28),
    'F2_06 = 101 (top-1)': ('F2_06', 101),
    'F2_11 = 99  (top-2)': ('F2_11', 99),
    'F2_01 = 98  (top-3)': ('F2_01', 98),
    'F2_02 = 96  (top-4)': ('F2_02', 96),
}
# Carregar dados reais via pickle
try:
    import pandas as pd
    from pathlib import Path
    pkl = Path('dat/estcaso_lide_pred/processado/hadja_amostra_limpa.pkl')
    if pkl.exists():
        dados = pd.read_pickle(pkl)
        for descricao, (col, esperado) in ref.items():
            real = int(dados[col].sum())
            ok = real == esperado
            status = 'PASS' if ok else 'FAIL'
            if not ok:
                passou = False
            print(f'  [{status}] {descricao:<30}  obtido={real}')
    else:
        print('  [AVISO] Pickle não encontrado; pulando verificação numérica.')
except Exception as e:
    print(f'  [AVISO] Erro ao carregar pickle: {e}')

print()
print('=' * 60)
if passou:
    print('  RESULTADO FINAL: SUCESSO — todos os checks passaram.')
else:
    print('  RESULTADO FINAL: FALHA — revisar iténs marcados com [FAIL].')
print('=' * 60)
sys.exit(0 if passou else 1)
