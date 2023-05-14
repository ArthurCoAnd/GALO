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