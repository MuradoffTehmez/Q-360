"""
E-Learning Platform Integration Module.
Supports integration with popular e-learning platforms like Udemy, Coursera, LinkedIn Learning.
Implements SSO, content synchronization, and progress tracking.
"""
from django.conf import settings
import requests
import hashlib
import hmac
import base64
from datetime import datetime, timedelta
from typing import Dict, List, Optional


class ELearningProvider:
    """Base class for e-learning platform integrations."""

    def authenticate_user(self, user):
        """Authenticate user for SSO."""
        raise NotImplementedError

    def sync_courses(self):
        """Sync available courses."""
        raise NotImplementedError

    def get_user_enrollments(self, user):
        """Get user's enrolled courses."""
        raise NotImplementedError

    def track_progress(self, user, course_id):
        """Track user progress in a course."""
        raise NotImplementedError


class UdemyBusinessIntegration(ELearningProvider):
    """
    Udemy for Business integration.
    Requires Udemy Business API credentials.
    """

    def __init__(self):
        self.base_url = getattr(settings, 'UDEMY_BASE_URL', 'https://www.udemy.com/api-2.0')
        self.client_id = getattr(settings, 'UDEMY_CLIENT_ID', '')
        self.client_secret = getattr(settings, 'UDEMY_CLIENT_SECRET', '')
        self.organization_id = getattr(settings, 'UDEMY_ORG_ID', '')

    def _make_request(self, endpoint, method='GET', params=None, data=None):
        """Make authenticated API request to Udemy."""
        if not self.client_id or not self.client_secret:
            return {'success': False, 'error': 'Udemy credentials not configured'}

        headers = {
            'Authorization': f'Basic {self._get_auth_token()}'
        }

        url = f"{self.base_url}/{endpoint}"

        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, params=params)
            elif method == 'POST':
                response = requests.post(url, headers=headers, json=data)
            else:
                return {'success': False, 'error': 'Unsupported method'}

            response.raise_for_status()
            return {'success': True, 'data': response.json()}
        except requests.exceptions.RequestException as e:
            return {'success': False, 'error': str(e)}

    def _get_auth_token(self):
        """Generate basic auth token."""
        credentials = f"{self.client_id}:{self.client_secret}"
        return base64.b64encode(credentials.encode()).decode()

    def authenticate_user(self, user):
        """Create SSO token for user."""
        # Udemy SSO implementation
        timestamp = int(datetime.now().timestamp())

        sso_data = {
            'email': user.email,
            'name': user.get_full_name(),
            'timestamp': timestamp
        }

        return {
            'success': True,
            'sso_url': f"{self.base_url}/sso?user={user.email}&timestamp={timestamp}"
        }

    def sync_courses(self):
        """Sync courses from Udemy Business."""
        result = self._make_request(f'organizations/{self.organization_id}/courses')

        if not result['success']:
            return result

        courses = []
        for course_data in result.get('data', {}).get('results', []):
            courses.append({
                'external_id': course_data.get('id'),
                'title': course_data.get('title'),
                'description': course_data.get('headline', ''),
                'instructor': ', '.join([i.get('display_name', '') for i in course_data.get('visible_instructors', [])]),
                'duration_hours': course_data.get('estimated_content_length', 0) / 3600,
                'language': course_data.get('locale', {}).get('english_title'),
                'link': f"https://www.udemy.com{course_data.get('url')}",
                'image_url': course_data.get('image_480x270')
            })

        return {
            'success': True,
            'courses': courses,
            'count': len(courses)
        }

    def get_user_enrollments(self, user):
        """Get user's enrolled courses from Udemy."""
        result = self._make_request(f'users/{user.email}/subscribed-courses')

        if not result['success']:
            return result

        enrollments = []
        for course in result.get('data', {}).get('results', []):
            enrollments.append({
                'course_id': course.get('id'),
                'course_title': course.get('title'),
                'enrollment_date': course.get('enrollment_time'),
                'completion_ratio': course.get('completion_ratio', 0)
            })

        return {
            'success': True,
            'enrollments': enrollments
        }

    def track_progress(self, user, course_id):
        """Track user's progress in a course."""
        result = self._make_request(
            f'users/{user.email}/subscribed-courses/{course_id}/progress'
        )

        if not result['success']:
            return result

        progress_data = result.get('data', {})

        return {
            'success': True,
            'progress': {
                'completion_percentage': progress_data.get('completion_ratio', 0) * 100,
                'lectures_completed': progress_data.get('num_lectures_completed', 0),
                'total_lectures': progress_data.get('num_lectures', 0),
                'last_accessed': progress_data.get('last_accessed_time')
            }
        }


