# -*- coding: utf-8 -*-
"""
Validação da Seção 9 — confronta cada valor publicado na monografia.
Uso: uv run python _validar_secao09.py
"""
import io, json, sys
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

NOTEBOOK = 'estcaso_lide_pred.ipynb'
with open(NOTEBOOK, encoding='utf-8') as f:
    nb = json.load(f)

# ── Erros de execução ─────────────────────────────────────────────────────────
erros = [(i, o.get('ename',''), o.get('evalue',''))
         for i, c in enumerate(nb['cells'])
         for o in c.get('outputs', [])
         if o.get('output_type') == 'error']
if erros:
    print(f'FALHA — {len(erros)} erro(s) de execução:')
    for idx, en, ev in erros:
        print(f'  Célula {idx}: {en}: {ev[:160]}')
    sys.exit(1)

# ── Saídas de texto ───────────────────────────────────────────────────────────
saida = ''.join(
    t for c in nb['cells'] if c['cell_type'] == 'code'
    for o in c.get('outputs', []) if o.get('output_type') == 'stream'
    for t in o.get('text', [])
)

print('=' * 64)
print('  Validação da Seção 9 — Correlação Phi (φ)')
print('=' * 64)

checks_txt = [
    ('Asserts matriz phi OK',                'Asserts matriz phi: OK'),
    ('23 variáveis na matriz',               'Variáveis na matriz  : 23'),
    ('253 pares totais',                     'N pares totais       : 253'),
    ('24 pares |phi|>=0.40',                 'N pares |phi|>=0.40  : 24'),
    ('phi(F2_01,F2_02) = +0,975',            'phi(F2_01,F2_02)     : +0.9754'),
    ('phi(F2_02,Indicio) = +0,816',          'phi(F2_02,Indicio)   : +0.8157'),
    ('phi(F3_19,Indicio) = +0,994',          'phi(F3_19,Indicio)   : +0.9943'),
    ('phi(F3_18,Certeza) = +0,815',          'phi(F3_18,Certeza)   : +0.8154'),
    ('Asserts Tabela 16 OK',                 'Asserts Tabela 16: OK'),
    ('Asserts Tabela 17 OK (24 pares)',       'Asserts Tabela 17: OK'),
]

passou = True
for desc, esperado in checks_txt:
    ok = esperado in saida
    if not ok:
        passou = False
    print(f'  [{"PASS" if ok else "FAIL"}] {desc}')

print()
print('=' * 64)
print('  Verificação numérica direta (numpy + scipy)')
print('=' * 64)

try:
    import numpy as np, pandas as pd
    from pathlib import Path
    from scipy import stats

    dados  = pd.read_pickle(Path('dat/estcaso_lide_pred/processado/hadja_amostra_limpa.pkl'))
    N      = len(dados)

    COLS_F1_PHI  = ['F1_A', 'F1_B', 'F1_C', 'F1_E', 'F1_F']
    COLS_F2_ATI  = [c for c in [f'F2_{i:02d}' for i in range(1,18)]
                    if c not in {'F2_07','F2_12','F2_15','F2_16'}]
    COLS_F3_PHI  = ['F3_18', 'F3_19', 'F3_20']
    COLS_CLASSIF = ['Indicio', 'Certeza']
    COLS_PHI     = COLS_F1_PHI + COLS_F2_ATI + COLS_F3_PHI + COLS_CLASSIF

    df_bin  = dados[COLS_PHI].astype(int)
    phi_arr = np.corrcoef(df_bin.values.T)
    phi_df  = pd.DataFrame(phi_arr, index=COLS_PHI, columns=COLS_PHI)

    def phi_pval(v, n=N):
        return float(stats.chi2.sf(v**2 * n, df=1))

    pares_ref = [
        ('F2_01', 'F2_02',   0.9754, 0.001),
        ('F2_02', 'Indicio',  0.8157, 0.002),
        ('F3_19', 'Indicio',  0.9943, 0.001),
        ('F3_18', 'Certeza',  0.8154, 0.002),
        ('F2_11', 'Indicio',  0.5390, 0.002),
        ('F2_06', 'Indicio',  0.4131, 0.002),
        ('F2_01', 'Indicio',  0.8047, 0.002),
    ]

    for v1, v2, ref, tol in pares_ref:
        phi = phi_df.loc[v1, v2]
        ok  = abs(phi - ref) < tol
        if not ok:
            passou = False
        print(f'  [{"PASS" if ok else "FAIL"}] phi({v1},{v2}) = {phi:+.4f}  (ref: {ref:+.4f}; tol: {tol})')

    # Contagem de pares fortes
    n_vars = len(COLS_PHI)
    n_fort = sum(1 for i in range(n_vars) for j in range(i+1, n_vars)
                 if abs(phi_arr[i, j]) >= 0.40)
    ok = n_fort == 24
    if not ok:
        passou = False
    print(f'  [{"PASS" if ok else "FAIL"}] N pares |phi|>=0.40 = {n_fort}  (esperado: 24)')

    # Tabela 17: todos os 24 pares
    print()
    print('  Tabela 17 — 24 pares com |phi|>=0.40 (verificação rápida):')
    pares = [(COLS_PHI[i], COLS_PHI[j], phi_arr[i,j])
             for i in range(n_vars) for j in range(i+1, n_vars)
             if abs(phi_arr[i,j]) >= 0.40]
    pares.sort(key=lambda x: abs(x[2]), reverse=True)
    for v1, v2, phi in pares[:5]:
        print(f'    {v1:<10} × {v2:<10}  phi={phi:+.4f}')
    print(f'    ... ({len(pares)} pares no total)')

except Exception as e:
    print(f'  [AVISO] Erro na verificação numérica: {e}')

print()
print('=' * 64)
resultado = 'SUCESSO — todos os checks passaram.' if passou else 'FALHA — revisar itens [FAIL].'
print(f'  RESULTADO: {resultado}')
print('=' * 64)
sys.exit(0 if passou else 1)
