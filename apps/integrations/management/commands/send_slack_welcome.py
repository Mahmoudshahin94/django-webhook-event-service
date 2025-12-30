"""
Management command to send Slack welcome message.
Usage: python manage.py send_slack_welcome
"""
from django.core.management.base import BaseCommand
from django.conf import settings
from apps.integrations.slack_handler import send_welcome_message, send_dm_webhook


class Command(BaseCommand):
    help = 'Send welcome message via Slack (both SDK and webhook approaches)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--user-id',
            type=str,
            default=None,
            help='Slack user ID (default: from settings)'
        )
        parser.add_argument(
            '--method',
            type=str,
            choices=['sdk', 'webhook', 'both'],
            default='both',
            help='Method to use: sdk, webhook, or both'
        )

    def handle(self, *args, **options):
        user_id = options['user_id'] or settings.SLACK_DM_USER_ID
        method = options['method']
        
        if method in ['sdk', 'both']:
            self.stdout.write(self.style.WARNING('Sending message via Slack SDK...'))
            try:
                result = send_welcome_message(user_id)
                self.stdout.write(self.style.SUCCESS('✓ Message sent via SDK'))
                self.stdout.write(f"  Channel: {result['channel']}")
                self.stdout.write(f"  Timestamp: {result['timestamp']}")
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'✗ SDK Error: {str(e)}'))
                if method == 'sdk':
                    raise
        
        if method in ['webhook', 'both']:
            self.stdout.write(self.style.WARNING('Sending message via Slack Webhook...'))
            try:
                welcome_text = "🎉 Welcome from Django Webhook Service (via Webhook)!"
                result = send_dm_webhook(message=welcome_text)
                self.stdout.write(self.style.SUCCESS('✓ Message sent via Webhook'))
                self.stdout.write(f"  Response: {result['response']}")
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'✗ Webhook Error: {str(e)}'))
                if method == 'webhook':
                    raise

