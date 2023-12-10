from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'is_host', 'is_guest', 'image']
    list_filter = ['is_host', 'is_guest']

admin.site.register(User, CustomUserAdmin)
