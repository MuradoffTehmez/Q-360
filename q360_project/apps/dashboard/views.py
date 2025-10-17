from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q, Count, Avg, Sum
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from datetime import datetime, timedelta
from decimal import Decimal
import json

from .models import SystemKPI, DashboardWidget, AnalyticsReport, TrendData, ForecastData, RealTimeStat
from apps.departments.models import Department, Organization
from apps.accounts.models import User
from apps.evaluations.models import EvaluationCampaign, Response
# Use high-level helpers only; specific salary model imported lazily when needed.
from apps.recruitment.models import Application
from apps.leave_attendance.models import LeaveRequest, Attendance


@login_required
def dashboard_home(request):
    """
    Ana dashboard səhifəsi
    """
    context = {
        'title': _('Dashboard'),
        'widgets': DashboardWidget.objects.filter(is_active=True).order_by('order'),
        'kpi_stats': SystemKPI.objects.all()[:6],  # İlk 6 KPI göstəricisi
    }
    return render(request, 'dashboard/home.html', context)


@login_required
def real_time_stats_api(request):
    """
    Real vaxt statistikası API
    """
    stats = RealTimeStat.objects.all()
    data = []
    for stat in stats:
        data.append({
            'id': stat.id,
            'stat_type': stat.stat_type,
            'current_value': float(stat.current_value),
            'previous_value': float(stat.previous_value) if stat.previous_value else None,
            'unit': stat.unit,
            'description': stat.description,
            'last_updated': stat.last_updated.isoformat(),
        })
    
    return JsonResponse({'stats': data})


@login_required
def kpi_dashboard(request):
    """
    KPI dashboard səhifəsi
    """
    # Performans göstəriciləri
    active_users = User.objects.filter(is_active=True).count()
    active_evaluations = EvaluationCampaign.objects.filter(status='active').count()
    total_departments = Department.objects.count()
    
    # Ən son KPI göstəriciləri
    latest_kpis = SystemKPI.objects.all().order_by('-created_at')[:10]
    
    # Bölmələr üzrə KPI göstəriciləri
    department_kpis = []
    for dept in Department.objects.all():
        dept_users = User.objects.filter(department=dept).count()
        dept_avg_performance = Response.objects.filter(
            assignment__evaluatee__department=dept
        ).aggregate(Avg('score'))['score__avg'] or 0
        
        department_kpis.append({
            'name': dept.name,
            'user_count': dept_users,
            'avg_performance': round(dept_avg_performance, 2)
        })
    
    context = {
        'title': _('KPI Dashboard'),
        'active_users': active_users,
        'active_evaluations': active_evaluations,
        'total_departments': total_departments,
        'latest_kpis': latest_kpis,
        'department_kpis': department_kpis[:5],  # Top 5 departments
    }
    return render(request, 'dashboard/kpi_dashboard.html', context)


