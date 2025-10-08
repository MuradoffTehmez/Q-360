"""
URL configuration for departments app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrganizationViewSet, DepartmentViewSet, PositionViewSet

router = DefaultRouter()
router.register(r'organizations', OrganizationViewSet, basename='organization')
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'positions', PositionViewSet, basename='position')

app_name = 'departments'

urlpatterns = [
    path('', include(router.urls)),
]
