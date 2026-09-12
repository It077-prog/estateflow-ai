from rest_framework.routers import DefaultRouter

from .api_views import (
    ActivityViewSet,
    LeadViewSet,
    NoteViewSet,
)


router = DefaultRouter()

router.register(
    "leads",
    LeadViewSet,
    basename="api-lead",
)

router.register(
    "notes",
    NoteViewSet,
    basename="api-note",
)

router.register(
    "activities",
    ActivityViewSet,
    basename="api-activity",
)


urlpatterns = router.urls
