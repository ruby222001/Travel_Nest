import json
from django.urls import path
import requests
from .models import Payment
from django.contrib import messages

from django.http import JsonResponse
from django.shortcuts import redirect, render
from homestay.models import Userdetails
from django.views.decorators.csrf import csrf_exempt



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
        information = request.POST.get('info')
        print(f'Username: {Username}, Email: {Email}, PhoneNumber: {PhoneNumber}, AdditionalInformation: {information}')

        if PhoneNumber:
            en = Userdetails(
                GuestFullName=Username,
                Email=Email,
                PhoneNumber=PhoneNumber,
                AdditionalInformation=information
            )
            en.save() 
            return redirect('payment')
    else:
        return render(request, 'user_details_form.html', {'step': step})

def payment(request):
    step = 3
    if request.method == 'POST':
        username = request.POST.get('fullInput')
        email = request.POST.get('email')
        phone_number = request.POST.get('number')

        # Create an instance of Userdetails and save it to the database
        user_detail = Userdetails.objects.create(
            GuestFullName=username,
            Email=email,
            PhoneNumber=phone_number,
            AdditionalInformation=""
        )

        # Perform any additional logic or redirect to another page
        return redirect('payment')

    else:
        return render(request, 'payment.html', {'step': step})
@csrf_exempt
def verify_payment(request):
    try:
        if request.method == 'POST':
          data = request.POST
          product_id = data.get('product_identity')
          token = data.get('token')
          amount = data.get('amount')

          url = "https://khalti.com/api/v2/payment/verify/"
          verify_payload = {
            "token": token,
            "amount": amount,
        }

          headers = {
            "Authorization": "Key test_secret_key_5e4c4d2114a54d119fbb859d4086947b"
        }

        response = requests.post(url, json=verify_payload, headers=headers)
        response_data = response.json()

        if response.status_code == 200:
            return JsonResponse({'status': 'success', 'message': 'Payment verified', 'data': response_data})
        else:
            return JsonResponse({'status': 'error', 'message': 'Payment verification failed', 'data': response_data}, status=500)

    
    except Exception as e:
        print(f"Exception: {e}") 
    # Handle other HTTP methods if needed
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)