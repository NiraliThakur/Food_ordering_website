from django import forms
from .models import ShippingInformation

class ShippingForm(forms.ModelForm):
    class Meta:
        model = ShippingInformation
        fields = ['full_name', 'address', 'city', 'state', 'zip_code', 'email']
