from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from .views import RoomViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"",RoomViewSet, basename="room")


urlpatterns = [
    url(r"^", include(router.urls)),
]