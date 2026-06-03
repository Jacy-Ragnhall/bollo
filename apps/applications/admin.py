from django.contrib import admin
from .models import Application

class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['job', 'seeker', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['job__title', 'seeker__username']

admin.site.register(Application, ApplicationAdmin)
