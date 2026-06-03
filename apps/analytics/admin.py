from django.contrib import admin
from .models import JobViewLog

class JobViewLogAdmin(admin.ModelAdmin):
    list_display = ['job', 'ip_address', 'viewed_at']
    search_fields = ['job__title', 'ip_address']

admin.site.register(JobViewLog, JobViewLogAdmin)
