"""
Calibration views for 360-degree evaluation results.
Allows managers and HR to adjust evaluation scores for fairness and consistency.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Avg, Count, Q
from decimal import Decimal

from .models import EvaluationCampaign, EvaluationResult
from apps.accounts.models import User


@login_required
def calibration_dashboard(request, campaign_id):
    """
    Calibration dashboard for managers/HR to review and adjust scores.
    """
    if not (request.user.is_admin or request.user.is_manager()):
        messages.error(request, 'Bu səhifəyə giriş icazəniz yoxdur.')
        return redirect('dashboard')

    campaign = get_object_or_404(EvaluationCampaign, id=campaign_id)

    # Get all results for this campaign
    results = EvaluationResult.objects.filter(
        campaign=campaign
    ).select_related('evaluatee', 'evaluatee__department').order_by('-overall_score')

    # Calculate statistics
    stats = {
        'total_evaluations': results.count(),
        'avg_score': results.aggregate(Avg('overall_score'))['overall_score__avg'],
        'finalized_count': results.filter(is_finalized=True).count(),
        'pending_count': results.filter(is_finalized=False).count(),
    }

    # Score distribution
    score_distribution = {
        'excellent': results.filter(overall_score__gte=4.5).count(),
        'good': results.filter(overall_score__gte=3.5, overall_score__lt=4.5).count(),
        'average': results.filter(overall_score__gte=2.5, overall_score__lt=3.5).count(),
        'needs_improvement': results.filter(overall_score__lt=2.5).count(),
    }

    # Department breakdown (if admin)
    dept_stats = []
    if request.user.is_admin:
        from apps.departments.models import Department
        departments = Department.objects.filter(is_active=True)

        for dept in departments:
            dept_results = results.filter(evaluatee__department=dept)
            if dept_results.exists():
                dept_stats.append({
                    'name': dept.name,
                    'count': dept_results.count(),
                    'avg_score': dept_results.aggregate(Avg('overall_score'))['overall_score__avg'],
                    'finalized': dept_results.filter(is_finalized=True).count(),
                })

    context = {
        'campaign': campaign,
        'results': results,
        'stats': stats,
        'score_distribution': score_distribution,
        'dept_stats': dept_stats,
    }

    return render(request, 'evaluations/calibration/dashboard.html', context)


@login_required
def calibration_detail(request, result_id):
    """
    Detailed view for calibrating a specific evaluation result.
    """
    if not (request.user.is_admin or request.user.is_manager()):
        messages.error(request, 'Bu səhifəyə giriş icazəniz yoxdur.')
        return redirect('dashboard')

    result = get_object_or_404(
        EvaluationResult.objects.select_related('campaign', 'evaluatee', 'evaluatee__department'),
        id=result_id
    )

    # Get all assignments for this result
    from .models import EvaluationAssignment, Response, QuestionCategory
    assignments = EvaluationAssignment.objects.filter(
        campaign=result.campaign,
        evaluatee=result.evaluatee,
        status='completed'
    ).select_related('evaluator')

    # Category breakdown
    categories = QuestionCategory.objects.filter(is_active=True)
    category_scores = []

    for category in categories:
        responses = Response.objects.filter(
            assignment__in=assignments,
            question__category=category,
            score__isnull=False
        )

        if responses.exists():
            avg_score = responses.aggregate(Avg('score'))['score__avg']
            category_scores.append({
                'name': category.name,
                'avg_score': round(avg_score, 2) if avg_score else 0,
                'response_count': responses.count(),
            })

    # Relationship breakdown
    relationship_breakdown = []
    for rel_type, rel_display in [
        ('self', 'Özünüdəyərləndirmə'),
        ('supervisor', 'Rəhbər'),
        ('peer', 'Həmkar'),
        ('subordinate', 'Tabelik')
    ]:
        rel_assignments = assignments.filter(relationship=rel_type)
        if rel_assignments.exists():
            rel_responses = Response.objects.filter(
                assignment__in=rel_assignments,
                score__isnull=False
            )
            if rel_responses.exists():
                relationship_breakdown.append({
                    'type': rel_type,
                    'display': rel_display,
                    'count': rel_assignments.count(),
                    'avg_score': rel_responses.aggregate(Avg('score'))['score__avg'],
                })

    context = {
        'result': result,
        'assignments': assignments,
        'category_scores': category_scores,
        'relationship_breakdown': relationship_breakdown,
    }

    return render(request, 'evaluations/calibration/detail.html', context)


@login_required
@require_http_methods(["POST"])
def adjust_score(request, result_id):
    """
    Adjust evaluation score (calibration).
    """
    if not (request.user.is_admin or request.user.is_manager()):
        return JsonResponse({'success': False, 'message': 'İcazəniz yoxdur'}, status=403)

    result = get_object_or_404(EvaluationResult, id=result_id)

    try:
        # Get adjusted scores
        new_overall = request.POST.get('overall_score')
        adjustment_reason = request.POST.get('reason', '')

        if new_overall:
            # Save old score for history
            old_score = result.overall_score

            # Update score
            result.overall_score = Decimal(new_overall)
            result.save()

            # Log calibration (you might want to create a CalibrationLog model)
            # For now, we'll just return success
            return JsonResponse({
                'success': True,
                'message': f'Bal {old_score} -> {new_overall} olaraq dəyişdirildi',
                'old_score': float(old_score) if old_score else 0,
                'new_score': float(new_overall),
            })
        else:
            return JsonResponse({'success': False, 'message': 'Yeni bal daxil edilməlidir'})

    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@login_required
@require_http_methods(["POST"])
def finalize_result(request, result_id):
    """
    Finalize evaluation result (lock it from further changes).
    """
    if not (request.user.is_admin or request.user.is_manager()):
        return JsonResponse({'success': False, 'message': 'İcazəniz yoxdur'}, status=403)

    result = get_object_or_404(EvaluationResult, id=result_id)

    try:
        from django.utils import timezone

        result.is_finalized = True
        result.finalized_at = timezone.now()
        result.save()

        return JsonResponse({
            'success': True,
            'message': 'Qiymətləndirmə yekunlaşdırıldı'
        })

    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@login_required
@require_http_methods(["POST"])
def bulk_finalize(request, campaign_id):
    """
    Finalize all results in a campaign.
    """
    if not request.user.is_admin:
        return JsonResponse({'success': False, 'message': 'Yalnız admin icazə verilir'}, status=403)

    campaign = get_object_or_404(EvaluationCampaign, id=campaign_id)

    try:
        from django.utils import timezone

        # Finalize all non-finalized results
        results = EvaluationResult.objects.filter(
            campaign=campaign,
            is_finalized=False
        )

        count = results.update(
            is_finalized=True,
            finalized_at=timezone.now()
        )

        return JsonResponse({
            'success': True,
            'message': f'{count} qiymətləndirmə yekunlaşdırıldı'
        })

    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
