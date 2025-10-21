"""
Template views for continuous feedback app.
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from .models import QuickFeedback, FeedbackBank, PublicRecognition, FeedbackTag
from apps.accounts.models import User


@login_required
def send_feedback_view(request):
    """Send quick feedback to a colleague."""
    if request.method == 'POST':
        # Process feedback submission
        recipient_id = request.POST.get('recipient')
        feedback_type = request.POST.get('feedback_type')
        visibility = request.POST.get('visibility')
        title = request.POST.get('title')
        message = request.POST.get('message')
        is_anonymous = request.POST.get('is_anonymous') == 'on'

        try:
            recipient = User.objects.get(id=recipient_id)

            feedback = QuickFeedback.objects.create(
                sender=request.user,
                recipient=recipient,
                feedback_type=feedback_type,
                visibility=visibility,
                title=title,
                message=message,
                is_anonymous=is_anonymous
            )

            # If public recognition, create PublicRecognition
            if feedback_type == 'recognition' and visibility == 'public':
                PublicRecognition.objects.create(feedback=feedback)

            # Update recipient's feedback bank
            bank, created = FeedbackBank.objects.get_or_create(user=recipient)
            bank.update_stats()

            messages.success(request, 'Rəyiniz uğurla göndərildi!')
            return redirect('continuous_feedback:my-feedback')
        except Exception as e:
            messages.error(request, f'Xəta baş verdi: {str(e)}')

    # Get all active users except current user
    users = User.objects.filter(is_active=True).exclude(id=request.user.id).order_by('first_name', 'last_name')

    # Get available tags
    tags = FeedbackTag.objects.filter(is_active=True)

    context = {
        'users': users,
        'tags': tags,
    }

    return render(request, 'continuous_feedback/send_feedback.html', context)


@login_required
def my_feedback_view(request):
    """View feedback sent by current user."""
    # Get sent feedback
    sent_feedback = QuickFeedback.objects.filter(
        sender=request.user
    ).select_related('recipient').order_by('-created_at')

    # Filter by type
    type_filter = request.GET.get('type', '')
    if type_filter:
        sent_feedback = sent_feedback.filter(feedback_type=type_filter)

    # Statistics
    stats = {
        'total_sent': sent_feedback.count(),
        'recognitions': sent_feedback.filter(feedback_type='recognition').count(),
        'improvements': sent_feedback.filter(feedback_type='improvement').count(),
        'read': sent_feedback.filter(is_read=True).count(),
    }

    context = {
        'sent_feedback': sent_feedback,
        'type_filter': type_filter,
        'stats': stats,
    }

    return render(request, 'continuous_feedback/my_feedback.html', context)


@login_required
def received_feedback_view(request):
    """View feedback received by current user."""
    # Get received feedback
    received_feedback = QuickFeedback.objects.filter(
        recipient=request.user
    ).select_related('sender').order_by('-created_at')

    # Mark as read when viewed
    unread = received_feedback.filter(is_read=False)
    for feedback in unread:
        feedback.is_read = True
        feedback.read_at = timezone.now()
        feedback.save()

    # Filter by type
    type_filter = request.GET.get('type', '')
    if type_filter:
        received_feedback = received_feedback.filter(feedback_type=type_filter)

    # Statistics
    stats = {
        'total_received': received_feedback.count(),
        'recognitions': received_feedback.filter(feedback_type='recognition').count(),
        'improvements': received_feedback.filter(feedback_type='improvement').count(),
        'this_month': received_feedback.filter(created_at__month=timezone.now().month).count(),
    }

    context = {
        'received_feedback': received_feedback,
        'type_filter': type_filter,
        'stats': stats,
    }

    return render(request, 'continuous_feedback/received_feedback.html', context)


@login_required
def my_feedback_bank_view(request):
    """View user's feedback bank with aggregated statistics."""
    # Get or create feedback bank
    bank, created = FeedbackBank.objects.get_or_create(user=request.user)

    if created or not bank.last_feedback_date:
        bank.update_stats()

    # Get all received feedback
    all_feedback = QuickFeedback.objects.filter(
        recipient=request.user
    ).select_related('sender').order_by('-created_at')

    # Recent feedback
    recent_feedback = all_feedback[:10]

    # Top senders (who gave most feedback)
    top_senders = all_feedback.values('sender__first_name', 'sender__last_name').annotate(
        count=Count('id')
    ).order_by('-count')[:5]

    context = {
        'bank': bank,
        'recent_feedback': recent_feedback,
        'top_senders': top_senders,
        'all_feedback_count': all_feedback.count(),
    }

    return render(request, 'continuous_feedback/my_feedback_bank.html', context)


