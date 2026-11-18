# Parte VII — Síntese, conclusões, limitações, recomendações e referências (seções 7.1 a 7.6).
# Executado por build_rafaelcc_ed2.py (exec): usa md(), code() e interp().
# Lê as estimativas exportadas pelas Partes III a V (dat/processado e tab/); não refaz análises.

md(r'''
# PARTE VII — SÍNTESE E CONCLUSÕES

Esta parte reúne os achados do notebook numa síntese executiva (7.1), com uma tabela-resumo das estimativas e dos intervalos de confiança e um gráfico dos efeitos (7.2); responde à pergunta de pesquisa (7.3); consolida as limitações e as recomendações para uma replicação, com um cálculo de poder (7.4); e lista as referências (7.6). Os números vêm das tabelas exportadas pelas Partes III a V; a seção de cada estimativa está indicada.
''')

md(r'''
## 7.1 Síntese executiva

1. **Os números divulgados não medem a duração.** As médias de 78,46 dias (planilha) e de 75,2 dias (resumo expandido) misturam 708 sentenças com os tempos parciais de 206 processos ainda em tramitação e contam 24 redistribuições como desfecho; foram reconstituídas exatamente e nenhuma estima uma quantidade interpretável (seção 2.1.2). A duração mediana correta, pelo Kaplan-Meier, é de 89 dias para o conjunto (seção 4.2).
2. **A AC obrigatória alongou o tempo até a sentença.** Medianas de Kaplan-Meier de 81 dias no Controle, 96 na AC presencial e 95 na AC remota; log-rank p = 0,023. Ajustado pelo mês e pela origem, o Cox estima HR de 0,87 (0,72–1,04) para a Presencial e de 0,81 (0,67–0,97) para a Remota (sentença **mais lenta**); o tempo médio restrito a 180 dias é 10,7 dias maior na Remota (IC 1,9–19,5). A diferença concentra-se entre 30 e 90 dias, o intervalo em que a AC ocorre (seções 4.3 a 4.6).
3. **O mecanismo é a troca do tipo de desfecho.** Entre os sentenciados, a extinção sem mérito passa de 30,2% no Controle para 47,4% na Presencial e 45,4% na Remota (OR 2,09 e 1,92), e a sentença de mérito cai de 61,8% para 41,7% e 38,4%; as sentenças de mérito, quando ocorrem, chegam mais tarde (medianas condicionais de 83, 112,5 e 106 dias). O padrão é compatível com a extinção por ausência do autor à audiência obrigatória (art. 51, I, da Lei 9.099/1995), mas a planilha não registra o motivo da extinção (seções 3.2, 4.7).
4. **A audiência não aumentou o acordo na audiência.** O acordo na AC foi de 5,1% na Presencial e de 4,6% na Remota (Fisher p = 1,000), muito abaixo do índice histórico de 13,3% da unidade. O acordo em qualquer momento é maior na Remota que no Controle (OR ≈ 2,2 entre os encerrados; 2,7 até 120 dias), mas esse contraste não sobrevive à correção de Holm sobre a família completa de testes da Parte III, e a maior parte dos acordos da Remota ocorreu **fora** da audiência (seções 3.3, 5.2).
5. **Modalidade, técnica e híbrida não fizeram diferença detectável.** Presencial × Remota não difere no tempo (log-rank par a par p = 0,519) nem no acordo; as seis técnicas foram sorteadas de modo compatível com o uniforme (p = 0,566; os "53,85%" do resumo não se reproduzem) e não diferem no tempo; a AC híbrida não difere da presencial pura (seções 2.5.3, 3.3.4, 4.8).
6. **O desenho é um ECA válido internamente, mas de unidade única.** O sorteio passou nos testes possíveis (corridas, equilíbrio por mês), com indício de restrição não documentada; a conciliadora está confundida com a modalidade, o juiz-pesquisador não é cego e não há covariáveis do processo. A generalização aos 14 JECs não tem base estatística (seções 6.1 a 6.9).
''')

