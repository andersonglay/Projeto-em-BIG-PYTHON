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

mensal_semana.head(3), resample_mensal.head(3)