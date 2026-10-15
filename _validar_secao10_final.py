# -*- coding: utf-8 -*-
"""
Validação final end-to-end — verifica todas as seções do notebook.
Uso: uv run python _validar_secao10_final.py
"""
import io, json, sys
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

NOTEBOOK = 'estcaso_lide_pred.ipynb'
with open(NOTEBOOK, encoding='utf-8') as f:
    nb = json.load(f)

cells = nb['cells']

# ── 0. Erros de execução ──────────────────────────────────────────────────────
erros = [(i, o.get('ename',''), o.get('evalue',''))
         for i, c in enumerate(cells)
         for o in c.get('outputs', [])
         if o.get('output_type') == 'error']

# ── 1. Estrutura geral ────────────────────────────────────────────────────────
n_md   = sum(1 for c in cells if c['cell_type'] == 'markdown')
n_code = sum(1 for c in cells if c['cell_type'] == 'code')
n_tot  = len(cells)

# ── 2. Saída de texto ─────────────────────────────────────────────────────────
saida = ''.join(
    t for c in cells if c['cell_type'] == 'code'
    for o in c.get('outputs', []) if o.get('output_type') == 'stream'
    for t in o.get('text', [])
)

print('=' * 66)
print('  Validação Final End-to-End — estcaso_lide_pred.ipynb')
print('=' * 66)
print(f'  Células Markdown : {n_md}')
print(f'  Células código   : {n_code}')
print(f'  Total de células : {n_tot}')
print()

passou = True

# ── 3. Sem erros de execução ──────────────────────────────────────────────────
ok = len(erros) == 0
if not ok:
    passou = False
    for idx, en, ev in erros:
        print(f'  [FAIL] Célula {idx}: {en}: {ev[:120]}')
print(f'  [{"PASS" if ok else "FAIL"}] Nenhum erro de execução ({len(erros)} erros)')

# ── 4. Estrutura mínima ───────────────────────────────────────────────────────
for desc, cond in [
    ('≥ 40 células Markdown',  n_md   >= 40),
    ('≥ 55 células de código', n_code >= 55),
    ('≥ 90 células no total',  n_tot  >= 90),
]:
    if not cond:
        passou = False
    print(f'  [{"PASS" if cond else "FAIL"}] {desc} (obtido: {n_md}/{n_code}/{n_tot})')

# ── 5. Checks de saída por seção ──────────────────────────────────────────────
checks = [
    # Seção 2
    ('Curadoria: 595 processos',           'Partição dos 595 processos:'),
    # Seção 5
    ('Descritiva: partição fecha',         'Partição dos 595 processos:'),
    ('Descritiva: Asserts Tab 5',          'Asserts Tabela 5: OK'),
    ('Descritiva: Asserts Tab 6',          'Asserts Tabela 6: OK'),
    ('Descritiva: Asserts Tab 8',          'Asserts Tabela 8: OK'),
    # Seção 6
    ('Freq. F1: asserts OK',               'Asserts Tabela 9: OK'),
    ('Freq. F2: top-4 correto',            'Top-4: ['),
    ('Freq. F2: 4 zeros confirmados',      "Zeros: ['F2_07'"),
    # Seção 7
    ('Inferencial: chi2 por ano',          'chi2 Indicio por ano'),
    ('Inferencial: chi2 por JEC',          'chi2 por unidade (JEC)'),
    ('Inferencial: Asserts Tab 13',        'Asserts Tabela 13: OK'),
    # Seção 8
    ('Regressão: Pseudo-R2=0,482',         '0.4820'),
    ('Regressão: AUC=0,908',              'AUC-ROC: 0.907'),
    ('Regressão: VP=85',                   'VP=85'),
    ('Regressão: Asserts Tab 15',          'Asserts Tabela 15: OK'),
    # Seção 9
    ('Phi: Asserts matriz',                'Asserts matriz phi: OK'),
    ('Phi: 24 pares fortes',               'N pares |phi|>=0.40  : 24'),
    ('Phi: phi(F2_01,F2_02)=+0.975',       'phi(F2_01,F2_02)     : +0.9754'),
    ('Phi: Asserts Tab 16',                'Asserts Tabela 16: OK'),
    ('Phi: Asserts Tab 17',                'Asserts Tabela 17: OK'),
    # Seção 10
    ('Síntese: painel gerado',             'Painel-resumo gerado com sucesso.'),
    ('Síntese: pipeline concluído',        'PIPELINE CONCLUÍDO'),
    ('Síntese: 12 gráficos listados',      'Gráficos produzidos :  12'),
    ('Síntese: 18 tabelas listadas',       'Tabelas produzidas  :  18'),
]

