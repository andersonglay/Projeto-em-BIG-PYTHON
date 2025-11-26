# app.py
from __future__ import annotations

import sys
from pathlib import Path
from dash import Dash

# --- Configuração de Caminho para Robustez ---
# Adiciona o diretório atual (raiz do projeto) ao caminho de busca do Python.
# Isso garante que as importações 'Model' e 'View' funcionem de forma confiável.
sys.path.append(str(Path(__file__).parent)) 
# ---------------------------------------------

# IMPORTAÇÕES ATUALIZADAS:
from controller.oficina_controller import register_callbacks
from Model.oficina_model import MechanicWorkshopModel # Importa do Model/oficina_model.py
from View.layout2 import create_layout                 # Importa do View/layout.py

# Nome do seu arquivo CSV, que está no mesmo nível do app.py
CSV_FILE_NAME = "dados/planilha_unificada.csv"


def create_app() -> Dash:
    
    # 1. Define o caminho do CSV
    csv_path = Path(CSV_FILE_NAME)

    # 2. Instancia o novo modelo
    model = MechanicWorkshopModel(csv_path=csv_path)

    # 3. Inicializa o app com o novo título
    app = Dash(
        __name__,
        title="Oficina Mecânica – Dashboard de Serviços",
    )

    # 4. Configura layout e callbacks
    app.layout = create_layout(model)
    # ATENÇÃO: O 'controller/callbacks.py' AINDA PRECISA SER ADAPTADO!
    register_callbacks(app, model)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)