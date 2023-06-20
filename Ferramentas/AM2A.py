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

# Ano-Mês para Ano
def AM2A(AM):
    A = []
    for x in AM:
        if x[5:] == "1":
            A.append(x[:4])
        else:
            A.append("")
    return A