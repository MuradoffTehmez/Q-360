"""
Management command to load all initial data using Python objects (not JSON fixtures).
This avoids issues with auto_now_add fields.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import date, datetime

from apps.departments.models import Organization, Department, Position
from apps.competencies.models import Competency, ProficiencyLevel, PositionCompetency, UserSkill
from apps.evaluations.models import QuestionCategory, Question, EvaluationCampaign, CampaignQuestion
from apps.training.models import TrainingResource, UserTraining
from apps.development_plans.models import DevelopmentGoal, ProgressLog
from apps.workforce_planning.models import TalentMatrix, CriticalRole, SuccessionCandidate, CompetencyGap
from apps.continuous_feedback.models import (
    FeedbackTag, QuickFeedback, FeedbackBank, PublicRecognition
)
from apps.support.models import SupportTicket, TicketComment

User = get_user_model()


class Command(BaseCommand):
    help = 'Load all initial data using Python objects'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write(self.style.SUCCESS('Q360 İlkin Data Yükləmə (Python Objects)'))
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write('')

        try:
            # Step 1: Organizations
            self.stdout.write('[1/10] Organizations və Departments yaradılır...')
            self.create_organizations_and_departments()

            # Step 2: Users
            self.stdout.write('[2/10] İstifadəçilər yaradılır...')
            self.create_users()

            # Step 3: Competencies
            self.stdout.write('[3/10] Kompetensiyalar yaradılır...')
            self.create_competencies()

            # Step 4: Evaluations
            self.stdout.write('[4/10] Qiymətləndirmə strukturu yaradılır...')
            self.create_evaluations()

            # Step 5: Training
            self.stdout.write('[5/10] Təlim resursları yaradılır...')
            self.create_training()

            # Step 6: Development Plans
            self.stdout.write('[6/10] İnkişaf planları yaradılır...')
            self.create_development_plans()

            # Step 7: Workforce Planning
            self.stdout.write('[7/10] Kadr planlaması dataları yaradılır...')
            self.create_workforce_planning()

            # Step 8: Continuous Feedback
            self.stdout.write('[8/10] Davamlı rəy sistemi yaradılır...')
            self.create_continuous_feedback()

            # Step 9: Support
            self.stdout.write('[9/10] Dəstək sistemi yaradılır...')
            self.create_support()

            # Step 10: Final steps
            self.stdout.write('[10/10] Final konfiqurasiyalar...')
            self.finalize()

            self.stdout.write('')
            self.stdout.write(self.style.SUCCESS('=' * 70))
            self.stdout.write(self.style.SUCCESS('🎉 Bütün data uğurla yükləndi!'))
            self.stdout.write(self.style.SUCCESS('=' * 70))
            self.stdout.write('')
            self.stdout.write('Test istifadəçilər:')
            self.stdout.write('  • admin / password')
            self.stdout.write('  • rashad.mammadov / password')
            self.stdout.write('  • leyla.huseynova / password')
            self.stdout.write('')

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Xəta: {str(e)}'))
            import traceback
            traceback.print_exc()

    def create_organizations_and_departments(self):
        """Create organizations, departments, and positions."""
        # Organizations
        org1, _ = Organization.objects.get_or_create(
            code='MINT',
            defaults={
                'name': 'Azərbaycan Respublikası Rəqəmsal İnkişaf və Nəqliyyat Nazirliyi',
                'short_name': 'RİNN',
                'description': 'Rəqəmsal texnologiyalar, informasiya cəmiyyəti və nəqliyyat',
                'address': 'Bakı şəhəri, Yasamal rayonu, Şərifzadə küçəsi 22',
                'phone': '+994 12 404 50 00',
                'email': 'info@mincom.gov.az',
                'website': 'https://mincom.gov.az',
                'is_active': True,
                'established_date': date(2019, 7, 15)
            }
        )

        # Departments
        dept_rid, _ = Department.objects.get_or_create(
            organization=org1,
            code='RID',
            defaults={
                'name': 'Rəqəmsal İnkişaf Departamenti',
                'description': 'Rəqəmsal transformasiya layihələrinin idarə edilməsi',
                'phone': '+994 12 404 50 10',
                'email': 'digital@mincom.gov.az',
                'location': 'Mərkəzi bina, 3-cü mərtəbə',
                'is_active': True
            }
        )

        dept_exs, _ = Department.objects.get_or_create(
            organization=org1,
            code='EXS',
            parent=dept_rid,
            defaults={
                'name': 'E-xidmətlər Şöbəsi',
                'description': 'Elektron xidmətlərin hazırlanması və idarə edilməsi',
                'phone': '+994 12 404 50 11',
                'email': 'eservices@mincom.gov.az',
                'location': 'Mərkəzi bina, 3-cü mərtəbə, otaq 310',
                'is_active': True
            }
        )

        dept_kts, _ = Department.objects.get_or_create(
            organization=org1,
            code='KTS',
            parent=dept_rid,
            defaults={
                'name': 'Kibertəhlükəsizlik Şöbəsi',
                'description': 'İnformasiya təhlükəsizliyi və kibertəhlükəsizlik',
                'phone': '+994 12 404 50 12',
                'email': 'cybersec@mincom.gov.az',
                'location': 'Mərkəzi bina, 2-ci mərtəbə',
                'is_active': True
            }
        )

        dept_irtm, _ = Department.objects.get_or_create(
            organization=org1,
            code='IRTM',
            defaults={
                'name': 'İnsan Resursları və Təlim Mərkəzi',
                'description': 'Kadr siyasəti və işçilərin inkişafı',
                'phone': '+994 12 404 50 20',
                'email': 'hr@mincom.gov.az',
                'location': 'Mərkəzi bina, 1-ci mərtəbə',
                'is_active': True
            }
        )

        self.stdout.write('  ✅ 1 təşkilat və 4 departament yaradıldı')

    def create_users(self):
        """Create demo users."""
        dept_rid = Department.objects.get(code='RID')
        dept_exs = Department.objects.get(code='EXS')
        dept_kts = Department.objects.get(code='KTS')
        dept_irtm = Department.objects.get(code='IRTM')

        # Admin user
        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@q360.gov.az',
                'first_name': 'Sistem',
                'last_name': 'Administrator',
                'role': 'superadmin',
                'is_superuser': True,
                'is_staff': True,
                'is_active': True,
                'employee_id': 'EMP001'
            }
        )
        if created:
            admin.set_password('password')
            admin.save()

        # Manager users
        rashad, created = User.objects.get_or_create(
            username='rashad.mammadov',
            defaults={
                'email': 'rashad.mammadov@mincom.gov.az',
                'first_name': 'Rəşad',
                'last_name': 'Məmmədov',
                'middle_name': 'Elçin',
                'role': 'admin',
                'department': dept_rid,
                'position': 'Departament direktoru',
                'is_staff': True,
                'is_active': True,
                'employee_id': 'EMP002'
            }
        )
        if created:
            rashad.set_password('password')
            rashad.save()

        leyla, created = User.objects.get_or_create(
            username='leyla.huseynova',
            defaults={
                'email': 'leyla.huseynova@mincom.gov.az',
                'first_name': 'Leyla',
                'last_name': 'Hüseynova',
                'middle_name': 'Vaqif',
                'role': 'manager',
                'department': dept_exs,
                'position': 'Şöbə müdiri',
                'supervisor': rashad,
                'is_active': True,
                'employee_id': 'EMP003'
            }
        )
        if created:
            leyla.set_password('password')
            leyla.save()

        # Employees
        murad, created = User.objects.get_or_create(
            username='murad.aliyev',
            defaults={
                'email': 'murad.aliyev@mincom.gov.az',
                'first_name': 'Murad',
                'last_name': 'Əliyev',
                'middle_name': 'Təbriz',
                'role': 'employee',
                'department': dept_exs,
                'position': 'Baş mütəxəssis',
                'supervisor': leyla,
                'is_active': True,
                'employee_id': 'EMP004'
            }
        )
        if created:
            murad.set_password('password')
            murad.save()

        self.stdout.write('  ✅ 4 istifadəçi yaradıldı (daha çoxu üçün create_demo_users command işlədin)')

    def create_competencies(self):
        """Create competencies and proficiency levels."""
        # Proficiency Levels
        basic, _ = ProficiencyLevel.objects.get_or_create(
            name='basic',
            defaults={
                'display_name': 'Əsas',
                'score_min': 0,
                'score_max': 25,
                'description': 'Əsas səviyyə - İlkin bilik və bacarıqlar'
            }
        )

        intermediate, _ = ProficiencyLevel.objects.get_or_create(
            name='intermediate',
            defaults={
                'display_name': 'Orta',
                'score_min': 25.01,
                'score_max': 50,
                'description': 'Orta səviyyə - Müstəqil iş apara bilir'
            }
        )

        # Competencies
        leadership, _ = Competency.objects.get_or_create(
            name='Rəhbərlik və Liderlik',
            defaults={
                'description': 'Komandaya rəhbərlik etmək, motivasiya yaratmaq və strateji qərarlar qəbul etmək',
                'is_active': True
            }
        )

        teamwork, _ = Competency.objects.get_or_create(
            name='Komanda İşi və Əməkdaşlıq',
            defaults={
                'description': 'Komanda ilə effektiv işləmək, koordinasiya və əməkdaşlıq bacarıqları',
                'is_active': True
            }
        )

        technical, _ = Competency.objects.get_or_create(
            name='Texniki Bilik (IT)',
            defaults={
                'description': 'İnformasiya texnologiyaları sahəsində texniki bilik və bacarıqlar',
                'is_active': True
            }
        )

        self.stdout.write('  ✅ 2 səviyyə və 3 kompetensiya yaradıldı')

    def create_evaluations(self):
        """Create evaluation structure."""
        cat1, _ = QuestionCategory.objects.get_or_create(
            name='Rəhbərlik və İdarəetmə',
            defaults={
                'description': 'Rəhbərlik, liderlik və komanda idarəetməsi bacarıqları',
                'order': 1,
                'is_active': True
            }
        )

        q1, _ = Question.objects.get_or_create(
            category=cat1,
            text='İşçi komandaya effektiv rəhbərlik edir və komanda üzvlərini motivasiya edir',
            defaults={
                'question_type': 'scale',
                'max_score': 5,
                'is_required': True,
                'order': 1,
                'is_active': True
            }
        )

        self.stdout.write('  ✅ 1 kateqoriya və 1 sual yaradıldı')

    def create_training(self):
        """Create training resources."""
        tech_comp = Competency.objects.get(name='Texniki Bilik (IT)')

        training1, _ = TrainingResource.objects.get_or_create(
            title='Python ilə Proqramlaşdırma - Əsaslar',
            defaults={
                'description': 'Python proqramlaşdırma dilinin əsasları',
                'type': 'course',
                'is_online': True,
                'delivery_method': 'online',
                'link': 'https://www.udemy.com/course/python-programming/',
                'difficulty_level': 'beginner',
                'duration_hours': 40,
                'language': 'İngilis',
                'provider': 'Udemy',
                'cost': 150,
                'is_active': True
            }
        )
        training1.required_competencies.add(tech_comp)

        self.stdout.write('  ✅ 1 təlim resursu yaradıldı')

    def create_development_plans(self):
        """Create development goals."""
        try:
            user = User.objects.get(username='murad.aliyev')
            manager = User.objects.get(username='leyla.huseynova')

            goal, _ = DevelopmentGoal.objects.get_or_create(
                user=user,
                title='Python proqramlaşdırma bacarıqlarını intermediate səviyyəyə çatdırmaq',
                defaults={
                    'description': 'Django framework-ü öyrənmək və real layihələrdə iştirak etmək',
                    'category': 'Texniki İnkişaf',
                    'status': 'active',
                    'target_date': date(2024, 5, 31),
                    'approved_by': manager,
                    'approved_at': timezone.now(),
                    'created_by': user
                }
            )

            self.stdout.write('  ✅ 1 inkişaf məqsədi yaradıldı')
        except User.DoesNotExist:
            self.stdout.write('  ⚠️ İstifadəçilər yoxdur, atlandı')

    def create_workforce_planning(self):
        """Create workforce planning data."""
        self.stdout.write('  ⏭️ Atlandı (optional)')

    def create_continuous_feedback(self):
        """Create feedback tags and sample feedbacks."""
        tag1, _ = FeedbackTag.objects.get_or_create(
            name='Komanda İşi',
            defaults={
                'description': 'Komanda ilə əməkdaşlıq və birlikdə iş',
                'icon': 'fa-users',
                'is_active': True
            }
        )

        self.stdout.write('  ✅ 1 feedback tag yaradıldı')

    def create_support(self):
        """Create support tickets."""
        self.stdout.write('  ⏭️ Atlandı (optional)')

    def finalize(self):
        """Final configurations."""
        self.stdout.write('  ✅ Konfiqurasiyalar tamamlandı')


