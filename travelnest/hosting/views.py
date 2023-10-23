from django.shortcuts import render, HttpResponse, redirect
from .models import Homestay

# Create your views here.


def host(request):
    return render(request, 'host.html')


def list_homestays(request):
    homestays = Homestay.objects.all()
    return render(request, 'list.html', {'homestays': homestays})


def add_homestay(request):
    if request.method == "POST":
        name = request.POST.get("name")
        photo = request.FILES.get("photo")
        price = request.POST.get("price")
        location = request.POST.get("location")
        features = request.POST.get("features")

        Homestay.objects.create(name=name, photo=photo, price=price, location=location, features=features)

        return redirect("list_homestays") 

    return render(request, "host.html")