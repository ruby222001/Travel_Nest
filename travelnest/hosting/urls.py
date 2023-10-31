from django.urls import path
from hosting import views

urlpatterns = [
    path('host', views.host, name="host"),
    path('add_homestay/', views.add_homestay, name='add_homestay'),
    path('list_homestays/', views.list_homestays, name='list_homestays'),
]