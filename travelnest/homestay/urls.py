from django.urls import path
from .import views 

urlpatterns = [
path('booking/', views.booking, name='booking'),
 path('user_details/', views.user_details, name='user_details'),
 path('payment/',views.payment,name='payment'),
 path('verify_payment/',views.verify_payment,name='verify_payment'),
   
    ]
