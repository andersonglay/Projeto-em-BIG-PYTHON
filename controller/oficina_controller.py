# controller/callbacks.py
from __future__ import annotations

from dash import Input, Output, dash_table, html
import plotly.express as px
import pandas as pd

# Mudar a importação para o novo modelo
from Model.oficina_model import MechanicWorkshopModel # Note a capitalização 'Model'


def register_callbacks(app, model: MechanicWorkshopModel) -> None:
    """Registra todos os callbacks da aplicação Dash."""

# --- Gráfico 1: Preço Médio por Tipo de Serviço ---
    @app.callback(
        Output("graph-avg-price-by-type", "figure"),
        [
            Input("service-type-dropdown", "value"),
            Input("month-dropdown", "value"),
        ],
    )
    def update_avg_price_graph(service_type, month):
        df = model.average_price_by_type(
            service_type=service_type,
            month=month,
        )

        if df.empty:
            return px.bar(title="Sem dados para os filtros selecionados.")

        # ESTA É A LINHA CRÍTICA QUE DEVE SER CORRIGIDA:
        fig = px.bar(
            df,
            x="Tipo",
            y="Preço_Médio",  # <--- CORREÇÃO AQUI: DEVE SER COM UNDERSCORE!
            title="Preço Médio do Serviço por Categoria",
            labels={"Tipo": "Tipo de Serviço", "Preço_Médio": "Preço Médio (R$)"},
            color="Tipo", 
            template="plotly_white",
        )
        fig.update_layout(margin=dict(l=40, r=20, t=60, b=40))
        return fig

    # --- Gráfico 2: Contagem de Serviços por Tipo ---
    @app.callback(
        Output("graph-count-by-type", "figure"),
        [
            Input("service-type-dropdown", "value"),
            Input("month-dropdown", "value"),
        ],
    )
    def update_count_graph(service_type, month):
        df = model.service_count_by_type(
            service_type=service_type,
            month=month,
        )

        if df.empty:
            return px.pie(title="Contagem de serviços não disponível para estes filtros.")

        fig = px.pie(
            df,
            names="Tipo",
            values="Contagem",
            title="Distribuição de Serviços por Categoria",
        )
        return fig

    # --- Gráfico 3: Heatmap Preço Médio por Tipo x Mês ---
    @app.callback(
        Output("graph-heatmap-price-by-month", "figure"),
        [
            Input("service-type-dropdown", "value"),
        ],
    )
    def update_heatmap(service_type):
        # CORREÇÃO: Usando o método correto do modelo (average_price_by_type_by_month)
        # O filtro de MÊS é desnecessário aqui, pois o gráfico mostra a distribuição MÊS x TIPO
        df_long = model.average_price_by_type_by_month(
            service_type=service_type,
        )

        if df_long.empty:
            return px.imshow(
                [[0]],
                labels=dict(x="Mês", y="Tipo de Serviço", color="Preço Médio"),
                title="Sem dados suficientes para o mapa de calor.",
            )
        
        # Plotando o Heatmap usando os dados no formato 'long' (tidy data)
        fig = px.density_heatmap(
            df_long,
            x="Mês",
            y="Tipo",
            z="Preço_Médio",
            title="Preço Médio do Serviço por Mês e Tipo",
            color_continuous_scale="Viridis",
            # CORREÇÃO: A chave no labels deve ser 'Preço_Médio'
            labels=dict(Mês="Mês do Serviço", Tipo="Tipo de Serviço", Preço_Médio="Preço Médio (R$)"),
        )
        
        fig.update_xaxes(side="top")
        return fig

    # --- Tabela de dados filtrados (Top 10 Serviços mais Caros) ---
    @app.callback(
        Output("table-container", "children"),
        [
            Input("service-type-dropdown", "value"),
            Input("month-dropdown", "value"),
        ],
    )
    def update_table(service_type, month):
        # CORREÇÃO: Usando o método correto do modelo (top_services_by_price)
        df = model.top_services_by_price(
            service_type=service_type,
            month=month,
            top_n=10
        )

        if df.empty:
            return html.P("Nenhum dado para os filtros selecionados.")

        # Prepara o DF para exibição (formata o preço)
        df_display = df.copy()
        # Coluna retornada pelo modelo é 'Preço_Unitário'
        df_display['Preço_Unitário'] = df_display['Preço_Unitário'].apply(lambda x: f"R$ {x:.2f}")

        return dash_table.DataTable(
            columns=[{"name": c, "id": c} for c in df_display.columns],
            data=df_display.to_dict("records"),
            page_size=10, 
            style_table={"overflowX": "auto"},
            style_header={
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold'
            },
            style_cell={
                'textAlign': 'left'
            }
        )