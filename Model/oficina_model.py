from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Sequence

import pandas as pd


@dataclass
class MechanicWorkshopModel:
    """Camada de acesso e transformação dos dados de serviços da oficina."""

    csv_path: Path

    # Lista canônica dos meses em português (CLASSE/STATIC)
    MONTHS_ORDER = [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ]

    def _translate_month(self, month_name: str) -> str:
        """Traduz o nome do mês do inglês (padrão do strftime) para português."""
        translation_map = {
            'January': 'Janeiro', 'February': 'Fevereiro', 'March': 'Março', 
            'April': 'Abril', 'May': 'Maio', 'June': 'Junho',
            'July': 'Julho', 'August': 'Agosto', 'September': 'Setembro', 
            'October': 'Outubro', 'November': 'Novembro', 'December': 'Dezembro'
        }
        # Retorna o nome do mês traduzido.
        return translation_map.get(month_name, month_name)

    def __post_init__(self) -> None:
        if not self.csv_path.exists():
            raise FileNotFoundError(f"CSV não encontrado em: {self.csv_path}")

        df = pd.read_csv(self.csv_path)

        # 1. Filtrar apenas os registros de serviço diário (ignorando as linhas de resumo mensal)
        df = df[df["Serviço"].notna()].copy()

        # 2. Renomear colunas para clareza
        df = df.rename(columns={"Mês": "Mes_Servico"})

        # 3. Garantir tipos de dados corretos
        
        # Garantir numérico para o Preço
        if "Preço" in df.columns:
            df["Preço"] = pd.to_numeric(df["Preço"], errors="coerce")
        
        # Converter 'Dia' para datetime, criando uma coluna 'Mes_Servico_Text' para o nome do mês
        if "Dia" in df.columns:
            df["Dia"] = pd.to_datetime(df["Dia"], format="%d/%m/%Y", errors="coerce")
            
            # --- CORREÇÃO AQUI: Garante o nome do mês em português ---
            # 1. Obtém o nome do mês no locale padrão (geralmente inglês)
            df["Mes_Servico_Text"] = df["Dia"].dt.strftime("%B")
            # 2. Traduz para português usando a função auxiliar
            df["Mes_Servico_Text"] = df["Mes_Servico_Text"].apply(self._translate_month)
            # 3. Cria coluna com número do mês para ordenação interna
            df["Mes_Servico_Num"] = df["Dia"].dt.month
        else:
            df["Mes_Servico_Text"] = pd.NA
            df["Mes_Servico_Num"] = pd.NA

        self.df = df

    # ---------- Métodos de "consulta" para popular filtros ----------

    def get_available_service_types(self) -> list[str]:
        """Categorias de serviço (Tipo)."""
        if "Tipo" not in self.df.columns:
            return []
        return self.df["Tipo"].dropna().astype(str).sort_values().unique().tolist()

    def get_available_months(self) -> list[str]:
        """Retorna os meses disponíveis nos dados, na ordem correta."""
        
        if "Mes_Servico_Text" not in self.df.columns:
             return []
             
        # 1. Obtém os meses únicos presentes na coluna 'Mes_Servico_Text'
        available_months = self.df["Mes_Servico_Text"].unique().tolist()
        
        # 2. Ordena essa lista de meses únicos usando a ordem canônica
        sorted_months = [
            month for month in self.MONTHS_ORDER if month in available_months
        ]

        return sorted_months

    # ---------- Filtro base ----------

    def filter_data(
        self,
        service_type: Optional[str] = None,
        month: Optional[str] = None,
    ) -> pd.DataFrame:
        """Filtra os dados por tipo de serviço e mês."""
        df = self.df.copy()

        if service_type and "Tipo" in df.columns:
            df = df[df["Tipo"] == service_type]

        # CORREÇÃO: Utiliza a nova coluna de texto em português
        if month and "Mes_Servico_Text" in df.columns:
            df = df[df["Mes_Servico_Text"] == month]

        return df

    # ---------- Agregações para os gráficos ----------

    def average_price_by_type(
        self,
        service_type: Optional[str] = None,
        month: Optional[str] = None,
    ) -> pd.DataFrame:
        """Média de preço por Tipo de Serviço."""
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

    def service_count_by_type(
        self,
        service_type: Optional[str] = None,
        month: Optional[str] = None,
    ) -> pd.DataFrame:
        """Distribuição da contagem por Tipo de Serviço."""
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

    def top_services_by_price(
        self,
        service_type: Optional[str] = None,
        month: Optional[str] = None,
        top_n: int = 10,
    ) -> pd.DataFrame:
        """Lista os N serviços mais caros (por preço individual)."""
        df = self.filter_data(service_type, month)
        
        # Inclusão de colunas importantes para a tabela
        columns_to_include = ["Serviço", "Preço", "Tipo", "Mes_Servico_Text", "Dia"]
        
        # Verifica se todas as colunas necessárias estão presentes
        if not all(col in df.columns for col in ["Serviço", "Preço", "Tipo", "Mes_Servico_Text", "Dia"]):
            return pd.DataFrame()
        
        # Ordena e pega os N mais caros
        grouped = (
            df[columns_to_include]
            .sort_values("Preço", ascending=False)
            .head(top_n)
            .reset_index(drop=True)
        )
        return grouped.rename(columns={"Preço": "Preço_Unitário", "Mes_Servico_Text": "Mês"})

    def average_price_by_type_by_month(
        self,
        service_type: Optional[str] = None,
    ) -> pd.DataFrame:
        """Média de preço por Tipo de Serviço × Mês — pronto para virar heatmap."""
        df = self.filter_data(service_type=service_type, month=None)
        if "Mes_Servico_Text" not in df.columns or "Tipo" not in df.columns:
            return pd.DataFrame()

        # Garante a ordenação correta dos meses para o heatmap
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