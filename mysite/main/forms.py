from django import forms
from .models import Account

class UpdateAccount(forms.Form):
    class Meta:
        model = Account
        image = forms.ImageField()