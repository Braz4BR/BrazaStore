import tkinter as tk
from tkinter import ttk
import os
from datetime import datetime
import subprocess
import sys

class VisualizarOS(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ordens de Serviço")
        self.geometry("600x500")
        self.ordem_decrescente = True
        self.criar_widgets()

    def criar_widgets(self):
        self.btn_ordenar = ttk.Button(self, text="Ordenar por data (Mais recentes)", command=self.alternar_ordem)
        self.btn_ordenar.pack(pady=(10, 0))

        ttk.Label(self, text="Ordens de Serviço", font=("Arial", 10, "bold")).pack(pady=(10, 0))
        self.lista_braza = tk.Listbox(self, width=80, height=10)
        self.lista_braza.pack(padx=10, pady=5)

        btn_voltar = ttk.Button(self, text="Voltar", command=self.voltar)
        btn_voltar.pack(pady=10)

        self.lista_braza.bind("<Double-Button-1>", lambda e: self.abrir_pdf(self.lista_braza, "pdf"))

        self.preencher_listas()

    def alternar_ordem(self):
        self.ordem_decrescente = not self.ordem_decrescente
        texto = "Ordenar por data (Mais recentes)" if self.ordem_decrescente else "Ordenar por data (Mais antigas)"
        self.btn_ordenar.config(text=texto)
        self.preencher_listas()

    def preencher_listas(self):
        self.lista_braza.delete(0, tk.END)
        self.preencher_lista_por_pasta("pdf", self.lista_braza)

    def preencher_lista_por_pasta(self, pasta, lista):
        if not os.path.exists(pasta):
            return

        arquivos = []
        for nome in os.listdir(pasta):
            if nome.endswith(".pdf"):
                caminho = os.path.join(pasta, nome)
                data = os.path.getmtime(caminho)
                arquivos.append((nome, data))

        arquivos.sort(key=lambda x: x[1], reverse=self.ordem_decrescente)

        for nome, data in arquivos:
            data_str = datetime.fromtimestamp(data).strftime("%d/%m/%Y %H:%M")
            exibicao = f"{nome} - {data_str}"
            lista.insert(tk.END, exibicao)

    def abrir_pdf(self, lista, pasta):
        selecionado = lista.curselection()
        if not selecionado:
            return
        nome_arquivo = lista.get(selecionado[0]).split(" - ")[0]
        caminho = os.path.join(pasta, nome_arquivo)

        if sys.platform == "win32":
            os.startfile(caminho)
        else:
            subprocess.call(["open" if sys.platform == "darwin" else "xdg-open", caminho])

    def voltar(self):
        self.destroy()

if __name__ == "__main__":
    app = VisualizarOS()
    app.mainloop()