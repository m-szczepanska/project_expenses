from django import forms
from .models import Expense, Category


class ExpenseSearchForm(forms.ModelForm):

    date_from = forms.DateField(required=False)
    date_to = forms.DateField(required=False)

    class Meta:
        model = Expense
        fields = ('category', 'date',)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].required = False
        self.fields['date'].required = False