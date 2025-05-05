import tkinter as tk
from interface import OrdemServicoApp
from visualizar_os import VisualizarOS

#tela hub principal

def abrir_os_joy():
    app = OrdemServicoApp()
    app.mainloop()

def abrir_visualizar_os():
    app = VisualizarOS()
    app.mainloop()

root = tk.Tk()
root.title("BrazaStore")
root.geometry("300x200")

root.iconbitmap("IMG\\iconeApp.ico")

btn_joy = tk.Button(root, text="Ordem de serviço", width=25, command=abrir_os_joy)
btn_joy.pack(pady=10)

btn_visualizar = tk.Button(root, text="Visualizar Ordens de Serviço", width=25, command=abrir_visualizar_os)
btn_visualizar.pack(pady=10)

root.mainloop()