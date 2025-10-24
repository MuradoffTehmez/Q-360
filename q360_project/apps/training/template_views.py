"""Template views for training app."""
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, Avg
from django.core.paginator import Paginator
from django.utils import timezone
from .models import TrainingResource, UserTraining
from apps.competencies.models import Competency

@login_required
def catalog(request):
    """Training catalog with full backend data."""
    # Get filter parameters
    search_query = request.GET.get('search', '')
    type_filter = request.GET.get('type', '')
    difficulty_filter = request.GET.get('difficulty', '')
    page_number = request.GET.get('page', 1)

    # Base queryset
    trainings = TrainingResource.objects.filter(is_active=True).annotate(
        enrolled_count=Count('user_trainings', filter=Q(user_trainings__status__in=['in_progress', 'completed']))
    )

    # Apply filters
    if search_query:
        trainings = trainings.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(provider__icontains=search_query)
        )

    if type_filter:
        trainings = trainings.filter(type=type_filter)

    if difficulty_filter:
        trainings = trainings.filter(difficulty_level=difficulty_filter)

    # Order by created date (newest first)
    trainings = trainings.order_by('-created_at')

    # Pagination
    paginator = Paginator(trainings, 9)  # 9 per page (3x3 grid)
    page_obj = paginator.get_page(page_number)

    # Statistics
    stats = {
        'total_resources': TrainingResource.objects.filter(is_active=True).count(),
        'my_trainings': UserTraining.objects.filter(user=request.user).count(),
        'in_progress': UserTraining.objects.filter(user=request.user, status='in_progress').count(),
        'completed': UserTraining.objects.filter(user=request.user, status='completed').count(),
    }

    # Type and difficulty choices
    type_choices = TrainingResource.TRAINING_TYPE_CHOICES
    difficulty_choices = TrainingResource.DIFFICULTY_LEVEL_CHOICES

    context = {
        'trainings': page_obj,
        'page_obj': page_obj,
        'stats': stats,
        'search_query': search_query,
        'type_filter': type_filter,
        'difficulty_filter': difficulty_filter,
        'type_choices': type_choices,
        'difficulty_choices': difficulty_choices,
    }

    return render(request, 'training/catalog.html', context)

@login_required
def my_trainings(request):
    """User's enrolled trainings with progress."""
    # Get user's trainings
    user_trainings = UserTraining.objects.filter(user=request.user).select_related(
        'resource', 'assigned_by'
    ).prefetch_related('resource__required_competencies').order_by('-created_at')

    # Filter by status if provided
    status_filter = request.GET.get('status', '')
    if status_filter:
        user_trainings = user_trainings.filter(status=status_filter)

    # Calculate statistics
    total_trainings = user_trainings.count()
    in_progress = user_trainings.filter(status='in_progress').count()
    completed = user_trainings.filter(status='completed').count()
    not_started = user_trainings.filter(status='pending').count()

    # Calculate average progress
    avg_progress = user_trainings.aggregate(
        avg=Avg('progress_percentage')
    )['avg'] or 0

    # Recent completions (last 5)
    recent_completions = user_trainings.filter(
        status='completed',
        completed_date__isnull=False
    ).order_by('-completed_date')[:5]

    # Upcoming deadlines
    upcoming_deadlines = user_trainings.filter(
        status__in=['pending', 'in_progress'],
        due_date__isnull=False,
        due_date__gte=timezone.now()
    ).order_by('due_date')[:5]

    context = {
        'user_trainings': user_trainings,
        'total_trainings': total_trainings,
        'in_progress': in_progress,
        'completed': completed,
        'not_started': not_started,
        'avg_progress': round(avg_progress, 1),
        'recent_completions': recent_completions,
        'upcoming_deadlines': upcoming_deadlines,
        'status_filter': status_filter,
    }

    return render(request, 'training/my_trainings.html', context)

@login_required
def training_detail(request, pk):
    """Detailed training view with enrollment."""
    training = get_object_or_404(TrainingResource, pk=pk)

    # Check if user is enrolled
    user_training = UserTraining.objects.filter(
        user=request.user,
        resource=training
    ).first()

    # Get required competencies
    required_competencies = training.required_competencies.all()

    # Get related trainings (same competencies)
    related_trainings = TrainingResource.objects.filter(
        is_active=True,
        required_competencies__in=required_competencies
    ).exclude(id=training.id).distinct()[:3]

    # Enrollment statistics
    total_enrolled = UserTraining.objects.filter(resource=training).count()
    completed_count = UserTraining.objects.filter(resource=training, status='completed').count()
    completion_rate = (completed_count / total_enrolled * 100) if total_enrolled > 0 else 0

    # Average rating (if you have ratings)
    # avg_rating = training.ratings.aggregate(avg=Avg('score'))['avg'] or 0

    context = {
        'training': training,
        'training_id': pk,
        'user_training': user_training,
        'required_competencies': required_competencies,
        'related_trainings': related_trainings,
        'total_enrolled': total_enrolled,
        'completed_count': completed_count,
        'completion_rate': round(completion_rate, 1),
        'is_enrolled': user_training is not None,
    }

    return render(request, 'training/training_detail.html', context)

