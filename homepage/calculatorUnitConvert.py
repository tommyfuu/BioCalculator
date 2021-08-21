from django import forms
# from .calculatorUnitConvert import *

unitDict = {('g', 'kg'): 0.001, ('g', 'pg'): 10**12, ('g', 'ng'): 10**9, ('g', 'μg'): 10**6, ('g', 'mg'): 10**3, ('g', 'cg'): 100, ('g', 'Mg'): 10**-6, ('g', 'Gg'): 10**-9, ('g', 'Tg'): 10**-12,
            ('M', 'kM'): 0.001, ('M', 'pM'): 10**12, ('M', 'nM'): 10**9, ('M', 'μM'): 10**6, ('M', 'mM'): 10**3, ('M', 'cM'): 100, ('M', 'MM'): 10**-6, ('M', 'GM'): 10**-9, ('M', 'TM'): 10**-12,
            ('L', 'kL'): 0.001, ('L', 'pL'): 10**12, ('L', 'nL'): 10**9, ('L', 'μL'): 10**6, ('L', 'mL'): 10**3, ('L', 'cL'): 100, ('L', 'ML'): 10**-6, ('L', 'GL'): 10**-9, ('L', 'TL'): 10**-12,
            ('mol', 'kmol'): 0.001, ('mol', 'pmol'): 10**12, ('mol', 'nmol'): 10**9, ('mol', 'μmol'): 10**6, ('mol', 'mmol'): 10**3, ('mol', 'cmol'): 100, ('mol', 'Mmol'): 10**-6, ('mol', 'Gmol'): 10**-9, ('mol', 'Tmol'): 10**-12,
            ('mol/L', 'M'): 1,
            ('g/L', 'kg/L'): 0.001, ('g/L', 'pg/L'): 10**12, ('g/L', 'ng/L'): 10**9, ('g/L', 'μg/L'): 10**6, ('g/L', 'mg/L'): 10**3, ('g/L', 'cg/L'): 100, ('g/L', 'Mg/L'): 10**-6, ('g/L', 'Gg/L'): 10**-9, ('g/L', 'Tg/L'): 10**-12}
unitMolarMassDict = {('kg/L', 'M'): 1}
metricUnits = ['g', 'M', 'L', 'mol']

MASSCHOICES = [('g', 'g'), ('kg', 'kg'), ('pg', 'pg'), ('ng', 'ng'), ('μg', 'μg'),
               ('mg', 'mg'), ('cg', 'cg'), ('Mg', 'Mg'), ('Gg', 'Gg'), ('Tg', 'Tg')]
VOLCHOICES = [('L', 'L'), ('kL', 'kL'), ('pL', 'pL'), ('nL', 'nL'), ('μL', 'μL'),
              ('mL', 'mL'), ('cL', 'cL'), ('ML', 'ML'), ('GL', 'GL'), ('TL', 'TL')]
CONCCHOICESMOLARITY = [('M', 'M'), ('kM', 'kM'), ('pM', 'pM'), ('nM', 'nM'), ('μM', 'μM'),
                       ('mM', 'mM'), ('cM', 'cM'), ('MM', 'MM'), ('GM', 'GM'), ('TM', 'TM'), ('ppm', 'ppm')]
CONCCHOICESMASSPERVOL = [('g/L', 'g/L'), ('kg/L', 'kg/L'),
                         ('mg/L', 'mg/L')]
SOLUTECHOICES = [('g', 'g'), ('kg', 'kg'), ('pg', 'pg'), ('ng', 'ng'), ('μg', 'μg'),
                 ('mg', 'mg'), ('cg', 'cg'), ('Mg',
                                              'Mg'), ('Gg', 'Gg'), ('Tg', 'Tg'),
                 ('L', 'L'), ('kL', 'kL'), ('pL',
                                            'pL'), ('nL', 'nL'), ('μL', 'μL'),
                 ('mL', 'mL'), ('cL', 'cL'), ('ML', 'ML'), ('GL', 'GL'), ('TL', 'TL')]
UNITCHOICES = MASSCHOICES + VOLCHOICES + \
    CONCCHOICESMOLARITY + CONCCHOICESMASSPERVOL + SOLUTECHOICES


class ConversionForm(forms.Form):
    INPUTVALUE = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=True, label=False)
    # INPUTUNIT = forms.CharField(
    #    label='Input Unit', max_length=80, required=True)
    INPUTUNIT = forms.CharField(
        label=False, widget=forms.Select(choices=UNITCHOICES), required=False)
    OUTPUTVALUE = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False, label=False)
    # OUTPUTUNIT = forms.CharField(
    #    label='Output Unit', max_length=80, required=True)
    OUTPUTUNIT = forms.CharField(
        label=False, widget=forms.Select(choices=UNITCHOICES), required=False)
    MOLARMASS = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False, label=False)


