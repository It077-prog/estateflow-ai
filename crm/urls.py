from django.urls import path

from . import views


urlpatterns = [
    path(
        "",
        views.lead_list,
        name="lead_list",
    ),
path(
    "dashboard/",
    views.dashboard,
    name="dashboard",
),
    path(
        "leads/new/",
        views.lead_create,
        name="lead_create",
    ),

    path(
        "leads/<int:pk>/",
        views.lead_detail,
        name="lead_detail",
    ),
path(
    "leads/<int:pk>/ai-summary/",
    views.generate_summary,
    name="generate_summary",
),

path(
    "leads/<int:pk>/ai-follow-up/",
    views.generate_ai_follow_up,
    name="generate_ai_follow_up",
),
    path(
        "leads/<int:pk>/edit/",
        views.lead_edit,
        name="lead_edit",
    ),

    path(
        "leads/<int:pk>/delete/",
        views.lead_delete,
        name="lead_delete",
    ),
path(
    "leads/<int:pk>/notes/new/",
    views.note_create,
    name="note_create",
),

path(
    "leads/<int:pk>/activities/new/",
    views.activity_create,
    name="activity_create",
),
]