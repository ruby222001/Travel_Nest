from django.urls import path
from . import views

urlpatterns = [
    path('list_of_homestay/', views.list, name='list'),
]