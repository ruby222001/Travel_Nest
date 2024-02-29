from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .models import HomeStay, Feature, HomeStayImage

# Create your views here.


def list(request):
    homestays = HomeStay.objects.filter(status='approved')
    return render(request,'list.html',{'homestays':homestays})