from django import forms
# from .calculatorUnitConvert import *

unitDict = {('g', 'kg'): 0.001, ('g', 'pg'): 10**12, ('g', 'ng'): 10**9, ('g', 'μg'): 10**6, ('g', 'mg'): 10**3, ('g', 'cg'): 100, ('g', 'Mg'): 10**-6, ('g', 'Gg'): 10**-9, ('g', 'Tg'): 10**-12,
            ('M', 'kM'): 0.001, ('M', 'pM'): 10**12, ('M', 'nM'): 10**9, ('M', 'μM'): 10**6, ('M', 'mM'): 10**3, ('M', 'cM'): 100, ('M', 'MM'): 10**-6, ('M', 'GM'): 10**-9, ('M', 'TM'): 10**-12,
            ('L', 'kL'): 0.001, ('L', 'pL'): 10**12, ('L', 'nL'): 10**9, ('L', 'μL'): 10**6, ('L', 'mL'): 10**3, ('L', 'cL'): 100, ('L', 'ML'): 10**-6, ('L', 'GL'): 10**-9, ('L', 'TL'): 10**-12,
            ('mol', 'kmol'): 0.001, ('mol', 'pmol'): 10**12, ('mol', 'nmol'): 10**9, ('mol', 'μmol'): 10**6, ('mol', 'mmol'): 10**3, ('mol', 'cmol'): 100, ('mol', 'Mmol'): 10**-6, ('mol', 'Gmol'): 10**-9, ('mol', 'Tmol'): 10**-12,
            ('mol/L', 'M'): 1}
unitMolarMassDict = {('kg/L', 'M'): 1}
metricUnits = ['g', 'M', 'L', 'mol']


class ConversionForm(forms.Form):
    INPUTVALUE = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=True, label='Input Value')
    INPUTUNIT = forms.CharField(
        label='Input Unit', max_length=80, required=True)
    OUTPUTVALUE = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False, label='Output Value')
    OUTPUTUNIT = forms.CharField(
        label='Output Unit', max_length=80, required=True)
    MOLARMASS = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False, label='Molar Mass')


def unitTable(inputValue, inputUnit, outputValue, outputUnit, molarMass):
    '''Input the input value, input unit, output unit, and molar mass (if needed) and it will
    calculate the output value'''

    # calculation of output value
    # while outputValue == None:
    error = False
    try:
        if inputValue != None and inputUnit != None and outputUnit != None and molarMass == None:
            outputValue = convert(inputValue, inputUnit, outputUnit)
        elif inputValue != None and inputUnit != None and outputUnit != None and molarMass != None:
            outputValue = convert(inputValue, inputUnit, outputUnit, molarMass)
    except:
        error = True
        print("Need to have an Input Value, Input Unit, Output Unit. Molar Mass is required if converting between mass and moles.")
    return inputValue, inputUnit, outputValue, outputUnit, molarMass, error


