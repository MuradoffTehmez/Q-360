"""
Celery tasks for asynchronous report generation.
Prevents timeout issues during PDF/Excel generation.
"""
from celery import shared_task
from django.utils import timezone
from django.core.files.base import ContentFile

from apps.reports.models import ReportGenerationLog
from apps.reports.utils import generate_pdf_report, generate_excel_report
from apps.notifications.utils import send_notification


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def generate_pdf_report_async(self, result_id, user_id):
    """
    Asynchronously generate PDF report for evaluation result.

    Args:
        result_id: ID of the EvaluationResult
        user_id: ID of the User requesting the report

    Returns:
        dict: Status and report log ID
    """
    from apps.evaluations.models import EvaluationResult
    from apps.accounts.models import User

    try:
        # Create log entry
        log = ReportGenerationLog.objects.create(
            report_type='pdf',
            requested_by_id=user_id,
            status='processing',
            metadata={'result_id': result_id, 'task_id': self.request.id}
        )

        # Get the evaluation result
        result = EvaluationResult.objects.select_related(
            'campaign', 'evaluatee'
        ).get(pk=result_id)

        # Generate PDF
        pdf_content = generate_pdf_report(result)

        # Save PDF file
        filename = f'hesabat_{result.evaluatee.username}_{result.campaign.pk}_{timezone.now().strftime("%Y%m%d_%H%M%S")}.pdf'
        log.file.save(filename, ContentFile(pdf_content), save=False)

        # Update log status
        log.status = 'completed'
        log.completed_at = timezone.now()
        log.save()

        # Send notification to user
        user = User.objects.get(pk=user_id)
        send_notification(
            recipient=user,
            title='Hesabat Hazırdır',
            message=f'{result.evaluatee.get_full_name()} üçün PDF hesabat hazırlandı. İndi yükləyə bilərsiniz.',
            notification_type='success',
            link=f'/reports/download/{log.pk}/',
            send_email=True
        )

        return {
            'status': 'success',
            'log_id': log.pk,
            'message': 'PDF hesabat uğurla yaradıldı'
        }

    except EvaluationResult.DoesNotExist:
        # Update log
        if 'log' in locals():
            log.status = 'failed'
            log.error_message = f'Qiymətləndirmə nəticəsi tapılmadı (ID: {result_id})'
            log.save()

        raise Exception(f'EvaluationResult with ID {result_id} not found')

    except Exception as exc:
        # Update log
        if 'log' in locals():
            log.status = 'failed'
            log.error_message = str(exc)
            log.save()

        # Retry the task
        raise self.retry(exc=exc)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def generate_excel_report_async(self, campaign_id, user_id):
    """
    Asynchronously generate Excel report for campaign.

    Args:
        campaign_id: ID of the EvaluationCampaign
        user_id: ID of the User requesting the report

    Returns:
        dict: Status and report log ID
    """
    from apps.evaluations.models import EvaluationCampaign
    from apps.accounts.models import User

    try:
        # Create log entry
        log = ReportGenerationLog.objects.create(
            report_type='excel',
            requested_by_id=user_id,
            status='processing',
            metadata={'campaign_id': campaign_id, 'task_id': self.request.id}
        )

        # Get the campaign
        campaign = EvaluationCampaign.objects.get(pk=campaign_id)

        # Generate Excel
        excel_content = generate_excel_report(campaign)

        # Save Excel file
        filename = f'kampaniya_{campaign.pk}_neticeler_{timezone.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
        log.file.save(filename, ContentFile(excel_content), save=False)

        # Update log status
        log.status = 'completed'
        log.completed_at = timezone.now()
        log.save()

        # Send notification to user
        user = User.objects.get(pk=user_id)
        send_notification(
            recipient=user,
            title='Hesabat Hazırdır',
            message=f'{campaign.title} kampaniyası üçün Excel hesabat hazırlandı. İndi yükləyə bilərsiniz.',
            notification_type='success',
            link=f'/reports/download/{log.pk}/',
            send_email=True
        )

        return {
            'status': 'success',
            'log_id': log.pk,
            'message': 'Excel hesabat uğurla yaradıldı'
        }

    except EvaluationCampaign.DoesNotExist:
        # Update log
        if 'log' in locals():
            log.status = 'failed'
            log.error_message = f'Kampaniya tapılmadı (ID: {campaign_id})'
            log.save()

        raise Exception(f'EvaluationCampaign with ID {campaign_id} not found')

    except Exception as exc:
        # Update log
        if 'log' in locals():
            log.status = 'failed'
            log.error_message = str(exc)
            log.save()

        # Retry the task
        raise self.retry(exc=exc)


@shared_task
def run_scheduled_report_exports():
    """
    Execute due scheduled report exports.
    """
    from apps.reports.services import process_due_schedules

    processed = process_due_schedules()
    return {
        'status': 'success',
        'processed': processed,
        'message': f'{processed} planlaşdırılmış hesabat icra olundu'
    }


@shared_task
def cleanup_old_report_logs():
    """
    Cleanup old report generation logs and files.
    Runs periodically via Celery Beat.
    """
    from datetime import timedelta

    # Delete logs older than 30 days
    cutoff_date = timezone.now() - timedelta(days=30)

    old_logs = ReportGenerationLog.objects.filter(
        created_at__lt=cutoff_date,
        status__in=['completed', 'failed']
    )

    # Delete files
    for log in old_logs:
        if log.file:
            log.file.delete(save=False)

    # Delete log records
    count = old_logs.count()
    old_logs.delete()

    return {
        'status': 'success',
        'deleted_count': count,
        'message': f'{count} köhnə hesabat loqu silindi'
    }
