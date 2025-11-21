import pandas as pd
import numpy as np # Importação adicionada caso você queira criar dados de exemplo.

data = {
    'Data_Serviço_Serviço': pd.to_datetime(pd.date_range('2024-01-01', periods=50, freq='2D')),
    'valor': np.random.randint(100, 500, 50),

    'semana': np.random.choice(['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta'], 50)
}
df_csv = pd.DataFrame(data)

df = df_csv.copy()


df["Data_Serviço"] = pd.to_datetime(df["Data_Serviço_Serviço"])


mensal_semana = (df
    .groupby([pd.Grouper(key="Data_Serviço", freq="MS"), "semana"])["valor"]
    .sum()
    .unstack("semana", fill_value=0)
)

resample_mensal = (df.set_index("Data_Serviço")["valor"]
    .resample("MS").sum()
)

print("--- Resultado Mensal por Semana (Head 3) ---")
print(mensal_semana.head(3))
print("\n--- Resultado Mensal Total (Head 3) ---")
print(resample_mensal.head(3))