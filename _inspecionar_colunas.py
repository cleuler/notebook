import pandas as pd, numpy as np
from pathlib import Path

xlsx = Path("dat/estcaso_4JEC_natal/ControleDosProcessos_Mestrado_Atualizacao_07.10.2026.xlsx")
raw = pd.read_excel(xlsx, sheet_name="Processos", header=None)

# Linha 1 (índice 1) é o cabeçalho real
cabecalho = raw.iloc[1].fillna("").astype(str).str.strip()
dados = raw.iloc[2:].copy()
dados.columns = cabecalho
dados = dados.dropna(how="all").reset_index(drop=True)

print("Total de linhas:", len(dados))
print("\nColunas originais:")
for i, c in enumerate(dados.columns): print(f"  {i:2d}: {repr(c)}")

print("\nAmostras de valores por coluna:")
for c in dados.columns:
    vals = dados[c].dropna().unique()[:6]
    print(f"  {c[:40]:40s} => {vals}")

print("\nValores únicos de SORTEIO:")
print(dados.iloc[:,2].value_counts(dropna=False))

print("\nValores únicos de STATUS:")
print(dados.iloc[:,-1].value_counts(dropna=False))

print("\nValores únicos de SENTENÇA (col 7):")
print(dados.iloc[:,7].value_counts(dropna=False))

print("\nValores únicos de TÉCNICA (col 5):")
print(dados.iloc[:,5].value_counts(dropna=False))

print("\nDescrição das colunas numéricas (cols 9-12):")
num_cols = dados.iloc[:,9:13]
num_cols.columns = ["DURACAO-SENT2","DURACAO-TECN","DURACAO-SORT","DURACAO-PROC"]
for c in num_cols.columns:
    num_cols[c] = pd.to_numeric(num_cols[c], errors="coerce")
print(num_cols.describe(percentiles=[.25,.5,.75,.9,.95]).round(1))
