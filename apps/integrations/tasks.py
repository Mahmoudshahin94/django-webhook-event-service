from celery import shared_task
import logging

logger = logging.getLogger(__name__)


@shared_task
def backup_to_github_task():
    """
    Celery task to backup processes to GitHub.
    This is scheduled to run daily via Celery Beat.
    """
    from .github_backup import backup_processes_to_github
    
    try:
        logger.info("Starting scheduled GitHub backup...")
        result = backup_processes_to_github()
        logger.info(f"GitHub backup completed: {result}")
        return result
    except Exception as e:
        logger.error(f"GitHub backup failed: {str(e)}")
        raise


@shared_task
def send_slack_message_task(user_id, message):
    """
    Celery task to send Slack message asynchronously.
    """
    from .slack_handler import send_dm_sdk
    
    try:
        logger.info(f"Sending Slack message to {user_id}...")
        result = send_dm_sdk(user_id, message)
        logger.info(f"Slack message sent: {result}")
        return result
    except Exception as e:
        logger.error(f"Failed to send Slack message: {str(e)}")
        raise


@shared_task
def write_to_gsheet_task(data, sheet_name, worksheet_name='Sheet1'):
    """
    Celery task to write data to Google Sheet asynchronously.
    """
    from .google_sheets import write_to_sheet
    
    try:
        logger.info(f"Writing data to Google Sheet: {sheet_name}...")
        result = write_to_sheet(data, sheet_name, worksheet_name)
        logger.info(f"Data written to Google Sheet: {result}")
        return result
    except Exception as e:
        logger.error(f"Failed to write to Google Sheet: {str(e)}")
        raise

