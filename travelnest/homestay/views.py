from django.shortcuts import render, redirect
from django.http import HttpResponse

def home(request):
    return render(request, "home.html")

def booking(request):
    step = 1
    return render(request, 'booking.html', {'step': step})

def user_details(request):
    step = 2
    if request.method == 'POST':
        # Process the form data and save it to the database
        # Redirect to a success page or do what's necessary
        return redirect('payment')
    return render(request, 'user_details_form.html', {'step': step})

def payment(request):
    step = 3
    return render(request, 'payment.html', {'step': step})
