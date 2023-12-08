from django.shortcuts import render, HttpResponse

# Create your views here.

def show_home(request):
    return render(request, 'index.html')

def list(request):
    return render(request, 'list.html')

def a(request):
    return render(request, 'a.html')

def details(request):
    return render(request, 'details.html')