from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.jobs.views import home_view

urlpatterns = [
    path('', home_view, name='home'),
    
    # Custom apps must be registered before the admin site so their prefixes
    # like /admin/approvals/ are not swallowed by Django admin's catch-all.
    path('', include('apps.jobs.urls')),
    path('admin/', admin.site.urls),
    
    # Social auth / django-allauth
    path('accounts/', include('allauth.urls')),
    
    # Custom apps
    path('users/', include('apps.users.urls')),
    path('applications/', include('apps.applications.urls')),
    path('companies/', include('apps.companies.urls')),
    path('payments/', include('apps.payments.urls')),
    path('analytics/', include('apps.analytics.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
