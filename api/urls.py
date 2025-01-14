from django.urls import path, include  # NOQA: F401

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


urlpatterns = [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-docs"),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("users/", include("api.users.urls")),
    path("events/", include("api.events.urls")),
]
