"""
Template views for workforce planning app.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from .models import TalentMatrix, CriticalRole, SuccessionCandidate, CompetencyGap


@login_required
def talent_matrix_view(request):
    """9-Box Talent Matrix visualization."""
    # Get all talent assessments
    talent_assessments = TalentMatrix.objects.select_related('user', 'assessed_by').order_by('-assessment_date')

    # Filter by assessment period if provided
    period_filter = request.GET.get('period', '')
    if period_filter:
        talent_assessments = talent_assessments.filter(assessment_period=period_filter)

    # Get available periods
    periods = TalentMatrix.objects.values_list('assessment_period', flat=True).distinct()

    # Count by box category
    box_distribution = {}
    for i in range(1, 10):
        box_key = f'box{i}'
        box_distribution[box_key] = talent_assessments.filter(box_category=box_key).count()

    # Statistics
    stats = {
        'total_assessed': talent_assessments.count(),
        'high_performers': talent_assessments.filter(performance_level='high').count(),
        'high_potential': talent_assessments.filter(potential_level='high').count(),
        'top_talent': talent_assessments.filter(box_category='box9').count(),
    }

    context = {
        'talent_assessments': talent_assessments[:50],  # Limit to 50 for performance
        'box_distribution': box_distribution,
        'periods': periods,
        'period_filter': period_filter,
        'stats': stats,
    }

    return render(request, 'workforce_planning/talent_matrix.html', context)


@login_required
def succession_planning_view(request):
    """Succession planning dashboard."""
    # Get critical roles with succession candidates
    critical_roles = CriticalRole.objects.filter(is_active=True).select_related(
        'position', 'current_holder'
    ).prefetch_related('succession_candidates')

    # Filter by criticality
    criticality_filter = request.GET.get('criticality', '')
    if criticality_filter:
        critical_roles = critical_roles.filter(criticality_level=criticality_filter)

    # Filter by readiness
    readiness_filter = request.GET.get('readiness', '')
    if readiness_filter:
        critical_roles = critical_roles.filter(succession_readiness=readiness_filter)

    # Statistics
    stats = {
        'total_critical_roles': critical_roles.count(),
        'no_successor': critical_roles.filter(succession_readiness='no_successor').count(),
        'ready_now': critical_roles.filter(succession_readiness='ready_now').count(),
        'needs_development': critical_roles.filter(succession_readiness='needs_development').count(),
    }

    # Get all succession candidates
    succession_candidates = SuccessionCandidate.objects.filter(
        is_active=True
    ).select_related('critical_role', 'candidate', 'nominated_by').order_by('-readiness_score')

    context = {
        'critical_roles': critical_roles,
        'succession_candidates': succession_candidates[:20],
        'criticality_filter': criticality_filter,
        'readiness_filter': readiness_filter,
        'stats': stats,
    }

    return render(request, 'workforce_planning/succession_planning.html', context)


@login_required
def critical_roles_view(request):
    """List of critical roles."""
    critical_roles = CriticalRole.objects.filter(is_active=True).select_related(
        'position', 'current_holder'
    ).prefetch_related('required_competencies', 'succession_candidates')

    # Statistics
    stats = {
        'total': critical_roles.count(),
        'critical': critical_roles.filter(criticality_level='critical').count(),
        'high': critical_roles.filter(criticality_level='high').count(),
        'medium': critical_roles.filter(criticality_level='medium').count(),
    }

    context = {
        'critical_roles': critical_roles,
        'stats': stats,
    }

    return render(request, 'workforce_planning/critical_roles.html', context)


@login_required
def gap_analysis_view(request):
    """Competency gap analysis overview."""
    # Get all competency gaps
    gaps = CompetencyGap.objects.filter(is_closed=False).select_related(
        'user', 'competency', 'current_level', 'target_level', 'target_position'
    ).order_by('-priority', '-gap_score')

    # Filter by priority
    priority_filter = request.GET.get('priority', '')
    if priority_filter:
        gaps = gaps.filter(priority=priority_filter)

    # Filter by gap status
    status_filter = request.GET.get('status', '')
    if status_filter:
        gaps = gaps.filter(gap_status=status_filter)

    # Statistics
    stats = {
        'total_gaps': gaps.count(),
        'urgent': gaps.filter(priority='urgent').count(),
        'high': gaps.filter(priority='high').count(),
        'major_gaps': gaps.filter(gap_status='major_gap').count(),
    }

    context = {
        'gaps': gaps[:50],
        'priority_filter': priority_filter,
        'status_filter': status_filter,
        'stats': stats,
    }

    return render(request, 'workforce_planning/gap_analysis.html', context)


@login_required
def my_gaps_view(request):
    """User's personal competency gaps."""
    # Get user's competency gaps
    my_gaps = CompetencyGap.objects.filter(
        user=request.user,
        is_closed=False
    ).select_related(
        'competency', 'current_level', 'target_level', 'target_position'
    ).prefetch_related('recommended_trainings').order_by('-priority', '-gap_score')

    # Statistics
    stats = {
        'total_gaps': my_gaps.count(),
        'urgent': my_gaps.filter(priority='urgent').count(),
        'high': my_gaps.filter(priority='high').count(),
        'major_gaps': my_gaps.filter(gap_status='major_gap').count(),
        'avg_gap_score': my_gaps.aggregate(avg=Count('gap_score'))['avg'] or 0,
    }

    # Closed gaps
    closed_gaps = CompetencyGap.objects.filter(
        user=request.user,
        is_closed=True
    ).order_by('-closed_date')[:10]

    context = {
        'my_gaps': my_gaps,
        'closed_gaps': closed_gaps,
        'stats': stats,
    }

    return render(request, 'workforce_planning/my_gaps.html', context)
