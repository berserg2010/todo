from rest_framework.routers import DefaultRouter

from authorization.views import UserViewSet
from event.views import EventViewSet


router = DefaultRouter()

router.register(r"users", UserViewSet, basename="users")
router.register(r"events", EventViewSet, basename="events")
