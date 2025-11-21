import pandas as pd

df = pd.read_csv("dados/pecas.csv", encoding="utf-8-sig")
print(df.columns.tolist())