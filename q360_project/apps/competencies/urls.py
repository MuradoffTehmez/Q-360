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

app_name = 'competencies'

router = DefaultRouter()
router.register(r'competencies', CompetencyViewSet, basename='competency')
router.register(r'proficiency-levels', ProficiencyLevelViewSet, basename='proficiency-level')
router.register(r'position-competencies', PositionCompetencyViewSet, basename='position-competency')
router.register(r'user-skills', UserSkillViewSet, basename='user-skill')

urlpatterns = [
    path('', include(router.urls)),
]
