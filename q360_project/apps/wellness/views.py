"""
Views for Wellness & Well-Being module.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.db.models import Avg, Count, Sum, Q
from django.utils import timezone
from datetime import datetime, timedelta
from .models import (
    HealthCheckup,
    MentalHealthSurvey,
    FitnessProgram,
    MedicalClaim,
    WellnessChallenge,
    WellnessChallengeParticipation,
    HealthScore,
    StepTracking
)
from .forms import (
    HealthCheckupForm,
    MentalHealthSurveyForm,
    MedicalClaimForm,
    FitnessProgramEnrollForm
)


@login_required
def health_dashboard(request):
    """
    Sağlamlıq və wellness ana dashboard-u.
    Main health and wellness dashboard.
    """
    user = request.user

    # İstifadəçinin son sağlamlıq skoru
    latest_health_score = HealthScore.objects.filter(employee=user).order_by('-score_date').first()

    # Gələcək tibbi müayinələr
    upcoming_checkups = HealthCheckup.objects.filter(
        employee=user,
        status='scheduled',
        scheduled_date__gte=timezone.now()
    ).order_by('scheduled_date')[:5]

    # Son 7 günün addım məlumatları
    seven_days_ago = timezone.now().date() - timedelta(days=7)
    recent_steps = StepTracking.objects.filter(
        employee=user,
        tracking_date__gte=seven_days_ago
    ).order_by('-tracking_date')

    # Ortalama günlük addımlar
    avg_daily_steps = recent_steps.aggregate(Avg('steps'))['steps__avg'] or 0

    # Aktiv fitness proqramları
    active_fitness_programs = FitnessProgram.objects.filter(
        participants=user,
        status='active'
    )

    # Aktiv wellness yarışları
    active_challenges = WellnessChallenge.objects.filter(
        participants=user,
        status='active'
    )

    # Gözləyən medical claims
    pending_claims = MedicalClaim.objects.filter(
        employee=user,
        status='pending'
    ).count()

    # Son mental health survey
    latest_survey = MentalHealthSurvey.objects.filter(
        employee=user
    ).order_by('-survey_date').first()

    context = {
        'title': _('Sağlamlıq Dashboard'),
        'latest_health_score': latest_health_score,
        'upcoming_checkups': upcoming_checkups,
        'recent_steps': recent_steps,
        'avg_daily_steps': int(avg_daily_steps),
        'active_fitness_programs': active_fitness_programs,
        'active_challenges': active_challenges,
        'pending_claims': pending_claims,
        'latest_survey': latest_survey,
    }

    return render(request, 'wellness/dashboard.html', context)


@login_required
def checkup_list(request):
    """
    Tibbi müayinələrin siyahısı.
    List of medical checkups.
    """
    checkups = HealthCheckup.objects.filter(employee=request.user).order_by('-scheduled_date')

    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        checkups = checkups.filter(status=status_filter)

    context = {
        'title': _('Tibbi Müayinələr'),
        'checkups': checkups,
        'status_filter': status_filter,
    }

    return render(request, 'wellness/checkups.html', context)


@login_required
def checkup_detail(request, pk):
    """
    Tibbi müayinə detalları.
    Medical checkup details.
    """
    checkup = get_object_or_404(HealthCheckup, pk=pk, employee=request.user)

    context = {
        'title': _('Müayinə Detalları'),
        'checkup': checkup,
    }

    return render(request, 'wellness/checkup_detail.html', context)


@login_required
def checkup_create(request):
    """
    Yeni tibbi müayinə planlaşdır.
    Schedule new medical checkup.
    """
    if request.method == 'POST':
        form = HealthCheckupForm(request.POST)
        if form.is_valid():
            checkup = form.save(commit=False)
            checkup.employee = request.user
            checkup.save()
            messages.success(request, _('Tibbi müayinə uğurla planlaşdırıldı.'))
            return redirect('wellness:checkup_list')
    else:
        form = HealthCheckupForm()

    context = {
        'title': _('Yeni Müayinə'),
        'form': form,
    }

    return render(request, 'wellness/checkup_form.html', context)


@login_required
def mental_health_survey(request):
    """
    Mental sağlamlıq survey-i.
    Mental health survey.
    """
    if request.method == 'POST':
        form = MentalHealthSurveyForm(request.POST)
        if form.is_valid():
            survey = form.save(commit=False)
            survey.employee = request.user
            survey.save()

            # Əgər yüksək stress səviyyəsi varsa, follow-up təyin et
            if survey.stress_level >= 4 or survey.anxiety_level >= 4:
                survey.follow_up_required = True
                survey.follow_up_date = timezone.now().date() + timedelta(days=7)
                survey.save()

            messages.success(request, _('Survey uğurla tamamlandı. Təşəkkürlər!'))
            return redirect('wellness:dashboard')
    else:
        form = MentalHealthSurveyForm()

    context = {
        'title': _('Mental Sağlamlıq Survey'),
        'form': form,
    }

    return render(request, 'wellness/mental_health_survey.html', context)


@login_required
def mental_health_history(request):
    """
    Mental sağlamlıq survey tarixçəsi.
    Mental health survey history.
    """
    surveys = MentalHealthSurvey.objects.filter(
        employee=request.user
    ).order_by('-survey_date')

    context = {
        'title': _('Survey Tarixçəsi'),
        'surveys': surveys,
    }

    return render(request, 'wellness/mental_health_history.html', context)


@login_required
def fitness_programs(request):
    """
    Fitness proqramları siyahısı.
    List of fitness programs.
    """
    # Bütün aktiv və gələcək proqramlar
    available_programs = FitnessProgram.objects.filter(
        Q(status='active') | Q(status='upcoming')
    ).order_by('-start_date')

    # İstifadəçinin qoşulduğu proqramlar
    my_programs = FitnessProgram.objects.filter(
        participants=request.user
    ).order_by('-start_date')

    context = {
        'title': _('Fitness Proqramları'),
        'available_programs': available_programs,
        'my_programs': my_programs,
    }

    return render(request, 'wellness/fitness_programs.html', context)


@login_required
def fitness_program_detail(request, pk):
    """
    Fitness proqramı detalları.
    Fitness program details.
    """
    program = get_object_or_404(FitnessProgram, pk=pk)
    is_enrolled = program.participants.filter(id=request.user.id).exists()

    if request.method == 'POST' and not is_enrolled:
        if not program.is_full():
            program.participants.add(request.user)
            messages.success(request, _('Proqrama uğurla qoşuldunuz!'))
            return redirect('wellness:fitness_program_detail', pk=pk)
        else:
            messages.error(request, _('Proqram doludur.'))

    context = {
        'title': program.title,
        'program': program,
        'is_enrolled': is_enrolled,
    }

    return render(request, 'wellness/fitness_program_detail.html', context)


@login_required
def medical_claims(request):
    """
    Tibbi xərc tələbləri siyahısı.
    List of medical claims.
    """
    claims = MedicalClaim.objects.filter(employee=request.user).order_by('-claim_date')

    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        claims = claims.filter(status=status_filter)

    # Statistika
    total_claimed = claims.aggregate(Sum('amount_claimed'))['amount_claimed__sum'] or 0
    total_approved = claims.filter(status__in=['approved', 'paid']).aggregate(
        Sum('amount_approved')
    )['amount_approved__sum'] or 0
    pending_count = claims.filter(status='pending').count()

    context = {
        'title': _('Tibbi Xərc Tələbləri'),
        'claims': claims,
        'status_filter': status_filter,
        'total_claimed': total_claimed,
        'total_approved': total_approved,
        'pending_count': pending_count,
    }

    return render(request, 'wellness/medical_claims.html', context)


@login_required
def medical_claim_create(request):
    """
    Yeni tibbi xərc tələbi yarat.
    Create new medical claim.
    """
    if request.method == 'POST':
        form = MedicalClaimForm(request.POST, request.FILES)
        if form.is_valid():
            claim = form.save(commit=False)
            claim.employee = request.user
            claim.save()
            messages.success(request, _('Tələb uğurla göndərildi.'))
            return redirect('wellness:medical_claims')
    else:
        form = MedicalClaimForm()

    context = {
        'title': _('Yeni Tələb'),
        'form': form,
    }

    return render(request, 'wellness/medical_claim_form.html', context)


@login_required
def medical_claim_detail(request, pk):
    """
    Tibbi xərc tələbi detalları.
    Medical claim details.
    """
    claim = get_object_or_404(MedicalClaim, pk=pk, employee=request.user)

    context = {
        'title': _('Tələb Detalları'),
        'claim': claim,
    }

    return render(request, 'wellness/medical_claim_detail.html', context)


@login_required
def wellness_challenges(request):
    """
    Wellness yarışları siyahısı.
    List of wellness challenges.
    """
    # Aktiv yarışlar
    active_challenges = WellnessChallenge.objects.filter(status='active')

    # İstifadəçinin iştirak etdiyi yarışlar
    my_challenges = WellnessChallenge.objects.filter(
        participants=request.user
    ).order_by('-start_date')

    # İstifadəçinin iştirak məlumatları
    my_participations = WellnessChallengeParticipation.objects.filter(
        participant=request.user
    ).select_related('challenge')

    context = {
        'title': _('Wellness Yarışları'),
        'active_challenges': active_challenges,
        'my_challenges': my_challenges,
        'my_participations': my_participations,
    }

    return render(request, 'wellness/challenges.html', context)


@login_required
def wellness_challenge_detail(request, pk):
    """
    Wellness yarışı detalları və iştirak.
    Wellness challenge details and participation.
    """
    challenge = get_object_or_404(WellnessChallenge, pk=pk)

    # İstifadəçinin iştirak statusu
    participation = WellnessChallengeParticipation.objects.filter(
        challenge=challenge,
        participant=request.user
    ).first()

    # Leaderboard - ən yüksək progress
    leaderboard = challenge.participations.order_by('-progress', '-current_value')[:10]

    # Yarışa qoşul
    if request.method == 'POST' and not participation:
        WellnessChallengeParticipation.objects.create(
            challenge=challenge,
            participant=request.user
        )
        messages.success(request, _('Yarışa uğurla qoşuldunuz!'))
        return redirect('wellness:challenge_detail', pk=pk)

    context = {
        'title': challenge.title,
        'challenge': challenge,
        'participation': participation,
        'leaderboard': leaderboard,
    }

    return render(request, 'wellness/challenge_detail.html', context)


@login_required
def step_tracking(request):
    """
    Addım izləmə səhifəsi.
    Step tracking page.
    """
    # Son 30 günün məlumatları
    thirty_days_ago = timezone.now().date() - timedelta(days=30)
    step_data = StepTracking.objects.filter(
        employee=request.user,
        tracking_date__gte=thirty_days_ago
    ).order_by('-tracking_date')

    # Statistika
    total_steps = step_data.aggregate(Sum('steps'))['steps__sum'] or 0
    avg_steps = step_data.aggregate(Avg('steps'))['steps__avg'] or 0
    total_distance = step_data.aggregate(Sum('distance_km'))['distance_km__sum'] or 0
    total_calories = step_data.aggregate(Sum('calories_burned'))['calories_burned__sum'] or 0

    context = {
        'title': _('Addım İzləmə'),
        'step_data': step_data,
        'total_steps': int(total_steps),
        'avg_steps': int(avg_steps),
        'total_distance': total_distance,
        'total_calories': int(total_calories),
    }

    return render(request, 'wellness/step_tracking.html', context)


@login_required
def health_score_history(request):
    """
    Sağlamlıq skoru tarixçəsi.
    Health score history.
    """
    health_scores = HealthScore.objects.filter(
        employee=request.user
    ).order_by('-score_date')

    context = {
        'title': _('Sağlamlıq Skoru Tarixçəsi'),
        'health_scores': health_scores,
    }

    return render(request, 'wellness/health_score_history.html', context)
