"""URLs for OKR module."""
from django.urls import path
from . import views_okr

app_name = 'okr'

urlpatterns = [
    path('', views_okr.okr_dashboard, name='dashboard'),
    path('objectives/', views_okr.objective_list, name='objective_list'),
    path('objectives/<int:pk>/', views_okr.objective_detail, name='objective_detail'),
    path('objectives/<int:pk>/edit/', views_okr.objective_edit, name='objective_edit'),
    path('objectives/<int:pk>/activate/', views_okr.objective_activate, name='objective_activate'),
    path('objectives/<int:pk>/complete/', views_okr.objective_complete, name='objective_complete'),
    path('objectives/create/', views_okr.objective_create, name='objective_create'),
    path('objectives/<int:objective_id>/keyresult/', views_okr.keyresult_create, name='keyresult_create'),
    path('keyresults/<int:kr_id>/edit/', views_okr.keyresult_edit, name='keyresult_edit'),
    path('keyresults/<int:kr_id>/update/', views_okr.keyresult_update_value, name='keyresult_update_value'),
    path('objectives/<int:objective_id>/<int:kr_id>/complete/', views_okr.keyresult_complete, name='keyresult_complete'),
    path('objectives/<int:objective_id>/milestone/', views_okr.milestone_create, name='milestone_create'),
    path('objectives/<int:objective_id>/milestone/<int:milestone_id>/complete/', views_okr.milestone_complete, name='milestone_complete'),
    path('objectives/<int:objective_id>/update/', views_okr.objective_update_create, name='objective_update_create'),
    path('kpi/', views_okr.kpi_dashboard, name='kpi_dashboard'),
    path('kpi/<int:kpi_id>/measurement/', views_okr.kpi_measurement_create, name='kpi_measurement_create'),
]
