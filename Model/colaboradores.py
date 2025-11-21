import pandas as pd
from datetime import datetime

ANO = datetime.now().year

# --- Leitura segura ---
try:
    df_csv = pd.read_csv("dados/colaboradores.csv", encoding="utf-8-sig")
except FileNotFoundError:
    print("ERRO: O arquivo 'dados/colaboradores.csv' não foi encontrado. Verifique o caminho.")
    exit()

# Remove colunas Unnamed
df_csv = df_csv.drop(columns=[col for col in df_csv.columns if "Unnamed:" in col], errors="ignore")

# Remove linhas totalmente vazias
df_csv = df_csv.dropna(how='all')

# Criar coluna ano
df_csv["Ano"] = ANO

# Criar a coluna Data_Completa usando o primeiro dia de cada mês
df_csv["Data_Completa"] = df_csv["Mes"] + " " + df_csv["Ano"].astype(str)

# Converter para datetime
df_csv["Data_Servico"] = pd.to_datetime(df_csv["Data_Completa"], format="%B %Y", errors="coerce")

# Exibir resultados
print("Processamento concluído com sucesso!")
print(f"Ano assumido para os registros: {ANO}")
print("\nDimensões do DataFrame:", df_csv.shape)
print("\nPrimeiras linhas:")
print(df_csv.head(20))