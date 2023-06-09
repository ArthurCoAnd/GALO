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
import os

# Módulos
from Módulos.ARENA_MRV import ARENA_MRV
from Módulos.CIDADE_DO_GALO import CIDADE_DO_GALO
from Módulos.GALO_NA_VEIA import GALO_NA_VEIA
from Módulos.ITATIAIA import ITATIAIA
from Módulos.SEDE_DE_LOURDES import SEDE_DE_LOURDES

def GALO():
	try: SEDE_DE_LOURDES()
	except: pass
	try: GALO_NA_VEIA()
	except: pass
	try: CIDADE_DO_GALO()
	except: pass
	try: ARENA_MRV()
	except: pass
	try: ITATIAIA()
	except: pass

if __name__ == "__main__":
	os.system("cls" if os.name == "nt" else "clear")
	print(" ██████╗  █████╗ ██╗      ██████╗ ")
	print("██╔════╝ ██╔══██╗██║     ██╔═══██╗")
	print("██║  ███╗███████║██║     ██║   ██║")
	print("██║   ██║██╔══██║██║     ██║   ██║")
	print("╚██████╔╝██║  ██║███████╗╚██████╔╝")
	print(" ╚═════╝ ╚═╝  ╚═╝╚══════╝ ╚═════╝ ")
	print("Gerador de Análises Livre e Open-source")
	GALO()