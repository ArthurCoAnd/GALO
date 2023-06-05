# Bibliotecas
import os
import pandas as PD
import sys

parent = os.path.abspath('.')
sys.path.insert(1, parent)

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
            PotGer_ANO.append(PotInst[i] * PotGer_ANO_IRRA[idx] * 0.8 * 30 * 12 / 1000)
        else: PotGer_ANO.append(0)
    ANEEL["PotGer_ANO"] = PotGer_ANO
    ANEEL.to_csv(arq_ANEEL,index=False,sep=";",encoding='latin-1')

if __name__ == "__main__":
	AGEA()