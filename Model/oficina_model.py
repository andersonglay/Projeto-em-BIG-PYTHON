from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Sequence

import pandas as pd


@dataclass
class MechanicWorkshopModel:

    csv_path: Path
    
    MONTHS_ORDER = [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ]

# Tradução dos meses, pois estava conflitando
    def _translate_month(self, month_name: str) -> str:
        translation_map = {
            'January': 'Janeiro', 'February': 'Fevereiro', 'March': 'Março', 
            'April': 'Abril', 'May': 'Maio', 'June': 'Junho',
            'July': 'Julho', 'August': 'Agosto', 'September': 'Setembro', 
            'October': 'Outubro', 'November': 'Novembro', 'December': 'Dezembro'
        }
        return translation_map.get(month_name, month_name)

    def __post_init__(self) -> None:
        if not self.csv_path.exists():
            raise FileNotFoundError(f"CSV não encontrado em: {self.csv_path}")

        df = pd.read_csv(self.csv_path)

# Filtrar apenas os registros de serviço diário, ignorando resumo mensal
        df = df[df["Serviço"].notna()].copy()

# Renomear colunas para clareza
        df = df.rename(columns={"Mês": "Mes_Servico"})

# Ajustar os tipos de dados para as operações
        if "Preço" in df.columns:
            df["Preço"] = pd.to_numeric(df["Preço"], errors="coerce")
        
# Converter e identificar o dia do mês, traduzindo para português, pois estava conflitando
        if "Dia" in df.columns:
            df["Dia"] = pd.to_datetime(df["Dia"], format="%d/%m/%Y", errors="coerce")
            df["Mes_Servico_Text"] = df["Dia"].dt.strftime("%B")
            df["Mes_Servico_Text"] = df["Mes_Servico_Text"].apply(self._translate_month)
            df["Mes_Servico_Num"] = df["Dia"].dt.month
        else:
            df["Mes_Servico_Text"] = pd.NA
            df["Mes_Servico_Num"] = pd.NA
        self.df = df

# Criar métodos de consulta para os filtros, levando em consideração a categoria dos serviços
    def get_available_service_types(self) -> list[str]:
        if "Tipo" not in self.df.columns:
            return []
        return self.df["Tipo"].dropna().astype(str).sort_values().unique().tolist()

# Retornar cada um dos meses da planilha na ordem correta
    def get_available_months(self) -> list[str]:
        if "Mes_Servico_Text" not in self.df.columns:
            return []
        available_months = self.df["Mes_Servico_Text"].unique().tolist()
        sorted_months = [
            month for month in self.MONTHS_ORDER if month in available_months
        ]
        return sorted_months

### Filtro base por tipo de serviço e mês, traduzindo para português ###
    def filter_data(
        self,
        service_type: Optional[str] = None,
        month: Optional[str] = None,
    ) -> pd.DataFrame:
        df = self.df.copy()

        if service_type and "Tipo" in df.columns:
            df = df[df["Tipo"] == service_type]
            
        if month and "Mes_Servico_Text" in df.columns:
            df = df[df["Mes_Servico_Text"] == month]

        return df

### Preparação dos gráficos ###
# Preço por tipo de serviço
    def average_price_by_type(
        self,
        service_type: Optional[str] = None,
        month: Optional[str] = None,
    ) -> pd.DataFrame:
        df = self.filter_data(service_type, month)
        if "Tipo" not in df.columns or "Preço" not in df.columns:
            return pd.DataFrame()

        grouped = (
            df.groupby("Tipo")["Preço"]
            .mean()
            .reset_index()
            .sort_values("Preço", ascending=False)
        )
        return grouped.rename(columns={"Preço": "Preço_Médio"})

# Contagem por tipo de serviço
    def service_count_by_type(
        self,
        service_type: Optional[str] = None,
        month: Optional[str] = None,
    ) -> pd.DataFrame:
        df = self.filter_data(service_type, month)
        if "Tipo" not in df.columns:
            return pd.DataFrame()

        grouped = (
            df.groupby("Tipo")
            .size()
            .reset_index(name="Contagem")
            .sort_values("Contagem", ascending=False)
        )
        return grouped

# Listagem dos serviços mais caros
    def top_services_by_price(
        self,
        service_type: Optional[str] = None,
        month: Optional[str] = None,
        top_n: int = 10,
    ) -> pd.DataFrame:
        df = self.filter_data(service_type, month)
        
        # Colunas da tabela
        columns_to_include = ["Serviço", "Preço", "Tipo", "Mes_Servico_Text", "Dia"]
        if not all(col in df.columns for col in ["Serviço", "Preço", "Tipo", "Mes_Servico_Text", "Dia"]):
            return pd.DataFrame()
        
        # Ordena e retorna os mais caros
        grouped = (
            df[columns_to_include]
            .sort_values("Preço", ascending=False)
            .head(top_n)
            .reset_index(drop=True)
        )
        return grouped.rename(columns={"Preço": "Preço_Unitário", "Mes_Servico_Text": "Mês"})

# Média de preço por tipo de serviço de acordo com o mês
    def average_price_by_type_by_month(
        self,
        service_type: Optional[str] = None,
    ) -> pd.DataFrame:
        df = self.filter_data(service_type=service_type, month=None)
        if "Mes_Servico_Text" not in df.columns or "Tipo" not in df.columns:
            return pd.DataFrame()
        
        month_order = self.get_available_months()
        if month_order:
            df["Mes_Servico_Text"] = pd.Categorical(
                df["Mes_Servico_Text"], 
                categories=month_order, 
                ordered=True
            )

        grouped = (
            df.groupby(["Mes_Servico_Text", "Tipo"])["Preço"]
            .mean()
            .reset_index()
            .rename(columns={"Mes_Servico_Text": "Mês", "Preço": "Preço_Médio"})
            .sort_values(["Mês", "Tipo"])
        )
        return grouped