from rest_framework import viewsets
from .models import Teams, GameData
from .serializers import TeamSerializer, GameDataSerializer
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Teams.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]


class GameDataViewSet(viewsets.ModelViewSet):
    queryset = GameData.objects.all()
    serializer_class = GameDataSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        queryset = super().get_queryset()
        discipline = self.request.query_params.get('discipline', None)
        order = self.request.query_params.get('order', None)  # 'asc' for ascending, 'desc' for descending
        limit = self.request.query_params.get('limit', None)

        if discipline is not None:
            queryset = queryset.filter(
                Q(home_team__discipline=discipline) | Q(away_team__discipline=discipline)
            )
        
        if order in ['asc', 'desc']:
            ordering = 'game_date' if order == 'asc' else '-game_date'
            queryset = queryset.order_by(ordering)
        
        if limit is not None:
            try:
                limit = int(limit)
                queryset = queryset[:limit]
            except ValueError:
                pass  # ignore if limit is not a valid integer

        return queryset