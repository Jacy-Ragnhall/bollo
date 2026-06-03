from django import forms
from .models import CompanyReview

class CompanyReviewForm(forms.ModelForm):
    class Meta:
        model = CompanyReview
        fields = ['rating', 'review_text']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, str(i)) for i in range(5, 0, -1)]), # Rendered custom via stars-css
            'review_text': forms.Textarea(attrs={
                'class': 'form-control form-control-custom', 
                'rows': 4, 
                'placeholder': 'Share your experience working with or interviewing at this company...'
            }),
        }
