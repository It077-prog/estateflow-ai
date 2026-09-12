import secrets

from django.conf import settings

from rest_framework import status
from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Activity
from .serializers import LeadWebhookSerializer


@api_view(["POST"])
@permission_classes([AllowAny])
def lead_webhook(request):
    provided_secret = request.headers.get(
        "X-Webhook-Secret",
        "",
    )

    expected_secret = settings.WEBHOOK_SECRET

    if (
        not expected_secret
        or not provided_secret
        or not secrets.compare_digest(
            provided_secret,
            expected_secret,
        )
    ):
        return Response(
            {
                "detail": "Invalid webhook credentials.",
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )

    serializer = LeadWebhookSerializer(
        data=request.data
    )

    if not serializer.is_valid():
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    lead = serializer.save()

    Activity.objects.create(
        lead=lead,
        activity_type=Activity.ActivityType.OTHER,
        description=(
            "Lead created automatically "
            "through external webhook."
        ),
    )

    return Response(
        {
            "message": "Lead created successfully.",
            "lead_id": lead.id,
            "status": lead.status,
        },
        status=status.HTTP_201_CREATED,
    )