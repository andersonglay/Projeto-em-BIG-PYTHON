import pandas as pd
from datetime import datetime
import io

# --- Configuração e Leitura de Dados ---
ANO = datetime.now().year

try:
    # Tenta ler o arquivo CSV
    # O encoding "utf-8-sig" é bom para lidar com arquivos que vêm do Excel com BOM
    df_csv = pd.read_csv("dados/colaboradores.csv", encoding="utf-8-sig")
except FileNotFoundError:
    print("❌ ERRO: O arquivo 'dados/colaboradores.csv' não foi encontrado. Verifique o caminho.")
    exit()

# --------------------------------------------------
# CÓDIGO DE PROCESSAMENTO
# --------------------------------------------------

df = df_csv.copy()

# 🎯 CORREÇÃO: Renomear as colunas
# Garantindo que os nomes no MELT sejam usados após a renomeação.
df.rename(columns={
    # Coluna de Mês (Assumindo que você quer mudar 'Mês 2025' para 'Mes')
    'Mês 2025': 'Mes', 
    
    # Coluna Lázaro (Simplificação de nome, se necessário)
    'Lázaro': 'Lazaro', 
    
    # Coluna Conjunto (Simplificação de nome, se necessário)
    'Conjunto (Leandro & Lázaro)': 'Conjunto' 
    
    # Adicione aqui outras colunas que precisam de renomeação, por exemplo:
    # 'Nome Original do Leandro': 'Leandro',
}, inplace=True)

# Verificação das Colunas: 
# É crucial que as colunas 'Leandro', 'Lazaro', e 'Conjunto' estejam agora no DataFrame.
if 'Leandro' not in df.columns:
    # Se 'Leandro' não foi renomeado, mas é uma coluna, adicione a renomeação
    # Exemplo: df.rename(columns={'Nome Real do Leandro': 'Leandro'}, inplace=True)
    # Se 'Leandro' JÁ é o nome, o bloco de renomeação está ok.
    pass

# AGORA O MELT DEVE FUNCIONAR
df_long = df.melt(
    id_vars=['Mes'],
    # A lista value_vars deve conter os nomes das colunas de atendimentos (após a renomeação)
    value_vars=['Leandro', 'Lazaro', 'Conjunto'], 
    var_name='Colaborador', 
    value_name='Atendimentos_Colaborador'
)

# ----------------------------------------------------------------------
# 📈 Restante do Código: Agrupamento e Exibição de Resultados
# ----------------------------------------------------------------------

# Agrupamento Mensal por Colaborador
mensal_colaborador = (df_long
    .groupby(["Mes", "Colaborador"])["Atendimentos_Colaborador"]
    .sum()
    .unstack("Colaborador", fill_value=0)
)

# Agrupamento Mensal Total 
# Requer que a coluna 'Atendimentos' esteja presente no DataFrame original (df).
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