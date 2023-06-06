# "A LICENÇA AÇAÍWARE" (Revisão +55):
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
# Gerador de Análises Livre e Open-source

import os, sys
parent = os.path.abspath(".")
sys.path.insert(1, parent)

# Bibliotecas
from dateutil.relativedelta import relativedelta
from fpdf import FPDF
from tqdm import tqdm
import datetime as DT
import json
import pandas as PD

# Ferramentas
from Ferramentas.LSI import LSI
from Ferramentas.Mês import Mês
from Ferramentas.SigUF2NomeUF import SigUF2NomeUF as S2N
from Ferramentas.Título import Título

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

	def capa(self,ano,mês_txt):
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
		self.multi_cell(w=self.pdf_w_util, h=0, align="C", txt=f"{mês_txt}")

		self.set_xy(15,265); self.set_font("Franklin Gothic Heavy Italic", "B", 50)
		self.multi_cell(w=self.pdf_w_util, h=0, align="C", txt=f"{ano}")

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
		self.cell(w=self.pdf_w_util, h=0, align="", txt=f"Potência Instalada: {LSI(dados['PotInst'])}Wp")

		py += 13/2; self.set_xy(15,py); self.set_font("Univers", "B", 13)
		self.cell(w=self.pdf_w_util, h=0, align="", txt=f"Geração Estimada: {LSI(dados['PotGer']*1000)}Wh.ano")

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
		self.cell(w=self.pdf_w_util, h=0, align="", txt=f"Potência Instalada: {LSI(dados_m['PotInst'])}Wp")

		py += 13/2; self.set_xy(15,py); self.set_font("Univers", "B", 13)
		self.cell(w=self.pdf_w_util, h=0, align="", txt=f"Geração Estimada: {LSI(dados_m['PotInst']*1000)}Wh.ano")

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

#############
# ARENA MRV #
#############

