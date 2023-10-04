from django.shortcuts import render,redirect
from django.http import HttpResponse
# Create your views here.
def home(request):
    return render(request,"home.html")
def booking(request):
    return render(request,"booking.html")



def user_details(request):
    if request.method == 'POST':
        # Process the form data and save it to the database
        # Redirect to a success page or do what's necessary
        return redirect('payment')
    return render(request, 'user_details_form.html')
def payment(request):
   
    return render(request,'payment.html')
