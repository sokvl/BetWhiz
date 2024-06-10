from rest_framework import viewsets
from .models import Teams, GameData
from .serializers import TeamSerializer, GameDataSerializer
from django.db.models import Q

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Teams.objects.all()
    serializer_class = TeamSerializer

class GameDataViewSet(viewsets.ModelViewSet):
    queryset = GameData.objects.all()
    serializer_class = GameDataSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        discipline = self.request.query_params.get('discipline', None)
        if discipline is not None:
            queryset = queryset.filter(
                Q(home_team__discipline=discipline) | Q(away_team__discipline=discipline)
            )
        return queryset