class CourseraIntegration(ELearningProvider):
    """
    Coursera for Business integration.
    """

    def __init__(self):
        self.base_url = getattr(settings, 'COURSERA_BASE_URL', 'https://api.coursera.org/api')
        self.api_key = getattr(settings, 'COURSERA_API_KEY', '')
        self.program_id = getattr(settings, 'COURSERA_PROGRAM_ID', '')

    def _make_request(self, endpoint, method='GET', params=None, data=None):
        """Make authenticated API request to Coursera."""
        if not self.api_key:
            return {'success': False, 'error': 'Coursera credentials not configured'}

        headers = {
            'Authorization': f'Bearer {self.api_key}'
        }

        url = f"{self.base_url}/{endpoint}"

        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, params=params)
            elif method == 'POST':
                response = requests.post(url, headers=headers, json=data)
            else:
                return {'success': False, 'error': 'Unsupported method'}

            response.raise_for_status()
            return {'success': True, 'data': response.json()}
        except requests.exceptions.RequestException as e:
            return {'success': False, 'error': str(e)}

    def authenticate_user(self, user):
        """Create SSO for user."""
        # Generate SSO link
        sso_link = f"{self.base_url}/sso/{self.program_id}?email={user.email}"

        return {
            'success': True,
            'sso_url': sso_link
        }

    def sync_courses(self):
        """Sync courses from Coursera."""
        result = self._make_request(f'programs/{self.program_id}/courses')

        if not result['success']:
            return result

        courses = []
        for course_data in result.get('data', {}).get('elements', []):
            courses.append({
                'external_id': course_data.get('id'),
                'title': course_data.get('name'),
                'description': course_data.get('description', ''),
                'link': f"https://www.coursera.org/learn/{course_data.get('slug')}",
                'duration_hours': course_data.get('workload', 0)
            })

        return {
            'success': True,
            'courses': courses,
            'count': len(courses)
        }

    def get_user_enrollments(self, user):
        """Get user enrollments."""
        result = self._make_request(f'users/{user.email}/enrollments')

        if not result['success']:
            return result

        enrollments = []
        for enrollment in result.get('data', {}).get('elements', []):
            enrollments.append({
                'course_id': enrollment.get('courseId'),
                'enrollment_date': enrollment.get('enrolledAt'),
                'status': enrollment.get('status')
            })

        return {
            'success': True,
            'enrollments': enrollments
        }

    def track_progress(self, user, course_id):
        """Track course progress."""
        result = self._make_request(
            f'users/{user.email}/courses/{course_id}/progress'
        )

        if not result['success']:
            return result

        progress_data = result.get('data', {})

        return {
            'success': True,
            'progress': {
                'completion_percentage': progress_data.get('progressPercent', 0),
                'grade': progress_data.get('grade'),
                'status': progress_data.get('status')
            }
        }


class LinkedInLearningIntegration(ELearningProvider):
    """
    LinkedIn Learning integration.
    """

    def __init__(self):
        self.base_url = getattr(settings, 'LINKEDIN_LEARNING_URL', 'https://api.linkedin.com/v2')
        self.client_id = getattr(settings, 'LINKEDIN_CLIENT_ID', '')
        self.client_secret = getattr(settings, 'LINKEDIN_CLIENT_SECRET', '')
        self.access_token = getattr(settings, 'LINKEDIN_ACCESS_TOKEN', '')

    def _make_request(self, endpoint, method='GET', params=None, data=None):
        """Make authenticated API request to LinkedIn."""
        if not self.access_token:
            return {'success': False, 'error': 'LinkedIn credentials not configured'}

        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'X-Restli-Protocol-Version': '2.0.0'
        }

        url = f"{self.base_url}/{endpoint}"

        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, params=params)
            elif method == 'POST':
                response = requests.post(url, headers=headers, json=data)
            else:
                return {'success': False, 'error': 'Unsupported method'}

            response.raise_for_status()
            return {'success': True, 'data': response.json()}
        except requests.exceptions.RequestException as e:
            return {'success': False, 'error': str(e)}

    def authenticate_user(self, user):
        """SSO for LinkedIn Learning."""
        sso_url = f"https://www.linkedin.com/learning-login/go/{self.client_id}?email={user.email}"

        return {
            'success': True,
            'sso_url': sso_url
        }

    def sync_courses(self):
        """Sync LinkedIn Learning courses."""
        result = self._make_request('learningAssets')

        if not result['success']:
            return result

        courses = []
        for asset in result.get('data', {}).get('elements', []):
            if asset.get('type') == 'COURSE':
                courses.append({
                    'external_id': asset.get('urn'),
                    'title': asset.get('title', {}).get('value'),
                    'description': asset.get('description', {}).get('value', ''),
                    'link': asset.get('detailsUrl'),
                    'duration_hours': asset.get('timeToComplete', {}).get('duration', 0) / 3600
                })

        return {
            'success': True,
            'courses': courses,
            'count': len(courses)
        }

    def get_user_enrollments(self, user):
        """Get user enrollments."""
        # LinkedIn Learning uses learning activity API
        result = self._make_request(f'learningActivityReports?q=user&user={user.email}')

        if not result['success']:
            return result

        enrollments = []
        for activity in result.get('data', {}).get('elements', []):
            enrollments.append({
                'course_id': activity.get('learningAsset'),
                'enrollment_date': activity.get('firstViewedAt'),
                'last_viewed': activity.get('lastViewedAt')
            })

        return {
            'success': True,
            'enrollments': enrollments
        }

    def track_progress(self, user, course_id):
        """Track course progress."""
        result = self._make_request(
            f'learningActivityReports?q=criteria&learningAsset={course_id}&user={user.email}'
        )

        if not result['success']:
            return result

        progress_data = result.get('data', {}).get('elements', [{}])[0]

        return {
            'success': True,
            'progress': {
                'completion_percentage': progress_data.get('percentComplete', 0),
                'videos_viewed': progress_data.get('videosViewed', 0),
                'last_viewed': progress_data.get('lastViewedAt')
            }
        }