@login_required
def training_manage(request):
    """Admin view for managing trainings."""
    if not hasattr(request.user, 'is_admin') or not request.user.is_admin():
        return render(request, '403.html', status=403)
    return catalog(request)


@login_required
def my_certificates(request):
    """
    Sertifikat İdarəetməsi - İstifadəçinin tamamladığı təlimlərin sertifikatları.

    Funksiyalar:
    - Tamamlanmış təlimlər üçün sertifikat linki əlavə etmə
    - Mövcud sertifikatları görüntüləmə
    - Sertifikat linkini yeniləmə/silmə
    """
    # Get completed trainings with certificates
    trainings_with_certificates = UserTraining.objects.filter(
        user=request.user,
        status='completed',
        certificate_url__isnull=False
    ).exclude(certificate_url='').select_related('resource').order_by('-completed_date')

    # Get completed trainings without certificates
    trainings_without_certificates = UserTraining.objects.filter(
        user=request.user,
        status='completed'
    ).filter(
        Q(certificate_url__isnull=True) | Q(certificate_url='')
    ).select_related('resource').order_by('-completed_date')

    # Statistics
    total_completed = UserTraining.objects.filter(
        user=request.user,
        status='completed'
    ).count()

    with_certificates = trainings_with_certificates.count()
    without_certificates = trainings_without_certificates.count()

    # Calculate certificate completion rate
    certificate_rate = (with_certificates / total_completed * 100) if total_completed > 0 else 0

    # Recent certificates (last 5)
    recent_certificates = trainings_with_certificates[:5]

    # Training types distribution
    training_types = {}
    for training in trainings_with_certificates:
        type_display = training.resource.get_type_display()
        training_types[type_display] = training_types.get(type_display, 0) + 1

    context = {
        'trainings_with_certificates': trainings_with_certificates,
        'trainings_without_certificates': trainings_without_certificates,
        'total_completed': total_completed,
        'with_certificates': with_certificates,
        'without_certificates': without_certificates,
        'certificate_rate': round(certificate_rate, 1),
        'recent_certificates': recent_certificates,
        'training_types': training_types,
    }

    return render(request, 'training/my_certificates.html', context)


@login_required
def skill_matrix(request):
    """
    Skill Matrix view - Interactive skill matrix for team/department.
    Shows proficiency levels across competencies for all team members.
    """
    from apps.competencies.models import UserSkill, ProficiencyLevel
    from apps.accounts.models import User

    user = request.user

    # Get filter parameters
    department_id = request.GET.get('department')
    team_filter = request.GET.get('team')

    # Determine users to display based on user role
    if user.is_admin():
        # Admins can see all users
        if department_id:
            users = User.objects.filter(is_active=True, department_id=department_id)
        else:
            users = User.objects.filter(is_active=True)
    elif hasattr(user, 'is_manager') and user.is_manager():
        # Managers see their subordinates
        users = user.get_subordinates() if hasattr(user, 'get_subordinates') else [user]
    else:
        # Regular users see only themselves and their team
        if user.department:
            users = User.objects.filter(is_active=True, department=user.department)
        else:
            users = User.objects.filter(id=user.id)

    users = users.order_by('first_name', 'last_name')[:50]  # Limit for performance

    # Get all competencies (limit to relevant ones)
    if department_id:
        from apps.competencies.models import PositionCompetency
        # Get competencies required by positions in this department
        position_ids = User.objects.filter(
            department_id=department_id,
            position__isnull=False
        ).values_list('position_id', flat=True)

        competency_ids = PositionCompetency.objects.filter(
            position_id__in=position_ids
        ).values_list('competency_id', flat=True).distinct()

        competencies = Competency.objects.filter(
            id__in=competency_ids,
            is_active=True
        ).order_by('name')[:20]  # Limit to 20 competencies
    else:
        # Get top 20 most common competencies
        competencies = Competency.objects.filter(
            is_active=True
        ).annotate(
            user_count=Count('user_skills')
        ).order_by('-user_count', 'name')[:20]

    # Get all user skills for these users and competencies
    user_skills = UserSkill.objects.filter(
        user__in=users,
        competency__in=competencies,
        is_approved=True
    ).select_related('user', 'competency', 'level')

    # Build skill matrix data structure
    skill_matrix = {}
    for skill in user_skills:
        if skill.user.id not in skill_matrix:
            skill_matrix[skill.user.id] = {}
        skill_matrix[skill.user.id][skill.competency.id] = {
            'level': skill.level.score_min if skill.level else 0,
            'level_name': skill.level.name if skill.level else 'Yoxdur',
        }

    # Calculate statistics
    stats = {
        'total_users': users.count(),
        'total_competencies': competencies.count(),
        'total_skills': user_skills.count(),
        'avg_skills_per_user': user_skills.count() / users.count() if users.count() > 0 else 0,
    }

    # Identify skill gaps (users missing critical competencies)
    gaps = []
    for usr in users:
        user_competency_ids = set(skill_matrix.get(usr.id, {}).keys())
        missing_competencies = set(c.id for c in competencies) - user_competency_ids
        if missing_competencies:
            gaps.append({
                'user': usr,
                'missing_count': len(missing_competencies),
            })

    gaps.sort(key=lambda x: x['missing_count'], reverse=True)

    # Get departments for filter
    from apps.departments.models import Department
    departments = Department.objects.all().order_by('name')

    context = {
        'users': users,
        'competencies': competencies,
        'skill_matrix': skill_matrix,
        'stats': stats,
        'gaps': gaps[:10],  # Top 10 users with most gaps
        'departments': departments,
        'selected_department': department_id,
    }

    return render(request, 'training/skill_matrix.html', context)


