from django import forms
from .models import Job, JobAlert

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'category', 'job_type', 'location', 'description', 'salary_min', 'salary_max']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control form-control-custom', 'placeholder': 'e.g. Senior Software Engineer'}),
            'category': forms.Select(attrs={'class': 'form-select form-control-custom'}),
            'job_type': forms.Select(attrs={'class': 'form-select form-control-custom'}),
            'location': forms.TextInput(attrs={'class': 'form-control form-control-custom', 'placeholder': 'e.g. Remote, San Francisco, CA'}),
            'description': forms.Textarea(attrs={'class': 'form-control form-control-custom', 'rows': 6, 'placeholder': 'Job description and requirements...'}),
            'salary_min': forms.NumberInput(attrs={'class': 'form-control form-control-custom', 'placeholder': 'Min salary'}),
            'salary_max': forms.NumberInput(attrs={'class': 'form-control form-control-custom', 'placeholder': 'Max salary'}),
        }

class JobAlertForm(forms.ModelForm):
    class Meta:
        model = JobAlert
        fields = ['keywords', 'category', 'location']
        widgets = {
            'keywords': forms.TextInput(attrs={'class': 'form-control form-control-custom', 'placeholder': 'e.g. Django, Python'}),
            'category': forms.Select(attrs={'class': 'form-select form-control-custom'}),
            'location': forms.TextInput(attrs={'class': 'form-control form-control-custom', 'placeholder': 'e.g. Remote'}),
        }
