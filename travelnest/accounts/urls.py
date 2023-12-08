from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_home, name='home'),
    path('list/', views.list, name='list'),
    path('a/', views.a, name='a'),
    path('details/', views.details, name='details'),
]