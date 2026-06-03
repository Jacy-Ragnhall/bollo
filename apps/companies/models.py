from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.users.models import EmployerProfile

class CompanyReview(models.Model):
    seeker = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='reviews'
    )
    company = models.ForeignKey(
        EmployerProfile, 
        on_delete=models.CASCADE, 
        related_name='reviews'
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 to 5 stars"
    )
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('seeker', 'company')

    def __str__(self):
        return f"{self.seeker.username} rated {self.company.company_name}: {self.rating} stars"
