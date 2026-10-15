# -*- coding: utf-8 -*-
"""
Seção 6 — Frequência das Variáveis F1 e F2
============================================
Gera as células do notebook referentes à seção 4.2 da monografia.

Outputs desta seção
--------------------
  Tabela 9  — Frequência das variáveis da Fase I (n = 595)
  Gráfico 7 — Frequência das variáveis da Fase II (barras horizontais,
               duas escalas: sobre 595 e sobre 444)
  Tabela 10 — Incidência por classe processual

Valores de referência (monografia, cap. 4)
-------------------------------------------
  F1_A: 79 (13,3%) — maior exclusor na Fase I
  F1_D: 0  (0,0%)  — retirada durante a pesquisa
  F1_B: 28 (4,7%)
  Top-4 F2: F2_06 (101), F2_11 (99), F2_01 (98), F2_02 (96)
  Variáveis F2 nulas: F2_07, F2_12, F2_15, F2_16
  Proc. Juizado Especial Cível: 528 (88,7%) da amostra

Seção da monografia: 4.2.1 e 4.2.2
"""

# ──────────────────────────────────────────────────────────────────────────────
# WRAPPERS DEFENSIVOS — evitam blocos vazios na API da Anthropic
# Strips whitespace do conteúdo antes de repassar às funções originais;
# chamadas com conteúdo vazio (ou só whitespace) são silenciosamente ignoradas.
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
# CÉLULA 1 — MARKDOWN: INTRODUÇÃO À ANÁLISE DE FREQUÊNCIAS
# ──────────────────────────────────────────────────────────────────────────────
md(r'''
---

## 6. Frequência das Variáveis Observacionais

### 6.1 Panorama das variáveis de exclusão — Fase I (Tabela 9)

As seis variáveis da Fase I são critérios de **exclusão**: processos que
apresentam qualquer uma delas não reúnem as condições mínimas para serem
analisados como casos de potencial litigância predatória pelo polo ativo.
De 595 processos avaliados, **151 (25,4%)** foram excluídos — em 150 casos
por um único critério e em 1 caso por dois critérios simultâneos.

O critério mais acionado foi **F1_A** — ações com pessoa física no polo
passivo (79 processos; 13,3%) —, o que é consistente com o perfil esperado
do fenômeno: litigância predatória pressupõe a presença de pessoa jurídica
no polo passivo (ex.: operadoras de planos de saúde, instituições financeiras,
empresas de telecomunicações), não o reverso.

**F1_D** (processos suspensos) não apresentou nenhuma ocorrência (0,0%).
Esse resultado decorre de decisão metodológica adotada no curso da pesquisa:
os processos suspensos foram depurados diretamente na planilha-base do TJRN,
tornando a variável tecnicamente não observável nesta amostra. Por essa razão,
F1_D não integra o Quadro 3 da monografia (25 variáveis) e é mantida aqui
apenas para documentação da completude do instrumento de coleta.
''')

# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 2 — CÓDIGO: TABELA 9 — FASE I
# ──────────────────────────────────────────────────────────────────────────────
code(r'''
# ── Configuração dos rótulos e descrições das variáveis F1 ───────────────────
NOMES_F1 = {
    'F1_A': 'Ações com pessoa física no polo passivo',
    'F1_B': 'Ausência de grande litigante no polo passivo',
    'F1_C': 'Causas ajuizadas sem advogado (atermação)',
    'F1_D': 'Processos suspensos (*)  — variável retirada',
    'F1_E': 'Distribuição incorreta',
    'F1_F': 'Parte jurídica no polo ativo',
}

DESC_F1 = {
    'F1_A': 'Excluir quando o polo passivo é formado por pessoa física',
    'F1_B': 'Excluir quando não há grande litigante no polo passivo',
    'F1_C': 'Excluir processos ajuizados sem representação por advogado',
    'F1_D': 'Excluir processos suspensos por determinação judicial',
    'F1_E': 'Processos erroneamente distribuídos aos Juizados Especiais',
    'F1_F': 'Excluir quando o polo ativo é pessoa jurídica',
}

CRITERIO_F1 = {c: 'Consulta às partes e movimentações do PJe' for c in COLS_F1}

# ── Calcular frequências ──────────────────────────────────────────────────────
linhas_f1 = []
for col in COLS_F1:
    n_sim = int(dados[col].sum())
    n_nao = int((~dados[col]).sum())
    # IC Wilson sobre os 595 (mesmo para variáveis de exclusão)
    if n_sim > 0:
        li, ls = proportion_confint(n_sim, N_AMST, alpha=ALPHA, method='wilson')
    else:
        li, ls = 0.0, 0.0
    linhas_f1.append({
        'Código'         : col,
        'Nome da Variável': NOMES_F1[col],
        'Critério'       : 'Exclusão (se Sim → excluído da análise)',
        'Sim'            : n_sim,
        '% Sim'          : n_sim / N_AMST,
        'IC 2,5%'        : li,
        'IC 97,5%'       : ls,
        'Não'            : n_nao,
        '% Não'          : n_nao / N_AMST,
    })

tab9 = pd.DataFrame(linhas_f1)

# Validar valores da monografia
assert tab9.loc[tab9['Código'] == 'F1_A', 'Sim'].values[0] == 79, \
    'F1_A: esperado 79'
assert tab9.loc[tab9['Código'] == 'F1_D', 'Sim'].values[0] == 0, \
    'F1_D: esperado 0 (retirada da pesquisa)'
assert tab9.loc[tab9['Código'] == 'F1_B', 'Sim'].values[0] == 28, \
    'F1_B: esperado 28'
assert tab9['Sim'].sum() == 152, \
    f'Soma de Sim na F1: esperado 152 (151 excluídos + 1 processo c/ F1_A+F1_B); obtido {tab9["Sim"].sum()}'
print('Asserts Tabela 9: OK')
print()

# Exibição estilizada
display(
    tab9[['Código', 'Nome da Variável', 'Sim', '% Sim', 'IC 2,5%', 'IC 97,5%', 'Não', '% Não']].style
    .set_caption(
        'Tabela 9 – Frequência das variáveis da Fase I — exclusão (n = 595) | '
        'Fonte: elaborada pela autora, a partir da aba AMOSTRA (2025).\n'
        '(*) F1_D: variável retirada no curso da pesquisa; processos suspensos '
        'foram depurados diretamente na planilha-base.'
    )
    .format({
        'Sim'    : '{:,.0f}',
        '% Sim'  : '{:.1%}',
        'IC 2,5%': '{:.1%}',
        'IC 97,5%':'{:.1%}',
        'Não'    : '{:,.0f}',
        '% Não'  : '{:.1%}',
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
        # Destacar F1_D (retirada) em cinza
        'background-color: #f0f0f0; color: #999999'
        if tab9.iloc[r]['Código'] == 'F1_D'
        else 'background-color: #eef3fc' if r % 2 == 0
        else ''
        for r in range(len(col))
    ])
    .bar(subset=['% Sim'], color='#eb6834', vmin=0, vmax=0.16)
    .hide(axis='index')
)
''')

# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 3 — CÓDIGO: GRÁFICO COMPLEMENTAR — DISTRIBUIÇÃO DE F1 POR PROCESSO
# ──────────────────────────────────────────────────────────────────────────────
code(r'''
# ── Gráfico complementar: distribuição dos exclusores F1 ──────────────────────
# Barras horizontais com dois grupos: frequência de cada variável sobre os 595
# e, separadamente, a sobreposição (processos com múltiplos critérios).

fig, axes = plt.subplots(1, 2, figsize=(14, 4))

# Painel esquerdo: frequência de cada variável F1 sobre os 595
cols_f1_plot = COLS_F1  # inclui F1_D para mostrar que é zero
nomes_curtos = {
    'F1_A': 'F1_A: Pessoa física\nno polo passivo',
    'F1_B': 'F1_B: Ausência de\ngrande litigante',
    'F1_C': 'F1_C: Sem advogado\n(atermação)',
    'F1_D': 'F1_D: Suspenso (*)\n(retirada)',
    'F1_E': 'F1_E: Distribuição\nincorreta',
    'F1_F': 'F1_F: PJ no\npolo ativo',
}
vals_f1 = [int(dados[c].sum()) for c in cols_f1_plot]
cores_f1 = [
    COR_PRINCIPAL if v > 0 else GRADE
    for v in vals_f1
]
y = np.arange(len(cols_f1_plot))
barras_f1 = axes[0].barh(
    y, vals_f1,
    color=cores_f1, edgecolor='white',
    linewidth=0.8, height=0.60,
)
for barra, v in zip(barras_f1, vals_f1):
    if v > 0:
        axes[0].text(
            barra.get_width() + 0.8,
            barra.get_y() + barra.get_height() / 2,
            f'{v}  ({v/N_AMST*100:.1f}%)',
            va='center', ha='left', fontsize=9.5, color=TINTA,
        )
    else:
        axes[0].text(
            0.5, barra.get_y() + barra.get_height() / 2,
            '0  (retirada)',
            va='center', ha='left', fontsize=9, color='#999999', style='italic',
        )

axes[0].set_yticks(y)
axes[0].set_yticklabels([nomes_curtos[c] for c in cols_f1_plot], fontsize=9)
axes[0].invert_yaxis()
axes[0].set_xlabel('Processos (n = 595)')
axes[0].set_xlim(0, max(vals_f1) * 1.50)
axes[0].set_title('Frequência de cada variável F1\n(sobre os 595 processos)', fontsize=10.5)
axes[0].grid(axis='y', visible=False)

# Painel direito: composição dos 151 excluídos
dados_excl = dados[dados['Excluido_F1']].copy()
n_excl_total = len(dados_excl)
n_f1_por_proc = dados_excl[COLS_F1].sum(axis=1)
dist_mult = n_f1_por_proc.value_counts().sort_index()

axes[1].bar(
    [f'{int(k)} critério{"s" if k > 1 else ""}' for k in dist_mult.index],
    dist_mult.values,
    color=[CORES[1], CORES[7]][:len(dist_mult)],
    edgecolor='white', linewidth=0.8, width=0.5,
)
for i, v in enumerate(dist_mult.values):
    axes[1].text(
        i, v + 0.5,
        f'{v}  ({v/n_excl_total*100:.1f}%)',
        ha='center', fontsize=10, color=TINTA,
    )
axes[1].set_ylabel('Processos excluídos')
axes[1].set_ylim(0, dist_mult.max() * 1.25)
axes[1].set_title(
    f'Multiplicidade de critérios F1\nnos {n_excl_total} processos excluídos',
    fontsize=10.5,
)
axes[1].grid(axis='x', visible=False)

plt.suptitle(
    'Tabela 9 — Contextualização gráfica das variáveis F1\n'
    'Fonte: elaborada pela autora, a partir da aba AMOSTRA (2025).',
    fontsize=11, fontweight='bold', y=1.02,
)
plt.tight_layout()
plt.show()
''')

# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 4 — MARKDOWN: SEÇÃO 4.2.2 — VARIÁVEIS F2
# ──────────────────────────────────────────────────────────────────────────────
md(r'''
### 6.2 Frequência das variáveis de indício — Fase II (Gráfico 7)

Das 17 variáveis de indício observadas na Fase II, quatro apresentaram
**zero ocorrências** em toda a amostra de 595 processos:

- **F2_07** (Pedidos vagos/hipotéticos)
- **F2_12** (Valor da causa inadequado)
- **F2_15** (Desistência após notificação)
- **F2_16** (Desistência após contestação)

As quatro variáveis com zero ocorrências serão **excluídas das análises
bivariada e multivariada** (Seções 7 e 8), pois são constantes e,
portanto, não discriminantes para modelos preditivos.

As demais 13 variáveis apresentam frequências muito concentradas:
as **quatro variáveis mais comuns** — F2_06, F2_11, F2_01 e F2_02 —
representam, em conjunto, **quase 80%** de todas as positivações da Fase II.
Isso revela um padrão altamente estruturado de irregularidades:
documentação deficiente, advogado fora da comarca e petição padronizada
são os marcadores mais associados ao fenômeno no universo dos JECs de Natal.

> **Base de cálculo:** as frequências da Tabela abaixo e do Gráfico 7
> são apresentadas em duas escalas — sobre os **595 processos totais**
> e sobre os **444 que avançaram à Fase II** —, pois a interpretação
> substantiva depende do denominador adotado. Para os 151 excluídos na
> Fase I, as variáveis F2 foram computadas como `False` (não aplicáveis).
''')

# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 5 — CÓDIGO: CÁLCULO DAS FREQUÊNCIAS F2
# ──────────────────────────────────────────────────────────────────────────────
code(r'''
# ── Rótulos detalhados das variáveis F2 ──────────────────────────────────────
NOMES_F2 = {
    'F2_01': 'F2_01 — Petição vaga/genérica',
    'F2_02': 'F2_02 — Ausência de documentos essenciais',
    'F2_03': 'F2_03 — Documentos sem relação com a causa',
    'F2_04': 'F2_04 — Pedido de dispensa de audiência',
    'F2_05': 'F2_05 — Foro inadequado',
    'F2_06': 'F2_06 — Documentos incompletos/ilegíveis',
    'F2_07': 'F2_07 — Pedidos vagos/hipotéticos (*)',
    'F2_08': 'F2_08 — Demanda idêntica não declarada',
    'F2_09': 'F2_09 — Procuração incompleta',
    'F2_10': 'F2_10 — Procuração irregular (assin. digital)',
    'F2_11': 'F2_11 — Advogado fora da comarca',
    'F2_12': 'F2_12 — Valor da causa inadequado (*)',
    'F2_13': 'F2_13 — Classe ou assunto incorreto',
    'F2_14': 'F2_14 — Desistência após indeferi. de liminar',
    'F2_15': 'F2_15 — Desistência após notificação (*)',
    'F2_16': 'F2_16 — Desistência após contestação (*)',
    'F2_17': 'F2_17 — Contrato de honorários abusivo',
}

# ── Subconjunto Fase II ───────────────────────────────────────────────────────
dados_f2_base = dados[~dados['Excluido_F1']].copy()   # 444 processos
N_F2 = len(dados_f2_base)   # 444

# ── Calcular frequências nas duas bases ──────────────────────────────────────
linhas_freq_f2 = []
for col in COLS_F2:
    n_595 = int(dados[col].sum())
    n_444 = int(dados_f2_base[col].sum())
    linhas_freq_f2.append({
        'Código'             : col,
        'Nome'               : NOMES_F2[col],
        'n (sobre 595)'      : n_595,
        '% (sobre 595)'      : n_595 / N_AMST,
        'n (sobre 444)'      : n_444,
        '% (sobre 444)'      : n_444 / N_F2,
        'Zero ocorrências'   : n_595 == 0,
    })

freq_f2 = (pd.DataFrame(linhas_freq_f2)
           .sort_values('n (sobre 595)', ascending=False)
           .reset_index(drop=True))

# Validar top-4
top4 = freq_f2.head(4)['Código'].tolist()
assert set(top4) == {'F2_06', 'F2_11', 'F2_01', 'F2_02'}, \
    f'Top-4 F2 inesperado: {top4}'

# Validar zeros
zeros_f2 = freq_f2.loc[freq_f2['Zero ocorrências'], 'Código'].tolist()
assert set(zeros_f2) == {'F2_07', 'F2_12', 'F2_15', 'F2_16'}, \
    f'Variáveis com zero inesperadas: {zeros_f2}'

print('Asserts frequencias F2: OK')
print(f'  Top-4: {top4}')
print(f'  Zeros: {sorted(zeros_f2)}')
print()

# Variáveis com ocorrências (para modelos preditivos)
COLS_F2_ATIVOS = freq_f2.loc[~freq_f2['Zero ocorrências'], 'Código'].tolist()
print(f'  F2 com ocorrencias (n = {len(COLS_F2_ATIVOS)}): {COLS_F2_ATIVOS}')
''')

# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 6 — CÓDIGO: GRÁFICO 7 — FREQUÊNCIA DAS VARIÁVEIS F2
# ──────────────────────────────────────────────────────────────────────────────
code(r'''
# ── Gráfico 7: frequência das variáveis F2 (barras horizontais duplas) ─────────
# Duas sub-figuras lado a lado:
#   Esquerdo: todas as 17 variáveis (% sobre 595)
#   Direito : variáveis com ao menos 1 ocorrência (% sobre 444 da Fase II)

fig, axes = plt.subplots(1, 2, figsize=(16, 6.5))

# ── Painel esquerdo: % sobre 595 ─────────────────────────────────────────────
freq_plot = freq_f2.copy()  # já ordenado por n decrescente
y = np.arange(len(freq_plot))

# Cores: laranja para não-nulas, cinza para zero-ocorrências
cores_graf7 = [
    COR_DESTAQUE if not row['Zero ocorrências'] else GRADE
    for _, row in freq_plot.iterrows()
]

barras_esq = axes[0].barh(
    y, freq_plot['% (sobre 595)'] * 100,
    color=cores_graf7, edgecolor='white',
    linewidth=0.7, height=0.65,
)
for barra, (_, row) in zip(barras_esq, freq_plot.iterrows()):
    v = row['% (sobre 595)'] * 100
    n = int(row['n (sobre 595)'])
    if n > 0:
        axes[0].text(
            v + 0.3, barra.get_y() + barra.get_height() / 2,
            f'{n}  ({v:.1f}%)',
            va='center', ha='left', fontsize=8.5, color=TINTA,
        )
    else:
        axes[0].text(
            0.3, barra.get_y() + barra.get_height() / 2,
            '0  (*)',
            va='center', ha='left', fontsize=8.5, color='#aaaaaa', style='italic',
        )

axes[0].set_yticks(y)
axes[0].set_yticklabels(freq_plot['Nome'], fontsize=8.5)
axes[0].invert_yaxis()
axes[0].set_xlabel('% dos 595 processos da amostra')
axes[0].xaxis.set_major_formatter(mticker.PercentFormatter())
axes[0].set_xlim(0, freq_plot['% (sobre 595)'].max() * 100 * 1.55)
axes[0].set_title('Frequência das variáveis F2\n(base: 595 processos da amostra)',
                  fontsize=10.5, fontweight='bold')
axes[0].grid(axis='y', visible=False)

# ── Painel direito: só variáveis ativas (% sobre 444 da Fase II) ───────────────
freq_ativas = freq_plot[~freq_plot['Zero ocorrências']].copy()
y2 = np.arange(len(freq_ativas))

barras_dir = axes[1].barh(
    y2, freq_ativas['% (sobre 444)'] * 100,
    color=COR_PRINCIPAL, edgecolor='white',
    linewidth=0.7, height=0.65,
)
for barra, (_, row) in zip(barras_dir, freq_ativas.iterrows()):
    v = row['% (sobre 444)'] * 100
    n = int(row['n (sobre 444)'])
    axes[1].text(
        v + 0.4, barra.get_y() + barra.get_height() / 2,
        f'{n}  ({v:.1f}%)',
        va='center', ha='left', fontsize=8.5, color=TINTA,
    )

axes[1].set_yticks(y2)
axes[1].set_yticklabels(freq_ativas['Nome'], fontsize=8.5)
axes[1].invert_yaxis()
axes[1].set_xlabel('% dos 444 processos avaliados na Fase II')
axes[1].xaxis.set_major_formatter(mticker.PercentFormatter())
axes[1].set_xlim(0, freq_ativas['% (sobre 444)'].max() * 100 * 1.55)
axes[1].set_title(
    'Gráfico 7 – Frequência das variáveis F2\n'
    '(base: 444 processos avaliados na Fase II)',
    fontsize=10.5, fontweight='bold',
)
axes[1].grid(axis='y', visible=False)

plt.suptitle(
    'Fonte: elaborada pela autora, a partir da aba AMOSTRA (2025).\n'
    '(*) Variáveis com zero ocorrências: F2_07, F2_12, F2_15, F2_16.',
    fontsize=9, y=-0.02, color=TINTA_2,
)
plt.tight_layout()
plt.show()
''')

# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 7 — MARKDOWN: INTERPRETAÇÃO DAS VARIÁVEIS F2
# ──────────────────────────────────────────────────────────────────────────────
md(r'''
### 6.3 Interpretação das frequências da Fase II

O Gráfico 7 evidencia uma estrutura bimodal nas frequências das variáveis F2:
há um **bloco superior de quatro variáveis de alta frequência** (F2_06,
F2_11, F2_01 e F2_02 — todas com 16% a 17% dos 595 processos) e um **grupo
inferior de longa cauda**, com frequências entre 0,2% e 3%.

Essa concentração tem implicações metodológicas e substantivas relevantes:

**Do ponto de vista substantivo**, as quatro variáveis de alta frequência
revelam o perfil característico da litigância predatória nos JECs de Natal:

- **F2_06** (Documentos incompletos/ilegíveis — 101 processos): padrão
  característico de produção em escala, em que a personalização dos anexos
  é dispensada em favor de documentos genéricos ou copiados de outros processos.
- **F2_11** (Advogado fora da comarca — 99 processos): advogados com sede
  em outra localidade que ajuízam demandas em série nos JECs de Natal,
  muitas vezes sem conhecimento do contexto local da relação jurídica.
- **F2_01** (Petição vaga/genérica — 98 processos): narrativa padronizada
  sem fatos específicos, traço clássico da industrialização da litigância.
- **F2_02** (Ausência de documentos essenciais — 96 processos): a ausência de
  documentos que comprovem minimamente a relação jurídica alegada é consistente
  com a estratégia de "tentativa de sorte", na qual a ausência de defesa ou a
  homologação automática de acordos são o verdadeiro objetivo.

**Do ponto de vista metodológico**, a alta correlação esperada entre F2_01,
F2_02, F2_06 e F2_11 — confirmada na análise da matriz phi (Seção 9) — impõe
cautela na regressão logística: a inclusão simultânea de variáveis altamente
colineares pode inflar os erros padrão dos coeficientes e dificultar a
interpretação dos odds ratios individuais.
''')

# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 8 — MARKDOWN: SEÇÃO 4.2.2 — INCIDÊNCIA POR CLASSE
# ──────────────────────────────────────────────────────────────────────────────
md(r'''
### 6.4 Incidência por classe processual (Tabela 10)

A análise por classe processual é feita sobre os **595 processos**,
cruzando a classificação final (sem indício / indício sem certeza / certeza)
com a classe registrada no PJe. Como esperado, dada a composição da amostra
(**88,7% de "Procedimento do Juizado Especial Cível"**), a concentração dos
casos de indício e certeza está nessa classe.

A ocorrência de **2 processos com certeza e 4 com indício** entre os 67
processos de outras classes (majoritariamente Cumprimento de Sentença —
n = 58) sinaliza que o fenômeno não é absolutamente restrito ao procedimento
típico dos JECs, embora com frequência substancialmente menor: 6/67 = **9,0%**
nas outras classes vs. 99/528 = **18,8%** no procedimento típico.
''')

# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 9 — CÓDIGO: TABELA 10 — INCIDÊNCIA POR CLASSE PROCESSUAL
# ──────────────────────────────────────────────────────────────────────────────
code(r'''
# ── Tabela 10: incidência por classe processual ────────────────────────────────

# Classificação em três grupos para esta tabela
dados['classif3'] = pd.Categorical(
    np.where(dados['Certeza'], 'Certeza',
    np.where(dados['Indicio'], 'Indício (sem certeza)',
             'Sem indício')),
    categories=['Sem indício', 'Indício (sem certeza)', 'Certeza'],
    ordered=True,
)

# Classe resumida: procedimento típico vs. demais
CLASSE_PRINC = 'PROCEDIMENTO DO JUIZADO ESPECIAL CÍVEL'
dados['classe_tab10'] = dados['classe'].where(
    dados['classe'] == CLASSE_PRINC,
    other='Outras classes',
)

# Crosstab: classe × classificação
tab10_raw = pd.crosstab(
    dados['classe_tab10'],
    dados['classif3'],
    margins=True,
    margins_name='Total',
)
# Reordenar: classe principal primeiro
tab10_raw = tab10_raw.reindex([CLASSE_PRINC, 'Outras classes', 'Total'])

# Adicionar % por linha
for col in ['Sem indício', 'Indício (sem certeza)', 'Certeza']:
    tab10_raw[f'% {col}'] = (tab10_raw[col] / tab10_raw['Total'] * 100).round(1)

# % total com indício (qualquer)
tab10_raw['% c/ Indício'] = (
    (tab10_raw['Indício (sem certeza)'] + tab10_raw['Certeza'])
    / tab10_raw['Total'] * 100
).round(1)

# Validar valores da monografia
assert tab10_raw.loc[CLASSE_PRINC, 'Certeza'] == 28, \
    f'Certeza em Proc. JEC: esperado 28; obtido {tab10_raw.loc[CLASSE_PRINC, "Certeza"]}'
assert tab10_raw.loc['Outras classes', 'Certeza'] == 2, \
    f'Certeza nas outras classes: esperado 2'
assert tab10_raw.loc['Total', 'Total'] == 595, \
    'Total geral deve ser 595'
print('Asserts Tabela 10: OK')

display(
    tab10_raw[['Sem indício', 'Indício (sem certeza)', 'Certeza',
               'Total', '% Sem indício', '% Indício (sem certeza)',
               '% Certeza', '% c/ Indício']].style
    .set_caption(
        'Tabela 10 – Incidência de litigância predatória por classe '
        'processual (n = 595) | '
        'Fonte: elaborada pela autora, a partir da aba AMOSTRA (2025).\n'
        'Nota: "Outras classes" inclui Cumprimento de Sentença (n=58), '
        'Procedimento Comum Cível (n=4) e demais classes residuais (n=5).'
    )
    .format({
        'Sem indício'            : '{:,.0f}',
        'Indício (sem certeza)'  : '{:,.0f}',
        'Certeza'                : '{:,.0f}',
        'Total'                  : '{:,.0f}',
        '% Sem indício'          : '{:.1f}%',
        '% Indício (sem certeza)': '{:.1f}%',
        '% Certeza'              : '{:.1f}%',
        '% c/ Indício'           : '{:.1f}%',
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
        'font-weight: bold; background-color: #d0e3f7'
        if idx == 'Total' else
        'background-color: #eef3fc' if i % 2 == 0 else ''
        for i, idx in enumerate(tab10_raw.index)
    ])
    .bar(subset=['% c/ Indício'], color=COR_DESTAQUE, vmin=0, vmax=25)
)
''')

# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 10 — CÓDIGO: GRÁFICO TABELA 10 — COMPOSIÇÃO POR CLASSE
# ──────────────────────────────────────────────────────────────────────────────
code(r'''
# ── Gráfico de barras empilhadas: composição por classe processual ─────────────
classes_plot = [CLASSE_PRINC, 'Outras classes']
rots_plot    = ['Procedimento do\nJuizado Especial Cível\n(n=528)',
                'Outras classes\n(n=67)']

vals_si = [
    tab10_raw.loc[c, 'Sem indício'] / tab10_raw.loc[c, 'Total'] * 100
    for c in classes_plot
]
vals_is = [
    tab10_raw.loc[c, 'Indício (sem certeza)'] / tab10_raw.loc[c, 'Total'] * 100
    for c in classes_plot
]
vals_ce = [
    tab10_raw.loc[c, 'Certeza'] / tab10_raw.loc[c, 'Total'] * 100
    for c in classes_plot
]

fig, ax = plt.subplots(figsize=(9, 4.5))
x = np.arange(len(classes_plot))
larg = 0.45

# Empilhar as três categorias
b_si = ax.bar(x, vals_si, larg, label='Sem indício',          color=GRADE,    edgecolor='white')
b_is = ax.bar(x, vals_is, larg, bottom=vals_si,
              label='Indício (sem certeza)',  color=CORES[1],  edgecolor='white')
b_ce = ax.bar(x, vals_ce, larg, bottom=[a+b for a, b in zip(vals_si, vals_is)],
              label='Certeza',               color=CORES[7],  edgecolor='white')

# Rótulos percentuais dentro das fatias
for i, (si, is_, ce) in enumerate(zip(vals_si, vals_is, vals_ce)):
    if si > 3:
        ax.text(i, si / 2, f'{si:.1f}%', ha='center', va='center',
                fontsize=9.5, color=TINTA, fontweight='bold')
    if is_ > 2:
        ax.text(i, si + is_ / 2, f'{is_:.1f}%', ha='center', va='center',
                fontsize=9.5, color='white', fontweight='bold')
    if ce > 1.5:
        ax.text(i, si + is_ + ce / 2, f'{ce:.1f}%', ha='center', va='center',
                fontsize=9.5, color='white', fontweight='bold')

ax.set_xticks(x)
ax.set_xticklabels(rots_plot, fontsize=10)
ax.set_ylabel('% da sub-amostra por classe')
ax.yaxis.set_major_formatter(mticker.PercentFormatter())
ax.set_ylim(0, 108)
ax.legend(loc='upper right', fontsize=9.5, frameon=False)
ax.set_title(
    'Tabela 10 — Composição da classificação por classe processual\n'
    'Fonte: elaborada pela autora, a partir da aba AMOSTRA (2025).',
    fontsize=11, fontweight='bold',
)
ax.grid(axis='x', visible=False)
plt.tight_layout()
plt.show()
''')

# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 11 — MARKDOWN: SÍNTESE E LIMITAÇÕES DA ANÁLISE DE FREQUÊNCIAS
# ──────────────────────────────────────────────────────────────────────────────
md(r'''
### 6.5 Síntese e limitações

**Fase I — Exclusão.** A taxa de exclusão de 25,4% é expressiva: um em cada
quatro processos da amostra não reunia as condições mínimas para análise de
litigância predatória. F1_A (polo passivo formado por pessoa física) responde
por 52,3% dos excluídos (79/151), sinalizando que a demanda nos JECs de Natal
é heterogênea, com parcela relevante de litígios interpessoais (ex.: ações de
cobrança entre particulares) que não se enquadram no fenômeno estudado.

**Fase II — Indícios formais.** A estrutura bimodal das frequências — com
quatro variáveis concentrando a maioria das positivações — facilita a
construção de instrumentos de triagem automatizados: um fluxo de análise
baseado apenas em F2_01, F2_02, F2_06 e F2_11 capturaria a maior parte
dos processos com irregularidades formais.

**Limitações:**

1. **Variáveis com zero ocorrências (F2_07, F2_12, F2_15, F2_16):** a ausência
   não implica irrelevância substantiva do critério. Pode refletir limitações
   do canal de consulta ao PJe (ex.: campos não preenchidos pelos serventuários)
   ou ainda, no caso de F2_15 e F2_16, adaptação do comportamento dos litigantes
   às notas técnicas dos centros de inteligência que passaram a monitorar
   desistências pós-contestação como indicativo de litigância de má-fé.

2. **Dupla contagem entre F2_01, F2_02 e F2_06:** um mesmo processo pode ter
   simultaneamente petição vaga, ausência de documentos e documentos ilegíveis.
   A frequência marginal de cada variável subestima o total de processos
   irregulares (que é dado pela variável `Alguma_F2`, = 233) e superestima
   a prevalência individual se interpretada de forma aditiva.

3. **Classe processual como possível confundidor:** a predominância da classe
   "Procedimento do Juizado Especial Cível" (88,7%) limita a comparabilidade
   entre classes. A análise por classe é apresentada apenas de forma descritiva,
   sem inferência estatística, dado o desequilíbrio amostral.
''')