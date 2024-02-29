from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from accounts.models import User
from django.db.models import Q
from homestay.models import HomeStay


# Create your views here.


def custom_admin_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        # Check if email and password match static credentials
        if email == 'travelnest18@gmail.com' and password == 'travelnest':
            # Redirect to the admin panel if credentials are correct
            return redirect(admin_home)
        else:
            # Display login form again with error message
            messages.error(request, 'Invalid email or password')
            return redirect('login')
    else:
        # Display login form
        return redirect(login)
    

def login(request):
    return render(request ,'admin_login.html')


def admin_home(request):
    return render(request, 'admin_home.html')


def all_users(request):
    # Retrieve all users
    users = User.objects.all()
    return render(request, 'users.html', {'users': users})


def homestay_requests(request):
    pending_homestays = HomeStay.objects.filter(status='pending')
    return render(request, 'homestay_requests.html', {'pending_homestays': pending_homestays})

def homestay_details_request(request, homestay_id):
    homestay = HomeStay.objects.get(id=homestay_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        homestay.status = status
        homestay.save()
        messages.success(request, 'Homestay status changed successfully.')
        return redirect('homestay_requests')
    return render(request, 'admin_homestay_details.html', {'homestay': homestay})


def approved_homestays(request):
    # Retrieve all approved homestays
    approved_homestays = HomeStay.objects.filter(status='approved')
    return render(request, 'admin_homestay.html', {'approved_homestays': approved_homestays})