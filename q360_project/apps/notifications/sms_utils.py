"""SMS utility functions for notifications app."""
import logging
from django.conf import settings
from django.utils import timezone
from .models import SMSProvider, SMSLog
from apps.accounts.models import User


logger = logging.getLogger(__name__)


def send_sms_notification(recipient_phone, message, provider_name=None, user=None):
    """
    Send SMS notification to a phone number using configured provider.

    Args:
        recipient_phone (str): Recipient's phone number
        message (str): SMS message content
        provider_name (str): Name of SMS provider to use (optional)
        user (User): User object to link with the SMS log

    Returns:
        bool: True if SMS sent successfully, False otherwise
    """
    # Find or use default SMS provider
    if provider_name:
        try:
            provider = SMSProvider.objects.get(name=provider_name, is_active=True)
        except SMSProvider.DoesNotExist:
            logger.error(f"SMS provider '{provider_name}' not found or inactive")
            return False
    else:
        # Use the first active provider
        provider = SMSProvider.objects.filter(is_active=True).first()
        if not provider:
            logger.error("No active SMS providers configured")
            return False
    
    # Create SMS log entry
    sms_log = SMSLog.objects.create(
        recipient=user,
        recipient_phone=recipient_phone,
        message=message,
        provider=provider,
        status='pending'
    )
    
    try:
        # Send SMS using the provider based on its type
        if provider.provider == 'twilio':
            success = send_sms_via_twilio(provider.configuration, recipient_phone, message)
        elif provider.provider == 'aws_sns':
            success = send_sms_via_aws_sns(provider.configuration, recipient_phone, message)
        elif provider.provider == 'clickatell':
            success = send_sms_via_clickatell(provider.configuration, recipient_phone, message)
        elif provider.provider == 'azercell':
            success = send_sms_via_azercell(provider.configuration, recipient_phone, message)
        elif provider.provider == 'bakcell':
            success = send_sms_via_bakcell(provider.configuration, recipient_phone, message)
        elif provider.provider == 'custom':
            success = send_sms_via_custom(provider.configuration, recipient_phone, message)
        else:
            logger.error(f"Unsupported SMS provider: {provider.provider}")
            success = False
        
        # Update SMS log status
        if success:
            sms_log.status = 'sent'
            sms_log.sent_at = timezone.now()
        else:
            sms_log.status = 'failed'
            sms_log.error_message = 'SMS sending failed'
        
        sms_log.save()
        return success
        
    except Exception as e:
        sms_log.status = 'failed'
        sms_log.error_message = str(e)
        sms_log.save()
        logger.error(f"Error sending SMS: {e}")
        return False


def send_sms_via_twilio(config, recipient_phone, message):
    """
    Send SMS using Twilio API.

    Args:
        config (dict): Twilio configuration
        recipient_phone (str): Recipient's phone number
        message (str): SMS message content

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Import Twilio (only if needed, to avoid dependency if not using Twilio)
        from twilio.rest import Client
        
        # Extract config parameters
        account_sid = config.get('account_sid')
        auth_token = config.get('auth_token')
        from_number = config.get('from_number')
        
        if not all([account_sid, auth_token, from_number]):
            logger.error("Missing Twilio configuration parameters")
            return False
        
        client = Client(account_sid, auth_token)
        
        # Send message
        twilio_message = client.messages.create(
            body=message,
            from_=from_number,
            to=recipient_phone
        )
        
        # Here you would typically track the message SID for delivery status
        # For now, we'll just return success
        return True
        
    except ImportError:
        logger.error("Twilio library not installed")
        return False
    except Exception as e:
        logger.error(f"Error sending SMS via Twilio: {e}")
        return False


def send_sms_via_aws_sns(config, recipient_phone, message):
    """
    Send SMS using AWS SNS.

    Args:
        config (dict): AWS SNS configuration
        recipient_phone (str): Recipient's phone number
        message (str): SMS message content

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        import boto3
        from botocore.exceptions import ClientError
        
        # Extract config parameters
        aws_access_key_id = config.get('aws_access_key_id')
        aws_secret_access_key = config.get('aws_secret_access_key')
        aws_region = config.get('aws_region', 'us-east-1')
        
        if not all([aws_access_key_id, aws_secret_access_key, aws_region]):
            logger.error("Missing AWS SNS configuration parameters")
            return False
        
        # Create SNS client
        sns_client = boto3.client(
            'sns',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=aws_region
        )
        
        # Send SMS
        response = sns_client.publish(
            PhoneNumber=recipient_phone,
            Message=message,
            MessageAttributes={
                'AWS.SNS.SMS.SMSType': {
                    'DataType': 'String',
                    'StringValue': 'Transactional'  # or 'Promotional'
                }
            }
        )
        
        # Check if message was sent successfully
        return 'MessageId' in response
        
    except ImportError:
        logger.error("Boto3 library not installed")
        return False
    except ClientError as e:
        logger.error(f"Error sending SMS via AWS SNS: {e}")
        return False
    except Exception as e:
        logger.error(f"Error sending SMS via AWS SNS: {e}")
        return False


