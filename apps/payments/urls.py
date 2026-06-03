from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('checkout/<int:job_id>/', views.checkout_view, name='checkout'),
    path('success/<int:pk>/', views.payment_success_view, name='payment_success'),
]
