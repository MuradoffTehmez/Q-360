"""
Learning Management System (LMS) Integration Module.
Supports integration with popular LMS platforms like Moodle, Canvas, and custom LMS.
"""
from django.conf import settings
import requests
from datetime import datetime
from typing import Dict, List, Optional


class LMSProvider:
    """Base class for LMS providers."""

    def authenticate(self):
        """Authenticate with LMS platform."""
        raise NotImplementedError

    def sync_courses(self):
        """Sync courses from LMS."""
        raise NotImplementedError

    def enroll_user(self, user, course_id):
        """Enroll user in a course."""
        raise NotImplementedError

    def get_user_progress(self, user, course_id):
        """Get user's progress in a course."""
        raise NotImplementedError

    def get_user_completions(self, user):
        """Get all course completions for a user."""
        raise NotImplementedError


class MoodleIntegration(LMSProvider):
    """
    Moodle LMS integration.
    Uses Moodle Web Services API.
    """

    def __init__(self):
        self.base_url = getattr(settings, 'MOODLE_URL', '')
        self.token = getattr(settings, 'MOODLE_TOKEN', '')
        self.api_endpoint = f"{self.base_url}/webservice/rest/server.php"

    def _make_request(self, function, params=None):
        """Make API request to Moodle."""
        if not self.base_url or not self.token:
            return {
                'success': False,
                'error': 'Moodle credentials not configured'
            }

        request_params = {
            'wstoken': self.token,
            'wsfunction': function,
            'moodlewsrestformat': 'json'
        }

        if params:
            request_params.update(params)

        try:
            response = requests.get(self.api_endpoint, params=request_params)
            response.raise_for_status()
            return {
                'success': True,
                'data': response.json()
            }
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': str(e)
            }

    def authenticate(self):
        """Test authentication with Moodle."""
        result = self._make_request('core_webservice_get_site_info')
        return result.get('success', False)

    def sync_courses(self):
        """Sync courses from Moodle."""
        result = self._make_request('core_course_get_courses')

        if not result['success']:
            return result

        courses = []
        for course_data in result.get('data', []):
            courses.append({
                'external_id': course_data.get('id'),
                'title': course_data.get('fullname'),
                'description': course_data.get('summary', ''),
                'category': course_data.get('categoryname', ''),
                'start_date': datetime.fromtimestamp(course_data.get('startdate', 0)),
                'end_date': datetime.fromtimestamp(course_data.get('enddate', 0)) if course_data.get('enddate') else None,
                'link': f"{self.base_url}/course/view.php?id={course_data.get('id')}"
            })

        return {
            'success': True,
            'courses': courses,
            'count': len(courses)
        }

    def enroll_user(self, user, course_id):
        """Enroll user in Moodle course."""
        params = {
            'enrolments[0][roleid]': 5,  # Student role
            'enrolments[0][userid]': user.id,
            'enrolments[0][courseid]': course_id
        }

        result = self._make_request('enrol_manual_enrol_users', params)
        return result

    def get_user_progress(self, user, course_id):
        """Get user's progress in a course."""
        params = {
            'courseid': course_id,
            'userid': user.id
        }

        result = self._make_request('core_completion_get_course_completion_status', params)

        if not result['success']:
            return result

        completion_data = result.get('data', {})

        return {
            'success': True,
            'progress': {
                'completed': completion_data.get('complete', False),
                'completion_percentage': self._calculate_completion_percentage(completion_data),
                'activities_completed': completion_data.get('completedactivities', 0),
                'total_activities': completion_data.get('totalactivities', 0)
            }
        }

    def get_user_completions(self, user):
        """Get all course completions for a user."""
        params = {
            'userid': user.id
        }

        result = self._make_request('core_completion_get_user_completions', params)

        if not result['success']:
            return result

        completions = []
        for completion in result.get('data', []):
            completions.append({
                'course_id': completion.get('courseid'),
                'course_name': completion.get('coursename'),
                'completed': completion.get('complete'),
                'completion_date': datetime.fromtimestamp(completion.get('timecompleted', 0)) if completion.get('timecompleted') else None,
                'grade': completion.get('grade')
            })

        return {
            'success': True,
            'completions': completions
        }

    def _calculate_completion_percentage(self, completion_data):
        """Calculate completion percentage from completion data."""
        total = completion_data.get('totalactivities', 0)
        completed = completion_data.get('completedactivities', 0)

        if total == 0:
            return 0

        return int((completed / total) * 100)


