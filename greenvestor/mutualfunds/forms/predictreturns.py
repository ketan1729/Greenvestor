from django import forms
from ..models import Fund

ALL_FUND_NAMES = list(Fund.objects.values_list('symbol', flat=True).distinct())


def validate_name(value):
    fund_names = [x.strip() for x in value.split(",")]
    for fund in fund_names:
        if fund.upper() not in ALL_FUND_NAMES:
            raise forms.ValidationError("Incorrect fund names")
    return value


class PredictReturnsForm(forms.Form):
    fund = forms.CharField(label="Enter name of fund", max_length=250,
                            widget=forms.TextInput(attrs={'class': "form-element"}), validators=[validate_name])