@login_required
def trend_analysis(request):
    """
    Trend analizi səhifəsi
    """
    # Son 12 ay üçün trend məlumatları
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=365)
    
    salary_trends = TrendData.objects.filter(
        data_type='salary',
        period__range=[start_date, end_date]
    ).order_by('period')
    
    performance_trends = TrendData.objects.filter(
        data_type='performance',
        period__range=[start_date, end_date]
    ).order_by('period')
    
    hiring_trends = TrendData.objects.filter(
        data_type='hiring',
        period__range=[start_date, end_date]
    ).order_by('period')
    
    # Trend statistikaları
    current_avg_salary = salary_trends.last().value if salary_trends else 0
    current_avg_performance = performance_trends.last().value if performance_trends else 0
    current_hiring_rate = sum([t.value for t in hiring_trends]) / hiring_trends.count() if hiring_trends.count() > 0 else 0
    
    # 6 aylıq dəyişikliklər
    six_months_ago = end_date - timedelta(days=180)
    prev_avg_salary = TrendData.objects.filter(
        data_type='salary',
        period__range=[start_date, six_months_ago]
    ).order_by('-period').first()
    salary_change = ((current_avg_salary - (prev_avg_salary.value if prev_avg_salary else current_avg_salary)) / 
                     (prev_avg_salary.value if prev_avg_salary and prev_avg_salary.value != 0 else 1)) * 100 if current_avg_salary != 0 else 0
    
    prev_avg_performance = TrendData.objects.filter(
        data_type='performance',
        period__range=[start_date, six_months_ago]
    ).order_by('-period').first()
    performance_change = ((current_avg_performance - (prev_avg_performance.value if prev_avg_performance else current_avg_performance)) / 
                         (prev_avg_performance.value if prev_avg_performance and prev_avg_performance.value != 0 else 1)) * 100 if current_avg_performance != 0 else 0
    
    context = {
        'title': _('Trend Analizi'),
        'salary_trends': salary_trends,
        'performance_trends': performance_trends,
        'hiring_trends': hiring_trends,
        'current_avg_salary': current_avg_salary,
        'current_avg_performance': current_avg_performance,
        'current_hiring_rate': current_hiring_rate,
        'salary_change': salary_change,
        'performance_change': performance_change,
    }
    return render(request, 'dashboard/trend_analysis.html', context)


@login_required
def forecasting_dashboard(request):
    """
    Proqnozlaşdırma dashboard səhifəsi
    """
    # Son proqnoz məlumatları
    staffing_forecasts = ForecastData.objects.filter(forecast_type='staffing').order_by('-forecast_date')[:10]
    budget_forecasts = ForecastData.objects.filter(forecast_type='budget').order_by('-forecast_date')[:10]
    hiring_forecasts = ForecastData.objects.filter(forecast_type='hiring').order_by('-forecast_date')[:10]
    
    context = {
        'title': _('Proqnozlaşdırma'),
        'staffing_forecasts': staffing_forecasts,
        'budget_forecasts': budget_forecasts,
        'hiring_forecasts': hiring_forecasts,
    }
    return render(request, 'dashboard/forecasting.html', context)


@login_required
def update_real_time_stats(request):
    """
    Real vaxt statistikalarını yeniləyir
    """
    if request.method == 'POST':
        # Aktiv istifadəçilər
        active_users_count = User.objects.filter(is_active=True).count()
        stat, created = RealTimeStat.objects.get_or_create(
            stat_type='active_users',
            defaults={'current_value': active_users_count, 'unit': '', 'description': _('Aktiv İstifadəçilər')}
        )
        if not created:
            stat.current_value = active_users_count
            stat.save()
        
        # Gözləyən qiymətləndirmələr
        pending_evaluations_count = Response.objects.filter(is_completed=False).count()
        stat, created = RealTimeStat.objects.get_or_create(
            stat_type='pending_evaluations',
            defaults={'current_value': pending_evaluations_count, 'unit': '', 'description': _('Gözləyən Qiymətləndirmələr')}
        )
        if not created:
            stat.current_value = pending_evaluations_count
            stat.save()
        
        # Yeni işə qəbul olunanlar (bu ay)
        this_month = timezone.now().replace(day=1)
        new_hires_count = User.objects.filter(date_joined__gte=this_month).count()
        stat, created = RealTimeStat.objects.get_or_create(
            stat_type='new_hires',
            defaults={'current_value': new_hires_count, 'unit': '', 'description': _('Bu Ay Yeni İşə Qəbul')}
        )
        if not created:
            stat.current_value = new_hires_count
            stat.save()
        
        # Ortalama performans
        avg_performance = Response.objects.aggregate(Avg('score'))['score__avg']
        if avg_performance:
            stat, created = RealTimeStat.objects.get_or_create(
                stat_type='avg_performance',
                defaults={'current_value': avg_performance, 'unit': '', 'description': _('Ortalama Performans')}
            )
            if not created:
                stat.current_value = avg_performance
                stat.save()
        
        return JsonResponse({'status': 'success', 'message': _('Statistika yeniləndi')})
    
    return JsonResponse({'status': 'error', 'message': _('Yalnız POST sorğuları qəbul olunur')})


