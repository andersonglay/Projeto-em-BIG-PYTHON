from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence, Union
import numpy as np
import pandas as pd

@dataclass
class Servico:
    """
    Classe responsável por ler o CSV, limpar a coluna 'Preço'
    e criar novas colunas de análise.
    """
    csv_path: Union[Path, str]   # AGORA ACEITA URL!

    df: pd.DataFrame = None

    SERV_COLS: Sequence[str] = (
        "Dia",
        "Mês",
        "Serviço",
        "Preço",
        "Tipo",
    )

    def __post_init__(self) -> None:

        # Agora permite ler tanto local quanto URL
        if isinstance(self.csv_path, Path):
            if not self.csv_path.exists():
                raise FileNotFoundError(f"CSV não encontrado em: {self.csv_path}")
            df = pd.read_csv(self.csv_path, sep=';', encoding='latin1')

        else:
            # Leitura via URL do GitHub RAW
            df = pd.read_csv(self.csv_path, sep=';', encoding='latin1')

        df.dropna(subset=['Serviço'], inplace=True)
        df.reset_index(drop=True, inplace=True)

        df['Data_Atendimento'] = pd.to_datetime(df['Dia'], format='%d/%m/%Y', errors='coerce')

        if 'Preço' in df.columns:
            df['Custo'] = (
                df['Preço']
                .astype(str)
                .str.replace('R$', '', regex=False)
                .str.replace(' ', '', regex=False)
                .str.replace('.', '', regex=False)
                .str.replace(',', '.', regex=False)
            )
            df['Custo'] = pd.to_numeric(df['Custo'], errors='coerce')
        else:
            df['Custo'] = np.nan

        df['Dia_Semana'] = df['Data_Atendimento'].dt.day_name(locale='pt_BR')

        if 'Custo' in df.columns:
            df['Faixa_Custo'] = pd.cut(
                df['Custo'],
                bins=[-float('inf'), 30.01, 80.01, float('inf')],
                labels=["Custo Baixo", "Custo Médio", "Custo Alto"],
                right=True,
            )
        else:
            df['Faixa_Custo'] = np.nan

        self.df = df


if __name__ == "__main__":
    # URL RAW DO CSV NO GITHUB
    CSV_URL = "https://raw.githubusercontent.com/USUARIO/REPO/BRANCH/servico.csv"

    print(f"Tentando processar o arquivo remoto do GitHub...")

    try:
        servico_data = Servico(csv_path=CSV_URL)

        print("\n" + "="*50)
        print("RESULTADO FINAL: DATAFRAME PROCESSADO (10 Primeiras Linhas)")
        print("="*50)

        colunas_final = ['Dia', 'Serviço', 'Preço', 'Custo', 'Dia_Semana', 'Faixa_Custo', 'Tipo']

        print(servico_data.df[colunas_final].head(10).to_markdown(index=False))

        print("\n--- Estatísticas Resumidas ---")
        print(f"Total de Registros Processados: {len(servico_data.df)}")
        print(f"Custo Médio dos Serviços (R$): {servico_data.df['Custo'].mean():.2f}")
        print("-" * 30)

    except Exception as e:
        print(f"\nErro inesperado: {e}")