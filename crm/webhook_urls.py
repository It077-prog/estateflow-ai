from django.urls import path

from .webhook_views import lead_webhook


urlpatterns = [
    path(
        "leads/",
        lead_webhook,
        name="lead-webhook",
    ),
]