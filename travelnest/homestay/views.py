from django.shortcuts import render,redirect
# Create your views here.
def home(request):
    return render(request,"home.html")
def booking(request):
    return render(request,"booking.html")



def user_details(request):
    if request.method == 'POST':
        # Process the form data and save it to the database
        # Redirect to a success page or do what's necessary
        return redirect('success_page')
    return render(request, 'user_details_form.html')