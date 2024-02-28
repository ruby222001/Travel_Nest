from django.shortcuts import render, HttpResponse

# Create your views here.


def host(request):
    return render(request, 'host.html')
