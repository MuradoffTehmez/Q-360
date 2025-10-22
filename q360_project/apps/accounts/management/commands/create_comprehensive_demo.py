"""
Management command to create comprehensive demo data for ALL modules.
This creates a complete, realistic dataset covering every aspect of the Q360 system.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import datetime, timedelta, date
from decimal import Decimal
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Tam və ətraflı demo məlumat bazası yaradır (BÜTÜN MODULLAR)'

    def __init__(self):
        super().__init__()
        self.users = {}
        self.departments = {}
        self.positions = {}
        self.org = None
        self.campaigns = []
        self.questions = []
        self.competencies = []
        self.leave_types = []
        self.training_resources = []

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('\n' + '='*80))
        self.stdout.write(self.style.SUCCESS('🚀 TAM ƏHATƏLI DEMO MƏLUMAT BAZASI YARADILIR'))
        self.stdout.write(self.style.SUCCESS('='*80 + '\n'))

        # Core structure
        self.create_organizations_and_departments()
        self.create_users()

        # Evaluations
        self.create_evaluations_data()

        # Development & Learning
        self.create_development_data()
        self.create_competencies_data()
        self.create_training_data()

        # Recruitment & Compensation
        self.create_recruitment_data()
        self.create_compensation_data()

        # Attendance & Leave
        self.create_leave_attendance_data()

        # Feedback & Communication
        self.create_feedback_data()
        self.create_notifications_data()

        # Workforce Planning
        self.create_workforce_planning_data()

        # Onboarding
        self.create_onboarding_data()

        # Support & Audit
        self.create_support_data()
        self.create_audit_data()

        # Final summary
        self.print_summary()

    def create_organizations_and_departments(self):
        """Step 1: Organizations and Departments"""
        from apps.departments.models import Organization, Department, Position

        self.stdout.write(self.style.WARNING('\n📋 1/14: TƏŞKİLAT VƏ ŞÖBƏLƏR'))

        self.org, created = Organization.objects.get_or_create(
            code='GOV001',
            defaults={
                'name': 'Azərbaycan Dövlət Xidməti İdarəsi',
                'short_name': 'ADXI',
                'description': 'Dövlət qulluqçularının idarə edilməsi və inkişafı',
                'email': 'info@adxi.gov.az',
                'phone': '+994 12 555 55 55',
                'address': 'Bakı şəhəri, Nizami küçəsi 10',
                'established_date': date(2010, 1, 1)
            }
        )

        # Departments
        dept_data = [
            {'code': 'HR', 'name': 'İnsan Resursları Departamenti', 'parent': None},
            {'code': 'HR-REC', 'name': 'İşəgötürmə Şöbəsi', 'parent': 'HR'},
            {'code': 'HR-DEV', 'name': 'İnkişaf və Təlim Şöbəsi', 'parent': 'HR'},
            {'code': 'IT', 'name': 'İnformasiya Texnologiyaları Departamenti', 'parent': None},
            {'code': 'IT-DEV', 'name': 'Proqram Təminatı Şöbəsi', 'parent': 'IT'},
            {'code': 'IT-OPS', 'name': 'Sistem Administrasiyası Şöbəsi', 'parent': 'IT'},
            {'code': 'FIN', 'name': 'Maliyyə Departamenti', 'parent': None},
            {'code': 'FIN-ACC', 'name': 'Mühasibatlıq Şöbəsi', 'parent': 'FIN'},
            {'code': 'LEGAL', 'name': 'Hüquq Departamenti', 'parent': None},
            {'code': 'PR', 'name': 'İctimaiyyətlə Əlaqələr Departamenti', 'parent': None},
        ]

        for dept in dept_data:
            parent = self.departments.get(dept['parent']) if dept['parent'] else None
            d, _ = Department.objects.get_or_create(
                organization=self.org,
                code=dept['code'],
                defaults={'name': dept['name'], 'parent': parent}
            )
            self.departments[dept['code']] = d

        # Positions
        positions_data = [
            {'code': 'CEO', 'title': 'İcraçı Direktor', 'level': 1, 'dept': 'HR'},
            {'code': 'DIR-HR', 'title': 'HR Direktoru', 'level': 1, 'dept': 'HR'},
            {'code': 'DIR-IT', 'title': 'IT Direktoru', 'level': 1, 'dept': 'IT'},
            {'code': 'DIR-FIN', 'title': 'Maliyyə Direktoru', 'level': 1, 'dept': 'FIN'},
            {'code': 'MGR-HR', 'title': 'HR Meneceri', 'level': 2, 'dept': 'HR'},
            {'code': 'MGR-IT', 'title': 'IT Meneceri', 'level': 2, 'dept': 'IT'},
            {'code': 'MGR-FIN', 'title': 'Maliyyə Meneceri', 'level': 2, 'dept': 'FIN'},
            {'code': 'SPEC-HR', 'title': 'HR Mütəxəssisi', 'level': 3, 'dept': 'HR'},
            {'code': 'DEV', 'title': 'Proqramçı', 'level': 3, 'dept': 'IT'},
            {'code': 'SYSADM', 'title': 'Sistem Administratoru', 'level': 3, 'dept': 'IT'},
            {'code': 'ACC', 'title': 'Mühasib', 'level': 3, 'dept': 'FIN'},
            {'code': 'LAW', 'title': 'Hüquqşünas', 'level': 3, 'dept': 'LEGAL'},
            {'code': 'PR-SPEC', 'title': 'PR Mütəxəssisi', 'level': 3, 'dept': 'PR'},
        ]

        for pos in positions_data:
            p, _ = Position.objects.get_or_create(
                organization=self.org,
                code=pos['code'],
                defaults={
                    'title': pos['title'],
                    'level': pos['level'],
                    'department': self.departments.get(pos['dept'])
                }
            )
            self.positions[pos['code']] = p

        self.stdout.write(f'  ✓ {len(self.departments)} şöbə, {len(self.positions)} vəzifə')

    def create_users(self):
        """Step 2: Users with profiles"""
        self.stdout.write(self.style.WARNING('\n👥 2/14: İSTİFADƏÇİLƏR VƏ PROFİLLƏR'))

        # Admin
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@q360.az',
                password='admin123',
                first_name='Admin',
                last_name='Sistemi',
                role='superadmin',
                department=self.departments['HR'],
                position='Sistem Administratoru'
            )
            self.users['admin'] = admin
        else:
            self.users['admin'] = User.objects.get(username='admin')

        # Directors
        directors = [
            {'username': 'kamran', 'first': 'Kamran', 'last': 'Məmmədov', 'dept': 'HR', 'pos': 'DIR-HR'},
            {'username': 'elvin', 'first': 'Elvin', 'last': 'Quliyev', 'dept': 'IT', 'pos': 'DIR-IT'},
            {'username': 'leyla', 'first': 'Leyla', 'last': 'Həsənova', 'dept': 'FIN', 'pos': 'DIR-FIN'},
        ]

        self.users['directors'] = []
        for d in directors:
            user, _ = User.objects.get_or_create(
                username=d['username'],
                defaults={
                    'email': f"{d['username']}@q360.az",
                    'password': 'pbkdf2_sha256$600000$test$hash',
                    'first_name': d['first'],
                    'last_name': d['last'],
                    'role': 'admin',
                    'department': self.departments[d['dept']],
                    'position': self.positions[d['pos']].title,
                    'supervisor': self.users['admin']
                }
            )
            user.set_password('director123')
            user.save()
            self.users['directors'].append(user)

        # Managers (15)
        managers_data = [
            {'username': 'rashad', 'first': 'Rəşad', 'last': 'Əliyev', 'dept': 'HR-REC'},
            {'username': 'gunel', 'first': 'Günəl', 'last': 'İsmayılova', 'dept': 'HR-DEV'},
            {'username': 'tural', 'first': 'Tural', 'last': 'Cəfərov', 'dept': 'IT-DEV'},
            {'username': 'nigar', 'first': 'Nigar', 'last': 'Məmmədova', 'dept': 'IT-OPS'},
            {'username': 'farid', 'first': 'Farid', 'last': 'Abdullayev', 'dept': 'FIN-ACC'},
        ]

        self.users['managers'] = []
        for m in managers_data:
            sup = next((d for d in self.users['directors'] if d.department.code == m['dept'][:m['dept'].find('-') if '-' in m['dept'] else len(m['dept'])]), self.users['admin'])
            user, _ = User.objects.get_or_create(
                username=m['username'],
                defaults={
                    'email': f"{m['username']}@q360.az",
                    'first_name': m['first'],
                    'last_name': m['last'],
                    'role': 'manager',
                    'department': self.departments[m['dept']],
                    'position': 'Menecer',
                    'supervisor': sup
                }
            )
            user.set_password('manager123')
            user.save()
            self.users['managers'].append(user)

        # Employees (30)
        employees_data = [
            {'username': f'emp{i:02d}', 'first': f'İşçi{i}', 'last': f'Soyad{i}',
             'dept': random.choice(['HR-REC', 'HR-DEV', 'IT-DEV', 'IT-OPS', 'FIN-ACC', 'LEGAL', 'PR'])}
            for i in range(1, 31)
        ]

        self.users['employees'] = []
        for e in employees_data:
            sup = random.choice(self.users['managers'])
            user, _ = User.objects.get_or_create(
                username=e['username'],
                defaults={
                    'email': f"{e['username']}@q360.az",
                    'first_name': e['first'],
                    'last_name': e['last'],
                    'role': 'employee',
                    'department': self.departments[e['dept']],
                    'position': 'Mütəxəssis',
                    'supervisor': sup
                }
            )
            user.set_password('employee123')
            user.save()
            self.users['employees'].append(user)

        # Create profiles
        from apps.accounts.models import Profile
        all_users = [self.users['admin']] + self.users['directors'] + self.users['managers'] + self.users['employees']
        for user in all_users:
            Profile.objects.get_or_create(
                user=user,
                defaults={
                    'date_of_birth': date(1985, 1, 1) + timedelta(days=random.randint(0, 7300)),
                    'hire_date': date(2018, 1, 1) + timedelta(days=random.randint(0, 2000)),
                    'language_preference': 'az',
                    'email_notifications': True
                }
            )

        self.stdout.write(f'  ✓ {len(all_users)} istifadəçi (3 direktor, 5 menecer, 30 işçi)')

    def create_evaluations_data(self):
        """Step 3: Evaluation campaigns, questions, assignments, responses"""
        from apps.evaluations.models import (
            EvaluationCampaign, QuestionCategory, Question,
            CampaignQuestion, EvaluationAssignment, Response
        )

        self.stdout.write(self.style.WARNING('\n📊 3/14: QİYMƏTLƏNDİRMƏ SİSTEMİ'))

        # Categories
        categories_data = [
            {'name': 'Liderlik', 'desc': 'Liderlik bacarıqları', 'order': 1},
            {'name': 'Kommunikasiya', 'desc': 'Ünsiyyət bacarıqları', 'order': 2},
            {'name': 'Peşəkarlıq', 'desc': 'Peşəkar bilik', 'order': 3},
            {'name': 'Problem Həlli', 'desc': 'Analitik düşüncə', 'order': 4},
            {'name': 'Nəticə', 'desc': 'İş nəticələri', 'order': 5},
        ]

        categories = []
        for cat in categories_data:
            c, _ = QuestionCategory.objects.get_or_create(
                name=cat['name'],
                defaults={'description': cat['desc'], 'order': cat['order']}
            )
            categories.append(c)

        # Questions
        questions_data = [
            {'text': 'Komanda üzvlərini motivasiya etmək bacarığı', 'cat': 0, 'type': 'scale'},
            {'text': 'Strateji düşüncə və qərar qəbul etmə', 'cat': 0, 'type': 'scale'},
            {'text': 'Aydın və effektiv ünsiyyət qurma', 'cat': 1, 'type': 'scale'},
            {'text': 'Komanda ilə əməkdaşlıq', 'cat': 1, 'type': 'scale'},
            {'text': 'Dinləmə və fikirləri qəbul etmə', 'cat': 1, 'type': 'scale'},
            {'text': 'Peşəkar bilik və bacarıqlar', 'cat': 2, 'type': 'scale'},
            {'text': 'Məsuliyyətli yanaşma', 'cat': 2, 'type': 'scale'},
            {'text': 'Davamlı öyrənmə istəyi', 'cat': 2, 'type': 'scale'},
            {'text': 'Problemləri həll etmək bacarığı', 'cat': 3, 'type': 'scale'},
            {'text': 'Yaradıcı və innovativ yanaşma', 'cat': 3, 'type': 'scale'},
            {'text': 'Tapşırıqların vaxtında yerinə yetirilməsi', 'cat': 4, 'type': 'scale'},
            {'text': 'Məhsuldarlıq və effektivlik', 'cat': 4, 'type': 'scale'},
            {'text': 'Ən güclü tərəfləri hansılardır?', 'cat': 0, 'type': 'text'},
            {'text': 'Hansı sahələrdə inkişaf etməlidir?', 'cat': 0, 'type': 'text'},
            {'text': 'Əlavə rəy və təkliflər', 'cat': 4, 'type': 'text', 'required': False},
        ]

        for q_data in questions_data:
            q, _ = Question.objects.get_or_create(
                text=q_data['text'],
                defaults={
                    'category': categories[q_data['cat']],
                    'question_type': q_data['type'],
                    'is_required': q_data.get('required', True),
                    'order': len(self.questions)
                }
            )
            self.questions.append(q)

        # Campaigns
        campaigns_data = [
            {
                'title': '2024 - İllik Performans Qiymətləndirməsi',
                'desc': '2024-cü il illik qiymətləndirmə',
                'start': date.today() - timedelta(days=60),
                'end': date.today() + timedelta(days=30),
                'status': 'active'
            },
            {
                'title': '2024 - Rüblük Qiymətləndirmə (Q3)',
                'desc': '3-cü rüb qiymətləndirməsi',
                'start': date.today() - timedelta(days=120),
                'end': date.today() - timedelta(days=30),
                'status': 'completed'
            },
        ]

        for camp in campaigns_data:
            c, _ = EvaluationCampaign.objects.get_or_create(
                title=camp['title'],
                defaults={
                    'description': camp['desc'],
                    'start_date': camp['start'],
                    'end_date': camp['end'],
                    'status': camp['status'],
                    'created_by': self.users['admin'],
                    'allow_self_evaluation': True,
                    'is_anonymous': False
                }
            )
            self.campaigns.append(c)

            # Assign questions
            for i, question in enumerate(self.questions):
                CampaignQuestion.objects.get_or_create(
                    campaign=c,
                    question=question,
                    defaults={'order': i}
                )

        # Assignments and responses
        all_users = self.users['directors'] + self.users['managers'] + self.users['employees']
        active_campaign = self.campaigns[0]

        assignment_count = 0
        response_count = 0

        for evaluatee in all_users[:20]:  # Limit to 20 users for demo
            # Self evaluation
            assign, created = EvaluationAssignment.objects.get_or_create(
                campaign=active_campaign,
                evaluator=evaluatee,
                evaluatee=evaluatee,
                defaults={'relationship': 'self', 'status': random.choice(['pending', 'completed'])}
            )
            if created:
                assignment_count += 1

            # Supervisor evaluation
            if evaluatee.supervisor:
                assign, created = EvaluationAssignment.objects.get_or_create(
                    campaign=active_campaign,
                    evaluator=evaluatee.supervisor,
                    evaluatee=evaluatee,
                    defaults={'relationship': 'supervisor', 'status': random.choice(['pending', 'completed'])}
                )
                if created:
                    assignment_count += 1

            # Peer evaluations
            peers = [u for u in all_users if u.department == evaluatee.department and u != evaluatee][:2]
            for peer in peers:
                assign, created = EvaluationAssignment.objects.get_or_create(
                    campaign=active_campaign,
                    evaluator=peer,
                    evaluatee=evaluatee,
                    defaults={'relationship': 'peer', 'status': random.choice(['pending', 'in_progress', 'completed'])}
                )
                if created:
                    assignment_count += 1

                # Create responses for completed assignments
                if assign.status == 'completed':
                    for question in self.questions:
                        if question.question_type == 'scale':
                            Response.objects.get_or_create(
                                assignment=assign,
                                question=question,
                                defaults={'score': random.randint(3, 5)}
                            )
                            response_count += 1
                        elif question.question_type == 'text':
                            comments = [
                                'Çox yaxşı işləyir və komanda ilə əla əməkdaşlıq edir.',
                                'Peşəkar yanaşması və problemləri həll etmək bacarığı yüksəkdir.',
                                'Daha çox təşəbbüskarlıq göstərməlidir.',
                            ]
                            Response.objects.get_or_create(
                                assignment=assign,
                                question=question,
                                defaults={'text_answer': random.choice(comments)}
                            )
                            response_count += 1

        self.stdout.write(f'  ✓ {len(self.campaigns)} kampaniya, {assignment_count} tapşırıq, {response_count} cavab')

    def create_development_data(self):
        """Step 4: Development goals, OKRs"""
        from apps.development_plans.models import DevelopmentGoal, StrategicObjective, ProgressLog

        self.stdout.write(self.style.WARNING('\n🎯 4/14: İNKİŞAF PLANLARI VƏ MƏQSƏDLƏR'))

        # Strategic objectives
        obj, _ = StrategicObjective.objects.get_or_create(
            title='2024 - Korporativ İnkişaf',
            defaults={
                'description': 'İşçilərin peşəkar inkişafı',
                'owner': self.users['admin'],
                'fiscal_year': 2024,
                'quarter': 'annual',
                'start_date': date(2024, 1, 1),
                'end_date': date(2024, 12, 31),
                'status': 'active'
            }
        )

        # Goals
        goal_count = 0
        for user in self.users['managers'] + self.users['employees'][:10]:
            goal, created = DevelopmentGoal.objects.get_or_create(
                user=user,
                title=f'{user.get_full_name()} - 2024 İnkişaf Məqsədi',
                defaults={
                    'description': 'Peşəkar bacarıqların inkişafı və performansın artırılması',
                    'category': 'professional',
                    'goal_level': 'individual',
                    'target_date': date(2024, 12, 31),
                    'status': random.choice(['active', 'pending_approval', 'completed']),
                    'progress_percentage': random.randint(20, 90),
                    'created_by': user
                }
            )
            if created:
                goal_count += 1

                # Progress logs
                for _ in range(random.randint(1, 3)):
                    ProgressLog.objects.get_or_create(
                        goal=goal,
                        defaults={
                            'note': 'Məqsəd üzrə irəliləyiş qeyd edildi',
                            'progress_percentage': random.randint(10, 100),
                            'logged_by': user
                        }
                    )

        self.stdout.write(f'  ✓ 1 strateji məqsəd, {goal_count} fərdi inkişaf məqsədi')

    def create_competencies_data(self):
        """Step 5: Competencies and user skills"""
        from apps.competencies.models import Competency, ProficiencyLevel, UserSkill

        self.stdout.write(self.style.WARNING('\n🌟 5/14: KOMPETENSİYALAR VƏ BACARIQLAR'))

        # Proficiency levels
        levels_data = [
            {'name': 'basic', 'display': 'Əsas', 'min': 0, 'max': 30},
            {'name': 'intermediate', 'display': 'Orta', 'min': 31, 'max': 60},
            {'name': 'advanced', 'display': 'Yüksək', 'min': 61, 'max': 85},
            {'name': 'expert', 'display': 'Ekspert', 'min': 86, 'max': 100},
        ]

        levels = {}
        for lvl in levels_data:
            l, _ = ProficiencyLevel.objects.get_or_create(
                name=lvl['name'],
                defaults={
                    'display_name': lvl['display'],
                    'score_min': lvl['min'],
                    'score_max': lvl['max']
                }
            )
            levels[lvl['name']] = l

        # Competencies
        comp_data = [
            'Liderlik', 'Kommunikasiya', 'Problem həlli', 'Komanda işi',
            'Proqramlaşdırma', 'Data Analizi', 'Layihə idarəetməsi',
            'Strateji düşüncə', 'Müştəri xidməti', 'Maliyyə analizi'
        ]

        for comp_name in comp_data:
            c, _ = Competency.objects.get_or_create(
                name=comp_name,
                defaults={'description': f'{comp_name} bacarıqları'}
            )
            self.competencies.append(c)

        # User skills
        skill_count = 0
        all_users = self.users['managers'] + self.users['employees'][:15]
        for user in all_users:
            # Assign 3-5 random competencies
            user_comps = random.sample(self.competencies, k=random.randint(3, 5))
            for comp in user_comps:
                score = random.randint(40, 95)
                level = levels['basic']
                if score > 85:
                    level = levels['expert']
                elif score > 60:
                    level = levels['advanced']
                elif score > 30:
                    level = levels['intermediate']

                UserSkill.objects.get_or_create(
                    user=user,
                    competency=comp,
                    defaults={
                        'level': level,
                        'current_score': score,
                        'is_approved': True,
                        'approved_by': user.supervisor or self.users['admin']
                    }
                )
                skill_count += 1

        self.stdout.write(f'  ✓ {len(self.competencies)} kompetensiya, {skill_count} istifadəçi bacarığı')

    def create_training_data(self):
        """Step 6: Training resources, user training, certifications"""
        from apps.training.models import TrainingResource, UserTraining, Certification

        self.stdout.write(self.style.WARNING('\n📚 6/14: TƏLİM VƏ SERTİFİKATLAR'))

        # Training resources
        resources_data = [
            {'title': 'Python Advanced', 'type': 'course', 'hours': 40, 'level': 'advanced'},
            {'title': 'Liderlik Təlimi', 'type': 'workshop', 'hours': 16, 'level': 'intermediate'},
            {'title': 'Agile Scrum Master', 'type': 'certification', 'hours': 24, 'level': 'intermediate'},
            {'title': 'Data Science Fundamentals', 'type': 'course', 'hours': 60, 'level': 'beginner'},
            {'title': 'Project Management Professional', 'type': 'certification', 'hours': 80, 'level': 'advanced'},
        ]

        for res in resources_data:
            tr, _ = TrainingResource.objects.get_or_create(
                title=res['title'],
                defaults={
                    'description': f"{res['title']} üzrə təlim proqramı",
                    'type': res['type'],
                    'delivery_method': 'online',
                    'difficulty_level': res['level'],
                    'duration_hours': res['hours'],
                    'provider': 'Q360 Akademiya',
                    'is_active': True
                }
            )
            self.training_resources.append(tr)

        # User training
        training_count = 0
        all_users = self.users['managers'] + self.users['employees'][:15]
        for user in all_users:
            # Assign 1-3 trainings
            user_trainings = random.sample(self.training_resources, k=random.randint(1, 3))
            for tr in user_trainings:
                UserTraining.objects.get_or_create(
                    user=user,
                    resource=tr,
                    defaults={
                        'assigned_by': user.supervisor or self.users['admin'],
                        'assignment_type': random.choice(['manager_assigned', 'self_enrolled']),
                        'start_date': date.today() - timedelta(days=random.randint(10, 60)),
                        'due_date': date.today() + timedelta(days=random.randint(10, 90)),
                        'status': random.choice(['pending', 'in_progress', 'completed']),
                        'progress_percentage': random.randint(20, 100)
                    }
                )
                training_count += 1

        # Certifications
        cert_count = 0
        for user in self.users['managers'][:3] + self.users['employees'][:5]:
            Certification.objects.get_or_create(
                user=user,
                certification_name='AWS Solutions Architect',
                defaults={
                    'certification_code': f'AWS-SAA-{random.randint(1000, 9999)}',
                    'issuing_organization': 'Amazon Web Services',
                    'issue_date': date.today() - timedelta(days=random.randint(100, 500)),
                    'expiration_date': date.today() + timedelta(days=random.randint(200, 700)),
                    'status': 'active',
                    'company_sponsored': True
                }
            )
            cert_count += 1

        self.stdout.write(f'  ✓ {len(self.training_resources)} təlim, {training_count} təyin, {cert_count} sertifikat')

    def create_recruitment_data(self):
        """Step 7: Job postings, applications, interviews, offers"""
        from apps.recruitment.models import JobPosting, Application, Interview, Offer

        self.stdout.write(self.style.WARNING('\n💼 7/14: İŞƏGÖTÜRMƏ VƏ MÜRACİƏTLƏR'))

        # Job postings
        jobs_data = [
            {'title': 'Senior Python Developer', 'dept': 'IT-DEV', 'positions': 2, 'type': 'full_time'},
            {'title': 'HR Specialist', 'dept': 'HR-REC', 'positions': 1, 'type': 'full_time'},
            {'title': 'Financial Analyst', 'dept': 'FIN-ACC', 'positions': 1, 'type': 'contract'},
        ]

        job_postings = []
        for job in jobs_data:
            jp, _ = JobPosting.objects.get_or_create(
                title=job['title'],
                code=f"JOB-{random.randint(1000, 9999)}",
                defaults={
                    'department': self.departments[job['dept']],
                    'description': f"{job['title']} vəzifəsi üçün açıq vakansiya",
                    'employment_type': job['type'],
                    'experience_level': 'mid',
                    'number_of_positions': job['positions'],
                    'salary_min': Decimal('2000'),
                    'salary_max': Decimal('4000'),
                    'salary_currency': 'AZN',
                    'status': 'open',
                    'posted_date': date.today() - timedelta(days=random.randint(5, 30)),
                    'closing_date': date.today() + timedelta(days=random.randint(30, 60)),
                    'hiring_manager': random.choice(self.users['managers']),
                    'created_by': self.users['admin']
                }
            )
            job_postings.append(jp)

        # Applications
        app_count = 0
        for jp in job_postings:
            # 5-10 applications per job
            for i in range(random.randint(5, 10)):
                Application.objects.create(
                    job_posting=jp,
                    first_name=f'Namizəd{i}',
                    last_name=f'Soyad{i}',
                    email=f'candidate{i}_{jp.id}@example.com',
                    phone=f'+994 50 555 {random.randint(1000, 9999)}',
                    status=random.choice(['received', 'screening', 'interview', 'offer', 'hired', 'rejected']),
                    source=random.choice(['website', 'linkedin', 'referral']),
                    years_of_experience=random.randint(1, 10),
                    expected_salary=Decimal(random.randint(2500, 5000)),
                    applied_at=timezone.now() - timedelta(days=random.randint(1, 20))
                )
                app_count += 1

        self.stdout.write(f'  ✓ {len(job_postings)} vakansiya, {app_count} müraciət')

    def create_compensation_data(self):
        """Step 8: Salaries, bonuses, allowances"""
        from apps.compensation.models import (
            SalaryInformation, CompensationHistory, Bonus,
            Allowance, DepartmentBudget
        )

        self.stdout.write(self.style.WARNING('\n💰 8/14: MAAŞ VƏ KOMPENSASİYA'))

        # Salaries
        salary_count = 0
        all_users = self.users['directors'] + self.users['managers'] + self.users['employees'][:20]

        for user in all_users:
            base = Decimal(random.randint(2000, 8000))
            if user in self.users['directors']:
                base = Decimal(random.randint(8000, 12000))
            elif user in self.users['managers']:
                base = Decimal(random.randint(4000, 7000))

            SalaryInformation.objects.get_or_create(
                user=user,
                defaults={
                    'base_salary': base,
                    'currency': 'AZN',
                    'payment_frequency': 'monthly',
                    'effective_date': date(2024, 1, 1),
                    'is_active': True,
                    'updated_by': self.users['admin']
                }
            )
            salary_count += 1

        # Bonuses
        bonus_count = 0
        for user in all_users[:10]:
            Bonus.objects.get_or_create(
                user=user,
                defaults={
                    'bonus_type': 'performance',
                    'amount': Decimal(random.randint(500, 2000)),
                    'currency': 'AZN',
                    'status': random.choice(['approved', 'paid']),
                    'payment_date': date.today() - timedelta(days=random.randint(10, 60)),
                    'fiscal_year': 2024,
                    'approved_by': self.users['admin'],
                    'created_by': self.users['admin']
                }
            )
            bonus_count += 1

        # Allowances
        allow_count = 0
        for user in all_users[:15]:
            Allowance.objects.get_or_create(
                user=user,
                allowance_type='transportation',
                defaults={
                    'amount': Decimal('150'),
                    'currency': 'AZN',
                    'payment_frequency': 'monthly',
                    'start_date': date(2024, 1, 1),
                    'is_taxable': False,
                    'is_active': True,
                    'approved_by': self.users['admin']
                }
            )
            allow_count += 1

        self.stdout.write(f'  ✓ {salary_count} maaş, {bonus_count} bonus, {allow_count} müavinət')

    def create_leave_attendance_data(self):
        """Step 9: Leave types, leave requests, attendance"""
        from apps.leave_attendance.models import LeaveType, LeaveBalance, LeaveRequest, Attendance, Holiday

        self.stdout.write(self.style.WARNING('\n🏖️ 9/14: MƏZUNİYYƏT VƏ DAVAMIYYƏT'))

        # Leave types
        leave_types_data = [
            {'name': 'İllik Məzuniyyət', 'code': 'ANNUAL', 'days': 20, 'paid': True},
            {'name': 'Xəstəlik Məzuniyyəti', 'code': 'SICK', 'days': 10, 'paid': True},
            {'name': 'Analıq Məzuniyyəti', 'code': 'MATERNITY', 'days': 126, 'paid': True},
            {'name': 'Ödənişsiz Məzuniyyət', 'code': 'UNPAID', 'days': 30, 'paid': False},
        ]

        for lt in leave_types_data:
            leave_type, _ = LeaveType.objects.get_or_create(
                code=lt['code'],
                defaults={
                    'name': lt['name'],
                    'days_per_year': lt['days'],
                    'is_paid': lt['paid'],
                    'requires_approval': True,
                    'is_active': True
                }
            )
            self.leave_types.append(leave_type)

        # Leave balances and requests
        leave_count = 0
        all_users = self.users['managers'] + self.users['employees'][:15]

        for user in all_users:
            for leave_type in self.leave_types[:2]:  # Annual and Sick
                LeaveBalance.objects.get_or_create(
                    user=user,
                    leave_type=leave_type,
                    year=2024,
                    defaults={
                        'entitled_days': leave_type.days_per_year,
                        'used_days': random.randint(0, 5),
                        'pending_days': 0,
                        'carried_forward_days': 0
                    }
                )

                # Create 0-2 leave requests
                for _ in range(random.randint(0, 2)):
                    start = date.today() + timedelta(days=random.randint(-30, 60))
                    days = random.randint(1, 5)
                    LeaveRequest.objects.get_or_create(
                        user=user,
                        leave_type=leave_type,
                        start_date=start,
                        defaults={
                            'end_date': start + timedelta(days=days - 1),
                            'number_of_days': days,
                            'reason': 'Şəxsi işlər',
                            'status': random.choice(['pending', 'approved', 'rejected']),
                            'approved_by': user.supervisor or self.users['admin']
                        }
                    )
                    leave_count += 1

        # Attendance (last 30 days for 10 users)
        attendance_count = 0
        for user in all_users[:10]:
            for day_offset in range(30):
                att_date = date.today() - timedelta(days=day_offset)
                if att_date.weekday() < 5:  # Weekdays only
                    from datetime import time
                    Attendance.objects.get_or_create(
                        user=user,
                        date=att_date,
                        defaults={
                            'status': random.choice(['present', 'present', 'present', 'late', 'on_leave']),
                            'check_in': time(9, random.randint(0, 30)),
                            'check_out': time(18, random.randint(0, 30)),
                            'work_hours': Decimal('8.5')
                        }
                    )
                    attendance_count += 1

        # Holidays
        Holiday.objects.get_or_create(
            name='Novruz Bayramı',
            date=date(2024, 3, 21),
            defaults={'holiday_type': 'public', 'is_recurring': True, 'is_active': True}
        )

        self.stdout.write(f'  ✓ {len(self.leave_types)} məzuniyyət növü, {leave_count} müraciət, {attendance_count} davamiyyət qeydi')

    def create_feedback_data(self):
        """Step 10: Quick feedback, recognition"""
        from apps.continuous_feedback.models import QuickFeedback, FeedbackBank, FeedbackTag

        self.stdout.write(self.style.WARNING('\n💬 10/14: GERİBİLDİRİM VƏ TƏQDİR'))

        # Feedback tags
        tags_data = ['Komanda işi', 'Liderlik', 'Kommunikasiya', 'İnovasiya', 'Peşəkarlıq']
        tags = []
        for tag_name in tags_data:
            tag, _ = FeedbackTag.objects.get_or_create(
                name=tag_name,
                defaults={'description': f'{tag_name} sahəsində'}
            )
            tags.append(tag)

        # Quick feedbacks
        feedback_count = 0
        all_users = self.users['managers'] + self.users['employees'][:15]

        for _ in range(30):
            sender = random.choice(all_users)
            recipient = random.choice([u for u in all_users if u != sender])

            feedback_texts = [
                'Əla iş görmüsünüz, təşəkkürlər!',
                'Layihədə göstərdiyiniz dəstəyə görə minnətdaram.',
                'Komanda ilə əməkdaşlığınız çox yaxşıdır.',
                'Problem həllində göstərdiyiniz yaradıcılıq təqdirəlayiqdir.',
            ]

            fb = QuickFeedback.objects.create(
                sender=sender,
                recipient=recipient,
                feedback_type=random.choice(['recognition', 'general']),
                visibility=random.choice(['private', 'public', 'team']),
                source_relationship=random.choice(['peer', 'manager', 'direct_report']),
                title='Geri bildiriş',
                message=random.choice(feedback_texts),
                rating=random.randint(4, 5),
                is_anonymous=random.choice([True, False])
            )
            fb.tags.set(random.sample(tags, k=random.randint(1, 2)))
            feedback_count += 1

        # Feedback banks
        for user in all_users[:10]:
            FeedbackBank.objects.get_or_create(
                user=user,
                defaults={
                    'total_feedbacks_received': random.randint(5, 20),
                    'total_recognitions': random.randint(3, 15),
                    'total_improvements': random.randint(1, 5),
                    'average_rating': Decimal(str(round(random.uniform(3.5, 5.0), 1)))
                }
            )

        self.stdout.write(f'  ✓ {feedback_count} geri bildiriş, {len(tags)} etiket')

    def create_notifications_data(self):
        """Step 11: Notifications"""
        from apps.notifications.models import Notification, NotificationPreference

        self.stdout.write(self.style.WARNING('\n🔔 11/14: BİLDİRİŞLƏR'))

        # Notification preferences
        pref_count = 0
        all_users = self.users['managers'] + self.users['employees'][:10]

        for user in all_users:
            for method in ['email', 'in_app']:
                NotificationPreference.objects.get_or_create(
                    user=user,
                    method=method,
                    category='assignment',
                    defaults={'enabled': True}
                )
                pref_count += 1

        # Sample notifications
        notif_count = 0
        for user in all_users[:10]:
            for _ in range(random.randint(3, 8)):
                Notification.objects.create(
                    user=user,
                    title='Yeni tapşırıq',
                    message='Sizə yeni qiymətləndirmə tapşırığı təyin edilib',
                    notification_type=random.choice(['info', 'assignment', 'reminder']),
                    channel='in_app',
                    is_read=random.choice([True, False]),
                    priority='normal'
                )
                notif_count += 1

        self.stdout.write(f'  ✓ {notif_count} bildiriş, {pref_count} parametr')

    def create_workforce_planning_data(self):
        """Step 12: Talent matrix, succession planning"""
        from apps.workforce_planning.models import TalentMatrix, CriticalRole, SuccessionCandidate, CompetencyGap

        self.stdout.write(self.style.WARNING('\n📈 12/14: İŞÇİ QÜVVƏSI PLANLAŞDIRMASI'))

        # Talent matrix (9-box)
        matrix_count = 0
        all_users = self.users['managers'] + self.users['employees'][:15]

        for user in all_users:
            perf_score = random.randint(40, 95)
            pot_score = random.randint(40, 95)

            TalentMatrix.objects.get_or_create(
                user=user,
                assessment_period='2024-Q4',
                defaults={
                    'performance_level': 'high' if perf_score > 70 else ('medium' if perf_score > 40 else 'low'),
                    'performance_score': perf_score,
                    'potential_level': 'high' if pot_score > 70 else ('medium' if pot_score > 40 else 'low'),
                    'potential_score': pot_score,
                    'assessed_by': user.supervisor or self.users['admin'],
                    'assessment_date': date.today(),
                    'notes': 'Qiymətləndirmə qeydi'
                }
            )
            matrix_count += 1

        # Critical roles
        role_count = 0
        for pos_code in ['DIR-HR', 'DIR-IT', 'MGR-IT']:
            if pos_code in self.positions:
                CriticalRole.objects.get_or_create(
                    position=self.positions[pos_code],
                    defaults={
                        'criticality_level': 'high',
                        'business_impact': 'Vacib strateji vəzifə',
                        'succession_readiness': random.choice(['ready_now', 'ready_1_2_years', 'needs_development']),
                        'is_active': True
                    }
                )
                role_count += 1

        self.stdout.write(f'  ✓ {matrix_count} talent qiyməti, {role_count} kritik vəzifə')

    def create_onboarding_data(self):
        """Step 13: Onboarding templates and processes"""
        from apps.onboarding.models import OnboardingTemplate, OnboardingTaskTemplate, OnboardingProcess, OnboardingTask

        self.stdout.write(self.style.WARNING('\n🎓 13/14: ONBOARDİNQ PROSESİ'))

        # Template
        template, _ = OnboardingTemplate.objects.get_or_create(
            slug='standard-employee',
            defaults={
                'name': 'Standart İşçi Onboarding',
                'description': 'Yeni işçilər üçün standart onboarding prosesi',
                'is_default': True,
                'is_active': True
            }
        )

        # Task templates
        tasks_data = [
            {'title': 'Sistem girişi yaratmaq', 'type': 'general', 'days': 1, 'role': 'it'},
            {'title': 'Şirkət siyasətlərini oxumaq', 'type': 'general', 'days': 3, 'role': 'hr'},
            {'title': 'İlk həftə təlimi', 'type': 'training_plan', 'days': 7, 'role': 'manager'},
            {'title': '90 günlük performans qiyməti', 'type': 'performance_review', 'days': 90, 'role': 'manager'},
        ]

        for task in tasks_data:
            OnboardingTaskTemplate.objects.get_or_create(
                template=template,
                title=task['title'],
                defaults={
                    'description': f"{task['title']} tapşırığı",
                    'task_type': task['type'],
                    'due_in_days': task['days'],
                    'assignee_role': task['role'],
                    'order': len(tasks_data)
                }
            )

        # Processes for new employees
        process_count = 0
        for user in self.users['employees'][:3]:
            OnboardingProcess.objects.get_or_create(
                employee=user,
                defaults={
                    'template': template,
                    'department': user.department,
                    'start_date': date.today() - timedelta(days=random.randint(10, 60)),
                    'status': random.choice(['active', 'completed']),
                    'created_by': self.users['admin']
                }
            )
            process_count += 1

        self.stdout.write(f'  ✓ 1 şablon, {len(tasks_data)} tapşırıq növü, {process_count} aktiv proses')

    def create_support_data(self):
        """Step 14: Support tickets"""
        from apps.support.models import SupportTicket, TicketComment

        self.stdout.write(self.style.WARNING('\n🆘 14/14: DƏSTƏK SİSTEMİ'))

        # Support tickets
        ticket_count = 0
        all_users = self.users['managers'] + self.users['employees'][:10]

        for _ in range(15):
            user = random.choice(all_users)
            ticket = SupportTicket.objects.create(
                title=random.choice([
                    'Sistem girişi problemi',
                    'Hesabat yaratma xətası',
                    'Məzuniyyət müraciəti problemi',
                    'Qiymətləndirmə tapşırığı görünmür'
                ]),
                description='Köməyə ehtiyacım var',
                status=random.choice(['open', 'in_progress', 'resolved', 'closed']),
                priority=random.choice(['low', 'medium', 'high']),
                created_by=user,
                assigned_to=random.choice(self.users['managers'])
            )
            ticket_count += 1

            # Comments
            if random.random() > 0.5:
                TicketComment.objects.create(
                    ticket=ticket,
                    comment='Problem araşdırılır',
                    created_by=ticket.assigned_to or self.users['admin'],
                    is_internal=False
                )

        self.stdout.write(f'  ✓ {ticket_count} dəstək müraciəti')

    def create_audit_data(self):
        """Create audit logs"""
        from apps.audit.models import AuditLog

        self.stdout.write(self.style.WARNING('\n🔍 BONUS: AUDİT LOQLARI'))

        # Sample audit logs
        log_count = 0
        all_users = self.users['directors'] + self.users['managers'][:5]

        for _ in range(50):
            user = random.choice(all_users)
            AuditLog.objects.create(
                user=user,
                action=random.choice(['create', 'update', 'view', 'delete', 'login']),
                model_name=random.choice(['User', 'EvaluationCampaign', 'SalaryInformation', 'LeaveRequest']),
                object_id=random.randint(1, 100),
                changes={'field': 'value'},
                request_path='/admin/accounts/user/',
                http_method='POST',
                status_code=200,
                severity='info',
                ip_address=f'192.168.1.{random.randint(1, 254)}'
            )
            log_count += 1

        self.stdout.write(f'  ✓ {log_count} audit qeydi')

    def print_summary(self):
        """Print final summary"""
        from apps.departments.models import Organization, Department, Position
        from apps.evaluations.models import EvaluationCampaign, Question, EvaluationAssignment, Response
        from apps.development_plans.models import DevelopmentGoal
        from apps.competencies.models import Competency, UserSkill
        from apps.training.models import TrainingResource, UserTraining, Certification
        from apps.recruitment.models import JobPosting, Application
        from apps.compensation.models import SalaryInformation, Bonus
        from apps.leave_attendance.models import LeaveType, LeaveRequest, Attendance
        from apps.continuous_feedback.models import QuickFeedback
        from apps.notifications.models import Notification
        from apps.workforce_planning.models import TalentMatrix
        from apps.onboarding.models import OnboardingProcess
        from apps.support.models import SupportTicket
        from apps.audit.models import AuditLog

        self.stdout.write(self.style.SUCCESS('\n' + '='*80))
        self.stdout.write(self.style.SUCCESS('✅ TAM ƏHATƏLI DEMO MƏLUMAT BAZASI YARADILDI!'))
        self.stdout.write(self.style.SUCCESS('='*80))

        self.stdout.write(self.style.WARNING('\n📊 YARADILMIŞ MƏLUMATLAR:\n'))

        stats = [
            ('Təşkilatlar', Organization.objects.count()),
            ('Şöbələr', Department.objects.count()),
            ('Vəzifələr', Position.objects.count()),
            ('İstifadəçilər', User.objects.count()),
            ('Qiymətləndirmə Kampaniyaları', EvaluationCampaign.objects.count()),
            ('Suallar', Question.objects.count()),
            ('Qiymətləndirmə Tapşırıqları', EvaluationAssignment.objects.count()),
            ('Cavablar', Response.objects.count()),
            ('İnkişaf Məqsədləri', DevelopmentGoal.objects.count()),
            ('Kompetensiyalar', Competency.objects.count()),
            ('İstifadəçi Bacarıqları', UserSkill.objects.count()),
            ('Təlim Resursları', TrainingResource.objects.count()),
            ('Təlim Təyinatları', UserTraining.objects.count()),
            ('Sertifikatlar', Certification.objects.count()),
            ('Vakansiyalar', JobPosting.objects.count()),
            ('Müraciətlər', Application.objects.count()),
            ('Maaş Qeydləri', SalaryInformation.objects.count()),
            ('Bonuslar', Bonus.objects.count()),
            ('Məzuniyyət Növləri', LeaveType.objects.count()),
            ('Məzuniyyət Müraciətləri', LeaveRequest.objects.count()),
            ('Davamiyyət Qeydləri', Attendance.objects.count()),
            ('Geri Bildirişlər', QuickFeedback.objects.count()),
            ('Bildirişlər', Notification.objects.count()),
            ('Talent Qiymətləri', TalentMatrix.objects.count()),
            ('Onboarding Prosesləri', OnboardingProcess.objects.count()),
            ('Dəstək Müraciətləri', SupportTicket.objects.count()),
            ('Audit Logları', AuditLog.objects.count()),
        ]

        for name, count in stats:
            self.stdout.write(f'  • {name}: {count}')

        self.stdout.write(self.style.WARNING('\n🔐 GİRİŞ MƏLUMATLARI:\n'))
        self.stdout.write(self.style.SUCCESS('  Admin:'))
        self.stdout.write('    Username: admin')
        self.stdout.write('    Password: admin123\n')

        self.stdout.write(self.style.SUCCESS('  Direktorlar:'))
        self.stdout.write('    Username: kamran, elvin, leyla')
        self.stdout.write('    Password: director123\n')

        self.stdout.write(self.style.SUCCESS('  Menecerlər:'))
        self.stdout.write('    Username: rashad, gunel, tural, nigar, farid')
        self.stdout.write('    Password: manager123\n')

        self.stdout.write(self.style.SUCCESS('  İşçilər:'))
        self.stdout.write('    Username: emp01 - emp30')
        self.stdout.write('    Password: employee123\n')

        self.stdout.write(self.style.WARNING('🌐 SAYT:'))
        self.stdout.write('    http://127.0.0.1:8000/')
        self.stdout.write('    http://127.0.0.1:8000/admin/\n')
