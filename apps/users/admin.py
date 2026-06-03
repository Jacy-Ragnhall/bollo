from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, JobSeekerProfile, EmployerProfile

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'is_job_seeker', 'is_employer', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Roles', {'fields': ('is_job_seeker', 'is_employer')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Roles', {'fields': ('is_job_seeker', 'is_employer')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(JobSeekerProfile)
admin.site.register(EmployerProfile)
