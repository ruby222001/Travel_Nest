from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from accounts.models import User
from django.db.models import Q


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


def filter_and_search_users(request):
    user_type = request.GET.get('user_type')
    search_query = request.GET.get('search_query')
    users = User.objects.all()

    # Filter users by user type if specified
    if user_type in ['guest', 'host']:
        users = users.filter(is_guest=(user_type == 'guest'), is_host=(user_type == 'host'))

    # Perform search if search query is provided
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(mobile__icontains=search_query) |
            Q(address__icontains=search_query)
        )

    return render(request, 'users.html', {'users': users})