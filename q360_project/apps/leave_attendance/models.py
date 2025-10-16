"""
Models for Leave & Attendance Management.
Handles leave types, leave balances, leave requests, and attendance tracking.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from decimal import Decimal
from datetime import date, timedelta
from simple_history.models import HistoricalRecords
from apps.accounts.models import User


class LeaveType(models.Model):
    """
    Leave types configuration (annual, sick, maternity, etc.).
    """

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_('Ad')
    )
    code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name=_('Kod')
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('Təsvir')
    )
    days_per_year = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        validators=[MinValueValidator(Decimal('0.0'))],
        verbose_name=_('İllik Gün Sayı')
    )
    max_consecutive_days = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_('Maksimum Ardıcıl Gün Sayı')
    )
    is_paid = models.BooleanField(
        default=True,
        verbose_name=_('Ödənişli')
    )
    requires_approval = models.BooleanField(
        default=True,
        verbose_name=_('Təsdiq Tələb Olunur')
    )
    requires_document = models.BooleanField(
        default=False,
        verbose_name=_('Sənəd Tələb Olunur')
    )
    carry_forward = models.BooleanField(
        default=False,
        verbose_name=_('Növbəti İlə Keçir')
    )
    max_carry_forward_days = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_('Maksimum Keçid Gün Sayı')
    )
    notice_days = models.IntegerField(
        default=3,
        verbose_name=_('Bildiriş Günləri')
    )
    color_code = models.CharField(
        max_length=7,
        default='#3B82F6',
        verbose_name=_('Rəng Kodu')
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Aktiv')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Yaradılma Tarixi')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Yenilənmə Tarixi')
    )

    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Məzuniyyət Növü')
        verbose_name_plural = _('Məzuniyyət Növləri')
        ordering = ['name']

    def __str__(self):
        return self.name


class LeaveBalance(models.Model):
    """
    Employee leave balance tracking.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='leave_balances',
        verbose_name=_('İstifadəçi')
    )
    leave_type = models.ForeignKey(
        LeaveType,
        on_delete=models.CASCADE,
        related_name='balances',
        verbose_name=_('Məzuniyyət Növü')
    )
    year = models.IntegerField(
        verbose_name=_('İl')
    )
    entitled_days = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        default=Decimal('0.0'),
        verbose_name=_('Hüquqlu Gün Sayı')
    )
    used_days = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        default=Decimal('0.0'),
        verbose_name=_('İstifadə Olunan Gün Sayı')
    )
    pending_days = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        default=Decimal('0.0'),
        verbose_name=_('Gözləyən Gün Sayı')
    )
    carried_forward_days = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        default=Decimal('0.0'),
        verbose_name=_('Keçmiş Gün Sayı')
    )
    notes = models.TextField(
        blank=True,
        verbose_name=_('Qeydlər')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Yaradılma Tarixi')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Yenilənmə Tarixi')
    )

    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Məzuniyyət Qalığı')
        verbose_name_plural = _('Məzuniyyət Qalıqları')
        ordering = ['-year', 'user', 'leave_type']
        unique_together = ['user', 'leave_type', 'year']
        indexes = [
            models.Index(fields=['user', 'year']),
            models.Index(fields=['leave_type', 'year']),
        ]

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.leave_type.name} ({self.year})"

    @property
    def available_days(self):
        """Calculate available leave days."""
        return self.entitled_days + self.carried_forward_days - self.used_days - self.pending_days


class LeaveRequest(models.Model):
    """
    Employee leave requests.
    """

    STATUS_CHOICES = [
        ('draft', 'Qaralama'),
        ('pending', 'Gözləyir'),
        ('approved', 'Təsdiqləndi'),
        ('rejected', 'Rədd Edildi'),
        ('cancelled', 'Ləğv Edildi'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='leave_requests',
        verbose_name=_('İstifadəçi')
    )
    leave_type = models.ForeignKey(
        LeaveType,
        on_delete=models.CASCADE,
        related_name='requests',
        verbose_name=_('Məzuniyyət Növü')
    )
    start_date = models.DateField(
        verbose_name=_('Başlanğıc Tarixi')
    )
    end_date = models.DateField(
        verbose_name=_('Bitmə Tarixi')
    )
    number_of_days = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        verbose_name=_('Gün Sayı')
    )
    reason = models.TextField(
        verbose_name=_('Səbəb')
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name=_('Status')
    )
    attachment = models.FileField(
        upload_to='leave_attachments/%Y/%m/',
        null=True,
        blank=True,
        verbose_name=_('Əlavə Sənəd')
    )

    # Approval workflow
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_leave_requests',
        verbose_name=_('Təsdiqləyən')
    )
    approved_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Təsdiq Tarixi')
    )
    rejection_reason = models.TextField(
        blank=True,
        verbose_name=_('Rədd Səbəbi')
    )

    # Additional fields
    is_half_day_start = models.BooleanField(
        default=False,
        verbose_name=_('Başlanğıc Yarım Gün')
    )
    is_half_day_end = models.BooleanField(
        default=False,
        verbose_name=_('Bitmə Yarım Gün')
    )
    emergency = models.BooleanField(
        default=False,
        verbose_name=_('Təcili')
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Yaradılma Tarixi')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Yenilənmə Tarixi')
    )

    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Məzuniyyət Sorğusu')
        verbose_name_plural = _('Məzuniyyət Sorğuları')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['start_date', 'end_date']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.leave_type.name} ({self.start_date} - {self.end_date})"

    def save(self, *args, **kwargs):
        # Calculate number of days if not provided
        if not self.number_of_days:
            self.number_of_days = self.calculate_days()
        super().save(*args, **kwargs)

    def calculate_days(self):
        """Calculate working days between start and end date."""
        if not self.start_date or not self.end_date:
            return Decimal('0.0')

        days = Decimal('0.0')
        current_date = self.start_date

        while current_date <= self.end_date:
            # Skip weekends (Saturday=5, Sunday=6)
            if current_date.weekday() < 5:
                days += Decimal('1.0')
            current_date += timedelta(days=1)

        # Adjust for half days
        if self.is_half_day_start:
            days -= Decimal('0.5')
        if self.is_half_day_end:
            days -= Decimal('0.5')

        return days

    def approve(self, approved_by):
        """Approve the leave request."""
        from django.utils import timezone

        self.status = 'approved'
        self.approved_by = approved_by
        self.approved_at = timezone.now()
        self.save()

        # Update leave balance
        self.update_leave_balance()

    def reject(self, rejected_by, reason):
        """Reject the leave request."""
        self.status = 'rejected'
        self.approved_by = rejected_by
        self.rejection_reason = reason
        self.save()

    def update_leave_balance(self):
        """Update user's leave balance after approval."""
        year = self.start_date.year
        balance, created = LeaveBalance.objects.get_or_create(
            user=self.user,
            leave_type=self.leave_type,
            year=year,
            defaults={'entitled_days': self.leave_type.days_per_year}
        )

        if self.status == 'approved':
            balance.used_days += self.number_of_days
            if balance.pending_days >= self.number_of_days:
                balance.pending_days -= self.number_of_days
        elif self.status == 'pending':
            balance.pending_days += self.number_of_days

        balance.save()


