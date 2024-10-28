import logging
from celery import shared_task
from django.core.mail import send_mail
from .models import Booking  # Make sure to adjust the import based on your actual models.py location

logger = logging.getLogger(__name__)

@shared_task
def send_booking_email(booking_id, email,event_name):
    logger.info(f'Sending email for booking ID {booking_id} to {email}')
    try:
        # Fetch the booking details from the database
        booking = Booking.objects.get(id=booking_id)

        # Prepare the email content
        event_name = booking.event_name  # Assuming you have an event_name field in your Booking model
        email_subject = 'Thank you for your booking'
        email_body = f'Thank you for your booking of "{event_name}" (Booking ID: {booking_id}). We will contact you soon with further information.'

        # Send the email
        send_mail(
            email_subject,
            email_body,
            'lulu.umaira@gmail.com',  # Sender email
            [email],  # Recipient email
            fail_silently=False,
        )
        logger.info('Email sent successfully')
    except Booking.DoesNotExist:
        logger.error(f'Booking with ID {booking_id} does not exist.')
    except Exception as e:
        logger.error(f'Error sending email: {e}')




