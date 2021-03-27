from django import forms


class PCRForm(forms.Form):
    # reference: https://www.genscript.com/pcr-protocol-pcr-steps.html
    TOTALVOL = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False,)
    WATER = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False)
    PCRBUFFERVOL = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False)
    PCRBUFFERINITCONC = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False)
    PCRBUFFERFINALCONC = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False)
    POLYMERASEVOL = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False)
    POLYMERASECONC = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False)
    dNTPVOL = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False)
    dNTPCONC = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False)
    MgCl2VOL = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False)
    MgCl2CONC = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False)
    FORWARDPRIMERVOL = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False)
    FORWARDPRIMERCONC = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False)
    BACKWARDPRIMERVOL = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False)
    BACKWARDPRIMERCONC = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False)
    TEMPLATEDNAVOL = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False)
    TEMPLATEDNACONC = forms.DecimalField(
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
        inputonc = inputVol/totalVol
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
        PCRBufferFinalConc= PCRBufferVol/totalVol
    elif PCRBufferVol != None and PCRBufferFinalConc != None:
        PCRBufferInitConc = (totalVol/PCRBufferVol)*PCRBufferFinalConc
    # the rest of calculations
    polymeraseVol, polymeraseConc = getVolumesPCRHelper(polymeraseConc, polymeraseVol, totalVol)
    dNTPVol, dNTPConc = getVolumesPCRHelper(dNTPConc, dNTPVol, totalVol)
    MgCl2Vol, MgCl2Conc = getVolumesPCRHelper(MgCl2Conc, MgCl2Vol, totalVol)
    forwardPrimerVol, forwardPrimerConc = getVolumesPCRHelper(forwardPrimerConc, forwardPrimerVol, totalVol)
    backwardPrimerVol, backwardPrimerConc = backwardPrimerConcgetVolumesPCRHelper(backwardPrimerConc, backwardPrimerVol, totalVol)
    templateDNAVol, templateDNAConc = getVolumesPCRHelper(templateDNAConc, templateDNAVol, totalVol)
    DMSOptionalVol, DMSOptionalConc = getVolumesPCRHelper(DMSOptionalConc, DMSOptionalVol, totalVol)
    # water volume
    waterVol = totalVol - PCRBufferVol - polymeraseVol -dNTPVol -MgCl2Vol - forwardPrimerVol - backwardPrimerVol - templateDNAVol - DMSOptionalVol
    return totalVol, waterVol, PCRBufferVol, PCRBufferInitConc, PCRBufferFinalConc, polymeraseVol, polymeraseConc, dNTPVol, dNTPConc, MgCl2Vol, MgCl2Conc, forwardPrimerVol, forwardPrimerConc, backwardPrimerVol, backwardPrimerConc, templateDNAVol, templateDNAConc, DMSOOptionalVol, DMSOOptionalConc