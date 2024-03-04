from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, logout
from .models import User
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import random
import string
from django.utils import timezone
from datetime import timedelta
from django.core.serializers.json import DjangoJSONEncoder
import os
from booking.models import Booking


# Create your views here.

def generate_pin():
    return ''.join(random.choices(string.digits, k=6))


def signup_host(request):
    return render(request, 'host_signup.html')


def signup_guest(request):
    return render(request, 'guest_signup.html')


def login_host(request):
    return render(request, 'host_login.html')


def login_guest(request):
    return render(request, 'guest_login.html')


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
            return redirect('signup_host')
        
        # Check if the email is already registered
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered. Please use a different email address.')
            return redirect('signup_host')
        
        request.session['signup_username'] = username
        request.session['signup_password'] = password
        request.session['signup_first_name'] = first_name
        request.session['signup_last_name'] = last_name
        request.session['signup_email'] = email
        request.session['signup_mobile'] = mobile
        request.session['signup_address'] = address

        
        # Generate and send PIN via email
        pin = generate_pin()
        request.session['signup_pin'] = pin
        request.session['pin_expiry'] = (timezone.now() + timedelta(minutes=5)).isoformat()  # Set expiry time to 5 minutes from now
        send_mail(
            'Registration Verification PIN',
            f'Your registration PIN is: {pin}',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )

        return render(request, 'verify_pin.html')
        
        # # If username is unique, proceed with user creation
        # user = User.objects.create(username=username, is_host=True, first_name=first_name,
        #     last_name=last_name,
        #     image=image,
        #     email=email,
        #     mobile=mobile,
        #     address=address)
        # user.set_password(password)
        # user.save()

        # success_condition = True
        # if success_condition:
        #     messages.success(request, 'You have registered successfully as a host.', extra_tags='confirm')
        # else:
        #     messages.error(request, 'An error occurred while registering. Please try again.')

        # return redirect('home')

            
    return redirect('home')

def verify_pin(request):
    if request.method == 'POST':
        entered_pin = request.POST.get('pin')
        pin_expiry_str = request.session.get('pin_expiry')
        pin_expiry = timezone.datetime.fromisoformat(pin_expiry_str) if pin_expiry_str else None
        if pin_expiry and timezone.now() <= pin_expiry:
            saved_pin = request.session.get('signup_pin')
            if entered_pin == saved_pin:
                # PIN is correct and within time limit, proceed with registration
                username = request.session.get('signup_username')
                password = request.session.get('signup_password')
                first_name = request.session.get('signup_first_name')
                last_name = request.session.get('signup_last_name')
                email = request.session.get('signup_email')
                mobile = request.session.get('signup_mobile')
                address = request.session.get('signup_address')
                image = request.session.get('signup_image')

                # Create user
                user = User.objects.create(
                    username=username,
                    is_guest=True,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    mobile=mobile,
                    address=address,
                    image=image
                )
                user.set_password(password)
                user.save()

                # Clear session data
                del request.session['signup_pin']
                del request.session['pin_expiry']
                del request.session['signup_username']
                del request.session['signup_password']
                del request.session['signup_first_name']
                del request.session['signup_last_name']
                del request.session['signup_email']
                del request.session['signup_mobile']
                del request.session['signup_address']

                messages.success(request, 'You have registered successfully as a guest.')
                return redirect('home')
            else:
                messages.error(request,'Incorrect PIN. Please try again.')
                return render(request, 'verify_pin.html')
        else:
            messages.error(request,'PIN has expired. Please register again.')
        return redirect('signup_host')

    return redirect('home')


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
            return redirect('signup_guest')
        
        # Check if the email is already registered
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered. Please use a different email address.')
            return redirect('signup_guest')
        
        request.session['signup_username'] = username
        request.session['signup_password'] = password
        request.session['signup_first_name'] = first_name
        request.session['signup_last_name'] = last_name
        request.session['signup_email'] = email
        request.session['signup_mobile'] = mobile
        request.session['signup_address'] = address

        
        # Generate and send PIN via email
        pin = generate_pin()
        request.session['signup_pin'] = pin
        request.session['pin_expiry'] = (timezone.now() + timedelta(minutes=5)).isoformat()  # Set expiry time to 5 minutes from now
        send_mail(
            'Registration Verification PIN',
            f'Your registration PIN is: {pin}',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )

        return render(request, 'verify1_pin.html')

        # # If username is unique, proceed with user creation
        # user = User.objects.create(username=username, is_guest=True,first_name=first_name,
        #     last_name=last_name,
        #     image=image,
        #     email=email,
        #     mobile=mobile,
        #     address=address)
        # user.set_password(password)
        # user.save()

        # success_condition = True
        # if success_condition:
        #     messages.success(request, 'You have registered successfully.', extra_tags='confirm')
        # else:
        #     messages.error(request, 'An error occurred while registering. Please try again.')

        # return redirect('home')

            
    return redirect('home')

