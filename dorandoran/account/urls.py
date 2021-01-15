from django.urls import path, include
from .views import (
    LoginView,
    RefreshJSONWebTokenView,
    UserViewSet,
)

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"users", UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("login", LoginView.as_view()),
    path("refresh", RefreshJSONWebTokenView.as_view()),
]
