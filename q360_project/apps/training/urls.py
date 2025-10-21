"""
URL configuration for training app.
"""
from django.urls import path
from . import template_views

app_name = 'training'

# Template-based URLs only - API endpoints are in config/api_urls.py
urlpatterns = [
    path('', template_views.catalog, name='catalog'),
    path('catalog/', template_views.catalog, name='catalog-alias'),
    path('my-trainings/', template_views.my_trainings, name='my-trainings'),
    path('my-certificates/', template_views.my_certificates, name='my-certificates'),
    path('manage/', template_views.training_manage, name='training-manage'),
    path('<int:pk>/', template_views.training_detail, name='training-detail'),

    # Skill Matrix & Certifications
    path('skill-matrix/', template_views.skill_matrix, name='skill-matrix'),
    path('certifications/', template_views.certification_tracking, name='certifications'),
]