@login_required
def certification_tracking(request):
    """
    Certification Tracking view - Professional certification management.
    Tracks certifications, expiry dates, CE hours, and renewal requirements.
    """
    from django.db.models import Sum
    from datetime import timedelta

    user = request.user

    # Check if we have a Certification model
    # If not, we'll use a simplified version based on training completions

    try:
        from apps.training.models import Certification
        has_certification_model = True
    except ImportError:
        has_certification_model = False

    if has_certification_model:
        # Get user's certifications
        my_certifications = Certification.objects.filter(
            user=user
        ).order_by('-issue_date')

        # Separate by status
        active_certs = my_certifications.filter(status='active')
        expiring_soon = my_certifications.filter(
            status='active',
            expiration_date__lte=timezone.now().date() + timedelta(days=90),
            expiration_date__gt=timezone.now().date()
        )
        expired_certs = my_certifications.filter(status='expired')

        # CE Hours tracking
        total_ce_hours = my_certifications.aggregate(
            total=Sum('ce_hours_completed')
        )['total'] or 0

        # Team certifications (if manager)
        if hasattr(user, 'is_manager') and user.is_manager():
            team_members = user.get_subordinates() if hasattr(user, 'get_subordinates') else []
            team_certifications = Certification.objects.filter(
                user__in=team_members
            ).select_related('user').order_by('-issue_date')[:20]
        else:
            team_certifications = []

    else:
        # Fallback: Use completed trainings as certifications
        my_certifications = UserTraining.objects.filter(
            user=user,
            status='completed',
            certificate_url__isnull=False
        ).exclude(certificate_url='').select_related('resource').order_by('-completed_date')

        active_certs = my_certifications
        expiring_soon = []
        expired_certs = []
        total_ce_hours = 0
        team_certifications = []

    # Statistics
    stats = {
        'total_certifications': my_certifications.count(),
        'active': active_certs.count() if has_certification_model else my_certifications.count(),
        'expiring_soon': expiring_soon.count() if has_certification_model else 0,
        'expired': expired_certs.count() if has_certification_model else 0,
        'total_ce_hours': total_ce_hours,
    }

    # Renewal reminders (next 6 months)
    renewal_reminders = []
    if has_certification_model:
        upcoming_renewals = my_certifications.filter(
            status='active',
            expiration_date__lte=timezone.now().date() + timedelta(days=180),
            expiration_date__gt=timezone.now().date()
        ).order_by('expiration_date')

        for cert in upcoming_renewals:
            days_until_expiry = (cert.expiration_date - timezone.now().date()).days
            renewal_reminders.append({
                'certification': cert,
                'days_until_expiry': days_until_expiry,
                'urgency': 'high' if days_until_expiry < 30 else 'medium' if days_until_expiry < 90 else 'low',
            })

    # Timeline view (last 12 months + next 6 months)
    timeline_items = []
    if has_certification_model:
        timeline_start = timezone.now().date() - timedelta(days=365)
        timeline_end = timezone.now().date() + timedelta(days=180)

        timeline_certs = my_certifications.filter(
            Q(issue_date__gte=timeline_start) |
            Q(expiration_date__lte=timeline_end, expiration_date__gte=timezone.now().date())
        ).order_by('-issue_date')

        for cert in timeline_certs:
            timeline_items.append({
                'date': cert.issue_date,
                'type': 'issued',
                'certification': cert,
            })
            if cert.expiration_date:
                timeline_items.append({
                    'date': cert.expiration_date,
                    'type': 'expires',
                    'certification': cert,
                })

        timeline_items.sort(key=lambda x: x['date'], reverse=True)

    context = {
        'my_certifications': my_certifications,
        'active_certs': active_certs,
        'expiring_soon': expiring_soon,
        'expired_certs': expired_certs,
        'team_certifications': team_certifications,
        'stats': stats,
        'renewal_reminders': renewal_reminders,
        'timeline_items': timeline_items[:20],
        'has_certification_model': has_certification_model,
    }

    return render(request, 'training/certification_tracking.html', context)