def unitTable(inputValue, inputUnit, outputValue, outputUnit, molarMass):
    '''Input the input value, input unit, output unit, and molar mass (if needed) and it will
    calculate the output value'''
    print("All inputs", (inputValue, inputUnit,
                         outputValue, outputUnit, molarMass))
    # calculation of output value
    # while outputValue == None:
    error = ''
    # try:
    if inputValue != None and inputUnit != None and outputUnit != None and molarMass == None:
        outputValue, error = convert(inputValue, inputUnit, outputUnit)
    elif inputValue != None and inputUnit != None and outputUnit != None and molarMass != None:
        print("AAAAAAAH", convert(inputValue, inputUnit, outputUnit, molarMass))
        outputValue, error = convert(
            inputValue, inputUnit, outputUnit, molarMass)
    if type(outputValue) == tuple:
        outputValue = round(outputValue[0], 20)
    elif outputValue != None:
        outputValue = round(outputValue, 20)
    # except Exception as ex:
    #     print(ex)
    #     error = ex.args[0]
        # error = "Need to have an Input Value, Input Unit, Output Unit. Molar Mass is required if converting between mass and moles."
    return inputValue, inputUnit, outputValue, outputUnit, molarMass, error


def convert(input, unitFrom, unitTo, molarMass=0):
    '''Converts the input number from unitFrom to unitTo'''
    # molarity to mass/V vice versa without molar mass
    print("HEHEHEHEHE", (input, unitFrom, unitTo, molarMass))
    error = ''
    if molarMass == None and ((unitFrom[-1] == 'M' and unitTo in [unit[0] for unit in CONCCHOICESMASSPERVOL]) or (unitFrom in [unit[0] for unit in CONCCHOICESMASSPERVOL] and unitTo in [unit[0] for unit in CONCCHOICESMOLARITY])):
        error = 'You can not convert from molarity to mass/volume or vice versa without molar mass'
        return None, error

    if (unitFrom == unitTo):
        return input, error

    # if unitFrom and unitTo in conversion dictionary
    # ERROR HERE! WHEN DOING CONVERSION from M to kg/L, needs to take into account of the molar mass, here we just skip it!
    if (unitFrom, unitTo) in unitDict:
        return float(input) * unitDict[(unitFrom, unitTo)], error
    elif (unitTo, unitFrom) in unitDict:
        return float(input) * (1/unitDict[(unitTo, unitFrom)]), error

    # if unitFrom in [unitPair[0] for unitPair in unitDict.keys]:
    #     for unitPair in unitDict.keys:
    #         if unitFrom == unitFrom[0]:
    #             return convert()

    if (unitFrom, unitTo) in unitMolarMassDict:

        return float(
            input) * float(unitMolarMassDict[(unitFrom, unitTo)])/float(molarMass), error
    elif (unitTo, unitFrom) in unitMolarMassDict:
        return float(
            input) * float((1/unitMolarMassDict[(unitTo, unitFrom)]))*float(molarMass), error

    # if we are converting ppm to M or vice versa
    elif (unitFrom == 'ppm' and unitTo in [unit[0] for unit in CONCCHOICESMOLARITY]) or (unitFrom in [unit[0] for unit in CONCCHOICESMOLARITY] and unitTo == 'ppm'):
        return MToPPM(input, unitFrom, unitTo, molarMass)

    # if we are converting ppm to concentration or vice versa
    elif (unitFrom == 'ppm' and unitTo in [unit[0] for unit in CONCCHOICESMASSPERVOL]) or (unitFrom in [unit[0] for unit in CONCCHOICESMASSPERVOL] and unitTo == 'ppm'):
        return GPerLToPPM(input, unitFrom, unitTo, molarMass)

    # if we are converting g/L to M or vice versa
    elif (unitFrom == 'g/L' and unitTo == 'M') or (unitFrom == 'M' and unitTo == 'g/L'):
        return MToGPerL(input, unitFrom, unitTo, molarMass), error

    # if we are converting mol to g or vice versa
    elif (unitFrom == 'mol' and unitTo == 'g') or (unitFrom == 'g' and unitTo == 'mol'):
        return molToG(input, unitFrom, unitTo, molarMass), error

    # converting some form of mol/L to some form of M or vice versa
    elif ('mol/' in unitFrom and unitFrom[-1] == 'L' and unitTo[-1] == 'M'):
        mols = unitFrom.split('/')[0]
        volume = unitFrom.split('/')[1]
        intermediate = convert(input, mols, 'mol')
        intermediate = convert(intermediate, 'L', volume)
        intermediate = convert(intermediate, 'M', unitTo[-2:])
        return intermediate, error
    elif ('mol/' in unitTo and unitTo[-1] == 'L' and unitFrom[-1] == 'M'):
        mols = unitTo.split('/')[0]
        volume = unitTo.split('/')[1]
        intermediate = convert(input, unitFrom, 'M')
        intermediate = convert(intermediate, volume, 'L')
        intermediate = convert(intermediate, 'mol', mols)
        return intermediate, error

    # converting some form of g/L to some form of M or vice versa
    elif ('g/' in unitFrom and unitFrom[-1] == 'L' and unitTo[-1] == 'M'):
        mass = unitFrom.split('/')[0]
        volume = unitFrom.split('/')[1]
        intermediate = convert(input, mass, 'mol', molarMass)[0]
        intermediate = convert(intermediate, 'L', volume)[0]
        intermediate = convert(intermediate, 'M', unitTo)[0]
        return intermediate, error
    elif ('g/' in unitTo and unitTo[-1] == 'L' and unitFrom[-1] == 'M'):
        mass = unitTo.split('/')[0]
        volume = unitTo.split('/')[1]
        intermediate = convert(input, unitFrom, 'M')[0]
        intermediate = convert(intermediate, volume, 'L')[0]
        intermediate = convert(intermediate, 'mol', mass, molarMass)
        return intermediate, error

    # if you can convert unitFrom to metric base and then to unitTo
    elif unitFrom[1:] in metricUnits:
        standard = convert(input, unitFrom, unitFrom[1:], molarMass)
        return convert(standard[0], unitFrom[1:], unitTo, molarMass), error

    # if you can convert To to metric base and then to unitTo
    elif unitTo[1:] in metricUnits:
        standard = convert(input, unitTo, unitTo[1:], molarMass)[0]
        return convert(standard, unitFrom, unitTo[1:], molarMass), error

    # if the inputs do not match any of the above cases, print an error message
    else:
        # Molarity to Volume
        if (unitTo[-1:] == 'L' and unitFrom[-1:] == 'M') or (unitTo[-1:] == 'M' and unitFrom[-1:] == 'L'):
            error = 'You can not convert from volume to molarity or vice versa'
        # Mass to Molarity
        elif (unitTo[-1] == 'g' and unitFrom[-1] == 'M') or (unitTo[-1] == 'M' and unitFrom[-1] == 'g'):
            error = 'You can not convert from mass to molarity or vice versa'
        # Mols to Molarity
        elif (unitTo[-3:] == 'mol' and unitFrom[-1] == 'M') or (unitTo[-1] == 'M' and unitFrom[-3:] == 'mol'):
            error = 'You can not convert from moles to molarity or vice versa'
        # Unrecognized error
        else:
            error = 'Unit conversion calculator has no case to handle this conversion'
        return None, error


