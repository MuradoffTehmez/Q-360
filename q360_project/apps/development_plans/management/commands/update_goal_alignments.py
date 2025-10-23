"""
Management command to recalculate alignment for all development goals.
Useful for bulk updates after algorithm changes or data migrations.
"""
from django.core.management.base import BaseCommand
from apps.development_plans.models import DevelopmentGoal


class Command(BaseCommand):
    help = 'Recalculate alignment percentage for all development goals'

    def add_arguments(self, parser):
        parser.add_argument(
            '--status',
            type=str,
            default='all',
            help='Filter goals by status (active, draft, all). Default: all'
        )
        parser.add_argument(
            '--with-parent',
            action='store_true',
            help='Only update goals that have a parent goal'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be updated without making changes'
        )

    def handle(self, *args, **options):
        status_filter = options['status']
        with_parent = options['with_parent']
        dry_run = options['dry_run']

        # Build queryset
        queryset = DevelopmentGoal.objects.all()

        if status_filter != 'all':
            queryset = queryset.filter(status=status_filter)

        if with_parent:
            queryset = queryset.filter(parent_goal__isnull=False)

        total_goals = queryset.count()

        if total_goals == 0:
            self.stdout.write(self.style.WARNING('No goals found matching criteria.'))
            return

        self.stdout.write(f'\nProcessing {total_goals} goals...')
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN - No changes will be saved\n'))

        updated_count = 0
        unchanged_count = 0
        error_count = 0

        for goal in queryset:
            try:
                old_alignment = goal.alignment_percentage
                new_alignment = goal.calculate_alignment_percentage()

                if old_alignment != new_alignment:
                    if not dry_run:
                        goal.alignment_percentage = new_alignment
                        goal.save(update_fields=['alignment_percentage', 'updated_at'])

                    self.stdout.write(
                        f'  [{goal.id}] {goal.title[:50]} | '
                        f'{old_alignment}% → {new_alignment}% '
                        f'{"(would update)" if dry_run else "✓"}'
                    )
                    updated_count += 1
                else:
                    unchanged_count += 1

            except Exception as e:
                error_count += 1
                self.stdout.write(
                    self.style.ERROR(f'  [{goal.id}] Error: {str(e)}')
                )

        # Summary
        self.stdout.write('\n' + '='*60)
        self.stdout.write(f'Total goals: {total_goals}')
        self.stdout.write(self.style.SUCCESS(f'Updated: {updated_count}'))
        self.stdout.write(f'Unchanged: {unchanged_count}')
        if error_count > 0:
            self.stdout.write(self.style.ERROR(f'Errors: {error_count}'))
        self.stdout.write('='*60 + '\n')

        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    '\nThis was a DRY RUN. Run without --dry-run to apply changes.'
                )
            )
