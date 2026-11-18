# Parte VIII — Síntese, conclusões, limitações e recomendações (seções 8.1 a 8.5). As referências ficam em secao98_referencias.py.
# Executado por build_rafaelcc_ed2.py (exec): usa md(), code() e interp().
# Lê as estimativas exportadas pelas Partes III a VI (dat/processado e tab/); não refaz análises.

md(r'''
# PARTE VIII — SÍNTESE E CONCLUSÕES

Esta parte reúne os achados das Partes I a VII:

- uma síntese executiva com a tabela-resumo das estimativas (8.1);
- um gráfico dos efeitos (8.2);
- a resposta à pergunta de pesquisa (8.3);
- as limitações e as recomendações para uma replicação, com o cálculo de poder (8.4);
- as considerações finais (8.5).

Os números vêm das tabelas exportadas pelas partes anteriores, com a seção de origem indicada. As referências de todo o notebook estão na seção **Referências**.
''')

md(r'''
## 8.1 Síntese executiva

1. **Os números divulgados não medem a duração.** As médias de 78,46 e 75,2 dias misturam sentenciados com processos ainda em curso (209 "ativos" na planilha; 206 censurados na base primária) e contam redistribuições como desfecho (2.1.2). A mediana de Kaplan-Meier é de 89 dias (4.2). Os "106,8 dias" anteriores não são verificáveis com a mesma definição; a medida mais próxima no DataJud dá 93,6 dias (6.6.4).
2. **A AC obrigatória não acelerou os processos; na Remota, alongou-os.** As medianas são de 81, 96 e 95 dias (log-rank p = 0,023; estratificado por mês, 0,045), um atraso de cerca de duas semanas.
   - **Remota**: HR 0,81 (0,67–0,97; p = 0,022) e ΔRMST180 de +10,7 dias (1,9 a 19,5).
   - **Presencial**: mesma direção, sem significância (HR 0,87, 0,72–1,04; +6,5 dias, −2,1 a 15,8).
   - Robustez: 11 de 12 cenários de curadoria (4.9) e seguimento estendido até 06/11/2026 (HR da Remota 0,75, 0,63–0,89; 6.4).
3. **Muda o tipo de sentença, com graus diferentes de certeza.**
   - O **déficit de mérito** é robusto: Fine-Gray sHR 0,46 e 0,42; em horizonte fixo, de 18 a 23 p.p. abaixo do Controle de 90 a 150 dias (Holm < 0,001; 3.2.6). Em parte, reflete a própria lentidão.
   - O **excesso de extinções sem mérito** é sugestivo, e mais claro na Presencial: sHR 1,46 (p = 0,014) e 1,32 (p = 0,081). Ele vai de 30,2% para 47,4% e 45,4% entre os sentenciados e de 25,2% para 34,7% e 31,5% entre os distribuídos, que são limites opostos; em horizonte fixo, não sobrevive ao Holm (p ≥ 0,164).
   - O excesso está nas extinções após 30 dias, o que é compatível com o art. 51, I, da Lei 9.099/1995; a planilha, porém, não registra o motivo.
4. **O acordo não aumentou na audiência; na Remota, há sinal sugestivo de mais acordos fora dela.**
   - Acordo na AC: 5,1% e 4,6% (Fisher p = 1,000).
   - Acordo em qualquer momento, Remota × Controle: RR 1,98 (+7,7 p.p.) entre os encerrados; RR 2,49 até 120 dias; CMH 2,72 (p = 0,004); sHR 1,87 (1,00–3,47). O excedente vem de fora da audiência.
   - O sinal é **sugestivo**: sobrevive ao BH, mas não ao Holm global sobre os 71 testes da Parte III.
   - Os 13,3% históricos (homologações ÷ sentenças) só se comparam com os 11,4% de mesma definição (2.5.2), e não com o acordo por audiência.
5. **Modalidade, técnica e híbrida não fizeram diferença demonstrável.** Presencial × Remota não difere no tempo (p = 0,519) nem em nenhuma causa do Fine-Gray. A modalidade, além disso, está confundida com a conciliadora. As técnicas foram sorteadas de modo uniforme (p = 0,566).
6. **Os dados são fidedignos, e o desenho é um ECA de unidade única com aleatorização não verificável.**
   - O DataJud confirma a planilha (κ = 0,961; datas 97,9% iguais; fins de semana reais), e o Controle de 2026 tramitou como o 4º JEC de 2025 (6.3, 6.6.3).
   - O sorteio não foi documentado nem ocultado, e o 4º JEC já era atípico em 2025. Não há base estatística para generalizar aos 14 JECs (7.1, 7.9).
''')

