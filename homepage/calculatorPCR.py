from django import forms


class PCRForm(forms.Form):
    TOTALVOL = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False)
    WACONC = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False)
    INPUTSOLUTE = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False)
    FINALVOL = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False)
    FINALCONC = forms.DecimalField(
        decimal_places=5, max_digits=10000, required=False)
