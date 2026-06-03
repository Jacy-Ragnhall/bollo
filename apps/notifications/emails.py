from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse

def send_application_submitted_email(application):
    """
    Alerts the Job Seeker that their application was successfully received,
    and alerts the Employer that a new candidate has applied.
    """
    # 1. Seeker confirmation
    seeker_subject = f"Application Received: {application.job.title}"
    seeker_message = (
        f"Hi {application.seeker.username},\n\n"
        f"Your application for the position of '{application.job.title}' at "
        f"'{application.job.employer.employer_profile.company_name}' has been successfully submitted!\n"
        f"The employer has been notified and will review your profile.\n\n"
        f"Thank you for using our Job Portal."
    )
    
    # 2. Employer alert
    employer_subject = f"New Applicant: {application.job.title}"
    employer_message = (
        f"Hi {application.job.employer.username},\n\n"
        f"A new candidate ({application.seeker.username}) has applied for your job posting: '{application.job.title}'.\n"
        f"Log in to your dashboard to review their resume and cover letter:\n"
        f"http://localhost:8000/dashboard/\n\n"
        f"Best regards,\nJob Portal Admin"
    )

    try:
        # Seeker
        send_mail(
            subject=seeker_subject,
            message=seeker_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[application.seeker.email],
            fail_silently=True
        )
        # Employer
        send_mail(
            subject=employer_subject,
            message=employer_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[application.job.employer.email],
            fail_silently=True
        )
    except Exception as e:
        print(f"SMTP error during submission emails: {e}")

def send_application_status_email(application):
    """
    Alerts the Job Seeker when the Employer changes their application status.
    """
    subject = f"Application Update: {application.job.title}"
    message = (
        f"Hi {application.seeker.username},\n\n"
        f"The status of your application for '{application.job.title}' has been updated to: "
        f"'{application.get_status_display()}'.\n\n"
        f"Log in to view more details:\n"
        f"http://localhost:8000/users/profile/\n\n"
        f"Best regards,\nJob Portal Team"
    )
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[application.seeker.email],
            fail_silently=True
        )
    except Exception as e:
        print(f"SMTP error during status email: {e}")

def send_job_approved_email(job):
    """
    Alerts the Employer when the Admin approves their job listing to go live.
    """
    subject = f"Job Posting Live: {job.title}"
    message = (
        f"Hi {job.employer.username},\n\n"
        f"Great news! Your job posting '{job.title}' has been approved by the administrator "
        f"and is now officially live on the portal!\n\n"
        f"You can view it here:\n"
        f"http://localhost:8000/jobs/{job.id}/\n\n"
        f"Thank you for listing with us."
    )
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[job.employer.email],
            fail_silently=True
        )
    except Exception as e:
        print(f"SMTP error during approval email: {e}")

def send_job_alert_email(user, matched_jobs):
    """
    Sends email alerts to a user showing a list of recent jobs matching their query.
    """
    subject = f"Job Alert: New Matching Jobs Found!"
    jobs_summary = ""
    for job in matched_jobs:
        jobs_summary += f"- {job.title} at {job.employer.employer_profile.company_name} ({job.location}) - http://localhost:8000/jobs/{job.id}/\n"

    message = (
        f"Hi {user.username},\n\n"
        f"New jobs matching your saved search criteria have been posted in the last 24 hours:\n\n"
        f"{jobs_summary}\n"
        f"Log in to apply for these positions before they close!\n\n"
        f"Best regards,\nJob Portal Alerts"
    )
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=True
        )
    except Exception as e:
        print(f"SMTP error during alert email: {e}")
