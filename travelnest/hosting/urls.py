from django.urls import path
from . import views

urlpatterns = [
    path('become-a-host/', views.host, name='host')
]