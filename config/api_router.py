from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from message_service.mailing.api.views import (
    ClientsViewSet,
    MailingViewSet,
    MessageViewSet,
)
from message_service.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("clients", ClientsViewSet, basename="clients")
router.register("mailing", MailingViewSet, basename="mailing-list")
router.register("messages", MessageViewSet, basename="message")


app_name = "api"
urlpatterns = router.urls