code(r'''
if 'dados' not in globals():
    dados = pd.read_pickle(PROC / 'ed2_tidy.pkl')
import re
from scipy.stats import norm


def s8_csv(nome, pasta='tab', **kw):
    caminho = RAIZ / pasta / nome
    if not caminho.exists():
        print(f'Aviso: {pasta}/{nome} não encontrado (é gerado pelas Partes III a VI).')
        return None
    opcoes = dict(sep=';', decimal=',', encoding='utf-8-sig')
    opcoes.update(kw)
    return pd.read_csv(caminho, **opcoes)


def s8_num(texto):
    """'0,87 (0,72–1,04)' → [0.87, 0.72, 1.04]."""
    return [float(x.replace(',', '.')) for x in re.findall(r'-?\d+(?:,\d+)?', str(texto))]


sint_sob = s8_csv('ed2_sintese_sobrevivencia.csv', pasta='dat/processado', index_col=0, decimal='.')
reg3 = s8_csv('ed2_parte3_testes.csv', pasta='dat/processado')
pares_tipo = s8_csv('tst_tipobin_pares.csv')
horiz_tipo = s8_csv('tst_tipo_horizontes.csv')
pares_120 = s8_csv('tst_acordo_horizonte_pares.csv')
tempo_tipo = s8_csv('tst_tempo_por_tipo.csv')
acordo_ac = s8_csv('tst_acordo_ac.csv')
logit_a = s8_csv('mul_logit_A_contrastes.csv')
fg_boot = s8_csv('sob_fine_gray_bootstrap.csv')
dj_est = s8_csv('dj_comparacao_estendido.csv')
n_inf3 = int((reg3['Natureza'] != 'didático').sum()) if reg3 is not None else np.nan


def s8_holm(trecho):
    """p bruto e p Holm global do registro de testes da Parte III (pelo nome do teste)."""
    if reg3 is None:
        return np.nan, np.nan
    lin = reg3[reg3['Teste'].str.contains(trecho, regex=False)]
    return (float(lin['p'].iloc[0]), float(lin['p Holm global'].iloc[0])) if len(lin) else (np.nan, np.nan)


def s8_par(tipo, comp):
    return pares_tipo[(pares_tipo['Tipo'] == tipo) & (pares_tipo['Comparação'] == comp)].iloc[0]


def s8_pct_xn(xn):
    x, n = (int(v) for v in str(xn).split('/'))
    return f'{pct_br(x / n, 1)} ({x}/{n})'


def s8_fg(desfecho, contraste):
    l = fg_boot[(fg_boot['Desfecho'] == desfecho) & (fg_boot['Contraste'] == contraste)].iloc[0]
    return float(l['sHR']), float(l['IC 95% inf. (bootstrap)']), float(l['IC 95% sup. (bootstrap)']), float(l['p (bootstrap)'])


col_s = list(sint_sob.columns) if sint_sob is not None else []
linhas = []
if sint_sob is not None:
    for chave, leitura, sec in [
        ('Mediana KM, dias (IC 95%)', 'maior = mais lento', '4.2.3'),
        ('RMST 180 d, dias (IC 95%)', 'dias sem sentença nos primeiros 180 d', '4.3.6'),
        ('ΔRMST 180 d vs. Controle (IC bootstrap)', '> 0 = mais lento que o Controle', '4.3.6'),
        ('HR Cox (b) (IC 95%)', '< 1 = sentença mais lenta; ajustado por mês e origem; p = 0,117 (P) e 0,022 (R)', '4.5.1'),
        ('Razão de tempos Weibull (IC 95%)', '> 1 = mais lento; Remota p = 0,051 (IC toca 1)', '4.6'),
    ]:
        v = sint_sob.loc[chave]
        linhas.append(['Tempo até a sentença (corte 07/10/2026)', chave.replace(' (IC 95%)', '').replace(' (IC bootstrap)', ''),
                       v.iloc[0], v.iloc[1], v.iloc[2], leitura, sec])
if dj_est is not None:
    e = dj_est.set_index('Medida').iloc[:, 1]
    linhas.append(['Seguimento estendido (DataJud, 06/11/2026)', 'HR Cox (b)', 'referência', e['HR Presencial (IC 95%)'],
                   e['HR Remota (IC 95%)'], 'sensibilidade; 797 sentenças; riscos proporcionais não rejeitados', '6.4.3'])
    linhas.append(['Seguimento estendido (DataJud, 06/11/2026)', 'ΔRMST 180 d (dias)', 'referência', e['ΔRMST180 Presencial (dias)'],
                   e['ΔRMST180 Remota (dias)'], '> 0 = mais lento que o Controle', '6.4.3'])
if fg_boot is not None:
    for desf, rot in [('Mérito', 'Sentença de mérito'), ('Sem mérito', 'Extinção sem mérito'), ('Homologação', 'Homologação de acordo')]:
        cel = []
        for contr in ['AC presencial × Controle', 'AC remota × Controle']:
            est, lo, hi, p = s8_fg(desf, contr)
            cel.append(f'{fmt_br(est, 2)} ({fmt_br(lo, 2)}–{fmt_br(hi, 2)}); p = {fmt_p(p)}')
        est, lo, hi, p = s8_fg(desf, 'AC remota × AC presencial')
        linhas.append(['Riscos competitivos (Fine-Gray, sHR)', rot, 'referência', cel[0], cel[1],
                       f'IC bootstrap; Remota × Presencial {fmt_br(est, 2)} (p = {fmt_p(p)})', '4.7.5'])
if horiz_tipo is not None:
    h = horiz_tipo[horiz_tipo['Horizonte (dias)'] == 120]
    ph_rng = {t: horiz_tipo.loc[horiz_tipo['Tipo'] == t, 'p Holm'] for t in ['Sentença de mérito', 'Extinção sem mérito']}
    for tipo in ['Sentença de mérito', 'Extinção sem mérito']:
        hp = h[(h['Tipo'] == tipo) & (h['Comparação'] == 'Presencial × Controle')].iloc[0]
        hr_ = h[(h['Tipo'] == tipo) & (h['Comparação'] == 'Remota × Controle')].iloc[0]
        cel = lambda l: f'{s8_pct_xn(l["Braço"])}; {l["Dif. p.p. [IC Newcombe]"]} p.p.; p Holm {fmt_p(l["p Holm"])}'
        faixa = (f'Holm < 0,001 nos 8 pares' if ph_rng[tipo].max() < 0.001 else
                 f'Holm de {fmt_p(ph_rng[tipo].min())} a {fmt_p(ph_rng[tipo].max())} nos 8 pares')
        linhas.append(['Horizonte fixo de 120 d (sem censura)', tipo, s8_pct_xn(hp['Controle']), cel(hp), cel(hr_),
                       f'Fisher; 65 a 150 d: {faixa}', '3.2.6'])
if pares_tipo is not None:
    for tipo, rot in [('Sentença de mérito', 'Sentença de mérito'), ('Extinção sem mérito', 'Extinção sem mérito'),
                      ('Homologação de acordo', 'Homologação de acordo')]:
        lp, lr_ = s8_par(tipo, 'Presencial × Controle'), s8_par(tipo, 'Remota × Controle')
        celula = lambda l: (f'{s8_pct_xn(l["x/n (1º)"])}; OR {fmt_br(l["OR"], 2)} ({fmt_br(l["OR IC inf"], 2)}–'
                            f'{fmt_br(l["OR IC sup"], 2)}); p Holm {fmt_p(l["p Holm"])}')
        linhas.append(['% dos sentenciados (condicional)', rot, s8_pct_xn(lp['x/n (2º)']), celula(lp), celula(lr_),
                       ('limite superior; ' if tipo == 'Extinção sem mérito' else 'condicional (exclui os ativos); ')
                       + 'Fisher, Holm em 9 pares', '3.2.3'])
    sm = dados.assign(sm=dados['tipo_desfecho'].astype(str).eq('Sem mérito')).groupby('grupo', observed=True)['sm']
    cel_d = {g: f'{pct_br(s.mean(), 1)} ({int(s.sum())}/{len(s)})' for g, s in sm}
    linhas.append(['% dos distribuídos', 'Extinção sem mérito', cel_d['Controle'], cel_d['Presencial'], cel_d['Remota'],
                   'limite inferior (ativos no denominador)', '2.5'])
if tempo_tipo is not None:
    tm = tempo_tipo[tempo_tipo['Tipo'] == 'Sentença de mérito'].iloc[0]
    linhas.append(['Tempo condicional (sentenciados)', 'Mediana até a sentença de mérito (dias)',
                   fmt_br(tm['Mediana Controle (dias)'], 1), fmt_br(tm['Mediana Presencial (dias)'], 1), fmt_br(tm['Mediana Remota (dias)'], 1),
                   f'condicional; Kruskal-Wallis p Holm {fmt_p(tm["p Holm"])}', '3.4.5'])
if acordo_ac is not None:
    p_ac, _ = s8_holm('Fisher acordo na AC: Presencial × Remota')
    a = acordo_ac.set_index('Grupo')
    cel = lambda g: f'{pct_br(a.loc[g, "Acordo na AC"] / (a.loc[g, "Acordo na AC"] + a.loc[g, "Sem acordo"]), 1)} ' \
                    f'({int(a.loc[g, "Acordo na AC"])}/{int(a.loc[g, "Acordo na AC"] + a.loc[g, "Sem acordo"])})'
    linhas.append(['Acordo', 'Acordo na AC (% das AC realizadas)', 'não se aplica (sem AC)', cel('Presencial'), cel('Remota'),
                   f'Presencial × Remota: Fisher p = {fmt_p(p_ac)}', '3.3.1'])
if pares_120 is not None:
    p_r, ph_r = s8_holm('Fisher acordo até 120 d: Remota × Controle')
    sub = pares_120[pares_120['Horizonte (dias)'] == 120].set_index('Comparação')
    cel = lambda c: f'{sub.loc[c, "1º"]}; OR {fmt_br(sub.loc[c, "OR"], 2)} ({sub.loc[c, "OR IC"].replace(" a ", "–")})'
    linhas.append(['Acordo', 'Acordo em qualquer momento até 120 dias', str(sub.loc['Presencial × Controle', '2º']),
                   cel('Presencial × Controle'), cel('Remota × Controle'),
                   f'Remota × Controle: p = {fmt_p(p_r)}; p Holm global ({n_inf3} testes) = {fmt_p(ph_r)}', '3.3.2'])
if logit_a is not None:
    la = logit_a.set_index('Contraste')
    cel = lambda c: f'RC {fmt_br(la.loc[c, "RC"], 2)} ({fmt_br(la.loc[c, "IC 95% inf."], 2)}–{fmt_br(la.loc[c, "IC 95% sup."], 2)}); ' \
                    f'p Holm {fmt_p(la.loc[c, "p (Holm)"])}'
    linhas.append(['Acordo', 'Acordo entre os encerrados (logit ajustado pelo mês)', 'referência', cel('Presencial vs Controle'),
                   cel('Remota vs Controle'), 'Holm nos 3 contrastes do modelo; RR da Remota 1,98', '5.2.1'])
linhas = [[c.replace('p = <', 'p <') if isinstance(c, str) else c for c in l] for l in linhas]
resumo8 = pd.DataFrame(linhas, columns=['Dimensão', 'Estimativa', 'Controle (rito atual)', 'AC presencial', 'AC remota', 'Leitura', 'Seção'])
resumo8 = resumo8.set_index(['Dimensão', 'Estimativa'])
tabela(resumo8, 'sin_resumo', 'Síntese das estimativas: a AC obrigatória não acelera a sentença (na Remota, atrasa) e reduz o mérito; '
       'o excesso de extinção sem mérito e o de acordo são sugestivos', secao='8.1', indice=True,
       nota='IC 95% entre parênteses; HR, sHR e razão de tempos contra o Controle; OR = razão de chances; RC = razão de chances do logit. '
            'As linhas condicionais aos sentenciados e as dos distribuídos são limites opostos; as de horizonte fixo e as de riscos '
            'competitivos respeitam o seguimento.',
       fonte='Elaboração própria a partir das tabelas exportadas pelas Partes III a VI.')
''')

