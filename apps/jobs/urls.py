from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('jobs/', views.job_list_view, name='job_list'),
    path('jobs/<int:pk>/', views.job_detail_view, name='job_detail'),
    path('jobs/<int:pk>/save/', views.toggle_save_job_view, name='toggle_save'),
    
    # Employer
    path('dashboard/', views.employer_dashboard_view, name='employer_dashboard'),
    path('jobs/new/', views.job_create_view, name='job_create'),
    path('jobs/<int:pk>/edit/', views.job_edit_view, name='job_edit'),
    path('jobs/<int:pk>/delete/', views.job_delete_view, name='job_delete'),
    
    # Alerts
    path('alerts/', views.manage_alerts_view, name='manage_alerts'),
    path('alerts/<int:pk>/delete/', views.delete_alert_view, name='delete_alert'),
    
    # Admin Moderation
    path('admin/approvals/', views.admin_jobs_approval_list, name='admin_approval_list'),
    path('admin/approvals/<int:pk>/approve/', views.admin_approve_job, name='admin_approve'),
]
