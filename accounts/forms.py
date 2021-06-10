from django import forms
from .models import Customer

class SignupForm(forms.ModelForm):

    name = forms.CharField(
        widget = forms.TextInput(
            attrs= {
                'label' : 'name',
            }
        )
    )
    class Meta:
        model = Customer
        fields = [
           'name',
            'email',
            'phone_number',
            'address'
        ]
