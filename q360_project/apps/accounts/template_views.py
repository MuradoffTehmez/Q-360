"""
Template-based views for accounts app.
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .forms import UserLoginForm, UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from .models import User, Profile
from apps.evaluations.models import EvaluationAssignment, EvaluationCampaign
from apps.notifications.models import Notification


def login_view(request):
    """Handle user login."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Xoş gəlmisiniz, {user.get_full_name()}!')

                next_page = request.GET.get('next', 'dashboard')
                return redirect(next_page)
        else:
            messages.error(request, 'İstifadəçi adı və ya şifrə yanlışdır.')
    else:
        form = UserLoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """Handle user logout."""
    logout(request)
    messages.info(request, 'Uğurla çıxış etdiniz.')
    return redirect('accounts:login')


def register_view(request):
    """Handle user registration - DISABLED for internal use."""
    messages.warning(request, 'Qeydiyyat funksiyası daxili istifadə üçün söndürülüb. Admin ilə əlaqə saxlayın.')
    return redirect('accounts:login')


@login_required
def dashboard_view(request):
    """Main dashboard view with complete backend data."""
    from django.db.models import Avg, Count
    from datetime import datetime, timedelta
    import json
    user = request.user

    # Get evaluation statistics
    pending_evaluations = EvaluationAssignment.objects.filter(
        evaluator=user,
        status__in=['pending', 'in_progress']
    ).select_related('evaluatee', 'campaign')

    completed_evaluations = EvaluationAssignment.objects.filter(
        evaluator=user,
        status='completed'
    ).select_related('evaluatee', 'campaign')

    active_campaigns = EvaluationCampaign.objects.filter(
        status='active'
    )

    # Get recent notifications
    notifications = Notification.objects.filter(
        user=user,
        is_read=False
    ).order_by('-created_at')[:5]

    # Get pending assignments (first 5)
    pending_assignments = pending_evaluations[:5]

    # Calculate average score from evaluation results
    from apps.evaluations.models import EvaluationResult
    user_results = EvaluationResult.objects.filter(
        evaluatee=user
    ).order_by('-calculated_at')

    average_score = None
    latest_result = user_results.first()
    if latest_result and latest_result.overall_score:
        average_score = f"{latest_result.overall_score:.1f}"

    # Get performance trend data (last 6 months)
    trend_labels = []
    trend_data = []

    for i in range(5, -1, -1):
        month_date = datetime.now() - timedelta(days=30 * i)
        month_name = month_date.strftime('%b')
        trend_labels.append(month_name)

        # Get average score for that month
        month_results = user_results.filter(
            calculated_at__year=month_date.year,
            calculated_at__month=month_date.month
        ).aggregate(avg=Avg('overall_score'))

        score = month_results['avg'] or 0
        trend_data.append(round(score, 1) if score else 0)

    # Get score distribution by relationship type
    score_distribution = []
    relationship_types = ['self', 'manager', 'peer', 'subordinate']

    from apps.evaluations.models import Response
    for rel_type in relationship_types:
        responses = Response.objects.filter(
            assignment__evaluatee=user,
            assignment__relationship=rel_type
        ).aggregate(avg=Avg('rating'))

        avg_score = responses['avg'] or 0
        score_distribution.append(round(avg_score, 1) if avg_score else 0)

    # Get skills and training stats
    from apps.competencies.models import UserSkill
    from apps.training.models import UserTraining

    total_skills = UserSkill.objects.filter(user=user, is_approved=True).count()
    total_trainings = UserTraining.objects.filter(user=user).count()
    in_progress_trainings = UserTraining.objects.filter(
        user=user,
        status='in_progress'
    ).count()

    # Get development goals
    from apps.development_plans.models import DevelopmentGoal
    active_goals = DevelopmentGoal.objects.filter(
        user=user,
        status='active'
    ).count()

    context = {
        # Evaluation stats
        'pending_evaluations_count': pending_evaluations.count(),
        'completed_evaluations_count': completed_evaluations.count(),
        'active_campaigns_count': active_campaigns.count(),
        'average_score': average_score,
        'pending_assignments': pending_assignments,

        # Notifications
        'notifications': notifications,

        # Charts data
        'user_stats': bool(user_results.exists()),  # Flag to enable charts
        'trend_labels': json.dumps(trend_labels),
        'trend_data': json.dumps(trend_data),
        'score_distribution': json.dumps(score_distribution),

        # Additional stats
        'total_skills': total_skills,
        'total_trainings': total_trainings,
        'in_progress_trainings': in_progress_trainings,
        'active_goals': active_goals,
    }

    return render(request, 'accounts/dashboard.html', context)


