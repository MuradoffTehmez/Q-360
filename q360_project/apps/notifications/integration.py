"""Integration functions to add enhanced notifications to existing apps."""
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .utils import send_notification
from .models import NotificationTemplate, UserNotificationPreference


User = get_user_model()


def send_evaluation_assignment_notification(assignment):
    """
    Send notification when a user is assigned to evaluate someone.
    
    Args:
        assignment: EvaluationAssignment object
    """
    # Check if notification template exists
    try:
        template = NotificationTemplate.objects.get(trigger='evaluation_assigned', is_active=True)
        
        # Check if user has enabled assignment notifications
        user_pref, created = UserNotificationPreference.objects.get_or_create(user=assignment.evaluator)
        
        if user_pref.email_assignment or user_pref.push_assignment or user_pref.sms_assignment:
            # Send notification using the template
            send_notification(
                recipient=assignment.evaluator,
                title=template.subject,
                message=template.inapp_content.format(
                    evaluator_name=assignment.evaluator.get_full_name(),
                    evaluatee_name=assignment.evaluatee.get_full_name(),
                    campaign_title=assignment.campaign.title
                ),
                notification_type='assignment',
                link=f'/evaluations/assignment/{assignment.pk}/',
                send_email=user_pref.email_assignment,
                send_sms=user_pref.sms_assignment and user_pref.sms_notifications,
                send_push=user_pref.push_assignment,
                channel='in_app'
            )
    except NotificationTemplate.DoesNotExist:
        # Fallback to basic notification
        send_notification(
            recipient=assignment.evaluator,
            title=_('Qiymətləndirmə Tapşırığı'),
            message=_('Sizə') + f' {assignment.campaign.title} ' + _('kampaniyası çərçivəsində qiymətləndirmə tapşırıldı.'),
            notification_type='assignment',
            link=f'/evaluations/assignment/{assignment.pk}/',
            send_email=True,
            send_sms=False,
            send_push=True,
            channel='in_app'
        )


def send_campaign_start_notification(campaign):
    """
    Send notification when a campaign starts.
    
    Args:
        campaign: EvaluationCampaign object
    """
    try:
        template = NotificationTemplate.objects.get(trigger='campaign_start', is_active=True)
        
        # Get all users who have assignments in this campaign
        evaluators = User.objects.filter(
            given_evaluations__campaign=campaign
        ).distinct()
        
        for evaluator in evaluators:
            user_pref, created = UserNotificationPreference.objects.get_or_create(user=evaluator)
            
            if user_pref.email_announcement or user_pref.push_announcement or user_pref.sms_notifications:
                send_notification(
                    recipient=evaluator,
                    title=template.subject,
                    message=template.inapp_content.format(
                        campaign_title=campaign.title,
                        end_date=campaign.end_date.strftime('%d.%m.%Y')
                    ),
                    notification_type='announcement',
                    link=f'/evaluations/my-assignments/',
                    send_email=user_pref.email_announcement,
                    send_sms=False,  # Campaign start is usually not sent via SMS
                    send_push=user_pref.push_announcement,
                    channel='in_app'
                )
    except NotificationTemplate.DoesNotExist:
        # Fallback notification
        evaluators = User.objects.filter(given_evaluations__campaign=campaign).distinct()
        
        for evaluator in evaluators:
            send_notification(
                recipient=evaluator,
                title=_('Qiymətləndirmə Kampaniyası Başladı'),
                message=f'{campaign.title} kampaniyası başladı. Bitmə tarixi: {campaign.end_date.strftime("%d.%m.%Y")}',
                notification_type='announcement',
                link=f'/evaluations/my-assignments/',
                send_email=True,
                send_sms=False,
                send_push=True,
                channel='in_app'
            )


