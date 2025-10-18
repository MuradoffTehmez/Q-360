from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.db.models import Q, Count, Avg, Sum, Max
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
import json

from apps.departments.models import Department, Organization
from apps.accounts.models import User
from apps.evaluations.models import EvaluationCampaign, Response, EvaluationAssignment
from apps.recruitment.models import Application
from apps.leave_attendance.models import LeaveRequest, Attendance
from apps.dashboard.models import SystemKPI, DashboardWidget, AnalyticsReport, TrendData, ForecastData, RealTimeStat


class DashboardAPI(View):
    """
    Dashboard API sinifi
    """
    
    def get(self, request, endpoint):
        """
        Fərqli endpointlər üçün məlumat təmin edir
        """
        if endpoint == 'stats':
            return self.get_real_time_stats(request)
        elif endpoint == 'kpis':
            return self.get_kpi_data(request)
        elif endpoint == 'trends':
            return self.get_trend_data(request)
        elif endpoint == 'forecasts':
            return self.get_forecast_data(request)
        elif endpoint == 'reports':
            return self.get_report_data(request)
        elif endpoint == 'advanced-analytics':
            return self.get_advanced_analytics(request)
        else:
            return JsonResponse({'error': 'Endpoint tapılmadı'}, status=404)
    
    def get_real_time_stats(self, request):
        """
        Real vaxt statistikası
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
    
    def get_kpi_data(self, request):
        """
        KPI məlumatları
        """
        # Filter parametrləri
        kpi_type = request.GET.get('type', None)
        limit = int(request.GET.get('limit', 10))
        
        kpis = SystemKPI.objects.all().order_by('-created_at')
        
        if kpi_type:
            kpis = kpis.filter(kpi_type=kpi_type)
        
        kpis = kpis[:limit]
        
        data = []
        for kpi in kpis:
            data.append({
                'id': kpi.id,
                'name': kpi.name,
                'kpi_type': kpi.kpi_type,
                'value': float(kpi.value),
                'target': float(kpi.target) if kpi.target else None,
                'unit': kpi.unit,
                'period_start': kpi.period_start.isoformat() if kpi.period_start else None,
                'period_end': kpi.period_end.isoformat() if kpi.period_end else None,
                'created_at': kpi.created_at.isoformat() if kpi.created_at else None,
            })
        
        return JsonResponse({'kpis': data})
    
    def get_trend_data(self, request):
        """
        Trend məlumatları
        """
        data_type = request.GET.get('type', 'all')  # all, salary, performance, hiring
        department_id = request.GET.get('department_id', None)
        months = int(request.GET.get('months', 12))
        
        from datetime import date
        from dateutil.relativedelta import relativedelta
        
        end_date = date.today()
        start_date = end_date - relativedelta(months=months)
        
        trend_data = TrendData.objects.filter(period__range=[start_date, end_date])
        
        if data_type != 'all':
            trend_data = trend_data.filter(data_type=data_type)
        
        if department_id:
            trend_data = trend_data.filter(department_id=department_id)
        
        data = []
        for item in trend_data.order_by('period'):
            data.append({
                'date': item.period.isoformat(),
                'value': float(item.value),
                'data_type': item.data_type,
                'department': item.department.name if item.department else None,
            })
        
        return JsonResponse({'trends': data})
    
    def get_forecast_data(self, request):
        """
        Proqnoz məlumatları
        """
        forecast_type = request.GET.get('type', 'all')  # all, staffing, budget, performance
        department_id = request.GET.get('department_id', None)
        limit = int(request.GET.get('limit', 10))
        
        forecasts = ForecastData.objects.all().order_by('-forecast_date')
        
        if forecast_type != 'all':
            forecasts = forecasts.filter(forecast_type=forecast_type)
        
        if department_id:
            forecasts = forecasts.filter(department_id=department_id)
        
        forecasts = forecasts[:limit]
        
        data = []
        for forecast in forecasts:
            data.append({
                'id': forecast.id,
                'forecast_type': forecast.forecast_type,
                'forecast_date': forecast.forecast_date.isoformat(),
                'predicted_value': float(forecast.predicted_value),
                'confidence_level': float(forecast.confidence_level),
                'actual_value': float(forecast.actual_value) if forecast.actual_value else None,
                'explanation': forecast.explanation,
                'department': forecast.department.name if forecast.department else None,
                'created_at': forecast.created_at.isoformat() if forecast.created_at else None,
            })
        
        return JsonResponse({'forecasts': data})
    
    def get_advanced_analytics(self, request):
        """
        Genişləndirilmiş analitik məlumatlar
        """
        from .utils import get_advanced_trend_analysis
        
        data_type = request.GET.get('type', 'performance')
        department_id = request.GET.get('department_id', None)
        months = int(request.GET.get('months', 12))
        
        # Advanced trend analysis
        advanced_trend = get_advanced_trend_analysis(
            data_type=data_type,
            department_id=department_id,
            months=months
        )
        
        # Additional analytics
        from apps.evaluations.models import Response
        from apps.accounts.models import User
        from apps.compensation.models import SalaryInformation
        import numpy as np
        
        # Calculate volatility (standard deviation)
        values = [item['value'] for item in advanced_trend['data']]
        volatility = float(np.std(values)) if values else 0
        
        # Get department-specific analytics if department is specified
        department_analytics = None
        if department_id:
            from apps.departments.models import Department
            dept = Department.objects.get(id=department_id)
            dept_users_count = User.objects.filter(department_id=department_id).count()
            dept_avg_performance = Response.objects.filter(
                assignment__evaluatee__department_id=department_id
            ).aggregate(Avg('score'))['score__avg'] or 0
            
            department_analytics = {
                'name': dept.name,
                'user_count': dept_users_count,
                'avg_performance': float(dept_avg_performance)
            }
        
        # Get prediction accuracy if actual values available
        forecast_accuracy = None
        if data_type in ['salary', 'performance', 'hiring']:
            forecast_records = ForecastData.objects.filter(
                forecast_type=data_type
            ).exclude(actual_value=None)[:10]  # Last 10 with actual values
            
            if forecast_records:
                errors = []
                for record in forecast_records:
                    error = abs(float(record.predicted_value) - float(record.actual_value)) / float(record.actual_value) * 100 if float(record.actual_value) != 0 else float(record.predicted_value) * 100
                    errors.append(error)
                
                avg_error = sum(errors) / len(errors) if errors else 0
                forecast_accuracy = {
                    'avg_error_rate': avg_error,
                    'accuracy_rate': max(0, 100 - avg_error),
                    'sample_size': len(errors)
                }
        
        analytics_data = {
            'advanced_trend': advanced_trend,
            'volatility': volatility,
            'department_analytics': department_analytics,
            'forecast_accuracy': forecast_accuracy,
            'data_type': data_type,
            'months_analyzed': months
        }
        
        return JsonResponse({'analytics': analytics_data})
    
    def get_report_data(self, request):
        """
        Hesabat məlumatları
        """
        report_type = request.GET.get('type', None)
        limit = int(request.GET.get('limit', 10))
        
        reports = AnalyticsReport.objects.all().order_by('-created_at')
        
        if report_type:
            reports = reports.filter(report_type=report_type)
        
        reports = reports[:limit]
        
        data = []
        for report in reports:
            data.append({
                'id': report.id,
                'name': report.name,
                'report_type': report.report_type,
                'generated_by': {
                    'id': report.generated_by.id,
                    'username': report.generated_by.username,
                    'first_name': report.generated_by.first_name,
                    'last_name': report.generated_by.last_name,
                },
                'start_date': report.start_date.isoformat() if report.start_date else None,
                'end_date': report.end_date.isoformat() if report.end_date else None,
                'is_published': report.is_published,
                'created_at': report.created_at.isoformat() if report.created_at else None,
            })
        
        return JsonResponse({'reports': data})


@csrf_exempt
@login_required
@require_http_methods(["GET", "POST"])
def dashboard_api_endpoint(request, endpoint):
    """
    Dashboard API endpoint
    """
    api_view = DashboardAPI()
    
    if request.method == 'GET':
        return api_view.get(request, endpoint)
    elif request.method == 'POST':
        # POST üçün əlavə funksiyalar gələcəkdə əlavə olunacaq
        return JsonResponse({'error': 'POST methodu hələ dəstəklənmir'}, status=405)


@login_required
def dashboard_widget_config(request):
    """
    Dashboard widget konfiqurasiya endpointi
    """
    if request.method == 'GET':
        widgets = DashboardWidget.objects.filter(is_active=True).order_by('order')
        data = []
        for widget in widgets:
            data.append({
                'id': widget.id,
                'name': widget.name,
                'widget_type': widget.widget_type,
                'title': widget.title,
                'description': widget.description,
                'order': widget.order,
                'config': widget.config,
            })
        return JsonResponse({'widgets': data})
    
    elif request.method == 'POST':
        # Widget konfiqurasiyasını yeniləmək
        try:
            data = json.loads(request.body)
            widget_id = data.get('widget_id')
            new_config = data.get('config', {})
            
            widget = DashboardWidget.objects.get(id=widget_id)
            widget.config = new_config
            widget.save()
            
            return JsonResponse({'status': 'success', 'message': 'Widget konfiqurasiyası yeniləndi'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})


@login_required
def department_analytics(request):
    """
    Bölmələr üzrə analitika
    """
    from apps.dashboard.utils import get_salary_trends, get_performance_trends, get_hiring_trends
    
    department_id = request.GET.get('department_id', None)
    months = int(request.GET.get('months', 12))
    
    if department_id:
        # Müəyyən bölmə üçün analitika
        dept = Department.objects.get(id=department_id)
        
        salary_trends = get_salary_trends(department_id=department_id, months=months)
        performance_trends = get_performance_trends(department_id=department_id, months=months)
        hiring_trends = get_hiring_trends(department_id=department_id, months=months)
        
        # Əlavə statistikalar
        dept_users = User.objects.filter(department_id=department_id).count()
        dept_avg_performance = Response.objects.filter(
            assignment__evaluatee__department_id=department_id
        ).aggregate(Avg('score'))['score__avg'] or 0
        
        data = {
            'department': {
                'id': dept.id,
                'name': dept.name,
                'user_count': dept_users,
                'avg_performance': round(dept_avg_performance, 2)
            },
            'trends': {
                'salary': salary_trends,
                'performance': performance_trends,
                'hiring': hiring_trends
            }
        }
    else:
        # Bütün bölmələr üzrə analitika
        departments = Department.objects.all()
        dept_analytics = []
        
        for dept in departments:
            dept_users = User.objects.filter(department=dept).count()
            dept_avg_performance = Response.objects.filter(
                assignment__evaluatee__department=dept
            ).aggregate(Avg('score'))['score__avg'] or 0
            
            dept_analytics.append({
                'id': dept.id,
                'name': dept.name,
                'user_count': dept_users,
                'avg_performance': round(dept_avg_performance, 2)
            })
        
        data = {
            'departments': dept_analytics,
            'total_departments': len(dept_analytics),
            'total_users': User.objects.count()
        }
    
    return JsonResponse(data)
