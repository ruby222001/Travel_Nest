from django.urls import path
from . import views

urlpatterns = [
    path('become-a-host/', views.hosting, name='hosting'),
    path('host/', views.host, name='host'),
    path('add_homestay/', views.add_homestay, name='add_homestay'),
    path('homestay_detail/<int:homestay_id>/', views.homestay_detail, name='homestay_detail'),
    path('homestay_list/', views.homestay_list, name='homestay_list'),
    path('homestay/<int:homestay_id>/bookings/', views.view_bookings, name='view_bookings'),
]