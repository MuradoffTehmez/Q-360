"""
Models for Compensation & Benefits Management.
Handles salary, bonuses, allowances, deductions, and compensation history.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from decimal import Decimal
from simple_history.models import HistoricalRecords
from apps.accounts.models import User


class SalaryInformation(models.Model):
    """
    Employee salary information model.
    Stores current and historical salary data.
    """

    CURRENCY_CHOICES = [
        ('AZN', 'Azərbaycan Manatı'),
        ('USD', 'ABŞ Dolları'),
        ('EUR', 'Avro'),
    ]

    PAYMENT_FREQUENCY_CHOICES = [
        ('monthly', 'Aylıq'),
        ('biweekly', 'İki həftədə bir'),
        ('weekly', 'Həftəlik'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='salary_info',
        verbose_name=_('İstifadəçi')
    )
    base_salary = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name=_('Əsas Maaş')
    )
    currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES,
        default='AZN',
        verbose_name=_('Valyuta')
    )
    payment_frequency = models.CharField(
        max_length=20,
        choices=PAYMENT_FREQUENCY_CHOICES,
        default='monthly',
        verbose_name=_('Ödəniş Tezliyi')
    )
    effective_date = models.DateField(
        verbose_name=_('Qüvvəyə Minmə Tarixi')
    )
    end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Bitmə Tarixi')
    )

    # Bank information
    bank_name = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_('Bank Adı')
    )
    bank_account_number = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('Bank Hesab Nömrəsi')
    )
    swift_code = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_('SWIFT Kodu')
    )

    # Additional information
    notes = models.TextField(
        blank=True,
        verbose_name=_('Qeydlər')
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
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='salary_updates',
        verbose_name=_('Yeniləyən')
    )

    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Maaş Məlumatı')
        verbose_name_plural = _('Maaş Məlumatları')
        ordering = ['-effective_date']

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.base_salary} {self.currency}"


class CompensationHistory(models.Model):
    """
    Track all salary changes over time.
    """

    CHANGE_REASON_CHOICES = [
        ('hire', 'İşə Qəbul'),
        ('promotion', 'Tərtiqə'),
        ('annual_increase', 'İllik Artım'),
        ('performance', 'Performans Artımı'),
        ('market_adjustment', 'Bazar Uyğunlaşması'),
        ('cost_of_living', 'Yaşayış Xərci Artımı'),
        ('demotion', 'Vəzifə Aşağı Salınması'),
        ('other', 'Digər'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='compensation_history',
        verbose_name=_('İstifadəçi')
    )
    previous_salary = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_('Əvvəlki Maaş')
    )
    new_salary = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name=_('Yeni Maaş')
    )
    currency = models.CharField(
        max_length=3,
        default='AZN',
        verbose_name=_('Valyuta')
    )
    change_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_('Dəyişiklik Faizi')
    )
    change_reason = models.CharField(
        max_length=50,
        choices=CHANGE_REASON_CHOICES,
        verbose_name=_('Dəyişiklik Səbəbi')
    )
    effective_date = models.DateField(
        verbose_name=_('Qüvvəyə Minmə Tarixi')
    )
    notes = models.TextField(
        blank=True,
        verbose_name=_('Qeydlər')
    )
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='approved_salary_changes',
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
        related_name='created_salary_changes',
        verbose_name=_('Yaradan')
    )

    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Kompensasiya Tarixçəsi')
        verbose_name_plural = _('Kompensasiya Tarixçələri')
        ordering = ['-effective_date']

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.new_salary} {self.currency} ({self.effective_date})"

    def save(self, *args, **kwargs):
        # Calculate change percentage if both salaries are present
        if self.previous_salary and self.new_salary and self.previous_salary > 0:
            change = self.new_salary - self.previous_salary
            self.change_percentage = (change / self.previous_salary) * 100
        super().save(*args, **kwargs)


class Bonus(models.Model):
    """
    Employee bonuses and premiums.
    """

    BONUS_TYPE_CHOICES = [
        ('performance', 'Performans Bonusu'),
        ('annual', 'İllik Bonus'),
        ('project', 'Layihə Bonusu'),
        ('signing', 'İmza Bonusu'),
        ('retention', 'Saxlanma Bonusu'),
        ('referral', 'İstinad Bonusu'),
        ('holiday', 'Bayram Bonusu'),
        ('other', 'Digər'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Gözləyir'),
        ('approved', 'Təsdiqləndi'),
        ('paid', 'Ödənildi'),
        ('rejected', 'Rədd Edildi'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bonuses',
        verbose_name=_('İstifadəçi')
    )
    bonus_type = models.CharField(
        max_length=50,
        choices=BONUS_TYPE_CHOICES,
        verbose_name=_('Bonus Növü')
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name=_('Məbləğ')
    )
    currency = models.CharField(
        max_length=3,
        default='AZN',
        verbose_name=_('Valyuta')
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name=_('Status')
    )
    payment_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Ödəniş Tarixi')
    )
    fiscal_year = models.IntegerField(
        verbose_name=_('Maliyyə İli')
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('Təsvir')
    )
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_bonuses',
        verbose_name=_('Təsdiqləyən')
    )
    approved_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Təsdiq Tarixi')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Yaradılma Tarixi')
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_bonuses',
        verbose_name=_('Yaradan')
    )

    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Bonus')
        verbose_name_plural = _('Bonuslar')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'fiscal_year']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_bonus_type_display()} - {self.amount} {self.currency}"


class Allowance(models.Model):
    """
    Employee allowances (housing, transportation, meal, etc.).
    """

    ALLOWANCE_TYPE_CHOICES = [
        ('housing', 'Mənzil Müavinəti'),
        ('transportation', 'Nəqliyyat Müavinəti'),
        ('meal', 'Yemək Müavinəti'),
        ('mobile', 'Mobil Telefon Müavinəti'),
        ('education', 'Təhsil Müavinəti'),
        ('health', 'Sağlamlıq Müavinəti'),
        ('relocation', 'Köçürmə Müavinəti'),
        ('other', 'Digər'),
    ]

    PAYMENT_FREQUENCY_CHOICES = [
        ('monthly', 'Aylıq'),
        ('quarterly', 'Rüblük'),
        ('annual', 'İllik'),
        ('one_time', 'Birdəfəlik'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='allowances',
        verbose_name=_('İstifadəçi')
    )
    allowance_type = models.CharField(
        max_length=50,
        choices=ALLOWANCE_TYPE_CHOICES,
        verbose_name=_('Müavinət Növü')
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name=_('Məbləğ')
    )
    currency = models.CharField(
        max_length=3,
        default='AZN',
        verbose_name=_('Valyuta')
    )
    payment_frequency = models.CharField(
        max_length=20,
        choices=PAYMENT_FREQUENCY_CHOICES,
        default='monthly',
        verbose_name=_('Ödəniş Tezliyi')
    )
    start_date = models.DateField(
        verbose_name=_('Başlanğıc Tarixi')
    )
    end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Bitmə Tarixi')
    )
    is_taxable = models.BooleanField(
        default=True,
        verbose_name=_('Vergiyə Cəlb Olunur')
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('Təsvir')
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Aktiv')
    )
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='approved_allowances',
        verbose_name=_('Təsdiqləyən')
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
        verbose_name = _('Müavinət')
        verbose_name_plural = _('Müavinətlər')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'allowance_type']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_allowance_type_display()} - {self.amount} {self.currency}"


class Deduction(models.Model):
    """
    Employee deductions (tax, insurance, etc.).
    """

    DEDUCTION_TYPE_CHOICES = [
        ('income_tax', 'Gəlir Vergisi'),
        ('social_insurance', 'Sosial Sığorta'),
        ('health_insurance', 'Tibbi Sığorta'),
        ('pension', 'Pensiya Ayırması'),
        ('unemployment_insurance', 'İşsizlik Sığortası'),
        ('loan_repayment', 'Kredit Ödənişi'),
        ('advance_payment', 'Avans Ödənişi'),
        ('garnishment', 'Məhkəmə Qərarı'),
        ('other', 'Digər'),
    ]

    CALCULATION_METHOD_CHOICES = [
        ('fixed', 'Sabit Məbləğ'),
        ('percentage', 'Faiz'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='deductions',
        verbose_name=_('İstifadəçi')
    )
    deduction_type = models.CharField(
        max_length=50,
        choices=DEDUCTION_TYPE_CHOICES,
        verbose_name=_('Tutma Növü')
    )
    calculation_method = models.CharField(
        max_length=20,
        choices=CALCULATION_METHOD_CHOICES,
        default='percentage',
        verbose_name=_('Hesablama Metodu')
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name=_('Məbləğ / Faiz')
    )
    currency = models.CharField(
        max_length=3,
        default='AZN',
        verbose_name=_('Valyuta')
    )
    start_date = models.DateField(
        verbose_name=_('Başlanğıc Tarixi')
    )
    end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Bitmə Tarixi')
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
        verbose_name = _('Tutma')
        verbose_name_plural = _('Tutmalar')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'deduction_type']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_deduction_type_display()}"
