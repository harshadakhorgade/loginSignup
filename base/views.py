from django.shortcuts import render, redirect, get_object_or_404 # Import get_object_or_404
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from rest_framework_simplejwt.tokens import AccessToken
from .models import Product, Cart ,FarmerProfile, Crop,Notification
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from .serializers import FarmerSignUpSerializer
from django.contrib.auth import authenticate, login
from .forms import FarmerSignUpForm , CoordinatorSignUpForm ,NotificationForm
from .forms import FarmerProfileForm,FarmerProfile,Profile,CoordinatorProfile,CoordinatorProfileForm
from .forms import CropForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Profile , ProductImage
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Profile, FarmerProfile
from .forms import FarmerProfileForm
from .serializers import FarmerSignUpSerializer,CoordinatorSignUpSerializer
from .forms import CropForm,Crop
from django.contrib import messages
import json
from .serializers import CropSerializer
from django.http import HttpResponseNotAllowed
from .forms import LoginForm  # Adjust the import based on your project structure
from .serializers import ProductSerializer, CartSerializer


from django.http import JsonResponse
from rest_framework.parsers import JSONParser

from django.http import Http404
from django.contrib import messages


# farmer home page
# base/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import NotificationForm
from .models import Notification, CoordinatorProfile, Profile ,CartItem # Import necessary models


@login_required
def home(request):
    user_profile, created = Profile.objects.get_or_create(user=request.user)  # Ensures a profile exists

    if user_profile.user_type == 'Farmer':
        return render(request, 'home.html')

    elif user_profile.user_type == 'Coordinator':
        return render(request, 'coordinator_dashboard.html')

    return render(request, 'home.html')  # Default fallback

#--------- ---------notifications ------------------->

def send_notification(request):
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            notification = form.save(commit=False)
            # Create a notification for all farmers
            farmers = User.objects.filter(profile__user_type='Farmer')
            for farmer in farmers:
                Notification.objects.create(user=farmer, title=notification.title, message=notification.message)
            return redirect('base:notifications_list')  # Redirect to home or another relevant page
    else:
        form = NotificationForm()

    return render(request, 'send_notification.html', {'form': form})


def notifications_list(request):
    # Allow only farmers to view notifications
    if request.user.profile.user_type != 'Farmer':
        return redirect('base:home')  # Redirect coordinators or other user types

    # Fetch notifications for the authenticated farmer
    notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')  # Newest first
    return render(request, 'notifications_list.html', {'notifications': notifications})


def mark_notification_read(request, notification_id):
    if request.method == "POST" and request.user.is_authenticated:
        notification = get_object_or_404(Notification, id=notification_id, user=request.user)
        notification.is_read = True
        notification.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)


def unread_notifications_count(request):
    if request.user.is_authenticated:
        unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
        return JsonResponse({'unread_count': unread_count})
    return JsonResponse({'unread_count': 0})




def delete_notification(request, notification_id):
    

    if request.method == "POST":
        notification = get_object_or_404(Notification, id=notification_id)
        notification.delete()
    
        return redirect('base:notifications_list')

    return redirect('base:notifications_list')  # Redirect if the method is not POST


