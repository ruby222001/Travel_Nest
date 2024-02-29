from django.shortcuts import render, HttpResponse, redirect, HttpResponse, get_object_or_404
from homestay.models import HomeStay, HomeStayImage, Feature
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from itertools import groupby

# Create your views here.


def hosting(request):
    return render(request, 'host.html')


@login_required
def host(request):
    user = request.user
    print(f"User: {user}")
    homestays = user.homestay_set.all()
    print("Number of homestays:", homestays.count())
    
    if homestays.exists():
        if homestays.count() == 1:
            homestay_id = homestays.first().id
            return redirect('homestay_detail', homestay_id)
        else:
            return redirect('homestay_list') 
    else:
        return redirect('add_homestay')
    

@login_required
def add_homestay(request):
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

        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

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
            latitude=latitude,  
            longitude=longitude,  
        )
        homestay.save()

        # Add secondary images
        for image in request.FILES.getlist('secondary_images'):
            HomeStayImage.objects.create(homestay=homestay, image=image)

        # Add features
        for feature_id in features:
            feature = Feature.objects.get(pk=feature_id)
            homestay.features.add(feature)

        # Redirect to home
        messages.success(request, 'Request submitted successfully. You will be notified later.', extra_tags='confirm')
        return redirect('home')

    else:
        features = Feature.objects.all().order_by('category', 'name')
        organized_features = {}
        for category, group in groupby(features, lambda x: x.category):
            organized_features[category] = list(group)
        return render(request, 'add.html', {'organized_features': organized_features})


@login_required
def homestay_detail(request, homestay_id):
    homestay = get_object_or_404(HomeStay, id=homestay_id)
    return render(request, 'homestay_detail.html', {'homestay': homestay})


@login_required
def homestay_list(request):
    user = request.user 
    homestays = HomeStay.objects.filter(host=user) 
    return render(request, 'homestay_list.html', {'homestays': homestays}) 