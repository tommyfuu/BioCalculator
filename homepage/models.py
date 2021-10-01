# from django.db import models


# class Country(models.Model):
#     name = models.CharField(max_length=30)

#     def __str__(self):
#         return self.name

# class City(models.Model):
#     country = models.ForeignKey(Country, on_delete=models.CASCADE)
#     name = models.CharField(max_length=30)

#     def __str__(self):
#         return self.name

# class Person(models.Model):
#     name = models.CharField(max_length=100)
#     birthdate = models.DateField(null=True, blank=True)
#     country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
#     city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)

#     def __str__(self):
#         return self.name


# ############ MAYBE WILL BE USEFUL LATER
# # Create your models here.
# unitDict = {('g', 'kg'): 0.001, ('g', 'pg'): 10**12, ('g', 'ng'): 10**9, ('g', 'μg'): 10**6, ('g', 'mg'): 10**3, ('g', 'cg'): 100, ('g', 'Mg'): 10**-6, ('g', 'Gg'): 10**-9, ('g', 'Tg'): 10**-12,
#             ('M', 'kM'): 0.001, ('M', 'pM'): 10**12, ('M', 'nM'): 10**9, ('M', 'μM'): 10**6, ('M', 'mM'): 10**3, ('M', 'cM'): 100, ('M', 'MM'): 10**-6, ('M', 'GM'): 10**-9, ('M', 'TM'): 10**-12,
#             ('L', 'kL'): 0.001, ('L', 'pL'): 10**12, ('L', 'nL'): 10**9, ('L', 'μL'): 10**6, ('L', 'mL'): 10**3, ('L', 'cL'): 100, ('L', 'ML'): 10**-6, ('L', 'GL'): 10**-9, ('L', 'TL'): 10**-12,
#             ('mol', 'kmol'): 0.001, ('mol', 'pmol'): 10**12, ('mol', 'nmol'): 10**9, ('mol', 'μmol'): 10**6, ('mol', 'mmol'): 10**3, ('mol', 'cmol'): 100, ('mol', 'Mmol'): 10**-6, ('mol', 'Gmol'): 10**-9, ('mol', 'Tmol'): 10**-12,
#             ('mol/L', 'M'): 1,
#             ('g/L', 'kg/L'): 0.001, ('g/L', 'pg/L'): 10**12, ('g/L', 'ng/L'): 10**9, ('g/L', 'μg/L'): 10**6, ('g/L', 'mg/L'): 10**3, ('g/L', 'cg/L'): 100, ('g/L', 'Mg/L'): 10**-6, ('g/L', 'Gg/L'): 10**-9, ('g/L', 'Tg/L'): 10**-12}
# unitMolarMassDict = {('kg/L', 'M'): 1}
# metricUnits = ['g', 'M', 'L', 'mol']

# MASSCHOICES = [('g', 'g'), ('kg', 'kg'), ('pg', 'pg'), ('ng', 'ng'), ('μg', 'μg'),
#                ('mg', 'mg'), ('cg', 'cg'), ('Mg', 'Mg'), ('Gg', 'Gg'), ('Tg', 'Tg')]
# VOLCHOICES = [('L', 'L'), ('kL', 'kL'), ('pL', 'pL'), ('nL', 'nL'), ('μL', 'μL'),
#               ('mL',                    'mL'), ('cL', 'cL'), ('ML', 'ML'), ('GL', 'GL'), ('TL', 'TL')]
# CONCCHOICESMOLARITY = [('M', 'M'), ('kM', 'kM'), ('pM', 'pM'), ('nM', 'nM'), ('μM', 'μM'),
#                        ('mM', 'mM'), ('cM', 'cM'), ('MM', 'MM'), ('GM', 'GM'), ('TM', 'TM'), ('ppm', 'ppm')]
# CONCCHOICESMASSPERVOL = [('g/L', 'g/L'), ('kg/L', 'kg/L'),
#                          ('mg/L', 'mg/L')]

# UNITCHOICES = MASSCHOICES + VOLCHOICES + \
#     CONCCHOICESMOLARITY + CONCCHOICESMASSPERVOL


# # For the unit conversion dependent drop-down menu to reduce options
# class UnitSubset(models.Model):
#     name = models.CharField(max_length=10)

#     def __str__(self):
#         return self.name


# class Unit(models.Model):
#     unitSubset = models.ForeignKey(UnitSubset, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.name


# class UnitConversionInputs(models.Model):
#     INPUTVALUE = models.DecimalField(
#         decimal_places=5, max_digits=10000, required=True, label=False)
#     INPUTUNITSUBSET = models.ForeignKey(
#         UnitSubset, on_delete=models.SETNULL, blank=True, null=True)
#     INPUTUNIT = models.ForeignKey(
#         Unit, on_delete=models.SETNULL, blank=True, null=True)
#     OUTPUTVALUE = models.DecimalField(
#         decimal_places=5, max_digits=10000, required=False, label=False)
#     OUTPUTUNIT = models.ForeignKey(
#         UnitSubset, on_delete=models.SETNULL, blank=True, null=True)
#     MOLARMASS = models.DecimalField(
#         decimal_places=5, max_digits=10000, required=False, label=False)
    
#     def __str__(self):
#         return self.name