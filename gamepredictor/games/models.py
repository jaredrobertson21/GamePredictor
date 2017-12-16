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

    def winner(self):
        if self.away_team_score:
            if self.away_team_score > self.home_team_score:
                return self.away_team
            else:
                return self.home_team
        return "Game has not yet been played"

    def is_overtime(self):
        if self.overtime != '':
            return True
        return False


class GamePredictions(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User)
    game_date = models.DateField(null=False)
    game_id = models.CharField(max_length=12, blank=False, null=False)
    prediction = models.CharField(max_length=32, blank=False, null=False)


class TeamStats(models.Model):
    id = models.AutoField(primary_key=True)
    team = models.CharField(max_length=32, blank=False, null=False)
    year = models.CharField(max_length=7, blank=False, null=False)
    wins = models.IntegerField()
    losses = models.IntegerField()
    otl = models.IntegerField()
    streak = models.CharField(max_length=3)
    logo = models.ImageField(upload_to="static/logos")


class UserStats(models.Model):
    id = models.OneToOneField(User, primary_key=True)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    otl = models.IntegerField(default=0)
