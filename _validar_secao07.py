# -*- coding: utf-8 -*-
"""
Validação da Seção 7 — confronta cada valor publicado na monografia.
Uso: uv run python _validar_secao07.py
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
print('  Validação da Seção 7 — Testes Inferenciais')
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
    ('Setup Seção 7 concluído',           'Setup da Secao 7 concluido.'),
    ('Fase III = 233 processos',          '233 processos'),
    ('χ² indício por ano ≈ 1,87',         'chi2=1.8'),
    ('χ² certeza por ano ≈ 4,36',         'chi2=4.3'),
    ('χ² por unidade ≈ 20,83',            'chi2=20.8'),
    ('Asserts Tabela 13 passaram',         'Asserts Tabela 13: OK'),
    ('OR F2_02 ≈ 45,2',                   'OR F2_02 = 45.2'),
    ('OR F2_01 ≈ 37,6',                   'OR F2_01 = 37.6'),
    ('OR F2_11 ≈ 3,83',                   'OR F2_11 = 3.8'),
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

# ── Confronto direto com valores numéricos via scipy ─────────────────────────
print('  Verificação numérica direta (scipy)')
print('=' * 60)
try:
    import pandas as pd
    import numpy as np
    from pathlib import Path
    from scipy import stats as scipy_stats
    from statsmodels.stats.proportion import proportion_confint

    pkl   = Path('dat/estcaso_lide_pred/processado/hadja_amostra_limpa.pkl')
    dados = pd.read_pickle(pkl)

    ALPHA  = 0.05
    N_AMST = 595

    # χ² por ano — indício
    tab_ind = pd.crosstab(dados['ano'], dados['Indicio']).reindex(columns=[False, True])
    chi2_ind, p_ind, gl_ind, _ = scipy_stats.chi2_contingency(tab_ind, correction=False)
    ok = abs(chi2_ind - 1.87) < 0.05 and gl_ind == 2
    if not ok:
        passou = False
    print(f'  [{"PASS" if ok else "FAIL"}] χ² indício/ano  = {chi2_ind:.3f}  (gl={gl_ind}; p={p_ind:.3f})  ref: 1,87')

    # χ² por ano — certeza
    tab_cert = pd.crosstab(dados['ano'], dados['Certeza']).reindex(columns=[False, True])
    chi2_cert, p_cert, gl_cert, _ = scipy_stats.chi2_contingency(tab_cert, correction=False)
    ok = abs(chi2_cert - 4.36) < 0.10 and gl_cert == 2
    if not ok:
        passou = False
    print(f'  [{"PASS" if ok else "FAIL"}] χ² certeza/ano  = {chi2_cert:.3f}  (gl={gl_cert}; p={p_cert:.3f})  ref: 4,36')

    # χ² por JEC
    tab_jec = pd.crosstab(dados['JEC_numero'], dados['Indicio']).reindex(columns=[False, True])
    chi2_jec, p_jec, gl_jec, _ = scipy_stats.chi2_contingency(tab_jec, correction=False)
    ok = abs(chi2_jec - 20.83) < 0.10 and gl_jec == 13
    if not ok:
        passou = False
    print(f'  [{"PASS" if ok else "FAIL"}] χ² por JEC      = {chi2_jec:.3f}  (gl={gl_jec}; p={p_jec:.3f})  ref: 20,83')

    # OR F2_02, F2_01, F2_11
    dados_f3 = dados[dados['Avancou_F3']].copy()

    def calc_or(col):
        a = int(( dados_f3[col] &  dados_f3['Indicio']).sum())
        b = int(( dados_f3[col] & ~dados_f3['Indicio']).sum())
        c = int((~dados_f3[col] &  dados_f3['Indicio']).sum())
        d = int((~dados_f3[col] & ~dados_f3['Indicio']).sum())
        if a == 0 or b == 0 or c == 0 or d == 0:
            a, b, c, d = a+0.5, b+0.5, c+0.5, d+0.5
        return (a * d) / (b * c)

    for col, ref_or, tol in [('F2_02', 45.2, 0.10), ('F2_01', 37.6, 1.0), ('F2_11', 3.83, 0.50)]:
        or_val = calc_or(col)
        ok = abs(or_val - ref_or) < tol
        if not ok:
            passou = False
        print(f'  [{"PASS" if ok else "FAIL"}] OR {col}      = {or_val:.2f}  (ref: {ref_or:.2f}; tol: ±{tol})')

except Exception as e:
    print(f'  [AVISO] Erro na verificação numérica: {e}')

print()
print('=' * 60)
if passou:
    print('  RESULTADO FINAL: SUCESSO — todos os checks passaram.')
else:
    print('  RESULTADO FINAL: FALHA — revisar iténs marcados com [FAIL].')
print('=' * 60)
sys.exit(0 if passou else 1)
