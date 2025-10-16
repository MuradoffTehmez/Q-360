"""Views for P-File (Employee Information Management) module."""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.db import models
from .models import User, Profile, EmployeeDocument, WorkHistory
from apps.departments.models import Department


@login_required
def employee_list(request):
    """List all employees with search and filter."""
    employees = User.objects.select_related('profile', 'department', 'supervisor').filter(is_active=True)

    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        employees = employees.filter(
            models.Q(first_name__icontains=search_query) |
            models.Q(last_name__icontains=search_query) |
            models.Q(employee_id__icontains=search_query) |
            models.Q(email__icontains=search_query)
        )

    # Filter by department
    department_id = request.GET.get('department', '')
    if department_id:
        employees = employees.filter(department_id=department_id)

    # Filter by role
    role = request.GET.get('role', '')
    if role:
        employees = employees.filter(role=role)

    departments = Department.objects.filter(is_active=True)

    context = {
        'employees': employees,
        'departments': departments,
        'search_query': search_query,
        'selected_department': department_id,
        'selected_role': role,
    }
    return render(request, 'accounts/pfile/employee_list.html', context)


@login_required
def employee_detail(request, pk):
    """View employee P-File details."""
    employee = get_object_or_404(User.objects.select_related('profile', 'department', 'supervisor'), pk=pk)

    # Get or create profile
    profile, created = Profile.objects.get_or_create(user=employee)

    context = {
        'employee': employee,
    }
    return render(request, 'accounts/pfile/employee_detail.html', context)


@login_required
@require_http_methods(["POST"])
def document_create(request, employee_id):
    """Create new document for employee."""
    employee = get_object_or_404(User, pk=employee_id)

    try:
        document = EmployeeDocument.objects.create(
            user=employee,
            document_type=request.POST.get('document_type'),
            title=request.POST.get('title'),
            description=request.POST.get('description', ''),
            file=request.FILES.get('file'),
            issue_date=request.POST.get('issue_date') or None,
            expiry_date=request.POST.get('expiry_date') or None,
            uploaded_by=request.user
        )
        return JsonResponse({'success': True, 'message': 'Sənəd uğurla əlavə edildi'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@login_required
@require_http_methods(["DELETE"])
def document_delete(request, pk):
    """Delete employee document."""
    document = get_object_or_404(EmployeeDocument, pk=pk)

    try:
        document.delete()
        return JsonResponse({'success': True, 'message': 'Sənəd silindi'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@login_required
@require_http_methods(["POST"])
def history_create(request, employee_id):
    """Create new work history entry."""
    employee = get_object_or_404(User, pk=employee_id)

    try:
        history = WorkHistory.objects.create(
            user=employee,
            change_type=request.POST.get('change_type'),
            effective_date=request.POST.get('effective_date'),
            old_position=request.POST.get('old_position', ''),
            new_position=request.POST.get('new_position', ''),
            reason=request.POST.get('reason', ''),
            created_by=request.user
        )
        return JsonResponse({'success': True, 'message': 'Tarixçə qeydi əlavə edildi'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@login_required
@require_http_methods(["DELETE"])
def history_delete(request, pk):
    """Delete work history entry."""
    history = get_object_or_404(WorkHistory, pk=pk)

    try:
        history.delete()
        return JsonResponse({'success': True, 'message': 'Qeyd silindi'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
