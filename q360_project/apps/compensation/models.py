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
from apps.departments.models import Department


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

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='salary_information',
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


class DepartmentBudget(models.Model):
    """
    Department salary budget tracking.
    Allows budget validation for salary changes.
    """

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='salary_budgets',
        verbose_name=_('Departament')
    )
    fiscal_year = models.IntegerField(
        verbose_name=_('Maliyyə İli')
    )
    annual_budget = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name=_('İllik Büdcə'),
        help_text=_('Departamentin illik maaş büdcəsi')
    )
    currency = models.CharField(
        max_length=3,
        default='AZN',
        verbose_name=_('Valyuta')
    )
    utilized_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name=_('İstifadə Olunan Məbləğ')
    )
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
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_budgets',
        verbose_name=_('Yaradan')
    )

    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Departament Büdcəsi')
        verbose_name_plural = _('Departament Büdcələri')
        ordering = ['-fiscal_year']
        unique_together = [['department', 'fiscal_year']]
        indexes = [
            models.Index(fields=['department', 'fiscal_year']),
        ]

    def __str__(self):
        return f"{self.department.name} - {self.fiscal_year} - {self.annual_budget} {self.currency}"

    @property
    def remaining_budget(self):
        """Calculate remaining budget."""
        return self.annual_budget - self.utilized_amount

    @property
    def utilization_percentage(self):
        """Calculate budget utilization percentage."""
        if self.annual_budget > 0:
            return (self.utilized_amount / self.annual_budget) * 100
        return Decimal('0.00')

    @property
    def is_over_budget(self):
        """Check if budget is exceeded."""
        return self.utilized_amount > self.annual_budget

    def can_afford(self, amount):
        """Check if department can afford additional salary expense."""
        return (self.utilized_amount + amount) <= self.annual_budget


class MarketBenchmark(models.Model):
    """
    Market salary benchmarking data.
    Stores external market data for competitive compensation analysis.
    """

    MARKET_SOURCE_CHOICES = [
        ('salary_survey', 'Maaş Sorğusu'),
        ('industry_report', 'Sənaye Hesabatı'),
        ('competitor_data', 'Rəqib Məlumatları'),
        ('job_board', 'İş Elanları'),
        ('recruitment_agency', 'İşəqəbul Agentliyi'),
        ('other', 'Digər'),
    ]

    position_title = models.CharField(
        max_length=200,
        verbose_name=_('Vəzifə Adı')
    )
    job_level = models.CharField(
        max_length=50,
        verbose_name=_('Vəzifə Səviyyəsi'),
        help_text=_('Məsələn: Entry, Mid, Senior')
    )
    industry = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('Sənaye')
    )
    location = models.CharField(
        max_length=100,
        default='Bakı, Azərbaycan',
        verbose_name=_('Yerləşmə')
    )

    # Salary ranges
    min_salary = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name=_('Minimum Maaş')
    )
    median_salary = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name=_('Median Maaş')
    )
    max_salary = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name=_('Maksimum Maaş')
    )
    currency = models.CharField(
        max_length=3,
        default='AZN',
        verbose_name=_('Valyuta')
    )

    # Statistical data
    percentile_25 = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_('25-ci Persentil')
    )
    percentile_75 = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_('75-ci Persentil')
    )

    # Data source
    data_source = models.CharField(
        max_length=30,
        choices=MARKET_SOURCE_CHOICES,
        verbose_name=_('Məlumat Mənbəyi')
    )
    source_name = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_('Mənbə Adı')
    )
    data_date = models.DateField(
        verbose_name=_('Məlumat Tarixi'),
        help_text=_('Bu məlumatın toplandığı tarix')
    )

    # Sample size and confidence
    sample_size = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_('Nümunə Ölçüsü'),
        help_text=_('Bu məlumata daxil olan işçi sayı')
    )
    confidence_level = models.CharField(
        max_length=20,
        choices=[
            ('high', 'Yüksək'),
            ('medium', 'Orta'),
            ('low', 'Aşağı'),
        ],
        default='medium',
        verbose_name=_('Etibarlılıq Səviyyəsi')
    )

    # Additional info
    notes = models.TextField(
        blank=True,
        verbose_name=_('Qeydlər')
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Aktiv')
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_benchmarks',
        verbose_name=_('Yaradan')
    )

    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Bazar Müqayisəsi')
        verbose_name_plural = _('Bazar Müqayisələri')
        ordering = ['-data_date', 'position_title']
        indexes = [
            models.Index(fields=['position_title', 'job_level']),
            models.Index(fields=['industry', 'location']),
            models.Index(fields=['-data_date']),
        ]

    def __str__(self):
        return f"{self.position_title} ({self.job_level}) - {self.median_salary} {self.currency}"

    def compare_to_salary(self, salary):
        """
        Compare a salary to market benchmarks.

        Args:
            salary: Decimal, salary to compare

        Returns:
            dict with comparison results
        """
        if salary < self.min_salary:
            position = 'below_min'
            percentile = 0
        elif salary > self.max_salary:
            position = 'above_max'
            percentile = 100
        elif salary < self.median_salary:
            # Between min and median
            position = 'below_median'
            # Estimate percentile (simple linear interpolation)
            percentile = 25 + ((salary - self.min_salary) / (self.median_salary - self.min_salary)) * 25
        else:
            # Between median and max
            position = 'above_median'
            percentile = 50 + ((salary - self.median_salary) / (self.max_salary - self.median_salary)) * 50

        return {
            'position': position,
            'percentile': round(percentile, 1),
            'difference_from_median': salary - self.median_salary,
            'difference_percent': ((salary - self.median_salary) / self.median_salary) * 100 if self.median_salary > 0 else 0,
            'is_competitive': self.percentile_25 <= salary <= self.percentile_75 if self.percentile_25 and self.percentile_75 else self.min_salary <= salary <= self.max_salary
        }


