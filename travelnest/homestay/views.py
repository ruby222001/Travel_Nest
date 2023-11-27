import json
from django.urls import path
import requests
from . import views

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
    return render(request, 'payment.html', {'step': step})

@csrf_exempt
def verify_payment(request):
    if request.method == 'POST':
        data = request.POST
        product_id = data.get('product_identity')
        token = data.get('token')
        amount = data.get('amount')

        url = "https://khalti.com/api/v2/payment/verify/"
        payload = {
            "token": token,
            "amount": amount,
        }

        headers = {
            "Authorization": "Key test_secret_key_5e4c4d2114a54d119fbb859d4086947b"
        }

        response = requests.post(url, payload, headers = headers)
   
        response_data = json.loads(response.text)
        status_code = str(response.status_code)

        if status_code == '400':
         response = JsonResponse({'status':'false','message':response_data['detail']}, status=500)
         return response

        import pprint 
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(response_data)
   
        return JsonResponse(f"Payment Done !! With IDX. {response_data['user']['idx']}",safe=False)
          