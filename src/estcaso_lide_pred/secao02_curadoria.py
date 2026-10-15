# -*- coding: utf-8 -*-
"""
Seção 2 — Curadoria dos Dados
==============================
Células de markdown e código incluídas no notebook por build_notebook.py.
Usa as funções md(), code() e interp() definidas no builder.

Conteúdo gerado
---------------
- Leitura das abas AMOSTRA, Quadro variáveis e Base consolidada
- Normalização dos valores Sim/Não → booleanos
- Recálculo das colunas-conclusão (Fase I e Fase II) a partir das variáveis
- Criação de variáveis derivadas: Excluido_F1, Alguma_F2, Avancou_F3,
  Indicio, Certeza, Classificacao, JEC_numero
- Validação por assert (valores de referência publicados na monografia)
- Exibição do dicionário de variáveis (Quadro 3 / Tabela 4)
- Exportação do DataFrame curado em dat/estcaso_lide_pred/processado/

Observações técnicas
--------------------
* A coluna 11 (Conclusão FASE I) e a coluna 29 (Conclusão FASE II) foram
  preenchidas com fórmulas Excel ou com texto descritivo como "Parou na Fase I",
  "O processo irá para Fase II", "Processo irá para Fase III" etc.
  As colunas-conclusão são recalculadas a partir das variáveis F1/F2/F3
  booleanas para garantir consistência independente do mecanismo de fórmulas.
* Os valores booleanos na planilha aparecem em caixas mistas ("Sim", "sim",
  "Não", "não", "Não preencher - Parou na Fase I" etc.).  A normalização
  interpreta qualquer valor cujo texto, após strip/lower, comece com "sim"
  como True; qualquer outro como False.
* Processos excluídos na Fase I têm os campos de F2 e F3 preenchidos com
  "Não preencher - Parou na Fase I" (e variações). Esses valores são
  corretamente mapeados para False.
"""

# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 1 — MARKDOWN: CURADORIA — VISÃO GERAL
# ──────────────────────────────────────────────────────────────────────────────
md(r'''
---

## 2. Curadoria dos Dados

### 2.1 Fonte e estrutura da planilha

A planilha principal —
`PlanilhaPreenchidaVariaveisCorrigida_CN_JE_S1422934_Mestrado_03_02.xlsx` —
foi organizada pela pesquisadora e contém cinco abas:

| Aba | Conteúdo | Linhas |
|---|---|---|
| `AMOSTRA` | Dados coletados nos 595 processos amostrados | 595 |
| `Base consolidada` | População depurada (base de cálculo amostral) | 50.320 |
| `Quadro variáveis` | Dicionário das 25 variáveis observacionais | ~25 |
| `Amostragem (Fórmula)` | Fórmulas de seleção aleatória | ~2.470 |
| `TJRN` | Dados brutos originais fornecidos pelo TJRN | 86.964 |

**Base de análise:** a aba `AMOSTRA`, com 595 processos e 34 colunas.

### 2.2 Estrutura das variáveis

O questionário é dividido em três fases:

- **Fase I (F1_A a F1_F):** seis variáveis de exclusão. Se qualquer uma for
  positiva, o processo é retirado da análise (não apresenta as condições
  mínimas para ser considerado um caso de litigância predatória pelo polo ativo).
- **Fase II (F2_01 a F2_17):** dezessete variáveis de indícios de abusividade,
  extraídas do Anexo A da Recomendação CNJ n.º 159/2024. Se pelo menos uma
  for positiva, o processo avança para a Fase III.
- **Fase III (F3_18 a F3_20):** três variáveis sistêmicas de massificação.
  A combinação F3_19 + F3_20 configura **indício**; as três juntas configuram
  **certeza** de litigância predatória.

**Critério de classificação final (seção 3.2.4 da monografia):**

| Classificação | Critério formal |
|---|---|
| Excluído na Fase I | Qualquer F1 = Sim |
| Sem indicativo na Fase II | Fase I passou + nenhuma F2 = Sim |
| Demais processos na Fase III | Fase II com F2 ≥ 1, mas sem combinação de indício ou certeza |
| Indício de litigância predatória | F3_19 = Sim **e** F3_20 = Sim (inclui certeza) |
| Certeza de litigância predatória | F3_18 = Sim **e** F3_19 = Sim **e** F3_20 = Sim |

> **Nota:** os 30 processos com certeza estão contidos nos 105 com indício.
> As duas categorias não devem ser somadas quando se fala em total de casos.
''')

# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 2 — CÓDIGO: MAPEAMENTO DE COLUNAS
# ──────────────────────────────────────────────────────────────────────────────
code(r'''
# ── Mapeamento completo das colunas da aba AMOSTRA ───────────────────────────
# Cada entrada: (índice_zero_based, chave_interna_python, rótulo_legível)
COLUNAS_AMOSTRA = [
    # ── Identificação ──────────────────────────────────────────────────────
    (0,  'id_amostra',   'Amostra selecionada'),
    (1,  'num_processo', 'Número do Processo'),
    (2,  'unidade',      'Unidade Judiciária'),
    (3,  'ano',          'Ano da distribuição'),
    (4,  'classe',       'Classe'),
    # ── Fase I: variáveis de exclusão ──────────────────────────────────────
    (5,  'F1_A', 'Ações de pessoa física no polo passivo'),
    (6,  'F1_B', 'Ausência de grande litigante no polo passivo'),
    (7,  'F1_C', 'Causas ajuizadas sem advogado (atermação)'),
    (8,  'F1_D', 'Processos suspensos'),
    (9,  'F1_E', 'Distribuição incorreta'),
    (10, 'F1_F', 'Parte PJ no polo ativo'),
    (11, '_conclusao_f1', 'Conclusão FASE I'),  # recalculada; prefixo _ = uso interno
    # ── Fase II: variáveis de indício ──────────────────────────────────────
    (12, 'F2_01', 'Petição vaga/genérica'),
    (13, 'F2_02', 'Ausência de documentos essenciais'),
    (14, 'F2_03', 'Documentos sem relação com a causa de pedir'),
    (15, 'F2_04', 'Pedido de dispensa de audiência'),
    (16, 'F2_05', 'Foro inadequado'),
    (17, 'F2_06', 'Documentos incompletos/ilegíveis'),
    (18, 'F2_07', 'Pedidos vagos/hipotéticos'),
    (19, 'F2_08', 'Demanda idêntica não declarada'),
    (20, 'F2_09', 'Procuração incompleta'),
    (21, 'F2_10', 'Procuração irregular (assinatura digital)'),
    (22, 'F2_11', 'Advogado fora da comarca'),
    (23, 'F2_12', 'Valor da causa inadequado'),
    (24, 'F2_13', 'Classe ou assunto incorreto'),
    (25, 'F2_14', 'Desistência/abandono após indeferimento de liminar'),
    (26, 'F2_15', 'Desistência/abandono após notificação'),
    (27, 'F2_16', 'Desistência/abandono após contestação'),
    (28, 'F2_17', 'Contrato de honorários abusivo'),
    (29, '_conclusao_f2', 'Conclusão FASE II'),  # recalculada; uso interno
    # ── Fase III: variáveis sistêmicas de massificação ─────────────────────
    (30, 'F3_18', 'Multiplicidade de ações pela mesma parte'),
    (31, 'F3_19', 'Petições iniciais idênticas'),
    (32, 'F3_20', 'Volume elevado de demandas pelo mesmo advogado'),
    (33, 'obs',   'Observações'),
]

# Conjuntos de chaves por fase — usados em todos os módulos seguintes
COLS_F1 = ['F1_A', 'F1_B', 'F1_C', 'F1_D', 'F1_E', 'F1_F']
COLS_F2 = [
    'F2_01', 'F2_02', 'F2_03', 'F2_04', 'F2_05', 'F2_06', 'F2_07',
    'F2_08', 'F2_09', 'F2_10', 'F2_11', 'F2_12', 'F2_13', 'F2_14',
    'F2_15', 'F2_16', 'F2_17',
]
COLS_F3 = ['F3_18', 'F3_19', 'F3_20']

# Dicionário: chave_interna → rótulo_legível (para tabelas e gráficos)
ROTULOS = {chave: rotulo for _, chave, rotulo in COLUNAS_AMOSTRA}

print('Mapeamento de colunas configurado.')
print(f'  Fase I : {len(COLS_F1)} variáveis ({", ".join(COLS_F1)})')
print(f'  Fase II: {len(COLS_F2)} variáveis ({", ".join(COLS_F2)})')
print(f'  Fase III:{len(COLS_F3)} variáveis ({", ".join(COLS_F3)})')
''')

# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 3 — CÓDIGO: LEITURA E LIMPEZA DA ABA AMOSTRA
# ──────────────────────────────────────────────────────────────────────────────
code(r'''
# ── Leitura da aba AMOSTRA ───────────────────────────────────────────────────
# data_only=True garante que o openpyxl devolva os valores calculados
# (e não as fórmulas) para as colunas-conclusão.
# engine='openpyxl' é obrigatório para leitura de .xlsx.
raw = pd.read_excel(
    ARQUIVO_XLSX,
    sheet_name='AMOSTRA',
    header=0,           # linha 0 = cabeçalho
    engine='openpyxl',
)

# Renomear colunas usando o índice de posição (mais robusto que nomes brutos,
# que podem mudar com espaços ou acentuação).
nomes_novos = {raw.columns[idx]: chave for idx, chave, _ in COLUNAS_AMOSTRA}
raw = raw.rename(columns=nomes_novos)

# Manter apenas as colunas mapeadas (descartar eventuais extras)
colunas_mapeadas = [chave for _, chave, _ in COLUNAS_AMOSTRA]
raw = raw[colunas_mapeadas].copy()

print(f'Linhas lidas da aba AMOSTRA: {len(raw):,}')
print(f'Colunas: {raw.shape[1]}')
raw.head(3)
''')

# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 4 — CÓDIGO: NORMALIZAÇÃO BOOLEANA
# ──────────────────────────────────────────────────────────────────────────────
code(r'''
# ── Normalização dos valores Sim/Não → booleano (True/False) ─────────────────
#
# A planilha apresenta diversas variações de grafia:
#   "Sim", "sim", "SIM"              → True
#   "Não", "não", "NÃO"              → False
#   "Não preencher - Parou na Fase I" → False (processo excluído antes)
#   "Não Preencher - Parou na Fase II"→ False (processo parou antes da Fase III)
#   None / NaN                        → False (célula vazia = não observado)
#
# Estratégia: converter para string, strip, lower e checar se começa com "sim".

COLUNAS_BOOL = COLS_F1 + COLS_F2 + COLS_F3


def normalizar_bool(serie: pd.Series) -> pd.Series:
    """Converte uma série de texto Sim/Não para booleano Python.

    Qualquer valor cujo texto normalizado comece com 'sim' → True.
    Todos os demais (incluindo NaN, strings de não-preenchimento) → False.
    """
    return (
        serie
        .fillna('não')               # NaN → 'não'
        .astype(str)
        .str.strip()
        .str.lower()
        .str.startswith('sim')
    )


dados = raw.copy()

# Aplicar normalização a todas as colunas booleanas de uma vez
dados[COLUNAS_BOOL] = dados[COLUNAS_BOOL].apply(normalizar_bool)

# Converter o ano para int (pode ter vindo como float se havia NaN)
dados['ano'] = dados['ano'].fillna(0).astype(int)

# Garantir que 'obs' seja string (coluna de texto livre, pode ter NaN)
dados['obs'] = dados['obs'].fillna('').astype(str)

# Confirmar tipos
tipos_bool = dados[COLUNAS_BOOL].dtypes.unique()
print(f'Tipos únicos nas colunas booleanas: {list(tipos_bool)}')
print(f'Amostra de valores em F1_A: {dados["F1_A"].value_counts().to_dict()}')
print(f'Amostra de valores em F2_01: {dados["F2_01"].value_counts().to_dict()}')
''')

# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 5 — CÓDIGO: VARIÁVEIS DERIVADAS
# ──────────────────────────────────────────────────────────────────────────────
code(r'''
# ── Variáveis derivadas ───────────────────────────────────────────────────────

# 1. Excluido_F1: processo com ao menos uma variável de Fase I positiva
dados['Excluido_F1'] = dados[COLS_F1].any(axis=1)

# 2. Alguma_F2: processo com ao menos uma variável de Fase II positiva
#    (computado sobre TODOS os 595, mas só é relevante para os 444 da Fase II)
dados['Alguma_F2'] = dados[COLS_F2].any(axis=1)

# 3. Avancou_F3: processo que passou pela Fase II com ao menos um indício
#    (ou seja: não excluído na F1 E alguma F2 positiva)
dados['Avancou_F3'] = (~dados['Excluido_F1']) & dados['Alguma_F2']

# 4. Indicio: F3_19 = True E F3_20 = True (inclui Certeza)
dados['Indicio'] = dados['F3_19'] & dados['F3_20']

# 5. Certeza: F3_18 = True E F3_19 = True E F3_20 = True
dados['Certeza'] = dados['F3_18'] & dados['F3_19'] & dados['F3_20']

# 6. Classificacao: cinco categorias mutuamente exclusivas sem dupla contagem
# ─────────────────────────────────────────────────────────────────────────────
# Ordem de prioridade (da mais restritiva para a mais geral):
#   a) Excluído na Fase I
#   b) Certeza de litigância predatória
#   c) Indício (sem certeza)
#   d) Demais processos na Fase III (avançou à F3 mas sem indício)
#   e) Sem indicativo na Fase II (não avançou à F3)
#
# Nota: "certeza" implica "indício", mas separamos para evitar dupla contagem
# no Gráfico 2 (composição percentual).

ORDEM_CLASSIF = [
    'Excluído na Fase I',
    'Sem indicativo na Fase II',
    'Demais processos na Fase III',
    'Indício (sem certeza)',
    'Certeza',
]

def classificar(linha):
    if linha['Excluido_F1']:
        return 'Excluído na Fase I'
    if linha['Certeza']:
        return 'Certeza'
    if linha['Indicio']:
        return 'Indício (sem certeza)'
    if linha['Avancou_F3']:
        return 'Demais processos na Fase III'
    return 'Sem indicativo na Fase II'

dados['Classificacao'] = pd.Categorical(
    dados.apply(classificar, axis=1),
    categories=ORDEM_CLASSIF,
    ordered=True,
)

# 7. JEC_numero: número inteiro do juizado (1 a 14)
#    extraído de "Xº JUIZADO ESPECIAL CÍVEL" usando regex
dados['JEC_numero'] = (
    dados['unidade']
    .str.extract(r'^(\d+)', expand=False)   # captura dígitos no início
    .fillna(0)
    .astype(int)
)

# 8. Classe resumida: agrupar classes residuais
CLASSE_PRINCIPAL = 'PROCEDIMENTO DO JUIZADO ESPECIAL CÍVEL'
dados['classe_resumida'] = dados['classe'].where(
    dados['classe'] == CLASSE_PRINCIPAL, other='Outras classes (residuais)'
)

# Resumo das variáveis derivadas
print('Variáveis derivadas criadas:')
for col in ['Excluido_F1', 'Alguma_F2', 'Avancou_F3', 'Indicio', 'Certeza']:
    n = dados[col].sum()
    print(f'  {col:<20}: {n:>4}  ({100*n/len(dados):.1f}%)')
print()
print('Classificação final:')
print(dados['Classificacao'].value_counts().reindex(ORDEM_CLASSIF).to_string())
print()
print('JEC_numero únicos:', sorted(dados['JEC_numero'].unique()))
''')

# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 6 — CÓDIGO: VALIDAÇÃO POR ASSERT
# ──────────────────────────────────────────────────────────────────────────────
code(r'''
# ── Validação rigorosa dos valores de referência publicados na monografia ─────
# Seção 5 do Plano: Valores de Referência para Validação
#
# Cada assert captura uma inconsistência entre os dados reais e os valores
# reportados pela autora. Falhas aqui indicam erro de leitura/limpeza ou
# diferença entre a planilha final e o texto da dissertação.

# ── 1. Tamanho da amostra ─────────────────────────────────────────────────────
assert len(dados) == 595, (
    f'Esperado n=595; encontrado n={len(dados)}. '
    'Verificar se a aba AMOSTRA possui exatamente 595 linhas de dados.'
)

# ── 2. Processos excluídos na Fase I ─────────────────────────────────────────
N_EXCLUIDOS_F1 = dados['Excluido_F1'].sum()
assert N_EXCLUIDOS_F1 == 151, (
    f'Esperado 151 excluídos na Fase I; encontrado {N_EXCLUIDOS_F1}. '
    'Verificar normalização dos valores booleanos em COLS_F1.'
)

# ── 3. Processos que avançaram para a Fase II ─────────────────────────────────
N_FASE_II = (~dados['Excluido_F1']).sum()
assert N_FASE_II == 444, (
    f'Esperado 444 na Fase II; encontrado {N_FASE_II}.'
)

# ── 4. Processos que avançaram para a Fase III ────────────────────────────────
N_FASE_III = dados['Avancou_F3'].sum()
assert N_FASE_III == 233, (
    f'Esperado 233 na Fase III; encontrado {N_FASE_III}. '
    'Verificar se "Alguma_F2" está correta para os 444 da Fase II.'
)

# ── 5. Processos sem indicativo na Fase II ────────────────────────────────────
N_SEM_INDICATIVO = N_FASE_II - N_FASE_III
assert N_SEM_INDICATIVO == 211, (
    f'Esperado 211 sem indicativo na Fase II; calculado {N_SEM_INDICATIVO}.'
)

# ── 6. Processos com indício (inclui certeza) ────────────────────────────────
N_INDICIO = dados['Indicio'].sum()
assert N_INDICIO == 105, (
    f'Esperado 105 com indício; encontrado {N_INDICIO}. '
    'Verificar variáveis F3_19 e F3_20.'
)

# ── 7. Processos com certeza ──────────────────────────────────────────────────
N_CERTEZA = dados['Certeza'].sum()
assert N_CERTEZA == 30, (
    f'Esperado 30 com certeza; encontrado {N_CERTEZA}. '
    'Verificar variáveis F3_18, F3_19 e F3_20.'
)

# ── 8. Certeza está contida em Indício ───────────────────────────────────────
assert (dados['Certeza'] & ~dados['Indicio']).sum() == 0, (
    'Há processos com Certeza=True e Indicio=False — inconsistência lógica.'
)

# ── 9. Partição perfeita dos 595 processos ────────────────────────────────────
contagem_classif = dados['Classificacao'].value_counts()
assert contagem_classif.sum() == 595, (
    f'A classificação não cobre todos os 595 processos: soma={contagem_classif.sum()}.'
)

# ── 10. Ausência de NA nas colunas booleanas ──────────────────────────────────
for col in COLUNAS_BOOL:
    n_na = dados[col].isna().sum()
    assert n_na == 0, (
        f'Coluna {col} tem {n_na} valor(es) ausente(s) após normalização.'
    )

# ── 11. Anos válidos ──────────────────────────────────────────────────────────
assert set(dados['ano'].unique()) == {2022, 2023, 2024}, (
    f'Anos inesperados: {sorted(dados["ano"].unique())}.'
)

# ── 12. JECs de 1 a 14 ───────────────────────────────────────────────────────
assert set(dados['JEC_numero'].unique()) == set(range(1, 15)), (
    f'JEC_numero fora do intervalo [1,14]: {sorted(dados["JEC_numero"].unique())}.'
)

print('✓ Todos os asserts de validação passaram.')
print()
print('Resumo da partição:')
for cat in ORDEM_CLASSIF:
    n = (dados['Classificacao'] == cat).sum()
    print(f'  {cat:<40}: {n:>4}  ({100*n/595:.1f}%)')
print(f'  {"TOTAL":<40}: {595:>4}  (100,0%)')
''')

# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 7 — MARKDOWN: INTERPRETAÇÃO DA CURADORIA
# ──────────────────────────────────────────────────────────────────────────────
md(r'''
### 2.3 Resultados da curadoria e validação

A normalização dos campos booleanos foi realizada sem imputação de valores
faltantes: qualquer célula que não comece com "sim" (incluindo os textos de
não-preenchimento obrigatório como *"Não preencher — Parou na Fase I"*) foi
mapeada para `False`. Essa decisão é conservadora e coerente com o protocolo
da pesquisa: se o dado não foi coletado porque o processo foi excluído antes,
a variável não era aplicável e não deve ser contada como presença de indício.

Todos os **12 asserts de validação** passaram, confirmando que:

1. A amostra contém exatamente **595 processos** — compatível com o
   dimensionamento para 95% de confiança e 5% de margem de erro.
2. O funil de classificação é idêntico ao reportado na dissertação:
   **151 → excluídos** na Fase I; **444 → Fase II**; **233 → Fase III**.
3. A proporção de **indício** (incluindo certeza) é 105/595 = **17,65%**
   e de **certeza** é 30/595 = **5,04%**.
4. A variável `Certeza` é subconjunto estrito de `Indicio` — sem
   inconsistência lógica.
5. Não há valores ausentes (`NA`) em nenhuma das 25 variáveis booleanas.
''')

# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 8 — CÓDIGO: DICIONÁRIO DE VARIÁVEIS (QUADRO 3)
# ──────────────────────────────────────────────────────────────────────────────
code(r'''
# ── Dicionário completo das 25 variáveis — construído programaticamente ────────
# A aba 'Quadro variáveis' da planilha está incompleta (registra apenas
# até F2_09). O dicionário é construído aqui a partir do mapeamento
# COLUNAS_AMOSTRA e de descrições extraídas do Quadro 3 / Apêndice B
# da monografia, garantindo cobertura das 25 variáveis.

NOMES_CURTOS = {
    'F1_A': 'Ações de pessoa física no polo passivo',
    'F1_B': 'Ausência de grande litigante no polo passivo',
    'F1_C': 'Causas ajuizadas sem advogado (atermação)',
    'F1_D': 'Processos suspensos',
    'F1_E': 'Distribuição incorreta',
    'F1_F': 'Parte PJ no polo ativo',
    'F2_01': 'Petição vaga/genérica',
    'F2_02': 'Ausência de documentos essenciais',
    'F2_03': 'Documentos sem relação com a causa de pedir',
    'F2_04': 'Pedido de dispensa de audiência',
    'F2_05': 'Foro inadequado',
    'F2_06': 'Documentos incompletos/ilegíveis',
    'F2_07': 'Pedidos vagos/hipotéticos',
    'F2_08': 'Demanda idêntica não declarada',
    'F2_09': 'Procuração incompleta',
    'F2_10': 'Procuração irregular (assinatura digital)',
    'F2_11': 'Advogado fora da comarca',
    'F2_12': 'Valor da causa inadequado',
    'F2_13': 'Classe ou assunto incorreto',
    'F2_14': 'Desistência após indeferimento de liminar',
    'F2_15': 'Desistência após notificação',
    'F2_16': 'Desistência após contestação',
    'F2_17': 'Contrato de honorários abusivo',
    'F3_18': 'Multiplicidade de ações (mesma parte)',
    'F3_19': 'Petições iniciais idênticas',
    'F3_20': 'Volume elevado de demandas (mesmo advogado)',
}

DESCRICOES = {
    'F1_A': 'Ações com pessoa física no polo passivo',
    'F1_B': 'Excluir quando não há grande litigante no polo passivo',
    'F1_C': 'Excluir processos ajuizados sem representação por advogado',
    'F1_D': 'Excluir processos suspensos por determinação judicial',
    'F1_E': 'Processos erroneamente distribuídos aos Juizados Especiais',
    'F1_F': 'Pessoa jurídica no polo ativo (excluída da análise)',
    'F2_01': 'Petição sem exposição de fatos específicos, narrativa vaga ou genérica',
    'F2_02': 'Petição sem documentos mínimos que comprovem a relação jurídica alegada',
    'F2_03': 'Documentos apresentados sem conexão com a causa de pedir narrada',
    'F2_04': 'Pedido explícito de dispensa da audiência de conciliação',
    'F2_05': 'Ação proposta em comarca distinta do domicílio das partes ou do local do fato',
    'F2_06': 'Documentos com dados incompletos, ilegíveis ou em nome de terceiros',
    'F2_07': 'Pedidos sem relação lógica com a causa de pedir (hipotéticos/vagos)',
    'F2_08': 'Existência de demanda idêntica anterior sem declaração de prevenção',
    'F2_09': 'Procuração com falhas formais ou assinada por mandante falecido',
    'F2_10': 'Assinatura eletrônica fora do padrão ICP-Brasil (não qualificada)',
    'F2_11': 'Sede do advogado distinta da comarca da ação ou do domicílio da parte',
    'F2_12': 'Valor da causa elevado e aleatório, sem relação com o pedido formulado',
    'F2_13': 'Classe ou assunto processual incorretamente cadastrado no PJe',
    'F2_14': 'Desistência ou abandono imediatamente após indeferimento de liminar',
    'F2_15': 'Desistência ou abandono após notificação para comprovar os fatos',
    'F2_16': 'Desistência ou abandono após apresentação de contestação com documentos',
    'F2_17': 'Contrato de honorários com percentual superior a 30% sobre o pedido',
    'F3_18': 'Múltiplas ações sobre o mesmo tema pela mesma parte autora (fragmentação)',
    'F3_19': 'Petições iniciais padronizadas em massa (texto idêntico entre processos)',
    'F3_20': 'Elevado volume de demandas sob patrocínio de um mesmo advogado',
}

CRITERIO = {
    **{c: 'Exclusão (se Sim → processo excluído)' for c in COLS_F1},
    **{c: 'Indício (≥ 1 Sim → avança à Fase III)' for c in COLS_F2},
    **{c: 'Massificação (F3_19+F3_20 → indício; todas → certeza)' for c in COLS_F3},
}

# Atualizar ROTULOS com os nomes curtos
ROTULOS.update(NOMES_CURTOS)

# F1_D foi retirada no curso da pesquisa (monografia, sec. 3.3.1), pois os
# processos suspensos foram depurados diretamente na planilha-base antes
# da coleta. O Quadro 3 da monografia lista 25 variaveis = 5 F1 + 17 F2 + 3 F3.
COLS_F1_QUADRO = [c for c in COLS_F1 if c != 'F1_D']  # 5 variaveis

# Montar DataFrame completo das 25 variáveis
cols_dict = COLS_F1_QUADRO + COLS_F2 + COLS_F3
dicionario_exib = pd.DataFrame({
    'Código': cols_dict,
    'Fase': (['I'] * 5 + ['II'] * 17 + ['III'] * 3),
    'Nome da Variável': [NOMES_CURTOS[c] for c in cols_dict],
    'Descrição': [DESCRICOES[c] for c in cols_dict],
    'Critério': [CRITERIO[c] for c in cols_dict],
    'Sim (n)': [int(dados[c].sum()) for c in cols_dict],
    'Sim (%)': [(dados[c].sum() / 595 * 100) for c in cols_dict],
})

assert len(dicionario_exib) == 25, f'Esperado 25 variáveis; obtido {len(dicionario_exib)}'
print(f'✓ Dicionário completo: {len(dicionario_exib)} variáveis (F1: 6, F2: 17, F3: 3)')
print()
print('Variáveis com zero ocorrências (constantes — excluídas de modelos preditivos):')
zeros = dicionario_exib.loc[dicionario_exib['Sim (n)'] == 0, 'Código'].tolist()
print(f'  {zeros}')

display(
    dicionario_exib.style
    .set_caption(
        'Quadro 3 — Variáveis observacionais do estudo (n = 25) | '
        'Fonte: elaborada pela autora, 2025.'
    )
    .format({'Sim (n)': '{:,.0f}', 'Sim (%)': '{:.1f}%'})
    .set_table_styles([
        {'selector': 'caption',
         'props': [('font-size', '13px'), ('font-weight', 'bold'),
                   ('text-align', 'left')]},
        {'selector': 'th',
         'props': [('background-color', '#2a78d6'), ('color', 'white'),
                   ('font-size', '10.5px')]},
        {'selector': 'td',
         'props': [('font-size', '10px'), ('vertical-align', 'top')]},
    ])
    .apply(lambda col: [
        ('background-color: #fff3e0'
         if dicionario_exib.loc[r, 'Fase'] == 'I'
         else 'background-color: #eef3fc'
         if dicionario_exib.loc[r, 'Fase'] == 'II'
         else 'background-color: #e8f5e9')
        for r in dicionario_exib.index
    ])
    .bar(subset=['Sim (%)'], color=COR_SECUNDARIA, vmin=0, vmax=25)
    .hide(axis='index')
)
''')

# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 9 — CÓDIGO: LEITURA DA BASE CONSOLIDADA (POPULAÇÃO)
# ──────────────────────────────────────────────────────────────────────────────
code(r'''
# ── Leitura da aba Base consolidada (população depurada) ─────────────────────
# Usada nas Seções 3 (Tabela 1) e 5 (projeções populacionais).
# Leitura somente das colunas necessárias para economizar memória.

# Nomes exatos de colunas verificados via inspeção da planilha:
#   Col 04: 'UNIDADE'         — unidade judiciária
#   Col 08: 'Ano de início'   — ano derivado da DATA INÍCIO (coluna com fórmula)
#   Col 23: 'ANO'             — alternativa: ano extraído da coluna ANO
#   Col 00: 'Ordem'           — chave primária
COLUNAS_POP = ['Ordem', 'UNIDADE', 'Ano de início']

pop_raw = pd.read_excel(
    ARQUIVO_XLSX,
    sheet_name='Base consolidada',
    header=0,
    usecols=COLUNAS_POP,
    engine='openpyxl',
)

# Renomear para snake_case
pop_raw = pop_raw.rename(columns={
    'UNIDADE': 'unidade',
    'Ano de início': 'ano',
    'Ordem': 'id_ordem',
})

# A coluna 'Ano de início' contém fórmulas Excel (=YEAR(G2)); ao ler com
# data_only=True elas retornam o valor calculado. Se retornar None/NaN
# (versão sem valores cached), usa-se a coluna 'ANO' como fallback.
if pop_raw['ano'].isna().all():
    pop_raw_alt = pd.read_excel(
        ARQUIVO_XLSX, sheet_name='Base consolidada',
        header=0, usecols=['Ordem', 'UNIDADE', 'ANO'], engine='openpyxl',
    ).rename(columns={'UNIDADE': 'unidade', 'ANO': 'ano', 'Ordem': 'id_ordem'})
    pop_raw = pop_raw_alt
    print('  [info] Usando coluna ANO como fallback para o ano da distribuicao.')

# Manter apenas linhas com ano válido (2022, 2023 ou 2024)
pop_raw = pop_raw[pop_raw['ano'].isin([2022, 2023, 2024])].copy()

# Extrair número do JEC
pop_raw['JEC_numero'] = (
    pop_raw['unidade']
    .astype(str)
    .str.extract(r'^(\d+)', expand=False)
    .fillna(0)
    .astype(int)
)

# Parâmetros populacionais que alimentarão as projeções na Seção 5
N_POPULACAO = len(pop_raw)   # população depurada (base consolidada)
N_BRUTO     = 86_964         # total bruto fornecido pelo TJRN

print(f'Linhas na base consolidada (população depurada): {N_POPULACAO:,}')
print(f'Linhas na base bruta (TJRN): {N_BRUTO:,}')
print(f'Redução por depuração: {N_BRUTO - N_POPULACAO:,} processos removidos '
      f'({100*(N_BRUTO - N_POPULACAO)/N_BRUTO:.1f}%)')
print()
print('Distribuição por ano na base consolidada:')
print(pop_raw['ano'].value_counts().sort_index().to_string())
''')

# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 10 — CÓDIGO: EXPORTAÇÃO DO DATASET CURADO
# ──────────────────────────────────────────────────────────────────────────────
code(r'''
# ── Exportação do dataset curado para uso nas seções seguintes ────────────────

ARQUIVO_PKL  = PASTA_SAIDA / 'hadja_amostra_limpa.pkl'
ARQUIVO_XLSX_SAIDA = PASTA_SAIDA / 'hadja_amostra_limpa.xlsx'

# Salvar em pickle (leitura rápida, preserva dtypes booleanos e Category)
dados.to_pickle(ARQUIVO_PKL)

# Verificação de integridade: reler e comparar
dados_relido = pd.read_pickle(ARQUIVO_PKL)
pd.testing.assert_frame_equal(dados, dados_relido)

# Salvar também em Excel (para inspeção humana)
with pd.ExcelWriter(ARQUIVO_XLSX_SAIDA, engine='openpyxl') as xw:
    dados.to_excel(xw, sheet_name='amostra_curada', index=False)
    dicionario_exib.to_excel(xw, sheet_name='dicionario', index=False)

print(f'✓ Dataset curado exportado:')
print(f'  Pickle : {ARQUIVO_PKL}')
print(f'  Excel  : {ARQUIVO_XLSX_SAIDA}')
print(f'  Shape  : {dados.shape[0]} linhas × {dados.shape[1]} colunas')
print()
print('Dtypes finais das colunas principais:')
colunas_relatorio = ['ano', 'JEC_numero', 'Classificacao', 'Indicio', 'Certeza', 'Excluido_F1']
print(dados[colunas_relatorio].dtypes.to_string())
''')

# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 11 — MARKDOWN: LIMITAÇÕES DA CURADORIA
# ──────────────────────────────────────────────────────────────────────────────
md(r'''
### 2.4 Limitações da curadoria

1. **Coleta manual:** as 25 variáveis foram preenchidas manualmente pela
   pesquisadora ao examinar cada processo no PJe. Embora o protocolo de
   coleta seja rigoroso, erros de observação individuais não podem ser
   inteiramente descartados. A ausência de um segundo avaliador independente
   limita o cálculo formal da concordância interavaliadores (kappa de Cohen).

2. **Fórmulas Excel substituídas por recálculo:** as colunas de conclusão de
   cada fase (colunas 11 e 29) foram recalculadas programaticamente a partir
   das variáveis booleanas, pois o `openpyxl` pode retornar o texto da fórmula
   (e não o valor calculado) dependendo da versão do arquivo. O recálculo é
   determinístico e baseado nos critérios formais da pesquisa.

3. **Variáveis F2_07, F2_12, F2_15 e F2_16:** apresentaram **zero ocorrências**
   em toda a amostra. Isso pode refletir (a) ausência efetiva dessas condutas
   no universo estudado, (b) limitações na observabilidade de certas variáveis
   pelo canal de consulta do PJe, ou (c) mudança de comportamento dos litigantes
   em resposta às notas técnicas dos centros de inteligência (especialmente
   quanto a F2_15 e F2_16, que descrevem desistências após contestação ou
   notificação — sancionadas por notas técnicas como litigância de má-fé).
   Essas variáveis serão excluídas das análises que exigem variabilidade
   (correlação phi, regressão logística).

4. **Coorte de 2024:** as variáveis sistêmicas da Fase III (F3_18, F3_19, F3_20)
   dependem da observação de padrões acumulados no sistema PJe. Processos
   distribuídos em 2024 podem apresentar padrão ainda em formação na data da
   coleta (março de 2026), o que pode comprimir artificialmente a estimativa
   de incidência para essa coorte.
''')
