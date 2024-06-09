from rest_framework import viewsets
from .models import Teams, GameData
from .serializers import TeamSerializer, GameDataSerializer


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Teams.objects.all()
    serializer_class = TeamSerializer

class GameDataViewSet(viewsets.ModelViewSet):
    queryset = GameData.objects.all()
    serializer_class = GameDataSerializer