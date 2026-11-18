"""Revisão final para entrega (16/11/2026): correções de texto e de código aplicadas pelo gerador.

Cada substituição exige que o trecho original exista; se o notebook-base mudar, o
gerador falha em vez de produzir uma edição silenciosamente desatualizada.

Correções
1. Seção 10.6: o texto dizia "discriminam pouco" com AUC 0,85; agora decompõe o sinal
   (com e sem assunto) e explica que o universo difere do da logística dos F2.
2. Seções 10.3, 10.4, 14 e limitações: a conclusão "o DataJud não separa nada" passa a
   distinguir trajetória (pouco sinal) de assunto (sinal forte, Seções 24 e 31).
3. Seção 12 (R19): exibe a sensibilidade com n = 593 (decisão D4) e os totais na moldura.
4. Seção 8.3: "o efeito da F2_11 dobra" era afirmação forte demais (intervalos sobrepostos;
   OR não colapsável).
5. Seção 6.3: ressalva de comensurabilidade da comparação com os 30% da NT CIJMG.
6. Limpeza: margem de equivalência removida, código morto do TOST, D9 na tabela de
   decisões, título da Seção 1, numeração da Parte I, referência "Seção 6.4/8".
7. Mapa do roteiro, próximos passos e referências da Parte VI.
"""
from __future__ import annotations

import re

REFERENCIAS: str | None = None  # preenchido por markdown(); usado no fim do notebook


def troca(source: str, old: str, new: str, *, rotulo: str) -> str:
    if old not in source:
        raise RuntimeError(f"[revisão final] trecho ausente em {rotulo}: {old[:80]!r}")
    return source.replace(old, new)


def _bloco(source: str, chave: str, texto: str) -> str:
    novo, n = re.subn(rf"exibir\('{chave}', r'''[\s\S]*?'''\)", lambda _: f"exibir('{chave}', r'''{texto}''')",
                      source, count=1)
    if n != 1:
        raise RuntimeError(f"[revisão final] bloco {chave} não encontrado")
    return novo