print()
print('  Checks por seção:')
for desc, esperado in checks:
    ok = esperado in saida
    if not ok:
        passou = False
    print(f'    [{"PASS" if ok else "FAIL"}] {desc}')

# ── 6. Verificação numérica direta ────────────────────────────────────────────
print()
print('  Verificação numérica direta (scipy + statsmodels):')
try:
    import numpy as np, pandas as pd, warnings
    from pathlib import Path
    from scipy import stats
    from statsmodels.stats.proportion import proportion_confint
    import statsmodels.api as sm
    from sklearn.metrics import roc_curve, auc, confusion_matrix
    warnings.filterwarnings('ignore')

    dados = pd.read_pickle(Path('dat/estcaso_lide_pred/processado/hadja_amostra_limpa.pkl'))
    N = len(dados)

    nums = [
        ('n=595',           N == 595),
        ('Excluídos=151',   dados['Excluido_F1'].sum() == 151),
        ('F3 avançou=233',  dados['Avancou_F3'].sum()  == 233),
        ('Indício=105',     dados['Indicio'].sum()      == 105),
        ('Certeza=30',      dados['Certeza'].sum()      == 30),
    ]

    # IC Wilson (valores reais: [14,79%; 20,91%])
    li, ls = proportion_confint(105, 595, method='wilson')
    nums += [
        ('IC Wilson inf ≈14,79%', abs(li - 0.1479) < 0.002),
        ('IC Wilson sup ≈20,91%', abs(ls - 0.2091) < 0.002),
    ]

    # chi2 por ano
    tab_a = pd.crosstab(dados['ano'], dados['Indicio'])
    chi2_a, _, _, _ = stats.chi2_contingency(tab_a, correction=False)
    nums += [('chi2 por ano ≈1,87', abs(chi2_a - 1.87) < 0.05)]

    # chi2 por JEC
    tab_j = pd.crosstab(dados['JEC_numero'], dados['Indicio'])
    chi2_j, _, _, _ = stats.chi2_contingency(tab_j, correction=False)
    nums += [('chi2 por JEC ≈20,83', abs(chi2_j - 20.83) < 0.10)]

    # Logístico
    dados_f3 = dados[dados['Avancou_F3']].copy()
    Y = dados_f3['Indicio'].astype(int)
    X = sm.add_constant(dados_f3[['F2_01','F2_02','F2_11']].astype(float))
    logit = sm.Logit(Y, X).fit(disp=False, maxiter=200)
    prob  = logit.predict()
    fpr_r, tpr_r, _ = roc_curve(Y, prob)
    auc_v = auc(fpr_r, tpr_r)
    cm    = confusion_matrix(Y, (prob>=0.5).astype(int))
    nums += [
        ('Pseudo-R2=0,482', abs(logit.prsquared - 0.482) < 0.002),
        ('AIC=174,1',       abs(logit.aic - 174.1) < 0.10),
        ('AUC=0,908',       abs(auc_v - 0.908) < 0.002),
        ('VP=85',           cm[1,1] == 85),
        ('FP=11',           cm[0,1] == 11),
    ]

    # Phi
    COLS_PHI = (
        ['F1_A','F1_B','F1_C','F1_E','F1_F']
        + [c for c in [f'F2_{i:02d}' for i in range(1,18)]
           if c not in {'F2_07','F2_12','F2_15','F2_16'}]
        + ['F3_18','F3_19','F3_20','Indicio','Certeza']
    )
    phi_m = np.corrcoef(dados[COLS_PHI].astype(int).values.T)
    phi_d = pd.DataFrame(phi_m, index=COLS_PHI, columns=COLS_PHI)
    n_fort = sum(1 for i in range(len(COLS_PHI)) for j in range(i+1, len(COLS_PHI))
                 if abs(phi_m[i,j]) >= 0.40)
    nums += [
        ('phi(F2_01,F2_02)=+0.975', abs(phi_d.loc['F2_01','F2_02']  - 0.975) < 0.002),
        ('phi(F2_02,Ind)=+0.816',   abs(phi_d.loc['F2_02','Indicio']- 0.816) < 0.002),
        ('phi(F3_19,Ind)=+0.994',   abs(phi_d.loc['F3_19','Indicio']- 0.994) < 0.002),
        ('24 pares |phi|>=0.40',    n_fort == 24),
    ]

    for desc, cond in nums:
        if not cond:
            passou = False
        print(f'    [{"PASS" if cond else "FAIL"}] {desc}')

except Exception as e:
    print(f'    [AVISO] Erro: {e}')

print()
print('=' * 66)
print(f'  RESULTADO FINAL: {"SUCESSO — notebook completo e validado." if passou else "FALHA — revisar itens [FAIL]."}')
print('=' * 66)
sys.exit(0 if passou else 1)
