from django.urls import path, include
from . import views
from .views import authView, farmer_profile, home, farmer_signup, coordinator_signup, coordinator_profile,delete_crop
from .forms import MyPasswordChangeForm
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'base'

urlpatterns = [
    path("", views.home, name="home"),
    path("signup/farmer", views.farmer_signup, name="farmer_signup"),
    path("signup/coordinator", views.coordinator_signup, name="coordinator_signup"),
    path("accounts/", include("django.contrib.auth.urls")),
    path('farmer_profile/', views.farmer_profile, name='farmer_profile'),
    path('coordinator_profile/', views.coordinator_profile, name='coordinator_profile'),
    path('crop-form/', views.crop_form, name='crop_form'),
    path('crops/delete/<int:crop_id>/', delete_crop, name='delete_crop'),

    # Password change
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
]
