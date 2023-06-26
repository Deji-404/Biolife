from django import forms
from .models import Payment


class PaymentInitForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['username', 'email', 'phone', 'address',]