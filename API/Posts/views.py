from rest_framework import viewsets, status
from .models import TweetContent, TweetData
from .serializers import TweetContentSerializer, TweetDataSerializer, ContentOutcomeSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import F, Q
from rest_framework.permissions import IsAuthenticated


class TweetContentViewSet(viewsets.ModelViewSet):
    queryset = TweetContent.objects.all()
    serializer_class = TweetContentSerializer
    permission_classes = [IsAuthenticated]


class TweetDataViewSet(viewsets.ModelViewSet):
    queryset = TweetData.objects.all()
    serializer_class = TweetDataSerializer
    permission_classes = [IsAuthenticated]


class ContentOutcomeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ContentOutcomeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        limit = self.request.query_params.get('limit', None)
        discipline = self.request.query_params.get('discipline', None)
        
        queryset = TweetData.objects.select_related('content_id', 'related_game').annotate(
            content=F('content_id__content'),
            outcome=F('related_game__outcome'),
            home=F('related_game__home_team__team_name'),
            away=F('related_game__away_team__team_name')
        ).exclude(
            #For model testing purposes only!!!
            related_game__in=[3903, 3902, 3904, 1852, 1850, 204, 203, 205, 197, 199]
        ).values('content', 'outcome', 'home', 'away')
        
        if discipline:
            queryset = queryset.filter(
                Q(related_game__home_team__discipline=discipline) | Q(related_game__away_team__discipline=discipline)
            )
        
        if limit is not None:
            try:
                limit = int(limit)
                queryset = queryset[:limit]
            except ValueError:
                pass
        
        return queryset