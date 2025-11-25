import pandas as pd
import numpy as np

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