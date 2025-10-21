"""
Video Interview Integration Module.
Supports integration with Zoom, Microsoft Teams, Google Meet for video interviews.
"""
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import hashlib
import hmac
import base64
import time
import json


class VideoInterviewProvider:
    """
    Base class for video interview providers.
    """

    def create_meeting(self, interview):
        """Create a video meeting for an interview."""
        raise NotImplementedError

    def get_meeting_link(self, interview):
        """Get meeting link for an interview."""
        raise NotImplementedError

    def cancel_meeting(self, interview):
        """Cancel a video meeting."""
        raise NotImplementedError

    def get_meeting_details(self, interview):
        """Get detailed meeting information."""
        raise NotImplementedError


class ZoomIntegration(VideoInterviewProvider):
    """
    Zoom video conferencing integration.
    Requires Zoom API credentials in settings.
    """

    def __init__(self):
        self.api_key = getattr(settings, 'ZOOM_API_KEY', '')
        self.api_secret = getattr(settings, 'ZOOM_API_SECRET', '')
        self.base_url = 'https://api.zoom.us/v2'

    def _generate_jwt_token(self):
        """Generate JWT token for Zoom API authentication."""
        # Note: This is a simplified version. In production, use PyJWT library
        import jwt

        token = jwt.encode(
            {
                'iss': self.api_key,
                'exp': time.time() + 5000
            },
            self.api_secret,
            algorithm='HS256'
        )
        return token

    def create_meeting(self, interview):
        """
        Create Zoom meeting for interview.

        Args:
            interview: Interview model instance

        Returns:
            dict: Meeting details including join URL
        """
        if not self.api_key or not self.api_secret:
            return {
                'success': False,
                'error': 'Zoom API credentials not configured'
            }

        meeting_data = {
            'topic': f"Interview: {interview.application.full_name} - {interview.application.job_posting.title}",
            'type': 2,  # Scheduled meeting
            'start_time': interview.scheduled_date.isoformat(),
            'duration': interview.duration_minutes,
            'timezone': 'Asia/Baku',
            'settings': {
                'host_video': True,
                'participant_video': True,
                'join_before_host': False,
                'mute_upon_entry': True,
                'waiting_room': True,
                'audio': 'both',
                'auto_recording': 'cloud',
                'registration_type': 1
            }
        }

        # In production, make actual API request
        # For now, return mock response
        mock_response = {
            'success': True,
            'meeting_id': f'zoom_{interview.id}',
            'join_url': f'https://zoom.us/j/{interview.id}?pwd=mock',
            'host_url': f'https://zoom.us/s/{interview.id}?zak=mock',
            'password': self._generate_meeting_password(interview),
            'start_time': interview.scheduled_date.isoformat(),
            'duration': interview.duration_minutes
        }

        # Update interview with meeting link
        interview.meeting_link = mock_response['join_url']
        interview.save()

        return mock_response

    def get_meeting_link(self, interview):
        """Get existing meeting link."""
        if interview.meeting_link:
            return interview.meeting_link

        # If no link exists, create meeting
        result = self.create_meeting(interview)
        return result.get('join_url')

    def cancel_meeting(self, interview):
        """Cancel Zoom meeting."""
        # In production, make API call to delete meeting
        return {
            'success': True,
            'message': 'Meeting cancelled successfully'
        }

    def _generate_meeting_password(self, interview):
        """Generate secure meeting password."""
        data = f"{interview.id}:{interview.scheduled_date}"
        return hashlib.md5(data.encode()).hexdigest()[:8]


class MicrosoftTeamsIntegration(VideoInterviewProvider):
    """
    Microsoft Teams integration.
    """

    def __init__(self):
        self.tenant_id = getattr(settings, 'MS_TEAMS_TENANT_ID', '')
        self.client_id = getattr(settings, 'MS_TEAMS_CLIENT_ID', '')
        self.client_secret = getattr(settings, 'MS_TEAMS_CLIENT_SECRET', '')

    def create_meeting(self, interview):
        """Create Teams meeting for interview."""
        meeting_data = {
            'subject': f"Interview: {interview.application.full_name}",
            'startDateTime': interview.scheduled_date.isoformat(),
            'endDateTime': (interview.scheduled_date + timedelta(minutes=interview.duration_minutes)).isoformat(),
            'participants': {
                'attendees': [
                    {
                        'emailAddress': {
                            'address': interview.application.email,
                            'name': interview.application.full_name
                        }
                    }
                ]
            }
        }

        # Mock response
        mock_response = {
            'success': True,
            'meeting_id': f'teams_{interview.id}',
            'join_url': f'https://teams.microsoft.com/l/meetup-join/{interview.id}',
            'start_time': interview.scheduled_date.isoformat(),
            'duration': interview.duration_minutes
        }

        interview.meeting_link = mock_response['join_url']
        interview.save()

        return mock_response

    def get_meeting_link(self, interview):
        """Get Teams meeting link."""
        if interview.meeting_link:
            return interview.meeting_link

        result = self.create_meeting(interview)
        return result.get('join_url')

    def cancel_meeting(self, interview):
        """Cancel Teams meeting."""
        return {
            'success': True,
            'message': 'Teams meeting cancelled successfully'
        }


