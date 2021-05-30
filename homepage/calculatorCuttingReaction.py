from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class CuttingEdgeForm(forms.Form):
    # reference: https://www.genscript.com/pcr-protocol-pcr-steps.html
    totalVol = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False)

    # initial DNA concentration, final mass of dna;
    # don’t worry about unit conversion for now

    templateDNAVol = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False, label="Template DNA Volume")
    templateDNAInitConc = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False, label="Template DNA Initial Concentration")
    templateDNAFinalMass = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False, label="Template DNA Final Mass")

    bufferVol = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False, label="Buffer Solution Volume")
    bufferConc = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False, label="Buffer Solution Concentration")

    restrictionEnzymeVol = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False, label="Restriction Enzyme Volume")
    restrictionEnzymeConc = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False, label="Restriction Enzyme Concentration")

# 10 X PCR Buffer -> 1X PCR Buffer in the final concentration
# final solution has total volume 100 microL
# we can just put in 10 microL of PCR


def updateVolumes(inputConc, inputVol, totalVol):
    '''
    Takes in an ingredient with a certain concentration and volume,
    and updates it with the current volume and concentration with
    respect to the total volume
    '''
    if inputConc != None and inputVol != None:
        tempinputConc = inputVol/totalVol
        # Raises an error meesage
        if tempinputConc != inputConc:
            return "CALCULATION CONFLICT ERROR"
        else:
            return "IT's FINE"
    elif inputConc != None:  # When inputVol is empty
        inputVol = totalVol*inputConc
    elif inputVol != None:  # When inputConc is empty
        inputConc = inputVol/totalVol
    elif inputConc == None and inputVol == None:
        inputVol = 0
        inputConc = 0
    return inputVol, inputConc


def getVolumesCuttingReaction(totalVol, templateDNAVol, templateDNAInitConc, templateDNAFinalMass, bufferVol,
                              bufferConc, restrictionEnzymeVol, restrictionEnzymeConc):
    '''Given all the concentrations and the total volume of the PCR reaction, calculate 
    the volumes for the PCR reactions'''

    # make sure totalVol is always inputted
    error = False
    if totalVol == None:
        return "TOTALVOL MISSING ERROR", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True

    # DNA Calculation (Assuming that the units match for now)
    if templateDNAVol != None and templateDNAInitConc != None and templateDNAFinalMass != None:
        # Checking that the three inputs match
        if templateDNAVol != templateDNAInitConc / templateDNAFinalMass:
            return "CALCULATION CONFLICT ERROR"
        else:
            return "IT's FINE"
    elif templateDNAVol != None and templateDNAInitConc != None:
        templateDNAFinalMass = templateDNAInitConc / templateDNAVol
    elif templateDNAVol != None and templateDNAFinalMass != None:
        templateDNAInitConc = templateDNAFinalMass * templateDNAVol
    elif templateDNAInitConc != None and templateDNAFinalMass != None:
        templateDNAVol = templateDNAInitConc / templateDNAFinalMass
    # What about the case when we only have one given value

    # the rest of calculations
    restrictionEnzymeVol, restrictionEnzymeConc = updateVolumes(
        restrictionEnzymeVol, restrictionEnzymeConc, totalVol)
    bufferVol, bufferConc = updateVolumes(bufferVol, bufferConc, totalVol)

    # water volume
    waterVol = totalVol - templateDNAVol - restrictionEnzymeVol - bufferVol
    # Return an error if water volume is negative

    return totalVol, templateDNAVol, templateDNAInitConc, templateDNAFinalMass, bufferVol, bufferConc, restrictionEnzymeVol, restrictionEnzymeConc, waterVol
