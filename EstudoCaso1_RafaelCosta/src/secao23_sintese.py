# Seção 15 — Exportação final e síntese. Trecho incluído por build_rafaelcc_ed1.py.

# =====================================================================
md(r'''
---

# SÍNTESE

## 23. Exportação Final e Conclusões

### 23.1 Bases exportadas

As variáveis de desfecho criadas nas Partes II e III são acrescentadas ao dataset da amostra, que é regravado. A base da população, já tratada, é gravada sem a lista bruta de movimentos. As duas ficam prontas para estudos posteriores.
''')

code(r'''
dados = dados.drop(columns=['Desfecho_top6'], errors='ignore')  # auxiliar do Exercício 4, reconstruível
NOVAS_VARIAVEIS = pd.DataFrame([
    ('Tempo_fase_judicial', 'Tempo', 'Quantitativa discreta (censurada)', 'Int64', 'dias', 'Derivada (seção 15)', 'Desfecho'),
    ('Tempo_total', 'Tempo', 'Quantitativa discreta (censurada, truncada)', 'Int64', 'dias', 'Derivada (seção 15)', 'Desfecho'),
    ('Idade_entrada_anos', 'Tempo', 'Quantitativa contínua', 'Float64', 'anos', 'Derivada (seção 15)', 'Entrada tardia'),
    ('Multiplas_vitimas', 'Caso', 'Qualitativa dicotômica', 'boolean', '', 'Derivada (seção 15)', 'Categórica'),
    ('Ano_recebimento_projudi', 'Tempo', 'Qualitativa ordinal', 'category', '', 'Derivada (seção 15)', 'Categórica'),
    ('Coorte_instauracao', 'Tempo', 'Qualitativa ordinal', 'category', '', 'Derivada (seção 15)', 'Categórica'),
    ('Tipo_desfecho', 'Desfecho', 'Qualitativa nominal', 'category', '', 'Derivada (seção 17)', 'Categórica'),
], columns=['Variável', 'Grupo', 'Tipo estatístico', 'dtype pandas', 'Unidade', 'Origem', 'Uso analítico'])
NOVAS_VARIAVEIS['Não nulos'] = [int(dados[v].notna().sum()) for v in NOVAS_VARIAVEIS['Variável']]
NOVAS_VARIAVEIS['Ausentes'] = [int(dados[v].isna().sum()) for v in NOVAS_VARIAVEIS['Variável']]
NOVAS_VARIAVEIS['Distintos'] = [int(dados[v].nunique()) for v in NOVAS_VARIAVEIS['Variável']]
ESQUEMA_FINAL = pd.concat([ESQUEMA_EXPORT, NOVAS_VARIAVEIS], ignore_index=True)
assert set(ESQUEMA_FINAL['Variável']) == set(dados.columns), set(ESQUEMA_FINAL['Variável']) ^ set(dados.columns)
divergentes = [v for v, t in zip(ESQUEMA_FINAL['Variável'], ESQUEMA_FINAL['dtype pandas']) if str(dados[v].dtype) != t]
assert not divergentes, divergentes

dados.to_pickle(ARQUIVO_PKL)
with pd.ExcelWriter(ARQUIVO_XLSX, engine='openpyxl') as planilha:
    dados.to_excel(planilha, sheet_name='dados')
    ESQUEMA_FINAL.to_excel(planilha, sheet_name='esquema', index=False)
    auditoria.to_excel(planilha, sheet_name='auditoria', index=False)
    diligencias_longas.to_excel(planilha, sheet_name='diligencias_longas', index=False)
pd.testing.assert_frame_equal(pd.read_pickle(ARQUIVO_PKL), dados)

ARQUIVO_POP = PASTA_SAIDA / 'rafaelcc_datajud_cvli_go.pkl'
pop.drop(columns=['Movimentos']).to_pickle(ARQUIVO_POP)
print(f'Amostra: {ARQUIVO_PKL.name} ({dados.shape[0]} × {dados.shape[1]}) | '
      f'População: {ARQUIVO_POP.name} ({len(pop):,} processos × {pop.shape[1] - 1} variáveis)')
''')

interp('sintese')
interp('limitacoes')

md(r'''
---

## Referências

### Métodos
- Kaplan, E. L.; Meier, P. (1958). Nonparametric estimation from incomplete observations. *JASA*, 53, 457–481.
- Cox, D. R. (1972). Regression models and life-tables. *JRSS-B*, 34, 187–220.
- Grambsch, P. M.; Therneau, T. M. (1994). Proportional hazards tests and diagnostics based on weighted residuals. *Biometrika*, 81, 515–526.
- Tsai, W.-Y. (1990). Testing the assumption of independence of truncation time and failure time. *Biometrika*, 77, 169–177.
- Prentice, R. L. (1974). A log gamma model and its maximum likelihood estimation. *Biometrika*, 61, 539–544 (gama generalizada).
- Cox, C. et al. (2007). Parametric survival analysis and taxonomy of hazard functions for the generalized gamma distribution. *Statistics in Medicine*, 26, 4352–4374.
- Dunn, O. J. (1964). Multiple comparisons using rank sums. *Technometrics*, 6, 241–252.
- Benjamini, Y.; Hochberg, Y. (1995). Controlling the false discovery rate. *JRSS-B*, 57, 289–300.

### Dados e conceitos
- CNJ. API Pública do DataJud — https://datajud-wiki.cnj.jus.br/api-publica/ ; Tabelas Processuais Unificadas (TPU) — https://www.cnj.jus.br/sgt/consulta_publica_classes.php
- Fórum Brasileiro de Segurança Pública (2023). *Anuário Brasileiro de Segurança Pública* (Mortes Violentas Intencionais).
- MJSP/Senasp. Indicadores de Crimes Violentos Letais Intencionais (CVLI).
- IBGE. Censo Demográfico 2022 (tabela 4709) e cadastro de municípios (API de localidades).

### Bibliotecas
pandas, numpy, scipy, statsmodels, lifelines, scikit-posthocs, matplotlib, seaborn.

### Base legal
Código de Processo Penal, art. 10 (prazos do inquérito); Código Penal, arts. 14, II (tentativa), 109 (prescrição), 121, 129 §3º e 157 §3º.
''')
