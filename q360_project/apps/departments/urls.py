"""
URL configuration for departments app.
"""
from django.urls import path
from . import template_views

app_name = 'departments'

# Template-based URLs only - API endpoints are in config/api_urls.py
urlpatterns = [
    path('', template_views.organization_structure, name='department-list'),
    path('structure/', template_views.organization_structure, name='organization-structure'),
    path('chart/', template_views.department_chart, name='department-chart'),
    path('department/<int:pk>/', template_views.DepartmentDetailView.as_view(), name='department-detail'),
]
