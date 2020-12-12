from django.conf.urls import url, include
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import TeamViewSet, ReadOnlyTeamViewSet

router = DefaultRouter()
router.register(r"", TeamViewSet, basename="team")
router.register(r"show", ReadOnlyTeamViewSet, basename="get_team")

urlpatterns = [
    url("", include(router.urls)),
]
