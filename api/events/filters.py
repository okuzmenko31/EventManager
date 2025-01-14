from django_filters.rest_framework import FilterSet, NumberFilter, DateTimeFromToRangeFilter
from .models import EventRegistration


class EventRegistrationFilter(FilterSet):
    event_id = NumberFilter(field_name="event__id", lookup_expr="exact")
    user_id = NumberFilter(field_name="user__id", lookup_expr="exact")
    registered_at = DateTimeFromToRangeFilter(field_name="registered_at")

    class Meta:
        model = EventRegistration
        fields = ["event_id", "user_id", "registered_at"]
