"""Views for Compensation & Benefits module."""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q, Sum
from decimal import Decimal
from datetime import date
from .models import (
    SalaryInformation, CompensationHistory, Bonus,
    Allowance, Deduction, DepartmentBudget
)
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
        # For regular users, show their own salary info
        user = request.user
        salary = SalaryInformation.objects.filter(user=user, is_active=True).first()
        allowances = Allowance.objects.filter(user=user, is_active=True)
        deductions = Deduction.objects.filter(user=user, is_active=True)
        salary_history = SalaryInformation.objects.filter(user=user).order_by('-effective_date')

        total_allowances = sum(a.amount for a in allowances)
        total_deductions = sum(d.amount for d in deductions)
        net_salary = (salary.base_salary if salary else 0) + total_allowances - total_deductions

        context = {
            'salary': salary,
            'allowances': allowances,
            'deductions': deductions,
            'salary_history': salary_history,
            'total_allowances': total_allowances,
            'total_deductions': total_deductions,
            'net_salary': net_salary,
        }
        return render(request, 'compensation/salary_list.html', context)

    # For managers - show all salaries
    salaries = SalaryInformation.objects.select_related('user').filter(is_active=True)

    search = request.GET.get('search', '')
    if search:
        salaries = salaries.filter(
            Q(user__first_name__icontains=search) |
            Q(user__last_name__icontains=search) |
            Q(user__employee_id__icontains=search)
        )

    context = {'salaries': salaries, 'search': search, 'is_manager_view': True}
    return render(request, 'compensation/salary_manager_list.html', context)


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


@login_required
def salary_change_form(request, user_id=None):
    """Form to change employee salary (managers/HR only)."""
    if not (request.user.is_manager() or request.user.is_admin):
        return redirect('compensation:dashboard')

    # If user_id provided, get that user, otherwise show selection
    employee = None
    current_salary = None

    if user_id:
        employee = get_object_or_404(User, id=user_id)
        current_salary = SalaryInformation.objects.filter(user=employee, is_active=True).first()

    if request.method == 'POST':
        try:
            employee_id = request.POST.get('employee_id') or user_id
            if not employee_id:
                return JsonResponse({
                    'success': False,
                    'message': 'Employee identifier is required for salary updates.'
                }, status=400)

            employee = get_object_or_404(User, id=employee_id)

            # Get current salary
            current_salary_obj = SalaryInformation.objects.filter(
                user=employee,
                is_active=True
            ).first()

            old_amount = current_salary_obj.base_salary if current_salary_obj else Decimal('0.00')
            new_amount = Decimal(request.POST.get('new_salary'))
            currency = request.POST.get('currency', 'AZN')

            if new_amount <= 0:
                return JsonResponse({
                    'success': False,
                    'message': 'Yeni maaş müsbət olmalıdır.'
                })

            # BUDGET VALIDATION
            if employee.department:
                current_year = date.today().year
                dept_budget = DepartmentBudget.objects.filter(
                    department=employee.department,
                    fiscal_year=current_year,
                    is_active=True
                ).first()

                if dept_budget:
                    # Calculate the increase (or decrease)
                    salary_difference = new_amount - old_amount

                    # Check if department can afford this increase
                    if salary_difference > 0:  # Only check for increases
                        if not dept_budget.can_afford(salary_difference):
                            return JsonResponse({
                                'success': False,
                                'message': (
                                    f'Büdcə kifayət etmir! '
                                    f'Departament: {employee.department.name}, '
                                    f'Qalıq büdcə: {dept_budget.remaining_budget} {dept_budget.currency}, '
                                    f'Tələb olunan: {salary_difference} {currency}'
                                ),
                                'budget_exceeded': True,
                                'remaining_budget': float(dept_budget.remaining_budget),
                                'required_amount': float(salary_difference)
                            })

                        # Update utilized amount
                        dept_budget.utilized_amount += salary_difference
                        dept_budget.save()

            # Deactivate old salary FIRST (important for OneToOne -> ForeignKey migration)
            if current_salary_obj:
                current_salary_obj.is_active = False
                current_salary_obj.end_date = date.today()
                current_salary_obj.save()
                # Ensure it's saved before creating new one

            # Create new salary record AFTER deactivating old one
            new_salary = SalaryInformation.objects.create(
                user=employee,
                base_salary=new_amount,
                currency=currency,
                payment_frequency=request.POST.get('payment_frequency', 'monthly'),
                effective_date=request.POST.get('effective_date', date.today()),
                is_active=True,
                updated_by=request.user
            )

            # Create compensation history entry
            CompensationHistory.objects.create(
                user=employee,
                previous_salary=old_amount if old_amount > 0 else None,
                new_salary=new_amount,
                currency=currency,
                change_reason=request.POST.get('change_reason', 'other'),
                effective_date=request.POST.get('effective_date', date.today()),
                notes=request.POST.get('notes', ''),
                approved_by=request.user,
                created_by=request.user
            )

            return JsonResponse({
                'success': True,
                'message': f'{employee.get_full_name()} üçün maaş uğurla dəyişdirildi',
                'old_salary': float(old_amount),
                'new_salary': float(new_amount),
                'change_percentage': float((new_amount - old_amount) / old_amount * 100) if old_amount > 0 else 0
            })
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    # GET request - show form
    from apps.departments.models import Department
    employees = User.objects.filter(is_active=True).select_related('department')

    context = {
        'employees': employees,
        'employee': employee,
        'current_salary': current_salary,
    }
    return render(request, 'compensation/salary_change_form.html', context)
