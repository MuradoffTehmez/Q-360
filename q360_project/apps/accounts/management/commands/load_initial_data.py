"""
Management command to load all initial data fixtures for Q360 system.
"""
import os
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings


class Command(BaseCommand):
    help = 'Load all initial data fixtures for Q360 system in the correct order'

    def add_arguments(self, parser):
        parser.add_argument(
            '--skip-users',
            action='store_true',
            help='Skip loading user data (useful if users already exist)',
        )

    def handle(self, *args, **options):
        """Load fixtures in the correct order to handle dependencies."""

        fixtures_dir = os.path.join(settings.BASE_DIR, 'fixtures')

        # Define fixtures in dependency order
        fixtures = [
            '01_departments.json',      # Organizations, Departments, Positions
            '02_accounts.json',          # Users and Profiles
            '03_competencies.json',      # Competencies, Levels, Position Competencies, User Skills
            '04_evaluations.json',       # Question Categories, Questions, Campaigns
            '05_training.json',          # Training Resources, User Trainings
            '06_development_plans.json', # Development Goals, Progress Logs
            '07_workforce_planning.json',# Talent Matrix, Critical Roles, Succession, Gaps
            '08_continuous_feedback.json',# Feedback Tags, Quick Feedback, Feedback Bank
            '09_support.json',           # Support Tickets, Ticket Comments
        ]

        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write(self.style.SUCCESS('Q360 İlkin Data Yükləmə Prosesi'))
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write('')

        # Skip users if requested
        if options['skip_users']:
            self.stdout.write(self.style.WARNING('⚠️  --skip-users flag aktiv: İstifadəçi dataları atlanacaq'))
            fixtures.remove('02_accounts.json')

        total_fixtures = len(fixtures)
        loaded_count = 0
        failed_count = 0

        for i, fixture_file in enumerate(fixtures, 1):
            fixture_path = os.path.join(fixtures_dir, fixture_file)

            self.stdout.write(f'\n[{i}/{total_fixtures}] {fixture_file} yüklənir...')

            if not os.path.exists(fixture_path):
                self.stdout.write(
                    self.style.ERROR(f'   ❌ Xəta: Fayl tapılmadı: {fixture_path}')
                )
                failed_count += 1
                continue

            try:
                call_command('loaddata', fixture_path, verbosity=0)
                self.stdout.write(
                    self.style.SUCCESS(f'   ✅ Uğurla yükləndi: {fixture_file}')
                )
                loaded_count += 1
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'   ❌ Xəta: {fixture_file} yüklənərkən problem: {str(e)}')
                )
                failed_count += 1

                # Show hint for common errors
                if 'duplicate key' in str(e).lower():
                    self.stdout.write(
                        self.style.WARNING('   💡 Məsləhət: Bu data artıq mövcuddur. Database-i təmizləyin və ya --skip-users istifadə edin.')
                    )
                elif 'foreign key' in str(e).lower():
                    self.stdout.write(
                        self.style.WARNING('   💡 Məsləhət: Dependency problemi ola bilər. Fixtures ardıcıllığını yoxlayın.')
                    )

        # Summary
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write(self.style.SUCCESS('Yükləmə Tamamlandı'))
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write(f'✅ Uğurlu: {loaded_count}/{total_fixtures}')
        if failed_count > 0:
            self.stdout.write(self.style.ERROR(f'❌ Uğursuz: {failed_count}/{total_fixtures}'))

        if failed_count == 0:
            self.stdout.write('')
            self.stdout.write(self.style.SUCCESS('🎉 Bütün ilkin data uğurla yükləndi!'))
            self.stdout.write('')
            self.stdout.write('İndi sistemi test edə bilərsiniz:')
            self.stdout.write('  • Admin panel: http://localhost:8000/admin/')
            self.stdout.write('  • İstifadəçi: admin / password (ilk dəfə dəyişdirin)')
        else:
            self.stdout.write('')
            self.stdout.write(self.style.WARNING('⚠️  Bəzi fixtures yüklənmədi. Yuxarıdakı xətaları yoxlayın.'))

        self.stdout.write('')