def send_sms_via_clickatell(config, recipient_phone, message):
    """
    Send SMS using Clickatell API.

    Args:
        config (dict): Clickatell configuration
        recipient_phone (str): Recipient's phone number
        message (str): SMS message content

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        import requests
        
        # Extract config parameters
        api_key = config.get('api_key')
        base_url = config.get('base_url', 'https://platform.clickatell.com')
        
        if not api_key:
            logger.error("Missing Clickatell API key")
            return False
        
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'to': [recipient_phone],
            'content': message
        }
        
        response = requests.post(
            f'{base_url}/messages',
            headers=headers,
            json=payload
        )
        
        # Check if the request was successful
        if response.status_code == 202:  # Accepted
            return True
        else:
            logger.error(f"Clickatell API error: {response.status_code} - {response.text}")
            return False
            
    except ImportError:
        logger.error("Requests library not installed")
        return False
    except Exception as e:
        logger.error(f"Error sending SMS via Clickatell: {e}")
        return False


def send_sms_via_azercell(config, recipient_phone, message):
    """
    Send SMS using Azercell SMS Gateway.

    Azercell SMS Gateway API integration for Azerbaijan.

    Args:
        config (dict): Azercell configuration with 'username', 'password', 'originator'
        recipient_phone (str): Recipient's phone number (format: 994xxxxxxxxx)
        message (str): SMS message content

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        import requests

        username = config.get('username')
        password = config.get('password')
        originator = config.get('originator', 'Q360')
        api_url = config.get('api_url', 'https://sms.azercell.com/api/send')

        if not all([username, password]):
            logger.error("Missing Azercell credentials")
            return False

        # Prepare request payload
        payload = {
            'username': username,
            'password': password,
            'originator': originator,
            'recipient': recipient_phone,
            'message': message
        }

        response = requests.post(api_url, json=payload, timeout=30)

        if response.status_code == 200:
            result = response.json()
            if result.get('status') == 'success':
                logger.info(f"SMS sent via Azercell to {recipient_phone}")
                return True
            else:
                logger.error(f"Azercell API error: {result.get('message', 'Unknown error')}")
                return False
        else:
            logger.error(f"Azercell API HTTP error: {response.status_code}")
            return False

    except Exception as e:
        logger.error(f"Error sending SMS via Azercell: {e}")
        return False


