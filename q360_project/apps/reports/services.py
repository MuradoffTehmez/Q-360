"""
Service layer for advanced reporting features.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
from typing import Dict, List, Optional

from django.apps import apps
from django.core.files.base import ContentFile
from django.db.models import Avg, Count
from django.utils import timezone

from .models import ReportBlueprint, ReportSchedule, ReportScheduleLog, ReportGenerationLog
from .utils import build_dataset_excel, build_dataset_pdf, build_dataset_csv


@dataclass
class ReportDataset:
    title: str
    columns: List[str]
    rows: List[List]
    metadata: Dict


def build_dataset_for_blueprint(blueprint: ReportBlueprint, params: Optional[Dict] = None) -> ReportDataset:
    """
    Build dataset for the given blueprint.
    """
    params = params or {}
    data_source = blueprint.data_source
    title = params.get('title') or blueprint.title
    columns = blueprint.get_columns()

    if data_source == 'evaluations':
        dataset = _build_evaluations_dataset(columns, params)
    elif data_source == 'training':
        dataset = _build_training_dataset(columns, params)
    elif data_source == 'compensation':
        dataset = _build_compensation_dataset(columns, params)
    else:
        dataset = _build_workforce_dataset(columns, params)

    return ReportDataset(title=title, columns=columns, rows=dataset['rows'], metadata=dataset['metadata'])


def export_blueprint(blueprint: ReportBlueprint, export_format: str, requested_by, params: Optional[Dict] = None) -> ReportGenerationLog:
    """
    Export a blueprint to the desired format and store output in ReportGenerationLog.
    """
    params = params or {}
    dataset = build_dataset_for_blueprint(blueprint, params)
    report_type = export_format.lower()

    log = ReportGenerationLog.objects.create(
        report_type=report_type,
        requested_by=requested_by,
        status='processing',
        metadata={
            'blueprint_id': blueprint.pk,
            'blueprint_slug': blueprint.slug,
            'params': params,
            'generated_at': timezone.now().isoformat(),
        },
    )

    try:
        if report_type == 'excel':
            content = build_dataset_excel(dataset.title, dataset.columns, dataset.rows, dataset.metadata)
            extension = 'xlsx'
        elif report_type == 'pdf':
            content = build_dataset_pdf(dataset.title, dataset.columns, dataset.rows, dataset.metadata)
            extension = 'pdf'
        else:
            content = build_dataset_csv(dataset.title, dataset.columns, dataset.rows)
            extension = 'csv'

        filename = f"{blueprint.slug}_{timezone.now().strftime('%Y%m%d_%H%M%S')}.{extension}"
        log.file.save(filename, ContentFile(content), save=False)
        log.status = 'completed'
        log.completed_at = timezone.now()
        log.metadata = {**log.metadata, **dataset.metadata}
        log.save()
    except Exception as exc:
        log.status = 'failed'
        log.error_message = str(exc)
        log.save(update_fields=['status', 'error_message'])
        raise

    return log


def process_due_schedules() -> int:
    """
    Execute scheduled reports whose next_run is due.
    """
    now = timezone.now()
    schedules = ReportSchedule.objects.filter(is_active=True, next_run__isnull=False, next_run__lte=now)
    processed = 0

    for schedule in schedules.select_related('blueprint'):
        log_entry = ReportScheduleLog.objects.create(schedule=schedule, status='processing')
        try:
            export_log = export_blueprint(
                blueprint=schedule.blueprint,
                export_format=schedule.export_format,
                requested_by=schedule.created_by or schedule.recipients.first(),
                params={**schedule.parameters, 'scheduled_run': True},
            )
            log_entry.status = 'completed'
            log_entry.completed_at = timezone.now()
            log_entry.export_log = export_log
            log_entry.message = 'Scheduled export hazırlandı.'
            schedule.mark_run('completed', run_time=log_entry.completed_at)
            processed += 1
        except Exception as exc:
            log_entry.status = 'failed'
            log_entry.message = str(exc)
            schedule.mark_run('failed')
        finally:
            log_entry.save()

    return processed


def _build_evaluations_dataset(columns: List[str], params: Dict) -> Dict:
    Campaign = apps.get_model('evaluations', 'EvaluationCampaign')
    Result = apps.get_model('evaluations', 'EvaluationResult')

    campaigns = Campaign.objects.all().order_by('-start_date')
    status = params.get('status')
    if status:
        campaigns = campaigns.filter(status=status)

    rows = []
    total_participants = 0
    average_score_total = 0
    campaign_count = 0

    for campaign in campaigns:
        result_qs = Result.objects.filter(campaign=campaign)
        stats = result_qs.aggregate(
            participants=Count('id'),
            avg_score=Avg('overall_score'),
        )
        participants = stats['participants'] or 0
        average_score = float(stats['avg_score']) if stats['avg_score'] else 0
        total_participants += participants
        average_score_total += average_score
        campaign_count += 1

        row = [
            campaign.title,
            campaign.start_date.isoformat(),
            campaign.end_date.isoformat(),
            participants,
            round(average_score, 2),
        ]
        rows.append(_align_row(columns, row))

    metadata = {
        'total_campaigns': campaign_count,
        'total_participants': total_participants,
        'average_score': round(average_score_total / campaign_count, 2) if campaign_count else 0,
    }
    return {'rows': rows, 'metadata': metadata}


def _build_training_dataset(columns: List[str], params: Dict) -> Dict:
    TrainingResource = apps.get_model('training', 'TrainingResource')

    queryset = TrainingResource.objects.all().order_by('title')
    delivery = params.get('delivery_method')
    if delivery:
        queryset = queryset.filter(delivery_method=delivery)

    rows = []
    total_duration = 0
    for resource in queryset:
        row = [
            resource.title,
            resource.get_type_display(),
            resource.get_delivery_method_display(),
            resource.get_difficulty_level_display(),
        ]
        if hasattr(resource, 'duration_hours') and resource.duration_hours:
            total_duration += float(resource.duration_hours)
            row.append(float(resource.duration_hours))
        rows.append(_align_row(columns, row))

    metadata = {
        'total_resources': queryset.count(),
        'total_duration_hours': round(total_duration, 2),
    }
    return {'rows': rows, 'metadata': metadata}


def _build_compensation_dataset(columns: List[str], params: Dict) -> Dict:
    SalaryInformation = apps.get_model('compensation', 'SalaryInformation')

    queryset = SalaryInformation.objects.filter(is_active=True).select_related('user').order_by('-effective_date')
    currency = params.get('currency')
    if currency:
        queryset = queryset.filter(currency=currency)

    rows = []
    totals = {}
    for info in queryset:
        salary = float(info.base_salary)
        totals.setdefault(info.currency, 0)
        totals[info.currency] += salary

        row = [
            info.user.get_full_name() if info.user_id else '-',
            salary,
            info.currency,
            info.effective_date.isoformat(),
        ]
        rows.append(_align_row(columns, row))

    metadata = {
        'total_records': queryset.count(),
        'total_salary_by_currency': totals,
    }
    return {'rows': rows, 'metadata': metadata}


def _build_workforce_dataset(columns: List[str], params: Dict) -> Dict:
    User = apps.get_model('accounts', 'User')
    Department = apps.get_model('departments', 'Department')

    departments = Department.objects.filter(is_active=True).order_by('name')
    dept_id = params.get('department_id')
    if dept_id:
        departments = departments.filter(pk=dept_id)

    rows = []
    total_employees = 0

    for dept in departments:
        employee_qs = User.objects.filter(department=dept, is_active=True)
        manager = dept.head.get_full_name() if dept.head_id else '-'
        count = employee_qs.count()
        total_employees += count

        row = [
            dept.name,
            count,
            manager,
        ]
        rows.append(_align_row(columns, row))

    metadata = {
        'total_departments': departments.count(),
        'total_employees': total_employees,
    }
    return {'rows': rows, 'metadata': metadata}


def _align_row(columns: List[str], row_values: List) -> List:
    """
    Ensure row has same length as columns by padding with blanks.
    """
    values = list(row_values)
    if len(values) < len(columns):
        values.extend([''] * (len(columns) - len(values)))
    elif len(values) > len(columns):
        values = values[: len(columns)]
    return values
