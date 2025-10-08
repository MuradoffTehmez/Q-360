"""
Template views for departments app.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count

from .models import Organization, Department
from apps.accounts.models import User


@login_required
def organization_structure(request):
    """View organization structure with departments tree."""
    # Get root departments
    root_departments = Department.objects.filter(parent__isnull=True, is_active=True)

    # Get organization
    organization = Organization.objects.first()

    # Statistics
    total_departments = Department.objects.filter(is_active=True).count()
    total_employees = User.objects.filter(is_active=True).count()

    # Department sizes
    department_stats = Department.objects.filter(is_active=True).annotate(
        employee_count=Count('users')
    ).order_by('-employee_count')[:10]

    context = {
        'organization': organization,
        'root_departments': root_departments,
        'total_departments': total_departments,
        'total_employees': total_employees,
        'department_stats': department_stats,
    }

    return render(request, 'departments/organization_structure.html', context)


class DepartmentDetailView(LoginRequiredMixin, DetailView):
    """View department details with employees."""
    model = Department
    template_name = 'departments/department_detail.html'
    context_object_name = 'department'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        department = self.object

        # Get employees in this department
        employees = User.objects.filter(
            department=department,
            is_active=True
        ).select_related('supervisor')

        # Get child departments
        children = department.get_children().filter(is_active=True)

        # Get all descendants for total count
        all_descendants = department.get_descendants(include_self=True)
        total_employees = User.objects.filter(
            department__in=all_descendants,
            is_active=True
        ).count()

        context['employees'] = employees
        context['children'] = children
        context['total_employees'] = total_employees
        context['direct_employees'] = employees.count()

        return context


@login_required
def department_chart(request):
    """View organization chart."""
    root_departments = Department.objects.filter(parent__isnull=True, is_active=True)

    context = {
        'root_departments': root_departments,
    }

    return render(request, 'departments/department_chart.html', context)