def send_sms_via_bakcell(config, recipient_phone, message):
    """
    Send SMS using Bakcell SMS API.

    Bakcell SMS API integration for Azerbaijan.

    Args:
        config (dict): Bakcell configuration with 'api_key', 'sender_id'
        recipient_phone (str): Recipient's phone number (format: 994xxxxxxxxx)
        message (str): SMS message content

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        import requests

        api_key = config.get('api_key')
        sender_id = config.get('sender_id', 'Q360')
        api_url = config.get('api_url', 'https://api.bakcell.com/sms/send')

        if not api_key:
            logger.error("Missing Bakcell API key")
            return False

        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }

        payload = {
            'sender': sender_id,
            'recipient': recipient_phone,
            'text': message
        }

        response = requests.post(api_url, headers=headers, json=payload, timeout=30)

        if response.status_code in [200, 201]:
            result = response.json()
            if result.get('success'):
                logger.info(f"SMS sent via Bakcell to {recipient_phone}")
                return True
            else:
                logger.error(f"Bakcell API error: {result.get('error', 'Unknown error')}")
                return False
        else:
            logger.error(f"Bakcell API HTTP error: {response.status_code}")
            return False

    except Exception as e:
        logger.error(f"Error sending SMS via Bakcell: {e}")
        return False


def send_sms_via_custom(config, recipient_phone, message):
    """
    Send SMS using a custom provider implementation.

    Args:
        config (dict): Custom provider configuration
        recipient_phone (str): Recipient's phone number
        message (str): SMS message content

    Returns:
        bool: True if successful, False otherwise
    """
    # This is a placeholder for custom SMS providers
    # In a real implementation, you would have specific logic based on the configuration

    # For demonstration, let's assume there's a custom_url and custom_token in config
    try:
        import requests

        custom_url = config.get('custom_url')
        custom_token = config.get('custom_token')
        custom_method = config.get('method', 'POST').upper()

        if not custom_url:
            logger.error("Missing custom SMS provider URL")
            return False

        headers = {
            'Authorization': f'Bearer {custom_token}' if custom_token else '',
            'Content-Type': 'application/json'
        }

        payload = {
            'to': recipient_phone,
            'message': message
        }

        if custom_method == 'GET':
            response = requests.get(custom_url, headers=headers, params=payload, timeout=30)
        else:
            response = requests.post(custom_url, headers=headers, json=payload, timeout=30)

        # Check if the request was successful
        success = response.status_code in [200, 201, 202]

        if success:
            logger.info(f"SMS sent via custom provider to {recipient_phone}")
        else:
            logger.error(f"Custom provider error: {response.status_code} - {response.text}")

        return success

    except Exception as e:
        logger.error(f"Error sending SMS via custom provider: {e}")
        return False


def send_bulk_sms(recipients, message, provider_name=None):
    """
    Send bulk SMS messages to multiple recipients.

    Args:
        recipients: List of phone numbers or User queryset
        message (str): SMS message content
        provider_name (str): Name of SMS provider to use (optional)

    Returns:
        dict: Result with sent, failed counts
    """
    from django.contrib.auth import get_user_model
    
    User = get_user_model()
    
    # Convert to phone number list
    phone_list = []
    if recipients and hasattr(recipients, 'model') and recipients.model == User:
        # This is a User queryset
        for user in recipients:
            phone = getattr(user, 'phone_number', None) or \
                    getattr(user.profile, 'work_phone', None) if hasattr(user, 'profile') else None
            if phone:
                phone_list.append(phone)
    elif isinstance(recipients, list) and recipients:
        if isinstance(recipients[0], User):
            # List of User objects
            for user in recipients:
                phone = getattr(user, 'phone_number', None) or \
                        getattr(user.profile, 'work_phone', None) if hasattr(user, 'profile') else None
                if phone:
                    phone_list.append(phone)
        else:
            # List of phone numbers
            phone_list = recipients
    
    sent_count = 0
    failed_count = 0
    
    for phone in phone_list:
        success = send_sms_notification(phone, message, provider_name=provider_name)
        if success:
            sent_count += 1
        else:
            failed_count += 1
    
    return {
        'total': len(phone_list),
        'sent': sent_count,
        'failed': failed_count
    }


def get_sms_statistics_for_user(user):
    """
    Get SMS statistics for a specific user.

    Args:
        user (User): User object

    Returns:
        dict: SMS statistics
    """
    total_sms = SMSLog.objects.filter(recipient=user).count()
    sent_sms = SMSLog.objects.filter(recipient=user, status='sent').count()
    failed_sms = SMSLog.objects.filter(recipient=user, status='failed').count()
    
    return {
        'total': total_sms,
        'sent': sent_sms,
        'failed': failed_sms,
        'success_rate': (sent_sms / total_sms * 100) if total_sms > 0 else 0
    }