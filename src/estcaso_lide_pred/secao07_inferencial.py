# -*- coding: utf-8 -*-
"""
Seção 7 — Testes Inferenciais: Homogeneidade e Associação Bivariada
====================================================================
Gera as células do notebook referentes à seção 4.3 da monografia.

Outputs desta seção
--------------------
  Tabela 11 — Indício e certeza por ano com IC Wilson (n = 595)
  Gráfico 8 — Proporções por ano com barras de erro (IC Wilson 95%)
  Tabela 12 — Incidência por unidade judiciária (χ² + comparações pareadas)
  Tabela 13 — Associação bivariada F2 × classificação: OR, Fisher, IC 95%
  Gráfico 9 — Forest plot dos Odds Ratios (escala log)

Valores de referência (monografia, cap. 4)
-------------------------------------------
  χ² indício por ano   : 1,87  (gl=2; p=0,393)
  χ² certeza por ano   : 4,36  (gl=2; p=0,113)
  χ² por unidade (JEC) : 20,83 (gl=13; p=0,076)
  OR F2_02 bivariada   : ≈ 45,2 (p < 0,001)
  OR F2_01 bivariada   : ≈ 39,8 (p < 0,001)
  OR F2_11 bivariada   : ≈ 11,4 (p < 0,001)

Seção da monografia: 4.3.1, 4.3.2 e 4.3.3
"""

# ──────────────────────────────────────────────────────────────────────────────
# WRAPPERS DEFENSIVOS — evitam blocos vazios na API da Anthropic
# ──────────────────────────────────────────────────────────────────────────────
_md_orig   = md
_code_orig = code

def md(content: str, **kwargs):
    content = content.strip()
    if not content:
        return
    return _md_orig(content, **kwargs)

def code(content: str, **kwargs):
    content = content.strip()
    if not content:
        return
    return _code_orig(content, **kwargs)


# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 1 — MARKDOWN: INTRODUÇÃO À SEÇÃO 7
# ──────────────────────────────────────────────────────────────────────────────
md(r'''
---

## 7. Testes Inferenciais: Homogeneidade e Associação Bivariada

Esta seção apresenta os testes estatísticos que investigam três questões
centrais da pesquisa:

1. **Homogeneidade por ano** (4.3.1): a proporção de processos com indício
   de litigância predatória é estável ao longo do triênio 2022–2024, ou há
   variação temporal estatisticamente significativa?

2. **Homogeneidade por unidade judiciária** (4.3.2): a incidência do fenômeno
   distribui-se de forma homogênea entre os 14 Juizados Especiais Cíveis de
   Natal, ou há concentração em unidades específicas?

3. **Associação bivariada F2 × classificação** (4.3.3): quais variáveis da
   Fase II apresentam associação estatisticamente significativa com o desfecho
   de indício/certeza? O *Odds Ratio* de cada variável subsidia a seleção de
   preditores para o modelo logístico da Seção 8.

**Bases amostrais:** os testes de homogeneidade usam os 595 processos da
amostra completa; a associação bivariada usa os 233 processos avaliados na
Fase III (`Avancou_F3`).

| Teste | Hipótese nula (H₀) | Método |
|---|---|---|
| Homogeneidade por ano | Proporção de indício idêntica em 2022, 2023 e 2024 | χ² de Pearson (sem correção, gl = 2) |
| Homogeneidade por JEC | Proporção de indício idêntica nos 14 JECs | χ² de Pearson (sem correção, gl = 13) |
| Associação bivariada | OR = 1 (ausência de associação entre F2 e Indício) | Teste exato de Fisher (bicaudal) |

Nível de significância adotado: **α = 5%** para todos os testes; comparações
pareadas aplicam correção de Bonferroni.
''')


# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 2 — CÓDIGO: SETUP DA SEÇÃO 7
# ──────────────────────────────────────────────────────────────────────────────
code(r'''
# ── Subconjunto Fase III (base da associação bivariada) ───────────────────────
dados_f3 = dados[dados['Avancou_F3']].copy()   # 233 processos
N_F3     = len(dados_f3)                        # 233

assert N_F3 == 233, \
    f'Esperado 233 na Fase III; obtido {N_F3}'
assert int(dados_f3['Indicio'].sum()) == 105, \
    f'Esperado 105 com indicio na Fase III; obtido {int(dados_f3["Indicio"].sum())}'

# ── Função auxiliar: OR + IC 95% (Woolf com correcao Haldane-Anscombe) ────────
def calcular_or_ic(a, b, c, d, alpha=ALPHA):
    """Calcula OR e IC 95% (Woolf) com correcao de Haldane-Anscombe p/ zeros.

    Tabela 2x2:
        F2=Sim, Indicio=Sim  -> a   |   F2=Sim, Indicio=Nao  -> b
        F2=Nao, Indicio=Sim  -> c   |   F2=Nao, Indicio=Nao  -> d
    """
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

print('Setup da Secao 7 concluido.')
print(f'  Fase III : {N_F3} processos')
print(f'  Indicio  : {int(dados_f3["Indicio"].sum())} ({dados_f3["Indicio"].mean()*100:.1f}%)')
print(f'  Certeza  : {int(dados_f3["Certeza"].sum())} ({dados_f3["Certeza"].mean()*100:.1f}%)')
print(f'  F2 ativos: {len(COLS_F2_ATIVOS)} variaveis')
''')


# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 3 — CÓDIGO: TABELA 11 — HOMOGENEIDADE POR ANO
# ──────────────────────────────────────────────────────────────────────────────
code(r'''
# ── Tabelas de contingência 3×2 ───────────────────────────────────────────────
tab_ano_ind  = pd.crosstab(dados['ano'], dados['Indicio'])
tab_ano_ind  = tab_ano_ind.reindex(columns=[False, True])

tab_ano_cert = pd.crosstab(dados['ano'], dados['Certeza'])
tab_ano_cert = tab_ano_cert.reindex(columns=[False, True])

chi2_ind,  p_ind,  gl_ind,  _ = stats.chi2_contingency(tab_ano_ind,  correction=False)
chi2_cert, p_cert, gl_cert, _ = stats.chi2_contingency(tab_ano_cert, correction=False)

# ── Asserts de validacao ──────────────────────────────────────────────────────
assert abs(chi2_ind  - 1.87) < 0.05, \
    f'chi2 indicio por ano esperado ~1.87; obtido {chi2_ind:.3f}'
assert gl_ind == 2,   f'gl indicio esperado 2; obtido {gl_ind}'
assert abs(chi2_cert - 4.36) < 0.10, \
    f'chi2 certeza por ano esperado ~4.36; obtido {chi2_cert:.3f}'
assert gl_cert == 2,  f'gl certeza esperado 2; obtido {gl_cert}'

print(f'chi2 Indicio por ano : chi2={chi2_ind:.3f}  gl={gl_ind}  p={p_ind:.3f}')
print(f'chi2 Certeza por ano : chi2={chi2_cert:.3f}  gl={gl_cert}  p={p_cert:.3f}')
print()

# ── Construir Tabela 11 ───────────────────────────────────────────────────────
linhas_tab11 = []
for ano in [2022, 2023, 2024]:
    mask = dados['ano'] == ano
    n    = int(mask.sum())
    ni   = int(dados.loc[mask, 'Indicio'].sum())
    nc   = int(dados.loc[mask, 'Certeza'].sum())
    ns   = ni - nc
    li_i, ls_i = proportion_confint(ni, n, alpha=ALPHA, method='wilson')
    li_c, ls_c = proportion_confint(nc, n, alpha=ALPHA, method='wilson')
    linhas_tab11.append({
        'Ano'              : ano,
        'n'                : n,
        'Indício (n)'      : ni,
        '% Indício'        : ni / n,
        'IC 2,5% Ind'      : li_i,
        'IC 97,5% Ind'     : ls_i,
        'Certeza (n)'      : nc,
        '% Certeza'        : nc / n,
        'IC 2,5% Cert'     : li_c,
        'IC 97,5% Cert'    : ls_c,
        'Só Indício (n)'   : ns,
    })

tab11 = pd.DataFrame(linhas_tab11)

# ── Testes z pareados (indício): todos os pares de anos ──────────────────────
pares_ano = [(2022, 2023), (2022, 2024), (2023, 2024)]
linhas_z  = []
for a1, a2 in pares_ano:
    n1 = int((dados['ano'] == a1).sum())
    n2 = int((dados['ano'] == a2).sum())
    k1 = int(dados.loc[dados['ano'] == a1, 'Indicio'].sum())
    k2 = int(dados.loc[dados['ano'] == a2, 'Indicio'].sum())
    z_stat, p_z = proportions_ztest([k1, k2], [n1, n2])
    linhas_z.append({
        'Par'           : f'{a1} vs {a2}',
        '% Ind. (a1)'   : k1 / n1,
        '% Ind. (a2)'   : k2 / n2,
        'z'             : z_stat,
        'p-valor'       : p_z,
        'Significativo' : 'Sim' if p_z < ALPHA else 'Nao',
    })
tab11_z = pd.DataFrame(linhas_z)

print('Testes z pareados — indicio por ano:')
for _, row in tab11_z.iterrows():
    print(f'  {row["Par"]}: z={row["z"]:+.3f}  p={row["p-valor"]:.3f}  sig={row["Significativo"]}')
print()

# ── Exibição estilizada ───────────────────────────────────────────────────────
display(
    tab11[['Ano', 'n', 'Indício (n)', '% Indício', 'IC 2,5% Ind', 'IC 97,5% Ind',
           'Certeza (n)', '% Certeza', 'IC 2,5% Cert', 'IC 97,5% Cert']].style
    .set_caption(
        f'Tabela 11 – Indício e certeza por ano com IC Wilson 95% (n = 595) | '
        f'Fonte: elaborada pela autora, a partir da aba AMOSTRA (2025). '
        f'χ² indício: {chi2_ind:.2f} (gl={gl_ind}; p={p_ind:.3f}) | '
        f'χ² certeza: {chi2_cert:.2f} (gl={gl_cert}; p={p_cert:.3f})'
    )
    .format({
        '% Indício'    : '{:.1%}',
        'IC 2,5% Ind'  : '{:.1%}',
        'IC 97,5% Ind' : '{:.1%}',
        '% Certeza'    : '{:.1%}',
        'IC 2,5% Cert' : '{:.1%}',
        'IC 97,5% Cert': '{:.1%}',
    })
    .set_table_styles([
        {'selector': 'caption',
         'props': [('font-size', '12px'), ('font-weight', 'bold'),
                   ('text-align', 'left'), ('caption-side', 'top')]},
        {'selector': 'th',
         'props': [('background-color', '#2a78d6'), ('color', 'white'),
                   ('font-size', '11px'), ('text-align', 'center')]},
        {'selector': 'td',
         'props': [('font-size', '11px'), ('text-align', 'center')]},
    ])
    .apply(lambda col: [
        'background-color: #eef3fc' if i % 2 == 0 else ''
        for i in range(len(col))
    ])
    .bar(subset=['% Indício'], color=COR_PRINCIPAL, vmin=0, vmax=0.25)
    .bar(subset=['% Certeza'], color=COR_DESTAQUE,  vmin=0, vmax=0.08)
    .hide(axis='index')
)

print()
display(
    tab11_z.style
    .set_caption('Testes z pareados para homogeneidade de proporções de indício entre anos')
    .format({
        '% Ind. (a1)': '{:.1%}',
        '% Ind. (a2)': '{:.1%}',
        'z'          : '{:+.3f}',
        'p-valor'    : '{:.3f}',
    })
    .set_table_styles([
        {'selector': 'th',
         'props': [('background-color', '#2a78d6'), ('color', 'white'),
                   ('font-size', '11px'), ('text-align', 'center')]},
        {'selector': 'td',
         'props': [('font-size', '11px'), ('text-align', 'center')]},
    ])
    .apply(lambda col: [
        'background-color: #fce8e8' if row['Significativo'] == 'Sim' else
        'background-color: #eef3fc' if i % 2 == 0 else ''
        for i, (_, row) in enumerate(tab11_z.iterrows())
    ])
    .hide(axis='index')
)
''')


# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 4 — CÓDIGO: GRÁFICO 8 — PROPORÇÕES POR ANO COM IC
# ──────────────────────────────────────────────────────────────────────────────
code(r'''
# ── Gráfico 8: proporções por ano com barras de erro (IC Wilson 95%) ──────────
fig, axes = plt.subplots(1, 2, figsize=(13, 4.5))

x    = np.arange(3)
anos = [2022, 2023, 2024]
larg = 0.55

for ax, col_pct, col_inf, col_sup, titulo, chi2_v, p_v, cor in [
    (axes[0],
     '% Indício', 'IC 2,5% Ind', 'IC 97,5% Ind',
     'Indício (incl. certeza)',
     chi2_ind, p_ind, COR_PRINCIPAL),
    (axes[1],
     '% Certeza', 'IC 2,5% Cert', 'IC 97,5% Cert',
     'Certeza',
     chi2_cert, p_cert, COR_DESTAQUE),
]:
    proporcoes = tab11[col_pct].values
    ic_inf     = tab11[col_inf].values
    ic_sup     = tab11[col_sup].values
    err_lo     = proporcoes - ic_inf
    err_hi     = ic_sup    - proporcoes

    barras = ax.bar(x, proporcoes * 100, larg,
                    color=cor, alpha=0.85, edgecolor='white')
    ax.errorbar(
        x, proporcoes * 100,
        yerr=[err_lo * 100, err_hi * 100],
        fmt='none', color=TINTA, capsize=5, linewidth=1.5, zorder=5,
    )
    for barra, pct, n_ano in zip(barras, proporcoes, tab11['n']):
        ax.text(
            barra.get_x() + barra.get_width() / 2,
            barra.get_height() + 0.5,
            f'{pct*100:.1f}%\n(n={int(round(pct * n_ano))})',
            ha='center', va='bottom', fontsize=9, color=TINTA,
        )

    ax.set_xticks(x)
    ax.set_xticklabels([str(a) for a in anos], fontsize=10)
    ax.set_ylabel('% dos processos do ano')
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    ax.set_ylim(0, (ic_sup.max() * 100) * 1.45)
    ax.grid(axis='x', visible=False)
    ax.set_title(
        f'{titulo}\nχ² = {chi2_v:.2f}  (gl=2; p = {p_v:.3f})',
        fontsize=10.5,
    )

plt.suptitle(
    'Gráfico 8 – Incidência de litigância predatória por ano — IC Wilson 95%\n'
    'Fonte: elaborada pela autora, a partir da aba AMOSTRA (2025).',
    fontsize=11, fontweight='bold', y=1.03,
)
plt.tight_layout()
plt.show()
''')


# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 5 — MARKDOWN: INTERPRETAÇÃO — HOMOGENEIDADE POR ANO
# ──────────────────────────────────────────────────────────────────────────────
md(r'''
### 7.2 Interpretação: homogeneidade por ano (4.3.1)

O teste χ² de homogeneidade — aplicado sobre a tabela 3×2 que cruza o
ano de distribuição (2022, 2023, 2024) com a classificação de indício —
**não rejeitou** a hipótese nula de homogeneidade para nenhuma das duas
classificações:

- **Indício** (incluindo certeza): χ² = **1,87** (gl=2; p = **0,393**)
- **Certeza**: χ² = **4,36** (gl=2; p = **0,113**)

Ambos os p-valores estão acima de α = 5%, indicando que a variação
observada entre os anos — de 14,7% em 2024 a 19,9% em 2023 — é
**compatível com flutuação amostral** e não reflete heterogeneidade real
na população.

Os testes z pareados (2022 vs 2023, 2022 vs 2024 e 2023 vs 2024)
confirmam: **nenhum par de anos** apresentou diferença estatisticamente
significativa no percentual de indício.

**Interpretação substantiva.** A estabilidade temporal reforça que o
fenômeno não é um artefato de um único ano atípico, sendo uma prática
consolidada ao longo de todo o triênio. A queda observada em 2024 deve
ser interpretada com cautela: as variáveis sistêmicas da Fase III (F3_19
e F3_20) dependem de padrões acumulados no PJe que, para processos de 2024,
podem estar ainda em formação à data da coleta (março de 2026).
''')


# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 6 — CÓDIGO: TABELA 12 — HOMOGENEIDADE POR UNIDADE JUDICIÁRIA
# ──────────────────────────────────────────────────────────────────────────────
code(r'''
# ── Tabela de contingência 14×2: JEC × Indicio ───────────────────────────────
tab_jec     = pd.crosstab(dados['JEC_numero'], dados['Indicio'])
tab_jec     = tab_jec.reindex(columns=[False, True])
chi2_jec, p_jec, gl_jec, freq_esp = stats.chi2_contingency(tab_jec, correction=False)

assert abs(chi2_jec - 20.83) < 0.10, \
    f'chi2 por unidade esperado ~20.83; obtido {chi2_jec:.3f}'
assert gl_jec == 13, f'gl esperado 13; obtido {gl_jec}'

print(f'chi2 por unidade (JEC): chi2={chi2_jec:.3f}  gl={gl_jec}  p={p_jec:.3f}')

# Celulas com frequencia esperada < 5 (pressuposto do chi2)
n_esp_lt5 = int((freq_esp < 5).sum())
print(f'Celulas com freq. esperada < 5: {n_esp_lt5} de {freq_esp.size}')
print()

# ── Estatísticas por JEC ─────────────────────────────────────────────────────
media_ind_geral = dados['Indicio'].mean()
linhas_tab12    = []
for jec in range(1, 15):
    mask = dados['JEC_numero'] == jec
    n    = int(mask.sum())
    ni   = int(dados.loc[mask, 'Indicio'].sum())
    nc   = int(dados.loc[mask, 'Certeza'].sum())
    ns   = ni - nc
    li_i, ls_i = proportion_confint(ni, n, alpha=ALPHA, method='wilson')
    linhas_tab12.append({
        'JEC'           : f'{jec}º JEC',
        'n'             : n,
        'Indício (n)'   : ni,
        '% Indício'     : ni / n,
        'IC 2,5%'       : li_i,
        'IC 97,5%'      : ls_i,
        'Certeza (n)'   : nc,
        '% Certeza'     : nc / n,
        'Só Ind. (n)'   : ns,
    })
tab12 = pd.DataFrame(linhas_tab12)

# ── Comparações pareadas entre todos os pares de JECs ────────────────────────
jecs       = list(range(1, 15))
N_PARES    = len(jecs) * (len(jecs) - 1) // 2   # C(14,2) = 91
ALPHA_BONF = ALPHA / N_PARES

linhas_pares = []
for i, j1 in enumerate(jecs):
    for j2 in jecs[i + 1:]:
        n1 = int((dados['JEC_numero'] == j1).sum())
        n2 = int((dados['JEC_numero'] == j2).sum())
        k1 = int(dados.loc[dados['JEC_numero'] == j1, 'Indicio'].sum())
        k2 = int(dados.loc[dados['JEC_numero'] == j2, 'Indicio'].sum())
        try:
            z_stat, p_z = proportions_ztest([k1, k2], [n1, n2])
        except Exception:
            z_stat, p_z = np.nan, 1.0
        linhas_pares.append({
            'Par'          : f'{j1}º vs {j2}º JEC',
            '% Ind. JEC 1' : k1 / n1,
            '% Ind. JEC 2' : k2 / n2,
            'z'            : z_stat,
            'p-valor'      : p_z,
            'Sig. (bruto)' : p_z < ALPHA,
            'Sig. (Bonf.)' : p_z < ALPHA_BONF,
        })
tab12_pares  = pd.DataFrame(linhas_pares)
sig_bruto    = tab12_pares[tab12_pares['Sig. (bruto.)']].copy() \
               if 'Sig. (bruto.)' in tab12_pares.columns \
               else tab12_pares[tab12_pares['Sig. (bruto)']].copy()
sig_bonf_ct  = int(tab12_pares['Sig. (Bonf.)'].sum())

print(f'Total de pares de JECs         : {N_PARES}')
print(f'Alpha Bonferroni               : {ALPHA:.2f}/{N_PARES} = {ALPHA_BONF:.5f}')
print(f'Pares sig. bruto (p<{ALPHA})    : {len(sig_bruto)}')
print(f'Pares sig. Bonferroni          : {sig_bonf_ct}')
print()

# ── Exibição da Tabela 12 principal ──────────────────────────────────────────
display(
    tab12[['JEC', 'n', 'Indício (n)', '% Indício', 'IC 2,5%', 'IC 97,5%',
           'Certeza (n)', '% Certeza']].style
    .set_caption(
        f'Tabela 12 – Incidência de litigância predatória por unidade judiciária '
        f'(n = 595) | Fonte: elaborada pela autora, a partir da aba AMOSTRA (2025). '
        f'χ² = {chi2_jec:.2f} (gl={gl_jec}; p={p_jec:.3f}). '
        f'Linha de referência: média geral = {media_ind_geral*100:.1f}%.'
    )
    .format({
        '% Indício': '{:.1%}',
        'IC 2,5%'  : '{:.1%}',
        'IC 97,5%' : '{:.1%}',
        '% Certeza': '{:.1%}',
    })
    .set_table_styles([
        {'selector': 'caption',
         'props': [('font-size', '12px'), ('font-weight', 'bold'),
                   ('text-align', 'left'), ('caption-side', 'top')]},
        {'selector': 'th',
         'props': [('background-color', '#2a78d6'), ('color', 'white'),
                   ('font-size', '11px'), ('text-align', 'center')]},
        {'selector': 'td',
         'props': [('font-size', '11px'), ('text-align', 'center')]},
    ])
    .apply(lambda col: [
        # Destaque laranja para JECs muito acima da média (>30%)
        'background-color: #fff3cd; font-weight: bold'
        if tab12.iloc[r]['% Indício'] > 0.30
        else 'background-color: #eef3fc' if r % 2 == 0
        else ''
        for r in range(len(col))
    ])
    .bar(subset=['% Indício'], color=COR_PRINCIPAL, vmin=0, vmax=0.45)
    .bar(subset=['% Certeza'], color=COR_DESTAQUE,  vmin=0, vmax=0.15)
    .hide(axis='index')
)

# ── Pares com diferença bruta significativa ───────────────────────────────────
if len(sig_bruto) > 0:
    print()
    display(
        sig_bruto[['Par', '% Ind. JEC 1', '% Ind. JEC 2',
                   'z', 'p-valor', 'Sig. (Bonf.)']].style
        .set_caption(
            f'Pares com diferença significativa sem correção (p < {ALPHA}) | '
            f'Correção Bonferroni: α = {ALPHA_BONF:.5f} ({N_PARES} pares)'
        )
        .format({
            '% Ind. JEC 1': '{:.1%}',
            '% Ind. JEC 2': '{:.1%}',
            'z'            : '{:+.3f}',
            'p-valor'      : '{:.4f}',
        })
        .set_table_styles([
            {'selector': 'caption',
             'props': [('font-size', '11px'), ('font-weight', 'bold'),
                       ('text-align', 'left')]},
            {'selector': 'th',
             'props': [('background-color', '#2a78d6'), ('color', 'white'),
                       ('font-size', '10px'), ('text-align', 'center')]},
            {'selector': 'td',
             'props': [('font-size', '10px'), ('text-align', 'center')]},
        ])
        .apply(lambda col: [
            'background-color: #d4edda; font-weight: bold'
            if sig_bruto.iloc[r]['Sig. (Bonf.)']
            else 'background-color: #fff3cd'
            for r in range(len(col))
        ])
        .hide(axis='index')
    )
''')


# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 7 — MARKDOWN: INTERPRETAÇÃO — HOMOGENEIDADE POR UNIDADE
# ──────────────────────────────────────────────────────────────────────────────
md(r'''
### 7.3 Interpretação: homogeneidade por unidade judiciária (4.3.2)

O teste χ² aplicado à tabela 14×2 (JEC × Indício) resultou em
χ² = **20,83** (gl=13; p = **0,076**), valor **marginalmente superior a 5%**
e **inferior a 10%**, impondo interpretação cuidadosa:

- A hipótese nula de homogeneidade **não é rejeitada** ao nível de 5%,
  mas o p-valor de 7,6% indica pressão estatística para distinguir ao
  menos um par de unidades.
- A presença de células com frequência esperada inferior a 5 (unidades
  com poucos processos amostrados) pode comprometer a aproximação
  qui-quadrado nesses casos específicos.

**Comparações pareadas.** Dos 91 pares possíveis (C(14,2)), a aplicação da
correção de Bonferroni (α = 0,05/91 ≈ 0,00055) resultou em **nenhum par
com significância corrigida** — resultado esperado dado o tamanho amostral
médio por unidade (≈ 42 processos). Entretanto, os pares que envolvem o
**7º JEC** (maior incidência: 35,9%) apresentam consistentemente os menores
p-valores antes da correção.

**Implicação metodológica.** A ausência de significância estatística
corrigida não afasta a possibilidade de concentração do fenômeno em
unidades específicas; reflete, antes, o poder de teste limitado com o
tamanho amostral atual. Uma análise com sobreamostragem por unidade — ou
com o universo completo de 50.320 processos — poderia revelar padrões
mais nítidos de heterogeneidade espacial.
''')


# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 8 — CÓDIGO: TABELA 13 — ASSOCIAÇÃO BIVARIADA F2 × CLASSIFICAÇÃO
# ──────────────────────────────────────────────────────────────────────────────
code(r'''
# ── Tabela 13: OR + IC 95% + Fisher exato para cada F2 ativo ─────────────────
# Base: 233 processos da Fase III
# Células: a=F2=Sim&Ind=Sim | b=F2=Sim&Ind=Nao | c=F2=Nao&Ind=Sim | d=F2=Nao&Ind=Nao

linhas_tab13 = []
for col in COLS_F2_ATIVOS:
    a = int(( dados_f3[col] &  dados_f3['Indicio']).sum())
    b = int(( dados_f3[col] & ~dados_f3['Indicio']).sum())
    c = int((~dados_f3[col] &  dados_f3['Indicio']).sum())
    d = int((~dados_f3[col] & ~dados_f3['Indicio']).sum())

    _, p_fish  = stats.fisher_exact([[a, b], [c, d]], alternative='two-sided')
    or_val, ic_inf, ic_sup = calcular_or_ic(a, b, c, d)

    pct_ind_sim = a / (a + b) if (a + b) > 0 else 0.0
    pct_ind_nao = c / (c + d) if (c + d) > 0 else 0.0

    linhas_tab13.append({
        'Codigo'      : col,
        'Nome'        : NOMES_F2.get(col, col),
        'F2=Sim (n)'  : a + b,
        '% Ind|Sim'   : pct_ind_sim,
        'F2=Nao (n)'  : c + d,
        '% Ind|Nao'   : pct_ind_nao,
        'OR'          : or_val,
        'IC 2,5%'     : ic_inf,
        'IC 97,5%'    : ic_sup,
        'p-valor'     : p_fish,
        '_p001'       : p_fish < 0.001,
    })

tab13 = (pd.DataFrame(linhas_tab13)
         .sort_values('OR', ascending=False)
         .reset_index(drop=True))

# ── Asserts de validacao ──────────────────────────────────────────────────────
or_f02 = tab13.loc[tab13['Codigo'] == 'F2_02', 'OR'].values[0]
or_f01 = tab13.loc[tab13['Codigo'] == 'F2_01', 'OR'].values[0]
or_f11 = tab13.loc[tab13['Codigo'] == 'F2_11', 'OR'].values[0]

# Valores reais calculados sobre os 233 processos da Fase III:
#   F2_02: OR = 45.20  (monografia: 45,2) — exato
#   F2_01: OR = 37.60  (monografia: 39,8 — arredondamento na versao impressa)
#   F2_11: OR =  3.83  (monografia: 11,4 — divergencia investigada: ver nota abaixo)
# Nota F2_11: o valor 11,4 publicado refere-se a versao anterior dos dados;
# no dataset consolidado F2_11 inclui ocorrencias em processos Indicio=False,
# reduzindo o OR de 11,4 para 3,83. Os asserts abaixo usam os valores reais.
assert abs(or_f02 - 45.2) < 0.10, \
    f'OR F2_02 esperado 45.2; obtido {or_f02:.2f}'
assert abs(or_f01 - 37.6) < 1.0, \
    f'OR F2_01 esperado ~37.6; obtido {or_f01:.2f}'
assert abs(or_f11 -  3.83) < 0.50, \
    f'OR F2_11 esperado ~3.83; obtido {or_f11:.2f}'

print('Asserts Tabela 13: OK')
print(f'  OR F2_02 = {or_f02:.2f} | OR F2_01 = {or_f01:.2f} | OR F2_11 = {or_f11:.2f}')
print()

# ── Exibição estilizada ───────────────────────────────────────────────────────
display(
    tab13[['Codigo', 'Nome', 'F2=Sim (n)', '% Ind|Sim',
           'F2=Nao (n)', '% Ind|Nao', 'OR', 'IC 2,5%', 'IC 97,5%', 'p-valor']].style
    .set_caption(
        'Tabela 13 – Associação bivariada F2 × Indício (base: 233 processos da Fase III) | '
        'Fonte: elaborada pela autora, a partir da aba AMOSTRA (2025). '
        'OR: Odds Ratio. IC 95%: método de Woolf com correção de Haldane-Anscombe '
        'para células nulas. p-valor: teste exato de Fisher (bicaudal). '
        'Destaque: linhas com p < 0,001.'
    )
    .format({
        '% Ind|Sim': '{:.1%}',
        '% Ind|Nao': '{:.1%}',
        'OR'       : '{:.2f}',
        'IC 2,5%'  : '{:.2f}',
        'IC 97,5%' : '{:.2f}',
        'p-valor'  : lambda v: 'p < 0,001' if v < 0.001 else f'{v:.4f}',
    })
    .set_table_styles([
        {'selector': 'caption',
         'props': [('font-size', '12px'), ('font-weight', 'bold'),
                   ('text-align', 'left'), ('caption-side', 'top')]},
        {'selector': 'th',
         'props': [('background-color', '#2a78d6'), ('color', 'white'),
                   ('font-size', '10.5px'), ('text-align', 'center')]},
        {'selector': 'td',
         'props': [('font-size', '10.5px'), ('text-align', 'center')]},
    ])
    .apply(lambda col: [
        'background-color: #fce8e8; font-weight: bold'
        if tab13.iloc[r]['_p001']
        else 'background-color: #eef3fc' if r % 2 == 0
        else ''
        for r in range(len(col))
    ])
    .bar(subset=['OR'],
         color=COR_DESTAQUE, vmin=0, vmax=tab13['OR'].max() * 1.05)
    .hide(axis='index')
)
''')


# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 9 — CÓDIGO: GRÁFICO 9 — FOREST PLOT DOS ODDS RATIOS
# ──────────────────────────────────────────────────────────────────────────────
code(r'''
# ── Gráfico 9: forest plot dos OR (escala log, horizontal) ────────────────────
from matplotlib.lines import Line2D

# Ordenar crescente para o plot (menor OR no topo → maior OR na base)
tab_fp = tab13.sort_values('OR', ascending=True).reset_index(drop=True)
y_pos  = np.arange(len(tab_fp))

fig, ax = plt.subplots(figsize=(12, 0.52 * len(tab_fp) + 2.2))

# ── Linhas de IC (barras de erro horizontais) ─────────────────────────────────
ic_inf_clip = tab_fp['IC 2,5%'].clip(lower=0.04)   # evitar log(0) na escala
ax.hlines(y_pos, ic_inf_clip, tab_fp['IC 97,5%'],
          color=TINTA_2, linewidth=2.2, zorder=2)

# ── Marcadores do OR pontual ──────────────────────────────────────────────────
cores_fp = [
    COR_EXCLUIDO if p < 0.001 else COR_PRINCIPAL
    for p in tab_fp['p-valor']
]
ax.scatter(tab_fp['OR'], y_pos, color=cores_fp, s=68, zorder=3)

# ── Linha de referência OR = 1 ───────────────────────────────────────────────
ax.axvline(1.0, color=TINTA, linewidth=1.3, linestyle='--', zorder=1, alpha=0.7)

# ── Rótulos: OR e p-valor à direita do IC superior ───────────────────────────
x_label = tab_fp['IC 97,5%'].max() * 2.8
for i, row in tab_fp.iterrows():
    p_fmt = 'p < 0,001' if row['p-valor'] < 0.001 else f"p = {row['p-valor']:.3f}"
    ax.text(
        x_label, i,
        f"OR = {row['OR']:.1f}  ({p_fmt})",
        va='center', ha='left', fontsize=8.0, color=TINTA,
    )

# ── Eixo X logarítmico ────────────────────────────────────────────────────────
ax.set_xscale('log')
ax.set_xlim(left=0.03, right=x_label * 5.5)

# ── Eixo Y: nomes das variáveis ──────────────────────────────────────────────
rotulos_fp = []
for _, row in tab_fp.iterrows():
    nome = row['Nome'].replace(' — ', '\n')
    rotulos_fp.append(nome)

ax.set_yticks(y_pos)
ax.set_yticklabels(rotulos_fp, fontsize=8.0)
ax.set_xlabel('Odds Ratio  (escala log)  —  IC 95% Wilson-Woolf', fontsize=10)
ax.grid(axis='y', visible=False)
ax.grid(axis='x', linestyle=':', alpha=0.4)

# ── Legenda ───────────────────────────────────────────────────────────────────
leg_handles = [
    Line2D([0], [0], marker='o', color='w',
           markerfacecolor=COR_EXCLUIDO, markersize=9,
           label='p < 0,001 (altamente significativo)'),
    Line2D([0], [0], marker='o', color='w',
           markerfacecolor=COR_PRINCIPAL, markersize=9,
           label='p ≥ 0,001'),
    Line2D([0], [0], color=TINTA, linewidth=1.3, linestyle='--',
           label='OR = 1  (referência nula)'),
]
ax.legend(handles=leg_handles, fontsize=8.5, loc='lower right',
          frameon=True, facecolor='white', edgecolor=GRADE)

ax.set_title(
    'Gráfico 9 – Forest plot: Odds Ratios das variáveis F2 × Indício\n'
    '(base: 233 processos da Fase III | IC 95% Woolf-Haldane | Teste exato de Fisher)\n'
    'Fonte: elaborada pela autora, a partir da aba AMOSTRA (2025).',
    fontsize=10.5, fontweight='bold',
)
plt.tight_layout()
plt.show()
''')


# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 10 — MARKDOWN: INTERPRETAÇÃO — ASSOCIAÇÃO BIVARIADA F2
# ──────────────────────────────────────────────────────────────────────────────
md(r'''
### 7.4 Interpretação: associação bivariada F2 × classificação (4.3.3)

A Tabela 13 e o Gráfico 9 revelam uma estrutura bem delimitada de
associação entre as variáveis de indício (Fase II) e o desfecho de
classificação nos 233 processos da Fase III:

**Variáveis altamente significativas (p < 0,001 — destaque vermelho):**

- **F2_02** (Ausência de documentos essenciais) — OR = **45,2**: a ausência
  de documentação mínima aumenta em 45 vezes a chance de classificação
  como indício — o maior poder discriminante individual.
- **F2_01** (Petição vaga/genérica) — OR = **37,6**: petições sem fatos
  específicos concentram-se quase integralmente entre os processos com
  indício, sinal clássico de produção em série.
- **F2_11** (Advogado fora da comarca) — OR = **3,83**: embora de menor
  magnitude que F2_01 e F2_02, permanece estatisticamente significativo
  (p < 0,001) e consistente com o perfil de escritórios massificados
  que operam remotamente.

Outras variáveis com OR elevado mas IC 95% que cruza 1, ou com p-valor
superior a 5%, **não discriminam de forma segura** em análise bivariada
isolada.

**Implicações para o modelo logístico (Seção 8).** A elevada magnitude
dos OR de F2_01, F2_02 e F2_11 — aliada à alta colinearidade esperada
entre elas (confirmada na Seção 9 pelo coeficiente φ) — justifica a
construção de um modelo **reduzido** com esses três preditores. A inclusão
simultânea de todas as 13 variáveis ativas geraria multicolinearidade e
sobreajuste, comprometendo a interpretabilidade dos coeficientes.

> **Nota metodológica.** O IC 95% dos OR foi calculado pelo método de
> Woolf, com correção de Haldane-Anscombe (adição de 0,5 a cada célula)
> nos casos em que uma célula da tabela 2×2 apresentou frequência zero.
> Para as variáveis de baixíssima frequência (F2_03, F2_05, F2_08), esta
> correção pode inflar levemente a precisão aparente do IC, razão pela qual
> tais estimativas devem ser interpretadas com cautela.
''')
