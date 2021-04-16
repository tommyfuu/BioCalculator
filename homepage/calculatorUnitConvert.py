
unitDict = {('g', 'kg'): 0.001, ('g', 'pg'): 10**12, ('g', 'ng'): 10**9, ('g', 'μg'): 10**6, ('g', 'mg'): 10**3, ('g', 'cg'): 100, ('g', 'Mg'): 10**-6, ('g', 'Gg'): 10**-9, ('g', 'Tg'): 10**-12,
            ('M', 'kM'): 0.001, ('M', 'pM'): 10**12, ('M', 'nM'): 10**9, ('M', 'μM'): 10**6, ('M', 'mM'): 10**3, ('M', 'cM'): 100, ('M', 'MM'): 10**-6, ('M', 'GM'): 10**-9, ('M', 'TM'): 10**-12,
            ('L', 'kL'): 0.001, ('L', 'pL'): 10**12, ('L', 'nL'): 10**9, ('L', 'μL'): 10**6, ('L', 'mL'): 10**3, ('L', 'cL'): 100, ('L', 'ML'): 10**-6, ('L', 'GL'): 10**-9, ('L', 'TL'): 10**-12,
            ('mol', 'kmol'): 0.001, ('mol', 'pmol'): 10**12, ('mol', 'nmol'): 10**9, ('mol', 'μmol'): 10**6, ('mol', 'mmol'): 10**3, ('mol', 'cmol'): 100, ('mol', 'Mmol'): 10**-6, ('mol', 'Gmol'): 10**-9, ('mol', 'Tmol'): 10**-12,
            ('mol/L', 'M'): 1, ('kg/L', 'M'): 1000}
metricUnits = ['g', 'M', 'L']


def convert(input, unitFrom, unitTo, molarMass=0):
    '''Converts the input number from unitFrom to unitTo'''
    if (unitFrom == unitTo):
        return input

    # if unitFrom and unitTo in conversion dictionary
    if (unitFrom, unitTo) in unitDict:
        return input*unitDict[(unitFrom, unitTo)]
    elif (unitTo, unitFrom) in unitDict:
        return input*(1/unitDict[(unitTo, unitFrom)])

    # if we are converting M to ppm or vice versa
    elif (unitFrom == 'ppm' and unitTo == 'M') or (unitFrom == 'M' and unitTo == 'ppm'):
        return MToPPM(input, unitFrom, unitTo, molarMass)

    elif (unitFrom == 'g/L' and unitTo == 'M') or (unitFrom == 'M' and unitTo == 'g/L'):
        return MToGPerL(input, unitFrom, unitTo, molarMass)
    
    # converting some form of mol/L to some form of M or vice versa
    elif ('/' in unitFrom and unitFrom[-1]=='L' and unitTo[-1]=='M'):
        mols = unitFrom.split('/')[0]
        volume = unitFrom.split('/')[1]
        intermediate = convert(input, mols, 'mol')
        intermediate = convert(intermediate, 'L', volume)
        intermediate = convert(intermediate, 'M', unitTo[-2:])
        return intermediate
    elif ('/' in unitTo and unitFrom[-1]=='M' and unitTo[-1]=='L'):
        mols = unitTo.split('/')[0]
        volume = unitTo.split('/')[1]
        intermediate = convert(input, unitFrom, 'M')
        intermediate = convert(intermediate, volume, 'L')
        intermediate = convert(intermediate, 'mol', mols)
        return intermediate

    # if you can convert unitFrom to metric base and then to unitTo
    elif unitFrom[-1] in metricUnits:
        standard = convert(input, unitFrom, unitFrom[-1])
        return convert(standard, unitFrom[-1], unitTo)


def MToPPM(input, unitFrom, unitTo, molarMass):
    '''Converts M to ppm and vice versa, but you have to know the 
    molar mass'''
    if unitFrom == 'ppm' and unitTo == 'M':
        return input * 0.001 * (1/molarMass)
    elif unitFrom == 'M' and unitTo == 'ppm':
        return input * molarMass * 1000


def MToGPerL(input, unitFrom, unitTo, molarMass):
    '''Converts M to g/L and vice versa, but you have to know the molar mass'''
    if unitFrom == 'g/L' and unitTo == 'M':
        return input * (1/molarMass)
    elif unitFrom == 'M' and unitTo == 'g/L':
        return input * molarMass
