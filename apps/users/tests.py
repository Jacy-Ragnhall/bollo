from django.test import TestCase
from .models import CustomUser, JobSeekerProfile, EmployerProfile
from django_otp.plugins.otp_totp.models import TOTPDevice

class UsersTestCase(TestCase):
    def setUp(self):
        self.seeker = CustomUser.objects.create_user(
            username='seeker_test',
            email='seeker@example.com',
            password='testpassword123',
            is_job_seeker=True
        )
        self.employer = CustomUser.objects.create_user(
            username='employer_test',
            email='employer@example.com',
            password='testpassword123',
            is_employer=True
        )

    def test_profile_creation_signals(self):
        # Verify job seeker profile is automatically provisioned
        self.assertTrue(JobSeekerProfile.objects.filter(user=self.seeker).exists())
        # Verify employer profile is automatically provisioned
        self.assertTrue(EmployerProfile.objects.filter(user=self.employer).exists())
        self.assertEqual(self.employer.employer_profile.company_name, "employer_test Corp")

    def test_otp_2fa_setup(self):
        # Create unconfirmed TOTP device
        device = TOTPDevice.objects.create(user=self.seeker, name="Default", confirmed=False)
        self.assertFalse(device.confirmed)
        self.assertEqual(TOTPDevice.objects.filter(user=self.seeker).count(), 1)
