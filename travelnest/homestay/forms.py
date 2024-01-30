from django import forms

class ConfirmationForm(forms.Form):
    fullname = forms.CharField(label='Guest Full Name')
    email = forms.EmailField(label='Email')
    phone_number = forms.CharField(label='Phone Number')
