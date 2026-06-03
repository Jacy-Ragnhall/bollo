from django.db import models
from apps.jobs.models import Job

class JobViewLog(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='view_logs')
    viewed_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    session_key = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        ordering = ['-viewed_at']

    def __str__(self):
        return f"View of {self.job.title} at {self.viewed_at}"
