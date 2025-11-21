import pandas as pd
from datetime import datetime

ANO = datetime.now().year

try:
    df_csv = pd.read_csv("dados/pecas.csv", encoding="utf-8-sig")
except FileNotFoundError:
    print("ERRO: O arquivo 'dados/pecas.csv' não foi encontrado. Verifique o caminho.")
    exit()

print("Colunas originais:", df_csv.columns.tolist())

# Remover apenas colunas Unnamed
colunas_para_remover = [c for c in df_csv.columns if c.startswith("Unnamed")]
df_csv = df_csv.drop(columns=colunas_para_remover, errors='ignore')

# Se existir a coluna Dia, tratar
if 'Dia' in df_csv.columns:
    df_csv['Dia'] = pd.to_datetime(df_csv['Dia'], format='%d/%m/%Y', errors='coerce')
    df_csv['Data_Completa'] = df_csv['Dia'].dt.strftime('%d-%m-%Y')

# Só remover colunas que realmente existirem
colunas_para_excluir = ['Mês', 'Ano', 'Data_Completa']
colunas_existentes = [c for c in colunas_para_excluir if c in df_csv.columns]

df_csv = df_csv.drop(columns=colunas_existentes, errors='ignore')

# --- Exibição dos resultados ---
print("Processamento concluído com sucesso!")
print(f"Ano assumido para os registros: {ANO}")
print("\nDimensões do DataFrame:", df_csv.shape)
print("\nPrimeiras linhas:")
print(df_csv.head(10))