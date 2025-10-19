from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q, Count, Avg, Sum, Max
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
    # Update real-time stats if needed
    from .utils import update_real_time_statistics
    update_real_time_statistics()
    
    stats = RealTimeStat.objects.all()
    data = []
    for stat in stats:
        # Calculate percentage change if previous value exists
        percentage_change = None
        if stat.previous_value and float(stat.previous_value) != 0:
            current_val = float(stat.current_value)
            previous_val = float(stat.previous_value)
            percentage_change = ((current_val - previous_val) / previous_val) * 100
        
        data.append({
            'id': stat.id,
            'stat_type': stat.stat_type,
            'current_value': float(stat.current_value),
            'previous_value': float(stat.previous_value) if stat.previous_value else None,
            'unit': stat.unit,
            'description': stat.description,
            'last_updated': stat.last_updated.isoformat(),
            'percentage_change': percentage_change,
            'trend': 'up' if percentage_change and percentage_change > 0 else 'down' if percentage_change and percentage_change < 0 else 'neutral'
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
        
        # Calculate performance trend for this department
        from datetime import timedelta
        from django.utils import timezone
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=30)  # Last 30 days
        
        recent_performance = Response.objects.filter(
            assignment__evaluatee__department=dept,
            created_at__date__range=[start_date, end_date]
        ).aggregate(Avg('score'))['score__avg'] or 0
        
        prev_start_date = start_date - timedelta(days=30)
        prev_recent_performance = Response.objects.filter(
            assignment__evaluatee__department=dept,
            created_at__date__range=[prev_start_date, start_date]
        ).aggregate(Avg('score'))['score__avg'] or 0
        
        performance_trend = None
        if prev_recent_performance != 0:
            performance_trend = ((recent_performance - prev_recent_performance) / prev_recent_performance) * 100
        
        department_kpis.append({
            'name': dept.name,
            'user_count': dept_users,
            'avg_performance': round(dept_avg_performance, 2),
            'performance_trend': round(performance_trend, 2) if performance_trend else 0,
            'trend_direction': 'up' if performance_trend and performance_trend > 0 else 'down' if performance_trend and performance_trend < 0 else 'neutral'
        })
    
    # Get KPI statistics by type
    kpi_by_type = {}
    for kpi in SystemKPI.objects.all():
        kpi_type = kpi.get_kpi_type_display()
        if kpi_type not in kpi_by_type:
            kpi_by_type[kpi_type] = []
        kpi_by_type[kpi_type].append({
            'name': kpi.name,
            'value': float(kpi.value),
            'target': float(kpi.target) if kpi.target else None,
            'unit': kpi.unit,
            'achieved_percentage': (kpi.value / kpi.target * 100) if kpi.target else 0
        })
    
    context = {
        'title': _('KPI Dashboard'),
        'active_users': active_users,
        'active_evaluations': active_evaluations,
        'total_departments': total_departments,
        'latest_kpis': latest_kpis,
        'department_kpis': department_kpis[:10],  # Top 10 departments
        'kpi_by_type': kpi_by_type,
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
    
    # Compensation trends (if available)
    compensation_trends = TrendData.objects.filter(
        data_type='compensation',
        period__range=[start_date, end_date]
    ).order_by('period')
    
    # Attendance trends (if available)
    attendance_trends = TrendData.objects.filter(
        data_type='attendance',
        period__range=[start_date, end_date]
    ).order_by('period')
    
    # Trend statistikaları
    current_avg_salary = float(salary_trends.last().value) if salary_trends else 0
    current_avg_performance = float(performance_trends.last().value) if performance_trends else 0
    current_hiring_rate = sum([float(t.value) for t in hiring_trends]) / hiring_trends.count() if hiring_trends.count() > 0 else 0
    current_avg_compensation = float(compensation_trends.last().value) if compensation_trends else 0
    current_avg_attendance = float(attendance_trends.last().value) if attendance_trends else 0
    
    # 6 aylıq dəyişikliklər
    six_months_ago = end_date - timedelta(days=180)
    prev_avg_salary = TrendData.objects.filter(
        data_type='salary',
        period__range=[start_date, six_months_ago]
    ).order_by('-period').first()
    salary_change = ((current_avg_salary - (float(prev_avg_salary.value) if prev_avg_salary else current_avg_salary)) / 
                     (float(prev_avg_salary.value) if prev_avg_salary and float(prev_avg_salary.value) != 0 else 1)) * 100 if current_avg_salary != 0 else 0
    
    prev_avg_performance = TrendData.objects.filter(
        data_type='performance',
        period__range=[start_date, six_months_ago]
    ).order_by('-period').first()
    performance_change = ((current_avg_performance - (float(prev_avg_performance.value) if prev_avg_performance else current_avg_performance)) / 
                         (float(prev_avg_performance.value) if prev_avg_performance and float(prev_avg_performance.value) != 0 else 1)) * 100 if current_avg_performance != 0 else 0
    
    # Trend təhlili və proqnozlaşdırma
    from datetime import date
    from dateutil.relativedelta import relativedelta
    
    # Salary trend analysis
    salary_values = [float(t.value) for t in salary_trends]
    if len(salary_values) >= 2:
        # Calculate average monthly change
        monthly_changes = [salary_values[i+1] - salary_values[i] for i in range(len(salary_values)-1)]
        avg_monthly_change = sum(monthly_changes) / len(monthly_changes)
        
        # Forecast next 3 months
        last_salary = salary_values[-1] if salary_values else 0
        forecast_salaries = [last_salary + avg_monthly_change * (i+1) for i in range(3)]
    else:
        avg_monthly_change = 0
        forecast_salaries = [current_avg_salary] * 3
    
    # Performance trend analysis
    performance_values = [float(t.value) for t in performance_trends]
    if len(performance_values) >= 2:
        # Calculate average monthly change
        monthly_changes = [performance_values[i+1] - performance_values[i] for i in range(len(performance_values)-1)]
        avg_monthly_change_perf = sum(monthly_changes) / len(monthly_changes)
        
        # Forecast next 3 months
        last_performance = performance_values[-1] if performance_values else 0
        forecast_performance = [last_performance + avg_monthly_change_perf * (i+1) for i in range(3)]
    else:
        avg_monthly_change_perf = 0
        forecast_performance = [current_avg_performance] * 3
    
    # Department-based trends (if available)
    department_trends = {}
    for dept in Department.objects.all()[:5]:  # Top 5 departments
        dept_salary_trends = TrendData.objects.filter(
            data_type='salary',
            department=dept,
            period__range=[start_date, end_date]
        ).order_by('period')
        
        dept_performance_trends = TrendData.objects.filter(
            data_type='performance',
            department=dept,
            period__range=[start_date, end_date]
        ).order_by('period')
        
        if dept_salary_trends.exists() or dept_performance_trends.exists():
            department_trends[dept.name] = {
                'salary_trends': [{'date': t.period.isoformat(), 'value': float(t.value)} for t in dept_salary_trends],
                'performance_trends': [{'date': t.period.isoformat(), 'value': float(t.value)} for t in dept_performance_trends],
            }
    
    context = {
        'title': _('Trend Analizi'),
        'salary_trends': [{'date': t.period.isoformat(), 'value': float(t.value)} for t in salary_trends],
        'performance_trends': [{'date': t.period.isoformat(), 'value': float(t.value)} for t in performance_trends],
        'hiring_trends': [{'date': t.period.isoformat(), 'value': float(t.value)} for t in hiring_trends],
        'compensation_trends': [{'date': t.period.isoformat(), 'value': float(t.value)} for t in compensation_trends],
        'attendance_trends': [{'date': t.period.isoformat(), 'value': float(t.value)} for t in attendance_trends],
        'current_avg_salary': current_avg_salary,
        'current_avg_performance': current_avg_performance,
        'current_hiring_rate': current_hiring_rate,
        'current_avg_compensation': current_avg_compensation,
        'current_avg_attendance': current_avg_attendance,
        'salary_change': salary_change,
        'performance_change': performance_change,
        'forecast_salaries': forecast_salaries,
        'forecast_performance': forecast_performance,
        'department_trends': department_trends,
    }
    return render(request, 'dashboard/trend_analysis.html', context)


@login_required
def forecasting_dashboard(request):
    """
    Proqnozlaşdırma dashboard səhifəsi
    """
    from datetime import date
    from dateutil.relativedelta import relativedelta
    
    # Son proqnoz məlumatları
    staffing_forecasts = ForecastData.objects.filter(forecast_type='staffing').order_by('-forecast_date')[:10]
    budget_forecasts = ForecastData.objects.filter(forecast_type='budget').order_by('-forecast_date')[:10]
    hiring_forecasts = ForecastData.objects.filter(forecast_type='hiring').order_by('-forecast_date')[:10]
    performance_forecasts = ForecastData.objects.filter(forecast_type='performance').order_by('-forecast_date')[:10]
    
    # Ən son proqnoz dövrü
    latest_forecast_date = ForecastData.objects.aggregate(latest=Max('forecast_date'))['latest']
    if latest_forecast_date:
        # Sonrakı 12 ay üçün proqnoz məlumatları
        next_12_months = []
        for i in range(12):
            month_date = latest_forecast_date + relativedelta(months=i+1)
            next_12_months.append({
                'date': month_date,
                'staffing': ForecastData.objects.filter(forecast_type='staffing', forecast_date=month_date).first(),
                'budget': ForecastData.objects.filter(forecast_type='budget', forecast_date=month_date).first(),
                'hiring': ForecastData.objects.filter(forecast_type='hiring', forecast_date=month_date).first(),
                'performance': ForecastData.objects.filter(forecast_type='performance', forecast_date=month_date).first(),
            })
    
    # Departamentlər üzrə proqnozlar
    department_forecasts = {}
    for dept in Department.objects.all()[:5]:  # Top 5 departments
        dept_staffing = ForecastData.objects.filter(
            forecast_type='staffing', 
            department=dept
        ).order_by('-forecast_date')[:5]
        
        dept_budget = ForecastData.objects.filter(
            forecast_type='budget', 
            department=dept
        ).order_by('-forecast_date')[:5]
        
        department_forecasts[dept.name] = {
            'staffing': dept_staffing,
            'budget': dept_budget,
        }
    
    # Proqnoz dəqiqliyi statistikası (həqiqi dəyərlərlə müqayisə)
    forecast_accuracy = {}
    for f_type in ['staffing', 'budget', 'hiring', 'performance']:
        forecasts_with_actual = ForecastData.objects.filter(
            forecast_type=f_type,
            actual_value__isnull=False
        )[:20]  # Son 20 forecast
        
        if forecasts_with_actual.exists():
            errors = []
            for forecast in forecasts_with_actual:
                error = abs(float(forecast.predicted_value) - float(forecast.actual_value)) / float(forecast.actual_value) * 100 if forecast.actual_value != 0 else float(forecast.predicted_value) * 100
                errors.append(error)
            
            avg_error = sum(errors) / len(errors) if errors else 0
            forecast_accuracy[f_type] = {
                'avg_error': avg_error,
                'accuracy_rate': max(0, 100 - avg_error),  # Təxmini dəqiqlik nisbəti
                'total_forecasts': len(errors)
            }
    
    context = {
        'title': _('Proqnozlaşdırma'),
        'staffing_forecasts': staffing_forecasts,
        'budget_forecasts': budget_forecasts,
        'hiring_forecasts': hiring_forecasts,
        'performance_forecasts': performance_forecasts,
        'next_12_months': next_12_months,
        'department_forecasts': department_forecasts,
        'forecast_accuracy': forecast_accuracy,
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


@login_required
def ai_management(request):
    """
    AI Model İdarəetmə Paneli
    """
    # Cari model məlumatları (mock data - real implementation would fetch from actual model)
    current_model = {
        'version': '1.2.3',
        'accuracy': 87.5,
        'last_trained': timezone.now() - timedelta(days=15),
        'model_type': 'Regression',
        'algorithm': 'random_forest',
        'training_data_size': '15,000 records',
        'feature_count': 24,
        'updated_at': timezone.now(),
        'forecast_horizon': 6,
        'confidence_level': 85,
        'data_lookback': 12,
        'enabled_features': ['employee_performance', 'salary_trends', 'market_data'],
        'enable_realtime': True
    }
    
    # Mövcud xüsusiyyətlər siyahısı
    available_features = [
        'employee_performance',
        'salary_trends',
        'market_data',
        'economic_indicators',
        'department_metrics',
        'recruitment_rates',
        'turnover_statistics',
        'training_completion',
        'engagement_scores',
        'productivity_metrics'
    ]
    
    # Təlim tarixçəsi (mock data)
    training_history = [
        {
            'created_at': timezone.now() - timedelta(days=15),
            'accuracy': 87.5,
            'status': 'completed',
            'algorithm': 'Random Forest'
        },
        {
            'created_at': timezone.now() - timedelta(days=45),
            'accuracy': 82.3,
            'status': 'completed',
            'algorithm': 'Linear Regression'
        },
        {
            'created_at': timezone.now() - timedelta(days=75),
            'accuracy': 79.8,
            'status': 'completed',
            'algorithm': 'Neural Network'
        }
    ]
    
    # Performans məlumatları (chart üçün)
    performance_labels = ['Yan', 'Fev', 'Mar', 'Apr', 'May', 'İyun']
    accuracy_data = [82, 84, 85, 86, 87, 87.5]
    precision_data = [80, 82, 83, 84, 85, 86]
    recall_data = [78, 80, 81, 82, 83, 84]
    
    # Emal statistikası
    processing_stats = {
        'completion_rate': 92
    }
    
    # Etibarlılıq qiyməti
    reliability_score = 88
    
    context = {
        'current_model': current_model,
        'available_features': available_features,
        'training_history': training_history,
        'performance_labels': json.dumps(performance_labels),
        'accuracy_data': accuracy_data,
        'precision_data': precision_data,
        'recall_data': recall_data,
        'processing_stats': processing_stats,
        'reliability_score': reliability_score,
        'title': _('AI Model İdarəetmə Paneli')
    }
    
    return render(request, 'dashboard/ai_management.html', context)


@login_required
def train_model(request):
    """
    Modeli yenidən təlim et
    """
    if request.method == 'POST':
        # Burada modeli təlim etmə məntiqi olacaq
        # Mock implementation for now
        return JsonResponse({
            'success': True,
            'message': _('Model uğurla təlim edildi'),
            'model_version': '1.2.4'
        })
    
    return JsonResponse({
        'success': False,
        'message': _('Yalnız POST sorğuları qəbul olunur')
    })


@login_required
def export_model(request):
    """
    Modeli ixrac et
    """
    # Burada modeli ixrac etmə məntiqi olacaq
    # Mock implementation for now
    return JsonResponse({
        'success': True,
        'message': _('Model uğurla ixrac edildi'),
        'download_url': '/downloads/model_1.2.3.pkl'
    })
