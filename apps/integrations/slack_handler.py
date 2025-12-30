"""
Slack integration using both webhook and SDK approaches.
"""
import requests
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def send_dm_sdk(user_id=None, message="Hello from Django Webhook Service!"):
    """
    Send a direct message to a Slack user using Slack SDK.
    
    Args:
        user_id: Slack user ID (default: from settings)
        message: Message to send
    
    Returns:
        dict with status and response data
    """
    if user_id is None:
        user_id = settings.SLACK_DM_USER_ID
    
    if not settings.SLACK_BOT_TOKEN:
        raise ValueError("SLACK_BOT_TOKEN not configured in settings")
    
    try:
        # Initialize Slack client
        client = WebClient(token=settings.SLACK_BOT_TOKEN)
        
        # Send message to user via DM
        response = client.chat_postMessage(
            channel=user_id,
            text=message,
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": message
                    }
                }
            ]
        )
        
        logger.info(f"Message sent successfully to user {user_id}")
        
        return {
            'status': 'success',
            'message': 'Slack message sent via SDK',
            'channel': response['channel'],
            'timestamp': response['ts']
        }
        
    except SlackApiError as e:
        error_msg = f"Slack API error: {e.response['error']}"
        logger.error(error_msg)
        raise Exception(error_msg)
    except Exception as e:
        logger.error(f"Error sending Slack message: {str(e)}")
        raise


def send_dm_webhook(webhook_url=None, message="Hello from Django Webhook Service!"):
    """
    Send a message to Slack using an Incoming Webhook.
    Note: Webhooks post to a specific channel, not directly to users.
    
    Args:
        webhook_url: Slack webhook URL (default: from settings)
        message: Message to send
    
    Returns:
        dict with status
    """
    if webhook_url is None:
        webhook_url = settings.SLACK_WEBHOOK_URL
    
    if not webhook_url:
        raise ValueError("SLACK_WEBHOOK_URL not configured in settings")
    
    try:
        # Prepare webhook payload
        payload = {
            "text": message,
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": message
                    }
                }
            ]
        }
        
        # Send POST request to webhook
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
        
        logger.info(f"Message sent successfully via webhook")
        
        return {
            'status': 'success',
            'message': 'Slack message sent via webhook',
            'response': response.text
        }
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error sending webhook: {str(e)}")
        raise


def send_welcome_message(user_id=None):
    """
    Send a welcome message to a Slack user.
    This demonstrates using the SDK approach.
    """
    welcome_text = """
🎉 *Welcome to Django Webhook Event Service!*

This is an automated message to confirm that the Slack integration is working correctly.

*Features Available:*
• Webhook event receiving and processing
• JWT Authentication
• Celery background tasks
• Google Sheets integration
• GitHub backup system
• And more!

Have a great day! 🚀
    """
    
    return send_dm_sdk(user_id, welcome_text)


def send_webhook_notification(event_data):
    """
    Send a notification about a webhook event.
    Example of using webhook approach.
    """
    message = f"""
📨 *New Webhook Event Received*

*Source:* {event_data.get('source', 'Unknown')}
*Time:* {event_data.get('timestamp', 'N/A')}
*Status:* Processing...

Check the admin panel for more details.
    """
    
    try:
        return send_dm_webhook(message=message)
    except Exception as e:
        # Fallback to SDK if webhook fails
        logger.warning(f"Webhook failed, trying SDK: {str(e)}")
        return send_dm_sdk(message=message)

