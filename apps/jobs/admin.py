from django.contrib import admin
from .models import Category, Job, SavedJob, JobAlert

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'slug']

class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'employer', 'category', 'job_type', 'location', 'is_paid', 'is_approved', 'created_at']
    list_filter = ['is_paid', 'is_approved', 'job_type', 'category']
    search_fields = ['title', 'description', 'location']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(SavedJob)
admin.site.register(JobAlert)
