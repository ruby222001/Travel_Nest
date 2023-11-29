from django.urls import path
from .views import map, add_location

urlpatterns = [
    path('', map, name='map'),
    path('add/', add_location, name='add_location'),
]
