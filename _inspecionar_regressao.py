# -*- coding: utf-8 -*-
"""
Inspeciona os valores reais da regressão logística e das variáveis auxiliares
para calibrar os asserts da Seção 8.
Uso: uv run python _inspecionar_regressao.py
"""
import io, sys
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import numpy as np
import pandas as pd
import warnings
from pathlib import Path
from scipy import stats as scipy_stats
from statsmodels.stats.proportion import proportion_confint
import statsmodels.api as sm
from sklearn.metrics import roc_curve, auc, confusion_matrix, classification_report

warnings.filterwarnings('ignore')

# ── Carregar dados ────────────────────────────────────────────────────────────
pkl   = Path('dat/estcaso_lide_pred/processado/hadja_amostra_limpa.pkl')
dados = pd.read_pickle(pkl)
ALPHA = 0.05

# Subconjunto Fase III
dados_f3 = dados[dados['Avancou_F3']].copy()
N_F3 = len(dados_f3)
print(f'Fase III: {N_F3} processos | Indicio: {dados_f3["Indicio"].sum()} | Certeza: {dados_f3["Certeza"].sum()}')
print()

# ── Colunas F2 ativas ─────────────────────────────────────────────────────────
COLS_F2 = [f'F2_{i:02d}' for i in range(1, 18)]
ZEROS   = {'F2_07', 'F2_12', 'F2_15', 'F2_16'}
COLS_F2_ATIVOS = [c for c in COLS_F2 if c not in ZEROS]

# ── Frequências na Fase III por variável ativo ────────────────────────────────
print('=' * 65)
print('  Frequências F2 na Fase III (233 processos)')
print('=' * 65)
for col in COLS_F2_ATIVOS:
    n = int(dados_f3[col].sum())
    print(f'  {col}: {n:>3}  ({n/N_F3*100:.1f}%)  | indicio=sim: {int((dados_f3[col] & dados_f3["Indicio"]).sum()):>3}')

# ── Frequência das F2_14 a F2_17 por classificação ───────────────────────────
print()
print('=' * 65)
print('  F2_14 a F2_17 — distribuição por classificação')
print('=' * 65)
for col in ['F2_14', 'F2_15', 'F2_16', 'F2_17']:
    n_total  = int(dados[col].sum())
    n_ind    = int((dados[col] & dados['Indicio']).sum())
    n_cert   = int((dados[col] & dados['Certeza']).sum())
    n_nind   = int((dados[col] & ~dados['Indicio']).sum())
    print(f'  {col}: total={n_total:>3} | Indicio=Sim: {n_ind:>3} | Certeza: {n_cert:>2} | Nao-Indicio: {n_nind:>3}')

# Chi2 F2_14 × Indicio
tab_chi_f214 = pd.crosstab(dados['F2_14'], dados['Indicio'])
chi2_f214, p_f214, gl_f214, _ = scipy_stats.chi2_contingency(tab_chi_f214, correction=False)
print(f'  chi2 F2_14 x Indicio: chi2={chi2_f214:.3f}  gl={gl_f214}  p={p_f214:.6f}')
print()

# ── Modelo Logístico Reduzido (F2_01, F2_02, F2_11) ──────────────────────────
print('=' * 65)
print('  Modelo Logístico Reduzido: F2_01 + F2_02 + F2_11')
print('=' * 65)
y     = dados_f3['Indicio'].astype(int)
X_red = sm.add_constant(dados_f3[['F2_01', 'F2_02', 'F2_11']].astype(float))

logit_red = sm.Logit(y, X_red).fit(disp=False, maxiter=200)
print(logit_red.summary2())
print()
print(f'  Pseudo-R2 McFadden: {logit_red.prsquared:.4f}')
print(f'  AIC               : {logit_red.aic:.4f}')
print(f'  Log-likelihood    : {logit_red.llf:.4f}')
print(f'  Log-likelihood 0  : {logit_red.llnull:.4f}')
print()

# OR e IC 95%
print('  Odds Ratios (exp(coef)):')
for var in X_red.columns:
    coef   = logit_red.params[var]
    ci_lo  = logit_red.conf_int().loc[var, 0]
    ci_hi  = logit_red.conf_int().loc[var, 1]
    pval   = logit_red.pvalues[var]
    or_v   = np.exp(coef)
    ic_lo  = np.exp(ci_lo)
    ic_hi  = np.exp(ci_hi)
    print(f'    {var:<12}: OR={or_v:>8.3f}  IC=[{ic_lo:.3f}, {ic_hi:.3f}]  p={pval:.6f}')
print()

# ROC e AUC
prob      = logit_red.predict()
fpr, tpr, thresholds = roc_curve(y, prob)
roc_auc   = auc(fpr, tpr)
print(f'  AUC ROC: {roc_auc:.4f}')

# Matriz de confusão (corte 0.5)
pred_50 = (prob >= 0.5).astype(int)
cm      = confusion_matrix(y, pred_50)
vn, fp_v  = cm[0]
fn, vp_v  = cm[1]
acc = (vp_v + vn) / N_F3
sen = vp_v / (vp_v + fn)
esp = vn  / (vn  + fp_v)
print(f'  Matriz confusão (corte=0.5):')
print(f'    VP={vp_v}  FP={fp_v}  FN={fn}  VN={vn}')
print(f'    Acuracia     : {acc*100:.2f}%')
print(f'    Sensibilidade: {sen*100:.2f}%')
print(f'    Especificidade:{esp*100:.2f}%')
print()

# ── Modelo Completo (todas as F2 ativas com ≥10 na Fase III) ─────────────────
cols_10 = [c for c in COLS_F2_ATIVOS if dados_f3[c].sum() >= 10]
print('=' * 65)
print(f'  Variáveis F2 com >= 10 ocorrências na Fase III: {cols_10}')
print('=' * 65)
X_full = sm.add_constant(dados_f3[cols_10].astype(float))
try:
    logit_full = sm.Logit(y, X_full).fit(disp=False, maxiter=200)
    print(f'  Pseudo-R2 McFadden (completo): {logit_full.prsquared:.4f}')
    print(f'  AIC (completo)               : {logit_full.aic:.4f}')
except Exception as e:
    print(f'  ERRO no modelo completo: {e}')

# ── Melhor corte (Youden) ─────────────────────────────────────────────────────
J = tpr - fpr
ix = np.argmax(J)
melhor_corte = thresholds[ix]
print()
print(f'  Melhor corte (Youden J): {melhor_corte:.4f}')
pred_youden = (prob >= melhor_corte).astype(int)
cm_y = confusion_matrix(y, pred_youden)
vn_y, fp_y = cm_y[0]
fn_y, vp_y = cm_y[1]
print(f'    VP={vp_y}  FP={fp_y}  FN={fn_y}  VN={vn_y}')
print(f'    Acuracia     : {(vp_y+vn_y)/N_F3*100:.2f}%')
print(f'    Sensibilidade: {vp_y/(vp_y+fn_y)*100:.2f}%')
print(f'    Especificidade:{vn_y/(vn_y+fp_y)*100:.2f}%')