def authView(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect("base:login")  # Ensure you have a URL named 'login' in your URLs configuration
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})

    
@csrf_exempt
def farmer_signup(request):
    if request.method == 'POST':
        # Check if the request is coming from Postman with JSON data
        if request.headers.get('Content-Type') == 'application/json':
            data = json.loads(request.body)
            form = FarmerSignUpForm(data)
            is_json_request = True
        else:
            form = FarmerSignUpForm(request.POST)
            is_json_request = False

        if form.is_valid():
            # Save the user
            user = form.save()

            # Create a Profile for the user
            profile, created = Profile.objects.get_or_create(user=user)

            # Automatically create a token for the new user
            token, _ = Token.objects.get_or_create(user=user)
            print(f"Token for the user {user.username}: {token.key}")  # For testing

            # Create FarmerProfile linked to the Profile
            farmer_profile, created = FarmerProfile.objects.get_or_create(profile=profile)

            # Populate FarmerProfile fields if created
            if created:
                farmer_profile.username = user.username
                farmer_profile.role = 'Farmer'  # Set role as 'Farmer'
                farmer_profile.first_name = form.cleaned_data.get('first_name', '')
                farmer_profile.last_name = form.cleaned_data.get('last_name', '')
                farmer_profile.mobile_number = form.cleaned_data.get('mobile_number', '')
                farmer_profile.date_of_birth = form.cleaned_data.get('date_of_birth', None)
                farmer_profile.email = user.email  # Automatically set from the user object
                farmer_profile.village = form.cleaned_data.get('village', '')
                farmer_profile.district = form.cleaned_data.get('district', '')
                farmer_profile.taluka = form.cleaned_data.get('taluka', '')
                farmer_profile.state = form.cleaned_data.get('state', '')
                farmer_profile.save()

            # Log the user in after successful registration
            login(request, user)

            # If the request is from Postman (JSON), return the token in the response
            if is_json_request:
                return JsonResponse({
                    'message': 'User registered successfully',
                    'token': token.key
                })

            # If the request is from the website (form submission), redirect to the login page
            return redirect("base:login")

        else:
            # Return form errors as JSON response if request was JSON, else show errors on page
            if is_json_request:
                return JsonResponse({
                    'message': 'Registration failed',
                    'errors': form.errors
                }, status=400)
    
    elif request.method == 'GET':
        # Check if the request is from Postman by looking at the headers
        if request.headers.get('Content-Type') == 'application/json':
            # Fetch all users
            users = User.objects.all().values('id', 'username', 'email', 'first_name', 'last_name')

            # Convert QuerySet to list
            users_list = list(users)

            return JsonResponse({
                'users': users_list
            })

    # Render the form for regular web requests
    form = FarmerSignUpForm()
    return render(request, "registration/farmer_signup.html", {'form': form})
    
@csrf_exempt
def coordinator_signup(request):
    if request.method == 'POST':
        # Check if the request is coming from Postman with JSON data
        if request.headers.get('Content-Type') == 'application/json':
            data = json.loads(request.body)
            form = CoordinatorSignUpForm(data)
            is_json_request = True
        else:
            form = CoordinatorSignUpForm(request.POST)
            is_json_request = False

        if form.is_valid():
            # Save the user
            user = form.save()

            # Create a Profile for the user
            profile, created = Profile.objects.get_or_create(user=user)

            # Automatically create a token for the new user
            token, _ = Token.objects.get_or_create(user=user)
            print(f"Token for the user {user.username}: {token.key}")  # For testing

            # Create CoordinatorProfile linked to the Profile
            coordinator_profile, created = CoordinatorProfile.objects.get_or_create(profile=profile)

            # Populate CoordinatorProfile fields if created
            if created:
                coordinator_profile.username = user.username
                coordinator_profile.role = 'Coordinator'  # Set role as 'Coordinator'
                coordinator_profile.first_name = form.cleaned_data.get('first_name', '')
                coordinator_profile.last_name = form.cleaned_data.get('last_name', '')
                coordinator_profile.mobile_number = form.cleaned_data.get('mobile_number', '')
                coordinator_profile.date_of_birth = form.cleaned_data.get('date_of_birth', None)
                coordinator_profile.email = user.email  # Automatically set from the user object
                coordinator_profile.village = form.cleaned_data.get('village', '')
                coordinator_profile.district = form.cleaned_data.get('district', '')
                coordinator_profile.taluka = form.cleaned_data.get('taluka', '')
                coordinator_profile.state = form.cleaned_data.get('state', '')
                coordinator_profile.save()

            # Log the user in after successful registration
            login(request, user)

            # If the request is from Postman (JSON), return the token in the response
            if is_json_request:
                return JsonResponse({
                    'message': 'User registered successfully',
                    'token': token.key
                })

            # If the request is from the website (form submission), redirect to the login page
            return redirect("base:login")

        else:
            # Return form errors as JSON response if request was JSON, else show errors on page
            if is_json_request:
                return JsonResponse({
                    'message': 'Registration failed',
                    'errors': form.errors
                }, status=400)

    elif request.method == 'GET':
        # Check if the request is from Postman by looking at the headers
        if request.headers.get('Content-Type') == 'application/json':
            # Fetch all users
            users = User.objects.all().values('id', 'username', 'email', 'first_name', 'last_name')

            # Convert QuerySet to list
            users_list = list(users)

            return JsonResponse({
                'users': users_list
            })

    # Render the form for regular web requests
    form = CoordinatorSignUpForm()
    return render(request, "registration/coordinator_signup.html", {'form': form})