class EquityGrant(models.Model):
    """
    Equity/Stock grants for employees.
    Manages stock options, RSUs, and other equity compensation.
    """

    EQUITY_TYPE_CHOICES = [
        ('stock_option', 'Səhm Seçimi (Stock Option)'),
        ('rsu', 'Məhdudlaşdırılmış Səhm Vahidi (RSU)'),
        ('sar', 'Səhm Artım Hüququ (SAR)'),
        ('phantom_stock', 'Fantom Səhm'),
        ('espp', 'İşçi Səhm Alış Planı (ESPP)'),
    ]

    VESTING_SCHEDULE_CHOICES = [
        ('cliff', 'Cliff (Birdəfəlik)'),
        ('graded', 'Qademeli'),
        ('custom', 'Xüsusi'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Gözləyir'),
        ('approved', 'Təsdiqləndi'),
        ('vesting', 'Vesting Davam Edir'),
        ('vested', 'Tam Vested'),
        ('exercised', 'İcra Edildi'),
        ('expired', 'Müddəti Keçdi'),
        ('cancelled', 'Ləğv Edildi'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='equity_grants',
        verbose_name=_('İşçi')
    )

    # Grant details
    equity_type = models.CharField(
        max_length=20,
        choices=EQUITY_TYPE_CHOICES,
        verbose_name=_('Səhm Növü')
    )
    grant_date = models.DateField(
        verbose_name=_('Təqdim Tarixi')
    )
    number_of_shares = models.IntegerField(
        verbose_name=_('Səhm Sayı')
    )
    strike_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_('İcra Qiyməti'),
        help_text=_('Stock options üçün - səhmi almaq üçün qiymət')
    )
    currency = models.CharField(
        max_length=3,
        default='USD',
        verbose_name=_('Valyuta')
    )

    # Vesting schedule
    vesting_schedule = models.CharField(
        max_length=20,
        choices=VESTING_SCHEDULE_CHOICES,
        default='graded',
        verbose_name=_('Vesting Cədvəli')
    )
    vesting_start_date = models.DateField(
        verbose_name=_('Vesting Başlanğıc Tarixi')
    )
    vesting_period_months = models.IntegerField(
        default=48,
        verbose_name=_('Vesting Müddəti (ay)'),
        help_text=_('Ümumi vesting müddəti aylarla')
    )
    cliff_months = models.IntegerField(
        default=12,
        verbose_name=_('Cliff Müddəti (ay)'),
        help_text=_('İlk vesting-dən əvvəl gözləmə müddəti')
    )

    # Current status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name=_('Status')
    )
    vested_shares = models.IntegerField(
        default=0,
        verbose_name=_('Vested Səhmlər')
    )
    exercised_shares = models.IntegerField(
        default=0,
        verbose_name=_('İcra Edilmiş Səhmlər')
    )

    # Valuation
    current_share_value = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_('Cari Səhm Dəyəri')
    )
    last_valuation_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Son Qiymətləndirmə Tarixi')
    )

    # Expiration
    expiration_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Bitmə Tarixi')
    )

    # Approval
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_equity_grants',
        verbose_name=_('Təsdiqləyən')
    )
    approved_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Təsdiq Tarixi')
    )

    notes = models.TextField(
        blank=True,
        verbose_name=_('Qeydlər')
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_equity_grants',
        verbose_name=_('Yaradan')
    )

    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Səhm Təqdimi')
        verbose_name_plural = _('Səhm Təqdimləri')
        ordering = ['-grant_date']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['grant_date']),
            models.Index(fields=['vesting_start_date']),
        ]

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.number_of_shares} {self.get_equity_type_display()}"

    def calculate_vested_shares(self):
        """
        Calculate number of vested shares based on current date.
        """
        from datetime import date
        from dateutil.relativedelta import relativedelta

        today = date.today()

        # Check if cliff period has passed
        cliff_date = self.vesting_start_date + relativedelta(months=self.cliff_months)

        if today < cliff_date:
            # Before cliff - no shares vested
            self.vested_shares = 0
        else:
            # Calculate months since vesting start
            months_elapsed = (today.year - self.vesting_start_date.year) * 12 + \
                           (today.month - self.vesting_start_date.month)

            if months_elapsed >= self.vesting_period_months:
                # Fully vested
                self.vested_shares = self.number_of_shares
                self.status = 'vested'
            else:
                # Partially vested - linear vesting after cliff
                vesting_percentage = months_elapsed / self.vesting_period_months
                self.vested_shares = int(self.number_of_shares * vesting_percentage)
                self.status = 'vesting'

        self.save()
        return self.vested_shares

    def calculate_current_value(self):
        """Calculate current value of vested shares."""
        if not self.current_share_value:
            return Decimal('0.00')

        vested_value = Decimal(self.vested_shares) * self.current_share_value

        if self.equity_type == 'stock_option' and self.strike_price:
            # For stock options, value is (current price - strike price) * shares
            gain_per_share = max(Decimal('0'), self.current_share_value - self.strike_price)
            vested_value = Decimal(self.vested_shares) * gain_per_share

        return vested_value

    @property
    def unvested_shares(self):
        """Get number of unvested shares."""
        return self.number_of_shares - self.vested_shares - self.exercised_shares

    @property
    def exercisable_shares(self):
        """Get number of shares that can be exercised."""
        return self.vested_shares - self.exercised_shares
