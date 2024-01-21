from django import forms
from .models import *


# mtn_payment_app/forms.py


from django import forms

class PaymentForm(forms.Form):
    correlatorId = forms.CharField(max_length=36, required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter Correlator ID'}))
    amount = forms.DecimalField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter Amount'}))
    units = forms.CharField(max_length=10, required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter Units'}))
    payerIdType = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter Payer ID Type'}))
    payerId = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter Payer ID'}))
    payerNote = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter Payer Note'}))
    payerRef = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter Payer Reference'}))
    includePayerCharges = forms.BooleanField(required=False)
    payeeIdType = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter Payee ID Type'}))
    payeeId = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter Payee ID'}))
    payeeNote = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter Payee Note'}))
    callbackURL = forms.URLField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter Callback URL'}))
    channel = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter Channel'}))
    