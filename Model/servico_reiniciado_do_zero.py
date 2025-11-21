import pandas as pd
from datetime import datetime
ANO = datetime.now().year
try:
    df_csv = pd.read_csv("dados/servico.csv",encoding="utf-8-sig" )
except FileNotFoundError:
    print("ERRO: O arquivo 'Dados/servico.csv' não foi encontrado. Verifique o caminho.")
    exit()

colunas_para_remover = [col for col in df_csv.columns if 'Unnamed:' in col]
df_csv = df_csv.drop(columns=colunas_para_remover, errors='ignore')

df_csv['Ano'] = ANO

df_csv['Data_Completa'] = (df_csv['Dia'].astype(str) + '-' + df_csv['Mês'].astype(str) + '-' + df_csv['Ano'].astype(str))

# --- Conversão para Datetime com Formato Específico ---
df_csv['Data_Servico'] = pd.to_datetime(df_csv['Data_Completa'],format='%d-%m-%Y',errors='coerce')

df_csv = df_csv.drop(columns=['Dia', 'Mês', 'Ano', 'Data_Completa'], errors='ignore')


# --- Exibição dos Resultados ---
print("Processamento concluído com sucesso!")
print(f"Data assumida para os registros: {ANO}")
print("\nDimensões do DataFrame:", df_csv.shape)
print("\nPrimeiras 5 linhas (com a nova coluna 'Data_Servico'):")
print(df_csv.head(300))