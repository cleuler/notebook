# Seção 9 — Auditoria complementar (prescrição, regras textuais) e regravação do dataset.
# Trecho incluído por build_rafaelcc_ed1.py (usa md, code e interp de lá).

# =====================================================================
md(r'''
---

## 9. Auditoria Complementar: Prescrição e Regras Textuais

Duas verificações de coerência que dependem de conhecimento jurídico ou de leitura humana completam a curadoria. Ambas usam a **data de referência da coleta**: a base não a informa, por isso adota-se a data mais recente registrada em qualquer campo de evento.
''')

code(r'''
DATA_REFERENCIA = dados[SEQUENCIA_DATAS].max().max()
print(f'Data de referência da coleta (inferida): {DATA_REFERENCIA:%d/%m/%Y}')
''')

md(r'''
### 9.1 Prescrição: coerência das datas e risco dos casos em curso

O homicídio, em todas as suas formas, tem pena máxima superior a 12 anos. Por isso, a prescrição da pretensão punitiva ocorre em **20 anos** (art. 109, I, do CP), contados do fato (art. 111). Antes da denúncia não há causa interruptiva (art. 117). A regra esperada é, portanto, `Data_prescricao_projudi ≈ Data_fato + 20 anos`. Os desvios não são necessariamente erros: prazo pela metade para agente menor de 21 anos na data do fato ou maior de 70 na sentença (art. 115), tentativa, ou outro marco inicial. Mas são pontos a conferir nos autos.
''')

code(r'''
anos_ate_prescricao = (dados['Data_prescricao_projudi'] - dados['Data_fato']).dt.days / 365.25
TOLERANCIA_DIAS = 7  # admite pequenas diferenças de contagem do dia inicial
desvio_fato = (dados['Data_prescricao_projudi'] - (dados['Data_fato'] + pd.DateOffset(years=20))).dt.days
desvio_instauracao = (dados['Data_prescricao_projudi'] - (dados['Data_instauracao'] + pd.DateOffset(years=20))).dt.days
classe_prescricao = np.select(
    [dados['Data_prescricao_projudi'].isna(),
     desvio_fato.abs().le(TOLERANCIA_DIAS).fillna(False),
     desvio_instauracao.abs().le(TOLERANCIA_DIAS).fillna(False),
     anos_ate_prescricao.lt(20).fillna(False)],
    ['Sem data de prescrição', '20 anos contados do fato', '20 anos contados da instauração', 'Menos de 20 anos'],
    default='Mais de 20 anos')
ORDEM_PRESCRICAO = ['20 anos contados do fato', '20 anos contados da instauração', 'Menos de 20 anos',
                    'Mais de 20 anos', 'Sem data de prescrição']
dados['Coerencia_prescricao'] = para_categoria(pd.Series(classe_prescricao, index=dados.index),
                                               {c: c for c in ORDEM_PRESCRICAO}, ORDEM_PRESCRICAO)
display(verificar_particao(dados['Coerencia_prescricao']))

fig, axes = plt.subplots(1, 2, figsize=(16, 5), gridspec_kw={'width_ratios': [1, 1.6]})
# 1. Quantos inquéritos em cada classe (escala linear, contagem e % sobre a barra)
contagem = dados['Coerencia_prescricao'].value_counts().reindex(ORDEM_PRESCRICAO)
cores_classe = [CORES[2], CORES[3], CORES[4], COR_DESTAQUE, TINTA_2]
axes[0].bar(range(len(contagem)), contagem.values, color=cores_classe, width=0.65)
for i, n in enumerate(contagem.values):
    axes[0].text(i, n + 1.5, f'{n}\n({100 * n / len(dados):.0f}%)', ha='center', va='bottom', fontsize=9)
axes[0].set_xticks(range(len(contagem)), [quebrar(c, 14) for c in contagem.index], fontsize=8.5)
axes[0].set_ylim(0, contagem.max() * 1.25)
axes[0].set_ylabel('inquéritos')
axes[0].set_title('Coerência da data de prescrição do Projudi')
axes[0].grid(axis='x', visible=False)

# 2. Onde estão os prazos incoerentes: só os casos que NÃO estão nos 20 anos do fato
fora = anos_ate_prescricao[dados['Coerencia_prescricao'].isin(['Menos de 20 anos', 'Mais de 20 anos', '20 anos contados da instauração'])]
barras = np.arange(np.floor(fora.min()), np.ceil(fora.max()) + 1, 1.0)
n_barra, bordas, retangulos = axes[1].hist(fora, bins=barras, color=COR_DESTAQUE, edgecolor='white')
for n, esquerda in zip(n_barra, bordas[:-1]):
    if n > 0:
        axes[1].text(esquerda + 0.5, n + 0.1, f'{int(n)}', ha='center', va='bottom', fontsize=8.5)
axes[1].axvline(20, color=TINTA, linewidth=2, linestyle='--', label='20 anos (art. 109, I): prazo esperado')
axes[1].axvline(10, color=TINTA_2, linewidth=1.5, linestyle=':', label='10 anos: prazo reduzido pela metade (art. 115)')
axes[1].set_xlabel('data de prescrição − data do fato (anos)')
axes[1].set_ylabel('inquéritos')
axes[1].set_title(f'Os {len(fora)} prazos que não seguem a regra dos 20 anos do fato')
axes[1].legend(fontsize=8.5, loc='upper left')
axes[1].grid(axis='x', visible=False)
plt.tight_layout()
plt.show()

print('Arquivamentos por prescrição: anos entre o fato e a conclusão no MP')
arq_prescricao = dados.loc[dados['Status_projudi'].eq('Arquivado: extinção da punibilidade (prescrição)'),
                           ['Comarca', 'Assunto_resumido', 'Data_fato', 'Data_conclusao_mp', 'Data_prescricao_projudi']]
arq_prescricao['Anos fato → conclusão'] = ((arq_prescricao['Data_conclusao_mp'] - arq_prescricao['Data_fato']).dt.days / 365.25).round(1)
display(arq_prescricao)
for n_ordem in arq_prescricao.index[arq_prescricao['Anos fato → conclusão'] < 10]:
    registrar(n_ordem, 'Status_projudi', 'Arquivado - EXTINÇÃO DA PUNIBILIDADE - PRESCRIÇÃO',
              'Prescrição com menos de 10 anos entre o fato e a conclusão', 'Mantido; conferir no processo')
''')