class ARENA_MRV():
	def __init__(self,RR=False):
		Título("ARENA MRV")

		self.ATLETICANOS = PD.read_csv("BDD/ATLETICANOS.csv",sep=";")

		self.POP = PD.read_csv("BDD/IBGE/POPULAÇÃO.csv",sep=",")

		self.BID_CBF = PD.read_csv("BDD/BID_CBF.csv",sep=";")
		self.dt_BDD = self.BID_CBF["dt_ANEEL"][0]
		self.ult_Data = DT.datetime.strptime(self.dt_BDD, "%Y-%m-%d")
		if(int(self.dt_BDD[8:]) <= 10):
			self.Data_lim = self.ult_Data - DT.timedelta(days=self.ult_Data.day) - relativedelta(months=+1)
		else:
			self.Data_lim = self.ult_Data - DT.timedelta(days=self.ult_Data.day)
		self.mês = self.Data_lim.month
		self.mês_txt = Mês(self.mês)
		self.ano = self.Data_lim.year

		with open(f"BDD/ANÁLISES/BRASIL/{self.ano} - {self.mês} [TOTAL].json") as f:
			self.BR_DT = json.load(f)
		with open(f"BDD/ANÁLISES/BRASIL/{self.ano} - {self.mês} [MÊS].json") as f:
			self.BR_DM = json.load(f)

		self.GALOUCURA(RR)

	def GALOUCURA(self, RR=False):
		self.filtro = ["Emp","UC","PotInst","PotGer"]
		self.filtro_txt = ["Empreendimentos","Unidades Consumidoras","Potência Instalada [W]","Geração Estimada [kWh.ano]"]

		for i in (ibar := tqdm(self.ATLETICANOS.index, leave=False, position=0)):
			nome = self.ATLETICANOS["Nome"][i]
			ibar.set_description(f"{nome}")

			Brasil = self.ATLETICANOS["Brasil"][i]
			try:	agentes = self.ATLETICANOS["Agentes"][i].split(", ") # SigAgente
			except: agentes = []
			try:	estados = self.ATLETICANOS["Estados"][i].split(", ") # SigUF
			except: estados = []
			try:	municípios = self.ATLETICANOS["Municípios"][i].split(", ") # CodMunicipioIbge
			except: municípios = []

			P_PDF = f"BDD/RELATÓRIOS/GALO - {nome} - {self.ano} - {self.mês}.pdf"

			if not os.path.isfile(P_PDF) or RR:
				PDF = GALO_PDF()
				PDF.capa(self.ano,self.mês_txt)
				for fi in (fbar := tqdm(["Brasil","Agentes","Estados","Municípios"], leave=False, position=1)):
					fbar.set_description(f"{fi}")
					if fi == "Brasil" and Brasil == "Sim": self.análises_Brasil(PDF)
					elif fi == "Agentes": self.análises_Agentes(PDF,agentes)
					elif fi == "Estados": self.análises_Estados(PDF,estados)
					elif fi == "Municípios": self.análises_Municípios(PDF,municípios)
				PDF.output(P_PDF,"F")

	##########
	# BRASIL #
	##########
	def análises_Brasil(self,PDF:GALO_PDF):
		for anl in (anlbar := tqdm(["Dados","Total","Mês","Mês-a-Mês","Ano-a-Ano"], leave=False, position=2)):
			anlbar.set_description(f"{anl}")
			if anl == "Dados": PDF.pg_FD("B","Brasil","Dados - Total",self.BR_DT,f"Dados - {self.mês_txt} de {self.ano}",self.BR_DM)
			elif anl == "Total":
				PDF.pg_TG(f"Brasil - Total",f"BDD/GRÁFICOS/BRASIL/{self.ano} - {self.mês} [Total Est].png")
				PDF.pg_TG(f"Brasil - Total",f"BDD/GRÁFICOS/BRASIL/{self.ano} - {self.mês} [Total Mun].png")
			elif anl == "Mês":
				PDF.pg_TG(f"Brasil - {self.mês_txt} de {self.ano}",f"BDD/GRÁFICOS/BRASIL/{self.ano} - {self.mês} [Mês Est].png")
				PDF.pg_TG(f"Brasil - {self.mês_txt} de {self.ano}",f"BDD/GRÁFICOS/BRASIL/{self.ano} - {self.mês} [Mês Mun].png")
			elif anl == "Mês-a-Mês":
				filtro = ["Emp","UC","PotInst","PotGer"]
				for MM in (MMbar := tqdm(filtro, leave=False, position=3)):
					MMbar.set_description(f"{MM}")
					P = f"BDD/GRÁFICOS/BRASIL/{self.ano} - {self.mês} [Mês-a-Mês {MM}].png"
					if os.path.isfile(P):
						PDF.pg_TG(f"Brasil - Mês-a-Mês [{MM}]",P)
			elif anl == "Ano-a-Ano":
				filtro = ["Emp","UC","PotInst","PotGer"]
				for AA in (AAbar := tqdm(filtro, leave=False, position=3)):
					AAbar.set_description(f"{AA}")
					P = f"BDD/GRÁFICOS/BRASIL/{self.ano} - {self.mês} [Ano-a-Ano {AA}].png"
					if os.path.isfile(P):
						PDF.pg_TG(f"Brasil - Ano-a-Ano [{AA}]",P)

	###########
	# AGENTES #
	###########
	def análises_Agentes(self,PDF:GALO_PDF,agentes):
		for ai in (abar := tqdm(agentes, leave=False, position=2)):
			abar.set_description(f"{ai}")

			with open(f"BDD/ANÁLISES/AGENTES/{ai}/{self.ano} - {self.mês} [TOTAL].json") as f:
				A_DT = json.load(f)
			with open(f"BDD/ANÁLISES/AGENTES/{ai}/{self.ano} - {self.mês} [MÊS].json") as f:
				A_DM = json.load(f)

			for anl in (anlbar := tqdm(["Dados","Total","Mês","Mês-a-Mês","Ano-a-Ano"], leave=False, position=3)):
				anlbar.set_description(f"{anl}")
				if anl == "Dados":
					PDF.pg_FD("A",f"{ai}",f"Dados - Total",A_DT,f"Dados - {self.mês_txt} de {self.ano}",A_DM)
				elif anl == "Total":
					P = f"BDD/GRÁFICOS/AGENTES/{ai}/{self.ano} - {self.mês} [Total Mun].png"
					if os.path.isfile(P):
						PDF.pg_TG(f"{ai} - Total",P)
				elif anl == "Mês":
					P = f"BDD/GRÁFICOS/AGENTES/{ai}/{self.ano} - {self.mês} [Mês Mun].png"
					if os.path.isfile(P):
						PDF.pg_TG(f"{ai} - {self.mês_txt} de {self.ano}",P)
				elif anl == "Mês-a-Mês":
					for MM in (MMbar := tqdm(self.filtro, leave=False, position=4)):
						MMbar.set_description(f"{MM}")
						P = f"BDD/GRÁFICOS/AGENTES/{ai}/{self.ano} - {self.mês} [Mês-a-Mês {MM}].png"
						if os.path.isfile(P):
							PDF.pg_TG(f"{ai} - Mês-a-Mês [{MM}]",P)
				elif anl == "Ano-a-Ano":
					for AA in (AAbar := tqdm(self.filtro, leave=False, position=4)):
						AAbar.set_description(f"{AA}")
						P = f"BDD/GRÁFICOS/AGENTES/{ai}/{self.ano} - {self.mês} [Ano-a-Ano {AA}].png"
						if os.path.isfile(P):
							PDF.pg_TG(f"{ai} - Ano-a-Ano [{AA}]",P)

	###########
	# ESTADOS #
	###########
	def análises_Estados(self,PDF:GALO_PDF,estados):
		for ei in (ebar := tqdm(estados, leave=False, position=2)):
			ei_nome = S2N(ei)
			ebar.set_description(f"{ei}")

			with open(f"BDD/ANÁLISES/ESTADOS/{ei}/{self.ano} - {self.mês} [TOTAL].json") as f:
				E_DT = json.load(f)
			with open(f"BDD/ANÁLISES/ESTADOS/{ei}/{self.ano} - {self.mês} [MÊS].json") as f:
				E_DM = json.load(f)

			for anl in (anlbar := tqdm(["Dados","Total","Mês","Mês-a-Mês","Ano-a-Ano"], leave=False, position=3)):
				anlbar.set_description(f"{anl}")
				if anl == "Dados":
					PDF.pg_FD("E",f"{ei_nome}",f"Dados - Total",E_DT,f"Dados - {self.mês_txt} de {self.ano}",E_DM)
				elif anl == "Total":
					P = f"BDD/GRÁFICOS/ESTADOS/{ei}/{self.ano} - {self.mês} [Total Mun].png"
					if os.path.isfile(P):
						PDF.pg_TG(f"{ei_nome} - Total",P)
				elif anl == "Mês":
					P = f"BDD/GRÁFICOS/ESTADOS/{ei}/{self.ano} - {self.mês} [Mês Mun].png"
					if os.path.isfile(P):
						PDF.pg_TG(f"{ei_nome} - {self.mês_txt} de {self.ano}",P)
				elif anl == "Mês-a-Mês":
					for MM in (MMbar := tqdm(self.filtro, leave=False, position=4)):
						MMbar.set_description(f"{MM}")
						P = f"BDD/GRÁFICOS/ESTADOS/{ei}/{self.ano} - {self.mês} [Mês-a-Mês {MM}].png"
						if os.path.isfile(P):
							PDF.pg_TG(f"{ei} - Mês-a-Mês [{MM}]",P)
				elif anl == "Ano-a-Ano":
					for AA in (AAbar := tqdm(self.filtro, leave=False, position=4)):
						AAbar.set_description(f"{AA}")
						P = f"BDD/GRÁFICOS/ESTADOS/{ei}/{self.ano} - {self.mês} [Ano-a-Ano {AA}].png"
						if os.path.isfile(P):
							PDF.pg_TG(f"{ei} - Ano-a-Ano [{AA}]",P)

	##############
	# MUNICÍPIOS #
	##############
	def análises_Municípios(self,PDF:GALO_PDF,municípios):
		for mi in (mbar := tqdm(municípios, leave=False, position=2)):
			try: M = self.POP.loc[self.POP["CodMunicipioIbge"] == int(mi)]
			except: continue
			
			mi_nome = M["NomMunicipio"][M.index[0]]
			mi_uf = M["SigUF"][M.index[0]]
			mbar.set_description(f"{mi_nome} [{mi_uf}]")

			with open(f"BDD/ANÁLISES/MUNICÍPIOS/{mi}/{self.ano} - {self.mês} [TOTAL].json") as f:
				M_DT = json.load(f)
			with open(f"BDD/ANÁLISES/MUNICÍPIOS/{mi}/{self.ano} - {self.mês} [MÊS].json") as f:
				M_DM = json.load(f)

			PDF.pg_FD("M",f"{mi_nome} [{mi_uf}]",f"Dados - Total",M_DT,f"Dados - {self.mês_txt} de {self.ano}",M_DM)

			for anl in (anlbar := tqdm(["Dados","Mês-a-Mês","Ano-a-Ano"], leave=False, position=3)):
				anlbar.set_description(f"{anl}")
				if anl == "Dados": PDF.pg_FD("M",f"{mi_nome} [{mi_uf}]",f"Dados - Total",M_DT,f"Dados - {self.mês_txt} de {self.ano}",M_DM)
				elif anl == "Mês-a-Mês":
					for MM in (MMbar := tqdm(self.filtro, leave=False, position=4)):
						MMbar.set_description(f"{MM}")
						P = f"BDD/GRÁFICOS/MUNICÍPIOS/{mi}/{self.ano} - {self.mês} [Mês-a-Mês {MM}].png"
						if os.path.isfile(P):
							PDF.pg_TG(f"{mi_nome} - Mês-a-Mês [{MM}]",P)
				elif anl == "Ano-a-Ano":
					for AA in (AAbar := tqdm(self.filtro, leave=False, position=4)):
						AAbar.set_description(f"{AA}")
						P = f"BDD/GRÁFICOS/MUNICÍPIOS/{mi}/{self.ano} - {self.mês} [Ano-a-Ano {AA}].png"
						if os.path.isfile(P):
							PDF.pg_TG(f"{mi_nome} - Ano-a-Ano [{AA}]",P)

if __name__ == "__main__":
	os.system("cls" if os.name == "nt" else "clear")
	print(" ██████╗  █████╗ ██╗      ██████╗ ")
	print("██╔════╝ ██╔══██╗██║     ██╔═══██╗")
	print("██║  ███╗███████║██║     ██║   ██║")
	print("██║   ██║██╔══██║██║     ██║   ██║")
	print("╚██████╔╝██║  ██║███████╗╚██████╔╝")
	print(" ╚═════╝ ╚═╝  ╚═╝╚══════╝ ╚═════╝ ")
	print("Gerador de Análises Livre e Open-source")
	APP = ARENA_MRV(True)
