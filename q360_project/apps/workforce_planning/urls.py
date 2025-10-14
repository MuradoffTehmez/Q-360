"""
URL configuration for workforce planning app.
"""
from django.urls import path
from . import template_views

app_name = 'workforce_planning'

urlpatterns = [
    # Talent Matrix
    path('talent-matrix/', template_views.talent_matrix_view, name='talent-matrix'),

    # Critical Roles & Succession Planning
    path('succession-planning/', template_views.succession_planning_view, name='succession-planning'),
    path('critical-roles/', template_views.critical_roles_view, name='critical-roles'),

    # Gap Analysis
    path('gap-analysis/', template_views.gap_analysis_view, name='gap-analysis'),
    path('my-gaps/', template_views.my_gaps_view, name='my-gaps'),
]
