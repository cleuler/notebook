# -*- coding: utf-8 -*-
"""
Seção 9 — Análise de Correlação Phi (φ)
=========================================
Gera as células do notebook referentes à seção 4.3.4.4 da monografia.

Outputs desta seção
--------------------
  Gráfico 11 — Heatmap da matriz phi completa (23 × 23)
               triangular inferior, anotações numéricas para |φ| ≥ 0,20
  Gráfico 12 — Barras horizontais duplas: φ com Indício e φ com Certeza,
               ordenadas por |φ| com Indício (apenas variáveis não-classificação)
  Tabela 16  — Coeficientes φ de todas as variáveis com Indício e Certeza
               + p-valor do χ² associado (gl=1)
  Tabela 17  — Todos os pares com |φ| ≥ 0,40, ordenados por |φ| decrescente

Valores de referência (monografia, seção 4.3.4.4)
--------------------------------------------------
  φ(F2_01, F2_02)   = +0,975   (p < 0,001)   ← multicolinearidade extrema
  φ(F2_02, Indício) = +0,816   (p < 0,001)
  φ(F3_19, Indício) = +0,994   (p < 0,001)   ← critério de indício embutido
  φ(F3_18, Certeza) = +0,815   (p < 0,001)
  N pares com |φ| ≥ 0,40  : 24
  N variáveis na matriz    : 23

Seção da monografia: 4.3.4.4
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
# CÉLULA 1 — MARKDOWN: INTRODUÇÃO À SEÇÃO 9
# ──────────────────────────────────────────────────────────────────────────────
md(r'''
---

## 9. Análise de Correlação Phi (φ)

O **coeficiente phi (φ)** é a medida padrão de associação entre duas variáveis
binárias. Matematicamente, é idêntico ao coeficiente de correlação de Pearson
calculado sobre variáveis codificadas 0/1, e pode ser expresso em termos da
tabela 2×2 como:

$$\varphi = \frac{ad - bc}{\sqrt{(a+b)(c+d)(a+c)(b+d)}}$$

onde *a, b, c, d* são as frequências das células da tabela de contingência.
O valor varia de −1 (associação negativa perfeita) a +1 (associação positiva
perfeita), com 0 indicando ausência de associação linear.

**Objetivos desta seção:**

1. Mapear a **estrutura de interdependência** entre todas as 23 variáveis do
   estudo (5 F1 + 13 F2 ativas + 3 F3 + 2 classificações), identificando
   blocos de variáveis colineares que justificam o modelo reduzido da Seção 8.

2. Quantificar a **força de associação de cada variável preditora com os
   desfechos** (Indício e Certeza), fornecendo uma ordenação complementar
   à análise bivariada de Odds Ratios (Seção 7).

3. Identificar **pares de variáveis com correlação forte** (|φ| ≥ 0,40) que,
   se incluídas simultaneamente em modelos preditivos, introduziriam
   multicolinearidade relevante.

> **Nota metodológica:** o coeficiente φ, por ser equivalente ao Pearson,
> captura apenas **associação linear** entre as variáveis binárias. Para
> padrões de dependência não-linear (ex.: efeitos de interação),
> complementar com o V de Cramér ou análise de correspondência.
> No contexto deste estudo, em que todas as variáveis são binárias e o
> interesse é o alinhamento com o desfecho (também binário), φ é o índice
> mais natural e diretamente interpretável.
''')


# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 2 — CÓDIGO: SETUP E CÁLCULO DA MATRIZ PHI
# ──────────────────────────────────────────────────────────────────────────────
code(r'''
# ── Conjunto de variáveis da matriz ──────────────────────────────────────────
# 5 F1 (sem F1_D — retirada)
# 13 F2 ativas (sem F2_07, F2_12, F2_15, F2_16 — zero ocorrências)
# 3 F3
# 2 classificações (Indicio, Certeza)
# Total: 23 variáveis

COLS_F1_PHI  = ['F1_A', 'F1_B', 'F1_C', 'F1_E', 'F1_F']
COLS_F3_PHI  = ['F3_18', 'F3_19', 'F3_20']
COLS_CLASSIF = ['Indicio', 'Certeza']
COLS_PHI     = COLS_F1_PHI + COLS_F2_ATIVOS + COLS_F3_PHI + COLS_CLASSIF

assert len(COLS_PHI) == 23, f'Esperado 23 variáveis; obtido {len(COLS_PHI)}'

# ── Nomes legíveis para rótulos ───────────────────────────────────────────────
NOMES_PHI = {
    # F1
    'F1_A' : 'F1_A PF polo passivo',
    'F1_B' : 'F1_B Sem grande lit.',
    'F1_C' : 'F1_C Sem advogado',
    'F1_E' : 'F1_E Dist. incorreta',
    'F1_F' : 'F1_F PJ polo ativo',
    # F2
    'F2_01': 'F2_01 Petição vaga',
    'F2_02': 'F2_02 Sem docs. ess.',
    'F2_03': 'F2_03 Docs sem relação',
    'F2_04': 'F2_04 Disp. audiência',
    'F2_05': 'F2_05 Foro inadequado',
    'F2_06': 'F2_06 Docs incompl.',
    'F2_08': 'F2_08 Demanda idênt.',
    'F2_09': 'F2_09 Procur. incomp.',
    'F2_10': 'F2_10 Procur. irreg.',
    'F2_11': 'F2_11 Adv. fora com.',
    'F2_13': 'F2_13 Classe incorreta',
    'F2_14': 'F2_14 Desist. liminar',
    'F2_17': 'F2_17 Hon. abusivo',
    # F3
    'F3_18': 'F3_18 Multiplic. ações',
    'F3_19': 'F3_19 Pet. idênticas',
    'F3_20': 'F3_20 Vol. elevado',
    # Classificações
    'Indicio': 'Indício',
    'Certeza': 'Certeza',
}

# ── Matriz binária 0/1 ────────────────────────────────────────────────────────
df_bin = dados[COLS_PHI].astype(int)

# Verificar ausência de variáveis constantes
stds = df_bin.std()
vars_cte = stds[stds == 0].index.tolist()
assert len(vars_cte) == 0, f'Variáveis constantes (desvio zero): {vars_cte}'

# ── Phi = correlação de Pearson entre binárias ────────────────────────────────
phi_arr = np.corrcoef(df_bin.values.T)          # (23, 23)
phi_df  = pd.DataFrame(phi_arr,
                       index=COLS_PHI, columns=COLS_PHI)

# ── P-valores: χ² = φ² × N, gl = 1 ──────────────────────────────────────────
def phi_pval(phi_val: float, n: int = N_AMST) -> float:
    """p-valor pelo teste qui-quadrado associado a φ (gl=1)."""
    chi2 = phi_val ** 2 * n
    return float(stats.chi2.sf(chi2, df=1))

pval_arr = np.vectorize(phi_pval)(phi_arr)
pval_df  = pd.DataFrame(pval_arr,
                        index=COLS_PHI, columns=COLS_PHI)

# ── Asserts de referência ─────────────────────────────────────────────────────
assert abs(phi_df.loc['F2_01', 'F2_02']  - 0.975) < 0.002, \
    f'phi(F2_01,F2_02) esperado 0,975; obtido {phi_df.loc["F2_01","F2_02"]:.4f}'
assert abs(phi_df.loc['F2_02', 'Indicio'] - 0.816) < 0.002, \
    f'phi(F2_02,Indicio) esperado 0,816; obtido {phi_df.loc["F2_02","Indicio"]:.4f}'
assert abs(phi_df.loc['F3_19', 'Indicio'] - 0.994) < 0.002, \
    f'phi(F3_19,Indicio) esperado 0,994; obtido {phi_df.loc["F3_19","Indicio"]:.4f}'
assert abs(phi_df.loc['F3_18', 'Certeza'] - 0.815) < 0.002, \
    f'phi(F3_18,Certeza) esperado 0,815; obtido {phi_df.loc["F3_18","Certeza"]:.4f}'

# Contar pares com |phi| >= 0.40 (excluindo diagonal)
N_VARS  = len(COLS_PHI)
n_fortes = sum(
    1 for i in range(N_VARS) for j in range(i + 1, N_VARS)
    if abs(phi_arr[i, j]) >= 0.40
)
assert n_fortes == 24, f'Esperado 24 pares com |phi|>=0.40; obtido {n_fortes}'

print('Asserts matriz phi: OK')
print(f'  Variáveis na matriz  : {N_VARS}')
print(f'  N pares totais       : {N_VARS*(N_VARS-1)//2}')
print(f'  N pares |phi|>=0.40  : {n_fortes}')
print(f'  phi(F2_01,F2_02)     : {phi_df.loc["F2_01","F2_02"]:+.4f}')
print(f'  phi(F2_02,Indicio)   : {phi_df.loc["F2_02","Indicio"]:+.4f}')
print(f'  phi(F3_19,Indicio)   : {phi_df.loc["F3_19","Indicio"]:+.4f}')
print(f'  phi(F3_18,Certeza)   : {phi_df.loc["F3_18","Certeza"]:+.4f}')
''')


# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 3 — CÓDIGO: GRÁFICO 11 — HEATMAP DA MATRIZ PHI (23 × 23)
# ──────────────────────────────────────────────────────────────────────────────
code(r'''
# ── Gráfico 11: heatmap da matriz phi (triangular inferior, renderização rápida) ─
# Usa imshow diretamente para evitar o overhead de linewidths no seaborn.

rot_curtos = [NOMES_PHI[c] for c in COLS_PHI]
N_VARS     = len(COLS_PHI)

# Máscara triangular superior (inclui diagonal) → NaN fora do triângulo inferior
phi_plot = phi_arr.copy().astype(float)
for i in range(N_VARS):
    for j in range(i, N_VARS):          # i >= j → triângulo superior + diag
        phi_plot[i, j] = np.nan

# Texto de anotação: mostrar apenas |phi| >= 0.20
LIMIAR_ANOT = 0.20

fig, ax = plt.subplots(figsize=(14, 12))

im = ax.imshow(
    phi_plot,
    cmap=MAPA_DIVERGENTE,
    vmin=-1, vmax=1,
    aspect='auto',
    interpolation='nearest',
)

# Anotações numéricas (apenas |phi| >= limiar)
for i in range(N_VARS):
    for j in range(i):              # triângulo inferior estrito
        v = phi_arr[i, j]
        if abs(v) >= LIMIAR_ANOT:
            cor_txt = 'white' if abs(v) >= 0.55 else TINTA
            ax.text(j, i, f'{v:+.2f}',
                    ha='center', va='center',
                    fontsize=5.8, color=cor_txt, fontweight='bold')

# Separadores visuais dos blocos
n_f1 = len(COLS_F1_PHI)      # 5
n_f2 = len(COLS_F2_ATIVOS)   # 13
n_f3 = len(COLS_F3_PHI)      # 3
for sep in [n_f1, n_f1 + n_f2, n_f1 + n_f2 + n_f3]:
    ax.axhline(sep - 0.5, color=TINTA, linewidth=1.5, linestyle='-')
    ax.axvline(sep - 0.5, color=TINTA, linewidth=1.5, linestyle='-')

# Eixos
ax.set_xticks(range(N_VARS))
ax.set_xticklabels(rot_curtos, rotation=45, ha='right', fontsize=7.0)
ax.set_yticks(range(N_VARS))
ax.set_yticklabels(rot_curtos, fontsize=7.0)

# Colorbar
cbar = fig.colorbar(im, ax=ax, shrink=0.55, aspect=22, pad=0.01)
cbar.set_label('Coeficiente φ (phi)', fontsize=9)

# Rótulos dos blocos acima do heatmap
blocos_lab = [
    (n_f1 / 2 - 0.5,                    'F1 (Fase I)',       'center'),
    (n_f1 + n_f2 / 2 - 0.5,             'F2 ativas',         'center'),
    (n_f1 + n_f2 + n_f3 / 2 - 0.5,     'F3',                'center'),
    (n_f1 + n_f2 + n_f3 + 0.5,          'Class.',            'center'),
]
for x_pos, rotulo, ha in blocos_lab:
    ax.text(x_pos, -1.5, rotulo,
            ha=ha, va='bottom', fontsize=8.5,
            color=TINTA_2, fontweight='bold')

ax.set_title(
    'Gráfico 11 – Matriz de correlação φ entre as 23 variáveis do estudo\n'
    'Triângulo inferior | Anotações: |φ| ≥ 0,20 | '
    'Separadores: blocos F1, F2, F3 e classificações\n'
    'Fonte: elaborada pela autora, a partir da aba AMOSTRA (2025).',
    fontsize=11, fontweight='bold', pad=14,
)
plt.tight_layout()
plt.show()
''')


# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 4 — CÓDIGO: GRÁFICO 12 — BARRAS PHI COM INDÍCIO E CERTEZA
# ──────────────────────────────────────────────────────────────────────────────
code(r'''
# ── Gráfico 12: barras horizontais φ com Indício e Certeza ────────────────────
# Apenas as variáveis preditoras (F1 + F2 ativas + F3) — exclui a outra classif.

COLS_PRED = COLS_F1_PHI + COLS_F2_ATIVOS + COLS_F3_PHI   # 21 variáveis

phi_ind  = phi_df.loc[COLS_PRED, 'Indicio']
phi_cert = phi_df.loc[COLS_PRED, 'Certeza']

# Ordenar por |phi com Indício| decrescente
ordem = phi_ind.abs().sort_values(ascending=True).index   # ascending para plot invertido
phi_ind_plot  = phi_ind.loc[ordem]
phi_cert_plot = phi_cert.loc[ordem]

y       = np.arange(len(ordem))
espess  = 0.38

fig, ax = plt.subplots(figsize=(13, 0.45 * len(ordem) + 2.2))

bars_ind = ax.barh(
    y + espess / 2, phi_ind_plot,
    height=espess,
    color=[COR_PRINCIPAL if v >= 0 else COR_EXCLUIDO for v in phi_ind_plot],
    alpha=0.88, label='φ com Indício',
)
bars_cert = ax.barh(
    y - espess / 2, phi_cert_plot,
    height=espess,
    color=[COR_CERTEZA if v >= 0 else COR_INDICIO for v in phi_cert_plot],
    alpha=0.75, label='φ com Certeza',
)

# Linha de referência φ = 0
ax.axvline(0, color=TINTA, linewidth=1.0, linestyle='-', zorder=1)

# Limiares de interpretação
for lim, estilo in [(0.20, ':'), (0.40, '--')]:
    ax.axvline( lim, color=TINTA_2, linewidth=0.9, linestyle=estilo, alpha=0.55)
    ax.axvline(-lim, color=TINTA_2, linewidth=0.9, linestyle=estilo, alpha=0.55)

# Rótulos de valor nas barras com |phi| >= 0,10
for barra, v in zip(bars_ind, phi_ind_plot):
    if abs(v) >= 0.10:
        ax.text(
            v + (0.012 if v >= 0 else -0.012),
            barra.get_y() + barra.get_height() / 2,
            f'{v:+.2f}',
            va='center',
            ha='left' if v >= 0 else 'right',
            fontsize=7.5, color=TINTA,
        )

ax.set_yticks(y)
ax.set_yticklabels([NOMES_PHI.get(c, c) for c in ordem], fontsize=8.0)
ax.set_xlabel('Coeficiente φ (phi)', fontsize=10)
ax.set_xlim(-1.05, 1.30)
ax.legend(fontsize=9.5, loc='lower right')

# Anotações dos limiares
ax.text(0.20, len(ordem) - 0.5, '|φ|=0,20', fontsize=7,
        color=TINTA_2, ha='center', va='top', style='italic')
ax.text(0.40, len(ordem) - 0.5, '|φ|=0,40', fontsize=7,
        color=TINTA_2, ha='center', va='top', style='italic')

ax.set_title(
    'Gráfico 12 – Correlação φ das variáveis preditoras com Indício e Certeza\n'
    'Ordenado por |φ com Indício| crescente | Limiares: 0,20 (moderado) e 0,40 (forte)\n'
    'Fonte: elaborada pela autora, a partir da aba AMOSTRA (2025).',
    fontsize=11, fontweight='bold',
)
plt.tight_layout()
plt.show()
''')


# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 5 — CÓDIGO: TABELA 16 — φ DE CADA VARIÁVEL COM INDÍCIO E CERTEZA
# ──────────────────────────────────────────────────────────────────────────────
code(r'''
# ── Tabela 16: coeficientes φ e p-valores ─────────────────────────────────────
linhas_tab16 = []
for col in COLS_PRED:
    phi_i   = phi_df.loc[col, 'Indicio']
    phi_c   = phi_df.loc[col, 'Certeza']
    pval_i  = phi_pval(phi_i)
    pval_c  = phi_pval(phi_c)
    linhas_tab16.append({
        'Código'           : col,
        'Nome'             : NOMES_PHI.get(col, col),
        'φ (Indício)'      : phi_i,
        'p (Indício)'      : pval_i,
        'Sig. Ind.'        : pval_i < 0.05,
        'φ (Certeza)'      : phi_c,
        'p (Certeza)'      : pval_c,
        'Sig. Cert.'       : pval_c < 0.05,
        '|φ| Ind. sort'    : abs(phi_i),     # chave de ordenação, ocultada
    })

tab16 = (pd.DataFrame(linhas_tab16)
         .sort_values('|φ| Ind. sort', ascending=False)
         .reset_index(drop=True))

# Validar os pares de referência na tabela
val_f2_02_ind = tab16.loc[tab16['Código'] == 'F2_02', 'φ (Indício)'].values[0]
val_f3_19_ind = tab16.loc[tab16['Código'] == 'F3_19', 'φ (Indício)'].values[0]
assert abs(val_f2_02_ind - 0.8157) < 0.002
assert abs(val_f3_19_ind - 0.9943) < 0.002
print('Asserts Tabela 16: OK')
print()

def fmt_phi(v):
    return f'{v:+.4f}'

def fmt_p16(v):
    if v < 0.001:
        return 'p < 0,001'
    if v < 0.01:
        return f'{v:.4f}'.replace('.', ',')
    return f'{v:.3f}'.replace('.', ',')

display(
    tab16[['Código', 'Nome', 'φ (Indício)', 'p (Indício)',
           'φ (Certeza)', 'p (Certeza)']].style
    .set_caption(
        'Tabela 16 – Coeficientes phi (φ) de cada variável preditora com '
        'Indício e Certeza | '
        'Fonte: elaborada pela autora, a partir da aba AMOSTRA (2025).\n'
        'φ = correlação de Pearson entre variáveis binárias 0/1 (N = 595). '
        'p-valor: teste χ² associado (φ² × N, gl = 1). '
        'Destaque: |φ| ≥ 0,40 com Indício (vermelho) ou 0,20 ≤ |φ| < 0,40 (azul claro).'
    )
    .format({
        'φ (Indício)': fmt_phi,
        'p (Indício)': fmt_p16,
        'φ (Certeza)': fmt_phi,
        'p (Certeza)': fmt_p16,
    })
    .set_table_styles([
        {'selector': 'caption',
         'props': [('font-size', '12px'), ('font-weight', 'bold'),
                   ('text-align', 'left'), ('caption-side', 'top')]},
        {'selector': 'th',
         'props': [('background-color', '#2a78d6'), ('color', 'white'),
                   ('font-size', '11px'), ('text-align', 'center')]},
        {'selector': 'td',
         'props': [('font-size', '10.5px'), ('text-align', 'center')]},
    ])
    .apply(lambda col: [
        'background-color: #fce8e8; font-weight: bold'   # forte: |phi|>=0.40
        if abs(tab16.iloc[r]['φ (Indício)']) >= 0.40
        else 'background-color: #eef3fc'                  # moderado: |phi|>=0.20
        if abs(tab16.iloc[r]['φ (Indício)']) >= 0.20
        else 'background-color: #f9f9f9' if r % 2 == 0   # fraco: alternado
        else ''
        for r in range(len(col))
    ])
    .bar(subset=['φ (Indício)', 'φ (Certeza)'],
         align='mid', color=[COR_PRINCIPAL, COR_CERTEZA],
         vmin=-1, vmax=1)
    .hide(axis='index')
)
''')


# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 6 — CÓDIGO: TABELA 17 — PARES COM |φ| ≥ 0,40
# ──────────────────────────────────────────────────────────────────────────────
code(r'''
# ── Tabela 17: todos os pares com |φ| >= 0,40 ─────────────────────────────────
LIMIAR_T17 = 0.40
linhas_tab17 = []
for i, v1 in enumerate(COLS_PHI):
    for v2 in COLS_PHI[i + 1:]:
        phi = phi_df.loc[v1, v2]
        if abs(phi) >= LIMIAR_T17:
            pval = phi_pval(phi)
            # Bloco de cada variável
            def bloco(c):
                if c in COLS_F1_PHI:    return 'F1'
                if c in COLS_F2_ATIVOS: return 'F2'
                if c in COLS_F3_PHI:    return 'F3'
                return 'Classif.'
            linhas_tab17.append({
                'Variável 1'   : v1,
                'Bloco 1'      : bloco(v1),
                'Variável 2'   : v2,
                'Bloco 2'      : bloco(v2),
                'φ'            : phi,
                '|φ|'          : abs(phi),
                'p-valor'      : pval,
                'Interpretação': (
                    'Critério embutido'       if (v1 in COLS_F3_PHI or v2 in COLS_F3_PHI)
                                                and ('Indicio' in (v1, v2) or 'Certeza' in (v1, v2))
                    else 'Multicolinearidade' if bloco(v1) == bloco(v2) == 'F2'
                    else 'Preditor × desfecho'
                ),
            })

tab17 = (pd.DataFrame(linhas_tab17)
         .sort_values('|φ|', ascending=False)
         .reset_index(drop=True))

# Validar contagem
assert len(tab17) == 24, f'Esperado 24 pares; obtido {len(tab17)}'
print(f'Asserts Tabela 17: OK — {len(tab17)} pares com |phi|>={LIMIAR_T17}')
print()

def fmt_p17(v):
    return 'p < 0,001' if v < 0.001 else f'{v:.4f}'.replace('.', ',')

COR_INTERP = {
    'Critério embutido'   : '#fce8e8',
    'Multicolinearidade'  : '#fff3e0',
    'Preditor × desfecho' : '#eef3fc',
}

display(
    tab17[['Variável 1', 'Bloco 1', 'Variável 2', 'Bloco 2',
           'φ', 'p-valor', 'Interpretação']].style
    .set_caption(
        f'Tabela 17 – Pares de variáveis com |φ| ≥ {LIMIAR_T17} (N = 595) | '
        'Fonte: elaborada pela autora, a partir da aba AMOSTRA (2025).\n'
        'Ordenado por |φ| decrescente. φ = Pearson entre binárias 0/1. '
        'p-valor: χ² (gl=1). '
        'Critério embutido: par F3 × classificação (redundância estrutural). '
        'Multicolinearidade: dois preditores do mesmo bloco F2.'
    )
    .format({
        'φ'      : '{:+.4f}',
        'p-valor': fmt_p17,
    })
    .set_table_styles([
        {'selector': 'caption',
         'props': [('font-size', '12px'), ('font-weight', 'bold'),
                   ('text-align', 'left'), ('caption-side', 'top')]},
        {'selector': 'th',
         'props': [('background-color', '#2a78d6'), ('color', 'white'),
                   ('font-size', '11px'), ('text-align', 'center')]},
        {'selector': 'td',
         'props': [('font-size', '10.5px'), ('text-align', 'center')]},
    ])
    .apply(lambda col: [
        f'background-color: {COR_INTERP.get(tab17.iloc[r]["Interpretação"], "")}'
        for r in range(len(col))
    ])
    .bar(subset=['φ'], align='mid',
         color=[COR_PRINCIPAL, COR_EXCLUIDO], vmin=-1, vmax=1)
    .hide(axis='index')
)
''')


# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 7 — MARKDOWN: INTERPRETAÇÃO DA MATRIZ PHI
# ──────────────────────────────────────────────────────────────────────────────
md(r'''
### 9.1 Interpretação da matriz de correlação φ (4.3.4.4)

A análise da matriz phi revela **quatro padrões estruturais** relevantes
para a compreensão do fenômeno e para a validade dos modelos preditivos:

---

#### Padrão 1 — Critério embutido: variáveis F3 × classificações

As correlações mais altas da matriz são, por construção, entre as variáveis
da Fase III e as classificações derivadas delas:

| Par | φ |
|---|---|
| F3_19 × Indício | **+0,994** |
| F3_20 × Indício | **+0,941** |
| F3_18 × Certeza | **+0,815** |

Esses valores altíssimos não indicam poder preditivo independente — são
uma consequência direta da **definição operacional** das classificações
(Indício = F3_19 **∧** F3_20; Certeza = F3_18 **∧** F3_19 **∧** F3_20).
Incluir variáveis F3 como preditoras de Indício ou Certeza seria uma
tautologia e foi corretamente evitado na modelagem logística da Seção 8.

---

#### Padrão 2 — Multicolinearidade extrema: F2_01 × F2_02

φ(F2_01, F2_02) = **+0,975** — a correlação mais alta entre variáveis
de blocos diferentes de classificação/F3. Esse valor indica que, na
prática, as duas variáveis medem o mesmo fenômeno subjacente: processos
com petição vaga quase invariavelmente carecem de documentação essencial
e vice-versa.

Essa multicolinearidade extrema explica a instabilidade dos coeficientes
individuais no modelo logístico (Seção 8): F2_01, embora com OR bivariado
de 37,6, tem OR ajustado de apenas 1,7 (p = 0,665) quando controlado por
F2_02. As duas variáveis disputam o mesmo "espaço explicativo".

---

#### Padrão 3 — Correlações F2 × Indício: bloco de preditores válidos

Excluídas as variáveis F3 (critério embutido), as correlações com Indício
seguem ordem decrescente clara:

| Variável | φ com Indício | Interpretação |
|---|---|---|
| F2_02 | +0,816 | Preditor mais forte |
| F2_01 | +0,805 | Proxy de F2_02 |
| F2_11 | +0,539 | Preditor independente |
| F2_06 | +0,413 | Preditor moderado |
| F2_10 | +0,291 | Efeito fraco |
| F2_14 | +0,212 | Efeito fraco mas significativo |

Esse ordenamento confirma a seleção de variáveis do modelo reduzido
(Seção 8) e a descontinuidade entre F2_11 (φ = 0,54) e F2_06 (φ = 0,41)
— sugerindo que um modelo ainda mais parcimonioso (apenas F2_02 e F2_11)
capturaria boa parte do poder preditivo.

---

#### Padrão 4 — Bloco F2_06 × F3: co-ocorrência

φ(F2_06, F3_19) = **+0,421** e φ(F2_06, F3_20) = **+0,444** indicam que
processos com documentação incompleta (F2_06) tendem a ser ajuizados por
advogados com volume elevado de demandas e petições idênticas — padrão
consistente com a hipótese de produção em escala.

---

**Limitação:** φ mede apenas associação linear. Interações entre variáveis
(ex.: F2_01 **∧** F2_11) podem ter poder discriminante adicional não capturado
pela matriz, demandando análise exploratória complementar (ex.: árvores de
decisão ou regras de associação) em pesquisas futuras.
''')


# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 8 — CÓDIGO: GRÁFICO AUXILIAR — HEATMAP RESTRITO F2 × F3 + CLASSIF.
# ──────────────────────────────────────────────────────────────────────────────
code(r'''
# ── Gráfico 11b: submatriz phi F2 × (F3 + classificações) ────────────────────
# Heatmap pequeno (13×5) — usa imshow para velocidade; anotações em todas as células.

COLS_X = COLS_F2_ATIVOS           # 13 linhas
COLS_Y = COLS_F3_PHI + COLS_CLASSIF  # 5 colunas
nr, nc = len(COLS_X), len(COLS_Y)

sub_arr = phi_df.loc[COLS_X, COLS_Y].values.astype(float)
rot_x   = [NOMES_PHI.get(c, c) for c in COLS_X]
rot_y   = [NOMES_PHI.get(c, c) for c in COLS_Y]

fig, ax = plt.subplots(figsize=(8, 6.5))
im2 = ax.imshow(sub_arr, cmap=MAPA_DIVERGENTE,
                vmin=-1, vmax=1, aspect='auto',
                interpolation='nearest')

for i in range(nr):
    for j in range(nc):
        v = sub_arr[i, j]
        cor_txt = 'white' if abs(v) >= 0.55 else TINTA
        ax.text(j, i, f'{v:+.2f}',
                ha='center', va='center',
                fontsize=9.0, color=cor_txt, fontweight='bold')

# Separador F3 | classificações
ax.axvline(len(COLS_F3_PHI) - 0.5, color=TINTA, linewidth=2.0)

ax.set_xticks(range(nc))
ax.set_xticklabels(rot_y, rotation=25, ha='right', fontsize=9.0)
ax.set_yticks(range(nr))
ax.set_yticklabels(rot_x, fontsize=8.5)

cbar2 = fig.colorbar(im2, ax=ax, shrink=0.60, aspect=20, pad=0.01)
cbar2.set_label('φ', fontsize=9)

ax.set_title(
    'Gráfico 11b – Submatriz phi: variáveis F2 × Fase III e classificações\n'
    'Fonte: elaborada pela autora, a partir da aba AMOSTRA (2025).',
    fontsize=11, fontweight='bold',
)
plt.tight_layout()
plt.show()
''')


# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 9 — MARKDOWN: SÍNTESE DA SEÇÃO 9
# ──────────────────────────────────────────────────────────────────────────────
md(r'''
### 9.2 Síntese e implicações para a pesquisa

**Achados principais da análise de correlação phi:**

1. **A multicolinearidade F2_01 × F2_02 (φ = 0,975)** é o principal fator
   de instabilidade do modelo logístico. Em aplicações práticas, bastaria
   registrar *qualquer* dessas duas variáveis — ambas capturam essencialmente
   a mesma dimensão de irregularidade documental.

2. **F2_11 é um preditor genuinamente independente** (φ com F2_02 = 0,442;
   φ com F2_01 = 0,446 — correlações moderadas, não extremas), o que justifica
   sua manutenção no modelo mesmo controlado pelas demais variáveis.

3. **F2_06 (documentos incompletos/ilegíveis) forma um bloco coerente com
   F2_01 e F2_02** (φ ≈ 0,41–0,42), mas sua correlação com o desfecho
   (φ com Indício = 0,413) é inferior à de F2_11 (0,539). O modelo reduzido
   corretamente prioriza F2_11 em detrimento de F2_06.

4. **As variáveis F1 têm correlação negativa fraca com Indício**
   (F1_A: φ = −0,181; F1_B: φ = −0,103): processos excluídos na Fase I
   não chegam à análise de indício, criando uma correlação negativa
   artificial — não um efeito substantivo.

5. **Implicação prática para triagem automatizada:** um sistema de alerta
   poderia operar com apenas **dois gatilhos documentais** — F2_02 (ausência
   de documentos essenciais) e F2_11 (advogado fora da comarca) —, capturando
   a maior parte da variância explicada com mínima carga de coleta de dados.
   A adição de F2_01 ou F2_06 marginaliza o ganho informativo dado o alto
   grau de redundância.
''')
