# reminder/tasks.py
import logging
from celery import shared_task
from django.core.mail import send_mail
from twilio.rest import Client
from django.conf import settings
from .models import Reminder
from datetime import datetime

logger = logging.getLogger(__name__)

# @shared_task(bind=True)
# def send_reminder_message(self, reminder_id):
#     logger.info(f"Executing send_reminder_message for reminder_id={reminder_id}")
#     try:
#         reminder = Reminder.objects.get(id=reminder_id)
#         print(f"Reminder time: {reminder.remind_at}")
        
#         if reminder.remind_via == 'SMS':
#             send_sms(reminder.phone_number, reminder.message)
#         elif reminder.remind_via == 'Email':
#             send_email(reminder.email, reminder.message)

#         return "Done"
#     except Exception as e:
#         logger.error(f"Task failed: {str(e)}", exc_info=True)
#         self.retry(exc=e, countdown=60, max_retries=3)
@shared_task
def send_reminder_message(reminder_id):
    try:
        logger.info(f"Executing send_reminder_message for reminder_id={reminder_id}")
        reminder = Reminder.objects.get(id=reminder_id)
        logger.info(f"Reminder is set for: {reminder.remind_at}")
        if reminder.remind_via == 'SMS':
            send_sms(reminder.phone_number, reminder.message)
        elif reminder.remind_via == 'Email':
            send_email(reminder.email, reminder.message)
        
        logger.info("Reminder sent successfully.")
        return "Done"
    
    except Exception as e:
        logger.error(f"Error in send_reminder_message: {str(e)}", exc_info=True)
        return "Failed"


def send_sms(phone_number, message):
    # Twilio settings (ensure to replace these with your actual Twilio credentials)
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    from_phone = settings.TWILIO_PHONE_NUMBER  # Your Twilio phone number
    
    client = Client(account_sid, auth_token)
    client.messages.create(
        to=phone_number,
        from_=from_phone,
        body=message
    )

def send_email(email, message):
    # Use Django's built-in send_mail function
    send_mail(
        'Reminder from Remind Me Later',
        message,
        'bikashsharma5151@gmail.com',
        [email],
        fail_silently=False,
    )
