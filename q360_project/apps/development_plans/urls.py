from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import template_views

router = DefaultRouter()

app_name = 'development_plans'

urlpatterns = [
    # Goal views
    path('my-goals/', template_views.my_goals, name='my-goals'),
    path('goals/create/', template_views.GoalCreateView.as_view(), name='goal-create'),
    path('goals/<int:pk>/', template_views.GoalDetailView.as_view(), name='goal-detail'),
    path('goals/<int:pk>/edit/', template_views.GoalUpdateView.as_view(), name='goal-edit'),
    path('goals/<int:pk>/complete/', template_views.goal_complete, name='goal-complete'),
    path('goals/<int:goal_pk>/progress/', template_views.add_progress, name='add-progress'),

    # Team and templates
    path('team-goals/', template_views.team_goals, name='team-goals'),
    path('templates/', template_views.goal_templates, name='goal-templates'),

    # API
    path('api/', include(router.urls)),
]
