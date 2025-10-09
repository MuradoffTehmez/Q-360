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

        # Progress logs (exclude drafts)
        context['progress_logs'] = goal.progress_logs.filter(is_draft=False).order_by('-created_at')

        # Draft progress
        context['draft_progress'] = goal.progress_logs.filter(
            is_draft=True,
            logged_by=self.request.user
        ).first()

        # Calculate progress (only from non-draft logs)
        non_draft_logs = goal.progress_logs.filter(is_draft=False)
        if non_draft_logs.exists():
            latest_log = non_draft_logs.first()
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

    # Check for existing draft
    draft_progress = ProgressLog.objects.filter(
        goal=goal,
        logged_by=request.user,
        is_draft=True
    ).first()

    if request.method == 'POST':
        is_draft = request.POST.get('save_as_draft') == 'true'

        # If editing draft, update it; otherwise create new
        if draft_progress and is_draft:
            form = ProgressLogForm(request.POST, instance=draft_progress)
        else:
            form = ProgressLogForm(request.POST)

        if form.is_valid():
            progress = form.save(commit=False)
            progress.goal = goal
            progress.logged_by = request.user
            progress.is_draft = is_draft
            progress.save()

            if is_draft:
                messages.success(request, 'İrəliləyiş layihə kimi saxlanıldı.')
            else:
                # If there was a draft, delete it after final save
                if draft_progress and draft_progress.pk != progress.pk:
                    draft_progress.delete()
                messages.success(request, 'İrəliləyiş qeyd edildi.')

            return redirect('development-plans:goal-detail', pk=goal_pk)
    else:
        # Load draft if exists
        if draft_progress:
            form = ProgressLogForm(instance=draft_progress)
        else:
            form = ProgressLogForm()

    context = {
        'form': form,
        'goal': goal,
        'draft_progress': draft_progress
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


@login_required
def goal_approve(request, pk):
    """Approve or reject a development goal (managers only)."""
    if not (request.user.is_manager() or request.user.is_admin()):
        messages.error(request, 'Bu əməliyyatı yerinə yetirmək icazəniz yoxdur.')
        return redirect('development-plans:my-goals')

    goal = get_object_or_404(DevelopmentGoal, pk=pk)

    # Check if user is the goal owner's manager
    if not request.user.is_admin():
        subordinates = request.user.get_subordinates()
        if goal.user not in subordinates:
            messages.error(request, 'Bu məqsədi təsdiqləmək icazəniz yoxdur.')
            return redirect('development-plans:team-goals')

    # Check if goal is in pending approval status
    if goal.status != 'pending_approval':
        messages.warning(request, 'Bu məqsəd təsdiq gözləmir.')
        return redirect('development-plans:team-goals')

    if request.method == 'POST':
        action = request.POST.get('action')
        approval_note = request.POST.get('approval_note', '')

        if action == 'approve':
            goal.status = 'active'
            goal.approved_by = request.user
            goal.approved_at = timezone.now()
            goal.approval_note = approval_note
            goal.save()

            messages.success(request, f'{goal.user.get_full_name()} - "{goal.title}" məqsədi təsdiqləndi.')

            # Send notification to goal owner
            from apps.notifications.utils import send_notification
            notification_message = f'"{goal.title}" məqsədiniz {request.user.get_full_name()} tərəfindən təsdiqləndi.'
            if approval_note:
                notification_message += f'\n\nQeyd: {approval_note}'

            send_notification(
                recipient=goal.user,
                title='Məqsəd Təsdiqləndi',
                message=notification_message,
                notification_type='success',
                link=f'/development-plans/goals/{goal.pk}/',
                send_email=True
            )

        elif action == 'reject':
            goal.status = 'rejected'
            goal.approved_by = request.user
            goal.approved_at = timezone.now()
            goal.approval_note = approval_note
            goal.save()

            messages.success(request, f'{goal.user.get_full_name()} - "{goal.title}" məqsədi rədd edildi.')

            # Send notification to goal owner
            from apps.notifications.utils import send_notification
            notification_message = f'"{goal.title}" məqsədiniz {request.user.get_full_name()} tərəfindən rədd edildi.'
            if approval_note:
                notification_message += f'\n\nSəbəb: {approval_note}'
            else:
                notification_message += '\n\nZəhmət olmasa məqsədi yenidən nəzərdən keçirin və düzəliş edin.'

            send_notification(
                recipient=goal.user,
                title='Məqsəd Rədd Edildi',
                message=notification_message,
                notification_type='warning',
                link=f'/development-plans/goals/{goal.pk}/',
                send_email=True
            )

        return redirect('development-plans:team-goals')

    context = {
        'goal': goal
    }

    return render(request, 'development_plans/goal_approve.html', context)
