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

    # Get documents and work history
    documents = EmployeeDocument.objects.filter(user=employee).order_by('-created_at')
    work_history = WorkHistory.objects.filter(user=employee).order_by('-effective_date')

    context = {
        'employee': employee,
        'documents': documents,
        'work_history': work_history,
    }
    return render(request, 'accounts/pfile/employee_detail.html', context)


@login_required
def employee_edit(request, pk):
    """Edit employee P-File."""
    employee = get_object_or_404(User.objects.select_related('profile', 'department', 'supervisor'), pk=pk)

    # Get or create profile
    profile, created = Profile.objects.get_or_create(user=employee)

    if request.method == 'POST':
        try:
            # Update user fields
            employee.first_name = request.POST.get('first_name', employee.first_name)
            employee.last_name = request.POST.get('last_name', employee.last_name)
            employee.email = request.POST.get('email', employee.email)
            employee.phone_number = request.POST.get('phone_number', employee.phone_number)

            department_id = request.POST.get('department')
            if department_id:
                employee.department_id = department_id

            supervisor_id = request.POST.get('supervisor')
            if supervisor_id:
                employee.supervisor_id = supervisor_id

            employee.save()

            # Update profile fields
            date_of_birth = request.POST.get('date_of_birth')
            if date_of_birth:
                profile.date_of_birth = date_of_birth

            gender = request.POST.get('gender')
            if gender:
                profile.gender = gender

            profile.address = request.POST.get('address', profile.address)
            profile.city = request.POST.get('city', profile.city)
            profile.country = request.POST.get('country', profile.country)

            education_level = request.POST.get('education_level')
            if education_level:
                profile.education_level = education_level

            profile.field_of_study = request.POST.get('field_of_study', profile.field_of_study)
            profile.emergency_contact_name = request.POST.get('emergency_contact_name', profile.emergency_contact_name)
            profile.emergency_contact_phone = request.POST.get('emergency_contact_phone', profile.emergency_contact_phone)
            profile.save()

            messages.success(request, 'Profil uğurla yeniləndi!')
            return redirect('pfile:employee_detail', pk=pk)
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"ERROR in employee_edit: {error_details}")
            messages.error(request, f'Xəta baş verdi: {str(e)}')

    # Get documents and work history
    documents = EmployeeDocument.objects.filter(user=employee).order_by('-created_at')
    work_history = WorkHistory.objects.filter(user=employee).order_by('-effective_date')

    # Get departments and users for dropdowns
    departments = Department.objects.filter(is_active=True)
    supervisors = User.objects.filter(is_active=True).exclude(pk=pk)

    context = {
        'employee': employee,
        'documents': documents,
        'work_history': work_history,
        'departments': departments,
        'supervisors': supervisors,
    }
    return render(request, 'accounts/pfile/employee_edit.html', context)


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
