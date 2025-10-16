"""Views for OKR/Goal Management module."""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q, Avg
from django.utils import timezone
from .models_okr import StrategicObjective, KeyResult, KPI, KPIMeasurement, Milestone, ObjectiveUpdate


@login_required
def okr_dashboard(request):
    """OKR dashboard with overview."""
    user = request.user
    current_year = 2025

    # User's objectives
    my_objectives = StrategicObjective.objects.filter(
        owner=user,
        fiscal_year=current_year
    ).prefetch_related('key_results')

    # Department objectives
    dept_objectives = StrategicObjective.objects.filter(
        department=user.department,
        level='department',
        fiscal_year=current_year
    ) if user.department else []

    # Organization objectives
    org_objectives = StrategicObjective.objects.filter(
        level='organization',
        fiscal_year=current_year
    )

    context = {
        'my_objectives': my_objectives,
        'dept_objectives': dept_objectives,
        'org_objectives': org_objectives,
        'current_year': current_year,
    }
    return render(request, 'development_plans/okr/dashboard.html', context)


@login_required
def objective_list(request):
    """List all objectives."""
    level = request.GET.get('level', '')
    status = request.GET.get('status', '')

    objectives = StrategicObjective.objects.all().select_related('owner', 'department')

    if level:
        objectives = objectives.filter(level=level)
    if status:
        objectives = objectives.filter(status=status)

    objectives = objectives.order_by('-fiscal_year', '-created_at')

    context = {'objectives': objectives, 'level': level, 'status': status}
    return render(request, 'development_plans/okr/objective_list.html', context)


@login_required
def objective_detail(request, pk):
    """Objective detail with key results."""
    objective = get_object_or_404(
        StrategicObjective.objects.prefetch_related(
            'key_results',
            'child_objectives',
            'milestones',
            'progress_updates'
        ),
        pk=pk
    )

    # Get milestones and updates
    milestones = objective.milestones.all().order_by('due_date')
    updates = objective.progress_updates.all().order_by('-created_at')

    context = {
        'objective': objective,
        'milestones': milestones,
        'updates': updates,
    }
    return render(request, 'development_plans/okr/objective_detail.html', context)


@login_required
def objective_create(request):
    """Create new objective."""
    if request.method == 'POST':
        try:
            objective = StrategicObjective.objects.create(
                title=request.POST.get('title'),
                description=request.POST.get('description'),
                level=request.POST.get('level'),
                fiscal_year=request.POST.get('fiscal_year'),
                quarter=request.POST.get('quarter', 'annual'),
                start_date=request.POST.get('start_date'),
                end_date=request.POST.get('end_date'),
                owner=request.user,
                created_by=request.user
            )
            return JsonResponse({'success': True, 'objective_id': objective.id})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    # GET request - show form
    context = {
        'current_year': 2025,
    }
    return render(request, 'development_plans/okr/objective_create.html', context)


@login_required
def objective_edit(request, pk):
    """Edit objective."""
    objective = get_object_or_404(StrategicObjective, pk=pk)

    if request.method == 'POST':
        try:
            objective.title = request.POST.get('title')
            objective.description = request.POST.get('description')
            objective.level = request.POST.get('level')
            objective.status = request.POST.get('status')
            objective.fiscal_year = request.POST.get('fiscal_year')
            objective.quarter = request.POST.get('quarter', 'annual')
            objective.start_date = request.POST.get('start_date')
            objective.end_date = request.POST.get('end_date')
            objective.save()
            return redirect('okr:objective_detail', pk=objective.id)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    context = {
        'objective': objective,
        'current_year': 2025,
    }
    return render(request, 'development_plans/okr/objective_edit.html', context)


