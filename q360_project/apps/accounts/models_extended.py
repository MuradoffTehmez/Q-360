"""
Extended models for Employee Information Management (P-File).
Document management and work history tracking.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords
from .models import User


class EmployeeDocument(models.Model):
    """
    Employee document storage model for P-File system.
    Stores all employee-related documents securely.
    """

    DOCUMENT_TYPES = [
        ('id_card', 'Şəxsiyyət Vəsiqəsi'),
        ('passport', 'Pasport'),
        ('resume', 'CV/Rezume'),
        ('diploma', 'Diplom'),
        ('certificate', 'Sertifikat'),
        ('contract', 'Əmək Müqaviləsi'),
        ('termination', 'İşdən Çıxma Sənədi'),
        ('medical', 'Tibbi Sənəd'),
        ('police_clearance', 'Məhkumsuzluq Arayışı'),
        ('other', 'Digər')
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='documents',
        verbose_name=_('İstifadəçi')
    )
    document_type = models.CharField(
        max_length=50,
        choices=DOCUMENT_TYPES,
        verbose_name=_('Sənəd Növü')
    )
    title = models.CharField(
        max_length=200,
        verbose_name=_('Başlıq')
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('Təsvir')
    )
    file = models.FileField(
        upload_to='employee_documents/%Y/%m/',
        verbose_name=_('Fayl')
    )
    file_size = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_('Fayl Ölçüsü (bytes)')
    )
    issue_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Verilmə Tarixi')
    )
    expiry_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Bitmə Tarixi')
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Aktiv')
    )
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='uploaded_documents',
        verbose_name=_('Yükləyən')
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
        verbose_name = _('İşçi Sənədi')
        verbose_name_plural = _('İşçi Sənədləri')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'document_type']),
            models.Index(fields=['expiry_date']),
        ]

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_document_type_display()}"

    def save(self, *args, **kwargs):
        if self.file and not self.file_size:
            self.file_size = self.file.size
        super().save(*args, **kwargs)

    @property
    def is_expired(self):
        """Check if document has expired."""
        if self.expiry_date:
            from datetime import date
            return date.today() > self.expiry_date
        return False

    @property
    def days_until_expiry(self):
        """Calculate days until document expiry."""
        if self.expiry_date:
            from datetime import date
            delta = self.expiry_date - date.today()
            return delta.days
        return None


class WorkHistory(models.Model):
    """
    Employee work history tracking.
    Records all position changes, department transfers, and salary adjustments.
    """

    CHANGE_TYPES = [
        ('hire', 'İşə Qəbul'),
        ('promotion', 'Vəzifə Dəyişikliyi (Tərtiqə)'),
        ('transfer', 'Şöbə Köçürülməsi'),
        ('salary_adjustment', 'Maaş Düzəlişi'),
        ('termination', 'İşdən Çıxma'),
        ('other', 'Digər')
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='work_history',
        verbose_name=_('İstifadəçi')
    )
    change_type = models.CharField(
        max_length=50,
        choices=CHANGE_TYPES,
        verbose_name=_('Dəyişiklik Növü')
    )
    effective_date = models.DateField(
        verbose_name=_('Qüvvəyə Minmə Tarixi')
    )

    # Old values
    old_position = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_('Əvvəlki Vəzifə')
    )
    old_department = models.ForeignKey(
        'departments.Department',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='old_work_histories',
        verbose_name=_('Əvvəlki Şöbə')
    )

    # New values
    new_position = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_('Yeni Vəzifə')
    )
    new_department = models.ForeignKey(
        'departments.Department',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='new_work_histories',
        verbose_name=_('Yeni Şöbə')
    )

    reason = models.TextField(
        blank=True,
        verbose_name=_('Səbəb')
    )
    notes = models.TextField(
        blank=True,
        verbose_name=_('Qeydlər')
    )
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_work_histories',
        verbose_name=_('Təsdiqləyən')
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Yaradılma Tarixi')
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_work_histories',
        verbose_name=_('Yaradan')
    )

    history = HistoricalRecords()

    class Meta:
        verbose_name = _('İş Tarixçəsi')
        verbose_name_plural = _('İş Tarixçələri')
        ordering = ['-effective_date']
        indexes = [
            models.Index(fields=['user', 'effective_date']),
            models.Index(fields=['change_type']),
        ]

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_change_type_display()} ({self.effective_date})"
