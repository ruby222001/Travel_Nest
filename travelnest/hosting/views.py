from http.client import PAYMENT_REQUIRED
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import requests
from .models import HomeStay, Feature, HomeStayImage
from django.http import JsonResponse
from booking.models import Booking, Review
from django.utils import timezone
from django.db.models import Avg
from django.db import connection
from django.contrib.auth.models import User
from django.db.models import Count
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.views.decorators.csrf import csrf_exempt




# Create your views here.


def home(request):
    return render(request, 'home.html')
def about(request):
    return render(request,'about.html')

def host_dashboard(request):
    user = request.user
    homestays = HomeStay.objects.filter(host=user)

    # Get the status parameter from the URL
    status = request.GET.get('status', 'approved')

    # Filter homestays based on status
    if status == 'approved':
        homestays = homestays.filter(status='approved')
    elif status == 'pending':
        homestays = homestays.filter(status='pending')
    elif status == 'unapproved':
        homestays = homestays.filter(status='unapproved')

    return render(request, 'host.html', {'user': user, 'homestays': homestays, 'status': status})

@login_required
def add(request):
    if request.method == 'POST':
        host = request.user
        name = request.POST.get('name')
        location = request.POST.get('location')
        num_guests = request.POST.get('num_guests')
        price_per_night = request.POST.get('price_per_night')
        ownership_documents = request.FILES.get('ownership_documents')
        citizenship_documents = request.FILES.get('citizenship_documents')
        thumbnail_image = request.FILES.get('thumbnail_image')
        secondary_images = request.FILES.getlist('secondary_images')
        description = request.POST.get('description')
        features = request.POST.getlist('features')
        status = 'pending'

        homestay = HomeStay(
            host=host,
            name=name,
            location=location,
            num_guests=num_guests,
            price_per_night=price_per_night,
            ownership_documents=ownership_documents,
            citizenship_documents=citizenship_documents,
            thumbnail_image=thumbnail_image,
            description=description,
            status=status,
        )
        homestay.save()

        # Add secondary images
        for image in request.FILES.getlist('secondary_images'):
            HomeStayImage.objects.create(homestay=homestay, image=image)

        # Add features
        for feature_id in features:
            feature = Feature.objects.get(pk=feature_id)
            homestay.features.add(feature)

        # Redirect to a success page or do something else
        return redirect('host_dashboard')  # Change 'success_page' to your desired success page URL

    else:
        features = Feature.objects.all()
        return render(request, 'add.html', {'features': features})

def approved(request):
    # Logic for handling "Add Approved" option
    return render(request, 'approved.html')

def pending(request):
    # Logic for handling "Pending" option
    return render(request, 'a.html')

def unapproved(request):
    # Logic for handling "Unapproved" option
    return render(request, 'unapproved.html')

def bookings(request):
    # Logic for handling "Bookings" option
    return render(request, 'bookings.html')

def list(request):
    homestays = HomeStay.objects.filter(status='approved')
    for homestay in homestays:
        average_rating = Review.objects.filter(homestay=homestay).aggregate(Avg('rating'))['rating__avg']
        homestay.average_rating = round(average_rating, 1) if average_rating else None
    return render(request, 'list.html', {'homestays': homestays})

@login_required
def like_homestay(request, homestay_id):
    homestay = get_object_or_404(HomeStay, id=homestay_id)

    if request.method == 'POST' and request.user.is_guest:
        if homestay.liked_by_users.filter(id=request.user.id).exists():
            homestay.liked_by_users.remove(request.user)
        else:
            homestay.liked_by_users.add(request.user)
        return redirect('list')
    if request.method == 'POST' and request.user.is_host:
        messages.error('You are logged in as a host.')
    else:
        return redirect('guest_login')


def homestay_details(request, homestay_id):
    homestay = get_object_or_404(HomeStay, id=homestay_id)

    if request.user.is_authenticated:
        # Check if the user has booked the homestay in the past
        today = timezone.now().date()
        user_has_booked_homestay = Booking.objects.filter(
            homestay=homestay,
            user=request.user,
            check_out_date__lt=today
        ).exists()

        booked_dates = Booking.objects.filter(homestay=homestay).values_list('check_in_date', 'check_out_date')

        reviews = Review.objects.filter(homestay=homestay).order_by('-created_at')
        print("Homestay ID:", homestay_id)
        print("User has booked homestay:", user_has_booked_homestay)

        if request.method == 'POST':
            # Handle form submission and create Booking instance
            check_in_date = request.POST.get('check_in_date')
            check_out_date = request.POST.get('check_out_date')
            num_guests = request.POST.get('num_guests')
            payment_method = request.POST.get('paymentMethod')
            if request.user.is_authenticated:
                # Check if the user is a host
                if request.user.is_host:
                    messages.error(request, 'Hosts cannot book their own homestays.')
                else:
                    # Create a Booking instance associated with the current user
                    booking = Booking.objects.create(
                        homestay=homestay,
                        user=request.user,  # Associate the booking with the current user
                        check_in_date=check_in_date,
                        check_out_date=check_out_date,
                        num_guests=num_guests,
                        paymentMethod =payment_method
                    )
                    messages.success(request, 'Booking Confirmed.')
                    booked_dates = Booking.objects.filter(homestay=homestay).values_list('check_in_date', 'check_out_date')
            else:
                messages.error(request, 'You need to be logged in to book a homestay.')

        return render(request, 'details.html', {'homestay': homestay, 'booked_dates': booked_dates, 'reviews': reviews, 'user_has_booked_homestay': user_has_booked_homestay})
    else:
            return render(request, 'details.html', {'homestay': homestay})


