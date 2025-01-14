from celery import app

from django.conf import settings
from django.core.mail import send_mail


@app.shared_task
def send_event_registration_mail(email, event_title, event_date, description, location):
    send_mail(
        "Event Manager event registration",
        f"Event: {event_title}\nDate: {event_date}\nDescription: {description}\nLocation: {location}",
        settings.EMAIL_HOST_USER,
        [email],
    )
