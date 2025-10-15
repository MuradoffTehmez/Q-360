"""
URL configuration for continuous feedback app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import template_views
from .views import (
    QuickFeedbackViewSet, FeedbackBankViewSet,
    PublicRecognitionViewSet, FeedbackTagViewSet,
    FeedbackStatisticsViewSet
)

# API Router
router = DefaultRouter()
router.register(r'api/feedbacks', QuickFeedbackViewSet, basename='feedback-api')
router.register(r'api/feedback-bank', FeedbackBankViewSet, basename='feedback-bank-api')
router.register(r'api/recognitions', PublicRecognitionViewSet, basename='recognition-api')
router.register(r'api/tags', FeedbackTagViewSet, basename='tag-api')
router.register(r'api/statistics', FeedbackStatisticsViewSet, basename='statistics-api')

app_name = 'continuous_feedback'

urlpatterns = [
    # Quick Feedback
    path('send/', template_views.send_feedback_view, name='send-feedback'),
    path('my-feedback/', template_views.my_feedback_view, name='my-feedback'),
    path('received/', template_views.received_feedback_view, name='received-feedback'),

    # Feedback Bank
    path('my-bank/', template_views.my_feedback_bank_view, name='my-bank'),

    # Public Recognition Feed
    path('recognition-feed/', template_views.recognition_feed_view, name='recognition-feed'),

    # API URLs
    path('', include(router.urls)),
]
