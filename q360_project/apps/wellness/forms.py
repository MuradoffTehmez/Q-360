"""
Forms for Wellness & Well-Being module.
"""
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import (
    HealthCheckup,
    MentalHealthSurvey,
    MedicalClaim,
    FitnessProgram
)


class HealthCheckupForm(forms.ModelForm):
    """Tibbi müayinə planlaşdırma forması."""

    class Meta:
        model = HealthCheckup
        fields = [
            'checkup_type',
            'scheduled_date',
            'provider',
            'location',
            'notes'
        ]
        widgets = {
            'checkup_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'scheduled_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'provider': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Tibbi Xidmət Təminatçısı')
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Yer')
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': _('Əlavə qeydlər')
            }),
        }


class MentalHealthSurveyForm(forms.ModelForm):
    """Mental sağlamlıq survey forması."""

    class Meta:
        model = MentalHealthSurvey
        fields = [
            'stress_level',
            'workload_satisfaction',
            'work_life_balance',
            'sleep_quality',
            'anxiety_level',
            'seeking_support',
            'comments',
            'is_anonymous'
        ]
        widgets = {
            'stress_level': forms.RadioSelect(attrs={
                'class': 'form-check-input'
            }),
            'workload_satisfaction': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 5
            }),
            'work_life_balance': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 5
            }),
            'sleep_quality': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 5
            }),
            'anxiety_level': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 5
            }),
            'seeking_support': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'comments': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': _('Şərhlər (istəyə bağlı)')
            }),
            'is_anonymous': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Stress level üçün özel radio button layout
        self.fields['stress_level'].widget.choices = [
            (1, _('Çox Aşağı')),
            (2, _('Aşağı')),
            (3, _('Orta')),
            (4, _('Yüksək')),
            (5, _('Çox Yüksək')),
        ]


class MedicalClaimForm(forms.ModelForm):
    """Tibbi xərc tələbi forması."""

    class Meta:
        model = MedicalClaim
        fields = [
            'claim_type',
            'treatment_date',
            'provider',
            'description',
            'amount_claimed',
            'receipt_file',
            'notes'
        ]
        widgets = {
            'claim_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'treatment_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'provider': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Tibbi Xidmət Təminatçısı')
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': _('Müalicə təsviri')
            }),
            'amount_claimed': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': _('Məbləğ')
            }),
            'receipt_file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.jpg,.jpeg,.png'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': _('Əlavə qeydlər')
            }),
        }

    def clean_amount_claimed(self):
        """Məbləğin müsbət olduğunu yoxla."""
        amount = self.cleaned_data.get('amount_claimed')
        if amount and amount <= 0:
            raise forms.ValidationError(_('Məbləğ müsbət olmalıdır.'))
        return amount


class FitnessProgramEnrollForm(forms.Form):
    """Fitness proqramına qoşulma forması."""

    confirm = forms.BooleanField(
        required=True,
        label=_('Bu proqrama qoşulmaq istədiyimi təsdiq edirəm'),
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )


class StepTrackingForm(forms.Form):
    """Addım məlumatları daxiletmə forması."""

    tracking_date = forms.DateField(
        label=_('Tarix'),
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    steps = forms.IntegerField(
        label=_('Addım Sayı'),
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': _('Addım sayı')
        })
    )
    distance_km = forms.DecimalField(
        label=_('Məsafə (km)'),
        required=False,
        min_value=0,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'placeholder': _('Məsafə')
        })
    )
    calories_burned = forms.IntegerField(
        label=_('Yandırılan Kalori'),
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': _('Kalori')
        })
    )
    active_minutes = forms.IntegerField(
        label=_('Aktiv Dəqiqələr'),
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': _('Dəqiqə')
        })
    )
