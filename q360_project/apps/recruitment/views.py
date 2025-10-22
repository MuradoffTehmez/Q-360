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

    from apps.departments.models import Department
    departments = Department.objects.all()

    context = {
        'jobs': jobs,
        'status_filter': status_filter,
        'departments': departments
    }
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
            closing_date = request.POST.get('closing_date') or None
            number_of_positions = request.POST.get('openings', 1)

            job = JobPosting.objects.create(
                title=request.POST.get('title'),
                code=request.POST.get('code'),
                department_id=request.POST.get('department'),
                description=request.POST.get('description'),
                responsibilities=request.POST.get('responsibilities'),
                requirements=request.POST.get('requirements'),
                employment_type=request.POST.get('employment_type'),
                location=request.POST.get('location', ''),
                closing_date=closing_date,
                number_of_positions=number_of_positions,
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
def job_posting_edit(request, pk):
    """Edit job posting."""
    job = get_object_or_404(JobPosting, pk=pk)

    if request.method == 'POST':
        try:
            job.title = request.POST.get('title')
            job.code = request.POST.get('code')
            job.department_id = request.POST.get('department')
            job.description = request.POST.get('description')
            job.responsibilities = request.POST.get('responsibilities')
            job.requirements = request.POST.get('requirements')
            job.employment_type = request.POST.get('employment_type')
            job.location = request.POST.get('location')
            job.status = request.POST.get('status', job.status)
            job.save()
            return JsonResponse({'success': True, 'job_id': job.id})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    # GET request - show form
    from apps.departments.models import Department
    departments = Department.objects.all()
    context = {'job': job, 'departments': departments}
    return render(request, 'recruitment/job_edit.html', context)


@login_required
def application_detail(request, pk):
    """Application detail view."""
    application = get_object_or_404(
        Application.objects.select_related('job_posting').prefetch_related('interviews', 'offers'),
        pk=pk
    )

    # Get interviews for this application
    interviews = Interview.objects.filter(application=application).prefetch_related('interviewers').order_by('-scheduled_date')

    # Get notes (if you have notes model, add it. For now empty list)
    notes = []

    context = {
        'application': application,
        'interviews': interviews,
        'notes': notes
    }
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
@require_http_methods(["POST"])
def application_change_status(request, pk):
    """Change application status via JSON."""
    import json
    application = get_object_or_404(Application, pk=pk)

    try:
        data = json.loads(request.body)
        new_status = data.get('status')
        application.status = new_status
        application.save()
        return JsonResponse({'success': True, 'message': 'Status yeniləndi'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@login_required
@require_http_methods(["POST"])
def application_reject(request, pk):
    """Reject application."""
    import json
    application = get_object_or_404(Application, pk=pk)

    try:
        data = json.loads(request.body)
        reason = data.get('reason', '')
        application.status = 'rejected'
        if reason:
            application.notes = (application.notes + '\n\n' + f'Rədd səbəbi: {reason}').strip()
        application.save()
        return JsonResponse({'success': True, 'message': 'Müraciət rədd edildi'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@login_required
@require_http_methods(["POST"])
def application_schedule_interview(request, pk):
    """Schedule interview for application."""
    application = get_object_or_404(Application, pk=pk)

    try:
        interview_type = request.POST.get('interview_type')
        scheduled_date = request.POST.get('scheduled_date')
        interviewer_id = request.POST.get('interviewer')
        location = request.POST.get('location', '')
        notes = request.POST.get('notes', '')
        duration_minutes = request.POST.get('duration_minutes', 60)

        from apps.accounts.models import User

        interview = Interview.objects.create(
            application=application,
            interview_type=interview_type,
            scheduled_date=scheduled_date,
            location=location,
            duration_minutes=duration_minutes,
            created_by=request.user
        )

        # Add interviewer if provided
        if interviewer_id:
            interviewer = User.objects.get(id=interviewer_id)
            interview.interviewers.add(interviewer)

        # Update application status to interview
        application.status = 'interview'
        application.save()

        return JsonResponse({'success': True, 'message': 'Müsahibə planlaşdırıldı'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@login_required
@require_http_methods(["POST"])
def application_add_note(request, pk):
    """Add note to application."""
    application = get_object_or_404(Application, pk=pk)

    try:
        content = request.POST.get('content', '')
        if content:
            note_text = f'\n\n[{request.user.get_full_name()} - {timezone.now().strftime("%d/%m/%Y %H:%M")}]: {content}'
            application.notes = (application.notes or '') + note_text
            application.save()
        return JsonResponse({'success': True, 'message': 'Qeyd əlavə edildi'})
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


@login_required
def candidate_pipeline(request, job_id=None):
    """Kanban-style candidate pipeline view."""
    if not (request.user.is_manager() or request.user.is_admin):
        return redirect('recruitment:dashboard')

    # Get job posting
    jobs = JobPosting.objects.filter(status='open')
    selected_job = None

    if job_id:
        selected_job = get_object_or_404(JobPosting, id=job_id)
        applications = Application.objects.filter(job_posting=selected_job)
    else:
        # Show all open positions
        applications = Application.objects.filter(job_posting__status='open')

    # Group applications by status
    pipeline_stages = {
        'received': applications.filter(status='received'),
        'screening': applications.filter(status='screening'),
        'interview': applications.filter(status='interview'),
        'assessment': applications.filter(status='assessment'),
        'offer': applications.filter(status='offer'),
        'hired': applications.filter(status='hired'),
        'rejected': applications.filter(status='rejected'),
    }

    context = {
        'jobs': jobs,
        'selected_job': selected_job,
        'pipeline_stages': pipeline_stages,
        'all_applications': applications,
    }
    return render(request, 'recruitment/candidate_pipeline.html', context)


@login_required
@require_http_methods(["POST"])
def update_application_status(request, application_id):
    """Update application status (for pipeline drag-drop)."""
    application = get_object_or_404(Application, id=application_id)

    if not (request.user.is_manager() or request.user.is_admin):
        return JsonResponse({'success': False, 'message': 'İcazəniz yoxdur'}, status=403)

    try:
        new_status = request.POST.get('status')
        notes = request.POST.get('notes', '')

        application.status = new_status
        if notes:
            application.notes = (application.notes + '\n\n' + notes).strip()
        application.save()

        return JsonResponse({
            'success': True,
            'message': f'Status dəyişdirildi: {application.get_status_display()}'
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@login_required
def ai_screening(request):
    """
    AI-Powered CV Screening view.
    Shows applications with AI screening scores and filters.
    """
    from django.db.models import Avg

    # Get all recent applications
    applications = Application.objects.select_related(
        'job_posting'
    ).order_by('-applied_at')

    # Filter by job if specified
    job_id = request.GET.get('job')
    if job_id:
        applications = applications.filter(job_posting_id=job_id)

    # Filter by score range if model has ai_screening_score field
    has_ai_score = hasattr(Application, 'ai_screening_score')

    if has_ai_score:
        min_score = request.GET.get('min_score')
        if min_score:
            applications = applications.filter(ai_screening_score__gte=float(min_score))

        # Order by AI score
        applications = applications.order_by('-ai_screening_score', '-applied_at')
    else:
        # Just order by date if no AI score field
        applications = applications.order_by('-applied_at')

    # Get active jobs for filter dropdown
    jobs = JobPosting.objects.filter(status='open').order_by('-posted_date')

    # Calculate statistics
    total_applications = applications.count()

    if has_ai_score:
        avg_score = applications.aggregate(Avg('ai_screening_score'))['ai_screening_score__avg'] or 0
        high_match = applications.filter(ai_screening_score__gte=80).count()
        medium_match = applications.filter(ai_screening_score__gte=60, ai_screening_score__lt=80).count()
        low_match = applications.filter(ai_screening_score__lt=60).count()
    else:
        avg_score = 0
        high_match = 0
        medium_match = 0
        low_match = total_applications

    context = {
        'applications': applications[:100],  # Limit for performance
        'jobs': jobs,
        'selected_job_id': job_id,
        'stats': {
            'total': total_applications,
            'avg_score': round(avg_score, 1),
            'high_match': high_match,
            'medium_match': medium_match,
            'low_match': low_match,
        },
        'has_ai_score': has_ai_score,
    }

    return render(request, 'recruitment/ai_screening.html', context)


@login_required
def video_interview_schedule(request):
    """
    Video Interview Scheduling view.
    Schedule video interviews with platform integration (Zoom, Teams, Google Meet).
    """
    from django.utils import timezone
    from datetime import timedelta

    # Get upcoming video interviews
    upcoming_interviews = Interview.objects.filter(
        scheduled_date__gte=timezone.now(),
        status='scheduled'
    ).select_related(
        'application',
        'application__job_posting'
    ).prefetch_related('interviewers').order_by('scheduled_date')

    # Get applications ready for interview
    interview_ready_applications = Application.objects.filter(
        status__in=['screening', 'interview']
    ).select_related('job_posting').order_by('-applied_at')[:20]

    # Get interviewers (managers and HR staff)
    from apps.accounts.models import User
    interviewers = User.objects.filter(
        Q(is_superuser=True) | Q(groups__name__in=['HR', 'Managers'])
    ).distinct().order_by('first_name')

    # Check if Interview model has video_platform field
    has_video_platform = hasattr(Interview, 'video_platform')

    # Statistics
    today = timezone.now().date()
    this_week_start = today - timedelta(days=today.weekday())
    this_week_end = this_week_start + timedelta(days=6)

    stats = {
        'total_scheduled': upcoming_interviews.count(),
        'today': upcoming_interviews.filter(scheduled_date__date=today).count(),
        'this_week': upcoming_interviews.filter(
            scheduled_date__date__gte=this_week_start,
            scheduled_date__date__lte=this_week_end
        ).count(),
    }

    if has_video_platform:
        stats['zoom'] = upcoming_interviews.filter(video_platform='zoom').count()
        stats['teams'] = upcoming_interviews.filter(video_platform='teams').count()
        stats['meet'] = upcoming_interviews.filter(video_platform='meet').count()

    context = {
        'upcoming_interviews': upcoming_interviews[:20],
        'applications': interview_ready_applications,
        'interviewers': interviewers,
        'stats': stats,
        'has_video_platform': has_video_platform,
    }

    return render(request, 'recruitment/video_interview_schedule.html', context)


@login_required
def candidate_experience(request):
    """
    Candidate Experience Tracking view.
    NPS tracking and candidate journey analytics.
    """
    from django.db.models import Avg, Count
    from django.utils import timezone
    from datetime import timedelta
    import json

    # Check if Application model has candidate experience fields
    has_nps_score = hasattr(Application, 'nps_score')
    has_touchpoint_ratings = hasattr(Application, 'touchpoint_ratings')

    # Get all applications
    all_applications = Application.objects.select_related('job_posting')

    # Last 90 days
    ninety_days_ago = timezone.now() - timedelta(days=90)
    recent_applications = all_applications.filter(applied_at__gte=ninety_days_ago)

    # Calculate NPS
    if has_nps_score:
        # NPS Score: % Promoters (9-10) - % Detractors (0-6)
        applications_with_nps = recent_applications.exclude(nps_score__isnull=True)
        total_responses = applications_with_nps.count()

        promoters = applications_with_nps.filter(nps_score__gte=9).count()
        passives = applications_with_nps.filter(nps_score__range=[7, 8]).count()
        detractors = applications_with_nps.filter(nps_score__lte=6).count()

        if total_responses > 0:
            nps = ((promoters - detractors) / total_responses) * 100
        else:
            nps = 0

        avg_nps = round(nps, 1)
    else:
        promoters = 0
        passives = 0
        detractors = 0
        avg_nps = 0
        total_responses = 0

    # Touchpoint ratings - calculated from candidate_experience JSON field
    touchpoint_data = {
        'application_process': 0,
        'communication': 0,
        'interview_experience': 0,
        'feedback_timeliness': 0,
        'overall_experience': 0,
    }

    if has_touchpoint_ratings:
        # Calculate average for each touchpoint from JSON field
        touchpoint_counts = {key: 0 for key in touchpoint_data.keys()}

        for app in recent_applications:
            if app.candidate_experience:
                # candidate_experience is a JSON field like:
                # {"application_process": 4.5, "communication": 5, ...}
                for key in touchpoint_data.keys():
                    rating = app.candidate_experience.get(key)
                    if rating and isinstance(rating, (int, float)):
                        touchpoint_data[key] += float(rating)
                        touchpoint_counts[key] += 1

        # Calculate averages
        for key in touchpoint_data.keys():
            if touchpoint_counts[key] > 0:
                touchpoint_data[key] = round(touchpoint_data[key] / touchpoint_counts[key], 2)
            else:
                touchpoint_data[key] = 0

    # Group by status for journey analysis
    status_breakdown = recent_applications.values('status').annotate(
        count=Count('id')
    ).order_by('-count')

    # Trend data (last 6 months)
    months = []
    nps_trend = []

    for i in range(5, -1, -1):
        month_start = timezone.now() - timedelta(days=30*i)
        month_end = timezone.now() - timedelta(days=30*(i-1)) if i > 0 else timezone.now()

        if has_nps_score:
            month_apps = all_applications.filter(
                applied_at__gte=month_start,
                applied_at__lt=month_end
            ).exclude(nps_score__isnull=True)

            month_total = month_apps.count()
            if month_total > 0:
                month_promoters = month_apps.filter(nps_score__gte=9).count()
                month_detractors = month_apps.filter(nps_score__lte=6).count()
                month_nps = ((month_promoters - month_detractors) / month_total) * 100
            else:
                month_nps = 0
        else:
            month_nps = 0

        months.append(month_start.strftime('%b'))
        nps_trend.append(round(month_nps, 1))

    # Recent feedback comments
    recent_feedback = []
    if has_nps_score:
        # Get applications with feedback
        feedback_apps = recent_applications.exclude(
            nps_score__isnull=True
        ).order_by('-applied_at')[:10]

        for app in feedback_apps:
            recent_feedback.append({
                'candidate': app.candidate_name,
                'job': app.job_posting.title,
                'nps_score': app.nps_score,
                'date': app.applied_at,
                'feedback': getattr(app, 'feedback_comments', ''),
            })

    context = {
        'stats': {
            'avg_nps': avg_nps,
            'total_responses': total_responses,
            'promoters': promoters,
            'passives': passives,
            'detractors': detractors,
            'response_rate': round((total_responses / recent_applications.count() * 100), 1) if recent_applications.count() > 0 else 0,
        },
        'touchpoint_data': touchpoint_data,
        'status_breakdown': list(status_breakdown),
        'months': json.dumps(months),
        'nps_trend': json.dumps(nps_trend),
        'recent_feedback': recent_feedback,
        'has_nps_score': has_nps_score,
    }

    return render(request, 'recruitment/candidate_experience.html', context)
