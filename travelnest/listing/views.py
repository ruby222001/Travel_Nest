from django.shortcuts import render

from hosting.models import Homestay
# Create your views here.
def show_homestay(request):
    list_homestays = Homestay.objects.get(id=id)

    return render(request,'properties.html', {'list_homestays':list_homestays})

def show_singleproperty(request):
    return render(request,'singleproperty.html')