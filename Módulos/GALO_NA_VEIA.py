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
parent = os.path.abspath('.')
sys.path.insert(1, parent)

# Bibliotecas
from gsheets import Sheets
import json

# Ferramentas
from Ferramentas.Título import Título

def GALO_NA_VEIA():
	Título("GALO NA VEIA")

	with open("BDD/CFG.json") as f:
		CFG = json.load(f)

	planilha = f"https://docs.google.com/spreadsheets/d/{CFG['planilha_id']}"

	sheets = Sheets.from_files("GALO.json")
	sheet = sheets.get(planilha)
	ATLETICANOS = sheet[1651774562].to_frame()
	ATLETICANOS.to_csv("BDD/ATLETICANOS.csv",sep=";")

if __name__ == "__main__":
	os.system('cls' if os.name == 'nt' else 'clear')
	print(" ██████╗  █████╗ ██╗      ██████╗ ")
	print("██╔════╝ ██╔══██╗██║     ██╔═══██╗")
	print("██║  ███╗███████║██║     ██║   ██║")
	print("██║   ██║██╔══██║██║     ██║   ██║")
	print("╚██████╔╝██║  ██║███████╗╚██████╔╝")
	print(" ╚═════╝ ╚═╝  ╚═╝╚══════╝ ╚═════╝ ")
	print("Gerador de Análises Livre e Open-source")
	GALO_NA_VEIA()