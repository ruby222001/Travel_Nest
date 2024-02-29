from django.contrib import admin
from .models import Feature, HomeStay, HomeStayImage, Category

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(Category, CategoryAdmin)

class FeatureAdmin(admin.ModelAdmin):
    list_display = ('name','category')


@admin.register(HomeStay)
class HomeStayAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'num_guests', 'price_per_night', 'host', 'status')
    search_fields = ('name', 'host__username')
    list_filter = ('status',)


# Register the admin classes
admin.site.register(Feature, FeatureAdmin)