"""
URL configuration for training app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TrainingResourceViewSet, UserTrainingViewSet
from . import template_views

app_name = 'training'

# DRF Router for API endpoints
router = DefaultRouter()
router.register(r'resources', TrainingResourceViewSet, basename='training-resource')
router.register(r'user-trainings', UserTrainingViewSet, basename='user-training')

urlpatterns = router.urls + [
    # Template-based URLs
    path('', template_views.my_trainings, name='my-trainings'),
    path('<int:pk>/', template_views.training_detail, name='training-detail'),
    path('catalog/', template_views.catalog, name='catalog'),
    path('manage/', template_views.training_manage, name='training-manage'),
]
