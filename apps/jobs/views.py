from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required

from .models import Job, Category, SavedJob, JobAlert
from .forms import JobForm, JobAlertForm
from apps.companies.models import CompanyReview

def home_view(request):
    categories = Category.objects.all()
    # Featured jobs: Live jobs (Paid + Approved)
    recent_jobs = Job.objects.filter(is_paid=True, is_approved=True).select_related('employer', 'category')[:6]
    return render(request, 'jobs/home.html', {
        'categories': categories,
        'recent_jobs': recent_jobs
    })

def job_list_view(request):
    jobs = Job.objects.filter(is_paid=True, is_approved=True).select_related('employer', 'category')
    categories = Category.objects.all()

    # Search query
    q = request.GET.get('q', '')
    if q:
        jobs = jobs.filter(Q(title__icontains=q) | Q(description__icontains=q))

    # Filters
    location = request.GET.get('location', '')
    if location:
        jobs = jobs.filter(location__icontains=location)

    category_id = request.GET.get('category', '')
    if category_id:
        jobs = jobs.filter(category_id=category_id)

    job_type = request.GET.get('job_type', '')
    if job_type:
        jobs = jobs.filter(job_type=job_type)

    min_salary = request.GET.get('min_salary', '')
    if min_salary:
        try:
            jobs = jobs.filter(salary_max__gte=float(min_salary))
        except ValueError:
            pass

    return render(request, 'jobs/job_list.html', {
        'jobs': jobs,
        'categories': categories,
        'params': request.GET
    })

def job_detail_view(request, pk):
    # If the user is the employer, they can view even if unapproved/unpaid
    job = get_object_or_404(Job, pk=pk)
    if not job.is_live and job.employer != request.user and not request.user.is_superuser:
        messages.error(request, "This job posting is not active.")
        return redirect('home')

    # Get reviews of the company
    reviews = []
    avg_rating = 0
    if job.employer.is_employer and hasattr(job.employer, 'employer_profile'):
        reviews = CompanyReview.objects.filter(company=job.employer.employer_profile).select_related('seeker')
        ratings = [r.rating for r in reviews]
        if ratings:
            avg_rating = sum(ratings) / len(ratings)

    is_saved = False
    if request.user.is_authenticated:
        is_saved = SavedJob.objects.filter(user=request.user, job=job).exists()

    return render(request, 'jobs/job_detail.html', {
        'job': job,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'is_saved': is_saved
    })

@login_required
def employer_dashboard_view(request):
    if not request.user.is_employer:
        messages.error(request, "Access restricted to employers.")
        return redirect('home')

    # Fetch jobs posted by employer
    jobs = Job.objects.filter(employer=request.user).select_related('category')
    return render(request, 'jobs/employer_dashboard.html', {
        'jobs': jobs
    })

@login_required
def job_create_view(request):
    if not request.user.is_employer:
        messages.error(request, "Access restricted to employers.")
        return redirect('home')

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user
            job.save()
            messages.success(request, "Job created successfully. Please proceed to payment to post it live.")
            return redirect('payments:checkout', job_id=job.id)
    else:
        form = JobForm()
    return render(request, 'jobs/job_form.html', {'form': form, 'action': 'Create'})

@login_required
def job_edit_view(request, pk):
    job = get_object_or_404(Job, pk=pk, employer=request.user)
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, "Job updated successfully.")
            return redirect('jobs:employer_dashboard')
    else:
        form = JobForm(instance=job)
    return render(request, 'jobs/job_form.html', {'form': form, 'action': 'Edit', 'job': job})

@login_required
def job_delete_view(request, pk):
    job = get_object_or_404(Job, pk=pk, employer=request.user)
    if request.method == 'POST':
        job.delete()
        messages.success(request, "Job deleted successfully.")
    return redirect('jobs:employer_dashboard')

@login_required
def toggle_save_job_view(request, pk):
    job = get_object_or_404(Job, pk=pk)
    saved_job, created = SavedJob.objects.get_or_create(user=request.user, job=job)
    if not created:
        saved_job.delete()
        messages.info(request, "Job removed from saved list.")
    else:
        messages.success(request, "Job saved successfully.")
    return redirect('jobs:job_detail', pk=pk)

@login_required
def manage_alerts_view(request):
    alerts = JobAlert.objects.filter(user=request.user).select_related('category')
    if request.method == 'POST':
        form = JobAlertForm(request.POST)
        if form.is_valid():
            alert = form.save(commit=False)
            alert.user = request.user
            alert.save()
            messages.success(request, "Job alert created successfully.")
            return redirect('jobs:manage_alerts')
    else:
        form = JobAlertForm()

    return render(request, 'jobs/manage_alerts.html', {
        'alerts': alerts,
        'form': form
    })

@login_required
def delete_alert_view(request, pk):
    alert = get_object_or_404(JobAlert, pk=pk, user=request.user)
    if request.method == 'POST':
        alert.delete()
        messages.success(request, "Job alert deleted.")
    return redirect('jobs:manage_alerts')

@staff_member_required
def admin_jobs_approval_list(request):
    pending_jobs = Job.objects.filter(is_paid=True, is_approved=False).select_related('employer', 'category')
    return render(request, 'jobs/admin_approval_list.html', {
        'pending_jobs': pending_jobs
    })

@staff_member_required
def admin_approve_job(request, pk):
    job = get_object_or_404(Job, pk=pk, is_paid=True)
    if request.method == 'POST':
        job.is_approved = True
        job.save()
        messages.success(request, f"Job '{job.title}' approved successfully.")
        
        # Import notification helper here to avoid circular imports
        from apps.notifications.emails import send_job_approved_email
        send_job_approved_email(job)
        
    return redirect('jobs:admin_approval_list')
