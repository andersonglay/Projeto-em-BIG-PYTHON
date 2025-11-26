# controller/callbacks.py
from __future__ import annotations

from dash import Input, Output, dash_table, html
import plotly.express as px
import pandas as pd

# Mudar a importação para o novo modelo
from Model.oficina_model import MechanicWorkshopModel # Note a capitalização 'Model'


# Os IDs dos filtros são:
# Input("service-type-dropdown", "value") -> Tipo de Serviço
# Input("month-dropdown", "value") -> Mês do Serviço

# Os IDs dos outputs são:
# Output("graph-avg-price-by-type", "figure")
# Output("graph-count-by-type", "figure")
# Output("graph-heatmap-price-by-month", "figure")
# Output("table-container", "children")


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
        # Novo método no modelo
        df = model.average_price_by_type(
            service_type=service_type,
            month=month,
        )

        if df.empty:
            return px.bar(title="Sem dados para os filtros selecionados.")

        # Criação do gráfico de barras para preço médio
        fig = px.bar(
            df,
            x="Tipo",
            y="Preço Médio",
            title="Preço Médio do Serviço por Categoria",
            labels={"Tipo": "Tipo de Serviço", "Preço Médio": "Preço Médio (R$)"},
            color="Tipo", # Colore por tipo
            template="plotly_white", # Estilo
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
        # Novo método no modelo
        df = model.service_count_by_type(
            service_type=service_type,
            month=month,
        )

        if df.empty:
            return px.pie(title="Contagem de serviços não disponível para estes filtros.")

        # Criação do gráfico de pizza para a contagem
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
            Input("month-dropdown", "value"),
        ],
    )
    def update_heatmap(service_type, month):
        # O heatmap usará o método do modelo para a tabela pivot/heatmap
        # ATENÇÃO: Se o modelo retornar o DF no formato pivot, os rótulos X e Y devem ser ajustados.
        df_heatmap = model.heatmap_price_by_month(
            service_type=service_type,
            month=month,
        )

        if df_heatmap.empty:
            return px.imshow(
                [[0]],
                labels=dict(x="Tipo de Serviço", y="Mês", color="Preço Médio"),
                title="Sem dados suficientes para o mapa de calor.",
            )
        
        # A função model.heatmap_price_by_month deve retornar um DataFrame pronto para o heatmap
        # (index=Tipo, columns=Mês, values=Preço Médio)

        # Plotly Express heatmap/imshow
        fig = px.imshow(
            df_heatmap,
            x=df_heatmap.columns.tolist(), # Meses
            y=df_heatmap.index.tolist(),   # Tipos
            color_continuous_scale="Viridis",
            labels=dict(x="Mês do Serviço", y="Tipo de Serviço", color="Preço Médio (R$)"),
            title="Preço Médio do Serviço por Mês e Tipo",
        )
        
        # Adiciona rótulos de texto nas células para melhor leitura (opcional, mas útil)
        for i in range(len(df_heatmap.index)):
            for j in range(len(df_heatmap.columns)):
                fig.add_annotation(
                    x=df_heatmap.columns[j],
                    y=df_heatmap.index[i],
                    text=f"R$ {df_heatmap.iloc[i, j]:.0f}",
                    showarrow=False,
                    font=dict(color="white" if df_heatmap.iloc[i, j] > df_heatmap.values.mean() else "black", size=10)
                )

        fig.update_xaxes(side="top")
        return fig

    # --- Tabela de dados filtrados ---
    @app.callback(
        Output("table-container", "children"),
        [
            Input("service-type-dropdown", "value"),
            Input("month-dropdown", "value"),
        ],
    )
    def update_table(service_type, month):
        # Novo método no modelo: Tabela dos 10 serviços mais caros
        df = model.top_expensive_services(
            service_type=service_type,
            month=month,
        )

        if df.empty:
            return html.P("Nenhum dado para os filtros selecionados.")

        # Formata a coluna Preço para ser exibida corretamente
        # (Fazendo uma cópia para evitar SettingWithCopyWarning)
        df_display = df[['Serviço', 'Preço', 'Tipo', 'Mês', 'Dia']].copy()
        df_display['Preço'] = df_display['Preço'].apply(lambda x: f"R$ {x:.2f}")

        return dash_table.DataTable(
            columns=[{"name": c, "id": c} for c in df_display.columns],
            data=df_display.to_dict("records"),
            page_size=10, # Limitar a 10 linhas, pois é o Top 10
            style_table={"overflowX": "auto"},
            style_header={
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold'
            },
            style_cell={
                'textAlign': 'left'
            }
        )