code(r'''
if 'dados' not in globals():
    dados = pd.read_pickle(PROC / 'ed2_tidy.pkl')
import re
from scipy.stats import norm


def s7_csv(nome, pasta='tab', **kw):
    caminho = RAIZ / pasta / nome
    if not caminho.exists():
        print(f'Aviso: {pasta}/{nome} não encontrado (é gerado pelas Partes III a V).')
        return None
    opcoes = dict(sep=';', decimal=',', encoding='utf-8-sig')
    opcoes.update(kw)
    return pd.read_csv(caminho, **opcoes)


def s7_num(texto):
    """'0,87 (0,72–1,04)' → [0.87, 0.72, 1.04]."""
    return [float(x.replace(',', '.')) for x in re.findall(r'-?\d+(?:,\d+)?', str(texto))]


sint_sob = s7_csv('ed2_sintese_sobrevivencia.csv', pasta='dat/processado', index_col=0, decimal='.')
reg3 = s7_csv('ed2_parte3_testes.csv', pasta='dat/processado')
pares_tipo = s7_csv('tst_tipobin_pares.csv')
pares_120 = s7_csv('tst_acordo_horizonte_pares.csv')
tempo_tipo = s7_csv('tst_tempo_por_tipo.csv')
acordo_ac = s7_csv('tst_acordo_ac.csv')
logit_a = s7_csv('mul_logit_A_contrastes.csv')


def s7_holm(trecho):
    """p bruto e p Holm global do registro de testes da Parte III (pelo nome do teste)."""
    if reg3 is None:
        return np.nan, np.nan
    lin = reg3[reg3['Teste'].str.contains(trecho, regex=False)]
    return (float(lin['p'].iloc[0]), float(lin['p Holm global'].iloc[0])) if len(lin) else (np.nan, np.nan)


def s7_par(tipo, comp):
    lin = pares_tipo[(pares_tipo['Tipo'] == tipo) & (pares_tipo['Comparação'] == comp)].iloc[0]
    return lin


def s7_pct_xn(xn):
    x, n = (int(v) for v in str(xn).split('/'))
    return f'{pct_br(x / n, 1)} ({x}/{n})'

col_s = list(sint_sob.columns) if sint_sob is not None else []
linhas = []
if sint_sob is not None:
    for rot, chave, leitura, sec in [
        ('Tempo até a sentença', 'Mediana KM, dias (IC 95%)', 'maior = mais lento', '4.2.3'),
        ('Tempo até a sentença', 'RMST 180 d, dias (IC 95%)', 'dias sem sentença nos primeiros 180 d', '4.3.6'),
        ('Tempo até a sentença', 'ΔRMST 180 d vs. Controle (IC bootstrap)', '> 0 = mais lento que o Controle', '4.3.6'),
        ('Tempo até a sentença', 'HR Cox (b) (IC 95%)', '< 1 = sentença mais lenta; ajustado por mês e origem', '4.5.1'),
        ('Tempo até a sentença', 'Razão de tempos Weibull (IC 95%)', '> 1 = mais lento', '4.6'),
        ('Incidência acumulada aos 90 dias', 'FIA 90 d: Mérito', 'riscos competitivos (Aalen-Johansen)', '4.7.2'),
        ('Incidência acumulada aos 90 dias', 'FIA 90 d: Sem mérito', 'riscos competitivos (Aalen-Johansen)', '4.7.2'),
        ('Incidência acumulada aos 90 dias', 'FIA 90 d: Homologação', 'riscos competitivos (Aalen-Johansen)', '4.7.2'),
    ]:
        v = sint_sob.loc[chave]
        linhas.append([rot, chave.replace(' (IC 95%)', '').replace(' (IC bootstrap)', ''), v.iloc[0], v.iloc[1], v.iloc[2], leitura, sec])
if pares_tipo is not None:
    for tipo, rot in [('Sentença de mérito', 'Sentença de mérito'), ('Extinção sem mérito', 'Extinção sem mérito'),
                      ('Homologação de acordo', 'Homologação de acordo')]:
        lp, lr_ = s7_par(tipo, 'Presencial × Controle'), s7_par(tipo, 'Remota × Controle')
        celula = lambda l: (f'{s7_pct_xn(l["x/n (1º)"])}; OR {fmt_br(l["OR"], 2)} ({fmt_br(l["OR IC inf"], 2)}–'
                            f'{fmt_br(l["OR IC sup"], 2)}); p Holm {fmt_p(l["p Holm"])}')
        linhas.append(['Tipo de sentença (% dos sentenciados)', rot, s7_pct_xn(lp['x/n (2º)']), celula(lp), celula(lr_),
                       'OR contra o Controle; Fisher, Holm em 9 pares', '3.2.3'])
if tempo_tipo is not None:
    tm = tempo_tipo[tempo_tipo['Tipo'] == 'Sentença de mérito'].iloc[0]
    linhas.append(['Tempo condicional (sentenciados)', 'Mediana até a sentença de mérito (dias)',
                   fmt_br(tm['Mediana Controle (dias)'], 1), fmt_br(tm['Mediana Presencial (dias)'], 1), fmt_br(tm['Mediana Remota (dias)'], 1),
                   f'condicional; Kruskal-Wallis p Holm {fmt_p(tm["p Holm"])}', '3.4.5'])
if acordo_ac is not None:
    p_ac, ph_ac = s7_holm('Fisher acordo na AC: Presencial × Remota')
    a = acordo_ac.set_index('Grupo')
    cel = lambda g: f'{pct_br(a.loc[g, "Acordo na AC"] / (a.loc[g, "Acordo na AC"] + a.loc[g, "Sem acordo"]), 1)} ' \
                    f'({int(a.loc[g, "Acordo na AC"])}/{int(a.loc[g, "Acordo na AC"] + a.loc[g, "Sem acordo"])})'
    linhas.append(['Acordo', 'Acordo na AC (% das AC realizadas)', 'não se aplica (sem AC)', cel('Presencial'), cel('Remota'),
                   f'Presencial × Remota: Fisher p = {fmt_p(p_ac)}', '3.3.1'])
if pares_120 is not None:
    p_r, ph_r = s7_holm('Fisher acordo até 120 d: Remota × Controle')
    sub = pares_120[pares_120['Horizonte (dias)'] == 120].set_index('Comparação')
    cel = lambda c: f'{sub.loc[c, "1º"]}; OR {fmt_br(sub.loc[c, "OR"], 2)} ({sub.loc[c, "OR IC"].replace(" a ", "–")})'
    linhas.append(['Acordo', 'Acordo em qualquer momento até 120 dias', str(sub.loc['Presencial × Controle', '2º']),
                   cel('Presencial × Controle'), cel('Remota × Controle'),
                   f'Remota × Controle: p = {fmt_p(p_r)}; p Holm global (55 testes) = {fmt_p(ph_r)}', '3.3.2'])
if logit_a is not None:
    la = logit_a.set_index('Contraste')
    cel = lambda c: f'RC {fmt_br(la.loc[c, "RC"], 2)} ({fmt_br(la.loc[c, "IC 95% inf."], 2)}–{fmt_br(la.loc[c, "IC 95% sup."], 2)}); ' \
                    f'p Holm {fmt_p(la.loc[c, "p (Holm)"])}'
    linhas.append(['Acordo', 'Acordo entre os encerrados (logit ajustado pelo mês)', 'referência', cel('Presencial vs Controle'),
                   cel('Remota vs Controle'), 'Holm nos 3 contrastes do modelo', '5.2.1'])
resumo7 = pd.DataFrame(linhas, columns=['Dimensão', 'Estimativa', 'Controle (rito atual)', 'AC presencial', 'AC remota', 'Leitura', 'Seção'])
resumo7 = resumo7.set_index(['Dimensão', 'Estimativa'])
tabela(resumo7, 'sin_resumo', 'Síntese das estimativas: a AC obrigatória atrasa a sentença e troca mérito por extinção sem mérito, '
       'sem aumentar o acordo na audiência', secao='7.1', indice=True,
       nota='IC 95% entre parênteses; HR e razão de tempos contra o Controle; OR = razão de chances contra o Controle; '
            'FIA = função de incidência acumulada.', fonte='Elaboração própria a partir das tabelas exportadas pelas Partes III a V.')
''')

