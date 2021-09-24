from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Image
import random


class ColonyCounterForm(forms.ModelForm):
    # floor = forms.DecimalField(
    #     decimal_places=0, max_digits=10000, required=True, label=False
    # )
    # ceiling = forms.DecimalField(
    #     decimal_places=0, max_digits=10000, required=True, label=False
    # )
    class Meta:
        model = Image
        fields = ('title', 'image')


def randomNumGenerator_1(floor, ceiling):
    """Given a floor and ceiling integer, generates a random
    number between those two integers"""

    return random.randint(floor, ceiling)
