import json
from django.urls import path
import requests
from hosting.models import Homestay
from hosting.views import list_homestays
from .models import Payment
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404


def home(request):
    return render(request, "home.html")

def booking(request,id):
    step = 1
    list_homestays = Homestay.objects.get(id=id) 
     
    return render(request,'booking.html',  {'step': step,'list_homestays':list_homestays,'homestay_id':id})

def confirmation(request, homestay_id):
    arrival_date = request.GET.get('arrival_date')
    departure_date = request.GET.get('departure_date')
    total_guests = request.GET.get('total_guests')

    list_homestays = get_object_or_404(Homestay, id=homestay_id)

    return render(request, 'confirmation.html', {
        'step': 2,
        'list_homestays': list_homestays,
        'arrival_date': arrival_date,
        'departure_date': departure_date,
        'total_guests': total_guests,
        'total_price': calculate_total_price(list_homestays.price),
    })

def calculate_total_price(base_price):
    # Perform any calculations for total price here
    return base_price
def payment(request):
    step=3
    if request.method == 'POST':
        username = request.POST.get('fullInput')
        email = request.POST.get('email')
        phone_number = request.POST.get('number')
        payment_method = request.POST.get('paymentMethod')

        payment_instance = Payment.objects.create(
            GuestFullName=username,
            Email=email,
            PhoneNumber=phone_number,
            paymentmethod=payment_method,
        )

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
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)
    