@login_required
def recognition_feed_view(request):
    """Public recognition feed - social feed of appreciation."""
    # Get public recognitions
    recognitions = PublicRecognition.objects.select_related(
        'feedback__sender',
        'feedback__recipient'
    ).prefetch_related(
        'likes',
        'comments'
    ).order_by('-published_at')

    # Filter: featured first
    featured = recognitions.filter(is_featured=True)
    regular = recognitions.filter(is_featured=False)

    context = {
        'featured_recognitions': featured[:3],
        'recognitions': regular[:20],
    }

    return render(request, 'continuous_feedback/recognition_feed.html', context)


@login_required
def proactive_feedback_suggestions(request):
    """
    Təşəbbüskar Rəy Təklifləri - AI-powered suggestions for who to give feedback to.

    Funksiyalar:
    - Son rəy tarixi əsasılı xatırlatmalar
    - Komanda üzvlərinə rəy təklifləri
    - Son layihə iştirakçılarına rəy təklifləri
    - Rəy statistikaları və təşviqlər
    """
    from datetime import timedelta
    from django.db.models import Max

    user = request.user

    # Get supervisor first (needed for exclusion list)
    supervisor = user.supervisor if hasattr(user, 'supervisor') else None

    # Get user's team members (colleagues in same department)
    # Exclude supervisor to avoid duplication
    exclude_ids = [user.id]
    if supervisor:
        exclude_ids.append(supervisor.id)

    team_members = User.objects.filter(
        is_active=True,
        department=user.department
    ).exclude(id__in=exclude_ids) if user.department else User.objects.none()

    # Get user's subordinates if manager
    subordinates = user.get_subordinates() if hasattr(user, 'get_subordinates') and user.is_manager() else []

    # Calculate days since last feedback to each person
    suggestions = []

    # 1. Team members suggestions
    for member in team_members[:10]:  # Limit to 10
        last_feedback = QuickFeedback.objects.filter(
            sender=user,
            recipient=member
        ).aggregate(Max('created_at'))['created_at__max']

        days_since_feedback = None
        priority = 'medium'

        if last_feedback:
            days_since_feedback = (timezone.now() - last_feedback).days
            if days_since_feedback > 30:
                priority = 'high'
            elif days_since_feedback > 14:
                priority = 'medium'
            else:
                priority = 'low'
        else:
            # Never given feedback
            priority = 'high'
            days_since_feedback = 999

        suggestions.append({
            'user': member,
            'relationship': 'Həmkar',
            'days_since_feedback': days_since_feedback,
            'last_feedback_date': last_feedback,
            'priority': priority,
            'reason': 'Komanda üzvü' if not last_feedback else f'{days_since_feedback} gündür rəy verməmisiniz'
        })

    # 2. Supervisor suggestion
    if supervisor:
        last_feedback = QuickFeedback.objects.filter(
            sender=user,
            recipient=supervisor
        ).aggregate(Max('created_at'))['created_at__max']

        days_since_feedback = (timezone.now() - last_feedback).days if last_feedback else 999

        # Priority logic for supervisor
        if last_feedback:
            if days_since_feedback > 30:
                priority = 'high'
            elif days_since_feedback > 14:
                priority = 'medium'
            else:
                priority = 'low'
        else:
            priority = 'high'

        suggestions.append({
            'user': supervisor,
            'relationship': 'Rəhbər',
            'days_since_feedback': days_since_feedback,
            'last_feedback_date': last_feedback,
            'priority': priority,
            'reason': 'Rəhbərinizə rəy vermək vacibdir'
        })

    # 3. Subordinates suggestions (if manager)
    if subordinates:
        for subordinate in subordinates[:5]:  # Limit to 5
            last_feedback = QuickFeedback.objects.filter(
                sender=user,
                recipient=subordinate
            ).aggregate(Max('created_at'))['created_at__max']

            days_since_feedback = (timezone.now() - last_feedback).days if last_feedback else 999

            suggestions.append({
                'user': subordinate,
                'relationship': 'Tabelik',
                'days_since_feedback': days_since_feedback,
                'last_feedback_date': last_feedback,
                'priority': 'high' if days_since_feedback > 14 or not last_feedback else 'low',
                'reason': 'Komanda üzvünə dəstək'
            })

    # Sort by priority (high first) and days since feedback
    priority_order = {'high': 0, 'medium': 1, 'low': 2}
    suggestions.sort(key=lambda x: (priority_order.get(x['priority'], 3), -x['days_since_feedback']))

    # Limit to top 15 suggestions
    suggestions = suggestions[:15]

    # Statistics
    feedback_stats = {
        'total_sent': QuickFeedback.objects.filter(sender=user).count(),
        'this_month': QuickFeedback.objects.filter(
            sender=user,
            created_at__gte=timezone.now() - timedelta(days=30)
        ).count(),
        'recognitions_sent': QuickFeedback.objects.filter(
            sender=user,
            feedback_type='recognition'
        ).count(),
        'last_feedback_date': QuickFeedback.objects.filter(
            sender=user
        ).aggregate(Max('created_at'))['created_at__max'],
    }

    # Calculate engagement score (0-100)
    engagement_score = min(100, (feedback_stats['this_month'] * 10))

    # Milestones
    milestones = [
        {'count': 10, 'title': 'İlk 10 Rəy', 'icon': 'fa-star', 'achieved': feedback_stats['total_sent'] >= 10},
        {'count': 25, 'title': 'Rəy Ustası', 'icon': 'fa-trophy', 'achieved': feedback_stats['total_sent'] >= 25},
        {'count': 50, 'title': 'Rəy Çempionu', 'icon': 'fa-medal', 'achieved': feedback_stats['total_sent'] >= 50},
        {'count': 100, 'title': 'Rəy Əfsanəsi', 'icon': 'fa-crown', 'achieved': feedback_stats['total_sent'] >= 100},
    ]

    context = {
        'suggestions': suggestions,
        'feedback_stats': feedback_stats,
        'engagement_score': engagement_score,
        'milestones': milestones,
        'high_priority_count': len([s for s in suggestions if s['priority'] == 'high']),
        'medium_priority_count': len([s for s in suggestions if s['priority'] == 'medium']),
    }

    return render(request, 'continuous_feedback/proactive_suggestions.html', context)


