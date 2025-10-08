"""
Management command to create sample evaluation questions.
"""
from django.core.management.base import BaseCommand
from apps.evaluations.models import QuestionCategory, Question


class Command(BaseCommand):
    help = 'Nümunə qiymətləndirmə sualları yaradır'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Nümunə suallar yaradılır...'))

        # Question categories and their questions
        categories_data = {
            'Rəhbərlik': [
                'Komandaya aydın istiqamət və vizyon verir',
                'Qərarlar qəbul edərkən effektiv və vaxtında hərəkət edir',
                'Komanda üzvlərinə güvənir və səlahiyyət verir',
                'Dəyişikliklərə uyğunlaşma qabiliyyəti yüksəkdir',
                'Strateji düşüncə qabiliyyətinə sahibdir'
            ],
            'Kommunikasiya': [
                'Məlumatları aydın və anlaşılan şəkildə çatdırır',
                'Aktiv dinləyici olaraq başqalarının fikirlərinə hörmət edir',
                'Yazılı kommunikasiya bacarıqları yüksəkdir',
                'Konflikt situasiyalarında effektiv ünsiyyət qurur',
                'Prezentasiya bacarıqları peşəkardır'
            ],
            'Texniki Bacarıqlar': [
                'İşi üçün lazım olan texniki bilikləri tam əhatə edir',
                'Yeni texnologiyaları öyrənməyə açıqdır',
                'Problemləri texniki yanaşma ilə həll edir',
                'İşində keyfiyyət standartlarına riayət edir',
                'Texniki yenilikləri işə tətbiq edir'
            ],
            'Komanda İşi': [
                'Komanda üzvləri ilə əməkdaşlıq edir',
                'Digər şöbələrlə səmərəli iş qurur',
                'Komanda məqsədlərinə töhfə verir',
                'Komanda ruhunu dəstəkləyir',
                'Paylaşma və kömək mədəniyyətini dəstəkləyir'
            ],
            'Problemlərin Həlli': [
                'Problemləri tez müəyyən edir',
                'Yaradıcı həll yolları tapır',
                'Analitik düşüncə qabiliyyəti güclüdür',
                'Qərar qəbul etmədə məntiqli yanaşır',
                'Nəticəyönümlü həllər təklif edir'
            ],
            'Vaxt İdarəetməsi': [
                'İşləri vaxtında tamamlayır',
                'Prioritetləri düzgün müəyyən edir',
                'Çoxsaylı tapşırıqları eyni vaxtda idarə edə bilir',
                'Son tarixlərə riayət edir',
                'İş yükünü effektiv planlaşdırır'
            ],
            'İnnovasiya': [
                'Yenilikçi ideya və təkliflər verir',
                'Mövcud prosesləri təkmilləşdirmək üçün çalışır',
                'Dəyişikliklərə açıqdır və dəstək verir',
                'Yaradıcı yanaşmalar təklif edir',
                'Risk götürməkdən çəkinmir'
            ],
            'Peşəkarlıq': [
                'İş etikasına riayət edir',
                'Məsuliyyətli və etibarlıdır',
                'Müştəri və ya daxili tərəfdaşlara xidmətdə keyfiyyətlidir',
                'Peşəkar davranış nümayiş etdirir',
                'Öz inkişafına diqqət yetirir'
            ]
        }

        for category_name, questions in categories_data.items():
            # Create category
            category, created = QuestionCategory.objects.get_or_create(
                name=category_name,
                defaults={
                    'description': f'{category_name} ilə bağlı qiymətləndirmə meyarları',
                    'is_active': True
                }
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Kateqoriya yaradıldı: {category_name}')
                )

            # Create questions
            for idx, question_text in enumerate(questions, 1):
                question, created = Question.objects.get_or_create(
                    category=category,
                    text=question_text,
                    defaults={
                        'question_type': 'scale',
                        'max_score': 5,
                        'is_required': True,
                        'order': idx,
                        'is_active': True
                    }
                )

                if created:
                    self.stdout.write(f'  • Sual əlavə edildi: {question_text[:50]}...')

        # Add some boolean and text questions
        misc_category, created = QuestionCategory.objects.get_or_create(
            name='Ümumi Qiymətləndirmə',
            defaults={
                'description': 'Ümumi suallar',
                'is_active': True
            }
        )

        boolean_questions = [
            'Bu şəxsi iş yoldaşınız kimi tövsiyə edərdiniz?',
            'Bu şəxs komandaya dəyərli töhfələr verir?',
        ]

        for question_text in boolean_questions:
            Question.objects.get_or_create(
                category=misc_category,
                text=question_text,
                defaults={
                    'question_type': 'boolean',
                    'is_required': True,
                    'is_active': True
                }
            )

        text_questions = [
            'Bu şəxsin əsas güclü tərəfləri nələrdir?',
            'İnkişaf etməli olduğu sahələr hansılardır?',
            'Əlavə şərh və ya tövsiyələriniz:',
        ]

        for question_text in text_questions:
            Question.objects.get_or_create(
                category=misc_category,
                text=question_text,
                defaults={
                    'question_type': 'text',
                    'is_required': False,
                    'is_active': True
                }
            )

        total_questions = Question.objects.count()
        total_categories = QuestionCategory.objects.count()

        self.stdout.write(self.style.SUCCESS(f'\n✅ Yaradılma tamamlandı!'))
        self.stdout.write(f'  Toplam kateqoriya: {total_categories}')
        self.stdout.write(f'  Toplam sual: {total_questions}')
