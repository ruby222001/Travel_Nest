from django.contrib import admin
from .models import Homestay

# Register your models here.
@admin.register(Homestay)
class HomestayAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'location','features')
    search_fields = ('name', 'location')