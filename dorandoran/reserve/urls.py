from django.conf.urls import url
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import ReservationViewSet


router = DefaultRouter()
router.register(r"", ReservationViewSet, basename="reserve")


urlpatterns = [
    url(r"^", include(router.urls)),
]
