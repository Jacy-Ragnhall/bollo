from django import forms
from .models import Application

class ApplicationForm(forms.ModelForm):
    use_profile_resume = forms.BooleanField(
        required=False, 
        initial=True, 
        label="Use resume from my profile profile",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = Application
        fields = ['resume', 'cover_letter']
        widgets = {
            'resume': forms.ClearableFileInput(attrs={'class': 'form-control form-control-custom'}),
            'cover_letter': forms.Textarea(attrs={'class': 'form-control form-control-custom', 'rows': 5, 'placeholder': 'Introduce yourself and pitch why you are the perfect fit for this job...'}),
        }

    def __init__(self, *args, **kwargs):
        has_profile_resume = kwargs.pop('has_profile_resume', False)
        super().__init__(*args, **kwargs)
        if not has_profile_resume:
            self.fields['use_profile_resume'].widget = forms.HiddenInput()
            self.fields['use_profile_resume'].initial = False
            self.fields['resume'].required = True
        else:
            self.fields['resume'].required = False

class ResumeBuilderForm(forms.Form):
    full_name = forms.CharField(
        max_length=150, 
        widget=forms.TextInput(attrs={'class': 'form-control form-control-custom', 'placeholder': 'John Doe'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control form-control-custom', 'placeholder': 'john.doe@example.com'})
    )
    phone = forms.CharField(
        max_length=20, 
        widget=forms.TextInput(attrs={'class': 'form-control form-control-custom', 'placeholder': '+1 (555) 123-4567'})
    )
    summary = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control form-control-custom', 'rows': 4, 'placeholder': 'Write a brief professional summary...'})
    )
    education = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control form-control-custom', 'rows': 4, 'placeholder': 'e.g. B.S. in Computer Science - Stanford University (2020-2024)'})
    )
    experience = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control form-control-custom', 'rows': 5, 'placeholder': 'e.g. Software Engineer Intern - Tech Corp (2023-Present)\n- Built Django microservices\n- Optimized database queries'})
    )
    skills = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control form-control-custom', 'placeholder': 'e.g. Python, Django, PostgreSQL, HTML, CSS, Git'})
    )
