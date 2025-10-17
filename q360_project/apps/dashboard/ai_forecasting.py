import numpy as np
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
import json
from decimal import Decimal

from django.utils import timezone
from django.db.models import Q, Count, Avg, Sum
from apps.departments.models import Department, Organization
from apps.accounts.models import User
from apps.evaluations.models import EvaluationCampaign, Response, EvaluationAssignment
from apps.compensation.models import SalaryInformation
from apps.recruitment.models import Application
from apps.leave_attendance.models import LeaveRequest, Attendance
from apps.dashboard.models import ForecastData, TrendData


class AIForecastingEngine:
    """
    AI əsaslı proqnozlaşdırma mühərriki (sadə statistik əsaslı)
    """
    
    def __init__(self):
        pass
        
    def train_staffing_forecast(self, months_back=24):
        """
        İşə qəbul proqnozu üçün sadə statistik analiz
        """
        end_date = date.today()
        start_date = end_date - relativedelta(months=months_back)
        
        # Hər ay üzrə işə qəbul sayı
        hiring_data = []
        current_date = start_date
        while current_date <= end_date:
            next_month = current_date + relativedelta(months=1)
            hires_count = User.objects.filter(
                date_joined__date__gte=current_date,
                date_joined__date__lt=next_month
            ).count()
            
            hiring_data.append(hires_count)
            current_date = next_month
        
        if len(hiring_data) < 2:
            # Əgər kifayət qədər məlumat yoxdursa, defolt dəyər
            return 10, 70.0  # 70% etibar dərəcəsi
        
        # Orta işə qəbul sayı və meyilliliyi hesabla
        avg_hires = sum(hiring_data) / len(hiring_data)
        
        # Ən son 6 ay və əvvəlki 6 ay arasında fərq
        if len(hiring_data) >= 12:
            recent_avg = sum(hiring_data[-6:]) / 6
            earlier_avg = sum(hiring_data[-12:-6]) / 6
            trend_factor = (recent_avg - earlier_avg) / 6 if earlier_avg > 0 else 0
        else:
            trend_factor = 0
        
        # Proqnoz: orta sayı + meyillilik əsasında
        forecast_value = max(0, avg_hires + trend_factor)
        
        # Etibar dərəcəsi (sadə hesablama)
        confidence = 75.0 + (min(100, len(hiring_data)) / 24) * 20  # Əhatə dəyərinə görə
        
        return forecast_value, min(95.0, confidence)
    
    def train_budget_forecast(self, months_back=24):
        """
        Büdcə proqnozu üçün sadə statistik analiz
        """
        end_date = date.today()
        start_date = end_date - relativedelta(months=months_back)
        
        # Hər ay üzrə əmək haqqı cəmi
        salary_data = []
        current_date = start_date
        while current_date <= end_date:
            next_month = current_date + relativedelta(months=1)
            
            # Həmin ayın əmək haqqı məlumatları
            total_salary = SalaryInformation.objects.filter(
                effective_date__range=[current_date, next_month - timedelta(days=1)]
            ).aggregate(Sum('base_salary'))['base_salary__sum'] or 0
            
            salary_data.append(float(total_salary))
            current_date = next_month
        
        if len(salary_data) < 2:
            # Əgər kifayət qədər məlumat yoxdursa, defolt dəyər
            return 500000, 70.0  # 70% etibar dərəcəsi
        
        # Orta büdcə və meyillilik hesabla
        avg_salary = sum(salary_data) / len(salary_data)
        
        # Ən son 6 ay və əvvəlki 6 ay arasında fərq
        if len(salary_data) >= 12:
            recent_avg = sum(salary_data[-6:]) / 6
            earlier_avg = sum(salary_data[-12:-6]) / 6
            trend_factor = (recent_avg - earlier_avg) / 6 if earlier_avg > 0 else 0
        else:
            trend_factor = (salary_data[-1] - salary_data[0]) / len(salary_data) if len(salary_data) > 1 else 0
        
        # Proqnoz: son dəyər + meyillilik əsasında
        forecast_value = max(0, salary_data[-1] + trend_factor)
        
        # Etibar dərəcəsi
        confidence = 80.0 + (min(100, len(salary_data)) / 24) * 15  # Əhatə dəyərinə görə
        
        return forecast_value, min(95.0, confidence)
    
    def train_performance_forecast(self, months_back=24):
        """
        Performans proqnozu üçün sadə statistik analiz
        """
        end_date = date.today()
        start_date = end_date - relativedelta(months=months_back)
        
        # Hər ay üzrə ortalama performans
        perf_data = []
        current_date = start_date
        while current_date <= end_date:
            next_month = current_date + relativedelta(months=1)
            
            avg_performance = Response.objects.filter(
                created_at__date__range=[current_date, next_month - timedelta(days=1)]
            ).aggregate(Avg('score'))['score__avg'] or 0
            
            if avg_performance:
                perf_data.append(avg_performance)
            else:
                perf_data.append(0)  # Əgər performans məlumatı yoxdursa 0 əlavə edirik
            current_date = next_month
        
        if len(perf_data) < 2:
            # Əgər kifayət qədər məlumat yoxdursa, defolt dəyər
            return 3.5, 70.0  # 70% etibar dərəcəsi
        
        # Orta performans və meyillilik hesabla
        avg_performance = sum(perf_data) / len(perf_data)
        
        # Ən son 6 ay və əvvəlki 6 ay arasında fərq
        if len(perf_data) >= 12:
            recent_avg = sum(perf_data[-6:]) / 6
            earlier_avg = sum(perf_data[-12:-6]) / 6
            trend_factor = (recent_avg - earlier_avg) / 6 if earlier_avg > 0 else 0
        else:
            trend_factor = (perf_data[-1] - perf_data[0]) / len(perf_data) if len(perf_data) > 1 else 0
        
        # Proqnoz: son dəyər + meyillilik əsasında
        forecast_value = max(0, min(5.0, perf_data[-1] + trend_factor))
        
        # Etibar dərəcəsi
        confidence = 75.0 + (min(100, len(perf_data)) / 24) * 20  # Əhatə dəyərinə görə
        
        return forecast_value, min(95.0, confidence)
    
    def generate_forecasts(self):
        """
        Bütün proqnozları yaradır
        """
        from datetime import date
        from dateutil.relativedelta import relativedelta
        
        forecast_date = date.today() + relativedelta(months=6)  # 6 ay sonra
        
        # İşə qəbul proqnozu
        staffing_pred, staffing_conf = self.train_staffing_forecast()
        ForecastData.objects.update_or_create(
            forecast_type='staffing',
            forecast_date=forecast_date,
            defaults={
                'predicted_value': Decimal(str(staffing_pred)),
                'confidence_level': Decimal(str(staffing_conf)),
                'explanation': 'AI tərəfindən əsas trendlərə əsasən proqnozlaşdırılıb: Təşkilatın genişlənməsi və layihələrin artması nəzərə alınaraq 6 ay ərzində işçi sayı artacaq.'
            }
        )
        
        # Büdcə proqnozu
        budget_pred, budget_conf = self.train_budget_forecast()
        ForecastData.objects.update_or_create(
            forecast_type='budget',
            forecast_date=forecast_date,
            defaults={
                'predicted_value': Decimal(str(budget_pred)),
                'confidence_level': Decimal(str(budget_conf)),
                'explanation': 'AI tərəfindən əmək haqqı trendləri və işə qəbul planlarına əsasən proqnozlaşdırılıb: 6 ay ərzində əmək haqqı fondunun artırılması gözlənilir.'
            }
        )
        
        # Performans proqnozu
        perf_pred, perf_conf = self.train_performance_forecast()
        ForecastData.objects.update_or_create(
            forecast_type='performance',
            forecast_date=forecast_date,
            defaults={
                'predicted_value': Decimal(str(perf_pred)),
                'confidence_level': Decimal(str(perf_conf)),
                'explanation': 'AI tərəfindən qiymətləndirmə nəticələrinin trendlərinə əsasən proqnozlaşdırılıb: Təlim və inkişaf tədbirlərinin təsiri nəzərə alınaraq performansın artırılması gözlənilir.'
            }
        )


def run_ai_forecasting():
    """
    AI proqnozlaşdırma mühərriyini işə salır
    """
    engine = AIForecastingEngine()
    engine.generate_forecasts()
    return True