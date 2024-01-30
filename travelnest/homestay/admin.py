from django.contrib import admin
from .models import Payment
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('GuestFullName', 'Email', 'PhoneNumber', 'paymentmethod')
    list_filter = ('paymentmethod',)

