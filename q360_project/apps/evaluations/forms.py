"""
Forms for evaluations app.
"""
from django import forms
from django.core.exceptions import ValidationError
from .models import (
    EvaluationCampaign, Question, QuestionCategory,
    EvaluationAssignment, Response
)


class EvaluationCampaignForm(forms.ModelForm):
    """Form for creating/editing evaluation campaigns."""

    class Meta:
        model = EvaluationCampaign
        fields = ['title', 'description', 'start_date', 'end_date',
                  'is_anonymous', 'allow_self_evaluation',
                  'target_departments', 'target_users']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'target_departments': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'target_users': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            if end_date <= start_date:
                raise ValidationError('Bitmə tarixi başlama tarixindən sonra olmalıdır.')

        return cleaned_data


class QuestionForm(forms.ModelForm):
    """Form for creating/editing questions."""

    class Meta:
        model = Question
        fields = ['category', 'text', 'question_type', 'max_score',
                  'is_required', 'order']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'question_type': forms.Select(attrs={'class': 'form-select'}),
            'max_score': forms.NumberInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class QuestionCategoryForm(forms.ModelForm):
    """Form for creating/editing question categories."""

    class Meta:
        model = QuestionCategory
        fields = ['name', 'description', 'order']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class ResponseForm(forms.ModelForm):
    """Form for submitting evaluation responses."""

    class Meta:
        model = Response
        fields = ['score', 'boolean_answer', 'text_answer', 'comment']
        widgets = {
            'score': forms.NumberInput(attrs={'class': 'form-control'}),
            'text_answer': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def clean(self):
        cleaned_data = super().clean()
        question = self.instance.question if self.instance else None

        if question:
            if question.question_type == 'scale' and not cleaned_data.get('score'):
                raise ValidationError('Bal skalası üçün bal daxil edilməlidir.')
            elif question.question_type == 'boolean' and cleaned_data.get('boolean_answer') is None:
                raise ValidationError('Bəli/Xeyr sualı üçün cavab seçilməlidir.')
            elif question.question_type == 'text' and not cleaned_data.get('text_answer'):
                raise ValidationError('Mətn cavabı daxil edilməlidir.')

        return cleaned_data


class EvaluationAssignmentForm(forms.ModelForm):
    """Form for creating evaluation assignments."""

    class Meta:
        model = EvaluationAssignment
        fields = ['campaign', 'evaluator', 'evaluatee', 'relationship']
        widgets = {
            'campaign': forms.Select(attrs={'class': 'form-select'}),
            'evaluator': forms.Select(attrs={'class': 'form-select'}),
            'evaluatee': forms.Select(attrs={'class': 'form-select'}),
            'relationship': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        evaluator = cleaned_data.get('evaluator')
        evaluatee = cleaned_data.get('evaluatee')
        relationship = cleaned_data.get('relationship')

        if evaluator and evaluatee:
            # Check if evaluator can evaluate evaluatee
            if not evaluator.can_evaluate(evaluatee):
                raise ValidationError(
                    'Bu istifadəçinin göstərilən şəxsi qiymətləndirməyə icazəsi yoxdur.'
                )

            # Self-evaluation check
            if relationship == 'self' and evaluator != evaluatee:
                raise ValidationError(
                    'Özünüdəyərləndirmə üçün qiymətləndirən və qiymətləndirilən eyni olmalıdır.'
                )

            # Check for duplicates
            if EvaluationAssignment.objects.filter(
                campaign=cleaned_data.get('campaign'),
                evaluator=evaluator,
                evaluatee=evaluatee
            ).exists():
                raise ValidationError('Bu tapşırıq artıq mövcuddur.')

        return cleaned_data


class BulkAssignmentForm(forms.Form):
    """Form for creating bulk evaluation assignments."""

    campaign = forms.ModelChoiceField(
        queryset=EvaluationCampaign.objects.filter(status='draft'),
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    include_self_evaluation = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    include_supervisor = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    include_peers = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    include_subordinates = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
