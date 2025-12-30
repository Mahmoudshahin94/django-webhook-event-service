from celery import shared_task
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)


@shared_task
def process_webhook_event(event_id):
    """
    Process a webhook event asynchronously.
    This is where you would add custom logic to handle different webhook types.
    """
    from .models import WebhookEvent
    
    try:
        event = WebhookEvent.objects.get(id=event_id)
        event.status = 'processing'
        event.save()
        
        logger.info(f"Processing webhook event {event_id} from {event.source}")
        
        # Add your custom processing logic here based on the source
        # For example:
        # if event.source == 'slack':
        #     handle_slack_webhook(event.payload)
        # elif event.source == 'stripe':
        #     handle_stripe_webhook(event.payload)
        
        # For now, just log the event
        logger.info(f"Webhook payload: {event.payload}")
        
        # Mark as completed
        event.status = 'completed'
        event.processed_at = timezone.now()
        event.save()
        
        logger.info(f"Successfully processed webhook event {event_id}")
        
    except WebhookEvent.DoesNotExist:
        logger.error(f"Webhook event {event_id} not found")
    except Exception as e:
        logger.error(f"Error processing webhook event {event_id}: {str(e)}")
        try:
            event = WebhookEvent.objects.get(id=event_id)
            event.status = 'failed'
            event.error_message = str(e)
            event.processed_at = timezone.now()
            event.save()
        except:
            pass

