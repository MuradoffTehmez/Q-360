"""Views for Recruitment/ATS module."""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q, Count
from .models import JobPosting, Application, Interview, Offer, OnboardingTask


@login_required
def recruitment_dashboard(request):
    """Recruitment dashboard."""
    open_jobs = JobPosting.objects.filter(status='open').count()
    total_applications = Application.objects.exclude(status__in=['rejected', 'withdrawn']).count()
    pending_interviews = Interview.objects.filter(status='scheduled').count()
    recent_applications = Application.objects.order_by('-applied_at')[:10]

    context = {
        'open_jobs': open_jobs,
        'total_applications': total_applications,
        'pending_interviews': pending_interviews,
        'recent_applications': recent_applications,
    }
    return render(request, 'recruitment/dashboard.html', context)


@login_required
def job_posting_list(request):
    """List all job postings."""
    jobs = JobPosting.objects.annotate(
        app_count=Count('applications')
    ).order_by('-posted_date')

    status_filter = request.GET.get('status', '')
    if status_filter:
        jobs = jobs.filter(status=status_filter)

    context = {'jobs': jobs, 'status_filter': status_filter}
    return render(request, 'recruitment/job_list.html', context)


@login_required
def job_posting_detail(request, pk):
    """Job posting detail with applications."""
    job = get_object_or_404(JobPosting.objects.prefetch_related('applications'), pk=pk)
    applications = job.applications.all().order_by('-applied_at')

    context = {'job': job, 'applications': applications}
    return render(request, 'recruitment/job_detail.html', context)


@login_required
def job_posting_create(request):
    """Create new job posting."""
    if request.method == 'POST':
        try:
            job = JobPosting.objects.create(
                title=request.POST.get('title'),
                code=request.POST.get('code'),
                department_id=request.POST.get('department'),
                description=request.POST.get('description'),
                responsibilities=request.POST.get('responsibilities'),
                requirements=request.POST.get('requirements'),
                employment_type=request.POST.get('employment_type'),
                location=request.POST.get('location'),
                created_by=request.user
            )
            return JsonResponse({'success': True, 'job_id': job.id})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    # GET request - show form
    from apps.departments.models import Department
    departments = Department.objects.all()
    context = {'departments': departments}
    return render(request, 'recruitment/job_create.html', context)


@login_required
def application_detail(request, pk):
    """Application detail view."""
    application = get_object_or_404(
        Application.objects.select_related('job_posting').prefetch_related('interviews', 'offers'),
        pk=pk
    )

    context = {'application': application}
    return render(request, 'recruitment/application_detail.html', context)


@login_required
@require_http_methods(["POST"])
def application_update_status(request, pk):
    """Update application status."""
    application = get_object_or_404(Application, pk=pk)

    try:
        new_status = request.POST.get('status')
        application.status = new_status
        application.save()
        return JsonResponse({'success': True, 'message': 'Status yeniləndi'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@login_required
def interview_calendar(request):
    """Interview calendar view."""
    from datetime import datetime, timedelta
    from django.utils import timezone

    interviews = Interview.objects.filter(
        status='scheduled'
    ).select_related('application', 'application__job_posting').order_by('scheduled_date')

    completed_interviews = Interview.objects.filter(
        status='completed'
    ).select_related('application', 'application__job_posting').order_by('-scheduled_date')[:10]

    # Calculate statistics
    today = timezone.now().date()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)

    today_count = interviews.filter(scheduled_date__date=today).count()
    this_week_count = interviews.filter(
        scheduled_date__date__gte=week_start,
        scheduled_date__date__lte=week_end
    ).count()

    context = {
        'interviews': interviews,
        'completed_interviews': completed_interviews,
        'today_count': today_count,
        'this_week_count': this_week_count,
    }
    return render(request, 'recruitment/interview_calendar.html', context)


@login_required
@require_http_methods(["POST"])
def interview_create(request, application_id):
    """Schedule new interview."""
    application = get_object_or_404(Application, pk=application_id)

    try:
        interview = Interview.objects.create(
            application=application,
            interview_type=request.POST.get('interview_type'),
            scheduled_date=request.POST.get('scheduled_date'),
            duration_minutes=request.POST.get('duration_minutes', 60),
            location=request.POST.get('location', ''),
            meeting_link=request.POST.get('meeting_link', ''),
            created_by=request.user
        )
        return JsonResponse({'success': True, 'message': 'Müsahibə planlaşdırıldı'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
