from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, logout
from .models import User
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required

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
