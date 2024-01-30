from django.contrib import admin
from .models import Feature, HomeStay, HomeStayImage


# Register your models here.


class FeatureAdmin(admin.ModelAdmin):
    list_display = ('name',)

class FeatureInline(admin.TabularInline):
    model = HomeStay.features.through
    extra = 0  # Set to 0 to remove "Add Another" option
    readonly_fields = ['feature']
    can_delete = False  # Remove the delete option
    show_add_another = False

class HomeStayImageInline(admin.TabularInline):
    model = HomeStayImage
    extra = 0  # Set to 0 to remove "Add Another" option
    readonly_fields = ['image']
    can_delete = False  # Remove the delete option
    show_add_another = False

@admin.register(HomeStay)
class HomeStayAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'num_guests', 'price_per_night', 'host', 'status')
    search_fields = ('name', 'host__username')
    list_filter = ('status',)
    inlines = [HomeStayImageInline, FeatureInline]
    show_add_another = False  # Remove the "Add Another" option

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.status == 'pending':
            return [f.name for f in self.model._meta.fields if f.name not in ['status']]
        else:
            return []
        
    def get_fieldsets(self, request, obj=None):
        if obj:
            # Exclude the fields you want to hide
            return [(None, {
                'fields': ['status', 'host', 'name', 'location', 'num_guests', 'price_per_night', 'ownership_documents', 'citizenship_documents', 'thumbnail_image'],
            })]
        else:
            return super().get_fieldsets(request, obj)

# Register the admin classes
admin.site.register(Feature, FeatureAdmin)