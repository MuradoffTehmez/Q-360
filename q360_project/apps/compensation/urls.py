"""URLs for Compensation module."""
from django.urls import path
from . import views

app_name = 'compensation'

urlpatterns = [
    path('', views.compensation_dashboard, name='dashboard'),
    path('salaries/', views.salary_list, name='salary_list'),
    path('bonuses/', views.bonus_list, name='bonus_list'),
    path('bonuses/create/', views.bonus_create, name='bonus_create'),
    path('history/', views.compensation_history, name='history'),
]
