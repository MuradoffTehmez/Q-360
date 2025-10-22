from django.core.management.base import BaseCommand
from apps.engagement.models import PulseSurvey, SurveyQuestion


class Command(BaseCommand):
    help = 'Create sample questions for existing surveys'

    def handle(self, *args, **options):
        # Get surveys without questions
        surveys_without_questions = PulseSurvey.objects.filter(questions__isnull=True).distinct()

        for survey in surveys_without_questions:
            self.stdout.write(f"Adding questions to: {survey.title}")

            if 'weekly' in survey.title.lower():
                questions_data = [
                    {
                        'question_text': 'How satisfied are you with your work this week?',
                        'question_type': 'rating',
                        'order': 1,
                        'is_required': True,
                    },
                    {
                        'question_text': 'How likely are you to recommend our company?',
                        'question_type': 'nps',
                        'order': 2,
                        'is_required': True,
                    },
                    {
                        'question_text': 'Do you have the resources you need?',
                        'question_type': 'yes_no',
                        'order': 3,
                        'is_required': True,
                    },
                    {
                        'question_text': 'What went well this week?',
                        'question_type': 'text',
                        'order': 4,
                        'is_required': False,
                    },
                    {
                        'question_text': 'How are you feeling?',
                        'question_type': 'emoji',
                        'order': 5,
                        'is_required': True,
                    },
                ]
            else:
                questions_data = [
                    {
                        'question_text': 'I feel valued at work',
                        'question_type': 'rating',
                        'order': 1,
                        'is_required': True,
                    },
                    {
                        'question_text': 'My manager supports my development',
                        'question_type': 'rating',
                        'order': 2,
                        'is_required': True,
                    },
                    {
                        'question_text': 'I have opportunities to grow',
                        'question_type': 'yes_no',
                        'order': 3,
                        'is_required': True,
                    },
                    {
                        'question_text': 'What can we improve?',
                        'question_type': 'text',
                        'order': 4,
                        'is_required': False,
                    },
                ]

            for q_data in questions_data:
                SurveyQuestion.objects.create(survey=survey, **q_data)

            self.stdout.write(self.style.SUCCESS(f"✅ Added {len(questions_data)} questions"))

        self.stdout.write(self.style.SUCCESS("\n✅ All done!"))
