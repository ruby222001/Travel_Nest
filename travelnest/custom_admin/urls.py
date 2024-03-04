from django.urls import path
from . import views

urlpatterns = [
    path('', views.custom_admin_login, name='custom_admin_login'),
    path('login/', views.login, name='login'),
    path('home/', views.admin_home, name="admin_home"),
    path('users/', views.all_users, name='all_users'),
    path('homestay-requests/', views.homestay_requests, name='homestay_requests'),
    path('homestay/<int:homestay_id>/', views.homestay_details_request, name='homestay_details'),
    path('approved_homestays/', views.approved_homestays, name='approved_homestays'),
    path('users/', views.filter_and_search_users, name='filter_and_search_users'),
]