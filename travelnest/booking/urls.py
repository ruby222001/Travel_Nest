from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('details/',views.details,name='details'),
    path('verify_payment/',views.verify_payment,name='verify_payment'),
    
]
