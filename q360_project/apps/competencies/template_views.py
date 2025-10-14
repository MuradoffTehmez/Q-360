"""Template views for competencies app."""
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, Avg
from django.core.paginator import Paginator
from .models import Competency, UserSkill, ProficiencyLevel, PositionCompetency
import json

@login_required
def competency_list(request):
    """Competency list with full backend data."""
    # Get filter parameters
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    page_number = request.GET.get('page', 1)

    # Base queryset
    competencies = Competency.objects.annotate(
        active_positions_count=Count('position_competencies', filter=Q(position_competencies__position__is_active=True)),
        total_users_with_skill=Count('user_skills', filter=Q(user_skills__is_approved=True))
    )

    # Apply filters
    if search_query:
        competencies = competencies.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )

    if status_filter:
        is_active = status_filter.lower() == 'true'
        competencies = competencies.filter(is_active=is_active)

    # Order by name
    competencies = competencies.order_by('name')

    # Pagination
    paginator = Paginator(competencies, 12)  # 12 per page
    page_obj = paginator.get_page(page_number)

    # Statistics
    stats = {
        'total': Competency.objects.filter(is_active=True).count(),
        'active': Competency.objects.filter(is_active=True).count(),
        'skills': UserSkill.objects.filter(is_approved=True).count(),
        'pending': UserSkill.objects.filter(approval_status='pending').count(),
    }

    context = {
        'competencies': page_obj,
        'page_obj': page_obj,
        'stats': stats,
        'search_query': search_query,
        'status_filter': status_filter,
        'competencies_json': json.dumps([
            {
                'id': c.id,
                'name': c.name,
                'description': c.description or '',
                'is_active': c.is_active,
                'active_positions_count': c.active_positions_count,
                'total_users_with_skill': c.total_users_with_skill,
                'updated_at': c.updated_at.isoformat() if c.updated_at else None,
            }
            for c in page_obj
        ])
    }

    return render(request, 'competencies/competency_list.html', context)

@login_required
def my_skills(request):
    """User's skills with progress tracking."""
    # Get user's skills
    user_skills = UserSkill.objects.filter(user=request.user).select_related(
        'competency', 'level', 'approved_by'
    ).order_by('-created_at')

    # Get proficiency levels
    proficiency_levels = ProficiencyLevel.objects.all().order_by('score_min')

    # Calculate statistics
    total_skills = user_skills.count()
    approved_skills = user_skills.filter(is_approved=True).count()
    pending_skills = user_skills.filter(approval_status='pending').count()

    # Average proficiency
    avg_score = user_skills.filter(is_approved=True, level__isnull=False).aggregate(
        avg=Avg('level__score_min')
    )['avg'] or 0

    # Required competencies for user's position
    required_competencies = []
    if hasattr(request.user, 'profile') and request.user.profile.position:
        required_competencies = PositionCompetency.objects.filter(
            position=request.user.profile.position
        ).select_related('competency', 'required_level')

    # Skill gap analysis
    skill_gaps = []
    for pos_comp in required_competencies:
        user_skill = user_skills.filter(competency=pos_comp.competency).first()
        if not user_skill or (user_skill.level and user_skill.level.score_min < pos_comp.required_level.score_min):
            skill_gaps.append({
                'competency': pos_comp.competency,
                'required_level': pos_comp.required_level,
                'current_level': user_skill.level if user_skill else None,
                'gap': True
            })

    context = {
        'user_skills': user_skills,
        'proficiency_levels': proficiency_levels,
        'total_skills': total_skills,
        'approved_skills': approved_skills,
        'pending_skills': pending_skills,
        'avg_score': round(avg_score, 1),
        'skill_gaps': skill_gaps,
        'required_competencies': required_competencies,
    }

    return render(request, 'competencies/my_skills.html', context)

@login_required
def competency_detail(request, pk):
    """Detailed competency view with positions and users."""
    competency = get_object_or_404(Competency, pk=pk)

    # Related positions
    position_competencies = PositionCompetency.objects.filter(
        competency=competency,
        position__is_active=True
    ).select_related('position', 'required_level').order_by('-weight')

    # Users with this skill
    user_skills = UserSkill.objects.filter(
        competency=competency,
        is_approved=True,
        user__is_active=True
    ).select_related('user', 'level').order_by('-level__score_min')[:10]

    # Statistics
    total_users = user_skills.count()
    avg_level = user_skills.aggregate(avg=Avg('level__score_min'))['avg'] or 0

    # Check if current user has this skill
    user_has_skill = UserSkill.objects.filter(
        user=request.user,
        competency=competency
    ).first()

    context = {
        'competency': competency,
        'competency_id': pk,
        'position_competencies': position_competencies,
        'user_skills': user_skills,
        'total_users': total_users,
        'avg_level': round(avg_level, 1),
        'user_has_skill': user_has_skill,
    }

    return render(request, 'competencies/competency_detail.html', context)

@login_required
def competency_manage(request):
    """Admin view for managing competencies."""
    if not hasattr(request.user, 'is_admin') or not request.user.is_admin():
        return render(request, '403.html', status=403)
    return competency_list(request)