interp('sin_resumo')

md(r'''
## 8.2 Os efeitos num só gráfico

O gráfico de floresta resume, em escala logarítmica, os efeitos de cada braço com AC contra o Controle:

- **à esquerda, o tempo**: a razão de riscos do Cox, em que valores **abaixo** de 1 indicam sentença mais lenta, e a razão de tempos do Weibull, em que valores **acima** de 1 indicam processo mais longo;
- **à direita, o tipo de desfecho**: as razões de sub-riscos do Fine-Gray, que respeitam a censura e o risco competitivo, e a razão de chances do acordo até 120 dias, observado sem censura.

A linha vertical marca a ausência de efeito. Um intervalo que não a cruza é significativo a 5%, sem correção de multiplicidade.
''')

code(r'''
if sint_sob is not None and fg_boot is not None and pares_120 is not None:
    efeitos_t = []
    for chave, nome in [('HR Cox (b) (IC 95%)', 'HR de sentença (Cox)\n< 1: mais lento'),
                        ('Razão de tempos Weibull (IC 95%)', 'Razão de tempos (Weibull)\n> 1: mais lento')]:
        for g, col in zip(['Presencial', 'Remota'], col_s[1:]):
            est, lo, hi = s8_num(sint_sob.loc[chave, col])[:3]
            efeitos_t.append((nome, g, est, lo, hi))
    efeitos_o = []
    for desf, nome in [('Mérito', 'Sentença de mérito\n(sHR Fine-Gray)'), ('Sem mérito', 'Extinção sem mérito\n(sHR Fine-Gray)'),
                       ('Homologação', 'Homologação de acordo\n(sHR Fine-Gray)')]:
        for g, contr in [('Presencial', 'AC presencial × Controle'), ('Remota', 'AC remota × Controle')]:
            est, lo, hi, _ = s8_fg(desf, contr)
            efeitos_o.append((nome, g, est, lo, hi))
    sub120 = pares_120[pares_120['Horizonte (dias)'] == 120].set_index('Comparação')
    for g in ['Presencial', 'Remota']:
        lo, hi = s8_num(sub120.loc[f'{g} × Controle', 'OR IC'])
        efeitos_o.append(('Acordo até 120 dias\n(OR, sem censura)', g, sub120.loc[f'{g} × Controle', 'OR'], lo, hi))

    fig, axs = plt.subplots(1, 2, figsize=(14, 5.6), gridspec_kw={'width_ratios': [1, 1.25]})
    for ax, efeitos, titulo, xlab in [(axs[0], efeitos_t, 'Tempo até a sentença', 'HR ou razão de tempos (escala log)'),
                                      (axs[1], efeitos_o, 'Tipo de desfecho e acordo', 'sHR ou razão de chances (escala log)')]:
        nomes = list(dict.fromkeys(e[0] for e in efeitos))
        ypos = {}
        for i, nome in enumerate(nomes):
            for j, g in enumerate(['Presencial', 'Remota']):
                ypos[(nome, g)] = i * 1.0 + (j - 0.5) * 0.32
        for nome, g, est, lo, hi in efeitos:
            y = ypos[(nome, g)]
            ax.plot([lo, hi], [y, y], color=CORES_GRUPO[g], lw=2.2)
            ax.plot(est, y, 'o', color=CORES_GRUPO[g], ms=8, mec='white', mew=0.8)
            ax.text(1.02, y, f'{fmt_br(est, 2)} ({fmt_br(lo, 2)}–{fmt_br(hi, 2)})', transform=ax.get_yaxis_transform(),
                    va='center', ha='left', fontsize=8.5, color=CORES_GRUPO[g])
        ax.axvline(1, color=TINTA_2, lw=1, ls='--')
        ax.set_xscale('log')
        ax.set_yticks(range(len(nomes)), nomes)
        ax.set_xlabel(xlab)
        ax.set_title(titulo)
        lo_all = min(e[3] for e in efeitos); hi_all = max(e[4] for e in efeitos)
        ax.set_xlim(lo_all / 1.15, hi_all * 1.15)
        ax.set_ylim(len(nomes) - 0.45, -0.55)
        ax.xaxis.set_major_formatter(mpl.ticker.FuncFormatter(lambda v, p: fmt_br(v, 2 if v < 1 else 1)))
        ax.xaxis.set_minor_formatter(mpl.ticker.NullFormatter())
        ticks = [t for t in [0.25, 0.5, 0.75, 1, 1.5, 2, 3, 4, 6] if lo_all / 1.15 <= t <= hi_all * 1.15]
        ax.set_xticks(ticks)
        ax.grid(axis='y', visible=False)
    # legenda presa a um eixo (o figura() aplica tight_layout, que ignora fig.legend)
    axs[1].legend(handles=[mpl.lines.Line2D([], [], color=CORES_GRUPO[g], marker='o', lw=2.2, label=f'{ROTULO_GRUPO[g]} × Controle')
                           for g in ['Presencial', 'Remota']], loc='upper center', ncol=2, frameon=False,
                  bbox_to_anchor=(0.2, -0.17))
    figura(fig, 'sin_forest', 'Efeitos da AC obrigatória contra o rito atual: sentença mais lenta na Remota, menos mérito nos dois braços; '
           'sem mérito e acordo com intervalos que tocam 1',
           secao='8.2', nota='IC 95%; Cox ajustado por mês e origem (4.5.1); Weibull AFT (4.6); Fine-Gray com IC bootstrap (4.7.5); '
                             'acordo até 120 dias entre os processos com seguimento ≥ 120 dias (3.3.2). IC sem correção de multiplicidade.')
''')

