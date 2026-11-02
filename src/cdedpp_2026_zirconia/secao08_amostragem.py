# -*- coding: utf-8 -*-
"""Seção 8: tamanho amostral e uso do piloto."""

from collections.abc import Callable


def construir(md: Callable[[str], None], code: Callable[[str], None]) -> None:
    """Emite células de dimensionamento amostral para variáveis quantitativas e multinomiais."""
    md(r"""
    ## 8. Tamanho Amostral e Piloto

    Esta seção usa o piloto simulado com **n = 50** para demonstrar como
    transformar erro tipo I, erro tipo II, desvio padrão preliminar, efeito mínimo
    relevante e razão entre grupos em planejamento amostral. O piloto não serve
    para “provar” a hipótese. Ele fornece insumos instáveis, mas úteis, para
    dimensionamento prospectivo.

    O protocolo separa três exercícios:

    1. **Variável quantitativa intervalar assumida:** cálculo aproximado por teste
       t de duas amostras para `indice_acesso_saude`, usando o desvio padrão do
       piloto e a razão controle/atendido observada no piloto.
    2. **Desfecho multinomial 2x5:** simulação de poder para associação entre
       assistência jurídica e cinco categorias de `desfecho_pedido`, com vetores
       de probabilidades pré-especificados sob alternativa substantiva.
    3. **Calibração do OLS ajustado:** simulação de sensibilidade para o mesmo tipo
       de modelo usado na seção 6, reconhecendo efeitos fixos, covariáveis e
       inferência agrupada.

    O cálculo t é apenas aproximação. Ele ignora que a regressão ajustada pode
    reduzir variância residual ao controlar bons preditores, mas também pode
    aumentar incerteza por colinearidade entre exposição e covariáveis, capturada
    pelo $R^2$ auxiliar de `X` e pelo VIF. Também ignora dependência intraunidade,
    desequilíbrio de grupos e número finito de clusters. Portanto, não deve ser
    chamado de “conservador” sem demonstrar que o ganho de precisão supera essas
    fontes de inflação de variância.
    """)

    code(r"""
    # Separar grupos do piloto para estimar desvio padrão e razão de alocação observada.
    piloto_amostragem = piloto.copy()
    n_atendidos_piloto = int((piloto_amostragem["assistencia_juridica"].astype(str) == "Sim").sum())
    n_controles_piloto = int((piloto_amostragem["assistencia_juridica"].astype(str) == "Não").sum())
    ratio_piloto = n_controles_piloto / n_atendidos_piloto

    # Usar o desvio padrão amostral do piloto com ddof=1, como em planejamento clássico.
    s_piloto = float(piloto_amostragem["indice_acesso_saude"].std(ddof=1))

    # Definir efeito mínimo relevante antes de usar os testes principais.
    delta_minimo_relevante = 5.0
    d_cohen_piloto = delta_minimo_relevante / s_piloto

    # Calcular tamanho amostral aproximado para teste t bilateral de dois grupos.
    poder_t = TTestIndPower()
    n_atendidos_float = poder_t.solve_power(
        effect_size=d_cohen_piloto,
        alpha=alpha,
        power=poder_alvo,
        ratio=ratio_piloto,
        alternative="two-sided",
    )
    n_atendidos_quant = int(np.ceil(n_atendidos_float))
    n_controles_quant = int(np.ceil(ratio_piloto * n_atendidos_quant))
    N_quant = n_atendidos_quant + n_controles_quant

    # Avaliar sensibilidade a razões alternativas sem substituir silenciosamente o piloto por 1:1.
    ratios_sensibilidade = [ratio_piloto, 1.0, 0.50, 2.00]
    linhas_sensibilidade_quant = []
    for ratio_cenario in ratios_sensibilidade:
        n1_cenario = poder_t.solve_power(
            effect_size=d_cohen_piloto,
            alpha=alpha,
            power=poder_alvo,
            ratio=ratio_cenario,
            alternative="two-sided",
        )
        n_atendidos_cenario = int(np.ceil(n1_cenario))
        n_controles_cenario = int(np.ceil(ratio_cenario * n_atendidos_cenario))
        linhas_sensibilidade_quant.append(
            {
                "cenario": "ratio piloto" if np.isclose(ratio_cenario, ratio_piloto) else f"ratio {ratio_cenario:.2f}",
                "ratio_controle_por_atendido": ratio_cenario,
                "n_atendidos": n_atendidos_cenario,
                "n_controles": n_controles_cenario,
                "N_total": n_atendidos_cenario + n_controles_cenario,
            }
        )
    sensibilidade_quant = pd.DataFrame(linhas_sensibilidade_quant)

    # Definir vetores multinomiais de cinco níveis para H1 substantiva.
    p_controle_2x5 = np.array([0.22, 0.32, 0.18, 0.15, 0.13], dtype=float)
    p_atendido_2x5 = np.array([0.34, 0.33, 0.22, 0.06, 0.05], dtype=float)

    # Conferir probabilidades estritamente positivas e normalizadas.
    assert np.all(p_controle_2x5 > 0) and np.isclose(p_controle_2x5.sum(), 1)
    assert np.all(p_atendido_2x5 > 0) and np.isclose(p_atendido_2x5.sum(), 1)
    assert len(p_controle_2x5) == len(CATEGORIAS_DESFECHO) == 5
    assert len(p_atendido_2x5) == len(CATEGORIAS_DESFECHO) == 5

    def pvalor_tabela_2x5_planejamento(tabela, seed_offset=0, b_reamostragem=399):
        # Aplicar a mesma lógica da seção 7: qui-quadrado quando esperadas >= 5,
        # reamostragem condicional quando alguma esperada for pequena.
        chi2_obs, p_chi, gl, esperadas = stats.chi2_contingency(tabela, correction=False)
        if np.asarray(esperadas).min() >= 5:
            return float(p_chi), "qui-quadrado"

        rng_local = np.random.default_rng(SEMENTE + 9000 + seed_offset)
        margens_linha = np.asarray(tabela).sum(axis=1).astype(int)
        margens_coluna = np.asarray(tabela).sum(axis=0).astype(int)
        estatisticas = np.empty(b_reamostragem, dtype=float)
        for indice in range(b_reamostragem):
            tabela_sim = stats.random_table.rvs(
                margens_linha,
                margens_coluna,
                random_state=rng_local,
            )
            total = tabela_sim.sum()
            esperada_sim = np.outer(tabela_sim.sum(axis=1), tabela_sim.sum(axis=0)) / total
            estatisticas[indice] = ((tabela_sim - esperada_sim) ** 2 / esperada_sim).sum()
        p_reamostrado = (1 + int((estatisticas >= chi2_obs).sum())) / (1 + b_reamostragem)
        return float(p_reamostrado), "reamostragem"

    def estimar_poder_multinomial(N_total, ratio, reps=250):
        # Simular poder para a associação 2x5 sob alternativa pré-especificada.
        n_atendidos = int(np.ceil(N_total / (1 + ratio)))
        n_controles = int(np.ceil(ratio * n_atendidos))
        N_ajustado = n_atendidos + n_controles
        rng_mult = np.random.default_rng(SEMENTE + 3000 + int(N_total))
        rejeicoes = 0
        metodos = {"qui-quadrado": 0, "reamostragem": 0}

        for rep in range(reps):
            cont_atendidos = rng_mult.multinomial(n_atendidos, p_atendido_2x5)
            cont_controles = rng_mult.multinomial(n_controles, p_controle_2x5)
            tabela = np.vstack([cont_controles, cont_atendidos])
            p_valor, metodo = pvalor_tabela_2x5_planejamento(tabela, seed_offset=rep)
            rejeicoes += int(p_valor < alpha)
            metodos[metodo] += 1

        poder_estimado = rejeicoes / reps
        erro_mc_local = float(np.sqrt(poder_estimado * (1 - poder_estimado) / reps))
        return {
            "N_grid": N_total,
            "N_ajustado": N_ajustado,
            "n_atendidos": n_atendidos,
            "n_controles": n_controles,
            "ratio": ratio,
            "poder_estimado": poder_estimado,
            "erro_mc": erro_mc_local,
            "reps": reps,
            "usos_qui_quadrado": metodos["qui-quadrado"],
            "usos_reamostragem": metodos["reamostragem"],
        }

    # Buscar o menor N em uma grade moderada para manter o notebook executável.
    grade_N = list(range(120, 901, 60))
    resultados_mult = pd.DataFrame(
        [estimar_poder_multinomial(N, ratio_piloto, reps=250) for N in grade_N]
    )
    candidatos_mult = resultados_mult.loc[
        resultados_mult["poder_estimado"] >= poder_alvo
    ].copy()
    if candidatos_mult.empty:
        N_multinomial_2x5 = int(resultados_mult.loc[resultados_mult["poder_estimado"].idxmax(), "N_ajustado"])
        status_mult = "poder alvo não atingido na grade; ampliar busca"
    else:
        N_multinomial_2x5 = int(candidatos_mult.iloc[0]["N_ajustado"])
        status_mult = "poder alvo atingido na grade"

    # Cálculo complementar de aderência de uma amostra, rotulado como distinto do teste 2x5.
    p0_gof = p_controle_2x5.copy()
    p1_gof = p_atendido_2x5.copy()
    w_gof = float(np.sqrt(np.sum((p1_gof - p0_gof) ** 2 / p0_gof)))
    poder_gof = GofChisquarePower()
    N_gof = int(
        np.ceil(
            poder_gof.solve_power(
                effect_size=w_gof,
                n_bins=len(CATEGORIAS_DESFECHO),
                alpha=alpha,
                power=poder_alvo,
            )
        )
    )

    # Calibração por simulação do OLS ajustado, com número moderado de repetições.
    def calibrar_ols_cluster(N_total, reps=50):
        # Gerar bases novas e aplicar modelo semelhante ao da seção 6.
        rejeicoes = 0
        estimativas_validas = 0
        for rep in range(reps):
            simulado, _ = gerar_pedidos_simulados(
                n=N_total,
                prefixo_id=f"CAL{N_total}_{rep}",
                seed=SEMENTE + 50000 + N_total + rep,
            )
            base = simulado.copy()
            base["assistencia_binaria"] = (
                base["assistencia_juridica"].astype(str).eq("Sim").astype(int)
            )
            base["unidade_zus"] = base["unidade_zus"].astype("category")
            base["ano_pedido"] = base["ano_pedido"].astype("category")
            base["completude_documental"] = base["completude_documental"].astype("category")

            # Pular réplica se não houver dois grupos ou clusters suficientes.
            if base["assistencia_binaria"].nunique() < 2 or base["unidade_zus"].nunique() < 30:
                continue

            try:
                formula_calibracao = (
                    "indice_acesso_saude ~ assistencia_binaria"
                    " + gravidade_clinica + renda_pc_zirc + idade"
                    " + C(completude_documental)"
                    " + C(ano_pedido)"
                    " + C(unidade_zus)"
                )
                ajuste_cal = smf.ols(formula_calibracao, data=base).fit(
                    cov_type="cluster",
                    cov_kwds={"groups": base["unidade_zus"], "use_correction": True},
                    use_t=True,
                )
                p_cal = float(ajuste_cal.pvalues["assistencia_binaria"])
                if np.isfinite(p_cal):
                    estimativas_validas += 1
                    rejeicoes += int(p_cal < alpha)
            except Exception:
                continue

        if estimativas_validas == 0:
            return {
                "N": N_total,
                "poder_estimado": np.nan,
                "erro_mc": np.nan,
                "reps_validas": 0,
            }
        poder_estimado = rejeicoes / estimativas_validas
        erro_mc_local = float(np.sqrt(poder_estimado * (1 - poder_estimado) / estimativas_validas))
        return {
            "N": N_total,
            "poder_estimado": poder_estimado,
            "erro_mc": erro_mc_local,
            "reps_validas": estimativas_validas,
        }

    grade_ols = sorted(set([max(240, N_quant // 2), N_quant, max(N_quant + 200, 600), 900]))
    resultados_ols = pd.DataFrame([calibrar_ols_cluster(N, reps=50) for N in grade_ols])
    candidatos_ols = resultados_ols.dropna().loc[
        resultados_ols["poder_estimado"] >= poder_alvo
    ]
    if candidatos_ols.empty:
        N_OLS_calibrado = int(resultados_ols.dropna().sort_values("poder_estimado").iloc[-1]["N"])
        status_ols = "poder alvo não atingido na grade calibrada"
    else:
        N_OLS_calibrado = int(candidatos_ols.iloc[0]["N"])
        status_ols = "poder alvo atingido na grade calibrada"

    # Definir N final do protocolo, usando o maior objetivo inferencial e perdas.
    taxa_perda = 0.10
    N_sem_perdas = int(max(N_quant, N_multinomial_2x5, N_OLS_calibrado))
    N_final = int(np.ceil(N_sem_perdas / (1 - taxa_perda)))

    # Verificar contagens esperadas 2x5 para o N proposto sob as probabilidades planejadas.
    n_atendidos_final = int(np.ceil(N_final / (1 + ratio_piloto)))
    n_controles_final = int(np.ceil(ratio_piloto * n_atendidos_final))
    esperadas_final = np.vstack(
        [
            n_controles_final * p_controle_2x5,
            n_atendidos_final * p_atendido_2x5,
        ]
    )
    menor_esperada_final = float(esperadas_final.min())

    # Reunir síntese do dimensionamento.
    resumo_amostragem = pd.DataFrame(
        [
            {
                "objetivo": "Quantitativo intervalar - teste t aproximado",
                "N_recomendado": N_quant,
                "observacao": "Usa s_piloto, delta e ratio controle/atendido do piloto.",
            },
            {
                "objetivo": "Multinomial 2x5 - associação",
                "N_recomendado": N_multinomial_2x5,
                "observacao": status_mult,
            },
            {
                "objetivo": "OLS ajustado com EP cluster - calibração",
                "N_recomendado": N_OLS_calibrado,
                "observacao": status_ols,
            },
            {
                "objetivo": "Protocolo com perdas",
                "N_recomendado": N_final,
                "observacao": f"Maior N sem perdas = {N_sem_perdas}; taxa de perdas = {taxa_perda:.0%}.",
            },
        ]
    )

    # Asserts exigidos pelo protocolo.
    assert len(piloto_amostragem) == 50
    assert s_piloto > 0
    assert delta_minimo_relevante > 0
    assert n_atendidos_piloto > 0 and n_controles_piloto > 0
    assert ratio_piloto > 0
    assert np.isclose(ratio_piloto, n_controles_piloto / n_atendidos_piloto)
    assert n_controles_quant == int(np.ceil(ratio_piloto * n_atendidos_quant))
    assert 0 < alpha < 1 and 0 < beta < 1 and 0 < taxa_perda < 1
    assert w_gof > 0
    assert N_quant > 0 and N_multinomial_2x5 > 0 and N_gof > 0 and N_OLS_calibrado > 0
    assert N_final >= max(N_quant, N_multinomial_2x5, N_OLS_calibrado)
    assert menor_esperada_final >= 5, "N final não garante esperadas mínimas planejadas."
    assert resultados_mult["poder_estimado"].between(0, 1).all()
    assert resultados_ols["poder_estimado"].dropna().between(0, 1).all()

    # Exibir resultados.
    parametros_piloto = pd.DataFrame(
        [
            ("n_piloto", len(piloto_amostragem)),
            ("n_atendidos_piloto", n_atendidos_piloto),
            ("n_controles_piloto", n_controles_piloto),
            ("ratio_controle_por_atendido", ratio_piloto),
            ("s_piloto_ddof1", s_piloto),
            ("delta_minimo_relevante", delta_minimo_relevante),
            ("d_cohen_piloto", d_cohen_piloto),
        ],
        columns=["parametro", "valor"],
    )
    display(parametros_piloto)
    display(sensibilidade_quant)
    display(resultados_mult.round(3))
    display(pd.DataFrame({"categoria": CATEGORIAS_DESFECHO, "p_controle": p_controle_2x5, "p_atendido": p_atendido_2x5}))
    display(pd.DataFrame([{"w_gof_aderencia": w_gof, "N_gof_uma_amostra": N_gof}]).round(3))
    display(resultados_ols.round(3))
    display(resumo_amostragem)

    # Gráfico: poder estimado para multinomial e OLS calibrado.
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.lineplot(
        data=resultados_mult,
        x="N_ajustado",
        y="poder_estimado",
        marker="o",
        label="Multinomial 2x5",
        ax=ax,
    )
    sns.lineplot(
        data=resultados_ols,
        x="N",
        y="poder_estimado",
        marker="s",
        label="OLS ajustado cluster",
        ax=ax,
    )
    ax.axhline(poder_alvo, color="black", linestyle="--", label=f"poder alvo = {poder_alvo:.2f}")
    ax.set_title("Poder estimado por simulação no planejamento amostral")
    ax.set_xlabel("N total planejado")
    ax.set_ylabel("Poder estimado")
    ax.set_ylim(0, 1.02)
    ax.legend()
    ax.text(
        0.01,
        -0.20,
        "Fonte: simulações de planejamento baseadas no piloto e nos parâmetros pré-especificados.",
        transform=ax.transAxes,
        fontsize=9,
    )
    fig.tight_layout()
    fig.savefig(PASTA_FIGURAS / "amostragem_poder_simulado.png", dpi=150)
    plt.show()

    caminho_figura = PASTA_FIGURAS / "amostragem_poder_simulado.png"
    assert caminho_figura.is_file()
    assert caminho_figura.stat().st_size > 0

    print("Dimensionamento amostral concluído.")
    print("N_quant:", N_quant)
    print("N_multinomial_2x5:", N_multinomial_2x5)
    print("N_OLS_calibrado:", N_OLS_calibrado)
    print("N_final_com_perdas:", N_final)
    """)

    md(r"""
    ### Interpretação do dimensionamento

    O cálculo quantitativo usa o desvio padrão observado no piloto e um efeito
    mínimo relevante de 5 pontos no índice de acesso à saúde. Como a razão entre
    controles e atendidos foi estimada em apenas 50 observações, a sensibilidade a
    outras razões deve ser lida com cuidado. Não se deve substituir a razão piloto
    por 1:1 sem declarar essa decisão.

    O dimensionamento multinomial 2x5 usa vetores de probabilidades sob alternativa
    substantiva. Esse exercício corresponde à hipótese de associação entre dois
    grupos e cinco categorias; o cálculo complementar por `GofChisquarePower` é
    apenas uma demonstração de aderência de uma amostra, não substitui a hipótese
    2x5.

    A calibração do OLS ajustado aproxima o modelo realmente usado no notebook e
    explicita que o teste t simples pode ser otimista ou pessimista, conforme a
    estrutura de covariáveis, colinearidade, clusters e variância residual. Em um
    protocolo real, essa calibração deveria ser refinada com pressupostos vindos
    de literatura, estudo piloto independente ou dados administrativos prévios,
    nunca escolhida retroativamente para justificar resultados já observados.
    """)
