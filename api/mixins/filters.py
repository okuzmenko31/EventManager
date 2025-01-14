from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


class FilterMixin:
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    def apply_filters(self, queryset):
        """
        Apply filters, search, and ordering to the provided queryset.
        """
        for backend in self.filter_backends:
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset
