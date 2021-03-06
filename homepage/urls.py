from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('faq/', views.faq, name='faq'),
    path('about/', views.about, name='about'),
    path('calculators/', views.calculators, name='calculators'),
    path('dilutionCalculator/', views.dilution_input_view, name='dilution'),
    path('dilutionCalculatorResult/', views.dilution_result_view, name='dilution'),
    path('PCRCalc/', views.pcr_input_view, name='PCR'),
    path('PCRCalcResult/', views.pcr_result_view, name='PCR'),
    path('PCRCalcError/', views.pcr_error_view, name='PCR'),
    path('calcUnitConvert/', views.unit_convert_input_view, name='unit conversion'),
    path('calcUnitConvertResult/', views.pcr_result_view, name='unit conversion'),
    path('calcUnitConvertError/', views.pcr_error_view, name='unit conversion'),
    path('calcUnitConvert/', views.unit_convert_input_view, name='unit conversion'),
    path('cutting/', views.cutting_reaction_input_view, name='Cutting Reaction'),
    path('cuttingResults/', views.cutting_reaction_result_view, name = 'Cutting Reaction')
    ]
