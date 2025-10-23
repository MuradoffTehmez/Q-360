"""
Recruitment Module API Views.
"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q, Avg
from django.utils import timezone

from .models import JobPosting, Application, Interview, Offer
from .serializers import (
    JobPostingSerializer, ApplicationSerializer,
    InterviewSerializer, OfferSerializer
)


class JobPostingViewSet(viewsets.ModelViewSet):
    """ViewSet for managing job postings."""
    queryset = JobPosting.objects.select_related('department', 'created_by')
    serializer_class = JobPostingSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['department', 'status', 'employment_type', 'location']
    search_fields = ['title', 'description', 'requirements']
    ordering_fields = ['posted_date', 'closing_date', 'created_at']
    ordering = ['-posted_date']

    def get_permissions(self):
        """Public can view active jobs, authenticated users can apply."""
        if self.action in ['list', 'retrieve', 'active_jobs']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        """Filter based on user permissions and action."""
        queryset = super().get_queryset()

        # Public can only see active jobs
        if not self.request.user.is_authenticated:
            return queryset.filter(status='active')

        # Admins and HR see all
        if self.request.user.is_admin():
            return queryset

        # Managers see their department's jobs
        if self.request.user.is_manager():
            return queryset.filter(Q(department=self.request.user.department) | Q(status='active'))

        # Regular users see only active jobs
        return queryset.filter(status='active')

    def perform_create(self, serializer):
        """Set created_by to current user."""
        serializer.save(created_by=self.request.user, posted_date=timezone.now().date())

    @action(detail=False, methods=['get'])
    def active_jobs(self, request):
        """Get all active job postings."""
        queryset = self.get_queryset().filter(status='active')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        """Publish a job posting."""
        job = self.get_object()

        if not request.user.is_admin():
            return Response(
                {'error': 'Only admins can publish job postings'},
                status=status.HTTP_403_FORBIDDEN
            )

        job.status = 'active'
        job.posted_date = timezone.now().date()
        job.save()

        return Response(
            JobPostingSerializer(job).data,
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'])
    def close(self, request, pk=None):
        """Close a job posting."""
        job = self.get_object()

        if not request.user.is_admin():
            return Response(
                {'error': 'Only admins can close job postings'},
                status=status.HTTP_403_FORBIDDEN
            )

        job.status = 'closed'
        job.save()

        return Response(
            JobPostingSerializer(job).data,
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['get'])
    def applications(self, request, pk=None):
        """Get all applications for this job posting."""
        job = self.get_object()
        applications = Application.objects.filter(job_posting=job)
        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data)


class ApplicationViewSet(viewsets.ModelViewSet):
    """ViewSet for managing applications."""
    queryset = Application.objects.select_related('job_posting')
    serializer_class = ApplicationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['job_posting', 'status']
    search_fields = ['applicant_name', 'applicant_email']
    ordering_fields = ['applied_date', 'created_at']
    ordering = ['-applied_date']

    def get_permissions(self):
        """Allow anonymous applications."""
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        """Filter based on user permissions."""
        if not self.request.user.is_authenticated:
            return Application.objects.none()

        queryset = super().get_queryset()

        if self.request.user.is_admin():
            return queryset

        if self.request.user.is_manager():
            return queryset.filter(job_posting__department=self.request.user.department)

        return queryset.none()

    @action(detail=True, methods=['post'])
    def shortlist(self, request, pk=None):
        """Shortlist an application."""
        application = self.get_object()

        if not (request.user.is_admin() or request.user.is_manager()):
            return Response(
                {'error': 'Only admins and managers can shortlist applications'},
                status=status.HTTP_403_FORBIDDEN
            )

        application.status = 'shortlisted'
        application.save()

        return Response(
            ApplicationSerializer(application).data,
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Reject an application."""
        application = self.get_object()

        if not (request.user.is_admin() or request.user.is_manager()):
            return Response(
                {'error': 'Only admins and managers can reject applications'},
                status=status.HTTP_403_FORBIDDEN
            )

        rejection_reason = request.data.get('notes', '')
        application.status = 'rejected'
        application.notes = rejection_reason
        application.save()

        return Response(
            ApplicationSerializer(application).data,
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'])
    def pending(self, request):
        """Get all pending applications."""
        queryset = self.get_queryset().filter(status='pending')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class InterviewViewSet(viewsets.ModelViewSet):
    """ViewSet for managing interviews."""
    queryset = Interview.objects.select_related('application__job_posting', 'interviewer')
    serializer_class = InterviewSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['application', 'interviewer', 'status', 'interview_type']
    search_fields = ['application__applicant_name']
    ordering_fields = ['scheduled_date', 'scheduled_time', 'created_at']
    ordering = ['scheduled_date', 'scheduled_time']

    def get_queryset(self):
        """Filter based on user permissions."""
        queryset = super().get_queryset()
        user = self.request.user

        if user.is_admin():
            return queryset

        # Managers see their department's interviews
        if user.is_manager():
            return queryset.filter(
                Q(application__job_posting__department=user.department) | Q(interviewer=user)
            )

        # Regular users see only interviews they're conducting
        return queryset.filter(interviewer=user)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark interview as completed."""
        interview = self.get_object()

        if not (request.user.is_admin() or interview.interviewer == request.user):
            return Response(
                {'error': 'Only the interviewer can mark interview as completed'},
                status=status.HTTP_403_FORBIDDEN
            )

        interview.status = 'completed'
        interview.save()

        return Response(
            InterviewSerializer(interview).data,
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel an interview."""
        interview = self.get_object()

        if not (request.user.is_admin() or interview.interviewer == request.user):
            return Response(
                {'error': 'Only admin or interviewer can cancel interview'},
                status=status.HTTP_403_FORBIDDEN
            )

        interview.status = 'cancelled'
        interview.save()

        return Response(
            InterviewSerializer(interview).data,
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming interviews."""
        today = timezone.now().date()
        queryset = self.get_queryset().filter(
            scheduled_date__gte=today,
            status='scheduled'
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def my_interviews(self, request):
        """Get interviews for current user as interviewer."""
        queryset = Interview.objects.filter(interviewer=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class OfferViewSet(viewsets.ModelViewSet):
    """ViewSet for managing job offers."""
    queryset = Offer.objects.select_related('application__job_posting', 'offered_by')
    serializer_class = OfferSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['application', 'status']
    ordering_fields = ['offer_date', 'expiry_date', 'created_at']
    ordering = ['-offer_date']

    def get_queryset(self):
        """Filter based on user permissions."""
        queryset = super().get_queryset()
        user = self.request.user

        if user.is_admin():
            return queryset

        # Managers see their department's offers
        if user.is_manager():
            return queryset.filter(application__job_posting__department=user.department)

        return queryset.none()

    def perform_create(self, serializer):
        """Set offered_by to current user."""
        serializer.save(offered_by=self.request.user)

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        """Mark offer as accepted."""
        offer = self.get_object()

        if not request.user.is_admin():
            return Response(
                {'error': 'Only admins can mark offers as accepted'},
                status=status.HTTP_403_FORBIDDEN
            )

        offer.status = 'accepted'
        offer.save()

        return Response(
            OfferSerializer(offer).data,
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'])
    def decline(self, request, pk=None):
        """Mark offer as declined."""
        offer = self.get_object()

        if not request.user.is_admin():
            return Response(
                {'error': 'Only admins can mark offers as declined'},
                status=status.HTTP_403_FORBIDDEN
            )

        offer.status = 'declined'
        offer.save()

        return Response(
            OfferSerializer(offer).data,
            status=status.HTTP_200_OK
        )
