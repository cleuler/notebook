# -*- coding: utf-8 -*-
"""
Seção 5 — Resultados Descritivos Gerais
========================================
Gera as células do notebook referentes à seção 4.1 da monografia.

Outputs desta seção
--------------------
  Gráfico 1  — Funil de classificação dos processos (595 → Fase III → Indício/Certeza)
  Gráfico 2  — Composição percentual da amostra por categoria (barras empilhadas)
  Tabela 5   — Indicadores estatísticos: proporção, IC Wilson 95% e projeção
  Tabela 6   — Combinações das variáveis F3 entre os 233 processos da Fase III
  Gráfico 3  — Visualização das combinações F3 (barras horizontais)
  Gráfico 4  — Frequência absoluta das variáveis F3 isoladas
  Tabela 7   — Distribuição da classificação por ano (com IC Wilson)
  Gráfico 5  — Indício e certeza por ano (barras empilhadas)
  Tabela 8   — Indício e certeza por unidade judiciária (14 JECs)
  Gráfico 6  — Percentual por JEC com linha de média

Valores de referência (monografia, cap. 4)
-------------------------------------------
  Indício (incl. certeza) : 105/595 = 17,65%
  Certeza                 : 30/595  = 5,04%
  7º JEC (maior)          : 35,9%
  13º JEC (menor)         : 5,6%
  Média geral             : 17,6%

Seção da monografia: 4.1.1 a 4.1.5
"""

# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 1 — MARKDOWN: ABERTURA DO CAPÍTULO DE RESULTADOS
# ──────────────────────────────────────────────────────────────────────────────
md(r'''
---

## 5. Resultados Descritivos Gerais

Esta seção apresenta os achados descritivos da pesquisa, percorrendo o funil
de classificação dos 595 processos amostrados, as estimativas pontuais e
intervalares projetadas para a população, o detalhamento das combinações
das variáveis sistêmicas da Fase III e a distribuição do fenômeno por ano
de distribuição e por unidade judiciária.

> **Nota sobre dupla contagem:** os 30 processos classificados com *certeza*
> estão integralmente contidos nos 105 com *indício* (pois certeza implica
> as mesmas condições de indício, acrescidas de F3_18). As duas categorias
> **não devem ser somadas**; sempre que se reporta a prevalência do fenômeno
> em sentido amplo, usa-se o número de *indício* (105).
''')

# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 2 — CÓDIGO: CARREGAR DADOS E DEFINIR SUBCONJUNTOS
# ──────────────────────────────────────────────────────────────────────────────
code(r'''
# ── Recarregar o dataset curado (produzido pela Seção 2) ─────────────────────
# Necessário porque cada seção do notebook é autocontida após a execução.
import pandas as pd
import numpy as np
from pathlib import Path
from statsmodels.stats.proportion import proportion_confint, proportions_ztest

ARQUIVO_PKL = Path('dat/estcaso_lide_pred/processado/hadja_amostra_limpa.pkl')
dados = pd.read_pickle(ARQUIVO_PKL)

# ── Subconjuntos usados nesta seção ──────────────────────────────────────────
# Fase III: processos que avançaram com ao menos um indício na Fase II
dados_f3 = dados[dados['Avancou_F3']].copy()   # n = 233

# ── Parâmetros populacionais e amostrais ──────────────────────────────────────
N_AMST  = 595       # tamanho da amostra
N_POP   = 50_320    # população depurada (base consolidada)
ALPHA   = 0.05      # nível de significância para todos os IC

# ── Constantes de contagem (verificadas pelos asserts da Seção 2) ─────────────
N_EXCLUIDOS = int(dados['Excluido_F1'].sum())    # 151
N_FASE_II   = N_AMST - N_EXCLUIDOS              # 444
N_FASE_III  = int(dados['Avancou_F3'].sum())     # 233
N_SEM_IND   = N_FASE_II - N_FASE_III            # 211
N_INDICIO   = int(dados['Indicio'].sum())        # 105
N_CERTEZA   = int(dados['Certeza'].sum())        # 30
N_IND_ONLY  = N_INDICIO - N_CERTEZA             # 75 (indício sem certeza)
N_DEMAIS_F3 = N_FASE_III - N_INDICIO            # 128

# ── Verificação de partição ───────────────────────────────────────────────────
assert N_EXCLUIDOS + N_SEM_IND + N_DEMAIS_F3 + N_IND_ONLY + N_CERTEZA == N_AMST, \
    'Partição não fecha em 595!'

print('Partição dos 595 processos:')
for label, val in [
    ('Excluídos na Fase I',          N_EXCLUIDOS),
    ('Sem indicativo na Fase II',    N_SEM_IND),
    ('Demais processos na Fase III', N_DEMAIS_F3),
    ('Indício (sem certeza)',        N_IND_ONLY),
    ('Certeza',                      N_CERTEZA),
]:
    print(f'  {label:<40}: {val:>4}  ({val/N_AMST*100:.1f}%)')
print(f'  {"TOTAL":<40}: {N_AMST:>4}')
''')

# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 3 — MARKDOWN: SEÇÃO 4.1.1 — FLUXO DAS FASES
# ──────────────────────────────────────────────────────────────────────────────
md(r'''
### 5.1 Fluxo dos processos pelas três fases (Gráficos 1 e 2)

A metodologia em funil revela o afunilamento progressivo da amostra ao longo
das três fases de triagem. **151 processos (25,4%)** foram eliminados na
Fase I por não apresentarem as condições mínimas para análise de litigância
predatória pelo polo ativo. **211 processos (35,5%)** que avançaram à Fase II
não apresentaram nenhum dos indicativos de abusividade listados na Recomendação
CNJ n.º 159/2024, sendo encerrada ali a sua análise. Dos **233 processos
(39,2%)** que chegaram à Fase III, **105** preencheram o critério de indício
e **30** o critério de certeza.

O dado dos 211 processos que não apresentaram qualquer irregularidade na
Fase II é relevante do ponto de vista metodológico: ele corrobora a conjectura
presente na Recomendação n.º 159/2024, segundo a qual as demandas legítimas
— mesmo dentro do ecossistema dos juizados — não ostentam, em regra, os
marcadores formais de abusividade identificados nas variáveis F2.
''')

# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 4 — CÓDIGO: GRÁFICO 1 — FUNIL DE CLASSIFICAÇÃO
# ──────────────────────────────────────────────────────────────────────────────
code(r'''
# ── Gráfico 1: Funil de classificação dos processos ──────────────────────────
# Representa o afunilamento progressivo da amostra pelas três fases.
# Layout: barras horizontais decrescentes, com setas indicando o fluxo.

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker
import numpy as np

fig, ax = plt.subplots(figsize=(12, 6))
ax.set_axis_off()

# Definição dos estágios do funil
estagios = [
    # (rótulo, n, pct_sobre_595, cor, y_centro)
    ('Amostra total',            595,  100.0, '#2a78d6',  0.90),
    ('Avançaram à Fase II',      444,   74.6, '#9ec5f4',  0.70),
    ('Avançaram à Fase III\n(ao menos 1 indício na F2)',
                                 233,   39.2, '#eda100',  0.50),
    ('Indício de litigância\npredatória (F3_19+F3_20)',
                                 105,   17.6, '#eb6834',  0.30),
    ('Certeza de litigância\npredatória (F3_18+F3_19+F3_20)',
                                  30,    5.0, '#e34948',  0.10),
]

larguras = [s[1] / 595 for s in estagios]   # proporção de 0 a 1
L_MAX    = 0.82   # largura máxima do funil no plot (em unidades de axes)
X_CENTER = 0.50

for i, (label, n_val, pct, cor, y) in enumerate(estagios):
    larg  = larguras[i] * L_MAX
    x0    = X_CENTER - larg / 2
    # Barra horizontal
    rect = mpatches.FancyBboxPatch(
        (x0, y - 0.06), larg, 0.12,
        boxstyle='round,pad=0.005',
        facecolor=cor, edgecolor='white', linewidth=1.5,
        transform=ax.transAxes, clip_on=False,
    )
    ax.add_patch(rect)
    # Rótulo dentro da barra (esquerda)
    ax.text(x0 + 0.01, y, label,
            transform=ax.transAxes, va='center', ha='left',
            fontsize=9, color='white', fontweight='bold')
    # Contagem e percentual (direita)
    ax.text(x0 + larg - 0.01, y, f'n = {n_val:,}  ({pct:.1f}%)',
            transform=ax.transAxes, va='center', ha='right',
            fontsize=9, color='white', fontweight='bold')
    # Seta de fluxo entre estágios
    if i < len(estagios) - 1:
        ax.annotate('',
            xy=(X_CENTER, estagios[i+1][4] + 0.07),
            xytext=(X_CENTER, y - 0.07),
            xycoords='axes fraction', textcoords='axes fraction',
            arrowprops=dict(arrowstyle='->', color=TINTA_2, lw=1.5),
        )
    # Anotação lateral: excluídos ou "contido em"
    if i == 0:
        ax.text(X_CENTER + larguras[0]*L_MAX/2 + 0.03, y,
                f'← excluídos na F1: {N_EXCLUIDOS} ({N_EXCLUIDOS/595*100:.1f}%)',
                transform=ax.transAxes, va='center', ha='left',
                fontsize=8.5, color=TINTA_2, style='italic')
    if i == 1:
        ax.text(X_CENTER + larguras[1]*L_MAX/2 + 0.03, y,
                f'← sem indicativo na F2: {N_SEM_IND} ({N_SEM_IND/595*100:.1f}%)',
                transform=ax.transAxes, va='center', ha='left',
                fontsize=8.5, color=TINTA_2, style='italic')
    if i == 3:
        ax.text(X_CENTER + larguras[3]*L_MAX/2 + 0.03, y,
                f'← certeza contida no indício',
                transform=ax.transAxes, va='center', ha='left',
                fontsize=8.5, color=TINTA_2, style='italic')

ax.set_title(
    'Gráfico 1 – Funil de classificação dos processos da amostra (n = 595)\n'
    'Fonte: elaborada pela autora, a partir da aba AMOSTRA (2025).',
    fontsize=11, fontweight='bold', pad=12,
)
plt.tight_layout()
plt.show()
''')

# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 5 — CÓDIGO: GRÁFICO 2 — COMPOSIÇÃO PERCENTUAL DA AMOSTRA
# ──────────────────────────────────────────────────────────────────────────────
code(r'''
# ── Gráfico 2: Composição percentual da amostra por categoria ─────────────────
# Cinco categorias mutuamente exclusivas — sem dupla contagem.
# Layout: barra empilhada horizontal + gráfico de pizza lado a lado.

categorias = [
    ('Excluído na Fase I',          N_EXCLUIDOS, '#9ec5f4'),
    ('Sem indicativo na Fase II',   N_SEM_IND,   '#e4e3df'),
    ('Demais processos na Fase III',N_DEMAIS_F3, '#eda100'),
    ('Indício (sem certeza)',        N_IND_ONLY,  '#eb6834'),
    ('Certeza',                      N_CERTEZA,   '#e34948'),
]

rotulos  = [c[0] for c in categorias]
valores  = [c[1] for c in categorias]
cores    = [c[2] for c in categorias]
percents = [v / N_AMST * 100 for v in valores]

fig, axes = plt.subplots(1, 2, figsize=(14, 4.5))

# ── Painel esquerdo: barra empilhada horizontal ───────────────────────────
esq = 0.0
for rot, val, cor, pct in zip(rotulos, valores, cores, percents):
    axes[0].barh(0, pct, left=esq, color=cor,
                 edgecolor='white', linewidth=1.2, height=0.55)
    # Rótulo dentro da fatia (só se largura suficiente)
    if pct >= 4:
        axes[0].text(esq + pct / 2, 0,
                     f'{val}\n({pct:.1f}%)',
                     va='center', ha='center',
                     fontsize=9, color='white', fontweight='bold')
    esq += pct

axes[0].set_xlim(0, 100)
axes[0].set_yticks([])
axes[0].set_xlabel('% da amostra (n = 595)')
axes[0].set_title('Composição percentual da amostra\npor resultado da classificação',
                  fontsize=11)
axes[0].xaxis.set_major_formatter(mticker.PercentFormatter())

# Legenda abaixo do gráfico
handles = [mpatches.Patch(facecolor=c, label=r)
           for r, c in zip(rotulos, cores)]
axes[0].legend(handles=handles, loc='lower center',
               bbox_to_anchor=(0.5, -0.45),
               ncol=2, fontsize=8.5, frameon=False)

# ── Painel direito: pizza das 5 categorias ────────────────────────────────
wedge_props = dict(linewidth=1.2, edgecolor='white')
_, texts, autotexts = axes[1].pie(
    valores,
    labels=None,
    autopct=lambda p: f'{p:.1f}%' if p > 2 else '',
    colors=cores,
    wedgeprops=wedge_props,
    startangle=120,
    pctdistance=0.72,
)
for at in autotexts:
    at.set_fontsize(9)
    at.set_color('white')
    at.set_fontweight('bold')
axes[1].set_title('Gráfico 2 – Composição da amostra\nsegundo o desfecho da classificação',
                  fontsize=11)
axes[1].legend(handles=handles, loc='lower center',
               bbox_to_anchor=(0.5, -0.30),
               ncol=1, fontsize=8.5, frameon=False)

plt.suptitle(
    'Fonte: elaborada pela autora, a partir da aba AMOSTRA (2025).\n'
    'Nota: indício (sem certeza) e certeza são categorias mutuamente exclusivas.',
    fontsize=8.5, y=-0.04, color=TINTA_2,
)
plt.tight_layout()
plt.show()
''')

# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 6 — MARKDOWN: SEÇÃO 4.1.2 — ESTIMATIVAS PARA A POPULAÇÃO
# ──────────────────────────────────────────────────────────────────────────────
md(r'''
### 5.2 Estimativa pontual e intervalar para a população (Tabela 5)

A estimativa de prevalência do fenômeno na população é derivada diretamente
da proporção amostral, com intervalo de confiança calculado pelo **método
de Wilson** — mais adequado que o de Wald para proporções extremas e amostras
de tamanho moderado, pois não assume normalidade assintótica irrestrita.

O **indício de litigância predatória** em sentido amplo (incluindo os
processos com certeza) representa **17,65%** da amostra — IC 95% de
**[14,59%; 20,70%]** — o que, projetado sobre a população depurada,
equivale a uma estimativa de cerca de **8.880 processos** no triênio 2022–2024.

O **critério de certeza**, mais restritivo (três variáveis F3 positivadas
simultaneamente), aponta para **5,04%** da amostra — IC 95% de
**[3,29%; 6,79%]** — equivalendo a cerca de **2.537 processos**.

> **Importante:** as projeções populacionais devem ser interpretadas como
> estimativas de ordem de grandeza e não como contagens absolutas precisas.
> A magnitude dos números é, entretanto, relevante para a administração
> judiciária: mesmo na hipótese mais conservadora (certeza), estima-se
> número superior a **dois mil quinhentos** casos no período analisado.
''')

# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 7 — CÓDIGO: TABELA 5 — INDICADORES ESTATÍSTICOS
# ──────────────────────────────────────────────────────────────────────────────
code(r'''
# ── Tabela 5: Indicadores estatísticos da classificação (n = 595) ─────────────

linhas = []
for label, k in [('Indício (incl. certeza)', N_INDICIO), ('Certeza', N_CERTEZA)]:
    prop      = k / N_AMST
    li, ls    = proportion_confint(k, N_AMST, alpha=ALPHA, method='wilson')
    proj      = prop * N_POP
    proj_li   = li * N_POP
    proj_ls   = ls * N_POP
    linhas.append({
        'Classificação'          : label,
        'n (amostra)'            : k,
        'Proporção'              : prop,
        'IC 2,5% (Wilson)'       : li,
        'IC 97,5% (Wilson)'      : ls,
        'Projeção (população)'   : proj,
        'Proj. IC inf.'          : proj_li,
        'Proj. IC sup.'          : proj_ls,
    })

tab5 = pd.DataFrame(linhas)

# Validar contra valores publicados na monografia
assert abs(tab5.loc[0, 'Proporção'] - 0.1765) < 0.001, \
    f"Proporção indício: esperado ~17,65%; obtido {tab5.loc[0,'Proporção']*100:.2f}%"
assert abs(tab5.loc[1, 'Proporção'] - 0.0504) < 0.001, \
    f"Proporção certeza: esperado ~5,04%; obtido {tab5.loc[1,'Proporção']*100:.2f}%"
print('Asserts Tabela 5: OK')
print()

# Exibição estilizada
display(
    tab5.style
    .set_caption(
        'Tabela 5 – Indicadores estatísticos da classificação (n = 595) | '
        'Fonte: elaborada pela autora, a partir da aba AMOSTRA (2025).\n'
        'IC calculado pelo método de Wilson (95%). '
        f'Projeção sobre N = {N_POP:,} (base consolidada).'
    )
    .format({
        'n (amostra)'           : '{:,.0f}',
        'Proporção'             : '{:.2%}',
        'IC 2,5% (Wilson)'      : '{:.2%}',
        'IC 97,5% (Wilson)'     : '{:.2%}',
        'Projeção (população)'  : '{:,.0f}',
        'Proj. IC inf.'         : '{:,.0f}',
        'Proj. IC sup.'         : '{:,.0f}',
    })
    .set_table_styles([
        {'selector': 'caption',
         'props': [('font-size', '12px'), ('font-weight', 'bold'),
                   ('text-align', 'left'), ('caption-side', 'top')]},
        {'selector': 'th',
         'props': [('background-color', '#2a78d6'), ('color', 'white'),
                   ('font-size', '11px'), ('text-align', 'center')]},
        {'selector': 'td',
         'props': [('text-align', 'right'), ('font-size', '11px')]},
    ])
    .apply(lambda col: [
        'background-color: #fff3e0' if r == 0 else 'background-color: #fce8e8'
        for r in range(len(col))
    ])
    .hide(axis='index')
)
''')

# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 8 — MARKDOWN: SEÇÃO 4.1.3 — ANÁLISE DAS VARIÁVEIS F3
# ──────────────────────────────────────────────────────────────────────────────
md(r'''
### 5.3 Análise detalhada das variáveis da Fase III (Tabela 6, Gráficos 3 e 4)

Cinco achados se destacam na análise das combinações das variáveis F3
entre os **233 processos avaliados na Fase III**:

1. **Em quase metade (104 = 44,6%)**, nenhuma das três variáveis sistêmicas
   foi positivada — o que reforça que a presença de irregularidades formais
   na Fase II não é, por si só, indicativo de massificação.
2. A combinação **F3_19 + F3_20** (petições idênticas + volume elevado), sem
   F3_18, foi a configuração mais frequente entre os positivos: **75 processos**,
   confirmando que a marca mais comum do fenômeno é a articulação entre
   padronização e volume.
3. A **tríade completa** (F3_18 + F3_19 + F3_20), critério de *certeza*, foi
   observada em **30 processos** (12,9% dos 233).
4. A combinação **F3_18 + F3_19 sem F3_20** não foi observada em nenhum processo,
   sugerindo que a positivação de petições idênticas tende a vir acompanhada de
   elevado volume de demandas pelo mesmo advogado.
5. **24 processos** exibem combinações parciais que não atingem o limiar de
   indício (9 com apenas F3_18; 1 com apenas F3_19; 9 com apenas F3_20;
   2 com F3_18 + F3_20 sem F3_19). Esses casos podem representar lides
   com estratégia ainda em formação, ou litigância abusiva individual
   ainda não massificada.
''')

# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 9 — CÓDIGO: TABELA 6 + GRÁFICOS 3 E 4 — COMBINAÇÕES F3
# ──────────────────────────────────────────────────────────────────────────────
code(r'''
# ── Tabela 6: combinações das variáveis F3 entre os 233 da Fase III ───────────

# Calcular todas as combinações presentes nos dados
combos_raw = (
    dados_f3
    .groupby(['F3_18', 'F3_19', 'F3_20'])
    .size()
    .reset_index(name='n')
)

# Gerar as 8 combinações possíveis de três booleanos e fazer merge
from itertools import product as iter_prod
todas_combos = pd.DataFrame(
    list(iter_prod([False, True], repeat=3)),
    columns=['F3_18', 'F3_19', 'F3_20'],
)
tab6 = todas_combos.merge(combos_raw, on=['F3_18', 'F3_19', 'F3_20'], how='left')
tab6['n']   = tab6['n'].fillna(0).astype(int)
tab6['%']   = (tab6['n'] / N_FASE_III * 100).round(1)

# Rótulo legível da combinação
def rotulo_combo(row):
    partes = []
    for col in ['F3_18', 'F3_19', 'F3_20']:
        partes.append(col if row[col] else f'¬{col}')
    return ' ∧ '.join(partes)

tab6['Combinação'] = tab6.apply(rotulo_combo, axis=1)

# Classificação formal
def classif_combo(row):
    if row['F3_18'] and row['F3_19'] and row['F3_20']:
        return 'Certeza'
    if row['F3_19'] and row['F3_20']:
        return 'Indício'
    if row['n'] == 0:
        return 'Não observada'
    return 'Sem classificação'

tab6['Classificação'] = tab6.apply(classif_combo, axis=1)

# Ordenar: sem nenhuma → parciais → indício → certeza
ordem_sort = {'Não observada': 0, 'Sem classificação': 1, 'Indício': 2, 'Certeza': 3}
tab6['_ord'] = tab6['Classificação'].map(ordem_sort)
tab6 = tab6.sort_values(['_ord', 'n'], ascending=[True, False]).drop(columns='_ord')

# Verificação de fechamento
assert tab6['n'].sum() == N_FASE_III, \
    f'Combinações não somam 233: {tab6["n"].sum()}'
assert tab6.loc[tab6['Classificação'] == 'Indício', 'n'].sum() == N_IND_ONLY, \
    'Total de indício (sem certeza) diverge'
assert tab6.loc[tab6['Classificação'] == 'Certeza', 'n'].sum() == N_CERTEZA, \
    'Total de certeza diverge'
print('Asserts Tabela 6: OK')

# Exibição estilizada
COR_TAB = {
    'Certeza'          : '#fce8e8',
    'Indício'          : '#fff3e0',
    'Sem classificação': '#f5f5f5',
    'Não observada'    : '#fafafa',
}

display(
    tab6[['Combinação', 'n', '%', 'Classificação']].style
    .set_caption(
        'Tabela 6 – Combinações das variáveis F3 entre os 233 processos '
        'avaliados na Fase III | '
        'Fonte: elaborada pela autora, a partir da aba AMOSTRA (2025).\n'
        'Nota: percentuais calculados sobre os 233 processos da Fase III.'
    )
    .format({'n': '{:,.0f}', '%': '{:.1f}'})
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
        f'background-color: {COR_TAB.get(tab6.iloc[r]["Classificação"], "")}'
        for r in range(len(col))
    ])
    .hide(axis='index')
)
''')

# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 10 — CÓDIGO: GRÁFICO 3 — BARRAS DAS COMBINAÇÕES F3
# ──────────────────────────────────────────────────────────────────────────────
code(r'''
# ── Gráfico 3: combinações de variáveis F3 entre os 233 da Fase III ───────────
# Exibe apenas as combinações com n > 0, ordenadas por contagem.

tab6_plot = tab6[tab6['n'] > 0].sort_values('n', ascending=True)

cores_combo = {
    'Certeza'          : '#e34948',
    'Indício'          : '#eb6834',
    'Sem classificação': '#9ec5f4',
}

fig, ax = plt.subplots(figsize=(11, 4.5))
y = np.arange(len(tab6_plot))
barras = ax.barh(
    y,
    tab6_plot['n'],
    color=[cores_combo.get(c, GRADE) for c in tab6_plot['Classificação']],
    edgecolor='white', linewidth=0.8, height=0.65,
)
# Rótulos de valor
for barra, (_, row) in zip(barras, tab6_plot.iterrows()):
    ax.text(barra.get_width() + 1.5, barra.get_y() + barra.get_height() / 2,
            f'{int(row["n"])}  ({row["%"]:.1f}%)',
            va='center', ha='left', fontsize=9.5, color=TINTA)

ax.set_yticks(y)
ax.set_yticklabels(tab6_plot['Combinação'], fontsize=9)
ax.set_xlabel('Processos (n)')
ax.set_xlim(0, tab6_plot['n'].max() * 1.30)
ax.set_title(
    'Gráfico 3 – Combinações de variáveis F3 entre os 233 processos da Fase III\n'
    'Fonte: elaborada pela autora, a partir da aba AMOSTRA (2025).',
    fontsize=11, fontweight='bold',
)
ax.grid(axis='y', visible=False)

# Legenda
handles = [mpatches.Patch(facecolor=c, label=r)
           for r, c in cores_combo.items()]
ax.legend(handles=handles, loc='lower right', fontsize=9, frameon=False)
plt.tight_layout()
plt.show()
''')

# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 11 — CÓDIGO: GRÁFICO 4 — FREQUÊNCIA DAS VARIÁVEIS F3 ISOLADAS
# ──────────────────────────────────────────────────────────────────────────────
code(r'''
# ── Gráfico 4: frequência absoluta das variáveis F3 isoladas ──────────────────
# Exibe quantos processos (sobre os 595 totais) têm cada variável positivada.
# Evidencia o gap entre F3_20/F3_19 (~17-20%) e F3_18 (~7%).

f3_freq = pd.DataFrame({
    'Variável': ['F3_18\n(Multiplicidade de ações)', 'F3_19\n(Petições idênticas)',
                 'F3_20\n(Volume elevado de demandas)'],
    'n':        [int(dados['F3_18'].sum()), int(dados['F3_19'].sum()),
                 int(dados['F3_20'].sum())],
})
f3_freq['% (sobre 595)'] = f3_freq['n'] / N_AMST * 100
f3_freq['% (sobre 233)'] = f3_freq['n'] / N_FASE_III * 100

fig, axes = plt.subplots(1, 2, figsize=(13, 4))

# Painel esquerdo: frequência sobre os 595
cores_f3 = [CORES[1], CORES[2], CORES[0]]
barras_l = axes[0].bar(f3_freq['Variável'], f3_freq['n'],
                       color=cores_f3, alpha=0.88, width=0.55)
anotar_barras(axes[0], barras_l, formato='{:.0f}', fontsize=10)
axes[0].set_ylabel('Processos (n = 595)')
axes[0].set_title('Frequência absoluta\n(sobre os 595 processos da amostra)', fontsize=10.5)
axes[0].set_ylim(0, f3_freq['n'].max() * 1.28)

# Painel direito: frequência sobre os 233 da Fase III
barras_r = axes[1].bar(f3_freq['Variável'], f3_freq['% (sobre 233)'],
                       color=cores_f3, alpha=0.88, width=0.55)
anotar_barras(axes[1], barras_r,
              formato='{:.1f}%', fontsize=10)
axes[1].set_ylabel('% dos 233 processos da Fase III')
axes[1].set_title('Frequência relativa\n(sobre os 233 processos da Fase III)', fontsize=10.5)
axes[1].yaxis.set_major_formatter(mticker.PercentFormatter())
axes[1].set_ylim(0, f3_freq['% (sobre 233)'].max() * 1.28)

plt.suptitle(
    'Gráfico 4 – Frequência absoluta e relativa das variáveis da Fase III\n'
    'Fonte: elaborada pela autora, a partir da aba AMOSTRA (2025).',
    fontsize=11, fontweight='bold', y=1.02,
)
plt.tight_layout()
plt.show()
print(f'F3_18: {int(dados["F3_18"].sum())} processos | '
      f'F3_19: {int(dados["F3_19"].sum())} | '
      f'F3_20: {int(dados["F3_20"].sum())}')
''')

# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 12 — MARKDOWN: SEÇÃO 4.1.4 — INCIDÊNCIA POR ANO
# ──────────────────────────────────────────────────────────────────────────────
md(r'''
### 5.4 Incidência por ano de distribuição (Tabela 7, Gráfico 5)

A análise temporal revela uma aparente flutuação da incidência entre os
três anos: **2022** apresenta 18,0% de indício; **2023**, 19,9% (pico);
e **2024**, 14,7%. Contudo, conforme demonstrado na seção de testes
inferenciais (seção 7.1), essa variação **não é estatisticamente significativa**
(χ² = 1,87; gl = 2; p = 0,393), sendo atribuível à variabilidade amostral.

A queda observada em 2024 deve ser interpretada com cautela metodológica:
as variáveis sistêmicas da Fase III (especialmente F3_19 e F3_20) dependem
da observação de padrões acumulados no sistema PJe. Para processos distribuídos
em 2024, esse padrão pode estar ainda em formação à data da coleta
(março de 2026), comprimindo artificialmente a estimativa de incidência
para essa coorte.
''')

# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 13 — CÓDIGO: TABELA 7 + GRÁFICO 5 — POR ANO
# ──────────────────────────────────────────────────────────────────────────────
code(r'''
# ── Tabela 7: distribuição da classificação por ano ───────────────────────────

linhas_ano = []
for ano in [2022, 2023, 2024]:
    d  = dados[dados['ano'] == ano]
    n  = len(d)
    ni = int(d['Indicio'].sum())
    nc = int(d['Certeza'].sum())
    ns = ni - nc
    li_i, ls_i = proportion_confint(ni, n, alpha=ALPHA, method='wilson')
    li_c, ls_c = proportion_confint(nc, n, alpha=ALPHA, method='wilson')
    linhas_ano.append({
        'Ano'                  : ano,
        'n'                    : n,
        'Indício (incl. cert.)': ni,
        '% Indício'            : ni / n,
        'IC inf. Indício'      : li_i,
        'IC sup. Indício'      : ls_i,
        'Certeza'              : nc,
        '% Certeza'            : nc / n,
        'IC inf. Certeza'      : li_c,
        'IC sup. Certeza'      : ls_c,
        'Só Indício'           : ns,
    })

tab7 = pd.DataFrame(linhas_ano)

display(
    tab7.style
    .set_caption(
        'Tabela 7 – Distribuição da classificação por ano | '
        'Fonte: elaborada pela autora, a partir da aba AMOSTRA (2025).\n'
        'Nota: percentuais calculados sobre o total anual. '
        'IC Wilson 95%. Indício inclui certeza.'
    )
    .format({
        'n'                    : '{:,.0f}',
        'Indício (incl. cert.)': '{:,.0f}',
        '% Indício'            : '{:.1%}',
        'IC inf. Indício'      : '{:.1%}',
        'IC sup. Indício'      : '{:.1%}',
        'Certeza'              : '{:,.0f}',
        '% Certeza'            : '{:.1%}',
        'IC inf. Certeza'      : '{:.1%}',
        'IC sup. Certeza'      : '{:.1%}',
        'Só Indício'           : '{:,.0f}',
    })
    .set_table_styles([
        {'selector': 'caption',
         'props': [('font-size', '12px'), ('font-weight', 'bold'),
                   ('text-align', 'left'), ('caption-side', 'top')]},
        {'selector': 'th',
         'props': [('background-color', '#2a78d6'), ('color', 'white'),
                   ('font-size', '11px'), ('text-align', 'center')]},
        {'selector': 'td',
         'props': [('text-align', 'center'), ('font-size', '11px')]},
    ])
    .apply(lambda col: [
        'background-color: #eef3fc' if r % 2 == 0 else ''
        for r in range(len(col))
    ])
    .hide(axis='index')
)

# ── Gráfico 5: Indício e certeza por ano ──────────────────────────────────────
fig, ax = plt.subplots(figsize=(9, 5))

anos_lab = ['2022', '2023', '2024']
x        = np.arange(3)
larg     = 0.32

# Barras: Só Indício (empilhado abaixo da Certeza)
bars_si = ax.bar(x - larg/2, tab7['Só Indício'] / tab7['n'] * 100,
                 larg, label='Indício (sem certeza)',
                 color=CORES[1], alpha=0.88)
bars_ce = ax.bar(x + larg/2, tab7['% Certeza'] * 100,
                 larg, label='Certeza',
                 color=CORES[7], alpha=0.88)

# Barras de erro (IC Wilson) para Indício total
for i, row in tab7.iterrows():
    pct_i  = row['% Indício'] * 100
    err_lo = pct_i - row['IC inf. Indício'] * 100
    err_hi = row['IC sup. Indício'] * 100 - pct_i
    ax.errorbar(i - larg/2, pct_i,
                yerr=[[err_lo], [err_hi]],
                fmt='none', color=TINTA, capsize=5, linewidth=1.5, zorder=5)

anotar_barras(ax, bars_si, formato='{:.1f}%', fontsize=9)
anotar_barras(ax, bars_ce, formato='{:.1f}%', fontsize=9)

ax.set_xticks(x)
ax.set_xticklabels([f'{a}\n(n = {tab7.iloc[i]["n"]})' for i, a in enumerate(anos_lab)])
ax.set_ylabel('% da sub-amostra anual')
ax.yaxis.set_major_formatter(mticker.PercentFormatter())
ax.set_ylim(0, max(tab7['% Indício'].max() * 100, tab7['% Certeza'].max() * 100) * 1.45)
ax.legend(fontsize=10, loc='upper right')
ax.set_title(
    'Gráfico 5 – Indício e certeza de litigância predatória por ano\n'
    'Barras de erro: IC Wilson 95% para indício (incl. certeza)\n'
    'Fonte: elaborada pela autora, a partir da aba AMOSTRA (2025).',
    fontsize=11, fontweight='bold',
)
plt.tight_layout()
plt.show()
''')

# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 14 — MARKDOWN: SEÇÃO 4.1.5 — INCIDÊNCIA POR UNIDADE
# ──────────────────────────────────────────────────────────────────────────────
md(r'''
### 5.5 Incidência por unidade judiciária (Tabela 8, Gráfico 6)

A análise por unidade revela **variabilidade relevante** entre os 14 Juizados.
A média geral é de **17,6%** (indício + certeza), mas a faixa de variação
é ampla: de **5,6%** no 13º JEC a **35,9%** no 7º JEC.

O **7º JEC** apresenta a maior incidência observada (35,9%), com destaque
para a proporção de certeza (12,8% — mais que o dobro da média geral de 5,0%).
As comparações pareadas (seção 7.2) confirmam que essa diferença é
**estatisticamente significativa** (p < 0,001 vs. os demais JECs agrupados).

Sete unidades apresentam percentuais acima da média geral: 1º, 2º, 4º,
5º, 7º, 8º e 14º JEC, sugerindo distribuição heterogênea do fenômeno.
Como a distribuição processual é aleatorizada pelo sistema PJe, não é
possível atribuir esse padrão a direcionamento intencional das demandas,
demandando investigação adicional com dados complementares.
''')

# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 15 — CÓDIGO: TABELA 8 + GRÁFICO 6 — POR UNIDADE
# ──────────────────────────────────────────────────────────────────────────────
code(r'''
# ── Tabela 8: indício e certeza por unidade judiciária ────────────────────────

linhas_jec = []
for j in range(1, 15):
    d  = dados[dados['JEC_numero'] == j]
    n  = len(d)
    ni = int(d['Indicio'].sum())
    nc = int(d['Certeza'].sum())
    ns = ni - nc
    linhas_jec.append({
        'JEC'                  : f'{j}º JEC',
        'n'                    : n,
        'Indício (sem cert.)'  : ns,
        'Certeza'              : nc,
        'Total c/ indício'     : ni,
        '% Indício'            : ni / n,
        '% Certeza'            : nc / n,
    })

tab8 = pd.DataFrame(linhas_jec)

# Verificação dos valores-âncora da monografia
assert tab8.loc[tab8['JEC'] == '7º JEC', '% Indício'].values[0] > 0.35, \
    '7º JEC deveria ter >35% de indício'
assert tab8.loc[tab8['JEC'] == '13º JEC', 'Certeza'].values[0] == 0, \
    '13º JEC deveria ter Certeza = 0'
print('Asserts Tabela 8: OK')
print(f'Média geral % Indício: {tab8["% Indício"].mean()*100:.2f}%')

display(
    tab8.style
    .set_caption(
        'Tabela 8 – Indício e certeza de litigância predatória por unidade '
        'judiciária (n = 595) | '
        'Fonte: elaborada pela autora, a partir da aba AMOSTRA (2025).\n'
        'Nota: a coluna "Indício (sem cert.)" exclui os processos de certeza '
        'para evitar dupla contagem.'
    )
    .format({
        'n'                  : '{:,.0f}',
        'Indício (sem cert.)': '{:,.0f}',
        'Certeza'            : '{:,.0f}',
        'Total c/ indício'   : '{:,.0f}',
        '% Indício'          : '{:.1%}',
        '% Certeza'          : '{:.1%}',
    })
    .set_table_styles([
        {'selector': 'caption',
         'props': [('font-size', '12px'), ('font-weight', 'bold'),
                   ('text-align', 'left'), ('caption-side', 'top')]},
        {'selector': 'th',
         'props': [('background-color', '#2a78d6'), ('color', 'white'),
                   ('font-size', '11px'), ('text-align', 'center')]},
        {'selector': 'td',
         'props': [('text-align', 'center'), ('font-size', '11px')]},
    ])
    .apply(lambda col: [
        'background-color: #eef3fc' if r % 2 == 0 else ''
        for r in range(len(col))
    ])
    .bar(subset=['% Indício', '% Certeza'],
         color=[COR_PRINCIPAL, COR_DESTAQUE], vmin=0, vmax=0.40)
    .hide(axis='index')
)

# ── Gráfico 6: Percentual de indício e certeza por JEC ────────────────────────
MEDIA_IND = tab8['% Indício'].mean()

fig, ax = plt.subplots(figsize=(13, 6))
x    = np.arange(1, 15)
larg = 0.36

# Barras: Só Indício (base) e Certeza (acima)
pct_si = (tab8['Indício (sem cert.)'] / tab8['n']).values * 100
pct_ce = tab8['% Certeza'].values * 100

bars_si = ax.bar(x - larg/2, pct_si, larg,
                 label='Indício (sem certeza)', color=CORES[1], alpha=0.88)
bars_ce = ax.bar(x + larg/2, pct_ce, larg,
                 label='Certeza', color=CORES[7], alpha=0.88)

# Linha de média geral
ax.axhline(MEDIA_IND * 100, color=TINTA, linewidth=1.5,
           linestyle='--', label=f'Média geral: {MEDIA_IND*100:.1f}%', zorder=5)

# Rótulos nas barras
for barra in list(bars_si) + list(bars_ce):
    h = barra.get_height()
    if h >= 1.5:
        ax.text(barra.get_x() + barra.get_width() / 2, h + 0.4,
                f'{h:.1f}%', ha='center', va='bottom',
                fontsize=7.5, color=TINTA)

# Destacar 7º e 13º JEC com fundo
for j_dest, cor_dest in [(7, '#fff3cd'), (13, '#d4edda')]:
    ax.axvspan(j_dest - 0.55, j_dest + 0.55, alpha=0.18,
               color=cor_dest, zorder=0)

ax.set_xticks(x)
ax.set_xticklabels(
    [f'{j}º\n(n={tab8.iloc[j-1]["n"]})' for j in range(1, 15)],
    fontsize=8.5,
)
ax.set_xlabel('Unidade Judiciária (JEC nº)')
ax.set_ylabel('% da sub-amostra da unidade')
ax.yaxis.set_major_formatter(mticker.PercentFormatter())
ax.set_ylim(0, max(pct_si + pct_ce) * 1.35)
ax.legend(fontsize=9.5, loc='upper right')
ax.set_title(
    'Gráfico 6 – Percentual de indício e certeza por unidade judiciária\n'
    'Linha tracejada: média geral (17,6%) | '
    'Fonte: elaborada pela autora, a partir da aba AMOSTRA (2025).',
    fontsize=11, fontweight='bold',
)
plt.tight_layout()
plt.show()
''')

# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 16 — MARKDOWN: INTERPRETAÇÃO E LIMITAÇÕES
# ──────────────────────────────────────────────────────────────────────────────
md(r'''
### 5.6 Síntese dos achados descritivos

A análise descritiva revela um fenômeno de **relevo sistêmico**: mesmo na
hipótese mais conservadora (certeza, com três variáveis F3 positivadas
simultaneamente), estima-se que **mais de 2.500 processos** no triênio
2022–2024 nos 14 JECs de Natal possam ser classificados como litigância
predatória. Na hipótese de indício em sentido amplo, esse número pode superar
**8.800 processos**.

Do ponto de vista temporal, a incidência mostrou-se **estável** ao longo
do triênio — a variação entre os anos não atingiu significância estatística
—, afastando a hipótese de que o fenômeno seja transitório ou esteja em
declínio espontâneo no período.

Do ponto de vista espacial, a **heterogeneidade entre os JECs** é digna de
atenção: o 7º JEC concentra incidência quase o dobro da média geral, enquanto
o 13º JEC apresenta a menor incidência observada. Investigar as causas dessa
assimetria — composição da carteira, padrões de distribuição, concentração
de advogados específicos — é passo metodológico relevante para pesquisas futuras.

**Limitações:** as estimativas populacionais pressupõem que a amostra é
representativa da população depurada (50.320 processos). Eventuais vieses
de seleção não detectados — como a eventual concentração dos advogados
predatórios em períodos ou unidades específicos — poderiam afetar a
generalização dos resultados. Adicionalmente, a coorte de 2024 pode estar
subestimada em função da imaturidade dos padrões sistêmicos no PJe à época
da coleta.
''')
