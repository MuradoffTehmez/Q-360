"""
Recruitment Module Serializers.
"""
from rest_framework import serializers
from .models import JobPosting, Application, Interview, Offer
from apps.accounts.models import User


class JobPostingSerializer(serializers.ModelSerializer):
    """Serializer for JobPosting model."""
    department_name = serializers.CharField(source='department.name', read_only=True, allow_null=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True, allow_null=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = JobPosting
        fields = [
            'id', 'title', 'department', 'department_name', 'description',
            'requirements', 'responsibilities', 'employment_type', 'location',
            'salary_min', 'salary_max', 'currency', 'status', 'status_display',
            'posted_date', 'closing_date', 'created_by', 'created_by_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'posted_date', 'created_by']


class ApplicationSerializer(serializers.ModelSerializer):
    """Serializer for Application model."""
    job_title = serializers.CharField(source='job_posting.title', read_only=True)
    applicant_name = serializers.CharField(source='applicant_name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Application
        fields = [
            'id', 'job_posting', 'job_title', 'applicant_name', 'applicant_email',
            'applicant_phone', 'resume', 'cover_letter', 'status', 'status_display',
            'applied_date', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'applied_date']


class InterviewSerializer(serializers.ModelSerializer):
    """Serializer for Interview model."""
    application_info = serializers.SerializerMethodField()
    interviewer_name = serializers.CharField(source='interviewer.get_full_name', read_only=True, allow_null=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Interview
        fields = [
            'id', 'application', 'application_info', 'interview_type',
            'scheduled_date', 'scheduled_time', 'duration_minutes',
            'location', 'interviewer', 'interviewer_name',
            'status', 'status_display', 'feedback', 'rating', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_application_info(self, obj):
        """Get application summary info."""
        return {
            'id': obj.application.id,
            'job_title': obj.application.job_posting.title,
            'applicant_name': obj.application.applicant_name,
            'applicant_email': obj.application.applicant_email
        }


class OfferSerializer(serializers.ModelSerializer):
    """Serializer for Offer model."""
    application_info = serializers.SerializerMethodField()
    offered_by_name = serializers.CharField(source='offered_by.get_full_name', read_only=True, allow_null=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Offer
        fields = [
            'id', 'application', 'application_info', 'offered_salary',
            'currency', 'start_date', 'offer_date', 'expiry_date',
            'status', 'status_display', 'offered_by', 'offered_by_name',
            'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_application_info(self, obj):
        """Get application summary info."""
        return {
            'id': obj.application.id,
            'job_title': obj.application.job_posting.title,
            'applicant_name': obj.application.applicant_name
        }
