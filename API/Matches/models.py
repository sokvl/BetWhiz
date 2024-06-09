from django.db import models

# Create your models here.
class Teams(models.Model):
    _id = models.AutoField(primary_key=True)
    team_name = models.TextField(unique=True)
    team_fullname = models.TextField(blank=True)
    team_abbreviation = models.TextField(blank=True)
    league = models.TextField(default='nba')
    discipline = models.TextField(default='basketball')

    class Meta:
        db_table = 'teams'


class GameData(models.Model):
    _id = models.AutoField(primary_key=True)
    outcome = models.BooleanField(null=True)
    home_team = models.ForeignKey(Teams, related_name='home_team_game', on_delete=models.CASCADE, default="")
    away_team = models.ForeignKey(Teams, related_name='away_team_game', on_delete=models.CASCADE, default="")
    home_team_score = models.IntegerField(blank=True, null=True)
    visitor_team_score = models.IntegerField(blank=True,  null=True)
    game_date = models.DateField()

    class Meta:
        db_table = 'games_data'
