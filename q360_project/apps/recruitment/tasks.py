"""
Celery tasks for recruitment/ATS module.
"""
from celery import shared_task
from django.utils import timezone
from .ai_screening import AIScreeningEngine


@shared_task
def screen_application_task(application_id):
    """
    Background task to screen an application using AI.

    Args:
        application_id: Application ID to screen

    Returns:
        Dict with screening results
    """
    from .models import Application
    import logging

    logger = logging.getLogger(__name__)

    try:
        application = Application.objects.select_related('job_posting', 'candidate').get(id=application_id)

        # Extract resume text
        # In production, this would read from the actual resume file
        resume_text = f"""
        {application.cover_letter}
        Position: {application.current_position}
        Company: {application.current_company or ''}
        Years of Experience: {application.years_of_experience or 0}
        Skills: {application.skills_summary or ''}
        Education: {application.education_summary or ''}
        """

        # Run AI screening
        result = AIScreeningEngine.screen_application(application, resume_text)

        # Update application with screening results
        application.ai_screening_score = result['scores']['overall_score']
        application.ai_screening_data = {
            'scores': result['scores'],
            'recommendation': result['recommendation'],
            'recommendation_text': result['recommendation_text'],
            'summary': result['screening_summary'],
            'screened_at': timezone.now().isoformat(),
            'parsed_cv': result['parsed_cv']
        }
        application.save(update_fields=['ai_screening_score', 'ai_screening_data'])

        logger.info(f"Successfully screened application {application_id}. Score: {result['scores']['overall_score']:.1f}")

        return {
            'success': True,
            'application_id': application_id,
            'score': result['scores']['overall_score'],
            'recommendation': result['recommendation']
        }

    except Application.DoesNotExist:
        logger.error(f"Application {application_id} not found")
        return {'success': False, 'error': 'Application not found'}

    except Exception as e:
        logger.error(f"Error screening application {application_id}: {str(e)}")
        return {'success': False, 'error': str(e)}


@shared_task
def batch_screen_applications_task(job_posting_id, limit=None):
    """
    Background task to screen multiple applications for a job posting.

    Args:
        job_posting_id: JobPosting ID
        limit: Maximum number of applications to screen

    Returns:
        Dict with batch screening results
    """
    from .models import JobPosting, Application
    import logging

    logger = logging.getLogger(__name__)

    try:
        job_posting = JobPosting.objects.get(id=job_posting_id)

        # Get applications to screen
        applications = Application.objects.filter(
            job_posting=job_posting,
            status='received',
            ai_screening_score__isnull=True  # Only unscreened applications
        ).order_by('-applied_at')

        if limit:
            applications = applications[:limit]

        total = applications.count()
        screened = 0
        failed = 0

        logger.info(f"Starting batch screening for job posting {job_posting_id}. Total: {total}")

        # Screen each application
        for application in applications:
            try:
                result = screen_application_task.delay(application.id)
                screened += 1
            except Exception as e:
                logger.error(f"Failed to screen application {application.id}: {str(e)}")
                failed += 1

        return {
            'success': True,
            'job_posting_id': job_posting_id,
            'total': total,
            'screened': screened,
            'failed': failed
        }

    except JobPosting.DoesNotExist:
        logger.error(f"JobPosting {job_posting_id} not found")
        return {'success': False, 'error': 'Job posting not found'}

    except Exception as e:
        logger.error(f"Error in batch screening for job posting {job_posting_id}: {str(e)}")
        return {'success': False, 'error': str(e)}


@shared_task
def send_interview_reminder_task(interview_id, hours_before=24):
    """
    Send interview reminder to candidate and interviewer.

    Args:
        interview_id: Interview ID
        hours_before: Hours before interview to send reminder

    Returns:
        Dict with task result
    """
    from .models import Interview
    from apps.notifications.utils import send_notification_by_smart_routing
    import logging

    logger = logging.getLogger(__name__)

    try:
        interview = Interview.objects.select_related(
            'application__candidate',
            'interviewer'
        ).get(id=interview_id)

        # Send reminder to candidate
        candidate = interview.application.candidate
        send_notification_by_smart_routing(
            user=candidate,
            title=f'Müsahibə xatırlatması',
            message=f'Salam {candidate.get_full_name()}, sizin {interview.interview_date} tarixli müsahibəniz yaxınlaşır.',
            notification_type='email',
            priority='high',
            context={
                'interview_date': interview.interview_date,
                'interview_type': interview.get_interview_type_display(),
                'job_title': interview.application.job_posting.title,
                'interviewer': interview.interviewer.get_full_name() if interview.interviewer else 'N/A'
            }
        )

        # Send reminder to interviewer
        if interview.interviewer:
            send_notification_by_smart_routing(
                user=interview.interviewer,
                title=f'Müsahibə xatırlatması',
                message=f'Sizin {interview.interview_date} tarixli {candidate.get_full_name()} ilə müsahibəniz yaxınlaşır.',
                notification_type='email',
                priority='high',
                context={
                    'interview_date': interview.interview_date,
                    'candidate_name': candidate.get_full_name(),
                    'job_title': interview.application.job_posting.title
                }
            )

        logger.info(f"Successfully sent interview reminders for interview {interview_id}")

        return {
            'success': True,
            'interview_id': interview_id,
            'reminders_sent': 2
        }

    except Interview.DoesNotExist:
        logger.error(f"Interview {interview_id} not found")
        return {'success': False, 'error': 'Interview not found'}

    except Exception as e:
        logger.error(f"Error sending interview reminders for {interview_id}: {str(e)}")
        return {'success': False, 'error': str(e)}
