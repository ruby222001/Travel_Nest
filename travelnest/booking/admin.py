from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('homestay' , 'user','check_in_date', 'check_out_date', 'num_guests', 'paymentMethod')
    search_fields = ('homestay__name', 'homestay__host__username', 'paymentMethod', 'user__username')
    list_filter = ('homestay__status', 'paymentMethod')
