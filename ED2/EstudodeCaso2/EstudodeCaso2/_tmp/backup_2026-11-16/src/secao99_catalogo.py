# Apêndice — painel-resumo e catálogo de figuras e tabelas.
# Executado por build_rafaelcc_ed2.py (exec) por último, só no build completo (ou se indicado em --somente).
# Usa a camada de visualização da seção 1.2 (figura, tabela, CATALOGO, TABELAS_EXPORT).

md(r'''
---

# APÊNDICE — CATÁLOGO DE FIGURAS E TABELAS

O apêndice reúne (A.1) um **painel-resumo** do estudo, com seis gráficos que condensam os achados principais, cada um com o seu achado no título; e (A.2) o **catálogo** de todas as figuras e tabelas do notebook, com número, título, seção e arquivo. As tabelas são exportadas também numa pasta de trabalho única, `tab/ed2_tabelas.xlsx` (uma aba por tabela), e o catálogo em `tab/catalogo.csv`.

## A.1 Painel-resumo

O painel é estático e deve ser lido junto com as partes em que cada resultado é demonstrado:

- **(a)** e **(f)**: o sorteio produziu grupos de tamanho quase igual, mas a entrada foi escalonada e a composição mensal variou (por isso o mês é covariável nas Partes IV e V);
- **(b)**: a composição dos desfechos por grupo (Parte III, seção 3.2);
- **(c)**: a curva de Kaplan-Meier, a forma correta de comparar o tempo com censura (Parte IV);
- **(d)**: a proporção de processos encerrados por homologação de acordo até a data de corte, com IC 95% de Wilson (Parte III, seção 3.3);
- **(e)**: o tempo até a sentença de mérito entre os que a tiveram — estatística **condicional**, enviesada para tempos curtos, mostrada só como descrição.
''')

code(r'''
if 'dados' not in globals():
    dados = pd.read_pickle(PROC / 'ed2_tidy.pkl')
from statsmodels.stats.proportion import proportion_confint

ap = dados.copy()
ap['grupo'] = ap['grupo'].cat.set_categories(ORDEM_GRUPO)
n_g = ap['grupo'].value_counts().reindex(ORDEM_GRUPO)
mix = pd.crosstab(ap['grupo'], ap['tipo_desfecho'], normalize='index').reindex(index=ORDEM_GRUPO, columns=ORDEM_DESFECHO).fillna(0)
homol = ap.groupby('grupo', observed=False)['causa'].apply(lambda s: int(s.eq(1).sum())).reindex(ORDEM_GRUPO)
ic_h = np.array([proportion_confint(homol[g], n_g[g], method='wilson') for g in ORDEM_GRUPO])
p_h = homol / n_g
merito = ap[ap['tipo_desfecho'].eq('Mérito')]
md_merito = merito.groupby('grupo', observed=False)['tempo'].median().reindex(ORDEM_GRUPO).astype(float)
mes = pd.crosstab(ap['mes_distribuicao'], ap['grupo']).reindex(columns=ORDEM_GRUPO)

fig, ax = plt.subplots(3, 2, figsize=(13, 14.5))
ax = ax.ravel()

# (a) tamanho dos grupos
barras_verticais(ax[0], ORDEM_GRUPO, n_g.to_numpy(), ylabel=ROTULOS['n'], fmt=fmt_int)
ax[0].set_title(quebra(f'(a) O sorteio produziu grupos quase iguais: {fmt_br(n_g.min(), 0)} a {fmt_br(n_g.max(), 0)} '
                       f'processos (N = {fmt_br(n_g.sum(), 0)})', 60))

# (b) composição dos desfechos
barras_empilhadas(ax[1], mix, ns=n_g.to_numpy(), rotulos_serie=ROTULO_DESFECHO, rotulo_min=0.05)
ax[1].set_title(quebra(f'(b) O Controle tem mais sentenças de mérito ({pct_br(mix.loc["Controle", "Mérito"], 0)}) e menos '
                       f'extinções sem mérito ({pct_br(mix.loc["Controle", "Sem mérito"], 0)}) que os grupos com AC', 60))

# (c) Kaplan-Meier
kms_painel = plot_km(ax[2], ap, tabela_risco=False, passo=30)
ax[2].legend(loc='upper right', fontsize=8)
_med = {g: kms_painel[g].median_survival_time_ for g in ORDEM_GRUPO}
ax[2].set_title(quebra('(c) Tempo até a sentença com censura (Kaplan-Meier): medianas de '
                       + ', '.join(f'{g} {fmt_br(_med[g], 0)}' for g in ORDEM_GRUPO) + ' dias', 60))

# (d) homologações de acordo com IC
barras_verticais(ax[3], ORDEM_GRUPO, 100 * p_h.to_numpy(), erro=(100 * ic_h[:, 0], 100 * ic_h[:, 1]),
                 fmt=lambda v: fmt_br(v, 1) + '%', ylabel='Processos encerrados por homologação (%)', ns=n_g.to_numpy())
_sobrepostos = ic_h[:, 0].max() <= ic_h[:, 1].min()
ax[3].set_title(quebra(f'(d) Acordos homologados até 07/10/2026: {fmt_br(100 * p_h.min(), 1)}% a '
                       f'{fmt_br(100 * p_h.max(), 1)}% dos processos'
                       + (', com IC 95% que se sobrepõem' if _sobrepostos else ''), 60))

# (e) tempo até o mérito (condicional)
boxplot_grupos(ax[4], merito, 'tempo', ylabel=ROTULOS['tempo_sentenca'], tam_ponto=5)
ax[4].set_title(quebra('(e) Entre as sentenças de mérito, medianas de ' +
                       ', '.join(f'{g} {fmt_br(md_merito[g], 0)}' for g in ORDEM_GRUPO) +
                       ' dias (condicional aos sentenciados)', 60))

# (f) entradas por mês
mes.index = [str(m) for m in mes.index]
barras_agrupadas(ax[5], mes, ylabel='Processos distribuídos', xlabel=ROTULOS['mes_distribuicao'])
_pico = mes.div(mes.sum(axis=1), axis=0)[mes.sum(axis=1) >= 30]     # meses com poucos processos não definem o achado
_mx = _pico.stack().idxmax()
ax[5].set_title(quebra(f'(f) A entrada foi escalonada e a composição mensal variou: em {_mx[0]}, '
                       f'{pct_br(_pico.loc[_mx], 0)} dos processos do mês foram para a {_mx[1]}', 60))
fig.subplots_adjust(hspace=0.55, wspace=0.45)
figura(fig, 'apx_painel', 'Painel-resumo do estudo: grupos, desfechos, tempo e acordos', secao='99',
       nota='(c) S(t) com IC 95% e marcas de censura; (d) IC 95% de Wilson; (e) só processos com sentença de mérito, '
            'estatística condicional e enviesada para tempos curtos.')
''')

