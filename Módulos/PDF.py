# "A LICENÇA AÇAÍWARE" (Revisão +13*5):
# arthurcoand@gmail.com escreveu este arquivo em 2023.
# Enquanto você manter este comentário, você poderá fazer o que quiser com este arquivo.
# Caso nos encontremos algum dia e você ache que este arquivo vale, você poderá me comprar uma açaí em retribuição.
# Arthur Cordeiro Andrade.

#  ██████╗  █████╗ ██╗      ██████╗ 
# ██╔════╝ ██╔══██╗██║     ██╔═══██╗
# ██║  ███╗███████║██║     ██║   ██║
# ██║   ██║██╔══██║██║     ██║   ██║
# ╚██████╔╝██║  ██║███████╗╚██████╔╝
#  ╚═════╝ ╚═╝  ╚═╝╚══════╝ ╚═════╝ 

# Bibliotecas
from fpdf import FPDF
import os
import sys

parent = os.path.abspath('.')
sys.path.insert(1, parent)

# Ferramentas
from Ferramentas.LSI import LSI

# https://towardsdatascience.com/creating-pdf-files-with-python-ad3ccadfae0f

class GALO_PDF(FPDF):
    def __init__(self, orientation="P", unit="mm", format="A4"):
        super().__init__(orientation, unit, format)
        
        # Variáveis
        self.pdf_w = int(self.w)
        self.pdf_w_util = self.pdf_w - 15 - 15
        self.pdf_h = int(self.h)
        self.pdf_h_util = self.pdf_h - 15 - 15

        self.add_font("Franklin Gothic Heavy Italic", "B", "Fontes/FGHI.ttf", uni=True)
        self.add_font("Univers", "B", "Fontes/Univers.ttf", uni=True)
        self.set_author("GALO")

    def borda(self):
        self.set_draw_color(13,13,13)
        for d in range(13):
            w = self.pdf_w - 2*(d+1); h = self.pdf_h - 2*(d+1)
            self.rect(d+1,d+1,w,h,style="")

    def título(self):
        self.set_text_color(13, 13, 13)
        
        self.set_xy(15,0)
        self.set_font("Franklin Gothic Heavy Italic", "B", 71)
        self.cell(w=self.pdf_w_util, h=50, align="C", txt="GALO")
        
        self.set_xy(15,0)
        self.set_font("Franklin Gothic Heavy Italic", "B", 13)
        self.cell(w=self.pdf_w_util, h=75, align="C", txt="Gerador de Análises Livre e Open-source")

        self.set_xy(15,0)
        self.set_font("Franklin Gothic Heavy Italic", "B", 13)
        self.cell(w=self.pdf_w_util, h=90, align="C", txt=f"Relatório da Relação de Empreendimentos de Geração Distribuída do Brasil")

    def img_título(self):
        w = 1586/80
        self.set_xy(self.pdf_w-w-13,13)
        self.image("./Imagens/GALO.png", w=w, h=1920/80)
        self.set_xy(w+13,13)
        self.image("./Imagens/GALO.png", w=-w, h=1920/80)

    def capa(self,dados):
        self.add_page()
        self.borda()
        
        self.set_text_color(13, 13, 13)
        
        self.set_xy(15,50); self.set_font("Franklin Gothic Heavy Italic", "B", 131)
        self.cell(w=self.pdf_w_util, h=0, align="C", txt="GALO")

        self.set_xy(15,70); self.set_font("Franklin Gothic Heavy Italic", "B", 21)
        self.cell(w=self.pdf_w_util, h=0, align="C", txt="Gerador de Análises Livre e Open-source")

        w = 1586/20; self.set_xy(self.pdf_w/2-w/2,90)
        self.image("./Imagens/GALO.png", w=w, h=1920/20)

        self.set_xy(15,190); self.set_font("Franklin Gothic Heavy Italic", "B", 21)
        self.multi_cell(w=self.pdf_w_util, h=10, align="C", txt="Relatório da Relação de Empreendimentos de Geração Distribuída do Brasil")

        self.set_xy(15,245); self.set_font("Franklin Gothic Heavy Italic", "B", 50)
        self.multi_cell(w=self.pdf_w_util, h=0, align="C", txt=f"{dados['Mês_txt']}")

        self.set_xy(15,265); self.set_font("Franklin Gothic Heavy Italic", "B", 50)
        self.multi_cell(w=self.pdf_w_util, h=0, align="C", txt=f"{dados['Ano']}")

    def gerar_pg(self):
        self.add_page()
        self.borda()
        self.título()
        self.img_título()

    def pg_FD(self,tipo,nome,título,dados,título_m,dados_m):
        self.gerar_pg()
        self.set_text_color(13, 13, 13)

        py = 13*5; self.set_xy(15,py); self.set_font("Franklin Gothic Heavy Italic", "B", 31)
        self.cell(w=self.pdf_w_util, h=0, align="C", txt=nome)

        # Total
        py += 13*2; self.set_xy(15,py); self.set_font("Franklin Gothic Heavy Italic", "B", 13)
        self.cell(w=self.pdf_w_util, h=0, align="C", txt=título)
        
        if tipo == "B" or tipo == "E" or tipo == "M":
            py += 13/2; self.set_xy(15,py); self.set_font("Univers", "B", 13)
            self.cell(w=self.pdf_w_util, h=0, align="", txt=f"Agentes: {dados['Age']}")

        if tipo == "B" or tipo == "A":
            py += 13/2; self.set_xy(15,py); self.set_font("Univers", "B", 13)
            self.cell(w=self.pdf_w_util, h=0, align="", txt=f"Estados: {dados['Est']}")

        if tipo == "B" or tipo == "A" or tipo == "E":
            py += 13/2; self.set_xy(15,py); self.set_font("Univers", "B", 13)
            self.cell(w=self.pdf_w_util, h=0, align="", txt=f"Municípios: {dados['Mun']}")

        py += 13/2; self.set_xy(15,py); self.set_font("Univers", "B", 13)
        self.cell(w=self.pdf_w_util, h=0, align="", txt=f"Empreendimentos: {dados['Emp']}")

        py += 13/2; self.set_xy(15,py); self.set_font("Univers", "B", 13)
        self.cell(w=self.pdf_w_util, h=0, align="", txt=f"Unidades Consumidoras: {dados['UC']}")

        py += 13/2; self.set_xy(15,py); self.set_font("Univers", "B", 13)
        self.cell(w=self.pdf_w_util, h=0, align="", txt=f"Potência Instalada: {LSI(dados['PotInst'])}W")

        # Mês
        py += 13; self.set_xy(15,py);self.set_font("Franklin Gothic Heavy Italic", "B", 13)
        self.cell(w=self.pdf_w_util, h=0, align="C", txt=título_m)
        
        if tipo == "B" or tipo == "E" or tipo == "M":
            py += 13/2; self.set_xy(15,py); self.set_font("Univers", "B", 13)
            self.cell(w=self.pdf_w_util, h=0, align="", txt=f"Agentes: {dados_m['Age']}")

        if tipo == "B" or tipo == "A":
            py += 13/2; self.set_xy(15,py); self.set_font("Univers", "B", 13)
            self.cell(w=self.pdf_w_util, h=0, align="", txt=f"Estados: {dados_m['Est']}")

        if tipo == "B" or tipo == "A" or tipo == "E":
            py += 13/2; self.set_xy(15,py); self.set_font("Univers", "B", 13)
            self.cell(w=self.pdf_w_util, h=0, align="", txt=f"Municípios: {dados_m['Mun']}")

        py += 13/2; self.set_xy(15,py); self.set_font("Univers", "B", 13)
        self.cell(w=self.pdf_w_util, h=0, align="", txt=f"Empreendimentos: {dados_m['Emp']}")

        py += 13/2; self.set_xy(15,py); self.set_font("Univers", "B", 13)
        self.cell(w=self.pdf_w_util, h=0, align="", txt=f"Unidades Consumidoras: {dados_m['UC']}")

        py += 13/2; self.set_xy(15,py); self.set_font("Univers", "B", 13)
        self.cell(w=self.pdf_w_util, h=0, align="", txt=f"Potência Instalada: {LSI(dados_m['PotInst'])}W")

    def pg_TG(self,título,gráfico):
        self.gerar_pg()
        self.set_text_color(13, 13, 13)
        self.set_font("Univers", "B", 13)

        py = 13*5
        self.set_xy(15,py)
        self.cell(w=self.pdf_w_util, h=0, align="C", txt=título)

        py += 13/2
        self.set_xy(15,py)
        self.image(gráfico, w=self.pdf_w_util)

if __name__ == "__main__":
    print(" ██████╗  █████╗ ██╗      ██████╗ ")
    print("██╔════╝ ██╔══██╗██║     ██╔═══██╗")
    print("██║  ███╗███████║██║     ██║   ██║")
    print("██║   ██║██╔══██║██║     ██║   ██║")
    print("╚██████╔╝██║  ██║███████╗╚██████╔╝")
    print(" ╚═════╝ ╚═╝  ╚═╝╚══════╝ ╚═════╝ ")
    print("Gerador de Análises Livre e Open-source - PDF")