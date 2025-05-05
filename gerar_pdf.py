from fpdf import FPDF
from datetime import datetime
import os

class OrdemServico(FPDF):

    def header(self):

        # Verfificação que garante cabecalho só na primeira folha, tava indo em todas lkkkkk
        if self.page_no() > 1:
            return

        self.set_font("Arial", 'B', 12)
        self.set_xy(10, 10)
        self.cell(100, 6, "Braza Tech Solutions Computadores", ln=True, align="L")

        self.set_font("Arial", size=9)
        self.set_x(10)
        self.cell(100, 5, "CNPJ: 12.345.678/0001-90  IE: 123.456.789.000", ln=True)
        self.set_x(10)
        self.cell(100, 5, "Rua das Inovações, 123", ln=True)
        self.set_x(10)
        self.cell(100, 5, "Parque Tecnologia, Nova Tech-SP", ln=True)
        self.set_x(10)
        self.cell(100, 5, "CEP 01234-567", ln=True)

        # Contatos
        y_base = 10
        if os.path.exists("IMG/email.png"):
            self.image("IMG/email.png", x=120, y=y_base, w=4)
        self.set_xy(125, y_base)
        self.cell(0, 5, "contato@brazatech.com", ln=True)

        y_base += 5
        if os.path.exists("IMG/whatsapp.png"):
            self.image("IMG/whatsapp.png", x=120, y=y_base, w=4)
        self.set_xy(125, y_base)
        self.cell(0, 5, "(11) 91234-5678", ln=True)

        y_base += 5
        if os.path.exists("IMG/whatsapp.png"):
            self.image("IMG/whatsapp.png", x=120, y=y_base, w=4)
        self.set_xy(125, y_base)
        self.cell(0, 5, "(11) 3456-7890", ln=True)

        self.ln(12)
        y_redes = self.get_y()

        if os.path.exists("IMG/instagram.png"):
            self.image("IMG/instagram.png", x=10, y=y_redes, w=4)
        self.set_xy(16, y_redes)
        self.cell(60, 5, "@brazatechoficial", ln=False)

        if os.path.exists("IMG/facebook.png"):
            self.image("IMG/facebook.png", x=80, y=y_redes, w=4)
        self.set_xy(86, y_redes)
        self.cell(0, 5, "facebook.com/brazatechoficial", ln=True)

        self.ln(5)

    def secao(self, titulo):
        self.set_font("Arial", 'B', 11)
        self.set_fill_color(180, 180, 180)
        self.cell(0, 6, titulo, ln=True, fill=True)
        self.ln(1)

    def gerar_os(self, dados):
        self.set_font("Arial", 'B', 11)
        self.set_fill_color(180, 180, 180)
        self.cell(120, 10, f"Ordem de Serviço: {dados['numero_os']}", fill=True)
        self.cell(0, 10, f"Data: {datetime.now().strftime('%d/%m/%Y')}", ln=True, align="R", fill=True)
        self.ln(2)

        self.set_font("Arial", '', 10)
        self.cell(100, 6, dados['nome'], ln=False)
        x_telefone = 115
        for telefone in dados.get('telefones', []):
            if os.path.exists("IMG/whatsapp.png"):
                self.image("IMG/whatsapp.png", x=x_telefone, y=self.get_y(), w=4)
            self.set_xy(x_telefone + 6, self.get_y())
            self.cell(35, 6, telefone, ln=False)
            x_telefone += 45
        self.ln(6)

        self.multi_cell(0, 6, dados['endereco'])
        if dados.get("cnpj"):
            self.cell(0, 6, f"CNPJ: {dados['cnpj']}", ln=True)
        self.ln(2)

        self.secao("Informações Básicas")
        self.set_font("Arial", 'B', 10)
        self.cell(90, 6, "Marca:", ln=False)
        self.cell(90, 6, "Modelo:", ln=True)
        self.set_font("Arial", '', 10)
        self.cell(90, 6, dados.get('marca', ''), ln=False)
        self.cell(90, 6, dados.get('modelo', ''), ln=True)
        self.ln(2)
        self.set_font("Arial", 'B', 10)
        self.cell(90, 6, "Equipamento:", ln=False)
        self.cell(90, 6, "Defeito:", ln=True)
        self.set_font("Arial", '', 10)
        self.cell(90, 6, dados.get('equipamento', ''), ln=False)
        self.cell(90, 6, dados.get('defeito', ''), ln=True)

        self.ln(2)
        self.secao("Laudo Técnico")
        self.multi_cell(0, 8, dados['laudo_tecnico'])
        self.ln(2)

        self.secao("Peças e Serviços")
        self.set_font("Arial", 'B', 9)
        row_height = 6
        self.cell(90, row_height, "Peça(s)/Serviço(s)", border=0)
        self.cell(20, row_height, "Qtd", border=0)
        self.cell(30, row_height, "Vl Un", border=0)
        self.cell(40, row_height, "Total", border=0, ln=True)

        self.set_font("Arial", size=8)
        for peca in dados['pecas']:
            self.cell(90, row_height, peca['nome'], border=0)
            self.cell(20, row_height, str(peca['qtd']), border=0)
            self.cell(30, row_height, f"R$ {peca['vl_unitario']}", border=0)
            self.cell(40, row_height, f"R$ {peca['total']}", border=0, ln=True)

        self.ln(2)
        self.secao("VALOR TOTAL")
        self.ln(0.2)  # diminui o espaço vertical
        self.set_font("Arial", 'B', 11)
        self.cell(0, 8, f"R$ {dados['valor_total']}", ln=True)



        self.set_font("Arial", 'B', 10)
        self.cell(0, 6, "Meios de Pagamento", ln=True)
        self.set_font("Arial", size=8)
        self.multi_cell(0, 5, "Boleto, transferência bancária, dinheiro, cheque, cartão de crédito, débito ou PIX.")
        self.cell(0, 5, "Prazo de validade do orçamento: 7 dias.", ln=True)

        self.set_font("Arial", 'B', 10)
        self.cell(0, 6, "Informações Adicionais", ln=True)
        self.set_font("Arial", size=8)
        self.multi_cell(0, 5, "A garantia de 90 dias cobre peças substituídas e mão de obra.")
        self.multi_cell(0, 5, "Observação: pagamento de entrada no ato e o restante ao término do serviço.")

        self.ln(10)
        data_hoje = datetime.now().strftime('%d/%m/%Y')
        self.cell(0, 6, f"São Paulo, {data_hoje}", ln=True, align="C")
        self.ln(10)

        largura_assinatura = 80
        y_assinatura = self.get_y()

        self.set_xy(20, y_assinatura)
        self.cell(largura_assinatura, 6, "_" * 30, ln=False, align="C")

        self.set_xy(110, y_assinatura)
        self.cell(largura_assinatura, 6, "_" * 30, ln=True, align="C")

        self.set_font("Arial", 'B', 9)
        self.set_xy(20, y_assinatura + 6)
        self.cell(largura_assinatura, 5, "Braza Tech Solutions Computadores", ln=False, align="C")

        self.set_xy(110, y_assinatura + 6)
        self.cell(largura_assinatura, 5, dados.get("nome", "Cliente"), ln=True, align="C")

def obter_proxima_os():
    caminho = "contador_os.txt"
    if os.path.exists(caminho):
        with open(caminho, "r") as f:
            numero_atual = int(f.read().strip())
    else:
        numero_atual = 8800
    proxima_os = numero_atual + 1
    with open(caminho, "w") as f:
        f.write(str(proxima_os))
    return proxima_os

def gerar_ordem_servico(dados):
    numero_os = obter_proxima_os()
    dados["numero_os"] = str(numero_os)
    pdf = OrdemServico()
    pdf.add_page()
    pdf.gerar_os(dados)
    nome_arquivo = f"OS_Braza_{numero_os}.pdf"
    caminho = os.path.join("pdf", nome_arquivo)
    os.makedirs("pdf", exist_ok=True)
    pdf.output(caminho)
    return caminho