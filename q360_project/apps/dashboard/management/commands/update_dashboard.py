from django.core.management.base import BaseCommand
from apps.dashboard.utils import update_real_time_statistics, update_trend_data, update_forecast_data, calculate_kpi_indicators


class Command(BaseCommand):
    help = 'Update dashboard statistics, trends, forecasts, and KPIs'

    def add_arguments(self, parser):
        parser.add_argument(
            '--stats',
            action='store_true',
            help='Update real-time statistics',
        )
        parser.add_argument(
            '--trends',
            action='store_true',
            help='Update trend data',
        )
        parser.add_argument(
            '--forecasts',
            action='store_true',
            help='Update forecast data',
        )
        parser.add_argument(
            '--kpis',
            action='store_true',
            help='Update KPI indicators',
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Update all dashboard elements',
        )

    def handle(self, *args, **options):
        if options['all'] or options['stats']:
            self.stdout.write('Updating real-time statistics...')
            update_real_time_statistics()
            self.stdout.write(self.style.SUCCESS('Successfully updated real-time statistics'))

        if options['all'] or options['trends']:
            self.stdout.write('Updating trend data...')
            update_trend_data()
            self.stdout.write(self.style.SUCCESS('Successfully updated trend data'))

        if options['all'] or options['forecasts']:
            self.stdout.write('Updating forecast data...')
            update_forecast_data()
            self.stdout.write(self.style.SUCCESS('Successfully updated forecast data'))

        if options['all'] or options['kpis']:
            self.stdout.write('Updating KPI indicators...')
            calculate_kpi_indicators()
            self.stdout.write(self.style.SUCCESS('Successfully updated KPI indicators'))

        if not any([options['stats'], options['trends'], options['forecasts'], options['kpis'], options['all']]):
            self.stdout.write(self.style.WARNING('Please specify at least one option or use --all'))