interp('sin_forest')

md(r'''
## 8.3 Resposta à pergunta de pesquisa

**A audiência de conciliação obrigatória reduz o tempo de tramitação no 4º JEC em relação ao rito atual? Aumenta os acordos?**

**Não, nas duas perguntas.**

- **H1 (tempo).** Não se confirma em nenhum braço. Na Remota é **contrariada**: a sentença chega cerca de duas semanas mais tarde na mediana. Na Presencial, a estimativa vai na mesma direção, mas é compatível com ausência de efeito, o que não equivale a demonstrar ausência de efeito (8.4.3).
- **H2 (acordo).** A AC obrigatória não aumentou o acordo **na** audiência. O excedente da Remota, fora da audiência, é sugestivo.
- **H3 (modalidade).** Presencial e remota não diferem, mas a comparação está confundida com a conciliadora.
- **H4 e H5.** Não são testáveis neste desenho (7.3, 7.7).

**O mecanismo.** A AC obrigatória funcionou mais como **etapa adicional** do rito do que como espaço de autocomposição: menos julgamentos de mérito, e mais tardios (achado robusto), e possivelmente mais extinções tardias pelo art. 51, I, da Lei 9.099/1995 (achado sugestivo).

O resultado vale **para o 4º JEC**, uma unidade já atípica em Natal (6.6.2). A conclusão do resumo expandido ("não haver discrepância significativa") decorre de médias que ignoram a censura (7.10).
''')

