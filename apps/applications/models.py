from django.db import models
from django.conf import settings
from apps.jobs.models import Job

class Application(models.Model):
    STATUS_CHOICES = (
        ('AP', 'Applied'),
        ('UR', 'Under Review'),
        ('IV', 'Interviewing'),
        ('OF', 'Offered'),
        ('RJ', 'Rejected'),
    )

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    seeker = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='applications'
    )
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField(blank=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='AP')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('job', 'seeker')

    def __str__(self):
        return f"{self.seeker.username} -> {self.job.title}"

    @property
    def get_status_class(self):
        mapping = {
            'AP': 'bg-secondary',
            'UR': 'bg-warning text-dark',
            'IV': 'bg-primary',
            'OF': 'bg-success',
            'RJ': 'bg-danger'
        }
        return mapping.get(self.status, 'bg-secondary')
