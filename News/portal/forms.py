
from django import forms


class DateRangeFilterForm(forms.Form):
    start_range = forms.DateTimeField(required=True, label='Data Inicial',
                                      widget=forms.DateTimeInput(attrs={'class': 'input-group-field', 'type': 'date'}))
    end_range = forms.DateTimeField(required=True, label='Data Final',
                                    widget=forms.DateTimeInput(attrs={'class': 'input-group-field', 'type': 'date'}))

