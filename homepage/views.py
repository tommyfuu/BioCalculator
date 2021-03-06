from django.shortcuts import render, HttpResponse, HttpResponseRedirect
# importing calculators
from .calculatorDilution import DilutionForm
from .calculatorDilution import *
# Create your views here.


def home(request):
    # return HttpResponse("Home page!")
    return render(request, 'login.html', {})


def contact(request):
    # return HttpResponse("Contact page!")
    return render(request, 'contact.html', {})


def about(request):
    # return HttpResponse("Contact page!")
    return render(request, 'about.html', {})

# CALCULATORS
# DILUTION CALCULATOR
### GLOBAL VARIABLES
INPUTVOL = None
INPUTCONC = None
INPUTSOLUTE = None
FINALVOL = None
FINALCONC = None
ADDEDSOLUTE = None
ADDEDWATER = None

def dilution_input_view(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = DilutionForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            inputVol = form.cleaned_data['INPUTVOL']
            inputConc = form.cleaned_data['INPUTCONC']
            inputSolute = form.cleaned_data['INPUTSOLUTE']
            finalVol = form.cleaned_data['FINALVOL']
            finalConc = form.cleaned_data['FINALCONC']
            addedSoluteVol = form.cleaned_data['ADDEDSOLUTE']
            waterVol = form.cleaned_data['ADDEDWATER']
            # inputVol, inputConc, inputSolute, finalVol, finalConc, addedSoluteVol, addedWater = changeConcentrationTable(
            #     inputVol, inputConc, finalVol, finalConc, inputSolute, addedSoluteVol)
            # INPUTVOL = inputVol
            # INPUTCONC = inputConc
            # INPUTSOLUTE = inputSolute
            # FINALCONC = finalConc

            INPUTVOL, INPUTCONC, INPUTSOLUTE, FINALVOL, FINALCONC, ADDEDSOLUTE, ADDEDWATER = changeConcentrationTable(inputVol, inputConc, finalVol, finalConc, inputSolute, addedSoluteVol)
            print("Here are the calculated input values for your desired output:")
            # print(c)
            # print(inputVol, inputConc, inputSolute, finalVol,
            #       finalConc, addedSoluteVol, addedWater)
            # redirect to a new URL:
            # return HttpResponseRedirect('http://127.0.0.1:8000/dilutionCalculatorResult')
            return render(request, 'concentrationCalcResult.html', {"inputVol": INPUTVOL, "inputConc": INPUTCONC, "inputSolute": INPUTSOLUTE, "finalVol": FINALVOL, "finalConc": FINALCONC, "addedSolute": ADDEDSOLUTE, "addedWater": ADDEDWATER})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = DilutionForm()
    return render(request, "concentrationCalc.html", {'form': form})


def dilution_result_view(request):
    # return HttpResponse("Contact page!")
    return render(request, 'concentrationCalcResult.html', {"inputVol": INPUTVOL, "inputConc": INPUTCONC, "inputSolute": INPUTSOLUTE, "finalVol": FINALVOL, "finalConc": FINALCONC, "addedSolute": ADDEDSOLUTE, "addedWater": ADDEDWATER})
