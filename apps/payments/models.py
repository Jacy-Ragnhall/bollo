from django.db import models
from apps.jobs.models import Job

class JobPayment(models.Model):
    STATUS_CHOICES = (
        ('PND', 'Pending'),
        ('PAID', 'Paid'),
        ('FAIL', 'Failed'),
    )

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=5000.00) # Standard pricing e.g. $5,000 per post
    transaction_id = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=4, choices=STATUS_CHOICES, default='PND')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for {self.job.title} - Status: {self.get_status_display()}"
