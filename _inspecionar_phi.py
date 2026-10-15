# -*- coding: utf-8 -*-
"""
Inspeciona todos os valores reais da matriz de correlação phi (φ)
para calibrar os asserts da Seção 9.
Uso: uv run python _inspecionar_phi.py
"""
import io, sys
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import numpy as np
import pandas as pd
from pathlib import Path
from scipy import stats as scipy_stats

# ── Carregar dados ────────────────────────────────────────────────────────────
dados = pd.read_pickle(
    Path('dat/estcaso_lide_pred/processado/hadja_amostra_limpa.pkl')
)

# ── Definir conjunto de variáveis da matriz (plano: 23 variáveis + 2 classif.)
# Excluir F1_D (retirada), F2_07, F2_12, F2_15, F2_16 (zero ocorrências)
COLS_F1  = ['F1_A', 'F1_B', 'F1_C', 'F1_E', 'F1_F']           # 5 (sem F1_D)
COLS_F2_ATIVOS = [
    'F2_01','F2_02','F2_03','F2_04','F2_05','F2_06',
    'F2_08','F2_09','F2_10','F2_11','F2_13','F2_14','F2_17'
]                                                                # 13
COLS_F3  = ['F3_18', 'F3_19', 'F3_20']                          # 3
COLS_CLASSIF = ['Indicio', 'Certeza']                            # 2
TODAS = COLS_F1 + COLS_F2_ATIVOS + COLS_F3 + COLS_CLASSIF       # 23

print(f'Total de variáveis na matriz: {len(TODAS)}')
print(f'  F1: {len(COLS_F1)} | F2 ativas: {len(COLS_F2_ATIVOS)} | F3: {len(COLS_F3)} | Classif: {len(COLS_CLASSIF)}')
print()

# ── Construir matriz phi = Pearson entre binárias 0/1 ─────────────────────────
df_bin = dados[TODAS].astype(int)

# Verificar variáveis constantes (soma=0 ou soma=n → desvio-padrão = 0)
constantes = [c for c in TODAS if df_bin[c].std() == 0]
if constantes:
    print(f'AVISO: variáveis constantes (excluir do cálculo): {constantes}')
else:
    print('Nenhuma variável constante — OK para calcular phi completa.')
print()

# Phi = np.corrcoef sobre a matriz 0/1
phi_mat  = np.corrcoef(df_bin.values.T)
phi_df   = pd.DataFrame(phi_mat, index=TODAS, columns=TODAS)

# ── Calcular p-valores (chi2 = phi^2 * n, gl=1) ───────────────────────────────
N = len(dados)

def phi_pvalor(phi_val, n):
    chi2 = phi_val**2 * n
    return scipy_stats.chi2.sf(chi2, df=1)

# ── Pares mais importantes segundo o plano ────────────────────────────────────
print('=' * 70)
print('  Pares de referência — plano menciona φ(F2_01,F2_02)≈0,98')
print('=' * 70)
pares_ref = [
    ('F2_01', 'F2_02'),
    ('F2_02', 'F2_11'),
    ('F2_01', 'F2_06'),
    ('F2_02', 'Indicio'),
    ('F2_01', 'Indicio'),
    ('F2_11', 'Indicio'),
    ('F3_19', 'Indicio'),
    ('F3_20', 'Indicio'),
    ('F3_18', 'Certeza'),
    ('F3_19', 'Certeza'),
]
for v1, v2 in pares_ref:
    phi = phi_df.loc[v1, v2]
    p   = phi_pvalor(phi, N)
    print(f'  phi({v1},{v2}) = {phi:+.4f}   p={p:.2e}')

# ── Todos os pares com |phi| >= 0.40 ─────────────────────────────────────────
print()
print('=' * 70)
print('  Todos os pares com |φ| >= 0,40  (Tab. 17)')
print('=' * 70)
variaveis = TODAS
pares_fortes = []
for i, v1 in enumerate(variaveis):
    for v2 in variaveis[i+1:]:
        phi = phi_df.loc[v1, v2]
        if abs(phi) >= 0.40:
            p = phi_pvalor(phi, N)
            pares_fortes.append((v1, v2, phi, p))
pares_fortes.sort(key=lambda x: abs(x[2]), reverse=True)
for v1, v2, phi, p in pares_fortes:
    print(f'  {v1:<10} × {v2:<10}  phi={phi:+.4f}   p={p:.2e}')

# ── Correlações com Indício e Certeza (Tab. 16) ────────────────────────────────
print()
print('=' * 70)
print('  Correlações phi com Indício (top-10 |phi|)')
print('=' * 70)
phi_ind = phi_df['Indicio'].drop('Indicio')
phi_ind_ord = phi_ind.abs().sort_values(ascending=False)
for var in phi_ind_ord.index[:15]:
    phi = phi_df.loc[var, 'Indicio']
    p   = phi_pvalor(phi, N)
    print(f'  {var:<10}  phi={phi:+.4f}   p={p:.2e}')

print()
print('=' * 70)
print('  Correlações phi com Certeza (top-10 |phi|)')
print('=' * 70)
phi_cert = phi_df['Certeza'].drop('Certeza')
phi_cert_ord = phi_cert.abs().sort_values(ascending=False)
for var in phi_cert_ord.index[:15]:
    phi = phi_df.loc[var, 'Certeza']
    p   = phi_pvalor(phi, N)
    print(f'  {var:<10}  phi={phi:+.4f}   p={p:.2e}')

# ── Sumário da diagonal ───────────────────────────────────────────────────────
print()
print('=' * 70)
print(f'  Tamanho da matriz: {len(TODAS)} × {len(TODAS)}')
print(f'  N pares (triangular sup.): {len(TODAS)*(len(TODAS)-1)//2}')
print(f'  N pares com |phi|>=0.40  : {len(pares_fortes)}')
print(f'  N pares com |phi|>=0.20  : {sum(1 for i,v1 in enumerate(variaveis) for v2 in variaveis[i+1:] if abs(phi_df.loc[v1,v2])>=0.20)}')