md(r'''
## 8.4 Limitações e recomendações para a replicação

### 8.4.1 Limitações deste estudo

- **Unidade única, escolhida por conveniência e atípica** entre os 14 JECs (mais extinção sem mérito e menos mérito já em 2025): sem inferência estatística para os 14 (7.9, 6.6.2).
- **Aleatorização não verificável**: equilíbrio final improvável num sorteio simples (P ≈ 1%), compensação concentrada em julho e alocação sem ocultação, feita no gabinete do juiz-pesquisador (7.1). A estratificação por mês mitiga a associação período × grupo, mas não substitui a documentação.
- **Conciliadora confundida com a modalidade**: Presencial × Remota não separa a modalidade da pessoa (7.7).
- **Juiz-pesquisador não cego**: não verificável. Para a reatividade e a contaminação, a Parte VI dá só um teste indireto, sem sinal no Controle (6.6.3).
- **Seguimento curto e escalonado** (65 a 279 dias; 24,5% sem desfecho): por isso se usaram a mediana de Kaplan-Meier e o RMST até 180 dias. A extensão pelo DataJud até 06/11/2026 mantém a direção (6.4).
- **Ausência de covariáveis do processo, de datas intermediárias e do motivo da extinção**: impede verificar o equilíbrio, decompor o tempo e demonstrar o mecanismo do art. 51, I, que fica plausível, mas não demonstrado.
- **Riscos não proporcionais**: o efeito concentra-se entre 30 e 90 dias (análise por janelas, 4.5.2, embora o teste de Schoenfeld não acuse violação), de modo que um único HR o resume mal; o RMST e as curvas são a leitura preferível.
- **Comparação entre os 14 JECs incompleta**: só contagens agregadas, descritivas e sem teste de tendências paralelas, porque a API não permitiu coletar os tempos dos outros 13 (6.6.1).
- **Aspectos ético-jurídicos não documentados**: apreciação ética, consentimento e fundamentação legal do rito do Controle (7.11).

### 8.4.2 Recomendações

O quadro consolida as recomendações para uma replicação, cada uma ligada ao problema que resolve e ao tipo de validade que fortalece. O cálculo de poder que o segue dimensiona a replicação.
''')

