from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Count, Q, F
from django.utils.translation import gettext as _
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta, datetime

from .models import (
    PulseSurvey, SurveyQuestion, SurveyResponse,
    EngagementScore, Recognition, AnonymousFeedback,
    SentimentAnalysis, GamificationBadge, UserBadge,
    UserPoints, PointsTransaction
)
from .forms import PulseSurveyForm, RecognitionForm, AnonymousFeedbackForm


@login_required
def engagement_dashboard(request):
    """
    Əsas engagement dashboard
    """
    user = request.user

    # Get user's engagement scores
    latest_scores = EngagementScore.objects.filter(user=user).order_by('-calculated_at')[:5]

    # Get active surveys for user
    active_surveys = PulseSurvey.objects.filter(
        status='active',
        start_date__lte=timezone.now(),
        end_date__gte=timezone.now()
    ).filter(
        Q(target_users=user) | Q(target_departments=user.department)
    ).distinct()

    # Get recent recognitions
    recent_recognitions = Recognition.objects.filter(
        Q(given_to=user) | Q(given_by=user)
    ).order_by('-created_at')[:10]

    # Get user points and badges
    user_points, created = UserPoints.objects.get_or_create(user=user)
    user_badges = UserBadge.objects.filter(user=user, is_displayed=True).order_by('-earned_at')[:5]

    # Calculate team engagement score
    team_engagement = None
    if user.department:
        team_scores = EngagementScore.objects.filter(
            department=user.department,
            calculated_at__gte=timezone.now() - timedelta(days=30)
        ).aggregate(avg_score=Avg('score_value'))
        team_engagement = team_scores['avg_score']

    # Get sentiment trend
    sentiment_data = SentimentAnalysis.objects.filter(
        analyzed_at__gte=timezone.now() - timedelta(days=30)
    ).values('sentiment').annotate(count=Count('id'))

    context = {
        'latest_scores': latest_scores,
        'active_surveys': active_surveys,
        'recent_recognitions': recent_recognitions,
        'user_points': user_points,
        'user_badges': user_badges,
        'team_engagement': team_engagement,
        'sentiment_data': sentiment_data,
    }

    return render(request, 'engagement/dashboard.html', context)


@login_required
def pulse_surveys(request):
    """
    Pulse Survey siyahısı və cavablandırma səhifəsi
    """
    user = request.user

    # Active surveys
    active_surveys = PulseSurvey.objects.filter(
        status='active',
        start_date__lte=timezone.now(),
        end_date__gte=timezone.now()
    ).filter(
        Q(target_users=user) | Q(target_departments=user.department)
    ).distinct()

    # Surveys user has responded to
    responded_survey_ids = SurveyResponse.objects.filter(user=user).values_list('survey_id', flat=True).distinct()

    # Pending surveys
    pending_surveys = active_surveys.exclude(id__in=responded_survey_ids)

    # Completed surveys
    completed_surveys = active_surveys.filter(id__in=responded_survey_ids)

    context = {
        'pending_surveys': pending_surveys,
        'completed_surveys': completed_surveys,
    }

    return render(request, 'engagement/surveys.html', context)


@login_required
def survey_detail(request, survey_id):
    """
    Survey detayı və cavablandırma
    """
    survey = get_object_or_404(PulseSurvey, id=survey_id)
    user = request.user

    # Check if user has already responded
    has_responded = SurveyResponse.objects.filter(survey=survey, user=user).exists()

    if request.method == 'POST' and not has_responded:
        # Process survey responses
        questions = survey.questions.all()

        for question in questions:
            response_key = f'question_{question.id}'

            if question.question_type == 'rating' or question.question_type == 'nps':
                rating_value = request.POST.get(response_key)
                if rating_value:
                    SurveyResponse.objects.create(
                        survey=survey,
                        question=question,
                        user=user if not survey.is_anonymous else None,
                        rating_value=int(rating_value)
                    )

            elif question.question_type == 'text':
                text_value = request.POST.get(response_key)
                if text_value:
                    SurveyResponse.objects.create(
                        survey=survey,
                        question=question,
                        user=user if not survey.is_anonymous else None,
                        text_value=text_value
                    )

            elif question.question_type == 'yes_no':
                boolean_value = request.POST.get(response_key) == 'yes'
                SurveyResponse.objects.create(
                    survey=survey,
                    question=question,
                    user=user if not survey.is_anonymous else None,
                    boolean_value=boolean_value
                )

        messages.success(request, _('Survey response submitted successfully!'))

        # Award points for completing survey
        user_points, created = UserPoints.objects.get_or_create(user=user)
        user_points.add_points(20, category='collaboration')

        PointsTransaction.objects.create(
            user=user,
            transaction_type='earned',
            points=20,
            reason='Survey Completion',
            description=f'Completed survey: {survey.title}',
            source_type='pulse_survey',
            source_id=survey.id
        )

        return redirect('engagement:pulse_surveys')

    questions = survey.questions.all()

    context = {
        'survey': survey,
        'questions': questions,
        'has_responded': has_responded,
    }

    return render(request, 'engagement/survey_detail.html', context)