code(r'''
em_curso = dados[dados['Status_macro'].isin(['Ativo', 'Suspenso'])].copy()
em_curso['Anos até prescrever'] = ((em_curso['Data_prescricao_projudi'] - DATA_REFERENCIA).dt.days / 365.25).round(1)
em_curso['Idade do fato (anos)'] = ((DATA_REFERENCIA - em_curso['Data_fato']).dt.days / 365.25).round(1)
risco = em_curso[['Comarca', 'Desfecho', 'Data_fato', 'Idade do fato (anos)', 'Data_prescricao_projudi', 'Anos até prescrever',
                  'Houve_indiciamento']].sort_values('Idade do fato (anos)', ascending=False)
print(f'{len(risco)} inquéritos em curso (ativos ou suspensos) na data de referência; fato mais antigo há '
      f'{risco["Idade do fato (anos)"].max():.1f} anos; menor prazo restante até a prescrição: '
      f'{risco["Anos até prescrever"].min():.1f} anos; {int(risco["Houve_indiciamento"].eq(False).sum())} sem indiciado')
display(risco)
''')

interp('rb_prescricao')

md(r'''
### 9.2 Validação das regras textuais

As categorias de diligência e o indício de intervenção estatal vêm de expressões regulares. Duas verificações:

1. **Ambiguidade**: quantos itens casam com mais de uma regra? Nesses itens, a categoria foi decidida pela **ordem** das regras, e não pelo conteúdo;
2. **Amostra para conferência humana**: até 6 itens por categoria, sorteados com semente fixa, e todos os casos de intervenção estatal são exportados para a planilha `rafaelcc_validacao_regras.xlsx`, com colunas em branco para o parecer do leitor. O parecer preenchido é salvo à parte, em `rafaelcc_validacao_regras_parecer.xlsx`, que a reexecução não sobrescreve. Dele saem a taxa de acerto de cada regra e a precisão do indício de intervenção estatal.
''')

