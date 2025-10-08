"""
URL configuration for evaluations app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EvaluationCampaignViewSet, QuestionCategoryViewSet, QuestionViewSet,
    EvaluationAssignmentViewSet, ResponseViewSet, EvaluationResultViewSet
)
from . import template_views

router = DefaultRouter()
router.register(r'api/campaigns', EvaluationCampaignViewSet, basename='campaign-api')
router.register(r'api/categories', QuestionCategoryViewSet, basename='category-api')
router.register(r'api/questions', QuestionViewSet, basename='question-api')
router.register(r'api/assignments', EvaluationAssignmentViewSet, basename='assignment-api')
router.register(r'api/responses', ResponseViewSet, basename='response-api')
router.register(r'api/results', EvaluationResultViewSet, basename='result-api')

app_name = 'evaluations'

urlpatterns = [
    # Campaign URLs
    path('campaigns/', template_views.CampaignListView.as_view(), name='campaign-list'),
    path('campaigns/create/', template_views.CampaignCreateView.as_view(), name='campaign-create'),
    path('campaigns/<int:pk>/', template_views.CampaignDetailView.as_view(), name='campaign-detail'),
    path('campaigns/<int:pk>/edit/', template_views.CampaignUpdateView.as_view(), name='campaign-edit'),
    path('campaigns/<int:pk>/activate/', template_views.campaign_activate, name='campaign-activate'),
    path('campaigns/<int:pk>/complete/', template_views.campaign_complete, name='campaign-complete'),

    # Assignment URLs
    path('my-assignments/', template_views.my_assignments, name='my-assignments'),
    path('assignments/<int:pk>/', template_views.assignment_detail, name='assignment-detail'),
    path('assignments/<int:pk>/save-draft/', template_views.assignment_save_draft, name='assignment-save-draft'),
    path('bulk-assign/', template_views.bulk_assign, name='bulk-assign'),

    # Question URLs
    path('questions/', template_views.QuestionListView.as_view(), name='question-list'),
    path('questions/create/', template_views.QuestionCreateView.as_view(), name='question-create'),
    path('categories/', template_views.QuestionCategoryListView.as_view(), name='category-list'),

    # Results URLs
    path('results/<int:campaign_pk>/', template_views.evaluation_results, name='results'),
    path('result/<int:result_pk>/', template_views.individual_result, name='individual-result'),

    # API URLs
    path('', include(router.urls)),
]
