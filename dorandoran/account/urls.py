from django.urls import path, include
from .views import (
    RegistrationView,
    LoginView,
    SignOutView,
    RefreshJSONWebTokenView,
    MyUserInfoView,
    UserViewSet,
)

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"users", UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("sign-up", RegistrationView.as_view()),
    path("login", LoginView.as_view()),
    path("sign-out", SignOutView.as_view()),
    path("refresh", RefreshJSONWebTokenView.as_view()),
    path("my-info", MyUserInfoView.as_view()),
]
