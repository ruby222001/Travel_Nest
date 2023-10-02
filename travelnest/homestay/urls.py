
from django.urls import path
from .import views

urlpatterns = [
    path("", views.home,name="home"),
    path("booking/",views.booking,),
    path('submit_user_details/', views.submit_user_details, name='submit_user_details'),
 path('user_details/', views.user_details, name='user_details'),
]
