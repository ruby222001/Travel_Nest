from django.shortcuts import render
#from homestay.models import Homestay
# Create your views here.
def show_homestay(request):
    return render(request,'properties.html')

def show_singleproperty(request):
    return render(request,'singleproperty.html')