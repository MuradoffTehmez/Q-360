"""Admin configuration for OKR models."""
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models_okr import StrategicObjective, KeyResult, KPI, KPIMeasurement


class KeyResultInline(admin.TabularInline):
    """Inline admin for Key Results."""
    model = KeyResult
    extra = 1
    fields = ['title', 'unit', 'baseline_value', 'target_value', 'current_value', 'weight', 'is_active']
    readonly_fields = []


@admin.register(StrategicObjective)
class StrategicObjectiveAdmin(SimpleHistoryAdmin):
    """Admin for Strategic Objectives."""

    list_display = [
        'title', 'level', 'status', 'fiscal_year', 'quarter',
        'owner', 'department', 'progress_percentage'
    ]
    list_filter = ['level', 'status', 'fiscal_year', 'quarter', 'department']
    search_fields = ['title', 'description', 'owner__username']
    date_hierarchy = 'start_date'
    readonly_fields = ['created_at', 'updated_at', 'progress_percentage']
    inlines = [KeyResultInline]

    fieldsets = (
        ('Əsas Məlumat', {
            'fields': ('title', 'description', 'level', 'status')
        }),
        ('Məsuliyyət', {
            'fields': ('owner', 'department')
        }),
        ('İyerarxiya', {
            'fields': ('parent_objective',)
        }),
        ('Zaman Çərçivəsi', {
            'fields': ('fiscal_year', 'quarter', 'start_date', 'end_date')
        }),
        ('İrəliləyiş', {
            'fields': ('progress_percentage', 'weight')
        }),
        ('Sistem Məlumatları', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['cascade_to_departments', 'activate_objectives', 'complete_objectives']

    def cascade_to_departments(self, request, queryset):
        """Cascade organization-level objectives to all departments."""
        count = 0
        for obj in queryset.filter(level='organization'):
            obj.cascade_to_departments()
            count += 1
        self.message_user(request, f"{count} məqsəd şöbələrə yönləndirildi.")
    cascade_to_departments.short_description = "Şöbələrə Yönləndir"

    def activate_objectives(self, request, queryset):
        """Activate selected objectives."""
        queryset.update(status='active')
        self.message_user(request, f"{queryset.count()} məqsəd aktivləşdirildi.")
    activate_objectives.short_description = "Aktivləşdir"

    def complete_objectives(self, request, queryset):
        """Mark selected objectives as completed."""
        queryset.update(status='completed')
        self.message_user(request, f"{queryset.count()} məqsəd tamamlandı.")
    complete_objectives.short_description = "Tamamlandı Kimi İşarələ"


@admin.register(KeyResult)
class KeyResultAdmin(SimpleHistoryAdmin):
    """Admin for Key Results."""

    list_display = [
        'title', 'objective', 'unit', 'baseline_value',
        'target_value', 'current_value', 'progress_percentage', 'weight'
    ]
    list_filter = ['unit', 'is_active', 'objective__level']
    search_fields = ['title', 'description', 'objective__title']
    readonly_fields = ['created_at', 'updated_at', 'progress_percentage']

    fieldsets = (
        ('Əsas Məlumat', {
            'fields': ('objective', 'title', 'description')
        }),
        ('Ölçmə', {
            'fields': ('unit', 'baseline_value', 'target_value', 'current_value', 'progress_percentage')
        }),
        ('Parametrlər', {
            'fields': ('weight', 'is_active')
        }),
        ('Sistem Məlumatları', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class KPIMeasurementInline(admin.TabularInline):
    """Inline admin for KPI Measurements."""
    model = KPIMeasurement
    extra = 1
    fields = ['measurement_date', 'actual_value', 'trend', 'notes', 'measured_by']
    readonly_fields = []


@admin.register(KPI)
class KPIAdmin(SimpleHistoryAdmin):
    """Admin for KPIs."""

    list_display = [
        'code', 'name', 'owner', 'department', 'target_value',
        'unit', 'measurement_frequency', 'is_active'
    ]
    list_filter = ['measurement_frequency', 'is_active', 'department']
    search_fields = ['code', 'name', 'description', 'owner__username']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [KPIMeasurementInline]

    fieldsets = (
        ('Əsas Məlumat', {
            'fields': ('code', 'name', 'description')
        }),
        ('Məsuliyyət', {
            'fields': ('owner', 'department', 'objective')
        }),
        ('Ölçmə', {
            'fields': ('unit', 'target_value', 'measurement_frequency')
        }),
        ('Hədlər', {
            'fields': ('red_threshold', 'yellow_threshold', 'green_threshold')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Sistem Məlumatları', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(KPIMeasurement)
class KPIMeasurementAdmin(SimpleHistoryAdmin):
    """Admin for KPI Measurements."""

    list_display = [
        'kpi', 'measurement_date', 'actual_value', 'achievement_percentage',
        'status_color', 'trend', 'measured_by'
    ]
    list_filter = ['measurement_date', 'trend', 'kpi__department']
    search_fields = ['kpi__code', 'kpi__name', 'notes']
    date_hierarchy = 'measurement_date'
    readonly_fields = ['created_at', 'status_color', 'achievement_percentage']

    fieldsets = (
        ('KPI Məlumatları', {
            'fields': ('kpi', 'measurement_date')
        }),
        ('Ölçmə Nəticəsi', {
            'fields': ('actual_value', 'achievement_percentage', 'status_color', 'trend')
        }),
        ('Əlavə Məlumat', {
            'fields': ('notes', 'measured_by')
        }),
        ('Sistem Məlumatları', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def status_color(self, obj):
        """Display status color."""
        return obj.status_color
    status_color.short_description = 'Status'

    def achievement_percentage(self, obj):
        """Display achievement percentage."""
        return f"{obj.achievement_percentage:.2f}%"
    achievement_percentage.short_description = 'Nail Olma %'
