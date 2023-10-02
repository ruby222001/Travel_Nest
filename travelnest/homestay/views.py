from django.shortcuts import render,HttpResponse

# Create your views here.
def home(request):
    return render(request,"home.html")
def booking(request):
    return render(request,"booking.html")

def submit_user_details(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        
        # Process the user data or save it to the database as needed
        # You can add validation and data handling logic here

        # Render the same template with user details
        return render(request, 'booking_details.html', {'name': name, 'email': email})
def user_details(request):
    # Get user data from the session or database
    user_data = {
        'name': request.POST.get('name'),  # You may need to modify this to get user data from where you store it
        'email': request.POST.get('email'),
    }
    return render(request, 'user_details.html', user_data)