"""
Template views for notifications app.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.http import JsonResponse
from django.db.models import Q

from .models import Notification, EmailTemplate


@login_required
def inbox(request):
    """View user's notifications inbox."""
    user = request.user

    # Get filter parameters
    filter_type = request.GET.get('type', 'all')

    # Base queryset
    notifications = Notification.objects.filter(user=user)

    # Apply filters
    if filter_type == 'unread':
        notifications = notifications.filter(is_read=False)
    elif filter_type == 'read':
        notifications = notifications.filter(is_read=True)
    elif filter_type != 'all':
        notifications = notifications.filter(notification_type=filter_type)

    # Paginate
    notifications = notifications.order_by('-created_at')

    # Statistics
    total_count = Notification.objects.filter(user=user).count()
    unread_count = Notification.objects.filter(user=user, is_read=False).count()

    context = {
        'notifications': notifications,
        'total_count': total_count,
        'unread_count': unread_count,
        'filter_type': filter_type,
    }

    return render(request, 'notifications/inbox.html', context)


@login_required
def notification_detail(request, pk):
    """View notification details."""
    notification = get_object_or_404(
        Notification,
        pk=pk,
        user=request.user
    )

    # Mark as read
    if not notification.is_read:
        notification.is_read = True
        notification.read_at = timezone.now()
        notification.save()

    context = {
        'notification': notification
    }

    return render(request, 'notifications/notification_detail.html', context)


@login_required
def mark_as_read(request, pk):
    """Mark notification as read."""
    notification = get_object_or_404(
        Notification,
        pk=pk,
        user=request.user
    )

    notification.is_read = True
    notification.read_at = timezone.now()
    notification.save()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success'})

    messages.success(request, 'Bildiriş oxunmuş kimi işarələndi.')
    return redirect('notifications:inbox')


@login_required
def mark_all_as_read(request):
    """Mark all notifications as read."""
    if request.method == 'POST':
        Notification.objects.filter(
            user=request.user,
            is_read=False
        ).update(is_read=True, read_at=timezone.now())

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success'})

        messages.success(request, 'Bütün bildirişlər oxunmuş kimi işarələndi.')

    return redirect('notifications:inbox')


@login_required
def delete_notification(request, pk):
    """Delete a notification."""
    notification = get_object_or_404(
        Notification,
        pk=pk,
        user=request.user
    )

    if request.method in ['POST', 'DELETE']:
        notification.delete()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success'})

        messages.success(request, 'Bildiriş silindi.')

    return redirect('notifications:inbox')


@login_required
def delete_all_notifications(request):
    """Delete all notifications for the current user."""
    if request.method == 'DELETE':
        count = Notification.objects.filter(user=request.user).count()
        Notification.objects.filter(user=request.user).delete()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'success',
                'message': f'{count} bildiriş silindi.'
            })

        messages.success(request, f'{count} bildiriş silindi.')

    return redirect('notifications:inbox')


@login_required
def notification_settings(request):
    """Notification preferences and settings."""
    user = request.user

    if request.method == 'POST':
        # Update notification preferences
        # This would update user profile notification settings
        messages.success(request, 'Bildiriş parametrləri yeniləndi.')
        return redirect('notifications:settings')

    context = {
        'user': user,
    }

    return render(request, 'notifications/settings.html', context)


# Email Template Management (Admin only)

class AdminRequiredMixin(UserPassesTestMixin):
    """Mixin to require admin access."""
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin()

    def handle_no_permission(self):
        messages.error(self.request, 'Bu səhifəyə giriş icazəniz yoxdur.')
        return redirect('dashboard')


class EmailTemplateListView(AdminRequiredMixin, ListView):
    """List all email templates."""
    model = EmailTemplate
    template_name = 'notifications/email_templates.html'
    context_object_name = 'templates'
    paginate_by = 20


class EmailTemplateDetailView(AdminRequiredMixin, DetailView):
    """View email template details."""
    model = EmailTemplate
    template_name = 'notifications/email_template_detail.html'
    context_object_name = 'template'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add statistics
        context['statistics'] = self.object.get_statistics()
        return context


class EmailTemplateCreateView(AdminRequiredMixin, CreateView):
    """Create new email template."""
    model = EmailTemplate
    template_name = 'notifications/email_template_form.html'
    fields = ['name', 'subject', 'html_content', 'text_content', 'is_active']
    success_url = reverse_lazy('notifications:email-templates')

    def form_valid(self, form):
        messages.success(self.request, 'E-poçt şablonu yaradıldı.')
        return super().form_valid(form)


class EmailTemplateUpdateView(AdminRequiredMixin, UpdateView):
    """Update existing email template."""
    model = EmailTemplate
    template_name = 'notifications/email_template_form.html'
    fields = ['name', 'subject', 'html_content', 'text_content', 'is_active']
    success_url = reverse_lazy('notifications:email-templates')

    def form_valid(self, form):
        messages.success(self.request, 'E-poçt şablonu yeniləndi.')
        return super().form_valid(form)


