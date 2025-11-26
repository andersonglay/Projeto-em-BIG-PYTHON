import pandas as pd
import numpy as np
from datetime import datetime
ANO = datetime.now().year

try:
    df_csv = pd.read_csv("dados/unificada.csv", encoding="utf-8-sig")
except FileNotFoundError:
    print("ERRO: O arquivo 'dados/unificada.csv' não foi encontrado. Verifique o caminho.")
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


try:
    df_csv = pd.read_csv("dados/unificada.csv", encoding="utf-8-sig")
except FileNotFoundError:
    print("ERRO: O arquivo 'dados/unificada.csv' não foi encontrado. Verifique o caminho.")
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

try:
    df_csv = pd.read_csv("dados/unificada.csv",encoding="utf-8-sig" )
except FileNotFoundError:
    print("ERRO: O arquivo 'Dados/unificada.csv' não foi encontrado. Verifique o caminho.")
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
# Seus dados de exemplo (mantidos para que o código seja executável)
data = {
    'Data_Serviço_Serviço': pd.to_datetime(pd.date_range('2024-01-01', periods=50, freq='2D')),
    'valor': np.random.randint(100, 500, 50),
    'semana': np.random.choice(['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta'], 50)
}
df_csv = pd.DataFrame(data)

df = df_csv.copy()

# Preparação do DataFrame
df["Data_Serviço"] = pd.to_datetime(df["Data_Serviço_Serviço"])

# --- CÁLCULO ORIGINAL: SOMA E UNSTACK (Agrupamento por Mês e Semana) ---
mensal_semana = (df
    .groupby([pd.Grouper(key="Data_Serviço", freq="MS"), "semana"])["valor"]
    .sum()
    .unstack("semana", fill_value=0)
)

# --- NOVO CÁLCULO: MÉDIA E UNSTACK (Agrupamento por Mês e Semana) ---
media_mensal_semana = (df
    .groupby([pd.Grouper(key="Data_Serviço", freq="MS"), "semana"])["valor"]
    .mean() # Alteração de .sum() para .mean()
    .unstack("semana", fill_value=0)
)

# --- CÁLCULO ORIGINAL: SOMA (Resample Mensal Total) ---
resample_mensal = (df.set_index("Data_Serviço")["valor"]
    .resample("MS").sum()
)

# --- NOVO CÁLCULO: MÉDIA (Resample Mensal Total) ---
media_resample_mensal = (df.set_index("Data_Serviço")["valor"]
    .resample("MS").mean() # Alteração de .sum() para .mean()
)

print("--- 1. Soma Mensal por Semana (Head 3) ---")
print(mensal_semana.head(3))

print("\n--- 2. MÉDIA Mensal por Semana (Head 3) ---")
print(media_mensal_semana.head(3))

print("\n--- 3. Soma Mensal Total (Head 3) ---")
print(resample_mensal.head(3))

print("\n--- 4. MÉDIA Mensal Total (Head 3) ---")
print(media_resample_mensal.head(3))