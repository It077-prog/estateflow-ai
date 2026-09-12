from django.contrib import admin

from .models import Activity, Lead, Note


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "status",
        "source",
        "budget",
        "follow_up_date",
        "assigned_to",
        "created_at",
    )

    list_filter = (
        "status",
        "source",
        "created_at",
        "follow_up_date",
    )

    search_fields = (
        "first_name",
        "last_name",
        "email",
        "phone",
        "property_interest",
    )


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = (
        "lead",
        "author",
        "created_at",
    )

    search_fields = (
        "lead__first_name",
        "lead__last_name",
        "content",
    )


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = (
        "lead",
        "activity_type",
        "created_at",
    )

    list_filter = (
        "activity_type",
        "created_at",
    )

    search_fields = (
        "lead__first_name",
        "lead__last_name",
        "description",
    )