import pandas as pd
from datetime import datetime
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