from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
import json

from .models import SentimentFeedback
from apps.evaluations.models import Response
from apps.accounts.models import User
from apps.departments.models import Department


@login_required
def sentiment_dashboard(request):
    """
    Sentiment Analysis Dashboard
    """
    # Get date filter parameters
    date_filter = request.GET.get('date_filter', '30')  # Default to last 30 days
    days = int(date_filter)
    start_date = timezone.now().date() - timedelta(days=days)
    
    # Total feedback count
    total_feedback = SentimentFeedback.objects.filter(created_at__date__gte=start_date).count()
    
    # Sentiment distribution
    sentiment_stats = SentimentFeedback.objects.filter(
        created_at__date__gte=start_date
    ).values('sentiment_label').annotate(count=Count('id'))
    
    # Calculate percentages
    positive_count = 0
    negative_count = 0
    neutral_count = 0
    
    for stat in sentiment_stats:
        if stat['sentiment_label'] == 'positive':
            positive_count = stat['count']
        elif stat['sentiment_label'] == 'negative':
            negative_count = stat['count']
        else:
            neutral_count = stat['count']
    
    total = positive_count + negative_count + neutral_count
    positive_percentage = round((positive_count / total * 100) if total > 0 else 0, 2)
    negative_percentage = round((negative_count / total * 100) if total > 0 else 0, 2)
    
    # Alert count (negative feedback)
    alert_count = negative_count
    
    # Sentiment trends over time
    trend_data = []
    for i in range(days):
        current_date = start_date + timedelta(days=i)
        daily_stats = SentimentFeedback.objects.filter(
            created_at__date=current_date
        ).values('sentiment_label').annotate(count=Count('id'))
        
        daily_positive = daily_negative = daily_neutral = 0
        for stat in daily_stats:
            if stat['sentiment_label'] == 'positive':
                daily_positive = stat['count']
            elif stat['sentiment_label'] == 'negative':
                daily_negative = stat['count']
            else:
                daily_neutral = stat['count']
        
        trend_data.append({
            'date': current_date.strftime('%Y-%m-%d'),
            'positive': daily_positive,
            'negative': daily_negative,
            'neutral': daily_neutral
        })
    
    # Extract data for chart
    trend_dates = [item['date'] for item in trend_data]
    positive_trends = [item['positive'] for item in trend_data]
    negative_trends = [item['negative'] for item in trend_data]
    neutral_trends = [item['neutral'] for item in trend_data]
    
    # Get negative feedback for detailed analysis
    negative_feedback = SentimentFeedback.objects.filter(
        sentiment_label='negative',
        created_at__date__gte=start_date
    ).order_by('-created_at')[:10]  # Get last 10 negative feedbacks
    
    context = {
        'total_feedback': total_feedback,
        'positive_percentage': positive_percentage,
        'negative_percentage': negative_percentage,
        'alert_count': alert_count,
        'positive_count': positive_count,
        'negative_count': negative_count,
        'neutral_count': neutral_count,
        'trend_dates': json.dumps(trend_dates),
        'positive_trends': positive_trends,
        'negative_trends': negative_trends,
        'neutral_trends': neutral_trends,
        'negative_feedback': negative_feedback,
    }
    
    return render(request, 'sentiment_analysis/dashboard.html', context)


@login_required
def feedback_detail(request, pk):
    """
    Detailed view of a specific feedback
    """
    feedback = get_object_or_404(SentimentFeedback, pk=pk)
    
    context = {
        'feedback': feedback
    }
    
    return render(request, 'sentiment_analysis/feedback_detail.html', context)


@login_required
def feedback_resolve(request, pk):
    """
    Mark feedback as resolved
    """
    feedback = get_object_or_404(SentimentFeedback, pk=pk)
    
    # Add resolution logic here
    feedback.is_resolved = True
    feedback.resolved_at = timezone.now()
    feedback.resolved_by = request.user
    feedback.save()
    
    # Add notification logic (optional)
    
    # Redirect back to dashboard or detail page
    return JsonResponse({'success': True, 'message': 'Feedback marked as resolved'})