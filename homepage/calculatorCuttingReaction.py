from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class CuttingEdgeForm(forms.Form):
    # reference: https://www.genscript.com/pcr-protocol-pcr-steps.html
    totalVol = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False, label=False)

    # initial DNA concentration, final mass of dna;
    # don’t worry about unit conversion for now

    templateDNAVol = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False, label=False)
    templateDNAInitConc = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False, label=False)
    templateDNAFinalMass = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False, label=False)

    bufferVol = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False, label=False)
    bufferInitConc = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False, label=False)
    bufferFinalConc = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False, label=False)

    restrictionEnzymeVol = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False, label=False)
    restrictionEnzymeInitConc = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False, label=False)
    restrictionEnzymeFinalConc = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False, label=False)

# 10 X PCR Buffer -> 1X PCR Buffer in the final concentration
# final solution has total volume 100 microL
# we can just put in 10 microL of PCR


def updateVolumes(inputVol, inputConc, totalVol):
    '''
    Takes in an ingredient with a certain concentration and volume,
    and updates it with the current volume and concentration with
    respect to the total volume
    '''
    if inputConc != None and inputVol != None:
        tempTotalVol = inputConc * inputVol
        # Raises an error meesage
        if tempTotalVol != totalVol:
            return "CALCULATION CONFLICT ERROR"
        else:
            return "IT's FINE"
    elif inputConc != None:  # When inputVol is empty
        inputVol = totalVol/inputConc
    elif inputVol != None:  # When inputConc is empty
        inputConc = totalVol/inputVol
    elif inputConc == None and inputVol == None:
        inputVol = 0.0
        inputConc = 0.0
    return inputVol, inputConc


def updateVolumes1(inputVol, inputConc, outputConc, totalVol):
    '''
    Takes in an ingredient with a certain concentration and volume,
    and updates it with the current volume and concentration with
    respect to the total volume
    '''
    if inputConc != None and inputVol != None and outputConc != None:
        tempTotalVol = (inputConc * inputVol)/outputConc
        # Raises an error meesage
        if tempTotalVol != totalVol:
            return None, None, "CALCULATION CONFLICT ERROR"
        else:
            return None, None, "IT's FINE"
    elif outputConc == None:
        return None, None, "NO OUTPUT CONC, DOESN'T MAKE SENSE"
    elif inputConc != None:  # When inputVol is empty
        inputVol = (totalVol*outputConc)/inputConc
    elif inputVol != None:  # When inputConc is empty
        inputConc = (totalVol*outputConc)/inputVol
    elif (inputConc == None and inputVol == None) or outputConc == None:
        inputVol = 0.0
        inputConc = 0.0
    return inputVol, inputConc, False


def getVolumesCuttingReaction(totalVol, templateDNAVol, templateDNAInitConc, templateDNAFinalMass, bufferVol,
                              bufferInitConc, bufferFinalConc, restrictionEnzymeVol, restrictionEnzymeInitConc, restrictionEnzymeFinalConc):
    '''Given all the concentrations and the total volume of the PCR reaction, calculate 
    the volumes for the PCR reactions'''

    # make sure totalVol is always inputted
    error = False
    if totalVol == None:
        return None, None, None, None, None, None, None, None, None, None, None, "Total Volume None"
    # DNA Calculation (Assuming that the units match for now)
    if templateDNAVol != None and templateDNAInitConc != None and templateDNAFinalMass != None:
        # Checking that the three inputs match
        if templateDNAVol != templateDNAFinalMass / templateDNAInitConc:
            return None, None, None, None, None, None, None, None, None, None, None, "CALCULATION CONFLICT ERROR"
    elif templateDNAVol != None and templateDNAInitConc != None:
        templateDNAFinalMass = templateDNAInitConc * templateDNAVol
    elif templateDNAVol != None and templateDNAFinalMass != None:
        templateDNAInitConc = templateDNAFinalMass / templateDNAVol
    elif templateDNAInitConc != None and templateDNAFinalMass != None:
        templateDNAVol = templateDNAFinalMass / templateDNAInitConc
    # What about the case when we only have one given value

    # the rest of calculations
    bufferVol, bufferInitConc, error = updateVolumes1(
        bufferVol, bufferInitConc, bufferFinalConc, totalVol)
    if error != False:
        error = "buffer:"+error
    restrictionEnzymeVol, restrictionEnzymeInitConc, error = updateVolumes1(
        restrictionEnzymeVol, restrictionEnzymeInitConc, restrictionEnzymeFinalConc, totalVol)
    if error != False:
        error = "restriction enzymes:"+error

    # water volume
    waterVol = totalVol - templateDNAVol - restrictionEnzymeVol - bufferVol
    # Return an error if water volume is negative

    return totalVol, templateDNAVol, templateDNAInitConc, templateDNAFinalMass, bufferVol, bufferInitConc, bufferFinalConc, restrictionEnzymeVol, restrictionEnzymeInitConc, restrictionEnzymeFinalConc, waterVol, error

# Test Case #1 from example
# totalVol = 40
# templateDNAVol = None
# templateDNAInitConc = 0.1
# templateDNAFinalMass = 1
# bufferVol = None
# bufferConc = 10
# restrictionEnzymeVol = None
# restrictionEyznmeConc = 20
# (40, None, 0.1, 1, None, 10, None, 20)
