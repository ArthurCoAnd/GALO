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
from bs4 import BeautifulSoup as BS
from datetime import datetime as DT
import pandas as PD
import requests
import wget

# Ferramentas
from Ferramentas.AGEA import AGEA
from Ferramentas.Título import Título

def SEDE_DE_LOURDES():
	Título("SEDE DE LOURDES")

	# Data da última atualização do BDD
	BID_CBF = PD.read_csv("BDD/BID_CBF.csv",sep=";")
	dt_BDD = BID_CBF["dt_ANEEL"][0]

	# URL site dados abertos da ANEEL
	url_ANEEL = "https://dadosabertos.aneel.gov.br/dataset/relacao-de-empreendimentos-de-geracao-distribuida"

	# Download informações do site
	try:
		html_ANEEL = requests.get(url_ANEEL).text
		site_ANEEL = BS(html_ANEEL,"lxml")

		# Data da última atualização dos dados da ANEEL
		dt_ANEEL = site_ANEEL.find(class_="automatic-local-datetime").get("data-datetime")[:10]

		# URL para download da última atualização dos dados da ANEEL
		url_ATL = site_ANEEL.find_all(class_="resource-url-analytics")
		url_ATL = url_ATL[1].get("href")
		# https://dadosabertos.aneel.gov.br/dataset/5e0fafd2-21b9-4d5b-b622-40438d40aba2/resource/b1bd71e7-d0ad-4214-9053-cbd58e9564a7/download/empreendimento-geracao-distribuida.csv

		print(f"Última Atualização:")
		print(f"ANEEL  {dt_ANEEL}")
		print(f"BDD    {dt_BDD}")

		# Virificar necessidade de atualizar BDD
		if dt_BDD != dt_ANEEL:
			Título("Banco de Dados DESATUALIZADO","*",1)
			try:
				# Download última atualização de dados da ANEEL
				try:
					print(f"Download: {url_ATL}")
					wget.download(url_ATL, f"BDD/ELENCO/{dt_ANEEL}.csv")

					# Tratamento dos novos dados - Substituir "," por "."
					try:
						arq = open(f"BDD/ELENCO/{dt_ANEEL}.csv","rt")
						dados = arq.read()
						dados = dados.replace(",",".")
						arq.close()
						arq = open(f"BDD/ELENCO/{dt_ANEEL}.csv","wt")
						arq.write(dados)
						arq.close()

						# Registrando nova atualização de BDD
						try:
							agora = str(DT.now())[:19]
							ATL = PD.DataFrame([[dt_ANEEL,agora]],columns=["dt_ANEEL","dt_BDD"])
							BID_CBF = PD.concat([ATL,BID_CBF])
							BID_CBF.to_csv("BDD/BID_CBF.csv", sep=";", index=False)

                            # Calcular e adicionar a geração estimada aos dados
							try: AGEA()
							except: Título("ERRO - FALHA AO CALCULAR GERAÇÃO ESTIMADA","*",1)

							# Remover dados antigos
							# try:
							# 	dts = REG_ATL["dt_ANEEL"].to_list()[2:-1]
							# 	for d in dts:
							# 		if os.path.exists(f"BDD/ANEEL/{d}.csv"):
							# 			os.remove(f"BDD/ANEEL/{d}.csv")
							# except:
							# 	Título("ERRO - FALHA AO REMOVER DADOS ANTIGOS","*")
						except:
							Título("ERRO - FALHA NO REGISTRO DE NOVA ATUALIZAÇÃO","*",1)
					except:
						Título("ERRO - FALHA NO TRATAMENTO DOS NOVOS DADOS","*",1)
						
					Título("Banco de Dados ATUALIZADO","+",1)
				except:
					Título("ERRO - FALHA NO DOWNLOAD DA ATUALIZAÇÃO","*",1)
			except:
				Título("ERRO - FALHA NA ATUALIZAÇÃO","*",1)
		else:
			Título("Banco de Dados ATUALIZADO","+",1)
	except:
		Título("ERRO - FALHA NA OBTENÇÃO DOS DADOS DA ANEEL","*",1)

if __name__ == "__main__":
	os.system("cls" if os.name == "nt" else "clear")
	print(" ██████╗  █████╗ ██╗      ██████╗ ")
	print("██╔════╝ ██╔══██╗██║     ██╔═══██╗")
	print("██║  ███╗███████║██║     ██║   ██║")
	print("██║   ██║██╔══██║██║     ██║   ██║")
	print("╚██████╔╝██║  ██║███████╗╚██████╔╝")
	print(" ╚═════╝ ╚═╝  ╚═╝╚══════╝ ╚═════╝ ")
	print("Gerador de Análises Livre e Open-source")
	SEDE_DE_LOURDES()