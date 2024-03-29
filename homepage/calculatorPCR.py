from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class PCRForm(forms.Form):
    # reference: https://www.genscript.com/pcr-protocol-pcr-steps.html

    totalVol = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False, label=False)
    waterVol = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False, label=False)
    PCRBufferVol = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False, label=False)
    PCRBufferInitConc = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False, label=False)
    PCRBufferFinalConc = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False, label=False)
    polymeraseVol = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False, label=False)
    polymeraseConc = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False, label=False)
    dNTPVol = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False, label=False)
    dNTPConc = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False, label=False)
    MgCl2Vol = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False, label=False)
    MgCl2Conc = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False, label=False)
    forwardPrimerVol = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False, label=False)
    forwardPrimerConc = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False, label=False)
    backwardPrimerVol = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False, label=False)
    backwardPrimerConc = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False, label=False)
    templateDNAVol = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False, label=False)
    templateDNAConc = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False, label=False)
    DMSOOptionalVol = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False, label=False)
    DMSOOptionalConc = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False, label=False)

# 10 X PCR Buffer -> 1X PCR Buffer in the final concentration
# final solution has total volume 100 microL
# we can just put in 10 microL of PCR


def getVolumesPCRHelper(inputConc, inputVol, totalVol):
    if inputConc != None and inputVol != None:
        tempinputConc = inputVol/totalVol
        if tempinputConc != inputConc:
            return "CALCULATION CONFLICT ERROR"
        else:
            return "IT's FINE"
    elif inputConc != None:
        inputVol = totalVol*inputConc
    elif inputVol != None:
        inputConc = inputVol/totalVol
    elif inputConc == None and inputVol == None:
        inputVol = 0
        inputConc = 0
    return inputVol, inputConc


def getVolumesPCR(totalVol, waterVol, PCRBufferVol, PCRBufferInitConc, PCRBufferFinalConc, polymeraseVol, polymeraseConc, dNTPVol, dNTPConc, MgCl2Vol, MgCl2Conc, forwardPrimerVol, forwardPrimerConc, backwardPrimerVol, backwardPrimerConc, templateDNAVol, templateDNAConc, DMSOOptionalVol, DMSOOptionalConc):
    """Given all the concentrations and the total volume of the PCR reaction, calculate the volumes for the PCR reactions"""
    # make sure totalVol is always inputted
    error = False
    if totalVol == None:
        return "TOTALVOL MISSING ERROR", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True
    # 1. PCR Buffer calculation
    if PCRBufferInitConc != None and PCRBufferFinalConc != None and PCRBufferVol != None:
        tempPCRBufferVol = totalVol*(PCRBufferFinalConc/PCRBufferInitConc)
        if tempPCRBufferVol != PCRBufferVol:
            return "CALCULATION CONFLICT ERROR"
        else:
            return "IT's FINE"
    elif PCRBufferInitConc != None and PCRBufferFinalConc != None:
        PCRBufferVol = totalVol*(PCRBufferFinalConc/PCRBufferInitConc)
    elif PCRBufferVol != None and PCRBufferInitConc != None:
        PCRBufferFinalConc = PCRBufferVol/totalVol
    elif PCRBufferVol != None and PCRBufferFinalConc != None:
        PCRBufferInitConc = (totalVol/PCRBufferVol)*PCRBufferFinalConc
    # the rest of calculations
    polymeraseVol, polymeraseConc = getVolumesPCRHelper(
        polymeraseConc, polymeraseVol, totalVol)
    dNTPVol, dNTPConc = getVolumesPCRHelper(dNTPConc, dNTPVol, totalVol)
    MgCl2Vol, MgCl2Conc = getVolumesPCRHelper(MgCl2Conc, MgCl2Vol, totalVol)
    forwardPrimerVol, forwardPrimerConc = getVolumesPCRHelper(
        forwardPrimerConc, forwardPrimerVol, totalVol)
    backwardPrimerVol, backwardPrimerConc = getVolumesPCRHelper(
        backwardPrimerConc, backwardPrimerVol, totalVol)
    templateDNAVol, templateDNAConc = getVolumesPCRHelper(
        templateDNAConc, templateDNAVol, totalVol)
    DMSOOptionalVol, DMSOOptionalConc = getVolumesPCRHelper(
        DMSOOptionalVol, DMSOOptionalVol, totalVol)
    # water volume
    waterVol = totalVol - PCRBufferVol - polymeraseVol - dNTPVol - MgCl2Vol - \
        forwardPrimerVol - backwardPrimerVol - templateDNAVol - DMSOOptionalVol
    return totalVol, waterVol, PCRBufferVol, PCRBufferInitConc, PCRBufferFinalConc, polymeraseVol, polymeraseConc, dNTPVol, dNTPConc, MgCl2Vol, MgCl2Conc, forwardPrimerVol, forwardPrimerConc, backwardPrimerVol, backwardPrimerConc, templateDNAVol, templateDNAConc, DMSOOptionalVol, DMSOOptionalConc, error

# Things to work on: UNIT CONVERSION AAAAAAH!
# Edge cases ideas
# 1. when the pcr buffer row's volume is inputted, we don't need to calculate the initial and final conc of pcr buffer
# 2. edge case for negative water volume