@csrf_exempt
@login_required
def farmer_profile(request):
    user = request.user
    
    # Get the farmer profile for the logged-in user
    profile, created = Profile.objects.get_or_create(user=user)
    farmer_profile, created = FarmerProfile.objects.get_or_create(profile=profile)

    if request.method == 'GET':
        # Check if the request is from Postman or expects JSON
        if request.headers.get('Accept') == 'application/json':
            # Prepare the farmer profile data to return as JSON
            farmer_data = {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "mobile_number": farmer_profile.mobile_number,
                "village": farmer_profile.village,
                "district": farmer_profile.district,
                "taluka": farmer_profile.taluka,
                "state": farmer_profile.state,
            }
            return JsonResponse(farmer_data, status=200)

        # For normal GET requests (render HTML)
        form = FarmerProfileForm(instance=farmer_profile)
        return render(request, 'farmer_profile.html', {'form': form})
    
    if request.method in ['POST', 'PUT']:
        try:
            # Check if the request is a JSON request
            if request.content_type == 'application/json':
                data = json.loads(request.body)
                form = FarmerProfileForm(data, instance=farmer_profile)
                
                if form.is_valid():
                    form.save()
                    # Return success response with submitted data
                    response_data = {
                        "message": "Profile saved successfully",
                        "data": form.cleaned_data
                    }
                    return JsonResponse(response_data, status=201)  # 201 Created
                else:
                    # Return errors if the form is invalid
                    return JsonResponse({
                        "message": "Profile submission failed. Please check your input.",
                        "errors": form.errors
                    }, status=400)  # 400 Bad Request

            else:
                # Handle standard form submission
                form = FarmerProfileForm(request.POST, instance=farmer_profile)
                if form.is_valid():
                    form.save()
                    return redirect('base:home')  # Redirect to the home page after saving
                else:
                    print("Form errors:", form.errors)  # Log errors if needed
                    return render(request, 'farmer_profile.html', {'form': form})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    elif request.method == 'DELETE':
        # Delete the farmer's profile for the logged-in user
        farmer_profile.delete()
        return JsonResponse({"message": "Profile deleted successfully"}, status=204)

    return JsonResponse({"error": "Method not allowed"}, status=405)



