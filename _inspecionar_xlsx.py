import pandas as pd
from pathlib import Path

xlsx = Path("dat/estcaso_4JEC_natal/ControleDosProcessos_Mestrado_Atualizacao_07.10.2026.xlsx")
xl = pd.ExcelFile(xlsx)
print("Abas:", xl.sheet_names)

for sh in xl.sheet_names:
    df = pd.read_excel(xlsx, sheet_name=sh, header=None, nrows=12)
    print(f"\n{'='*60}\nAba: {sh}\n{'='*60}")
    print(df.to_string())