SINTESE = r"""
**Síntese provisória (Partes I a IV).** Todos os números abaixo vêm das seções indicadas. As {{n_conferencias}} conferências contra o gabarito da apostila passaram. Foram registrados {{n_avisos}} avisos, listados acima. **A resposta final, que incorpora as Partes V e VI, está na Seção 35.**

| Item | Resposta curta | Seção |
|---|---|---|
| R1–R2 | P(indício) muda com o denominador: {{den_595}} (sorteados), {{den_444}} (elegíveis), {{den_233}} (Fase III). P(indício \| F2_02) = {{F2_02_lin_sim}} ≠ P(F2_02 \| indício) = {{F2_02_col_ind}} | §5 |
| R3–R4 | Bayes na notação do professor; dois pares H₀ × Hₐ: processo (partição do espaço amostral) e prevalência (partição do espaço de θ) | §6 |
| R5, R9 | priori principal 0,30 (NT CIJMG/Araripina) e Beta(6, 14); sensibilidade com 0,10, 0,50 e três outras Beta. A revisão de escopo é conceitual: os números vêm das notas técnicas | §6 |
| R6 | desfecho pelo proxy completo do DataJud: RV(extinção) = {{bay_0_RV}} {{bay_0_RVic}}; RV(acordo) = {{bay_1_RV}}. Evidência **fraca** | §3, §6 |
| R7–R8 | com priori 0,30 e extinção: P(D) = {{bay_0_tot03}} e posteriori {{bay_0_post03}}. Na prevalência da moldura, P(θ ≥ 0,30 \| dados) = {{beta_h0_444}} ({{n_elegiveis}} elegíveis) | §6 |
| R10 | multinomial: RRR de F2_02 = {{mn_rrr_ind_02}} (indício) e {{mn_rrr_cert_02}} (certeza) | §8 |
| R11 | ordinal: chances proporcionais **rejeitadas** (LR = {{lr_po}}; {{p_po}}); o PPO com F2_02 livre é adequado; a razão contínua mostra que os F2 não separam a certeza (OR de F2_02 no segundo passo = {{rc2_or02}} {{rc2_or02_ic}}) | §8 |
| R12 | condicional (JEC × ano, {{cl_uteis}} estratos úteis): OR de F2_11 = {{cl_or11}} {{cl_or11_ic}} | §8 |
| R13 | melhor ajuste: {{aj_bic_melhor}} pelo BIC; {{cv_melhor}} fora da amostra. Contra a Hadja, **empate** na dicotomia | §9 |
| R14 | AUC = {{auc_h}} e Gini = {{gini_h}} em **todos** os modelos (DeLong p igual a um: há só {{n_padroes}} padrões de preditores); fora da amostra, AUC = {{cv_auc}} | §9 |
| R15–R16 | LCA não supervisionada nos dados do DataJud: três trajetórias processuais; kappa ponderado contra a Hadja = {{av_kpond}}, J = {{av_J}}. Com os rótulos, as mesmas variáveis chegam a AUC {{sup_auc}}, e {{sup_auc_sem}} sem o assunto: o sinal do DataJud está no **assunto**. Nos F2, kappa ponderado = {{f2_kp}}; com F3, {{f23_kp}} (circular) | §10 |
| R17–R18 | perfis de trajetória em `estcaso3_revisado/tabelas/trajetorias_processuais.xlsx`: {{lista_0}} / {{lista_1}} / {{lista_2}} processos; sem valor de triagem jurídica | §11 |
| R19 | os perfis não permitem responder: proporção aparente {{r19_pap}} e correção instável {{r19_rg}} (intervalo exploratório {{r19_ic}}). Pela amostra: {{p_indicio}}, Wilson aproximado por n efetivo {{ic_des}}, isto é, {{total_des}} processos na moldura; sem os {{n_nao_localizados}} não localizados, {{p_593}} {{ic_593}}. O intervalo publicado é Wald + FPC, e não Wilson. A estimativa com o assunto de toda a moldura está na Seção 31 | §12, §31 |
| P1 | CA de JEC × classe3 (inércia {{ca_inercia}} = χ²/n; {{ca_p}}); MCA com eixo documental dominante ({{mca_b1}} Benzécri); biplots simétrico, assimétrico e de contribuição | §7 |
| P2 | gerador encadeado (LCA → logística → desfecho → lognormal), recuperação dos parâmetros e Quadro de Variáveis ({{qt_n}} linhas) para a turma | §2, §13 |

**O que se pode afirmar até aqui.** Os sinais formais da petição (F2_01, F2_02, F2_11) separam bem a predação da não predação: AUC ≈ {{cv_auc}} fora da amostra. Eles **não** separam a certeza do indício. A **trajetória** registrada no DataJud (desfecho, recurso, tempo) quase não separa nenhuma das duas, mas o **assunto** do processo, que também está no DataJud, separa o indício (Seção 10.6, aprofundada nas Seções 24 e 31). A certeza depende da multiplicidade de ações da parte (F3_18), que não aparece em nenhuma das fontes automáticas.
"""

R19 = r"""
**O exercício populacional não identifica a prevalência jurídica.** A proporção aparente de perfis que receberiam o antigo nome de indício é {{r19_pap}}, mas a concordância com a classificação da pesquisa é fraca (J de Youden = {{r19_J}}). A inversão de Rogan–Gladen produz {{r19_rg}}, com intervalo exploratório {{r19_ic}}; a amplitude mostra que esse número não tem precisão útil. Para a certeza, J = {{r19c_J}} e a correção é indefinida.

O bootstrap aqui mantém o modelo ajustado e suas atribuições fixos. Ele não incorpora toda a incerteza de ajuste e escolha dos grupos; por isso o intervalo não deve ser usado para afirmar igualdade ou equivalência com a pesquisa.

**O que a amostra probabilística sustenta.**

- **Indício:** {{p_indicio}}, com aproximação de Wilson por tamanho efetivo {{ic_des}}. Projetado na moldura de {{N_moldura}}, são **{{total_des}}** processos, a mesma ordem de grandeza dos "cerca de 8.880" do roteiro.
- **Certeza:** {{p_certeza}} {{ic_des_c}}, ou {{total_des_c}} processos.
- **Sensibilidade D4:** sem os {{n_nao_localizados}} processos não localizados no PJe, o indício seria {{p_593}} {{ic_593}}. A decisão de mantê-los no denominador não muda a conclusão.
- **O intervalo publicado** {{ic_pub}} foi calculado por Wald com correção de população finita (N = 83.139), apesar do nome usado no roteiro. A estimativa amostral cai dentro dele.

Os perfis do DataJud descrevem trajetórias, mas não refinam a prevalência. O que **refina** é o assunto, conhecido para todos os processos da moldura: a Seção 31 refaz esta estimativa por regressão hierárquica com pós-estratificação.
"""

