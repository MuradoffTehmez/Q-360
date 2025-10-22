"""Tests for dashboard models."""
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from apps.dashboard.models import (
    ForecastData, TrendData, RealTimeStat, SystemKPI
)
from apps.departments.models import Department, Organization


class ForecastDataModelTest(TestCase):
    """Test ForecastData model."""

    def setUp(self):
        self.org = Organization.objects.create(name='Test Org')
        self.dept = Department.objects.create(
            name='Test Department',
            organization=self.org
        )

    def test_create_forecast_data(self):
        """Test creating forecast data."""
        forecast = ForecastData.objects.create(
            forecast_type='staffing',
            forecast_date=timezone.now().date() + timedelta(days=30),
            predicted_value=Decimal('100.00'),
            confidence_level=Decimal('85.50'),
            department=self.dept,
            organization=self.org
        )

        self.assertEqual(forecast.forecast_type, 'staffing')
        self.assertEqual(forecast.confidence_level, Decimal('85.50'))
        self.assertEqual(forecast.department, self.dept)


class TrendDataModelTest(TestCase):
    """Test TrendData model."""

    def setUp(self):
        self.org = Organization.objects.create(name='Test Org')

    def test_create_trend_data(self):
        """Test creating trend data."""
        trend = TrendData.objects.create(
            data_type='salary',
            period=timezone.now().date(),
            value=Decimal('50000.00'),
            organization=self.org
        )

        self.assertEqual(trend.data_type, 'salary')
        self.assertEqual(trend.value, Decimal('50000.00'))


class RealTimeStatModelTest(TestCase):
    """Test RealTimeStat model."""

    def setUp(self):
        self.org = Organization.objects.create(name='Test Org')

    def test_create_realtime_stat(self):
        """Test creating real-time stat."""
        stat = RealTimeStat.objects.create(
            stat_type='active_users',
            current_value=Decimal('150'),
            previous_value=Decimal('140'),
            unit='users',
            organization=self.org
        )

        self.assertEqual(stat.stat_type, 'active_users')
        self.assertEqual(stat.current_value, Decimal('150'))
        self.assertEqual(stat.unit, 'users')


class SystemKPIModelTest(TestCase):
    """Test SystemKPI model."""

    def test_create_system_kpi(self):
        """Test creating system KPI."""
        kpi = SystemKPI.objects.create(
            name='Overall Performance',
            kpi_type='overall',
            value=Decimal('92.5'),
            target=Decimal('90.0'),
            unit='%',
            period_start=timezone.now(),
            period_end=timezone.now() + timedelta(days=30)
        )

        self.assertEqual(kpi.name, 'Overall Performance')
        self.assertEqual(kpi.value, Decimal('92.5'))
        self.assertGreater(kpi.value, kpi.target)
