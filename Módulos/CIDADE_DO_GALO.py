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
from matplotlib.ticker import EngFormatter as EF
from tqdm import tqdm
import datetime as DT
import json
import pandas as PD
import matplotlib.pyplot as MPL
import os

# Ferramentas
from Ferramentas.AM2A import AM2A
from Ferramentas.Filtrar_Dados import Filtrar_Dados as FD
from Ferramentas.LSI import LSI
from Ferramentas.Mês import Mês
from Ferramentas.Título import Título

class CIDADE_DO_GALO():
	def __init__(self,RG=False):
		Título("CIDADE DO GALO")

		# Resolução dos Gráficos
		self.gráfico_dpi = 100

		# Cores
		self.COR_GALO_AMARELA = "#FFE600" # Amarelo
		self.COR_GALO_BRANCA = "#FFFFFF" # Branco
		self.COR_GALO_CINZA = "#BABABA" # Cinza
		self.COR_GALO_DOURADA = "#998F30" # Dourado
		self.COR_GALO_VERMELHA = "#FF0017" # Vermelho
		self.COR_GALO_PRETA = "#000000" # Preto

		self.carregar_dados()
		self.carregar_ANEEL()
		
		self.TREINADOR(RG)

	def carregar_dados(self):
		self.ATLETICANOS = PD.read_csv("BDD/ATLETICANOS.csv",sep=";")
		
		self.BID_CBF = PD.read_csv("BDD/BID_CBF.csv",sep=";")
		self.dt_BDD = self.BID_CBF["dt_ANEEL"][0]

		self.CodUF = PD.read_csv("BDD/IBGE/CodUF.csv",sep=";")
		
		self.POP = PD.read_csv("BDD/IBGE/POPULAÇÃO.csv",sep=",")

	def carregar_ANEEL(self):
		self.ANEEL = PD.read_csv(f"BDD/ELENCO/{self.dt_BDD}.csv",sep=";",encoding="latin-1",low_memory=False)
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

		self.DADOS = self.DADOS.loc[self.DADOS["SigTipoGeracao"] == "UFV"]

		self.primeira_Data = self.DADOS["DthAtualizaCadastralEmpreend"].min()
		self.ult_Data = self.DADOS["DthAtualizaCadastralEmpreend"].max()
		if(int(self.dt_BDD[8:]) <= 13):
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

	############
	# ANÁLISES #
	############

	def gerar_dados(self,DADOS,tipo,P):
		D = {}
		D["Mês"] = self.mês
		D["Mês_txt"] = self.mês_txt
		D["Ano"] = self.ano
		D["Emp"] = len(DADOS)
		D["UC"] = sum(DADOS["QtdUCRecebeCredito"])
		D["PotInst"] = sum(DADOS["MdaPotenciaInstaladaKW"])*1000
		D["PotGer"] = sum(DADOS["PotGer_ANO"])
		# Nº de Agentes
		if tipo == "B" or tipo == "E" or tipo == "M":
			D["Age"] = len(DADOS["NumCNPJDistribuidora"].unique().tolist())
		# Nº de Estados
		if tipo == "B" or tipo == "A":
			D["Est"] = len(DADOS["codUFibge"].unique().tolist())
		# Nº de Municípios
		if tipo == "B" or tipo == "A" or tipo == "E":
			D["Mun"] = len(DADOS["CodMunicipioIbge"].unique().tolist())
		with open(P,"w") as anl:
			json.dump(D, anl)

	def CALC_DADOS_ESTADOS(self,DADOS):
		codUF_DADOS = DADOS["codUFibge"].unique().tolist()
		codUF_DADOS = [x for x in codUF_DADOS if str(x) != "nan"]
		D = []
		for e in codUF_DADOS:
			E = DADOS.loc[DADOS["codUFibge"] == e]
			P = self.POP.loc[self.POP["codUFibge"] == e]
			CodUF = e
			SigUF = E["SigUF"][E.index[0]]
			pop = sum(P["pop"])
			Emp = len(E)
			UC = sum(E["QtdUCRecebeCredito"])
			PotInst = sum(E["MdaPotenciaInstaladaKW"])*1000
			PotGer = sum(E["PotGer_ANO"])
			D.append([CodUF,SigUF,pop,Emp,UC,PotInst,PotGer])
		DADOS_ESTADOS = PD.DataFrame(D,columns=["CodUF","SigUF","pop","Emp","UC","PotInst","PotGer"])
		DADOS_ESTADOS = DADOS_ESTADOS.sort_values(by="Emp",ascending=False)
		return DADOS_ESTADOS

	def CALC_DADOS_MUNICÍPIOS(self,DADOS):
		codMun_DADOS = DADOS["CodMunicipioIbge"].unique().tolist()
		codMun_DADOS = [x for x in codMun_DADOS if str(x) != "nan"]
		D = []
		for m in codMun_DADOS:
			M = DADOS.loc[DADOS["CodMunicipioIbge"] == m]
			P = self.POP.loc[self.POP["CodMunicipioIbge"] == m]
			mun = M["NomMunicipio"][M.index[0]]
			pop = sum(P["pop"])
			Emp = len(M)
			UC = sum(M["QtdUCRecebeCredito"])
			PotInst = sum(M["MdaPotenciaInstaladaKW"])*1000
			PotGer = sum(M["PotGer_ANO"])
			D.append([m,mun,pop,Emp,UC,PotInst,PotGer])
		DADOS_MUNICÍPIOS = PD.DataFrame(D,columns=["CodMun","Mun","pop","Emp","UC","PotInst","PotGer"])
		DADOS_MUNICÍPIOS = DADOS_MUNICÍPIOS.sort_values(by="Emp",ascending=False)
		return DADOS_MUNICÍPIOS

	def CALC_MES_MES(self,DADOS):
		ano_i = self.ano
		mês_i = self.mês
		ano_min = min(DADOS["Ano"].unique().tolist())
		mês_min = min(DADOS.loc[DADOS["Ano"] == ano_min]["Mês"].unique().tolist())
		mês = 0
		D = []
		while ano_i != ano_min or mês_i >= mês_min:
			if mês_i == 0:
				mês_i = 12
				ano_i -= 1
			M = DADOS.loc[DADOS["Ano-Mês"] == f"{ano_i}-{mês_i}"]
			Emp = len(M)
			if Emp != 0:
				UC = sum(M["QtdUCRecebeCredito"])
				PotInst = sum(M["MdaPotenciaInstaladaKW"])*1000
				PotGer = sum(M["PotGer_ANO"])
			else:
				UC = 0
				PotInst = 0
				PotGer = 0
			D.append([mês,f"{ano_i}-{mês_i}",ano_i,mês_i,Emp,UC,PotInst,PotGer])
			mês_i -= 1
			mês += 1
		D = PD.DataFrame(D,columns=["idx","Ano-Mês","Ano","Mês","Emp","UC","PotInst","PotGer"])
		return D

	def CALC_ANO_ANO(self,DADOS):
		ano_i = self.ano
		ano_min = min(DADOS["Ano"].unique().tolist())
		D = []
		while ano_i >= ano_min:
			A = DADOS.loc[DADOS["Ano"] == ano_i]
			Emp = len(A)
			if Emp != 0:
				UC = sum(A["QtdUCRecebeCredito"])
				PotInst = sum(A["MdaPotenciaInstaladaKW"])*1000
				PotGer = sum(A["PotGer_ANO"])
			else:
				UC = 0
				PotInst = 0
				PotGer = 0
			D.append([ano_i,Emp,UC,PotInst,PotGer])
			ano_i -= 1
		D = PD.DataFrame(D,columns=["Ano","Emp","UC","PotInst","PotGer"])
		return D
	
	############
	# GRÁFICOS #
	############

	# GFG - Gerar Figura do Gráfico

	def GFG_Básico(self,DADOS,tipo,caminho,cor1="",cor2=""):
		if cor1 == "": cor1 = self.COR_GALO_PRETA
		if cor2 == "": cor2 = self.COR_GALO_CINZA

		fig = MPL.figure(figsize=(10,10),constrained_layout=True)

		D = DADOS.copy().sort_values(by="Emp",ascending=False).head(n=10).sort_values(by="Emp")
		ax = MPL.subplot(221)
		ax.barh(D[tipo].tolist(),D["Emp"].tolist(),color=cor1)
		ax.set_xlabel("nº de Empreendimentos",fontsize=8)
		ax.xaxis.set_major_formatter(EF())
		ax.xaxis.set_tick_params(labelsize=8)
		ax.bar_label(ax.containers[0], labels=[LSI(x) for x in D["Emp"]],color=cor2,label_type="center",fontsize=8)

		D = DADOS.copy().sort_values(by="PotInst",ascending=False).head(n=10).sort_values(by="PotInst")
		ax = MPL.subplot(222)
		ax.barh(D[tipo].tolist(),D["PotInst"].tolist(),color=cor1)
		ax.set_xlabel("Potência Instalada [W]",fontsize=8)
		ax.xaxis.set_major_formatter(EF())
		ax.xaxis.set_tick_params(labelsize=8)
		ax.bar_label(ax.containers[0], labels=[LSI(x) for x in D["PotInst"]],color=cor2,label_type="center",fontsize=8)

		D = DADOS.copy().sort_values(by="UC",ascending=False).head(n=10).sort_values(by="UC")
		ax = MPL.subplot(223)
		ax.barh(D[tipo].tolist(),D["UC"].tolist(),color=cor1)
		ax.set_xlabel("Unidades Consumidoras",fontsize=8)
		ax.xaxis.set_major_formatter(EF())
		ax.xaxis.set_tick_params(labelsize=8)
		ax.bar_label(ax.containers[0], labels=[LSI(x) for x in D["UC"]],color=cor2,label_type="center",fontsize=8)

		D = DADOS.copy().sort_values(by="PotGer",ascending=False).head(n=10).sort_values(by="PotGer")
		ax = MPL.subplot(224)
		ax.barh(D[tipo].tolist(),D["PotGer"].tolist(),color=cor1)
		ax.set_xlabel("Geração Estimada [kWh.ano]",fontsize=8)
		ax.xaxis.set_major_formatter(EF())
		ax.xaxis.set_tick_params(labelsize=8)
		ax.bar_label(ax.containers[0], labels=[LSI(x) for x in D["PotGer"]],color=cor2,label_type="center",fontsize=8)

		MPL.savefig(caminho,bbox_inches="tight",dpi=self.gráfico_dpi)
		MPL.close()

	def GFG_MM_Filtro(self,DADOS,P,filtro,filtro_txt,A,FS,cor1="",cor2="",cor3=""):
		if cor1 == "": cor1 = self.COR_GALO_PRETA
		if cor2 == "": cor2 = self.COR_GALO_CINZA
		if cor3 == "": cor3 = self.COR_GALO_VERMELHA

		D = DADOS.copy().sort_values(by="idx",ascending=False)
		D_am_tot = D["Ano-Mês"]
		D_val_tot = D[filtro]
		D_acu_ini = sum(D_val_tot[:-12])
		D_acu_tot = [sum(D_val_tot[:x+1]) for x in range(len(D_val_tot))]

		D = DADOS.copy().head(12).sort_values(by="idx",ascending=False)
		D_am = D["Ano-Mês"]
		D_val = D[filtro]
		D_acu = [sum(D_val[:x+1]) + D_acu_ini for x in range(len(D_val))]

		fig = MPL.figure(figsize=(10,10),constrained_layout=True)

		ax = MPL.subplot(211)
		ax.set_title("Mensal")
		ax.bar(D_am,D_val,color=cor1)
		ax.set_ylabel(filtro_txt,fontsize=FS)
		ax.yaxis.set_major_formatter(EF())
		ax.yaxis.set_tick_params(labelsize=FS)
		ax.xaxis.set_tick_params(labelsize=FS, rotation=-90)
		ax.bar_label(ax.containers[0], labels=[LSI(x) for x in D_val],color=cor2,label_type="center",fontsize=FS, rotation=-90)
		# z = NP.polyfit(D_ano, D_val, A)
		# p = NP.poly1d(z)
		# ax.plot(D_ano,p(D_ano),color=cor3)

		ax = MPL.subplot(212)
		ax.set_title("Acumulado")
		# ax.bar(D_am,D_acu,color=cor1)
		ax.plot(D_am_tot,D_acu_tot,color=cor1)
		ax.set_ylabel(filtro_txt,fontsize=FS)
		ax.yaxis.set_major_formatter(EF())
		ax.yaxis.set_tick_params(labelsize=FS)
		ax.xaxis.set_ticks(D_am_tot,labels=AM2A(D_am_tot))
		ax.xaxis.set_tick_params(labelsize=8, rotation=-90)
		# ax.bar_label(ax.containers[0], labels=[LSI(x) for x in D_acu],color=cor2,label_type="center",fontsize=FS, rotation=-90)
		# z = NP.polyfit(D.index, D_acu, A)
		# p = NP.poly1d(z)
		# ax.plot(D_ano,p(D.index),color=cor3)

		MPL.savefig(P,bbox_inches="tight",dpi=self.gráfico_dpi)
		MPL.close()

	def GFG_AA_Filtro(self,DADOS,P,filtro,filtro_txt,A,FS,cor1="",cor2="",cor3=""):
		if cor1 == "": cor1 = self.COR_GALO_PRETA
		if cor2 == "": cor2 = self.COR_GALO_CINZA
		if cor3 == "": cor3 = self.COR_GALO_VERMELHA

		D = DADOS.copy().sort_values(by="Ano")
		D_ano = [str(x) for x in D["Ano"]]
		D_val = D[filtro]
		D_acu = [sum(D_val[:x+1]) for x in range(len(D_val))]

		fig = MPL.figure(figsize=(10,10),constrained_layout=True)

		ax = MPL.subplot(211)
		ax.set_title("Anual")
		ax.bar(D_ano,D_val,color=cor1)
		ax.set_ylabel(filtro_txt,fontsize=FS)
		ax.yaxis.set_major_formatter(EF())
		ax.yaxis.set_tick_params(labelsize=FS)
		ax.xaxis.set_tick_params(labelsize=FS, rotation=-90)
		ax.bar_label(ax.containers[0], labels=[LSI(x) for x in D_val],color=cor2,label_type="center",fontsize=FS, rotation=-90)
		# z = NP.polyfit(D_ano, D_val, A)
		# p = NP.poly1d(z)
		# ax.plot(D_ano,p(D_ano),color=cor3)

		ax = MPL.subplot(212)
		ax.set_title("Acumulado")
		ax.bar(D_ano,D_acu,color=cor1)
		ax.set_ylabel(filtro_txt,fontsize=FS)
		ax.yaxis.set_major_formatter(EF())
		ax.yaxis.set_tick_params(labelsize=FS)
		ax.xaxis.set_tick_params(labelsize=FS, rotation=-90)
		ax.bar_label(ax.containers[0], labels=[LSI(x) for x in D_acu],color=cor2,label_type="center",fontsize=FS, rotation=-90)
		# z = NP.polyfit(D.index, D_acu, A)
		# p = NP.poly1d(z)
		# ax.plot(D_ano,p(D.index),color=cor3)

		MPL.savefig(P,bbox_inches="tight",dpi=self.gráfico_dpi)
		MPL.close()

	#############
	# TREINADOR #
	#############
	def TREINADOR(self,RG=False):
		self.filtros = ["Emp","UC","PotInst","PotGer"]
		self.filtros_txt = ["Empreendimentos","Unidades Consumidoras","Potência Instalada [W]","Geração Estimada [kWh.ano]"]

		age = []
		for x in self.ATLETICANOS["Agentes"].unique().tolist():
			try: age.extend(x.split(", "))
			except: pass
		age = list(set(age)); age.sort()	
		
		est = []
		for x in self.ATLETICANOS["Estados"].unique().tolist():
			try: est.extend(x.split(", "))
			except: pass
		est = list(set(est)); est.sort()

		mun = []
		for x in self.ATLETICANOS["Municípios"].unique().tolist():
			try: mun.extend(x.replace('"','').split(", "))
			except: pass
		mun = list(set(mun)); mun.sort()

		for fi in (fbar := tqdm(["Brasil","Agentes","Estados","Municípios"], leave=False, position=0)):
			fbar.set_description(f"{fi}")
			if fi == "Brasil": self.treinar_Brasil(RG)
			elif fi == "Agentes": self.treinar_Agentes(age,RG)
			elif fi == "Estados": self.treinar_Estados(est,RG)
			elif fi == "Municípios": self.treinar_Municípios(mun,RG)

	##########
	# BRASIL #
	##########
	def treinar_Brasil(self,RG=False):
		if not os.path.exists(f"BDD/ANÁLISES/BRASIL"):
			os.makedirs(f"BDD/ANÁLISES/BRASIL")

		if not os.path.exists(f"BDD/GRÁFICOS/BRASIL"):
			os.makedirs(f"BDD/GRÁFICOS/BRASIL")

		for anl in (anlbar := tqdm(["Dados","Total","Mês","Mês-a-Mês","Ano-a-Ano"], leave=False, position=1)):
			anlbar.set_description(f"{anl}")
			if anl == "Dados":
				P = f"BDD/ANÁLISES/BRASIL/{self.ano} - {self.mês} [TOTAL].json"
				if not os.path.isfile(P) or RG:
					self.gerar_dados(self.DADOS,"B",P)
				P = f"BDD/ANÁLISES/BRASIL/{self.ano} - {self.mês} [MÊS].json"
				if not os.path.isfile(P) or RG:
					BR_MÊS = self.DADOS.loc[self.DADOS["Ano-Mês"] == f"{self.ano}-{self.mês}"]
					self.gerar_dados(BR_MÊS,"B",P)
			elif anl == "Total":
				P = f"BDD/GRÁFICOS/BRASIL/{self.ano} - {self.mês} [Total Est].png"
				if not os.path.isfile(P) or RG:
					BR_EST = self.CALC_DADOS_ESTADOS(self.DADOS)
					self.GFG_Básico(BR_EST,"SigUF",P)
				P = f"BDD/GRÁFICOS/BRASIL/{self.ano} - {self.mês} [Total Mun].png"
				if not os.path.isfile(P) or RG:
					BR_MUN = self.CALC_DADOS_MUNICÍPIOS(self.DADOS)
					self.GFG_Básico(BR_MUN,"Mun",P)
			elif anl == "Mês":
				P = f"BDD/GRÁFICOS/BRASIL/{self.ano} - {self.mês} [Mês Est].png"
				if not os.path.isfile(P) or RG:
					BR_MÊS = self.DADOS.loc[self.DADOS["Ano-Mês"] == f"{self.ano}-{self.mês}"]
					BR_MÊS_EST = self.CALC_DADOS_ESTADOS(BR_MÊS)
					if len(BR_MÊS_EST) != 0:
						self.GFG_Básico(BR_MÊS_EST,"SigUF",P)
				P = f"BDD/GRÁFICOS/BRASIL/{self.ano} - {self.mês} [Mês Mun].png"
				if not os.path.isfile(P) or RG:
					BR_MÊS = self.DADOS.loc[self.DADOS["Ano-Mês"] == f"{self.ano}-{self.mês}"]
					BR_MÊS_MUN = self.CALC_DADOS_MUNICÍPIOS(BR_MÊS)
					if len(BR_MÊS_MUN) != 0:
						self.GFG_Básico(BR_MÊS_MUN,"Mun",P)
			elif anl == "Mês-a-Mês":
				for MM in (MMbar := tqdm(self.filtros, leave=False, position=2)):
					MMbar.set_description(f"{MM}")
					idx = self.filtros.index(MM)
					P = f"BDD/GRÁFICOS/BRASIL/{self.ano} - {self.mês} [Mês-a-Mês {MM}].png"
					if not os.path.isfile(P) or RG:
						BR_MaM = self.CALC_MES_MES(self.DADOS)
						self.GFG_MM_Filtro(BR_MaM,P,MM,self.filtros_txt[idx],3,13)
			elif anl == "Ano-a-Ano":
				for AA in (AAbar := tqdm(self.filtros, leave=False, position=2)):
					AAbar.set_description(f"{AA}")
					idx = self.filtros.index(AA)
					P = f"BDD/GRÁFICOS/BRASIL/{self.ano} - {self.mês} [Ano-a-Ano {AA}].png"
					if not os.path.isfile(P) or RG:
						BR_AaA = self.CALC_ANO_ANO(self.DADOS)
						self.GFG_AA_Filtro(BR_AaA,P,AA,self.filtros_txt[idx],3,13)

	###########
	# AGENTES #
	###########
	def treinar_Agentes(self,agentes,RG=False):
		for ai in (abar := tqdm(agentes, leave=False, position=1)):
			try: A = self.DADOS.loc[self.DADOS["SigAgente"] == ai]
			except: continue
			if len(A) == 0:
				continue
			else:
				abar.set_description(f"{ai}")

				if not os.path.exists(f"BDD/ANÁLISES/AGENTES/{ai}"):
					os.makedirs(f"BDD/ANÁLISES/AGENTES/{ai}")

				if not os.path.exists(f"BDD/GRÁFICOS/AGENTES/{ai}"):
					os.makedirs(f"BDD/GRÁFICOS/AGENTES/{ai}")

				for anl in (anlbar := tqdm(["Dados","Total","Mês","Mês-a-Mês","Ano-a-Ano"], leave=False, position=2)):
					anlbar.set_description(f"{anl}")
					if anl == "Dados":
						P = f"BDD/ANÁLISES/AGENTES/{ai}/{self.ano} - {self.mês} [TOTAL].json"
						if not os.path.isfile(P) or RG:
							self.gerar_dados(A,"A",P)
						P = f"BDD/ANÁLISES/AGENTES/{ai}/{self.ano} - {self.mês} [MÊS].json"
						if not os.path.isfile(P) or RG:
							A_MÊS = A.loc[A["Ano-Mês"] == f"{self.ano}-{self.mês}"]
							self.gerar_dados(A_MÊS,"A",P)
					elif anl == "Total":
						P = f"BDD/GRÁFICOS/AGENTES/{ai}/{self.ano} - {self.mês} [Total Mun].png"
						if not os.path.isfile(P) or RG:
							A_MUN = self.CALC_DADOS_MUNICÍPIOS(A)
							self.GFG_Básico(A_MUN,"Mun",P)
					elif anl == "Mês":
						P = f"BDD/GRÁFICOS/AGENTES/{ai}/{self.ano} - {self.mês} [Mês Mun].png"
						if not os.path.isfile(P) or RG:
							A_MÊS = A.loc[A["Ano-Mês"] == f"{self.ano}-{self.mês}"]
							A_MÊS_MUN = self.CALC_DADOS_MUNICÍPIOS(A_MÊS)
							if len(A_MÊS_MUN) != 0:
								self.GFG_Básico(A_MÊS_MUN,"Mun",P)
					elif anl == "Mês-a-Mês":
						for MM in (MMbar := tqdm(self.filtros, leave=False, position=3)):
							MMbar.set_description(f"{MM}")
							idx = self.filtros.index(MM)
							P = f"BDD/GRÁFICOS/AGENTES/{ai}/{self.ano} - {self.mês} [Mês-a-Mês {MM}].png"
							if not os.path.isfile(P) or RG:
								A_MaM = self.CALC_MES_MES(A)
								self.GFG_MM_Filtro(A_MaM,P,MM,self.filtros_txt[idx],3,13)
					elif anl == "Ano-a-Ano":
						for AA in (AAbar := tqdm(self.filtros, leave=False, position=3)):
							AAbar.set_description(f"{AA}")
							idx = self.filtros.index(AA)
							P = f"BDD/GRÁFICOS/AGENTES/{ai}/{self.ano} - {self.mês} [Ano-a-Ano {AA}].png"
							if not os.path.isfile(P) or RG:
								A_AaA = self.CALC_ANO_ANO(A)
								self.GFG_AA_Filtro(A_AaA,P,AA,self.filtros_txt[idx],3,13)

	###########
	# ESTADOS #
	###########
	def treinar_Estados(self,estados,RG=False):
		for ei in (ebar := tqdm(estados, leave=False, position=1)):
			try: E = self.DADOS.loc[self.DADOS["SigUF"] == ei]
			except: continue
			if len(E) == 0:
				continue
			else:
				ebar.set_description(f"{ei}")

				if not os.path.exists(f"BDD/ANÁLISES/ESTADOS/{ei}"):
					os.makedirs(f"BDD/ANÁLISES/ESTADOS/{ei}")

				if not os.path.exists(f"BDD/GRÁFICOS/ESTADOS/{ei}"):
					os.makedirs(f"BDD/GRÁFICOS/ESTADOS/{ei}")

				for anl in (anlbar := tqdm(["Dados","Total","Mês","Mês-a-Mês","Ano-a-Ano"], leave=False, position=2)):
					anlbar.set_description(f"{anl}")
					if anl == "Dados":
						P = f"BDD/ANÁLISES/ESTADOS/{ei}/{self.ano} - {self.mês} [TOTAL].json"
						if not os.path.isfile(P) or RG:
							self.gerar_dados(E,"E",P)
						P = f"BDD/ANÁLISES/ESTADOS/{ei}/{self.ano} - {self.mês} [MÊS].json"
						if not os.path.isfile(P) or RG:
							E_MÊS = E.loc[E["Ano-Mês"] == f"{self.ano}-{self.mês}"]
							self.gerar_dados(E_MÊS,"E",P)
					elif anl == "Total":
						P = f"BDD/GRÁFICOS/ESTADOS/{ei}/{self.ano} - {self.mês} [Total Mun].png"
						if not os.path.isfile(P) or RG:
							E_MUN = self.CALC_DADOS_MUNICÍPIOS(E)
							self.GFG_Básico(E_MUN,"Mun",P)
					elif anl == "Mês":
						P = f"BDD/GRÁFICOS/ESTADOS/{ei}/{self.ano} - {self.mês} [Mês Mun].png"
						if not os.path.isfile(P) or RG:
							E_MÊS = E.loc[E["Ano-Mês"] == f"{self.ano}-{self.mês}"]
							E_MÊS_MUN = self.CALC_DADOS_MUNICÍPIOS(E_MÊS)
							if len(E_MÊS_MUN) != 0:
								self.GFG_Básico(E_MÊS_MUN,"Mun",P)
					elif anl == "Mês-a-Mês":
						for MM in (MMbar := tqdm(self.filtros, leave=False, position=3)):
							MMbar.set_description(f"{MM}")
							idx = self.filtros.index(MM)
							P = f"BDD/GRÁFICOS/ESTADOS/{ei}/{self.ano} - {self.mês} [Mês-a-Mês {MM}].png"
							if not os.path.isfile(P) or RG:
								E_MaM = self.CALC_MES_MES(E)
								self.GFG_MM_Filtro(E_MaM,P,MM,self.filtros_txt[idx],3,13)
					elif anl == "Ano-a-Ano":
						for AA in (AAbar := tqdm(self.filtros, leave=False, position=3)):
							AAbar.set_description(f"{AA}")
							idx = self.filtros.index(AA)
							P = f"BDD/GRÁFICOS/ESTADOS/{ei}/{self.ano} - {self.mês} [Ano-a-Ano {AA}].png"
							if not os.path.isfile(P) or RG:
								E_AaA = self.CALC_ANO_ANO(E)
								self.GFG_AA_Filtro(E_AaA,P,AA,self.filtros_txt[idx],3,13)

	##############
	# MUNICÍPIOS #
	##############
	def treinar_Municípios(self,municípios,RG=False):
		for mi in (mbar := tqdm(municípios, leave=False, position=1)):
			try: M = self.DADOS.loc[self.DADOS["CodMunicipioIbge"] == int(mi)]
			except: continue
			if len(M) == 0:
				continue
			else:
				mi_nome = M["NomMunicipio"][M.index[0]]
				mi_uf = M["SigUF"][M.index[0]]
				mbar.set_description(f"{mi_nome} [{mi_uf}]")

				if not os.path.exists(f"BDD/ANÁLISES/MUNICÍPIOS/{mi}"):
					os.makedirs(f"BDD/ANÁLISES/MUNICÍPIOS/{mi}")

				if not os.path.exists(f"BDD/GRÁFICOS/MUNICÍPIOS/{mi}"):
					os.makedirs(f"BDD/GRÁFICOS/MUNICÍPIOS/{mi}")

				for anl in (anlbar := tqdm(["Dados","Total","Mês","Mês-a-Mês","Ano-a-Ano"], leave=False, position=2)):
					anlbar.set_description(f"{anl}")
					if anl == "Dados":
						P = f"BDD/ANÁLISES/MUNICÍPIOS/{mi}/{self.ano} - {self.mês} [TOTAL].json"
						if not os.path.isfile(P) or RG:
							self.gerar_dados(M,"M",P)
						P = f"BDD/ANÁLISES/MUNICÍPIOS/{mi}/{self.ano} - {self.mês} [MÊS].json"
						if not os.path.isfile(P) or RG:
							M_MÊS = M.loc[M["Ano-Mês"] == f"{self.ano}-{self.mês}"]
							self.gerar_dados(M_MÊS,"M",P)
					elif anl == "Mês-a-Mês":
						for MM in (MMbar := tqdm(self.filtros, leave=False, position=3)):
							MMbar.set_description(f"{MM}")
							idx = self.filtros.index(MM)
							P = f"BDD/GRÁFICOS/MUNICÍPIOS/{mi}/{self.ano} - {self.mês} [Mês-a-Mês {MM}].png"
							if not os.path.isfile(P) or RG:
								M_MaM = self.CALC_MES_MES(M)
								self.GFG_MM_Filtro(M_MaM,P,MM,self.filtros_txt[idx],3,13)
					elif anl == "Ano-a-Ano":
						for AA in (AAbar := tqdm(self.filtros, leave=False, position=3)):
							AAbar.set_description(f"{AA}")
							idx = self.filtros.index(AA)
							P = f"BDD/GRÁFICOS/MUNICÍPIOS/{mi}/{self.ano} - {self.mês} [Ano-a-Ano {AA}].png"
							if not os.path.isfile(P) or RG:
								M_AaA = self.CALC_ANO_ANO(M)
								self.GFG_AA_Filtro(M_AaA,P,AA,self.filtros_txt[idx],3,13)

if __name__ == "__main__":
	os.system("cls" if os.name == "nt" else "clear")
	print(" ██████╗  █████╗ ██╗      ██████╗ ")
	print("██╔════╝ ██╔══██╗██║     ██╔═══██╗")
	print("██║  ███╗███████║██║     ██║   ██║")
	print("██║   ██║██╔══██║██║     ██║   ██║")
	print("╚██████╔╝██║  ██║███████╗╚██████╔╝")
	print(" ╚═════╝ ╚═╝  ╚═╝╚══════╝ ╚═════╝ ")
	print("Gerador de Análises Livre e Open-source")
	APP = CIDADE_DO_GALO(True)