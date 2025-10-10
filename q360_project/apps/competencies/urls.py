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

router = DefaultRouter()
router.register(r'api/competencies', CompetencyViewSet, basename='api-competency')
router.register(r'api/proficiency-levels', ProficiencyLevelViewSet, basename='api-proficiency-level')
router.register(r'api/position-competencies', PositionCompetencyViewSet, basename='api-position-competency')
router.register(r'api/user-skills', UserSkillViewSet, basename='api-user-skill')

urlpatterns = [
    # Template URLs
    path('', template_views.competency_list, name='competency-list'),
    path('<int:pk>/', template_views.competency_detail, name='competency-detail'),
    path('my-skills/', template_views.my_skills, name='my-skills'),
    path('manage/', template_views.competency_manage, name='competency-manage'),

    # API URLs
    path('', include(router.urls)),
]
