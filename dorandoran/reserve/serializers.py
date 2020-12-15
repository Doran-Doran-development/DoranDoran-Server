from rest_framework import serializers
from .models import ReservationQueue
from account.serializers import UserSerializer
from django.utils.translation import ugettext as _


class ReservationQueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationQueue
        fields = "__all__"
        extra_kwargs = {"reserver_id": {"required": False}}

    
    def create(self, validated_data):
        self.validate_duplicate_reservation(validated_data)

        instance = ReservationQueue.objects.create(**validated_data)
        return instance

    # validate if reservation duplicated
    def validate_duplicate_reservation(self, data):
        exist_reservation = ReservationQueue.objects.filter(
            room_id=data["room_id"], team_id=data["team_id"]
        )

        if exist_reservation is not None:
            msg = _("room_id is already reserved by your team")
            raise serializers.ValidationError(msg)