class Attendance(models.Model):
    """
    Daily attendance tracking.
    """

    STATUS_CHOICES = [
        ('present', 'İştirak Edib'),
        ('absent', 'İştirak Etməyib'),
        ('half_day', 'Yarım Gün'),
        ('late', 'Gecikmə'),
        ('on_leave', 'Məzuniyyətdə'),
        ('holiday', 'Bayram'),
        ('weekend', 'Həftə Sonu'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='attendance_records',
        verbose_name=_('İstifadəçi')
    )
    date = models.DateField(
        verbose_name=_('Tarix')
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='present',
        verbose_name=_('Status')
    )
    check_in = models.TimeField(
        null=True,
        blank=True,
        verbose_name=_('Giriş Vaxtı')
    )
    check_out = models.TimeField(
        null=True,
        blank=True,
        verbose_name=_('Çıxış Vaxtı')
    )
    work_hours = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_('İş Saatı')
    )
    late_minutes = models.IntegerField(
        default=0,
        verbose_name=_('Gecikməsi (Dəqiqə)')
    )
    early_leave_minutes = models.IntegerField(
        default=0,
        verbose_name=_('Erkən Çıxış (Dəqiqə)')
    )
    notes = models.TextField(
        blank=True,
        verbose_name=_('Qeydlər')
    )
    leave_request = models.ForeignKey(
        LeaveRequest,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='attendance_records',
        verbose_name=_('Məzuniyyət Sorğusu')
    )
    verified_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='verified_attendance',
        verbose_name=_('Təsdiqləyən')
    )
    verified_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Təsdiq Tarixi')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Yaradılma Tarixi')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Yenilənmə Tarixi')
    )

    history = HistoricalRecords()

    class Meta:
        verbose_name = _('İştirak Qeydi')
        verbose_name_plural = _('İştirak Qeydləri')
        ordering = ['-date', 'user']
        unique_together = ['user', 'date']
        indexes = [
            models.Index(fields=['user', 'date']),
            models.Index(fields=['date', 'status']),
        ]

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.date} - {self.get_status_display()}"

    def save(self, *args, **kwargs):
        # Calculate work hours if check_in and check_out are present
        if self.check_in and self.check_out:
            from datetime import datetime, timedelta

            # Convert to datetime for calculation
            check_in_dt = datetime.combine(date.today(), self.check_in)
            check_out_dt = datetime.combine(date.today(), self.check_out)

            # Calculate hours
            delta = check_out_dt - check_in_dt
            self.work_hours = Decimal(str(delta.total_seconds() / 3600))

        super().save(*args, **kwargs)


class Holiday(models.Model):
    """
    Public holidays and non-working days.
    """

    HOLIDAY_TYPE_CHOICES = [
        ('public', 'Dövlət Bayramı'),
        ('religious', 'Dini Bayram'),
        ('company', 'Şirkət Bayramı'),
        ('other', 'Digər'),
    ]

    name = models.CharField(
        max_length=200,
        verbose_name=_('Ad')
    )
    date = models.DateField(
        verbose_name=_('Tarix')
    )
    holiday_type = models.CharField(
        max_length=20,
        choices=HOLIDAY_TYPE_CHOICES,
        default='public',
        verbose_name=_('Bayram Növü')
    )
    is_recurring = models.BooleanField(
        default=False,
        verbose_name=_('Təkrarlanan')
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('Təsvir')
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Aktiv')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Yaradılma Tarixi')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Yenilənmə Tarixi')
    )

    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Bayram')
        verbose_name_plural = _('Bayramlar')
        ordering = ['date']
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.name} - {self.date}"