@login_required
def feedback_360_request(request):
    """
    360-Degree Feedback Request view.
    Allows requesting feedback from multiple sources (self, manager, peers, etc.)
    """
    from apps.evaluations.models import EvaluationCycle

    # Get active evaluation cycles
    active_cycles = EvaluationCycle.objects.filter(
        is_active=True,
        start_date__lte=timezone.now(),
        end_date__gte=timezone.now()
    ).order_by('-start_date')

    # Get potential reviewers by relationship type
    user = request.user

    # Manager
    manager = user.supervisor if hasattr(user, 'supervisor') else None

    # Peers (same department, excluding self and manager)
    exclude_ids = [user.id]
    if manager:
        exclude_ids.append(manager.id)

    peers = User.objects.filter(
        is_active=True,
        department=user.department
    ).exclude(id__in=exclude_ids) if user.department else []

    # Direct reports
    direct_reports = user.get_subordinates() if hasattr(user, 'get_subordinates') and user.is_manager() else []

    # Cross-functional (other departments)
    cross_functional = User.objects.filter(
        is_active=True
    ).exclude(
        Q(department=user.department) | Q(id=user.id)
    ) if user.department else []

    # All users for customer/external selection
    all_users = User.objects.filter(is_active=True).exclude(id=user.id).order_by('first_name', 'last_name')

    context = {
        'active_cycles': active_cycles,
        'manager': manager,
        'peers': peers[:20],  # Limit for performance
        'direct_reports': direct_reports,
        'cross_functional': cross_functional[:20],
        'all_users': all_users,
    }

    return render(request, 'continuous_feedback/360_feedback_request.html', context)


