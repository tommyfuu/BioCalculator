from django import forms
from .calculatorUnitConvert import *

# given a VOLUME of liquid,CONCENTRATION of this liquid, and TARGET concentration
# calculate the VOLUME of water needed to add

MASSCHOICES = [('g', 'g'), ('kg', 'kg'), ('pg', 'pg'), ('ng', 'ng'), ('μg', 'μg'),
               ('mg', 'mg'), ('cg', 'cg'), ('Mg', 'Mg'), ('Gg', 'Gg'), ('Tg', 'Tg')]
VOLCHOICES = [('L', 'L'), ('kL', 'kL'), ('pL', 'pL'), ('nL', 'nL'), ('μL', 'μL'),
              ('mL', 'mL'), ('cL', 'cL'), ('ML', 'ML'), ('GL', 'GL'), ('TL', 'TL')]
CONCCHOICES = [('M', 'M'), ('kM', 'kM'), ('pM', 'pM'), ('nM', 'nM'), ('μM', 'μM'),
               ('mM', 'mM'), ('cM', 'cM'), ('MM', 'MM'), ('GM', 'GM'), ('TM', 'TM'), ('g/L', 'g/L'), ('kg/L', 'kg/L')]
SOLUTECHOICES = [('g', 'g'), ('kg', 'kg'), ('pg', 'pg'), ('ng', 'ng'), ('μg', 'μg'),
                 ('mg', 'mg'), ('cg', 'cg'), ('Mg',
                                              'Mg'), ('Gg', 'Gg'), ('Tg', 'Tg'),
                 ('L', 'L'), ('kL', 'kL'), ('pL',
                                            'pL'), ('nL', 'nL'), ('μL', 'μL'),
                 ('mL', 'mL'), ('cL', 'cL'), ('ML', 'ML'), ('GL', 'GL'), ('TL', 'TL')]

# for checking whether to use molar mass
NORMALCONCOPTIONS = ['kg/L', 'g/L']
MOLARCONCOPTIONS = ['M', 'kM', 'pM', 'nM', 'μM', 'mM', 'cM', 'MM', 'GM', 'TM']


def checkWhetherUseMolarMass(inputConcUnit, outputConcUnit):
    if (inputConcUnit in NORMALCONCOPTIONS) and (outputConcUnit in MOLARCONCOPTIONS):
        return True
    if (outputConcUnit in NORMALCONCOPTIONS) and (inputConcUnit in MOLARCONCOPTIONS):
        return True
    return False


class DilutionForm(forms.Form):
    INPUTVOL = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False, label='Input Liquid Volume')
    INPUTCONC = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False, label='Input Liquid Concentration')
    INPUTSOLUTE = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False, label='Input Solute Mass')
    FINALVOL = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False, label='Final Liquid Volume')
    FINALCONC = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False, label='Final Liquid Concentration')
    INPUTSOLUTEUNIT = forms.CharField(
        label='Input solute unit (Volume or mass)', widget=forms.Select(choices=MASSCHOICES), required=False)
    MOLARMASS = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False, label='Molar Mass (kg/mol)')
    INPUTVOLUNIT = forms.CharField(
        label='Input volume unit', widget=forms.Select(choices=VOLCHOICES), required=False)
    INPUTCONCUNIT = forms.CharField(
        label='Input concentration unit', widget=forms.Select(choices=CONCCHOICES), required=False)
    FINALVOLUNIT = forms.CharField(
        label='Final volume unit', widget=forms.Select(choices=VOLCHOICES), required=False)
    FINALCONCUNIT = forms.CharField(
        label='Final concentration unit', widget=forms.Select(choices=CONCCHOICES), required=False)
    OUTPUTVOLUNIT = forms.CharField(
        label='Displayed volume unit', widget=forms.Select(choices=VOLCHOICES), required=False)
    OUTPUTCONCUNIT = forms.CharField(
        label='Displayed concentration unit', widget=forms.Select(choices=CONCCHOICES), required=False)
    OUTPUTSOLUTEUNIT = forms.CharField(
        label='Displayed solute unit', widget=forms.Select(choices=MASSCHOICES), required=False)


