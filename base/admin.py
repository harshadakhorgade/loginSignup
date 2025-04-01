from django.contrib import admin
from .models import Profile, FarmerProfile,CoordinatorProfile,Crop,Product,Notification
from django.utils.html import format_html

from .models import Product, ProductImage


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'message', 'timestamp')  # Ensure timestamp is a field in your Notification model

admin.site.register(Notification, NotificationAdmin)



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





class ProductImageInline(admin.TabularInline):  # or use StackedInline
    model = ProductImage
    extra = 3  # Allows adding 3 additional images by default (change as needed)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')  # Display these fields in the admin list
    inlines = [ProductImageInline]  # Add multiple images in the Product admin page

admin.site.register(Product, ProductAdmin)

admin.site.register(Profile, ProfileAdmin)
admin.site.register(FarmerProfile, FarmerProfileAdmin)
admin.site.register(CoordinatorProfile, CoordinatorProfileAdmin)
admin.site.register(Crop, CropAdmin)

