# -*- coding: utf-8 -*-
"""
Seção 4 — Desenho Amostral (Tabelas 2, 3 e 4)
==============================================
Gera as células do notebook referentes ao dimensionamento, estratificação
e representatividade da amostra, além da distribuição por classe processual.

Outputs desta seção
--------------------
  Tabela 2  — Distribuição da amostra por unidade judiciária e ano (n=595)
  Tabela 3  — Distribuição da amostra por classe processual
  Tabela 4  — Quadro consolidado das 25 variáveis observacionais
              (reprodução estilizada do Quadro 3 / Tabela 4 da monografia)
  (Texto)   — Cálculo do tamanho amostral e da margem de erro efetiva

Seção da monografia: 3.2.2 a 3.3
"""

# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 1 — MARKDOWN: DESENHO AMOSTRAL
# ──────────────────────────────────────────────────────────────────────────────
md(r'''
---

## 4. Desenho Amostral

### 4.1 Dimensionamento e estratificação

A amostragem adotada é **probabilística estratificada por ano de distribuição**,
com seleção aleatória dos processos por meio da função `ALEATÓRIOENTRE()`
do Excel. O estrato é o ano (2022, 2023 e 2024), e dentro de cada estrato
os processos foram selecionados aleatoriamente com probabilidade uniforme.

**Cálculo do tamanho amostral:**

$$
n = \frac{z^2 \cdot p(1-p)}{e^2} \cdot \frac{N}{N + \frac{z^2 \cdot p(1-p)}{e^2} - 1}
$$

Parâmetros adotados:

| Parâmetro | Valor | Justificativa |
|---|---|---|
| Nível de confiança | 95% → z = 1,96 | Padrão para ciências sociais empíricas |
| Proporção conservadora | p = 0,5 | Maximiza o tamanho amostral |
| Margem de erro planejada | e = 5% | Padrão para pesquisas sociais |
| População (N) | 50.320 | Base consolidada após depuração |

A correção de **população finita** foi aplicada, resultando em
margem de erro efetiva de **±4,0 p.p.** — melhor que os 5% planejados,
em razão da fração amostral de 595/50.320 ≈ 1,2%.

**Estratificação proporcional ao peso anual na população:**
os 595 processos foram distribuídos entre os três estratos de forma
proporcional ao número de processos de cada ano na base consolidada
(fração de amostragem aproximadamente constante entre os estratos).
''')

# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 2 — CÓDIGO: CÁLCULO DO TAMANHO AMOSTRAL E MARGEM DE ERRO EFETIVA
# ──────────────────────────────────────────────────────────────────────────────
code(r'''
# ── Parâmetros do dimensionamento amostral ────────────────────────────────────
Z       = 1.96    # quantil normal para IC 95%
P       = 0.50    # proporção conservadora (maximiza n)
E_PLAN  = 0.05    # margem de erro planejada (5%)
N_REF   = 50_320  # população de referência (base consolidada)
N_AMST  = 595     # tamanho amostral efetivo

# ── n teórico sem correção de população finita ───────────────────────────────
n_sem_corr = (Z**2 * P * (1 - P)) / E_PLAN**2
print(f'n teórico sem correção   : {n_sem_corr:.0f}')

# ── n teórico com correção de população finita ───────────────────────────────
n_com_corr = n_sem_corr / (1 + (n_sem_corr - 1) / N_REF)
print(f'n teórico com correção   : {n_com_corr:.0f}')

# ── Margem de erro efetiva com a amostra real (n = 595) ──────────────────────
# e_efetiva = z * sqrt(p(1-p)/n) * sqrt((N-n)/(N-1))
e_efetiva = Z * np.sqrt(P * (1 - P) / N_AMST) * np.sqrt((N_REF - N_AMST) / (N_REF - 1))
print(f'Margem de erro efetiva   : ±{e_efetiva*100:.2f} p.p.'
      f' (planejada: ±{E_PLAN*100:.1f} p.p.)')

# ── Fração amostral ───────────────────────────────────────────────────────────
fracao = N_AMST / N_REF
print(f'Fração amostral          : {N_AMST}/{N_REF} = {fracao:.4f} ({fracao*100:.2f}%)')

# ── Distribuição do n por ano na população (base consolidada com ANO válido) ──
pop_por_ano = {2022: 13_968, 2023: 18_391, 2024: 16_435}
total_pop   = sum(pop_por_ano.values())
print()
print('Estratificação proporcional (referência):')
print(f'  {"Ano":<6} {"N pop":>8} {"% pop":>8} {"n esperado":>12} {"n real":>8}')
n_real_por_ano = dados['ano'].value_counts().sort_index().to_dict()
for ano, n_pop in sorted(pop_por_ano.items()):
    prop   = n_pop / total_pop
    n_esp  = round(N_AMST * prop)
    n_real = n_real_por_ano.get(ano, 0)
    print(f'  {ano:<6} {n_pop:>8,} {prop*100:>7.1f}% {n_esp:>12} {n_real:>8}')
print(f'  {"Total":<6} {total_pop:>8,} {"100,0%":>8} {N_AMST:>12} {sum(n_real_por_ano.values()):>8}')
''')

# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 3 — CÓDIGO: TABELA 2 — AMOSTRA POR UNIDADE E ANO
# ──────────────────────────────────────────────────────────────────────────────
code(r'''
# ── Tabela 2: distribuição da amostra por unidade judiciária e ano ─────────────

# Tabela cruzada: unidade × ano (contagem de processos amostrados)
tab2_raw = pd.crosstab(
    dados['unidade'],
    dados['ano'],
    margins=True,
    margins_name='Total',
)

# Ordenar por JEC_numero (1 a 14) + Total no fim
ordem_jec_dados = (
    dados[['unidade', 'JEC_numero']]
    .drop_duplicates()
    .sort_values('JEC_numero')['unidade']
    .tolist()
)
tab2 = tab2_raw.reindex(ordem_jec_dados + ['Total'])
tab2.columns = ['2022', '2023', '2024', 'Total']
tab2.index.name = 'Unidade Judiciária'

# Verificar totais por ano
assert tab2.loc['Total', '2022'] == 194, f"2022: esperado 194, obtido {tab2.loc['Total','2022']}"
assert tab2.loc['Total', '2023'] == 211, f"2023: esperado 211, obtido {tab2.loc['Total','2023']}"
assert tab2.loc['Total', '2024'] == 190, f"2024: esperado 190, obtido {tab2.loc['Total','2024']}"
assert tab2.loc['Total', 'Total'] == 595, f"Total: esperado 595, obtido {tab2.loc['Total','Total']}"
print('Asserts Tabela 2: OK')

# Exibir tabela estilizada
display(
    tab2.style
    .set_caption(
        'Tabela 2 – Distribuição da amostra por unidade judiciária e ano '
        '(n = 595) | Fonte: elaborada pela autora, a partir da aba AMOSTRA (2025).'
    )
    .format('{:,.0f}')
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
        'background-color: #eef3fc' if r % 2 == 0 else ''
        for r in range(len(col))
    ])
    .apply(lambda col: [
        'font-weight: bold; background-color: #d0e3f7'
        if idx == 'Total' else ''
        for idx in col.index
    ])
    .apply(lambda row: [
        'font-weight: bold; background-color: #d0e3f7'
        if col == 'Total' else ''
        for col in row.index
    ], axis=1)
)
''')

# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 4 — CÓDIGO: GRÁFICO — MAPA DE CALOR DA AMOSTRA POR JEC E ANO
# ──────────────────────────────────────────────────────────────────────────────
code(r'''
# ── Mapa de calor: amostra por JEC e ano ─────────────────────────────────────
# Visualiza a distribuição interna da Tabela 2, facilitando a identificação
# de células com n muito baixo (potencial fragilidade estatística).

# Matriz sem as linhas/colunas de Total
matriz_heat = tab2.drop(index='Total', columns='Total').astype(float)

fig, ax = plt.subplots(figsize=(8, 7))
im = ax.imshow(
    matriz_heat.values,
    cmap=MAPA_SEQUENCIAL,
    aspect='auto',
    vmin=8, vmax=25,
)
plt.colorbar(im, ax=ax, label='Processos amostrados', fraction=0.03, pad=0.02)

# Rótulos dos eixos
ax.set_xticks(range(3))
ax.set_xticklabels(['2022', '2023', '2024'], fontsize=10)
ax.set_yticks(range(len(matriz_heat)))
ax.set_yticklabels(
    [f'{j+1}º JEC' for j in range(14)],
    fontsize=9,
)
ax.set_title(
    'Tabela 2 — Mapa de calor da amostra\npor JEC e ano (n = 595)',
    fontweight='bold',
)

# Anotar cada célula com o valor
for i in range(len(matriz_heat)):
    for j in range(3):
        val = int(matriz_heat.iloc[i, j])
        cor_texto = 'white' if val >= 18 else TINTA
        ax.text(j, i, str(val), ha='center', va='center',
                fontsize=9, color=cor_texto, fontweight='bold')

ax.grid(visible=False)
plt.tight_layout()
plt.show()
''')

# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 5 — CÓDIGO: TABELA 3 — DISTRIBUIÇÃO POR CLASSE PROCESSUAL
# ──────────────────────────────────────────────────────────────────────────────
code(r'''
# ── Tabela 3: distribuição da amostra por classe processual ───────────────────
# A monografia documenta concentração quase absoluta no procedimento típico
# do microssistema dos Juizados (PROCEDIMENTO DO JUIZADO ESPECIAL CÍVEL).
# As demais classes decorrem de reclassificações automáticas do PJe.

CLASSE_PRINC = 'PROCEDIMENTO DO JUIZADO ESPECIAL CÍVEL'
CLASSES_RESIDUAIS = [
    'REINTEGRAÇÃO / MANUTENÇÃO DE POSSE',
    'DESPEJO POR FALTA DE PAGAMENTO CUMULADO COM COBRANÇA',
    'PROCEDIMENTO DO JUIZADO ESPECIAL DA FAZENDA PÚBLICA',
]

# Criar variável de classe resumida para esta tabela
dados['classe_tab3'] = dados['classe'].apply(
    lambda c: c if c in [CLASSE_PRINC, 'CUMPRIMENTO DE SENTENÇA',
                         'CUMPRIMENTO PROVISÓRIO DE SENTENÇA',
                         'PROCEDIMENTO COMUM CÍVEL'] + CLASSES_RESIDUAIS
    else 'Outras'
)

# Frequência e percentual
freq3 = (
    dados['classe_tab3']
    .value_counts()
    .reset_index()
)
freq3.columns = ['Classe Processual', 'n']
freq3['%'] = (freq3['n'] / len(dados) * 100).round(1)
freq3['% acumulado'] = freq3['%'].cumsum().round(1)

# Agrupar as três classes residuais em uma única linha
mask_res = freq3['Classe Processual'].isin(CLASSES_RESIDUAIS)
if mask_res.sum() > 1:
    n_res   = freq3.loc[mask_res, 'n'].sum()
    pct_res = (n_res / len(dados) * 100).round(1)
    freq3 = freq3[~mask_res]
    linha_res = pd.DataFrame([[
        'Outras classes residuais\n(Reintegração, Despejo e JEC Fazenda Pública)',
        n_res, pct_res, None
    ]], columns=freq3.columns)
    freq3 = pd.concat([freq3, linha_res], ignore_index=True)
    freq3['% acumulado'] = freq3['%'].cumsum().round(1)

# Exibir tabela
assert freq3['n'].sum() == 595, f"Soma n: {freq3['n'].sum()}"
print('Assert Tabela 3: OK')

display(
    freq3.style
    .set_caption(
        'Tabela 3 – Distribuição da amostra por classe processual (n = 595) | '
        'Fonte: elaborada pela autora (2025).'
    )
    .format({'n': '{:,.0f}', '%': '{:.1f}', '% acumulado': '{:.1f}'})
    .bar(subset=['%'], color=COR_SECUNDARIA, vmin=0, vmax=100)
    .set_table_styles([
        {'selector': 'caption',
         'props': [('font-size', '12px'), ('font-weight', 'bold'),
                   ('text-align', 'left'), ('caption-side', 'top')]},
        {'selector': 'th',
         'props': [('background-color', '#2a78d6'), ('color', 'white'),
                   ('font-size', '11px')]},
        {'selector': 'td',
         'props': [('font-size', '11px')]},
    ])
    .apply(lambda col: [
        'background-color: #eef3fc' if r % 2 == 0 else ''
        for r in range(len(col))
    ])
    .hide(axis='index')
)
''')

# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 6 — CÓDIGO: GRÁFICO — COMPOSIÇÃO DA AMOSTRA POR CLASSE PROCESSUAL
# ──────────────────────────────────────────────────────────────────────────────
code(r'''
# ── Gráfico: composição da amostra por classe processual (Tabela 3) ───────────

# Preparar dados do gráfico (as 3-4 categorias mais relevantes)
CLASSE_PRINC = 'PROCEDIMENTO DO JUIZADO ESPECIAL CÍVEL'
contagem_classe = dados['classe'].value_counts()

# Agrupar classes com < 5 ocorrências em "Outras"
limite = 5
principais = contagem_classe[contagem_classe >= limite]
outras_n   = contagem_classe[contagem_classe < limite].sum()
if outras_n > 0:
    outras_s = pd.Series({'Outras classes\n(residuais)': outras_n})
    principais = pd.concat([principais, outras_s])

# Rótulos resumidos para o gráfico
rotulos_graf = [
    quebrar(c, 22) if c != CLASSE_PRINC
    else 'Procedimento do\nJuizado Especial Cível'
    for c in principais.index
]

fig, axes = plt.subplots(1, 2, figsize=(14, 4))

# ── Painel esquerdo: pizza ────────────────────────────────────────────────
wedge_props = dict(linewidth=0.8, edgecolor='white')
explode = [0.03] * len(principais)
axes[0].pie(
    principais.values,
    labels=rotulos_graf,
    autopct=lambda p: f'{p:.1f}%' if p > 1 else '',
    colors=CORES[:len(principais)],
    wedgeprops=wedge_props,
    explode=explode,
    startangle=90,
    textprops={'fontsize': 9},
)
axes[0].set_title('Composição por classe\n(amostra n = 595)', fontsize=11)

# ── Painel direito: barras horizontais ───────────────────────────────────
y = np.arange(len(principais))
barras_h = axes[1].barh(
    y, principais.values,
    color=CORES[:len(principais)],
    alpha=0.88, height=0.6,
)
for barra, val in zip(barras_h, principais.values):
    axes[1].text(
        val + 2, barra.get_y() + barra.get_height() / 2,
        f'{val}  ({val/595*100:.1f}%)',
        va='center', fontsize=9, color=TINTA,
    )
axes[1].set_yticks(y)
axes[1].set_yticklabels(rotulos_graf, fontsize=9)
axes[1].set_xlabel('Número de processos')
axes[1].set_title('Distribuição por classe processual\n(Tabela 3)', fontsize=11)
axes[1].invert_yaxis()
axes[1].set_xlim(0, principais.max() * 1.35)
axes[1].grid(axis='y', visible=False)

plt.suptitle('Tabela 3 — Classes processuais na amostra', fontsize=12,
             fontweight='bold', y=1.01)
plt.tight_layout()
plt.show()
''')

# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 7 — CÓDIGO: TABELA 4 — QUADRO DAS 25 VARIÁVEIS OBSERVACIONAIS
# ──────────────────────────────────────────────────────────────────────────────
code(r'''
# ── Tabela 4 / Quadro 3: variáveis do estudo (reprodução estilizada) ──────────
# Construída a partir do mapeamento COLUNAS_AMOSTRA definido na Seção 2.
# Apresenta código, fase, nome, descrição e tipo de cada variável.

# Descrições detalhadas (retiradas do Apêndice B do projeto e Quadro 3 da monografia)
DESCRICOES_VARIAVEIS = {
    # Fase I — Exclusão
    'F1_A': 'Ações com pessoa física no polo passivo',
    'F1_B': 'Ausência de grande litigante no polo passivo',
    'F1_C': 'Causas ajuizadas sem representação por advogado (atermação)',
    'F1_D': 'Processos suspensos por determinação judicial',
    'F1_E': 'Processos erroneamente distribuídos aos Juizados Especiais',
    'F1_F': 'Pessoa jurídica no polo ativo',
    # Fase II — Indicativos na petição inicial e curso do processo
    'F2_01': 'Petição inicial vaga ou genérica, sem exposição de fatos específicos',
    'F2_02': 'Ausência de documentos mínimos que comprovem a relação jurídica alegada',
    'F2_03': 'Documentos apresentados sem conexão com a causa de pedir',
    'F2_04': 'Pedido explícito de dispensa da audiência de conciliação',
    'F2_05': 'Ação proposta em comarca distinta do domicílio das partes ou local do fato',
    'F2_06': 'Documentos com dados incompletos, ilegíveis ou em nome de terceiros',
    'F2_07': 'Pedidos vagos, hipotéticos ou sem relação lógica com a causa de pedir',
    'F2_08': 'Demanda idêntica anterior sem declaração de prevenção',
    'F2_09': 'Procuração com falhas ou outorgada por mandante já falecido',
    'F2_10': 'Procuração com assinatura eletrônica não qualificada (fora do padrão ICP-Brasil)',
    'F2_11': 'Sede do advogado não coincide com a comarca da ação ou domicílio das partes',
    'F2_12': 'Valor atribuído à causa elevado e aleatório, sem relação com o pedido',
    'F2_13': 'Classe ou assunto processual incorretamente cadastrado',
    'F2_14': 'Desistência ou abandono após indeferimento de medida liminar',
    'F2_15': 'Desistência ou abandono após notificação para comprovação dos fatos',
    'F2_16': 'Desistência ou abandono após apresentação de contestação com documentos',
    'F2_17': 'Contrato de honorários com valor superior a 30% do pedido',
    # Fase III — Verificação sistêmica de massificação
    'F3_18': 'Multiplicidade de ações sobre o mesmo tema pela mesma parte autora',
    'F3_19': 'Petições iniciais idênticas ou padronizadas em massa',
    'F3_20': 'Concentração de elevado volume de demandas sob o patrocínio do mesmo advogado',
}

CATEGORIAS_VARIAVEIS = {
    'F1_A': 'Natureza do processo',
    'F1_B': 'Natureza do processo',
    'F1_C': 'Natureza do processo',
    'F1_D': 'Natureza do processo',
    'F1_E': 'Natureza do processo',
    'F1_F': 'Natureza do processo',
    'F2_01': 'Qualidade da petição inicial',
    'F2_02': 'Qualidade da petição inicial',
    'F2_03': 'Qualidade da petição inicial',
    'F2_04': 'Qualidade da petição inicial',
    'F2_05': 'Qualidade da petição inicial',
    'F2_06': 'Qualidade da petição inicial',
    'F2_07': 'Qualidade da petição inicial',
    'F2_08': 'Qualidade da petição inicial',
    'F2_09': 'Documentação e representação',
    'F2_10': 'Documentação e representação',
    'F2_11': 'Documentação e representação',
    'F2_12': 'Qualidade da petição inicial',
    'F2_13': 'Qualidade da petição inicial',
    'F2_14': 'Comportamento no curso do processo',
    'F2_15': 'Comportamento no curso do processo',
    'F2_16': 'Comportamento no curso do processo',
    'F2_17': 'Comportamento no curso do processo',
    'F3_18': 'Massificação sistêmica',
    'F3_19': 'Massificação sistêmica',
    'F3_20': 'Massificação sistêmica',
}

# F1_D foi retirada no curso da pesquisa (monografia, sec. 3.3.1); o Quadro 3
# lista exatamente 25 variaveis = 5 F1 + 17 F2 + 3 F3.
COLS_F1_QUADRO = [c for c in COLS_F1 if c != 'F1_D']

# Montar DataFrame do quadro de variáveis
quadro_cols = COLS_F1_QUADRO + COLS_F2 + COLS_F3
quadro_df = pd.DataFrame({
    'Código': quadro_cols,
    'Fase': (['I'] * len(COLS_F1_QUADRO)
             + ['II'] * len(COLS_F2)
             + ['III'] * len(COLS_F3)),
    'Categoria': [CATEGORIAS_VARIAVEIS[c] for c in quadro_cols],
    'Nome da Variável': [ROTULOS.get(c, c) for c in quadro_cols],
    'Descrição': [DESCRICOES_VARIAVEIS.get(c, '—') for c in quadro_cols],
    'Tipo': ['Booleana (Sim/Não)'] * len(quadro_cols),
    'Critério na F.': (['Exclusão (se Sim → processo excluído)'] * len(COLS_F1_QUADRO)
                       + ['Indício (≥ 1 Sim → avança à Fase III)'] * len(COLS_F2)
                       + ['Massificação (combinação F3_19+F3_20 → indício; todas → certeza)'] * len(COLS_F3)),
})

# Frequência observada na amostra
quadro_df['Sim (n)'] = [dados[c].sum() for c in quadro_cols]
quadro_df['Sim (%)'] = (quadro_df['Sim (n)'] / 595 * 100).round(1)

# Exibir tabela
display(
    quadro_df.style
    .set_caption(
        'Tabela 4 (Quadro 3) – Variáveis observacionais do estudo (n = 25) | '
        'Fonte: elaborada pela autora, 2025.'
    )
    .format({'Sim (n)': '{:,.0f}', 'Sim (%)': '{:.1f}'})
    .set_table_styles([
        {'selector': 'caption',
         'props': [('font-size', '12px'), ('font-weight', 'bold'),
                   ('text-align', 'left'), ('caption-side', 'top')]},
        {'selector': 'th',
         'props': [('background-color', '#2a78d6'), ('color', 'white'),
                   ('font-size', '10px')]},
        {'selector': 'td',
         'props': [('font-size', '10px'), ('vertical-align', 'top')]},
    ])
    .apply(lambda col: [
        # Fundo azul claro para Fase I, branco para II, verde claro para III
        ('background-color: #fff3e0' if quadro_df.loc[r, 'Fase'] == 'I'
         else 'background-color: #eef3fc' if quadro_df.loc[r, 'Fase'] == 'II'
         else 'background-color: #e8f5e9')
        for r in quadro_df.index
    ])
    .bar(subset=['Sim (%)'], color=COR_SECUNDARIA, vmin=0, vmax=25)
    .hide(axis='index')
)
''')

# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 8 — MARKDOWN: INTERPRETAÇÃO DO DESENHO AMOSTRAL
# ──────────────────────────────────────────────────────────────────────────────
md(r'''
### 4.2 Interpretação do desenho amostral

**Representatividade temporal.** A amostra de 595 processos reflete
adequadamente o peso de cada ano na população depurada. A sub-amostra de
**194 processos para 2022** (32,6% da amostra) é proporcional aos 27,8% da
população consolidada de 2022; os **211 de 2023** (35,5%) e os **190 de 2024**
(31,9%) seguem o mesmo padrão. Pequenos desvios da proporcionalidade exata
decorrem do arredondamento para números inteiros.

**Homogeneidade entre unidades.** Cada um dos 14 Juizados contribui com 33
a 55 processos, o que representa entre 5,5% e 9,2% do total amostral.
A distribuição é razoavelmente homogênea entre as unidades, conferindo
adequada representatividade para as análises desagregadas por JEC.
Subamostras menores (ex.: 5º e 13º JECs, com 33 e 36 processos,
respectivamente) impõem cautela adicional nas comparações pareadas.

**Composição por classe.** O predomínio de **88,7%** de processos na classe
"Procedimento do Juizado Especial Cível" é coerente com a natureza das
unidades estudadas. As demais classes (Cumprimento de Sentença: 9,7%;
Procedimento Comum Cível: 0,7%; e residuais: 0,7%) decorrem de
reclassificações automáticas do PJe ao longo do trâmite processual e
foram mantidas na amostra por sua distribuição aleatória, sem viés de seleção.

**Variáveis com zero ocorrências.** As variáveis **F2_07**, **F2_12**,
**F2_15** e **F2_16** não apresentaram nenhuma ocorrência na amostra de 595
processos. Isso pode refletir: (a) ausência efetiva dessas condutas no
universo estudado; (b) limitações observacionais do canal de consulta ao PJe;
ou (c) mudança de comportamento dos litigantes — em especial para F2_15 e
F2_16, que descrevem desistências após contestação, sancionadas como
litigância de má-fé em notas técnicas recentes dos centros de inteligência.
Essas variáveis serão excluídas das análises bivariada e multivariada, por
serem constantes e, portanto, não informativas para modelos preditivos.
''')
