from django.urls import path
from . import views

urlpatterns = [
    path('list_of_homestay/', views.list, name='list'),
    path('homestay_detail/<int:homestay_id>/', views.detail, name='detail'),
    path('like_homestay/<int:homestay_id>/', views.like_homestay, name='like_homestay'),
    path('verifyy_payment',views.verifyy_payment,name='verifyy_payment'),
    path('search/', views.search, name='search'),
    path('search_input/', views.search_input, name='search_input'),
]