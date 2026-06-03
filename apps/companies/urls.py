from django.urls import path
from . import views

app_name = 'companies'

urlpatterns = [
    path('companies/', views.company_list_view, name='company_list'),
    path('companies/<int:pk>/', views.company_detail_view, name='company_detail'),
    path('companies/<int:pk>/review/', views.submit_review_view, name='submit_review'),
]
