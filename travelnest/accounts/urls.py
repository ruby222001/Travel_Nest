from django.urls import path
from . import views

urlpatterns = [
    path('host/signup/', views.host_signup, name='host_signup'),
    path('guest/signup/', views.guest_signup, name='guest_signup'),
    path('host/login/', views.host_login, name='host_login'),
    path('guest/login/', views.guest_login, name='guest_login'),
    path('logout/', views.user_logout, name='logout'),
    path('host/profile/', views.host_profile, name='host_profile'),
    path('host/edit-profile/', views.edit_host_profile, name='edit_host_profile'),
    path('host/change-password/', views.change_host_password, name='change_host_password'),
    path('guest/profile/', views.guest_profile, name='guest_profile'),
    path('guest/edit-profile/', views.edit_guest_profile, name='edit_guest_profile'),
    path('guest/change-password/', views.change_guest_password, name='change_guest_password'),
    path('host-signup/', views.signup_host, name='signup_host'),
    path('guest-signup/', views.signup_guest, name='signup_guest'),
    path('host-login/', views.login_host, name='login_host'),
    path('guest-login/', views.login_guest, name='login_guest'),
]