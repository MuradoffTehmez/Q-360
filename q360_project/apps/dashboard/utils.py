from django.db.models import Q, Count, Avg, Sum, F, ExpressionWrapper, DecimalField
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
from apps.departments.models import Department, Organization
from apps.accounts.models import User
from apps.evaluations.models import EvaluationCampaign, Response, EvaluationAssignment
from apps.compensation.models import SalaryInformation
from apps.recruitment.models import Application
from apps.leave_attendance.models import LeaveRequest, Attendance
from .models import SystemKPI, TrendData, ForecastData, RealTimeStat


def update_real_time_statistics():
    """
    Real vaxt statistikalarını yeniləyir
    """
    # Aktiv istifadəçilər
    active_users_count = User.objects.filter(is_active=True).count()
    stat, created = RealTimeStat.objects.get_or_create(
        stat_type='active_users',
        defaults={
            'current_value': active_users_count, 
            'unit': '', 
            'description': 'Aktiv İstifadəçilər'
        }
    )
    if not created:
        stat.current_value = active_users_count
        stat.save()

    # Gözləyən qiymətləndirmələr
    pending_evaluations_count = EvaluationAssignment.objects.filter(
        status__in=['pending', 'in_progress']
    ).count()
    stat, created = RealTimeStat.objects.get_or_create(
        stat_type='pending_evaluations',
        defaults={
            'current_value': pending_evaluations_count, 
            'unit': '', 
            'description': 'Gözləyən Qiymətləndirmələr'
        }
    )
    if not created:
        stat.current_value = pending_evaluations_count
        stat.save()

    # Bu ay yeni işə qəbul olunanlar
    this_month = timezone.now().replace(day=1)
    new_hires_count = User.objects.filter(date_joined__gte=this_month).count()
    stat, created = RealTimeStat.objects.get_or_create(
        stat_type='new_hires',
        defaults={
            'current_value': new_hires_count, 
            'unit': '', 
            'description': 'Bu Ay Yeni İşə Qəbul'
        }
    )
    if not created:
        stat.current_value = new_hires_count
        stat.save()

    # Ortalama performans
    avg_performance = Response.objects.aggregate(Avg('score'))['score__avg']
    if avg_performance:
        stat, created = RealTimeStat.objects.get_or_create(
            stat_type='avg_performance',
            defaults={
                'current_value': avg_performance, 
                'unit': '', 
                'description': 'Ortalama Performans'
            }
        )
        if not created:
            stat.current_value = avg_performance
            stat.save()

    # Büdcə istifadəsi
    total_budget = SalaryInformation.objects.aggregate(Sum('base_salary'))['base_salary__sum'] or 0
    stat, created = RealTimeStat.objects.get_or_create(
        stat_type='budget_utilization',
        defaults={
            'current_value': total_budget, 
            'unit': '₼', 
            'description': 'Ümumi Maaş Fonduna'
        }
    )
    if not created:
        stat.current_value = total_budget
        stat.save()

    # Məzuniyyət sorğuları
    pending_leaves = LeaveRequest.objects.filter(status='pending').count()
    stat, created = RealTimeStat.objects.get_or_create(
        stat_type='leave_requests',
        defaults={
            'current_value': pending_leaves, 
            'unit': '', 
            'description': 'Gözləyən Məzuniyyət Sorğuları'
        }
    )
    if not created:
        stat.current_value = pending_leaves
        stat.save()

    # Təlim tamamlamaları
    completed_trainings = 0  # Placeholder - real model mövcud deyilsə 0 saxlayırıq
    stat, created = RealTimeStat.objects.get_or_create(
        stat_type='training_completions',
        defaults={
            'current_value': completed_trainings, 
            'unit': '', 
            'description': 'Təlim Tamamlamaları'
        }
    )
    if not created:
        stat.current_value = completed_trainings
        stat.save()