code(r'''
def regras_que_casam(item):
    chave = normalizar_chave(item)
    return [categoria for categoria, padrao in REGRAS_DILIGENCIA if re.search(padrao, chave)]


diligencias_longas['Regras que casam'] = diligencias_longas['Item'].map(regras_que_casam)
diligencias_longas['N regras'] = diligencias_longas['Regras que casam'].map(len)
ambiguidade = (diligencias_longas.groupby('Categoria', observed=True)
               .agg(Itens=('Item', 'size'),
                    Sem_regra=('N regras', lambda s: int((s == 0).sum())),
                    Ambiguos=('N regras', lambda s: int((s > 1).sum())))
               .assign(**{'% ambíguos': lambda t: (100 * t['Ambiguos'] / t['Itens']).round(1)}))
print(f"Itens que casam com mais de uma regra: {int((diligencias_longas['N regras'] > 1).sum())} de {len(diligencias_longas)} "
      f"({100 * (diligencias_longas['N regras'] > 1).mean():.1f}%)")
display(ambiguidade)

amostra_validacao = pd.concat([
    grupo.sample(min(len(grupo), 6), random_state=2026)
    for _, grupo in diligencias_longas.groupby('Categoria', observed=True)
])[['N_ordem', 'Item', 'Categoria']].assign(**{'Regras que casam': lambda t: diligencias_longas.loc[t.index, 'Regras que casam'].str.join(' | '),
                                               'Parecer (OK/Errado)': '', 'Categoria correta': ''})
casos_intervencao_validar = dados.loc[dados['Indicio_intervencao_estatal'], ['Comarca', 'Capitulacao', 'Tipo_manifestacao_mp']].assign(
    **{'Parecer (Sim/Não)': ''})

ARQUIVO_VALIDACAO = PASTA_SAIDA / 'rafaelcc_validacao_regras.xlsx'
with pd.ExcelWriter(ARQUIVO_VALIDACAO, engine='openpyxl') as planilha:
    amostra_validacao.to_excel(planilha, sheet_name='diligencias', index=False)
    casos_intervencao_validar.to_excel(planilha, sheet_name='intervencao_estatal')
print(f'Amostra de validação: {len(amostra_validacao)} itens de diligência e {len(casos_intervencao_validar)} casos de '
      f'intervenção → {ARQUIVO_VALIDACAO.name}')
diligencias_longas = diligencias_longas.drop(columns=['Regras que casam', 'N regras'])

# O parecer fica num arquivo separado, que a reexecução não sobrescreve
ARQUIVO_PARECER = PASTA_SAIDA / 'rafaelcc_validacao_regras_parecer.xlsx'
if ARQUIVO_PARECER.exists():
    parecer_dil = pd.read_excel(ARQUIVO_PARECER, sheet_name='diligencias')
    parecer_int = pd.read_excel(ARQUIVO_PARECER, sheet_name='intervencao_estatal')
    print(f"Parecer: {ARQUIVO_PARECER.name} | revisor: {'; '.join(parecer_dil['Revisor'].dropna().unique())}")
    acerto = (parecer_dil.assign(OK=parecer_dil['Parecer (OK/Errado)'].str.strip().str.upper().eq('OK'))
              .groupby('Categoria').agg(Itens=('OK', 'size'), Corretos=('OK', 'sum')))
    acerto.loc['Total'] = acerto.sum()
    acerto['Acerto'] = acerto['Corretos'] / acerto['Itens']
    acerto['IC 95% (Wilson)'] = [
        '{:.0%}–{:.0%}'.format(*proportion_confint(c, n, method='wilson')) for c, n in zip(acerto['Corretos'], acerto['Itens'])]
    display(acerto.style.format({'Acerto': '{:.0%}'}))
    confirmados = parecer_int['Parecer (Sim/Não)'].str.strip().str.lower().eq('sim')
    li, ls = proportion_confint(confirmados.sum(), len(confirmados), method='wilson')
    print(f'Intervenção estatal: {confirmados.sum()} de {len(confirmados)} casos confirmados '
          f'(precisão {confirmados.mean():.0%}; IC 95% {li:.0%}–{ls:.0%})')
    display(parecer_int[['N_ordem', 'Comarca', 'Parecer (Sim/Não)', 'Evidência']])
    observacoes = parecer_dil.loc[parecer_dil['Observação'].notna(), ['N_ordem', 'Item', 'Categoria', 'Observação']]
    if len(observacoes):
        display(observacoes)
else:
    print(f'Parecer ainda não preenchido: salve a planilha revisada como {ARQUIVO_PARECER.name}')
''')

interp('rb_validacao')

md(r'''
**Auditoria atualizada.** A tabela de auditoria, acrescida dos registros desta seção, e a nova variável `Coerencia_prescricao` são regravadas no dataset exportado.
''')

code(r'''
auditoria = pd.DataFrame(registros_auditoria).drop_duplicates().sort_values(['Variável', 'N_ordem']).reset_index(drop=True)
ESQUEMA_EXPORT = pd.concat([ESQUEMA, pd.DataFrame([{
    'Variável': 'Coerencia_prescricao', 'Grupo': 'Tempo', 'Tipo estatístico': 'Qualitativa nominal', 'dtype pandas': 'category',
    'Unidade': '', 'Origem': 'Derivada (seção 9.1)', 'Uso analítico': 'Auditoria',
    'Não nulos': int(dados['Coerencia_prescricao'].notna().sum()), 'Ausentes': int(dados['Coerencia_prescricao'].isna().sum()),
    'Distintos': int(dados['Coerencia_prescricao'].nunique())}])], ignore_index=True)
assert set(ESQUEMA_EXPORT['Variável']) == set(dados.columns)

dados.to_pickle(ARQUIVO_PKL)
with pd.ExcelWriter(ARQUIVO_XLSX, engine='openpyxl') as planilha:
    dados.to_excel(planilha, sheet_name='dados')
    ESQUEMA_EXPORT.to_excel(planilha, sheet_name='esquema', index=False)
    auditoria.to_excel(planilha, sheet_name='auditoria', index=False)
    diligencias_longas.to_excel(planilha, sheet_name='diligencias_longas', index=False)
pd.testing.assert_frame_equal(pd.read_pickle(ARQUIVO_PKL), dados)
print(f'Dataset regravado: {dados.shape[0]} × {dados.shape[1]}; auditoria com {len(auditoria)} registros')
display(auditoria[auditoria['Problema'].str.contains('Prescrição')])
''')