def dilutionHelper(inputConc, finalVol, finalConc):
    'first convert to g, ml, and Molar'
    inputVol = (finalVol * finalConc) / inputConc
    inputSolute = inputVol * inputConc
    waterVol = finalVol - inputVol
    return inputVol, waterVol, inputSolute


def dilutionTable(inputVol, inputConc, finalVol, finalConc, addedSoluteVol, waterVol, molarMass, checkWhetherUseMolarMassBool, outputConcUnit, outputSoluteUnit, outputVolUnit):
    '''Assumptions
    1: the given input solute dissolves in the input
    liquid 100%
    2: diluting, not increasing concentration'''
    error = False
    # conversion among the four variables inputVol, inputConc, finalVol, finalConc
    if addedSoluteVol == None:
        finalSoluteInKG = convert(finalVol, outputVolUnit, 'L')*convert(
            finalConc, outputConcUnit, 'kg/L', molarMass)
        inputSoluteInKG = convert(inputVol, outputVolUnit, 'L')*convert(
            inputConc, outputConcUnit, 'kg/L', molarMass)
        addedSoluteVol = convert(
            finalSoluteInKG-inputSoluteInKG, 'kg', outputSoluteUnit, molarMass)
        print(addedSoluteVol)
    if finalVol == None:
        if not checkWhetherUseMolarMassBool:
            finalSolute = inputVol * inputConc + addedSoluteVol
            finalVol = finalSolute/finalConc
        else:
            finalSolute = inputVol * inputConc*molarMass + addedSoluteVol
            finalVol = finalSolute/(finalConc*molarMass)
    if waterVol == None:
        waterVol = finalVol-inputVol

    return inputVol, inputConc, finalVol, finalConc, waterVol, error


def upConcentrationTable(inputVol, inputConc, finalVol, finalConc, addedSoluteVol, addedWaterVol, molarMass, checkWhetherUseMolarMassBool, outputConcUnit, outputSoluteUnit, outputVolUnit):
    '''Assumptions
    1: the given output solute concentration allows the solute to dissolve
     in the input liquid 100%
    2: diluting, not increasing concentration
    3: assume good unit conversion: g vs. ml; kg vs L'''
    error = False
    if addedSoluteVol == None:
        # if not checkWhetherUseMolarMassBool:
        #     addedSoluteVol = finalConc*finalVol-inputVol*inputConc
        # else:
        print("PRINTING ADDED SOLUTE VOL")
        print(convert((finalVol-inputVol), outputVolUnit, 'L'))
        print(convert(finalConc, outputConcUnit, 'kg/L', molarMass))
        print(convert(inputConc, outputConcUnit, 'kg/L', molarMass))
        finalSoluteInKG = convert(finalVol, outputVolUnit, 'L')*convert(
            finalConc, outputConcUnit, 'kg/L', molarMass)
        inputSoluteInKG = convert(inputVol, outputVolUnit, 'L')*convert(
            inputConc, outputConcUnit, 'kg/L', molarMass)
        addedSoluteVol = convert(
            finalSoluteInKG-inputSoluteInKG, 'kg', outputSoluteUnit, molarMass)
        print(addedSoluteVol)
    if finalVol == None:
        if not checkWhetherUseMolarMassBool:
            finalSolute = inputVol * inputConc + addedSoluteVol
            finalVol = finalSolute/finalConc
        else:
            finalSolute = inputVol * inputConc*molarMass + addedSoluteVol
            finalVol = finalSolute/(finalConc*molarMass)
    if addedWaterVol == None:
        addedWaterVol = finalVol-inputVol
    return inputVol, inputConc, finalVol, finalConc, addedSoluteVol, addedWaterVol, error


