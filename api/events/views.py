from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Event, EventRegistration
from .serializers import EventSerializer, EventRegistrationSerializer
from .filters import EventRegistrationFilter
from .tasks import send_event_registration_mail

from ..mixins.filters import FilterMixin


class EventViewSet(FilterMixin, viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["date", "location", "organizer"]
    search_fields = ["title", "description", "organizer__email", "organizer__username"]
    ordering_fields = ["date", "created_at"]

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

    def get_queryset(self):
        queryset = (
            super()
            .get_queryset()
            .select_related("organizer")
            .prefetch_related("registrations__user")
        )

        if self.action in ["create", "update", "destroy"]:
            queryset = queryset.filter(organizer=self.request.user)

        return self.apply_filters(queryset)

    @action(detail=False, methods=["get"], url_path="user_registered_events")
    def user_registered_events(self, request):
        """
        Custom action to get events that the logged-in user is registered for.
        """
        user = request.user
        registered_events = (
            Event.objects.select_related("organizer")
            .prefetch_related("registrations__user")
            .filter(registrations__user=user)
        )
        events = self.apply_filters(registered_events)
        serializer = self.get_serializer(events, many=True)
        return Response(serializer.data)


class EventRegistrationViewSet(FilterMixin, viewsets.ModelViewSet):
    queryset = EventRegistration.objects.all()
    serializer_class = EventRegistrationSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = EventRegistrationFilter
    search_fields = [
        "event__title",
        "user__email",
        "event__organizer__email",
        "event__organizer__username",
    ]

    def perform_create(self, serializer):
        event_id = self.kwargs.get("event_id")
        event = Event.objects.get(id=event_id)
        send_event_registration_mail.delay(
            self.request.user.email,
            event.title,
            event.date,
            event.description,
            event.location,
        )
        serializer.save(user=self.request.user, event=event)

    def get_queryset(self):
        queryset = EventRegistration.objects.select_related("user", "event__organizer")
        queryset = queryset.filter(user=self.request.user)
        return self.apply_filters(queryset)

    @action(detail=False, methods=["get"], url_path="by_event/(?P<event_id>\\d+)")
    def registrations_by_event(self, request, event_id=None):
        event = Event.objects.filter(id=event_id).first()
        if not event:
            return Response({"error": "Event not found."}, status=status.HTTP_400_BAD_REQUEST)

        registrations = EventRegistration.objects.select_related("user", "event__organizer").filter(
            event=event, user=self.request.user
        )
        registrations = self.apply_filters(registrations)

        serializer = self.get_serializer(registrations, many=True)
        return Response(serializer.data)
