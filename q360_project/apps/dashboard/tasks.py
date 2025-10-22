"""
Celery tasks for dashboard AI forecasting and analytics.
"""
from celery import shared_task
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)


@shared_task
def run_ai_forecasting_task():
    """
    Background task to run AI forecasting and update ForecastData.

    This should be scheduled to run periodically (e.g., weekly or monthly).

    Returns:
        Dict with task results
    """
    try:
        from .ai_forecasting import run_ai_forecasting

        logger.info("Starting AI forecasting task...")

        result = run_ai_forecasting()

        logger.info("AI forecasting task completed successfully")

        return {
            'success': True,
            'message': 'AI forecasting completed',
            'timestamp': timezone.now().isoformat()
        }

    except Exception as e:
        logger.error(f"Error in AI forecasting task: {str(e)}", exc_info=True)
        return {
            'success': False,
            'error': str(e),
            'timestamp': timezone.now().isoformat()
        }


@shared_task
def update_trend_data_task():
    """
    Background task to update TrendData with latest metrics.

    Returns:
        Dict with task results
    """
    from .models import TrendData
    from apps.accounts.models import User
    from apps.compensation.models import SalaryInformation
    from apps.evaluations.models import Response
    from django.db.models import Avg
    from datetime import date
    from decimal import Decimal

    try:
        logger.info("Starting trend data update task...")

        today = date.today()
        updated_count = 0

        # Update salary trend
        avg_salary = SalaryInformation.objects.filter(
            is_active=True
        ).aggregate(Avg('base_salary'))['base_salary__avg'] or 0

        if avg_salary > 0:
            TrendData.objects.update_or_create(
                data_type='salary',
                period=today,
                defaults={'value': Decimal(str(avg_salary))}
            )
            updated_count += 1

        # Update performance trend
        avg_performance = Response.objects.filter(
            created_at__month=today.month,
            created_at__year=today.year
        ).aggregate(Avg('score'))['score__avg'] or 0

        if avg_performance > 0:
            TrendData.objects.update_or_create(
                data_type='performance',
                period=today,
                defaults={'value': Decimal(str(avg_performance))}
            )
            updated_count += 1

        # Update hiring trend
        new_hires = User.objects.filter(
            date_joined__month=today.month,
            date_joined__year=today.year
        ).count()

        TrendData.objects.update_or_create(
            data_type='hiring',
            period=today,
            defaults={'value': Decimal(str(new_hires))}
        )
        updated_count += 1

        logger.info(f"Trend data update task completed. Updated {updated_count} trends.")

        return {
            'success': True,
            'updated_count': updated_count,
            'timestamp': timezone.now().isoformat()
        }

    except Exception as e:
        logger.error(f"Error in trend data update task: {str(e)}", exc_info=True)
        return {
            'success': False,
            'error': str(e),
            'timestamp': timezone.now().isoformat()
        }


@shared_task
def generate_kpi_report_task(user_id=None):
    """
    Generate KPI report and send notification.

    Args:
        user_id: Optional user ID to send report to (admin/manager)

    Returns:
        Dict with task results
    """
    from .models import SystemKPI
    from apps.accounts.models import User
    from apps.notifications.utils import send_notification_by_smart_routing
    import json

    try:
        logger.info("Starting KPI report generation task...")

        # Get all active KPIs
        kpis = SystemKPI.objects.filter(
            period_end__gte=timezone.now()
        ).order_by('-created_at')[:10]

        # Generate summary
        summary = {
            'total_kpis': kpis.count(),
            'kpis': []
        }

        for kpi in kpis:
            summary['kpis'].append({
                'name': kpi.name,
                'value': float(kpi.value),
                'target': float(kpi.target) if kpi.target else None,
                'unit': kpi.unit,
                'achievement': float((kpi.value / kpi.target * 100)) if kpi.target else None
            })

        # Send notification if user specified
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                send_notification_by_smart_routing(
                    user=user,
                    title='KPI Hesabatı Hazırdır',
                    message=f'{kpis.count()} əsas göstərici üzrə hesabat yaradıldı.',
                    notification_type='email',
                    priority='normal',
                    context={'summary': summary}
                )
            except User.DoesNotExist:
                logger.warning(f"User {user_id} not found for KPI report notification")

        logger.info("KPI report generation task completed")

        return {
            'success': True,
            'summary': summary,
            'timestamp': timezone.now().isoformat()
        }

    except Exception as e:
        logger.error(f"Error in KPI report generation task: {str(e)}", exc_info=True)
        return {
            'success': False,
            'error': str(e),
            'timestamp': timezone.now().isoformat()
        }
