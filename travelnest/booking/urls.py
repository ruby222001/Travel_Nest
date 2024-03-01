from django.urls import path
from . import views


urlpatterns = [
    path('book_homestay/<int:homestay_id>/', views.book_homestay, name='book_homestay'),
    path('homestay/<int:homestay_id>/add_review/', views.add_review, name='add_review'),
    path('initiate',views.initkhalti,name="initiate"),
    path('verify_payment/', views.verify_payment, name='verify_payment'),

    ]