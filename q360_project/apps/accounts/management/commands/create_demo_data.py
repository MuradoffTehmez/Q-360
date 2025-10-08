"""
Management command to create demo data for testing.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.departments.models import Organization, Department
from apps.accounts.models import Profile

User = get_user_model()


class Command(BaseCommand):
    help = 'Demo məlumatlar yaradır (test üçün)'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Demo məlumatlar yaradılır...'))

        # Create organization
        org, created = Organization.objects.get_or_create(
            code='GOV001',
            defaults={
                'name': 'Dövlət İdarəsi',
                'short_name': 'DI',
                'description': 'Test təşkilatı',
                'email': 'info@gov.az'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Təşkilat yaradıldı: {org.name}'))

        # Create departments
        hr_dept, created = Department.objects.get_or_create(
            organization=org,
            code='HR',
            defaults={
                'name': 'İnsan Resursları Şöbəsi',
                'description': 'HR department'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Şöbə yaradıldı: {hr_dept.name}'))

        it_dept, created = Department.objects.get_or_create(
            organization=org,
            code='IT',
            defaults={
                'name': 'İnformasiya Texnologiyaları Şöbəsi',
                'description': 'IT department'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Şöbə yaradıldı: {it_dept.name}'))

        # Create superadmin
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@q360.az',
                password='admin123',
                first_name='Admin',
                last_name='İstifadəçi',
                role='superadmin',
                department=hr_dept,
                position='Sistem Administratoru'
            )
            self.stdout.write(self.style.SUCCESS('✓ Superadmin yaradıldı (admin/admin123)'))

        # Create manager
        if not User.objects.filter(username='manager').exists():
            manager = User.objects.create_user(
                username='manager',
                email='manager@q360.az',
                password='manager123',
                first_name='Rəşad',
                last_name='Məmmədov',
                role='manager',
                department=hr_dept,
                position='HR Meneceri'
            )
            self.stdout.write(self.style.SUCCESS('✓ Menecer yaradıldı (manager/manager123)'))

        # Create employees
        employees_data = [
            {
                'username': 'employee1',
                'email': 'employee1@q360.az',
                'first_name': 'Aynur',
                'last_name': 'Əliyeva',
                'department': hr_dept,
                'position': 'HR Mütəxəssisi'
            },
            {
                'username': 'employee2',
                'email': 'employee2@q360.az',
                'first_name': 'Elçin',
                'last_name': 'Həsənov',
                'department': it_dept,
                'position': 'Proqramçı'
            },
            {
                'username': 'employee3',
                'email': 'employee3@q360.az',
                'first_name': 'Günel',
                'last_name': 'İsmayılova',
                'department': it_dept,
                'position': 'Sistem Analitiki'
            }
        ]

        for emp_data in employees_data:
            if not User.objects.filter(username=emp_data['username']).exists():
                User.objects.create_user(
                    username=emp_data['username'],
                    email=emp_data['email'],
                    password='employee123',
                    first_name=emp_data['first_name'],
                    last_name=emp_data['last_name'],
                    role='employee',
                    department=emp_data['department'],
                    position=emp_data['position']
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ İşçi yaradıldı: {emp_data["first_name"]} {emp_data["last_name"]} '
                        f'({emp_data["username"]}/employee123)'
                    )
                )

        self.stdout.write(self.style.SUCCESS('\n✅ Bütün demo məlumatlar uğurla yaradıldı!'))
        self.stdout.write(self.style.WARNING('\nGiriş məlumatları:'))
        self.stdout.write('  Admin: admin / admin123')
        self.stdout.write('  Menecer: manager / manager123')
        self.stdout.write('  İşçilər: employee1, employee2, employee3 / employee123')
