from django import forms

# given a VOLUME of liquid,CONCENTRATION of this liquid, and TARGET concentration
# calculate the VOLUME of water needed to add


class DilutionForm(forms.Form):
    INPUTVOL = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False, label='Input Liquid Volume')
    INPUTCONC = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False, label='Input Liquid Concentration')
    INPUTSOLUTE = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False, label='Input Solute Mass/Volume')
    FINALVOL = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False, label='Final Liquid Volume')
    FINALCONC = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False, label='Final Liquid Concentration')
    # ADDEDSOLUTE = forms.DecimalField(
    #     decimal_places=5, max_digits=10000, required=False)
    # ADDEDWATER = forms.DecimalField(
    #     decimal_places=5, max_digits=10000, required=False)


def dilutionHelper(inputConc, finalVol, finalConc):
    'first convert to g, ml, and Molar'
    inputVol = (finalVol * finalConc) / inputConc
    inputSolute = inputVol * inputConc
    waterVol = finalVol - inputVol
    return inputVol, waterVol, inputSolute


def dilutionTable(inputVol, inputConc, finalVol, finalConc):
    '''Assumptions
    1: the given input solute dissolves in the input
    liquid 100%
    2: diluting, not increasing concentration'''
    error = False
    # conversion among the four variables inputVol, inputConc, finalVol, finalConc
    while None in [inputVol, inputConc, finalVol, finalConc]:
        try:
            if inputVol == None:
                inputVol = dilutionHelper(inputConc, finalVol, finalConc)[0]
            if inputConc == None:
                inputConc = (finalVol*finalConc)/inputVol
            if finalVol == None:
                finalVol = (inputVol * inputConc)/finalConc
            if finalConc == None:
                finalConc = (inputVol * inputConc)/finalVol
        except:
            error = True
            print("Have to have at least three values to calculate the fourth one")
    # calculate the amount of water added
    waterVol = dilutionHelper(inputConc, finalVol, finalConc)[1]
    return inputVol, inputConc, finalVol, finalConc, waterVol, error


def upConcentrationHelper(inputVol, inputConc, finalVol, finalConc):
    'first convert to g, ml, and Molar'
    inputSolute = inputVol * inputConc
    finalSolute = finalVol * finalConc
    addedSoluteVol = finalVol - inputVol
    return inputSolute, finalSolute, addedSoluteVol


def upConcentrationTable(inputVol, inputConc, finalVol, finalConc, addedSoluteVol, addedWaterVol):
    '''Assumptions
    1: the given output solute concentration allows the solute to dissolve
     in the input liquid 100%
    2: diluting, not increasing concentration
    3: assume good unit conversion: g vs. ml; kg vs L'''
    error = False
    while None in [inputVol, inputConc, finalVol, finalConc, addedWaterVol, addedSoluteVol]:
        try:
            if inputVol == None:
                inputSolute = finalVol*finalConc-addedSoluteVol
                inputVol = inputSolute/inputConc
            if inputConc == None:
                inputSolute = finalVol*finalConc-addedSoluteVol
                inputConc = inputSolute/inputVol
            if finalVol == None:
                finalSolute = inputVol * inputConc + addedSoluteVol
                finalVol = finalSolute/finalConc
            if finalConc == None:
                finalConc = (inputVol*inputConc + addedSoluteVol)/finalVol
            if addedSoluteVol == None:
                addedSoluteVol = finalConc*finalVol-inputVol*inputConc
            if addedWaterVol == None:
                addedWaterVol = finalVol-inputVol
        except:
            error = True
            print("Have to have at least four values to calculate the fifth one")
    return inputVol, inputConc, finalVol, finalConc, addedSoluteVol, addedWaterVol, error


def changeConcentrationTable(inputVol, inputConc, finalVol, finalConc, inputSolute, addedSoluteVol, addedWaterVol):
    # check inputConc and relevant errors
    if inputSolute != None and inputConc != None:
        # 1 if solute contradicts
        if inputConc != inputSolute/inputVol:
            return inputVol, inputConc, inputSolute, finalVol, finalConc, 0, 0, "Solute"
    # 2 if inputted inputSolute instead of inputConc, convert
    elif inputSolute != None and inputConc == None:
        inputConc = inputSolute/inputVol
    # 3 Calculate inputSolute if necessary
    elif inputConc != None and inputSolute == None:
        inputSolute = inputVol * inputConc
    # 4 if no inputConc measure, assume input Conc = 0
    elif inputConc == None and inputSolute == None:
        inputConc = 0
        inputSolute = 0

    # check calculation cases
    # 1 no finalConc, no point of doing calculations
    if finalConc == None:
        print(1)
        print("finalConc == None")
        return inputVol, inputConc, inputSolute, finalVol, finalConc, 0, 0, True
    # 2 Concentration unchanged
    if inputConc == finalConc:
        print(2)
        print("Conc unchanged")
        return inputVol, inputConc, inputSolute, finalVol, finalConc, 0, 0, False
    # 3 if input Vol = 0 and there is a final volume, automatically go to upConc:
    if (inputVol == None or inputVol == 0) and finalVol != None:
        print(3)
        inputVol, inputConc, finalVol, finalConc, addedSoluteVol, addedWaterVol, error = upConcentrationTable(
            0, inputConc, finalVol, finalConc, addedSoluteVol, addedWaterVol)
        return inputVol, inputConc, inputSolute, finalVol, finalConc, addedSoluteVol, addedWaterVol, error
    # 4 if input Vol = 0 and there is no final volume, return not enough input error
    elif (inputVol == None or inputVol == 0) and finalVol == None:
        print(4)
        return inputVol, inputConc, inputSolute, finalVol, finalConc, 0, 0, True
    # 5 if input Vol and Conc are fine, and input only final concentration:
    elif inputVol > 0 and inputConc >= 0 and finalVol == None:
        if inputConc > finalConc:
            print("5.1")
            inputVol, inputConc, finalVol, finalConc, waterVol, error = dilutionTable(
                inputVol, inputConc, inputVol, finalConc)
            return inputVol, inputConc, inputSolute, finalVol, finalConc, 0, waterVol, error
        elif inputConc < finalConc:
            print("5.2")
            inputVol, inputConc, finalVol, finalConc, addedSoluteVol, addedWaterVol, error = upConcentrationTable(
                inputVol, inputConc, inputVol, finalConc, addedSoluteVol, addedWaterVol)
            return inputVol, inputConc, inputSolute, finalVol, finalConc, addedSoluteVol, addedWaterVol, error
    # 6 dilution calculation
    elif inputConc > finalConc:
        print(6)
        addedSoluteVol = "/"
        inputVol, inputConc, finalVol, finalConc, waterVol, error = dilutionTable(
            inputVol, inputConc, finalVol, finalConc)
        return inputVol, inputConc, inputSolute, finalVol, finalConc, 0, waterVol, error
    # 7 upConc calculation
    elif inputConc < finalConc:
        print(7)
        inputVol, inputConc, finalVol, finalConc, addedSoluteVol, addedWaterVol, error = upConcentrationTable(
            inputVol, inputConc, finalVol, finalConc, addedSoluteVol, addedWaterVol)
        return inputVol, inputConc, inputSolute, finalVol, finalConc, addedSoluteVol, addedWaterVol, error


# how many rows do we need?
# inputVol
# inputConcentration
# inputSolute (interchangeable from row 2)
# finalVol
# finalConcentration
# addedSolute
# addedWater
# class NameForm(forms.Form):
