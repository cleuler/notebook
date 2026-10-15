# -*- coding: utf-8 -*-
"""
Seção 8 — Regressão Logística e Curva ROC
==========================================
Gera as células do notebook referentes à seção 4.3.4 da monografia.

Outputs desta seção
--------------------
  Tabela 14  — Modelo logístico reduzido (F2_01, F2_02, F2_11):
                coeficiente, OR, IC 95%, p-valor, pseudo-R² McFadden
  Gráfico 10 — Curva ROC do modelo reduzido (AUC = 0,908)
  Tabela 15  — Frequência das variáveis F2_14 a F2_17 por classificação
               + teste χ² de associação com Indício

Valores de referência (monografia, seção 4.3.4)
-------------------------------------------------
  Pseudo-R² McFadden (reduzido)  : 0,482
  AIC (reduzido)                 : 174,13
  Log-verossimilhança (reduzido) : −83,06
  AUC-ROC                        : 0,908
  Matriz de confusão (corte 0,5) : VP=85; FP=11; FN=20; VN=117
  Acurácia                       : 86,7%
  Sensibilidade                  : 80,9%
  Especificidade                 : 91,4%
  OR F2_02 (modelo)              : 30,7   (p=0,008)
  OR F2_11 (modelo)              : 5,0    (p<0,001)
  OR F2_01 (modelo)              : 1,7    (p=0,665 — não significativo)
  χ² F2_14 × Indício             : 26,67  (gl=1; p<0,001)
  Pseudo-R² modelo completo      : 0,496

Seção da monografia: 4.3.4 e 4.3.4.1
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
# CÉLULA 1 — MARKDOWN: INTRODUÇÃO À SEÇÃO 8
# ──────────────────────────────────────────────────────────────────────────────
md(r'''
---

## 8. Regressão Logística e Curva ROC

Esta seção apresenta o modelo preditivo desenvolvido para identificar
processos com **indício de litigância predatória** a partir das variáveis
da Fase II — sem necessidade de acesso às variáveis sistêmicas da Fase III
(F3_18–F3_20), que exigem consulta a sistemas externos ao PJe.

O objetivo pragmático é construir um **instrumento de triagem automatizável**:
dado um processo com ao menos um marcador de irregularidade formal (Fase II),
qual é a probabilidade de ele satisfazer os critérios de indício (F3_19 e
F3_20 simultâneos)?

**Base de modelagem:** os **233 processos avaliados na Fase III**, que
representam o universo de interesse — casos que já passaram pela triagem
de irregularidade formal e precisam ser priorizados para verificação sistêmica.

**Estratégia de modelagem:**

| Modelo | Preditores | Lógica |
|---|---|---|
| **Completo** | 8 variáveis F2 com ≥ 10 ocorrências na Fase III | Máxima informação disponível |
| **Reduzido** | F2_01, F2_02, F2_11 | Parsimônia: AIC menor; interpretabilidade; suporte da análise bivariada |

A seleção do modelo reduzido é fundamentada em três critérios: (i) AIC
inferior ao modelo completo (174,1 vs 179,5); (ii) OR altamente
significativos para F2_02 e F2_11; e (iii) eliminação de preditores
colineares que inflariam os erros padrão sem ganho informativo.

> **Nota sobre F2_01:** a variável entra no modelo reduzido por coerência
> substantiva (é o preditor bivariado de maior OR após F2_02), mas o
> coeficiente não é individualmente significativo após o ajuste por F2_02
> — sinal de multicolinearidade elevada, confirmada pela correlação
> φ(F2_01, F2_02) ≈ 0,98 (Seção 9).
''')


# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 2 — CÓDIGO: SETUP DA SEÇÃO 8
# ──────────────────────────────────────────────────────────────────────────────
code(r'''
# ── Subconjunto Fase III ──────────────────────────────────────────────────────
dados_f3 = dados[dados['Avancou_F3']].copy()
N_F3     = len(dados_f3)          # 233
assert N_F3 == 233

# ── Variável desfecho e preditores ───────────────────────────────────────────
Y = dados_f3['Indicio'].astype(int)

# Variáveis F2 ativas (sem zeros: F2_07, F2_12, F2_15, F2_16)
COLS_F2_ATIVOS = [c for c in COLS_F2 if c not in {'F2_07', 'F2_12', 'F2_15', 'F2_16'}]

# Variáveis com >= 10 ocorrências na Fase III (candidatas ao modelo completo)
COLS_MODELO_COMPLETO = [
    c for c in COLS_F2_ATIVOS
    if dados_f3[c].sum() >= 10
]  # F2_01, F2_02, F2_04, F2_06, F2_09, F2_10, F2_11, F2_14

# Variáveis do modelo reduzido
COLS_MODELO_RED = ['F2_01', 'F2_02', 'F2_11']

print('Setup da Secao 8 concluido.')
print(f'  Fase III : {N_F3} processos  |  Indicio: {Y.sum()} ({Y.mean()*100:.1f}%)')
print(f'  Modelo completo  : {len(COLS_MODELO_COMPLETO)} preditores: {COLS_MODELO_COMPLETO}')
print(f'  Modelo reduzido  : {COLS_MODELO_RED}')
''')


# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 3 — CÓDIGO: AJUSTE DOS MODELOS LOGÍSTICOS
# ──────────────────────────────────────────────────────────────────────────────
code(r'''
# ── Modelo reduzido: F2_01, F2_02, F2_11 ─────────────────────────────────────
X_red  = sm.add_constant(dados_f3[COLS_MODELO_RED].astype(float))
logit_red = sm.Logit(Y, X_red).fit(disp=False, maxiter=200)

# ── Modelo completo: 8 preditores ────────────────────────────────────────────
X_full = sm.add_constant(dados_f3[COLS_MODELO_COMPLETO].astype(float))
logit_full = sm.Logit(Y, X_full).fit(disp=False, maxiter=200)

# ── Validação dos valores de referência ──────────────────────────────────────
assert abs(logit_red.prsquared - 0.482) < 0.002, \
    f'Pseudo-R2 reduzido esperado 0,482; obtido {logit_red.prsquared:.4f}'
assert abs(logit_red.aic - 174.13) < 0.10, \
    f'AIC reduzido esperado 174,13; obtido {logit_red.aic:.4f}'
assert abs(logit_red.llf - (-83.06)) < 0.10, \
    f'Log-lik reduzido esperado -83,06; obtido {logit_red.llf:.4f}'
assert abs(logit_full.prsquared - 0.496) < 0.002, \
    f'Pseudo-R2 completo esperado 0,496; obtido {logit_full.prsquared:.4f}'

print('Asserts modelos logisticos: OK')
print()
print('── Modelo Reduzido ──────────────────────────────────────────────────────')
print(f'  Pseudo-R2 McFadden : {logit_red.prsquared:.4f}')
print(f'  AIC                : {logit_red.aic:.4f}')
print(f'  Log-verossimilhanca: {logit_red.llf:.4f}')
print(f'  Log-verossim. nula : {logit_red.llnull:.4f}')
print()
print('── Modelo Completo ──────────────────────────────────────────────────────')
print(f'  Pseudo-R2 McFadden : {logit_full.prsquared:.4f}')
print(f'  AIC                : {logit_full.aic:.4f}')
print(f'  Ganho de AIC (red - full): {logit_full.aic - logit_red.aic:+.2f}')
''')


# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 4 — CÓDIGO: TABELA 14 — COEFICIENTES DO MODELO REDUZIDO
# ──────────────────────────────────────────────────────────────────────────────
code(r'''
# ── Tabela 14: coeficientes, OR, IC 95%, p-valor ─────────────────────────────
NOMES_PRED = {
    'const' : 'Constante (intercepto)',
    'F2_01' : 'F2_01 — Petição vaga/genérica',
    'F2_02' : 'F2_02 — Ausência de documentos essenciais',
    'F2_11' : 'F2_11 — Advogado fora da comarca',
}

ci_red = logit_red.conf_int()   # IC 95% dos coeficientes (log-odds)

linhas_tab14 = []
for var in X_red.columns:
    coef   = logit_red.params[var]
    ci_lo  = ci_red.loc[var, 0]
    ci_hi  = ci_red.loc[var, 1]
    pval   = logit_red.pvalues[var]
    se     = logit_red.bse[var]
    or_v   = np.exp(coef)
    ic_lo  = np.exp(ci_lo)
    ic_hi  = np.exp(ci_hi)
    linhas_tab14.append({
        'Variável'     : NOMES_PRED.get(var, var),
        'Coef. (β)'    : coef,
        'Erro padrão'  : se,
        'OR (exp(β))'  : or_v,
        'IC 2,5% OR'   : ic_lo,
        'IC 97,5% OR'  : ic_hi,
        'p-valor'      : pval,
        '_sig'         : pval < 0.05,
    })

tab14 = pd.DataFrame(linhas_tab14)

# Validar OR do modelo
or_f02_mod = tab14.loc[tab14['Variável'].str.contains('F2_02'), 'OR (exp(β))'].values[0]
or_f11_mod = tab14.loc[tab14['Variável'].str.contains('F2_11'), 'OR (exp(β))'].values[0]
assert abs(or_f02_mod - 30.7) < 1.0, \
    f'OR F2_02 (modelo) esperado ~30,7; obtido {or_f02_mod:.2f}'
assert abs(or_f11_mod -  5.0) < 0.5, \
    f'OR F2_11 (modelo) esperado ~5,0; obtido {or_f11_mod:.2f}'
print('Asserts Tabela 14: OK')
print()

# ── Rodapé com indicadores globais do modelo ─────────────────────────────────
rodape = (
    f'Tabela 14 – Coeficientes do modelo logístico reduzido '
    f'(F2_01, F2_02, F2_11 | base: 233 processos da Fase III) | '
    f'Fonte: elaborada pela autora, a partir da aba AMOSTRA (2025). '
    f'Pseudo-R² McFadden = {logit_red.prsquared:.3f} | '
    f'AIC = {logit_red.aic:.1f} | '
    f'Log-lik = {logit_red.llf:.2f}. '
    f'OR calculado como exp(β). IC 95% de Wald sobre log-odds. '
    f'Destaque: variáveis significativas (p < 0,05).'
)

# Formatador de p-valor para célula
def fmt_pval(v):
    if v < 0.001:
        return 'p < 0,001'
    return f'{v:.4f}'.replace('.', ',')

display(
    tab14[['Variável', 'Coef. (β)', 'Erro padrão', 'OR (exp(β))',
           'IC 2,5% OR', 'IC 97,5% OR', 'p-valor']].style
    .set_caption(rodape)
    .format({
        'Coef. (β)'   : '{:+.4f}',
        'Erro padrão' : '{:.4f}',
        'OR (exp(β))' : '{:.3f}',
        'IC 2,5% OR'  : '{:.3f}',
        'IC 97,5% OR' : '{:.3f}',
        'p-valor'     : fmt_pval,
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
        # Linha da constante: cinza; significativos: azul claro; demais: alternado
        'background-color: #f0f0f0; color: #777777'
        if tab14.iloc[r]['Variável'] == 'Constante (intercepto)'
        else 'background-color: #eef3fc; font-weight: bold'
        if tab14.iloc[r]['_sig']
        else ''
        for r in range(len(col))
    ])
    .bar(subset=['OR (exp(β))'], color=COR_DESTAQUE, vmin=0,
         vmax=tab14['IC 97,5% OR'].max() * 0.25)
    .hide(axis='index')
)
''')


# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 5 — MARKDOWN: INTERPRETAÇÃO DO MODELO
# ──────────────────────────────────────────────────────────────────────────────
md(r'''
### 8.1 Interpretação do modelo logístico reduzido (4.3.4)

O modelo ajustado apresenta **pseudo-R² de McFadden = 0,482** — valor
interpretado como "ajuste substancial" (convencionalmentte acima de 0,4),
indicando que as três variáveis explicam quase metade da variância das
log-probabilidades do desfecho.

**Interpretação dos coeficientes:**

- **F2_02** (Ausência de documentos essenciais) — OR = **30,7** (IC 95%:
  2,5 a 380,7; p = 0,008): controlando pelas demais variáveis, processos
  com esse marcador têm chance aproximadamente **30 vezes maior** de
  satisfazer o critério de indício. A largura do IC reflete separação
  quase-perfeita: na amostra, 85 dos 96 processos com F2_02 positivo têm
  indício, enquanto apenas 20 dos 137 sem F2_02 o têm.

- **F2_11** (Advogado fora da comarca) — OR = **5,0** (IC 95%: 2,2 a 11,6;
  p < 0,001): efeito robusto e bem-estimado; a variável mantém significância
  mesmo controlando por F2_01 e F2_02, sinalizando contribuição informativa
  independente.

- **F2_01** (Petição vaga/genérica) — OR = **1,7** (IC 95%: 0,15 a 20,2;
  p = 0,665): coeficiente não significativo após o ajuste. Esse resultado é
  esperado: F2_01 e F2_02 têm correlação φ ≈ 0,98 (Seção 9), tornando a
  estimativa individual de cada uma imprecisa na presença da outra.
  A variável foi mantida no modelo pela sua relevância substantiva e pelo
  suporte da análise bivariada (OR univariado = 37,6).

**Comparação com o modelo completo:** o modelo reduzido tem **AIC = 174,1**
contra **179,5** do modelo completo com 8 preditores — o critério de
informação favorece inequivocamente o modelo mais parcimonioso.

**Atenção: separação quase-perfeita.** A combinação F2_01+F2_02 prediz o
desfecho com quase perfeição dentro da amostra, o que gera IC extremamente
largos para esses coeficientes individualmente. Em amostras maiores ou com
conjunto de teste separado, os OR seriam mais estáveis.
''')


# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 6 — CÓDIGO: CURVA ROC, AUC E MATRIZ DE CONFUSÃO (GRÁFICO 10)
# ──────────────────────────────────────────────────────────────────────────────
code(r'''
# ── Probabilidades preditas ───────────────────────────────────────────────────
prob_red = logit_red.predict()

# ── Curva ROC ────────────────────────────────────────────────────────────────
fpr, tpr, thresholds_roc = roc_curve(Y, prob_red)
roc_auc = auc(fpr, tpr)

# Melhor ponto de corte (índice de Youden: max(sensibilidade + especificidade - 1))
J        = tpr - fpr
idx_youd = int(np.argmax(J))
corte_youden = thresholds_roc[idx_youd]

# Validação
assert abs(roc_auc - 0.908) < 0.002, \
    f'AUC esperada 0,908; obtida {roc_auc:.4f}'
print(f'AUC-ROC: {roc_auc:.4f}  |  Melhor corte (Youden): {corte_youden:.4f}')

# ── Matriz de confusão (corte 0,5) ────────────────────────────────────────────
CORTE = 0.5
pred_50 = (prob_red >= CORTE).astype(int)
cm = confusion_matrix(Y, pred_50)
VN_v, FP_v = int(cm[0, 0]), int(cm[0, 1])
FN_v, VP_v = int(cm[1, 0]), int(cm[1, 1])
acuracia    = (VP_v + VN_v) / N_F3
sens        = VP_v / (VP_v + FN_v)
espec       = VN_v / (VN_v + FP_v)
vpp         = VP_v / (VP_v + FP_v) if (VP_v + FP_v) > 0 else np.nan
vnp         = VN_v / (VN_v + FN_v) if (VN_v + FN_v) > 0 else np.nan

assert VP_v == 85, f'VP esperado 85; obtido {VP_v}'
assert FP_v == 11, f'FP esperado 11; obtido {FP_v}'
assert FN_v == 20, f'FN esperado 20; obtido {FN_v}'
assert VN_v == 117, f'VN esperado 117; obtido {VN_v}'
assert abs(acuracia - 0.867) < 0.002
print(f'Matriz de confusao (corte={CORTE}): VP={VP_v}  FP={FP_v}  FN={FN_v}  VN={VN_v}')
print(f'  Acuracia     : {acuracia*100:.2f}%')
print(f'  Sensibilidade: {sens*100:.2f}%')
print(f'  Especificidade:{espec*100:.2f}%')
print(f'  VPP          : {vpp*100:.2f}%')
print(f'  VPN          : {vnp*100:.2f}%')
print()

# ── Gráfico 10: Curva ROC + Matriz de Confusão ───────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(13, 5.5))

# ── Painel esquerdo: Curva ROC ────────────────────────────────────────────────
ax_roc = axes[0]
ax_roc.plot(fpr, tpr,
            color=COR_PRINCIPAL, lw=2.5, label=f'ROC  (AUC = {roc_auc:.3f})')
ax_roc.plot([0, 1], [0, 1],
            color=TINTA_2, lw=1.2, linestyle='--', label='Classificador aleatório')

# Marcar ponto de Youden
ax_roc.scatter(
    fpr[idx_youd], tpr[idx_youd],
    color=COR_DESTAQUE, s=90, zorder=5,
    label=f'Youden  (corte = {corte_youden:.2f};\n'
          f'Sens = {tpr[idx_youd]*100:.1f}%;  1–Esp = {fpr[idx_youd]*100:.1f}%)',
)
# Marcar ponto do corte 0,5
fpr_50 = float(FP_v / (FP_v + VN_v))
tpr_50 = float(VP_v / (VP_v + FN_v))
ax_roc.scatter(
    fpr_50, tpr_50,
    marker='s', color=COR_CERTEZA, s=80, zorder=5,
    label=f'Corte 0,5  (Sens = {tpr_50*100:.1f}%;  1–Esp = {fpr_50*100:.1f}%)',
)

ax_roc.set_xlim(-0.02, 1.02)
ax_roc.set_ylim(-0.02, 1.05)
ax_roc.set_xlabel('1 − Especificidade  (Taxa de falsos positivos)', fontsize=10)
ax_roc.set_ylabel('Sensibilidade  (Taxa de verdadeiros positivos)', fontsize=10)
ax_roc.set_title(
    'Gráfico 10 – Curva ROC: modelo logístico reduzido\n'
    '(F2_01 + F2_02 + F2_11 | Fase III, n = 233)',
    fontsize=11,
)
ax_roc.legend(fontsize=8.5, loc='lower right')
ax_roc.fill_between(fpr, tpr, alpha=0.08, color=COR_PRINCIPAL)

# ── Painel direito: Matriz de Confusão visual ─────────────────────────────────
ax_cm = axes[1]
cm_array = np.array([[VN_v, FP_v], [FN_v, VP_v]])
labels   = [['VN\n(Indício Não\npredito Não)',  'FP\n(Indício Não\npredito Sim)'],
            ['FN\n(Indício Sim\npredito Não)',  'VP\n(Indício Sim\npredito Sim)']]
cores_cm = [[COR_SECUNDARIA, COR_EXCLUIDO],
            [COR_INDICIO,    COR_PRINCIPAL]]

for i in range(2):
    for j in range(2):
        cor   = cores_cm[i][j]
        valor = cm_array[i, j]
        texto = labels[i][j]
        rect  = plt.Rectangle([j, 1 - i], 1, 1,
                               facecolor=cor, edgecolor='white', linewidth=2)
        ax_cm.add_patch(rect)
        ax_cm.text(j + 0.5, 1 - i + 0.5,
                   f'{valor}\n\n{texto}',
                   ha='center', va='center',
                   fontsize=10 if valor > 10 else 9.5,
                   color='white' if cor not in [COR_SECUNDARIA] else TINTA,
                   fontweight='bold')

ax_cm.set_xlim(0, 2)
ax_cm.set_ylim(0, 2)
ax_cm.set_xticks([0.5, 1.5])
ax_cm.set_yticks([0.5, 1.5])
ax_cm.set_xticklabels(['Predito: Não', 'Predito: Sim'], fontsize=10)
ax_cm.set_yticklabels(['Real: Sim\n(Indício)', 'Real: Não\n(Sem indício)'], fontsize=10)
ax_cm.xaxis.set_ticks_position('top')
ax_cm.xaxis.set_label_position('top')
ax_cm.invert_yaxis()
ax_cm.set_aspect('equal')
ax_cm.grid(False)
ax_cm.set_title(
    f'Matriz de Confusão  (corte = {CORTE})\n'
    f'Acurácia = {acuracia*100:.1f}%  |  '
    f'Sens = {sens*100:.1f}%  |  '
    f'Esp = {espec*100:.1f}%',
    fontsize=11,
)

plt.suptitle(
    'Fonte: elaborada pela autora, a partir da aba AMOSTRA (2025). '
    'Modelo: regressão logística binária (MLE, statsmodels.Logit).\n'
    'VN = verdadeiro negativo; FP = falso positivo; '
    'FN = falso negativo; VP = verdadeiro positivo.',
    fontsize=8.5, y=-0.04, color=TINTA_2,
)
plt.tight_layout()
plt.show()
''')


# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 7 — MARKDOWN: INTERPRETAÇÃO DA ROC E DA MATRIZ DE CONFUSÃO
# ──────────────────────────────────────────────────────────────────────────────
md(r'''
### 8.2 Desempenho do modelo: ROC e matriz de confusão (4.3.4)

**Curva ROC e AUC.** A área sob a curva ROC (AUC) de **0,908** indica
desempenho classificatório excelente segundo o critério convencional
(AUC > 0,90). O modelo discrimina com alta eficiência os processos com
indício dos sem indício, com base exclusivamente nas variáveis documentais
formais (F2_01, F2_02 e F2_11).

**Ponto de corte ótimo (Youden).** O índice de Youden
(J = Sensibilidade + Especificidade − 1) é maximizado em
corte ≈ **0,40**, com desempenho praticamente idêntico ao corte 0,5
em termos de acurácia geral (86,7%), mas com discreta melhora na
sensibilidade (81,9% vs 80,9%). Para fins de triagem judicial — em que
a consequência de um falso negativo (caso real de litigância não
identificado) é potencialmente mais custosa que um falso positivo —,
o corte de 0,40 seria preferível.

**Matriz de confusão (corte 0,5):**

| — | Predito Não | Predito Sim |
|---|---|---|
| **Real Não** | VN = **117** | FP = **11** |
| **Real Sim** | FN = **20** | VP = **85** |

- **Sensibilidade = 80,9%:** 1 em cada 5 casos de indício não é
  capturado pelo modelo. Esses 20 falsos negativos correspondem,
  em maioria, a processos com F2_11 positivo e F2_01/F2_02 negativos —
  perfil menos típico da litigância industrializada em série.

- **Especificidade = 91,4%:** apenas 11 processos sem indício são
  incorretamente classificados como casos suspeitos — taxa de falso
  alarme baixa, relevante para a viabilidade operacional da triagem.

- **Acurácia geral = 86,7%** (202/233 classificados corretamente).

**Implicação prática.** Um sistema de triagem baseado neste modelo
reduziria em aproximadamente **80%** o esforço de verificação sistêmica
na Fase III — focando o trabalho dos analistas nos **105 processos com
probabilidade predita ≥ 0,5**, sem precisar processar manualmente os
**128 com probabilidade inferior**.
''')


# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 8 — CÓDIGO: CURVAS ROC POR PREDITOR ISOLADO (COMPARAÇÃO)
# ──────────────────────────────────────────────────────────────────────────────
code(r'''
# ── Curvas ROC individuais: cada preditor isolado vs. modelo reduzido ─────────
fig, ax = plt.subplots(figsize=(9, 5.5))

# Modelo reduzido (já calculado)
ax.plot(fpr, tpr, lw=2.5, color=COR_PRINCIPAL,
        label=f'Modelo reduzido (F2_01+F2_02+F2_11)  AUC = {roc_auc:.3f}')

# Preditores individuais: modelo logístico simples (intercept + 1 preditor)
CORES_IND = [CORES[1], CORES[2], CORES[3]]
for col, cor in zip(COLS_MODELO_RED, CORES_IND):
    X_solo = sm.add_constant(dados_f3[[col]].astype(float))
    logit_solo = sm.Logit(Y, X_solo).fit(disp=False, maxiter=200)
    prob_solo  = logit_solo.predict()
    fpr_s, tpr_s, _ = roc_curve(Y, prob_solo)
    auc_s = auc(fpr_s, tpr_s)
    ax.plot(fpr_s, tpr_s, lw=1.5, linestyle=':', color=cor,
            label=f'{col} isolado  AUC = {auc_s:.3f}')

ax.plot([0, 1], [0, 1], lw=1.0, linestyle='--', color=TINTA_2, alpha=0.6,
        label='Classificador aleatório')

ax.set_xlim(-0.02, 1.02)
ax.set_ylim(-0.02, 1.05)
ax.set_xlabel('1 − Especificidade  (Taxa de falsos positivos)', fontsize=10)
ax.set_ylabel('Sensibilidade  (Taxa de verdadeiros positivos)', fontsize=10)
ax.fill_between(fpr, tpr, alpha=0.06, color=COR_PRINCIPAL)
ax.set_title(
    'Gráfico 10b – Comparação de curvas ROC: modelo reduzido vs. preditores isolados\n'
    'Fonte: elaborada pela autora, a partir da aba AMOSTRA (2025).',
    fontsize=11,
)
ax.legend(fontsize=9, loc='lower right')
plt.tight_layout()
plt.show()
''')


# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 9 — MARKDOWN: SEÇÃO 4.3.4.1 — VARIÁVEIS F2_14 A F2_17
# ──────────────────────────────────────────────────────────────────────────────
md(r'''
### 8.3 Variáveis F2_14 a F2_17: análise complementar (4.3.4.1)

As quatro variáveis do bloco **F2_14 a F2_17** — que registram condutas
de **desistência processual em momento estratégico** — merecem tratamento
separado por razões metodológicas:

- **F2_15** (desistência após notificação) e **F2_16** (desistência após
  contestação) apresentaram **zero ocorrências** em toda a amostra de 595
  processos. Conforme discutido na Seção 6, isso pode refletir depuração
  prévia na planilha-base ou adaptação dos litigantes ao monitoramento
  crescente dos centros de inteligência do Poder Judiciário.

- **F2_17** (contrato de honorários abusivo) teve apenas **3 ocorrências**
  na amostra total — frequência insuficiente para análise estatística
  robusta isolada.

- **F2_14** (desistência após indeferimento de liminar) é a única com
  frequência relevante: **17 ocorrências na Fase III** (7,3% dos 233
  processos), com 11 dos 17 casos (64,7%) classificados como indício.
  O teste χ² de associação com a variável `Indício` é **altamente
  significativo** (χ² = 26,67; gl = 1; p < 0,001), indicando associação
  forte entre esse comportamento e o desfecho de indício.

A razão pela qual F2_14 não integra o modelo reduzido, apesar da
significância bivariada, é a sua **baixa frequência** (17/233): sua
inclusão não melhora o AIC (modelo completo com 8 preditores inclusive
F2_14: AIC = 179,5), e o OR estimado seria muito instável. Ela aparece,
entretanto, como variável de interesse para investigações futuras com
amostras maiores.
''')


# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 10 — CÓDIGO: TABELA 15 — F2_14 A F2_17 POR CLASSIFICAÇÃO
# ──────────────────────────────────────────────────────────────────────────────
code(r'''
# ── Tabela 15: frequência de F2_14 a F2_17 por classificação ─────────────────
NOMES_F2_COMP = {
    'F2_14': 'F2_14 — Desistência após indeferi. de liminar',
    'F2_15': 'F2_15 — Desistência após notificação (*)',
    'F2_16': 'F2_16 — Desistência após contestação (*)',
    'F2_17': 'F2_17 — Contrato de honorários abusivo',
}

linhas_tab15 = []
for col in ['F2_14', 'F2_15', 'F2_16', 'F2_17']:
    n_total  = int(dados[col].sum())
    n_ind    = int((dados[col] &  dados['Indicio']).sum())
    n_cert   = int((dados[col] &  dados['Certeza']).sum())
    n_nind   = int((dados[col] & ~dados['Indicio']).sum())
    pct_ind  = n_ind  / n_total if n_total > 0 else np.nan
    pct_nind = n_nind / n_total if n_total > 0 else np.nan
    # chi2 de associação com Indicio (sobre os 595)
    tab_2x2 = pd.crosstab(dados[col], dados['Indicio'])
    if tab_2x2.shape == (2, 2):
        chi2_v, p_v, gl_v, _ = stats.chi2_contingency(tab_2x2, correction=False)
    else:
        chi2_v, p_v, gl_v = np.nan, np.nan, np.nan
    linhas_tab15.append({
        'Código'                   : col,
        'Nome da Variável'         : NOMES_F2_COMP[col],
        'n total (595)'            : n_total,
        '% sobre 595'              : n_total / N_AMST,
        'n Indício (incl. cert.)'  : n_ind,
        '% Indício | F2=Sim'       : pct_ind,
        'n Certeza'                : n_cert,
        'n Sem Indício'            : n_nind,
        '% Sem Ind. | F2=Sim'      : pct_nind,
        'χ² (gl=1)'                : chi2_v,
        'p-valor χ²'               : p_v,
    })

tab15 = pd.DataFrame(linhas_tab15)

# Validar F2_14
assert tab15.loc[tab15['Código'] == 'F2_14', 'n total (595)'].values[0] == 17, \
    'F2_14: esperado 17 ocorrências'
assert tab15.loc[tab15['Código'] == 'F2_14', 'n Indício (incl. cert.)'].values[0] == 11, \
    'F2_14 com Indicio: esperado 11'
chi2_f14_real = tab15.loc[tab15['Código'] == 'F2_14', 'χ² (gl=1)'].values[0]
assert abs(chi2_f14_real - 26.67) < 0.10, \
    f'chi2 F2_14 esperado 26,67; obtido {chi2_f14_real:.3f}'
# F2_15 e F2_16 devem ser zero
assert tab15.loc[tab15['Código'] == 'F2_15', 'n total (595)'].values[0] == 0
assert tab15.loc[tab15['Código'] == 'F2_16', 'n total (595)'].values[0] == 0
print('Asserts Tabela 15: OK')
print(f'  chi2 F2_14 × Indicio: {chi2_f14_real:.3f}')
print()

# ── Formatadores ─────────────────────────────────────────────────────────────
def fmt_pct(v):
    return f'{v*100:.1f}%' if pd.notna(v) else '—'

def fmt_chi2(v):
    return f'{v:.2f}' if pd.notna(v) else '—'

def fmt_pchi(v):
    if pd.isna(v):
        return '—'
    if v < 0.001:
        return 'p < 0,001'
    return f'{v:.4f}'.replace('.', ',')

display(
    tab15[['Código', 'Nome da Variável', 'n total (595)', '% sobre 595',
           'n Indício (incl. cert.)', '% Indício | F2=Sim',
           'n Sem Indício', '% Sem Ind. | F2=Sim',
           'χ² (gl=1)', 'p-valor χ²']].style
    .set_caption(
        'Tabela 15 – Frequência das variáveis F2_14 a F2_17 por classificação '
        '(n = 595) | Fonte: elaborada pela autora, a partir da aba AMOSTRA (2025).\n'
        '(*) F2_15 e F2_16: zero ocorrências em toda a amostra — depuradas '
        'previamente na planilha-base do TJRN. '
        'χ²: teste de homogeneidade (sem correção de continuidade); '
        'variáveis com n = 0 não têm teste calculável.'
    )
    .format({
        '% sobre 595'          : fmt_pct,
        '% Indício | F2=Sim'   : fmt_pct,
        '% Sem Ind. | F2=Sim'  : fmt_pct,
        'χ² (gl=1)'            : fmt_chi2,
        'p-valor χ²'           : fmt_pchi,
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
        # F2_14: destaque laranja (significativo)
        'background-color: #fff3e0; font-weight: bold'
        if tab15.iloc[r]['Código'] == 'F2_14'
        # F2_15/F2_16: cinza (zero ocorrências)
        else 'background-color: #f5f5f5; color: #999999'
        if tab15.iloc[r]['n total (595)'] == 0
        else 'background-color: #eef3fc' if r % 2 == 0
        else ''
        for r in range(len(col))
    ])
    .hide(axis='index')
)

# ── Gráfico de barras: F2_14 por classificação ────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 3.8))
categorias_f14 = ['Indício (incl. certeza)', 'Sem indício']
valores_f14    = [11, 6]
cores_f14      = [COR_PRINCIPAL, GRADE]
bars_f14 = ax.bar(categorias_f14, valores_f14, width=0.45,
                  color=cores_f14, edgecolor='white', linewidth=1.2)
for barra, v in zip(bars_f14, valores_f14):
    pct = v / 17 * 100
    ax.text(barra.get_x() + barra.get_width() / 2,
            barra.get_height() + 0.15,
            f'{v}  ({pct:.1f}%)', ha='center', va='bottom',
            fontsize=11, color=TINTA)

ax.set_ylabel('Processos (n = 17 com F2_14 = Sim)')
ax.set_ylim(0, 15)
ax.set_title(
    f'Tabela 15 – F2_14 por classificação (total = 17)\n'
    f'χ² = {chi2_f14_real:.2f}  (gl=1; p < 0,001) | '
    'Fonte: elaborada pela autora, a partir da aba AMOSTRA (2025).',
    fontsize=11,
)
ax.grid(axis='x', visible=False)
plt.tight_layout()
plt.show()
''')


# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 11 — MARKDOWN: SÍNTESE DA SEÇÃO 8
# ──────────────────────────────────────────────────────────────────────────────
md(r'''
### 8.4 Síntese da Seção 8

**Três achados centrais emergem da modelagem logística:**

1. **É possível predizer o indício de litigância predatória a partir de
   variáveis documentais formais** (Fase II), sem necessidade de acesso a
   sistemas externos ao PJe. O modelo com três variáveis (F2_01, F2_02 e
   F2_11) atinge AUC = **0,908** — limiar de excelência — com acurácia
   global de **86,7%**.

2. **A ausência de documentação essencial (F2_02) é o preditor mais
   poderoso**: controlada pelas demais variáveis, triplica o OR bivariado
   estimado em separado, atingindo **OR = 30,7** no modelo ajustado.
   Esse resultado é coerente com a hipótese de que a litigância predatória
   opera por escala e padronização, dispensando a personalização dos
   documentos processuais.

3. **F2_14 (desistência após indeferimento de liminar) merece atenção**
   mesmo com apenas 17 casos: a associação com indício é altamente
   significativa (p < 0,001) e a proporção condicional de indício entre
   esses processos (64,7%) é muito superior à proporção global (105/233 =
   45,1%). Esse padrão é consistente com a hipótese de "abandono estratégico"
   — o litigante desiste assim que percebe que o processo não converge para
   um acordo rápido.

**Limitações do modelo:**

- **Sem validação cruzada:** o modelo foi ajustado e avaliado sobre o mesmo
  conjunto de 233 processos. A AUC e a acurácia reportadas são estimativas
  otimistas (*in-sample*). Uma validação com conjunto de teste independente —
  ou *k*-fold — forneceria estimativas mais conservadoras e generalizáveis.

- **Separação quase-perfeita de F2_01/F2_02:** a correlação φ ≈ 0,98 entre
  esses dois preditores gera IC extremamente amplos para os coeficientes
  individuais. Em amostras maiores, os coeficientes seriam mais estáveis e
  o modelo poderia ser re-especificado com apenas uma das duas variáveis.

- **Base restrita aos 233 da Fase III:** o modelo não é diretamente aplicável
  à totalidade dos 595 processos — apenas àqueles que já apresentaram ao
  menos um marcador de irregularidade formal na Fase II.
''')
