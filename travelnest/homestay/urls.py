from django.urls import path
from . import views

urlpatterns = [
    path('list_of_homestay/', views.list, name='list'),
    path('homestay_detail/<int:homestay_id>/', views.detail, name='detail'),
    path('like_homestay/<int:homestay_id>/', views.like_homestay, name='like_homestay'),
]