interp('sin_resumo')

md(r'''
## 7.2 Os efeitos num só gráfico

O gráfico de floresta resume, em escala logarítmica, os efeitos de cada braço com AC contra o Controle: à esquerda, os dois modelos de tempo (a razão de riscos do Cox, em que valores **abaixo** de 1 indicam sentença mais lenta, e a razão de tempos do Weibull, em que valores **acima** de 1 indicam processo mais longo); à direita, as razões de chances dos tipos de sentença e do acordo. A linha vertical marca a ausência de efeito; um intervalo que não a cruza é significativo a 5% antes da correção de multiplicidade.
''')

code(r'''
if sint_sob is not None and pares_tipo is not None and pares_120 is not None:
    efeitos_t = []
    for chave, nome in [('HR Cox (b) (IC 95%)', 'HR de sentença (Cox)\n< 1: mais lento'),
                        ('Razão de tempos Weibull (IC 95%)', 'Razão de tempos (Weibull)\n> 1: mais lento')]:
        for g, col in zip(['Presencial', 'Remota'], col_s[1:]):
            est, lo, hi = s7_num(sint_sob.loc[chave, col])[:3]
            efeitos_t.append((nome, g, est, lo, hi))
    efeitos_o = []
    for tipo, nome in [('Sentença de mérito', 'Sentença de mérito'), ('Extinção sem mérito', 'Extinção sem mérito'),
                       ('Homologação de acordo', 'Homologação de acordo')]:
        for g in ['Presencial', 'Remota']:
            l = s7_par(tipo, f'{g} × Controle')
            efeitos_o.append((nome, g, l['OR'], l['OR IC inf'], l['OR IC sup']))
    sub120 = pares_120[pares_120['Horizonte (dias)'] == 120].set_index('Comparação')
    for g in ['Presencial', 'Remota']:
        lo, hi = s7_num(sub120.loc[f'{g} × Controle', 'OR IC'])
        efeitos_o.append(('Acordo até 120 dias', g, sub120.loc[f'{g} × Controle', 'OR'], lo, hi))

    fig, axs = plt.subplots(1, 2, figsize=(14, 5.4), gridspec_kw={'width_ratios': [1, 1.25], 'wspace': 0.75})
    for ax, efeitos, titulo, xlab in [(axs[0], efeitos_t, 'Tempo até a sentença', 'HR ou razão de tempos (escala log)'),
                                      (axs[1], efeitos_o, 'Tipo de desfecho e acordo (sentenciados)', 'Razão de chances (escala log)')]:
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
    fig.legend(handles=[mpl.lines.Line2D([], [], color=CORES_GRUPO[g], marker='o', lw=2.2, label=f'{ROTULO_GRUPO[g]} × Controle')
                        for g in ['Presencial', 'Remota']], loc='lower center', ncol=2, frameon=False, bbox_to_anchor=(0.5, -0.04))
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    figura(fig, 'sin_forest', 'Efeitos da AC obrigatória contra o rito atual: sentença mais lenta, menos mérito, mais extinção sem mérito',
           secao='7.2', nota='IC 95%; Cox ajustado por mês e origem (4.5.1); Weibull AFT (4.6); OR com IC exato condicional '
                             '(3.2.3) e acordo até 120 dias entre os processos com seguimento ≥ 120 dias (3.3.2). IC sem correção de multiplicidade.')
''')

