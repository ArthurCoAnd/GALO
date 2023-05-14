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

# Bibliotecas
from dateutil.relativedelta import relativedelta
from si_prefix import si_format as SI
from matplotlib.ticker import EngFormatter as EF
from tqdm import tqdm, trange
import datetime as DT
import json
import pandas as PD
import matplotlib.pyplot as MPL
import numpy as NP
import os

# Importar Módulos
from BDD.ATL_BDD import ATL_BDD
from Módulos.PDF import GALO_PDF

# Ferramentas
from Ferramentas.Dia_Da_Semana import Dia_Da_Semana as DDS
from Ferramentas.Filtrar_Dados import Filtrar_Dados as FD
from Ferramentas.Mês import Mês
from Ferramentas.LSI import LSI
from Ferramentas.Título import Título
from Ferramentas.SigUF2NomeUF import SigUF2NomeUF as S2N

# https://www.ibge.gov.br/explica/codigos-dos-municipios.php

class GALO():
	def __init__(self):
		print(" ██████╗  █████╗ ██╗      ██████╗ ")
		print("██╔════╝ ██╔══██╗██║     ██╔═══██╗")
		print("██║  ███╗███████║██║     ██║   ██║")
		print("██║   ██║██╔══██║██║     ██║   ██║")
		print("╚██████╔╝██║  ██║███████╗╚██████╔╝")
		print(" ╚═════╝ ╚═╝  ╚═╝╚══════╝ ╚═════╝ ")
		
		print("Gerador de Análises Livre e Open-source")

		self.gráfico_dpi = 100

		ATL_BDD()
		self.carregar_dados()

		RR = True # RR - Regerar Relatórios
		RG = True # RA - Regerar Gráficos
		self.GALOUCURA(RR,RG)

	def carregar_dados(self):
		print("Carregar Cores")
		self.carregar_cores()

		print("Carregar Atleticanos")
		self.ATLETICANOS = PD.read_csv("BDD/ATLETICANOS.csv",sep=";")
		
		print("Carregar Registro Atualização Banco de Dados")
		self.REG_ATL = PD.read_csv("BDD/REG_ATL.csv",sep=";")
		self.dt_BDD = self.REG_ATL["dt_ANEEL"][0]

		print("Carregar Dados Estados")
		self.CodUF = PD.read_csv("BDD/IBGE/CodUF.csv",sep=";")

		print("Carregar População")
		self.POP = PD.read_csv("BDD/IBGE/POPULAÇÃO.csv",sep=",")

		print("Carregar ANEEL")
		self.carregar_ANEEL()

	def carregar_ANEEL(self):
		self.ANEEL = PD.read_csv(f"BDD/ANEEL/{self.dt_BDD}.csv",sep=";",encoding='latin-1',low_memory=False)
		self.ANEEL = FD(self.ANEEL)

		INV_CNPJ_AGENTE = (self.ANEEL["NumCNPJDistribuidora"] == 0)
		INV_SIG_AGENTE = (self.ANEEL["SigAgente"] == "-")
		INV_COD_UF = (self.ANEEL["codUFibge"] == 0)
		INV_SIG_UF = (self.ANEEL["SigUF"] == "-")
		INV_COD_MUN = (self.ANEEL["CodMunicipioIbge"] == 0)
		INV_NOM_MUN = (self.ANEEL["NomMunicipio"] == "-")
		INV_POT = (self.ANEEL["MdaPotenciaInstaladaKW"] == 0)
		INV_UC = (self.ANEEL["QtdUCRecebeCredito"] == 0)
		INV_TIP_GER = (self.ANEEL["SigTipoGeracao"] == "-")

		print("Carregar DADOS")
		self.DADOS = self.ANEEL.copy()
		self.DADOS = self.DADOS.loc[~INV_CNPJ_AGENTE]
		self.DADOS = self.DADOS.loc[~INV_SIG_AGENTE]
		self.DADOS = self.DADOS.loc[~INV_COD_UF]
		self.DADOS = self.DADOS.loc[~INV_SIG_UF]
		self.DADOS = self.DADOS.loc[~INV_COD_MUN]
		self.DADOS = self.DADOS.loc[~INV_NOM_MUN]
		self.DADOS = self.DADOS.loc[~INV_POT]
		self.DADOS = self.DADOS.loc[~INV_UC]
		self.DADOS = self.DADOS.loc[~INV_TIP_GER]

		self.primeira_Data = self.DADOS["DthAtualizaCadastralEmpreend"].min()
		self.ult_Data = self.DADOS["DthAtualizaCadastralEmpreend"].max()
		if(int(self.dt_BDD[8:]) <= 10):
			self.Data_lim = self.ult_Data - DT.timedelta(days=self.ult_Data.day) - relativedelta(months=+1)
		else:
			self.Data_lim = self.ult_Data - DT.timedelta(days=self.ult_Data.day)

		self.DADOS = self.DADOS[self.DADOS["DthAtualizaCadastralEmpreend"] <= self.Data_lim]
		self.DADOS["Ano"] = [d.year for d in self.DADOS["DthAtualizaCadastralEmpreend"]]
		self.DADOS["Mês"] = [d.month for d in self.DADOS["DthAtualizaCadastralEmpreend"]]
		self.DADOS["Ano-Mês"] = [f"{d.year}-{d.month}" for d in self.DADOS["DthAtualizaCadastralEmpreend"]]

		self.mês = self.Data_lim.month
		self.mês_txt = Mês(self.mês)
		self.ano = self.Data_lim.year

		print("Gerar Análises Total")
		self.dados_total = self.gerar_dados(self.DADOS,"B")
		self.dados_total["Mês"] = self.mês
		self.dados_total["Mês_txt"] = self.mês_txt
		self.dados_total["Ano"] = self.ano

		DE = self.CALC_DADOS_ESTADOS(self.DADOS)
		DM = self.CALC_DADOS_MUNICÍPIOS(self.DADOS)
		DMM = self.CALC_MES_MES(self.DADOS)
		self.GFG_Emp_PotInst_Est_Mun(DE,DM,f"ANÁLISES/TOTAL/{self.ano} - {self.mês}.png")
		self.GFG_MM(DMM,f"ANÁLISES/ANUAL/{self.ano} - {self.mês}.png",12,3)

		print("Gerar Análises Mês")
		self.DADOS_MÊS = self.DADOS.loc[self.DADOS["Ano-Mês"] == f"{self.ano}-{self.mês}"]
		self.DADOS_MÊS = self.DADOS_MÊS.loc[self.DADOS_MÊS["Ano-Mês"] == f"{self.ano}-{self.mês}"]
		self.dados_mês = self.gerar_dados(self.DADOS_MÊS,"B")
		self.dados_mês["Mês"] = self.mês
		self.dados_mês["Mês_txt"] = self.mês_txt
		self.dados_mês["Ano"] = self.ano

		DE = self.CALC_DADOS_ESTADOS(self.DADOS_MÊS)
		DM = self.CALC_DADOS_MUNICÍPIOS(self.DADOS_MÊS)
		self.GFG_Emp_PotInst_Est_Mun(DE,DM,f"ANÁLISES/MÊS/{self.ano} - {self.mês}.png")

	def gerar_dados(self,DADOS,tipo):
		D = {}

		Emp = len(DADOS)
		D["Emp"] = Emp

		UC = sum(DADOS["QtdUCRecebeCredito"])
		D["UC"] = UC

		PotInst = sum(DADOS["MdaPotenciaInstaladaKW"])*1000
		D["PotInst"] = PotInst

		# Nº de Agentes
		if tipo == "B" or tipo == "E" or tipo == "M":
			Age = len(DADOS["NumCNPJDistribuidora"].unique().tolist())
			D["Age"] = Age

		# Nº de Estados
		if tipo == "B" or tipo == "A":
			Est = len(DADOS["codUFibge"].unique().tolist())
			D["Est"] = Est

		# Nº de Municípios
		if tipo == "B" or tipo == "A" or tipo == "E":
			Mun = len(DADOS["CodMunicipioIbge"].unique().tolist())
			D["Mun"] = Mun

		return D

	def carregar_cores(self):
		self.COR_GALO_AMARELA = "#FFE600" # Amarelo
		self.COR_GALO_PRETA = "#000000" # Preto
		self.COR_GALO_BRANCA = "#FFFFFF" # Branco
		self.COR_GALO_CINZA = "#BABABA" # Cinza
		self.COR_GALO_DOURADA = "#998F30" # Dourado
		self.COR_GALO_VERMELHA = "#FF0017" # Vermelho

	def CALC_DADOS_ESTADOS(self,DADOS):
		codUF_DADOS = DADOS["codUFibge"].unique().tolist()
		codUF_DADOS = [x for x in codUF_DADOS if str(x) != 'nan']
		D = []
		for e in codUF_DADOS:
			E = DADOS.loc[DADOS["codUFibge"] == e]
			P = self.POP.loc[self.POP["codUFibge"] == e]
			CodUF = e
			SigUF = E["SigUF"][E.index[0]]
			pop = sum(P["pop"])
			Emp = len(E)
			Emp_pop = Emp/pop
			UC = sum(E["QtdUCRecebeCredito"])
			UC_Emp = UC/Emp
			UC_pop = UC/pop
			PotInst = sum(E["MdaPotenciaInstaladaKW"])*1000
			PotInst_Emp = PotInst/Emp
			PotInst_pop = PotInst/pop
			D.append([CodUF,SigUF,pop,Emp,Emp_pop,UC,UC_Emp,UC_pop,PotInst,PotInst_Emp,PotInst_pop])
		DADOS_ESTADOS = PD.DataFrame(D,columns=["CodUF","SigUF","pop","Emp","Emp_pop","UC","UC_Emp","UC_pop","PotInst","PotInst_Emp","PotInst_pop"])
		DADOS_ESTADOS = DADOS_ESTADOS.sort_values(by="Emp",ascending=False)
		return DADOS_ESTADOS

	def CALC_DADOS_MUNICÍPIOS(self,DADOS):
		codMun_DADOS = DADOS["CodMunicipioIbge"].unique().tolist()
		codMun_DADOS = [x for x in codMun_DADOS if str(x) != 'nan']
		D = []
		for m in codMun_DADOS:
			M = DADOS.loc[DADOS["CodMunicipioIbge"] == m]
			P = self.POP.loc[self.POP["CodMunicipioIbge"] == m]
			mun = M["NomMunicipio"][M.index[0]]
			pop = sum(P["pop"])
			Emp = len(M)
			Emp_pop = Emp/pop
			UC = sum(M["QtdUCRecebeCredito"])
			UC_Emp = UC/Emp
			UC_pop = UC/pop
			PotInst = sum(M["MdaPotenciaInstaladaKW"])*1000
			PotInst_Emp = PotInst/Emp
			PotInst_pop = PotInst/pop
			D.append([m,mun,pop,Emp,Emp_pop,UC,UC_Emp,UC_pop,PotInst,PotInst_Emp,PotInst_pop])
		DADOS_MUNICÍPIOS = PD.DataFrame(D,columns=["CodMun","Mun","pop","Emp","Emp_pop","UC","UC_Emp","UC_pop","PotInst","PotInst_Emp","PotInst_pop"])
		DADOS_MUNICÍPIOS = DADOS_MUNICÍPIOS.sort_values(by="Emp",ascending=False)
		return DADOS_MUNICÍPIOS
	
	def CALC_MES_MES(self,DADO):
		# MELHORAR SISTEMA DE DATA INICIAL - TORNAR AUTOMATICO DE ACORDO COM OS DADOS
		mês_i = self.mês
		ano_i = self.ano

		mês_min = self.primeira_Data.month
		ano_min = self.primeira_Data.year

		D = []
		while ano_i != ano_min or mês_i != mês_min:
			if mês_i == 0:
				mês_i = 12
				ano_i -= 1
			M = DADO.loc[DADO["Ano-Mês"] == f"{ano_i}-{mês_i}"]
			ano_mes_inf = f"{ano_i}-{mês_i}"
			ano_inf = ano_i
			mes_inf = mês_i
			Emp = len(M)
			if len(M) != 0:
				UC = sum(M["QtdUCRecebeCredito"])
				UC_Emp = UC/Emp
				PotInst = sum(M["MdaPotenciaInstaladaKW"])*1000
				PotInst_Emp = PotInst/Emp
			else:
				UC = 0
				UC_Emp = 0
				PotInst = 0
				PotInst_Emp = 0
			D.append([ano_mes_inf,ano_inf,mes_inf,Emp,UC,UC_Emp,PotInst,PotInst_Emp])
			mês_i -= 1
		D = PD.DataFrame(D,columns=["Ano-Mês","Ano","Mês","Emp","UC","UC_Emp","PotInst","PotInst_Emp"])
		return D
	
	def GFG(self,dados,filtro,filtro_x,leg_x,caminho,cor1="",cor2=""):
		if cor1 == "": cor1 = self.COR_GALO_PRETA
		if cor2 == "": cor2 = self.COR_GALO_CINZA

		fig = MPL.figure(figsize=(10,13),constrained_layout=True)

		D = dados.copy().sort_values(by=filtro,ascending=False).head(n=15).sort_values(by=filtro)
		ax = MPL.subplot(111)
		ax.barh(D[filtro_x].tolist(),D[filtro].tolist(),color=cor1)
		ax.set_xlabel(leg_x,fontsize=13)
		ax.xaxis.set_major_formatter(EF())
		ax.xaxis.set_tick_params(labelsize=13)
		ax.bar_label(ax.containers[0],labels=[LSI(x) for x in D[filtro]],color=cor2,label_type="center",fontsize=13)

		MPL.savefig(caminho,bbox_inches="tight",dpi=self.gráfico_dpi)
		MPL.close()

	def GFG_Emp_PotInst_Est_Mun(self,DE,DM,caminho,cor1="",cor2=""):
		if cor1 == "": cor1 = self.COR_GALO_PRETA
		if cor2 == "": cor2 = self.COR_GALO_CINZA

		fig = MPL.figure(figsize=(10,10),constrained_layout=True)

		D = DE.copy().sort_values(by="Emp",ascending=False).head(n=10).sort_values(by="Emp")
		ax = MPL.subplot(221)
		ax.set_title("Estadual")
		ax.barh(D["SigUF"].tolist(),D["Emp"].tolist(),color=cor1)
		ax.set_xlabel("nº de Empreendimentos",fontsize=8)
		ax.xaxis.set_major_formatter(EF())
		ax.xaxis.set_tick_params(labelsize=8)
		ax.bar_label(ax.containers[0], labels=[LSI(x) for x in D["Emp"]],color=cor2,label_type="center",fontsize=8)

		D = DM.copy().sort_values(by="Emp",ascending=False).head(n=10).sort_values(by="Emp")
		ax = MPL.subplot(222)
		ax.set_title("Municipal")
		ax.barh(D["Mun"].tolist(),D["Emp"].tolist(),color=cor1)
		ax.set_xlabel("nº de Empreendimentos",fontsize=8)
		ax.xaxis.set_major_formatter(EF())
		ax.xaxis.set_tick_params(labelsize=8)
		ax.bar_label(ax.containers[0], labels=[LSI(x) for x in D["Emp"]],color=cor2,label_type="center",fontsize=8)

		D = DE.copy().sort_values(by="PotInst",ascending=False).head(n=10).sort_values(by="PotInst")
		ax = MPL.subplot(223)
		ax.barh(D["SigUF"].tolist(),D["PotInst"].tolist(),color=cor1)
		ax.set_xlabel("Potência Instalada (W)",fontsize=8)
		ax.xaxis.set_major_formatter(EF(unit="W"))
		ax.xaxis.set_tick_params(labelsize=8)
		ax.bar_label(ax.containers[0], labels=[LSI(x) for x in D["PotInst"]],color=cor2,label_type="center",fontsize=8)

		D = DM.copy().sort_values(by="PotInst",ascending=False).head(n=10).sort_values(by="PotInst")
		ax = MPL.subplot(224)
		ax.barh(D["Mun"].tolist(),D["PotInst"].tolist(),color=cor1)
		ax.set_xlabel("Potência Instalada (W)",fontsize=8)
		ax.xaxis.set_major_formatter(EF(unit="W"))
		ax.xaxis.set_tick_params(labelsize=8)
		ax.bar_label(ax.containers[0], labels=[LSI(x) for x in D["PotInst"]],color=cor2,label_type="center",fontsize=8)

		MPL.savefig(caminho,bbox_inches="tight",dpi=self.gráfico_dpi)
		MPL.close()

	def GFG_Emp_PotInst_Mun(self,DM,caminho,cor1="",cor2=""):
		if cor1 == "": cor1 = self.COR_GALO_PRETA
		if cor2 == "": cor2 = self.COR_GALO_CINZA

		fig = MPL.figure(figsize=(10,10),constrained_layout=True)

		D = DM.copy().sort_values(by="Emp",ascending=False).head(n=10).sort_values(by="Emp")
		ax = MPL.subplot(221)
		ax.barh(D["Mun"].tolist(),D["Emp"].tolist(),color=cor1)
		ax.set_xlabel("nº de Empreendimentos",fontsize=8)
		ax.xaxis.set_major_formatter(EF())
		ax.xaxis.set_tick_params(labelsize=8)
		ax.bar_label(ax.containers[0], labels=[LSI(x) for x in D["Emp"]],color=cor2,label_type="center",fontsize=8)

		D = DM.copy().sort_values(by="PotInst",ascending=False).head(n=10).sort_values(by="PotInst")
		ax = MPL.subplot(222)
		ax.barh(D["Mun"].tolist(),D["PotInst"].tolist(),color=cor1)
		ax.set_xlabel("Potência Instalada (W)",fontsize=8)
		ax.xaxis.set_major_formatter(EF(unit="W"))
		ax.xaxis.set_tick_params(labelsize=8)
		ax.bar_label(ax.containers[0], labels=[LSI(x) for x in D["PotInst"]],color=cor2,label_type="center",fontsize=8)

		D = DM.copy().sort_values(by="PotInst_Emp",ascending=False).head(n=10).sort_values(by="PotInst_Emp")
		ax = MPL.subplot(223)
		ax.barh(D["Mun"].tolist(),D["PotInst_Emp"].tolist(),color=cor1)
		ax.set_xlabel("Potência Instalada / Emp. (W)",fontsize=8)
		ax.xaxis.set_major_formatter(EF(unit="W"))
		ax.xaxis.set_tick_params(labelsize=8)
		ax.bar_label(ax.containers[0], labels=[LSI(x) for x in D["PotInst_Emp"]],color=cor2,label_type="center",fontsize=8)

		D = DM.copy().sort_values(by="PotInst_pop",ascending=False).head(n=10).sort_values(by="PotInst_pop")
		ax = MPL.subplot(224)
		ax.barh(D["Mun"].tolist(),D["PotInst_pop"].tolist(),color=cor1)
		ax.set_xlabel("Potência Instalada / Hab. (W)",fontsize=8)
		ax.xaxis.set_major_formatter(EF(unit="W"))
		ax.xaxis.set_tick_params(labelsize=8)
		ax.bar_label(ax.containers[0], labels=[LSI(x) for x in D["PotInst_pop"]],color=cor2,label_type="center",fontsize=8)

		MPL.savefig(caminho,bbox_inches="tight",dpi=self.gráfico_dpi)
		MPL.close()

	def GFG_MM(self,DF,P,nM,A,cor1="",cor2="",cor3=""):
		if cor1 == "": cor1 = self.COR_GALO_PRETA
		if cor2 == "": cor2 = self.COR_GALO_CINZA
		if cor3 == "": cor3 = self.COR_GALO_VERMELHA

		fig = MPL.figure(figsize=(10,10),constrained_layout=True)

		ax = MPL.subplot(311)
		D = DF.copy().head(nM).sort_index(ascending=False)
		ax.bar(D["Ano-Mês"].tolist(),D["Emp"].tolist(),color=cor1)
		ax.set_ylabel("nº de Empreendimentos",fontsize=8)
		ax.yaxis.set_major_formatter(EF())
		ax.yaxis.set_tick_params(labelsize=8)
		ax.xaxis.set_tick_params(labelsize=8, rotation=-90)
		ax.bar_label(ax.containers[0], labels=[SI(x,2) for x in D["Emp"]],color=cor2,label_type="center",fontsize=8, rotation=-90)
		z = NP.polyfit(D.index, D["Emp"].tolist(), A)
		p = NP.poly1d(z)
		ax.plot(D["Ano-Mês"].tolist(),p(D.index),color=cor3)

		ax = MPL.subplot(312)
		D = DF.copy().head(nM).sort_index(ascending=False)
		ax.bar(D["Ano-Mês"].tolist(),D["PotInst"].tolist(),color=cor1)
		ax.set_ylabel("Potência Instalada (W)",fontsize=8)
		ax.yaxis.set_major_formatter(EF())
		ax.yaxis.set_tick_params(labelsize=8)
		ax.xaxis.set_tick_params(labelsize=8, rotation=-90)
		ax.bar_label(ax.containers[0], labels=[SI(x,2) for x in D["PotInst"]],color=cor2,label_type="center",fontsize=8, rotation=-90)
		z = NP.polyfit(D.index, D["PotInst"].tolist(), A)
		p = NP.poly1d(z)
		ax.plot(D["Ano-Mês"].tolist(),p(D.index),color=cor3)

		ax = MPL.subplot(313)
		D = DF.copy().head(nM).sort_index(ascending=False)
		ax.bar(D["Ano-Mês"].tolist(),D["PotInst_Emp"].tolist(),color=cor1)
		ax.set_ylabel("Potência Instalada / Emp. (W)",fontsize=8)
		ax.yaxis.set_major_formatter(EF())
		ax.yaxis.set_tick_params(labelsize=8)
		ax.xaxis.set_tick_params(labelsize=8, rotation=-90)
		ax.bar_label(ax.containers[0], labels=[SI(x,2) for x in D["PotInst_Emp"]],color=cor2,label_type="center",fontsize=8, rotation=-90)
		z = NP.polyfit(D.index, D["PotInst_Emp"].tolist(), 3)
		p = NP.poly1d(z)
		ax.plot(D["Ano-Mês"].tolist(),p(D.index),color=cor3)

		MPL.savefig(P,bbox_inches="tight",dpi=self.gráfico_dpi)
		MPL.close()

	#############
	# GALOUCURA #
	#############
	def GALOUCURA(self,RR=False,RG=False):
		Título("GALOUCURA")
		for i in (ibar := tqdm(self.ATLETICANOS.index, leave=False, position=0)):
			nome = self.ATLETICANOS['nome'][i]
			ibar.set_description(f"{nome}")

			Brasil = self.ATLETICANOS['Brasil'][i]
			try:	agentes = self.ATLETICANOS['agentes'][i].split(',') # SigAgente
			except: agentes = []
			try:	estados = self.ATLETICANOS['estados'][i].split(',') # SigUF
			except: estados = []
			try:	municípios = self.ATLETICANOS['municípios'][i].split(',') # CodMunicipioIbge
			except: municípios = []

			P_PDF = f"PDF/GALO - {nome} - {self.ano} - {self.mês}.pdf"

			if not os.path.isfile(P_PDF) or RR:
				PDF = GALO_PDF()
				PDF.capa(self.dados_total)
				for fi in (fbar := tqdm(["Brasil","Agentes","Estados","Municípios"], leave=False, position=1)):
					fbar.set_description(f"{fi}")
					if fi == "Brasil" and Brasil == "Sim": self.análises_Brasil(PDF)
					elif fi == "Agentes": self.análises_Agentes(PDF,agentes,RG)
					elif fi == "Estados": self.análises_Estados(PDF,estados,RG)
					elif fi == "Municípios": self.análises_Municípios(PDF,municípios,RG)
				PDF.output(P_PDF,"F")

	##########
	# BRASIL #
	##########
	def análises_Brasil(self,PDF:GALO_PDF):
		for anl in (anlbar := tqdm(["Dados","Total","Anual",f"Mês"], leave=False, position=2)):
			anlbar.set_description(f"{anl}")
			if anl == "Dados": PDF.pg_FD("B","Brasil","Dados - Total",self.dados_total,f"Dados - {self.mês_txt} de {self.ano}",self.dados_mês)
			elif anl == "Total": PDF.pg_TG(f"Brasil - Total",f"ANÁLISES/TOTAL/{self.ano} - {self.mês}.png")
			elif anl == "Anual": PDF.pg_TG("Brasil - Anual",f"ANÁLISES/ANUAL/{self.ano} - {self.mês}.png")
			elif anl == "Mês": PDF.pg_TG(f"Brasil - {self.mês_txt} de {self.ano}",f"ANÁLISES/MÊS/{self.ano} - {self.mês}.png")

	###########
	# AGENTES #
	###########
	def análises_Agentes(self,PDF:GALO_PDF,agentes,RG):
		for ai in (abar := tqdm(agentes, leave=False, position=2)):
			abar.set_description(f"{ai}")

			A = self.DADOS.loc[self.DADOS["SigAgente"] == ai]
			A_MUN = self.CALC_DADOS_MUNICÍPIOS(A)
			A_MM = self.CALC_MES_MES(A)
			A_dados = self.gerar_dados(A,"A")

			A_MÊS = A.loc[A["Ano-Mês"] == f"{self.ano}-{self.mês}"]
			A_MÊS_MUN = self.CALC_DADOS_MUNICÍPIOS(A_MÊS)
			A_dados_mês = self.gerar_dados(A_MÊS,"A")

			if not os.path.exists(f"ANÁLISES/AGENTES/{ai}"):
				os.makedirs(f"ANÁLISES/AGENTES/{ai}")

			for anl in (anlbar := tqdm(["Dados","Total","Anual",f"Mês"], leave=False, position=3)):
				anlbar.set_description(f"{anl}")
				if anl == "Dados":
					PDF.pg_FD("A",f"{ai}",f"Dados - Total",A_dados,f"Dados - {self.mês_txt} de {self.ano}",A_dados_mês)
				elif anl == "Total":
					P = f"ANÁLISES/AGENTES/{ai}/{self.ano} - {self.mês} [Total Municipal].png"
					if not os.path.isfile(P) or RG:
						self.GFG_Emp_PotInst_Mun(A_MUN,P)
					if os.path.isfile(P):
						PDF.pg_TG(f"{ai} - Total",P)
				elif anl == "Anual":
					P = f"ANÁLISES/AGENTES/{ai}/{self.ano} - {self.mês} [Anual].png"
					if not os.path.isfile(P) or RG:
						self.GFG_MM(A_MM,P,12,3)
					if os.path.isfile(P):
						PDF.pg_TG(f"{ai} - Anual",P)
				elif anl == "Mês":
					P = f"ANÁLISES/AGENTES/{ai}/{self.ano} - {self.mês} [Mês Municipal].png"
					if not os.path.isfile(P) or RG:
						if len(A_MÊS_MUN) != 0:
							self.GFG_Emp_PotInst_Mun(A_MÊS_MUN,P)
					if os.path.isfile(P):
						PDF.pg_TG(f"{ai} - {self.mês_txt} de {self.ano}",P)

	###########
	# ESTADOS #
	###########
	def análises_Estados(self,PDF:GALO_PDF,estados,RG):
		for ei in (ebar := tqdm(estados, leave=False, position=2)):
			ei_nome = S2N(ei)
			ebar.set_description(f"{ei}")

			E = self.DADOS.loc[self.DADOS["SigUF"] == ei]
			E_MUN = self.CALC_DADOS_MUNICÍPIOS(E)
			E_MM = self.CALC_MES_MES(E)
			E_dados = self.gerar_dados(E,"E")

			E_MÊS = E.loc[E["Ano-Mês"] == f"{self.ano}-{self.mês}"]
			E_MÊS_MUN = self.CALC_DADOS_MUNICÍPIOS(E_MÊS)
			E_dados_mês = self.gerar_dados(E_MÊS,"E")

			if not os.path.exists(f"ANÁLISES/ESTADOS/{ei}"):
				os.makedirs(f"ANÁLISES/ESTADOS/{ei}")

			for anl in (anlbar := tqdm(["Dados","Total","Anual",f"Mês"], leave=False, position=3)):
				anlbar.set_description(f"{anl}")
				if anl == "Dados":
					PDF.pg_FD("E",f"{ei}",f"Dados - Total",E_dados,f"Dados - {self.mês_txt} de {self.ano}",E_dados_mês)
				elif anl == "Total":
					P = f"ANÁLISES/ESTADOS/{ei}/{self.ano} - {self.mês} [Total Municipal].png"
					if not os.path.isfile(P) or RG:
						self.GFG_Emp_PotInst_Mun(E_MUN,P)
					if os.path.isfile(P):
						PDF.pg_TG(f"{ei_nome} - Total",P)
				elif anl == "Anual":
					P = f"ANÁLISES/ESTADOS/{ei}/{self.ano} - {self.mês} [Anual].png"
					if not os.path.isfile(P) or RG:
						self.GFG_MM(E_MM,P,12,3)
					if os.path.isfile(P):
						PDF.pg_TG(f"{ei_nome} - Anual",P)
				elif anl == "Mês":
					P = f"ANÁLISES/ESTADOS/{ei}/{self.ano} - {self.mês} [Mês Municipal].png"
					if not os.path.isfile(P) or RG:
						if len(E_MÊS_MUN) != 0:
							self.GFG_Emp_PotInst_Mun(E_MÊS_MUN,P)
					if os.path.isfile(P):
						PDF.pg_TG(f"{ei_nome} - {self.mês_txt} de {self.ano}",P)

	##############
	# MUNICÍPIOS #
	##############
	def análises_Municípios(self,PDF:GALO_PDF,municípios,RG):
		for mi in (mbar := tqdm(municípios, leave=False, position=2)):
			M = self.DADOS.loc[self.DADOS["CodMunicipioIbge"] == int(mi)]
			
			mi_nome = M["NomMunicipio"][M.index[0]]
			mi_uf = M["SigUF"][M.index[0]]
			mbar.set_description(f"{mi_nome} [{mi_uf}]")

			M_MUN = self.CALC_DADOS_MUNICÍPIOS(M)
			M_MM = self.CALC_MES_MES(M)
			M_dados = self.gerar_dados(M,"M")

			M_MÊS = M.loc[M["Ano-Mês"] == f"{self.ano}-{self.mês}"]
			M_MÊS_MUN = self.CALC_DADOS_MUNICÍPIOS(M_MÊS)
			M_dados_mês = self.gerar_dados(M_MÊS,"M")

			PDF.pg_FD("M",f"{mi_nome} [{mi_uf}]",f"Dados - Total",M_dados,f"Dados - {self.mês_txt} de {self.ano}",M_dados_mês)

			if not os.path.exists(f"ANÁLISES/MUNICÍPIOS/{mi}"):
				os.makedirs(f"ANÁLISES/MUNICÍPIOS/{mi}")

			P = f"ANÁLISES/MUNICÍPIOS/{mi}/{self.ano} - {self.mês} [Anual].png"
			if not os.path.isfile(P) or RG:
				self.GFG_MM(M_MM,P,12,3)
			if os.path.isfile(P):
				PDF.pg_TG(f"{mi_nome} - Anual",P)

if __name__ == "__main__":
	os.system('cls' if os.name == 'nt' else 'clear')
	APP = GALO()