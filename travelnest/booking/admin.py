from django.contrib import admin
from .models import Booking

# Register your models here.


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('homestay', 'check_in_date', 'check_out_date', 'num_guests', 'amount', 'payment_type')
    search_fields = ('homestay__name', 'homestay__host__username')
    list_filter = ('homestay__status',)