# base/urls.py
from django.urls import path
from . import views 
from django.urls import path, include
from .views import authView, farmer_profile ,home , farmer_signup , coordinator_signup , coordinator_profile , products ,delete_crop,myfarm, crop_detail , notifications_list,unread_notifications_count,delete_notification,plus_cart,minus_cart,checkout
from .forms import  MyPasswordChangeForm
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import LogoutView

# >>>>>>>>>>>>>>>

app_name = 'base'




urlpatterns = [
   
    path('', views.home, name='home'),

    path('notifications/', views.send_notification, name='send_notification'),  # Updated
    path('mark-read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),
    path('ajax/unread_notifications_count/', views.unread_notifications_count, name='unread_notifications_count'),
    path('notification/list', views.notifications_list, name='notifications_list'),  # Confirm this path is correct
    path('notification/delete/<int:notification_id>/', delete_notification, name='delete_notification'),

    path("signup/farmer/", views.farmer_signup, name="farmer_signup"),
    path('accounts/login/farmer/', views.farmer_login, name='farmer_login'),
    # path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('accounts/login/', views.farmer_login, name='login'),
    path("signup/coordinator", views.coordinator_signup, name="coordinator_signup"),
    path("accounts/", include("django.contrib.auth.urls")),
    path('farmer_profile/', views.farmer_profile, name='farmer_profile'),
    path('coordinator_profile/', views.coordinator_profile, name='coordinator_profile'),
    path('coordinator_dashboard/', views.coordinator_dashboard, name='coordinator_dashboard'),
   
    
    # for crop page
    path('crop/<str:crop_name>/',  crop_detail, name='crop_view'),
    #crop form
    path('crop-form/', views.crop_form, name='crop_form'),
    path('crops/delete/<int:crop_id>/', delete_crop, name='delete_crop'),

    # path('add-crop/', views.add_crop, name='add_crop'),
    path('myfarm/', views.myfarm, name='myfarm'),



    # for products page
    path("products",views.products,name="products"),
    path("products/<int:id>/", views.detail, name="product_detail"),

    #add to cart
   
    path('checkout/', views.checkout, name='checkout'),
    path('payment/', views.payment, name='payment'),  # Add this line for 'payment'

    path('plus_cart/', views.plus_cart, name='plus_cart'),
    path('minus_cart/', views.minus_cart, name='minus_cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/count/', views.cart_count, name='cart_count'),
    # path('update-quantity/', views.update_quantity, name='update_quantity'),
    
    #password chanage 
    path('password-change/', 
         auth_views.PasswordChangeView.as_view(
             template_name='registration/password_change_form.html',
             form_class=MyPasswordChangeForm
         ), 
         name='password_change'),
    path('password-change/done/', 
         auth_views.PasswordChangeDoneView.as_view(
             template_name='registration/password_change_done.html'
         ), 
         name='password_change_done'),

    

  
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# added for product images  on products page 

