"""
Template tags for sidebar RBAC filtering.
Allows dynamic sidebar menu items based on user role.
"""
from django import template
from apps.accounts.rbac import RoleManager

register = template.Library()


# Menu visibility mapping based on role
MENU_PERMISSIONS = {
    'dashboard': {
        'all': True,  # Everyone can see dashboard
    },
    'evaluations': {
        'all': True,  # Everyone can participate in evaluations
    },
    'competencies': {
        'all': True,  # Everyone can manage their skills
    },
    'development': {
        'all': True,  # Everyone can set goals
    },
    'hr_management': {
        'manager': True,  # Manager and above
        'admin': True,
        'superadmin': True,
    },
    'wellness': {
        'all': True,  # Everyone can use wellness features
    },
    'engagement': {
        'all': True,  # Everyone can engage
    },
    'notifications': {
        'all': True,  # Everyone gets notifications
    },
    'settings': {
        'all': True,  # Everyone can manage their settings
    },
    'admin_settings': {
        'admin': True,  # Only admin and superadmin
        'superadmin': True,
    },
    # Specific menu items that need special permissions
    'user_list': {
        'manager': True,
        'admin': True,
        'superadmin': True,
    },
    'departments': {
        'admin': True,
        'superadmin': True,
    },
    'employee_files': {
        'manager': True,
        'admin': True,
        'superadmin': True,
    },
    'compensation_dashboard': {
        'manager': True,
        'admin': True,
        'superadmin': True,
    },
    'compensation_manage': {
        'admin': True,
        'superadmin': True,
    },
    'salary_list': {
        'manager': True,
        'admin': True,
        'superadmin': True,
    },
    'salary_change': {
        'admin': True,
        'superadmin': True,
    },
    'bonus_list': {
        'manager': True,
        'admin': True,
        'superadmin': True,
    },
    'compensation_history': {
        'manager': True,
        'admin': True,
        'superadmin': True,
    },
    'leave_approvals': {
        'manager': True,
        'admin': True,
        'superadmin': True,
    },
    'team_calendar': {
        'manager': True,
        'admin': True,
        'superadmin': True,
    },
    'recruitment_dashboard': {
        'manager': True,
        'admin': True,
        'superadmin': True,
    },
    'job_create': {
        'admin': True,
        'superadmin': True,
    },
    'candidate_pipeline': {
        'manager': True,
        'admin': True,
        'superadmin': True,
    },
    'job_list': {
        'manager': True,
        'admin': True,
        'superadmin': True,
    },
    'interview_calendar': {
        'manager': True,
        'admin': True,
        'superadmin': True,
    },
    'ai_screening': {
        'manager': True,
        'admin': True,
        'superadmin': True,
    },
    'video_interview': {
        'manager': True,
        'admin': True,
        'superadmin': True,
    },
    'candidate_experience': {
        'manager': True,
        'admin': True,
        'superadmin': True,
    },
    'market_benchmarking': {
        'manager': True,
        'admin': True,
        'superadmin': True,
    },
    'total_rewards': {
        'all': True,  # Everyone can see their total rewards
    },
    'sms_providers': {
        'admin': True,
        'superadmin': True,
    },
    'notification_templates': {
        'admin': True,
        'superadmin': True,
    },
    'email_templates': {
        'admin': True,
        'superadmin': True,
    },
    'delivery_logs': {
        'admin': True,
        'superadmin': True,
    },
    'bulk_notification': {
        'admin': True,
        'superadmin': True,
    },
    'campaign_builder': {
        'admin': True,
        'superadmin': True,
    },
    'competency_manage': {
        'admin': True,
        'superadmin': True,
    },
    'training_manage': {
        'admin': True,
        'superadmin': True,
    },
    'skill_matrix': {
        'manager': True,
        'admin': True,
        'superadmin': True,
    },
    'certifications': {
        'manager': True,
        'admin': True,
        'superadmin': True,
    },
    'team_goals': {
        'manager': True,
        'admin': True,
        'superadmin': True,
    },
    'goal_templates': {
        'admin': True,
        'superadmin': True,
    },
    'talent_matrix': {
        'manager': True,
        'admin': True,
        'superadmin': True,
    },
    'succession_planning': {
        'manager': True,
        'admin': True,
        'superadmin': True,
    },
    'gap_analysis': {
        'manager': True,
        'admin': True,
        'superadmin': True,
    },
    'campaign_list': {
        'manager': True,
        'admin': True,
        'superadmin': True,
    },
}


@register.simple_tag(takes_context=True)
def can_view_menu(context, menu_key):
    """
    Check if current user can view a specific menu item.

    Usage in template:
        {% can_view_menu 'dashboard' as can_view_dashboard %}
        {% if can_view_dashboard %}
            ...menu content...
        {% endif %}

    Args:
        context: Template context
        menu_key: Key from MENU_PERMISSIONS dict

    Returns:
        bool: True if user can view the menu
    """
    request = context.get('request')
    if not request or not hasattr(request, 'user'):
        return False

    user = request.user
    if not user.is_authenticated:
        return False

    permissions = MENU_PERMISSIONS.get(menu_key, {})

    # If 'all' is True, everyone can see it
    if permissions.get('all'):
        return True

    # Check role-specific permissions
    user_role = getattr(user, 'role', 'employee')

    # Check if user's role is explicitly allowed
    if permissions.get(user_role):
        return True

    # Check using RoleManager for hierarchical permissions
    # If admin is allowed and user is admin/superadmin, grant access
    if permissions.get('admin') and RoleManager.is_admin(user):
        return True

    # If manager is allowed and user is manager or above, grant access
    if permissions.get('manager') and RoleManager.is_manager(user):
        return True

    return False


@register.filter(name='has_role')
def has_role(user, role):
    """
    Check if user has a specific role or higher.

    Usage in template:
        {% if user|has_role:'manager' %}
            ...manager content...
        {% endif %}

    Args:
        user: User object
        role: Role name (employee, manager, admin, superadmin)

    Returns:
        bool: True if user has the role or higher
    """
    if not user or not user.is_authenticated:
        return False

    if role == 'superadmin':
        return RoleManager.is_superadmin(user)
    elif role == 'admin':
        return RoleManager.is_admin(user)
    elif role == 'manager':
        return RoleManager.is_manager(user)
    elif role == 'employee':
        return True  # All authenticated users are at least employees

    return False


@register.filter(name='has_capability')
def has_capability(user, capability):
    """
    Check if user has a specific capability.

    Usage in template:
        {% if user|has_capability:'can_manage_users' %}
            ...content...
        {% endif %}

    Args:
        user: User object
        capability: Capability name from ROLE_CAPABILITIES

    Returns:
        bool: True if user has the capability
    """
    if not user or not user.is_authenticated:
        return False

    return RoleManager.has_capability(user, capability)


@register.simple_tag(takes_context=True)
def get_user_role(context):
    """
    Get current user's role display name.

    Usage in template:
        {% get_user_role as user_role %}
        <p>Rol: {{ user_role }}</p>

    Returns:
        str: User's role display name
    """
    request = context.get('request')
    if not request or not hasattr(request, 'user'):
        return 'Qonaq'

    user = request.user
    if not user.is_authenticated:
        return 'Qonaq'

    role_names = {
        'superadmin': 'Super Admin',
        'admin': 'Administrator',
        'manager': 'Menecer',
        'employee': 'İşçi',
    }

    return role_names.get(user.role, 'İşçi')
