from rest_framework.routers import DefaultRouter

from authorization.api import UserViewSet
from event.api import EventViewSet


router = DefaultRouter()

router.register(r"users", UserViewSet, basename="users")
router.register(r"events", EventViewSet, basename="events")