def bookings(request):
    bookings = Booking.objects.filter(homestay__host=request.user)
    return render(request, 'bookings.html', {'bookings': bookings})

def add_review(request, homestay_id):
    today = timezone.now().date()
    print("Today's Date:", today)

    homestay = get_object_or_404(HomeStay, id=homestay_id)

    user_has_booked_homestay = Booking.objects.filter(
    homestay=homestay,
    user=request.user,
    check_out_date__lte=today
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


    return render(request, 'details.html', {'homestay': homestay, 'reviews': reviews, 'user_has_booked_homestay': user_has_booked_homestay})


def cosine_similarity(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    
    # Avoid division by zero
    if union == 0:
        return 0

    return intersection / union

@login_required
def recommend_homestays(request):
    # Get features liked by the user
    liked_features = Feature.objects.filter(homestay__liked_by_users=request.user).distinct()

    # Get homestays excluding those liked by the user
    homestays = HomeStay.objects.exclude(liked_by_users=request.user)

    # Prepare data for similarity calculation
    user_liked_feature_set = set(liked_features.values_list('name', flat=True))

    recommendations = []
    for homestay in homestays:
        homestay_feature_set = set(homestay.features.values_list('name', flat=True))
        similarity = cosine_similarity(user_liked_feature_set, homestay_feature_set)

        # You can adjust the threshold as needed
        if similarity > 0:
            recommendations.append({
                'homestay': homestay,
                'similarity': similarity,
                'similar_features': homestay_feature_set.intersection(user_liked_feature_set),
            })

    # Sort recommendations by similarity in descending order
    recommendations = sorted(recommendations, key=lambda x: x['similarity'], reverse=True)

    # Limit the number of recommendations
    top_n = 5
    recommendations = recommendations[:top_n]

    # Print recommendations in the console
    for recommendation in recommendations:
        print(f"Recommended Homestay: {recommendation['homestay'].name}")
        print(f"Similarity: {recommendation['similarity']}")
        print("-" * 20)

    context = {
        'user': request.user,
        'liked_features': liked_features,
        'recommendations': recommendations,
    }

    return render(request, 'recommendations.html', context)


def cosine_similarity1(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union != 0 else 0

def search_homestays(request):
    # Process user input
    location = request.GET.get('location')
    num_guests = int(request.GET.get('guests', 0))  # Convert to int or handle appropriately
    user_features = Feature.objects.filter(name__in=request.GET.getlist('features'))

    # Filter homestays based on location and number of guests
    homestays = HomeStay.objects.filter(location=location, num_guests__gte=num_guests)

    # Calculate similarity and add a similarity score to each homestay
    for homestay in homestays:
        homestay_features = homestay.features.all()
        similarity_score = cosine_similarity1(user_features, homestay_features)
        homestay.similarity_score = similarity_score

        print(f"Similarity Score for {homestay.name}: {similarity_score}")

    # Sort homestays by similarity score
    homestays = sorted(homestays, key=lambda x: x.similarity_score, reverse=True)

    # Pass the homestays to the template
    return render(request, 'results.html', {'recommended_homestays': homestays})


def details(request):
    if request.method == 'POST':
        username = request.POST.get('fullInput')
        email = request.POST.get('email')
        phone_number = request.POST.get('number')
        payment_method = request.POST.get('paymentMethod')

        payment_instance = PAYMENT_REQUIRED.objects.create(
            GuestFullName=username,
            Email=email,
            PhoneNumber=phone_number,
            paymentMethod=payment_method,
        )

        return redirect('details')

    else:
        return render(request, 'details.html')
@csrf_exempt
def verifypayment(request):
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
  "Authorization": "Key test_secret_key_b3552578ccbb4e02b7c3f1877bfedd4f"
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
    

