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
    """
    Enhanced AI-powered goal suggestions based on:
    1. Evaluation results (low scoring categories)
    2. Skill gaps (position requirements vs current skills)
    3. Feedback comments
    """
    user = request.user

    # Get latest evaluation result
    from apps.evaluations.models import EvaluationResult, Response, EvaluationAssignment
    from apps.competencies.models import UserSkill, PositionCompetency

    latest_result = EvaluationResult.objects.filter(
        evaluatee=user
    ).order_by('-calculated_at').first()

    suggestions = []

    # 1. EVALUATION-BASED SUGGESTIONS
    if latest_result:
        # Get low-scoring categories (below 3.5)
        assignments = EvaluationAssignment.objects.filter(
            campaign=latest_result.campaign,
            evaluatee=user,
            status='completed'
        )

        category_scores = {}
        for assignment in assignments:
            responses = Response.objects.filter(
                assignment=assignment,
                score__isnull=False
            ).select_related('question__category')

            for response in responses:
                cat_name = response.question.category.name
                if cat_name not in category_scores:
                    category_scores[cat_name] = []
                category_scores[cat_name].append(response.score)

        # Find low-scoring categories
        for category, scores in category_scores.items():
            avg_score = sum(scores) / len(scores) if scores else 0
            if avg_score < 3.5:  # Below threshold
                suggestions.append({
                    'title': f'{category} sahəsində təkmilləşdirmə',
                    'description': f'Qiymətləndirmə nəticələrinə görə "{category}" sahəsində ortalama {avg_score:.1f} bal aldınız. Bu sahədə inkişaf etməyi məsləhət edirik.',
                    'category': category,
                    'source': 'evaluation',
                    'priority': 'high' if avg_score < 3.0 else 'medium',
                    'score': round(avg_score, 2)
                })

        # Get text feedback
        development_responses = Response.objects.filter(
            assignment__in=assignments,
            question__text__icontains='inkişaf'
        ).exclude(text_answer='')[:3]

        for response in development_responses:
            suggestions.append({
                'title': f'{response.question.category.name} - Rəy əsaslı',
                'description': response.text_answer,
                'category': response.question.category.name,
                'source': 'feedback',
                'priority': 'medium',
                'evaluator': response.assignment.evaluator.get_full_name()
            })

    # 2. COMPETENCY GAP-BASED SUGGESTIONS
    if hasattr(user, 'position') and user.position and hasattr(user.position, 'id'):
        user_skills = UserSkill.objects.filter(user=user, is_approved=True).select_related('competency', 'level')
        user_skill_map = {
            skill.competency_id: skill.level.score_min if skill.level else 0
            for skill in user_skills
        }

        pos_competencies = PositionCompetency.objects.filter(
            position=user.position
        ).select_related('competency', 'required_level')

        for pos_comp in pos_competencies:
            current_level = user_skill_map.get(pos_comp.competency_id, 0)
            required_level = pos_comp.required_level.score_min if pos_comp.required_level else 0
            gap = required_level - current_level

            if gap > 0:
                suggestions.append({
                    'title': f'"{pos_comp.competency.name}" səriştəsini təkmilləşdirin',
                    'description': f'Vəzifəniz üçün "{pos_comp.required_level.name}" səviyyəsi tələb olunur, hal-hazırda {"heç bir səviyyədə deyilsiniz" if current_level == 0 else f"{current_level} səviyyəsiniz"}. Fərq: {gap:.1f} xal.',
                    'category': 'Səriştə İnkişafı',
                    'source': 'skill_gap',
                    'priority': 'high' if gap >= 2 else 'medium',
                    'gap': round(gap, 1),
                    'competency': pos_comp.competency.name
                })

    # Sort by priority
    priority_order = {'high': 0, 'medium': 1, 'low': 2}
    suggestions.sort(key=lambda x: priority_order.get(x.get('priority', 'low'), 2))

    context = {
        'suggestions': suggestions[:10],  # Limit to top 10
        'latest_result': latest_result,
        'total_suggestions': len(suggestions),
        'high_priority': len([s for s in suggestions if s.get('priority') == 'high']),
        'medium_priority': len([s for s in suggestions if s.get('priority') == 'medium']),
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


@login_required
def goal_approve_toggle(request, pk):
    """Toggle approval status of a development goal (managers only)."""
    from django.http import JsonResponse

    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid method'})

    if not (request.user.is_manager() or request.user.is_admin()):
        return JsonResponse({'success': False, 'error': 'Permission denied'})

    goal = get_object_or_404(DevelopmentGoal, pk=pk)

    # Check if user is the goal owner's manager
    if not request.user.is_admin():
        subordinates = request.user.get_subordinates()
        if goal.user not in subordinates:
            return JsonResponse({'success': False, 'error': 'Bu məqsədi təsdiqləmək icazəniz yoxdur.'})

    # Toggle approval status based on current status
    if goal.status == 'active':
        # Remove approval - revert to pending
        goal.status = 'pending_approval'
        goal.approved_by = None
        goal.approved_at = None
        message = 'Məqsədin təsdiqi ləğv edildi.'
        is_approved = False
    else:
        # Approve - change status to active
        goal.status = 'active'
        goal.approved_by = request.user
        goal.approved_at = timezone.now()
        message = 'Məqsəd təsdiqləndi.'
        is_approved = True

    goal.save()

    # Send notification to goal owner
    from apps.notifications.utils import send_notification

    if is_approved:
        notification_message = f'"{goal.title}" məqsədiniz {request.user.get_full_name()} tərəfindən təsdiqləndi.'
        send_notification(
            recipient=goal.user,
            title='Məqsəd Təsdiqləndi',
            message=notification_message,
            notification_type='success',
            link=f'/development-plans/goals/{goal.pk}/',
            send_email=True
        )
    else:
        notification_message = f'"{goal.title}" məqsədinin təsdiqi {request.user.get_full_name()} tərəfindən ləğv edildi.'
        send_notification(
            recipient=goal.user,
            title='Məqsəd Təsdiqi Ləğv Edildi',
            message=notification_message,
            notification_type='info',
            link=f'/development-plans/goals/{goal.pk}/',
            send_email=False
        )

    messages.success(request, message)

    return JsonResponse({
        'success': True,
        'message': message,
        'is_approved': is_approved,
        'approved_by': goal.approved_by.get_full_name() if goal.approved_by else None,
        'approved_at': goal.approved_at.isoformat() if goal.approved_at else None,
        'status': goal.status
    })