interp('sin_forest')

md(r'''
## 7.3 Resposta à pergunta de pesquisa

**A audiência de conciliação obrigatória, presencial ou remota, reduz o tempo de tramitação no 4º JEC de Natal em relação ao rito atual? Aumenta os acordos?**

**Não, nas duas perguntas.** Com os dados até 07/10/2026 e uma análise que respeita a censura, a AC obrigatória **aumentou** o tempo até a sentença em cerca de duas semanas na mediana (81 dias no rito atual contra 95 e 96 dias nos braços com AC), com evidência mais forte para a modalidade remota (HR ajustado 0,81; IC 0,67–0,97; ΔRMST de 10,7 dias em 180). A hipótese H1 do projeto ("a audiência obrigatória reduz o tempo médio de tramitação") é, portanto, **contrariada** pelos dados, e não apenas não confirmada. A conclusão do resumo expandido, de que não haveria "discrepância significativa" entre os ritos, decorre de médias que ignoram a censura e não resiste à análise correta (6.10).

Quanto ao acordo (H2), a AC obrigatória **não aumentou o acordo na audiência**, que ficou em torno de 5% das audiências realizadas em ambas as modalidades, e o excesso de acordos da Remota em relação ao Controle é **sugestivo, mas não robusto** à correção de multiplicidade e ocorre sobretudo fora da audiência. Quanto à modalidade (H3), presencial e remota **não diferem** em tempo nem em acordo, mas a comparação está confundida com a conciliadora. As hipóteses H4 (híbrida) e H5 (CEJUSC × vara) **não são testáveis** neste desenho (6.3, 6.7).

O achado juridicamente mais relevante é o **mecanismo**: a AC obrigatória funcionou menos como espaço de autocomposição e mais como **ocasião de extinção sem mérito** (de 30% para cerca de 46% das sentenças), compatível com o art. 51, I, da Lei 9.099/1995, enquanto as sentenças de mérito chegaram mais tarde. Do ponto de vista da política judiciária, o resultado sugere que, nesta unidade e neste período, a obrigatoriedade da AC acrescentou uma etapa ao rito sem produzir o ganho de conciliação que a justificaria. Esse resultado vale **para o 4º JEC**; a sua extensão aos demais JECs depende da comparação observacional da Parte VIII e, para a validade externa propriamente dita, de replicação.

**Confirmação pelo DataJud (Parte VIII).** A conferência processo a processo com a API pública do CNJ vinculou 926 dos 938 processos e reproduziu a planilha com alta fidedignidade (tipo de desfecho: κ = 0,971; datas de sentença iguais em cerca de 98%); as sentenças em fim de semana são reais. Estendendo o seguimento até 06/11/2026, 81 dos 206 processos censurados foram sentenciados, e os efeitos **aumentaram**: HR da AC remota de 0,81 para 0,76 (IC 95% 0,64–0,90; p = 0,002) e ΔRMST180 de 10,7 para 14,0 dias (IC 5,0–22,1). A análise principal era, portanto, conservadora. O grupo Controle de 2026 se comportou como o 4º JEC de 2025 (RMST180 80,4 × 79,7 dias), o que não indica mudança da unidade por efeito do próprio experimento; e a média "anterior" de 106,8 dias citada no projeto não se reproduz no DataJud (93,0 dias para os sentenciados nos 12 meses anteriores). A comparação com os outros 13 JECs de Natal ficou parcial por indisponibilidade da API.
''')

