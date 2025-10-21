"""URLs for Compensation module."""
from django.urls import path
from . import views

app_name = 'compensation'

urlpatterns = [
    path('', views.compensation_dashboard, name='dashboard'),
    path('salaries/', views.salary_list, name='salary_list'),
    path('salaries/change/', views.salary_change_form, name='salary_change'),
    path('salaries/change/', views.salary_change_form, name='salary-change'),
    path('salaries/change/<int:user_id>/', views.salary_change_form, name='salary_change_user'),
    path('salaries/change/<int:user_id>/', views.salary_change_form, name='salary-change'),
    path('bonuses/', views.bonus_list, name='bonus_list'),
    path('bonuses/create/', views.bonus_create, name='bonus_create'),
    path('history/', views.compensation_history, name='history'),

    # Market Benchmarking & Total Rewards
    path('market-benchmarking/', views.market_benchmarking, name='market-benchmarking'),
    path('total-rewards/', views.total_rewards_statement, name='total-rewards'),
]
