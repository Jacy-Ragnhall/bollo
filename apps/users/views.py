from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django_otp import login as otp_login, user_has_device
from django_otp.plugins.otp_totp.models import TOTPDevice

from .forms import CustomUserCreationForm, JobSeekerProfileForm, EmployerProfileForm, TOTPVerifyForm
from .models import CustomUser

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Account created successfully. Please login.")
            return redirect('users:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def custom_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Check if 2FA is active
            if TOTPDevice.objects.filter(user=user, confirmed=True).exists():
                # Stash user ID in session
                request.session['pre_2fa_user_id'] = user.id
                return redirect('users:otp_verify')
            else:
                auth_login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'registration/login.html')

def custom_logout(request):
    auth_logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')

@login_required
def profile_view(request):
    user = request.user
    device = TOTPDevice.objects.filter(user=user, confirmed=True).first()
    has_2fa = device is not None

    if user.is_job_seeker:
        profile = getattr(user, 'seeker_profile', None)
        if request.method == 'POST':
            form = JobSeekerProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                messages.success(request, "Profile updated successfully.")
                return redirect('users:profile')
        else:
            form = JobSeekerProfileForm(instance=profile)
    else:
        profile = getattr(user, 'employer_profile', None)
        if request.method == 'POST':
            form = EmployerProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                messages.success(request, "Company profile updated successfully.")
                return redirect('users:profile')
        else:
            form = EmployerProfileForm(instance=profile)

    return render(request, 'registration/profile.html', {
        'form': form,
        'has_2fa': has_2fa,
        'profile': profile
    })

@login_required
def otp_setup_view(request):
    user = request.user
    # Fetch or create an unconfirmed TOTP device
    device = TOTPDevice.objects.filter(user=user, confirmed=False).first()
    if not device:
        # Check if they already have a confirmed device
        if TOTPDevice.objects.filter(user=user, confirmed=True).exists():
            messages.warning(request, "2FA is already set up and active.")
            return redirect('users:profile')
        device = TOTPDevice.objects.create(user=user, name="Default")

    # Generate QR Code endpoint (we use a simple qr-code generator API for elegance)
    # Using device.config_url provides standard OTP provisioning details
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=220x220&margin=10&data={device.config_url}"

    if request.method == 'POST':
        form = TOTPVerifyForm(request.POST)
        if form.is_valid():
            token = form.cleaned_data['token']
            if device.verify_token(token):
                device.confirmed = True
                device.save()
                # Remove any existing confirmed devices to avoid duplicates
                TOTPDevice.objects.filter(user=user, confirmed=True).exclude(id=device.id).delete()
                # Log the OTP session in
                otp_login(request, device)
                messages.success(request, "Two-factor authentication enabled successfully.")
                return redirect('users:profile')
            else:
                messages.error(request, "Invalid verification token. Please try again.")
    else:
        form = TOTPVerifyForm()

    return render(request, 'registration/otp_setup.html', {
        'form': form,
        'qr_url': qr_url,
        'device': device
    })

def otp_verify_view(request):
    user_id = request.session.get('pre_2fa_user_id')
    if not user_id:
        return redirect('users:login')

    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return redirect('users:login')

    device = TOTPDevice.objects.filter(user=user, confirmed=True).first()
    if not device:
        return redirect('users:login')

    if request.method == 'POST':
        form = TOTPVerifyForm(request.POST)
        if form.is_valid():
            token = form.cleaned_data['token']
            if device.verify_token(token):
                # Login the user
                auth_login(request, user)
                otp_login(request, device)
                # Clear pre-auth session state
                del request.session['pre_2fa_user_id']
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('home')
            else:
                messages.error(request, "Invalid 2FA token. Please try again.")
    else:
        form = TOTPVerifyForm()

    return render(request, 'registration/otp_verify.html', {'form': form})

@login_required
def otp_disable_view(request):
    if request.method == 'POST':
        TOTPDevice.objects.filter(user=request.user).delete()
        messages.success(request, "Two-factor authentication has been disabled.")
    return redirect('users:profile')