md(r'''
## 7.4 Limitações e recomendações para a replicação

### 7.4.1 Limitações deste estudo

- **Unidade única e escolhida por conveniência**: sem inferência estatística para os 14 JECs (6.9).
- **Conciliadora confundida com a modalidade**: Presencial × Remota não separa a modalidade da pessoa (6.7).
- **Juiz-pesquisador não cego e reatividade da equipe**: não verificáveis com a planilha.
- **Seguimento curto e escalonado** (65 a 279 dias; 24,5% sem desfecho): a cauda da distribuição não é estimável; por isso se usaram a mediana de Kaplan-Meier e o RMST até 180 dias.
- **Ausência de covariáveis do processo** e de datas intermediárias: impede verificar o equilíbrio, decompor o tempo e explicar o mecanismo (Parte V).
- **Motivo da extinção sem mérito não registrado**: a leitura pelo art. 51, I, é plausível, mas não demonstrada.
- **Data da sentença possivelmente de lançamento** (18,4% em fins de semana): sem efeito nas conclusões (4.9), mas a validar no DataJud.
- **Riscos não proporcionais**: o efeito do rito concentra-se entre 30 e 90 dias (4.5.2), de modo que um único HR resume mal o efeito; o RMST e as curvas são a leitura preferível.
- **Mecanismo do sorteio não documentado**: o equilíbrio final é improvável num sorteio simples (P ≈ 1%), o que indica restrição; a análise estratificada por mês mitiga, mas não substitui a documentação.

### 7.4.2 Recomendações

O quadro consolida as recomendações para uma replicação, cada uma ligada ao problema que resolve e ao tipo de validade que fortalece. O cálculo de poder que o segue mostra que o próprio experimento, com o efeito observado, tinha poder modesto.
''')

code(r'''
quadro_rec = pd.DataFrame([
    ['Hipóteses e análise definidas depois dos dados', 'pré-registro do protocolo (desfecho primário, secundários, plano de análise ITT, regras de exclusão)',
     'registro público antes do 1º sorteio; relato CONSORT', 'interna; credibilidade'],
    ['Desfecho primário ambíguo; médias com censura', 'desfecho primário = tempo até a sentença, com censura; estimandos: mediana de KM, RMST(τ), HR',
     'τ e data de corte fixados no protocolo', 'interna; estatística'],
    ['Poder não calculado', 'cálculo de poder para o desfecho primário', 'eventos necessários pela fórmula de Schoenfeld (7.4.3)', 'estatística'],
    ['Sorteio sem documentação; equilíbrio improvável', 'lista de aleatorização em blocos permutados, estratificada por mês, gerada por terceiro',
     'semente registrada; ocultação (central externa ao juízo)', 'interna'],
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
    ['Unidade única (N = 1)', 'ensaio multicêntrico por conglomerados ou escalonado (stepped-wedge) entre JECs',
     'adesão das unidades via TJRN/NUPEMEC; sorteio das unidades e do momento de entrada', 'externa'],
    ['Efeito do experimento sobre a unidade desconhecido', 'comparação com o período anterior e com os outros JECs',
     'diferenças em diferenças com o DataJud (Parte VIII)', 'interna (reatividade); externa'],
], columns=['Problema encontrado', 'Recomendação', 'Como implementar', 'Validade fortalecida'])
tabela(quadro_rec, 'sin_recomendacoes', 'Recomendações para a replicação do experimento', secao='7.4',
       fonte='Elaboração própria a partir das Partes I a VI.')
''')

md(r'''
### 7.4.3 Cálculo de poder: quantos eventos seriam necessários?

Para comparar dois braços 1:1 com um modelo de riscos proporcionais, o número de **eventos** (sentenças) necessário para detectar uma razão de riscos HR, com nível α bilateral e poder 1 − β, é dado pela fórmula de Schoenfeld (1983): d = 4(z₁₋α/₂ + z₁₋β)² / (ln HR)². Inversamente, com d eventos, o poder para um HR verdadeiro é Φ(√(d/4)·|ln HR| − z₁₋α/₂). Para o acordo na AC, uma proporção baixa (cerca de 5%), o tamanho por grupo para detectar a diferença entre p₁ e p₂ usa a transformação arco-seno, h = 2·arcsen√p₂ − 2·arcsen√p₁, com n = 2[(z₁₋α/₂ + z₁₋β)/h]² processos com AC realizada por braço. Os cálculos usam α = 5% e poder de 80%; com a correção de Holm para duas comparações contra o Controle, o α efetivo da primeira comparação cai para 2,5%, o que aumenta as exigências em cerca de 20%.
''')

