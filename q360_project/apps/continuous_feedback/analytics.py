"""
Real-time analytics for continuous feedback system.
Provides trend analysis, sentiment tracking, and feedback insights.
"""
from django.db.models import Count, Avg, Q, F
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from .models import QuickFeedback, FeedbackBank


class FeedbackAnalytics:
    """
    Real-time feedback analytics engine.
    Analyzes feedback trends, patterns, and provides actionable insights.
    """

    def __init__(self, user=None, department=None, time_period_days=30):
        """
        Initialize analytics engine.

        Args:
            user: User instance to analyze (optional)
            department: Department instance to analyze (optional)
            time_period_days: Number of days to analyze (default: 30)
        """
        self.user = user
        self.department = department
        self.time_period_days = time_period_days
        self.start_date = timezone.now() - timedelta(days=time_period_days)

    def get_feedback_trends(self):
        """
        Get feedback trends over time period.
        Returns daily/weekly breakdown of feedback metrics.
        """
        queryset = self._get_base_queryset()

        # Get daily feedback counts
        daily_counts = queryset.filter(
            created_at__gte=self.start_date
        ).extra(
            select={'day': 'date(created_at)'}
        ).values('day').annotate(
            total=Count('id'),
            recognition=Count('id', filter=Q(feedback_type='recognition')),
            improvement=Count('id', filter=Q(feedback_type='improvement')),
            avg_rating=Avg('rating', filter=Q(rating__isnull=False))
        ).order_by('day')

        return list(daily_counts)

    def get_feedback_by_source(self):
        """
        Analyze feedback distribution by source relationship (360-degree).
        """
        queryset = self._get_base_queryset()

        source_breakdown = queryset.filter(
            created_at__gte=self.start_date,
            is_part_of_360=True
        ).values('source_relationship').annotate(
            count=Count('id'),
            avg_rating=Avg('rating', filter=Q(rating__isnull=False))
        ).order_by('-count')

        return list(source_breakdown)

    def get_sentiment_trends(self):
        """
        Analyze sentiment trends over time.
        Tracks positive, neutral, and negative feedback patterns.
        """
        queryset = self._get_base_queryset()

        sentiment_data = queryset.filter(
            created_at__gte=self.start_date,
            rating__isnull=False
        ).extra(
            select={'week': "strftime('%%Y-%%W', created_at)"}
        ).values('week').annotate(
            total=Count('id'),
            positive=Count('id', filter=Q(rating__gte=4)),
            neutral=Count('id', filter=Q(rating=3)),
            negative=Count('id', filter=Q(rating__lte=2)),
            avg_rating=Avg('rating')
        ).order_by('week')

        return list(sentiment_data)

    def get_top_competencies(self, limit=10):
        """
        Get most frequently mentioned competencies in feedback.
        """
        queryset = self._get_base_queryset()

        top_competencies = queryset.filter(
            created_at__gte=self.start_date,
            related_competency__isnull=False
        ).values(
            'related_competency__name',
            'related_competency__id'
        ).annotate(
            mention_count=Count('id'),
            avg_rating=Avg('rating', filter=Q(rating__isnull=False))
        ).order_by('-mention_count')[:limit]

        return list(top_competencies)

    def get_feedback_velocity(self):
        """
        Calculate feedback velocity - rate of feedback over time.
        Useful for identifying engagement trends.
        """
        queryset = self._get_base_queryset()

        # Calculate feedback per week
        current_period = queryset.filter(
            created_at__gte=self.start_date
        ).count()

        # Previous period for comparison
        previous_start = self.start_date - timedelta(days=self.time_period_days)
        previous_period = queryset.filter(
            created_at__gte=previous_start,
            created_at__lt=self.start_date
        ).count()

        # Calculate change percentage
        if previous_period > 0:
            change_percent = ((current_period - previous_period) / previous_period) * 100
        else:
            change_percent = 100 if current_period > 0 else 0

        return {
            'current_period_count': current_period,
            'previous_period_count': previous_period,
            'change_percentage': round(change_percent, 2),
            'avg_per_day': round(current_period / self.time_period_days, 2)
        }

    def get_response_rate(self):
        """
        Calculate feedback response and acknowledgment rate.
        """
        queryset = self._get_base_queryset()

        total_feedback = queryset.filter(
            created_at__gte=self.start_date
        ).count()

        if total_feedback == 0:
            return {
                'total_feedback': 0,
                'read_count': 0,
                'responded_count': 0,
                'read_rate': 0,
                'response_rate': 0
            }

        read_count = queryset.filter(
            created_at__gte=self.start_date,
            is_read=True
        ).count()

        responded_count = queryset.filter(
            created_at__gte=self.start_date,
            recipient_response__isnull=False
        ).exclude(recipient_response='').count()

        return {
            'total_feedback': total_feedback,
            'read_count': read_count,
            'responded_count': responded_count,
            'read_rate': round((read_count / total_feedback) * 100, 2),
            'response_rate': round((responded_count / total_feedback) * 100, 2)
        }

    def get_feedback_quality_score(self):
        """
        Calculate overall feedback quality score based on multiple factors.
        """
        queryset = self._get_base_queryset()

        recent_feedback = queryset.filter(created_at__gte=self.start_date)

        # Factors for quality score
        total_count = recent_feedback.count()
        if total_count == 0:
            return 0

        # Factor 1: Average rating (40%)
        avg_rating = recent_feedback.filter(
            rating__isnull=False
        ).aggregate(avg=Avg('rating'))['avg'] or 0

        # Factor 2: Competency linkage rate (30%)
        with_competency = recent_feedback.filter(
            related_competency__isnull=False
        ).count()
        competency_rate = (with_competency / total_count) * 5

        # Factor 3: Response rate (20%)
        response_metrics = self.get_response_rate()
        response_score = (response_metrics['response_rate'] / 100) * 5

        # Factor 4: Context/detail richness (10%)
        with_context = recent_feedback.exclude(
            Q(context='') | Q(context__isnull=True)
        ).count()
        context_score = (with_context / total_count) * 5

        # Calculate weighted quality score (out of 5)
        quality_score = (
            (avg_rating * 0.4) +
            (competency_rate * 0.3) +
            (response_score * 0.2) +
            (context_score * 0.1)
        )

        return round(quality_score, 2)

    def get_360_degree_completeness(self, user=None):
        """
        Analyze completeness of 360-degree feedback for a user.
        """
        target_user = user or self.user
        if not target_user:
            return None

        # Expected sources for comprehensive 360 feedback
        expected_sources = ['self', 'manager', 'peer', 'direct_report']

        received_feedback = QuickFeedback.objects.filter(
            recipient=target_user,
            is_part_of_360=True,
            created_at__gte=self.start_date
        )

        source_coverage = {}
        for source in expected_sources:
            count = received_feedback.filter(source_relationship=source).count()
            source_coverage[source] = {
                'count': count,
                'has_feedback': count > 0
            }

        # Calculate completeness percentage
        sources_covered = sum(1 for s in source_coverage.values() if s['has_feedback'])
        completeness = (sources_covered / len(expected_sources)) * 100

        return {
            'completeness_percentage': round(completeness, 2),
            'sources_covered': sources_covered,
            'total_sources': len(expected_sources),
            'source_breakdown': source_coverage,
            'total_feedback_count': received_feedback.count()
        }

    def get_engagement_metrics(self):
        """
        Calculate engagement metrics for feedback system.
        """
        queryset = self._get_base_queryset()

        total_feedback = queryset.filter(created_at__gte=self.start_date)

        # Unique senders and recipients
        unique_senders = total_feedback.values('sender').distinct().count()
        unique_recipients = total_feedback.values('recipient').distinct().count()

        # Public recognition engagement
        public_feedback = total_feedback.filter(visibility='public')

        return {
            'total_feedback': total_feedback.count(),
            'unique_senders': unique_senders,
            'unique_recipients': unique_recipients,
            'public_feedback_count': public_feedback.count(),
            'anonymous_feedback_count': total_feedback.filter(is_anonymous=True).count(),
            'avg_feedback_per_user': round(
                total_feedback.count() / max(unique_senders, 1), 2
            )
        }

    def get_trend_insights(self):
        """
        Generate actionable insights from feedback trends.
        """
        velocity = self.get_feedback_velocity()
        quality = self.get_feedback_quality_score()
        response_rate = self.get_response_rate()

        insights = []

        # Velocity insights
        if velocity['change_percentage'] > 20:
            insights.append({
                'type': 'positive',
                'category': 'engagement',
                'message': f"Feedback artıb: {velocity['change_percentage']:.1f}% artım müşahidə olunur",
                'metric': velocity
            })
        elif velocity['change_percentage'] < -20:
            insights.append({
                'type': 'warning',
                'category': 'engagement',
                'message': f"Feedback azalıb: {abs(velocity['change_percentage']):.1f}% azalma",
                'metric': velocity
            })

        # Quality insights
        if quality < 3.0:
            insights.append({
                'type': 'warning',
                'category': 'quality',
                'message': "Feedback keyfiyyəti aşağıdır. Daha ətraflı və strukturlaşdırılmış feedback tövsiyə olunur",
                'metric': {'quality_score': quality}
            })
        elif quality >= 4.0:
            insights.append({
                'type': 'positive',
                'category': 'quality',
                'message': "Feedback keyfiyyəti yüksəkdir",
                'metric': {'quality_score': quality}
            })

        # Response rate insights
        if response_rate['response_rate'] < 30:
            insights.append({
                'type': 'warning',
                'category': 'engagement',
                'message': "Cavab verənlərin sayı azdır. Feedback-ə cavab vermək tövsiyə olunur",
                'metric': response_rate
            })

        return insights

    def _get_base_queryset(self):
        """
        Get base queryset filtered by user or department if specified.
        """
        queryset = QuickFeedback.objects.all()

        if self.user:
            queryset = queryset.filter(
                Q(sender=self.user) | Q(recipient=self.user)
            )
        elif self.department:
            queryset = queryset.filter(
                Q(sender__department=self.department) |
                Q(recipient__department=self.department)
            )

        return queryset


