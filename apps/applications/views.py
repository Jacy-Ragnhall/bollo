import csv
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, Http404
from django.core.files.base import ContentFile

from .models import Application
from .forms import ApplicationForm, ResumeBuilderForm
from .utils import parse_resume_file, generate_resume_pdf
from apps.jobs.models import Job
from apps.notifications.emails import send_application_submitted_email, send_application_status_email

@login_required
def apply_job_view(request, job_id):
    if not request.user.is_job_seeker:
        messages.error(request, "Only job seekers can apply for jobs.")
        return redirect('home')

    job = get_object_or_404(Job, pk=job_id, is_paid=True, is_approved=True)

    # Check for existing application
    if Application.objects.filter(job=job, seeker=request.user).exists():
        messages.warning(request, "You have already applied for this job.")
        return redirect('jobs:job_detail', pk=job.id)

    seeker_profile = getattr(request.user, 'seeker_profile', None)
    has_profile_resume = bool(seeker_profile and seeker_profile.resume_file)

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES, has_profile_resume=has_profile_resume)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.seeker = request.user

            # If user checked 'Use profile resume' and has one
            if form.cleaned_data.get('use_profile_resume') and has_profile_resume:
                application.resume = seeker_profile.resume_file
            else:
                # User uploaded a new resume
                uploaded_resume = request.FILES.get('resume')
                if uploaded_resume:
                    application.resume = uploaded_resume
                    # Run Parser and update Profile
                    parsed_name, parsed_email = parse_resume_file(uploaded_resume)
                    if seeker_profile:
                        if parsed_name:
                            seeker_profile.resume_parsed_name = parsed_name
                        if parsed_email:
                            seeker_profile.resume_parsed_email = parsed_email
                        # Also save this resume as their default profile resume
                        seeker_profile.resume_file = uploaded_resume
                        seeker_profile.save()
            
            application.save()
            messages.success(request, f"Successfully applied for {job.title}!")
            
            # Send Notification Emails
            send_application_submitted_email(application)
            
            return redirect('users:profile')
    else:
        form = ApplicationForm(has_profile_resume=has_profile_resume)

    return render(request, 'applications/apply.html', {
        'form': form,
        'job': job,
        'has_profile_resume': has_profile_resume,
        'seeker_profile': seeker_profile
    })

@login_required
def applicants_list_view(request, job_id):
    job = get_object_or_404(Job, pk=job_id, employer=request.user)
    applicants = Application.objects.filter(job=job).select_related('seeker__seeker_profile')
    return render(request, 'applications/applicants_list.html', {
        'job': job,
        'applicants': applicants,
        'status_choices': Application.STATUS_CHOICES
    })

@login_required
def change_status_view(request, pk):
    application = get_object_or_404(Application, pk=pk)
    # Verify ownership
    if application.job.employer != request.user:
        messages.error(request, "Unauthorized access.")
        return redirect('home')

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Application.STATUS_CHOICES):
            application.status = new_status
            application.save()
            messages.success(request, f"Application status updated to '{application.get_status_display()}'.")
            
            # Send Notification Email
            send_application_status_email(application)
            
    return redirect('applications:applicants_list', job_id=application.job.id)

@login_required
def export_applicants_csv_view(request, job_id):
    job = get_object_or_404(Job, pk=job_id, employer=request.user)
    applications = Application.objects.filter(job=job).select_related('seeker')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="applicants_{job_id}.csv"'

    writer = csv.writer(response)
    writer.writerow(['Applicant Username', 'Applicant Email', 'Applied Date', 'Status', 'Cover Letter'])

    for app in applications:
        writer.writerow([
            app.seeker.username, 
            app.seeker.email, 
            app.created_at.strftime('%Y-%m-%d %H:%M:%S'), 
            app.get_status_display(), 
            app.cover_letter
        ])

    return response

@login_required
def resume_builder_view(request):
    if not request.user.is_job_seeker:
        messages.error(request, "Only job seekers can use the resume builder.")
        return redirect('home')

    if request.method == 'POST':
        form = ResumeBuilderForm(request.POST)
        if form.is_valid():
            # Generate the PDF document in memory
            pdf_buffer = generate_resume_pdf(form.cleaned_data)
            
            # Save generated resume to seeker's profile
            seeker_profile = getattr(request.user, 'seeker_profile', None)
            if seeker_profile:
                # Wrap the pdf stream in standard Django ContentFile
                pdf_file = ContentFile(pdf_buffer.getvalue(), name=f"resume_{request.user.username}.pdf")
                seeker_profile.resume_file = pdf_file
                seeker_profile.resume_parsed_name = form.cleaned_data['full_name']
                seeker_profile.resume_parsed_email = form.cleaned_data['email']
                seeker_profile.save()
                
            messages.success(request, "Resume generated successfully and saved to your profile!")
            
            # Send PDF as downloadable file response
            response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="resume_{request.user.username}.pdf"'
            return response
    else:
        # Pre-fill form from profile data if available
        seeker_profile = getattr(request.user, 'seeker_profile', None)
        initial_data = {
            'email': request.user.email,
            'full_name': request.user.get_full_name() or request.user.username,
            'phone': seeker_profile.phone if seeker_profile else '',
            'summary': seeker_profile.bio if seeker_profile else '',
        }
        form = ResumeBuilderForm(initial=initial_data)

    return render(request, 'applications/resume_builder.html', {'form': form})
