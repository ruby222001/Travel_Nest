from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, logout
from .models import User
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from booking.models import Booking
from django.utils import timezone
import math

# Create your views here.

def host_signup(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        mobile = request.POST['mobile']
        address = request.POST['address']
        
        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken. Please choose a different username.')
            return redirect('home')
        
        # If username is unique, proceed with user creation
        user = User.objects.create(username=username, is_host=True, first_name=first_name,
            last_name=last_name,
            image=image,
            email=email,
            mobile=mobile,
            address=address)
        user.set_password(password)
        user.save()
        
        # login(request, user)
        return redirect('home')  # Redirect to home page after signup
    
    return render(request, 'home.html')

def guest_signup(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        mobile = request.POST['mobile']
        address = request.POST['address']
        
        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken. Please choose a different username.')
            return redirect('home')
        
        # If username is unique, proceed with user creation
        user = User.objects.create(username=username, is_guest=True,first_name=first_name,
            last_name=last_name,
            image=image,
            email=email,
            mobile=mobile,
            address=address)
        user.set_password(password)
        user.save()
        return redirect('home')  # Redirect to home page after signup
    
    return render(request, 'home.html')

def host_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username, is_host=True)
            if user.check_password(password):
                login(request, user)
                return redirect('home')  # Redirect to home page after login
            else:
                messages.error(request, 'Invalid password for the host account.')
                return redirect('home')
        except User.DoesNotExist:
            messages.error(request, 'Host account does not exist.')
    
    return render(request, 'home.html')

def guest_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username, is_guest=True)
            if user.check_password(password):
                login(request, user)
                return redirect('home')  
            else:
                messages.error(request, 'Invalid password for the guest account.')
                return redirect('home')
        except User.DoesNotExist:
            messages.error(request, 'Guest account does not exist.')
    
    return render(request, 'home.html')

def user_logout(request):
    auth.logout(request)
    return redirect('home') 

def home(request):
    return render(request, 'home.html')


@login_required
def host_profile(request):
    return render(request, 'host_profile.html')

@login_required
def guest_profile(request):
    liked_homestays = request.user.liked_homestays.all()
    past_bookings = Booking.objects.filter(user=request.user, check_out_date__lt=timezone.now().date())
    upcoming_bookings = Booking.objects.filter(user=request.user, check_in_date__gte=timezone.now().date())


    context = {
        'user': request.user,
        'liked_homestays': liked_homestays,
        'past_bookings': past_bookings,
        'upcoming_bookings': upcoming_bookings,
    }
    return render(request, 'guest_profile.html', context)

@login_required
def edit_host_profile(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        request.user.image = image if image else request.user.image
        request.user.first_name = request.POST['first_name']
        request.user.last_name = request.POST['last_name']
        request.user.email = request.POST['email']
        request.user.mobile = request.POST['mobile']
        request.user.address = request.POST['address']
        request.user.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('host_profile')

    return render(request, 'host_profile.html')

@login_required
def change_host_password(request):
    if request.method == 'POST':
        old_password = request.POST['old_password']
        new_password1 = request.POST['new_password1']
        new_password2 = request.POST['new_password2']

        if not request.user.check_password(old_password):
            messages.error(request, 'Incorrect old password.')
            return redirect('host_profile')

        if new_password1 != new_password2:
            messages.error(request, 'New passwords do not match.')
            return redirect('host_profile')

        request.user.set_password(new_password1)
        request.user.save()
        update_session_auth_hash(request, request.user)  # To update the session with the new password
        messages.success(request, 'Password changed successfully.')
        return redirect('host_profile')

    return render(request, 'host_profile.html')

@login_required
def edit_guest_profile(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        request.user.image = image if image else request.user.image
        request.user.first_name = request.POST['first_name']
        request.user.last_name = request.POST['last_name']
        request.user.email = request.POST['email']
        request.user.mobile = request.POST['mobile']
        request.user.address = request.POST['address']
        request.user.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('guest_profile')

    return render(request, 'guest_profile.html')

@login_required
def change_guest_password(request):
    if request.method == 'POST':
        old_password = request.POST['old_password']
        new_password1 = request.POST['new_password1']
        new_password2 = request.POST['new_password2']

        if not request.user.check_password(old_password):
            messages.error(request, 'Incorrect old password.')
            return redirect('guest_profile')

        if new_password1 != new_password2:
            messages.error(request, 'New passwords do not match.')
            return redirect('guest_profile')

        request.user.set_password(new_password1)
        request.user.save()
        update_session_auth_hash(request, request.user)  # To update the session with the new password
        messages.success(request, 'Password changed successfully.')
        return redirect('guest_profile')

    return render(request, 'guest_profile.html')