@login_required
@require_http_methods(["POST"])
def keyresult_create(request, objective_id):
    """Create new key result."""
    objective = get_object_or_404(StrategicObjective, pk=objective_id)

    try:
        kr = KeyResult.objects.create(
            objective=objective,
            title=request.POST.get('title'),
            description=request.POST.get('description', ''),
            unit=request.POST.get('unit'),
            baseline_value=request.POST.get('baseline_value', 0),
            target_value=request.POST.get('target_value'),
            current_value=request.POST.get('current_value', 0),
            weight=request.POST.get('weight', 100)
        )
        return JsonResponse({'success': True, 'message': 'Açar nəticə əlavə edildi'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@login_required
@require_http_methods(["POST"])
def keyresult_complete(request, objective_id, kr_id):
    """Mark key result as complete."""
    keyresult = get_object_or_404(KeyResult, pk=kr_id, objective_id=objective_id)

    try:
        # Set current value to target value
        keyresult.current_value = keyresult.target_value
        keyresult.save()
        return JsonResponse({'success': True, 'message': 'Açar nəticə tamamlandı'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@login_required
def keyresult_edit(request, kr_id):
    """Edit key result."""
    keyresult = get_object_or_404(KeyResult, pk=kr_id)

    if request.method == 'POST':
        try:
            keyresult.title = request.POST.get('title')
            keyresult.description = request.POST.get('description', '')
            keyresult.unit = request.POST.get('unit')
            keyresult.baseline_value = request.POST.get('baseline_value', 0)
            keyresult.target_value = request.POST.get('target_value')
            keyresult.current_value = request.POST.get('current_value', keyresult.current_value)
            keyresult.weight = request.POST.get('weight', 100)
            keyresult.save()
            return JsonResponse({'success': True, 'message': 'Açar nəticə yeniləndi'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    context = {'keyresult': keyresult}
    return render(request, 'development_plans/okr/keyresult_edit.html', context)


@login_required
@require_http_methods(["POST"])
def keyresult_update_value(request, kr_id):
    """Update key result current value."""
    import json
    keyresult = get_object_or_404(KeyResult, pk=kr_id)

    try:
        data = json.loads(request.body)
        current_value = data.get('current_value')
        keyresult.current_value = current_value
        keyresult.save()
        return JsonResponse({
            'success': True,
            'message': 'Dəyər yeniləndi',
            'progress_percentage': keyresult.progress_percentage
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@login_required
def kpi_dashboard(request):
    """KPI dashboard."""
    user_kpis = KPI.objects.filter(owner=request.user, is_active=True)

    context = {'user_kpis': user_kpis}
    return render(request, 'development_plans/okr/kpi_dashboard.html', context)


@login_required
@require_http_methods(["POST"])
def kpi_measurement_create(request, kpi_id):
    """Create KPI measurement."""
    kpi = get_object_or_404(KPI, pk=kpi_id)

    try:
        measurement = KPIMeasurement.objects.create(
            kpi=kpi,
            measurement_date=request.POST.get('measurement_date'),
            actual_value=request.POST.get('actual_value'),
            trend=request.POST.get('trend', ''),
            notes=request.POST.get('notes', ''),
            measured_by=request.user
        )
        return JsonResponse({'success': True, 'message': 'Ölçmə əlavə edildi'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@login_required
@require_http_methods(["POST"])
def milestone_create(request, objective_id):
    """Create milestone for objective."""
    objective = get_object_or_404(StrategicObjective, pk=objective_id)

    try:
        milestone = Milestone.objects.create(
            objective=objective,
            title=request.POST.get('title'),
            description=request.POST.get('description', ''),
            due_date=request.POST.get('due_date'),
            created_by=request.user
        )
        return JsonResponse({
            'success': True,
            'message': 'Mərhələ əlavə edildi',
            'milestone': {
                'id': milestone.id,
                'title': milestone.title,
                'due_date': milestone.due_date.strftime('%Y-%m-%d'),
                'is_completed': milestone.is_completed
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@login_required
@require_http_methods(["POST"])
def milestone_complete(request, objective_id, milestone_id):
    """Mark milestone as complete."""
    milestone = get_object_or_404(Milestone, pk=milestone_id, objective_id=objective_id)

    try:
        milestone.is_completed = True
        milestone.completed_at = timezone.now()
        milestone.save()
        return JsonResponse({'success': True, 'message': 'Mərhələ tamamlandı'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@login_required
@require_http_methods(["POST"])
def objective_update_create(request, objective_id):
    """Create progress update for objective."""
    objective = get_object_or_404(StrategicObjective, pk=objective_id)

    try:
        update = ObjectiveUpdate.objects.create(
            objective=objective,
            content=request.POST.get('content'),
            progress_value=request.POST.get('progress_value', None),
            created_by=request.user
        )
        return JsonResponse({
            'success': True,
            'message': 'Yenilənmə əlavə edildi',
            'update': {
                'id': update.id,
                'content': update.content,
                'progress_value': str(update.progress_value) if update.progress_value else None,
                'created_at': update.created_at.strftime('%Y-%m-%d %H:%M')
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
