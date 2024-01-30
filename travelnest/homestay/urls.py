from django.urls import path

from hosting.views import confirmation
from .import views 

urlpatterns = [
path('booking/<int:id>/', views.booking, name='booking'),
 path('payment/',views.payment,name='payment'),
 path('verify_payment/',views.verify_payment,name='verify_payment'),
path('confirmation/<int:homestay_id>/', views.confirmation, name='confirmation')
    ]
