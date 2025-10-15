"""
Admin configuration for training app.
"""
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import TrainingResource, UserTraining


@admin.register(TrainingResource)
class TrainingResourceAdmin(SimpleHistoryAdmin):
    """Admin for TrainingResource model."""

    list_display = [
        'title',
        'type',
        'difficulty_level',
        'is_online',
        'duration_hours',
        'cost',
        'is_active',
        'is_mandatory',
        'get_assigned_count',
        'created_at'
    ]
    list_filter = [
        'type',
        'difficulty_level',
        'is_online',
        'is_active',
        'is_mandatory',
        'delivery_method',
        'created_at'
    ]
    search_fields = ['title', 'description', 'provider', 'instructor']
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['required_competencies']
    ordering = ['title']

    fieldsets = (
        ('Əsas Məlumat', {
            'fields': (
                'title',
                'description',
                'type',
                'difficulty_level',
                'language'
            )
        }),
        ('Çatdırılma Detalları', {
            'fields': (
                'is_online',
                'delivery_method',
                'link',
                'duration_hours'
            )
        }),
        ('Kompetensiyalar', {
            'fields': ('required_competencies',)
        }),
        ('Təminatçı Məlumatları', {
            'fields': ('provider', 'instructor')
        }),
        ('Qiymət və Tutum', {
            'fields': ('cost', 'max_participants')
        }),
        ('Status', {
            'fields': ('is_active', 'is_mandatory')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_assigned_count(self, obj):
        """Təyin olunmuş istifadəçi sayını qaytarır."""
        return obj.user_trainings.count()
    get_assigned_count.short_description = 'Təyin Sayı'


@admin.register(UserTraining)
class UserTrainingAdmin(SimpleHistoryAdmin):
    """Admin for UserTraining model."""

    list_display = [
        'user',
        'resource',
        'status',
        'assignment_type',
        'progress_percentage',
        'start_date',
        'due_date',
        'is_overdue_display',
        'rating',
        'created_at'
    ]
    list_filter = [
        'status',
        'assignment_type',
        'created_at',
        'start_date',
        'due_date'
    ]
    search_fields = [
        'user__username',
        'user__first_name',
        'user__last_name',
        'resource__title'
    ]
    readonly_fields = ['created_at', 'updated_at', 'completed_date']
    ordering = ['-created_at']

    fieldsets = (
        ('Əsas Məlumat', {
            'fields': (
                'user',
                'resource',
                'assigned_by',
                'assignment_type',
                'related_goal'
            )
        }),
        ('Tarixlər', {
            'fields': (
                'start_date',
                'due_date',
                'completed_date'
            )
        }),
        ('Status və Proqres', {
            'fields': (
                'status',
                'progress_percentage'
            )
        }),
        ('Rəy və Nəticələr', {
            'fields': (
                'completion_note',
                'user_feedback',
                'rating',
                'certificate_url'
            )
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['mark_as_completed', 'mark_as_in_progress']

    def is_overdue_display(self, obj):
        """Vaxtının keçib-keçmədiyini göstərir."""
        return obj.is_overdue()
    is_overdue_display.short_description = 'Vaxtı Keçib'
    is_overdue_display.boolean = True

    def mark_as_completed(self, request, queryset):
        """Toplu tamamlanma əməliyyatı."""
        count = 0
        for training in queryset:
            training.mark_completed()
            count += 1
        self.message_user(request, f'{count} təlim tamamlanmış kimi qeyd edildi.')
    mark_as_completed.short_description = 'Seçilmiş təlimləri tamamlanmış kimi qeyd et'

    def mark_as_in_progress(self, request, queryset):
        """Toplu proqresdə əməliyyatı."""
        count = 0
        for training in queryset:
            training.mark_in_progress()
            count += 1
        self.message_user(request, f'{count} təlim proqresdə kimi qeyd edildi.')
    mark_as_in_progress.short_description = 'Seçilmiş təlimləri proqresdə kimi qeyd et'
