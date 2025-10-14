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
