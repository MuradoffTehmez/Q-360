"""
Management command to create comprehensive demo data for testing.
Creates organizations, departments, users, campaigns, questions, and evaluations.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import datetime, timedelta
import random

from apps.departments.models import Organization, Department, Position
from apps.evaluations.models import (
    EvaluationCampaign, QuestionCategory, Question,
    EvaluationAssignment, Response, CampaignQuestion
)

User = get_user_model()


class Command(BaseCommand):
    help = 'Tam demo məlumat bazası yaradır (bütün modullar)'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('TAM DEMO MƏLUMAT BAZASI YARADILIR'))
        self.stdout.write(self.style.SUCCESS('='*60 + '\n'))

        # Step 1: Organizations and Departments
        self.stdout.write(self.style.WARNING('1️⃣  TƏŞKİLAT VƏ ŞÖBƏLƏR YARADILIR...'))
        org = self.create_organizations()
        departments = self.create_departments(org)
        positions = self.create_positions(org, departments)

        # Step 2: Users
        self.stdout.write(self.style.WARNING('\n2️⃣  İSTİFADƏÇİLƏR YARADILIR...'))
        users = self.create_users(departments, positions)

        # Step 3: Question Categories and Questions
        self.stdout.write(self.style.WARNING('\n3️⃣  SUAL KATEQORİYALARI VƏ SUALLAR YARADILIR...'))
        categories = self.create_question_categories()
        questions = self.create_questions(categories)

        # Step 4: Evaluation Campaigns
        self.stdout.write(self.style.WARNING('\n4️⃣  QİYMƏTLƏNDİRMƏ KAMPANİYALARI YARADILIR...'))
        campaigns = self.create_campaigns(users['admin'])

        # Step 5: Assign questions to campaigns
        self.stdout.write(self.style.WARNING('\n5️⃣  SUALLAR KAMPANİYALARA TƏYİN EDİLİR...'))
        self.assign_questions_to_campaigns(campaigns, questions)

        # Step 6: Create evaluation assignments
        self.stdout.write(self.style.WARNING('\n6️⃣  QİYMƏTLƏNDİRMƏ TAPŞIRIQLARI YARADILIR...'))
        self.create_evaluation_assignments(campaigns, users)

        # Step 7: Generate sample responses
        self.stdout.write(self.style.WARNING('\n7️⃣  NÜMUNƏ CAVABLAR YARADILIR...'))
        self.create_sample_responses()

        # Final summary
        self.print_summary(users)

    def create_organizations(self):
        """Create organization."""
        org, created = Organization.objects.get_or_create(
            code='GOV001',
            defaults={
                'name': 'Azərbaycan Dövlət Xidməti İdarəsi',
                'short_name': 'ADXI',
                'description': 'Dövlət qulluqçularının idarə edilməsi və qiymətləndirilməsi',
                'email': 'info@adxi.gov.az',
                'phone': '+994 12 555 55 55',
                'address': 'Bakı şəhəri, Nizami küçəsi 10'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'  ✓ Təşkilat: {org.name}'))
        return org

    def create_departments(self, org):
        """Create departments."""
        departments_data = [
            {'code': 'HR', 'name': 'İnsan Resursları Şöbəsi', 'description': 'Kadr idarəetməsi'},
            {'code': 'IT', 'name': 'İnformasiya Texnologiyaları Şöbəsi', 'description': 'Texniki dəstək və inkişaf'},
            {'code': 'FIN', 'name': 'Maliyyə Şöbəsi', 'description': 'Büdcə və maliyyə idarəetməsi'},
            {'code': 'LEGAL', 'name': 'Hüquq Şöbəsi', 'description': 'Hüquqi məsləhət və sənədləşmə'},
            {'code': 'PR', 'name': 'İctimaiyyətlə Əlaqələr Şöbəsi', 'description': 'PR və kommunikasiya'},
        ]

        departments = {}
        for dept_data in departments_data:
            dept, created = Department.objects.get_or_create(
                organization=org,
                code=dept_data['code'],
                defaults={
                    'name': dept_data['name'],
                    'description': dept_data['description']
                }
            )
            departments[dept_data['code']] = dept
            if created:
                self.stdout.write(f'  ✓ Şöbə: {dept.name}')

        return departments

    def create_positions(self, org, departments):
        """Create positions."""
        positions_data = [
            {'code': 'DIR', 'title': 'Direktor', 'level': 1, 'dept': 'HR'},
            {'code': 'HRMGR', 'title': 'HR Meneceri', 'level': 2, 'dept': 'HR'},
            {'code': 'HRSPEC', 'title': 'HR Mütəxəssisi', 'level': 3, 'dept': 'HR'},
            {'code': 'ITMGR', 'title': 'IT Meneceri', 'level': 2, 'dept': 'IT'},
            {'code': 'DEVELOPER', 'title': 'Proqramçı', 'level': 3, 'dept': 'IT'},
            {'code': 'SYSADMIN', 'title': 'Sistem Administratoru', 'level': 3, 'dept': 'IT'},
            {'code': 'FINMGR', 'title': 'Maliyyə Meneceri', 'level': 2, 'dept': 'FIN'},
            {'code': 'ACCOUNTANT', 'title': 'Mühasib', 'level': 3, 'dept': 'FIN'},
            {'code': 'LAWYER', 'title': 'Hüquqşünas', 'level': 3, 'dept': 'LEGAL'},
            {'code': 'PRSPEC', 'title': 'PR Mütəxəssisi', 'level': 3, 'dept': 'PR'},
        ]

        positions = {}
        for pos_data in positions_data:
            pos, created = Position.objects.get_or_create(
                organization=org,
                code=pos_data['code'],
                defaults={
                    'title': pos_data['title'],
                    'level': pos_data['level'],
                    'department': departments.get(pos_data['dept'])
                }
            )
            positions[pos_data['code']] = pos
            if created:
                self.stdout.write(f'  ✓ Vəzifə: {pos.title}')

        return positions

    def create_users(self, departments, positions):
        """Create users with various roles."""
        users = {}

        # Admin user
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@q360.az',
                password='admin123',
                first_name='Admin',
                last_name='Sistemi',
                role='superadmin',
                department=departments['HR'],
                position='Sistem Administratoru'
            )
            users['admin'] = admin
            self.stdout.write(self.style.SUCCESS('  ✓ Admin: admin / admin123'))
        else:
            users['admin'] = User.objects.get(username='admin')

        # Managers
        managers_data = [
            {'username': 'rashad', 'first_name': 'Rəşad', 'last_name': 'Məmmədov',
             'dept': 'HR', 'position': 'HR Meneceri'},
            {'username': 'elvin', 'first_name': 'Elvin', 'last_name': 'Quliyev',
             'dept': 'IT', 'position': 'IT Meneceri'},
            {'username': 'leyla', 'first_name': 'Leyla', 'last_name': 'Həsənova',
             'dept': 'FIN', 'position': 'Maliyyə Meneceri'},
        ]

        users['managers'] = []
        for mgr in managers_data:
            if not User.objects.filter(username=mgr['username']).exists():
                user = User.objects.create_user(
                    username=mgr['username'],
                    email=f"{mgr['username']}@q360.az",
                    password='manager123',
                    first_name=mgr['first_name'],
                    last_name=mgr['last_name'],
                    role='manager',
                    department=departments[mgr['dept']],
                    position=mgr['position']
                )
                users['managers'].append(user)
                self.stdout.write(f"  ✓ Menecer: {mgr['username']} / manager123")
            else:
                users['managers'].append(User.objects.get(username=mgr['username']))

        # Employees
        employees_data = [
            {'username': 'aynur', 'first_name': 'Aynur', 'last_name': 'Əliyeva',
             'dept': 'HR', 'position': 'HR Mütəxəssisi'},
            {'username': 'kamran', 'first_name': 'Kamran', 'last_name': 'Əliyev',
             'dept': 'HR', 'position': 'HR Mütəxəssisi'},
            {'username': 'elchin', 'first_name': 'Elçin', 'last_name': 'Həsənov',
             'dept': 'IT', 'position': 'Proqramçı'},
            {'username': 'gunel', 'first_name': 'Günəl', 'last_name': 'İsmayılova',
             'dept': 'IT', 'position': 'Proqramçı'},
            {'username': 'nigar', 'first_name': 'Nigar', 'last_name': 'Məmmədova',
             'dept': 'IT', 'position': 'Sistem Administratoru'},
            {'username': 'farid', 'first_name': 'Farid', 'last_name': 'Abdullayev',
             'dept': 'FIN', 'position': 'Mühasib'},
            {'username': 'sevinc', 'first_name': 'Sevinc', 'last_name': 'Qasımova',
             'dept': 'FIN', 'position': 'Mühasib'},
            {'username': 'tural', 'first_name': 'Tural', 'last_name': 'Cəfərov',
             'dept': 'LEGAL', 'position': 'Hüquqşünas'},
            {'username': 'aysel', 'first_name': 'Aysel', 'last_name': 'Rəhimova',
             'dept': 'PR', 'position': 'PR Mütəxəssisi'},
            {'username': 'murad', 'first_name': 'Murad', 'last_name': 'Süleymanov',
             'dept': 'PR', 'position': 'PR Mütəxəssisi'},
        ]

        users['employees'] = []
        for emp in employees_data:
            if not User.objects.filter(username=emp['username']).exists():
                user = User.objects.create_user(
                    username=emp['username'],
                    email=f"{emp['username']}@q360.az",
                    password='employee123',
                    first_name=emp['first_name'],
                    last_name=emp['last_name'],
                    role='employee',
                    department=departments[emp['dept']],
                    position=emp['position']
                )
                users['employees'].append(user)
                self.stdout.write(f"  ✓ İşçi: {emp['username']} / employee123")
            else:
                users['employees'].append(User.objects.get(username=emp['username']))

        # Set supervisors
        if users['managers']:
            for i, manager in enumerate(users['managers']):
                manager.supervisor = users['admin']
                manager.save()

            # Assign employees to managers
            for emp in users['employees']:
                if emp.department.code == 'HR':
                    emp.supervisor = users['managers'][0]  # Rashad
                elif emp.department.code == 'IT':
                    emp.supervisor = users['managers'][1]  # Elvin
                elif emp.department.code == 'FIN':
                    emp.supervisor = users['managers'][2]  # Leyla
                else:
                    emp.supervisor = users['admin']
                emp.save()

        return users

    def create_question_categories(self):
        """Create question categories."""
        categories_data = [
            {'name': 'Liderlik', 'description': 'Liderlik və komanda idarəetməsi bacarıqları', 'order': 1},
            {'name': 'Kommunikasiya', 'description': 'Ünsiyyət və əməkdaşlıq bacarıqları', 'order': 2},
            {'name': 'Peşəkarlıq', 'description': 'Peşəkar bilik və təcrübə', 'order': 3},
            {'name': 'Problem Həlli', 'description': 'Analitik düşüncə və problem həlli', 'order': 4},
            {'name': 'İş Nəticələri', 'description': 'Tapşırıqların yerinə yetirilməsi və nəticə', 'order': 5},
        ]

        categories = []
        for cat_data in categories_data:
            cat, created = QuestionCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'description': cat_data['description'],
                    'order': cat_data['order']
                }
            )
            categories.append(cat)
            if created:
                self.stdout.write(f"  ✓ Kateqoriya: {cat.name}")

        return categories

    def create_questions(self, categories):
        """Create evaluation questions."""
        questions_data = [
            # Liderlik
            {'text': 'Komanda üzvlərini motivasiya etmək və rəhbərlik etmək bacarığı', 'category': 0, 'type': 'scale'},
            {'text': 'Strateji düşüncə və qərar qəbul etmə bacarığı', 'category': 0, 'type': 'scale'},

            # Kommunikasiya
            {'text': 'Aydın və effektiv ünsiyyət qurma bacarığı', 'category': 1, 'type': 'scale'},
            {'text': 'Komanda ilə əməkdaşlıq və koordinasiya', 'category': 1, 'type': 'scale'},
            {'text': 'Dinləmə və başqalarının fikirlərini qəbul etmə bacarığı', 'category': 1, 'type': 'scale'},

            # Peşəkarlıq
            {'text': 'Peşəkar bilik və bacarıqların səviyyəsi', 'category': 2, 'type': 'scale'},
            {'text': 'İşə məsuliyyətli və ciddi yanaşma', 'category': 2, 'type': 'scale'},
            {'text': 'Davamlı öyrənmə və inkişaf istəyi', 'category': 2, 'type': 'scale'},

            # Problem Həlli
            {'text': 'Problemləri təhlil edib həll yolları tapmaq bacarığı', 'category': 3, 'type': 'scale'},
            {'text': 'Yaradıcı və innovativ yanaşma', 'category': 3, 'type': 'scale'},

            # İş Nəticələri
            {'text': 'Tapşırıqların vaxtında və keyfiyyətli yerinə yetirilməsi', 'category': 4, 'type': 'scale'},
            {'text': 'Məhsuldarlıq və effektivlik', 'category': 4, 'type': 'scale'},

            # Text questions
            {'text': 'Bu şəxsin ən güclü tərəfləri hansılardır?', 'category': 0, 'type': 'text'},
            {'text': 'Hansı sahələrdə inkişaf etməlidir?', 'category': 0, 'type': 'text'},
            {'text': 'Əlavə rəy və təkliflər', 'category': 4, 'type': 'text', 'required': False},
        ]

        questions = []
        for q_data in questions_data:
            q, created = Question.objects.get_or_create(
                text=q_data['text'],
                defaults={
                    'category': categories[q_data['category']],
                    'question_type': q_data['type'],
                    'is_required': q_data.get('required', True),
                    'order': len(questions)
                }
            )
            questions.append(q)
            if created:
                self.stdout.write(f"  ✓ Sual: {q.text[:50]}...")

        return questions

    def create_campaigns(self, creator):
        """Create evaluation campaigns."""
        campaigns_data = [
            {
                'title': '2024 - İllik Performans Qiymətləndirməsi',
                'description': '2024-cü il illik performans qiymətləndirmə kampaniyası',
                'start_date': datetime.now().date() - timedelta(days=60),
                'end_date': datetime.now().date() + timedelta(days=30),
                'status': 'active'
            },
            {
                'title': '2024 - Rüblük Qiymətləndirmə (Q3)',
                'description': '3-cü rüb üzrə qiymətləndirmə',
                'start_date': datetime.now().date() - timedelta(days=120),
                'end_date': datetime.now().date() - timedelta(days=30),
                'status': 'completed'
            },
        ]

        campaigns = []
        for camp_data in campaigns_data:
            camp, created = EvaluationCampaign.objects.get_or_create(
                title=camp_data['title'],
                defaults={
                    'description': camp_data['description'],
                    'start_date': camp_data['start_date'],
                    'end_date': camp_data['end_date'],
                    'status': camp_data['status'],
                    'created_by': creator,
                    'allow_self_evaluation': True,
                    'is_anonymous': True
                }
            )
            campaigns.append(camp)
            if created:
                self.stdout.write(f"  ✓ Kampaniya: {camp.title}")

        return campaigns

    def assign_questions_to_campaigns(self, campaigns, questions):
        """Assign questions to campaigns."""
        for campaign in campaigns:
            for i, question in enumerate(questions):
                CampaignQuestion.objects.get_or_create(
                    campaign=campaign,
                    question=question,
                    defaults={'order': i}
                )
            self.stdout.write(f"  ✓ {len(questions)} sual təyin edildi: {campaign.title}")

    def create_evaluation_assignments(self, campaigns, users):
        """Create evaluation assignments."""
        all_users = [users['admin']] + users['managers'] + users['employees']
        active_campaign = campaigns[0]  # Use active campaign

        count = 0
        for evaluatee in all_users:
            # Self evaluation
            EvaluationAssignment.objects.get_or_create(
                campaign=active_campaign,
                evaluator=evaluatee,
                evaluatee=evaluatee,
                defaults={'relationship': 'self', 'status': 'pending'}
            )
            count += 1

            # Supervisor evaluation
            if evaluatee.supervisor:
                EvaluationAssignment.objects.get_or_create(
                    campaign=active_campaign,
                    evaluator=evaluatee.supervisor,
                    evaluatee=evaluatee,
                    defaults={'relationship': 'supervisor', 'status': 'pending'}
                )
                count += 1

            # Peer evaluations (2-3 random peers from same department)
            peers = [u for u in all_users
                    if u.department == evaluatee.department and u != evaluatee][:3]
            for peer in peers:
                EvaluationAssignment.objects.get_or_create(
                    campaign=active_campaign,
                    evaluator=peer,
                    evaluatee=evaluatee,
                    defaults={'relationship': 'peer', 'status': 'pending'}
                )
                count += 1

        self.stdout.write(f"  ✓ {count} tapşırıq yaradıldı")

    def create_sample_responses(self):
        """Create sample responses for some assignments."""
        assignments = EvaluationAssignment.objects.filter(status='pending')[:10]

        for assignment in assignments:
            questions = assignment.campaign.campaign_questions.all()

            for cq in questions:
                question = cq.question

                if question.question_type == 'scale':
                    score = random.randint(3, 5)
                    Response.objects.get_or_create(
                        assignment=assignment,
                        question=question,
                        defaults={'score': score}
                    )
                elif question.question_type == 'text':
                    texts = [
                        'Çox peşəkar və məsuliyyətli yanaşma nümayiş etdirir.',
                        'Komanda ilə əla əməkdaşlıq edir, həmişə köməyə hazırdır.',
                        'Təcrübəli və biliklidir, problemləri tez həll edir.',
                    ]
                    Response.objects.get_or_create(
                        assignment=assignment,
                        question=question,
                        defaults={'text_answer': random.choice(texts)}
                    )

            # Mark some as completed
            if random.random() > 0.5:
                assignment.status = 'completed'
                assignment.completed_at = timezone.now()
                assignment.save()

        self.stdout.write(f"  ✓ {len(assignments)} tapşırıq üçün nümunə cavablar yaradıldı")

    def print_summary(self, users):
        """Print summary of created data."""
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('✅ DEMO MƏLUMAT BAZASI UĞURLA YARADILDI!'))
        self.stdout.write(self.style.SUCCESS('='*60))

        self.stdout.write(self.style.WARNING('\n📊 YARADILMIŞ MƏLUMATLAR:'))
        self.stdout.write(f"  • Təşkilatlar: {Organization.objects.count()}")
        self.stdout.write(f"  • Şöbələr: {Department.objects.count()}")
        self.stdout.write(f"  • Vəzifələr: {Position.objects.count()}")
        self.stdout.write(f"  • İstifadəçilər: {User.objects.count()}")
        self.stdout.write(f"  • Sual Kateqoriyaları: {QuestionCategory.objects.count()}")
        self.stdout.write(f"  • Suallar: {Question.objects.count()}")
        self.stdout.write(f"  • Kampaniyalar: {EvaluationCampaign.objects.count()}")
        self.stdout.write(f"  • Qiymətləndirmə Tapşırıqları: {EvaluationAssignment.objects.count()}")
        self.stdout.write(f"  • Cavablar: {Response.objects.count()}")

        self.stdout.write(self.style.WARNING('\n🔐 GİRİŞ MƏLUMATLARI:'))
        self.stdout.write(self.style.SUCCESS('  Admin:'))
        self.stdout.write('    Username: admin')
        self.stdout.write('    Password: admin123')

        self.stdout.write(self.style.SUCCESS('  Menecerlər:'))
        self.stdout.write('    Username: rashad, elvin, leyla')
        self.stdout.write('    Password: manager123')

        self.stdout.write(self.style.SUCCESS('  İşçilər:'))
        self.stdout.write('    Username: aynur, kamran, elchin, gunel, nigar, farid, sevinc, tural, aysel, murad')
        self.stdout.write('    Password: employee123')

        self.stdout.write(self.style.WARNING('\n🌐 SAYT:'))
        self.stdout.write('    http://127.0.0.1:8000/')
        self.stdout.write('    http://127.0.0.1:8000/admin/')
        self.stdout.write('')
