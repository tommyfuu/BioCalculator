from django.shortcuts import render, HttpResponse, HttpResponseRedirect

# importing calculators
from .calculatorDilution import DilutionForm
from .calculatorDilution import *
from .calculatorPCR import PCRForm
from .calculatorPCR import *
from .calculatorUnitConvert import ConversionForm
from .calculatorUnitConvert import *
from .calculatorCuttingReaction import CuttingEdgeForm
from .calculatorCuttingReaction import *
from .opentrons import RandomNumGenerator
from .opentrons import *
from .colonyCounter import ColonyCounterForm
from .colonyCounter import *

import time

# Create your views here.


def home(request):
    # return HttpResponse("Home page!")
    return render(request, "home.html", {})


def calculators(request):
    # return HttpResponse("Calculators page!")
    return render(request, "calculators.html", {})


def faq(request):
    # return HttpResponse("FAQ page!")
    return render(request, "faq.html", {})


def about(request):
    # return HttpResponse("About page!")
    return render(request, "about.html", {})


# CALCULATORS
# DILUTION CALCULATOR
# GLOBAL VARIABLES
INPUTVOL = None
INPUTCONC = None
INPUTSOLUTE = None
FINALVOL = None
FINALCONC = None
ADDEDSOLUTE = None
ADDEDWATER = None


