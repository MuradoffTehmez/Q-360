"""
Template views for development plans (IDP - Individual Development Plan).
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone

from .models import DevelopmentGoal, ProgressLog
from .forms import DevelopmentGoalForm, ProgressLogForm


@login_required
def my_goals(request):
    """View current user's development goals."""
    user = request.user

    # Get goals
    active_goals = DevelopmentGoal.objects.filter(
        user=user,
        status='active'
    ).order_by('target_date')

    completed_goals = DevelopmentGoal.objects.filter(
        user=user,
        status='completed'
    ).order_by('-completion_date')[:5]

    draft_goals = DevelopmentGoal.objects.filter(
        user=user,
        status='draft'
    )

    # Statistics
    total_goals = DevelopmentGoal.objects.filter(user=user).count()
    completed_count = DevelopmentGoal.objects.filter(user=user, status='completed').count()
    completion_rate = (completed_count / total_goals * 100) if total_goals > 0 else 0

    context = {
        'active_goals': active_goals,
        'completed_goals': completed_goals,
        'draft_goals': draft_goals,
        'total_goals': total_goals,
        'completed_count': completed_count,
        'completion_rate': completion_rate,
    }

    return render(request, 'development_plans/my_goals.html', context)


class GoalDetailView(LoginRequiredMixin, DetailView):
    """View goal details with progress logs."""
    model = DevelopmentGoal
    template_name = 'development_plans/goal_detail.html'
    context_object_name = 'goal'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        goal = self.object

        # Progress logs
        context['progress_logs'] = goal.progress_logs.order_by('-created_at')

        # Calculate progress
        if goal.progress_logs.exists():
            latest_log = goal.progress_logs.first()
            context['current_progress'] = latest_log.progress_percentage
        else:
            context['current_progress'] = 0

        # Days remaining
        if goal.target_date:
            delta = goal.target_date - timezone.now().date()
            context['days_remaining'] = delta.days

        return context


class GoalCreateView(LoginRequiredMixin, CreateView):
    """Create new development goal."""
    model = DevelopmentGoal
    form_class = DevelopmentGoalForm
    template_name = 'development_plans/goal_form.html'
    success_url = reverse_lazy('development-plans:my-goals')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.created_by = self.request.user
        messages.success(self.request, 'İnkişaf məqsədi yaradıldı.')
        return super().form_valid(form)


class GoalUpdateView(LoginRequiredMixin, UpdateView):
    """Update existing goal."""
    model = DevelopmentGoal
    form_class = DevelopmentGoalForm
    template_name = 'development_plans/goal_form.html'
    success_url = reverse_lazy('development-plans:my-goals')

    def get_queryset(self):
        # Users can only edit their own goals
        return DevelopmentGoal.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Məqsəd yeniləndi.')
        return super().form_valid(form)


@login_required
def goal_complete(request, pk):
    """Mark goal as completed."""
    goal = get_object_or_404(DevelopmentGoal, pk=pk, user=request.user)

    goal.status = 'completed'
    goal.completion_date = timezone.now().date()
    goal.save()

    # Add 100% progress log
    ProgressLog.objects.create(
        goal=goal,
        note='Məqsəd tamamlandı',
        progress_percentage=100,
        logged_by=request.user
    )

    messages.success(request, 'Təbriklər! Məqsəd tamamlandı.')
    return redirect('development-plans:goal-detail', pk=pk)


@login_required
def add_progress(request, goal_pk):
    """Add progress log to a goal."""
    goal = get_object_or_404(DevelopmentGoal, pk=goal_pk, user=request.user)

    if request.method == 'POST':
        form = ProgressLogForm(request.POST)
        if form.is_valid():
            progress = form.save(commit=False)
            progress.goal = goal
            progress.logged_by = request.user
            progress.save()

            messages.success(request, 'İrəliləyiş qeyd edildi.')
            return redirect('development-plans:goal-detail', pk=goal_pk)
    else:
        form = ProgressLogForm()

    context = {
        'form': form,
        'goal': goal
    }

    return render(request, 'development_plans/add_progress.html', context)


@login_required
def team_goals(request):
    """View team's development goals (for managers)."""
    if not request.user.is_manager():
        messages.error(request, 'Bu səhifəyə giriş icazəniz yoxdur.')
        return redirect('dashboard')

    # Get subordinates' goals
    if request.user.is_admin():
        goals = DevelopmentGoal.objects.filter(status='active')
    else:
        subordinates = request.user.get_subordinates()
        goals = DevelopmentGoal.objects.filter(
            user__in=subordinates,
            status='active'
        )

    goals = goals.select_related('user').order_by('target_date')

    context = {
        'goals': goals
    }

    return render(request, 'development_plans/team_goals.html', context)


@login_required
def goal_templates(request):
    """View goal templates based on evaluation results."""
    user = request.user

    # Get latest evaluation result
    from apps.evaluations.models import EvaluationResult, Response

    latest_result = EvaluationResult.objects.filter(
        evaluatee=user
    ).order_by('-calculated_at').first()

    suggestions = []

    if latest_result:
        # Get text responses for development areas
        assignments = latest_result.campaign.assignments.filter(
            evaluatee=user,
            status='completed'
        )

        development_responses = Response.objects.filter(
            assignment__in=assignments,
            question__text__icontains='inkişaf'
        ).exclude(text_answer='')

        # Create goal suggestions
        for response in development_responses[:5]:
            suggestions.append({
                'title': f'{response.question.category.name} - İnkişaf Sahəsi',
                'description': response.text_answer,
                'category': response.question.category.name
            })

    context = {
        'suggestions': suggestions,
        'latest_result': latest_result
    }

    return render(request, 'development_plans/goal_templates.html', context)