def send_campaign_end_notification(campaign):
    """
    Send notification when a campaign ends.
    
    Args:
        campaign: EvaluationCampaign object
    """
    try:
        template = NotificationTemplate.objects.get(trigger='campaign_end', is_active=True)
        
        # Notify all evaluators about campaign end
        evaluators = User.objects.filter(
            given_evaluations__campaign=campaign
        ).distinct()
        
        for evaluator in evaluators:
            user_pref, created = UserNotificationPreference.objects.get_or_create(user=evaluator)
            
            # Only send to users who completed their assignments
            if evaluator.given_evaluations.filter(campaign=campaign, status='completed').exists():
                send_notification(
                    recipient=evaluator,
                    title=template.subject,
                    message=template.inapp_content.format(
                        campaign_title=campaign.title
                    ),
                    notification_type='success',
                    link=f'/evaluations/results/{campaign.pk}/',
                    send_email=user_pref.email_announcement,
                    send_sms=False,
                    send_push=user_pref.push_announcement,
                    channel='in_app'
                )
    except NotificationTemplate.DoesNotExist:
        # Fallback notification
        evaluators = User.objects.filter(given_evaluations__campaign=campaign).distinct()
        
        for evaluator in evaluators:
            if evaluator.given_evaluations.filter(campaign=campaign, status='completed').exists():
                send_notification(
                    recipient=evaluator,
                    title=_('Qiymətləndirmə Kampaniyası Bitdi'),
                    message=f'{campaign.title} kampaniyası bitdi. Nəticələrə baxmaq üçün klikləyin.',
                    notification_type='success',
                    link=f'/evaluations/results/{campaign.pk}/',
                    send_email=True,
                    send_sms=False,
                    send_push=True,
                    channel='in_app'
                )


def send_evaluation_deadline_reminder(assignment):
    """
    Send reminder notification when evaluation deadline is approaching.
    
    Args:
        assignment: EvaluationAssignment object
    """
    try:
        template = NotificationTemplate.objects.get(trigger='deadline_reminder', is_active=True)
        
        user_pref, created = UserNotificationPreference.objects.get_or_create(user=assignment.evaluator)
        
        if user_pref.email_reminder or user_pref.push_reminder or user_pref.sms_reminder:
            send_notification(
                recipient=assignment.evaluator,
                title=template.subject,
                message=template.inapp_content.format(
                    campaign_title=assignment.campaign.title,
                    days_remaining=(assignment.campaign.end_date - timezone.now().date()).days
                ),
                notification_type='reminder',
                link=f'/evaluations/assignment/{assignment.pk}/',
                send_email=user_pref.email_reminder,
                send_sms=user_pref.sms_reminder and user_pref.sms_notifications,
                send_push=user_pref.push_reminder,
                channel='in_app'
            )
    except NotificationTemplate.DoesNotExist:
        # Fallback reminder
        days_remaining = (assignment.campaign.end_date - timezone.now().date()).days
        send_notification(
            recipient=assignment.evaluator,
            title=_('Qiymətləndirmə Bitmə Vaxtına Xatırlatma'),
            message=f'{assignment.campaign.title} kampaniyası üçün qiymətləndirmənizi tamamlamaq üçün tələb olunan vaxt {days_remaining} gün ərzində bitir.',
            notification_type='reminder',
            link=f'/evaluations/assignment/{assignment.pk}/',
            send_email=True,
            send_sms=False,
            send_push=True,
            channel='in_app'
        )


def send_salary_change_notification(user, old_salary, new_salary):
    """
    Send notification when user's salary changes.
    
    Args:
        user: User object
        old_salary: Old salary amount
        new_salary: New salary amount
    """
    try:
        template = NotificationTemplate.objects.get(trigger='salary_change', is_active=True)
        
        user_pref, created = UserNotificationPreference.objects.get_or_create(user=user)
        
        if user_pref.email_announcement or user_pref.push_announcement or user_pref.sms_notifications:
            send_notification(
                recipient=user,
                title=template.subject,
                message=template.inapp_content.format(
                    old_salary=old_salary,
                    new_salary=new_salary
                ),
                notification_type='announcement',
                link='/accounts/profile/',
                send_email=user_pref.email_announcement,
                send_sms=user_pref.sms_notifications and user_pref.sms_important_only,
                send_push=user_pref.push_announcement,
                channel='in_app'
            )
    except NotificationTemplate.DoesNotExist:
        # Fallback notification
        send_notification(
            recipient=user,
            title=_('Maaş Dəyişikliyi'),
            message=f'Sizin maaşınız {old_salary} AZN-dən {new_salary} AZN-ə dəyişdirildi.',
            notification_type='success',
            link='/accounts/profile/',
            send_email=True,
            send_sms=True,  # Salary changes are important
            send_push=True,
            channel='in_app'
        )


