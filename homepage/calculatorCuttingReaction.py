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
        decimal_places=5, max_digits=10000, required=False)
    templateDNAInitConc = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False)
    templateDNAFinalMass = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False)

    bufferVol = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False)
    bufferConc = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False)
    
    restrictionEnzymeVol = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False)
    restrictionEnzymeConc = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False)
    
    waterVol = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False)


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
            raise Exception("CALCULATION CONFLICT ERROR")
    elif inputConc != None: # When inputVol is empty
        inputVol = totalVol*inputConc
    elif inputVol != None: # When inputConc is empty
        inputConc = inputVol/totalVol
    elif inputConc == None and inputVol == None:
        inputVol = 0
        inputConc = 0
    return inputVol, inputConc

def getVolumesPCR(totalVol, templateDNAVol, templateDNAInitConc, templateDNAFinalMass, bufferVol, 
                    bufferConc, restrictionEnzymeVol, restrictionEnzymeConc, waterVol):
    '''Given all the concentrations and the total volume of the PCR reaction, calculate 
    the volumes for the PCR reactions'''

    # make sure totalVol is always inputted
    error = False
    if totalVol == None:
        return "TOTALVOL MISSING ERROR", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True
    
    # DNA Calculation (Assuming that the units match for now)
    # TODO: Implement DNA Calculation
    if templateDNAVol != None and templateDNAInitConc != None and templateDNAFinalMass != None:
        # Checking that the three inputs match
        if templateDNAVol != templateDNAInitConc / templateDNAFinalMass:
            raise Exception("CALCULATION CONFLICT ERROR")
    elif PCRBufferInitConc != None and PCRBufferFinalConc != None:
        PCRBufferVol = totalVol*(PCRBufferFinalConc/PCRBufferInitConc)
    # elif PCRBufferVol != None and PCRBufferInitConc != None:
    #     PCRBufferFinalConc = PCRBufferVol/totalVol
    # elif PCRBufferVol != None and PCRBufferFinalConc != None:
    #     PCRBufferInitConc = (totalVol/PCRBufferVol)*PCRBufferFinalConc
    
    # the rest of calculations
    restrictionEnzymeVol, restrictionEnzymeConc = updateVolumes(
        restrictionEnzymeVol, restrictionEnzymeConc, totalVol)
    bufferVol, bufferConc = updateVolumes(bufferVol, bufferConc, totalVol)
    
    # water volume
    waterVol = totalVol - templateDNAVol - restrictionEnzymeVol - bufferVol

    return totalVol, templateDNAVol, templateDNAInitConc, templateDNAFinalMass, bufferVol, bufferConc, restrictionEnzymeVol, restrictionEnzymeConc, waterVol

# Things to work on: UNIT CONVERSION AAAAAAH!
# Edge cases ideas
# 1. when the pcr buffer row's volume is inputted, we don't need to calculate the initial and final conc of pcr buffer
# 2. edge case for negative water volume
