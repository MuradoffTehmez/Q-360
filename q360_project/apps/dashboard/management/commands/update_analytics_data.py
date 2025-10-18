from django.core.management.base import BaseCommand
from apps.dashboard.utils import update_real_time_statistics, update_trend_data, calculate_kpi_indicators, update_forecast_data


class Command(BaseCommand):
    help = 'Update all analytics data including real-time stats, trends, KPIs, and forecasts'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('Starting analytics data update...')
        )
        
        # Update real-time statistics
        self.stdout.write('Updating real-time statistics...')
        update_real_time_statistics()
        self.stdout.write(
            self.style.SUCCESS('Real-time statistics updated successfully')
        )
        
        # Update trend data
        self.stdout.write('Updating trend data...')
        update_trend_data()
        self.stdout.write(
            self.style.SUCCESS('Trend data updated successfully')
        )
        
        # Calculate KPI indicators
        self.stdout.write('Calculating KPI indicators...')
        calculate_kpi_indicators()
        self.stdout.write(
            self.style.SUCCESS('KPI indicators calculated successfully')
        )
        
        # Update forecast data
        self.stdout.write('Updating forecast data...')
        update_forecast_data()
        self.stdout.write(
            self.style.SUCCESS('Forecast data updated successfully')
        )
        
        self.stdout.write(
            self.style.SUCCESS('All analytics data updated successfully!')
        )