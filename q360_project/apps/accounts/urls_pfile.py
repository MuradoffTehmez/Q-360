"""URLs for P-File module."""
from django.urls import path
from . import views_pfile

app_name = 'pfile'

urlpatterns = [
    path('employees/', views_pfile.employee_list, name='employee_list'),
    path('employees/<int:pk>/', views_pfile.employee_detail, name='employee_detail'),
    path('employees/<int:pk>/edit/', views_pfile.employee_edit, name='employee_edit'),
    path('employees/<int:employee_id>/document/create/', views_pfile.document_create, name='document_create'),
    path('document/<int:pk>/delete/', views_pfile.document_delete, name='document_delete'),
    path('employees/<int:employee_id>/history/create/', views_pfile.history_create, name='history_create'),
    path('history/<int:pk>/delete/', views_pfile.history_delete, name='history_delete'),
]