def convert(input, unitFrom, unitTo, molarMass=0):
    '''Converts the input number from unitFrom to unitTo'''
    print("CONFUZZLED")
    if (unitFrom == unitTo):
        return input

    # if unitFrom and unitTo in conversion dictionary
    # ERROR HERE! WHEN DOING CONVERSION from M to kg/L, needs to take into account of the molar mass, here we just skip it!
    if (unitFrom, unitTo) in unitDict:
        return input * unitDict[(unitFrom, unitTo)]
    elif (unitTo, unitFrom) in unitDict:
        return float(input) * (1/unitDict[(unitTo, unitFrom)])

    if (unitFrom, unitTo) in unitMolarMassDict:
        print(molarMass)
        return input * unitMolarMassDict[(unitFrom, unitTo)]/molarMass
    elif (unitTo, unitFrom) in unitMolarMassDict:
        return float(input) * (1/unitMolarMassDict[(unitTo, unitFrom)])*molarMass

    # if we are converting ppm to A or vice versa
    elif (unitFrom == 'ppm' and unitTo == 'M') or (unitFrom == 'M' and unitTo == 'ppm'):
        return MToPPM(input, unitFrom, unitTo, molarMass)

    # if we are converting g/L to M or vice versa
    elif (unitFrom == 'g/L' and unitTo == 'M') or (unitFrom == 'M' and unitTo == 'g/L'):
        print("XACAVCX")
        return MToGPerL(input, unitFrom, unitTo, molarMass)

    # if we are converting mol to g or vice versa
    elif (unitFrom == 'mol' and unitTo == 'g') or (unitFrom == 'g' and unitTo == 'mol'):
        return molToG(input, unitFrom, unitTo, molarMass)

    # converting some form of mol/L to some form of M or vice versa
    elif ('mol/' in unitFrom and unitFrom[-1] == 'L' and unitTo[-1] == 'M'):
        mols = unitFrom.split('/')[0]
        volume = unitFrom.split('/')[1]
        intermediate = convert(input, mols, 'mol')
        intermediate = convert(intermediate, 'L', volume)
        intermediate = convert(intermediate, 'M', unitTo[-2:])
        return intermediate
    elif ('mol/' in unitTo and unitTo[-1] == 'L' and unitFrom[-1] == 'M'):
        mols = unitTo.split('/')[0]
        volume = unitTo.split('/')[1]
        intermediate = convert(input, unitFrom, 'M')
        intermediate = convert(intermediate, volume, 'L')
        intermediate = convert(intermediate, 'mol', mols)
        return intermediate

    # converting some form of g/L to some form of M or vice versa
    elif ('g/' in unitFrom and unitFrom[-1] == 'L' and unitTo[-1] == 'M'):
        mass = unitFrom.split('/')[0]
        volume = unitFrom.split('/')[1]
        intermediate = convert(input, mass, 'mol', molarMass)
        intermediate = convert(intermediate, 'L', volume)
        intermediate = convert(intermediate, 'M', unitTo)
        return intermediate
    elif ('g/' in unitTo and unitTo[-1] == 'L' and unitFrom[-1] == 'M'):
        mass = unitTo.split('/')[0]
        volume = unitTo.split('/')[1]
        intermediate = convert(input, unitFrom, 'M')
        intermediate = convert(intermediate, volume, 'L')
        intermediate = convert(intermediate, 'mol', mass, molarMass)
        return intermediate

    # if you can convert unitFrom to metric base and then to unitTo
    elif unitFrom[1:] in metricUnits:
        standard = convert(input, unitFrom, unitFrom[1:], molarMass)
        return convert(standard, unitFrom[1:], unitTo, molarMass)

    # if you can convert To to metric base and then to unitTo
    elif unitTo[1:] in metricUnits:
        standard = convert(input, unitTo, unitTo[1:], molarMass)
        return convert(standard, unitFrom, unitTo[1:], molarMass)


def MToPPM(input, unitFrom, unitTo, molarMass):
    '''Converts M to ppm and vice versa, but you have to know the 
    molar mass'''
    if unitFrom == 'ppm' and unitTo == 'M':
        return input * 0.001 * (1/molarMass)
    elif unitFrom == 'M' and unitTo == 'ppm':
        return input * molarMass * 1000


def molToG(input, unitFrom, unitTo, molarMass):
    '''Converts mol to g and vice versa, but you have to know the 
    molar mass'''
    if unitFrom == 'mol' and unitTo == 'g':
        return input * molarMass
    elif unitFrom == 'g' and unitTo == 'mol':
        return input * (1/molarMass)


def MToGPerL(input, unitFrom, unitTo, molarMass):
    '''Converts M to g/L and vice versa, but you have to know the molar mass'''
    if unitFrom == 'g/L' and unitTo == 'M':
        return input * (1/molarMass)
    elif unitFrom == 'M' and unitTo == 'g/L':
        return input * molarMass
