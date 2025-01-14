from django.contrib import admin

from .models import Event, EventRegistration


class EventRegistrationInline(admin.TabularInline):
    model = EventRegistration
    extra = 0


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "date",
        "location",
        "organizer",
        "created_at",
        "registrants_list",
    )
    search_fields = ("id", "title", "date", "location", "organizer__username")
    list_filter = ("date", "location", "organizer")
    empty_value_display = "-empty-"
    date_hierarchy = "date"
    readonly_fields = ("created_at",)
    fieldsets = (
        (None, {"fields": ("title", "description")}),
        ("Event info", {"fields": ("date", "location", "organizer")}),
        ("Additional info", {"fields": ("created_at",)}),
    )
    save_on_top = True
    save_as = True
    actions_on_top = True
    actions_on_bottom = False
    list_per_page = 10
    list_max_show_all = 100
    show_full_result_count = True
    list_select_related = ("organizer",)
    inlines = [EventRegistrationInline]

    def registrants_list(self, obj):
        # Get a list of registrants for this event
        registrations = obj.registrations.all()
        return ", ".join([registration.user.username for registration in registrations])

    registrants_list.short_description = "Registrants"


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ("id", "event__title", "user__email", "registered_at")
    list_filter = ("event", "user")
    search_fields = ("id", "user__username", "event__title")
    readonly_fields = ("registered_at",)