code(r'''
quadro_rec = pd.DataFrame([
    ['Hipóteses e análise definidas depois dos dados', 'pré-registro do protocolo (desfecho primário, secundários, plano de análise ITT, regras de exclusão)',
     'registro público antes do 1º sorteio; relato CONSORT', 'interna; credibilidade'],
    ['Desfecho primário ambíguo; médias com censura', 'desfecho primário = tempo até a sentença, com censura; estimandos: mediana de KM, RMST(τ), HR',
     'τ e data de corte fixados no protocolo', 'interna; estatística'],
    ['Poder não calculado', 'cálculo de poder para o desfecho primário', 'eventos necessários pela fórmula de Schoenfeld (8.4.3)', 'estatística'],
    ['Sorteio sem documentação nem ocultação', 'lista de aleatorização em blocos permutados, estratificada por mês, gerada e guardada por terceiro',
     'semente registrada; alocação revelada só depois da inclusão (central externa ao juízo)', 'interna'],
    ['Reentradas re-sorteadas; prevenção sorteada', 'regras de elegibilidade e de reentrada', 'triagem de prevenção antes do sorteio; reentrada herda o grupo', 'interna'],
    ['Conciliadora confundida com a modalidade', 'rodízio das conciliadoras entre modalidades (ou várias por braço)',
     'escala de rodízio sorteada por semana', 'interna; constructo'],
    ['Juiz-pesquisador não cego', 'cegamento da extração e da análise', 'desfecho extraído do PJe/DataJud por terceiro; análise com grupos codificados', 'interna'],
    ['Sem covariáveis nem datas intermediárias', 'coleta das covariáveis basais e das datas de citação, AC, contestação e conclusão',
     'extração automática do PJe/DataJud pelo número CNJ', 'interna; precisão'],
    ['Motivo da extinção e comparecimento não registrados', 'registrar comparecimento de cada parte, formato real da AC e motivo da extinção',
     'campos fechados na planilha (lista de validação)', 'constructo; mecanismo'],
    ['Seguimento curto e escalonado', 'seguimento mínimo comum para todos', 'por exemplo, 180 dias após o último sorteio', 'estatística'],
    ['Mês como confundidor de calendário', 'estratificação por mês no sorteio e na análise', 'blocos por mês; Cox estratificado', 'interna'],
    ['Unidade única e atípica (N = 1)', 'ensaio multicêntrico por conglomerados ou escalonado (stepped-wedge) entre JECs',
     'adesão das unidades via TJRN/NUPEMEC; sorteio das unidades e do momento de entrada', 'externa'],
    ['Efeito do experimento sobre a unidade só descrito', 'diferenças em diferenças com tempos e horizonte fixo entre os 14 JECs',
     'concluir a coleta do DataJud (código retomável, 6.6.1); testar tendências paralelas', 'interna (reatividade); externa'],
    ['Apreciação ética e base legal não documentadas', 'submissão ao sistema CEP/Conep (Res. CNS 510/2016); consentimento ou dispensa justificada',
     'fundamentar a licitude de cada rito (Lei 9.099/1995, arts. 16, 21 e 22); autorização do tribunal', 'legitimidade; constructo'],
], columns=['Problema encontrado', 'Recomendação', 'Como implementar', 'Validade fortalecida'])
tabela(quadro_rec, 'sin_recomendacoes', 'Recomendações para a replicação do experimento', secao='8.4',
       fonte='Elaboração própria a partir das Partes I a VII.')
''')

