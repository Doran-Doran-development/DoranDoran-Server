from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from .views import ReservationViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"", ReservationViewSet, basename="reserve")


urlpatterns = [
    url(r"^", include(router.urls)),
]