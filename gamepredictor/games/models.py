from django.db import models
from django.contrib.auth.admin import User


class GamesList(models.Model):
    id = models.AutoField(primary_key=True)
    game_date = models.DateField(blank=True, null=True)
    away_team = models.CharField(max_length=32, blank=True, null=True)
    away_team_score = models.IntegerField(blank=True, null=True)
    home_team = models.CharField(max_length=32, blank=True, null=True)
    home_team_score = models.IntegerField(blank=True, null=True)
    game_id = models.CharField(max_length=12, blank=True, null=True)
    overtime = models.CharField(max_length=2, blank=True, null=True)
    attendance = models.IntegerField(blank=True, null=True)


class GamePredictions(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User)
    game_id = models.CharField(max_length=12, blank=False, null=False)
    prediction = models.CharField(max_length=32, blank=False, null=False)
