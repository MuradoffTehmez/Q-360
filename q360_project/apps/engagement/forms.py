from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from .models import PulseSurvey, Recognition, AnonymousFeedback
import uuid

User = get_user_model()


class PulseSurveyForm(forms.ModelForm):
    """
    Pulse Survey yaratmaq və redaktə etmək üçün forma
    """

    class Meta:
        model = PulseSurvey
        fields = [
            'title', 'description', 'survey_type', 'status',
            'start_date', 'end_date', 'is_anonymous', 'is_mandatory',
            'target_departments', 'target_users'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Enter survey title')
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': _('Enter survey description')
            }),
            'survey_type': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'end_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'is_anonymous': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_mandatory': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'target_departments': forms.SelectMultiple(attrs={
                'class': 'form-select',
                'size': '5'
            }),
            'target_users': forms.SelectMultiple(attrs={
                'class': 'form-select',
                'size': '5'
            }),
        }


class RecognitionForm(forms.ModelForm):
    """
    Təşəkkür və Recognition göndərmək üçün forma
    """

    class Meta:
        model = Recognition
        fields = ['given_to', 'recognition_type', 'title', 'message', 'is_public']
        widgets = {
            'given_to': forms.Select(attrs={
                'class': 'form-select',
                'placeholder': _('Select recipient')
            }),
            'recognition_type': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Recognition title')
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': _('Write your recognition message...')
            }),
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Exclude current user from recipient list
        if user:
            self.fields['given_to'].queryset = User.objects.exclude(id=user.id).filter(is_active=True)


class AnonymousFeedbackForm(forms.ModelForm):
    """
    Anonim feedback forması
    """

    class Meta:
        model = AnonymousFeedback
        fields = ['category', 'subject', 'message', 'department']
        widgets = {
            'category': forms.Select(attrs={
                'class': 'form-select',
                'placeholder': _('Select category')
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Enter subject')
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': _('Write your feedback anonymously...')
            }),
            'department': forms.Select(attrs={
                'class': 'form-select',
                'required': False
            }),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Generate unique anonymous ID
        instance.anonymous_id = str(uuid.uuid4())

        if commit:
            instance.save()

        return instance


class SurveyResponseForm(forms.Form):
    """
    Survey cavabları üçün dinamik forma
    """

    def __init__(self, *args, **kwargs):
        survey = kwargs.pop('survey', None)
        super().__init__(*args, **kwargs)

        if survey:
            questions = survey.questions.all()

            for question in questions:
                field_name = f'question_{question.id}'

                if question.question_type == 'rating':
                    self.fields[field_name] = forms.ChoiceField(
                        label=question.question_text,
                        choices=[(i, str(i)) for i in range(1, 6)],
                        widget=forms.RadioSelect(attrs={'class': 'rating-radio'}),
                        required=question.is_required
                    )

                elif question.question_type == 'nps':
                    self.fields[field_name] = forms.ChoiceField(
                        label=question.question_text,
                        choices=[(i, str(i)) for i in range(0, 11)],
                        widget=forms.RadioSelect(attrs={'class': 'nps-radio'}),
                        required=question.is_required
                    )

                elif question.question_type == 'text':
                    self.fields[field_name] = forms.CharField(
                        label=question.question_text,
                        widget=forms.Textarea(attrs={
                            'class': 'form-control',
                            'rows': 3,
                            'placeholder': _('Your answer...')
                        }),
                        required=question.is_required
                    )

                elif question.question_type == 'yes_no':
                    self.fields[field_name] = forms.ChoiceField(
                        label=question.question_text,
                        choices=[('yes', _('Yes')), ('no', _('No'))],
                        widget=forms.RadioSelect(attrs={'class': 'yes-no-radio'}),
                        required=question.is_required
                    )

                elif question.question_type == 'multiple_choice' and question.options:
                    choices = [(opt, opt) for opt in question.options.get('choices', [])]
                    self.fields[field_name] = forms.ChoiceField(
                        label=question.question_text,
                        choices=choices,
                        widget=forms.RadioSelect(attrs={'class': 'multiple-choice-radio'}),
                        required=question.is_required
                    )

                elif question.question_type == 'emoji':
                    emoji_choices = [
                        ('😢', _('Very Dissatisfied')),
                        ('😕', _('Dissatisfied')),
                        ('😐', _('Neutral')),
                        ('😊', _('Satisfied')),
                        ('😄', _('Very Satisfied')),
                    ]
                    self.fields[field_name] = forms.ChoiceField(
                        label=question.question_text,
                        choices=emoji_choices,
                        widget=forms.RadioSelect(attrs={'class': 'emoji-radio'}),
                        required=question.is_required
                    )
