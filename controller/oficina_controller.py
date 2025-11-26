from __future__ import annotations

from dash import Input, Output, dash_table, html
import plotly.express as px
import pandas as pd

# Mudar a importação para o novo modelo
from Model.oficina_model import MechanicWorkshopModel # Note a capitalização 'Model'


def register_callbacks(app, model: MechanicWorkshopModel) -> None:
    """Registra todos os callbacks da aplicação Dash."""

    # --- Gráfico 1: Preço Médio por Tipo de Serviço ---
    # AGORA USA APENAS month-dropdown
    @app.callback(
        Output("graph-avg-price-by-type", "figure"),
        [
            # Input("service-type-dropdown", "value"), # REMOVIDO!
            Input("month-dropdown", "value"),
        ],
    )
    def update_avg_price_graph(month):
        # O argumento service_type foi removido da função e da chamada do modelo
        df = model.average_price_by_type(
            service_type=None, # Define o valor como None, já que o filtro foi removido
            month=month,
        )

        if df.empty:
            return px.bar(title="Sem dados para os filtros selecionados.")

        fig = px.bar(
            df,
            x="Tipo",
            y="Preço_Médio",
            title="Preço Médio do Serviço por Categoria",
            labels={"Tipo": "Tipo de Serviço", "Preço_Médio": "Preço Médio (R$)"},
            color="Tipo", 
            template="plotly_white",
        )
        fig.update_layout(margin=dict(l=40, r=20, t=60, b=40))
        return fig

    # --- Gráfico 2: Contagem de Serviços por Tipo ---
    # AGORA USA APENAS month-dropdown
    @app.callback(
        Output("graph-count-by-type", "figure"),
        [
            # Input("service-type-dropdown", "value"), # REMOVIDO!
            Input("month-dropdown", "value"),
        ],
    )
    def update_count_graph(month):
        # O argumento service_type foi removido da função e da chamada do modelo
        df = model.service_count_by_type(
            service_type=None, # Define o valor como None, já que o filtro foi removido
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
    # AGORA USA month-dropdown como Input para forçar a renderização inicial
    @app.callback(
        Output("graph-heatmap-price-by-month", "figure"),
        # Adicionamos um Input apenas para garantir que o callback seja executado no carregamento
        # O valor do mês será ignorado na função.
        [
            Input("month-dropdown", "value"), 
        ], 
    )
    def update_heatmap(month):
        # O argumento 'month' é aceito apenas para acionar o callback.
        # Ele é ignorado na chamada do modelo para que o heatmap mostre todos os meses (Tipo x Mês).
        
        # Obtém todos os dados, pois não há filtro de service_type na interface
        df_long = model.average_price_by_type_by_month(service_type=None)

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
            labels=dict(Mês="Mês do Serviço", Tipo="Tipo de Serviço", Preço_Médio="Preço Médio (R$)"),
        )
        
        fig.update_xaxes(side="top")
        return fig

    # --- Tabela de dados filtrados (Top 10 Serviços mais Caros) ---
    # AGORA USA APENAS month-dropdown
    @app.callback(
        Output("table-container", "children"),
        [
            # Input("service-type-dropdown", "value"), # REMOVIDO!
            Input("month-dropdown", "value"),
        ],
    )
    def update_table(month):
        # O argumento service_type foi removido da função e da chamada do modelo
        df = model.top_services_by_price(
            service_type=None, # Define o valor como None, já que o filtro foi removido
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