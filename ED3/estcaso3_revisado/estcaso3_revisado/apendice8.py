"""Parte VI: modelos bayesianos e resposta final consolidada."""

BLOCKS = [
    ("markdown", r"""
---

# PARTE VI — MODELOS BAYESIANOS

As Seções 6 e 27 usaram Bayes com contas fechadas: verossimilhanças pontuais, uma Beta para a prevalência e a atualização de um período para o outro. Esta parte usa o mesmo raciocínio em quatro pontos em que ele acrescenta informação ou expõe incerteza que as contas anteriores deixavam de fora:

| Seção | Pergunta | Modelo |
|---|---|---|
| 31 | Qual a prevalência e o total de indício na moldura, usando o que se sabe de **todos** os 50.320 processos? | regressão logística hierárquica com pós-estratificação (MRP) |
| 32 | Quanto um dado do processo move a crença, levando em conta que as verossimilhanças também são estimadas? | Dirichlet-multinomial e Beta; validação temporal do assunto |
| 33 | Quanto a conclusão depende de a codificadora ter acertado? | prevalência com sensibilidade e especificidade incertas |
| 34 | Os coeficientes instáveis da Seção 8 ficam estáveis com prioris fracamente informativas? | logística com prioris t de Student; LOO |

Os ajustes usam PyMC (NUTS, quatro cadeias) e ArviZ. Cada tabela mostra os diagnósticos de convergência: R-hat perto de 1, tamanho efetivo de amostra (ESS) alto e nenhuma divergência. As prioris foram escolhidas pelo raciocínio declarado em cada seção, não pelo resultado. A **sensibilidade a elas** é mostrada quando a conclusão poderia depender delas (GELMAN et al., 2013, cap. 5 e 16; GELMAN et al., 2008; MCELREATH, 2020, cap. 12–13).
"""),
    ("markdown", r"""
## 31. Prevalência na moldura por regressão hierárquica e pós-estratificação (MRP)

A Seção 24 mostrou que o assunto do processo concentra o indício: o código 6226 (inclusão indevida em cadastro de inadimplentes) reúne 74 dos 105 indícios. O assunto é conhecido para **todos** os processos da moldura, e não só para os 595 sorteados. Essa informação auxiliar permite estimar melhor a prevalência, pelo mesmo princípio dos estimadores de regressão e de pós-estratificação da amostragem (BOLFARINE; BUSSAB, 2004).

**Modelo.** Para cada processo *i*, com ano *a*, juizado *j* e assunto *s*:

$$\operatorname{logit} P(\text{indício}_i = 1) = \alpha + \beta_{a} + u_{j} + v_{s},\qquad u_j \sim N(0, \sigma_{\text{JEC}}),\quad v_s \sim N(0, \sigma_{\text{assunto}}).$$

- **Ano** (o estrato do sorteio) entra como efeito com soma zero, de modo que o desenho é respeitado.
- **JEC e assunto** entram com **agrupamento parcial**: um assunto com poucos processos na amostra é puxado para a média, na proporção da incerteza (*shrinkage*). Os assuntos da moldura que não aparecem na amostra recebem um efeito sorteado da distribuição do grupo, e essa incerteza entra no resultado.
- **Prioris:** α ~ N(0; 1,5); β ~ N(0; 1) com soma zero; σ_JEC ~ meia-normal(0,5), porque a Seção 2.4 não sugere grande heterogeneidade entre juizados; σ_assunto ~ meia-normal(1,5), que admite diferenças grandes entre assuntos.

**Pós-estratificação.** As probabilidades do modelo são aplicadas às células ano × JEC × assunto dos **50.320 − 595 processos não sorteados**, com sorteios binomiais, e somadas aos valores observados dos sorteados. O resultado é a distribuição a posteriori do **total** de processos com indício na moldura e da prevalência, isto é, uma inferência de população finita (GELMAN; LITTLE, 1997; PARK; GELMAN; BAFUMI, 2004). O mesmo modelo dá estimativas por juizado com agrupamento parcial, que respondem à pergunta sobre o 7º JEC (Seção 5.3) sem testar 14 hipóteses.

A mesma análise é feita para a **certeza**. O contraste de desenho é o estimador pós-estratificado simples, com dois grupos (6226 e demais).
"""),
    ("code", r"""
# 31.1 MRP: indício e certeza na moldura de 50.320 processos
from estcaso3_revisado import bayes as BY

_mold_b = pd.DataFrame({'numero': base['NÚMERO PROCESSO'].astype(str).to_numpy(),
                        'ano': base['ano_inicio'].astype(int).to_numpy(),
                        'jec': base['jec'].astype(int).to_numpy(),
                        'assunto': base['CÓD ASSUNTO'].to_numpy()})
_am_b = (am[['numero', 'ano', 'jec', 'indicio', 'certeza']].assign(numero=lambda d: d.numero.astype(str))
         .merge(_mold_b[['numero', 'assunto']], on='numero', how='left', validate='one_to_one'))
_am_b['indicio'] = _am_b.indicio.astype(int)
_am_b['certeza'] = _am_b.certeza.astype(int)
assert len(_am_b) == 595 and _am_b.numero.isin(_mold_b.numero).all()
SEMENTE_BAYES = C.inteiro_semente(SEMENTES['simulacao'])

with C.capturar_avisos('MRP bayesiano (PyMC)', AVISOS):
    MRP_IND = BY.mrp_prevalencia(_am_b, _mold_b, 'indicio', seed=SEMENTE_BAYES)
    MRP_CER = BY.mrp_prevalencia(_am_b, _mold_b, 'certeza', seed=SEMENTE_BAYES + 1)
for _m in (MRP_IND, MRP_CER):
    assert _m['diagnosticos']['R-hat máximo'] < 1.01 and _m['diagnosticos']['divergências'] == 0
display(pd.DataFrame({'indício': MRP_IND['diagnosticos'], 'certeza': MRP_CER['diagnosticos']}))

_N_mold = len(_mold_b)
_grupo_b = np.where(_am_b.assunto.eq('6226'), '6226', 'demais')
_N_grupo = {'6226': int((_mold_b.assunto == '6226').sum()), 'demais': int((_mold_b.assunto != '6226').sum())}
PS_IND = BY.pos_estratificado(_am_b.indicio, _grupo_b, _N_grupo, _N_mold)
PS_CER = BY.pos_estratificado(_am_b.certeza, _grupo_b, _N_grupo, _N_mold)
display(tabela_ptbr(PS_IND['tabela'], casas=4, pct=['p_g', 'peso W_g']))

_lin = []
for _alvo, _est, _ps, _mrp in [('indício', est_ind, PS_IND, MRP_IND), ('certeza', est_cer, PS_CER, MRP_CER)]:
    _ic_log = intervalo_logit_desenho(_est['p_st'], _est['ep'])
    _r = BY.resumo(_mrp['prevalencia'])
    _lin += [
        {'resposta': _alvo, 'método': 'desenho: estratificado por ano (logito)', 'estimativa': _est['p_st'],
         'inferior': _ic_log[0], 'superior': _ic_log[1]},
        {'resposta': _alvo, 'método': 'desenho: pós-estratificado por assunto (6226 × demais)', 'estimativa': _ps['p'],
         'inferior': _ps['ic'][0], 'superior': _ps['ic'][1]},
        {'resposta': _alvo, 'método': 'bayesiano: MRP (ano + JEC + assunto)', 'estimativa': _r['mediana'],
         'inferior': _r['IC cred. inf.'], 'superior': _r['IC cred. sup.']}]
TAB_MRP = pd.DataFrame(_lin)
TAB_MRP['amplitude (p.p.)'] = 100 * (TAB_MRP.superior - TAB_MRP.inferior)
display(tabela_ptbr(TAB_MRP, casas=2, pct=['estimativa', 'inferior', 'superior']))

_tot_i, _tot_c = BY.resumo(MRP_IND['total']), BY.resumo(MRP_CER['total'])
TAB_TOTAIS = pd.DataFrame([
    {'resposta': 'indício', 'desenho (p × N)': est_ind['total'], 'desenho inf.': est_ind['total_ic'][0],
     'desenho sup.': est_ind['total_ic'][1], 'MRP mediana': _tot_i['mediana'], 'MRP inf.': _tot_i['IC cred. inf.'],
     'MRP sup.': _tot_i['IC cred. sup.']},
    {'resposta': 'certeza', 'desenho (p × N)': est_cer['total'], 'desenho inf.': est_cer['total_ic'][0],
     'desenho sup.': est_cer['total_ic'][1], 'MRP mediana': _tot_c['mediana'], 'MRP inf.': _tot_c['IC cred. inf.'],
     'MRP sup.': _tot_c['IC cred. sup.']}])
display(tabela_ptbr(TAB_TOTAIS, casas=0))
"""),
    ("code", r"""
# 31.2 Assunto 6226, juizados com agrupamento parcial e heterogeneidade
_p6 = MRP_IND['assunto']['6226']
_po = MRP_IND['assunto']['outros']
TAB_ASSUNTO_MRP = pd.DataFrame([BY.resumo(_p6, 'prevalência de indício no assunto 6226'),
                                BY.resumo(_po, 'prevalência de indício nos demais assuntos'),
                                BY.resumo(MRP_IND['sigma_assunto'], 'σ_assunto (logito)'),
                                BY.resumo(MRP_IND['sigma_jec'], 'σ_JEC (logito)')])
display(tabela_ptbr(TAB_ASSUNTO_MRP, casas=3))

_prev = MRP_IND['prevalencia']
_lin_j = []
for _j, _d in MRP_IND['jec'].items():
    _r = BY.resumo(_d)
    _bruta = am.loc[am.jec == _j, 'indicio'].astype(float)
    _lin_j.append({'JEC': int(_j), 'n na amostra': int(len(_bruta)), 'proporção bruta': float(_bruta.mean()),
                   'MRP mediana': _r['mediana'], 'MRP inf.': _r['IC cred. inf.'], 'MRP sup.': _r['IC cred. sup.'],
                   'P(acima da moldura)': float((_d > _prev).mean())})
TAB_JEC_MRP = pd.DataFrame(_lin_j)
display(tabela_ptbr(TAB_JEC_MRP, casas=3, pct=['proporção bruta', 'MRP mediana', 'MRP inf.', 'MRP sup.']))

fig, ax = plt.subplots(figsize=(9, 4.6))
ax.errorbar(TAB_JEC_MRP.JEC, 100 * TAB_JEC_MRP['MRP mediana'],
            yerr=[100 * (TAB_JEC_MRP['MRP mediana'] - TAB_JEC_MRP['MRP inf.']),
                  100 * (TAB_JEC_MRP['MRP sup.'] - TAB_JEC_MRP['MRP mediana'])],
            fmt='o', color='#0072B2', capsize=3, label='MRP: mediana e IC cred. 95%')
ax.scatter(TAB_JEC_MRP.JEC + 0.18, 100 * TAB_JEC_MRP['proporção bruta'], marker='x', color='#D55E00',
           label='proporção bruta na amostra')
ax.axhline(100 * np.median(_prev), color='#999', ls='--', lw=0.8, label='moldura (MRP)')
ax.set(xticks=TAB_JEC_MRP.JEC, xlabel='juizado', ylabel='% com indício',
       title='Indício por JEC: a estimativa hierárquica encolhe os extremos em direção à média')
ax.legend(fontsize=8); fig.tight_layout()
fig.savefig(FIGURAS / 'mrp_indicio_por_jec.png', dpi=150); plt.show()

_ri, _rc = BY.resumo(MRP_IND['prevalencia']), BY.resumo(MRP_CER['prevalencia'])
_j7 = TAB_JEC_MRP.set_index('JEC').loc[7]
_amp = TAB_MRP.set_index(['resposta', 'método'])['amplitude (p.p.)']
_ic_pub = IC_REF['indício']['publicado (Wald + FPC, N = 83.139)']
V.update(mrp_ind=fpct(_ri['mediana']), mrp_ind_ic=fic(_ri['IC cred. inf.'], _ri['IC cred. sup.'], pct=True),
         mrp_cer=fpct(_rc['mediana']), mrp_cer_ic=fic(_rc['IC cred. inf.'], _rc['IC cred. sup.'], pct=True),
         mrp_tot=fint(round(_tot_i['mediana'])), mrp_tot_ic=fic(_tot_i['IC cred. inf.'], _tot_i['IC cred. sup.'], casas=0),
         mrp_tot_c=fint(round(_tot_c['mediana'])), mrp_tot_c_ic=fic(_tot_c['IC cred. inf.'], _tot_c['IC cred. sup.'], casas=0),
         des_tot=fint(round(est_ind['total'])), des_tot_ic=fic(*est_ind['total_ic'], casas=0),
         des_tot_c=fint(round(est_cer['total'])), des_tot_c_ic=fic(*est_cer['total_ic'], casas=0),
         ps_ind=fpct(PS_IND['p']), ps_ind_ic=fic(*PS_IND['ic'], pct=True),
         ps_cer=fpct(PS_CER['p']), ps_cer_ic=fic(*PS_CER['ic'], pct=True),
         des_ic_logit=fic(*intervalo_logit_desenho(est_ind['p_st'], est_ind['ep']), pct=True),
         amp_des=fnum(_amp[('indício', 'desenho: estratificado por ano (logito)')], 1),
         amp_ps=fnum(_amp[('indício', 'desenho: pós-estratificado por assunto (6226 × demais)')], 1),
         amp_mrp=fnum(_amp[('indício', 'bayesiano: MRP (ano + JEC + assunto)')], 1),
         mrp_6226=fpct(np.median(_p6), 1), mrp_6226_ic=fic(*np.quantile(_p6, [.025, .975]), pct=True, casas=1),
         mrp_outros=fpct(np.median(_po), 1), mrp_outros_ic=fic(*np.quantile(_po, [.025, .975]), pct=True, casas=1),
         mrp_p6226_30=fpct((_p6 >= 0.30).mean(), 1), mrp_pind_30=fpct((MRP_IND['prevalencia'] >= 0.30).mean(), 1),
         mrp_sig_j=fnum(np.median(MRP_IND['sigma_jec']), 2),
         mrp_sig_j_ic=fic(*np.quantile(MRP_IND['sigma_jec'], [.025, .975]), casas=2),
         mrp_sig_a=fnum(np.median(MRP_IND['sigma_assunto']), 2),
         mrp_sig_a_ic=fic(*np.quantile(MRP_IND['sigma_assunto'], [.025, .975]), casas=2),
         mrp_j7_bruta=fpct(_j7['proporção bruta'], 1), mrp_j7=fpct(_j7['MRP mediana'], 1),
         mrp_j7_ic=fic(_j7['MRP inf.'], _j7['MRP sup.'], pct=True, casas=1), mrp_j7_p=fnum(_j7['P(acima da moldura)'], 2),
         mrp_jec_min=fpct(TAB_JEC_MRP['MRP mediana'].min(), 1), mrp_jec_max=fpct(TAB_JEC_MRP['MRP mediana'].max(), 1),
         mrp_jec_bmin=fpct(TAB_JEC_MRP['proporção bruta'].min(), 1), mrp_jec_bmax=fpct(TAB_JEC_MRP['proporção bruta'].max(), 1),
         mrp_rhat=fnum(max(MRP_IND['diagnosticos']['R-hat máximo'], MRP_CER['diagnosticos']['R-hat máximo']), 3),
         mrp_ess=fint(min(MRP_IND['diagnosticos']['ESS bulk mínimo'], MRP_CER['diagnosticos']['ESS bulk mínimo'])),
         mrp_assuntos_am=fint(MRP_IND['assuntos_na_amostra']), mrp_assuntos_mo=fint(MRP_IND['assuntos_na_moldura']),
         mrp_dentro_pub='dentro' if _ic_pub[0] <= _ri['mediana'] <= _ic_pub[1] else 'fora',
         mrp_p_pub=fpct(((MRP_IND['prevalencia'] >= _ic_pub[0]) & (MRP_IND['prevalencia'] <= _ic_pub[1])).mean(), 1),
         n_6226_mold=fint(_N_grupo['6226']), p_6226_mold=fpct(_N_grupo['6226'] / _N_mold, 1))
display(Markdown(C.preencher(r'''
**Leitura (R19 com a informação de toda a moldura).**

- **Prevalência de indício.** O MRP estima **{{mrp_ind}}** (IC cred. 95% {{mrp_ind_ic}}). O estimador do desenho dá {{p_indicio}} {{des_ic_logit}}, e o pós-estratificado por assunto, {{ps_ind}} {{ps_ind_ic}}. As três estimativas concordam. A amplitude do intervalo cai de {{amp_des}} p.p. (desenho) para {{amp_ps}} p.p. (pós-estratificação) e {{amp_mrp}} p.p. (MRP). O ganho vem de usar o assunto, conhecido para os 50.320 processos: o 6226 corresponde a {{p_6226_mold}} da moldura ({{n_6226_mold}} processos).
- **Total na moldura.** O MRP estima **{{mrp_tot}}** processos com indício (IC cred. 95% {{mrp_tot_ic}}), contra {{des_tot}} {{des_tot_ic}} pelo desenho. Para a certeza: {{mrp_cer}} {{mrp_cer_ic}}, ou {{mrp_tot_c}} processos {{mrp_tot_c_ic}} (desenho: {{des_tot_c}} {{des_tot_c_ic}}). É a resposta, com incerteza explícita, aos "cerca de 8.880" e "2.537" citados no roteiro.
- **Pergunta R19.** A mediana do MRP fica **{{mrp_dentro_pub}}** do intervalo publicado; {{mrp_p_pub}} da distribuição a posteriori está dentro dele.
- **Assunto.** A prevalência de indício é **{{mrp_6226}}** {{mrp_6226_ic}} no assunto 6226 e {{mrp_outros}} {{mrp_outros_ic}} nos demais. A heterogeneidade entre assuntos é grande (σ_assunto = {{mrp_sig_a}} {{mrp_sig_a_ic}} na escala logito). A heterogeneidade entre juizados é pequena (σ_JEC = {{mrp_sig_j}} {{mrp_sig_j_ic}}). Foram observados {{mrp_assuntos_am}} dos {{mrp_assuntos_mo}} códigos de assunto da moldura; os demais entram com o efeito sorteado do grupo.
- **Juizados.** As proporções brutas por JEC variam de {{mrp_jec_bmin}} a {{mrp_jec_bmax}}. As estimativas hierárquicas variam só de {{mrp_jec_min}} a {{mrp_jec_max}}, porque parte da variação bruta é ruído de amostras de 33 a 55 processos e parte vem da composição por assunto. No 7º JEC, a proporção bruta é {{mrp_j7_bruta}}, e a estimativa hierárquica é {{mrp_j7}} {{mrp_j7_ic}}, com P(acima da moldura) = {{mrp_j7_p}}. Isso confirma, com outro método, a leitura da Seção 5.3: não há evidência de um juizado diferente.
- **Comparação com os 30% da NT CIJMG.** A nota técnica fala do fluxo de **dois assuntos**. Para a moldura inteira, P(θ ≥ 0,30 | dados) = {{mrp_pind_30}}; dentro do assunto 6226, P(θ ≥ 0,30 | dados) = {{mrp_p6226_30}}. A conclusão da Seção 6.3 ("os dados contradizem 30%") vale para a moldura, e não para um assunto de alta incidência. Se os assuntos da NT forem comparáveis ao 6226, ela se inverte.
- **Diagnósticos.** R-hat máximo {{mrp_rhat}}, ESS mínimo {{mrp_ess}} e nenhuma divergência.

**Limites.** O modelo reproduz a regra de codificação da pesquisa, e não um diagnóstico jurídico independente (Seção 33). O assunto vem da moldura do TJRN, na data da extração. Os efeitos aditivos supõem que a diferença entre assuntos seja parecida em todos os juizados.
''', V)))
"""),
    ("markdown", r"""
## 32. Bayes por processo com as verossimilhanças estimadas

Na Seção 6, P(D | Hₐ) e P(D | H₀) entraram como números exatos, embora sejam proporções estimadas em 105 e 488 processos. Aqui elas recebem uma distribuição a posteriori. Os quatro desfechos são modelados **em conjunto**, com uma Dirichlet(1, 1, 1, 1) por hipótese, porque somam um dentro de cada hipótese e não são quatro evidências independentes. A priori P(Hₐ) também ganha incerteza: Beta(6, 14), média 0,30 com o peso de 20 processos, como na decisão D1, e Beta(1, 1) como cenário sem informação. O resultado é uma distribuição para a razão de verossimilhança (RV) e para a posteriori, e não um número só.

A segunda parte compara o desfecho com outra evidência disponível no ajuizamento: o **assunto 6226**. Para não usar os mesmos processos duas vezes, as verossimilhanças e a priori são estimadas em **2022–2023**, e a posteriori resultante é confrontada com os processos de **2024**, como teste preditivo.
"""),
    ("code", r"""
# 32.1 RV e posteriori com incerteza (Dirichlet-multinomial × Beta)
_ordem_d = ['acordo', 'mérito', 'extinção sem mérito', 'sem sentença registrada']
_cA = bay.loc[bay.Ha, 'desfecho'].astype(str).value_counts().reindex(_ordem_d, fill_value=0)
_c0 = bay.loc[~bay.Ha, 'desfecho'].astype(str).value_counts().reindex(_ordem_d, fill_value=0)
BP = pd.concat({nome: BY.bayes_processo(_cA, _c0, pri, seed=SEMENTE_BAYES + 20 + i)
                for i, (nome, pri) in enumerate([('Beta(6, 14): cenário CIJMG', (6, 14)),
                                                 ('Beta(1, 1): sem informação', (1, 1))])}, names=['priori P(Hₐ)'])
display(tabela_ptbr(BP.reset_index(level=0), casas=3))

# 32.2 Assunto 6226: verossimilhanças e priori de 2022–2023, previsão para 2024
_tr_b = _am_b.ano < 2024
_te_b = ~_tr_b
_Ha_b = _am_b.indicio == 1
_s6_b = _am_b.assunto.eq('6226')
BA = BY.bayes_assunto_temporal(int((_s6_b & _Ha_b & _tr_b).sum()), int((_Ha_b & _tr_b).sum()),
                               int((_s6_b & ~_Ha_b & _tr_b).sum()), int((~_Ha_b & _tr_b).sum()),
                               (1 + int((_Ha_b & _tr_b).sum()), 1 + int((~_Ha_b & _tr_b).sum())),
                               seed=SEMENTE_BAYES + 30)
_rng_pp = np.random.default_rng(SEMENTE_BAYES + 31)
_lin_a = []
for _nome, _mask, _post in [('assunto 6226', _s6_b, BA['post_6226']), ('demais assuntos', ~_s6_b, BA['post_outros'])]:
    _n24 = int((_mask & _te_b).sum())
    _k24 = int((_mask & _te_b & _Ha_b).sum())
    _pred = _rng_pp.binomial(_n24, _post)
    _lin_a.append({'grupo em 2024': _nome, 'processos': _n24, 'indícios observados': _k24,
                   'P(Hₐ | grupo) prevista': float(np.median(_post)),
                   'prevista inf.': float(np.quantile(_post, .025)), 'prevista sup.': float(np.quantile(_post, .975)),
                   'contagem prevista inf.': int(np.quantile(_pred, .025)),
                   'contagem prevista sup.': int(np.quantile(_pred, .975)),
                   'observado no intervalo preditivo': bool(np.quantile(_pred, .025) <= _k24 <= np.quantile(_pred, .975))})
TAB_ASSUNTO_PRED = pd.DataFrame(_lin_a)
display(tabela_ptbr(TAB_ASSUNTO_PRED, casas=3))
assert TAB_ASSUNTO_PRED['observado no intervalo preditivo'].all()

_bp = BP.loc['Beta(6, 14): cenário CIJMG'].set_index('dado')
_rv6 = BY.resumo(BA['RV_6226'])
_rvo = BY.resumo(BA['RV_outros'])
_ta = TAB_ASSUNTO_PRED.set_index('grupo em 2024')
V.update(bp_rv_ext=fnum(_bp.loc['extinção sem mérito', 'RV mediana'], 2),
         bp_rv_ext_ic=fic(_bp.loc['extinção sem mérito', 'RV inf.'], _bp.loc['extinção sem mérito', 'RV sup.']),
         bp_p_ext=fnum(_bp.loc['extinção sem mérito', 'P(RV > 1)'], 2),
         bp_post_ext=fnum(_bp.loc['extinção sem mérito', 'posteriori mediana'], 2),
         bp_post_ext_ic=fic(_bp.loc['extinção sem mérito', 'posteriori inf.'], _bp.loc['extinção sem mérito', 'posteriori sup.']),
         bp_rv_aco=fnum(_bp.loc['acordo', 'RV mediana'], 2),
         bp_rv_aco_ic=fic(_bp.loc['acordo', 'RV inf.'], _bp.loc['acordo', 'RV sup.']),
         bp_p_aco=fnum(_bp.loc['acordo', 'P(RV > 1)'], 2),
         rv6=fnum(_rv6['mediana'], 1), rv6_ic=fic(_rv6['IC cred. inf.'], _rv6['IC cred. sup.'], casas=1),
         rvo=fnum(_rvo['mediana'], 2), rvo_ic=fic(_rvo['IC cred. inf.'], _rvo['IC cred. sup.']),
         pred6=fpct(_ta.loc['assunto 6226', 'P(Hₐ | grupo) prevista'], 1),
         pred6_ic=fic(_ta.loc['assunto 6226', 'prevista inf.'], _ta.loc['assunto 6226', 'prevista sup.'], pct=True, casas=1),
         obs6=f"{fint(_ta.loc['assunto 6226', 'indícios observados'])}/{fint(_ta.loc['assunto 6226', 'processos'])}",
         predo=fpct(_ta.loc['demais assuntos', 'P(Hₐ | grupo) prevista'], 1),
         predo_ic=fic(_ta.loc['demais assuntos', 'prevista inf.'], _ta.loc['demais assuntos', 'prevista sup.'], pct=True, casas=1),
         obso=f"{fint(_ta.loc['demais assuntos', 'indícios observados'])}/{fint(_ta.loc['demais assuntos', 'processos'])}")
display(Markdown(C.preencher(r'''
**Leitura (R6–R8 com incerteza).**

- **O desfecho continua sendo evidência fraca.** A extinção sem mérito tem RV {{bp_rv_ext}} (IC cred. 95% {{bp_rv_ext_ic}}), com P(RV > 1) = {{bp_p_ext}}. Com a priori Beta(6, 14), a posteriori P(Hₐ | extinção) tem mediana {{bp_post_ext}}, mas o intervalo {{bp_post_ext_ic}} é quase tão largo quanto a própria priori. O acordo tem RV {{bp_rv_aco}} {{bp_rv_aco_ic}} (P(RV > 1) = {{bp_p_aco}}). A Seção 6 dava a mesma direção, mas um número exato; aqui fica visível que **a incerteza da priori domina** e que o desfecho mal a reduz.
- **O assunto é evidência forte.** Estimada em 2022–2023, a RV do assunto 6226 é **{{rv6}}** {{rv6_ic}}, e a dos demais assuntos, {{rvo}} {{rvo_ic}}. É a diferença entre uma evidência que move a crença uma ordem de grandeza e uma que quase não a move.
- **Teste preditivo em 2024.** Com a priori e as verossimilhanças de 2022–2023, a posteriori prevista para 2024 é {{pred6}} {{pred6_ic}} no 6226, e o observado foi {{obs6}}. Nos demais assuntos, a previsão é {{predo}} {{predo_ic}}, e o observado foi {{obso}}. As duas contagens caem dentro do intervalo preditivo: a atualização bayesiana feita com um período **prevê** o período seguinte.

**Cautela.** A RV do assunto mede quanto o assunto reproduz o **rótulo** da pesquisa. Se F3_19 e F3_20 foram avaliados olhando a massa de ações do mesmo assunto, parte da força dessa evidência é da própria regra de codificação (Seção 33). Isso não a torna inútil para triagem, mas a impede de ser lida como prova de predação de um processo individual.
''', V)))
"""),
    ("markdown", r"""
## 33. A prevalência quando a codificação pode errar

Os rótulos F1–F3 foram atribuídos por uma única codificadora, sem segunda leitura (Seção 2.6). A Seção 19 mostrou o efeito de taxas de erro **fixas** e hipotéticas. Aqui a sensibilidade (Se) e a especificidade (Sp) da codificação recebem prioris, e a prevalência verdadeira π é estimada com toda essa incerteza:

$$P(\text{rótulo} = 1) = \pi\,Se + (1-\pi)(1-Sp).$$

Sem processos recodificados, os dados **não identificam** Se e Sp: a posteriori delas é igual à priori, e a de π herda essa incerteza (GUSTAFSON, 2015; JOSEPH; GYORKOS; COUPAL, 1995). Por isso a seção compara cenários, e não escolhe um. Os cenários são declarados abaixo, com a média e a dispersão de cada priori. A conta usa o binomial dos 595, porque a amostra é autoponderada. A correção de população finita (fração amostral de 1,2%) é desprezível.
"""),
    ("code", r"""
# 33.1 Prevalência com Se e Sp incertas (amostragem-reamostragem por importância)
CENARIOS_ERRO = {
    'codificação perfeita (Se = Sp = 1)': None,
    'Seção 19 com incerteza: Se ~ Beta(45, 5), Sp ~ Beta(99, 1)': ((45, 5), (99, 1)),
    'codificadora mais sensível que específica: Se ~ Beta(98, 2), Sp ~ Beta(48, 2)': ((98, 2), (48, 2)),
    'erro maior nos dois sentidos: Se ~ Beta(16, 4), Sp ~ Beta(97, 3)': ((16, 4), (97, 3)),
}
_k, _n = funil['indicio'], funil['n']
_lin_e = []
for _i, (_nome, _pri) in enumerate(CENARIOS_ERRO.items()):
    if _pri is None:
        _pi = stats.beta(1 + _k, 1 + _n - _k).rvs(40_000, random_state=SEMENTE_BAYES + 40)
        _se_m = _sp_m = 1.0
        _ess = np.nan
    else:
        _e = BY.prevalencia_com_erro(_k, _n, _pri[0], _pri[1], seed=SEMENTE_BAYES + 41 + _i)
        _pi, _se_m, _sp_m, _ess = _e['pi'], float(_e['se'].mean()), float(_e['sp'].mean()), _e['ess_importancia']
    _r = BY.resumo(_pi)
    _lin_e.append({'cenário': _nome, 'Se média (posteriori)': _se_m, 'Sp média (posteriori)': _sp_m,
                   'π mediana': _r['mediana'], 'π inf.': _r['IC cred. inf.'], 'π sup.': _r['IC cred. sup.'],
                   'total na moldura (mediana)': _r['mediana'] * len(base), 'ESS da importância': _ess})
TAB_ERRO = pd.DataFrame(_lin_e)
display(tabela_ptbr(TAB_ERRO, casas=3, pct=['π mediana', 'π inf.', 'π sup.']))
_te = TAB_ERRO.set_index('cenário')
V.update(err_min=fpct(TAB_ERRO['π mediana'].min(), 1), err_max=fpct(TAB_ERRO['π mediana'].max(), 1),
         err_lo=fpct(TAB_ERRO['π inf.'].min(), 1), err_hi=fpct(TAB_ERRO['π sup.'].max(), 1),
         err_s19=fpct(_te.iloc[1]['π mediana'], 1), err_s19_ic=fic(_te.iloc[1]['π inf.'], _te.iloc[1]['π sup.'], pct=True, casas=1),
         err_esp=fpct(_te.iloc[2]['π mediana'], 1), err_esp_ic=fic(_te.iloc[2]['π inf.'], _te.iloc[2]['π sup.'], pct=True, casas=1))
display(Markdown(C.preencher(r'''
**Leitura.** Com codificação perfeita, a prevalência é {{p_indicio}}. No cenário da Seção 19, agora com incerteza, a mediana sobe para {{err_s19}} {{err_s19_ic}}: falsos negativos raros, mas possíveis, escondem predação. Se a codificadora marcasse indício com facilidade (Sp baixa), a mediana cairia para {{err_esp}} {{err_esp_ic}}. Entre os cenários, as medianas vão de {{err_min}} a {{err_max}}, e os intervalos, de {{err_lo}} a {{err_hi}}.

**Consequência.** A incerteza de medição pode ser **maior que a amostral**: o intervalo de Wilson ou do desenho supõe Se = Sp = 1. Sem uma subamostra recodificada, nenhum desses cenários pode ser preferido pelos dados. Se houver ocasião, uma segunda leitura independente de algumas dezenas de processos (com κ e uma tabela de concordância) informaria as prioris de Se e Sp e reduziria esse intervalo. Os modelos das Seções 31 e 32 também reproduzem o rótulo **tal como codificado**.
''', V)))
"""),
    ("markdown", r"""
## 34. Logística bayesiana para a quase separação

Na Seção 8, F2_01 e F2_02 andam juntas (φ = 0,97). Com isso, a máxima verossimilhança dá intervalos enormes e, no passo da certeza (30 eventos em 105), erros-padrão indefinidos. O Firth resolve parte do problema com uma penalização. A alternativa bayesiana é declarar que efeitos gigantescos são **improváveis a priori**. Aqui, cada coeficiente recebe uma t de Student com 3 graus de liberdade e escala 2,5, com os preditores centrados (GELMAN et al., 2008). Essa priori ainda admite ORs de 100 ou mais, mas não infinitos.

A comparação entre modelos usa a validação cruzada aproximada por LOO-PSIS (VEHTARI; GELMAN; GABRY, 2017), que estima o desempenho preditivo fora da amostra. O elpd é a log-densidade preditiva esperada: maior é melhor, e uma diferença menor que cerca de dois erros-padrão é empate prático.
"""),
    ("code", r"""
# 34.1 Passo 1 (indício | Fase III) e passo 2 (certeza | indício), com LOO
import arviz as az
_X1 = d233[X_HADJA].astype(int)
_d_ind = d233[sub]
_y2 = (y3[sub] == 2).astype(int)
with C.capturar_avisos('logística bayesiana (PyMC)', AVISOS):
    LB1 = BY.logistica_bayes(_X1, y_ind, seed=SEMENTE_BAYES + 50)
    LB1_sem01 = BY.logistica_bayes(d233[['F2_02', 'F2_11']].astype(int), y_ind, seed=SEMENTE_BAYES + 51)
    LB1_nulo = BY.logistica_bayes(d233[[]], y_ind, seed=SEMENTE_BAYES + 52)
    LB2 = BY.logistica_bayes(_d_ind[X_HADJA].astype(int), _y2, seed=SEMENTE_BAYES + 53)
    LB2_nulo = BY.logistica_bayes(_d_ind[[]], _y2, seed=SEMENTE_BAYES + 54)
    LOO1 = az.compare({'F2_01 + F2_02 + F2_11': LB1['idata'], 'F2_02 + F2_11': LB1_sem01['idata'],
                       'só intercepto': LB1_nulo['idata']}, ic='loo')
    LOO2 = az.compare({'F2_01 + F2_02 + F2_11': LB2['idata'], 'só intercepto': LB2_nulo['idata']}, ic='loo')
for _m in (LB1, LB1_sem01, LB1_nulo, LB2, LB2_nulo):
    assert _m['diagnosticos']['R-hat máximo'] < 1.01 and _m['diagnosticos']['divergências'] == 0

_mle = pd.DataFrame({'termo': X_HADJA, 'OR (MV)': np.exp(MOD_HADJA.params[X_HADJA]).to_numpy(),
                     'IC MV inf.': np.exp(MOD_HADJA.conf_int().loc[X_HADJA, 0]).to_numpy(),
                     'IC MV sup.': np.exp(MOD_HADJA.conf_int().loc[X_HADJA, 1]).to_numpy(),
                     'OR (Firth)': FIRTH_H.loc[X_HADJA, 'OR'].to_numpy(),
                     'IC Firth inf.': FIRTH_H.loc[X_HADJA, 'ic_lo'].to_numpy(),
                     'IC Firth sup.': FIRTH_H.loc[X_HADJA, 'ic_hi'].to_numpy()})
TAB_LB1 = _mle.merge(LB1['tabela'], on='termo')
display(tabela_ptbr(TAB_LB1, casas=2))
display(tabela_ptbr(LB2['tabela'], casas=2))
display(LOO1[['rank', 'elpd_loo', 'p_loo', 'elpd_diff', 'dse', 'weight']].round(2))
display(LOO2[['rank', 'elpd_loo', 'p_loo', 'elpd_diff', 'dse', 'weight']].round(2))

# probabilidade a posteriori por padrão de sinais e o funil completo P(certeza) = P(indício) × P(certeza | indício)
_pads = pad[X_HADJA + ['n', 'indicios']].copy()
_p1 = BY.prob_padroes(LB1, _pads[X_HADJA])
_p2 = BY.prob_padroes(LB2, _pads[X_HADJA])
_pads['observado'] = _pads.indicios / _pads.n
_pads['P(indício) mediana'] = np.median(_p1, 0)
_pads['P(indício) inf.'] = np.quantile(_p1, .025, 0)
_pads['P(indício) sup.'] = np.quantile(_p1, .975, 0)
_pads['P(certeza) mediana'] = np.median(_p1 * _p2, 0)
_pads['P(certeza) inf.'] = np.quantile(_p1 * _p2, .025, 0)
_pads['P(certeza) sup.'] = np.quantile(_p1 * _p2, .975, 0)
display(tabela_ptbr(_pads, casas=3))

_lb = LB1['tabela'].set_index('termo')
_lb2 = LB2['tabela'].set_index('termo')
_tl = TAB_LB1.set_index('termo')
_pc = _pads.set_index(X_HADJA)
V.update(lb_or02=fnum(_lb.loc['F2_02', 'OR mediana'], 1), lb_or02_ic=fic(_lb.loc['F2_02', 'OR inf.'], _lb.loc['F2_02', 'OR sup.'], 1),
         lb_or01=fnum(_lb.loc['F2_01', 'OR mediana'], 2), lb_or01_ic=fic(_lb.loc['F2_01', 'OR inf.'], _lb.loc['F2_01', 'OR sup.'], 2),
         lb_or11=fnum(_lb.loc['F2_11', 'OR mediana'], 2), lb_or11_ic=fic(_lb.loc['F2_11', 'OR inf.'], _lb.loc['F2_11', 'OR sup.'], 2),
         lb_mv02_ic=fic(_tl.loc['F2_02', 'IC MV inf.'], _tl.loc['F2_02', 'IC MV sup.'], 1),
         lb2_or02=fnum(_lb2.loc['F2_02', 'OR mediana'], 2), lb2_or02_ic=fic(_lb2.loc['F2_02', 'OR inf.'], _lb2.loc['F2_02', 'OR sup.'], 2),
         lb2_or11=fnum(_lb2.loc['F2_11', 'OR mediana'], 2), lb2_or11_ic=fic(_lb2.loc['F2_11', 'OR inf.'], _lb2.loc['F2_11', 'OR sup.'], 2),
         lb2_p02=fnum(_lb2.loc['F2_02', 'P(β > 0)'], 2),
         loo1_melhor=LOO1.index[0], loo1_dif01=fnum(LOO1.loc['F2_01 + F2_02 + F2_11', 'elpd_diff'], 2),
         loo1_dse01=fnum(LOO1.loc['F2_01 + F2_02 + F2_11', 'dse'], 2),
         loo1_difnulo=fnum(LOO1.loc['só intercepto', 'elpd_diff'], 1), loo1_dsenulo=fnum(LOO1.loc['só intercepto', 'dse'], 1),
         loo2_melhor=LOO2.index[0], loo2_dif=fnum(LOO2['elpd_diff'].max(), 2), loo2_dse=fnum(LOO2['dse'].max(), 2),
         pc111=fpct(_pc.loc[(1, 1, 1), 'P(certeza) mediana'], 1),
         pc111_ic=fic(_pc.loc[(1, 1, 1), 'P(certeza) inf.'], _pc.loc[(1, 1, 1), 'P(certeza) sup.'], pct=True, casas=1),
         pi111=fpct(_pc.loc[(1, 1, 1), 'P(indício) mediana'], 1),
         pi111_ic=fic(_pc.loc[(1, 1, 1), 'P(indício) inf.'], _pc.loc[(1, 1, 1), 'P(indício) sup.'], pct=True, casas=1),
         pi000=fpct(_pc.loc[(0, 0, 0), 'P(indício) mediana'], 1),
         pi000_ic=fic(_pc.loc[(0, 0, 0), 'P(indício) inf.'], _pc.loc[(0, 0, 0), 'P(indício) sup.'], pct=True, casas=1),
         lb_rhat=fnum(max(m['diagnosticos']['R-hat máximo'] for m in (LB1, LB1_sem01, LB1_nulo, LB2, LB2_nulo)), 3))
display(Markdown(C.preencher(r'''
**Leitura (R10–R13 com prioris fracamente informativas).**

- **Passo 1, indício na Fase III.** O OR de F2_02 é {{lb_or02}} (IC cred. 95% {{lb_or02_ic}}), contra o IC de máxima verossimilhança {{lb_mv02_ic}}. A estimativa fica no mesmo lugar, mas o limite superior deixa de ser arbitrário. F2_11: {{lb_or11}} {{lb_or11_ic}}. F2_01: {{lb_or01}} {{lb_or01_ic}}, porque a informação está no par F2_01/F2_02, e não em cada um.
- **LOO no passo 1.** O melhor modelo é "{{loo1_melhor}}". Incluir F2_01 muda o elpd em {{loo1_dif01}} (EP da diferença {{loo1_dse01}}): empate prático. Retirar todos os sinais custa {{loo1_difnulo}} (EP {{loo1_dsenulo}}). Os sinais formais predizem o indício, e F2_01 é redundante dado F2_02.
- **Passo 2, certeza dado indício.** F2_02: OR {{lb2_or02}} {{lb2_or02_ic}}, com P(β > 0) = {{lb2_p02}}; F2_11: {{lb2_or11}} {{lb2_or11_ic}}. Os intervalos são finitos, o que a máxima verossimilhança não dava, e ficam centrados em um. Pelo LOO, o melhor modelo é "{{loo2_melhor}}" (diferença {{loo2_dif}}; EP {{loo2_dse}}). **Os sinais da petição não predizem a certeza**: a conclusão da razão contínua (Seção 8.2) agora tem uma medida preditiva direta.
- **Funil completo.** Com os três sinais presentes, P(indício) = {{pi111}} {{pi111_ic}} e P(certeza) = {{pc111}} {{pc111_ic}}. Sem nenhum sinal, P(indício) = {{pi000}} {{pi000_ic}}.
- **Diagnósticos.** R-hat máximo {{lb_rhat}} e nenhuma divergência nos cinco ajustes.
''', V)))
"""),
    ("markdown", r"""
## 35. Resposta final ao roteiro

Esta tabela substitui a síntese provisória da Seção 14. Ela reúne os resultados das Partes I a VI. Todos os números são calculados neste notebook.
"""),
    ("code", r"""
# 35.1 Consolidação dos números das Partes V e VI para a resposta final
_aval25 = TAB_AVALIACAO_25.set_index('avaliação')
_com28 = TAB_COMBINACAO_28.set_index('informação')
_bench = BENCH.set_index('método')
V.update(fin_auc_ajz=fnum(_aval25.loc['modelo congelado em 2024', 'AUC'], 3),
         fin_ap_ajz=fnum(_aval25.loc['modelo congelado em 2024', 'precisão média'], 3),
         fin_auc_ajz_cv=fnum(_aval25.loc['procedimento completo: CV externa, 2022–2023', 'AUC'], 3),
         fin_auc_ajz_ic=fic(_boot_25['AUC'].quantile(.025), _boot_25['AUC'].quantile(.975), casas=3),
         fin_auc_s24=fnum(_tabela_e.set_index('modelo').loc['regressão logística com assunto', 'AUC 2024'], 3),
         fin_auc_s28=fnum(_com28.loc['assunto da moldura', 'AUC 2024'], 4),
         fin_auc_traj=fnum(_com28.loc['trajetória DataJud', 'AUC 2024'], 3),
         fin_ari=fnum(_bench.loc['LCA categórica', 'ARI com rótulos existentes'], 3),
         fin_kp24=fnum(kp_2024, 3), fin_cert3=fint(int(TAB_VALIDACAO_3.loc[TAB_VALIDACAO_3.classe == 'certeza', 'n real'].iloc[0])))
display(Markdown(C.preencher(r'''
| Item | Resposta | Seções |
|---|---|---|
| R1–R2 | A probabilidade de indício depende do denominador: {{den_595}} entre os sorteados, {{den_444}} entre os elegíveis e {{den_233}} na Fase III. P(indício \| F2_02) = {{F2_02_lin_sim}}, mas P(F2_02 \| indício) = {{F2_02_col_ind}}. | 5 |
| R3–R4 | Bayes na notação do professor, com dois pares H₀ × Hₐ: o processo (partição do espaço amostral) e a prevalência (partição do espaço de θ). | 6 |
| R5, R9 | Priori principal de 0,30 (NT CIJMG e Araripina) e Beta(6, 14), com sensibilidade a outras quatro prioris. A revisão de escopo é conceitual; os números vêm das notas técnicas. A NT fala de dois assuntos: no assunto 6226, P(θ ≥ 0,30) = {{mrp_p6226_30}}; na moldura inteira, {{mrp_pind_30}}. | 6, 31 |
| R6 | Desfecho pelo proxy TPU completo. RV(extinção) = {{bp_rv_ext}} {{bp_rv_ext_ic}} e RV(acordo) = {{bp_rv_aco}} {{bp_rv_aco_ic}}: evidência **fraca**. Para contraste, RV(assunto 6226) = {{rv6}} {{rv6_ic}}, estimada em 2022–2023. | 3, 6, 32 |
| R7–R8 | Com priori 0,30 e extinção: P(D) = {{bay_0_tot03}} e posteriori {{bay_0_post03}}. Com a priori incerta, a posteriori é {{bp_post_ext}} {{bp_post_ext_ic}}. A atualização feita com 2022–2023 prevê 2024: {{pred6}} previsto contra {{obs6}} observado no 6226. | 6, 32 |
| R10 | Multinomial: RRR de F2_02 = {{mn_rrr_ind_02}} (indício) e {{mn_rrr_cert_02}} (certeza). | 8 |
| R11 | Ordinal: chances proporcionais **rejeitadas** (LR = {{lr_po}}; {{p_po}}); o PPO com F2_02 livre é adequado. Na razão contínua, os F2 não separam a certeza. Na versão bayesiana, OR de F2_02 no segundo passo = {{lb2_or02}} {{lb2_or02_ic}}, e o LOO prefere o modelo sem sinais. | 8, 34 |
| R12 | Logística condicional (JEC × ano, {{cl_uteis}} estratos úteis): OR de F2_11 = {{cl_or11}} {{cl_or11_ic}}, maior que o marginal, mas com intervalos sobrepostos. | 8 |
| R13 | Melhor ajuste: {{aj_bic_melhor}} pelo BIC e {{cv_melhor}} fora da amostra. Contra a Hadja, **empate** na dicotomia. Nenhum modelo acerta a certeza fora do ajuste (0 de {{fin_cert3}}). | 9, 17, 25, 34 |
| R14 | AUC = {{auc_h}} e Gini = {{gini_h}} em **todos** os modelos, porque há só {{n_padroes}} padrões de preditores; fora da amostra, AUC = {{cv_auc}}. Só com o assunto, conhecido no ajuizamento, AUC = {{fin_auc_ajz}} em 2024 {{fin_auc_ajz_ic}}, com o modelo escolhido apenas em 2022–2023. | 9, 26 |
| R15–R16 | A LCA não supervisionada do DataJud encontra três **trajetórias processuais**. Na amostra, o kappa ponderado contra a Hadja é {{av_kpond}} e o J é {{av_J}}; em 2024, fora do ajuste, o kappa ponderado é {{fin_kp24}} e o ARI {{fin_ari}}. O DataJud tem sinal, mas no **assunto**, e não na trajetória: uma logística supervisionada chega a AUC {{sup_auc}}, que cai para {{sup_auc_sem}} sem o assunto. | 10, 15, 28 |
| R17–R18 | Perfis de trajetória em `estcaso3_revisado/tabelas/trajetorias_processuais.xlsx`: {{lista_0}} / {{lista_1}} / {{lista_2}} processos. Não servem como listas de predação nem para triagem. | 11 |
| R19 | Pela amostra: {{p_indicio}}, intervalo do desenho {{des_ic_logit}}; sem os 2 não localizados, {{p_593}} {{ic_593}}. MRP com o assunto de toda a moldura: **{{mrp_ind}} {{mrp_ind_ic}}**, isto é, {{mrp_tot}} processos {{mrp_tot_ic}}; a mediana fica {{mrp_dentro_pub}} do intervalo publicado. Certeza: {{mrp_cer}} {{mrp_cer_ic}}, ou {{mrp_tot_c}} processos. O intervalo publicado é Wald com correção de população finita, e não Wilson. Se a codificação errar, a prevalência pode ir de {{err_min}} a {{err_max}}. | 12, 16, 31, 33 |
| P1 | CA de JEC × classe3 (inércia {{ca_inercia}} = χ²/n; {{ca_p}}); MCA com eixo documental dominante ({{mca_b1}} pela correção de Benzécri); biplots simétrico, assimétrico e de contribuição. | 7 |
| P2 | Gerador encadeado (LCA → logística → desfecho → lognormal), simulação do funil, recuperação dos parâmetros e Quadro de Variáveis ({{qt_n}} linhas) para a turma. | 2, 13, 19, 23 |

**Conclusão do estudo.**

1. **O que separa o indício.** Os sinais formais da petição (F2_01/F2_02 e F2_11) separam o indício na Fase III (AUC ≈ {{cv_auc}} fora da amostra). No ajuizamento, o **assunto** sozinho tem desempenho semelhante (AUC {{fin_auc_ajz}} em 2024): o assunto 6226 tem prevalência de {{mrp_6226}}, contra {{mrp_outros}} nos demais.
2. **O que não separa.** Nada do que foi observado separa a **certeza** do indício. A certeza depende de F3_18 (multiplicidade de ações da parte), que não está na petição nem no DataJud. A **trajetória** processual do DataJud (desfecho, recurso, tempo, movimentos) acrescenta pouco ao assunto (AUC {{fin_auc_traj}} sozinha).
3. **A prevalência.** A melhor estimativa usa o desenho e a informação auxiliar da moldura: {{mrp_ind}} {{mrp_ind_ic}}. A maior incerteza restante é de **medição** (uma codificadora), e não de amostragem.
4. **Validade.** A força do assunto pode refletir, em parte, o modo como F3_19 e F3_20 foram avaliados. Antes de qualquer uso em triagem, o modelo precisa ser validado numa coorte posterior a 2024, com rótulos atribuídos sem conhecer o assunto.

**Sobre as três AUCs do modelo de assunto.** A Seção 24 relata {{fin_auc_s24}} (regularização C = 0,3, fixada na exploração). A Seção 26 relata {{fin_auc_ajz}}, com C escolhido por validação cruzada aninhada só em 2022–2023: **é o número de referência**. A Seção 28 relata {{fin_auc_s28}} com o mesmo modelo, nos 593 processos com documento no DataJud.
''', V)))
"""),
]
