"""URLs for Wellness module."""
from django.urls import path
from . import views

app_name = 'wellness'

urlpatterns = [
    # Dashboard
    path('', views.health_dashboard, name='dashboard'),

    # Health Checkups
    path('checkups/', views.checkup_list, name='checkup_list'),
    path('checkups/<int:pk>/', views.checkup_detail, name='checkup_detail'),
    path('checkups/create/', views.checkup_create, name='checkup_create'),

    # Mental Health
    path('mental-health/survey/', views.mental_health_survey, name='mental_health_survey'),
    path('mental-health/history/', views.mental_health_history, name='mental_health_history'),

    # Fitness Programs
    path('fitness/', views.fitness_programs, name='fitness_programs'),
    path('fitness/<int:pk>/', views.fitness_program_detail, name='fitness_program_detail'),

    # Medical Claims
    path('claims/', views.medical_claims, name='medical_claims'),
    path('claims/create/', views.medical_claim_create, name='medical_claim_create'),
    path('claims/<int:pk>/', views.medical_claim_detail, name='medical_claim_detail'),

    # Wellness Challenges
    path('challenges/', views.wellness_challenges, name='challenges'),
    path('challenges/<int:pk>/', views.wellness_challenge_detail, name='challenge_detail'),

    # Step Tracking
    path('steps/', views.step_tracking, name='step_tracking'),

    # Health Score
    path('health-score/', views.health_score_history, name='health_score_history'),
]
