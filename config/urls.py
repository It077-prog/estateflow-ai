from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path(
        "admin/",
        admin.site.urls,
    ),

    path(
        "api/webhooks/",
        include("crm.webhook_urls"),
    ),

    path(
        "api/",
        include("crm.api_urls"),
    ),

    path(
        "api-auth/",
        include("rest_framework.urls"),
    ),

    path(
        "",
        include("crm.urls"),
    ),

    path(
        "",
        include("django.contrib.auth.urls"),
    ),
]