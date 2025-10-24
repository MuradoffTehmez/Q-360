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


@login_required
def market_benchmarking(request):
    """
    Market Benchmarking view - Salary market comparison.
    Shows how salaries compare to market data by position, industry, and location.
    """
    from django.db.models import Avg, Min, Max, Count
    import json

    user = request.user

    # Get user's current salary
    user_salary = SalaryInformation.objects.filter(user=user, is_active=True).first()

    # Check if we have market data model
    has_market_data = hasattr(SalaryInformation, 'market_data_source')

    # Get position and department for comparison
    position = user.position if hasattr(user, 'position') else None
    department = user.department if hasattr(user, 'department') else None

    benchmarks = []

    if position:
        # Get all salaries for the same position
        position_salaries = SalaryInformation.objects.filter(
            is_active=True,
            user__position=position
        ).exclude(user=user)

        if position_salaries.exists():
            # Calculate percentiles
            all_amounts = list(position_salaries.values_list('base_salary', flat=True))
            all_amounts.sort()

            stats = position_salaries.aggregate(
                avg=Avg('base_salary'),
                min=Min('base_salary'),
                max=Max('base_salary'),
                count=Count('id')
            )

            # Calculate percentile position
            if user_salary and all_amounts:
                user_amount = float(user_salary.base_salary)
                below_count = sum(1 for amt in all_amounts if float(amt) < user_amount)
                percentile = (below_count / len(all_amounts)) * 100
            else:
                percentile = 50

            # Calculate percentile markers
            p25 = all_amounts[int(len(all_amounts) * 0.25)] if all_amounts else 0
            p50 = all_amounts[int(len(all_amounts) * 0.50)] if all_amounts else 0
            p75 = all_amounts[int(len(all_amounts) * 0.75)] if all_amounts else 0

            benchmarks.append({
                'category': f'{position.name} - Daxili',
                'source': 'internal',
                'sample_size': stats['count'],
                'min': float(stats['min']) if stats['min'] else 0,
                'avg': float(stats['avg']) if stats['avg'] else 0,
                'max': float(stats['max']) if stats['max'] else 0,
                'p25': float(p25),
                'p50': float(p50),
                'p75': float(p75),
                'current_salary': float(user_salary.base_salary) if user_salary else 0,
                'current_percentile': round(percentile, 1),
                'competitive_status': 'above' if percentile > 60 else 'competitive' if percentile > 40 else 'below',
            })

    if department:
        # Department average
        dept_salaries = SalaryInformation.objects.filter(
            is_active=True,
            user__department=department
        ).exclude(user=user)

        if dept_salaries.exists():
            dept_stats = dept_salaries.aggregate(
                avg=Avg('base_salary'),
                min=Min('base_salary'),
                max=Max('base_salary'),
                count=Count('id')
            )

            benchmarks.append({
                'category': f'{department.name} - Ortalama',
                'source': 'internal',
                'sample_size': dept_stats['count'],
                'min': float(dept_stats['min']) if dept_stats['min'] else 0,
                'avg': float(dept_stats['avg']) if dept_stats['avg'] else 0,
                'max': float(dept_stats['max']) if dept_stats['max'] else 0,
                'current_salary': float(user_salary.base_salary) if user_salary else 0,
                'competitive_status': 'competitive',
            })

    # Company-wide average (for context)
    company_stats = SalaryInformation.objects.filter(
        is_active=True
    ).aggregate(
        avg=Avg('base_salary'),
        min=Min('base_salary'),
        max=Max('base_salary')
    )

    # Mock external market data (would come from external sources in production)
    # You can integrate with salary APIs like Glassdoor, PayScale, etc.
    if position and has_market_data:
        # This would be real market data in production
        external_benchmarks = []
    else:
        external_benchmarks = []

    # Salary trend (user's salary history)
    salary_history = SalaryInformation.objects.filter(
        user=user
    ).order_by('effective_date')

    history_dates = [sh.effective_date.strftime('%Y-%m-%d') for sh in salary_history]
    history_amounts = [float(sh.base_salary) for sh in salary_history]

    # Recommendations
    recommendations = []

    if benchmarks and user_salary:
        primary_benchmark = benchmarks[0]
        if primary_benchmark['competitive_status'] == 'below':
            gap = primary_benchmark['avg'] - float(user_salary.base_salary)
            recommendations.append({
                'type': 'salary_review',
                'priority': 'high',
                'message': f'Sizin maaşınız bazar ortalamasından {gap:.2f} {user_salary.currency} aşağıdır. Maaş yenidən baxılması tövsiyə olunur.',
            })
        elif primary_benchmark['competitive_status'] == 'above':
            recommendations.append({
                'type': 'competitive',
                'priority': 'low',
                'message': 'Sizin maaşınız bazar ortalamasından yuxarıdır və rəqabətədavamlıdır.',
            })

    context = {
        'user_salary': user_salary,
        'benchmarks': benchmarks,
        'external_benchmarks': external_benchmarks,
        'company_stats': {
            'avg': float(company_stats['avg']) if company_stats['avg'] else 0,
            'min': float(company_stats['min']) if company_stats['min'] else 0,
            'max': float(company_stats['max']) if company_stats['max'] else 0,
        },
        'history_dates': json.dumps(history_dates),
        'history_amounts': json.dumps(history_amounts),
        'recommendations': recommendations,
        'position': position,
        'department': department,
    }

    return render(request, 'compensation/market_benchmarking.html', context)


