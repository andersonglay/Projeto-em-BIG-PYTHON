from __future__ import annotations

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from dash import dcc, html

from Model.oficina_model import MechanicWorkshopModel


def create_layout(model: MechanicWorkshopModel) -> html.Div:
    
    service_types = model.get_available_service_types()
    months = model.get_available_months()
    
    return html.Div(
        [
           
            html.H1("Oficina Mecânica – Análise de Serviços e Preços 🛠️"),
            html.P(
                "Explore a distribuição e o preço médio dos serviços por tipo e mês de execução."
            ),
            html.Hr(),
            
            html.Div(
                [
                  
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
                            "width": "100%",
                            "display": "inline-block",
                            "float": "none", 
                        },
                    ),
                ],
                style={"marginBottom": "20px"},
            ),
            html.Hr(),
            ### Linha de gráficos principais 
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
            ###  Tabela de Preço Médio 
            html.Div(
                [
                    html.H3("Preço Médio por Tipo de Serviço × Mês"),
                    dcc.Graph(id="graph-heatmap-price-by-month"),
                ],
                style={"marginTop": "40px"},
            ),
            ### Tabela de Serviços mais Caros
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