from django.contrib.auth.forms import UserCreationForm , PasswordChangeForm
from django import forms
from django.contrib.auth.models import User
from .models import Profile, FarmerProfile,CoordinatorProfile,Crop
from .models import Crop
from django.core.exceptions import ValidationError
from datetime import date


class FarmerSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Create Profile instance for the user
            profile = Profile.objects.create(user=user, user_type='Farmer')
            # Create FarmerProfile instance with empty initial data
            FarmerProfile.objects.create(
                profile=profile,
                username=user.username,  # Add username
                role='Farmer',           # Add role
                first_name='',
                last_name='',
                mobile_number='',
                date_of_birth=None,
                email=user.email,
                village='',
                district='',
                taluka='',
                state=''
            )
        return user


class FarmerProfileForm(forms.ModelForm):
    class Meta:
        model = FarmerProfile
        fields = ['first_name', 'last_name', 'username', 'mobile_number', 'date_of_birth', 'email', 'village', 'district', 'taluka', 'state']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'id': 'date_of_birth'}),
        }
    
    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        if date_of_birth and (date_of_birth.year >= date.today().year):
            raise ValidationError('The birth date must be before the current year.')
        return date_of_birth
        


class CoordinatorSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Create Profile instance for the user
            profile = Profile.objects.create(user=user, user_type='Coordinator')
            # Create FarmerProfile instance with empty initial data
            CoordinatorProfile.objects.create(
                profile=profile,
                username=user.username,  # Add username
                role='Coordinator',           # Add role
                first_name='',
                last_name='',
                mobile_number='',
                date_of_birth=None,
                email=user.email,
                village='',
                district='',
                taluka='',
                state=''
            )
        return user


class CoordinatorProfileForm(forms.ModelForm):
    class Meta:
        model = FarmerProfile
        fields = ['first_name', 'last_name', 'username', 'mobile_number', 'date_of_birth', 'email', 'village', 'district', 'taluka', 'state']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'id': 'date_of_birth'}),
        }
    
    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        if date_of_birth and (date_of_birth.year >= date.today().year):
            raise ValidationError('The birth date must be before the current year.')
        return date_of_birth

class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='Old Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Old Password'}),
    )
    new_password1 = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Password'}),
    )
    new_password2 = forms.CharField(
        label='Confirm New Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm New Password'}),
    )

    # class Meta:
    #     model = forms.Model
    #     fields = ['old_password', 'new_password1', 'new_password2']



class CropForm(forms.ModelForm):
    class Meta:
        model = Crop
        fields = [
            'username',
            'crop_type',
            'variety',
            'planting_date',
            'expected_harvest_date',
            'field_number',
            'fertilizer_usage',
            'condition',
            'problems',
            'irrigation_type',
            'season',
            'photo_crop_condition',
            'area_in_acres',
            'land_type',
            'crop_category', 
            'farmer_type',
        ]
        widgets = {
            'planting_date': forms.DateInput(attrs={'type': 'date'}),
            'expected_harvest_date': forms.DateInput(attrs={'type': 'date'}),
            'fertilizer_usage': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Specify fertilizers and quantities'}),
            'problems': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Describe any crop problems'}),
            'photo_crop_condition': forms.ClearableFileInput(attrs={'accept': 'image/*'}),  # Accept images
            'area_in_acres': forms.NumberInput(attrs={'placeholder': 'Enter area in acres'}),
        }
        
