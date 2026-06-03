from django.test import TestCase
from apps.users.models import CustomUser
from .models import Category, Job, SavedJob, JobAlert

class JobsTestCase(TestCase):
    def setUp(self):
        self.employer = CustomUser.objects.create_user(
            username='employer_test',
            email='employer@example.com',
            password='testpassword123',
            is_employer=True
        )
        self.seeker = CustomUser.objects.create_user(
            username='seeker_test',
            email='seeker@example.com',
            password='testpassword123',
            is_job_seeker=True
        )
        self.category = Category.objects.create(name='Technology', slug='technology')

    def test_job_workflow(self):
        job = Job.objects.create(
            employer=self.employer,
            title='Software Engineer',
            category=self.category,
            job_type='FT',
            location='Remote',
            description='We are hiring...',
            salary_min=100000.00,
            salary_max=120000.00
        )
        
        # Initially not live
        self.assertFalse(job.is_live)
        
        # Mark as paid
        job.is_paid = True
        job.save()
        self.assertFalse(job.is_live)

        # Mark as approved
        job.is_approved = True
        job.save()
        self.assertTrue(job.is_live)

    def test_saved_job_toggle(self):
        job = Job.objects.create(
            employer=self.employer,
            title='Data Analyst',
            category=self.category,
            location='Hybrid'
        )
        saved = SavedJob.objects.create(user=self.seeker, job=job)
        self.assertEqual(SavedJob.objects.filter(user=self.seeker).count(), 1)
        self.assertEqual(saved.job.title, "Data Analyst")
