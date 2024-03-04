import json
from django.contrib import messages
from .recommendations import RecommendationSystem

import requests
from django.contrib import messages
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from booking.models import Booking, Review

from .models import Feature, HomeStay, HomeStayImage
from django.db.models import Avg
from itertools import chain
from django.db.models import Q
from datetime import datetime

# Create your views here.


def list(request):
    homestays = HomeStay.objects.filter(status='approved')

    for homestay in homestays:
        average_rating = Review.objects.filter(homestay=homestay).aggregate(Avg('rating'))['rating__avg']
        homestay.average_rating = round(average_rating, 1) if average_rating else None

    homestays = sorted(homestays, key=lambda x: x.average_rating if x.average_rating is not None else float('-inf'), reverse=True)
        

    # Assuming you have a logged-in user
    if request.user.is_authenticated:
        if request.user.is_guest:
            user_liked_homestays = request.user.liked_homestays.all()
            user_past_bookings = Booking.objects.filter(user=request.user)
            recommendation_system = RecommendationSystem(homestays)
            recommendations = recommendation_system.recommend_homestays(user_liked_homestays, user_past_bookings)
            
            
            # Get IDs of homestays liked by the user
            liked_homestay_ids = user_liked_homestays.values_list('id', flat=True)
            
            # Get IDs of homestays from user's past bookings
            past_booking_homestay_ids = user_past_bookings.values_list('homestay__id', flat=True)

            # Combine both lists to get homestays to exclude
            exclude_homestay_ids = set(chain(liked_homestay_ids, past_booking_homestay_ids))

            # Filter recommendations to exclude homestays liked by the user and from past bookings
            filtered_recommendations = [recommendation for recommendation in recommendations if recommendation['homestay'].id not in exclude_homestay_ids]
            
            print(filtered_recommendations)  # Print filtered recommendations

        else:
          
            recommendations = []
            filtered_recommendations = []
            
        
    else:
        recommendations = []
        filtered_recommendations = []

    return render(request, 'list.html', {'homestays': homestays, 'recommendations': recommendations, 'filtered_recommendation':filtered_recommendations})


def detail(request, homestay_id):
    homestay = get_object_or_404(HomeStay, id=homestay_id)
    today = timezone.now().date()
    booked_dates = Booking.objects.filter(
        homestay=homestay,
        check_out_date__gt=today
    ).values_list('user', 'check_in_date', 'check_out_date')

    if request.user.is_authenticated:
        user_has_booked_homestay = Booking.objects.filter(
                homestay=homestay,
                user=request.user,
                check_out_date__lt=today
            ).exists()
    else:
        user_has_booked_homestay = None
    

    # Convert QuerySet to list of dictionaries
    booked_dates_list = [
        {'user': item[0], 'check_in_date': item[1], 'check_out_date': item[2]} 
        for item in booked_dates
    ]

    # Serialize booked_dates_list to JSON
    booked_dates_json = json.dumps(booked_dates_list, cls=DjangoJSONEncoder)

    print("booked Dates JSON:", booked_dates_json)
    reviews = Review.objects.filter(homestay=homestay).order_by('-created_at')

    return render(request, 'detail.html', {'homestay': homestay, 'bookeddates': booked_dates_json, 'reviews': reviews, 'user_has_booked_homestay': user_has_booked_homestay})


def like_homestay(request, homestay_id):
    homestay = get_object_or_404(HomeStay, id=homestay_id)
    user = request.user
    
    if user.is_authenticated:
        if user.is_guest:
            if homestay in user.liked_homestays.all():
                # User has already liked the homestay, so unlike it
                homestay.liked_by_users.remove(user)
            else:
                # User hasn't liked the homestay yet, so like it
                homestay.liked_by_users.add(user)
        if user.is_host:
            # Handle case where user is not a guest
            messages.error(request, 'You are logged in as a host.')
    else:
        # Handle case where user is not authenticated
        messages.error(request, 'Please log in to like a homestay')
    
    # Redirect the user back to the previous page
    return redirect(request.META.get('HTTP_REFERER'))



# //to admin

@csrf_exempt
def verifyy_payment(request):
    try:
        if request.method == 'POST':
            data = request.POST
            product_id = data.get('product_identity')
            token = data.get('token')
            amount = data.get('amount')

            url = "https://khalti.com/api/v2/payment/verifyy_payment/"
            verify_payload = {
                "token": token,
                "amount": amount,
            }

            headers = {
    "Authorization": "Key test_secret_key_f59e8b7d18b4499ca40f68195a846e9b"
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
    

def search(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        homestays = HomeStay.objects.all()

        if query:
            homestays = homestays.filter(
                Q(name__icontains=query) |
                Q(location__icontains=query) | 
                Q(features__name__icontains=query) 
                
            )
        else:
            homestays = HomeStay.objects.all()
            for homestay in homestays:
                average_rating = Review.objects.filter(homestay=homestay).aggregate(Avg('rating'))['rating__avg']
                homestay.average_rating = round(average_rating, 1) if average_rating else None
    else:
        homestays = HomeStay.objects.all()
        for homestay in homestays:
            average_rating = Review.objects.filter(homestay=homestay).aggregate(Avg('rating'))['rating__avg']
            homestay.average_rating = round(average_rating, 1) if average_rating else None

    return render(request, 'search.html', {'homestays': homestays})
    

def search_input(request):
    if request.method == 'GET':
        location = request.GET.get('location')
        checkin_date_str = request.GET.get('checkin_date')
        checkout_date_str = request.GET.get('checkout_date')

        if location and checkin_date_str and checkout_date_str:
            checkin_date = datetime.strptime(checkin_date_str, '%Y-%m-%d').date()
            checkout_date = datetime.strptime(checkout_date_str, '%Y-%m-%d').date()

            # Filter homestays by location
            homestays = HomeStay.objects.filter(location__icontains=location)

            # Exclude homestays with bookings overlapping with the provided dates
            booked_homestay_ids = Booking.objects.filter(
                Q(check_in_date__lte=checkin_date, check_out_date__gte=checkin_date) |
                Q(check_in_date__lte=checkout_date, check_out_date__gte=checkout_date)
            ).values_list('homestay_id', flat=True)

            homestays = homestays.exclude(id__in=booked_homestay_ids)
            for homestay in homestays:
                average_rating = Review.objects.filter(homestay=homestay).aggregate(Avg('rating'))['rating__avg']
                homestay.average_rating = round(average_rating, 1) if average_rating else None

        else:
            homestays = HomeStay.objects.all()
    else:
        homestays = HomeStay.objects.all()

    return render(request, 'search.html', {'homestays': homestays})


def all_bookings(request):
    bookings = Booking.objects.all()
    return render(request, 'all_bookings.html', {'bookings': bookings})