md(r'''
### 8.4.3 Cálculo de poder: quantos eventos uma replicação precisa?

**Fórmulas.**

- **Tempo (Cox, dois braços 1:1).** O número de **eventos** (sentenças) necessário para detectar uma razão de riscos HR, com nível α bilateral e poder 1 − β, é dado pela fórmula de Schoenfeld (1983): d = 4(z₁₋α/₂ + z₁₋β)² / (ln HR)². Inversamente, com d eventos, o poder para um HR **verdadeiro** é Φ(√(d/4)·|ln HR| − z₁₋α/₂).
- **Acordo na AC (duas proporções).** Usa-se a transformação arco-seno, h = 2·arcsen√p₂ − 2·arcsen√p₁, com n = 2[(z₁₋α/₂ + z₁₋β)/h]² processos com AC realizada por braço.

**Parâmetros.** α = 5% e poder de 80%. Com a correção de Holm para duas comparações contra o Controle, o α efetivo da primeira comparação cai para 2,5%, o que aumenta as exigências em cerca de 20%.

**Valores de planejamento.** Os efeitos a detectar são fixados antes de olhar os dados, e não iguais às estimativas obtidas. O "poder observado", calculado com o efeito estimado, é só uma transformação do valor-p e nada acrescenta à sua interpretação.
''')

