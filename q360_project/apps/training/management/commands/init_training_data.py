"""
Management command to initialize training data.
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.training.models import TrainingResource
from apps.competencies.models import Competency


class Command(BaseCommand):
    """Initialize training system with default data."""

    help = 'Təlim sistemini başlanğıc data ilə doldurur'

    def handle(self, *args, **options):
        """Execute the command."""
        self.stdout.write(self.style.MIGRATE_HEADING('Təlim data-sı yaradılır...'))

        with transaction.atomic():
            # Create sample training resources
            self._create_sample_trainings()

        self.stdout.write(self.style.SUCCESS('✓ Təlim data-sı uğurla yaradıldı!'))

    def _create_sample_trainings(self):
        """Create sample training resources."""
        trainings = [
            {
                'title': 'Liderlik Əsasları',
                'description': 'Effektiv liderlik prinsipləri və komanda idarəetməsi üzrə təlim',
                'type': 'course',
                'is_online': True,
                'delivery_method': 'online',
                'link': 'https://example.com/leadership',
                'difficulty_level': 'intermediate',
                'duration_hours': 16.0,
                'language': 'Azərbaycan',
                'provider': 'Q360 Academy',
                'instructor': 'Dr. Əli Məmmədov',
                'cost': 250.00,
                'is_active': True,
                'is_mandatory': False,
                'competencies': ['Liderlik', 'Komanda İşi']
            },
            {
                'title': 'Effektiv Kommunikasiya Bacarıqları',
                'description': 'Şifahi və yazılı ünsiyyət bacarıqlarının inkişafı',
                'type': 'workshop',
                'is_online': False,
                'delivery_method': 'offline',
                'link': '',
                'difficulty_level': 'beginner',
                'duration_hours': 8.0,
                'language': 'Azərbaycan',
                'provider': 'BizSkills Training Center',
                'instructor': 'Nigar Həsənova',
                'cost': 150.00,
                'is_active': True,
                'is_mandatory': False,
                'competencies': ['Kommunikasiya']
            },
            {
                'title': 'Problem Həlli və Kritik Düşüncə',
                'description': 'Analitik düşüncə və yaradıcı problem həlli texnikaları',
                'type': 'course',
                'is_online': True,
                'delivery_method': 'hybrid',
                'link': 'https://example.com/problem-solving',
                'difficulty_level': 'advanced',
                'duration_hours': 24.0,
                'language': 'Azərbaycan',
                'provider': 'Q360 Academy',
                'instructor': 'Prof. Rəşid Quliyev',
                'cost': 350.00,
                'is_active': True,
                'is_mandatory': False,
                'competencies': ['Problemlərin Həlli', 'İnnovasiya']
            },
            {
                'title': 'Müştəri Xidməti Mükəmməlliyi',
                'description': 'Müştəri məmnuniyyəti və xidmət keyfiyyətinin artırılması',
                'type': 'webinar',
                'is_online': True,
                'delivery_method': 'online',
                'link': 'https://example.com/customer-service',
                'difficulty_level': 'intermediate',
                'duration_hours': 4.0,
                'language': 'Azərbaycan',
                'provider': 'Service Excellence Institute',
                'instructor': 'Aynur Əliyeva',
                'cost': 75.00,
                'is_active': True,
                'is_mandatory': False,
                'competencies': ['Müştəri Yönümlülük', 'Kommunikasiya']
            },
            {
                'title': 'Vaxt İdarəetməsi və Məhsuldarlıq',
                'description': 'Effektiv vaxt planlaması və prioritet müəyyənləşdirmə',
                'type': 'self_study',
                'is_online': True,
                'delivery_method': 'online',
                'link': 'https://example.com/time-management',
                'difficulty_level': 'beginner',
                'duration_hours': 6.0,
                'language': 'Azərbaycan',
                'provider': 'Productivity Pro',
                'instructor': 'Kamran Məmmədov',
                'cost': 0.00,
                'is_active': True,
                'is_mandatory': True,
                'competencies': ['Vaxt İdarəetməsi']
            },
            {
                'title': 'Texniki Bacarıqların İnkişafı',
                'description': 'Sahə üzrə texniki bilik və praktiki tətbiq',
                'type': 'certification',
                'is_online': True,
                'delivery_method': 'online',
                'link': 'https://example.com/technical-skills',
                'difficulty_level': 'expert',
                'duration_hours': 40.0,
                'language': 'İngilis',
                'provider': 'Tech Academy',
                'instructor': 'International Experts',
                'cost': 500.00,
                'is_active': True,
                'is_mandatory': False,
                'competencies': ['Texniki Bilik', 'İnnovasiya']
            },
        ]

        for training_data in trainings:
            competency_names = training_data.pop('competencies', [])

            training, created = TrainingResource.objects.get_or_create(
                title=training_data['title'],
                defaults=training_data
            )

            if created:
                # Add competencies
                for comp_name in competency_names:
                    try:
                        competency = Competency.objects.get(name=comp_name)
                        training.required_competencies.add(competency)
                    except Competency.DoesNotExist:
                        self.stdout.write(
                            self.style.WARNING(f'  ! Kompetensiya tapılmadı: {comp_name}')
                        )

                self.stdout.write(f'  ✓ Təlim yaradıldı: {training.title}')
            else:
                self.stdout.write(f'  - Təlim mövcuddur: {training.title}')
