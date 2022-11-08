from collections import OrderedDict
from django import forms
from .models import Expense, Category


class ExpenseSearchForm(forms.Form):
    date_from = forms.DateField(required=False)
    date_to = forms.DateField(required=False)

    category = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        fields = ('category', 'date',)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].required = False