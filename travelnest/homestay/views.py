from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .models import HomeStay, Feature, HomeStayImage
from booking.models import Booking, Review
from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.contrib import messages
from .recommendations import RecommendationSystem


# Create your views here.


def list(request):
    homestays = HomeStay.objects.filter(status='approved')

    # Assuming you have a logged-in user
    if request.user.is_authenticated:
        user_liked_homestays = request.user.liked_homestays.all()
        user_past_bookings = Booking.objects.filter(user=request.user)
        recommendation_system = RecommendationSystem(homestays)
        recommendations = recommendation_system.recommend_homestays(user_liked_homestays, user_past_bookings)
        
    else:
        recommendations = []

    return render(request, 'list.html', {'homestays': homestays, 'recommendations': recommendations})


def detail(request, homestay_id):
    homestay = get_object_or_404(HomeStay, id=homestay_id)
    today = timezone.now().date()
    booked_dates = Booking.objects.filter(
        homestay=homestay,
        check_out_date__gt=today
    ).values_list('user', 'check_in_date', 'check_out_date')

    # Convert QuerySet to list of dictionaries
    booked_dates_list = [
        {'user': item[0], 'check_in_date': item[1], 'check_out_date': item[2]} 
        for item in booked_dates
    ]

    # Serialize booked_dates_list to JSON
    booked_dates_json = json.dumps(booked_dates_list, cls=DjangoJSONEncoder)

    print("booked Dates JSON:", booked_dates_json)
    reviews = Review.objects.filter(homestay=homestay).order_by('-created_at')

    return render(request, 'detail.html', {'homestay': homestay, 'bookeddates': booked_dates_json, 'reviews': reviews})


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
        return redirect('guest_login')
    
    # Redirect the user back to the previous page
    return redirect(request.META.get('HTTP_REFERER'))