class ELearningManager:
    """
    Manages e-learning platform integrations.
    """

    PROVIDERS = {
        'udemy': UdemyBusinessIntegration,
        'coursera': CourseraIntegration,
        'linkedin': LinkedInLearningIntegration
    }

    def __init__(self, provider='udemy'):
        """
        Initialize e-learning manager.

        Args:
            provider: Platform name ('udemy', 'coursera', 'linkedin')
        """
        provider_class = self.PROVIDERS.get(provider)
        if not provider_class:
            raise ValueError(f"Unsupported e-learning provider: {provider}")

        self.provider = provider_class()
        self.provider_name = provider

    def generate_sso_link(self, user):
        """
        Generate SSO link for user to access platform.

        Args:
            user: User instance

        Returns:
            dict: SSO URL and metadata
        """
        result = self.provider.authenticate_user(user)
        return result

    def sync_platform_courses(self):
        """
        Sync courses from e-learning platform to TrainingResource.
        """
        from .models import TrainingResource

        result = self.provider.sync_courses()

        if not result['success']:
            return result

        synced_count = 0
        updated_count = 0

        for course_data in result.get('courses', []):
            resource, created = TrainingResource.objects.update_or_create(
                link=course_data.get('link'),
                defaults={
                    'title': course_data.get('title'),
                    'description': course_data.get('description', ''),
                    'type': 'course',
                    'delivery_method': 'online',
                    'is_online': True,
                    'duration_hours': course_data.get('duration_hours', 0),
                    'provider': f"{self.provider_name.title()}",
                    'is_active': True
                }
            )

            if created:
                synced_count += 1
            else:
                updated_count += 1

        return {
            'success': True,
            'synced': synced_count,
            'updated': updated_count,
            'total': synced_count + updated_count
        }

    def sync_user_enrollments(self, user):
        """
        Sync user's enrollments from platform.

        Args:
            user: User instance

        Returns:
            dict: Sync results
        """
        from .models import UserTraining, TrainingResource

        result = self.provider.get_user_enrollments(user)

        if not result['success']:
            return result

        synced = 0

        for enrollment in result.get('enrollments', []):
            # Find corresponding training resource
            resource = TrainingResource.objects.filter(
                link__icontains=enrollment.get('course_id', '')
            ).first()

            if not resource:
                continue

            # Create or update UserTraining
            user_training, created = UserTraining.objects.get_or_create(
                user=user,
                resource=resource,
                defaults={
                    'assignment_type': 'self_enrolled',
                    'status': 'in_progress'
                }
            )

            synced += 1

        return {
            'success': True,
            'synced': synced
        }

    def sync_user_progress(self, user_training):
        """
        Sync user's progress from e-learning platform.

        Args:
            user_training: UserTraining instance

        Returns:
            dict: Progress data
        """
        # Extract course ID from resource link
        course_id = self._extract_course_id(user_training.resource.link)

        if not course_id:
            return {'success': False, 'error': 'Could not extract course ID'}

        result = self.provider.track_progress(user_training.user, course_id)

        if result['success']:
            progress = result['progress']

            # Update UserTraining
            completion = progress.get('completion_percentage', 0)
            user_training.progress_percentage = int(completion)

            if completion >= 100:
                user_training.mark_completed('Completed via e-learning platform sync')
            elif completion > 0:
                user_training.mark_in_progress()

            user_training.save()

        return result

    def _extract_course_id(self, link):
        """Extract course identifier from URL."""
        import re

        if not link:
            return None

        # Try to find course ID in URL
        patterns = [
            r'/courses?/([^/]+)',
            r'/learn/([^/]+)',
            r'urn:li:learningAsset:([^/]+)'
        ]

        for pattern in patterns:
            match = re.search(pattern, link)
            if match:
                return match.group(1)

        return None


# Factory function
def get_elearning_manager(provider='udemy'):
    """
    Get e-learning platform manager.

    Args:
        provider: Platform name

    Returns:
        ELearningManager instance
    """
    return ELearningManager(provider)
