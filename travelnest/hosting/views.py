from django.shortcuts import HttpResponse, redirect, render
from django.shortcuts import render, get_object_or_404

from .models import Homestay

# Create your views here.


def host(request):
    return render(request, 'host.html')


def list_homestays(request):
    homestays = Homestay.objects.all()
    return render(request, 'properties.html', {'homestays': homestays})


def add_homestay(request):
    if request.method == "POST":
        name = request.POST.get("name")
        photo = request.FILES.get("photo")
        price = request.POST.get("price")
        location = request.POST.get("location")
        features = request.POST.get("features")

        Homestay.objects.create(name=name, photo=photo, price=price, location=location, features=features)

        return redirect("list_homestays",id=Homestay.id) 

    return render(request, "host.html")

def show_homestay(request):
    return render(request,'properties.html', {'list_homestays':list_homestays})

def show_singleproperty(request,id):
    list_homestays = Homestay.objects.get(id=id)
    return render(request,'singleproperty.html', {'list_homestays':list_homestays})

def booking(request,id):
    step = 1
    list_homestays = Homestay.objects.get(id=id) 
     
    return render(request,'booking.html',  {'step': step,'list_homestays':list_homestays,'homestay_id':id})

def confirmation(request, homestay_id):
    arrival_date = request.GET.get('arrival_date')
    departure_date = request.GET.get('departure_date')
    total_guests = request.GET.get('total_guests')

    list_homestays = get_object_or_404(Homestay, id=homestay_id)

    return render(request, 'confirmation.html', {
        'step': 2,
        'list_homestays': list_homestays,
        'arrival_date': arrival_date,
        'departure_date': departure_date,
        'total_guests': total_guests,
        'total_price': calculate_total_price(list_homestays.price),
    })


def calculate_total_price(base_price):
    # Perform any calculations for total price here
    return base_price  # For simplicity, just returning the base price
