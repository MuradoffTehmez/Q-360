"""
Services for Wellness & Well-Being module.
Handles integrations with health tracking devices and APIs.
"""
import requests
from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone
from .models import StepTracking, HealthScore


class FitbitIntegration:
    """
    Fitbit API inteqrasiyası.
    Integration with Fitbit API for step tracking and health data.

    Documentation: https://dev.fitbit.com/build/reference/web-api/
    """

    BASE_URL = "https://api.fitbit.com/1/user/-/"

    def __init__(self, access_token):
        """
        Initialize Fitbit integration with user access token.

        Args:
            access_token: OAuth2 access token for Fitbit API
        """
        self.access_token = access_token
        self.headers = {
            'Authorization': f'Bearer {access_token}'
        }

    def get_daily_activity(self, date=None):
        """
        Gündəlik aktivlik məlumatlarını əldə et.
        Get daily activity data.

        Args:
            date: Date string in YYYY-MM-DD format. Defaults to today.

        Returns:
            dict: Activity data including steps, distance, calories
        """
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')

        url = f"{self.BASE_URL}activities/date/{date}.json"

        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            data = response.json()

            summary = data.get('summary', {})
            return {
                'date': date,
                'steps': summary.get('steps', 0),
                'distance_km': summary.get('distances', [{}])[0].get('distance', 0),
                'calories': summary.get('caloriesOut', 0),
                'active_minutes': summary.get('fairlyActiveMinutes', 0) + summary.get('veryActiveMinutes', 0),
            }
        except requests.exceptions.RequestException as e:
            print(f"Fitbit API error: {e}")
            return None

    def get_activity_series(self, start_date, end_date):
        """
        Müəyyən dövrün aktivlik məlumatlarını əldə et.
        Get activity data for a date range.

        Args:
            start_date: Start date string in YYYY-MM-DD format
            end_date: End date string in YYYY-MM-DD format

        Returns:
            list: List of daily activity data
        """
        url = f"{self.BASE_URL}activities/steps/date/{start_date}/{end_date}.json"

        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            data = response.json()

            return data.get('activities-steps', [])
        except requests.exceptions.RequestException as e:
            print(f"Fitbit API error: {e}")
            return []

    def sync_to_database(self, user, date=None):
        """
        Fitbit məlumatlarını verilənlər bazasına sinxronlaşdır.
        Sync Fitbit data to database.

        Args:
            user: User instance
            date: Date to sync. Defaults to today.

        Returns:
            StepTracking instance or None
        """
        activity_data = self.get_daily_activity(date)

        if not activity_data:
            return None

        # Create or update step tracking record
        tracking, created = StepTracking.objects.update_or_create(
            employee=user,
            tracking_date=activity_data['date'],
            defaults={
                'steps': activity_data['steps'],
                'distance_km': activity_data['distance_km'],
                'calories_burned': activity_data['calories'],
                'active_minutes': activity_data['active_minutes'],
                'data_source': 'fitbit'
            }
        )

        return tracking


class AppleHealthIntegration:
    """
    Apple Health inteqrasiyası.
    Integration with Apple Health for step tracking and health data.

    Note: Apple Health doesn't have a direct API. This would typically work
    through HealthKit on iOS apps or by parsing exported XML data.
    """

    def __init__(self, user):
        """
        Initialize Apple Health integration.

        Args:
            user: User instance
        """
        self.user = user

    def parse_health_export(self, xml_file_path):
        """
        Apple Health XML export faylını parse et.
        Parse Apple Health XML export file.

        Args:
            xml_file_path: Path to exported XML file from Apple Health

        Returns:
            list: List of daily activity data
        """
        import xml.etree.ElementTree as ET

        try:
            tree = ET.parse(xml_file_path)
            root = tree.getroot()

            # Parse step count records
            step_records = []
            for record in root.findall(".//Record[@type='HKQuantityTypeIdentifierStepCount']"):
                date = record.get('startDate')[:10]  # Get YYYY-MM-DD
                value = int(float(record.get('value', 0)))

                step_records.append({
                    'date': date,
                    'steps': value
                })

            return step_records
        except Exception as e:
            print(f"Apple Health XML parsing error: {e}")
            return []

    def sync_to_database(self, xml_file_path):
        """
        Apple Health məlumatlarını verilənlər bazasına sinxronlaşdır.
        Sync Apple Health data to database.

        Args:
            xml_file_path: Path to exported XML file

        Returns:
            int: Number of records synced
        """
        records = self.parse_health_export(xml_file_path)
        synced_count = 0

        for record in records:
            tracking, created = StepTracking.objects.update_or_create(
                employee=self.user,
                tracking_date=record['date'],
                defaults={
                    'steps': record['steps'],
                    'data_source': 'apple_health'
                }
            )
            synced_count += 1

        return synced_count