@csrf_exempt
@login_required
def coordinator_profile(request):
    user = request.user
    
    # Get the farmer profile for the logged-in user
    profile, created = Profile.objects.get_or_create(user=user)
    coordinator_profile, created = CoordinatorProfile.objects.get_or_create(profile=profile)

    if request.method == 'GET':
        # Check if the request is from Postman or expects JSON
        if request.headers.get('Accept') == 'application/json':
            # Prepare the farmer profile data to return as JSON
            coordinaor_data = {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "mobile_number": coordinator_profile.mobile_number,
                "village": coordinator_profile.village,
                "district": coordinator_profile.district,
                "taluka": coordinator_profile.taluka,
                "state": coordinator_profile.state,
            }
            
            return JsonResponse(coordinaor_data, status=200)

        # For normal GET requests (render HTML)
        form = CoordinatorProfileForm(instance=coordinator_profile)
        return render(request, 'coordinator_profile.html', {'form': form})
    
    if request.method in ['POST', 'PUT']:
        try:
            # Check if the request is a JSON request
            if request.content_type == 'application/json':
                data = json.loads(request.body)
                form = CoordinatorProfileForm(data, instance=coordinator_profile)
                
                if form.is_valid():
                    form.save()
                    # Return success response with submitted data
                    response_data = {
                        "message": "Profile saved successfully",
                        "data": form.cleaned_data
                    }
                    return JsonResponse(response_data, status=201)  # 201 Created
                else:
                    # Return errors if the form is invalid
                    return JsonResponse({
                        "message": "Profile submission failed. Please check your input.",
                        "errors": form.errors
                    }, status=400)  # 400 Bad Request

            else:
                # Handle standard form submission
                form = CoordinatorProfileForm(request.POST, instance=coordinator_profile)
                if form.is_valid():
                    form.save()
                    return redirect('base:coordinator_dashboard')  # Redirect to the home page after saving
                else:
                    print("Form errors:", form.errors)  # Log errors if needed
                    return render(request, 'coordinator_profile.html', {'form': form})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    elif request.method == 'DELETE':
        # Delete the farmer's profile for the logged-in user
        coordinator_profile.delete()
        return JsonResponse({"message": "Profile deleted successfully"}, status=204)

    return JsonResponse({"error": "Method not allowed"}, status=405)

@api_view(['POST', 'GET'])
def farmer_login(request):
    if request.method == 'POST':
        # For API clients
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # Create or retrieve the token for the user
            token, created = Token.objects.get_or_create(user=user)

            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                # Redirect to home page if HTML request
                return HttpResponseRedirect(reverse('base:home'))
            else:
                # Return JSON response for API clients
                return Response({
                    "message": "Login successful.",
                    "token": token.key
                }, status=status.HTTP_200_OK)
        else:
            # Return error response for invalid credentials
            return Response({"error": "Invalid username or password."}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        # For web browsers, render the login form
        form = LoginForm()  # Make sure you have a FarmerLoginForm defined
        return render(request, "registration/login.html", {'form': form})
    

@login_required
def coordinator_dashboard(request):
    print("Entered coordinator_dashboard view")  # Debug message
    
    # Accessing the coordinator's profile
    try:
        coordinator_profile = request.user.profile.coordinator_profile  # Get the associated CoordinatorProfile
    except AttributeError:
        print("User does not have a CoordinatorProfile.")
        return render(request, 'coordinator_dashboard.html', {'error': 'Coordinator profile not found.'})

    # Fetch farmers in the same location as the coordinator
    farmers = FarmerProfile.objects.filter(
        village=coordinator_profile.village,  # Accessing village directly from CoordinatorProfile
        district=coordinator_profile.district,  # Ensure these attributes exist in CoordinatorProfile
        taluka=coordinator_profile.taluka
    )

    # Fetch crops for each farmer
    crops = Crop.objects.filter(profile__in=[farmer.profile for farmer in farmers])

    print(farmers)  # Check if farmers are being fetched
    print(crops)    # Check if crops are being fetched

    context = {
        'farmers': farmers,
        'crops': crops,
    }
    
    return render(request, 'coordinator_dashboard.html', context)


@csrf_exempt # ------------------ Combined Views for Products--------- ---------
def is_api_request(request):
    return request.accepts('application/json')

def products(request):
    # Query to get all products
    products = Product.objects.all()
    
    if request.method == 'GET':
        # Check if the client expects a JSON response
        if request.headers.get('Accept') == 'application/json':
            # Build a list of product dictionaries
            product_list = [
                {
                    'id': product.id,
                    'name': product.name,
                    'description': product.description,
                    'price': str(product.price),  # Convert price to string if it's a Decimal
                    'image': product.image.url if product.image else None  # Add image URL if available
                }
                for product in products
            ]
            # Return JSON response
            return JsonResponse({'products': product_list}, safe=False)
        
        # Otherwise, render the HTML template
        return render(request, 'products.html', {'products': products})
    
def detail(request, id):
    product = get_object_or_404(Product, id=id)
    images = ProductImage.objects.filter(product=product)  # Get additional images
    return render(request, "detail.html", {"product": product, "images": images})


from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Cart, Product, CartItem
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Product, Cart, CartItem

@csrf_exempt
@login_required
def add_to_cart(request, product_id):
    try:
        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user, is_active=True)

        # Try to get the CartItem for this product; do not increment if it already exists
        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': 1})

        if not item_created:
            # Item already in the cart, no need to add again
            response_data = {
                'success': False,
                'message': f'Product {product.name} is already in your cart.',
                'cart_item_count': CartItem.objects.filter(cart=cart).count(),  # Distinct item count
                'total_quantity': sum(item.quantity for item in CartItem.objects.filter(cart=cart)),  # Total quantity
                'current_quantity': cart_item.quantity,  # Quantity of the current product
            }
            return JsonResponse(response_data, status=200)

        # If item is newly added, save and respond with success message
        cart_item.save()

        response_data = {
            'success': True,
            'message': f'Product {product.name} has been added to your cart.',
            'cart_item_count': CartItem.objects.filter(cart=cart).count(),
            'total_quantity': sum(item.quantity for item in CartItem.objects.filter(cart=cart)),
            'current_quantity': cart_item.quantity,
        }
        return JsonResponse(response_data, status=200)

    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)





