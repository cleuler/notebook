"""Modelos bayesianos da edição final do Estudo de Caso 3.

Funções puras: recebem tabelas ou contagens e devolvem sorteios e resumos. O
notebook mostra as entradas, as prioris e os diagnósticos de cada ajuste.

Conteúdo
- ``mrp_prevalencia``: regressão logística hierárquica (ano + JEC + assunto) com
  pós-estratificação na moldura de 50.320 processos (MRP), incluindo o total de
  processos como quantidade de população finita.
- ``pos_estratificado``: contraste de desenho, pós-estratificação simples por grupo.
- ``prevalencia_com_erro``: prevalência corrigida por sensibilidade e
  especificidade incertas da codificação (reamostragem por importância).
- ``bayes_processo``: Bayes por processo com verossimilhanças incertas
  (Dirichlet-multinomial) e priori Beta para P(Hₐ).
- ``logistica_bayes``: logística com prioris t de Student fracamente informativas.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats
from scipy.special import expit

Z95 = stats.norm.ppf(0.975)


def resumo(draws, nome: str | None = None, prob: float = 0.95) -> dict:
    """Mediana e intervalo de credibilidade de caudas iguais."""
    d = np.asarray(draws, dtype=float).ravel()
    a = (1 - prob) / 2
    out = {"mediana": float(np.median(d)), "média": float(d.mean()),
           "IC cred. inf.": float(np.quantile(d, a)), "IC cred. sup.": float(np.quantile(d, 1 - a))}
    if nome is not None:
        out = {"quantidade": nome, **out}
    return out


def _diagnosticos(idata, variaveis) -> dict:
    import arviz as az
    s = az.summary(idata, var_names=variaveis, kind="diagnostics")
    div = int(idata.sample_stats["diverging"].sum())
    return {"R-hat máximo": float(s["r_hat"].max()), "ESS bulk mínimo": float(s["ess_bulk"].min()),
            "ESS tail mínimo": float(s["ess_tail"].min()), "divergências": div,
            "sorteios": int(idata.posterior.sizes["chain"] * idata.posterior.sizes["draw"])}


# --------------------------------------------------------------------------------------------------------------
# MRP
# --------------------------------------------------------------------------------------------------------------
def mrp_prevalencia(amostra: pd.DataFrame, moldura: pd.DataFrame, resposta: str, *, seed: int,
                    draws: int = 1000, tune: int = 1500, chains: int = 4, target_accept: float = 0.95,
                    escala_jec: float = 0.5, escala_assunto: float = 1.5) -> dict:
    """Logito hierárquico + pós-estratificação na moldura.

    ``amostra``: colunas numero, ano, jec, assunto e ``resposta`` (0/1).
    ``moldura``: colunas numero, ano, jec, assunto (todos os N processos).

    Modelo: logit p = α + β_ano + u_jec + v_assunto; β_ano com soma zero ~ N(0, 1);
    u ~ N(0, σ_jec), v ~ N(0, σ_assunto), σ meia-normais. Assuntos da moldura que
    não aparecem na amostra recebem v sorteado da distribuição do grupo, isto é,
    a incerteza sobre assuntos nunca observados é propagada.

    O total na moldura soma os valores observados na amostra e sorteios
    binomiais para os N − n processos não sorteados (preditiva de população finita).
    """
    import pymc as pm

    am = amostra.copy()
    mo = moldura.copy()
    for df in (am, mo):
        df["assunto"] = df["assunto"].fillna("AUSENTE").astype(str)
        df["ano"] = df["ano"].astype(int)
        df["jec"] = df["jec"].astype(int)
    if not set(am["numero"]) <= set(mo["numero"]):
        raise ValueError("toda a amostra precisa pertencer à moldura")
    anos = sorted(mo["ano"].unique())
    jecs = sorted(mo["jec"].unique())
    assuntos = sorted(mo["assunto"].unique())
    ia = {a: i for i, a in enumerate(anos)}
    ij = {j: i for i, j in enumerate(jecs)}
    is_ = {s: i for i, s in enumerate(assuntos)}
    y = am[resposta].astype(int).to_numpy()
    xa, xj, xs = (am["ano"].map(ia).to_numpy(), am["jec"].map(ij).to_numpy(), am["assunto"].map(is_).to_numpy())

    with pm.Model() as modelo:
        alfa = pm.Normal("alfa", 0.0, 1.5)
        beta_ano = pm.ZeroSumNormal("beta_ano", sigma=1.0, shape=len(anos))
        s_jec = pm.HalfNormal("sigma_jec", escala_jec)
        s_ass = pm.HalfNormal("sigma_assunto", escala_assunto)
        z_jec = pm.Normal("z_jec", 0.0, 1.0, shape=len(jecs))
        z_ass = pm.Normal("z_assunto", 0.0, 1.0, shape=len(assuntos))
        u = pm.Deterministic("u_jec", s_jec * z_jec)
        v = pm.Deterministic("v_assunto", s_ass * z_ass)
        pm.Bernoulli("y", logit_p=alfa + beta_ano[xa] + u[xj] + v[xs], observed=y)
        idata = pm.sample(draws=draws, tune=tune, chains=chains, cores=chains, target_accept=target_accept,
                          random_seed=seed, progressbar=False, compute_convergence_checks=False)
    post = idata.posterior
    A = post["alfa"].values.reshape(-1)
    B = post["beta_ano"].values.reshape(len(A), -1)
    U = post["u_jec"].values.reshape(len(A), -1)
    Vv = post["v_assunto"].values.reshape(len(A), -1)

    # células da moldura entre os NÃO sorteados
    sorteado = mo["numero"].isin(set(am["numero"]))
    celulas = (mo.loc[~sorteado].groupby(["ano", "jec", "assunto"]).size().rename("N").reset_index())
    ca, cj, cs = (celulas["ano"].map(ia).to_numpy(), celulas["jec"].map(ij).to_numpy(),
                  celulas["assunto"].map(is_).to_numpy())
    eta = A[:, None] + B[:, ca] + U[:, cj] + Vv[:, cs]
    p_cel = expit(eta)
    rng = np.random.default_rng(seed)
    Y_ns = rng.binomial(celulas["N"].to_numpy()[None, :], p_cel)  # sorteios × células

    N = len(mo)
    total = y.sum() + Y_ns.sum(axis=1)

    def dominio(mask_cel: np.ndarray, mask_am: np.ndarray, N_dom: int) -> np.ndarray:
        return (y[mask_am].sum() + Y_ns[:, mask_cel].sum(axis=1)) / N_dom

    dom_jec = {}
    for j in jecs:
        dom_jec[j] = dominio(celulas["jec"].to_numpy() == j, am["jec"].to_numpy() == j, int((mo["jec"] == j).sum()))
    dom_ano = {a: dominio(celulas["ano"].to_numpy() == a, am["ano"].to_numpy() == a, int((mo["ano"] == a).sum()))
               for a in anos}
    dom_ass = {}
    for s in ("6226",):
        if s in is_:
            dom_ass[s] = dominio(celulas["assunto"].to_numpy() == s, am["assunto"].to_numpy() == s,
                                 int((mo["assunto"] == s).sum()))
    outros_cel = celulas["assunto"].to_numpy() != "6226"
    dom_ass["outros"] = dominio(outros_cel, am["assunto"].to_numpy() != "6226", int((mo["assunto"] != "6226").sum()))
    # efeito de cada assunto na escala de probabilidade (média dos anos e JEC)
    return {"idata": idata, "modelo": modelo, "prevalencia": total / N, "total": total, "N": N, "n": len(am),
            "jec": dom_jec, "ano": dom_ano, "assunto": dom_ass,
            "sigma_jec": post["sigma_jec"].values.ravel(), "sigma_assunto": post["sigma_assunto"].values.ravel(),
            "assuntos_na_amostra": int(am["assunto"].nunique()), "assuntos_na_moldura": len(assuntos),
            "diagnosticos": _diagnosticos(idata, ["alfa", "beta_ano", "sigma_jec", "sigma_assunto", "u_jec"])}


def pos_estratificado(y, grupo, N_grupo: dict, N: int) -> dict:
    """Estimador pós-estratificado (contraste de desenho) com variância condicional aos n_g.

    Aproxima a variância por Σ W_g² (1 − n_g/N_g) p_g (1 − p_g)/(n_g − 1).
    """
    y = np.asarray(y, dtype=float)
    grupo = np.asarray(grupo)
    p, v = 0.0, 0.0
    linhas = []
    for g, Ng in N_grupo.items():
        m = grupo == g
        ng = int(m.sum())
        pg = float(y[m].mean())
        W = Ng / N
        p += W * pg
        v += W ** 2 * (1 - ng / Ng) * pg * (1 - pg) / (ng - 1)
        linhas.append({"grupo": g, "N_g": Ng, "n_g": ng, "p_g": pg, "peso W_g": W})
    ep = float(np.sqrt(v))
    return {"p": p, "ep": ep, "ic": (p - Z95 * ep, p + Z95 * ep), "tabela": pd.DataFrame(linhas)}


# --------------------------------------------------------------------------------------------------------------
# Erro de classificação
# --------------------------------------------------------------------------------------------------------------
def prevalencia_com_erro(k: int, n: int, prior_se: tuple[float, float], prior_sp: tuple[float, float],
                         prior_pi: tuple[float, float] = (1.0, 1.0), *, seed: int, sorteios: int = 400_000,
                         reamostra: int = 40_000) -> dict:
    """Prevalência verdadeira π quando o rótulo tem Se e Sp incertas.

    P(rótulo = 1) = π·Se + (1 − π)(1 − Sp). Sem dados de validação, Se e Sp não são
    identificadas pelos dados: a posteriori delas fica igual à priori, e a de π
    herda essa incerteza. A integração é por amostragem-reamostragem por importância.
    """
    rng = np.random.default_rng(seed)
    pi = rng.beta(*prior_pi, sorteios)
    se = rng.beta(*prior_se, sorteios)
    sp = rng.beta(*prior_sp, sorteios)
    q = pi * se + (1 - pi) * (1 - sp)
    logw = stats.binom.logpmf(k, n, q)
    w = np.exp(logw - logw.max())
    w /= w.sum()
    ess = float(1 / np.sum(w ** 2))
    idx = rng.choice(sorteios, size=reamostra, replace=True, p=w)
    return {"pi": pi[idx], "se": se[idx], "sp": sp[idx], "ess_importancia": ess}


# --------------------------------------------------------------------------------------------------------------
# Bayes por processo
# --------------------------------------------------------------------------------------------------------------
def bayes_processo(cont_Ha: pd.Series, cont_H0: pd.Series, prior_pa: tuple[float, float], *, seed: int,
                   sorteios: int = 40_000, prior_dirichlet: float = 1.0) -> pd.DataFrame:
    """Posteriori P(Hₐ | D) com verossimilhanças e priori incertas.

    ``cont_Ha``/``cont_H0``: contagens das categorias de D (mesmo índice) em cada hipótese.
    P(D | H) ~ Dirichlet(prior + contagens): as categorias são tratadas em conjunto e
    somam um dentro de cada hipótese. P(Hₐ) ~ Beta(prior_pa).
    """
    cont_Ha = cont_Ha.astype(float)
    cont_H0 = cont_H0.reindex(cont_Ha.index).fillna(0).astype(float)
    rng = np.random.default_rng(seed)
    lA = rng.dirichlet(prior_dirichlet + cont_Ha.to_numpy(), sorteios)
    l0 = rng.dirichlet(prior_dirichlet + cont_H0.to_numpy(), sorteios)
    pa = rng.beta(*prior_pa, sorteios)
    linhas = []
    for j, cat in enumerate(cont_Ha.index):
        rv = lA[:, j] / l0[:, j]
        post = pa * lA[:, j] / (pa * lA[:, j] + (1 - pa) * l0[:, j])
        linhas.append({"dado": cat, "RV mediana": float(np.median(rv)),
                       "RV inf.": float(np.quantile(rv, .025)), "RV sup.": float(np.quantile(rv, .975)),
                       "P(RV > 1)": float((rv > 1).mean()),
                       "priori P(Hₐ) mediana": float(np.median(pa)),
                       "posteriori mediana": float(np.median(post)),
                       "posteriori inf.": float(np.quantile(post, .025)),
                       "posteriori sup.": float(np.quantile(post, .975))})
    return pd.DataFrame(linhas)


def bayes_assunto_temporal(k6226_Ha: int, nHa: int, k6226_H0: int, nH0: int, prior_pa: tuple[float, float],
                           *, seed: int, sorteios: int = 40_000) -> dict:
    """Razão de verossimilhança do assunto 6226 estimada num período e aplicada a outro.

    Verossimilhanças Beta(1 + k, 1 + n − k) e priori de prevalência Beta(prior_pa),
    ambas de 2022–2023; devolve P(Hₐ | 6226) e P(Hₐ | outro assunto) previstas para 2024.
    """
    rng = np.random.default_rng(seed)
    l6A = rng.beta(1 + k6226_Ha, 1 + nHa - k6226_Ha, sorteios)
    l60 = rng.beta(1 + k6226_H0, 1 + nH0 - k6226_H0, sorteios)
    pa = rng.beta(*prior_pa, sorteios)
    p6 = pa * l6A / (pa * l6A + (1 - pa) * l60)
    po = pa * (1 - l6A) / (pa * (1 - l6A) + (1 - pa) * (1 - l60))
    return {"RV_6226": l6A / l60, "RV_outros": (1 - l6A) / (1 - l60), "post_6226": p6, "post_outros": po}


# --------------------------------------------------------------------------------------------------------------
# Logística bayesiana
# --------------------------------------------------------------------------------------------------------------
def logistica_bayes(X: pd.DataFrame, y, *, seed: int, escala: float = 2.5, nu: float = 3.0,
                    draws: int = 1000, tune: int = 1500, chains: int = 4, target_accept: float = 0.95) -> dict:
    """Logística com prioris t de Student (ν = 3, escala 2,5) nos coeficientes.

    Preditores binários são centrados (média zero), como recomendam Gelman et al. (2008),
    para que a priori do intercepto se refira ao processo médio. Os coeficientes
    continuam na escala original de 0/1. Guarda a log-verossimilhança para o LOO.
    """
    import pymc as pm

    Xc = X.astype(float) - X.astype(float).mean()
    y = np.asarray(y, dtype=int)
    k = X.shape[1]
    with pm.Model(coords={"termo": list(X.columns)}) as modelo:
        a = pm.StudentT("intercepto_centrado", nu=nu, mu=0.0, sigma=10.0)
        if k:
            b = pm.StudentT("beta", nu=nu, mu=0.0, sigma=escala, dims="termo")
            eta = a + pm.math.dot(Xc.to_numpy(), b)
        else:  # modelo nulo, usado como referência no LOO
            eta = a * np.ones(len(y))
        pm.Bernoulli("y", logit_p=eta, observed=y)
        idata = pm.sample(draws=draws, tune=tune, chains=chains, cores=chains, target_accept=target_accept,
                          random_seed=seed, progressbar=False, compute_convergence_checks=False,
                          idata_kwargs={"log_likelihood": True})
    A0 = idata.posterior["intercepto_centrado"].values.ravel()
    Bd = idata.posterior["beta"].values.reshape(-1, k) if k else np.zeros((len(A0), 0))
    Ad = A0 - Bd @ X.astype(float).mean().to_numpy()
    tab = pd.DataFrame([{"termo": t, "OR mediana": float(np.exp(np.median(Bd[:, i]))),
                         "OR inf.": float(np.exp(np.quantile(Bd[:, i], .025))),
                         "OR sup.": float(np.exp(np.quantile(Bd[:, i], .975))),
                         "P(β > 0)": float((Bd[:, i] > 0).mean())} for i, t in enumerate(X.columns)])
    return {"idata": idata, "beta": Bd, "intercepto": Ad, "tabela": tab,
            "diagnosticos": _diagnosticos(idata, ["intercepto_centrado"] + (["beta"] if k else []))}


def prob_padroes(ajuste: dict, padroes: pd.DataFrame) -> np.ndarray:
    """Sorteios de P(y = 1 | padrão), um por linha de ``padroes`` (colunas na ordem do ajuste)."""
    eta = ajuste["intercepto"][:, None] + ajuste["beta"] @ padroes.astype(float).to_numpy().T
    return expit(eta)
