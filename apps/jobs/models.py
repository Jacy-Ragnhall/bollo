from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

class Job(models.Model):
    JOB_TYPE_CHOICES = (
        ('FT', 'Full-Time'),
        ('PT', 'Part-Time'),
        ('RM', 'Remote'),
        ('IN', 'Internship'),
    )

    employer = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='posted_jobs'
    )
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='jobs')
    job_type = models.CharField(max_length=2, choices=JOB_TYPE_CHOICES, default='FT')
    location = models.CharField(max_length=150)
    description = models.TextField()
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    # Workflow states
    is_paid = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def is_live(self):
        return self.is_paid and self.is_approved

class SavedJob(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_jobs')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='saved_by_users')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'job')

    def __str__(self):
        return f"{self.user.username} saved {self.job.title}"

class JobAlert(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='job_alerts')
    keywords = models.CharField(max_length=255, blank=True, help_text="Alert matches job title or description keywords")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    location = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        parts = []
        if self.keywords:
            parts.append(f"Keywords: '{self.keywords}'")
        if self.category:
            parts.append(f"Category: {self.category.name}")
        if self.location:
            parts.append(f"Location: {self.location}")
        return f"Alert for {self.user.username} ({', '.join(parts) or 'All jobs'})"
