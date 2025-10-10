"""
URL configuration for training app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TrainingResourceViewSet, UserTrainingViewSet

app_name = 'training'

router = DefaultRouter()
router.register(r'resources', TrainingResourceViewSet, basename='training-resource')
router.register(r'user-trainings', UserTrainingViewSet, basename='user-training')

urlpatterns = [
    path('', include(router.urls)),
]
