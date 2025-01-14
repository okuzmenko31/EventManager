from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import EventViewSet, EventRegistrationViewSet


router = DefaultRouter()
router.register(r"", EventViewSet, basename="events")


urlpatterns = [
    path("", include(router.urls)),
    path(
        "registrations/by_event/list/<int:event_id>/",
        EventRegistrationViewSet.as_view({"get": "list"}),
        name="registration-by-event-list",
    ),
    path(
        "registrations/create/<int:event_id>/",
        EventRegistrationViewSet.as_view({"post": "create"}),
        name="event-registration-create",
    ),
    path(
        "registrations/get/<int:pk>/",
        EventRegistrationViewSet.as_view({"get": "retrieve"}),
        name="event-registration-detail",
    ),
    path(
        "registrations/update/<int:pk>/",
        EventRegistrationViewSet.as_view({"put": "update"}),
        name="event-registration-detail",
    ),
    path(
        "registrations/delete/<int:pk>/",
        EventRegistrationViewSet.as_view({"delete": "destroy"}),
        name="event-registration-detail",
    ),
]
