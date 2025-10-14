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
    format_filter = request.GET.get('format', '')
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
            Q(content__icontains=search_query)
        )

    if format_filter:
        trainings = trainings.filter(format=format_filter)

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

    # Format and difficulty choices
    format_choices = TrainingResource._meta.get_field('format').choices
    difficulty_choices = TrainingResource._meta.get_field('difficulty_level').choices

    context = {
        'trainings': page_obj,
        'page_obj': page_obj,
        'stats': stats,
        'search_query': search_query,
        'format_filter': format_filter,
        'difficulty_filter': difficulty_filter,
        'format_choices': format_choices,
        'difficulty_choices': difficulty_choices,
    }

    return render(request, 'training/catalog.html', context)

@login_required
def my_trainings(request):
    """User's enrolled trainings with progress."""
    # Get user's trainings
    user_trainings = UserTraining.objects.filter(user=request.user).select_related(
        'resource', 'assigned_by'
    ).prefetch_related('resource__required_competencies').order_by('-enrolled_at')

    # Filter by status if provided
    status_filter = request.GET.get('status', '')
    if status_filter:
        user_trainings = user_trainings.filter(status=status_filter)

    # Calculate statistics
    total_trainings = user_trainings.count()
    in_progress = user_trainings.filter(status='in_progress').count()
    completed = user_trainings.filter(status='completed').count()
    not_started = user_trainings.filter(status='not_started').count()

    # Calculate average progress
    avg_progress = user_trainings.filter(progress__isnull=False).aggregate(
        avg=Avg('progress')
    )['avg'] or 0

    # Recent completions (last 5)
    recent_completions = user_trainings.filter(
        status='completed',
        completion_date__isnull=False
    ).order_by('-completion_date')[:5]

    # Upcoming deadlines
    upcoming_deadlines = user_trainings.filter(
        status__in=['not_started', 'in_progress'],
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
