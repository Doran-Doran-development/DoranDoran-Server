from django.db import models
from account.models import User
# Create your models here.

class Team(models.Model):
    team_id = models.AutoField(primary_key=True)
    project = models.CharField(max_length=50, blank=False)
    description = models.CharField(max_length=250, blank=False)
    teacher = models.ForeignKey('account.User', on_delete=models.SET_NULL)

    class Meta:
        ordering = ['team_id',]

    def __str__(self):
        return self.project

class LinkedTeamTable(models.Model):
    team_id = models.ForeignKey(primary_key=True, 'team.Team', on_delete=models.CASCADE)   
    email = models.ForeignKey(primary_key=True, 'account.User', on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['team_id',]
    def __str__(self):
        return self.team_id, self.email
    