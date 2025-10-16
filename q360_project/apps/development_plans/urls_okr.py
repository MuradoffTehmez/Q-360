"""URLs for OKR module."""
from django.urls import path
from . import views_okr

app_name = 'okr'

urlpatterns = [
    path('', views_okr.okr_dashboard, name='dashboard'),
    path('objectives/', views_okr.objective_list, name='objective_list'),
    path('objectives/<int:pk>/', views_okr.objective_detail, name='objective_detail'),
    path('objectives/<int:pk>/edit/', views_okr.objective_edit, name='objective_edit'),
    path('objectives/create/', views_okr.objective_create, name='objective_create'),
    path('objectives/<int:objective_id>/keyresult/', views_okr.keyresult_create, name='keyresult_create'),
    path('objectives/<int:objective_id>/<int:kr_id>/complete/', views_okr.keyresult_complete, name='keyresult_complete'),
    path('kpi/', views_okr.kpi_dashboard, name='kpi_dashboard'),
    path('kpi/<int:kpi_id>/measurement/', views_okr.kpi_measurement_create, name='kpi_measurement_create'),
]
