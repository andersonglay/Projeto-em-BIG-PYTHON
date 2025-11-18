from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence
import numpy as np
import pandas as pd
 
@dataclass
class Servico:
    """
    Camada de acesso e transformação dos dados de serviço da oficina.
    Esta classe é responsável por ler o CSV, limpar a coluna 'Preço'
    e criar novas colunas de análise (Data, Dia da Semana e Faixa de Custo).
    """
    csv_path: Path
    df: pd.DataFrame = None # Inicializa o DataFrame como None
 
    SERV_COLS: Sequence[str] = (
        "Dia",
        "Mês",
        "Serviço",
        "Preço",
        "Tipo",
    )
 
    def __post_init__(self) -> None:
        """Método chamado após a inicialização para carregar e processar o CSV."""
       
        # 1. Checagem de Arquivo
        if not self.csv_path.exists():
            raise FileNotFoundError(f"CSV não encontrado em: {self.csv_path}")
 
        # Leitura do CSV (usando separador ';')
        df = pd.read_csv(self.csv_path, sep=';', encoding='latin1')
 
        # 2. Limpeza de dados (removendo linhas sem Serviço)
        # O reset_index é para reorganizar o índice após a remoção
        df.dropna(subset=['Serviço'], inplace=True)
        df.reset_index(drop=True, inplace=True)
 
        # 3. Conversão da Data
        df['Data_Atendimento'] = pd.to_datetime(df['Dia'], format='%d/%m/%Y', errors='coerce')
 
        # 4. Limpeza e Conversão de Preço para Custo
        if 'Preço' in df.columns:
            # A) Limpeza do texto e conversão de vírgula para ponto
            df['Custo'] = (
                df['Preço']
                .astype(str)
                .str.replace('R$', '', regex=False)
                .str.replace(' ', '', regex=False) # Remove espaços em branco
                .str.replace('.', '', regex=False) # Remove separador de milhar
                .str.replace(',', '.', regex=False) # Substitui vírgula decimal por ponto
            )
            # B) Conversão final para numérico
            df['Custo'] = pd.to_numeric(df['Custo'], errors='coerce')
        else:
            # Se a coluna 'Preço' não existe
            df['Custo'] = np.nan
           
        # 5. Criação da coluna Dia_Semana
        # locale='pt_BR' garante os nomes dos dias em português
        df['Dia_Semana'] = df['Data_Atendimento'].dt.day_name(locale='pt_BR')
 
        # 6. Criação da coluna Faixa_Custo
        # Categoriza os custos em faixas (Baixo, Médio, Alto)
        if 'Custo' in df.columns:
            df['Faixa_Custo'] = pd.cut(
                df['Custo'],
                bins=[-float('inf'), 30.01, 80.01, float('inf')], # Faixas: <=30, 31-80, >80
                labels=["Custo Baixo", "Custo Médio", "Custo Alto"],
                right=True,
            )
        else:
            df['Faixa_Custo'] = np.nan
 
        self.df = df # Atribui o DataFrame processado ao atributo da classe
 
# Bloco de execução principal para gerar e imprimir o resultado
if __name__ == "__main__":
    # --- Configuração do caminho do arquivo ---
    # ASSUMA QUE O CSV ESTÁ NA MESMA PASTA DESTE SCRIPT
    NOME_DO_ARQUIVO = 'C:/Users/Moreira´s/OneDrive/Área de Trabalho/PYTHON-TRABALHO/servico.csv'
    csv_caminho = Path(NOME_DO_ARQUIVO)
 
    print(f"Tentando processar o arquivo: {NOME_DO_ARQUIVO}")
   
    try:
        # 1. Cria a instância (o processamento é executado automaticamente em __post_init__)
        servico_data = Servico(csv_path=csv_caminho)
 
        # 2. PRINTA O RESULTADO FINAL
       
        print("\n" + "="*50)
        print("RESULTADO FINAL: DATAFRAME PROCESSADO (10 Primeiras Linhas)")
        print("="*50)
       
        # Colunas que demonstram as transformações realizadas
        colunas_final = ['Dia', 'Serviço', 'Preço', 'Custo', 'Dia_Semana', 'Faixa_Custo', 'Tipo']
       
        # Imprime o DataFrame formatado como tabela
        # to_markdown é usado para uma visualização limpa no terminal
        print(servico_data.df[colunas_final].head(10).to_markdown(index=False))
 
        print("\n--- Estatísticas Resumidas ---")
        print(f"Total de Registros Processados: {len(servico_data.df)}")
        print(f"Custo Médio dos Serviços (R$): {servico_data.df['Custo'].mean():.2f}")
        print("-" * 30)
 
    except FileNotFoundError as e:
        print("\n" + "="*50)
        print("ERRO DE ARQUIVO")
        print("="*50)
        print(f"FALHA: O arquivo {NOME_DO_ARQUIVO} não foi encontrado.")
        print("Por favor, garanta que ele está na mesma pasta que este script Python.")
    except Exception as e:
        print(f"\nOcorreu um erro inesperado durante o processamento: {e}")
 