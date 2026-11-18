"""Análises de sensibilidade para a edição revisada do Estudo de Caso 3.

Funções puras para que o notebook exponha entradas, saídas e hipóteses dos
diagnósticos sem repetir a implementação em várias células.
"""
from __future__ import annotations

import itertools
import math

import numpy as np
import pandas as pd
from scipy.special import expit, logit
from scipy.stats import norm
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_mutual_info_score, adjusted_rand_score
from sklearn.preprocessing import OneHotEncoder
from kmodes.kmodes import KModes


def intervalo_logit_desenho(p: float, ep: float, z: float = norm.ppf(0.975)) -> tuple[float, float]:
    """IC assintótico na escala logito usando EP do estimador estratificado.

    O intervalo é baseado no desenho e fica em [0, 1]. Não é Wilson exato.
    """
    if not 0 < p < 1 or ep <= 0:
        raise ValueError("o intervalo logito requer 0 < p < 1 e EP > 0")
    margem = z * ep / (p * (1 - p))
    return float(expit(logit(p) - margem)), float(expit(logit(p) + margem))


def benchmark_agrupamentos(X_treino, X_teste, y_teste, pred_lca, *, seed: int = 2026):
    """Compara partições de três grupos em *casos de teste*, sem usar seus rótulos no ajuste.

    K-means recebe one-hot aprendida apenas no treino; k-modes recebe os códigos
    categóricos. ARI e AMI não dependem de ordenar ou renomear os grupos.
    """
    X_treino = np.asarray(X_treino, dtype=int)
    X_teste = np.asarray(X_teste, dtype=int)
    y_teste = np.asarray(y_teste, dtype=int)
    pred_lca = np.asarray(pred_lca, dtype=int)
    if X_treino.ndim != 2 or X_teste.shape[1] != X_treino.shape[1]:
        raise ValueError("treino e teste precisam ter as mesmas colunas")
    if len(y_teste) != len(X_teste) or len(pred_lca) != len(y_teste):
        raise ValueError("atribuições e rótulos precisam ter a extensão do teste")

    modos = KModes(n_clusters=3, init="Huang", n_init=20, random_state=seed)
    modos.fit(X_treino)
    pred_modos = modos.predict(X_teste)

    onehot = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    Z_treino = onehot.fit_transform(X_treino)
    Z_teste = onehot.transform(X_teste)
    medias = KMeans(n_clusters=3, n_init=30, random_state=seed)
    medias.fit(Z_treino)
    pred_medias = medias.predict(Z_teste)

    atribuicoes = {
        "LCA categórica": pred_lca,
        "k-modes categórico": pred_modos,
        "k-means em one-hot": pred_medias,
    }
    tabela = pd.DataFrame([
        {"método": nome, "ARI com rótulos existentes": adjusted_rand_score(y_teste, pred),
         "AMI com rótulos existentes": adjusted_mutual_info_score(y_teste, pred),
         "tamanhos dos grupos no teste": "/".join(map(str, sorted(np.bincount(pred, minlength=3)))),
         "n teste": len(y_teste)}
        for nome, pred in atribuicoes.items()
    ])
    concordancia = pd.DataFrame(
        {(a, b): adjusted_rand_score(atribuicoes[a], atribuicoes[b])
         for a, b in itertools.combinations(atribuicoes, 2)},
        index=["ARI entre métodos"]
    ).T.reset_index(names=["método A", "método B"])
    return tabela, concordancia, atribuicoes


def dependencia_local(X, modelo, nomes):
    """Resíduos de todas as marginais bivariadas sob independência local da LCA.

    O maior resíduo Pearson de cada par é diagnóstico descritivo; não é p-valor.
    """
    X = np.asarray(X, dtype=int)
    if X.shape[1] != len(nomes):
        raise ValueError("um nome para cada indicador")
    n = len(X)
    linhas = []
    for j, k in itertools.combinations(range(X.shape[1]), 2):
        cj, ck = modelo["ncat"][j], modelo["ncat"][k]
        obs = np.zeros((cj, ck), dtype=float)
        np.add.at(obs, (X[:, j], X[:, k]), 1)
        esp = n * np.einsum("q,qa,qb->ab", modelo["pi"], modelo["theta"][j], modelo["theta"][k])
        resid = (obs - esp) / np.sqrt(np.maximum(esp, 1e-12))
        ix = np.unravel_index(np.abs(resid).argmax(), resid.shape)
        linhas.append({"par": f"{nomes[j]} × {nomes[k]}",
                       "maior |resíduo|": float(np.abs(resid).max()),
                       "célula": f"{ix[0]}/{ix[1]}",
                       "observado": int(obs[ix]), "esperado": float(esp[ix])})
    return pd.DataFrame(linhas).sort_values("maior |resíduo|", ascending=False).reset_index(drop=True)


def simulacao_funil(estratos: pd.DataFrame, taxas: dict, *, repeticoes: int = 300,
                    seed: int = 2026, falso_positivo: float = 0.01,
                    falso_negativo: float = 0.10) -> pd.DataFrame:
    """Simula população finita, sorteio por ano e erro hipotético de classificação.

    ``taxas[ano]`` contém P(exclusão), P(algum F2 | elegível),
    P(indício | Fase III) e P(certeza | indício).
    """
    rng = np.random.default_rng(seed)
    N_total = int(estratos.N_h.sum())
    pesos = estratos.N_h / N_total
    resultados = []
    for _ in range(repeticoes):
        p_pop, p_am, p_erro = 0.0, 0.0, 0.0
        for ano, row in estratos.iterrows():
            N_h, n_h = int(row.N_h), int(row.n_h)
            t = taxas[int(ano)]
            excl = rng.random(N_h) < t[0]
            f2 = (~excl) & (rng.random(N_h) < t[1])
            ind = f2 & (rng.random(N_h) < t[2])
            # A certeza é simulada para completar o funil, ainda que o alvo
            # da comparação abaixo seja a prevalência de indício amplo.
            cert = ind & (rng.random(N_h) < t[3])
            assert not np.any(cert & ~ind)
            selecionados = rng.choice(N_h, n_h, replace=False)
            verdade = ind[selecionados]
            observado = np.where(verdade,
                                 rng.random(n_h) >= falso_negativo,
                                 rng.random(n_h) < falso_positivo)
            peso = float(pesos.loc[ano])
            p_pop += peso * ind.mean()
            p_am += peso * verdade.mean()
            p_erro += peso * observado.mean()
        resultados.append({"prevalência na população simulada": p_pop,
                           "estimativa estratificada sem erro": p_am,
                           "estimativa com erro hipotético": p_erro})
    return pd.DataFrame(resultados)
