"""Views for OKR/Goal Management module."""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q, Avg
from .models_okr import StrategicObjective, KeyResult, KPI, KPIMeasurement


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
        StrategicObjective.objects.prefetch_related('key_results', 'child_objectives'),
        pk=pk
    )

    context = {'objective': objective}
    return render(request, 'development_plans/okr/objective_detail.html', context)


@login_required
@require_http_methods(["POST"])
def objective_create(request):
    """Create new objective."""
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
