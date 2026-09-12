from rest_framework import serializers

from .models import Activity, Lead, Note


class LeadSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(
        source="get_status_display",
        read_only=True,
    )

    source_display = serializers.CharField(
        source="get_source_display",
        read_only=True,
    )

    class Meta:
        model = Lead

        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "source",
            "source_display",
            "status",
            "status_display",
            "property_interest",
            "budget",
            "assigned_to",
            "follow_up_date",
            "ai_summary",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
"ai_follow_up",
            "ai_summary",
            "created_at",
            "updated_at",
        ]


class NoteSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(
        source="author.username",
        read_only=True,
    )

    class Meta:
        model = Note

        fields = [
            "id",
            "lead",
            "author",
            "author_username",
            "content",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "author",
            "author_username",
            "created_at",
        ]


class ActivitySerializer(serializers.ModelSerializer):
    activity_type_display = serializers.CharField(
        source="get_activity_type_display",
        read_only=True,
    )

    class Meta:
        model = Activity

        fields = [
            "id",
            "lead",
            "activity_type",
            "activity_type_display",
            "description",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
        ]
class LeadWebhookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead

        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "source",
            "property_interest",
            "budget",
            "follow_up_date",
        ]

        extra_kwargs = {
            "first_name": {
                "required": True,
            },
            "source": {
                "required": False,
            },
        }