@login_required
def feedback_analytics(request):
    """
    Feedback Analytics Dashboard view.
    Real-time analytics and insights on received feedback.
    """
    from django.db.models import Count, Avg
    from datetime import timedelta
    import json

    user = request.user

    # Get all feedback received by user
    all_feedback = QuickFeedback.objects.filter(recipient=user)

    # Calculate KPIs
    total_feedback = all_feedback.count()

    # Last 30 days
    last_30_days = timezone.now() - timedelta(days=30)
    recent_feedback = all_feedback.filter(created_at__gte=last_30_days)
    recent_count = recent_feedback.count()

    # Recognition vs improvement ratio
    recognitions = all_feedback.filter(feedback_type='recognition').count()
    improvements = all_feedback.filter(feedback_type='improvement').count()

    # Trend data (last 6 months)
    months = []
    trend_data = []
    for i in range(5, -1, -1):
        month_start = timezone.now() - timedelta(days=30*i)
        month_end = timezone.now() - timedelta(days=30*(i-1)) if i > 0 else timezone.now()
        count = all_feedback.filter(created_at__gte=month_start, created_at__lt=month_end).count()
        months.append(month_start.strftime('%b'))
        trend_data.append(count)

    # Source distribution
    source_labels = []
    source_data = []

    # Group by sender's relationship to user
    feedback_by_source = all_feedback.values('sender__id').annotate(count=Count('id'))

    # Categorize sources
    from_manager = 0
    from_peers = 0
    from_reports = 0
    from_others = 0

    for fb in feedback_by_source:
        sender_id = fb['sender__id']
        count = fb['count']

        if sender_id == (user.supervisor.id if hasattr(user, 'supervisor') and user.supervisor else None):
            from_manager += count
        elif sender_id in [r.id for r in (user.get_subordinates() if hasattr(user, 'get_subordinates') and user.is_manager() else [])]:
            from_reports += count
        elif User.objects.get(id=sender_id).department == user.department:
            from_peers += count
        else:
            from_others += count

    source_labels = ['Rəhbər', 'Həmkarlar', 'Tabelilər', 'Digər']
    source_data = [from_manager, from_peers, from_reports, from_others]

    # Top competencies (if feedback has tags/competencies)
    # For now, use feedback types
    competency_labels = ['Liderlik', 'Kommunikasiya', 'Texniki', 'Təşkilatçılıq', 'Yaradıcılıq']
    competency_data = [
        all_feedback.filter(message__icontains='lider').count(),
        all_feedback.filter(message__icontains='kommunikasiya').count(),
        all_feedback.filter(message__icontains='texniki').count(),
        all_feedback.filter(message__icontains='təşkilat').count(),
        all_feedback.filter(message__icontains='yaradıcı').count(),
    ]

    # Insights
    insights = []

    if recent_count > 0:
        insights.append({
            'type': 'positive',
            'message': f'Son 30 gündə {recent_count} rəy aldınız'
        })

    if recognitions > improvements:
        insights.append({
            'type': 'success',
            'message': 'Qəbul etdiyiniz rəylərin əksəriyyəti təqdirlərdir'
        })
    else:
        insights.append({
            'type': 'info',
            'message': 'İnkişaf sahələrində faydalı rəylər alırsınız'
        })

    if from_manager > 0:
        insights.append({
            'type': 'info',
            'message': f'Rəhbərinizdən {from_manager} rəy aldınız'
        })

    context = {
        'analytics': {
            'total_feedback': total_feedback,
            'recent_count': recent_count,
            'recognitions': recognitions,
            'improvements': improvements,
            'trend_labels': json.dumps(months),
            'trend_data': json.dumps(trend_data),
            'source_labels': json.dumps(source_labels),
            'source_data': json.dumps(source_data),
            'competency_labels': json.dumps(competency_labels),
            'competency_data': json.dumps(competency_data),
        },
        'insights': insights,
    }

    return render(request, 'continuous_feedback/feedback_analytics.html', context)
