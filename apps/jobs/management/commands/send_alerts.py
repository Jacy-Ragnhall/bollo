from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from apps.jobs.models import Job, JobAlert
from apps.notifications.emails import send_job_alert_email

class Command(BaseCommand):
    help = 'Send daily email alerts to users for new matching jobs'

    def handle(self, *args, **options):
        # We look for jobs approved/paid in the last 24 hours
        yesterday = timezone.now() - timedelta(days=1)
        recent_jobs = Job.objects.filter(is_paid=True, is_approved=True, created_at__gte=yesterday)

        if not recent_jobs.exists():
            self.stdout.write(self.style.WARNING("No new jobs in the last 24 hours. No alerts sent."))
            return

        active_alerts = JobAlert.objects.filter(is_active=True).select_related('user')
        alerts_sent = 0

        for alert in active_alerts:
            matched_jobs = recent_jobs
            
            if alert.category:
                matched_jobs = matched_jobs.filter(category=alert.category)
            
            if alert.location:
                matched_jobs = matched_jobs.filter(location__icontains=alert.location)
                
            if alert.keywords:
                matched_jobs = matched_jobs.filter(
                    Q(title__icontains=alert.keywords) | Q(description__icontains=alert.keywords)
                )

            if matched_jobs.exists():
                send_job_alert_email(alert.user, list(matched_jobs))
                alerts_sent += 1

        self.stdout.write(self.style.SUCCESS(f"Successfully processed alerts. Sent {alerts_sent} emails."))