def send_training_assignment_notification(training_record):
    """
    Send notification when a user is assigned a training.
    
    Args:
        training_record: UserTraining object
    """
    try:
        template = NotificationTemplate.objects.get(trigger='new_training', is_active=True)
        
        user_pref, created = UserNotificationPreference.objects.get_or_create(user=training_record.user)
        
        if user_pref.email_assignment or user_pref.push_assignment or user_pref.sms_assignment:
            send_notification(
                recipient=training_record.user,
                title=template.subject,
                message=template.inapp_content.format(
                    training_title=training_record.training.title,
                    due_date=training_record.due_date.strftime('%d.%m.%Y') if training_record.due_date else 'mövcud deyil'
                ),
                notification_type='assignment',
                link=f'/training/user/{training_record.pk}/',
                send_email=user_pref.email_assignment,
                send_sms=user_pref.sms_assignment and user_pref.sms_notifications,
                send_push=user_pref.push_assignment,
                channel='in_app'
            )
    except NotificationTemplate.DoesNotExist:
        # Fallback notification
        due_date_str = training_record.due_date.strftime('%d.%m.%Y') if training_record.due_date else 'mövcud deyil'
        send_notification(
            recipient=training_record.user,
            title=_('Yeni Təlim Təyin Edildi'),
            message=f'"{training_record.training.title}" təlimi sizə təyin edildi. Bitmə tarixi: {due_date_str}',
            notification_type='assignment',
            link=f'/training/user/{training_record.pk}/',
            send_email=True,
            send_sms=False,
            send_push=True,
            channel='in_app'
        )


def send_performance_result_notification(user, campaign):
    """
    Send notification when performance results are available.
    
    Args:
        user: User object (the evaluated person)
        campaign: EvaluationCampaign object
    """
    try:
        template = NotificationTemplate.objects.get(trigger='performance_result', is_active=True)
        
        user_pref, created = UserNotificationPreference.objects.get_or_create(user=user)
        
        if user_pref.email_announcement or user_pref.push_announcement:
            send_notification(
                recipient=user,
                title=template.subject,
                message=template.inapp_content.format(
                    campaign_title=campaign.title
                ),
                notification_type='announcement',
                link=f'/evaluations/results/{campaign.pk}/',
                send_email=user_pref.email_announcement,
                send_sms=False,  # Performance results are detailed, better for email/push
                send_push=user_pref.push_announcement,
                channel='in_app'
            )
    except NotificationTemplate.DoesNotExist:
        # Fallback notification
        send_notification(
            recipient=user,
            title=_('Performans Nəticələri Mövcuddur'),
            message=f'{campaign.title} kampaniyası üzrə performans qiymətləndirmə nəticələriniz mövcuddur.',
            notification_type='success',
            link=f'/evaluations/results/{campaign.pk}/',
            send_email=True,
            send_sms=False,
            send_push=True,
            channel='in_app'
        )


def send_security_alert_notification(user, alert_type, description):
    """
    Send security alert notification.
    
    Args:
        user: User object
        alert_type: Type of security alert
        description: Description of the alert
    """
    try:
        template = NotificationTemplate.objects.get(trigger='security_alert', is_active=True)
        
        user_pref, created = UserNotificationPreference.objects.get_or_create(user=user)
        
        # Security alerts should always be sent via multiple channels
        send_notification(
            recipient=user,
            title=template.subject,
            message=template.inapp_content.format(
                alert_type=alert_type,
                description=description
            ),
            notification_type='security',
            link='/accounts/security/',
            send_email=True,  # Security alerts always via email
            send_sms=user_pref.sms_notifications and user_pref.sms_security,  # If SMS security alerts are enabled
            send_push=True,  # Security alerts always via push
            channel='in_app'
        )
    except NotificationTemplate.DoesNotExist:
        # Fallback security alert
        send_notification(
            recipient=user,
            title=_('Təhlükəsizlik Xəbərdarlığı'),
            message=f'{alert_type}: {description}',
            notification_type='security',
            link='/accounts/security/',
            send_email=True,
            send_sms=True,  # Security alerts via SMS too
            send_push=True,
            channel='in_app'
        )