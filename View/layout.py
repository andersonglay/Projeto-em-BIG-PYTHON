import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Leia o CSV
df = pd.read_csv("unificada.csv")

# Crie a janela principal Tkinter
root = tk.Tk()
root.title("Análise de Preços e Serviços")

# Função para criar um gráfico simples
def plot_graph():
    fig, ax = plt.subplots(figsize=(5, 4))
    df['ColunaNumericaExemplo'].plot(kind='bar', ax=ax)
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Botão para exibir gráfico
btn_plot = ttk.Button(root, text="Mostrar Gráfico", command=plot_graph)
btn_plot.pack()

root.mainloop()