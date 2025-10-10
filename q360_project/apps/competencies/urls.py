"""
URL configuration for competencies app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CompetencyViewSet,
    ProficiencyLevelViewSet,
    PositionCompetencyViewSet,
    UserSkillViewSet,
)
from . import template_views

app_name = 'competencies'

# DRF Router for API endpoints
router = DefaultRouter()
router.register(r'competencies', CompetencyViewSet, basename='competency')
router.register(r'proficiency-levels', ProficiencyLevelViewSet, basename='proficiency-level')
router.register(r'position-competencies', PositionCompetencyViewSet, basename='position-competency')
router.register(r'user-skills', UserSkillViewSet, basename='user-skill')

urlpatterns = router.urls + [
    # Template-based URLs
    path('', template_views.competency_list, name='competency-list'),
    path('<int:pk>/', template_views.competency_detail, name='competency-detail'),
    path('my-skills/', template_views.my_skills, name='my-skills'),
    path('manage/', template_views.competency_manage, name='competency-manage'),
]