@login_required
@require_http_methods(["GET"])
def get_trend_data(request, data_type):
    """
    Verilən növ üzrə trend məlumatlarını qaytarır
    """
    period = request.GET.get('period', '12months')  # 12months, 6months, 3months
    
    end_date = timezone.now()
    if period == '3months':
        start_date = end_date - timedelta(days=90)
    elif period == '6months':
        start_date = end_date - timedelta(days=180)
    else:  # 12months
        start_date = end_date - timedelta(days=365)
    
    trend_data = TrendData.objects.filter(
        data_type=data_type,
        period__range=[start_date, end_date]
    ).order_by('period')
    
    data = []
    for item in trend_data:
        data.append({
            'date': item.period.isoformat(),
            'value': float(item.value),
        })
    
    return JsonResponse({'data': data})


@login_required
@require_http_methods(["GET"])
def get_forecast_data(request, forecast_type):
    """
    Verilən növ üzrə proqnoz məlumatlarını qaytarır
    """
    forecast_data = ForecastData.objects.filter(
        forecast_type=forecast_type
    ).order_by('-forecast_date')[:12]  # Son 12 proqnozu qaytarır
    
    data = []
    for item in forecast_data:
        data.append({
            'date': item.forecast_date.isoformat(),
            'predicted_value': float(item.predicted_value),
            'confidence_level': float(item.confidence_level),
            'actual_value': float(item.actual_value) if item.actual_value else None,
            'explanation': item.explanation,
        })
    
    return JsonResponse({'data': data})


@login_required
def generate_analytics_report(request):
    """
    Analitik hesabat yaradır
    """
    if request.method == 'POST':
        report_type = request.POST.get('report_type')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        
        # Hesabat məlumatlarını yarat
        report_data = {}
        
        if report_type == 'kpi_summary':
            report_data['active_users'] = User.objects.filter(is_active=True).count()
            report_data['active_evaluations'] = EvaluationCampaign.objects.filter(status='active').count()
            report_data['avg_performance'] = Response.objects.aggregate(Avg('score'))['score__avg'] or 0
            report_data['total_departments'] = Department.objects.count()
        
        elif report_type == 'trend_analysis':
            # Trend məlumatları
            report_data['salary_trend'] = list(TrendData.objects.filter(
                data_type='salary',
                period__range=[start_date, end_date]
            ).values('period', 'value'))
            
            report_data['performance_trend'] = list(TrendData.objects.filter(
                data_type='performance',
                period__range=[start_date, end_date]
            ).values('period', 'value'))
            
            report_data['hiring_trend'] = list(TrendData.objects.filter(
                data_type='hiring',
                period__range=[start_date, end_date]
            ).values('period', 'value'))
        
        elif report_type == 'forecast':
            report_data['staffing_forecasts'] = list(ForecastData.objects.filter(
                forecast_type='staffing',
                forecast_date__range=[start_date, end_date]
            ).values('forecast_date', 'predicted_value', 'confidence_level'))
            
            report_data['budget_forecasts'] = list(ForecastData.objects.filter(
                forecast_type='budget',
                forecast_date__range=[start_date, end_date]
            ).values('forecast_date', 'predicted_value', 'confidence_level'))
        
        # Hesabatı yarat
        report = AnalyticsReport.objects.create(
            name=f"{report_type.title()} Report - {start_date} to {end_date}",
            report_type=report_type,
            generated_by=request.user,
            data=report_data,
            start_date=start_date,
            end_date=end_date,
            is_published=True
        )
        
        return JsonResponse({
            'status': 'success', 
            'message': _('Hesabat uğurla yaradıldı'),
            'report_id': report.id
        })
    
    return JsonResponse({'status': 'error', 'message': _('Yalnız POST sorğuları qəbul olunur')})
