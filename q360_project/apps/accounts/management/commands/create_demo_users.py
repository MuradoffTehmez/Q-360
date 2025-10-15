"""
Management command to create demo users with proper password hashing.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.departments.models import Organization, Department, Position
from apps.accounts.models import Profile

User = get_user_model()


class Command(BaseCommand):
    help = 'Create demo users with proper password hashing'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write(self.style.SUCCESS('Demo İstifadəçilər Yaradılır'))
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write('')

        # Get departments
        try:
            dept_rinn_rid = Department.objects.get(code='RID')
            dept_rinn_exs = Department.objects.get(code='EXS')
            dept_rinn_kts = Department.objects.get(code='KTS')
            dept_rinn_irtm = Department.objects.get(code='IRTM')
        except Department.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('❌ Xəta: Departamentlər tapılmadı. Əvvəlcə 01_departments.json yükləyin')
            )
            return

        # Define users
        users_data = [
            {
                'username': 'admin',
                'email': 'admin@q360.gov.az',
                'first_name': 'Sistem',
                'last_name': 'Administrator',
                'role': 'superadmin',
                'is_superuser': True,
                'is_staff': True,
                'department': None,
                'position': '',
                'employee_id': 'EMP001',
            },
            {
                'username': 'rashad.mammadov',
                'email': 'rashad.mammadov@mincom.gov.az',
                'first_name': 'Rəşad',
                'last_name': 'Məmmədov',
                'middle_name': 'Elçin',
                'role': 'admin',
                'is_staff': True,
                'department': dept_rinn_rid,
                'position': 'Departament direktoru',
                'employee_id': 'EMP002',
            },
            {
                'username': 'leyla.huseynova',
                'email': 'leyla.huseynova@mincom.gov.az',
                'first_name': 'Leyla',
                'last_name': 'Hüseynova',
                'middle_name': 'Vaqif',
                'role': 'manager',
                'department': dept_rinn_exs,
                'position': 'Şöbə müdiri',
                'employee_id': 'EMP003',
                'supervisor_username': 'rashad.mammadov',
            },
            {
                'username': 'murad.aliyev',
                'email': 'murad.aliyev@mincom.gov.az',
                'first_name': 'Murad',
                'last_name': 'Əliyev',
                'middle_name': 'Təbriz',
                'role': 'employee',
                'department': dept_rinn_exs,
                'position': 'Baş mütəxəssis',
                'employee_id': 'EMP004',
                'supervisor_username': 'leyla.huseynova',
            },
            {
                'username': 'nigar.hasanova',
                'email': 'nigar.hasanova@mincom.gov.az',
                'first_name': 'Nigar',
                'last_name': 'Həsənova',
                'middle_name': 'Ramiz',
                'role': 'employee',
                'department': dept_rinn_exs,
                'position': 'Aparıcı mütəxəssis',
                'employee_id': 'EMP005',
                'supervisor_username': 'leyla.huseynova',
            },
            {
                'username': 'elvin.quliyev',
                'email': 'elvin.quliyev@mincom.gov.az',
                'first_name': 'Elvin',
                'last_name': 'Quliyev',
                'middle_name': 'Məhəmməd',
                'role': 'employee',
                'department': dept_rinn_exs,
                'position': 'Mütəxəssis',
                'employee_id': 'EMP006',
                'supervisor_username': 'leyla.huseynova',
            },
            {
                'username': 'farid.ismayilov',
                'email': 'farid.ismayilov@mincom.gov.az',
                'first_name': 'Farid',
                'last_name': 'İsmayılov',
                'middle_name': 'Əli',
                'role': 'manager',
                'department': dept_rinn_kts,
                'position': 'Şöbə müdiri (Kibertəhlükəsizlik)',
                'employee_id': 'EMP007',
                'supervisor_username': 'rashad.mammadov',
            },
            {
                'username': 'aysel.memmedova',
                'email': 'aysel.memmedova@mincom.gov.az',
                'first_name': 'Aysel',
                'last_name': 'Məmmədova',
                'middle_name': 'İlham',
                'role': 'employee',
                'department': dept_rinn_kts,
                'position': 'Kibertəhlükəsizlik mütəxəssisi',
                'employee_id': 'EMP008',
                'supervisor_username': 'farid.ismayilov',
            },
            {
                'username': 'kamran.bashirov',
                'email': 'kamran.bashirov@mincom.gov.az',
                'first_name': 'Kamran',
                'last_name': 'Bəşirov',
                'middle_name': 'Rəhim',
                'role': 'admin',
                'is_staff': True,
                'department': dept_rinn_irtm,
                'position': 'İnsan Resursları Direktoru',
                'employee_id': 'EMP009',
            },
            {
                'username': 'sevinc.huseynli',
                'email': 'sevinc.huseynli@mincom.gov.az',
                'first_name': 'Sevinc',
                'last_name': 'Hüseynli',
                'middle_name': 'Ağa',
                'role': 'employee',
                'department': dept_rinn_irtm,
                'position': 'HR Business Partner',
                'employee_id': 'EMP010',
                'supervisor_username': 'kamran.bashirov',
            },
        ]

        created_count = 0
        skipped_count = 0

        # Create users
        for user_data in users_data:
            username = user_data.pop('username')
            supervisor_username = user_data.pop('supervisor_username', None)

            # Check if user exists
            if User.objects.filter(username=username).exists():
                self.stdout.write(
                    self.style.WARNING(f'⚠️  Atlandı: {username} (artıq mövcuddur)')
                )
                skipped_count += 1
                continue

            # Create user with hashed password
            user = User.objects.create_user(
                username=username,
                password='password',  # Django automatically hashes
                **user_data
            )

            # Set supervisor if specified
            if supervisor_username:
                try:
                    supervisor = User.objects.get(username=supervisor_username)
                    user.supervisor = supervisor
                    user.save()
                except User.DoesNotExist:
                    pass

            self.stdout.write(
                self.style.SUCCESS(f'✅ Yaradıldı: {username} ({user.get_full_name()})')
            )
            created_count += 1

        # Summary
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write(f'✅ Yaradıldı: {created_count}')
        self.stdout.write(f'⚠️  Atlandı: {skipped_count}')
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write('')
        self.stdout.write('Bütün istifadəçilərin parolu: password')
        self.stdout.write(self.style.WARNING('⚠️  İstehsal mühitində bu parolları dəyişdirin!'))
        self.stdout.write('')