from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Cart, CartItem

@csrf_exempt
@login_required
def cart_detail(request):
    # Get the user's active cart
    cart = get_object_or_404(Cart, user=request.user, is_active=True)
    items = cart.items.select_related('product')  # Fetch related products in one query

    # Calculate the total price and include shipping
    total_price = sum(item.total_price for item in items)
    shipping_charges = 40
    total_price_with_shipping = total_price + shipping_charges
    
    if request.headers.get('Accept') == 'application/json':
        product_list = [
            {
                'id': item.product.id,
                'name': item.product.name,
                'description': item.product.description,
                'price': str(item.product.price),
                'quantity': item.quantity,
                'total_price': str(item.total_price),
                'image': item.product.image.url if item.product.image else None
            }
            for item in items
        ]
        response_data = {
            'cart_id': cart.id,
            'products': product_list,
            'total_items': items.count(),
            'total_price': str(total_price),
            'total_price_with_shipping': str(total_price_with_shipping)
        }
        return JsonResponse(response_data, status=200)

    return render(request, 'cart.html', {
        'cart': cart,
        'items': items,
        'total_price': total_price,
        'total_price_with_shipping': total_price_with_shipping
    })


from django.shortcuts import get_object_or_404, redirect
from .models import Cart, Product


@csrf_exempt
@login_required
def remove_from_cart(request, product_id):
    cart = get_object_or_404(Cart, user=request.user, is_active=True)
    product = get_object_or_404(Product, id=product_id)

    if product in cart.products.all():
        cart.products.remove(product)

    # Check if the request expects a JSON response
    if request.headers.get('Accept') == 'application/json':
        response_data = {
            'message': 'Product removed from cart successfully.',
            'cart_id': cart.id,
            'total_items': cart.products.count()  # Optionally include the total number of items in the cart
        }
        return JsonResponse(response_data, status=200)  # Return a 200 OK response

    # Ensure the redirect uses the correct URL pattern
    return redirect('base:cart_detail')




