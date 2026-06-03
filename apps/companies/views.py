from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.users.models import EmployerProfile
from apps.jobs.models import Job
from .models import CompanyReview
from .forms import CompanyReviewForm

def company_list_view(request):
    companies = EmployerProfile.objects.exclude(company_name="")
    return render(request, 'companies/company_list.html', {
        'companies': companies
    })

def company_detail_view(request, pk):
    company = get_object_or_404(EmployerProfile, pk=pk)
    
    # Live jobs posted by this company
    jobs = Job.objects.filter(employer=company.user, is_paid=True, is_approved=True)
    
    # Reviews
    reviews = CompanyReview.objects.filter(company=company).select_related('seeker')
    
    # Calculated average
    ratings = [r.rating for r in reviews]
    avg_rating = sum(ratings) / len(ratings) if ratings else 0

    # User review check
    user_has_reviewed = False
    review_form = None
    if request.user.is_authenticated and request.user.is_job_seeker:
        user_has_reviewed = CompanyReview.objects.filter(seeker=request.user, company=company).exists()
        if not user_has_reviewed:
            review_form = CompanyReviewForm()

    return render(request, 'companies/company_detail.html', {
        'company': company,
        'jobs': jobs,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'user_has_reviewed': user_has_reviewed,
        'review_form': review_form
    })

@login_required
def submit_review_view(request, pk):
    if not request.user.is_job_seeker:
        messages.error(request, "Only job seekers can review companies.")
        return redirect('home')

    company = get_object_or_404(EmployerProfile, pk=pk)
    
    # Check duplicate
    if CompanyReview.objects.filter(seeker=request.user, company=company).exists():
        messages.warning(request, "You have already reviewed this company.")
        return redirect('companies:company_detail', pk=company.id)

    if request.method == 'POST':
        form = CompanyReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.seeker = request.user
            review.company = company
            review.save()
            messages.success(request, "Your review has been published successfully.")
            
    return redirect('companies:company_detail', pk=company.id)
