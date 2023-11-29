from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Userdetails,Payment



# Register your models here.
class UserdetailAdmin(admin.ModelAdmin):
    list_display =('GuestFullName',"Email","PhoneNumber","AdditionalInformation")
admin.site.register(Userdetails,UserdetailAdmin)

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('GuestFullName', 'Email', 'PhoneNumber', 'Amount')
admin.site.register(Payment, PaymentAdmin)

