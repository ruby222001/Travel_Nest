
from django.urls import path
from .import views

urlpatterns = [
    path("", views.home,name="home"),
    path("booking/",views.booking,),
 path('user_details/', views.user_details, name='user_details'),
 path('payment/',views.payment,name='payment'),
]