SUPERVISIONADO = r"""
**Leitura (sensibilidade): com os rótulos, as variáveis do DataJud discriminam o indício, e o sinal está no assunto.** Uma logística regularizada treinada **com** os rótulos da Hadja, sobre as mesmas sete variáveis do DataJud, tem AUC fora da amostra de **{{sup_auc}}** (DP {{sup_dp}}; validação cruzada estratificada repetida) nos {{sup_n}} processos com documento, com prevalência de {{sup_prev}}.

- **Sem o assunto**, só com a trajetória (desfecho, recurso, cumprimento, redistribuição, tempo e movimentos), a AUC cai para {{sup_auc_sem}} (DP {{sup_dp_sem}}).
- **Só com o assunto**, em cinco categorias, a AUC é {{sup_auc_ass}} (DP {{sup_dp_ass}}).

**Consequência.** A LCA não supervisionada (Seção 10.2) não encontra o sinal porque agrupa os processos pela trajetória, que domina a variação dos registros. O sinal existe, mas está no **assunto**, e só aparece quando se usam os rótulos. A AUC desta seção **não é comparável** com a da logística sobre os F2 (Seção 9): aquela foi calculada nos 233 da Fase III, e esta nos 593 processos com documento, com outra prevalência. As Seções 24 a 31 retomam a pergunta com o assunto detalhado, com divisão temporal e como informação auxiliar para a prevalência.
"""

CONDICIONAL_TITULO_OLD = "**Leitura (R12): comparando dentro do mesmo juizado e ano, o efeito da F2_11 dobra.**"
CONDICIONAL_TITULO_NEW = ("**Leitura (R12): dentro do mesmo juizado e ano, o OR da F2_11 é maior, mas a diferença em relação "
                          "à logística sem estratos não é demonstrada.**")
CONDICIONAL_LEITURA_OLD = ("  - **Leitura:** parte da variação da F2_11 entre juizados mascarava o efeito. Dentro do mesmo JEC e ano, "
                           "o advogado de fora da comarca se associa mais fortemente ao indício.")
CONDICIONAL_LEITURA_NEW = ("  - **Leitura:** o OR condicional é maior que o marginal, mas os intervalos se sobrepõem bastante. "
                           "Parte da diferença é esperada mesmo sem confundimento: o OR **não é colapsável**, e o OR dentro do "
                           "estrato tende a se afastar mais de um que o OR marginal quando os estratos diferem na taxa-base "
                           "(GREENLAND; ROBINS; PEARL, 1999). Não se conclui que o efeito \"dobre\" nem que a variação entre "
                           "juizados o mascarasse.")


