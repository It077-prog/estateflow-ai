from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (
    filters,
    permissions,
    status,
    viewsets,
)
from rest_framework.decorators import action
from rest_framework.response import Response

from .ai_service import (
    AIServiceUnavailable,
    generate_follow_up,
    generate_lead_summary,
)
from .models import Activity, Lead, Note
from .serializers import (
    ActivitySerializer,
    LeadSerializer,
    NoteSerializer,
)


class LeadViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.all().order_by("-created_at")
    serializer_class = LeadSerializer

    permission_classes = [
        permissions.IsAuthenticated,
    ]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = [
        "status",
        "source",
        "assigned_to",
        "follow_up_date",
    ]

    search_fields = [
        "first_name",
        "last_name",
        "email",
        "phone",
        "property_interest",
    ]

    ordering_fields = [
        "created_at",
        "updated_at",
        "follow_up_date",
        "budget",
        "first_name",
        "last_name",
    ]

    ordering = [
        "-created_at",
    ]

    @action(
        detail=True,
        methods=["post"],
        url_path="ai-summary",
    )
    def ai_summary(self, request, pk=None):
        lead = self.get_object()

        try:
            summary = generate_lead_summary(
                lead
            )

        except AIServiceUnavailable as exc:
            return Response(
                {
                    "detail": str(exc),
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        lead.ai_summary = summary

        lead.save(
            update_fields=[
                "ai_summary",
                "updated_at",
            ]
        )

        return Response(
            {
                "lead_id": lead.id,
                "summary": summary,
            }
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="ai-follow-up",
    )
    def ai_follow_up(self, request, pk=None):
        lead = self.get_object()

        try:
            follow_up = generate_follow_up(
                lead
            )

        except AIServiceUnavailable as exc:
            return Response(
                {
                    "detail": str(exc),
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        lead.ai_follow_up = follow_up

        lead.save(
            update_fields=[
                "ai_follow_up",
                "updated_at",
            ]
        )

        return Response(
            {
                "lead_id": lead.id,
                "follow_up": follow_up,
            }
        )


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all().order_by("-created_at")
    serializer_class = NoteSerializer

    permission_classes = [
        permissions.IsAuthenticated,
    ]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
    ]

    filterset_fields = [
        "lead",
        "author",
    ]

    search_fields = [
        "content",
    ]

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user
        )


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all().order_by("-created_at")
    serializer_class = ActivitySerializer

    permission_classes = [
        permissions.IsAuthenticated,
    ]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = [
        "lead",
        "activity_type",
    ]

    search_fields = [
        "description",
    ]

    ordering_fields = [
        "created_at",
    ]

    ordering = [
        "-created_at",
    ]