def dilution_input_view(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = DilutionForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            print("Extracting values")
            inputVol = form.cleaned_data["INPUTVOL"]
            inputConc = form.cleaned_data["INPUTCONC"]
            inputSolute = form.cleaned_data["INPUTSOLUTE"]
            finalVol = form.cleaned_data["FINALVOL"]
            finalConc = form.cleaned_data["FINALCONC"]

            inputSoluteUnit = form.cleaned_data["INPUTSOLUTEUNIT"]
            molarMass = form.cleaned_data["MOLARMASS"]
            inputVolUnit = form.cleaned_data["INPUTVOLUNIT"]
            inputConcUnit = form.cleaned_data["INPUTCONCUNIT"]
            finalVolUnit = form.cleaned_data["FINALVOLUNIT"]
            finalConcUnit = form.cleaned_data["FINALCONCUNIT"]
            outputVolUnit = form.cleaned_data["OUTPUTVOLUNIT"]
            outputConcUnit = form.cleaned_data["OUTPUTCONCUNIT"]
            outputSoluteUnit = form.cleaned_data["OUTPUTSOLUTEUNIT"]

            # addedSoluteVol = form.cleaned_data['ADDEDSOLUTE']
            # waterVol = form.cleaned_data['ADDEDWATER']
            addedSoluteVol = None
            waterVol = None

            # INPUTVOL, INPUTCONC, INPUTSOLUTE, FINALVOL, FINALCONC, ADDEDSOLUTE, ADDEDWATER, ERROR = changeConcentrationTable(
            #     inputVol, inputConc, finalVol, finalConc, inputSolute, addedSoluteVol, waterVol)
            (
                INPUTVOL,
                INPUTCONC,
                INPUTSOLUTE,
                FINALVOL,
                FINALCONC,
                ADDEDSOLUTE,
                ADDEDWATER,
                OUTPUTVOLUNIT,
                OUTPUTCONCUNIT,
                OUTPUTSOLUTEUNIT,
                ERROR,
            ) = changeConcentrationTable(
                inputVol,
                inputVolUnit,
                inputConc,
                inputConcUnit,
                inputSolute,
                inputSoluteUnit,
                molarMass,
                finalVol,
                finalVolUnit,
                finalConc,
                finalConcUnit,
                outputVolUnit,
                outputConcUnit,
                outputSoluteUnit,
                addedSoluteVol,
                waterVol,
            )

            print("Here are the calculated input values for your desired output:")
            if ERROR == False:
                print("GOTORESULTPAGE")
                return render(
                    request,
                    "dilutionCalcResult.html",
                    {
                        "inputVol": INPUTVOL,
                        "inputConc": INPUTCONC,
                        "inputSolute": INPUTSOLUTE,
                        "finalVol": FINALVOL,
                        "finalConc": FINALCONC,
                        "addedSolute": ADDEDSOLUTE,
                        "addedWater": ADDEDWATER,
                        "outputVolUnit": OUTPUTVOLUNIT,
                        "outputConcUnit": OUTPUTCONCUNIT,
                        "outputSoluteUnit": OUTPUTSOLUTEUNIT,
                    },
                )
            elif ERROR == True:
                # not enough inputs
                return render(request, "dilutionCalcError.html", {})
            else:
                if ERROR == "solute":
                    info = "Error: Input solution concentration not the same as the concentration value calculated with inputSolute and inputVol."
                if ERROR == "unachievable":
                    info = "Error: Computation unachievable. The amount of solute in the final solution is smaller than the amount of solute in the input solution."
                if ERROR == "inputVol==0":
                    info = "Error: input volume = 0, invalid input solution."
                if ERROR == "zeroMolarMass":
                    info = "Error: zero molar mass. You should either NOT input molar mass if your calculation does not involve molar conversion, or you should enter a numerical molar mass value."
                if ERROR == "displayUnit":
                    info = "Error: inputted input liquid concentration but not molar mass. This way the amount of solute cannot be displayed in mass, which is problematic for our current implementation."
                return render(request, "dilutionCalcSolute.html", {"error": info})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = DilutionForm()
    return render(request, "dilutionCalc.html", {"form": form})


def dilution_result_view(request):
    # return HttpResponse("dilution calculator result page")
    return render(
        request,
        "dilutionCalcResult.html",
        {
            "inputVol": INPUTVOL,
            "inputConc": INPUTCONC,
            "inputSolute": INPUTSOLUTE,
            "finalVol": FINALVOL,
            "finalConc": FINALCONC,
            "addedSolute": ADDEDSOLUTE,
            "addedWater": ADDEDWATER,
        },
    )


def dilution_error_view(request):
    # return HttpResponse("dilution calculator error page")
    return render(request, "dilutionCalcError.html", {"errorMsg": ERRORMSG})


# PCR CALCULATOR
# GLOBAL VARIABLES
RESULTtotalVol = None
RESULTwaterVol = None
RESULTPCRBufferVol = None
RESULTPCRBufferInitConc = None
RESULTPCRBufferFinalConc = None
RESULTpolymeraseVol = None
RESULTpolymeraseConc = None
RESULTdNTPVol = None
RESULTdNTPConc = None
RESULTMgCl2Vol = None
RESULTMgCl2Conc = None
RESULTforwardPrimerVol = None
RESULTforwardPrimerConc = None
RESULTbackwardPrimerVol = None
RESULTbackwardPrimerConc = None
RESULTtemplateDNAVol = None
RESULTtemplateDNAConc = None
RESULTDMSOOptionalVol = None
RESULTDMSOOptionalConc = None
ERRORMSG = ""


def pcr_input_view(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        pcrform = PCRForm(request.POST)
        # check whether it's valid:
        if pcrform.is_valid():
            totalVol = pcrform.cleaned_data["totalVol"]
            waterVol = pcrform.cleaned_data["waterVol"]
            PCRBufferVol = pcrform.cleaned_data["PCRBufferVol"]
            PCRBufferInitConc = pcrform.cleaned_data["PCRBufferInitConc"]
            PCRBufferFinalConc = pcrform.cleaned_data["PCRBufferFinalConc"]
            polymeraseVol = pcrform.cleaned_data["polymeraseVol"]
            polymeraseConc = pcrform.cleaned_data["polymeraseConc"]
            dNTPVol = pcrform.cleaned_data["dNTPVol"]
            dNTPConc = pcrform.cleaned_data["dNTPConc"]
            MgCl2Vol = pcrform.cleaned_data["MgCl2Vol"]
            MgCl2Conc = pcrform.cleaned_data["MgCl2Conc"]
            forwardPrimerVol = pcrform.cleaned_data["forwardPrimerVol"]
            forwardPrimerConc = pcrform.cleaned_data["forwardPrimerConc"]
            backwardPrimerVol = pcrform.cleaned_data["backwardPrimerVol"]
            backwardPrimerConc = pcrform.cleaned_data["backwardPrimerConc"]
            templateDNAVol = pcrform.cleaned_data["templateDNAVol"]
            templateDNAConc = pcrform.cleaned_data["templateDNAConc"]
            DMSOOptionalVol = pcrform.cleaned_data["DMSOOptionalVol"]
            DMSOOptionalConc = pcrform.cleaned_data["DMSOOptionalConc"]
            results = getVolumesPCR(
                totalVol,
                waterVol,
                PCRBufferVol,
                PCRBufferInitConc,
                PCRBufferFinalConc,
                polymeraseVol,
                polymeraseConc,
                dNTPVol,
                dNTPConc,
                MgCl2Vol,
                MgCl2Conc,
                forwardPrimerVol,
                forwardPrimerConc,
                backwardPrimerVol,
                backwardPrimerConc,
                templateDNAVol,
                templateDNAConc,
                DMSOOptionalVol,
                DMSOOptionalConc,
            )

            (
                RESULTtotalVol,
                RESULTwaterVol,
                RESULTPCRBufferVol,
                RESULTPCRBufferInitConc,
                RESULTPCRBufferFinalConc,
                RESULTpolymeraseVol,
                RESULTpolymeraseConc,
                RESULTdNTPVol,
                RESULTdNTPConc,
                RESULTMgCl2Vol,
                RESULTMgCl2Conc,
                RESULTforwardPrimerVol,
                RESULTforwardPrimerConc,
                RESULTbackwardPrimerVol,
                RESULTbackwardPrimerConc,
                RESULTtemplateDNAVol,
                RESULTtemplateDNAConc,
                RESULTDMSOOptionalVol,
                RESULTDMSOOptionalConc,
                ERROR,
            ) = results

            # ERROR = False
            if ERROR == False:
                return render(
                    request,
                    "calcPCRResult.html",
                    {
                        "RESULTtotalVol": RESULTtotalVol,
                        "RESULTwaterVol": RESULTwaterVol,
                        "RESULTPCRBufferVol": RESULTPCRBufferVol,
                        "RESULTPCRBufferInitConc": RESULTPCRBufferInitConc,
                        "RESULTPCRBufferFinalConc": RESULTPCRBufferFinalConc,
                        "RESULTpolymeraseVol": RESULTpolymeraseVol,
                        "RESULTpolymeraseConc": RESULTpolymeraseConc,
                        "RESULTdNTPVol": RESULTdNTPVol,
                        "RESULTdNTPConc": RESULTdNTPConc,
                        "RESULTMgCl2Vol": RESULTMgCl2Vol,
                        "RESULTMgCl2Conc": RESULTMgCl2Conc,
                        "RESULTforwardPrimerVol": RESULTforwardPrimerVol,
                        "RESULTforwardPrimerConc": RESULTforwardPrimerConc,
                        "RESULTbackwardPrimerVol": RESULTbackwardPrimerVol,
                        "RESULTbackwardPrimerConc": RESULTbackwardPrimerConc,
                        "RESULTtemplateDNAVol": RESULTtemplateDNAVol,
                        "RESULTtemplateDNAConc": RESULTtemplateDNAConc,
                        "RESULTDMSOOptionalVol": RESULTDMSOOptionalVol,
                        "RESULTDMSOOptionalConc": RESULTDMSOOptionalConc,
                    },
                )
            else:
                ERRORMSG = "There's some error"
                # return render(request, 'calcPCR.html', {'pcrform': pcrform})
                return render(request, "calcPCRError.html", {"errorMsg": ERRORMSG})
    else:
        pcrform = PCRForm()
    return render(request, "calcPCR.html", {"pcrform": pcrform})


def pcr_result_view(request):
    # return HttpResponse("PCR result page!")
    return render(
        request,
        "calcPCRResult.html",
        {
            "RESULTtotalVol": RESULTtotalVol,
            "RESULTwaterVol": RESULTwaterVol,
            "RESULTPCRBufferVol": RESULTPCRBufferVol,
            "RESULTPCRBufferInitConc": RESULTPCRBufferInitConc,
            "RESULTPCRBufferFinalConc": RESULTPCRBufferFinalConc,
            "RESULTpolymeraseVol": RESULTpolymeraseVol,
            "RESULTpolymeraseConc": RESULTpolymeraseConc,
            "RESULTdNTPVol": RESULTdNTPVol,
            "RESULTdNTPConc": RESULTdNTPConc,
            "RESULTMgCl2Vol": RESULTMgCl2Vol,
            "RESULTMgCl2Conc": RESULTMgCl2Conc,
            "RESULTforwardPrimerVol": RESULTforwardPrimerVol,
            "RESULTforwardPrimerConc": RESULTforwardPrimerConc,
            "RESULTbackwardPrimerVol": RESULTbackwardPrimerVol,
            "RESULTbackwardPrimerConc": RESULTbackwardPrimerConc,
            "RESULTtemplateDNAVol": RESULTtemplateDNAVol,
            "RESULTtemplateDNAConc": RESULTtemplateDNAConc,
            "RESULTDMSOOptionalVol": RESULTDMSOOptionalVol,
            "RESULTDMSOOptionalConc": RESULTDMSOOptionalConc,
        },
    )


def pcr_error_view(request):
    # return HttpResponse("PCR error page!")
    return render(request, "calcPCRError.html", {"errorMsg": ERRORMSG})


# UNIT CONVERSION CALCULATOR
# GLOBAL VARIABLES
INPUTVALUE = None
INPUTUNIT = None
OUTPUTVALUE = None
OUTPUTUNIT = None
MOLARMASS = None
ERROR = False


def unit_convert_input_view(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        conversionform = ConversionForm(request.POST)
        # check whether it's valid:

        if conversionform.is_valid():
            inputValue = conversionform.cleaned_data["INPUTVALUE"]
            inputUnit = conversionform.cleaned_data["INPUTUNIT"]
            outputValue = conversionform.cleaned_data["OUTPUTVALUE"]
            outputUnit = conversionform.cleaned_data["OUTPUTUNIT"]
            molarMass = conversionform.cleaned_data["MOLARMASS"]
            results = unitTable(
                inputValue, inputUnit, outputValue, outputUnit, molarMass
            )
            print("Here is conversion value for your input:")

            INPUTVALUE, INPUTUNIT, OUTPUTVALUE, OUTPUTUNIT, MOLARMASS, ERROR = results

            if ERROR == "":
                return render(
                    request,
                    "calcUnitConvertResult.html",
                    {
                        "inputValue": INPUTVALUE,
                        "inputUnit": INPUTUNIT,
                        "outputValue": OUTPUTVALUE,
                        "outputUnit": OUTPUTUNIT,
                        "molarMass": MOLARMASS,
                    },
                )
            else:
                return render(request, "calcUnitConvertError.html", {"errorMsg": ERROR})
        else:
            return render(
                request, "calcUnitConvertError.html", {"conversionform": conversionform}
            )
    else:
        conversionform = ConversionForm()
    return render(request, "calcUnitConvert.html", {"conversionform": conversionform})


def unit_convert_result_view(request):
    # return HttpResponse("unit conversion result page!")
    return render(
        request,
        "calcUnitConvertResult.html",
        {
            "inputValue": INPUTVALUE,
            "inputUnit": INPUTUNIT,
            "outputValue": OUTPUTVALUE,
            "outputUnit": OUTPUTUNIT,
            "molarMass": MOLARMASS,
        },
    )


def unit_convert_error_view(request):
    # return HttpResponse("unit conversion error page!")
    return render(request, "calcUnitConvertError.html", {"errorMsg": ERRORMSG})


######################################## CUTTING REACTION CALCULATOR #######################################
# GLOBAL VARIABLES
TOTALVOL = None
TEMPLATEDNAVOL = None
TEMPLATEDNAINITCONC = None
TEMPLATEDNAFINALMASS = None
BUFFERVOL = None
BUFFERCONC = None
RESTRICTIONENZYMEVOL = None
RESTRICTIONENZYMECONC = None
WATERVOL = None
ERRORMSG = ""


def cutting_reaction_input_view(request):
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        cuttingform = CuttingEdgeForm(request.POST)
        # check whether it's valid:
        if cuttingform.is_valid():
            totalVol = cuttingform.cleaned_data["totalVol"]
            templateDNAVol = cuttingform.cleaned_data["templateDNAVol"]
            templateDNAInitConc = cuttingform.cleaned_data["templateDNAInitConc"]
            templateDNAFinalMass = cuttingform.cleaned_data["templateDNAFinalMass"]
            bufferVol = cuttingform.cleaned_data["bufferVol"]
            bufferInitConc = cuttingform.cleaned_data["bufferInitConc"]
            bufferFinalConc = cuttingform.cleaned_data["bufferFinalConc"]
            restrictionEnzymeVol = cuttingform.cleaned_data["restrictionEnzymeVol"]
            restrictionEnzymeInitConc = cuttingform.cleaned_data[
                "restrictionEnzymeInitConc"
            ]
            restrictionEnzymeFinalConc = cuttingform.cleaned_data[
                "restrictionEnzymeFinalConc"
            ]

            # call python functions from your py file
            results = getVolumesCuttingReaction(
                totalVol,
                templateDNAVol,
                templateDNAInitConc,
                templateDNAFinalMass,
                bufferVol,
                bufferInitConc,
                bufferFinalConc,
                restrictionEnzymeVol,
                restrictionEnzymeInitConc,
                restrictionEnzymeFinalConc,
            )

            # parsing your results
            (
                totalVol,
                templateDNAVol,
                templateDNAInitConc,
                templateDNAFinalMass,
                bufferVol,
                bufferInitConc,
                bufferFinalConc,
                restrictionEnzymeVol,
                restrictionEnzymeInitConc,
                restrictionEnzymeFinalConc,
                waterVol,
                ERROR,
            ) = results
            # feed that into the result/error
            if ERROR == False:
                return render(
                    request,
                    "cuttingReactionCalcResult.html",
                    {
                        "totalVol": totalVol,
                        "templateDNAVol": templateDNAVol,
                        "templateDNAInitConc": templateDNAInitConc,
                        "templateDNAFinalMass": templateDNAFinalMass,
                        "bufferVol": bufferVol,
                        "bufferInitConc": bufferInitConc,
                        "bufferFinalConc": bufferFinalConc,
                        "restrictionEnzymeVol": restrictionEnzymeVol,
                        "restrictionEnzymeInitConc": restrictionEnzymeInitConc,
                        "restrictionEnzymeFinalConc": restrictionEnzymeFinalConc,
                        "waterVol": waterVol,
                    },
                )
        #     if ERROR == False:
        #         return render(request, 'calcUnitConvertResult.html', {"inputValue": INPUTVALUE, "inputUnit": INPUTUNIT, "outputValue": OUTPUTVALUE, "outputUnit": OUTPUTUNIT, "molarMass": MOLARMASS})
        #     else:
        #         ERRORMSG = "There's some error"
        #         return render(request, 'calcUnitConvertError.html', {'errorMsg': ERRORMSG})
        # else:
        #     return render(request, 'cuttingReactionCalcError.html', {'cuttingform': cuttingform})
    else:
        cuttingform = CuttingEdgeForm()
    return render(request, "cuttingReactionCalc.html", {"cuttingform": cuttingform})


# TODO: Define global variables --> Work on the results page
def cutting_reaction_result_view(request):
    # return HttpResponse("Contact page!")
    return render(
        request,
        "cuttingReactionCalcResult.html",
        {
            "totalVol": TOTALVOL,
            "templateDNAVol": TEMPLATEDNAVOL,
            "templateDNAInitConc": TEMPLATEDNAINITCONC,
            "templateDNAFinalMass": TEMPLATEDNAFINALMASS,
            "bufferVol": BUFFERVOL,
            "bufferConc": BUFFERCONC,
            "restrictionEnzymeVol": RESTRICTIONENZYMEVOL,
            "restrictionEnzymeConc": RESTRICTIONENZYMECONC,
            "waterVol": WATERVOL,
        },
    )


######################################## AR OPENTRONS CALCULATOR #######################################

# global variable
FLOOR = None
CEILING = None
OPENTRONS_RESULT = None


def opentrons_view(request):
    print("request method:", request.method)
    # if this is a POST request we need to process the form data
    # request.method="POST"
    print("request.method", request.method)
    if request.method == "POST":
        print("helloooooo")
        # create a form instance and populate it with data from the request:
        randomForm = RandomNumGenerator(request.POST)
        # check whether it's valid:
        if randomForm.is_valid():
            print("i want dessert")
            FLOOR = randomForm.cleaned_data["floor"]
            CEILING = randomForm.cleaned_data["ceiling"]

            # call python functions from your py file
            OPENTRONS_RESULT = randomNumGenerator(FLOOR, CEILING)

            return render(
                request,
                "opentronsResult.html",
                {"floor": FLOOR, "ceiling": CEILING, "result": OPENTRONS_RESULT},
            )
    # else clause should be 'else' compared to "if request.method == 'POST':"
    else:
        randomForm = RandomNumGenerator()

    # return HttpResponse("AR opentrons page")
    return render(request, "opentrons.html", {"randomForm": randomForm})


def opentrons_result_view(request):
    # return HTTP response object
    return render(
        request,
        "opentronsResult.html",
        {"floor": FLOOR, "ceiling": CEILING, "result": OPENTRONS_RESULT},
    )


######################################## AR OPENTRONS CALCULATOR #######################################

# global variable
FLOOR_1 = None
CEILING_1 = None
OPENTRONS_RESULT_1 = None
import os
import datetime


def colony_counter_view(request):
    # clean the output folder
    for root, dirs, files in os.walk(
        "/Users/chenlianfu/Documents/Github/BioCalculator/homepage/colonyCountOutputs/"
    ):
        for file in files:
            os.remove(os.path.join(root, file))
    print("request method:", request.method)
    # if this is a POST request we need to process the form data
    # request.method="POST"
    print("request.method", request.method)
    if request.method == "POST":
        print("helloooooo")
        # create a form instance and populate it with data from the request:
        colonyCounterForm = ColonyCounterForm(request.POST, request.FILES)
        # check whether it's valid:
        if colonyCounterForm.is_valid():
            colonyCounterForm.save()
            # Get the current instance object to display in the template
            img_obj = colonyCounterForm.instance
            run_model("./media/users/")
            # clean the current folder
            for root, dirs, files in os.walk("./media/users/"):
                for file in files:
                    os.remove(os.path.join(root, file))
            # TODO: return an output html page here once completely implemented
            return render(
                request,
                "colonyCounterCalculations.html",
                {"form": colonyCounterForm, "img_obj": img_obj},
            )

    # else clause should be 'else' compared to "if request.method == 'POST':"
    else:
        colonyCounterForm = ColonyCounterForm()

    # return HttpResponse("AR opentrons page")
    return render(request, "colonyCounterInput.html", {"form": colonyCounterForm})


def colony_counter_result_view(request):
    # return HTTP response object
    return render(
        request,
        "colonyCounterResult.html",
        {"floor": FLOOR_1, "ceiling": CEILING_1, "result": OPENTRONS_RESULT_1},
    )


def colony_counter_calculations_view(request):
    # return HTTP response object
    return render(
        request,
        "colonyCounterCalculations.html",
        {"floor": FLOOR_1, "ceiling": CEILING_1, "result": OPENTRONS_RESULT_1},
    )
