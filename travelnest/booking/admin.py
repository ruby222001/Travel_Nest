from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('homestay', 'user', 'check_in_date', 'check_out_date', 'num_guests', 'get_price_per_night', 'total_price_per_night', 'paymentMethod')
    search_fields = ('homestay__name', 'homestay__host__username', 'paymentMethod', 'user__username')
    list_filter = ('homestay__status', 'paymentMethod')

    def get_price_per_night(self, obj):
        return obj.homestay.price_per_night
    get_price_per_night.short_description = 'Price per Night'
    get_price_per_night.admin_order_field = 'homestay__price_per_night'
