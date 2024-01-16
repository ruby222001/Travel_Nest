from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('host-dashboard/', views.host_dashboard, name='host_dashboard'),
    path('add/', views.add, name='add'),
    path('approved/', views.approved, name='approved'),
    path('pending/', views.pending, name='pending'),
    path('unapproved/', views.unapproved, name='unapproved'),
    path('bookings/', views.bookings, name='bookings'),
    path('list/', views.list, name='list'),
    path('like_homestay/<int:homestay_id>/', views.like_homestay, name='like_homestay'),
    path('homestay/<int:homestay_id>/', views.homestay_details, name='homestay_details'),
    path('bookings/', views.bookings, name='bookings'),
    path('add_review/<int:homestay_id>/', views.add_review, name='add_review'),
    path('recommendations/', views.recommend_homestays, name='recommend_homestays'),
    path('search/', views.search_homestays, name='search_homestays'),
     path('details/',views.details,name='details'),
    path('verifypayment/',views.verifypayment,name='verifypayment'),
    path('about/',views.about,name='about'),

]
