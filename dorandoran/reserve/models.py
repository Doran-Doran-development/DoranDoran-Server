from django.db import models


class ReservationQueue(models.Model):
    room_id = models.ForeignKey("room.Room", on_delete=models.CASCADE)
    team_id = models.ForeignKey("team.Team", on_delete=models.CASCADE)
    status = models.IntegerField(default=0)
    reserve_time = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    reserver_id = models.ForeignKey("account.User", on_delete=models.CASCADE)

    class Meta:
        db_table = u"reservation_queue"

    def __str__():
        return team_id + "팀의 " + reserve_time + "교시 예약 요청"
