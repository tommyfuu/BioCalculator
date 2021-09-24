from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

import random


class RandomNumGenerator_1(forms.Form):
    floor = forms.DecimalField(
        decimal_places=0, max_digits=10000, required=True, label=False
    )
    ceiling = forms.DecimalField(
        decimal_places=0, max_digits=10000, required=True, label=False
    )


def randomNumGenerator_1(floor, ceiling):
    """Given a floor and ceiling integer, generates a random
    number between those two integers"""

    return random.randint(floor, ceiling)
