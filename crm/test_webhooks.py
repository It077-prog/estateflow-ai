from django.test import override_settings
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Activity, Lead


@override_settings(
    WEBHOOK_SECRET="test-webhook-secret"
)
class LeadWebhookTests(APITestCase):

    def setUp(self):
        self.url = reverse("lead-webhook")

        self.valid_payload = {
            "first_name": "Layla",
            "last_name": "Hassan",
            "email": "layla@example.com",
            "phone": "0505551234",
            "source": "WEBSITE",
            "property_interest": (
                "3 Bedroom Villa - Dubai Hills"
            ),
            "budget": "5200000.00",
        }

    def test_webhook_rejects_invalid_secret(self):
        response = self.client.post(
            self.url,
            self.valid_payload,
            format="json",
            HTTP_X_WEBHOOK_SECRET="wrong-secret",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

        self.assertEqual(
            Lead.objects.count(),
            0,
        )

    def test_webhook_creates_lead(self):
        response = self.client.post(
            self.url,
            self.valid_payload,
            format="json",
            HTTP_X_WEBHOOK_SECRET=(
                "test-webhook-secret"
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            Lead.objects.count(),
            1,
        )

        lead = Lead.objects.get()

        self.assertEqual(
            lead.first_name,
            "Layla",
        )

        self.assertEqual(
            lead.status,
            Lead.Status.NEW,
        )

        self.assertEqual(
            response.data["lead_id"],
            lead.id,
        )

    def test_webhook_creates_activity(self):
        response = self.client.post(
            self.url,
            self.valid_payload,
            format="json",
            HTTP_X_WEBHOOK_SECRET=(
                "test-webhook-secret"
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        lead = Lead.objects.get()

        activity = Activity.objects.get(
            lead=lead
        )

        self.assertEqual(
            activity.activity_type,
            Activity.ActivityType.OTHER,
        )

        self.assertIn(
            "external webhook",
            activity.description,
        )