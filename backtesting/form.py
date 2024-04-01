from django import forms
from django.core.exceptions import ValidationError

class ConditionForm(forms.Form):
    stock = forms.CharField(label="Enter stock ticker (e.g., AAPL for apple)", widget=forms.TextInput(attrs={'class': 'form-control'}))
    start_date = forms.DateField(label="Starting Date", widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    condition1 = forms.BooleanField(label="CONDITION 1 => Closing Price > Simple Moving Average-50", required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    condition2 = forms.BooleanField(label="CONDITION 2 => Closing Price > Simple Moving Average-100", required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    condition3 = forms.BooleanField(label="CONDITION 3 => Closing Price > Simple Moving Average-150", required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    condition4 = forms.BooleanField(label="CONDITION 4 => Closing Price > Simple Moving Average-200", required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    condition5 = forms.BooleanField(label="CONDITION 5 => Simple Moving Average-50 > Simple Moving Average-100", required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    condition6 = forms.BooleanField(label="CONDITION 6 => Simple Moving Average-50 > Simple Moving Average-150", required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    condition7 = forms.BooleanField(label="CONDITION 7 => Simple Moving Average-50 > Simple Moving Average-200", required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    condition8 = forms.BooleanField(label="CONDITION 8 => Simple Moving Average-100 > Simple Moving Average-150", required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    condition9 = forms.BooleanField(label="CONDITION 9 => Simple Moving Average-100 > Simple Moving Average-200", required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    condition10 = forms.BooleanField(label="CONDITION 10 => Simple Moving Average-150 > Simple Moving Average-200", required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    def clean(self):
        cleaned_data = super().clean()
        selected_conditions = [
            cleaned_data['condition1'], cleaned_data['condition2'], cleaned_data['condition3'],
            cleaned_data['condition4'], cleaned_data['condition5'], cleaned_data['condition6'],
            cleaned_data['condition7'], cleaned_data['condition8'], cleaned_data['condition9'],
            cleaned_data['condition10']
        ]

        if not any(selected_conditions):
            raise ValidationError("At least one condition must be selected.")

    