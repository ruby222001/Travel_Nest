from http.client import PAYMENT_REQUIRED
from django.http import JsonResponse
from django.shortcuts import redirect, render
import requests
from django.views.decorators.csrf import csrf_exempt


def home(request):
    return render(request, 'home.html')

def details(request):
    if request.method == 'POST':
        username = request.POST.get('fullInput')
        email = request.POST.get('email')
        phone_number = request.POST.get('number')
        payment_method = request.POST.get('paymentMethod')

        payment_instance = payment_method.objects.create(
            GuestFullName=username,
            Email=email,
            PhoneNumber=phone_number,
            paymentmethod=payment_method,
        )

        return redirect('details')

    else:
        return render(request, 'details.html')
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
    




