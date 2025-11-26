# view/layout.py
from __future__ import annotations

from dash import dcc, html

# Alteração aqui: O nome do arquivo do modelo é 'oficina_model.py'
from model.oficina_model import MechanicWorkshopModel


def create_layout(model: MechanicWorkshopModel) -> html.Div:
    # 1. Obter os novos filtros
    service_types = model.get_available_service_types()
    months = model.get_available_months()
    
    return html.Div(
        [
            # Mudar título e descrição
            html.H1("Oficina Mecânica – Análise de Serviços e Preços 🛠️"),
            html.P(
                "Explore a distribuição e o preço médio dos serviços por tipo e mês de execução."
            ),
            html.Hr(),
            # --------- Filtros (Tipo de Serviço e Mês) ----------
            html.Div(
                [
                    # Filtro 1: Tipo de Serviço (Substitui Gênero)
                    html.Div(
                        [
                            html.Label("Tipo de Serviço"),
                            dcc.Dropdown(
                                id="service-type-dropdown",
                                options=[
                                    {"label": t, "value": t} for t in service_types
                                ],
                                value=None,
                                placeholder="Todos os Tipos",
                                clearable=True,
                            ),
                        ],
                        style={"width": "48%", "display": "inline-block"},
                    ),
                    # Filtro 2: Mês do Serviço (Substitui Duração)
                    html.Div(
                        [
                            html.Label("Mês do Serviço"),
                            dcc.Dropdown(
                                id="month-dropdown",
                                options=[{"label": m, "value": m} for m in months],
                                value=None,
                                placeholder="Todos os Meses",
                                clearable=True,
                            ),
                        ],
                        style={
                            "width": "48%",
                            "display": "inline-block",
                            "float": "right",
                        },
                    ),
                ],
                style={"marginBottom": "20px"},
            ),
            html.Hr(),
            # --------- Linha de gráficos principais ----------
            html.Div(
                [
                    # Gráfico 1: Média de Preço por Tipo
                    html.Div(
                        [dcc.Graph(id="graph-avg-price-by-type")],
                        style={"width": "48%", "display": "inline-block"},
                    ),
                    # Gráfico 2: Contagem por Tipo
                    html.Div(
                        [dcc.Graph(id="graph-count-by-type")],
                        style={
                            "width": "48%",
                            "display": "inline-block",
                            "float": "right",
                        },
                    ),
                ]
            ),
            # --------- Heatmap / Tabela de Preço Médio ----------
            html.Div(
                [
                    html.H3("Preço Médio por Tipo de Serviço × Mês"),
                    dcc.Graph(id="graph-heatmap-price-by-month"),
                ],
                style={"marginTop": "40px"},
            ),
            # --------- Tabela ----------
            html.Div(
                [
                    html.H3("Dados filtrados (Top 10 Serviços mais Caros)"),
                    dcc.Loading(
                        id="loading-table",
                        type="default",
                        children=html.Div(id="table-container"),
                    ),
                ],
                style={"marginTop": "40px"},
            ),
        ],
        style={"margin": "20px"},
    )