from django import forms
# from django.db import models

# class PCRForm(forms.Form):
#     TOTALVOL = forms.DecimalField(
#         decimal_places=5, max_digits=10000, required=False)
#     WATER = forms.DecimalField(
#         decimal_places=5, max_digits=10000, required=False)
#     PCRBUFFER = forms.DecimalField(
#         decimal_places=5, max_digits=10000, required=False)
#     TEMPLATEDNA = forms.DecimalField(
#         decimal_places=5, max_digits=10000, required=False)
#     FINALCONC = forms.DecimalField(
#         decimal_places=5, max_digits=10000, required=False)

STATES = (
    ('', 'Choose...'),
    ('MG', 'Minas Gerais'),
    ('SP', 'Sao Paulo'),
    ('RJ', 'Rio de Janeiro')
)


class PCRForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput())
    address_1 = forms.CharField(
        label='Address',
        widget=forms.TextInput(attrs={'placeholder': '1234 Main St'})
    )
    address_2 = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Apartment, studio, or floor'})
    )
    city = forms.CharField()
    state = forms.ChoiceField(choices=STATES)
    zip_code = forms.CharField(label='Zip')
    check_me_out = forms.BooleanField(required=False)
    # PRIMER = forms.DecimalField(
    #     decimal_places=5, max_digits=10000, required=False, label='Input Liquid Volume')
    # TEMPLATEDNA = forms.DecimalField(
    #     decimal_places=5, max_digits=10000, required=False, label='Input Liquid Volume')

    # Last_Name=models.CharField(max_length=30)
    # City=models.CharField(max_length=30)
