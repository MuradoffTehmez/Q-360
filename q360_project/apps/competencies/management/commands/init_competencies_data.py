"""
Management command to initialize competencies data.
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.competencies.models import ProficiencyLevel, Competency


class Command(BaseCommand):
    """Initialize competencies system with default data."""

    help = 'Kompetensiya sistemini başlanğıc data ilə doldurur'

    def handle(self, *args, **options):
        """Execute the command."""
        self.stdout.write(self.style.MIGRATE_HEADING('Kompetensiya data-sı yaradılır...'))

        with transaction.atomic():
            # Create Proficiency Levels
            self._create_proficiency_levels()

            # Create sample competencies
            self._create_sample_competencies()

        self.stdout.write(self.style.SUCCESS('✓ Kompetensiya data-sı uğurla yaradıldı!'))

    def _create_proficiency_levels(self):
        """Create default proficiency levels."""
        levels = [
            {
                'name': 'basic',
                'display_name': 'Əsas',
                'score_min': 0.00,
                'score_max': 40.00,
                'description': 'Əsas səviyyə - Başlanğıc bilik və bacarıqlar'
            },
            {
                'name': 'intermediate',
                'display_name': 'Orta',
                'score_min': 40.01,
                'score_max': 70.00,
                'description': 'Orta səviyyə - Müstəqil işləmək bacarığı'
            },
            {
                'name': 'advanced',
                'display_name': 'Təkmil',
                'score_min': 70.01,
                'score_max': 90.00,
                'description': 'Təkmil səviyyə - Yüksək səviyyədə mütəxəssislik'
            },
            {
                'name': 'expert',
                'display_name': 'Ekspert',
                'score_min': 90.01,
                'score_max': 100.00,
                'description': 'Ekspert səviyyə - Sahə üzrə lider'
            },
        ]

        for level_data in levels:
            level, created = ProficiencyLevel.objects.get_or_create(
                name=level_data['name'],
                defaults={
                    'display_name': level_data['display_name'],
                    'score_min': level_data['score_min'],
                    'score_max': level_data['score_max'],
                    'description': level_data['description']
                }
            )
            if created:
                self.stdout.write(f'  ✓ Səviyyə yaradıldı: {level.display_name}')
            else:
                self.stdout.write(f'  - Səviyyə mövcuddur: {level.display_name}')

    def _create_sample_competencies(self):
        """Create sample competencies."""
        competencies = [
            {
                'name': 'Liderlik',
                'description': 'Komandaya rəhbərlik etmək və istiqamət vermək bacarığı'
            },
            {
                'name': 'Kommunikasiya',
                'description': 'Effektiv şifahi və yazılı ünsiyyət bacarıqları'
            },
            {
                'name': 'Problemlərin Həlli',
                'description': 'Analitik düşüncə və yaradıcı həll yolları tapmaq'
            },
            {
                'name': 'Komanda İşi',
                'description': 'Komanda mühitində effektiv əməkdaşlıq'
            },
            {
                'name': 'Texniki Bilik',
                'description': 'Sahə üzrə texniki bacarıq və biliklərin tətbiqi'
            },
            {
                'name': 'Müştəri Yönümlülük',
                'description': 'Müştəri ehtiyaclarını başa düşmək və cavab vermək'
            },
            {
                'name': 'Vaxt İdarəetməsi',
                'description': 'Vaxtı effektiv planlaşdırmaq və prioritetləri müəyyənləşdirmək'
            },
            {
                'name': 'İnnovasiya',
                'description': 'Yeni ideyalar və yanaşmalar təklif etmək'
            },
        ]

        for comp_data in competencies:
            comp, created = Competency.objects.get_or_create(
                name=comp_data['name'],
                defaults={
                    'description': comp_data['description'],
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(f'  ✓ Kompetensiya yaradıldı: {comp.name}')
            else:
                self.stdout.write(f'  - Kompetensiya mövcuddur: {comp.name}')
