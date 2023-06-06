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

def Dia_Da_Semana(dia):
    d = dia.date().isoweekday()
    if d == 1:
        return 'Segunda-feira'
    elif d == 2:
        return 'Terça-feira'
    elif d == 3:
        return 'Quarta-feira'
    elif d == 4:
        return 'Quinta-feira'
    elif d == 5:
        return 'Sexta-feira'
    elif d == 6:
        return 'Sábado'
    else:
        return 'Domingo'