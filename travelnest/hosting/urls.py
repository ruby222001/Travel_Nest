from django.urls import path
from hosting import views
from . import views

urlpatterns = [
    path('host', views.host, name="host"),
    path('add_homestay/', views.add_homestay, name='add_homestay'),
    path('list_homestays/', views.list_homestays, name='list_homestays'),
    path('show',views.show_homestay),
    path('showsingle/<id>',views.show_singleproperty, name='showsingle'),
    path('booking/<int:id>/', views.booking, name='booking'),
path('confirmation/<int:homestay_id>/', views.confirmation, name='confirmation')

]