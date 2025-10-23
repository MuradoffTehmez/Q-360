"""
Dashboard API endpoints for real-time data.
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Count, Avg, Q
from datetime import timedelta

from apps.evaluations.models import EvaluationCampaign, EvaluationResult
from apps.training.models import UserTraining
from apps.accounts.models import User
from apps.development_plans.models import DevelopmentGoal


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    """
    Get real-time dashboard statistics.
    """
    user = request.user

    # Time ranges
    now = timezone.now()
    last_30_days = now - timedelta(days=30)
    last_7_days = now - timedelta(days=7)

    # User stats
    if user.is_admin():
        total_users = User.objects.filter(is_active=True).count()
        active_users = User.objects.filter(
            last_login__gte=last_30_days,
            is_active=True
        ).count()
    else:
        total_users = User.objects.filter(
            department=user.department,
            is_active=True
        ).count()
        active_users = User.objects.filter(
            department=user.department,
            last_login__gte=last_30_days,
            is_active=True
        ).count()

    # Evaluation stats
    if user.is_admin():
        active_campaigns = EvaluationCampaign.objects.filter(
            status='active'
        ).count()
        completed_evaluations = EvaluationResult.objects.filter(
            status='completed',
            completed_at__gte=last_30_days
        ).count()
        avg_score = EvaluationResult.objects.filter(
            status='completed'
        ).aggregate(Avg('overall_score'))['overall_score__avg'] or 0
    else:
        active_campaigns = EvaluationCampaign.objects.filter(
            status='active',
            department=user.department
        ).count()
        completed_evaluations = EvaluationResult.objects.filter(
            status='completed',
            completed_at__gte=last_30_days,
            evaluated_user__department=user.department
        ).count()
        avg_score = EvaluationResult.objects.filter(
            status='completed',
            evaluated_user__department=user.department
        ).aggregate(Avg('overall_score'))['overall_score__avg'] or 0

    # Training stats
    if user.is_admin():
        completed_trainings = UserTraining.objects.filter(
            status='completed',
            completed_at__gte=last_30_days
        ).count()
        in_progress_trainings = UserTraining.objects.filter(
            status='in_progress'
        ).count()
    else:
        completed_trainings = UserTraining.objects.filter(
            user=user,
            status='completed',
            completed_at__gte=last_30_days
        ).count()
        in_progress_trainings = UserTraining.objects.filter(
            user=user,
            status='in_progress'
        ).count()

    # Development goals
    if user.is_admin():
        active_goals = DevelopmentGoal.objects.filter(
            status='in_progress'
        ).count()
        completed_goals = DevelopmentGoal.objects.filter(
            status='completed',
            completed_at__gte=last_30_days
        ).count()
    else:
        active_goals = DevelopmentGoal.objects.filter(
            user=user,
            status='in_progress'
        ).count()
        completed_goals = DevelopmentGoal.objects.filter(
            user=user,
            status='completed',
            completed_at__gte=last_30_days
        ).count()

    return Response({
        'success': True,
        'stats': {
            'users': {
                'total': total_users,
                'active': active_users,
                'growth_rate': round((active_users / total_users * 100) if total_users > 0 else 0, 1)
            },
            'evaluations': {
                'active_campaigns': active_campaigns,
                'completed_last_30_days': completed_evaluations,
                'average_score': round(avg_score, 2)
            },
            'training': {
                'completed_last_30_days': completed_trainings,
                'in_progress': in_progress_trainings
            },
            'goals': {
                'active': active_goals,
                'completed_last_30_days': completed_goals
            }
        }
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_trends(request):
    """
    Get trend data for charts (last 30 days).
    """
    user = request.user
    now = timezone.now()

    # Generate last 30 days
    days = []
    evaluation_counts = []
    training_counts = []

    for i in range(29, -1, -1):
        day = now - timedelta(days=i)
        days.append(day.strftime('%Y-%m-%d'))

        # Evaluation completions for this day
        if user.is_admin():
            eval_count = EvaluationResult.objects.filter(
                status='completed',
                completed_at__date=day.date()
            ).count()
        else:
            eval_count = EvaluationResult.objects.filter(
                status='completed',
                completed_at__date=day.date(),
                evaluated_user__department=user.department
            ).count()
        evaluation_counts.append(eval_count)

        # Training completions for this day
        if user.is_admin():
            training_count = UserTraining.objects.filter(
                status='completed',
                completed_at__date=day.date()
            ).count()
        else:
            training_count = UserTraining.objects.filter(
                user=user,
                status='completed',
                completed_at__date=day.date()
            ).count()
        training_counts.append(training_count)

    return Response({
        'success': True,
        'trends': {
            'labels': days,
            'datasets': [
                {
                    'label': 'Tamamlanmış Qiymətləndirmələr',
                    'data': evaluation_counts,
                    'borderColor': 'rgb(75, 192, 192)',
                    'backgroundColor': 'rgba(75, 192, 192, 0.2)',
                    'tension': 0.4
                },
                {
                    'label': 'Tamamlanmış Təlimlər',
                    'data': training_counts,
                    'borderColor': 'rgb(153, 102, 255)',
                    'backgroundColor': 'rgba(153, 102, 255, 0.2)',
                    'tension': 0.4
                }
            ]
        }
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_forecasting(request):
    """
    Get forecasting data for predictions.
    """
    user = request.user
    now = timezone.now()

    # Historical data (last 90 days)
    historical_days = []
    historical_scores = []

    for i in range(89, -1, -1):
        day = now - timedelta(days=i)
        historical_days.append(day.strftime('%Y-%m-%d'))

        if user.is_admin():
            avg_score = EvaluationResult.objects.filter(
                status='completed',
                completed_at__date=day.date()
            ).aggregate(Avg('overall_score'))['overall_score__avg']
        else:
            avg_score = EvaluationResult.objects.filter(
                status='completed',
                completed_at__date=day.date(),
                evaluated_user__department=user.department
            ).aggregate(Avg('overall_score'))['overall_score__avg']

        historical_scores.append(round(avg_score, 2) if avg_score else 0)

    # Simple forecasting (moving average)
    forecast_days = []
    forecast_scores = []

    if len(historical_scores) > 0:
        # Calculate moving average for last 7 days
        window = 7
        last_avg = sum(historical_scores[-window:]) / window if len(historical_scores) >= window else sum(historical_scores) / len(historical_scores)

        # Forecast next 30 days with slight growth trend (1% per week)
        for i in range(1, 31):
            day = now + timedelta(days=i)
            forecast_days.append(day.strftime('%Y-%m-%d'))

            # Add slight growth trend
            growth_factor = 1 + (0.01 * (i / 7))
            forecast_score = min(last_avg * growth_factor, 5.0)  # Cap at 5.0
            forecast_scores.append(round(forecast_score, 2))

    return Response({
        'success': True,
        'forecasting': {
            'historical': {
                'labels': historical_days,
                'data': historical_scores
            },
            'forecast': {
                'labels': forecast_days,
                'data': forecast_scores
            },
            'combined_labels': historical_days + forecast_days,
            'combined_datasets': [
                {
                    'label': 'Tarixi Məlumat',
                    'data': historical_scores + [None] * len(forecast_scores),
                    'borderColor': 'rgb(54, 162, 235)',
                    'backgroundColor': 'rgba(54, 162, 235, 0.2)',
                    'tension': 0.4
                },
                {
                    'label': 'Proqnoz',
                    'data': [None] * len(historical_scores) + forecast_scores,
                    'borderColor': 'rgb(255, 99, 132)',
                    'backgroundColor': 'rgba(255, 99, 132, 0.2)',
                    'borderDash': [5, 5],
                    'tension': 0.4
                }
            ]
        }
    })
