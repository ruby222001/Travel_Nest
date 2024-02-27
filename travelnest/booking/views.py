import json
from http.client import PAYMENT_REQUIRED

import requests
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

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
        transaction_id = request.GET.get('transaction_id')
        tidx = request.GET.get('tidx')
        amount = request.GET.get('amount')
        total_amount = request.GET.get('total_amount')
        mobile = request.GET.get('mobile')
        status = request.GET.get('status')
        purchase_order_id = request.GET.get('purchase_order_id')
        purchase_order_name = request.GET.get('purchase_order_name')

        data = {
            'pidx': pidx,
            'transaction_id': transaction_id,
            'tidx': tidx,
            'amount': amount,
            'total_amount': total_amount,
            'mobile': mobile,
            'status': status,
            'purchase_order_id': purchase_order_id,
            'purchase_order_name': purchase_order_name,
        }

        try:
            res = requests.post(url, headers=headers, data=json.dumps(data))
            print(res)
            print(res.text)

            new_res = res.json()
            print(new_res)

            if new_res.get('status') == 'Completed':
                # Payment successful, update your logic accordingly
                # For example:
                # user = request.user
                # user.has_verified = True
                # user.save()

                # Redirect to a success page or wherever you need
                return redirect('home')
            else:
                # Payment not successful, handle as needed
                # For example, show an error message
                return HttpResponseBadRequest("Payment not successful")
        except Exception as e:
            # Handle any exceptions or errors that might occur during the request
            print("Error verifying payment:", e)
            return HttpResponseBadRequest("Error verifying payment")

    return HttpResponseBadRequest("Invalid request")
