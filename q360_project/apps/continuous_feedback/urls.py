"""
URL configuration for continuous feedback app.
"""
from django.urls import path
from . import template_views

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
]
