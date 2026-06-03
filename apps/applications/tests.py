import io
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from apps.users.models import CustomUser
from apps.jobs.models import Category, Job
from .models import Application
from .utils import parse_resume_file, generate_resume_pdf

class ApplicationsTestCase(TestCase):
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
        self.cat = Category.objects.create(name='Design', slug='design')
        self.job = Job.objects.create(
            employer=self.employer,
            title='UI Designer',
            category=self.cat,
            location='London'
        )

    def test_application_submission(self):
        resume_data = b"Resume: Jane Doe, Email: jane.doe@example.com"
        uploaded_resume = SimpleUploadedFile("resume.txt", resume_data, content_type="text/plain")

        app = Application.objects.create(
            job=self.job,
            seeker=self.seeker,
            resume=uploaded_resume,
            cover_letter="I love design...",
            status='AP'
        )

        self.assertEqual(Application.objects.filter(job=self.job).count(), 1)
        self.assertEqual(app.get_status_display(), "Applied")

    def test_resume_parser_utility(self):
        resume_data = b"My name is John Smith and my email address is john.smith@example.com."
        resume_file = io.BytesIO(resume_data)
        
        parsed_name, parsed_email = parse_resume_file(resume_file)
        self.assertEqual(parsed_email, "john.smith@example.com")
        self.assertEqual(parsed_name, "John Smith")

    def test_resume_pdf_generation(self):
        data = {
            'full_name': 'Test User',
            'email': 'test@example.com',
            'phone': '1234567890',
            'summary': 'Summary statement...',
            'experience': 'Company Inc (2020-2026)',
            'education': 'University of Tech (B.S.)',
            'skills': 'Python, Django'
        }
        pdf_buffer = generate_resume_pdf(data)
        self.assertGreater(len(pdf_buffer.getvalue()), 1000)
