from django.db import models


class ReservationQueue(models.Model):
    room_id = models.ForeignKey(
        "room.Room", on_delete=models.CASCADE, db_column="room_id"
    )
    team_id = models.ForeignKey(
        "team.Team", on_delete=models.CASCADE, db_column="team_id"
    )
    status = models.IntegerField(default=0)
    reserve_time = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    reserver_id = models.ForeignKey(
        "account.User", on_delete=models.CASCADE, db_column="reserver_id"
    )

    class Meta:
        db_table = u"reservation_queue"
