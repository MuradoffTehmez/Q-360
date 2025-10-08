from django.contrib import admin
from .models import DevelopmentGoal, ProgressLog


@admin.register(DevelopmentGoal)
class DevelopmentGoalAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'category', 'status', 'target_date']
    list_filter = ['status', 'category', 'created_at']
    search_fields = ['title', 'user__username']


@admin.register(ProgressLog)
class ProgressLogAdmin(admin.ModelAdmin):
    list_display = ['goal', 'progress_percentage', 'logged_by', 'created_at']
    list_filter = ['created_at']
    search_fields = ['goal__title', 'note']
