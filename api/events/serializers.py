import datetime

from rest_framework import serializers

from .models import Event, EventRegistration
from ..users.serializers import UserSerializer


class EventRegistrationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = EventRegistration
        fields = ["id", "event", "user", "registered_at"]


class EventSerializer(serializers.ModelSerializer):
    organizer = UserSerializer(read_only=True)
    registrations = EventRegistrationSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = ["id", "title", "description", "date", "location", "organizer", "registrations"]


class EventRegistrationSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = EventRegistration
        fields = "__all__"
        read_only_fields = ["id", "event", "user", "registered_at"]

    def validate_event(self, value):
        """Ensure the event exists and is in the future."""
        if value.date < datetime.datetime.now(datetime.timezone.utc):
            raise serializers.ValidationError("Event has already passed.")
        return value

    def create(self, validated_data):
        """Automatically associate the logged-in user with the registration."""
        user = self.context["request"].user  # Access the logged-in user
        event = validated_data["event"]

        # Ensure the user isn't already registered for this event
        if EventRegistration.objects.filter(user=user, event=event).exists():
            raise serializers.ValidationError("You are already registered for this event.")

        # Check if the user is the organizer of the event
        if event.organizer == user:
            raise serializers.ValidationError(
                "You cannot register for your own event as you are the organizer."
            )

        # Create the event registration
        registration = EventRegistration.objects.create(user=user, event=event)
        return registration
