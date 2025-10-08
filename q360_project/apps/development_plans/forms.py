"""
Forms for development plans app.
"""
from django import forms
from .models import DevelopmentGoal, ProgressLog


class DevelopmentGoalForm(forms.ModelForm):
    """Form for creating/editing development goals."""

    class Meta:
        model = DevelopmentGoal
        fields = ['title', 'description', 'category', 'target_date', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'target_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }


class ProgressLogForm(forms.ModelForm):
    """Form for logging progress."""

    class Meta:
        model = ProgressLog
        fields = ['note', 'progress_percentage']
        widgets = {
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'progress_percentage': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 100
            }),
        }
