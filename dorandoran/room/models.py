from django.db import models


class Room(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=255)
    max_team = models.IntegerField()
    owner = models.ForeignKey("account.User", on_delete=models.SET_NULL, null=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Room"