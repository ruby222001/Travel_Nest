# map_app/views.py

from django.shortcuts import render, redirect
from .forms import LocationForm
from .models import Location

def map(request):
    locations = Location.objects.all()
    return render(request, 'map.html', {'locations': locations})

def add_location(request):
    new_location = None  # Initialize new_location variable
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            new_location = form.save()
            # Now, update the map with the new location
            return render(request, 'map.html', {'locations': Location.objects.all(), 'new_location': new_location})
    else:
        form = LocationForm()
    return render(request, 'add_location.html', {'form': form})