def update_trend_data():
    """
    Trend məlumatlarını yeniləyir
    """
    today = timezone.now().date()
    
    # Maaş trendi
    avg_salary = SalaryInformation.objects.filter(
        effective_date__lte=today
    ).aggregate(Avg('base_salary'))['base_salary__avg'] or 0
    
    TrendData.objects.get_or_create(
        data_type='salary',
        period=today,
        defaults={'value': avg_salary}
    )

    # Performans trendi
    avg_performance = Response.objects.filter(
        created_at__date=today
    ).aggregate(Avg('score'))['score__avg'] or 0
    
    TrendData.objects.get_or_create(
        data_type='performance',
        period=today,
        defaults={'value': avg_performance}
    )

    # İşə qəbul trendi
    daily_hires = User.objects.filter(
        date_joined__date=today
    ).count()
    
    TrendData.objects.get_or_create(
        data_type='hiring',
        period=today,
        defaults={'value': daily_hires}
    )


def update_forecast_data():
    """
    Proqnoz məlumatlarını yeniləyir
    """
    from datetime import date
    from dateutil.relativedelta import relativedelta

    # Bu funksiya real AI modulu ilə əvəz olunmalıdır
    # Hazırda sadəcə nümunə məlumatları yaradırıq
    
    # Vakansiya proqnozu (bu aydan 6 ay sonra)
    forecast_date = date.today() + relativedelta(months=6)
    
    # Təxmin edilən yeni işə qəbul sayı (sadəcə nümunə)
    staffing_forecast = (User.objects.filter(is_active=True).count() * 0.18)  # 18% artım gözlənilir
    
    ForecastData.objects.get_or_create(
        forecast_type='staffing',
        forecast_date=forecast_date,
        defaults={
            'predicted_value': staffing_forecast,
            'confidence_level': 75.00,  # 75% etibar dərəcəsi
            'explanation': 'AI tərəfindən təxmin edilən: Təşkilatın genişlənməsi və layihələrin artması nəzərə alınaraq 6 ay ərzində əlavə işçi tələb olunacaq.'
        }
    )

    # Təxmin edilən büdcə (maaş fonduna) artımı
    current_total_salary = SalaryInformation.objects.aggregate(Sum('base_salary'))['base_salary__sum'] or 0
    budget_forecast = current_total_salary * 1.12  # 12% artım gözlənilir
    
    ForecastData.objects.get_or_create(
        forecast_type='budget',
        forecast_date=forecast_date,
        defaults={
            'predicted_value': budget_forecast,
            'confidence_level': 80.00,  # 80% etibar dərəcəsi
            'explanation': 'AI tərəfindən təxmin edilən: 6 ay ərzində işə qəbul və maaş artırımları nəzərə alınaraq büdcə 12% artacaq.'
        }
    )

    # İşə qəbul proqnozu
    hiring_forecast = User.objects.filter(date_joined__gte=timezone.now()-timedelta(days=30)).count() * 2  # 2x artım gözlənilir
    
    ForecastData.objects.get_or_create(
        forecast_type='hiring',
        forecast_date=forecast_date,
        defaults={
            'predicted_value': hiring_forecast,
            'confidence_level': 70.00,  # 70% etibar dərəcəsi
            'explanation': 'AI tərəfindən təxmin edilən: Növbəti 6 ay ərzində işə qəbul aktivliyi 2 dəfə artacaq.'
        }
    )


