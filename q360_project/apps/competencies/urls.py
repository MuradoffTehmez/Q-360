"""
URL configuration for competencies app.
"""
from django.urls import path
from . import template_views

app_name = 'competencies'

# Template-based URLs only - API endpoints are in config/api_urls.py
urlpatterns = [
    path('', template_views.competency_list, name='competency-list'),
    path('my-skills/', template_views.my_skills, name='my-skills'),
    path('gap-analysis/', template_views.skill_gap_analysis, name='gap-analysis'),
    path('manage/', template_views.competency_manage, name='competency-manage'),
    path('<int:pk>/', template_views.competency_detail, name='competency-detail'),
]