@login_required
def total_rewards_statement(request):
    """
    Total Rewards Statement view - Comprehensive compensation breakdown.
    Shows all components: base salary, bonuses, benefits, equity, etc.
    """
    from django.db.models import Sum
    from datetime import datetime, timedelta
    import json

    user = request.user
    current_year = datetime.now().year

    # Base salary
    salary_info = SalaryInformation.objects.filter(user=user, is_active=True).first()
    base_salary = float(salary_info.base_salary) if salary_info else 0
    currency = salary_info.currency if salary_info else 'AZN'

    # Bonuses (this year)
    bonuses = Bonus.objects.filter(
        user=user,
        fiscal_year=current_year
    )
    total_bonuses = float(bonuses.aggregate(Sum('amount'))['amount__sum'] or 0)

    # Allowances (monthly recurring)
    allowances = Allowance.objects.filter(user=user, is_active=True)
    monthly_allowances = float(sum(a.amount for a in allowances))
    annual_allowances = monthly_allowances * 12

    # Benefits (actual annual value from EmployeeBenefit model)
    from apps.compensation.models import EmployeeBenefit
    from datetime import date

    from django.db.models import Q

    active_benefits = EmployeeBenefit.objects.filter(
        user=user,
        status='active',
        start_date__lte=date.today()
    ).filter(
        Q(end_date__isnull=True) | Q(end_date__gte=date.today())
    )

    benefits_value = float(sum(benefit.annual_value for benefit in active_benefits))

    # Check if we have equity/stock options
    from apps.compensation.models import EquityGrant

    equity_grants = EquityGrant.objects.filter(
        user=user,
        status__in=['vesting', 'vested', 'approved']
    )
    has_equity = equity_grants.exists()

    # Calculate vested equity value using the model's current_value property
    equity_value = 0
    if has_equity:
        for grant in equity_grants:
            # Update vested shares calculation
            grant.calculate_vested_shares()
            # Add current value
            equity_value += float(grant.current_value)

    # Total compensation
    total_cash = base_salary + total_bonuses + annual_allowances
    total_compensation = total_cash + benefits_value + equity_value

    # Breakdown for chart
    breakdown = {
        'base_salary': base_salary,
        'bonuses': total_bonuses,
        'allowances': annual_allowances,
        'benefits': benefits_value,
        'equity': equity_value,
    }

    # Market comparison (optional - from market benchmarking)
    position = user.position if hasattr(user, 'position') else None
    market_avg = 0

    if position:
        position_salaries = SalaryInformation.objects.filter(
            is_active=True,
            user__position=position
        ).exclude(user=user)

        if position_salaries.exists():
            from django.db.models import Avg
            market_avg = float(position_salaries.aggregate(Avg('base_salary'))['base_salary__avg'] or 0)

    # Compensation growth (last 3 years)
    growth_data = []
    for year in range(current_year - 2, current_year + 1):
        year_salary = SalaryInformation.objects.filter(
            user=user,
            effective_date__year__lte=year
        ).order_by('-effective_date').first()

        year_bonuses = Bonus.objects.filter(
            user=user,
            fiscal_year=year
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        year_total = (float(year_salary.base_salary) if year_salary else 0) + float(year_bonuses)

        growth_data.append({
            'year': year,
            'total': year_total,
        })

    # Benefits breakdown (real data from EmployeeBenefit model)
    benefits_breakdown = []
    benefit_types_map = {
        'health': 'Səhiyyə Sığortası',
        'dental': 'Diş Sığortası',
        'pension': 'Pensiya Töhfəsi',
        'retirement': 'Təqaüd Planı',
        'life': 'Həyat Sığortası',
        'education': 'Təhsil Yardımı',
        'transport': 'Nəqliyyat',
        'meal': 'Yemək',
        'gym': 'İdman',
        'other': 'Digər'
    }

    for benefit_type, benefit_name in benefit_types_map.items():
        benefit_value = active_benefits.filter(benefit_type=benefit_type).aggregate(
            Sum('annual_value')
        )['annual_value__sum'] or 0

        if benefit_value > 0:
            benefits_breakdown.append({
                'name': benefit_name,
                'value': float(benefit_value),
                'type': benefit_type
            })

    # If no benefits, add placeholder
    if not benefits_breakdown:
        benefits_breakdown = [
            {'name': 'Səhiyyə Sığortası', 'value': 0, 'type': 'health'},
            {'name': 'Pensiya Töhfəsi', 'value': 0, 'type': 'pension'},
        ]

    context = {
        'salary_info': salary_info,
        'base_salary': base_salary,
        'total_bonuses': total_bonuses,
        'annual_allowances': annual_allowances,
        'benefits_value': benefits_value,
        'equity_value': equity_value,
        'total_cash': total_cash,
        'total_compensation': total_compensation,
        'currency': currency,
        'breakdown': breakdown,
        'breakdown_json': json.dumps({
            'labels': ['Əsas Maaş', 'Bonuslar', 'Əlavələr', 'Benefitlər', 'Equity'],
            'data': [base_salary, total_bonuses, annual_allowances, benefits_value, equity_value]
        }),
        'market_avg': market_avg,
        'growth_data': growth_data,
        'benefits_breakdown': benefits_breakdown,
        'bonuses_list': bonuses,
        'allowances_list': allowances,
        'has_equity': has_equity,
        'current_year': current_year,
    }

    return render(request, 'compensation/total_rewards_statement.html', context)
