from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Userdetails


# Register your models here.
class UserdetailsAdmin(admin.ModelAdmin):
    list_display =('GuestFullName',"Email","PhoneNumber","AdditionalInformation")
admin.site.register(Userdetails)
