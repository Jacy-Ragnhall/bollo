from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('job/<int:job_id>/analytics/', views.job_analytics_view, name='job_analytics'),
]