class FeedbackVisualization:
    """
    Helper class for generating visualization-ready data.
    """

    @staticmethod
    def prepare_timeline_data(analytics_instance):
        """
        Prepare data for timeline visualization.
        """
        trends = analytics_instance.get_feedback_trends()

        return {
            'labels': [t['day'].strftime('%Y-%m-%d') if hasattr(t['day'], 'strftime') else str(t['day']) for t in trends],
            'datasets': [
                {
                    'label': 'Ümumi Feedback',
                    'data': [t['total'] for t in trends],
                    'color': '#4CAF50'
                },
                {
                    'label': 'Təşəkkür',
                    'data': [t['recognition'] for t in trends],
                    'color': '#2196F3'
                },
                {
                    'label': 'İnkişaf Təklifləri',
                    'data': [t['improvement'] for t in trends],
                    'color': '#FF9800'
                }
            ]
        }

    @staticmethod
    def prepare_360_radar_chart(analytics_instance, user):
        """
        Prepare 360-degree feedback radar chart data.
        """
        completeness = analytics_instance.get_360_degree_completeness(user)
        if not completeness:
            return None

        source_labels = {
            'self': 'Özünüdəyərləndirmə',
            'manager': 'Menecer',
            'peer': 'Həmkarlar',
            'direct_report': 'Tabeliklər'
        }

        return {
            'labels': [source_labels.get(k, k) for k in completeness['source_breakdown'].keys()],
            'values': [v['count'] for v in completeness['source_breakdown'].values()],
            'completeness': completeness['completeness_percentage']
        }
