import pandas as pd
from datetime import datetime
ANO = datetime.now().year
try:
    df_csv = pd.read_csv("dados/pecas.csv",encoding="utf-8-sig" )
except FileNotFoundError:
    print("ERRO: O arquivo 'dados/pecas.csv' não foi encontrado. Verifique o caminho.")
    exit()

colunas_para_remover = [col for col in df_csv.columns if 'Unnamed:' in col]
df_csv = df_csv.drop(columns=colunas_para_remover, errors='ignore')

df_csv['Ano'] = ANO

df_csv['Dia'] = pd.to_datetime(df_csv['Dia'], format='%d/%m/%Y', errors='coerce')

df_csv['Data_Completa'] = df_csv['Dia'].dt.strftime('%d-%m-%Y')

df_csv = df_csv.drop(columns=['Dia', 'Mês', 'Ano', 'Data_Completa'], errors='ignore')


# --- Exibição dos Resultados ---
print("Processamento concluído com sucesso!")
print(f"Dia assumida para os registros: {ANO}")
print("\nDimensões do DataFrame:", df_csv.shape)
print("\nPrimeiras 5 linhas (com a nova coluna 'Data_Reposicao'):")
print(df_csv.head(300))