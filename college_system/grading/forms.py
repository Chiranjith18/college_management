from django import forms
from .models import Grade

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['marks', 'feedback']
        widgets = {
            'marks': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter marks'}),
            'feedback': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter feedback'}),
        }
