"""Views for notification preferences and settings in the notifications app."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils.translation import gettext_lazy as _
from .models import UserNotificationPreference, NotificationMethod, NotificationTemplate, SMSProvider
from .forms import NotificationPreferenceForm, SMSProviderForm, NotificationTemplateForm
from apps.accounts.models import User


@login_required
def notification_preferences(request):
    """
    View for user to configure their notification preferences.
    """
    user_pref, created = UserNotificationPreference.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = NotificationPreferenceForm(request.POST, instance=user_pref)
        if form.is_valid():
            form.save()
            messages.success(request, _('Bildiriş tənzimləmələri uğurla yeniləndi.'))
            return redirect('notifications:preferences')
    else:
        form = NotificationPreferenceForm(instance=user_pref)
    
    # Get notification statistics for the user
    from .utils import get_unread_count
    unread_count = get_unread_count(request.user)
    
    # Get recent notification types
    from .models import Notification
    recent_notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:10]
    notification_types = Notification.objects.filter(user=request.user).values('notification_type').annotate(count=Count('notification_type'))
    
    # Get available SMS providers for the user to select
    from .models import SMSProvider
    sms_providers = SMSProvider.objects.filter(is_active=True)
    
    context = {
        'form': form,
        'title': _('Bildiriş Tənzimləmələri'),
        'unread_count': unread_count,
        'recent_notifications': recent_notifications,
        'notification_types': notification_types,
        'sms_providers': sms_providers,
    }
    return render(request, 'notifications/preferences.html', context)


@login_required
def notification_settings_dashboard(request):
    """
    Main dashboard for notification settings.
    """
    user_pref, created = UserNotificationPreference.objects.get_or_create(user=request.user)
    
    # Get statistics
    from .models import Notification
    total_notifications = Notification.objects.filter(user=request.user).count()
    unread_notifications = Notification.objects.filter(user=request.user, is_read=False).count()
    
    context = {
        'user_pref': user_pref,
        'total_notifications': total_notifications,
        'unread_notifications': unread_notifications,
        'title': _('Bildiriş Ayarları')
    }
    return render(request, 'notifications/settings_dashboard.html', context)


@login_required
@require_POST
def update_notification_preferences(request):
    """
    AJAX endpoint to update notification preferences.
    """
    try:
        user_pref, created = UserNotificationPreference.objects.get_or_create(user=request.user)
        
        # Update specific preference based on form data
        field_name = request.POST.get('field')
        field_value = request.POST.get('value')
        
        if field_name and hasattr(user_pref, field_name):
            # Convert to boolean if needed
            if field_value.lower() in ['true', 'false']:
                field_value = field_value.lower() == 'true'
            
            setattr(user_pref, field_name, field_value)
            user_pref.save()
            
            return JsonResponse({
                'status': 'success',
                'message': _('Tənzimləmə yeniləndi.')
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': _('Yanlış sahə adı.')
            })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })


@login_required
def sms_providers_list(request):
    """
    List all SMS providers.
    """
    providers = SMSProvider.objects.all()
    context = {
        'providers': providers,
        'title': _('SMS Təchizatçıları')
    }
    return render(request, 'notifications/sms_providers_list.html', context)


@login_required
def sms_provider_create(request):
    """
    Create a new SMS provider.
    """
    if request.method == 'POST':
        form = SMSProviderForm(request.POST)
        if form.is_valid():
            # Create SMSProvider instance based on the form data
            provider = SMSProvider.objects.create(
                name=form.cleaned_data['name'],
                provider=form.cleaned_data['provider'],
                configuration=get_provider_configuration(form.cleaned_data)
            )
            messages.success(request, _('SMS təchizatçısı uğurla yaradıldı.'))
            return redirect('notifications:sms-providers-list')
    else:
        form = SMSProviderForm()
    
    context = {
        'form': form,
        'title': _('Yeni SMS Təchizatçısı')
    }
    return render(request, 'notifications/sms_provider_form.html', context)


@login_required
def sms_provider_update(request, pk):
    """
    Update an existing SMS provider.
    """
    provider = get_object_or_404(SMSProvider, pk=pk)
    
    if request.method == 'POST':
        form = SMSProviderForm(request.POST)
        if form.is_valid():
            provider.name = form.cleaned_data['name']
            provider.provider = form.cleaned_data['provider']
            provider.configuration = get_provider_configuration(form.cleaned_data)
            provider.save()
            messages.success(request, _('SMS təchizatçısı uğurla yeniləndi.'))
            return redirect('notifications:sms-providers-list')
    else:
        # Populate form with existing provider data
        form_data = {'name': provider.name, 'provider': provider.provider}
        form_data.update(provider.configuration)
        form = SMSProviderForm(form_data)
    
    context = {
        'form': form,
        'provider': provider,
        'title': _('SMS Təchizatçısını Yenilə')
    }
    return render(request, 'notifications/sms_provider_form.html', context)


def get_provider_configuration(form_data):
    """
    Helper function to extract provider-specific configuration from form data.
    """
    provider = form_data.get('provider')
    config = {}
    
    if provider == 'twilio':
        config = {
            'account_sid': form_data.get('account_sid'),
            'auth_token': form_data.get('auth_token'),
            'from_number': form_data.get('from_number')
        }
    elif provider == 'aws_sns':
        config = {
            'aws_access_key_id': form_data.get('aws_access_key_id'),
            'aws_secret_access_key': form_data.get('aws_secret_access_key'),
            'aws_region': form_data.get('aws_region', 'us-east-1')
        }
    elif provider == 'clickatell':
        config = {
            'api_key': form_data.get('clickatell_api_key')
        }
    elif provider == 'custom':
        config = {
            'custom_url': form_data.get('custom_url'),
            'custom_token': form_data.get('custom_token')
        }
    
    return config


@login_required
def notification_templates_list(request):
    """
    List all notification templates.
    """
    templates = NotificationTemplate.objects.all()
    context = {
        'templates': templates,
        'title': _('Bildiriş Şablonları')
    }
    return render(request, 'notifications/templates_list.html', context)


@login_required
def notification_template_create(request):
    """
    Create a new notification template.
    """
    if request.method == 'POST':
        form = NotificationTemplateForm(request.POST)
        if form.is_valid():
            template = NotificationTemplate.objects.create(
                name=form.cleaned_data['name'],
                trigger=form.cleaned_data['trigger'],
                subject=form.cleaned_data['subject'],
                email_content=form.cleaned_data['email_content'],
                sms_content=form.cleaned_data['sms_content'],
                push_content=form.cleaned_data['push_content'],
                inapp_content=form.cleaned_data['inapp_content'],
                is_active=form.cleaned_data.get('is_active', False)
            )
            
            # Create NotificationMethod entries for selected methods
            selected_methods = form.cleaned_data.get('methods', [])
            for method_name in selected_methods:
                method_obj, created = NotificationMethod.objects.get_or_create(
                    name=method_name.title(),
                    defaults={'method_type': method_name}
                )
                template.methods.add(method_obj)
            
            messages.success(request, _('Bildiriş şablonu uğurla yaradıldı.'))
            return redirect('notifications:templates-list')
    else:
        form = NotificationTemplateForm()
    
    context = {
        'form': form,
        'title': _('Yeni Bildiriş Şablonu')
    }
    return render(request, 'notifications/template_form.html', context)


@login_required
def notification_template_update(request, pk):
    """
    Update an existing notification template.
    """
    template = get_object_or_404(NotificationTemplate, pk=pk)
    
    if request.method == 'POST':
        form = NotificationTemplateForm(request.POST)
        if form.is_valid():
            template.name = form.cleaned_data['name']
            template.trigger = form.cleaned_data['trigger']
            template.subject = form.cleaned_data['subject']
            template.email_content = form.cleaned_data['email_content']
            template.sms_content = form.cleaned_data['sms_content']
            template.push_content = form.cleaned_data['push_content']
            template.inapp_content = form.cleaned_data['inapp_content']
            template.is_active = form.cleaned_data.get('is_active', False)
            template.save()
            
            # Update methods
            template.methods.clear()
            selected_methods = form.cleaned_data.get('methods', [])
            for method_name in selected_methods:
                method_obj, created = NotificationMethod.objects.get_or_create(
                    name=method_name.title(),
                    defaults={'method_type': method_name}
                )
                template.methods.add(method_obj)
            
            messages.success(request, _('Bildiriş şablonu uğurla yeniləndi.'))
            return redirect('notifications:templates-list')
    else:
        # Pre-populate form with template data
        form = NotificationTemplateForm(initial={
            'name': template.name,
            'trigger': template.trigger,
            'subject': template.subject,
            'email_content': template.email_content,
            'sms_content': template.sms_content,
            'push_content': template.push_content,
            'inapp_content': template.inapp_content,
            'methods': [method.method_type for method in template.methods.all()],
            'is_active': template.is_active
        })
    
    context = {
        'form': form,
        'template': template,
        'title': _('Bildiriş Şablonunu Yenilə')
    }
    return render(request, 'notifications/template_form.html', context)


@login_required
def notification_template_delete(request, pk):
    """
    Delete a notification template.
    """
    template = get_object_or_404(NotificationTemplate, pk=pk)
    template.delete()
    messages.success(request, _('Bildiriş şablonu uğurla silindi.'))
    return redirect('notifications:templates-list')


@login_required
def notification_template_preview(request, pk):
    """
    Preview a notification template with sample data.
    """
    template = get_object_or_404(NotificationTemplate, pk=pk)
    
    # Sample data for preview
    sample_context = {
        'user_name': request.user.get_full_name() or request.user.username,
        'organization_name': 'Sample Organization',
        'notification_date': timezone.now().strftime('%d.%m.%Y'),
        'additional_info': 'This is a sample notification to demonstrate the template.',
    }
    
    # Replace template variables with sample data
    subject = template.subject
    email_content = template.email_content
    sms_content = template.sms_content
    push_content = template.push_content
    inapp_content = template.inapp_content
    
    for key, value in sample_context.items():
        placeholder = '{{ ' + key + ' }}'
        subject = subject.replace(placeholder, str(value))
        email_content = email_content.replace(placeholder, str(value))
        sms_content = sms_content.replace(placeholder, str(value))
        push_content = push_content.replace(placeholder, str(value))
        inapp_content = inapp_content.replace(placeholder, str(value))
    
    context = {
        'template': template,
        'subject': subject,
        'email_content': email_content,
        'sms_content': sms_content,
        'push_content': push_content,
        'inapp_content': inapp_content,
        'title': _('Şablonu Nəzərdən Keçir')
    }
    return render(request, 'notifications/template_preview.html', context)


@login_required
def notification_statistics(request):
    """
    Show notification statistics and analytics.
    """
    from django.db.models import Count, Avg
    from datetime import timedelta
    from django.utils import timezone
    
    # Notification statistics by type
    stats_by_type = Notification.objects.filter(
        user=request.user
    ).values('notification_type').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Notification statistics by channel
    stats_by_channel = Notification.objects.filter(
        user=request.user
    ).values('channel').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Daily notification count for the last 30 days
    thirty_days_ago = timezone.now() - timedelta(days=30)
    daily_counts = []
    for i in range(30):
        day = thirty_days_ago + timedelta(days=i)
        count = Notification.objects.filter(
            user=request.user,
            created_at__date=day.date()
        ).count()
        daily_counts.append({
            'date': day.strftime('%Y-%m-%d'),
            'count': count
        })
    
    # Read/unread ratio
    total_count = Notification.objects.filter(user=request.user).count()
    read_count = Notification.objects.filter(user=request.user, is_read=True).count()
    unread_count = total_count - read_count
    
    read_ratio = (read_count / total_count * 100) if total_count > 0 else 0
    unread_ratio = (unread_count / total_count * 100) if total_count > 0 else 0
    
    context = {
        'stats_by_type': stats_by_type,
        'stats_by_channel': stats_by_channel,
        'daily_counts': daily_counts,
        'total_count': total_count,
        'read_count': read_count,
        'unread_count': unread_count,
        'read_ratio': read_ratio,
        'unread_ratio': unread_ratio,
        'title': _('Bildiriş Statistikası')
    }
    return render(request, 'notifications/statistics.html', context)


@login_required
def test_notification(request):
    """
    Send a test notification to the current user.
    """
    if request.method == 'POST':
        from .utils import send_notification
        
        # Get the notification type and channel from the form
        notification_type = request.POST.get('type', 'info')
        channel = request.POST.get('channel', 'in_app')
        title = request.POST.get('title', 'Test Bildirişi')
        message = request.POST.get('message', 'Bu bir test bildirişidir.')
        
        # Send notification based on selected channel
        send_email = channel == 'email'
        send_sms = channel == 'sms'
        send_push = channel == 'push'
        
        notification = send_notification(
            recipient=request.user,
            title=title,
            message=message,
            notification_type=notification_type,
            send_email=send_email,
            send_sms=send_sms,
            send_push=send_push,
            channel=channel
        )
        
        if notification:
            messages.success(request, _('Test bildirişi uğurla göndərildi.'))
        else:
            messages.error(request, _('Test bildirişi göndərmək mümkün olmadı.'))
        
        return redirect('notifications:test')
    
    context = {
        'title': _('Test Bildirişi')
    }
    return render(request, 'notifications/test_notification.html', context)


@login_required
def notification_bulk_send(request):
    """
    Send bulk notifications to multiple users.
    """
    if not (request.user.is_admin() or request.user.is_manager()):
        messages.error(request, _('Bu funksiyanı istifadə etmək üçün kifayət qədər icazəniz yoxdur.'))
        return redirect('dashboard')
    
    from apps.accounts.models import User
    from apps.departments.models import Department
    from .utils import send_bulk_notification
    
    if request.method == 'POST':
        title = request.POST.get('title')
        message = request.POST.get('message')
        notification_type = request.POST.get('type', 'info')
        send_email = request.POST.get('send_email') == 'on'
        send_sms = request.POST.get('send_sms') == 'on'
        send_push = request.POST.get('send_push') == 'on'
        
        # Determine recipients
        recipient_type = request.POST.get('recipient_type')
        users_to_notify = User.objects.none()
        
        if recipient_type == 'all':
            users_to_notify = User.objects.filter(is_active=True)
        elif recipient_type == 'department':
            dept_id = request.POST.get('department_id')
            if dept_id:
                users_to_notify = User.objects.filter(department_id=dept_id, is_active=True)
        elif recipient_type == 'role':
            role = request.POST.get('role')
            if role:
                users_to_notify = User.objects.filter(role=role, is_active=True)
        elif recipient_type == 'selected':
            user_ids = request.POST.getlist('user_ids')
            users_to_notify = User.objects.filter(id__in=user_ids, is_active=True)
        
        # Send bulk notifications
        sent_notifications = send_bulk_notification(
            recipients=users_to_notify,
            title=title,
            message=message,
            notification_type=notification_type,
            send_email=send_email,
            send_sms=send_sms,
            send_push=send_push
        )
        
        messages.success(request, f'{len(sent_notifications)} bildiriş uğurla göndərildi.')
        return redirect('notifications:bulk-send')
    
    # Prepare context for GET request
    departments = Department.objects.all()
    users = User.objects.filter(is_active=True)
    role_choices = User.ROLE_CHOICES if hasattr(User, 'ROLE_CHOICES') else []
    
    context = {
        'title': _('Kütləvi Bildiriş Göndər'),
        'departments': departments,
        'users': users,
        'role_choices': role_choices,
    }
    
    return render(request, 'notifications/bulk_send.html', context)