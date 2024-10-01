from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import FarmerSignUpForm , CoordinatorSignUpForm
from .forms import FarmerProfileForm,FarmerProfile,Profile,CoordinatorProfile,CoordinatorProfileForm
from .forms import CropForm,Crop
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect

@login_required
def home(request):
    return render(request, "home.html", {})

def authView(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect("base:login")  # Ensure you have a URL named 'login' in your URLs configuration
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})

def farmer_signup(request):
    if request.method == 'POST':
        form = FarmerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("base:login")
    else:
        form = FarmerSignUpForm()
    
    return render(request, "registration/farmer_signup.html", {'form': form})

def coordinator_signup(request):
    if request.method == 'POST':
        form = CoordinatorSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("base:login")
    else:
        form = FarmerSignUpForm()
    
    return render(request, "registration/coordinator_signup.html", {'form': form})




@login_required
def farmer_profile(request):
    user = request.user
    # Get or create the Profile for the user
    profile, created = Profile.objects.get_or_create(user=user)
    
    # Get or create the FarmerProfile for the Profile
    farmer_profile, created = FarmerProfile.objects.get_or_create(profile=profile)
    
    if request.method == 'POST':
        form = FarmerProfileForm(request.POST, instance=farmer_profile)
        if form.is_valid():
            form.save()
            return redirect('base:home')  # Redirect to a success page or the home page
    else:
        form = FarmerProfileForm(instance=farmer_profile)
    
    return render(request, 'farmer_profile.html', {'form': form})

@login_required
def coordinator_profile(request):
    user = request.user
    # Get or create the Profile for the user
    profile, created = Profile.objects.get_or_create(user=user)
    
    # Get or create the FarmerProfile for the Profile
    coordinator_profile, created = CoordinatorProfile.objects.get_or_create(profile=profile)
    
    if request.method == 'POST':
        form = CoordinatorProfileForm(request.POST, instance=coordinator_profile)
        if form.is_valid():
            form.save()
            return redirect('base:home')  # Redirect to a success page or the home page
    else:
        form = CoordinatorProfileForm(instance=coordinator_profile)
    
    return render(request, 'coordinator_profile.html', {'form': form})


@login_required
def crop_form(request):
    if request.method == 'POST':
        form = CropForm(request.POST, request.FILES)  # Include request.FILES
        if form.is_valid():
            new_crop = form.save(commit=False)
            new_crop.profile = request.user.profile
            new_crop.save()
            messages.success(request, 'Crop data saved successfully.')
            return redirect('base:home')  # Replace with your actual URL name
    else:
        form = CropForm()

    crops = Crop.objects.filter(profile=request.user.profile)
    
    return render(request, 'crop_form.html', {
        'form': form,
        'crops': crops,
    })

@login_required
def delete_crop(request, crop_id):
    crop = get_object_or_404(Crop, id=crop_id, profile=request.user.profile)
    if request.method == 'POST':
        crop.delete()
        messages.success(request, 'Crop deleted successfully.')
        return redirect('base:crop_form')