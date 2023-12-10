from django.urls import path
from . import views

urlpatterns = [
    path('host/signup/', views.host_signup, name='host_signup'),
    path('guest/signup/', views.guest_signup, name='guest_signup'),
    path('host/login/', views.host_login, name='host_login'),
    path('guest/login/', views.guest_login, name='guest_login'),
    path('logout/', views.user_logout, name='logout'),
    path('', views.home, name='home'),
]
