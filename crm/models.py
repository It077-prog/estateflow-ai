from django.conf import settings
from django.db import models


class Lead(models.Model):
    class Status(models.TextChoices):
        NEW = "NEW", "New"
        CONTACTED = "CONTACTED", "Contacted"
        QUALIFIED = "QUALIFIED", "Qualified"
        VIEWING = "VIEWING", "Viewing"
        NEGOTIATION = "NEGOTIATION", "Negotiation"
        WON = "WON", "Won"
        LOST = "LOST", "Lost"

    class Source(models.TextChoices):
        WEBSITE = "WEBSITE", "Website"
        WHATSAPP = "WHATSAPP", "WhatsApp"
        REFERRAL = "REFERRAL", "Referral"
        PORTAL = "PORTAL", "Property Portal"
        SOCIAL = "SOCIAL", "Social Media"
        OTHER = "OTHER", "Other"
    ai_summary = models.TextField(blank=True)
    ai_follow_up = models.TextField(blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)

    source = models.CharField(
        max_length=20,
        choices=Source.choices,
        default=Source.OTHER,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
    )

    property_interest = models.CharField(
        max_length=255,
        blank=True,
    )

    budget = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_leads",
    )

    follow_up_date = models.DateField(
        null=True,
        blank=True,
    )

    ai_summary = models.TextField(blank=True)
    ai_follow_up = models.TextField(blank=True)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return (
            f"{self.first_name} {self.last_name}"
        ).strip()


class Note(models.Model):
    lead = models.ForeignKey(
        Lead,
        on_delete=models.CASCADE,
        related_name="notes",
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="lead_notes",
    )

    content = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Note for {self.lead}"


class Activity(models.Model):
    class ActivityType(models.TextChoices):
        CALL = "CALL", "Call"
        EMAIL = "EMAIL", "Email"
        WHATSAPP = "WHATSAPP", "WhatsApp"
        MEETING = "MEETING", "Meeting"
        STATUS_CHANGE = (
            "STATUS_CHANGE",
            "Status Change",
        )
        OTHER = "OTHER", "Other"

    lead = models.ForeignKey(
        Lead,
        on_delete=models.CASCADE,
        related_name="activities",
    )

    activity_type = models.CharField(
        max_length=20,
        choices=ActivityType.choices,
        default=ActivityType.OTHER,
    )

    description = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.get_activity_type_display()} "
            f"- {self.lead}"
        )