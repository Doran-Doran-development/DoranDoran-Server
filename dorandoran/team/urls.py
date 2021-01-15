from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TeamViewSet, TeamDetailAPI, MemberViewSet, TeamListAPI

router = DefaultRouter()
router.register(r"", TeamViewSet, basename="team")
router.register(r"member", MemberViewSet, basename="member")

urlpatterns = [
    url(r"^", include(router.urls)),
    path(r"show/", TeamListAPI.as_view()),
    path(r"show/<pk>", TeamDetailAPI.as_view())
]