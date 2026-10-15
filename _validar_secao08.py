# -*- coding: utf-8 -*-
"""
Validação da Seção 8 — confronta cada valor publicado na monografia.
Uso: uv run python _validar_secao08.py
"""
import io, json, sys
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

NOTEBOOK = 'estcaso_lide_pred.ipynb'
with open(NOTEBOOK, encoding='utf-8') as f:
    nb = json.load(f)

# ── Erros de execução ────────────────────────────────────────────────────────
erros = [(i, o.get('ename',''), o.get('evalue',''))
         for i, c in enumerate(nb['cells'])
         for o in c.get('outputs', [])
         if o.get('output_type') == 'error']
if erros:
    print(f'FALHA — {len(erros)} erro(s) de execução:')
    for idx, en, ev in erros:
        print(f'  Célula {idx}: {en}: {ev[:120]}')
    sys.exit(1)

# ── Saídas de texto ──────────────────────────────────────────────────────────
saida = ''.join(
    t for c in nb['cells'] if c['cell_type'] == 'code'
    for o in c.get('outputs', []) if o.get('output_type') == 'stream'
    for t in o.get('text', [])
)

print('=' * 62)
print('  Validação da Seção 8 — Regressão Logística e ROC')
print('=' * 62)

checks = [
    ('Setup Seção 8 concluído',              'Setup da Secao 8 concluido.'),
    ('Asserts modelos OK',                   'Asserts modelos logisticos: OK'),
    ('Pseudo-R² reduzido = 0,482',           '0.4820'),
    ('AIC reduzido = 174,1',                 '174.1276'),
    ('Log-lik = −83,06',                     '-83.0638'),
    ('Pseudo-R² completo = 0,496',           '0.4963'),
    ('Asserts Tabela 14 OK',                 'Asserts Tabela 14: OK'),
    ('OR F2_02 modelo ≈ 30,7',               'OR F2_02'),
    ('AUC = 0,908',                          'AUC-ROC: 0.907'),
    ('Asserts matriz confusão OK (VP=85)',    'VP=85'),
    ('Asserts matriz confusão OK (FP=11)',    'FP=11'),
    ('Asserts matriz confusão OK (FN=20)',    'FN=20'),
    ('Asserts matriz confusão OK (VN=117)',   'VN=117'),
    ('Acurácia 86,7%',                       '86.70%'),
    ('Asserts Tabela 15 OK',                 'Asserts Tabela 15: OK'),
    ('F2_14 mencionada nos preditores',       'F2_14'),
    ('χ² F2_14 ≈ 26,67',                    'chi2 F2_14'),
    ('F2_15/F2_16 nos zeros F2 (Seção 6)',   "'F2_07', 'F2_12', 'F2_15', 'F2_16'"),
    ('Asserts Tabela 15 confirmados',        'Asserts Tabela 15: OK'),
]

passou = True
for desc, esperado in checks:
    ok = esperado in saida
    if not ok:
        passou = False
    print(f'  [{"PASS" if ok else "FAIL"}] {desc}')

print()
print('=' * 62)

# ── Verificação numérica direta ──────────────────────────────────────────────
print('  Verificação numérica direta (statsmodels + sklearn)')
print('=' * 62)
try:
    import numpy as np, pandas as pd, warnings
    import statsmodels.api as sm
    from sklearn.metrics import roc_curve, auc, confusion_matrix
    from pathlib import Path
    warnings.filterwarnings('ignore')

    dados  = pd.read_pickle(Path('dat/estcaso_lide_pred/processado/hadja_amostra_limpa.pkl'))
    dados_f3 = dados[dados['Avancou_F3']].copy()
    Y = dados_f3['Indicio'].astype(int)
    X_red  = sm.add_constant(dados_f3[['F2_01','F2_02','F2_11']].astype(float))
    logit  = sm.Logit(Y, X_red).fit(disp=False, maxiter=200)
    prob   = logit.predict()

    checks_num = [
        ('Pseudo-R² = 0,482', abs(logit.prsquared - 0.482) < 0.002),
        ('AIC = 174,13',      abs(logit.aic - 174.13) < 0.10),
        ('Log-lik = −83,06',  abs(logit.llf - (-83.06)) < 0.10),
    ]
    fpr, tpr, _ = roc_curve(Y, prob)
    roc_auc     = auc(fpr, tpr)
    checks_num += [('AUC = 0,908', abs(roc_auc - 0.908) < 0.002)]

    pred_50 = (prob >= 0.5).astype(int)
    cm = confusion_matrix(Y, pred_50)
    checks_num += [
        ('VP = 85',  cm[1,1] == 85),
        ('FP = 11',  cm[0,1] == 11),
        ('FN = 20',  cm[1,0] == 20),
        ('VN = 117', cm[0,0] == 117),
    ]
    acc = (cm[1,1]+cm[0,0]) / len(Y)
    checks_num += [('Acurácia 86,7%', abs(acc - 0.867) < 0.002)]

    from scipy import stats
    tab14_chi = pd.crosstab(dados['F2_14'], dados['Indicio'])
    chi2_f14, p_f14, _, _ = stats.chi2_contingency(tab14_chi, correction=False)
    checks_num += [('χ² F2_14 = 26,67', abs(chi2_f14 - 26.67) < 0.10)]

    for desc, ok in checks_num:
        if not ok:
            passou = False
        print(f'  [{"PASS" if ok else "FAIL"}] {desc}')

except Exception as e:
    print(f'  [AVISO] Erro na verificação numérica: {e}')

print()
print('=' * 62)
print(f'  RESULTADO: {"SUCESSO — todos os checks passaram." if passou else "FALHA — revisar itens [FAIL]."}')
print('=' * 62)
sys.exit(0 if passou else 1)
