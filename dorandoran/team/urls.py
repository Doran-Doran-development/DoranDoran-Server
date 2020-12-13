from django.conf.urls import url, include
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import TeamViewSet, ReadOnlyTeamViewSet, MemberViewSet

router = DefaultRouter()
router.register(r"", TeamViewSet, basename="team")
router.register(r"show", ReadOnlyTeamViewSet, basename="get_team")
router.register(r"member", MemberViewSet, basename="member")

urlpatterns = [
    url("", include(router.urls)),
]
