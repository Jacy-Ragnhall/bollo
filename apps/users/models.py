from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUser(AbstractUser):
    is_job_seeker = models.BooleanField(default=False)
    is_employer = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class JobSeekerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='seeker_profile')
    phone = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)
    skills = models.TextField(blank=True, help_text="Comma-separated list of skills")
    resume_parsed_name = models.CharField(max_length=255, blank=True)
    resume_parsed_email = models.CharField(max_length=255, blank=True)
    resume_file = models.FileField(upload_to='resumes/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Seeker Profile"

class EmployerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='employer_profile')
    company_name = models.CharField(max_length=255, blank=True)
    company_logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    website = models.URLField(blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.company_name or f"{self.user.username}'s Employer Profile"

# Signals to automatically create profiles upon CustomUser creation
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_job_seeker:
            JobSeekerProfile.objects.create(user=instance)
        elif instance.is_employer:
            EmployerProfile.objects.create(user=instance, company_name=f"{instance.username} Corp")
        else:
            # Fallback (e.g., admin or unselected signup)
            JobSeekerProfile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.is_job_seeker and hasattr(instance, 'seeker_profile'):
        instance.seeker_profile.save()
    elif instance.is_employer and hasattr(instance, 'employer_profile'):
        instance.employer_profile.save()
