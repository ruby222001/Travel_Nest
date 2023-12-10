from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth
from .models import Homestay
from django.db import models
from django.db.models import Q


# Create your views here.


@login_required(login_url='home')  # Redirect to 'home' if not logged in
def host(request):
    if request.user.is_host:
        return render(request, 'host.html')
    else:
        # Redirect to 'home' if the user is not a host
        return redirect('home')
    


@login_required(login_url='home')
def save_homestay_info(request):
    if request.method == 'POST':
        homestay_name = request.POST.get('homestay_name')
        address = request.POST.get('address')
        location = request.POST.get('location')
        thumbnail_picture = request.FILES.get('thumbnail_picture')
        citizenship_photo = request.FILES.get('citizenship_photo')
        email = request.POST.get('email')
        mobile_number = request.POST.get('mobile_number')
        ownership_document_photo = request.FILES.get('ownership_document_photo')
        features = request.POST.get('features')

        if not (homestay_name and address and location and thumbnail_picture and citizenship_photo and email and mobile_number and ownership_document_photo):
            messages.error(request, 'Please fill in all required fields.')
            return redirect('home')

        homestay = Homestay.objects.create(
            homestay_name=homestay_name,
            address=address,
            location=location,
            thumbnail_picture=thumbnail_picture,
            citizenship_photo=citizenship_photo,
            email=email,
            mobile_number=mobile_number,
            ownership_document_photo=ownership_document_photo,
            features=features,  # Save features as a newline-separated string
            status='approved'
        )

        messages.success(request, 'Homestay information submitted successfully. It will be reviewed by the admin.')
        return redirect('home')
    else:
        return render(request, 'host.html')
    

def list_homestays(request):
    # Display all homestays with status 'approved'
    homestays = Homestay.objects.filter(status='approved')
    return render(request, 'list.html', {'homestays': homestays})

@login_required
def view_profile(request):
    user = request.user
    return render(request, 'profile.html')

@login_required
def edit_profile(request):
    # Implement logic to edit user profile details
    return render(request, 'edit_profile.html')

@login_required
def notifications(request):
    # Implement logic to fetch and display user notifications
    return render(request, 'notifications.html')

@login_required
def liked_items(request):
    # Implement logic to fetch and display user liked items
    return render(request, 'liked_items.html')

@login_required
def history(request):
    # Implement logic to fetch and display user history
    return render(request, 'history.html')

def homestay_detail(request, pk):
    homestay = get_object_or_404(Homestay, pk=pk)

    return render(request, 'details.html', {'homestay': homestay})

@login_required
def like_homestay(request, homestay_id):
    homestay = get_object_or_404(Homestay, id=homestay_id)
    if request.user in homestay.likes.all():
        # User has already liked, unlike it
        homestay.likes.remove(request.user)
    else:
        # User hasn't liked, add a like
        homestay.likes.add(request.user)
    return render(request, 'list.html', {'homestays': Homestay.objects.all()})


@login_required
def content_based_recommendation(request):
    # Get the homestays liked by the user
    liked_homestays = request.user.liked_homestays.all()

    # Extract features from liked homestays
    liked_features = set()
    for homestay in liked_homestays:
        features = homestay.features.lower().split()
        liked_features.update(features)

    # Get all homestays excluding the liked ones
    all_homestays = Homestay.objects.exclude(id__in=[homestay.id for homestay in liked_homestays])

    # Recommend homestays based on content-based filtering
    recommended_homestays = []
    for homestay in all_homestays:
        features = homestay.features.lower().split()
        common_features = set(features) & liked_features
        similarity = len(common_features) / len(liked_features)  # Jaccard similarity

        if similarity > 0.0:
            recommended_homestays.append((homestay, similarity))

    # Sort recommendations by similarity in descending order
    recommended_homestays.sort(key=lambda x: x[1], reverse=True)
    recommended_homestays = [(homestay, similarity) for homestay, similarity in recommended_homestays]

    print("Liked Features:", liked_features)
    print("Recommended Homestays:", recommended_homestays)
    
    for homestay, similarity in recommended_homestays:
        print(f"- {homestay.homestay_name}, Similarity: {similarity}")

    return render(request, 'recommendations.html', {'recommended_homestays': recommended_homestays})

@login_required
def recommend_homestays(request):
    # Get the homestays liked by the user
    liked_homestays = request.user.liked_homestays.all()

    # Extract features from liked homestays
    liked_features = set()
    for homestay in liked_homestays:
        features = homestay.features.lower().split()
        liked_features.update(features)

    # Get user input
    location = request.POST.get('location', '')
    time = request.POST.get('time', '')
    user_input = {
        'location': location,
        'time': time,
        'features': set(request.POST.get('features', '').lower().split())
    }
    print("Request POST data:", request.POST)

    # Get all homestays including liked ones
    all_homestays = Homestay.objects.all()

    # Recommend homestays based on content-based filtering for features
    recommended_homestays = []

    for homestay in all_homestays:
        features = homestay.features.lower().split()

        # Assign priorities based on matching criteria
        if (
            homestay.location.lower() == user_input['location'].lower()
            and set(features) & liked_features
            and set(features) & user_input['features']
        ):
            priority = 1  # Highest priority: Homestays matching location, input features, and features of liked homestays
        elif (
            homestay.location.lower() == user_input['location'].lower()
            and set(features) & user_input['features']
        ):
            priority = 2  # Second priority: Homestays matching location and input features
        elif (
            homestay.location.lower() == user_input['location'].lower()
            and set(features) & liked_features
        ):
            priority = 3  # Third priority: Homestays matching location and features of liked homestays
        elif homestay.location.lower() == user_input['location'].lower():
            priority = 4  # Last priority: Homestays matching location only
        else:
            continue  # Exclude other homestays

        recommended_homestays.append((homestay, priority))

    # Sort recommendations by priority in ascending order
    recommended_homestays.sort(key=lambda x: x[1])

    print("Liked Features:", liked_features)
    print("User Input:", user_input)
    print("Recommended Homestays:", recommended_homestays)

    for homestay, _ in recommended_homestays:
        print(f"- {homestay.homestay_name}")

    return render(request, 'recommend.html', {'recommended_homestays': recommended_homestays})





def search_homestays(request):
    query = request.GET.get('query', '')
    homestays = Homestay.objects.filter(
        models.Q(homestay_name__icontains=query) |
        models.Q(location__icontains=query) |
        models.Q(features__icontains=query)
    )

    return render(request, 'results.html', {'homestays': homestays, 'query': query})

def booking(request,id):
    step = 1
    list_homestays = Homestay.objects.get(id=id)
    
    return render(request,'booking.html',  {'step': step},{'list_homestays':list_homestays})

