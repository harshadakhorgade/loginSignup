from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    USER_TYPES = [
        ('Farmer', 'Farmer'),
        ('Coordinator', 'Coordinator'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, null=True)
    user_type = models.CharField(max_length=15, choices=USER_TYPES, default='Farmer')

    def __str__(self):
        return f"{self.user.username} - {self.user_type}"

class FarmerProfile(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='farmer_profile')
    username = models.CharField(max_length=150, unique=True, null=True)
    role = models.CharField(max_length=15, null=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    mobile_number = models.CharField(max_length=15)
    date_of_birth = models.DateField(null=True, blank=True)
    email = models.EmailField(unique=True, null=True)
    village = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    taluka = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    
    def __str__(self):
        return f"Farmer Profile: {self.first_name} {self.last_name}"

class CoordinatorProfile(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='coordinator_profile')
    username = models.CharField(max_length=150, unique=True, null=True)
    role = models.CharField(max_length=15, null=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    mobile_number = models.CharField(max_length=15)
    date_of_birth = models.DateField(null=True, blank=True)
    email = models.EmailField(unique=True, null=True)
    village = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    taluka = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    
    def __str__(self):
        return f"Coordinator Profile: {self.first_name} {self.last_name}"

# Updated Crop Model with Choices
class Crop(models.Model):
    SEASON_CHOICES = [
        ('Kharif', 'Kharif'),
        ('Rabi', 'Rabi'),
        ('Summer', 'Summer'),
    ]

    LAND_TYPE_CHOICES = [
        ('Jirayati', 'Jirayati'),
        ('Bagayati', 'Bagayati'),
        ('Koradwahi', 'Koradwahi'),
        ('Kharepat', 'Kharepat'),
    ]

    CROP_CATEGORY_CHOICES = [
        ('Food Crops', 'Food Crops'),
        ('Fodder Crops', 'Fodder Crops'),
        ('Fruit Crops', 'Fruit Crops'),
        ('Spices', 'Spices'),
        ('Vegetables', 'Vegetables'),
        ('Flower Crops', 'Flower Crops'),
    ]

    FARMER_TYPE_CHOICES = [
        ('Land Owner', 'Land Owner'),
        ('Tenant', 'Tenant'),
        ('Cultivator', 'Cultivator'),
        ('Contract', 'Contract'),
    ]

    IRRIGATION_CHOICES = [
        ('Drip', 'Drip'),
        ('Sprinkle', 'Sprinkle'),
        ('Pump', 'Pump'),
    ]

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='crops', default=1)
    username = models.CharField(max_length=150, null=True)
    crop_type = models.CharField(max_length=50)
    variety = models.CharField(max_length=100)
    planting_date = models.DateField()
    expected_harvest_date = models.DateField()
    field_number = models.CharField(max_length=100)
    fertilizer_usage = models.TextField(blank=True, null=True)
    condition = models.CharField(max_length=100)
    problems = models.TextField(default=1)
    irrigation_type = models.CharField(max_length=50, choices=IRRIGATION_CHOICES, default='Drip')
    season = models.CharField(max_length=50, choices=SEASON_CHOICES, default='Rabi')
    land_type = models.CharField(max_length=50, choices=LAND_TYPE_CHOICES, default='Jirayati')
    crop_category = models.CharField(max_length=50, choices=CROP_CATEGORY_CHOICES, default='Food Crops')
    farmer_type = models.CharField(max_length=50, choices=FARMER_TYPE_CHOICES, default='Land Owner')
    photo_crop_condition = models.ImageField(upload_to='crop_images/', blank=True, null=True)
    area_in_acres = models.DecimalField(max_digits=5, decimal_places=2, null=True, default=1)

    def __str__(self):
        return f"{self.crop_type} ({self.variety})"
