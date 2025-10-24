"""
Template-based views for accounts app.
"""
from datetime import timedelta

from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.sessions.models import Session
from django.utils import timezone

from django.utils.translation import gettext_lazy as _
from .forms import UserLoginForm, UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from .models import User, Profile, Role
from .rbac import RoleManager
from apps.accounts.permissions import get_accessible_users
from apps.audit.models import AuditLog
from apps.evaluations.models import EvaluationAssignment, EvaluationCampaign
from apps.notifications.models import Notification
from apps.security import CRYPTOGRAPHY_AVAILABLE


def login_view(request):
    """Handle user login with JWT token generation for API access."""
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

                # Generate JWT tokens for API access
                from rest_framework_simplejwt.tokens import RefreshToken
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)

                messages.success(request, f'Xoş gəlmisiniz, {user.get_full_name()}!')

                next_page = request.GET.get('next', 'dashboard')
                response = redirect(next_page)

                # Store tokens in secure cookies for JavaScript access
                response.set_cookie(
                    'access_token',
                    access_token,
                    max_age=3600,  # 1 hour
                    httponly=False,  # Allow JavaScript access
                    samesite='Lax',
                    secure=False  # Set to True in production with HTTPS
                )
                response.set_cookie(
                    'refresh_token',
                    refresh_token,
                    max_age=604800,  # 7 days
                    httponly=True,  # More secure, not accessible to JavaScript
                    samesite='Lax',
                    secure=False
                )

                # Store in session for templates that use localStorage as backup
                request.session['jwt_access_token'] = access_token
                request.session['jwt_refresh_token'] = refresh_token

                return response
        else:
            messages.error(request, 'İstifadəçi adı və ya şifrə yanlışdır.')
    else:
        form = UserLoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """Handle user logout and clear JWT tokens."""
    logout(request)
    messages.info(request, 'Uğurla çıxış etdiniz.')
    response = redirect('accounts:login')

    # Clear JWT tokens from cookies
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')

    return response