def unitConversion(inputVol, inputVolUnit, inputConc, inputConcUnit, inputSolute, inputSoluteUnit, molarMass, finalVol, finalVolUnit, finalConc, finalConcUnit, outputVolUnit, outputConcUnit, outputSoluteUnit):
    '''convert unit for easier calculation'''
    if inputVol != None:
        inputVolRightUnit = convert(inputVol, inputVolUnit, outputVolUnit)
    else:
        inputVolRightUnit = None
    if inputConc != None:
        inputConcRightUnit = convert(
            inputConc, inputConcUnit, outputConcUnit, molarMass)
    else:
        inputConcRightUnit = None
    if finalVol != None:
        finalVolRightUnit = convert(finalVol, finalVolUnit, outputVolUnit)
    else:
        finalVolRightUnit = None
    if finalConc != None:
        finalConcRightUnit = convert(
            finalConc, finalConcUnit, outputConcUnit, molarMass)
    else:
        finalConcRightUnit = None

    # solute
    if inputSolute != None:
        if not checkWhetherUseMolarMass(inputConcUnit, outputConcUnit):
            # not gonna use molar mass
            inputSoluteRightUnit = convert(
                inputSolute, inputSoluteUnit, outputSoluteUnit)
        else:
            inputSoluteRightUnit = convert(
                inputSolute, inputSoluteUnit, outputSoluteUnit, molarMass)
    else:
        inputSoluteRightUnit = None
    return inputVolRightUnit, inputConcRightUnit, finalVolRightUnit, finalConcRightUnit, inputSoluteRightUnit


