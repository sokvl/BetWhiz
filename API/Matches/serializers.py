from rest_framework import serializers
from .models import Teams, GameData

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teams
        fields = '__all__'

        def __str__(self):
            return self.team_name

class GameDataSerializer(serializers.ModelSerializer):
    home_team = serializers.CharField(source='home_team.team_name')
    away_team = serializers.CharField(source='away_team.team_name')
    discipline = serializers.CharField(source='home_team.discipline')
    league = serializers.CharField(source='home_team.league')
    
    if not all([home_team, away_team, discipline, league]):
            raise serializers.ValidationError("Missing required fields")

    class Meta:
        model = GameData
        fields = [ '_id','outcome', 'home_team', 'away_team', 'home_team_score', 'visitor_team_score', 'game_date', 'discipline', 'league']

    def create(self, validated_data):
        home_team_name = validated_data.pop('home_team')
        away_team_name = validated_data.pop('away_team')
        discipline = home_team_name['discipline']
        league = home_team_name['league']

        home_team, created = Teams.objects.get_or_create(team_name=home_team_name['team_name'].split()[-1],team_fullname=home_team_name['team_name'], discipline=discipline, league=league)
        away_team, created = Teams.objects.get_or_create(team_name=away_team_name['team_name'].split()[-1],team_fullname=away_team_name['team_name'], discipline=discipline, league=league)

        game_data = GameData.objects.create(home_team=home_team, away_team=away_team, **validated_data)
        return game_data