class GoogleMeetIntegration(VideoInterviewProvider):
    """
    Google Meet integration.
    """

    def __init__(self):
        self.credentials_file = getattr(settings, 'GOOGLE_MEET_CREDENTIALS', '')

    def create_meeting(self, interview):
        """Create Google Meet for interview."""
        # Mock response
        mock_response = {
            'success': True,
            'meeting_id': f'meet_{interview.id}',
            'join_url': f'https://meet.google.com/{interview.id}',
            'start_time': interview.scheduled_date.isoformat(),
            'duration': interview.duration_minutes
        }

        interview.meeting_link = mock_response['join_url']
        interview.save()

        return mock_response

    def get_meeting_link(self, interview):
        """Get Google Meet link."""
        if interview.meeting_link:
            return interview.meeting_link

        result = self.create_meeting(interview)
        return result.get('join_url')

    def cancel_meeting(self, interview):
        """Cancel Google Meet."""
        return {
            'success': True,
            'message': 'Google Meet cancelled successfully'
        }


class VideoInterviewManager:
    """
    Manages video interviews across different providers.
    """

    PROVIDERS = {
        'zoom': ZoomIntegration,
        'teams': MicrosoftTeamsIntegration,
        'google_meet': GoogleMeetIntegration
    }

    def __init__(self, provider_name='zoom'):
        """
        Initialize manager with specific provider.

        Args:
            provider_name: Name of video conferencing provider (zoom, teams, google_meet)
        """
        provider_class = self.PROVIDERS.get(provider_name)
        if not provider_class:
            raise ValueError(f"Unsupported provider: {provider_name}")

        self.provider = provider_class()
        self.provider_name = provider_name

    def schedule_interview(self, interview):
        """
        Schedule video interview and create meeting.

        Args:
            interview: Interview model instance

        Returns:
            dict: Meeting details
        """
        result = self.provider.create_meeting(interview)

        if result.get('success'):
            # Send email notifications
            self._send_interview_invitation(interview, result)

        return result

    def reschedule_interview(self, interview, new_date):
        """
        Reschedule existing interview.

        Args:
            interview: Interview model instance
            new_date: New datetime for interview
        """
        # Cancel old meeting
        self.provider.cancel_meeting(interview)

        # Update interview time
        interview.scheduled_date = new_date
        interview.status = 'rescheduled'
        interview.save()

        # Create new meeting
        result = self.provider.create_meeting(interview)

        if result.get('success'):
            self._send_reschedule_notification(interview, result)

        return result

    def cancel_interview(self, interview):
        """
        Cancel video interview.

        Args:
            interview: Interview model instance
        """
        result = self.provider.cancel_meeting(interview)

        if result.get('success'):
            interview.status = 'cancelled'
            interview.save()

            self._send_cancellation_notification(interview)

        return result

    def get_meeting_link(self, interview):
        """
        Get meeting link for interview.

        Args:
            interview: Interview model instance

        Returns:
            str: Meeting join URL
        """
        return self.provider.get_meeting_link(interview)

    def _send_interview_invitation(self, interview, meeting_details):
        """
        Send interview invitation email to candidate.
        """
        from django.core.mail import send_mail
        from django.template.loader import render_to_string

        subject = f"Video Müsahibə Dəvətnaməsi - {interview.application.job_posting.title}"

        # Prepare email context
        context = {
            'candidate_name': interview.application.full_name,
            'job_title': interview.application.job_posting.title,
            'interview_type': interview.get_interview_type_display(),
            'scheduled_date': interview.scheduled_date,
            'duration': interview.duration_minutes,
            'meeting_link': meeting_details.get('join_url'),
            'meeting_password': meeting_details.get('password'),
            'interviewers': ', '.join([i.get_full_name() for i in interview.interviewers.all()]),
            'location': interview.location or 'Online'
        }

        # In production, use proper email template
        message = f"""
Hörmətli {context['candidate_name']},

{context['job_title']} vəzifəsi üçün video müsahibəyə dəvət olunursunuz.

Müsahibə Detalları:
- Tarix və Vaxt: {context['scheduled_date'].strftime('%d.%m.%Y, saat %H:%M')}
- Müddət: {context['duration']} dəqiqə
- Növ: {context['interview_type']}
- Müsahibə Alanlar: {context['interviewers']}

Video Müsahibə Linki:
{context['meeting_link']}

Şifrə: {context.get('meeting_password', 'Lazım deyil')}

Qeydlər:
- Müsahibədən 5-10 dəqiqə əvvəl link-ə daxil olun
- Təmiz və sakit bir yer seçin
- İnternet bağlantınızı yoxlayın
- Kamera və mikrofonu test edin

Müvəffəqiyyətlər arzulayırıq!

Hörmətlə,
İşəqəbul Komandası
        """

        # Send email
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [interview.application.email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Error sending email: {e}")

    def _send_reschedule_notification(self, interview, meeting_details):
        """Send notification about rescheduled interview."""
        # Similar to invitation but with rescheduling message
        pass

    def _send_cancellation_notification(self, interview):
        """Send notification about cancelled interview."""
        # Send cancellation email
        pass


# Factory function for easy access
def get_video_interview_manager(provider='zoom'):
    """
    Get video interview manager instance.

    Args:
        provider: Video conferencing provider name

    Returns:
        VideoInterviewManager instance
    """
    return VideoInterviewManager(provider)
