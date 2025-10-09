"""
Template views for notifications app.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
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

    if request.method == 'POST':
        notification.delete()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success'})

        messages.success(request, 'Bildiriş silindi.')

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

class EmailTemplateListView(LoginRequiredMixin, ListView):
    """List all email templates."""
    model = EmailTemplate
    template_name = 'notifications/email_templates.html'
    context_object_name = 'templates'
    paginate_by = 20

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_admin():
            messages.error(request, 'Bu səhifəyə giriş icazəniz yoxdur.')
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)


class EmailTemplateDetailView(LoginRequiredMixin, DetailView):
    """View email template details."""
    model = EmailTemplate
    template_name = 'notifications/email_template_detail.html'
    context_object_name = 'template'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_admin():
            messages.error(request, 'Bu səhifəyə giriş icazəniz yoxdur.')
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)


class EmailTemplateCreateView(LoginRequiredMixin, CreateView):
    """Create new email template."""
    model = EmailTemplate
    template_name = 'notifications/email_template_form.html'
    fields = ['name', 'subject', 'html_content', 'text_content', 'is_active']
    success_url = reverse_lazy('notifications:email-templates')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_admin():
            messages.error(request, 'Bu səhifəyə giriş icazəniz yoxdur.')
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'E-poçt şablonu yaradıldı.')
        return super().form_valid(form)


class EmailTemplateUpdateView(LoginRequiredMixin, UpdateView):
    """Update existing email template."""
    model = EmailTemplate
    template_name = 'notifications/email_template_form.html'
    fields = ['name', 'subject', 'html_content', 'text_content', 'is_active']
    success_url = reverse_lazy('notifications:email-templates')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_admin():
            messages.error(request, 'Bu səhifəyə giriş icazəniz yoxdur.')
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'E-poçt şablonu yeniləndi.')
        return super().form_valid(form)


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
    notifications = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')[:10]

    data = [{
        'id': n.id,
        'title': n.title,
        'message': n.message,
        'type': n.notification_type,
        'is_read': n.is_read,
        'link': n.link,
        'created_at': n.created_at.isoformat(),
    } for n in notifications]

    return JsonResponse({'notifications': data})
