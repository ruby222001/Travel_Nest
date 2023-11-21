from django.http import HttpResponse
from django.shortcuts import redirect, render

from homestay.models import Userdetails


def home(request):
    return render(request, "home.html")

def booking(request):
    step = 1
    return render(request, 'booking.html', {'step': step})

def user_details(request):
    step = 2
    if request.method == 'POST':
        Username = request.POST.get('fullInput')
        Email = request.POST.get('email')
        PhoneNumber = request.POST.get('number')
        information=request.POST.get('info')
        print(f'Username: {Username}, Email: {Email}, PhoneNumber: {PhoneNumber}, AdditionalInformation: {information}')

        if PhoneNumber:
            en = Userdetails(
                GuestFullName=Username,
                Email=Email,
                PhoneNumber=PhoneNumber,
                AdditionalInformation=information)
        en = Userdetails(GuestFullName=Username, Email=Email, PhoneNumber=PhoneNumber,AdditionalInformation=information)
        en.save()
        # Process the form data and save it to the database
        # Redirect to a success page or do what's necessary
        return redirect('payment')
    else:

      return render(request, 'user_details_form.html', {'step': step})

def payment(request):
    step = 3
    return render(request, 'payment.html', {'step': step})
