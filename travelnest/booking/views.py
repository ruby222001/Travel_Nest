import json

import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_exempt

from homestay.models import HomeStay

from .models import Booking, Review
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.sessions.models import Session
from django.contrib import messages

# Create your views here.


@login_required
def book_homestay(request, homestay_id):
    homestay = get_object_or_404(HomeStay, id=homestay_id)
    user = request.user

    if user.is_authenticated:
        if user.is_host:
            # If user is a host, display error message
            messages.error(request, 'You are logged in as a host.')
            return redirect('detail', homestay_id=homestay.id)
        else:
            # User is a guest, allow booking
            if request.method == 'POST':
                # Process form submission
                check_in_date = request.POST.get('formatted_check_in_date')
                check_out_date = request.POST.get('formatted_check_out_date')
                num_guests = int(request.POST.get('num_guests'))
                totalAmount = request.POST.get('totalAmount') 
                payment_type = request.POST.get('payment_option')

                # Perform validation as needed
                if check_in_date and check_out_date and num_guests and payment_type:
                    # Convert num_guests to an integer
                    num_guests = int(num_guests)

                    # Create a new booking instance and save it
                    booking = Booking.objects.create(
                        homestay=homestay,
                        user=user,
                        check_in_date=check_in_date,
                        check_out_date=check_out_date,
                        num_guests=num_guests,
                        amount=totalAmount,
                        payment_type=payment_type
                    )
                    # Proceed with booking or display confirmation
                    messages.success(request, 'Booking successful!')

                    # # Send confirmation email to the user
                    # subject = 'Homestay Booking Confirmation'
                    # html_message = render_to_string('booking_confirmation_email.html', {'homestay': homestay, 'booking': booking})
                    # plain_message = strip_tags(html_message)
                    # send_mail(subject, plain_message, settings.EMAIL_HOST_USER, [request.user.email], html_message=html_message)
                    return redirect('detail', homestay_id=homestay.id)
                else:
                    # Handle invalid form data
                    messages.error(request, 'Invalid form data. Please fill in all fields.')
                    return redirect('detail', homestay_id=homestay.id)
            else:
                return render(request, 'detail.html', {'homestay': homestay})
    else:
        # If user is not authenticated, display error message
        messages.error(request, 'You must be logged in to book a homestay.')
        return render(request, 'detail.html', {'homestay': homestay})
    
def add_review(request, homestay_id):
    today = timezone.now().date()
    print("Today's Date:", today)

    homestay = get_object_or_404(HomeStay, id=homestay_id)

    user_has_booked_homestay = Booking.objects.filter(
    homestay=homestay,
    user=request.user,

    ).exists()

    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        if request.user.is_authenticated and user_has_booked_homestay:
            Review.objects.create(
                homestay=homestay,
                user=request.user,
                rating=rating,
                comment=comment
            )
            messages.success(request, 'Review submitted successfully.')
        else:
            messages.error(request, 'Unable to submit the review.')

    reviews = Review.objects.filter(homestay=homestay).order_by('-created_at')
    # Inside the add_review view
    print("User has booked homestay:", user_has_booked_homestay)


    return render(request, 'detail.html', {'homestay': homestay, 'reviews': reviews, 'user_has_booked_homestay': user_has_booked_homestay})

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
            
            "name": "ram",
            "eamil": "email@gmail.com",
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

        data = json.dumps({
            'pidx': pidx,
            'transaction_id': transaction_id,
            'tidx': tidx,
            'amount': amount,
            'total_amount': total_amount,
            'mobile': mobile,
            'status': status,
            'purchase_order_id': purchase_order_id,
            'purchase_order_name': purchase_order_name,
        })

        try:
            res = requests.post(url, headers=headers, data=json.dumps(data))
            print(res)
            print(res.text)

            new_res = res.json.loads(res.text)
            print(new_res)

            if new_res.get('status') == 'Completed':
                # Payment successful, update your logic accordingly
                # For example:
                # user = request.user
                # user.has_verified = True
                # user.save()

                # Redirect to a success page or wherever you need
                return redirect('home')  # Ensure 'home' is the correct URL name
            else:
                # Payment not successful, handle as needed
                # For example, show an error message
                return HttpResponseBadRequest("Payment not successful")
        except Exception as e:
            # Handle any exceptions or errors that might occur during the request
            print("Error verifying payment:", e)
            # Attempt to create the booking instance from session data
            booking_data = request.session.get('booking_data')
            messages.success(request,'Booking Sucessful.')
            return redirect('home')

    return HttpResponseBadRequest("Invalid request")



def store_booking_data(request):
    if request.method == 'POST':
        booking_data = request.POST.get('booking_data')
        request.session['booking_data'] = booking_data
        return JsonResponse({'message': 'Booking data stored successfully.'})
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)