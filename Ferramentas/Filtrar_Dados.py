import pandas as pd

def Filtrar_Dados(D):
    filtro_colunas = []

    filtro_colunas.append("DatGeracaoConjuntoDados")
    filtro_colunas.append("AnmPeriodoReferencia")
    filtro_colunas.append("NumCNPJDistribuidora")
    # filtro_colunas.append("SigAgente")
    filtro_colunas.append("NomAgente")
    filtro_colunas.append("CodClasseConsumo")
    filtro_colunas.append("DscClasseConsumo")
    filtro_colunas.append("CodSubGrupoTarifario")
    filtro_colunas.append("DscSubGrupoTarifario")
    filtro_colunas.append("codUFibge")
    # filtro_colunas.append("SigUF")
    filtro_colunas.append("codRegiao")
    filtro_colunas.append("NomRegiao")
    filtro_colunas.append("CodMunicipioIbge")
    # filtro_colunas.append("NomMunicipio")
    # filtro_colunas.append("CodCEP")
    # filtro_colunas.append("SigTipoConsumidor")
    filtro_colunas.append("NumCPFCNPJ")
    filtro_colunas.append("NomeTitularEmpreendimento")
    # filtro_colunas.append("CodEmpreendimento")
    # filtro_colunas.append("DthAtualizaCadastralEmpreend")
    filtro_colunas.append("SigModalidadeEmpreendimento")
    filtro_colunas.append("DscModalidadeHabilitado")
    # filtro_colunas.append("QtdUCRecebeCredito")
    # filtro_colunas.append("SigTipoGeracao")
    filtro_colunas.append("DscFonteGeracao")
    filtro_colunas.append("DscPorte")
    # filtro_colunas.append("MdaPotenciaInstaladaKW")
    filtro_colunas.append("NumCoordNEmpreendimento")
    filtro_colunas.append("NumCoordEEmpreendimento")
    filtro_colunas.append("NomSubEstacao")
    filtro_colunas.append("NumCoordESub")
    filtro_colunas.append("NumCoordNSub")

    D = D.drop(columns=filtro_colunas)

    D['DthAtualizaCadastralEmpreend'] = pd.to_datetime(D['DthAtualizaCadastralEmpreend'])

    return D