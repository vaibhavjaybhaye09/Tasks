from django import forms
from .models import Threshold, Station


class ThresholdForm(forms.ModelForm):
    class Meta:
        model = Threshold
        fields = ['limit_value']


class StationForm(forms.ModelForm):
    class Meta:
        model = Station
        fields = ['name', 'current_value']
