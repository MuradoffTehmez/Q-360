"""Views for Leave & Attendance module."""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from datetime import date
from .models import LeaveType, LeaveBalance, LeaveRequest, Attendance, Holiday
from django.contrib.auth import get_user_model

User = get_user_model()


@login_required
def leave_dashboard(request):
    """Leave management dashboard."""
    user = request.user
    current_year = date.today().year

    balances = LeaveBalance.objects.filter(user=user, year=current_year).select_related('leave_type')
    recent_requests = LeaveRequest.objects.filter(user=user).order_by('-created_at')[:10]
    pending_requests = LeaveRequest.objects.filter(user=user, status='pending').count()

    context = {
        'balances': balances,
        'recent_requests': recent_requests,
        'pending_requests': pending_requests,
        'current_year': current_year,
    }
    return render(request, 'leave_attendance/leave_dashboard.html', context)


@login_required
def leave_request_create(request):
    """Create new leave request."""
    leave_types = LeaveType.objects.filter(is_active=True)

    if request.method == 'POST':
        try:
            leave_request = LeaveRequest.objects.create(
                user=request.user,
                leave_type_id=request.POST.get('leave_type'),
                start_date=request.POST.get('start_date'),
                end_date=request.POST.get('end_date'),
                reason=request.POST.get('reason'),
                is_half_day_start=request.POST.get('is_half_day_start') == 'on',
                is_half_day_end=request.POST.get('is_half_day_end') == 'on',
            )
            leave_request.status = 'pending'
            leave_request.save()
            return JsonResponse({'success': True, 'message': 'Məzuniyyət sorğusu göndərildi'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    context = {'leave_types': leave_types}
    return render(request, 'leave_attendance/leave_request_create.html', context)


@login_required
def leave_request_list(request):
    """List leave requests."""
    requests = LeaveRequest.objects.filter(user=request.user).order_by('-created_at')

    status_filter = request.GET.get('status', '')
    if status_filter:
        requests = requests.filter(status=status_filter)

    context = {'requests': requests, 'status_filter': status_filter}
    return render(request, 'leave_attendance/leave_request_list.html', context)


@login_required
def attendance_calendar(request):
    """Attendance calendar view."""
    current_month = date.today().month
    current_year = date.today().year

    attendance_records = Attendance.objects.filter(
        user=request.user,
        date__month=current_month,
        date__year=current_year
    ).order_by('date')

    context = {
        'attendance_records': attendance_records,
        'current_month': current_month,
        'current_year': current_year,
    }
    return render(request, 'leave_attendance/attendance_calendar.html', context)


@login_required
def team_leave_calendar(request):
    """Team leave calendar for managers."""
    if not request.user.is_manager():
        return redirect('leave_attendance:leave_dashboard')

    # Get team members
    team = User.objects.filter(supervisor=request.user)
    current_month = date.today().month
    current_year = date.today().year

    # Get approved leave requests
    leave_requests = LeaveRequest.objects.filter(
        user__in=team,
        status='approved',
        start_date__year=current_year,
        start_date__month__lte=current_month + 2,
        end_date__month__gte=current_month - 1
    ).select_related('user', 'leave_type')

    context = {
        'leave_requests': leave_requests,
        'team': team,
        'current_month': current_month,
        'current_year': current_year,
    }
    return render(request, 'leave_attendance/team_calendar.html', context)
