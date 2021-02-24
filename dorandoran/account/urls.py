from django.urls import path, include
from .views import LoginView, RefreshJSONWebTokenView, UserViewSet, CurrentUserView

from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)
router.register(r"users", UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("login", LoginView.as_view()),
    path("refresh", RefreshJSONWebTokenView.as_view()),
    path("check", CurrentUserView.as_view()),
]