code(r'''
za, zb = norm.ppf(0.975), norm.ppf(0.80)
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
hr_obs = {}
if sint_sob is not None:
    for g, col in zip(['Presencial', 'Remota'], col_s[1:]):
        hr_obs[g] = s7_num(sint_sob.loc['HR Cox (b) (IC 95%)', col])[0]

linhas_p = []
for hr in [0.90, 0.85, 0.80, 0.75]:
    linhas_p.append(['Tempo até a sentença (Cox, 1:1)', f'HR = {fmt_br(hr, 2)}', eventos_nec(hr), eventos_nec(hr, a=0.025),
                     d_rc, poder_cox(d_rc, hr)])
for g, d in [('Presencial', d_pc), ('Remota', d_rc)]:
    if g in hr_obs:
        linhas_p.append(['Tempo até a sentença (Cox, 1:1)', f'HR observado {g} = {fmt_br(hr_obs[g], 2)}', eventos_nec(hr_obs[g]),
                         eventos_nec(hr_obs[g], a=0.025), d, poder_cox(d, hr_obs[g])])
n_disp = int(n_ac.min())
for p2 in [0.10, 0.133, 0.20]:
    linhas_p.append(['Acordo na AC (proporções)', f'{pct_br(p_base, 1)} → {pct_br(p2, 1)}', n_prop(p_base, p2), n_prop(p_base, p2, a=0.025),
                     n_disp, poder_prop(n_disp, p_base, p2)])
poder_df = pd.DataFrame(linhas_p, columns=['Desfecho', 'Efeito a detectar', 'Necessário (α = 5%)', 'Necessário (α = 2,5%, Holm)',
                                           'Disponível no estudo', 'Poder com o disponível'])
tabela(poder_df, 'sin_poder', 'Poder do experimento: cerca de 60% para o efeito observado sobre o tempo; no acordo na AC, só diferenças grandes eram detectáveis',
       secao='7.4.3', formatos={'Necessário (α = 5%)': 0, 'Necessário (α = 2,5%, Holm)': 0, 'Disponível no estudo': 'int',
                                 'Poder com o disponível': 'pct'},
       nota=f'tempo: número de sentenças nos dois braços comparados (Controle + Remota = {d_rc}; Controle + Presencial = {d_pc}); '
            f'acordo: AC realizadas por braço (menor braço = {n_disp}); taxa-base de acordo na AC = {pct_br(p_base, 1)} '
            f'({int(k_ac.sum())}/{int(n_ac.sum())}); 13,3% = índice histórico da unidade. Poder com α = 5%.',
       fonte='Elaboração própria; fórmula de Schoenfeld (1983) e aproximação arco-seno para proporções.')

fig, axs = plt.subplots(1, 2, figsize=(13, 5.2))
hrs = np.linspace(0.72, 0.93, 200)
ax = axs[0]
ax.plot(hrs, eventos_nec(hrs), color=TINTA_2, lw=2, label='α = 5%')
ax.plot(hrs, eventos_nec(hrs, a=0.025), color=TINTA_2, lw=1.4, ls='--', label='α = 2,5% (Holm)')
ax.axhline(d_rc, color=DESTAQUE, lw=1.2)
ax.annotate(f'sentenças disponíveis (Controle + Remota) = {d_rc}', (0.928, d_rc), xytext=(0, -14), textcoords='offset points',
            fontsize=8.5, color=DESTAQUE, ha='right')
for g in hr_obs:
    ax.plot(hr_obs[g], eventos_nec(hr_obs[g]), 'o', color=CORES_GRUPO[g], ms=8,
            label=f'HR observado {g} ({fmt_br(hr_obs[g], 2)}): poder {pct_br(poder_cox(d_rc if g == "Remota" else d_pc, hr_obs[g]), 0)}')
ax.set_ylim(0, 5000)
ax.set_xlabel('Razão de riscos a detectar (HR)'); ax.set_ylabel('Sentenças necessárias (poder 80%)')
ax.set_title('Tempo até a sentença (Cox, dois braços 1:1)')
ax.legend(loc='upper left', fontsize=8.5)
ax = axs[1]
p2s = np.linspace(0.07, 0.22, 200)
ax.plot(p2s * 100, n_prop(p_base, p2s), color=TINTA_2, lw=2, label='α = 5%')
ax.plot(p2s * 100, n_prop(p_base, p2s, a=0.025), color=TINTA_2, lw=1.4, ls='--', label='α = 2,5% (Holm)')
ax.axhline(n_disp, color=DESTAQUE, lw=1.2)
ax.annotate(f'AC realizadas no menor braço = {n_disp}', (21.8, n_disp), xytext=(0, 5), textcoords='offset points',
            fontsize=8.5, color=DESTAQUE, ha='right')
ax.axvline(13.3, color=CINZA, lw=1, ls=':')
ax.annotate('índice histórico\nda unidade (13,3%)', (13.3, 1200), xytext=(5, 0), textcoords='offset points', fontsize=8.5, color=TINTA_2)
ax.set_ylim(0, 1500)
ax.set_xlabel(f'Taxa de acordo na AC a detectar no outro braço (%; base {pct_br(p_base, 1)})')
ax.set_ylabel('AC realizadas necessárias por braço (poder 80%)')
ax.set_title('Acordo na AC (duas proporções)')
ax.legend(loc='upper right', fontsize=8.5)
figura(fig, 'sin_poder', 'Quantos processos uma replicação precisaria: o efeito observado na Remota exigiria cerca de 1,5 vez as sentenças disponíveis',
       secao='7.4.3', nota='fórmula de Schoenfeld (1983) para o Cox; transformação arco-seno para proporções; poder de 80%.')
''')