def markdown(idx: int, source: str) -> str:
    if idx == 0:
        source = troca(source, "| R19 | o resultado cai no IC de 17,65%? | 12 |",
                       "| R19 | o resultado cai no IC de 17,65%? | 12, 16 e 31 |", rotulo="mapa R19")
        source = troca(source, "| P2 | simulação, Quadro de Variáveis e Dicionário de Dados | 2 e 13 |",
                       "| P2 | simulação, Quadro de Variáveis e Dicionário de Dados | 2, 13, 19 e 23 |\n"
                       "| — | sensibilidade dos métodos e previsão no ajuizamento | 15–30 |\n"
                       "| — | modelos bayesianos: MRP, verossimilhanças incertas, erro de codificação, logística com prioris | 31–34 |\n"
                       "| — | **resposta final consolidada** | **35** |", rotulo="mapa P2")
        d10 = ("| D10 | auditoria dos desfechos | comparação automática de regras TPU e consistência temporal; "
               "validade jurídica externa não observável |")
        source = troca(source, d10,
                       "| D9 | volumes por parte e advogado (proxies de F3) | pendente; não aplicada |\n" + d10 +
                       "\n| D11 | prioris bayesianas (Parte VI) | fracamente informativas, declaradas em cada seção; "
                       "sensibilidade quando a conclusão depende delas |", rotulo="decisões D9 e D11")
    if "### 14.2 Limitações" in source:
        source = troca(source, "regra de ordenação das classes e margem de equivalência foram fixados",
                       "e regra de ordenação das classes foram fixados", rotulo="limitação 8")
        source = troca(source, "Priori, denominador, corte, e regra", "Priori, denominador, corte e regra",
                       rotulo="limitação 8 (vírgula)")
        source = troca(source,
                       "7. **Informação do DataJud.** A API não traz petição, partes nem advogados, e por isso não carrega "
                       "os sinais que definem a predação. O classificador da população é limitado por isso, e não pelo método.",
                       "7. **Informação do DataJud.** A API não traz petição, partes nem advogados. O assunto, que ela traz, "
                       "reproduz bem o rótulo de indício (Seções 24 e 31), mas nada nela informa a certeza (F3_18) nem a "
                       "massificação em si. A trajetória processual acrescenta pouco ao assunto (Seções 22 e 28–30).",
                       rotulo="limitação 7")
        source = troca(source, "   - o `OrderedModel` usa probit por padrão.\n",
                       "   - o `OrderedModel` usa probit por padrão.\n"
                       "10. **Validade da regra de codificação.** O assunto 6226 concentra 74 dos 105 indícios. Se F3_19 e "
                       "F3_20 foram avaliadas olhando a massa de ações do mesmo assunto, os modelos reproduzem em parte o "
                       "próprio critério da codificação (Seções 32 e 33).\n", rotulo="limitação 10")
        source = troca(source, "\n\n### 14.4 Referências",
                       "\n5. **Validar o modelo de assunto numa coorte posterior** (ajuizamentos de 2025), com rótulos "
                       "atribuídos sem conhecer o modelo, antes de qualquer uso em triagem.\n\n### 14.4 Referências",
                       rotulo="próximo passo 5")
        source = troca(source, "**Fontes primárias citadas por nome** (fora do acervo):",
                       "**Métodos bayesianos (Parte VI).**\n"
                       "- GELMAN, A. et al. *Bayesian data analysis*. 3. ed. Boca Raton: CRC, 2013.\n"
                       "- GELMAN, A.; JAKULIN, A.; PITTAU, M. G.; SU, Y.-S. A weakly informative default prior distribution "
                       "for logistic and other regression models. *The Annals of Applied Statistics*, v. 2, n. 4, "
                       "p. 1360–1383, 2008.\n"
                       "- GELMAN, A.; LITTLE, T. C. Poststratification into many categories using hierarchical logistic "
                       "regression. *Survey Methodology*, v. 23, n. 2, p. 127–135, 1997.\n"
                       "- GREENLAND, S.; ROBINS, J. M.; PEARL, J. Confounding and collapsibility in causal inference. "
                       "*Statistical Science*, v. 14, n. 1, p. 29–46, 1999.\n"
                       "- GUSTAFSON, P. *Bayesian inference for partially identified models*. Boca Raton: CRC, 2015.\n"
                       "- JOSEPH, L.; GYORKOS, T. W.; COUPAL, L. Bayesian estimation of disease prevalence and the "
                       "parameters of diagnostic tests in the absence of a gold standard. *American Journal of "
                       "Epidemiology*, v. 141, n. 3, p. 263–272, 1995.\n"
                       "- MCELREATH, R. *Statistical rethinking*. 2. ed. Boca Raton: CRC, 2020.\n"
                       "- PARK, D. K.; GELMAN, A.; BAFUMI, J. Bayesian multilevel estimation with poststratification. "
                       "*Political Analysis*, v. 12, n. 4, p. 375–385, 2004.\n"
                       "- VEHTARI, A.; GELMAN, A.; GABRY, J. Practical Bayesian model evaluation using leave-one-out "
                       "cross-validation and WAIC. *Statistics and Computing*, v. 27, p. 1413–1432, 2017.\n\n"
                       "**Fontes primárias citadas por nome** (fora do acervo):", rotulo="referências bayesianas")
        source = troca(source, "statsmodels, scikit-learn, lifelines, prince, stepmix, kmodes, matplotlib",
                       "statsmodels, scikit-learn, lifelines, prince, stepmix, kmodes, PyMC, ArviZ, matplotlib",
                       rotulo="software")
        # As referências saem do meio do notebook e vão para a última seção (ver build.py)
        global REFERENCIAS
        antes, marcador, depois = source.partition("\n\n### 14.4 Referências\n")
        if not marcador:
            raise RuntimeError("[revisão final] bloco de referências não encontrado")
        REFERENCIAS = depois.strip()
        source = antes.rstrip() + "\n"
    if "(Seção 6.4/8)" in source:
        source = troca(source, "(Seção 6.4/8)", "(Seções 6.4 e 8)", rotulo="referência 6.4/8")
    return source


