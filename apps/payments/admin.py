from django.contrib import admin
from .models import JobPayment

class JobPaymentAdmin(admin.ModelAdmin):
    list_display = ['job', 'amount', 'status', 'transaction_id', 'created_at']
    list_filter = ['status']
    search_fields = ['job__title', 'transaction_id']

admin.site.register(JobPayment, JobPaymentAdmin)
