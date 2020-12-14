from rest_framework import serializers
from .models import ReservationQueue


class ReservationQueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationQueue
        exclude = ("reserver_id",)