def code(idx: int, source: str) -> str:
    for antigo, novo in (("# 2.2 Tipagem", "# 2.1 Tipagem"), ("# 2.3 Ausência", "# 2.1 Ausência"),
                         ("# 2.4 Reconstrução", "# 2.2 Reconstrução"), ("# 2.5 Estratos", "# 2.3 Estratos")):
        source = source.replace(antigo, novo)
    if source.startswith("# 10.6 Sensibilidade"):
        source = troca(source, "V.update(sup_auc=fnum(auc_sup.mean(), 3), sup_dp=fnum(auc_sup.std(), 3))",
                       """V.update(sup_auc=fnum(auc_sup.mean(), 3), sup_dp=fnum(auc_sup.std(), 3))
# decomposição do sinal: a mesma logística sem o assunto e só com o assunto
X_sem_assunto = pd.get_dummies(XDJ.drop(columns=['assunto']).astype(str), drop_first=True).astype(float)
X_so_assunto = pd.get_dummies(XDJ[['assunto']].astype(str), drop_first=True).astype(float)
auc_sup_sem = cross_val_score(LogisticRegression(C=1.0, max_iter=2000), X_sem_assunto, ysup, scoring='roc_auc', cv=cv10)
auc_sup_ass = cross_val_score(LogisticRegression(C=1.0, max_iter=2000), X_so_assunto, ysup, scoring='roc_auc', cv=cv10)
display(pd.DataFrame({'AUC média (CV 5 × 10)': [auc_sup.mean(), auc_sup_sem.mean(), auc_sup_ass.mean()],
                      'DP': [auc_sup.std(), auc_sup_sem.std(), auc_sup_ass.std()]},
                     index=['sete variáveis do DataJud', 'sem o assunto (só trajetória)', 'só o assunto']).round(3))
V.update(sup_auc_sem=fnum(auc_sup_sem.mean(), 3), sup_dp_sem=fnum(auc_sup_sem.std(), 3),
         sup_auc_ass=fnum(auc_sup_ass.mean(), 3), sup_dp_ass=fnum(auc_sup_ass.std(), 3),
         sup_n=fint(len(ysup)), sup_prev=fpct(ysup.mean(), 1))""", rotulo="10.6 decomposição")
    if "R19 = {}" in source and "B_RG" in source:
        source = troca(source,
                       "    delta = (ref['publicado (Wald + FPC, N = 83.139)'][1] - ref['publicado (Wald + FPC, N = 83.139)'][0]) / 2\n"
                       "    dif = np.nan  # não testar igualdade a partir de correção instável e modelo sem validação\n"
                       "    ep_dif = np.nan\n", "", rotulo="12.1 código morto (delta)")
        source = troca(source,
                       "frac_truncado=np.nanmean((boot <= 0) | (boot >= 1)), delta=delta,\n"
                       "                     dif=dif, ic_dif=(dif - C.Z95 * ep_dif, dif + C.Z95 * ep_dif),\n"
                       "                     p_dif=np.nan,\n"
                       "                     tost=False,  # não identificado; TOST não aplicável\n",
                       "frac_truncado=np.nanmean((boot <= 0) | (boot >= 1)),\n", rotulo="12.1 código morto (dict)")
        source = troca(source, ", r19_delta=fnum(100 * ri['delta'], 2),\n", ",\n", rotulo="12.1 r19_delta")
        source = troca(source,
                       "         r19_dif=fnum(100 * ri['dif'], 1), r19_ic_dif=fic(100 * ri['ic_dif'][0], 100 * ri['ic_dif'][1], 1), r19_p_dif=fp(ri['p_dif']),\n"
                       "         r19_tost='equivalência demonstrada' if ri['tost'] else 'equivalência **não** demonstrada',\n",
                       "", rotulo="12.1 r19_dif/tost")
        source = troca(source,
                       "         r19c_tost='equivalência demonstrada' if rc['tost'] else 'equivalência **não** demonstrada',\n",
                       "", rotulo="12.1 r19c_tost")
        source += ("\nV.update(total_des_c=f\"{fint(est_cer['total'])} {fic(*[int(round(v)) for v in est_cer['total_ic']], casas=0)}\")\n")
    return source