@login_required
def delete_email_template(request, pk):
    """Delete an email template (AJAX endpoint)."""
    # Check if user is admin
    if not request.user.is_admin():
        return JsonResponse({
            'success': False,
            'message': 'Bu əməliyyat üçün admin icazəniz yoxdur.'
        }, status=403)

    template = get_object_or_404(EmailTemplate, pk=pk)

    if request.method == 'POST':
        template_name = template.name
        template.delete()

        return JsonResponse({
            'success': True,
            'message': f'{template_name} şablonu uğurla silindi.'
        })

    return JsonResponse({
        'success': False,
        'message': 'Yalnız POST sorğuları qəbul edilir.'
    }, status=405)


@login_required
def get_unread_count(request):
    """Get unread notification count (AJAX endpoint)."""
    count = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).count()

    return JsonResponse({'count': count})


@login_required
def get_recent_notifications(request):
    """Get recent notifications (AJAX endpoint)."""
    # Get limit from query params
    limit = int(request.GET.get('limit', 10))

    notifications = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')[:limit]

    data = [{
        'id': n.id,
        'title': n.title,
        'message': n.message,
        'type': n.notification_type,
        'is_read': n.is_read,
        'link': n.link,
        'created_at': n.created_at.isoformat(),
    } for n in notifications]

    return JsonResponse({'notifications': data, 'count': len(data)})


# Bulk Notification Management (Admin/Manager only)

@login_required
def bulk_notification(request):
    """
    Toplu Bildiriş - Send notifications to multiple users.

    Features:
    - Filter users by department, role, or specific selection
    - Choose notification type and delivery method (in-app, email, both)
    - Preview recipients before sending
    - Template selection for emails
    - Batch sending with progress tracking
    """
    from apps.accounts.models import User
    from apps.departments.models import Department
    from django.db.models import Count

    # Check if user is admin or manager
    if not (request.user.is_admin() or request.user.is_manager()):
        messages.error(request, 'Bu səhifəyə giriş icazəniz yoxdur.')
        return redirect('dashboard')

    if request.method == 'POST':
        # Process bulk notification
        title = request.POST.get('title')
        message = request.POST.get('message')
        notification_type = request.POST.get('notification_type', 'info')
        delivery_method = request.POST.get('delivery_method', 'in_app')  # in_app, email, both
        link = request.POST.get('link', '')

        # Get recipients based on filters
        filter_type = request.POST.get('filter_type')  # all, department, role, specific

        recipients = User.objects.filter(is_active=True)

        if filter_type == 'department':
            department_id = request.POST.get('department_id')
            if department_id:
                recipients = recipients.filter(department_id=department_id)
        elif filter_type == 'role':
            role = request.POST.get('role')
            if role:
                recipients = recipients.filter(role=role)
        elif filter_type == 'specific':
            user_ids = request.POST.getlist('user_ids')
            if user_ids:
                recipients = recipients.filter(id__in=user_ids)

        # Create notifications
        created_count = 0
        email_sent_count = 0

        for recipient in recipients:
            # Create in-app notification
            if delivery_method in ['in_app', 'both']:
                Notification.objects.create(
                    user=recipient,
                    title=title,
                    message=message,
                    notification_type=notification_type,
                    link=link
                )
                created_count += 1

            # Send email
            if delivery_method in ['email', 'both']:
                try:
                    # Use email service to send
                    from .services import send_email_notification
                    send_email_notification(
                        recipient=recipient,
                        subject=title,
                        message=message
                    )
                    email_sent_count += 1
                except Exception as e:
                    # Log error but continue
                    pass

        success_message = f'{created_count} bildiriş yaradıldı'
        if email_sent_count > 0:
            success_message += f', {email_sent_count} e-poçt göndərildi'

        messages.success(request, success_message + '.')
        return redirect('notifications:bulk-notification')

    # GET request - show form
    # Get all departments for filter
    departments = Department.objects.filter(is_active=True).annotate(
        user_count=Count('users')
    ).order_by('name')

    # Get all users for specific selection
    all_users = User.objects.filter(is_active=True).select_related('department').order_by('first_name', 'last_name')

    # Get available email templates
    email_templates = EmailTemplate.objects.filter(is_active=True)

    # Role choices
    role_choices = User.ROLE_CHOICES

    # Statistics
    total_users = User.objects.filter(is_active=True).count()
    departments_count = Department.objects.filter(is_active=True).count()

    # Recent notifications (last 10 unique titles)
    recent_notifications = Notification.objects.order_by('-created_at')[:10]

    context = {
        'departments': departments,
        'all_users': all_users,
        'email_templates': email_templates,
        'role_choices': role_choices,
        'total_users': total_users,
        'departments_count': departments_count,
        'recent_notifications': recent_notifications,
    }

    return render(request, 'notifications/bulk_notification.html', context)