class CanvasIntegration(LMSProvider):
    """
    Canvas LMS integration.
    Uses Canvas REST API.
    """

    def __init__(self):
        self.base_url = getattr(settings, 'CANVAS_URL', '')
        self.access_token = getattr(settings, 'CANVAS_ACCESS_TOKEN', '')
        self.api_endpoint = f"{self.base_url}/api/v1"

    def _make_request(self, endpoint, method='GET', params=None, data=None):
        """Make API request to Canvas."""
        if not self.base_url or not self.access_token:
            return {
                'success': False,
                'error': 'Canvas credentials not configured'
            }

        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }

        url = f"{self.api_endpoint}/{endpoint}"

        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, params=params)
            elif method == 'POST':
                response = requests.post(url, headers=headers, json=data)
            else:
                return {'success': False, 'error': 'Unsupported method'}

            response.raise_for_status()
            return {
                'success': True,
                'data': response.json()
            }
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': str(e)
            }

    def authenticate(self):
        """Test authentication with Canvas."""
        result = self._make_request('users/self')
        return result.get('success', False)

    def sync_courses(self):
        """Sync courses from Canvas."""
        result = self._make_request('courses')

        if not result['success']:
            return result

        courses = []
        for course_data in result.get('data', []):
            courses.append({
                'external_id': course_data.get('id'),
                'title': course_data.get('name'),
                'description': course_data.get('public_description', ''),
                'course_code': course_data.get('course_code'),
                'start_date': course_data.get('start_at'),
                'end_date': course_data.get('end_at'),
                'link': course_data.get('calendar', {}).get('ics')
            })

        return {
            'success': True,
            'courses': courses,
            'count': len(courses)
        }

    def enroll_user(self, user, course_id):
        """Enroll user in Canvas course."""
        data = {
            'enrollment': {
                'user_id': user.id,
                'type': 'StudentEnrollment',
                'enrollment_state': 'active'
            }
        }

        result = self._make_request(
            f'courses/{course_id}/enrollments',
            method='POST',
            data=data
        )
        return result

    def get_user_progress(self, user, course_id):
        """Get user's progress in a course."""
        result = self._make_request(f'courses/{course_id}/users/{user.id}/progress')

        if not result['success']:
            return result

        progress_data = result.get('data', {})

        return {
            'success': True,
            'progress': {
                'completed': progress_data.get('completed', False),
                'completion_percentage': progress_data.get('completion', 0),
                'current_score': progress_data.get('current_score'),
                'final_score': progress_data.get('final_score')
            }
        }

    def get_user_completions(self, user):
        """Get all course completions for a user."""
        result = self._make_request(f'users/{user.id}/courses')

        if not result['success']:
            return result

        completions = []
        for course in result.get('data', []):
            if course.get('workflow_state') == 'completed':
                completions.append({
                    'course_id': course.get('id'),
                    'course_name': course.get('name'),
                    'completed': True,
                    'completion_date': course.get('end_at'),
                    'grade': course.get('grade')
                })

        return {
            'success': True,
            'completions': completions
        }


class LMSManager:
    """
    Manages LMS integrations and synchronization.
    """

    PROVIDERS = {
        'moodle': MoodleIntegration,
        'canvas': CanvasIntegration
    }

    def __init__(self, provider='moodle'):
        """
        Initialize LMS manager.

        Args:
            provider: LMS platform name ('moodle', 'canvas')
        """
        provider_class = self.PROVIDERS.get(provider)
        if not provider_class:
            raise ValueError(f"Unsupported LMS provider: {provider}")

        self.provider = provider_class()
        self.provider_name = provider

    def sync_courses_to_training_resources(self):
        """
        Sync LMS courses to TrainingResource model.
        """
        from .models import TrainingResource

        result = self.provider.sync_courses()

        if not result['success']:
            return result

        synced_count = 0
        updated_count = 0

        for course_data in result.get('courses', []):
            resource, created = TrainingResource.objects.update_or_create(
                link=course_data['link'],
                defaults={
                    'title': course_data['title'],
                    'description': course_data['description'],
                    'type': 'course',
                    'delivery_method': 'online',
                    'is_online': True,
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

    def enroll_user_in_course(self, user, training_resource):
        """
        Enroll user in LMS course.

        Args:
            user: User instance
            training_resource: TrainingResource instance

        Returns:
            dict: Enrollment result
        """
        # Extract course ID from link or use external_id if available
        course_id = self._extract_course_id(training_resource.link)

        if not course_id:
            return {
                'success': False,
                'error': 'Could not extract course ID from training resource'
            }

        result = self.provider.enroll_user(user, course_id)

        if result['success']:
            # Create UserTraining record
            from .models import UserTraining

            UserTraining.objects.get_or_create(
                user=user,
                resource=training_resource,
                defaults={
                    'assignment_type': 'system_recommended',
                    'status': 'pending'
                }
            )

        return result

    def sync_user_progress(self, user_training):
        """
        Sync user's progress from LMS.

        Args:
            user_training: UserTraining instance

        Returns:
            dict: Progress data
        """
        course_id = self._extract_course_id(user_training.resource.link)

        if not course_id:
            return {
                'success': False,
                'error': 'Could not extract course ID'
            }

        result = self.provider.get_user_progress(user_training.user, course_id)

        if result['success']:
            progress = result['progress']

            # Update UserTraining with LMS progress
            user_training.progress_percentage = progress.get('completion_percentage', 0)

            if progress.get('completed'):
                user_training.mark_completed('Completed via LMS sync')
            elif progress.get('completion_percentage', 0) > 0:
                user_training.mark_in_progress()

            user_training.save()

        return result

    def batch_sync_user_progress(self, user):
        """
        Sync all LMS progress for a user.

        Args:
            user: User instance

        Returns:
            dict: Sync results
        """
        from .models import UserTraining

        user_trainings = UserTraining.objects.filter(
            user=user,
            resource__is_online=True,
            status__in=['pending', 'in_progress']
        )

        synced = 0
        errors = []

        for user_training in user_trainings:
            result = self.sync_user_progress(user_training)
            if result['success']:
                synced += 1
            else:
                errors.append({
                    'training': user_training.resource.title,
                    'error': result.get('error')
                })

        return {
            'success': True,
            'synced': synced,
            'total': user_trainings.count(),
            'errors': errors
        }

    def _extract_course_id(self, link):
        """Extract course ID from LMS link."""
        # Simple extraction - in production, use more robust parsing
        import re

        if not link:
            return None

        # Try to find ID in URL
        match = re.search(r'[?&]id=(\d+)', link)
        if match:
            return match.group(1)

        # Try to find course ID in path
        match = re.search(r'/courses?/(\d+)', link)
        if match:
            return match.group(1)

        return None


# Factory function
def get_lms_manager(provider='moodle'):
    """
    Get LMS manager instance.

    Args:
        provider: LMS platform name

    Returns:
        LMSManager instance
    """
    return LMSManager(provider)
