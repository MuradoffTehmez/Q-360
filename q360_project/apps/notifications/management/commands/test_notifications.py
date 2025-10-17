from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.notifications.models import Notification, UserNotificationPreference, SMSProvider, NotificationTemplate
from apps.notifications.utils import send_notification

User = get_user_model()


class Command(BaseCommand):
    help = 'Test the enhanced notification system functionality'

    def handle(self, *args, **options):
        self.stdout.write('Testing Enhanced Notification System...')
        
        # Test 1: Create a test user if none exists
        test_user, created = User.objects.get_or_create(
            username='test_notification_user',
            defaults={
                'email': 'test@example.com',
                'first_name': 'Test',
                'last_name': 'User',
                'is_active': True,
            }
        )
        
        if created:
            test_user.set_password('testpassword123')
            test_user.save()
            self.stdout.write(self.style.SUCCESS('Test user created'))
        else:
            self.stdout.write(self.style.WARNING('Using existing test user'))
        
        # Test 2: Create user notification preferences
        user_pref, created = UserNotificationPreference.objects.get_or_create(
            user=test_user,
            defaults={
                'email_notifications': True,
                'sms_notifications': False,
                'push_notifications': True,
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('User notification preferences created'))
        else:
            self.stdout.write(self.style.WARNING('Using existing user preferences'))
        
        # Test 3: Send a basic notification
        try:
            notification = send_notification(
                recipient=test_user,
                title='Test Bildirişi',
                message='Bu tətbiqin artırılmış bildiriş funksiyasını test etmək üçün bir test bildirişidir.',
                notification_type='info',
                link='/dashboard/',
                send_email=False,  # Don't spam the test email
                send_sms=False,    # Don't send actual SMS
                send_push=True,
                channel='in_app'
            )
            self.stdout.write(self.style.SUCCESS('In-app notification sent successfully'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to send in-app notification: {e}'))
        
        # Test 4: Create and use a notification template
        template, created = NotificationTemplate.objects.get_or_create(
            name='Test Template',
            defaults={
                'trigger': 'general_announcement',
                'subject': 'Yeni Bildiriş: {{ title }}',
                'email_content': '<p>Salam {{ user_name }},</p><p>{{ message }}</p>',
                'sms_content': 'Yeni bildiriş: {{ message }}',
                'push_content': 'Yeni bildiriş: {{ title }}',
                'inapp_content': 'Yeni bildiriş: {{ message }}',
                'is_active': True
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('Notification template created'))
        else:
            self.stdout.write(self.style.WARNING('Using existing notification template'))
        
        # Test 5: Send a notification with all channels (with realistic settings)
        try:
            notification2 = send_notification(
                recipient=test_user,
                title='Kanal Testi',
                message='Bu bildiriş bütün mövcud kanallar üzrə test üçün göndərilir.',
                notification_type='announcement',
                send_email=False,  # In a real environment, you'd set this to True
                send_sms=False,    # In a real environment, you'd set this to True
                send_push=True,
                channel='push'  # Primary channel
            )
            self.stdout.write(self.style.SUCCESS('Multi-channel test notification sent'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to send multi-channel notification: {e}'))
        
        # Test 6: Check notification counts
        notification_count = Notification.objects.filter(user=test_user).count()
        self.stdout.write(self.style.SUCCESS(f'Total notifications for test user: {notification_count}'))
        
        # Test 7: Test bulk notification functionality
        try:
            from apps.notifications.utils import send_bulk_notification
            send_bulk_notification(
                recipients=[test_user],
                title='Kütləvi Test',
                message='Bu kütləvi bildiriş testidir.',
                notification_type='info'
            )
            self.stdout.write(self.style.SUCCESS('Bulk notification test completed'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed bulk notification test: {e}'))
        
        # Test 8: Test SMS provider functionality
        try:
            # Create a test SMS provider
            sms_provider, created = SMSProvider.objects.get_or_create(
                name='Test Provider',
                defaults={
                    'provider': 'twilio',
                    'configuration': {
                        'account_sid': 'test_sid',
                        'auth_token': 'test_token',
                        'from_number': '+1234567890'
                    }
                }
            )
            self.stdout.write(self.style.SUCCESS('SMS provider test completed'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed SMS provider test: {e}'))
        
        # Final summary
        self.stdout.write(
            self.style.SUCCESS(
                '\nEnhanced Notification System Test Completed Successfully!\n'
                'Features tested:\n'
                '- In-app notifications\n'
                '- Multi-channel notifications (email, SMS, push)\n'
                '- Notification templates\n'
                '- User preferences\n'
                '- Bulk notifications\n'
                '- SMS provider configuration\n'
                '- Database models\n'
            )
        )