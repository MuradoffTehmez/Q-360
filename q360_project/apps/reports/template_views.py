"""
Template views for reports app.
Professional report generation and visualization.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.db.models import Avg, Count, Q
from django.utils import timezone
import json

from apps.evaluations.models import EvaluationResult, EvaluationCampaign, Response, EvaluationAssignment
from apps.accounts.models import User
from .models import Report, RadarChartData
from .utils import generate_pdf_report, generate_excel_report, calculate_radar_data


@login_required
def my_reports(request):
    """View current user's evaluation reports."""
    user = request.user

    # Get user's results
    results = EvaluationResult.objects.filter(
        evaluatee=user
    ).select_related('campaign').order_by('-calculated_at')

    # Latest result
    latest_result = results.first()

    # Performance trend data
    trend_data = {
        'labels': [],
        'data': []
    }

    for result in results[:6]:  # Last 6 evaluations
        trend_data['labels'].insert(0, result.campaign.title[:20])
        trend_data['data'].insert(0, float(result.overall_score) if result.overall_score else 0)

    # Radar chart data for latest result
    radar_data = None
    if latest_result:
        radar_data = calculate_radar_data(latest_result)

    context = {
        'results': results,
        'latest_result': latest_result,
        'trend_data': json.dumps(trend_data),
        'radar_data': json.dumps(radar_data) if radar_data else None,
    }

    return render(request, 'reports/my_reports.html', context)


@login_required
def team_reports(request):
    """View team evaluation reports (for managers)."""
    if not request.user.is_manager():
        messages.error(request, 'Bu səhifəyə giriş icazəniz yoxdur.')
        return redirect('dashboard')

    user = request.user

    # Get subordinates
    if user.is_admin():
        # Admin sees all
        team_members = User.objects.filter(is_active=True)
    else:
        # Manager sees subordinates
        team_members = user.get_subordinates()

    # Get campaign from query parameter or latest
    campaign_id = request.GET.get('campaign')
    if campaign_id:
        latest_campaign = EvaluationCampaign.objects.filter(
            pk=campaign_id,
            status__in=['active', 'completed']
        ).first()
    else:
        latest_campaign = EvaluationCampaign.objects.filter(
            status__in=['active', 'completed']
        ).order_by('-created_at').first()

    # Get results for team members
    results = None
    if latest_campaign:
        results = EvaluationResult.objects.filter(
            campaign=latest_campaign,
            evaluatee__in=team_members
        ).select_related('evaluatee').order_by('-overall_score')

    # Calculate team statistics
    team_stats = {
        'total_members': team_members.count() if hasattr(team_members, 'count') else len(team_members),
        'evaluated_members': results.count() if results else 0,
        'avg_score': results.aggregate(Avg('overall_score'))['overall_score__avg'] if results else None,
        'top_performers': list(results[:5]) if results else [],
        'needs_attention': list(results.order_by('overall_score')[:5]) if results else [],
    }

    # Department comparison data
    dept_comparison = []
    if user.is_admin() and results:
        from apps.departments.models import Department
        departments = Department.objects.filter(is_active=True)

        for dept in departments:
            dept_results = results.filter(evaluatee__department=dept)
            if dept_results.exists():
                dept_comparison.append({
                    'name': dept.name,
                    'avg_score': dept_results.aggregate(Avg('overall_score'))['overall_score__avg'],
                    'count': dept_results.count()
                })

    context = {
        'team_members': team_members,
        'results': results,
        'latest_campaign': latest_campaign,
        'team_stats': team_stats,
        'dept_comparison': dept_comparison,
    }

    return render(request, 'reports/team_reports.html', context)


@login_required
def detailed_report(request, result_pk):
    """View detailed individual report."""
    result = get_object_or_404(
        EvaluationResult.objects.select_related('campaign', 'evaluatee'),
        pk=result_pk
    )

    # Check permission
    if not (request.user.is_admin() or
            result.evaluatee == request.user or
            result.evaluatee.supervisor == request.user):
        messages.error(request, 'Bu hesabata baxmaq icazəniz yoxdur.')
        return redirect('dashboard')

    # Get all assignments for this result
    assignments = EvaluationAssignment.objects.filter(
        campaign=result.campaign,
        evaluatee=result.evaluatee,
        status='completed'
    ).select_related('evaluator')

    # Calculate category-wise scores
    from apps.evaluations.models import QuestionCategory
    categories = QuestionCategory.objects.filter(is_active=True)

    category_analysis = []
    for category in categories:
        scores_by_relationship = {
            'self': [],
            'supervisor': [],
            'peer': [],
            'subordinate': []
        }

        for assignment in assignments:
            responses = Response.objects.filter(
                assignment=assignment,
                question__category=category,
                score__isnull=False
            )

            for response in responses:
                scores_by_relationship[assignment.relationship].append(response.score)

        # Calculate averages
        category_data = {
            'name': category.name,
            'scores': {}
        }

        for rel_type, scores in scores_by_relationship.items():
            if scores:
                category_data['scores'][rel_type] = round(sum(scores) / len(scores), 2)
            else:
                category_data['scores'][rel_type] = None

        # Overall average for category
        all_scores = []
        for scores in scores_by_relationship.values():
            all_scores.extend(scores)
        if all_scores:
            category_data['average'] = round(sum(all_scores) / len(all_scores), 2)
        else:
            category_data['average'] = None

        category_analysis.append(category_data)

    # Get text responses (comments)
    text_responses = Response.objects.filter(
        assignment__in=assignments,
        question__question_type='text'
    ).select_related('question').exclude(text_answer='')

    # Strengths and development areas
    strengths = text_responses.filter(
        Q(question__text__icontains='güclü') | Q(question__text__icontains='strength')
    )
    development = text_responses.filter(
        Q(question__text__icontains='inkişaf') | Q(question__text__icontains='development')
    )

    # Radar chart data
    radar_data = calculate_radar_data(result)

    context = {
        'result': result,
        'assignments': assignments,
        'category_analysis': category_analysis,
        'text_responses': text_responses,
        'strengths': strengths,
        'development': development,
        'radar_data': json.dumps(radar_data),
    }

    return render(request, 'reports/detailed_report.html', context)