interp('sin_poder')

md(r'''
## 7.5 Considerações finais

O experimento do 4º JEC de Natal é uma contribuição valiosa justamente porque é um experimento: o sorteio permitiu responder a uma pergunta causal que estudos observacionais sobre a conciliação raramente conseguem responder. A resposta, porém, é a oposta da que os autores anunciaram: a obrigatoriedade da AC inaugural **não acelerou** os processos e **não aumentou** a conciliação na audiência; alongou o tempo até a sentença e transformou parte das sentenças de mérito em extinções sem mérito. A divergência não vem dos dados, que são fidedignos, mas da **análise**: médias calculadas sobre processos ainda em curso, sem tratamento da censura, sem teste e sem intervalo. O exercício mostra, assim, o valor da ciência de dados aplicada ao Direito: os mesmos registros, tratados com os métodos adequados (curadoria explícita, análise de sobrevivência, riscos competitivos e controle de multiplicidade), mudam a conclusão sobre uma política judiciária.

A replicação deve preservar o que o experimento fez bem (sorteio individual, controle contemporâneo, registro diário) e corrigir o que limitou a sua validade: pré-registro, aleatorização documentada e estratificada, rodízio das conciliadoras, cegamento da extração, coleta das covariáveis e do motivo da extinção, seguimento comum e, sobretudo, várias unidades judiciais.

## 7.6 Referências

AALEN, O. O.; JOHANSEN, S. An empirical transition matrix for non-homogeneous Markov chains based on censored observations. **Scandinavian Journal of Statistics**, v. 5, n. 3, p. 141-150, 1978.

ALENCAR, P. G. M. de. **Impacto da audiência de conciliação no tempo de tramitação dos processos do 4º JEC de Natal/RN**: efeitos do art. 334 do CPC e das mudanças impostas pela pandemia da Covid-19. Projeto de pesquisa (Mestrado Profissional em Direito e Políticas Públicas) — Universidade Federal de Goiás, Goiânia, 2026.

ALENCAR, P. G. M. de; NEVES, C. B. das. Eficácia da conciliação obrigatória na tramitação processual: um experimento no 4º Juizado Especial Cível de Natal (2026). In: ENCONTRO DE ADMINISTRAÇÃO DA JUSTIÇA (ENAJUS), Goiânia, 2026. **Resumo expandido**.

ARTES, R.; BARROSO, L. P. **Métodos multivariados de análise estatística**. São Paulo: Blucher, 2023.

AUSTIN, P. C.; LEE, D. S.; FINE, J. P. Introduction to the analysis of survival data in the presence of competing risks. **Circulation**, v. 133, n. 6, p. 601-609, 2016.

BARBETTA, P. A.; REIS, M. M.; BORNIA, A. C. **Estatística para cursos de engenharia e informática**. São Paulo: Atlas, 2020.

BECKER, J. L. **Estatística básica**: transformando dados em informação. Porto Alegre: Bookman, 2015.

BENJAMINI, Y.; HOCHBERG, Y. Controlling the false discovery rate: a practical and powerful approach to multiple testing. **Journal of the Royal Statistical Society: Series B**, v. 57, n. 1, p. 289-300, 1995.

BRASIL. Conselho Nacional de Justiça. **API Pública do DataJud**: documentação. Brasília: CNJ, [2023]. Disponível em: https://datajud-wiki.cnj.jus.br/api-publica/. Acesso em: 12 nov. 2026.

BRASIL. Conselho Nacional de Justiça. **Justiça em Números 2026**: ano-base 2025. Brasília: CNJ, 2026. Disponível em: https://www.cnj.jus.br/pesquisas-judiciarias/justica-em-numeros/. Acesso em: 12 nov. 2026.

BRASIL. Conselho Nacional de Justiça. Resolução nº 125, de 29 de novembro de 2010. Dispõe sobre a Política Judiciária Nacional de tratamento adequado dos conflitos de interesses no âmbito do Poder Judiciário. Brasília: CNJ, 2010.

BRASIL. Lei nº 9.099, de 26 de setembro de 1995. Dispõe sobre os Juizados Especiais Cíveis e Criminais. **Diário Oficial da União**, Brasília, 27 set. 1995.

BRASIL. Lei nº 13.105, de 16 de março de 2015. Código de Processo Civil. **Diário Oficial da União**, Brasília, 17 mar. 2015.

BRASIL. Lei nº 13.994, de 24 de abril de 2020. Altera a Lei nº 9.099, de 26 de setembro de 1995, para possibilitar a conciliação não presencial no âmbito dos Juizados Especiais Cíveis. **Diário Oficial da União**, Brasília, 27 abr. 2020.

BROOKMEYER, R.; CROWLEY, J. A confidence interval for the median survival time. **Biometrics**, v. 38, n. 1, p. 29-41, 1982.

COLOSIMO, E. A.; GIOLO, S. R. **Análise de sobrevivência aplicada**. São Paulo: Blucher, 2006. (Projeto Fisher.)

COX, D. R. Regression models and life-tables. **Journal of the Royal Statistical Society: Series B**, v. 34, n. 2, p. 187-220, 1972.

DAVIDSON-PILON, C. lifelines: survival analysis in Python. **Journal of Open Source Software**, v. 4, n. 40, p. 1317, 2019.

EFRON, B. The efficiency of Cox's likelihood function for censored data. **Journal of the American Statistical Association**, v. 72, n. 359, p. 557-565, 1977.

FINE, J. P.; GRAY, R. J. A proportional hazards model for the subdistribution of a competing risk. **Journal of the American Statistical Association**, v. 94, n. 446, p. 496-509, 1999.

FLEMING, T. R.; HARRINGTON, D. P. **Counting processes and survival analysis**. New York: Wiley, 1991.

GESKUS, R. B. Cause-specific cumulative incidence estimation and the Fine and Gray model under both left truncation and right censoring. **Biometrics**, v. 67, n. 1, p. 39-49, 2011.

GRAMBSCH, P. M.; THERNEAU, T. M. Proportional hazards tests and diagnostics based on weighted residuals. **Biometrika**, v. 81, n. 3, p. 515-526, 1994.

GRAY, R. J. A class of K-sample tests for comparing the cumulative incidence of a competing risk. **The Annals of Statistics**, v. 16, n. 3, p. 1141-1154, 1988.

HOLM, S. A simple sequentially rejective multiple test procedure. **Scandinavian Journal of Statistics**, v. 6, n. 2, p. 65-70, 1979.

HOSMER, D. W.; LEMESHOW, S.; STURDIVANT, R. X. **Applied logistic regression**. 3. ed. Hoboken: Wiley, 2013.

INSTITUTO DE PESQUISA ECONÔMICA APLICADA (IPEA). **Diagnóstico sobre os Juizados Especiais Cíveis**: relatório de pesquisa. Brasília: Ipea; CNJ, 2013.

KAPLAN, E. L.; MEIER, P. Nonparametric estimation from incomplete observations. **Journal of the American Statistical Association**, v. 53, n. 282, p. 457-481, 1958.

MOORE, D. S.; NOTZ, W. I.; FLIGNER, M. A. **A estatística básica e sua prática**. Rio de Janeiro: LTC, 2023.

MORETTIN, P. A.; SINGER, J. M. **Estatística e ciência de dados**. Versão preliminar. São Paulo: IME-USP, abr. 2021.

PUTTER, H.; FIOCCO, M.; GESKUS, R. B. Tutorial in biostatistics: competing risks and multi-state models. **Statistics in Medicine**, v. 26, n. 11, p. 2389-2430, 2007.

ROYSTON, P.; PARMAR, M. K. B. Restricted mean survival time: an alternative to the hazard ratio for the design and analysis of randomized trials with a time-to-event outcome. **BMC Medical Research Methodology**, v. 13, art. 152, 2013.

SCHOENFELD, D. A. Sample-size formula for the proportional-hazards regression model. **Biometrics**, v. 39, n. 2, p. 499-503, 1983.

SCHULZ, K. F.; ALTMAN, D. G.; MOHER, D. CONSORT 2010 Statement: updated guidelines for reporting parallel group randomised trials. **BMJ**, v. 340, c332, 2010.

SEABOLD, S.; PERKTOLD, J. statsmodels: econometric and statistical modeling with Python. In: PYTHON IN SCIENCE CONFERENCE, 9., 2010, Austin. **Proceedings** [...]. Austin: SciPy, 2010. p. 92-96.

SIEGEL, S.; CASTELLAN JR., N. J. **Estatística não-paramétrica para ciências do comportamento**. 2. ed. Porto Alegre: Artmed, 2006.

THERNEAU, T. M.; GRAMBSCH, P. M. **Modeling survival data**: extending the Cox model. New York: Springer, 2000.
''')
