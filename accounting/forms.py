from django import forms
from djmoney.forms import MoneyField
from moneyed import Money
from .models import Account


class TransactionCreateSimpleForm(forms.Form):
    date = forms.DateField()
    description = forms.CharField(max_length=765)
    source = forms.ModelChoiceField(queryset=Account.objects.all())
    dest = forms.ModelChoiceField(queryset=Account.objects.all())
    amount = MoneyField(initial=Money(0, 'EUR'))
