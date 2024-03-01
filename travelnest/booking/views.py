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
            return redirect('detail', homestay_id=homestay.id)
        else:
            messages.error(request, 'Unable to submit the review.')
            return redirect('detail', homestay_id=homestay.id)

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
        host_user = request.POST.get('host_user')
        host_email = request.POST.get('host_email')
        host_mobile = request.POST.get('host_mobile')
        homestay_id = request.POST.get('homestay_id')
        homestay_id = request.POST.get('homestay_name')
        check_in_date = request.POST.get('check_in')
        check_out_date = request.POST.get('check_out')
        num_guests = request.POST.get('num_guest')
        payment_type = request.POST.get('payment_type')
        
        # Store values in session
        request.session['host_name'] = host_user
        request.session['host_email'] = host_email
        request.session['homestay_id'] = homestay_id
        request.session['check_in_date'] = check_in_date
        request.session['check_out_date'] = check_out_date
        request.session['num_guests'] = num_guests
        request.session['total_amount'] = amount
        request.session['payment_type'] = payment_type

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
            "name": host_mobile,
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
            host_name = request.session.get('host_name')
            host_email = request.session.get('host_email')
            homestay_id = request.session.get('homestay_id')
            check_in_date = request.session.get('check_in_date')
            check_out_date = request.session.get('check_out_date')
            num_guests = request.session.get('num_guests')
            total_amount = request.session.get('total_amount')
            payment_type = request.session.get('payment_type')
            # user = request.user
            # user.has_verified_dairy = True
            # user.save()
            # perform your db interaction logic
            messages.success(request, 'You have booked successfully')
        
        # else:
        #     # give user a proper error message
        #     raise BadRequest("sorry ")

        return redirect('home')



def store_booking_data(request):
    if request.method == 'POST':
        booking_data = request.POST.get('booking_data')
        request.session['booking_data'] = booking_data
        return JsonResponse({'message': 'Booking data stored successfully.'})
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)