def calculate_kpi_indicators():
    """
    KPI göstəricilərini hesablayır
    """
    from datetime import datetime
    now = timezone.now()
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    start_of_prev_month = (start_of_month - timedelta(days=1)).replace(day=1)
    
    # Aktiv istifadəçilər KPI
    active_users = User.objects.filter(is_active=True).count()
    SystemKPI.objects.get_or_create(
        name='Aktiv İstifadəçilər',
        kpi_type='overall',
        period_start=start_of_month,
        period_end=now,
        defaults={
            'value': active_users,
            'target': active_users * 1.1,  # 10% artım hədəfi
            'unit': ''
        }
    )
    
    # Qiymətləndirmə iştirakı KPI
    total_assignments = EvaluationAssignment.objects.count()
    completed_assignments = EvaluationAssignment.objects.filter(status='completed').count()
    participation_rate = (completed_assignments / total_assignments * 100) if total_assignments > 0 else 0
    
    SystemKPI.objects.get_or_create(
        name='Qiymətləndirmə İştirakı',
        kpi_type='overall',
        period_start=start_of_month,
        period_end=now,
        defaults={
            'value': participation_rate,
            'target': 85.00,  # 85% hədəfi
            'unit': '%'
        }
    )
    
    # Ortalama performans KPI
    avg_performance = Response.objects.filter(
        created_at__gte=start_of_month
    ).aggregate(Avg('score'))['score__avg'] or 0
    
    SystemKPI.objects.get_or_create(
        name='Ortalama Performans',
        kpi_type='performance',
        period_start=start_of_month,
        period_end=now,
        defaults={
            'value': avg_performance,
            'target': 4.00,  # 4.00 hədəfi
            'unit': '/5'
        }
    )
    
    # Maaş ödənişi vaxtında edilməsi KPI (nümunə)
    SystemKPI.objects.get_or_create(
        name='Maaş Ödənişi Vaxtında',
        kpi_type='salary',
        period_start=start_of_month,
        period_end=now,
        defaults={
            'value': 98.5,  # 98.5% nisbəti
            'target': 100.00,  # 100% hədəfi
            'unit': '%'
        }
    )


def get_salary_trends(department_id=None, months=12):
    """
    Maaş trend məlumatlarını əldə edir
    """
    from datetime import date
    from dateutil.relativedelta import relativedelta
    
    end_date = date.today()
    start_date = end_date - relativedelta(months=months)
    
    trend_data = TrendData.objects.filter(
        data_type='salary',
        period__range=[start_date, end_date]
    )
    
    if department_id:
        trend_data = trend_data.filter(department_id=department_id)
    
    return [
        {
            'date': item.period.isoformat(),
            'value': float(item.value)
        }
        for item in trend_data.order_by('period')
    ]


def get_performance_trends(department_id=None, months=12):
    """
    Performans trend məlumatlarını əldə edir
    """
    from datetime import date
    from dateutil.relativedelta import relativedelta
    
    end_date = date.today()
    start_date = end_date - relativedelta(months=months)
    
    trend_data = TrendData.objects.filter(
        data_type='performance',
        period__range=[start_date, end_date]
    )
    
    if department_id:
        trend_data = trend_data.filter(department_id=department_id)
    
    return [
        {
            'date': item.period.isoformat(),
            'value': float(item.value)
        }
        for item in trend_data.order_by('period')
    ]


def get_hiring_trends(department_id=None, months=12):
    """
    İşə qəbul trend məlumatlarını əldə edir
    """
    from datetime import date
    from dateutil.relativedelta import relativedelta
    
    end_date = date.today()
    start_date = end_date - relativedelta(months=months)
    
    trend_data = TrendData.objects.filter(
        data_type='hiring',
        period__range=[start_date, end_date]
    )
    
    if department_id:
        trend_data = trend_data.filter(department_id=department_id)
    
    return [
        {
            'date': item.period.isoformat(),
            'value': float(item.value)
        }
        for item in trend_data.order_by('period')
    ]


def calculate_trend_analysis():
    """
    Trend analizini hesablayır və saxlayır
    """
    from datetime import date
    from dateutil.relativedelta import relativedelta
    
    # Maaş trendi
    end_date = date.today()
    start_date = end_date - relativedelta(months=12)
    
    # Maaş ortalaması
    avg_salary = Salary.objects.filter(
        effective_date__range=[start_date, end_date]
    ).aggregate(Avg('base_salary'))['base_salary__avg'] or 0
    
    if avg_salary > 0:
        TrendData.objects.update_or_create(
            data_type='salary',
            period=end_date,
            defaults={'value': avg_salary}
        )
    
    # Performans trendi
    avg_performance = Response.objects.filter(
        created_at__date__range=[start_date, end_date]
    ).aggregate(Avg('score'))['score__avg'] or 0
    
    if avg_performance > 0:
        TrendData.objects.update_or_create(
            data_type='performance',
            period=end_date,
            defaults={'value': avg_performance}
        )
    
    # İşə qəbul trendi
    hiring_count = User.objects.filter(
        date_joined__date__range=[start_date, end_date]
    ).count()
    
    TrendData.objects.update_or_create(
        data_type='hiring',
        period=end_date,
        defaults={'value': hiring_count}
    )


