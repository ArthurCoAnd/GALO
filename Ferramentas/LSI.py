from si_prefix import split
from si_prefix import si_format as SI

def LSI(x):
    xi = x/10**split(x)[1]
    if x <= 1e3:
        return SI(x,0)
    elif xi <= 10:
        return SI(x,2)
    elif xi <= 100:
        return SI(x,1)
    elif xi <= 1000:
        return SI(x,0)
    else:
        return SI(x,1)