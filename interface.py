import tkinter as tk
from tkinter import ttk, messagebox
from gerar_pdf import gerar_ordem_servico  # Certifique-se que gerar_pdf.py está correto

class OrdemServicoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ordem de Serviço - BrazaStore")
        self.geometry("700x600")

        self.pecas_servicos = []

        self.criar_campos_cliente_produto()
        self.criar_campos_pecas()
        self.criar_botoes()

    def criar_campos_cliente_produto(self):
        # Campos do cliente
        ttk.Label(self, text="Nome:").grid(row=0, column=0, sticky="e")
        self.entry_nome = ttk.Entry(self, width=50)
        self.entry_nome.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self, text="Telefones (vírgula):").grid(row=1, column=0, sticky="e")
        self.entry_telefones = ttk.Entry(self, width=50)
        self.entry_telefones.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self, text="Endereço:").grid(row=2, column=0, sticky="e")
        self.entry_endereco = ttk.Entry(self, width=50)
        self.entry_endereco.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self, text="CNPJ (opcional):").grid(row=3, column=0, sticky="e")
        self.entry_cnpj = ttk.Entry(self, width=50)
        self.entry_cnpj.grid(row=3, column=1, padx=5, pady=5)

        # Equipamento (obrigatório)
        ttk.Label(self, text="Equipamento:").grid(row=4, column=0, sticky="e")
        self.entry_equipamento = ttk.Entry(self, width=50)
        self.entry_equipamento.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(self, text="Modelo (opcional):").grid(row=5, column=0, sticky="e")
        self.entry_modelo = ttk.Entry(self, width=50)
        self.entry_modelo.grid(row=5, column=1, padx=5, pady=5)

        ttk.Label(self, text="Marca (opcional):").grid(row=6, column=0, sticky="e")
        self.entry_marca = ttk.Entry(self, width=50)
        self.entry_marca.grid(row=6, column=1, padx=5, pady=5)

        ttk.Label(self, text="Defeito:").grid(row=7, column=0, sticky="e")
        self.entry_defeito = ttk.Entry(self, width=50)
        self.entry_defeito.grid(row=7, column=1, padx=5, pady=5)

        ttk.Label(self, text="Laudo Técnico:").grid(row=8, column=0, sticky="ne")
        self.txt_laudo = tk.Text(self, width=38, height=4)
        self.txt_laudo.grid(row=8, column=1, padx=5, pady=5)

    def criar_campos_pecas(self):
        ttk.Label(self, text="Peça/Serviço:").grid(row=9, column=0, sticky="e")
        self.entry_peca = ttk.Entry(self, width=30)
        self.entry_peca.grid(row=9, column=1, sticky="w")

        ttk.Label(self, text="Quantidade:").grid(row=10, column=0, sticky="e")
        self.entry_qtd = ttk.Entry(self, width=10)
        self.entry_qtd.grid(row=10, column=1, sticky="w")

        ttk.Label(self, text="Valor Unitário:").grid(row=11, column=0, sticky="e")
        self.entry_valor = ttk.Entry(self, width=10)
        self.entry_valor.grid(row=11, column=1, sticky="w")

        self.btn_adicionar = ttk.Button(self, text="Adicionar Item", command=self.adicionar_item)
        self.btn_adicionar.grid(row=12, column=1, pady=5, sticky="w")

    # Scrollable Listbox
        frame_lista = tk.Frame(self)
        frame_lista.grid(row=13, column=0, columnspan=2, padx=5, pady=5)

        scrollbar = tk.Scrollbar(frame_lista)
        scrollbar.pack(side="right", fill="y")

        self.lista_itens = tk.Listbox(frame_lista, width=60, height=6, yscrollcommand=scrollbar.set)
        self.lista_itens.pack(side="left", fill="both")
        scrollbar.config(command=self.lista_itens.yview)

        # Botão de remover item
        self.btn_remover = ttk.Button(self, text="Remover Selecionado", command=self.remover_item)
        self.btn_remover.grid(row=14, column=1, sticky="w")

    def remover_item(self):
        selecionado = self.lista_itens.curselection()
        if selecionado:
            index = selecionado[0]
            self.lista_itens.delete(index)
            del self.pecas_servicos[index]


    def criar_botoes(self):
        self.btn_gerar = ttk.Button(self, text="Gerar PDF", command=self.gerar_pdf)
        self.btn_gerar.grid(row=14, column=1, sticky="e", pady=10)

    def adicionar_item(self):
        nome = self.entry_peca.get().strip()
        qtd = self.entry_qtd.get().strip()
        valor = self.entry_valor.get().strip().replace(",", ".")

        if not nome or not qtd or not valor:
            messagebox.showerror("Erro", "Preencha todos os campos do item.")
            return

        try:
            qtd = int(qtd)
            valor_float = float(valor)
            total = qtd * valor_float
        except ValueError:
            messagebox.showerror("Erro", "Quantidade deve ser número inteiro e valor deve ser numérico.")
            return

        item_str = f"{nome} - Qtd: {qtd} - R$ {valor_float:.2f} - Total: R$ {total:.2f}"
        self.lista_itens.insert(tk.END, item_str)

        self.pecas_servicos.append({
            "nome": nome,
            "qtd": qtd,
            "vl_unitario": f"{valor_float:.2f}",
            "total": f"{total:.2f}"
        })

        self.entry_peca.delete(0, tk.END)
        self.entry_qtd.delete(0, tk.END)
        self.entry_valor.delete(0, tk.END)

    def gerar_pdf(self):
        if not self.entry_nome.get().strip() or not self.entry_endereco.get().strip() or not self.entry_defeito.get().strip() or not self.entry_equipamento.get().strip():
            messagebox.showerror("Erro", "Preencha os campos obrigatórios.")
            return

        valor_total = sum(float(item["total"].replace(",", ".")) for item in self.pecas_servicos)

        dados = {
            "nome": self.entry_nome.get().strip(),
            "telefones": [t.strip() for t in self.entry_telefones.get().split(",") if t.strip()],
            "endereco": self.entry_endereco.get().strip(),
            "cnpj": self.entry_cnpj.get().strip(),
            "equipamento": self.entry_equipamento.get().strip(),
            "modelo": self.entry_modelo.get().strip(),
            "marca": self.entry_marca.get().strip(),
            "defeito": self.entry_defeito.get().strip(),
            "laudo_tecnico": self.txt_laudo.get("1.0", tk.END).strip(),
            "pecas": self.pecas_servicos,
            "valor_total": f"{valor_total:,.2f}".replace(".", ",")
        }

        caminho = gerar_ordem_servico(dados)
        messagebox.showinfo("Sucesso", f"PDF gerado em:\n{caminho}")

if __name__ == "__main__":
    app = OrdemServicoApp()
    app.mainloop()