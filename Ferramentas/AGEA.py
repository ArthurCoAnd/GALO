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
import pandas as PD

# Ferramentas
from Ferramentas.Filtrar_Dados import Filtrar_Dados as FD

# ADICIONAR GERAÇÃO ESTIMADA ANEEL
def AGEA():
    # Data da última atualização do BDD
    BID_CBF = PD.read_csv("BDD/BID_CBF.csv",sep=";")
    dt_BDD = BID_CBF["dt_ANEEL"][0]

    # Tabela dados de Irradiação por cidade
    IRRA = PD.read_csv("BDD/IBGE/IRRADIAÇÃO.csv",sep=";")

    # Tabela dados ANEEL
    arq_ANEEL = f"BDD/ELENCO/{dt_BDD}.csv"
    ANEEL = PD.read_csv(arq_ANEEL,sep=";",encoding='latin-1',low_memory=False)

    PotGer_ANO = []
    PotInst = ANEEL["MdaPotenciaInstaladaKW"].tolist()
    nome_IRRA = IRRA["NAME"].tolist()
    PotGer_ANO_IRRA = IRRA["ANNUAL"].tolist()
    for i, emp in enumerate(ANEEL["NomMunicipio"].tolist()):
        if emp in nome_IRRA:
            idx = nome_IRRA.index(emp)
            # Pger = Pfv * Irra * Txd * tempo
            PotGer_ANO.append(PotInst[i] * PotGer_ANO_IRRA[idx] * 0.8 * 365 / 1000)
        else: PotGer_ANO.append(0)
    ANEEL["PotGer_ANO"] = PotGer_ANO
    ANEEL.to_csv(arq_ANEEL,index=False,sep=";",encoding='latin-1')

if __name__ == "__main__":
	AGEA()