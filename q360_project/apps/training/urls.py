"""
URL configuration for training app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TrainingResourceViewSet, UserTrainingViewSet
from . import template_views

app_name = 'training'

router = DefaultRouter()
router.register(r'api/resources', TrainingResourceViewSet, basename='api-training-resource')
router.register(r'api/user-trainings', UserTrainingViewSet, basename='api-user-training')

urlpatterns = [
    # Template URLs
    path('', template_views.my_trainings, name='my-trainings'),
    path('<int:pk>/', template_views.training_detail, name='training-detail'),
    path('catalog/', template_views.catalog, name='catalog'),
    path('manage/', template_views.training_manage, name='training-manage'),

    # API URLs
    path('', include(router.urls)),
]