class HealthScoreCalculator:
    """
    Sağlamlıq skoru hesablayıcı.
    Health score calculator for employees.
    """

    @staticmethod
    def calculate_health_score(user, date=None):
        """
        İstifadəçinin sağlamlıq skorunu hesabla.
        Calculate health score for a user.

        Args:
            user: User instance
            date: Date for calculation. Defaults to today.

        Returns:
            HealthScore instance or None
        """
        if date is None:
            date = timezone.now().date()

        # Get recent step data (last 7 days)
        seven_days_ago = date - timedelta(days=7)
        recent_steps = StepTracking.objects.filter(
            employee=user,
            tracking_date__gte=seven_days_ago,
            tracking_date__lte=date
        )

        # Calculate activity level (0-100)
        from django.db.models import Avg
        avg_steps = recent_steps.aggregate(
            avg_steps=Avg('steps')
        )['avg_steps'] or 0

        # Activity score based on 10,000 steps target
        activity_level = min(100, (avg_steps / 10000) * 100)

        # Get latest mental health survey
        from .models import MentalHealthSurvey
        latest_survey = MentalHealthSurvey.objects.filter(
            employee=user,
            survey_date__lte=date
        ).order_by('-survey_date').first()

        mental_health = 70  # Default
        if latest_survey:
            mental_health = latest_survey.get_overall_score()

        # Physical health, nutrition, and sleep are placeholder values
        # These would come from additional data sources
        physical_health = 75  # Placeholder
        nutrition_score = 70  # Placeholder
        sleep_quality = 75  # Placeholder

        # Calculate overall score
        overall_score = (
            physical_health * 0.25 +
            mental_health * 0.25 +
            activity_level * 0.20 +
            nutrition_score * 0.15 +
            sleep_quality * 0.15
        )

        # Create or update health score
        health_score, created = HealthScore.objects.update_or_create(
            employee=user,
            score_date=date,
            defaults={
                'overall_score': int(overall_score),
                'physical_health': int(physical_health),
                'mental_health': int(mental_health),
                'activity_level': int(activity_level),
                'nutrition_score': int(nutrition_score),
                'sleep_quality': int(sleep_quality),
                'steps_per_day_avg': int(avg_steps)
            }
        )

        return health_score


# Utility functions
def sync_fitbit_data(user, access_token, days=7):
    """
    Son X günün Fitbit məlumatlarını sinxronlaşdır.
    Sync Fitbit data for last X days.

    Args:
        user: User instance
        access_token: Fitbit OAuth2 access token
        days: Number of days to sync

    Returns:
        int: Number of days synced
    """
    fitbit = FitbitIntegration(access_token)
    synced_count = 0

    for i in range(days):
        date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
        tracking = fitbit.sync_to_database(user, date)
        if tracking:
            synced_count += 1

    return synced_count


def calculate_all_health_scores():
    """
    Bütün istifadəçilər üçün sağlamlıq skorlarını hesabla.
    Calculate health scores for all users.
    This can be run as a periodic task (e.g., daily via Celery).
    """
    from apps.accounts.models import User

    users = User.objects.filter(is_active=True)
    calculated_count = 0

    for user in users:
        score = HealthScoreCalculator.calculate_health_score(user)
        if score:
            calculated_count += 1

    return calculated_count
