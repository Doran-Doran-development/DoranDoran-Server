from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .views import TeamViewSet

router = DefaultRouter()
router.register(r"", TeamViewSet, basename="team")

urlpatterns = [
    url(r"^", include(router.urls)),
]