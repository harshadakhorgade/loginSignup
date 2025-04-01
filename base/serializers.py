from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class FarmerSignUpSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, required=True, label="Password")
    password2 = serializers.CharField(write_only=True, required=True, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def validate(self, data):
        # Ensure both passwords match
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        # Use the cleaned password1
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password1'])  # Set the password
        user.save()
        return user
    

class CoordinatorSignUpSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, required=True, label="Password")
    password2 = serializers.CharField(write_only=True, required=True, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def validate(self, data):
        # Ensure both passwords match
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        # Use the cleaned password1
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password1'])  # Set the password
        user.save()
        return user


from .models import FarmerProfile,CoordinatorProfile,Crop

class FarmerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmerProfile
        fields = '__all__' 

class CoordinatorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoordinatorProfile
        fields = '__all__' 



class CropSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crop
        fields = '__all__'
        read_only_fields = ('profile',)  # Prevent overwriting in JSON requests

    def create(self, validated_data):
        request = self.context['request']
        validated_data['profile'] = request.user.profile  # Associate the crop with the user's profile
        return super().create(validated_data)

from rest_framework import serializers
from .models import Product, Cart

# Serializer for Product model
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'image']  # Include all the necessary fields

# Serializer for Cart model
class CartSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)  # Nested serializer for the products

    class Meta:
        model = Cart
        fields = ['id', 'user', 'products', 'is_active']  # Include fields for the cart
