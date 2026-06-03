from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, JobSeekerProfile, EmployerProfile

class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = (
        ('seeker', 'Job Seeker'),
        ('employer', 'Employer'),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect, required=True, label="Select Your Role")

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email')

    def save(self, commit=True):
        user = super().save(commit=False)
        role = self.cleaned_data.get('role')
        if role == 'seeker':
            user.is_job_seeker = True
        elif role == 'employer':
            user.is_employer = True
        if commit:
            user.save()
        return user

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')

class JobSeekerProfileForm(forms.ModelForm):
    class Meta:
        model = JobSeekerProfile
        fields = ['phone', 'bio', 'skills', 'resume_file']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control form-control-custom'}),
            'bio': forms.Textarea(attrs={'class': 'form-control form-control-custom', 'rows': 4}),
            'skills': forms.TextInput(attrs={'class': 'form-control form-control-custom', 'placeholder': 'e.g. Python, Django, HTML, CSS'}),
            'resume_file': forms.ClearableFileInput(attrs={'class': 'form-control form-control-custom'}),
        }

class EmployerProfileForm(forms.ModelForm):
    class Meta:
        model = EmployerProfile
        fields = ['company_name', 'company_logo', 'website', 'description']
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control form-control-custom'}),
            'company_logo': forms.ClearableFileInput(attrs={'class': 'form-control form-control-custom'}),
            'website': forms.URLInput(attrs={'class': 'form-control form-control-custom'}),
            'description': forms.Textarea(attrs={'class': 'form-control form-control-custom', 'rows': 4}),
        }

class TOTPVerifyForm(forms.Form):
    token = forms.CharField(
        max_length=6,
        min_length=6,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-custom text-center fs-2 letter-spacing-lg',
            'placeholder': '000000',
            'autocomplete': 'off',
            'autofocus': 'on'
        })
    )