class ProfileView(LoginRequiredMixin, TemplateView):
    """User profile view."""
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['user'] = user

        # Ensure profile exists
        if hasattr(user, 'profile'):
            context['profile'] = user.profile
        else:
            # Create profile if doesn't exist
            from .models import Profile
            context['profile'] = Profile.objects.create(user=user)

        # Get evaluation statistics
        from apps.evaluations.models import EvaluationAssignment, EvaluationResult
        context['completed_evaluations'] = EvaluationAssignment.objects.filter(
            evaluator=user,
            status='completed'
        ).count()

        # Get average score
        latest_result = EvaluationResult.objects.filter(
            evaluatee=user
        ).order_by('-calculated_at').first()

        if latest_result and latest_result.overall_score:
            context['average_score'] = f"{latest_result.overall_score:.2f}"
        else:
            context['average_score'] = "N/A"

        # Get active development goals
        from apps.development_plans.models import DevelopmentGoal
        context['active_goals'] = DevelopmentGoal.objects.filter(
            user=user,
            status='active'
        ).count()

        # Achievements count (placeholder)
        context['achievements_count'] = 0

        # Recent activities (placeholder)
        context['recent_activities'] = []

        # Competencies (placeholder)
        context['competencies'] = []

        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Update user profile."""
    model = User
    form_class = UserUpdateForm
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('accounts:profile')

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['profile_form'] = ProfileUpdateForm(
                self.request.POST,
                instance=self.request.user.profile
            )
        else:
            context['profile_form'] = ProfileUpdateForm(
                instance=self.request.user.profile
            )
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        profile_form = context['profile_form']

        if profile_form.is_valid():
            form.save()
            profile_form.save()
            messages.success(self.request, 'Profil uğurla yeniləndi.')
            return redirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))


@login_required
def user_list_view(request):
    """List all users (admin only)."""
    from django.db import models as django_models

    if not request.user.is_admin():
        messages.error(request, 'Bu səhifəyə giriş icazəniz yoxdur.')
        return redirect('dashboard')

    users = User.objects.select_related('department', 'profile').all()

    # Apply filters
    role = request.GET.get('role')
    department = request.GET.get('department')
    search = request.GET.get('search')

    if role:
        users = users.filter(role=role)
    if department:
        users = users.filter(department_id=department)
    if search:
        users = users.filter(
            django_models.Q(first_name__icontains=search) |
            django_models.Q(last_name__icontains=search) |
            django_models.Q(username__icontains=search) |
            django_models.Q(email__icontains=search)
        )

    context = {
        'users': users,
        'total_users': users.count(),
    }

    return render(request, 'accounts/user_list.html', context)


@login_required
def security_settings(request):
    """Security settings - change password."""
    from django.contrib.auth.forms import PasswordChangeForm

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            from django.contrib.auth import update_session_auth_hash
            update_session_auth_hash(request, user)
            messages.success(request, 'Şifrəniz uğurla dəyişdirildi.')
            return redirect('accounts:security')
        else:
            messages.error(request, 'Zəhmət olmasa xətaları düzəldin.')
    else:
        form = PasswordChangeForm(request.user)

    context = {
        'form': form
    }

    return render(request, 'accounts/security.html', context)


def password_reset_request(request):
    """Password reset request form."""
    from django.contrib.auth.forms import PasswordResetForm

    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(
                request=request,
                use_https=request.is_secure(),
                email_template_name='accounts/password_reset_email.html',
                subject_template_name='accounts/password_reset_subject.txt'
            )
            return redirect('accounts:password-reset-done')
    else:
        form = PasswordResetForm()

    return render(request, 'accounts/password_reset.html', {'form': form})


def password_reset_done(request):
    """Password reset request submitted."""
    return render(request, 'accounts/password_reset_done.html')


def password_reset_confirm(request, uidb64, token):
    """Password reset confirmation."""
    from django.contrib.auth.forms import SetPasswordForm
    from django.contrib.auth.tokens import default_token_generator
    from django.utils.http import urlsafe_base64_decode
    from django.utils.encoding import force_str

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return redirect('accounts:password-reset-complete')
        else:
            form = SetPasswordForm(user)

        return render(request, 'accounts/password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, 'Şifrə sıfırlama linki etibarsızdır.')
        return redirect('accounts:login')


def password_reset_complete(request):
    """Password reset complete."""
    return render(request, 'accounts/password_reset_complete.html')


# Alias for change_password (same as security_settings)
change_password = security_settings
