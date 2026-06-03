from django.contrib import admin
from .models import CompanyReview

class CompanyReviewAdmin(admin.ModelAdmin):
    list_display = ['company', 'seeker', 'rating', 'created_at']
    list_filter = ['rating']
    search_fields = ['company__company_name', 'seeker__username']

admin.site.register(CompanyReview, CompanyReviewAdmin)
