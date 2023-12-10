from django.urls import path
from . import views

urlpatterns = [
    # ... (your existing patterns)
    path('host/', views.host, name='host'),
    path('save_homestay_info/', views.save_homestay_info, name='save_homestay_info'),
    path('list_homestays/', views.list_homestays, name='list_homestays'),
    path('profile/', views.view_profile, name='view_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/notifications/', views.notifications, name='notifications'),
    path('profile/liked_items/', views.liked_items, name='liked_items'),
    path('profile/history/', views.history, name='history'),
    path('homestay_detail/<int:pk>/', views.homestay_detail, name='homestay_detail'),
    path('homestay/<int:homestay_id>/like/', views.like_homestay, name='like_homestay'),
    path('content_based_recommendation/', views.content_based_recommendation, name='content_based_recommendation'),
    path('recommend_homestays/', views.recommend_homestays, name='recommend_homestays'),
    path('search/', views.search_homestays, name='search_homestays'),
    path('booking/<int:id>', views.booking, name='booking'),
]
