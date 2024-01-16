from django import forms

class BookingForm(forms.Form):
    check_in_date = forms.DateField()
    check_out_date = forms.DateField()
    num_guests = forms.IntegerField()
    price_per_night=forms.IntegerField()
    payment_method = forms.CharField()
    user_email = forms.EmailField()
