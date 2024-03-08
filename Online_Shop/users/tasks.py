from celery import shared_task
from django.core.mail import send_mail
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_email_task(subject, message, from_email, recipient_list):
    try:
        send_mail(subject, message, from_email, recipient_list)
    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")