code(r'''
eventos_nec = lambda hr, a=0.05, pw=0.80: 4 * (norm.ppf(1 - a / 2) + norm.ppf(pw)) ** 2 / np.log(hr) ** 2
poder_cox = lambda d, hr, a=0.05: norm.cdf(np.sqrt(d / 4) * abs(np.log(hr)) - norm.ppf(1 - a / 2))
h_arc = lambda p1, p2: abs(2 * np.arcsin(np.sqrt(p2)) - 2 * np.arcsin(np.sqrt(p1)))
n_prop = lambda p1, p2, a=0.05, pw=0.80: 2 * ((norm.ppf(1 - a / 2) + norm.ppf(pw)) / h_arc(p1, p2)) ** 2
poder_prop = lambda n, p1, p2, a=0.05: norm.cdf(np.sqrt(n / 2) * h_arc(p1, p2) - norm.ppf(1 - a / 2))

ev = dados.groupby('grupo', observed=True)['evento'].apply(lambda s: int(s.astype(int).sum())).reindex(ORDEM_GRUPO)
d_pc, d_rc = int(ev['Controle'] + ev['Presencial']), int(ev['Controle'] + ev['Remota'])
acr = dados[dados['ac_realizada'].fillna(False).astype(bool)]
n_ac = acr.groupby('grupo', observed=True).size().reindex(['Presencial', 'Remota'])
k_ac = acr.groupby('grupo', observed=True)['acordo_ac'].apply(lambda s: int(s.fillna(False).astype(bool).sum())).reindex(['Presencial', 'Remota'])
p_base = k_ac.sum() / n_ac.sum()

linhas_p = []
for hr in [0.90, 0.85, 0.80, 0.75]:
    linhas_p.append(['Tempo até a sentença (Cox, 1:1)', f'HR = {fmt_br(hr, 2)}', eventos_nec(hr), eventos_nec(hr, a=0.025),
                     d_rc, poder_cox(d_rc, hr)])
n_disp = int(n_ac.min())
for p2 in [0.10, 0.15, 0.20]:
    linhas_p.append(['Acordo na AC (proporções)', f'{pct_br(p_base, 1)} → {pct_br(p2, 0)}', n_prop(p_base, p2), n_prop(p_base, p2, a=0.025),
                     n_disp, poder_prop(n_disp, p_base, p2)])
poder_df = pd.DataFrame(linhas_p, columns=['Desfecho', 'Efeito a detectar (planejamento)', 'Necessário (α = 5%)',
                                           'Necessário (α = 2,5%, Holm)', 'Disponível no estudo', 'Poder do estudo para esse efeito'])
tabela(poder_df, 'sin_poder', 'Poder do experimento para efeitos de planejamento: cerca de 70% para HR = 0,80; no acordo na AC, '
       'só diferenças grandes eram detectáveis',
       secao='8.4.3', formatos={'Necessário (α = 5%)': 0, 'Necessário (α = 2,5%, Holm)': 0, 'Disponível no estudo': 'int',
                                 'Poder do estudo para esse efeito': 'pct'},
       nota=f'tempo: sentenças nos braços Controle + Remota ({d_rc}; Controle + Presencial = {d_pc}); acordo: AC realizadas no menor '
            f'braço ({n_disp}); taxa-base de acordo na AC = {pct_br(p_base, 1)} ({int(k_ac.sum())}/{int(n_ac.sum())}). Poder com α = 5%.',
       fonte='Elaboração própria; fórmula de Schoenfeld (1983) e aproximação arco-seno para proporções.')

fig, axs = plt.subplots(1, 2, figsize=(13, 5.2))
hrs = np.linspace(0.72, 0.93, 200)
ax = axs[0]
ax.plot(hrs, eventos_nec(hrs), color=TINTA_2, lw=2, label='α = 5%')
ax.plot(hrs, eventos_nec(hrs, a=0.025), color=TINTA_2, lw=1.4, ls='--', label='α = 2,5% (Holm)')
ax.axhline(d_rc, color=DESTAQUE, lw=1.2)
ax.annotate(f'sentenças disponíveis (Controle + Remota) = {d_rc}', (0.928, d_rc), xytext=(0, -14), textcoords='offset points',
            fontsize=8.5, color=DESTAQUE, ha='right')
for hr in [0.85, 0.80]:
    ax.plot(hr, eventos_nec(hr), 'o', color=TINTA, ms=6)
    ax.annotate(f'HR {fmt_br(hr, 2)}: {fmt_int(round(eventos_nec(hr)))} sentenças\n(poder do estudo {pct_br(poder_cox(d_rc, hr), 0)})',
                (hr, eventos_nec(hr)), xytext=(-10, 12), textcoords='offset points', fontsize=8.5, color=TINTA, ha='right')
ax.set_ylim(0, 5000)
ax.set_xlabel('Razão de riscos a detectar (HR, valor de planejamento)'); ax.set_ylabel('Sentenças necessárias (poder 80%)')
ax.set_title('Tempo até a sentença (Cox, dois braços 1:1)')
ax.legend(loc='upper left', fontsize=8.5)
ax = axs[1]
p2s = np.linspace(0.07, 0.22, 200)
ax.plot(p2s * 100, n_prop(p_base, p2s), color=TINTA_2, lw=2, label='α = 5%')
ax.plot(p2s * 100, n_prop(p_base, p2s, a=0.025), color=TINTA_2, lw=1.4, ls='--', label='α = 2,5% (Holm)')
ax.axhline(n_disp, color=DESTAQUE, lw=1.2)
ax.annotate(f'AC realizadas no menor braço = {n_disp}', (21.8, n_disp), xytext=(0, 5), textcoords='offset points',
            fontsize=8.5, color=DESTAQUE, ha='right')
ax.set_ylim(0, 1500)
ax.set_xlabel(f'Taxa de acordo na AC a detectar no outro braço (%; base {pct_br(p_base, 1)})')
ax.set_ylabel('AC realizadas necessárias por braço (poder 80%)')
ax.set_title('Acordo na AC (duas proporções)')
ax.legend(loc='upper right', fontsize=8.5)
figura(fig, 'sin_poder', 'Quantos processos uma replicação precisaria: HR de 0,85 exige mais de mil sentenças por par de braços',
       secao='8.4.3', nota='fórmula de Schoenfeld (1983) para o Cox; transformação arco-seno para proporções; poder de 80%; '
                         'efeitos fixados como valores de planejamento, e não iguais às estimativas.')
''')

interp('sin_poder')

md(r'''
## 8.5 Considerações finais

O sorteio permitiu responder a uma pergunta causal que estudos observacionais sobre a conciliação raramente alcançam, e a resposta não é a que os autores anunciaram. A AC obrigatória não acelerou os processos (na Remota, atrasou-os), não aumentou a conciliação na audiência e tornou os julgamentos de mérito mais raros e mais tardios.

A divergência não vem dos dados, que uma fonte independente confirmou, e sim da **análise**: médias de processos ainda em curso, sem censura, sem teste e sem intervalo. Os mesmos registros, tratados com curadoria explícita, análise de sobrevivência, riscos competitivos e controle de multiplicidade, mudam a conclusão sobre uma política judiciária. Separam também o que é robusto (o déficit de mérito, o atraso da Remota) do que é apenas sugestivo (o excesso de extinções sem mérito, o acordo fora da audiência).

Uma replicação deve manter o sorteio individual, o controle contemporâneo e o registro diário, e acrescentar o que faltou: protocolo pré-registrado e apreciado por comitê de ética, aleatorização documentada e ocultada, rodízio das conciliadoras, cegamento, covariáveis, motivo da extinção e, sobretudo, várias unidades.
''')
