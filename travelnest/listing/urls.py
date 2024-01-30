from django.urls import path
from . import views

urlpatterns = [
    path('show/<id>',views.show_homestay),
    
]