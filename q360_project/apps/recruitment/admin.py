"""Admin configuration for recruitment app."""
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import (
    JobPosting,
    Application,
    Interview,
    Offer,
    OnboardingTask
)


class InterviewInline(admin.TabularInline):
    """Inline admin for Interviews."""
    model = Interview
    extra = 0
    fields = ['interview_type', 'scheduled_date', 'status', 'rating']
    readonly_fields = []


class OfferInline(admin.StackedInline):
    """Inline admin for Offers."""
    model = Offer
    extra = 0
    fields = ['position_title', 'salary', 'currency', 'status', 'sent_date', 'expiry_date']
    readonly_fields = []


@admin.register(JobPosting)
class JobPostingAdmin(SimpleHistoryAdmin):
    """Admin for Job Postings."""

    list_display = [
        'code', 'title', 'department', 'employment_type',
        'status', 'posted_date', 'application_count'
    ]
    list_filter = ['status', 'employment_type', 'experience_level', 'department', 'remote_allowed']
    search_fields = ['code', 'title', 'description']
    date_hierarchy = 'posted_date'
    readonly_fields = ['created_at', 'updated_at', 'application_count', 'active_application_count']
    filter_horizontal = ['recruiters']

    fieldsets = (
        ('Əsas Məlumat', {
            'fields': ('code', 'title', 'department', 'description')
        }),
        ('Vəzifə Təfərrüatı', {
            'fields': ('responsibilities', 'requirements', 'qualifications')
        }),
        ('İşə Qəbul Məlumatları', {
            'fields': ('employment_type', 'experience_level', 'number_of_positions')
        }),
        ('Maaş Məlumatı', {
            'fields': ('salary_min', 'salary_max', 'salary_currency', 'show_salary')
        }),
        ('Yer', {
            'fields': ('location', 'remote_allowed')
        }),
        ('Status və Tarixlər', {
            'fields': ('status', 'posted_date', 'closing_date')
        }),
        ('İşə Qəbul Komandası', {
            'fields': ('hiring_manager', 'recruiters')
        }),
        ('Statistika', {
            'fields': ('application_count', 'active_application_count'),
            'classes': ('collapse',)
        }),
        ('Sistem Məlumatları', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['open_postings', 'close_postings']

    def open_postings(self, request, queryset):
        """Open selected job postings."""
        queryset.update(status='open')
        self.message_user(request, f"{queryset.count()} vakansiya açıldı.")
    open_postings.short_description = "Vakansiyaları Aç"

    def close_postings(self, request, queryset):
        """Close selected job postings."""
        queryset.update(status='closed')
        self.message_user(request, f"{queryset.count()} vakansiya bağlandı.")
    close_postings.short_description = "Vakansiyaları Bağla"


@admin.register(Application)
class ApplicationAdmin(SimpleHistoryAdmin):
    """Admin for Applications."""

    list_display = [
        'full_name', 'job_posting', 'email', 'status',
        'rating', 'source', 'applied_at'
    ]
    list_filter = ['status', 'source', 'job_posting__department', 'applied_at']
    search_fields = ['first_name', 'last_name', 'email', 'phone']
    date_hierarchy = 'applied_at'
    readonly_fields = ['applied_at', 'updated_at', 'full_name']
    inlines = [InterviewInline, OfferInline]

    fieldsets = (
        ('Namizəd Məlumatları', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'full_name')
        }),
        ('Vakansiya', {
            'fields': ('job_posting',)
        }),
        ('Sənədlər', {
            'fields': ('resume', 'cover_letter', 'portfolio_url')
        }),
        ('Müraciət Məlumatları', {
            'fields': ('status', 'source', 'referrer')
        }),
        ('Təcrübə və Maaş', {
            'fields': ('current_position', 'years_of_experience', 'expected_salary', 'notice_period_days')
        }),
        ('Qiymətləndirmə', {
            'fields': ('rating', 'notes', 'assigned_to')
        }),
        ('Sistem Məlumatları', {
            'fields': ('applied_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['move_to_screening', 'move_to_interview', 'reject_applications']

    def move_to_screening(self, request, queryset):
        """Move applications to screening stage."""
        queryset.update(status='screening')
        self.message_user(request, f"{queryset.count()} müraciət sınaq mərhələsinə keçdi.")
    move_to_screening.short_description = "Sınaq Mərhələsinə Keçir"

    def move_to_interview(self, request, queryset):
        """Move applications to interview stage."""
        queryset.update(status='interview')
        self.message_user(request, f"{queryset.count()} müraciət müsahibə mərhələsinə keçdi.")
    move_to_interview.short_description = "Müsahibə Mərhələsinə Keçir"

    def reject_applications(self, request, queryset):
        """Reject selected applications."""
        queryset.update(status='rejected')
        self.message_user(request, f"{queryset.count()} müraciət rədd edildi.")
    reject_applications.short_description = "Müraciətləri Rədd Et"


@admin.register(Interview)
class InterviewAdmin(SimpleHistoryAdmin):
    """Admin for Interviews."""

    list_display = [
        'application', 'interview_type', 'scheduled_date',
        'status', 'rating', 'recommendation'
    ]
    list_filter = ['status', 'interview_type', 'recommendation', 'scheduled_date']
    search_fields = [
        'application__first_name', 'application__last_name',
        'application__email'
    ]
    date_hierarchy = 'scheduled_date'
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['interviewers']

    fieldsets = (
        ('Müsahibə Məlumatları', {
            'fields': ('application', 'interview_type', 'scheduled_date', 'duration_minutes')
        }),
        ('Yer və Link', {
            'fields': ('location', 'meeting_link')
        }),
        ('Müsahibəçilər', {
            'fields': ('interviewers',)
        }),
        ('Status və Rəy', {
            'fields': ('status', 'feedback', 'rating', 'recommendation')
        }),
        ('Sistem Məlumatları', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['mark_completed', 'mark_cancelled']

    def mark_completed(self, request, queryset):
        """Mark interviews as completed."""
        queryset.update(status='completed')
        self.message_user(request, f"{queryset.count()} müsahibə tamamlandı kimi işarələndi.")
    mark_completed.short_description = "Tamamlandı Kimi İşarələ"

    def mark_cancelled(self, request, queryset):
        """Mark interviews as cancelled."""
        queryset.update(status='cancelled')
        self.message_user(request, f"{queryset.count()} müsahibə ləğv edildi.")
    mark_cancelled.short_description = "Ləğv Et"


@admin.register(Offer)
class OfferAdmin(SimpleHistoryAdmin):
    """Admin for Offers."""

    list_display = [
        'application', 'position_title', 'salary', 'currency',
        'status', 'sent_date', 'expiry_date'
    ]
    list_filter = ['status', 'currency', 'sent_date']
    search_fields = [
        'application__first_name', 'application__last_name',
        'position_title'
    ]
    date_hierarchy = 'sent_date'
    readonly_fields = ['created_at', 'updated_at', 'is_expired']

    fieldsets = (
        ('Namizəd', {
            'fields': ('application',)
        }),
        ('Təklif Təfərrüatı', {
            'fields': ('position_title', 'salary', 'currency', 'bonus_potential', 'benefits', 'start_date')
        }),
        ('Status və Tarixlər', {
            'fields': ('status', 'sent_date', 'expiry_date', 'response_date', 'is_expired')
        }),
        ('Sənəd', {
            'fields': ('offer_letter', 'notes')
        }),
        ('Təsdiq', {
            'fields': ('approved_by', 'approved_at')
        }),
        ('Sistem Məlumatları', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['send_offers', 'mark_accepted']

    def send_offers(self, request, queryset):
        """Mark offers as sent."""
        from datetime import date
        queryset.update(status='sent', sent_date=date.today())
        self.message_user(request, f"{queryset.count()} təklif göndərildi kimi işarələndi.")
    send_offers.short_description = "Təklifləri Göndər"

    def mark_accepted(self, request, queryset):
        """Mark offers as accepted."""
        from datetime import date
        queryset.update(status='accepted', response_date=date.today())
        self.message_user(request, f"{queryset.count()} təklif qəbul edildi.")
    mark_accepted.short_description = "Qəbul Edildi Kimi İşarələ"

    def is_expired(self, obj):
        """Display if offer is expired."""
        return obj.is_expired
    is_expired.short_description = 'Müddəti Keçib'
    is_expired.boolean = True


@admin.register(OnboardingTask)
class OnboardingTaskAdmin(SimpleHistoryAdmin):
    """Admin for Onboarding Tasks."""

    list_display = [
        'application', 'new_hire', 'title', 'category',
        'status', 'assigned_to', 'due_date'
    ]
    list_filter = ['status', 'category', 'due_date']
    search_fields = [
        'application__first_name', 'application__last_name',
        'new_hire__username', 'title'
    ]
    date_hierarchy = 'due_date'
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Namizəd/Yeni İşçi', {
            'fields': ('application', 'new_hire')
        }),
        ('Tapşırıq Məlumatları', {
            'fields': ('title', 'description', 'category')
        }),
        ('Status və Təyin', {
            'fields': ('status', 'assigned_to', 'due_date', 'completed_date')
        }),
        ('Qeydlər', {
            'fields': ('notes',)
        }),
        ('Sistem Məlumatları', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['mark_completed', 'mark_in_progress']

    def mark_completed(self, request, queryset):
        """Mark tasks as completed."""
        from datetime import date
        queryset.update(status='completed', completed_date=date.today())
        self.message_user(request, f"{queryset.count()} tapşırıq tamamlandı.")
    mark_completed.short_description = "Tamamlandı Kimi İşarələ"

    def mark_in_progress(self, request, queryset):
        """Mark tasks as in progress."""
        queryset.update(status='in_progress')
        self.message_user(request, f"{queryset.count()} tapşırıq davam edir kimi işarələndi.")
    mark_in_progress.short_description = "Davam Edir Kimi İşarələ"
