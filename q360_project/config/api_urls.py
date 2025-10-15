"""
API URL configuration for Q360 Evaluation System.
All DRF API endpoints are registered here under /api/ prefix.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Import ViewSets
from apps.competencies.views import (
    CompetencyViewSet,
    ProficiencyLevelViewSet,
    PositionCompetencyViewSet,
    UserSkillViewSet,
)
from apps.training.views import (
    TrainingResourceViewSet,
    UserTrainingViewSet,
)
from apps.accounts.views import (
    UserViewSet,
    ProfileViewSet,
    RoleViewSet,
    check_password_strength,
)
from apps.departments.views import (
    OrganizationViewSet,
    DepartmentViewSet,
    PositionViewSet,
)

# Create routers for each app
competencies_router = DefaultRouter()
competencies_router.register(r'competencies', CompetencyViewSet, basename='competency')
competencies_router.register(r'proficiency-levels', ProficiencyLevelViewSet, basename='proficiency-level')
competencies_router.register(r'position-competencies', PositionCompetencyViewSet, basename='position-competency')
competencies_router.register(r'user-skills', UserSkillViewSet, basename='user-skill')

training_router = DefaultRouter()
training_router.register(r'resources', TrainingResourceViewSet, basename='training-resource')
training_router.register(r'user-trainings', UserTrainingViewSet, basename='user-training')

accounts_router = DefaultRouter()
accounts_router.register(r'users', UserViewSet, basename='user')
accounts_router.register(r'profiles', ProfileViewSet, basename='profile')
accounts_router.register(r'roles', RoleViewSet, basename='role')

departments_router = DefaultRouter()
departments_router.register(r'organizations', OrganizationViewSet, basename='organization')
departments_router.register(r'departments', DepartmentViewSet, basename='department')
departments_router.register(r'positions', PositionViewSet, basename='position')

# API URL patterns
urlpatterns = [
    path('competencies/', include(competencies_router.urls)),
    path('training/', include(training_router.urls)),
    path('accounts/', include(accounts_router.urls)),
    path('accounts/check-password-strength/', check_password_strength, name='check-password-strength'),
    path('departments/', include(departments_router.urls)),
]
