from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TeamViewSet, ReadOnlyTeamViewSet, MemberViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r"^", TeamViewSet, basename="team")
router.register(r"member", MemberViewSet, basename="member")
router.register(r"show", ReadOnlyTeamViewSet, basename="get_team")

urlpatterns = router.urls