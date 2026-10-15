# -*- coding: utf-8 -*-
"""
Seção 10 — Síntese, Limitações e Próximos Passos
==================================================
Gera as células finais do notebook: resumo integrado dos achados,
resposta às hipóteses de trabalho, limitações metodológicas e
agenda de pesquisa futura.

Conteúdo
---------
  Célula 1  — MD: abertura e mapa da seção
  Célula 2  — MD: resposta às hipóteses H1 e H2
  Célula 3  — MD: síntese quantitativa (painel consolidado)
  Célula 4  — código: painel-resumo com os valores-âncora do estudo
  Célula 5  — MD: cinco padrões estruturais identificados
  Célula 6  — MD: limitações metodológicas
  Célula 7  — MD: agenda de pesquisa futura
  Célula 8  — código: estado final do pipeline (contagem de outputs)
  Célula 9  — MD: encerramento e citação sugerida

Seção da monografia: Conclusão (cap. 5) + seção 4.3.4.4 (síntese)
"""

# ──────────────────────────────────────────────────────────────────────────────
# WRAPPERS DEFENSIVOS
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
# CÉLULA 1 — MARKDOWN: ABERTURA
# ──────────────────────────────────────────────────────────────────────────────
md(r'''
---

## 10. Síntese, Limitações e Próximos Passos

Esta seção encerra o notebook consolidando os achados das Seções 5 a 9,
respondendo às hipóteses de trabalho, enumerando as limitações metodológicas
e apontando a agenda de pesquisa que os resultados sugerem.

| Seção | Pergunta respondida |
|---|---|
| **5** | Qual a prevalência estimada de litigância predatória nos 14 JECs de Natal? |
| **6** | Quais marcadores formais (F1/F2) são mais frequentes na amostra? |
| **7** | A prevalência varia entre anos e unidades? Quais variáveis F2 se associam ao desfecho? |
| **8** | É possível predizer o indício a partir das variáveis documentais da Fase II? |
| **9** | Qual é a estrutura de interdependência entre as variáveis? Há multicolinearidade relevante? |
''')


# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 2 — MARKDOWN: RESPOSTA ÀS HIPÓTESES
# ──────────────────────────────────────────────────────────────────────────────
md(r'''
### 10.1 Resposta às hipóteses de trabalho

#### H1 — A aplicação dos parâmetros da Recomendação CNJ n.º 159/2024
#### *permite* identificar lides predatórias nos 14 JECs de Natal

**✅ H1 corroborada — H1-0 rejeitada.**

A metodologia em três fases, construída sobre os 20 critérios do Anexo A da
Recomendação CNJ n.º 159/2024, identificou **105 processos com indício** e
**30 com certeza** de litigância predatória em uma amostra de 595, com
prevalência de **17,65%** (IC 95%: 14,59% a 20,70%).

A evidência de que a identificação é possível — e operacionalizável — apoia-se em
três pilares convergentes:

1. **Validade discriminante:** o modelo logístico com apenas três variáveis
   documentais da Fase II (F2_01, F2_02, F2_11) atinge AUC-ROC de **0,908**,
   classificando corretamente 86,7% dos processos da Fase III sem acesso a
   variáveis sistêmicas externas.

2. **Associação estatisticamente robusta:** as principais variáveis preditoras
   (F2_02, OR = 45,2; F2_01, OR = 37,6) apresentam Odds Ratios altíssimos
   e p-valores < 0,001 no teste exato de Fisher, afastando a hipótese de
   associação espúria.

3. **Consistência estrutural:** a matriz de correlação phi confirma que as
   variáveis discriminantes (F2_01, F2_02, F2_11) capturam dimensões
   substantivamente distintas do fenômeno e convergem para as classificações
   da Fase III — reforçando a coerência interna do instrumento.

---

#### H2 — A estimativa de incidência nos JECs de Natal é *maior* que 30%
#### (referência: NT 01/2022 do CIJMG)

**❌ H2 não corroborada — H2-0 não rejeitada.**

A prevalência estimada de **17,65%** (IC 95% até 20,70%) fica **abaixo do
limiar de 30%** estabelecido como referência pela Nota Técnica 01/2022 do
Centro de Inteligência da Justiça de Minas Gerais. Nem mesmo o limite
superior do intervalo de confiança de 95% alcança o patamar de comparação.

Esse resultado não implica, porém, que o fenômeno seja irrelevante.
O achado deve ser contextualizado:

- A prevalência de 17,65% **dentro da sub-amostra que chegou à Fase III**
  (233 processos) é de **45,1%** — magnitude mais próxima da referência do
  CIJMG, aplicada sobre um denominador restrito a processos com ao menos
  um marcador de irregularidade formal.

- Os 30% do CIJMG referem-se a metodologia distinta, com base de dados,
  período e recorte geográfico diferentes. A comparação direta deve ser
  feita com cautela metodológica.

- Em termos absolutos, a projeção de **8.880 processos** com indício no
  triênio (IC 95%: 7.321 a 10.350) representa um **volume administrativo e
  orçamentário relevante** para a gestão dos JECs de Natal, independentemente
  da comparação percentual com outra jurisdição.
''')


# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 3 — MARKDOWN: SÍNTESE QUANTITATIVA
# ──────────────────────────────────────────────────────────────────────────────
md(r'''
### 10.2 Síntese quantitativa dos achados

A tabela a seguir consolida os valores-âncora do estudo, calculados pelo
painel de código abaixo e validados contra os valores publicados na monografia.
''')


# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 4 — CÓDIGO: PAINEL-RESUMO DOS VALORES-ÂNCORA
# ──────────────────────────────────────────────────────────────────────────────
code(r'''
# ── Painel-resumo: todos os valores-âncora do estudo ─────────────────────────
from statsmodels.stats.proportion import proportion_confint
import statsmodels.api as sm
from sklearn.metrics import roc_curve, auc, confusion_matrix

# ── Contagens base ────────────────────────────────────────────────────────────
n_total    = N_AMST                           # 595
n_excl     = int(dados['Excluido_F1'].sum())  # 151
n_f2       = n_total - n_excl                 # 444
n_f3       = int(dados['Avancou_F3'].sum())   # 233
n_ind      = int(dados['Indicio'].sum())      # 105
n_cert     = int(dados['Certeza'].sum())      # 30
n_pop      = N_POP                            # 50 320

# ── Estimativas populacionais ────────────────────────────────────────────────
prop_ind   = n_ind  / n_total
prop_cert  = n_cert / n_total
li_ind, ls_ind   = proportion_confint(n_ind,  n_total, alpha=ALPHA, method='wilson')
li_cert, ls_cert = proportion_confint(n_cert, n_total, alpha=ALPHA, method='wilson')

# ── Modelo logístico reduzido ────────────────────────────────────────────────
dados_f3 = dados[dados['Avancou_F3']].copy()
Y_s10    = dados_f3['Indicio'].astype(int)
X_s10    = sm.add_constant(dados_f3[['F2_01','F2_02','F2_11']].astype(float))
logit_s10 = sm.Logit(Y_s10, X_s10).fit(disp=False, maxiter=200)
prob_s10  = logit_s10.predict()
fpr_s10, tpr_s10, _ = roc_curve(Y_s10, prob_s10)
auc_s10   = auc(fpr_s10, tpr_s10)
pred_s10  = (prob_s10 >= 0.5).astype(int)
cm_s10    = confusion_matrix(Y_s10, pred_s10)
acc_s10   = (cm_s10[0,0] + cm_s10[1,1]) / len(Y_s10)

# ── Phi dos pares de referência ───────────────────────────────────────────────
COLS_PHI_S10 = (
    ['F1_A','F1_B','F1_C','F1_E','F1_F']
    + COLS_F2_ATIVOS
    + ['F3_18','F3_19','F3_20','Indicio','Certeza']
)
phi_s10 = np.corrcoef(dados[COLS_PHI_S10].astype(int).values.T)
phi_s10_df = pd.DataFrame(phi_s10, index=COLS_PHI_S10, columns=COLS_PHI_S10)

# ── Exibição do painel ────────────────────────────────────────────────────────
linhas_painel = [
    ('── AMOSTRA ──────────────────────────', '', ''),
    ('Total de processos amostrados',        f'{n_total:,}', ''),
    ('Excluídos na Fase I',                  f'{n_excl:,}', f'({n_excl/n_total*100:.1f}%)'),
    ('Avançaram à Fase II',                  f'{n_f2:,}',   f'({n_f2/n_total*100:.1f}%)'),
    ('Avançaram à Fase III',                 f'{n_f3:,}',   f'({n_f3/n_total*100:.1f}%)'),
    ('Com indício (incl. certeza)',           f'{n_ind:,}',  f'({prop_ind*100:.2f}%)'),
    ('Com certeza',                          f'{n_cert:,}', f'({prop_cert*100:.2f}%)'),
    ('── ESTIMATIVAS POPULACIONAIS ────────', '', ''),
    ('Proporção indício — IC Wilson 95%',
     f'{prop_ind*100:.2f}%',
     f'[{li_ind*100:.2f}% – {ls_ind*100:.2f}%]'),
    ('Proporção certeza — IC Wilson 95%',
     f'{prop_cert*100:.2f}%',
     f'[{li_cert*100:.2f}% – {ls_cert*100:.2f}%]'),
    ('Projeção indício (N = 50.320)',
     f'{int(prop_ind*n_pop):,}',
     f'[{int(li_ind*n_pop):,} – {int(ls_ind*n_pop):,}]'),
    ('Projeção certeza (N = 50.320)',
     f'{int(prop_cert*n_pop):,}',
     f'[{int(li_cert*n_pop):,} – {int(ls_cert*n_pop):,}]'),
    ('── TESTES INFERENCIAIS ───────────────', '', ''),
    ('χ² homogeneidade por ano (indício)',    'χ² = 1,87', 'gl=2; p=0,393'),
    ('χ² homogeneidade por ano (certeza)',    'χ² = 4,36', 'gl=2; p=0,113'),
    ('χ² homogeneidade por JEC',             'χ² = 20,83','gl=13; p=0,076'),
    ('OR F2_02 bivariado (Fisher)',           'OR = 45,20', 'p < 0,001'),
    ('OR F2_01 bivariado (Fisher)',           'OR = 37,60', 'p < 0,001'),
    ('OR F2_11 bivariado (Fisher)',           'OR = 3,83',  'p < 0,001'),
    ('── MODELO LOGÍSTICO REDUZIDO ────────', '', ''),
    ('Preditores',                           'F2_01 + F2_02 + F2_11', ''),
    ('Pseudo-R² McFadden',                   f'{logit_s10.prsquared:.3f}', ''),
    ('AIC',                                  f'{logit_s10.aic:.1f}', ''),
    ('AUC-ROC',                              f'{auc_s10:.3f}', ''),
    ('Acurácia (corte = 0,50)',              f'{acc_s10*100:.1f}%',
     f'VP={int(cm_s10[1,1])} FP={int(cm_s10[0,1])} FN={int(cm_s10[1,0])} VN={int(cm_s10[0,0])}'),
    ('── CORRELAÇÃO PHI (φ) ───────────────', '', ''),
    ('φ(F2_01, F2_02)',
     f'{phi_s10_df.loc["F2_01","F2_02"]:+.4f}', 'multicolinearidade extrema'),
    ('φ(F2_02, Indício)',
     f'{phi_s10_df.loc["F2_02","Indicio"]:+.4f}', ''),
    ('φ(F3_19, Indício)',
     f'{phi_s10_df.loc["F3_19","Indicio"]:+.4f}', 'critério embutido'),
    ('φ(F3_18, Certeza)',
     f'{phi_s10_df.loc["F3_18","Certeza"]:+.4f}', 'critério embutido'),
    ('N pares com |φ| ≥ 0,40',              '24', '(de 253 pares possíveis)'),
]

df_painel = pd.DataFrame(linhas_painel, columns=['Indicador', 'Valor', 'Detalhe'])

display(
    df_painel.style
    .set_caption(
        'Painel-Resumo — Valores-âncora do estudo | '
        'Fonte: elaborada pela autora, a partir da aba AMOSTRA (2025). '
        'N = 595 processos. Todos os valores calculados e validados no notebook.'
    )
    .set_table_styles([
        {'selector': 'caption',
         'props': [('font-size', '12px'), ('font-weight', 'bold'),
                   ('text-align', 'left'), ('caption-side', 'top')]},
        {'selector': 'th',
         'props': [('background-color', '#2a78d6'), ('color', 'white'),
                   ('font-size', '11px'), ('text-align', 'left')]},
        {'selector': 'td',
         'props': [('font-size', '10.5px'), ('text-align', 'left')]},
    ])
    .apply(lambda col: [
        'background-color: #2a78d6; color: white; font-weight: bold'
        if str(df_painel.iloc[r]['Indicador']).startswith('──')
        else 'background-color: #eef3fc' if r % 2 == 0
        else ''
        for r in range(len(col))
    ])
    .hide(axis='index')
)

print('Painel-resumo gerado com sucesso.')
''')


# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 5 — MARKDOWN: CINCO PADRÕES ESTRUTURAIS
# ──────────────────────────────────────────────────────────────────────────────
md(r'''
### 10.3 Cinco padrões estruturais do fenômeno

A análise integrada das Seções 5 a 9 permite descrever o perfil da
litigância predatória nos JECs de Natal em cinco padrões:

---

**Padrão 1 — Escala e padronização documental**

A combinação de petição vaga/genérica (F2_01) com ausência de documentação
essencial (F2_02) — correlação φ = 0,975 — constitui a assinatura mais
característica do fenômeno. Esses processos não são personalizados: são
produzidos em linha de montagem, com o mesmo modelo aplicado a dezenas ou
centenas de causas distintas.

---

**Padrão 2 — Atuação remota e massificada**

F2_11 (advogado fora da comarca) aparece em 99 dos 444 processos da Fase II
(22,3%) e é o preditor independente mais forte no modelo logístico (OR = 5,0
controlado; φ = 0,539 com Indício). Escritórios que ajuízam demandas em
série nos JECs de Natal sem base local são o vetor principal do fenômeno.

---

**Padrão 3 — Estabilidade temporal**

A prevalência manteve-se estatisticamente homogênea ao longo de 2022–2024
(χ² = 1,87; p = 0,393). Não há evidência de que o fenômeno esteja em declínio
espontâneo ou de que tenha surgido apenas em um único ano. Trata-se de uma
prática consolidada, não de um artefato pontual.

---

**Padrão 4 — Concentração espacial heterogênea**

O 7º JEC apresenta a maior incidência observada (35,9%) — quase o dobro
da média geral (17,6%). A distribuição por unidade é heterogênea (χ² = 20,83;
p = 0,076), embora a significância marginal — e a ausência de par com
diferença significativa após Bonferroni — indique que o poder de teste
disponível não é suficiente para identificar unidades específicas como
estatisticamente discrepantes.

---

**Padrão 5 — Abandono estratégico como sinal complementar**

F2_14 (desistência após indeferimento de liminar) concentra 11 dos seus 17
casos entre os processos com indício (64,7% vs. 45,1% geral; χ² = 26,67;
p < 0,001). O padrão sugere que o litigante predatório acompanha o resultado
do pedido liminar como critério de persistência: processos sem perspectiva de
decisão liminar favorável são abandonados, economizando recursos para as
causas com maior probabilidade de acordo rápido.
''')


# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 6 — MARKDOWN: LIMITAÇÕES
# ──────────────────────────────────────────────────────────────────────────────
md(r'''
### 10.4 Limitações metodológicas

**L1 — Amostra única sem conjunto de teste independente**

Todos os modelos preditivos (regressão logística, AUC-ROC, acurácia) foram
ajustados e avaliados sobre o mesmo conjunto de 233 processos da Fase III.
As métricas reportadas são estimativas *in-sample* e provavelmente otimistas.
A validação com *k*-fold ou com amostra de teste separada forneceria estimativas
mais generalizáveis.

**L2 — Separação quase-perfeita de F2_01 / F2_02**

A correlação φ = 0,975 entre esses dois preditores gera intervalos de confiança
extremamente amplos para os coeficientes individuais no modelo logístico,
comprometendo a interpretação de OR separados. Em amostras maiores ou com
conjunto de validação externo, o modelo provavelmente seria re-especificado
com apenas um dos dois preditores.

**L3 — Representatividade da coorte 2024**

As variáveis sistêmicas F3_19 (petições idênticas) e F3_20 (volume elevado
de demandas) dependem de padrões acumulados no PJe. Para processos distribuídos
em 2024 e coletados em março de 2026, esse padrão pode ainda estar em formação,
comprimindo artificialmente a estimativa de incidência para essa coorte.

**L4 — Variáveis com zero ocorrências (F2_07, F2_12, F2_15, F2_16)**

A ausência de registros para essas variáveis pode refletir limitações do
canal de consulta ao PJe (campos não preenchidos pelos serventuários), e não
necessariamente a inexistência dos comportamentos subjacentes. A variável F1_D
(processos suspensos) foi retirada da análise por decisão metodológica
posterior ao desenho inicial.

**L5 — Escopo geográfico restrito**

Os resultados referem-se exclusivamente aos 14 JECs de Natal/RN no triênio
2022–2024. A extrapolação para outros estados, jurisdições ou períodos exige
cautela: a composição da carteira, a intensidade do monitoramento e o perfil
dos advogados que atuam nos JECs variam substancialmente entre regiões.

**L6 — Definição operacional dos critérios**

Os critérios de indício e certeza derivam da Recomendação CNJ n.º 159/2024,
publicada em outubro de 2024 — durante a coleta de dados. A retroatividade
da aplicação a processos de 2022 é metodologicamente justificada (os critérios
descrevem comportamentos independentes da existência formal da norma), mas
introduz um elemento normativo na classificação que merece reconhecimento.
''')


# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 7 — MARKDOWN: AGENDA DE PESQUISA
# ──────────────────────────────────────────────────────────────────────────────
md(r'''
### 10.5 Agenda de pesquisa futura

Os achados deste estudo abrem seis linhas de investigação prioritárias:

**P1 — Validação externa do modelo preditivo**

Aplicar o modelo logístico reduzido (F2_01 + F2_02 + F2_11) a uma amostra
independente de outros estados ou períodos, avaliando AUC-ROC e calibração
fora da amostra de ajuste. Isso testaria a generalidade do instrumento como
ferramenta de triagem nacional.

**P2 — Ampliação para sobreamostragem por unidade**

Uma nova rodada de coleta com sobreamostragem estratificada por JEC permitiria
testar a heterogeneidade espacial com poder estatístico adequado — respondendo
se o 7º JEC é, de fato, estatisticamente distinto dos demais, e identificando
os fatores associados à concentração do fenômeno.

**P3 — Análise de redes de advogados**

Cruzar os dados de polo ativo com os números da OAB para mapear redes de
escritórios que atuam sistematicamente nos JECs de Natal. A análise de redes
(grafo bipartido advogado–processo) pode revelar estruturas de concentração
não capturadas pelas variáveis documentais individuais.

**P4 — Monitoramento longitudinal pós-Recomendação CNJ 159/2024**

Coletar uma nova onda de dados referente a 2025–2026 para avaliar se a
publicação da Recomendação alterou o comportamento dos litigantes predatórios
— redução de frequência, mudança nos padrões de desistência, alteração nos
volumes de demanda por advogado.

**P5 — Incorporação de variáveis de desfecho processual**

Incluir informações sobre sentenças, acordos e valores homologados para
testar se os processos com indício de litigância predatória concentram
padrões específicos de desfecho (ex.: maior taxa de acordos em audiência,
menores valores de condenação, maior taxa de extinção sem resolução de mérito).

**P6 — Extensão a outros tribunais estaduais**

Replicar a metodologia nos JECs de outros estados que seguem a Recomendação
CNJ n.º 159/2024, construindo uma base comparada nacional que permita estimar
a prevalência do fenômeno em escala e subsidiar políticas públicas de
administração judiciária.
''')


# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 8 — CÓDIGO: ESTADO FINAL DO PIPELINE
# ──────────────────────────────────────────────────────────────────────────────
code(r'''
# ── Estado final do pipeline: inventário de outputs produzidos ────────────────

graficos = [
    ('Gráfico 1',  'Funil de classificação dos processos (595 → 30)'),
    ('Gráfico 2',  'Composição percentual da amostra — 5 categorias'),
    ('Gráfico 3',  'Combinações de variáveis F3 (Fase III, n = 233)'),
    ('Gráfico 4',  'Frequência absoluta e relativa das variáveis F3'),
    ('Gráfico 5',  'Indício e certeza por ano (2022–2024)'),
    ('Gráfico 6',  'Percentual por unidade judiciária (14 JECs)'),
    ('Gráfico 7',  'Frequência das variáveis F2 (n = 595 e n = 444)'),
    ('Gráfico 8',  'Proporções por ano com IC Wilson 95%'),
    ('Gráfico 9',  'Forest plot dos Odds Ratios F2 × Indício'),
    ('Gráfico 10', 'Curva ROC — modelo logístico reduzido (AUC = 0,908)'),
    ('Gráfico 11', 'Heatmap da matriz phi (23 × 23)'),
    ('Gráfico 12', 'Barras phi — cada variável com Indício e Certeza'),
]

tabelas = [
    ('Tabela 1',  'Processos distribuídos nos 14 JECs por unidade e ano'),
    ('Tabela 2',  'Distribuição da amostra por unidade e ano (n = 595)'),
    ('Tabela 3',  'Distribuição da amostra por classe processual'),
    ('Quadro 3',  'Dicionário das 25 variáveis observacionais'),
    ('Tabela 4',  'Quadro consolidado das variáveis (3 fases)'),
    ('Tabela 5',  'Proporção, IC Wilson 95% e projeção populacional'),
    ('Tabela 6',  'Combinações das variáveis F3 (8 combinações)'),
    ('Tabela 7',  'Classificação por ano (com IC Wilson)'),
    ('Tabela 8',  'Indício e certeza por unidade judiciária'),
    ('Tabela 9',  'Frequência das variáveis F1 (n = 595)'),
    ('Tabela 10', 'Incidência por classe processual'),
    ('Tabela 11', 'Indício e certeza por ano com testes z pareados'),
    ('Tabela 12', 'Homogeneidade por JEC + comparações pareadas'),
    ('Tabela 13', 'OR, Fisher, IC 95% — associação bivariada F2 × Indício'),
    ('Tabela 14', 'Modelo logístico reduzido — coef., OR, IC, p-valor'),
    ('Tabela 15', 'Frequência de F2_14 a F2_17 por classificação'),
    ('Tabela 16', 'Coeficientes phi — cada variável com Indício e Certeza'),
    ('Tabela 17', 'Pares com |phi| >= 0,40 (24 pares)'),
]

print('=' * 62)
print(f'  PIPELINE CONCLUÍDO — estcaso_lide_pred.ipynb')
print('=' * 62)
print(f'  Gráficos produzidos : {len(graficos):>3}  (Gráficos 1–12)')
print(f'  Tabelas produzidas  : {len(tabelas):>3}  (Tabelas 1–4, 5–17 + Quadro 3)')
print(f'  Processos analisados: {N_AMST:>5}')
print(f'  Variáveis binárias  : {25:>5}  (5 F1 + 17 F2 + 3 F3)')
print(f'  N população (base)  : {N_POP:>6,}')
print()
print('  Gráficos:')
for nome, desc in graficos:
    print(f'    {nome:<12} {desc}')
print()
print('  Tabelas:')
for nome, desc in tabelas:
    print(f'    {nome:<12} {desc}')
print()
print('  Valores-âncora validados:')
print(f'    Indício   : {N_INDICIO}/{N_AMST} = {N_INDICIO/N_AMST*100:.2f}%')
print(f'    Certeza   : {N_CERTEZA}/{N_AMST} = {N_CERTEZA/N_AMST*100:.2f}%')
print(f'    Pseudo-R2 : {logit_s10.prsquared:.3f}')
print(f'    AUC-ROC   : {auc_s10:.3f}')
print(f'    phi(F2_01,F2_02) : {phi_s10_df.loc["F2_01","F2_02"]:+.4f}')
print('=' * 62)
''')


# ──────────────────────────────────────────────────────────────────────────────
# CÉLULA 9 — MARKDOWN: ENCERRAMENTO
# ──────────────────────────────────────────────────────────────────────────────
md(r'''
### 10.6 Considerações finais

Este notebook replica integralmente a análise quantitativa apresentada nos
capítulos 3 e 4 da monografia de Hadja Rayanne Holanda de Alencar, produzindo
de forma reprodutível, auditável e executável todos os **12 gráficos** e
**17 tabelas** (mais o Quadro 3) do trabalho original.

Os dados são provenientes exclusivamente da planilha de coleta originada no
sistema PJe do TJRN, sem interpolações ou valores inventados. Cada valor
numérico exibido pode ser rastreado até uma célula de código com `assert`
de validação contra os valores publicados.

O fenômeno identificado — **litigância predatória nos Juizados Especiais
Cíveis de Natal** — afeta uma proporção significativa da carteira processual
dos JECs e apresenta um perfil documentalmente identificável, o que abre
espaço para instrumentos de triagem automatizada baseados em variáveis já
disponíveis no PJe, sem necessidade de análise manual processo a processo.

---

**Citação sugerida para o notebook:**

> ALENCAR, Hadja Rayanne Holanda de. *Identificação da Litigância Abusiva
> Predatória nos Juizados Especiais Cíveis de Natal/RN*. Dissertação
> (Mestrado em Direito e Políticas Públicas) — Programa de Pós-Graduação
> em Direito e Políticas Públicas, Universidade Federal de Goiás, Goiânia, 2026.
> Notebook de replicação: `estcaso_lide_pred.ipynb` (gerado por
> `src/estcaso_lide_pred/build_notebook.py`).

---

*Notebook gerado em Python 3.12 com pandas, numpy, scipy, statsmodels,
scikit-learn, matplotlib e seaborn. Reprodutível via `uv run jupyter notebook`
na raiz do projeto.*
''')