@login_required
def export_pdf(request, result_pk):
    """Export report as PDF."""
    result = get_object_or_404(EvaluationResult, pk=result_pk)

    # Check permission
    if not (request.user.is_admin() or result.evaluatee == request.user):
        messages.error(request, 'Bu hesabatı ixrac etmək icazəniz yoxdur.')
        return redirect('dashboard')

    # Generate PDF
    pdf_content = generate_pdf_report(result)

    response = HttpResponse(pdf_content, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="qiymetlendirme_{result.evaluatee.username}_{result.campaign.pk}.pdf"'

    return response


@login_required
def export_excel(request, campaign_pk):
    """Export campaign results as Excel."""
    campaign = get_object_or_404(EvaluationCampaign, pk=campaign_pk)

    # Check permission
    if not request.user.is_admin():
        messages.error(request, 'Bu hesabatı ixrac etmək icazəniz yoxdur.')
        return redirect('dashboard')

    # Generate Excel
    excel_content = generate_excel_report(campaign)

    response = HttpResponse(
        excel_content,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="kampaniya_{campaign.pk}_neticeler.xlsx"'

    return response


@login_required
def comparison_report(request):
    """Compare multiple evaluation results."""
    user = request.user

    # Get selected campaigns or results
    campaign_ids = request.GET.getlist('campaigns')

    if not campaign_ids:
        # Show selection form
        campaigns = EvaluationCampaign.objects.filter(
            status__in=['completed', 'active']
        ).order_by('-created_at')[:10]

        context = {
            'campaigns': campaigns
        }
        return render(request, 'reports/comparison_select.html', context)

    # Get results for comparison
    results = EvaluationResult.objects.filter(
        campaign_id__in=campaign_ids,
        evaluatee=user
    ).select_related('campaign').order_by('campaign__start_date')

    # Prepare comparison data
    comparison_data = {
        'labels': [],
        'overall': [],
        'self': [],
        'supervisor': [],
        'peer': [],
        'subordinate': []
    }

    for result in results:
        comparison_data['labels'].append(result.campaign.title[:20])
        comparison_data['overall'].append(float(result.overall_score) if result.overall_score else 0)
        comparison_data['self'].append(float(result.self_score) if result.self_score else 0)
        comparison_data['supervisor'].append(float(result.supervisor_score) if result.supervisor_score else 0)
        comparison_data['peer'].append(float(result.peer_score) if result.peer_score else 0)
        comparison_data['subordinate'].append(float(result.subordinate_score) if result.subordinate_score else 0)

    context = {
        'results': results,
        'comparison_data': json.dumps(comparison_data),
    }

    return render(request, 'reports/comparison_report.html', context)


@login_required
def analytics_dashboard(request):
    """Advanced analytics dashboard (admin only)."""
    if not request.user.is_admin():
        messages.error(request, 'Bu səhifəyə giriş icazəniz yoxdur.')
        return redirect('dashboard')

    # Overall statistics
    total_campaigns = EvaluationCampaign.objects.count()
    active_campaigns = EvaluationCampaign.objects.filter(status='active').count()
    total_evaluations = EvaluationAssignment.objects.filter(status='completed').count()
    total_users = User.objects.filter(is_active=True).count()

    # Latest campaign analysis
    latest_campaign = EvaluationCampaign.objects.filter(
        status__in=['active', 'completed']
    ).order_by('-created_at').first()

    campaign_stats = None
    if latest_campaign:
        results = EvaluationResult.objects.filter(campaign=latest_campaign)
        campaign_stats = {
            'title': latest_campaign.title,
            'total_evaluations': latest_campaign.assignments.count(),
            'completed': latest_campaign.assignments.filter(status='completed').count(),
            'avg_score': results.aggregate(Avg('overall_score'))['overall_score__avg'],
            'participation_rate': latest_campaign.get_completion_rate(),
        }

    # Score distribution
    score_ranges = {
        '0-2': 0,
        '2-3': 0,
        '3-4': 0,
        '4-5': 0,
    }

    if latest_campaign:
        for result in results:
            if result.overall_score:
                score = float(result.overall_score)
                if score < 2:
                    score_ranges['0-2'] += 1
                elif score < 3:
                    score_ranges['2-3'] += 1
                elif score < 4:
                    score_ranges['3-4'] += 1
                else:
                    score_ranges['4-5'] += 1

    context = {
        'total_campaigns': total_campaigns,
        'active_campaigns': active_campaigns,
        'total_evaluations': total_evaluations,
        'total_users': total_users,
        'campaign_stats': campaign_stats,
        'score_distribution': json.dumps(score_ranges),
    }

    return render(request, 'reports/analytics_dashboard.html', context)