@login_required
def recognition_wall(request):
    """
    Təşəkkür lövhəsi - Recognition Wall
    """
    if request.method == 'POST':
        form = RecognitionForm(request.POST, user=request.user)
        if form.is_valid():
            recognition = form.save(commit=False)
            recognition.given_by = request.user
            recognition.save()

            # Award points
            recipient_points, created = UserPoints.objects.get_or_create(user=recognition.given_to)
            recipient_points.add_points(recognition.points, category='collaboration')

            PointsTransaction.objects.create(
                user=recognition.given_to,
                transaction_type='awarded',
                points=recognition.points,
                reason='Recognition Received',
                description=f'From: {request.user.get_full_name()}',
                source_type='recognition',
                source_id=recognition.id,
                created_by=request.user
            )

            messages.success(request, _('Recognition sent successfully!'))
            return redirect('engagement:recognition_wall')
    else:
        form = RecognitionForm(user=request.user)

    # Get all public recognitions
    recognitions = Recognition.objects.filter(is_public=True).select_related('given_by', 'given_to', 'badge').order_by('-created_at')[:50]

    context = {
        'form': form,
        'recognitions': recognitions,
    }

    return render(request, 'engagement/recognition.html', context)


@login_required
def like_recognition(request, recognition_id):
    """
    Recognition-a like at
    """
    if request.method == 'POST':
        recognition = get_object_or_404(Recognition, id=recognition_id)
        user = request.user

        if user in recognition.liked_by.all():
            recognition.liked_by.remove(user)
            recognition.likes_count -= 1
            liked = False
        else:
            recognition.liked_by.add(user)
            recognition.likes_count += 1
            liked = True

        recognition.save()

        return JsonResponse({
            'success': True,
            'liked': liked,
            'likes_count': recognition.likes_count
        })

    return JsonResponse({'success': False}, status=400)


@login_required
def anonymous_feedback(request):
    """
    Anonim feedback formu
    """
    if request.method == 'POST':
        form = AnonymousFeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save()

            # Run sentiment analysis
            from .services import analyze_sentiment
            sentiment_result = analyze_sentiment(feedback.message)

            feedback.sentiment_score = sentiment_result.get('score')
            feedback.sentiment_label = sentiment_result.get('label')
            feedback.save()

            messages.success(request, _('Your feedback has been submitted anonymously. Thank you!'))
            return redirect('engagement:engagement_dashboard')
    else:
        form = AnonymousFeedbackForm()

    context = {
        'form': form,
    }

    return render(request, 'engagement/anonymous_feedback.html', context)


@login_required
def leaderboard(request):
    """
    Gamification lider lövhəsi
    """
    # Get time period from query params
    period = request.GET.get('period', 'all')

    user_points_qs = UserPoints.objects.select_related('user').order_by('-total_points')

    if period == 'month':
        # Get transactions from last month
        start_date = timezone.now() - timedelta(days=30)
        monthly_leaders = PointsTransaction.objects.filter(
            created_at__gte=start_date
        ).values('user').annotate(
            total=Count('points')
        ).order_by('-total')[:20]

        user_ids = [item['user'] for item in monthly_leaders]
        user_points_qs = user_points_qs.filter(user_id__in=user_ids)

    elif period == 'week':
        # Get transactions from last week
        start_date = timezone.now() - timedelta(days=7)
        weekly_leaders = PointsTransaction.objects.filter(
            created_at__gte=start_date
        ).values('user').annotate(
            total=Count('points')
        ).order_by('-total')[:20]

        user_ids = [item['user'] for item in weekly_leaders]
        user_points_qs = user_points_qs.filter(user_id__in=user_ids)

    leaderboard_data = user_points_qs[:20]

    # Get top badges
    top_badges = GamificationBadge.objects.filter(is_active=True).order_by('-points_value')[:10]

    # Get recent badge awards
    recent_awards = UserBadge.objects.select_related('user', 'badge').order_by('-earned_at')[:10]

    context = {
        'leaderboard_data': leaderboard_data,
        'top_badges': top_badges,
        'recent_awards': recent_awards,
        'period': period,
    }

    return render(request, 'engagement/leaderboard.html', context)


@login_required
def my_profile(request):
    """
    İstifadəçinin öz engagement profili
    """
    user = request.user

    user_points, created = UserPoints.objects.get_or_create(user=user)
    user_badges = UserBadge.objects.filter(user=user).select_related('badge').order_by('-earned_at')

    # Get recent transactions
    recent_transactions = PointsTransaction.objects.filter(user=user).order_by('-created_at')[:20]

    # Get recognitions
    received_recognitions = Recognition.objects.filter(given_to=user).order_by('-created_at')[:10]
    given_recognitions = Recognition.objects.filter(given_by=user).order_by('-created_at')[:10]

    context = {
        'user_points': user_points,
        'user_badges': user_badges,
        'recent_transactions': recent_transactions,
        'received_recognitions': received_recognitions,
        'given_recognitions': given_recognitions,
    }

    return render(request, 'engagement/my_profile.html', context)