def MToPPM(input, unitFrom, unitTo, molarMass):
    '''Converts M to ppm and vice versa, but you have to know the molar mass'''
    if molarMass == (None or 0):
        return None, 'Convert between ppm and some molarity unit without molar mass is not viable.'
    elif unitFrom == 'ppm':
        unitFrom = 'M'
        input = float(input) * 0.001 * float((1/molarMass))
        return convert(input, unitFrom, unitTo, molarMass)
    elif unitTo == 'ppm':
        unitTo = 'M'
        input = float(input) * 1000 * float(molarMass)
        return convert(input, unitFrom, unitTo, molarMass)
    # return tempOut
    # if tempOut[-1] != '':
    #     return None, tempOut[-1]
    # else:
    #     return tempOut[:-1]


def GPerLToPPM(input, unitFrom, unitTo, molarMass):
    '''Converts g/L to ppm and vice versa, but you have to know the molar mass'''
    if unitFrom == 'ppm':
        unitFrom = 'g/L'
        input = float(input) * 0.001
        return convert(input, unitFrom, unitTo, molarMass)
    elif unitTo == 'ppm':
        unitTo = 'g/L'
        input = float(input) * 1000
        return convert(input, unitFrom, unitTo, molarMass)


def molToG(input, unitFrom, unitTo, molarMass):
    '''Converts mol to g and vice versa, but you have to know the molar mass'''
    if unitFrom == 'mol' and unitTo == 'g':
        return float(input) * float(molarMass)
    elif unitFrom == 'g' and unitTo == 'mol':
        return float(input) * float((1/molarMass))


def MToGPerL(input, unitFrom, unitTo, molarMass):
    '''Converts M to g/L and vice versa, but you have to know the molar mass'''
    if unitFrom == 'g/L' and unitTo == 'M':
        return float(input) * float((1/molarMass))
    elif unitFrom == 'M' and unitTo == 'g/L':
        return float(input) * float(molarMass)
