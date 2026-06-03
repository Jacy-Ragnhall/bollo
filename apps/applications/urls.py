from django.urls import path
from . import views

app_name = 'applications'

urlpatterns = [
    path('apply/<int:job_id>/', views.apply_job_view, name='apply'),
    path('job/<int:job_id>/applicants/', views.applicants_list_view, name='applicants_list'),
    path('status/<int:pk>/change/', views.change_status_view, name='change_status'),
    path('job/<int:job_id>/export/', views.export_applicants_csv_view, name='export_csv'),
    path('resume-builder/', views.resume_builder_view, name='resume_builder'),
]
