import json
from http.client import PAYMENT_REQUIRED

import requests
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect, render
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
def initkhalti(request):
    if request.method == 'POST':
        url = "https://a.khalti.com/api/v2/epayment/initiate/"
        return_url = request.POST.get('return_url')
        amount = request.POST.get('amount')
        purchase_order_id = request.POST.get('purchase_order_id')

        user=request.user
        print("return_url",return_url)
        print("amount",amount)
        print("purchase_order_id",purchase_order_id)
        payload = json.dumps({
        "return_url": return_url,
        "website_url" : "http://127.0.0.1:8000",
        "amount": amount,
        "purchase_order_id": purchase_order_id,
        "purchase_order_name": "test",
        "customer_info": {
            "name": user.username,
            "email": "test@gmail.com",
            "phone": "9800000005",
        }
        })

        headers = {
    'Authorization': 'key f6a457f2166d415e9172144907325c3d',
        'Content-Type': 'application/json',
    }

        response = requests.post(url, headers=headers, data=payload)
        print(response.text)
        new_res =json.loads(response.text)

        print(new_res)
        return redirect(new_res['payment_url'])
    

    


def verify_payment(request):
    
    url = "https://a.khalti.com/api/v2/epayment/lookup/"
    if request.method == 'GET':
        headers = {
            'Authorization': 'key f6a457f2166d415e9172144907325c3d',
            'Content-Type': 'application/json',
        }
        pidx = request.GET.get('pidx')
        data = json.dumps({
            'pidx':pidx
        })
        res = requests.request('POST',url,headers=headers,data=data)
        print(res)
        print(res.text)

        new_res = json.loads(res.text)
        print(new_res)
        

        if new_res['status'] == 'Completed':
            # user = request.user
            # user.has_verified_dairy = True
            # user.save()
            # perform your db interaction logic
            pass
        
        # else:
        #     # give user a proper error message
        #     raise BadRequest("sorry ")

        return redirect('home')

    