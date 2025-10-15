"""
URL configuration for workforce planning app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import template_views
from .views import (
    TalentMatrixViewSet, CriticalRoleViewSet,
    SuccessionCandidateViewSet, CompetencyGapViewSet
)

# API Router
router = DefaultRouter()
router.register(r'api/talent-matrix', TalentMatrixViewSet, basename='talent-matrix-api')
router.register(r'api/critical-roles', CriticalRoleViewSet, basename='critical-role-api')
router.register(r'api/succession-candidates', SuccessionCandidateViewSet, basename='succession-candidate-api')
router.register(r'api/competency-gaps', CompetencyGapViewSet, basename='competency-gap-api')

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

    # API URLs
    path('', include(router.urls)),
]
