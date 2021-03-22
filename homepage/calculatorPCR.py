from django import forms


class PCRForm(forms.Form):
    TOTALVOL = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False)
    WATER = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False)
    PCRBUFFER = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False)
    TEMPLATEDNA = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False)
    FINALCONC = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False)