def changeConcentrationTable(inputVol, inputVolUnit, inputConc, inputConcUnit, inputSolute, inputSoluteUnit, molarMass, finalVol, finalVolUnit, finalConc, finalConcUnit, outputVolUnit, outputConcUnit, outputSoluteUnit, addedSoluteVol, addedWaterVol):
    """wrapper function for changing concentration"""
    if inputVol != None:
        inputVol = float(inputVol)
    if inputConc != None:
        inputConc = float(inputConc)
    if inputSolute != None:
        inputSolute = float(inputSolute)
    if molarMass != None:
        molarMass = float(molarMass)
    if finalVol != None:
        finalVol = float(finalVol)
    if finalConc != None:
        finalConc = float(finalConc)
    checkWhetherUseMolarMassBool = checkWhetherUseMolarMass(
        inputConcUnit, outputConcUnit)  # if true, then we use molar mass
    inputVol, inputConc, finalVol, finalConc, inputSolute = unitConversion(
        inputVol, inputVolUnit, inputConc, inputConcUnit, inputSolute, inputSoluteUnit, molarMass, finalVol, finalVolUnit, finalConc, finalConcUnit, outputVolUnit, outputConcUnit, outputSoluteUnit)
    if finalConc == None:
        return inputVol, inputConc, inputSolute, finalVol, finalConc, 0, 0, outputVolUnit, outputConcUnit, outputSoluteUnit, True
    if inputVol == None:
        inputVol = 0

    if molarMass == 0:
        return inputVol, inputConc, inputSolute, finalVol, finalConc, 0, 0, outputVolUnit, outputConcUnit, outputSoluteUnit, "zeroMolarMass"

    # 0. if inputVol==0, it will potentially lead to line 102 division not calculable
    # it also doesn't make sense to not have any inputVol, make it an error case
    if inputVol == 0:
        return inputVol, inputConc, inputSolute, finalVol, finalConc, 0, 0, outputVolUnit, outputConcUnit, outputSoluteUnit, "inputVol==0"
    # check inputConc and relevant errors
    # 0.5 if there exists input liquid conc but not molar mass then that's problematic bc we need to display solute in mass
    if inputConc != None and molarMass == None:
        return inputVol, inputConc, inputSolute, finalVol, finalConc, 0, 0, outputVolUnit, outputConcUnit, outputSoluteUnit, "displayUnit"

    if inputSolute != None and inputConc != None:
        # 1 if solute contradicts
        #  TODO: FIX: with unit conversion this is much more complicated!
        if not checkWhetherUseMolarMassBool:
            # if inputConcUnit in MOLARCONCOPTIONS:

            if round(convert(inputConc, outputConcUnit, 'kg/L', molarMass), 10) != round(convert(inputSolute, outputSoluteUnit, 'kg')/convert(inputVol, outputVolUnit, 'L'), 10):
                # if inputConc != inputSolute/inputVol:
                return inputVol, inputConc, inputSolute, finalVol, finalConc, 0, 0, outputVolUnit, outputConcUnit, outputSoluteUnit, "solute"
        else:
            inputSoluteInKG = convert(
                inputSolute, outputSoluteUnit, 'kg', molarMass=molarMass)
            inputVolInL = convert(inputVol, outputVolUnit,
                                  'L', molarMass=molarMass)
            inputConcInM = convert(
                inputConc, outputConcUnit, 'M', molarMass=molarMass)
            if inputSoluteInKG != inputVolInL*inputConcInM*molarMass:
                return inputVol, inputConc, inputSolute, finalVol, finalConc, 0, 0, outputVolUnit, outputConcUnit, outputSoluteUnit, "solute"
    # 2 if inputted inputSolute instead of inputConc, convert
    elif inputSolute != None and inputConc == None:
        inputSoluteInKG = convert(
            inputSolute, outputSoluteUnit, 'kg', molarMass=molarMass)
        inputVolInL = convert(inputVol, outputVolUnit,
                              'L', molarMass=molarMass)
        inputConcInKGPerL = inputSolute/inputVol
        # if molarMass == None:
        inputConc = convert(inputConcInKGPerL, 'kg/L',
                            outputConcUnit, molarMass=molarMass)

    # 3 Calculate inputSolute if necessary
    elif inputConc != None and inputSolute == None:
        inputVolInL = convert(inputVol, outputVolUnit,
                              'L', molarMass=molarMass)
        print(3)
        print("molarMass", molarMass)
        inputConcInKGPerL = convert(
            inputConc, outputConcUnit, 'kg/L', molarMass=molarMass)
        print('inputConcInKGPerL', inputConcInKGPerL)
        inputSolute = convert(inputVolInL * inputConcInKGPerL,
                              'kg', outputSoluteUnit)
        print('inputSoluteInOutputUnit', inputSolute)
    # 4 if no inputConc measure, assume input Conc = 0
    elif inputConc == None and inputSolute == None:
        inputConc = 0
        inputSolute = 0

    # check calculation cases
    # 0 no finalConc, no point of doing calculations
    if finalConc == None:
        print(0)
        print("finalConc == None")
        return inputVol, inputConc, inputSolute, finalVol, finalConc, 0, 0, outputVolUnit, outputConcUnit, outputSoluteUnit, True
    # 2 Concentration unchanged
    if inputConc == finalConc:
        if inputVol == finalVol:
            print(2.1)
            print("Conc unchanged and nothing else need to be changed")
            return inputVol, inputConc, inputSolute, finalVol, finalConc, 0, 0, outputVolUnit, outputConcUnit, outputSoluteUnit, False
        elif inputVol < finalVol:
            print(2.2)
            print("Conc unchanged and increase vol")
            # addedSoluteVol = (finalVol-inputVol)*inputConc
            addedSoluteVol = convert(convert((finalVol-inputVol), outputVolUnit, 'L')*convert(
                inputConc, outputConcUnit, 'kg/L', molarMass), 'kg', outputSoluteUnit, molarMass)
            addedWaterVol = finalVol-inputVol
            return inputVol, inputConc, inputSolute, finalVol, finalConc, addedSoluteVol, addedWaterVol, outputVolUnit, outputConcUnit, outputSoluteUnit, False
    # 3 if input Vol = 0 and there is a final volume, automatically go to upConc:
    if (inputVol == None or inputVol == 0) and finalVol != None:
        print(3)
        inputVol, inputConc, finalVol, finalConc, addedSoluteVol, addedWaterVol, error = upConcentrationTable(
            0, inputConc, finalVol, finalConc, addedSoluteVol, addedWaterVol, molarMass, checkWhetherUseMolarMassBool, outputConcUnit, outputSoluteUnit, outputVolUnit)
        return inputVol, inputConc, inputSolute, finalVol, finalConc, addedSoluteVol, addedWaterVol, outputVolUnit, outputConcUnit, outputSoluteUnit, error
    # 4 if input Vol = 0 and there is no final volume, return not enough input error
    elif (inputVol == None or inputVol == 0) and finalVol == None:
        print(4)
        return inputVol, inputConc, inputSolute, finalVol, finalConc, 0, 0, outputVolUnit, outputConcUnit, outputSoluteUnit, True
    # 5 if input Vol and Conc are fine, and input only final concentration:
    elif inputVol > 0 and inputConc >= 0 and finalVol == None:
        if inputConc > finalConc:
            print("5.1")
            inputVol, inputConc, finalVol, finalConc, waterVol, error = dilutionTable(
                inputVol, inputConc, inputVol, finalConc, addedSoluteVol, addedWaterVol, molarMass, checkWhetherUseMolarMassBool, outputConcUnit, outputSoluteUnit, outputVolUnit)
            return inputVol, inputConc, inputSolute, finalVol, finalConc, 0, waterVol, outputVolUnit, outputConcUnit, outputSoluteUnit, error
        elif inputConc < finalConc:
            print("5.2")
            inputVol, inputConc, finalVol, finalConc, addedSoluteVol, addedWaterVol, error = upConcentrationTable(
                inputVol, inputConc, inputVol, finalConc, addedSoluteVol, addedWaterVol, molarMass, checkWhetherUseMolarMassBool, outputConcUnit, outputSoluteUnit, outputVolUnit)
            return inputVol, inputConc, inputSolute, finalVol, finalConc, addedSoluteVol, addedWaterVol, outputVolUnit, outputConcUnit, outputSoluteUnit, error
    # 0 unachievable: amount of solute in the final solution smaller than initial amount of solute
    if not checkWhetherUseMolarMassBool:
        if convert(inputSolute, outputSoluteUnit, 'kg') > convert(finalVol, outputVolUnit, 'L')*convert(finalConc, outputConcUnit, 'kg/L', molarMass):
            print(1)
            return inputVol, inputConc, inputSolute, finalVol, finalConc, 0, 0, outputVolUnit, outputConcUnit, outputSoluteUnit, "unachievable"
    else:
        inputSoluteInKG = convert(
            inputSolute, outputSoluteUnit, 'kg', molarMass=molarMass)
        finalVolInL = convert(finalVol, outputVolUnit,
                              'L', molarMass=molarMass)
        finalConcInM = convert(finalConc, outputConcUnit,
                               'M', molarMass=molarMass)
        if inputSoluteInKG > finalVolInL*finalConcInM*molarMass:
            print(1)
            print("unachievable computation")
            return inputVol, inputConc, inputSolute, finalVol, finalConc, 0, 0, outputVolUnit, outputConcUnit, outputSoluteUnit, "unachievable"
    # 6 dilution calculation
    if inputConc > finalConc:
        print(6)
        addedSoluteVol = "/"
        inputVol, inputConc, finalVol, finalConc, waterVol, error = dilutionTable(
            inputVol, inputConc, finalVol, finalConc, addedSoluteVol, addedWaterVol, molarMass, checkWhetherUseMolarMassBool, outputConcUnit, outputSoluteUnit, outputVolUnit)
        return inputVol, inputConc, inputSolute, finalVol, finalConc, 0, waterVol, outputVolUnit, outputConcUnit, outputSoluteUnit, error
    # 7 upConc calculation
    elif inputConc < finalConc:
        print(7)
        inputVol, inputConc, finalVol, finalConc, addedSoluteVol, addedWaterVol, error = upConcentrationTable(
            inputVol, inputConc, finalVol, finalConc, addedSoluteVol, addedWaterVol, molarMass, checkWhetherUseMolarMassBool, outputConcUnit, outputSoluteUnit, outputVolUnit)
        return inputVol, inputConc, inputSolute, finalVol, finalConc, addedSoluteVol, addedWaterVol, outputVolUnit, outputConcUnit, outputSoluteUnit, error
