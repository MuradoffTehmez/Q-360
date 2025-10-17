from django.core.management.base import BaseCommand
from apps.dashboard.ai_forecasting import run_ai_forecasting


class Command(BaseCommand):
    help = 'Run AI-based forecasting for staffing, budget, and performance'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        self.stdout.write('Running AI forecasting...')
        success = run_ai_forecasting()
        if success:
            self.stdout.write(
                self.style.SUCCESS('Successfully completed AI forecasting')
            )
        else:
            self.stdout.write(
                self.style.ERROR('AI forecasting failed')
            )