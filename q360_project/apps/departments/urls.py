"""
URL configuration for departments app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrganizationViewSet, DepartmentViewSet, PositionViewSet
from . import template_views

router = DefaultRouter()
router.register(r'organizations', OrganizationViewSet, basename='organization')
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'positions', PositionViewSet, basename='position')

app_name = 'departments'

urlpatterns = [
    # Template views
    path('', template_views.organization_structure, name='department-list'),  # Alias for compatibility
    path('structure/', template_views.organization_structure, name='organization-structure'),
    path('chart/', template_views.department_chart, name='department-chart'),
    path('department/<int:pk>/', template_views.DepartmentDetailView.as_view(), name='department-detail'),

    # API
    path('api/', include(router.urls)),
]
