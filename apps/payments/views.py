import uuid
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings

from .models import JobPayment
from apps.jobs.models import Job

@login_required
def checkout_view(request, job_id):
    if not request.user.is_employer:
        messages.error(request, "Access restricted to employers.")
        return redirect('home')

    job = get_object_or_404(Job, pk=job_id, employer=request.user)

    if job.is_paid:
        messages.warning(request, "This job has already been paid for.")
        return redirect('jobs:employer_dashboard')

    # Price for job posting
    price = 99.00

    if request.method == 'POST':
        card_number = request.POST.get('card_number', '').replace(' ', '')
        expiry = request.POST.get('expiry', '')
        cvc = request.POST.get('cvc', '')

        # Dummy verification flow (simulating payment processor response)
        # Using 4242-pattern test card is the standard Stripe mock testing protocol
        if len(card_number) == 16 and card_number.startswith('4242') and len(cvc) == 3:
            # Payment success!
            payment = JobPayment.objects.create(
                job=job,
                amount=price,
                transaction_id=f"ch_{uuid.uuid4().hex[:16]}",
                status='PAID'
            )
            
            job.is_paid = True
            job.save()

            messages.success(request, "Payment successful! Your job has been submitted to administrator for approval.")
            return redirect('payments:payment_success', pk=payment.id)
        else:
            # Payment failed!
            JobPayment.objects.create(
                job=job,
                amount=price,
                transaction_id=f"failed_{uuid.uuid4().hex[:8]}",
                status='FAIL'
            )
            messages.error(request, "Payment failed. Please verify card parameters (use Stripe test card: 4242 4242 4242 4242).")

    return render(request, 'payments/checkout.html', {
        'job': job,
        'price': price,
        'test_mode': getattr(settings, 'PAYMENT_TEST_MODE', True)
    })

@login_required
def payment_success_view(request, pk):
    payment = get_object_or_404(JobPayment, pk=pk, job__employer=request.user)
    return render(request, 'payments/success.html', {'payment': payment})
