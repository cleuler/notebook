# -*- coding: utf-8 -*-
"""
Seção 3 — População de Referência (Tabela 1)
=============================================
Gera as células do notebook referentes à análise da população bruta e
da população depurada (base consolidada), com produção da Tabela 1 da
monografia.

Outputs desta seção
--------------------
  Tabela 1 — Processos distribuídos nos 14 JEC de Natal (2022-2024),
              por unidade judiciária e ano.

Fontes de dados
---------------
  Aba TJRN (86.964 linhas)        : base bruta fornecida pelo TJRN
  Aba Base consolidada (50.320)   : população depurada (excluídas
    duplicatas, execuções extrajudiciais e processos sem advogado)

Seção da monografia: 3.2.1 — Populaçao de referência
"""

# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 1 — MARKDOWN: INTRODUÇÃO À POPULAÇÃO
# ──────────────────────────────────────────────────────────────────────────────
md(r'''
---

## 3. População de Referência

### 3.1 Da base bruta à população depurada

O arquivo recebido do TJRN em agosto de 2025 continha **86.964 registros**
referentes a processos distribuídos nos 14 Juizados Especiais Cíveis de Natal
no triênio 2022–2024. Antes de calcular o tamanho amostral, a pesquisadora
realizou três etapas de depuração automática sobre essa base bruta:

| Etapa | Critério de exclusão | Processos removidos |
|---|---|---|
| Remoção de duplicidades | Ordenação por *Data de início* + *Remover duplicatas* (Excel) | 20.739 |
| Exclusão de execuções extrajudiciais | Filtro na coluna Classe: contém "extrajudicial" | 6.903 |
| Identificação de processos sem advogado | Coluna Advogado = vazia | 9.001 |
| **Redução total** | | **36.643** |

Após a depuração restaram **50.320 processos** na aba *Base consolidada*,
que constitui a **população de referência** da pesquisa — ou seja, o universo
sobre o qual foi calculado o tamanho amostral.

> **Nota técnica:** a monografia registra "83.139 registros brutos na aba TJRN"
> (seção 3.2.1), refletindo que os dados foram extraídos do PJe com uma
> sobreposição de movimentações por processo, e não apenas os registros
> únicos. O total de processos únicos no triênio, verificado neste notebook
> a partir da aba TJRN, é compatível com esse valor.
''')

# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 2 — CÓDIGO: LEITURA DA BASE BRUTA (ABA TJRN)
# ──────────────────────────────────────────────────────────────────────────────
code(r'''
# ── Leitura da aba TJRN (base bruta) ─────────────────────────────────────────
# Colunas usadas:
#   Col 03: UNIDADE  — unidade judiciária
#   Col 20: ANO      — ano de distribuição (calculado no PJe)
# A leitura usa openpyxl diretamente para evitar carregar as ~30 colunas
# restantes desnecessariamente (arquivo grande).

import openpyxl

wb_bruto = openpyxl.load_workbook(
    ARQUIVO_XLSX,
    read_only=True,
    data_only=True,   # retorna valores calculados, não fórmulas
)
ws_tjrn = wb_bruto['TJRN']

# Iterar linha a linha e coletar apenas UNIDADE e ANO
linhas_bruto = []
for r in ws_tjrn.iter_rows(min_row=2, values_only=True):
    unidade_raw = r[3]   # Col 03: UNIDADE
    ano_raw     = r[20]  # Col 20: ANO
    if unidade_raw is None or ano_raw is None:
        continue
    try:
        ano_int = int(str(ano_raw))
    except (ValueError, TypeError):
        continue
    if ano_int in (2022, 2023, 2024):
        linhas_bruto.append((str(unidade_raw).strip(), ano_int))

wb_bruto.close()

# Montar DataFrame da base bruta
pop_bruta = pd.DataFrame(linhas_bruto, columns=['unidade', 'ano'])

# Extrair número do JEC (ordinal) para ordenação correta
pop_bruta['JEC_numero'] = (
    pop_bruta['unidade']
    .str.extract(r'^(\d+)', expand=False)
    .astype(int)
)

N_BRUTO_REAL = len(pop_bruta)
print(f'Registros com UNIDADE e ANO válidos na aba TJRN: {N_BRUTO_REAL:,}')
print(f'Distribuição por ano:')
print(pop_bruta['ano'].value_counts().sort_index().to_string())
''')

# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 3 — CÓDIGO: LEITURA DA BASE CONSOLIDADA (POPULAÇÃO DEPURADA)
# ──────────────────────────────────────────────────────────────────────────────
code(r'''
# ── Leitura da aba Base consolidada (população depurada) ─────────────────────
# Colunas usadas:
#   Col 04: UNIDADE  — unidade judiciária
#   Col 23: ANO      — ano de distribuição
# A coluna "Ano de início" (Col 08) contém fórmulas Excel (=YEAR(...))
# que retornam #VALUE! ao ler com openpyxl sem recálculo.
# Usamos a coluna ANO (Col 23), que armazena o valor diretamente.

wb_dep = openpyxl.load_workbook(
    ARQUIVO_XLSX,
    read_only=True,
    data_only=True,
)
ws_bc = wb_dep['Base consolidada']

linhas_dep = []
for r in ws_bc.iter_rows(min_row=2, values_only=True):
    unidade_raw = r[4]   # Col 04: UNIDADE
    ano_raw     = r[23]  # Col 23: ANO
    if unidade_raw is None or ano_raw is None:
        continue
    try:
        ano_int = int(str(ano_raw))
    except (ValueError, TypeError):
        continue
    if ano_int in (2022, 2023, 2024):
        linhas_dep.append((str(unidade_raw).strip(), ano_int))

wb_dep.close()

# Montar DataFrame da base consolidada
pop_dep = pd.DataFrame(linhas_dep, columns=['unidade', 'ano'])
pop_dep['JEC_numero'] = (
    pop_dep['unidade']
    .str.extract(r'^(\d+)', expand=False)
    .astype(int)
)

# ── Parâmetros globais de população (reutilizados nas seções seguintes) ───────
N_BRUTO      = 86_964          # total nominal declarado pela fonte (TJRN)
N_BRUTO_REAL = len(pop_bruta)  # total com ANO válido na aba TJRN (= 83.139)
N_POP        = 50_320          # base consolidada (população de referência)
N_POP_REAL   = len(pop_dep)    # verificação a partir dos dados lidos

print(f'Base bruta (TJRN, registros c/ ANO válido): {N_BRUTO_REAL:,}')
print(f'Base consolidada (população depurada total): {N_POP:,}')
print(f'  → verificado na leitura                 : {N_POP_REAL:,}')
print(f'  → registros c/ ANO 2022-2024            : {len(pop_dep):,}')
print()
print('Distribuição por ano na base consolidada:')
print(pop_dep['ano'].value_counts().sort_index().to_string())
''')

# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 4 — CÓDIGO: TABELA 1 — PROCESSOS POR JEC E ANO
# ──────────────────────────────────────────────────────────────────────────────
code(r'''
# ── Tabela 1: Processos distribuídos nos 14 JEC de Natal (2022-2024) ──────────
# Fonte: aba TJRN (base bruta com ANO válido = 83.139 registros).
# A monografia usa esta tabela para mostrar a distribuição da população
# de casos novos no período, antes de qualquer depuração.

# Tabela cruzada: unidade × ano (contagem de linhas)
tab1_raw = pd.crosstab(
    pop_bruta['unidade'],
    pop_bruta['ano'],
    margins=True,
    margins_name='Total',
)

# Reordenar as linhas por número do JEC (1º ao 14º) + linha Total no fim
ordem_jec = (
    pop_bruta[['unidade', 'JEC_numero']]
    .drop_duplicates()
    .sort_values('JEC_numero')['unidade']
    .tolist()
)
tab1 = tab1_raw.reindex(ordem_jec + ['Total'])

# Renomear colunas para exibição
tab1.columns = ['2022', '2023', '2024', 'Total']
tab1.index.name = 'Unidade Judiciária'

# Calcular percentual por ano sobre o total do triênio
total_geral = tab1.loc['Total', 'Total']
pct_por_ano = (tab1.loc['Total', ['2022', '2023', '2024']] / total_geral * 100).round(1)

print(f'Total de registros (base bruta com ANO válido): {total_geral:,}')
print(f'Participação por ano: '
      f'2022={pct_por_ano["2022"]}%, '
      f'2023={pct_por_ano["2023"]}%, '
      f'2024={pct_por_ano["2024"]}%')
print()

# Exibir tabela estilizada
display(
    tab1.style
    .set_caption(
        'Tabela 1 – Processos distribuídos nos 14 JEC de Natal (2022–2024), '
        'por unidade judiciária e ano | Fonte: TJRN (aba TJRN), agosto de 2025.'
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
    # Destacar a linha e coluna de Total
    .apply(lambda col: [
        'font-weight: bold; background-color: #d0e3f7'
        if (idx == 'Total') else ''
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
# CÉLULA 5 — CÓDIGO: GRÁFICO AUXILIAR — DISTRIBUIÇÃO ANUAL POR JEC
# ──────────────────────────────────────────────────────────────────────────────
code(r'''
# ── Gráfico auxiliar: distribuição de processos por JEC e ano ─────────────────
# Não numerado na monografia, mas útil para contextualizar a Tabela 1 e
# verificar a homogeneidade da carteira entre os juizados.

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# ── Painel esquerdo: barras agrupadas por ano ──────────────────────────────
anos_lista = [2022, 2023, 2024]
x = np.arange(1, 15)          # JECs 1 a 14
largura = 0.27
cores_anos = [CORES[0], CORES[1], CORES[2]]

for i, (ano, cor) in enumerate(zip(anos_lista, cores_anos)):
    vals = [
        pop_bruta.loc[pop_bruta['ano'].eq(ano) & pop_bruta['JEC_numero'].eq(j)].shape[0]
        for j in range(1, 15)
    ]
    deslocamento = (i - 1) * largura
    barras = axes[0].bar(x + deslocamento, vals, largura,
                         label=str(ano), color=cor, alpha=0.88)

axes[0].set_xlabel('Juizado Especial Cível (JEC nº)')
axes[0].set_ylabel('Número de processos')
axes[0].set_title('Distribuição de processos por JEC e ano\n(base bruta TJRN)')
axes[0].set_xticks(x)
axes[0].set_xticklabels([str(j) for j in range(1, 15)])
axes[0].legend(title='Ano', fontsize=9)
axes[0].yaxis.set_major_formatter(
    mpl.ticker.FuncFormatter(lambda v, _: f'{int(v):,}')
)

# ── Painel direito: total por JEC (barras simples com média) ──────────────
totais_jec = (
    pop_bruta.groupby('JEC_numero').size().reindex(range(1, 15)).fillna(0)
)
media_jec = totais_jec.mean()
cores_barra = [
    COR_DESTAQUE if v > media_jec * 1.02
    else (COR_SECUNDARIA if v < media_jec * 0.98 else COR_PRINCIPAL)
    for v in totais_jec
]
barras2 = axes[1].bar(totais_jec.index, totais_jec.values,
                      color=cores_barra, alpha=0.88)
axes[1].axhline(media_jec, color=TINTA, linewidth=1.4,
                linestyle='--', label=f'Média: {media_jec:,.0f}')
anotar_barras(axes[1], barras2, formato='{:,.0f}', fontsize=8.5)
axes[1].set_xlabel('Juizado Especial Cível (JEC nº)')
axes[1].set_ylabel('Total 2022–2024')
axes[1].set_title('Total de processos por JEC no triênio\n(base bruta TJRN)')
axes[1].set_xticks(range(1, 15))
axes[1].legend(fontsize=9)
axes[1].yaxis.set_major_formatter(
    mpl.ticker.FuncFormatter(lambda v, _: f'{int(v):,}')
)

plt.suptitle('Tabela 1 — Contextualização gráfica', fontsize=13,
             fontweight='bold', y=1.02)
plt.tight_layout()
plt.show()
''')

# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 6 — MARKDOWN: INTERPRETAÇÃO DA TABELA 1
# ──────────────────────────────────────────────────────────────────────────────
md(r'''
### 3.2 Interpretação da Tabela 1

A distribuição dos processos entre as 14 unidades judiciárias é **bastante
homogênea**: nenhum juizado concentra participação desproporcionalmente alta
no total do triênio. O volume individual varia de cerca de 5.500 a 6.200
processos por unidade no período.

No que se refere à distribuição **temporal**, observa-se que:

- **2022** concentra aproximadamente **27,6%** do total do triênio;
- **2023** representa cerca de **36,1%** — o ano de maior volume de
  distribuições;
- **2024** responde por aproximadamente **36,3%** do período.

O crescimento observado de 2022 para 2023 e a manutenção do patamar em 2024
são consistentes com o movimento nacional de aumento da litigiosidade
registrado pelo CNJ. O relatório *Justiça em Números 2024* apontou 83,8
milhões de processos pendentes no Judiciário brasileiro ao final de 2023 —
o maior valor da série histórica de medição.

> **Sobre a população de referência:** a base bruta (83.139 registros com ANO
> válido) foi depurada em três etapas — remoção de duplicidades (20.739),
> exclusão de execuções extrajudiciais (6.903) e identificação de processos
> sem advogado (9.001) — resultando em **50.320 processos**, que constituem
> a população de referência da pesquisa e sobre a qual foi calculado o tamanho
> amostral (Seção 4).
''')
