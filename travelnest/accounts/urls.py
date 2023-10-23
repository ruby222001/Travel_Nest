from django.urls import path
from accounts import views

urlpatterns = [
    path('login',views.login, name='login'),
    path('user_register', views.user_register, name='user_register'),
    path('host_register', views.host_register, name='host_register'),
    path('logout', views.logout, name='logout'),
]