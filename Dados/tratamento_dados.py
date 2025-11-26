import pandas as pd
import glob

# Importar os arquivos csv
colaboradores_csv = glob.glob('dados/colaboradores.csv')
pecas_csv = glob.glob('dados/pecas.csv')
servico_csv = glob.glob('dados/servico.csv')

# Criar uma lista para armazenar os DataFrames
lista_dataframes = []

# Ler cada arquivo e adicioná-los à lista
for colaboradores in colaboradores_csv:
    df = pd.read_csv(colaboradores, encoding='utf-8')
    lista_dataframes.append(df)
    
for servico in servico_csv:
    df = pd.read_csv(servico, encoding='utf-8')
    lista_dataframes.append(df)
    
for colaboradores in colaboradores_csv:
    df = pd.read_csv(colaboradores, encoding='utf-8')
    lista_dataframes.append(df)

# 4. Concatenar todos os DataFrames em um único
df_unificado = pd.concat(lista_dataframes, ignore_index=True)

# 5. Salvar o DataFrame unificado em um novo arquivo CSV
df_unificado.to_csv('dados/planilha_unificada.csv', index=False)

print("As planilhas foram unificadas com sucesso em 'planilha_unificada.csv'")