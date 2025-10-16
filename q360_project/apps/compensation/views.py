"""Views for Compensation & Benefits module."""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from .models import SalaryInformation, CompensationHistory, Bonus, Allowance, Deduction
from apps.accounts.models import User


@login_required
def compensation_dashboard(request):
    """Compensation dashboard with overview."""
    user = request.user
    salary_info = SalaryInformation.objects.filter(user=user, is_active=True).first()
    bonuses = Bonus.objects.filter(user=user).order_by('-created_at')[:5]
    allowances = Allowance.objects.filter(user=user, is_active=True)
    deductions = Deduction.objects.filter(user=user, is_active=True)

    context = {
        'salary_info': salary_info,
        'bonuses': bonuses,
        'allowances': allowances,
        'deductions': deductions,
    }
    return render(request, 'compensation/dashboard.html', context)


@login_required
def salary_list(request):
    """List all salary information (for managers)."""
    if not request.user.is_manager():
        return redirect('compensation:dashboard')

    salaries = SalaryInformation.objects.select_related('user').filter(is_active=True)

    search = request.GET.get('search', '')
    if search:
        salaries = salaries.filter(
            Q(user__first_name__icontains=search) |
            Q(user__last_name__icontains=search) |
            Q(user__employee_id__icontains=search)
        )

    context = {'salaries': salaries, 'search': search}
    return render(request, 'compensation/salary_list.html', context)


@login_required
def bonus_list(request):
    """List user bonuses."""
    bonuses = Bonus.objects.filter(user=request.user).order_by('-fiscal_year', '-created_at')
    context = {'bonuses': bonuses}
    return render(request, 'compensation/bonus_list.html', context)


@login_required
@require_http_methods(["POST"])
def bonus_create(request):
    """Create new bonus."""
    try:
        bonus = Bonus.objects.create(
            user=request.user,
            bonus_type=request.POST.get('bonus_type'),
            amount=request.POST.get('amount'),
            currency=request.POST.get('currency', 'AZN'),
            fiscal_year=request.POST.get('fiscal_year'),
            description=request.POST.get('description', ''),
            created_by=request.user
        )
        return JsonResponse({'success': True, 'message': 'Bonus əlavə edildi'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@login_required
def compensation_history(request):
    """View compensation history."""
    history = CompensationHistory.objects.filter(user=request.user).order_by('-effective_date')
    context = {'history': history}
    return render(request, 'compensation/history.html', context)
