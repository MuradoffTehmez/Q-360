from django.urls import path
from . import views

app_name = 'sentiment_analysis'

urlpatterns = [
    path('dashboard/', views.sentiment_dashboard, name='dashboard'),
    path('feedback/<int:pk>/', views.feedback_detail, name='feedback_detail'),
    path('feedback/<int:pk>/resolve/', views.feedback_resolve, name='feedback_resolve'),
]