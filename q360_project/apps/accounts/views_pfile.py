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
            # Handle profile picture upload separately
            if 'profile_picture' in request.FILES:
                employee.profile_picture = request.FILES['profile_picture']
                employee.save()
                messages.success(request, 'Profil şəkli uğurla yeniləndi!')
                return redirect('pfile:employee_edit', pk=pk)

            # Update user fields only if they exist in POST
            if 'first_name' in request.POST:
                employee.first_name = request.POST.get('first_name', employee.first_name)
            if 'last_name' in request.POST:
                employee.last_name = request.POST.get('last_name', employee.last_name)
            if 'middle_name' in request.POST:
                employee.middle_name = request.POST.get('middle_name', '')
            if 'email' in request.POST:
                employee.email = request.POST.get('email', employee.email)
            if 'phone_number' in request.POST:
                employee.phone_number = request.POST.get('phone_number', '')
            if 'employee_id' in request.POST:
                employee.employee_id = request.POST.get('employee_id', '')
            if 'position' in request.POST:
                employee.position = request.POST.get('position', '')

            department_id = request.POST.get('department')
            if department_id:
                employee.department_id = department_id

            supervisor_id = request.POST.get('supervisor')
            if supervisor_id:
                employee.supervisor_id = supervisor_id

            employee.save()

            # Update profile fields - Personal Information
            date_of_birth = request.POST.get('date_of_birth')
            if date_of_birth:
                profile.date_of_birth = date_of_birth

            place_of_birth = request.POST.get('place_of_birth')
            if place_of_birth is not None:
                profile.place_of_birth = place_of_birth

            gender = request.POST.get('gender')
            if gender:
                profile.gender = gender

            nationality = request.POST.get('nationality')
            if nationality is not None:
                profile.nationality = nationality

            national_id = request.POST.get('national_id')
            if national_id is not None:
                profile.national_id = national_id

            marital_status = request.POST.get('marital_status')
            if marital_status:
                profile.marital_status = marital_status

            number_of_children = request.POST.get('number_of_children')
            if number_of_children is not None:
                profile.number_of_children = int(number_of_children) if number_of_children else 0

            # Contact Information
            personal_email = request.POST.get('personal_email')
            if personal_email is not None:
                profile.personal_email = personal_email

            personal_phone = request.POST.get('personal_phone')
            if personal_phone is not None:
                profile.personal_phone = personal_phone

            address = request.POST.get('address')
            if address is not None:
                profile.address = address

            city = request.POST.get('city')
            if city is not None:
                profile.city = city

            postal_code = request.POST.get('postal_code')
            if postal_code is not None:
                profile.postal_code = postal_code

            country = request.POST.get('country')
            if country is not None:
                profile.country = country

            # Emergency Contact
            emergency_contact_name = request.POST.get('emergency_contact_name')
            if emergency_contact_name is not None:
                profile.emergency_contact_name = emergency_contact_name

            emergency_contact_relationship = request.POST.get('emergency_contact_relationship')
            if emergency_contact_relationship is not None:
                profile.emergency_contact_relationship = emergency_contact_relationship

            emergency_contact_phone = request.POST.get('emergency_contact_phone')
            if emergency_contact_phone is not None:
                profile.emergency_contact_phone = emergency_contact_phone

            # Professional Information
            hire_date = request.POST.get('hire_date')
            if hire_date:
                profile.hire_date = hire_date

            contract_type = request.POST.get('contract_type')
            if contract_type:
                profile.contract_type = contract_type

            contract_start_date = request.POST.get('contract_start_date')
            if contract_start_date:
                profile.contract_start_date = contract_start_date

            contract_end_date = request.POST.get('contract_end_date')
            if contract_end_date:
                profile.contract_end_date = contract_end_date

            probation_end_date = request.POST.get('probation_end_date')
            if probation_end_date:
                profile.probation_end_date = probation_end_date

            # Education
            education_level = request.POST.get('education_level')
            if education_level:
                profile.education_level = education_level

            specialization = request.POST.get('specialization')
            if specialization is not None:
                profile.specialization = specialization

            university = request.POST.get('university')
            if university is not None:
                profile.university = university

            graduation_year = request.POST.get('graduation_year')
            if graduation_year:
                profile.graduation_year = int(graduation_year) if graduation_year else None

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