def update_forecast_data():
    """
    Proqnoz məlumatlarını yeniləyir (AI əsaslı)
    """
    from apps.dashboard.ai_forecasting import run_ai_forecasting
    
    # AI əsaslı proqnozlaşdırma mühərriyini işə salır
    run_ai_forecasting()


def get_advanced_trend_analysis(data_type, department_id=None, months=12):
    """
    Genişləndirilmiş trend analizi məlumatlarını əldə edir
    """
    from datetime import date
    from dateutil.relativedelta import relativedelta
    import numpy as np
    
    # Try to import scipy for advanced statistics
    try:
        from scipy import stats
        scipy_available = True
    except ImportError:
        scipy_available = False
    
    end_date = date.today()
    start_date = end_date - relativedelta(months=months)
    
    trend_data = TrendData.objects.filter(
        data_type=data_type,
        period__range=[start_date, end_date]
    )
    
    if department_id:
        trend_data = trend_data.filter(department_id=department_id)
    
    trend_values = [(item.period, float(item.value)) for item in trend_data.order_by('period')]
    
    if len(trend_values) < 2:
        return {
            'data': [{'date': item[0].isoformat(), 'value': item[1]} for item in trend_values],
            'trend_direction': 'neutral',
            'trend_strength': 0,
            'forecast_next_month': trend_values[-1][1] if trend_values else 0
        }
    
    # Extract dates and values
    dates = [item[0] for item in trend_values]
    values = [item[1] for item in trend_values]
    
    if scipy_available:
        # Calculate trend using linear regression from scipy
        x = np.arange(len(values))
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, values)
        
        # Determine trend direction
        if slope > 0.1:  # Positive significant trend
            trend_direction = 'up'
        elif slope < -0.1:  # Negative significant trend
            trend_direction = 'down'
        else:  # No significant trend
            trend_direction = 'neutral'
        
        # Calculate forecast for next month
        next_month_value = intercept + slope * (len(values))
        
        return {
            'data': [{'date': date.isoformat(), 'value': value} for date, value in trend_values],
            'trend_direction': trend_direction,
            'trend_strength': abs(slope),
            'correlation_coefficient': r_value,
            'forecast_next_month': next_month_value,
            'trend_equation': f'y = {slope:.4f}x + {intercept:.4f}',
            'r_squared': r_value**2
        }
    else:
        # Simplified trend analysis without scipy
        x = np.arange(len(values))
        
        # Simple slope calculation (rise over run)
        if len(values) > 1:
            slope = (values[-1] - values[0]) / (len(values) - 1)
        else:
            slope = 0
        
        # Determine trend direction
        if slope > 0.1:  # Positive significant trend
            trend_direction = 'up'
        elif slope < -0.1:  # Negative significant trend
            trend_direction = 'down'
        else:  # No significant trend
            trend_direction = 'neutral'
        
        # Calculate forecast for next month (simple linear extrapolation)
        if len(values) > 1:
            next_month_value = values[-1] + slope
        else:
            next_month_value = values[0] if values else 0
        
        return {
            'data': [{'date': date.isoformat(), 'value': value} for date, value in trend_values],
            'trend_direction': trend_direction,
            'trend_strength': abs(slope),
            'correlation_coefficient': 0,  # Not calculated without scipy
            'forecast_next_month': next_month_value,
            'trend_equation': f'y = {slope:.4f}x + {values[0] if values else 0:.4f}',
            'r_squared': 0  # Not calculated without scipy
        }