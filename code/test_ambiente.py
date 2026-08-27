"""Verificacao automatizada da pilha analitica do projeto.

Rode com `uv run pytest`. Cada teste exercita de fato a biblioteca (nao apenas
o import), de modo que uma incompatibilidade entre versoes apareca aqui e nao
no meio de uma analise.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

RNG = np.random.default_rng(42)


@pytest.fixture(scope="module")
def dados() -> pd.DataFrame:
    n = 200
    return pd.DataFrame(
        {
            "x1": RNG.normal(size=n),
            "x2": RNG.normal(size=n),
            "grupo": RNG.choice(list("ABC"), n),
            "desfecho": RNG.integers(0, 2, n),
            "duracao": RNG.exponential(300, n),
            "evento": RNG.integers(0, 2, n),
        }
    )


def test_kernel_do_projeto() -> None:
    assert Path(sys.prefix).resolve().name == ".venv"


def test_leitura_e_escrita_de_planilhas(tmp_path: Path, dados: pd.DataFrame) -> None:
    xlsx = tmp_path / "t.xlsx"
    with pd.ExcelWriter(xlsx, engine="xlsxwriter") as writer:
        dados.to_excel(writer, sheet_name="dados", index=False)
    assert pd.read_excel(xlsx, engine="openpyxl").shape == dados.shape

    csv = tmp_path / "t.csv"
    dados.to_csv(csv, index=False, encoding="utf-8")
    assert pd.read_csv(csv).shape == dados.shape

    parquet = tmp_path / "t.parquet"
    dados.to_parquet(parquet)  # exige pyarrow
    assert pd.read_parquet(parquet).shape == dados.shape


def test_estatistica_inferencial(dados: pd.DataFrame) -> None:
    import pingouin as pg
    import scikit_posthocs as sp

    assert not pg.anova(data=dados, dv="x1", between="grupo").empty
    assert not pg.corr(dados["x1"], dados["x2"], method="spearman").empty
    assert sp.posthoc_dunn(dados, val_col="x1", group_col="grupo").shape == (3, 3)


def test_regressao_e_series_temporais(dados: pd.DataFrame) -> None:
    import statsmodels.api as sm
    import statsmodels.formula.api as smf

    logit = smf.logit("desfecho ~ x1 + x2 + C(grupo)", data=dados).fit(disp=0)
    assert np.isfinite(logit.prsquared)

    serie = pd.Series(
        RNG.poisson(20, 72),
        index=pd.date_range("2018-01-01", periods=72, freq="MS"),
    )
    assert sm.tsa.STL(serie, period=12).fit().trend.notna().all()
    assert sm.tsa.ARIMA(serie, order=(1, 0, 1)).fit().aic > 0


def test_analise_de_sobrevivencia(dados: pd.DataFrame) -> None:
    from lifelines import CoxPHFitter, KaplanMeierFitter

    km = KaplanMeierFitter().fit(dados["duracao"], dados["evento"])
    assert km.median_survival_time_ > 0

    cox = CoxPHFitter().fit(dados[["duracao", "evento", "x1", "x2"]], "duracao", "evento")
    assert 0 < cox.concordance_index_ < 1


def test_multivariada_categorica() -> None:
    import prince

    cat = pd.DataFrame({c: RNG.choice(list("AB"), 200) for c in ("v1", "v2", "v3")})
    mca = prince.MCA(n_components=2, random_state=42).fit(cat)
    assert mca.eigenvalues_.shape == (2,)


def test_machine_learning(dados: pd.DataFrame) -> None:
    import lightgbm as lgb
    import shap
    from sklearn.model_selection import StratifiedKFold, cross_val_score

    X, y = dados[["x1", "x2"]], dados["desfecho"]
    modelo = lgb.LGBMClassifier(n_estimators=20, verbose=-1)
    cv = StratifiedKFold(5, shuffle=True, random_state=42)
    assert len(cross_val_score(modelo, X, y, cv=cv, scoring="roc_auc")) == 5

    valores = shap.TreeExplainer(modelo.fit(X, y)).shap_values(X)
    assert np.asarray(valores).shape[0] == len(X)


def test_validacao_de_esquema(dados: pd.DataFrame) -> None:
    import pandera.pandas as pa

    esquema = pa.DataFrameSchema(
        {
            "x1": pa.Column(float, nullable=False),
            "desfecho": pa.Column(int, pa.Check.isin([0, 1])),
            "grupo": pa.Column(str, pa.Check.isin(["A", "B", "C"])),
        }
    )
    assert esquema.validate(dados).shape == dados.shape


def test_nlp_portugues() -> None:
    import spacy

    nlp = spacy.load("pt_core_news_sm")
    doc = nlp("O Ministerio Publico de Goias ajuizou acao civil publica em Anapolis.")
    assert [t.lemma_ for t in doc]
    assert doc.ents


def test_pareamento_de_texto() -> None:
    from rapidfuzz import process
    from unidecode import unidecode

    municipios = ["Anápolis", "Aparecida de Goiânia", "Sanclerlândia"]

    def normalizar(texto: str) -> str:
        return unidecode(texto).casefold()

    achado, score, _ = process.extractOne("aparecida de goiania", municipios, processor=normalizar)
    assert achado == "Aparecida de Goiânia" and score > 90


def test_graficos_sem_display(tmp_path: Path, dados: pd.DataFrame) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import missingno as msno
    import seaborn as sns

    sns.histplot(dados["x1"])
    plt.savefig(tmp_path / "hist.png")
    plt.close("all")

    msno.matrix(dados)
    plt.close("all")

    import plotly.express as px

    assert px.scatter(dados, x="x1", y="x2", color="grupo") is not None
