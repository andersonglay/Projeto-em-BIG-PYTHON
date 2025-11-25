# view/layout.py

from __future__ import annotations

import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(current_dir, '..')
sys.path.append(parent_dir)


from dash import dcc, html

from Model.colaboradores import colaboradores


def create_layout(model:colaboradores) -> html.Div:
    genders = model.get_available_genders()
    age_groups = model.get_available_age_groups()
    durations = model.get_available_durations()

    return html.Div(
        [
            html.H1("Finance Trends – Preferências de Investimento"),
            html.P(
                "Explore como as preferências de investimento variam por gênero, "
                "faixa etária e horizonte de tempo."
            ),
            # --------- Filtros ----------
            html.Div(
                [
                    html.Div(
                        [
                            html.Label("Gênero"),
                            dcc.Dropdown(
                                id="gender-dropdown",
                                options=[{"label": g, "value": g} for g in genders],
                                value=None,
                                placeholder="Todos",
                                clearable=True,
                            ),
                        ],
                        style={"width": "30%", "display": "inline-block"},
                    ),
                    html.Div(
                        [
                            html.Label("Faixa etária"),
                            dcc.Dropdown(
                                id="age-group-dropdown",
                                options=[
                                    {"label": ag, "value": ag} for ag in age_groups
                                ],
                                value=None,
                                placeholder="Todas",
                                clearable=True,
                            ),
                        ],
                        style={
                            "width": "30%",
                            "display": "inline-block",
                            "marginLeft": "2%",
                        },
                    ),
                    html.Div(
                        [
                            html.Label("Duração do investimento"),
                            dcc.Dropdown(
                                id="duration-dropdown",
                                options=[{"label": d, "value": d} for d in durations],
                                value=None,
                                placeholder="Todas",
                                clearable=True,
                            ),
                        ],
                        style={
                            "width": "30%",
                            "display": "inline-block",
                            "marginLeft": "2%",
                        },
                    ),
                ],
                style={"marginBottom": "20px"},
            ),
            html.Hr(),
            # --------- Linha de gráficos principais ----------
            html.Div(
                [
                    html.Div(
                        [dcc.Graph(id="graph-preferences")],
                        style={"width": "48%", "display": "inline-block"},
                    ),
                    html.Div(
                        [dcc.Graph(id="graph-factor")],
                        style={
                            "width": "48%",
                            "display": "inline-block",
                            "float": "right",
                        },
                    ),
                ]
            ),
            # --------- Heatmap / Duration ----------
            html.Div(
                [
                    html.H3("Preferências por produto × duração"),
                    dcc.Graph(id="graph-heatmap"),
                ],
                style={"marginTop": "40px"},
            ),
            # --------- Tabela ----------
            html.Div(
                [
                    html.H3("Dados filtrados"),
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