"""URLs for Recruitment module."""
from django.urls import path
from . import views

app_name = 'recruitment'

urlpatterns = [
    path('', views.recruitment_dashboard, name='dashboard'),
    path('jobs/', views.job_posting_list, name='job_list'),
    path('jobs/<int:pk>/', views.job_posting_detail, name='job_detail'),
    path('jobs/create/', views.job_posting_create, name='job_create'),
    path('applications/<int:pk>/', views.application_detail, name='application_detail'),
    path('applications/<int:pk>/status/', views.application_update_status, name='application_update_status'),
    path('interviews/', views.interview_calendar, name='interview_calendar'),
    path('applications/<int:application_id>/interview/', views.interview_create, name='interview_create'),
]
