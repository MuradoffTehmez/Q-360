from django.urls import path
from . import views

app_name = 'engagement'

urlpatterns = [
    # Dashboard
    path('', views.engagement_dashboard, name='engagement_dashboard'),

    # Pulse Surveys
    path('surveys/', views.pulse_surveys, name='pulse_surveys'),
    path('surveys/<int:survey_id>/', views.survey_detail, name='survey_detail'),

    # Recognition Wall
    path('recognition/', views.recognition_wall, name='recognition_wall'),
    path('recognition/<int:recognition_id>/like/', views.like_recognition, name='like_recognition'),

    # Anonymous Feedback
    path('feedback/', views.anonymous_feedback, name='anonymous_feedback'),

    # Gamification & Leaderboard
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('my-profile/', views.my_profile, name='my_profile'),
]
