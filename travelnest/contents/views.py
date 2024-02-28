from django.shortcuts import render, HttpResponse

# Create your views here.


def show_home(request):
    return render(request, 'index.html')