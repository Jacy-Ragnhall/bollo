from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from django.db.models.functions import TruncDay

from .models import JobViewLog
from apps.jobs.models import Job
from apps.applications.models import Application

@login_required
def job_analytics_view(request, job_id):
    if not request.user.is_employer:
        messages.error(request, "Access restricted to employers.")
        return redirect('home')

    job = get_object_or_404(Job, pk=job_id, employer=request.user)

    # General KPIs
    total_views = JobViewLog.objects.filter(job=job).count()
    total_apps = Application.objects.filter(job=job).count()

    # Time series tracking (last 7 days)
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=6)
    
    dates_list = [start_date + timedelta(days=i) for i in range(7)]
    date_labels = [d.strftime('%b %d') for d in dates_list]

    # Query views per day
    views_per_day = JobViewLog.objects.filter(
        job=job,
        viewed_at__date__range=[start_date, end_date]
    ).extra(select={'day': "date(viewed_at)"}).values('day').annotate(cnt=Count('id')).order_by('day')

    # Query applications per day
    apps_per_day = Application.objects.filter(
        job=job,
        created_at__date__range=[start_date, end_date]
    ).extra(select={'day': "date(created_at)"}).values('day').annotate(cnt=Count('id')).order_by('day')

    # Build default dictionaries with zero values
    # SQLite returns date strings 'YYYY-MM-DD' for date(viewed_at)
    views_map = {}
    for entry in views_per_day:
        day_str = entry['day']
        # SQLite raw format conversion if needed
        views_map[str(day_str)] = entry['cnt']

    apps_map = {}
    for entry in apps_per_day:
        day_str = entry['day']
        apps_map[str(day_str)] = entry['cnt']

    # Map zero values to missing dates
    views_chart_data = []
    apps_chart_data = []
    for d in dates_list:
        d_str = d.strftime('%Y-%m-%d')
        views_chart_data.append(views_map.get(d_str, 0))
        apps_chart_data.append(apps_map.get(d_str, 0))

    return render(request, 'analytics/job_analytics.html', {
        'job': job,
        'total_views': total_views,
        'total_apps': total_apps,
        'date_labels': date_labels,
        'views_chart_data': views_chart_data,
        'apps_chart_data': apps_chart_data
    })
