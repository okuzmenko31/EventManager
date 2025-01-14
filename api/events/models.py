from django.db import models

from api.users.models import User


class Event(models.Model):
    title = models.CharField(max_length=255, verbose_name="Event title")
    description = models.TextField(verbose_name="Event description")
    date = models.DateTimeField(verbose_name="Event date")
    location = models.CharField(max_length=255, verbose_name="Event location")
    organizer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Event organizer",
        related_name="events",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Event: {self.title}. Date: {self.date}"



class EventRegistration(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        verbose_name="Event",
        related_name="registrations",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="User",
        related_name="event_registrations",
    )
    registered_at = models.DateTimeField(auto_now_add=True, verbose_name="Registered at")

    class Meta:
        db_table = "event_registration"
        verbose_name = "Event registration"
        verbose_name_plural = "Event registrations"
        ordering = ["-registered_at"]

    def __str__(self):
        return f"Event: {self.event.title}. User: {self.user.email}"
