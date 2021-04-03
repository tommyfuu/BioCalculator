
unitDict = {('mM', 'M'): 0.001, ('g', 'kg'): 0.001}

def convert(input, unitFrom, unitTo):
    if (unitFrom,unitTo) in unitDict:
        return input*unitDict[(unitFrom,unitTo)]
    elif (unitTo,unitFrom) in unitDict:
        return input*(1/unitDict[(unitTo,unitFrom)])