from django.db.models import Sum
from .models import Cart  # Adjust the import based on your project structure
def cart_count(request):
    cart = Cart.objects.filter(user=request.user, is_active=True).first()
    cart_count = cart.products.count() if cart else 0  # Use count() for the number of products
    return JsonResponse({'cart_count': cart_count})

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Product, Cart, CartItem

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Product, Cart, CartItem
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Product, Cart, CartItem

def plus_cart(request):
    if request.method == "GET":
        # Retrieve product and cart information
        product_id = request.GET.get('prod_id')
        product = get_object_or_404(Product, id=product_id)
        cart = Cart.objects.get(user=request.user, is_active=True)
        

        # Retrieve or create the cart item
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        # Increment the quantity
        cart_item.quantity += 1
        cart_item.save()

        # Recalculate totals
        total_price = cart.calculate_total()
        shipping_charges = 40  # Define shipping charges
        total_price_with_shipping = total_price + shipping_charges

        return JsonResponse({
            'quantity': cart_item.quantity,
            'total_price': total_price,
            'total_price_with_shipping': total_price_with_shipping
        })

def minus_cart(request):
    if request.method == "GET":
        # Retrieve product and cart information
        product_id = request.GET.get('prod_id')
        product = get_object_or_404(Product, id=product_id)
        cart = Cart.objects.get(user=request.user, is_active=True)

        # Retrieve the cart item
        cart_item = get_object_or_404(CartItem, cart=cart, product=product)

        # Decrement the quantity only if it's greater than 1
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            # Optionally, remove the item from the cart when the quantity is 0
            cart_item.delete()

        # Recalculate totals
        total_price = cart.calculate_total()
        shipping_charges = 40
        total_price_with_shipping = total_price + shipping_charges

        return JsonResponse({
            'quantity': cart_item.quantity if cart_item.id else 0,  # Return 0 if item is deleted
            'total_price': total_price,
            'total_price_with_shipping': total_price_with_shipping
        })





from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cart, CartItem, FarmerProfile

from django.shortcuts import render

# base/views.py
def checkout(request):
    # Get the active cart for the user
    cart = Cart.objects.get(user=request.user, is_active=True)
    cart_items = CartItem.objects.filter(cart=cart)

    # Calculate total price (sum of item prices * quantity)
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    # Add shipping charges (₹40)
    shipping_charges = 40
    total_price_with_shipping = total_price + shipping_charges

    context = {
        'cart_items': cart_items,
        'total_price': total_price_with_shipping,  # Updated with shipping charges
    }

    return render(request, 'checkout.html', context)

def payment(request):
    # Payment view logic (you can render a payment template or handle payment here)
    return render(request, 'base/payment.html')

# ---------------------------crop views---------------------------------

