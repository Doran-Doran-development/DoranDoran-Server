from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TeamViewSet, MemberViewSet, TeamDetailView

router = DefaultRouter()
router.register(r"member", MemberViewSet, basename="member")
router.register(r"", TeamViewSet, basename="team")

urlpatterns = [
    path("", include(router.urls)),
    path(r"detail/<int:pk>", TeamDetailView.as_view()),
]