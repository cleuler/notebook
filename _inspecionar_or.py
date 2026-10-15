# -*- coding: utf-8 -*-
"""
Inspeciona os OR reais de todas as variáveis F2 ativas
para calibrar os asserts da Tabela 13.
"""
import io, sys
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import pandas as pd
import numpy as np
from pathlib import Path
from scipy import stats

# ── Carregar dados ────────────────────────────────────────────────────────────
pkl   = Path('dat/estcaso_lide_pred/processado/hadja_amostra_limpa.pkl')
dados = pd.read_pickle(pkl)

ALPHA   = 0.05
N_AMST  = 595

# Recriar COLS_F2_ATIVOS (mesmo critério da Seção 6)
COLS_F2 = [f'F2_{i:02d}' for i in range(1, 18)]
ZEROS   = {'F2_07', 'F2_12', 'F2_15', 'F2_16'}
COLS_F2_ATIVOS = [c for c in COLS_F2 if c not in ZEROS]

NOMES_F2 = {
    'F2_01': 'F2_01 — Petição vaga/genérica',
    'F2_02': 'F2_02 — Ausência de documentos essenciais',
    'F2_03': 'F2_03 — Documentos sem relação com a causa',
    'F2_04': 'F2_04 — Pedido de dispensa de audiência',
    'F2_05': 'F2_05 — Foro inadequado',
    'F2_06': 'F2_06 — Documentos incompletos/ilegíveis',
    'F2_08': 'F2_08 — Demanda idêntica não declarada',
    'F2_09': 'F2_09 — Procuração incompleta',
    'F2_10': 'F2_10 — Procuração irregular (assin. digital)',
    'F2_11': 'F2_11 — Advogado fora da comarca',
    'F2_13': 'F2_13 — Classe ou assunto incorreto',
    'F2_14': 'F2_14 — Desistência após indeferi. de liminar',
    'F2_17': 'F2_17 — Contrato de honorários abusivo',
}

# ── Subconjunto Fase III ──────────────────────────────────────────────────────
dados_f3 = dados[dados['Avancou_F3']].copy()
N_F3     = len(dados_f3)
assert N_F3 == 233

def calcular_or_ic(a, b, c, d, alpha=ALPHA):
    if a == 0 or b == 0 or c == 0 or d == 0:
        a_, b_, c_, d_ = a + 0.5, b + 0.5, c + 0.5, d + 0.5
    else:
        a_, b_, c_, d_ = float(a), float(b), float(c), float(d)
    or_val = (a_ * d_) / (b_ * c_)
    log_or = np.log(or_val)
    se_log = np.sqrt(1/a_ + 1/b_ + 1/c_ + 1/d_)
    z_crit = stats.norm.ppf(1 - alpha / 2)
    ic_inf = np.exp(log_or - z_crit * se_log)
    ic_sup = np.exp(log_or + z_crit * se_log)
    return or_val, ic_inf, ic_sup

# ── Calcular ORs ──────────────────────────────────────────────────────────────
print('=' * 70)
print('  Odds Ratios — associação bivariada F2 × Indício (Fase III, n=233)')
print('=' * 70)
print(f'  {"Código":<8}  {"a":>5}  {"b":>5}  {"c":>5}  {"d":>5}  '
      f'  {"OR":>8}  {"IC 2,5%":>8}  {"IC 97,5%":>9}  {"p-valor":>10}')
print('  ' + '-' * 66)

resultados = []
for col in COLS_F2_ATIVOS:
    a = int(( dados_f3[col] &  dados_f3['Indicio']).sum())
    b = int(( dados_f3[col] & ~dados_f3['Indicio']).sum())
    c = int((~dados_f3[col] &  dados_f3['Indicio']).sum())
    d = int((~dados_f3[col] & ~dados_f3['Indicio']).sum())

    _, p_fish = stats.fisher_exact([[a, b], [c, d]], alternative='two-sided')
    or_val, ic_inf, ic_sup = calcular_or_ic(a, b, c, d)
    resultados.append((col, a, b, c, d, or_val, ic_inf, ic_sup, p_fish))

# Ordenar por OR decrescente
resultados.sort(key=lambda x: x[5], reverse=True)

for col, a, b, c, d, or_val, ic_inf, ic_sup, p_fish in resultados:
    p_fmt = 'p < 0,001' if p_fish < 0.001 else f'{p_fish:.4f}'
    print(f'  {col:<8}  {a:>5}  {b:>5}  {c:>5}  {d:>5}  '
          f'  {or_val:>8.2f}  {ic_inf:>8.2f}  {ic_sup:>9.2f}  {p_fmt:>10}')

print()
print('Legenda: a=F2=Sim&Ind=Sim | b=F2=Sim&Ind=Não | c=F2=Não&Ind=Sim | d=F2=Não&Ind=Não')
print()

# ── Valores de referência da monografia ──────────────────────────────────────
print('=' * 70)
print('  Valores publicados na monografia')
print('=' * 70)
print('  F2_02: OR ≈ 45,2 (p < 0,001)')
print('  F2_01: OR ≈ 39,8 (p < 0,001)')
print('  F2_11: OR ≈ 11,4 (p < 0,001)')
print()

# Extrair valores reais dos três
for col, ref_or, ref_p in [('F2_02', 45.2, 0.001), ('F2_01', 39.8, 0.001), ('F2_11', 11.4, 0.001)]:
    row = next(r for r in resultados if r[0] == col)
    col_, a, b, c, d, or_val, ic_inf, ic_sup, p_fish = row
    print(f'  {col}: OR obtido = {or_val:.2f}  (ref: {ref_or})  diff = {abs(or_val - ref_or):.2f}')