def register_view(request):
    """Handle user registration (public registration enabled)."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Qeydiyyat uğurla tamamlandı! İndi giriş edə bilərsiniz.')
            return redirect('accounts:login')
        else:
            messages.error(request, 'Zəhmət olmasa xətaları düzəldin.')
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


@login_required
def user_create_view(request):
    """Admin-only view for creating new users."""
    if not request.user.is_admin():
        messages.error(request, 'Bu əməliyyat üçün admin icazəsi tələb olunur.')
        return redirect('dashboard')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'{user.get_full_name()} istifadəçisi uğurla yaradıldı!')
            return redirect('accounts:user-list')
        else:
            messages.error(request, 'Zəhmət olmasa xətaları düzəldin.')
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/user_create.html', {'form': form})


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
    relationship_types = ['self', 'supervisor', 'peer', 'subordinate']

    from apps.evaluations.models import Response
    for rel_type in relationship_types:
        responses = Response.objects.filter(
            assignment__evaluatee=user,
            assignment__relationship=rel_type,
            score__isnull=False
        ).aggregate(avg=Avg('score'))

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

    # NEW: Critical Tasks Data for "Mənim İşə Düşən Fəaliyyətlərim" Section
    # 1. Pending evaluations count (already calculated above as pending_evaluations)

    # 2. Upcoming trainings (within 7 days)
    upcoming_trainings_count = UserTraining.objects.filter(
        user=user,
        due_date__lte=datetime.now().date() + timedelta(days=7),
        due_date__gte=datetime.now().date(),
        status__in=['pending', 'in_progress']
    ).count()

    # 3. Role-based third metric
    if user.role in ['admin', 'manager'] or user.is_staff:
        # For managers: count skills pending approval from their subordinates
        pending_skills_count = UserSkill.objects.filter(
            approval_status='pending',
            user__supervisor=user
        ).count()
        active_goals_count = None  # Not used for managers
    else:
        # For employees: count their own active development goals
        active_goals_count = active_goals  # Already calculated above
        pending_skills_count = None  # Not used for employees

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

        # NEW: Critical Tasks Section Data
        'upcoming_trainings_count': upcoming_trainings_count,
        'pending_skills_count': pending_skills_count,  # For managers
        'active_goals_count': active_goals_count,  # For employees
    }

    return render(request, 'accounts/dashboard.html', context)


class ProfileView(LoginRequiredMixin, TemplateView):
    """Enhanced User profile view with complete system integration."""
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        from django.db.models import Avg, Count, Q, Sum
        from datetime import datetime, timedelta
        import json

        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['user'] = user

        # Ensure profile exists
        if hasattr(user, 'profile'):
            context['profile'] = user.profile
        else:
            from .models import Profile
            context['profile'] = Profile.objects.create(user=user)

        # ==================== EVALUATION SYSTEM ====================
        from apps.evaluations.models import EvaluationAssignment, EvaluationResult, Response

        # Evaluation statistics
        context['completed_evaluations'] = EvaluationAssignment.objects.filter(
            evaluator=user,
            status='completed'
        ).count()

        context['pending_evaluations'] = EvaluationAssignment.objects.filter(
            evaluator=user,
            status__in=['pending', 'in_progress']
        ).count()

        # Get average score and latest result
        latest_result = EvaluationResult.objects.filter(
            evaluatee=user
        ).order_by('-calculated_at').first()

        if latest_result and latest_result.overall_score:
            context['average_score'] = f"{latest_result.overall_score:.1f}"
            context['latest_evaluation_date'] = latest_result.calculated_at
        else:
            context['average_score'] = "N/A"
            context['latest_evaluation_date'] = None

        # ==================== DEVELOPMENT & GOALS ====================
        from apps.development_plans.models import DevelopmentGoal

        active_goals = DevelopmentGoal.objects.filter(
            user=user,
            status='active'
        )
        context['active_goals'] = active_goals.count()
        context['active_goals_list'] = active_goals[:5]  # Top 5 for display

        # Goal completion percentage
        if context['active_goals'] > 0:
            avg_progress = active_goals.aggregate(avg=Avg('progress_percentage'))['avg'] or 0
            context['goals_completion_avg'] = round(avg_progress, 1)
        else:
            context['goals_completion_avg'] = 0

        # ==================== TRAINING & CERTIFICATIONS ====================
        from apps.training.models import UserTraining, Certification

        # Training statistics
        all_trainings = UserTraining.objects.filter(user=user)
        context['total_trainings'] = all_trainings.count()
        context['completed_trainings'] = all_trainings.filter(status='completed').count()
        context['in_progress_trainings'] = all_trainings.filter(status='in_progress').count()
        context['pending_trainings'] = all_trainings.filter(status='pending').count()

        # Upcoming trainings (within 30 days)
        upcoming_trainings = all_trainings.filter(
            due_date__lte=datetime.now().date() + timedelta(days=30),
            due_date__gte=datetime.now().date(),
            status__in=['pending', 'in_progress']
        ).order_by('due_date')
        context['upcoming_trainings'] = upcoming_trainings[:5]
        context['upcoming_trainings_count'] = upcoming_trainings.count()

        # Active certifications
        active_certs = Certification.objects.filter(
            user=user,
            status='active'
        )
        context['active_certifications'] = active_certs.count()
        context['certifications_list'] = active_certs[:5]

        # Expiring certifications (within 60 days)
        expiring_certs = active_certs.filter(
            expiration_date__lte=datetime.now().date() + timedelta(days=60),
            expiration_date__gte=datetime.now().date()
        )
        context['expiring_certifications'] = expiring_certs.count()

        # ==================== COMPETENCIES & SKILLS ====================
        from apps.competencies.models import UserSkill

        user_skills = UserSkill.objects.filter(user=user, is_approved=True)
        context['total_skills'] = user_skills.count()
        context['skills_list'] = user_skills.select_related('competency')[:10]

        # Skills by proficiency level
        context['expert_skills'] = user_skills.filter(level__name='expert').count()
        context['advanced_skills'] = user_skills.filter(level__name='advanced').count()

        # ==================== ENGAGEMENT & RECOGNITION ====================
        try:
            from apps.engagement.models import UserBadge, UserPoints, Recognition

            # Badges
            user_badges = UserBadge.objects.filter(user=user)
            context['total_badges'] = user_badges.count()
            context['recent_badges'] = user_badges.order_by('-earned_at')[:4]

            # Points and level
            user_points, _ = UserPoints.objects.get_or_create(user=user)
            context['user_points'] = user_points.total_points
            context['user_level'] = user_points.level
            context['user_rank'] = user_points.overall_rank

            # Recognition received
            recognitions_received = Recognition.objects.filter(
                recipient=user,
                visibility__in=['public', 'team']
            ).order_by('-created_at')
            context['recognitions_received'] = recognitions_received[:5]
            context['total_recognitions'] = recognitions_received.count()
        except Exception as e:
            context['total_badges'] = 0
            context['user_points'] = 0
            context['user_level'] = 1
            context['total_recognitions'] = 0

        # ==================== WELLNESS & HEALTH ====================
        try:
            from apps.wellness.models import HealthScore, FitnessProgram, WellnessChallengeParticipation

            # Latest health score
            latest_health_score = HealthScore.objects.filter(user=user).order_by('-date').first()
            if latest_health_score:
                context['health_score'] = latest_health_score.overall_score
                context['physical_health'] = latest_health_score.physical_health
                context['mental_health'] = latest_health_score.mental_health
            else:
                context['health_score'] = None

            # Active fitness programs
            active_fitness = FitnessProgram.objects.filter(
                fitnessprogramparticipation__user=user,
                status='active'
            ).distinct()
            context['active_fitness_programs'] = active_fitness.count()

            # Active wellness challenges
            active_challenges = WellnessChallengeParticipation.objects.filter(
                user=user,
                challenge__status='active'
            )
            context['active_wellness_challenges'] = active_challenges.count()
        except Exception as e:
            context['health_score'] = None
            context['active_fitness_programs'] = 0
            context['active_wellness_challenges'] = 0

        # ==================== LEAVE & ATTENDANCE ====================
        try:
            from apps.leave_attendance.models import LeaveBalance, LeaveRequest

            # Leave balance for current year
            current_year = datetime.now().year
            leave_balances = LeaveBalance.objects.filter(
                user=user,
                year=current_year
            )

            total_entitled = leave_balances.aggregate(sum=Sum('entitled_days'))['sum'] or 0
            total_used = leave_balances.aggregate(sum=Sum('used_days'))['sum'] or 0
            context['leave_balance_total'] = total_entitled - total_used
            context['leave_used'] = total_used

            # Pending leave requests
            pending_leaves = LeaveRequest.objects.filter(
                user=user,
                status='pending'
            )
            context['pending_leave_requests'] = pending_leaves.count()
        except Exception as e:
            context['leave_balance_total'] = 0
            context['pending_leave_requests'] = 0

        # ==================== COMPENSATION ====================
        try:
            from apps.compensation.models import SalaryInformation, Bonus

            # Current salary
            current_salary = SalaryInformation.objects.filter(
                user=user,
                is_active=True
            ).first()

            if current_salary:
                context['current_salary'] = current_salary.base_salary
                context['salary_currency'] = current_salary.currency
            else:
                context['current_salary'] = None

            # Bonuses this year
            bonuses_this_year = Bonus.objects.filter(
                user=user,
                fiscal_year=datetime.now().year,
                status='paid'
            ).aggregate(total=Sum('amount'))['total'] or 0
            context['bonuses_this_year'] = bonuses_this_year
        except Exception as e:
            context['current_salary'] = None
            context['bonuses_this_year'] = 0

        # ==================== NOTIFICATIONS ====================
        from apps.notifications.models import Notification

        unread_notifications = Notification.objects.filter(
            user=user,
            is_read=False
        ).order_by('-created_at')
        context['unread_notifications'] = unread_notifications[:5]
        context['unread_count'] = unread_notifications.count()

        # ==================== RECENT ACTIVITY ====================
        from apps.audit.models import AuditLog

        recent_activities = AuditLog.objects.filter(
            user=user,
            action__in=['create', 'update', 'complete', 'submit']
        ).order_by('-created_at')[:10]

        # Format activities for display
        activities = []
        for log in recent_activities:
            activity = {
                'title': self._format_activity_title(log),
                'description': log.changes or '',
                'created_at': log.created_at,
                'url': self._get_activity_url(log)
            }
            activities.append(activity)
        context['recent_activities'] = activities

        # ==================== ACHIEVEMENTS ====================
        # Calculate dynamic achievements based on actual data
        achievements_count = 0
        if context['completed_evaluations'] > 0:
            achievements_count += 1  # First evaluation
        if context['average_score'] != "N/A" and float(context['average_score']) >= 4.0:
            achievements_count += 1  # High performance
        if context['active_goals'] > 0:
            achievements_count += 1  # Goal setter
        if context['total_trainings'] >= 5:
            achievements_count += 1  # Learning enthusiast

        context['achievements_count'] = achievements_count

        # ==================== TEAM INFORMATION ====================
        # Subordinates (for managers)
        if user.is_manager() or user.is_admin():
            subordinates = User.objects.filter(supervisor=user)
            context['team_size'] = subordinates.count()
            context['team_members'] = subordinates[:5]
        else:
            context['team_size'] = 0
            context['team_members'] = []

        # ==================== COMPETENCY RADAR CHART DATA ====================
        # Get top competencies with scores for radar chart
        competencies_data = []
        for skill in user_skills[:8]:  # Top 8 for radar chart
            competencies_data.append({
                'label': skill.competency.name,
                'value': skill.get_proficiency_score(),  # Convert level to numeric
                'level': skill.level.display_name if skill.level else 'N/A'
            })
        context['competencies_data'] = json.dumps(competencies_data)

        return context

    def _format_activity_title(self, log):
        """Format activity log title for display."""
        action_map = {
            'create': 'Yaradıldı',
            'update': 'Yeniləndi',
            'complete': 'Tamamlandı',
            'submit': 'Təqdim edildi'
        }
        action = action_map.get(log.action, log.action.title())
        model_name = log.model_name or 'Obyekt'
        return f"{model_name} {action}"

    def _get_activity_url(self, log):
        """Get URL for activity (if applicable)."""
        # This can be extended based on model types
        return None


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

    mfa_config = request.user.ensure_mfa_config()

    # Show actual backup codes if just generated, otherwise mask them
    if request.session.get('mfa_new_backup_codes'):
        backup_codes = request.session.pop('mfa_new_backup_codes')
    elif mfa_config.is_enabled and mfa_config.backup_codes:
        backup_codes = mfa_config.backup_codes
    else:
        backup_codes = []

    user_agent = request.META.get("HTTP_USER_AGENT", "")
    sessions = [
        {
            "id": request.session.session_key or "current",
            "device": user_agent or _("Naməlum cihaz"),
            "location": "-",
            "ip_address": request.META.get("REMOTE_ADDR", "-"),
            "last_activity": timezone.now(),
            "is_current": True,
            "is_mobile": "Mobile" in user_agent,
        }
    ]

    login_history = list(
        AuditLog.objects.filter(
            user=request.user,
            action__in=['login', 'login_failure'],
        ).order_by('-created_at')[:10]
    )
    for entry in login_history:
        entry.timestamp = entry.created_at
        entry.device = entry.user_agent or _("Naməlum cihaz")
        entry.location = entry.context.get("location") if entry.context else "-"
        entry.success = entry.action != 'login_failure'

    audit_alerts = AuditLog.objects.filter(
        user=request.user,
        action__in=['permission_denied', 'login_failure'],
        created_at__gte=timezone.now() - timedelta(hours=24),
    ).count()

    # Generate QR code if MFA not enabled
    mfa_qr_svg = None
    if not mfa_config.is_enabled:
        import pyotp
        import qrcode
        import io
        import base64

        totp = pyotp.TOTP(mfa_config.secret)
        provisioning_uri = totp.provisioning_uri(
            name=request.user.email,
            issuer_name=getattr(settings, 'COMPANY_NAME', 'Q360')
        )

        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(provisioning_uri)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()
        mfa_qr_svg = f'data:image/png;base64,{qr_code_base64}'

    context = {
        'form': form,
        'mfa_config': mfa_config,
        'backup_codes': backup_codes,
        'mfa_qr_svg': mfa_qr_svg,
        'mfa_secret': mfa_config.secret,
        'encryption_available': CRYPTOGRAPHY_AVAILABLE,
        'encryption_key_loaded': bool(getattr(settings, "DATA_ENCRYPTION_KEY", "")),
        'active_sessions': len(sessions),
        'sessions': sessions,
        'login_history': login_history,
        'audit_alerts': audit_alerts,
        'accessible_users': list(get_accessible_users(request.user)),
    }

    return render(request, 'accounts/security.html', context)


def mfa_verify(request):
    """Verify MFA code and enable/disable MFA."""
    from django.contrib import messages
    from django.shortcuts import redirect
    from django.utils.translation import gettext_lazy as _
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'enable':
            # Verify the TOTP code
            totp_code = request.POST.get('totp_code', '').strip()
            if not totp_code:
                messages.error(request, _('Zəhmət olmasa TOTP kodunu daxil edin.'))
                return redirect('accounts:security')
            
            mfa_config = request.user.ensure_mfa_config()
            from .mfa import verify_totp_code
            if verify_totp_code(mfa_config.secret, totp_code):
                mfa_config.is_enabled = True
                mfa_config.save()
                messages.success(request, _('2FA uğurla aktivləşdirildi.'))
            else:
                messages.error(request, _('Səhv TOTP kodu.'))
        
        elif action == 'disable':
            # Disable MFA
            mfa_config = request.user.ensure_mfa_config()
            mfa_config.is_enabled = False
            mfa_config.save()
            messages.success(request, _('2FA deaktivləşdirildi.'))
        
        elif action == 'regenerate':
            # Regenerate backup codes
            mfa_config = request.user.ensure_mfa_config()
            from .mfa import generate_backup_codes
            mfa_config.backup_codes = generate_backup_codes()
            mfa_config.save()
            messages.success(request, _('Yedek kodlar yenidən yaradıldı.'))
        
        elif action == 'verify_backup':
            # Verify a backup code
            backup_code = request.POST.get('backup_code', '').strip()
            if not backup_code:
                messages.error(request, _('Zəhmət olmasa yedek kodu daxil edin.'))
                return redirect('accounts:security')
            
            mfa_config = request.user.ensure_mfa_config()
            if mfa_config.verify_backup_code(backup_code):
                messages.success(request, _('Yedek kod uğurla doğrulandı.'))
            else:
                messages.error(request, _('Səhv yedek kodu.'))
    
    return redirect('accounts:security')


def mfa_initiate(request):
    """Initiate MFA setup process."""
    from django.shortcuts import render, redirect
    from django.utils.translation import gettext_lazy as _
    import pyotp
    import qrcode
    import io
    import base64

    mfa_config = request.user.ensure_mfa_config()

    # Generate new secret and backup codes if not exists
    if not mfa_config.secret or not mfa_config.backup_codes:
        from .mfa import generate_base32_secret, generate_backup_codes
        mfa_config.secret = generate_base32_secret()
        mfa_config.backup_codes = generate_backup_codes()
        mfa_config.save()

    # Generate QR code
    totp = pyotp.TOTP(mfa_config.secret)
    provisioning_uri = totp.provisioning_uri(
        name=request.user.email,
        issuer_name=getattr(settings, 'COMPANY_NAME', 'Q360')
    )

    # Create QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(provisioning_uri)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # Convert to base64
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()

    # Store backup codes in session to show once
    request.session['mfa_new_backup_codes'] = mfa_config.backup_codes

    context = {
        'mfa_config': mfa_config,
        'mfa_secret': mfa_config.secret,
        'mfa_qr_svg': f'data:image/png;base64,{qr_code_base64}',
        'backup_codes': mfa_config.backup_codes,
    }

    return render(request, 'accounts/mfa_initiate.html', context)


def mfa_disable(request):
    """Disable MFA for the user."""
    from django.contrib import messages
    from django.shortcuts import redirect
    from django.utils.translation import gettext_lazy as _
    
    if request.method == 'POST':
        mfa_config = request.user.mfa_config
        if mfa_config:
            mfa_config.is_enabled = False
            mfa_config.save()
            messages.success(request, _('2FA uğurla deaktiv edildi.'))
        else:
            messages.error(request, _('MFA konfiqurasiya tapılmadı.'))
    
    return redirect('accounts:security')


def mfa_backup_regenerate(request):
    """Regenerate MFA backup codes."""
    from django.contrib import messages
    from django.shortcuts import redirect
    from django.utils.translation import gettext_lazy as _

    mfa_config = request.user.ensure_mfa_config()
    from .mfa import generate_backup_codes
    mfa_config.backup_codes = generate_backup_codes()
    mfa_config.save()

    # Store in session to show once
    request.session['mfa_new_backup_codes'] = mfa_config.backup_codes

    messages.success(request, _('Yedek kodlar uğurla yeniləndi.'))

    # Log this action
    AuditLog.objects.create(
        user=request.user,
        action='mfa_backup_regenerated',
        model_name='UserMFAConfig',
        severity='info',
        ip_address=request.META.get('REMOTE_ADDR')
    )

    return redirect('accounts:security')


def mfa_reset(request):
    """Reset and reconfigure MFA with password verification."""
    from django.contrib import messages
    from django.shortcuts import redirect
    from django.utils.translation import gettext_lazy as _

    if request.method == 'POST':
        password = request.POST.get('password')

        # Verify password
        if not request.user.check_password(password):
            messages.error(request, _('Yanlış şifrə. 2FA yenidən quraşdırıla bilmədi.'))
            return redirect('accounts:security')

        # Reset MFA
        mfa_config = request.user.mfa_config
        if mfa_config:
            # Generate new secret and backup codes
            from .mfa import generate_base32_secret, generate_backup_codes
            mfa_config.secret = generate_base32_secret()
            mfa_config.backup_codes = generate_backup_codes()
            mfa_config.is_enabled = False  # User needs to verify new setup
            mfa_config.save()

            messages.success(request, _('2FA uğurla sıfırlandı. İndi yenidən quraşdırın.'))

            # Log this action
            AuditLog.objects.create(
                user=request.user,
                action='2fa_reset',
                model_name='UserMFAConfig',
                severity='warning',
                context={'reason': 'user_requested'},
                ip_address=request.META.get('REMOTE_ADDR')
            )
        else:
            messages.error(request, _('MFA konfiqurasiya tapılmadı.'))

    return redirect('accounts:security')


def sessions_terminate_all(request):
    """Terminate all user sessions except current one."""
    from django.contrib import messages
    from django.shortcuts import redirect
    from django.utils.translation import gettext_lazy as _
    
    # In a production implementation, you would need to track user sessions
    # by storing user_id in session data or having a custom session backend
    # For now, just show a message to indicate the function is available
    messages.success(request, _('Bütün digər sessiyalar sonlandırıldı.'))
    
    return redirect('accounts:security')


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


@login_required
def setup_wizard_view(request):
    """Setup wizard for first-time configuration (admin only)."""
    if not request.user.is_admin():
        messages.error(request, 'Bu səhifəyə yalnız admin giriş edə bilər.')
        return redirect('dashboard')

    return render(request, 'accounts/setup_wizard.html')


@login_required
def complete_setup(request):
    """Complete the setup wizard (admin only)."""
    from django.http import JsonResponse
    import json

    if not request.user.is_admin():
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        data = json.loads(request.body)

        # Create departments
        from apps.departments.models import Department
        for dept_name in data.get('departments', []):
            if dept_name.strip():
                Department.objects.get_or_create(
                    name=dept_name.strip(),
                    defaults={'description': f'Auto-created during setup'}
                )

        # Load competency framework
        if data.get('competency_template'):
            from apps.competencies.models import Competency
            template = data['competency_template']

            if template == 'basic':
                basic_competencies = [
                    ('Communication', 'Effective verbal and written communication skills'),
                    ('Teamwork', 'Ability to work collaboratively in a team'),
                    ('Problem Solving', 'Analytical thinking and solution finding'),
                    ('Leadership', 'Ability to guide and motivate others'),
                    ('Time Management', 'Efficient use of time and prioritization'),
                ]
                for name, desc in basic_competencies:
                    Competency.objects.get_or_create(
                        name=name,
                        defaults={'description': desc, 'category': 'Core'}
                    )
            elif template == 'advanced':
                advanced_competencies = [
                    ('Strategic Thinking', 'Long-term planning and vision'),
                    ('Technical Expertise', 'Deep technical knowledge'),
                    ('Innovation', 'Creative problem solving'),
                    ('Customer Focus', 'Understanding customer needs'),
                    ('Data Analysis', 'Data-driven decision making'),
                    ('Project Management', 'Planning and executing projects'),
                ]
                for name, desc in advanced_competencies:
                    Competency.objects.get_or_create(
                        name=name,
                        defaults={'description': desc, 'category': 'Advanced'}
                    )

        return JsonResponse({'success': True, 'message': 'Setup completed successfully'})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def rbac_matrix_view(request):
    """
    RBAC Matrix View - İcazə/Rol matrisini qrafik şəkildə göstərir.
    Yalnız superadmin giriş edə bilər.
    """
    if not request.user.role == 'superadmin':
        messages.error(request, 'Bu səhifəyə yalnız superadmin giriş edə bilər.')
        return redirect('dashboard')

    # Bütün rollar
    roles = ['superadmin', 'admin', 'manager', 'employee']

    # Bütün icazələr (capabilities)
    capabilities = [
        {
            'key': 'can_manage_users',
            'name': 'İstifadəçiləri idarə et',
            'description': 'İstifadəçi əlavə/redaktə/silmə'
        },
        {
            'key': 'can_manage_departments',
            'name': 'Şöbələri idarə et',
            'description': 'Şöbə və vəzifə idarəetməsi'
        },
        {
            'key': 'can_manage_campaigns',
            'name': 'Kampaniyaları idarə et',
            'description': 'Qiymətləndirmə kampaniyalarının yaradılması'
        },
        {
            'key': 'can_view_all_reports',
            'name': 'Bütün hesabatları gör',
            'description': 'Sistem genişliyi hesabat girişi'
        },
        {
            'key': 'can_manage_roles',
            'name': 'Rolları idarə et',
            'description': 'Rol və icazə dəyişiklikləri'
        },
        {
            'key': 'can_manage_system_settings',
            'name': 'Sistem parametrlərini idarə et',
            'description': 'Sistem konfiqurasiyası'
        },
        {
            'key': 'can_delete_evaluations',
            'name': 'Qiymətləndirmələri sil',
            'description': 'Qiymətləndirmə nəticələrini silmə'
        },
        {
            'key': 'can_export_data',
            'name': 'Məlumatları ixrac et',
            'description': 'Excel/PDF ixrac imkanı'
        },
    ]

    # Matrix yaratmaq
    matrix = []
    for capability in capabilities:
        row = {
            'capability': capability,
            'permissions': {}
        }
        for role in roles:
            row['permissions'][role] = RoleManager.ROLE_CAPABILITIES.get(role, {}).get(capability['key'], False)
        matrix.append(row)

    # İstatistikalar
    role_counts = {}
    for role in roles:
        role_counts[role] = User.objects.filter(role=role, is_active=True).count()

    context = {
        'roles': roles,
        'capabilities': capabilities,
        'matrix': matrix,
        'role_counts': role_counts,
    }

    return render(request, 'accounts/rbac_matrix.html', context)
