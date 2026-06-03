from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('2fa/setup/', views.otp_setup_view, name='otp_setup'),
    path('2fa/verify/', views.otp_verify_view, name='otp_verify'),
    path('2fa/disable/', views.otp_disable_view, name='otp_disable'),
]
