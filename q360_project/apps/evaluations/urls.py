"""
URL configuration for evaluations app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EvaluationCampaignViewSet, QuestionCategoryViewSet, QuestionViewSet,
    EvaluationAssignmentViewSet, ResponseViewSet, EvaluationResultViewSet
)

router = DefaultRouter()
router.register(r'campaigns', EvaluationCampaignViewSet, basename='campaign')
router.register(r'categories', QuestionCategoryViewSet, basename='category')
router.register(r'questions', QuestionViewSet, basename='question')
router.register(r'assignments', EvaluationAssignmentViewSet, basename='assignment')
router.register(r'responses', ResponseViewSet, basename='response')
router.register(r'results', EvaluationResultViewSet, basename='result')

app_name = 'evaluations'

urlpatterns = [
    path('', include(router.urls)),
]
