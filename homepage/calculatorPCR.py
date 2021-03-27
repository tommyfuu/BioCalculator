from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class PCRForm(forms.Form):
    # reference: https://www.genscript.com/pcr-protocol-pcr-steps.html

    totalVol = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False)
    waterVol = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False)
    PCRBufferVol = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False)
    PCRBufferInitConc = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False)
    PCRBufferFinalConc = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False)
    polymeraseVol = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False)
    polymeraseConc = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False)
    dNTPVol = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False)
    dNTPConc = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False)
    MgCl2Vol = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False)
    MgCl2Conc = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False)
    forwardPrimerVol = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False)
    forwardPrimerConc = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False)
    backwardPrimerVol = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False)
    backwardPrimerConc = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False)
    templateDNAVol = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False)
    templateDNAConc = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False)
    DMSOOptionalVol = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False)
    DMSOOptionalConc = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False)

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
        # TODO: BUG FIX HERE!
    return inputVol, inputConc


def getVolumesPCR(totalVol, waterVol, PCRBufferVol, PCRBufferInitConc, PCRBufferFinalConc, polymeraseVol, polymeraseConc, dNTPVol, dNTPConc, MgCl2Vol, MgCl2Conc, forwardPrimerVol, forwardPrimerConc, backwardPrimerVol, backwardPrimerConc, templateDNAVol, templateDNAConc, DMSOOptionalVol, DMSOOptionalConc):
    """Given all the concentrations and the total volume of the PCR reaction, calculate the volumes for the PCR reactions"""
    # make sure totalVol is always inputted
    if totalVol == None:
        return "TOTALVOL MISSING ERROR"
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
    print(PCRBufferVol)
    # the rest of calculations
    polymeraseVol, polymeraseConc = getVolumesPCRHelper(
        polymeraseConc, polymeraseVol, totalVol)
    print(polymeraseVol, polymeraseConc)
    dNTPVol, dNTPConc = getVolumesPCRHelper(dNTPConc, dNTPVol, totalVol)
    print(dNTPVol, dNTPConc)
    MgCl2Vol, MgCl2Conc = getVolumesPCRHelper(MgCl2Conc, MgCl2Vol, totalVol)
    print(MgCl2Vol, MgCl2Conc)
    forwardPrimerVol, forwardPrimerConc = getVolumesPCRHelper(
        forwardPrimerConc, forwardPrimerVol, totalVol)
    print(forwardPrimerVol, forwardPrimerConc)
    backwardPrimerVol, backwardPrimerConc = getVolumesPCRHelper(
        backwardPrimerConc, backwardPrimerVol, totalVol)
    print(backwardPrimerVol)
    templateDNAVol, templateDNAConc = getVolumesPCRHelper(
        templateDNAConc, templateDNAVol, totalVol)
    print(templateDNAVol)
    DMSOOptionalVol, DMSOOptionalConc = getVolumesPCRHelper(
        DMSOOptionalVol, DMSOOptionalVol, totalVol)
    print(DMSOOptionalVol)
    # water volume
    waterVol = totalVol - PCRBufferVol - polymeraseVol - dNTPVol - MgCl2Vol - \
        forwardPrimerVol - backwardPrimerVol - templateDNAVol - DMSOOptionalVol
    return totalVol, waterVol, PCRBufferVol, PCRBufferInitConc, PCRBufferFinalConc, polymeraseVol, polymeraseConc, dNTPVol, dNTPConc, MgCl2Vol, MgCl2Conc, forwardPrimerVol, forwardPrimerConc, backwardPrimerVol, backwardPrimerConc, templateDNAVol, templateDNAConc, DMSOOptionalVol, DMSOOptionalConc
