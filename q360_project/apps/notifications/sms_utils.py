"""
SMS notification utility functions using Twilio.
"""
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


def send_sms(phone_number, message):
    """
    Send SMS using Twilio.
    
    Args:
        phone_number (str): Recipient phone number (E.164 format: +994501234567)
        message (str): SMS message content
        
    Returns:
        bool: True if sent successfully
    """
    try:
        from twilio.rest import Client
        
        # Get Twilio credentials from settings
        account_sid = getattr(settings, 'TWILIO_ACCOUNT_SID', None)
        auth_token = getattr(settings, 'TWILIO_AUTH_TOKEN', None)
        from_number = getattr(settings, 'TWILIO_PHONE_NUMBER', None)
        
        if not all([account_sid, auth_token, from_number]):
            logger.error("Twilio credentials not configured in settings")
            return False
        
        # Initialize Twilio client
        client = Client(account_sid, auth_token)
        
        # Send SMS
        sms_message = client.messages.create(
            body=message,
            from_=from_number,
            to=phone_number
        )
        
        logger.info(f"SMS sent successfully. SID: {sms_message.sid}")
        return True
        
    except ImportError:
        logger.error("Twilio SDK not installed. Run: pip install twilio")
        return False
    except Exception as e:
        logger.error(f"Error sending SMS: {e}")
        return False


def send_bulk_sms(recipients, message):
    """
    Send SMS to multiple recipients.
    
    Args:
        recipients (list): List of phone numbers
        message (str): SMS message content
        
    Returns:
        dict: Result with sent/failed counts
    """
    sent_count = 0
    failed_count = 0
    
    for phone_number in recipients:
        success = send_sms(phone_number, message)
        if success:
            sent_count += 1
        else:
            failed_count += 1
    
    return {
        'total': len(recipients),
        'sent': sent_count,
        'failed': failed_count
    }


def send_sms_verification_code(phone_number, code):
    """
    Send verification code via SMS.
    
    Args:
        phone_number (str): Recipient phone number
        code (str): Verification code
        
    Returns:
        bool: True if sent successfully
    """
    message = f"Q360 təsdiq kodu: {code}. Bu kodu heç kəslə paylaşmayın."
    return send_sms(phone_number, message)


def send_sms_notification(user, message):
    """
    Send SMS notification to user.
    
    Args:
        user: User object
        message (str): Notification message
        
    Returns:
        bool: True if sent successfully
    """
    try:
        # Get user's phone number
        phone_number = None
        if hasattr(user, 'profile') and hasattr(user.profile, 'phone'):
            phone_number = user.profile.phone
        elif hasattr(user, 'phone'):
            phone_number = user.phone
        
        if not phone_number:
            logger.warning(f"No phone number for user {user.id}")
            return False
        
        return send_sms(phone_number, message)
        
    except Exception as e:
        logger.error(f"Error sending SMS notification: {e}")
        return False
