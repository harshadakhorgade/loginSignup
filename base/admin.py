from django.contrib import admin
from .models import Profile, FarmerProfile,CoordinatorProfile,Crop
from django.utils.html import format_html

class CropInline(admin.TabularInline):
    model = Crop
    extra = 1  # Allows one extra empty form for adding a new crop
    fields = ('crop_type', 'variety', 'planting_date', 'expected_harvest_date', 'field_number', 'fertilizer_usage', 'condition', 'problems', 'irrigation_type', 'season', 'photo_or_information', 'area_in_acres')
    readonly_fields = ('username',)  # Display but make it read-only
    can_delete = True

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type')
    search_fields = ('user__username', 'user_type')

class FarmerProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'username','mobile_number', 'email','village', 'district', 'state')
    search_fields = ('first_name', 'last_name', 'username','mobile_number','email','village', 'district', 'state')
    

class CoordinatorProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'username','mobile_number', 'email','village', 'district', 'state')
    search_fields = ('first_name', 'last_name', 'username','mobile_number','email','village', 'district', 'state')
    


class CropAdmin(admin.ModelAdmin):
    list_display = ('username','crop_type', 'variety', 'planting_date', 'expected_harvest_date', 'field_number','fertilizer_usage','problems','condition','irrigation_type', 'season', 'area_in_acres','photo_crop_condition','land_type', 'crop_category', 'farmer_type' ) # Fields to display in admin list view
    search_fields = ('crop_type', 'variety','condition')  # Fields searchable in admin
    list_filter = ('planting_date', 'expected_harvest_date', 'irrigation_type', 'season')

    def photo_condition_image(self, obj):
        if obj.photo_condition:
            return format_html('<img src="{}" width="100" />', obj.photo_condition.url)
        return "No Photo"

    photo_condition_image.short_description = 'Photo Condition'



admin.site.register(Profile, ProfileAdmin)
admin.site.register(FarmerProfile, FarmerProfileAdmin)
admin.site.register(CoordinatorProfile, CoordinatorProfileAdmin)
admin.site.register(Crop, CropAdmin)