def interpretacao(source: str) -> str:
    if source.startswith("exibir('ns_supervisionado'"):
        source = _bloco(source, "ns_supervisionado", SUPERVISIONADO)
    if source.startswith("exibir('r19_resposta'"):
        source = _bloco(source, "r19_resposta", R19)
    if source.startswith("exibir('sintese'"):
        source = _bloco(source, "sintese", SINTESE)
    if source.startswith("exibir('ns_confusao_datajud'"):
        source = troca(source, "As outras variáveis do DataJud (recurso, cumprimento, tempo, assunto) descrevem a "
                               "**trajetória do processo depois do ajuizamento**.",
                       "As outras variáveis do DataJud (recurso, cumprimento, tempo) descrevem a **trajetória do processo "
                       "depois do ajuizamento**. O assunto é a exceção, mas na LCA ele pesa pouco diante dos indicadores "
                       "de trajetória.", rotulo="10.3 assunto")
        source = troca(source, "e nada disso está no DataJud.", "e nenhuma dessas leituras está no DataJud.",
                       rotulo="10.3 F2/F3")
        source = troca(source, "e **esses dados não carregam a informação** necessária para separar as classes.",
                       "mas a **trajetória** processual, que domina a variação desses registros, não carrega a "
                       "informação necessária para separar as classes. O sinal que existe no DataJud está no assunto, e "
                       "só aparece com supervisão (Seção 10.6).", rotulo="10.3 conclusão")
    if source.startswith("exibir('ns_comparacoes'"):
        source = troca(source, "As variáveis processuais do DataJud não separam nenhuma das duas coisas.",
                       "A trajetória processual do DataJud, agrupada sem rótulos, não separa nenhuma das duas. O assunto "
                       "separa o indício quando usado com os rótulos (Seções 10.6, 24 e 31).", rotulo="10.4 resumo")
    if source.startswith("exibir('md_condicional_firth'"):
        source = troca(source, CONDICIONAL_TITULO_OLD, CONDICIONAL_TITULO_NEW, rotulo="8.3 título")
        source = troca(source, CONDICIONAL_LEITURA_OLD, CONDICIONAL_LEITURA_NEW, rotulo="8.3 leitura")
    if source.startswith("exibir('by_prevalencia'"):
        source = troca(source, "Com qualquer denominador e qualquer priori testada, os dados a contradizem.",
                       "Com qualquer denominador e qualquer priori testada, os dados a contradizem **para a moldura "
                       "inteira**.\n\n**Ressalva de comensurabilidade.** Os 30% da NT CIJMG referem-se ao fluxo de **dois "
                       "assuntos**, e θ aqui é a prevalência em todos os assuntos da moldura. É o mesmo problema de "
                       "denominador apontado na Seção 5.2 (A-23). A comparação compatível é por assunto: a Seção 31 mostra "
                       "que, no assunto 6226, a prevalência é muito superior a 30%.", rotulo="6.3 comensurabilidade")
    if source.startswith("exibir('by_processo'"):
        source = troca(source, "**Leitura jurídica.** A predação está na **forma** da petição (Seção 5), e não no resultado "
                               "do processo. É o que a Seção 10 vai confirmar no classificador.",
                       "**Leitura jurídica.** A predação aparece na **forma** da petição (Seção 5) e no **assunto** "
                       "(Seções 24 e 32), e não no resultado do processo. A Seção 32 refaz esta conta com as "
                       "verossimilhanças incertas.", rotulo="6.1 leitura jurídica")
    return source