def verify1_pin(request):
    if request.method == 'POST':
        entered_pin = request.POST.get('pin')
        pin_expiry_str = request.session.get('pin_expiry')
        pin_expiry = timezone.datetime.fromisoformat(pin_expiry_str) if pin_expiry_str else None
        if pin_expiry and timezone.now() <= pin_expiry:
            saved_pin = request.session.get('signup_pin')
            if entered_pin == saved_pin:
                # PIN is correct and within time limit, proceed with registration
                username = request.session.get('signup_username')
                password = request.session.get('signup_password')
                first_name = request.session.get('signup_first_name')
                last_name = request.session.get('signup_last_name')
                email = request.session.get('signup_email')
                mobile = request.session.get('signup_mobile')
                address = request.session.get('signup_address')
                image = request.session.get('signup_image')

                # Create user
                user = User.objects.create(
                    username=username,
                    is_guest=True,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    mobile=mobile,
                    address=address,
                    image=image
                )
                user.set_password(password)
                user.save()

                # Clear session data
                del request.session['signup_pin']
                del request.session['pin_expiry']
                del request.session['signup_username']
                del request.session['signup_password']
                del request.session['signup_first_name']
                del request.session['signup_last_name']
                del request.session['signup_email']
                del request.session['signup_mobile']
                del request.session['signup_address']

                messages.success(request,'You have registered successfully as a guest.')
                return redirect('home')
            else:
                messages.error(request, 'Incorrect PIN. Please try again.')
                return render(request, 'verify1_pin.html')
        else:
            messages.error(request,'PIN has expired. Please register again.')
        return render(request, 'signup_guest')

    return redirect('home')


def host_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username, is_host=True)
            if user.check_password(password):
                login(request, user)
                messages.success(request, 'Login Successful.')
                return redirect('home')
            else:
                messages.error(request, 'Invalid password for the host account.')
                return redirect('home')
        except User.DoesNotExist:
            messages.error(request, 'Host account does not exist.')
    
    return redirect('home')


def guest_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username, is_guest=True)
            if user.check_password(password):
                messages.success(request, 'Login Successful.')
                login(request, user)
                return redirect('home')  
            else:
                messages.error(request, 'Invalid password.')
                return redirect('home')
        except User.DoesNotExist:
            messages.error(request, 'Account does not exist.')
    
    return redirect('home')


def user_logout(request):
    auth.logout(request)
    return redirect('home') 


@login_required
def host_profile(request):
    return render(request, 'host_profile.html')


@login_required
def guest_profile(request):
    # Retrieve liked homestays, past bookings, and upcoming bookings
    liked_homestays = request.user.liked_homestays.all()
    past_bookings = Booking.objects.filter(user=request.user, check_out_date__lt=timezone.now().date())
    upcoming_bookings = Booking.objects.filter(user=request.user, check_in_date__gt=timezone.now().date())

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
        update_session_auth_hash(request, request.user) 
        messages.success(request, 'Password changed successfully.')
        return redirect('guest_profile')

    return render(request, 'guest_profile.html')