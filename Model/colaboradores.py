import pandas as pd
from datetime import datetime
<<<<<<< HEAD
import io

# --- Configuração e Leitura de Dados ---
ANO = datetime.now().year

try:
    # Tenta ler o arquivo CSV
    df_csv = pd.read_csv("dados/colaboradores.csv", encoding="utf-8-sig")
except FileNotFoundError:
    print("❌ ERRO: O arquivo 'dados/colaboradores.csv' não foi encontrado. Verifique o caminho.")
    exit()

# --------------------------------------------------
# CÓDIGO DE PROCESSAMENTO
# --------------------------------------------------

df = df_csv.copy()

# 🎯 CORREÇÃO: Renomear as colunas para os nomes que o MELT espera
df.rename(columns={
    # Coluna de Mês
    'Mês 2025': 'Mes', 
    
    # Coluna Lázaro
    'Lázaro': 'Lazaro', 
    
    # Coluna Conjunto
    'Conjunto (Leandro & Lázaro)': 'Conjunto' 
}, inplace=True)

# Verificação opcional:
# print("Colunas após renomeação:", df.columns.tolist()) 

# AGORA O MELT FUNCIONA com os nomes simplificados e corrigidos
df_long = df.melt(
    id_vars=['Mes'],
    value_vars=['Leandro', 'Lazaro', 'Conjunto'], # Usando os novos nomes
    var_name='Colaborador', 
    value_name='Atendimentos_Colaborador'
)

# ----------------------------------------------------------------------
# 📈 Restante do Código: Agrupamento e Exibição de Resultados
# ----------------------------------------------------------------------

# Agrupamento Mensal por Colaborador (Substitui 'mensal_semana')
mensal_colaborador = (df_long
    .groupby(["Mes", "Colaborador"])["Atendimentos_Colaborador"]
    .sum()
    .unstack("Colaborador", fill_value=0)
)

# Agrupamento Mensal Total (Substitui 'resample_mensal')
# Soma a coluna 'Atendimentos' (total do mês original)
resample_mensal = (df.groupby("Mes")["Atendimentos"]
    .sum()
)

# --- Exibição dos Resultados ---
print("\n## 📊 Análise de Atendimentos por Mês e Colaborador\n")
print(f"✅ Ano assumido para os registros: {ANO}")
print(f"✅ Dimensões do DataFrame original: {df_csv.shape}")

print("\n--- 📝 Resultado Mensal por Colaborador ---")
print("Total de atendimentos por colaborador em cada mês:")
print(mensal_colaborador)

print("\n--- 📈 Resultado Mensal Total de Atendimentos ---")
print("Total de atendimentos (todos) por Mês:")
print(resample_mensal)

print("\nProcessamento concluído com sucesso!")
print("\nPrimeiras linhas do DataFrame após renomeação:")
print(df.head(6).to_string())
=======

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
>>>>>>> bbe20b5a7d38ef6fa5834fce1cf1b1175f7a9906
