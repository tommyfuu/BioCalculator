import HTML
from django import forms
# given a VOLUME of liquid,CONCENTRATION of this liquid, and TARGET concentration
# calculate the VOLUME of water needed to add


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
            print("Have to have at least three values to calculate the fourth one")
    # calculate the amount of water added
    waterVol = dilutionHelper(inputConc, finalVol, finalConc)[1]
    return inputVol, inputConc, finalVol, finalConc, waterVol


def upConcentrationHelper(inputVol, inputConc, finalVol, finalConc):
    'first convert to g, ml, and Molar'
    inputSolute = inputVol * inputConc
    finalSolute = finalVol * finalConc
    addedSoluteVol = finalVol - inputVol
    return inputSolute, finalSolute, addedSoluteVol


def upConcentrationTable(inputVol, inputConc, finalVol, finalConc, addedSoluteVol):
    '''Assumptions 
    1: the given output solute concentration allows the solute to dissolve
     in the input liquid 100%
    2: diluting, not increasing concentration
    3: assume good unit conversion: g vs. ml; kg vs L'''
    while None in [inputVol, inputConc, finalVol, finalConc, addedSoluteVol]:
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
        except:
            print("Have to have at least four values to calculate the fifth one")
    return inputVol, inputConc, finalVol, finalConc, addedSoluteVol


def changeConcentrationTable(inputVol, inputConc, finalVol, finalConc, inputSolute, addedSoluteVol):
    # if inputted inputSolute instead of inputConc, convert
    if inputSolute != None and inputConc == None:
        inputConc = inputSolute/inputVol
    elif inputConc != None and inputSolute == None:
        inputSolute = inputVol * inputConc
    # check cases
    if inputConc == finalConc:
        return inputVol, inputConc, finalVol, finalConc, "Concentration Unchanged"
    elif inputConc < finalConc:
        addedSoluteVol = "/"
        inputVol, inputConc, finalVol, finalConc, waterVol = dilutionTable(
            inputVol, inputConc, finalVol, finalConc)
        return inputVol, inputConc, inputSolute, finalVol, finalConc, 0, waterVol
    elif inputConc > finalConc:
        waterVol = "/"
        inputVol, inputConc, finalVol, finalConc, addedSoluteVol = upConcentrationTable(
            inputVol, inputConc, finalVol, finalConc, addedSoluteVol)
        return inputVol, inputConc, inputSolute, finalVol, finalConc, addedSoluteVol, 0


# how many rows do we need?
# inputVol
# inputConcentration
# inputSolute (interchangeable from row 2)
# finalVol
# finalConcentration
# addedSolute
# addedWater
# class NameForm(forms.Form):