md(r'''
## A.2 Catálogo de figuras e tabelas

O catálogo lista, na ordem de aparição, todas as figuras e tabelas numeradas pela camada de visualização (seção 1.2). Cada figura está em `fig/<id>.png` (e `.svg`); cada tabela, em `tab/<id>.csv` e numa aba da pasta de trabalho `tab/ed2_tabelas.xlsx`.
''')

code(r'''
_ordem_parte = {p: i for i, p in enumerate(['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'A'])}


def _chave_catalogo(r):
    parte, num = r['Número'].rsplit('.', 1)
    return (0 if r['Tipo'] == 'Figura' else 1, _ordem_parte.get(parte, 99), int(num))


catalogo = pd.DataFrame(sorted(CATALOGO.values(), key=_chave_catalogo))
catalogo['Número'] = catalogo['Tipo'] + ' ' + catalogo['Número']
catalogo_exp = catalogo[['Tipo', 'Número', 'Título', 'Seção', 'Arquivo', 'id']]
catalogo_exp.to_csv(TAB / 'catalogo.csv', sep=';', encoding='utf-8-sig', index=False)
resumo_cat = catalogo.assign(Parte=catalogo['Número'].str.split(' ').str[1].str.rsplit('.', n=1).str[0]) \
    .pivot_table(index='Parte', columns='Tipo', values='id', aggfunc='count', fill_value=0) \
    .reindex([p for p in _ordem_parte if p in set(catalogo['Número'].str.split(' ').str[1].str.rsplit('.', n=1).str[0])])
print(f"{(catalogo['Tipo'] == 'Figura').sum()} figuras e {(catalogo['Tipo'] == 'Tabela').sum()} tabelas catalogadas.")
tabela(resumo_cat.rename_axis('Parte'), 'apx_contagem', 'Número de figuras e tabelas por parte do notebook', secao='99',
       exportar=False)
tabela(catalogo[catalogo['Tipo'] == 'Figura'][['Número', 'Título', 'Seção', 'Arquivo']], 'apx_catalogo_figuras',
       'Catálogo de figuras', secao='99', exportar=False, formatos={'Seção': 'texto'})
tabela(catalogo[catalogo['Tipo'] == 'Tabela'][['Número', 'Título', 'Seção', 'Arquivo']], 'apx_catalogo_tabelas',
       'Catálogo de tabelas', secao='99', exportar=False, formatos={'Seção': 'texto'})
''')

md(r'''
### A.2.1 Exportação das tabelas numa pasta de trabalho

Cada tabela exportada vira uma aba de `tab/ed2_tabelas.xlsx`, com o número da tabela no nome da aba (o Excel limita o nome a 31 caracteres) e o título na primeira linha. A primeira aba é o próprio catálogo.
''')

code(r'''
import re as _re
_numero_de = {r['id']: r['Número'] for r in CATALOGO.values() if r['Tipo'] == 'Tabela'}
_titulo_de = {r['id']: r['Título'] for r in CATALOGO.values() if r['Tipo'] == 'Tabela'}
_usadas = set()
_abas = []
with pd.ExcelWriter(TAB / 'ed2_tabelas.xlsx', engine='openpyxl') as _xl:
    catalogo_exp.to_excel(_xl, sheet_name='Catálogo', index=False)
    for _id, _df in sorted(TABELAS_EXPORT.items(), key=lambda kv: _chave_catalogo({'Tipo': 'Tabela', 'Número': _numero_de.get(kv[0], 'Z.0')})
                           if kv[0] in _numero_de else (2, 0, 0)):
        _nome = _re.sub(r'[\[\]:*?/\\]', '-', f"T{_numero_de.get(_id, '')} {_id}")[:31]
        _base, _k = _nome, 2
        while _nome.lower() in _usadas:
            _nome = f'{_base[:28]}~{_k}'; _k += 1
        _usadas.add(_nome.lower())
        _titulo = pd.DataFrame([[f"Tabela {_numero_de.get(_id, '?')} — {_titulo_de.get(_id, _id)}"]])
        _titulo.to_excel(_xl, sheet_name=_nome, index=False, header=False)
        _df.to_excel(_xl, sheet_name=_nome, index=False, startrow=2)
        _abas.append(_nome)
print(f'{len(_abas)} tabelas exportadas para {TAB / "ed2_tabelas.xlsx"} (+ aba Catálogo); catálogo em {TAB / "catalogo.csv"}')
''')
