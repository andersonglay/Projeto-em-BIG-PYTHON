from __future__ import annotations

import sys
from pathlib import Path
from dash import Dash

# Adicionar a pasta do app ao caminho de busca do Python
sys.path.append(str(Path(__file__).parent)) 

# Importações
from controller.oficina_controller import register_callbacks
from Model.oficina_model import MechanicWorkshopModel
from View.layout2 import create_layout

CSV_FILE_NAME = "dados/planilha_unificada.csv"

def create_app() -> Dash:
    
    # Definir o caminho do CSV
    csv_path = Path(CSV_FILE_NAME)

    # Instanciar
    model = MechanicWorkshopModel(csv_path=csv_path)

    # Inicializar
    app = Dash(
        __name__,
        title="Oficina Mecânica – Dashboard de Serviços",
    )

    # Layout da página
    app.layout = create_layout(model)
    
    register_callbacks(app, model)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)