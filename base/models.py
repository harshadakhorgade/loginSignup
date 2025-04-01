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
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='farmer_profile')
    username = models.CharField(max_length=150, unique=True, null=True)  # To store the username
    role = models.CharField(max_length=15,null=True)  # To store the role
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    mobile_number = models.CharField(max_length=15)
    date_of_birth = models.DateField(null=True, blank=True)
    email= models.EmailField(unique=True, null=True)
    village = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    taluka = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    
    def __str__(self):
        return f"Farmer Profile: {self.first_name} {self.last_name}"

class CoordinatorProfile(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='coordinator_profile')
    username = models.CharField(max_length=150, unique=True, null=True)  # To store the username
    role = models.CharField(max_length=15,null=True)  # To store the role
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    mobile_number = models.CharField(max_length=15)
    date_of_birth = models.DateField(null=True, blank=True)
    email= models.EmailField(unique=True, null=True)
    village = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    taluka = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    
    def __str__(self):
        return f"Coordinator Profile: {self.first_name} {self.last_name}"



  

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.name
    

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/additional/')

    def __str__(self):
        return f"{self.product.name} - Image"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem', blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Cart for {self.user.username}"
    
    
    # Method to calculate total price of products in the cart
    def calculate_total(self):
        total = sum(item.total_price for item in self.items.all())
        return total

    # Method to calculate total with shipping cost (optional)
    def calculate_total_with_shipping(self, shipping_cost=40):
        return self.calculate_total() + shipping_cost

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    @property
    def total_price(self):
        return self.product.price * self.quantity   

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
    condition = models.CharField(max_length=100 , default='Healthy')
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
    


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # Allow null for existing rows
    title = models.CharField(max_length=255)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.title