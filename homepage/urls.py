from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('dilutionCalculator/', views.dilution_input_view, name='dilution'),
    path('dilutionCalculatorResult/', views.dilution_result_view, name='dilution'),
    path('PCRCalc/', views.pcr_input_view, name='PCR'),
    path('PCRCalcResult/', views.pcr_result_view, name='PCR'),
    path('PCRCalcError/', views.pcr_error_view, name='PCR'),
    path('calcUnitConvert/', views.unit_convert_input_view, name='unit conversion'),
    path('calcUnitConvertResult/', views.pcr_result_view, name='unit conversion'), 
    path('calcUnitConvertError/', views.pcr_error_view, name='unit conversion'),
]
