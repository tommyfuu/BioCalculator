# import HTML
from django import forms

# given a VOLUME of liquid,CONCENTRATION of this liquid, and TARGET concentration
# calculate the VOLUME of water needed to add


class DilutionForm(forms.Form):
    INPUTVOL = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False)
    INPUTCONC = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False)
    INPUTSOLUTE = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False)
    FINALVOL = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False)
    FINALCONC = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False)
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
    # if inputted inputSolute instead of inputConc, convert
    if inputSolute != None and inputConc != None:
        if inputConc != inputSolute/inputVol:
            return inputVol, inputConc, inputSolute, finalVol, finalConc, 0, 0, "Solute"
    elif inputSolute != None and inputConc == None:
        inputConc = inputSolute/inputVol
    elif inputConc != None and inputSolute == None:
        inputSolute = inputVol * inputConc
    # if no inputConc measure, assume input Conc = 0
    elif inputConc == None and inputSolute == None:
        inputConc = 0
        inputSolute = 0

    # check cases
    if finalConc == None:
        print("AXSACXS")
        return inputVol, inputConc, inputSolute, finalVol, finalConc, 0, 0, True
    if inputConc == finalConc:
        print("Conc unchanged")
        return inputVol, inputConc, inputSolute, finalVol, finalConc, 0, 0, False
    # if input Vol = 0, automatically go to upConc:
    if inputVol == None and finalVol != None:
        inputVol, inputConc, finalVol, finalConc, addedSoluteVol, addedWaterVol, error = upConcentrationTable(
            0, inputConc, finalVol, finalConc, addedSoluteVol, addedWaterVol)
        return inputVol, inputConc, inputSolute, finalVol, finalConc, addedSoluteVol, addedWaterVol, error
    elif inputVol == None and finalVol == None:
        return inputVol, inputConc, inputSolute, finalVol, finalConc, 0, 0, True
    elif inputConc > finalConc:
        addedSoluteVol = "/"
        inputVol, inputConc, finalVol, finalConc, waterVol, error = dilutionTable(
            inputVol, inputConc, finalVol, finalConc)
        return inputVol, inputConc, inputSolute, finalVol, finalConc, 0, waterVol, error
    elif inputConc < finalConc:
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
