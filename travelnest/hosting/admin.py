from django.contrib import admin
from .models import Homestay

# Register your models here.
@admin.register(Homestay)
class HomestayAdmin(admin.ModelAdmin):
    list_display = ('homestay_name', 'address', 'location', 'status')
    list_filter = ('status',)