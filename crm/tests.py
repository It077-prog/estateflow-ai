from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from .ai_service import AIServiceUnavailable
from .models import Lead


User = get_user_model()


class LeadAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="TestPassword123!",
        )

        self.client.force_authenticate(
            user=self.user
        )

        self.lead = Lead.objects.create(
            first_name="Sarah",
            last_name="Ahmed",
            email="sarah@example.com",
            phone="0501234567",
            source=Lead.Source.WEBSITE,
            status=Lead.Status.QUALIFIED,
            property_interest=(
                "2 Bedroom Apartment - Dubai Marina"
            ),
            budget=1800000,
            assigned_to=self.user,
        )

    def test_lead_list(self):
        url = reverse("api-lead-list")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            1,
        )

    def test_create_lead(self):
        url = reverse("api-lead-list")

        data = {
            "first_name": "Omar",
            "last_name": "Khan",
            "email": "omar@example.com",
            "phone": "0509876543",
            "source": "WHATSAPP",
            "status": "NEW",
            "property_interest": "Villa - Dubai Hills",
            "budget": "4500000.00",
            "assigned_to": self.user.id,
        }

        response = self.client.post(
            url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            Lead.objects.count(),
            2,
        )

    def test_filter_leads_by_status(self):
        url = reverse("api-lead-list")

        response = self.client.get(
            url,
            {
                "status": "QUALIFIED",
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            1,
        )

        self.assertEqual(
            response.data[0]["status"],
            "QUALIFIED",
        )

    def test_search_leads(self):
        url = reverse("api-lead-list")

        response = self.client.get(
            url,
            {
                "search": "Marina",
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            1,
        )

        self.assertEqual(
            response.data[0]["first_name"],
            "Sarah",
        )

    def test_lead_detail(self):
        url = reverse(
            "api-lead-detail",
            args=[self.lead.pk],
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["first_name"],
            "Sarah",
        )

    def test_update_lead(self):
        url = reverse(
            "api-lead-detail",
            args=[self.lead.pk],
        )

        response = self.client.patch(
            url,
            {
                "status": "VIEWING",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.lead.refresh_from_db()

        self.assertEqual(
            self.lead.status,
            Lead.Status.VIEWING,
        )

    def test_delete_lead(self):
        url = reverse(
            "api-lead-detail",
            args=[self.lead.pk],
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertEqual(
            Lead.objects.count(),
            0,
        )

    @patch("crm.api_views.generate_lead_summary")
    def test_generate_ai_summary(
        self,
        mock_generate_summary,
    ):
        mock_generate_summary.return_value = (
            "Sarah is a qualified buyer interested "
            "in a two-bedroom apartment in Dubai Marina."
        )

        url = reverse(
            "api-lead-ai-summary",
            args=[self.lead.pk],
        )

        response = self.client.post(
            url,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["summary"],
            mock_generate_summary.return_value,
        )

        self.lead.refresh_from_db()

        self.assertEqual(
            self.lead.ai_summary,
            mock_generate_summary.return_value,
        )

        mock_generate_summary.assert_called_once()

    @patch("crm.api_views.generate_follow_up")
    def test_generate_ai_follow_up(
        self,
        mock_generate_follow_up,
    ):
        mock_generate_follow_up.return_value = (
            "Hi Sarah, following up regarding your "
            "Dubai Marina property search."
        )

        url = reverse(
            "api-lead-ai-follow-up",
            args=[self.lead.pk],
        )

        response = self.client.post(
            url,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["follow_up"],
            mock_generate_follow_up.return_value,
        )

        self.lead.refresh_from_db()

        self.assertEqual(
            self.lead.ai_follow_up,
            mock_generate_follow_up.return_value,
        )

        mock_generate_follow_up.assert_called_once()

    @patch("crm.api_views.generate_lead_summary")
    def test_ai_summary_returns_503_when_provider_fails(
        self,
        mock_generate_summary,
    ):
        mock_generate_summary.side_effect = (
            AIServiceUnavailable(
                "The AI service is temporarily unavailable."
            )
        )

        url = reverse(
            "api-lead-ai-summary",
            args=[self.lead.pk],
        )

        response = self.client.post(
            url,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_503_SERVICE_UNAVAILABLE,
        )

        self.assertIn(
            "temporarily unavailable",
            response.data["detail"],
        )