@csrf_exempt# Crop details stored in a dictionary
def crop_detail(request, crop_name):
    crops_data = {
        'onion': {
            'name': 'Onion',
            'description': 'Onions are widely used vegetables known for their pungent flavor.',
            'climate': 'Cool climate, ideal for growing in winter.',
            'season': 'Winter',
            'image': 'img/onion-icon.png'
        },
        'chilli': {
            'name': 'Chilli',
            'description': 'Chillies are small, spicy fruits used in cooking.',
            'climate': 'Hot and dry conditions are ideal for chillies.',
            'season': 'Summer',
            'image': 'img/chilli-icon.png'
        },
        'turmeric': {
            'name': 'Turmeric',
            'description': 'Turmeric is a spice known for its anti-inflammatory properties.',
            'climate': 'Tropical climate with good rainfall.',
            'season': 'Monsoon',
            'image': 'img/turmeric-icon.png'
        },
        'cumin': {
            'name': 'Cumin',
            'description': 'Cumin is an aromatic spice used in many dishes.',
            'climate': 'Hot and dry climate, requires a long growing season.',
            'season': 'Late Summer',
            'image': 'img/cumin-icon.jpg'
        },
        'garlic': {
            'name': 'Garlic',
            'description': 'Garlic is a bulbous plant often used for flavoring foods.',
            'climate': 'Cool and dry climate, well-drained soil.',
            'season': 'Winter',
            'image': 'img/garlic-icon.png'
        },
        'chickoo': {
            'name': 'Chickoo',
            'description': 'Chickoo, or sapodilla, is a tropical fruit known for its sweet and grainy texture.',
            'climate': 'Warm and tropical climate with moderate rainfall.',
            'season': 'Throughout the year, best in summer.',
            'image': 'img/chikoo-icon.png'
        },
        'spices': {
            'name': 'Spices',
            'description': 'A variety of spices including cumin, turmeric, and others used for seasoning.',
            'climate': 'Varies depending on the spice, generally hot and dry climates.',
            'season': 'Varies depending on the spice.',
            'image': 'img/spices-icon.png'
        },
        'cashew': {
            'name': 'Cashew',
            'description': 'Cashews are popular nuts rich in healthy fats and nutrients.',
            'climate': 'Tropical climate with high humidity.',
            'season': 'Spring to early summer.',
            'image': 'img/cashew-icon.png'
        }
      
    }

    crop = crops_data.get(crop_name)

    if crop is None:
        if request.headers.get('Accept') == 'application/json' or request.GET.get('format') == 'json':
            return JsonResponse({'error': 'Crop not found'}, status=404)
        else:
            raise Http404("Crop not found")

    # Check if the request is for JSON
    if request.headers.get('Accept') == 'application/json' or request.GET.get('format') == 'json':
        return JsonResponse(crop)

    # Otherwise, return HTML
    return render(request, 'crops.html', {'crop': crop})

@csrf_exempt  # For simplicity; handle CSRF properly in production
@login_required
def crop_form(request):
    if request.content_type == 'application/json':  # For API requests via Postman
        data = JSONParser().parse(request)
        serializer = CropSerializer(data=data, context={'request': request})

        if serializer.is_valid():
            serializer.save()  # Associate crop with the logged-in user's profile
            return JsonResponse({
                'message': 'Crop created successfully!',
                'crop': serializer.data
            }, status=201)  # HTTP 201 Created

        return JsonResponse(serializer.errors, status=400)  # HTTP 400 Bad Request

    elif request.method == 'POST':  # Handle regular form submission
        form = CropForm(request.POST, request.FILES)
        if form.is_valid():
            new_crop = form.save(commit=False)
            new_crop.profile = request.user.profile  # Associate crop with the user's profile
            new_crop.save()
            if request.headers.get('Content-Type') == 'application/json':  # Return JSON for Postman
                return JsonResponse({
                    'message': 'Crop saved successfully!',
                    'crop': new_crop.crop_type
                }, status=201)
            else:
                messages.success(request, 'Crop data saved successfully.')
                return redirect('base:myfarm')  # Redirect to 'myfarm' for non-JSON requests

    else:  # Handle GET request
        form = CropForm()
        crops = Crop.objects.filter(profile=request.user.profile)

    return render(request, 'crop_form.html', {
        'form': form,
        'crops': crops,
    })





@csrf_exempt
@csrf_exempt  # For simplicity; handle CSRF properly in production
@login_required
def myfarm(request):
    # Fetch crops for the logged-in user
    crops = Crop.objects.filter(profile=request.user.profile)

    # If the request is coming from Postman and expects JSON
    if request.headers.get('Content-Type') == 'application/json':
        serializer = CropSerializer(crops, many=True)
        return JsonResponse({
            'message': 'Crops fetched successfully!',
            'crops': serializer.data
        }, safe=False)

    # For GET requests, display crops
    return render(request, 'myfarm.html', {'crops': crops})

    
@login_required
def delete_crop(request, crop_id):
    crop = get_object_or_404(Crop, id=crop_id, profile=request.user.profile)
    if request.method == 'POST':
        crop.delete()
        messages.success(request, 'Crop deleted successfully.')
        return redirect('base:myfarm')