from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from Matches.models import Teams, GameData
from Posts.models import TweetData
from Posts.serializers import SingleContentSerializer
from Modules.toolkit import model_manager

"""
params: 
home
away
date

"""

class PredictionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        home_team_name = request.GET.get('home')
        away_team_name = request.GET.get('away')
        match_date = request.GET.get('date')
        tweet_text = request.GET.get('tweet')

        if not home_team_name or not away_team_name or (not match_date and not tweet_text):
            return Response({'error': 'Missing parameters'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            home_team = Teams.objects.get(team_name=home_team_name)
        except Teams.DoesNotExist:
            return Response({'error': f'Home team "{home_team_name}" does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            away_team = Teams.objects.get(team_name=away_team_name)
        except Teams.DoesNotExist:
            return Response({'error': f'Away team "{away_team_name}" does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

        if tweet_text:
            # Perform prediction based on the provided tweet text
            print(tweet_text, home_team.team_name, away_team.team_name)
            prediction = model_manager.predict(home_team.team_name, away_team.team_name, tweet_text)
            outcome = home_team_name if prediction == 0 else away_team_name
            return Response({
                'prediction': f"Predicted winner: {outcome} "
            }, status=status.HTTP_200_OK)
        else:
            try:
                game = GameData.objects.get(home_team=home_team, away_team=away_team, game_date=match_date)
            except GameData.DoesNotExist:
                return Response({'error': 'Game you are looking for does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
            except GameData.MultipleObjectsReturned:
                game = GameData.objects.filter(home_team=home_team, away_team=away_team, game_date=match_date).first()

            tweets = TweetData.objects.filter(related_game=game)
            print(f"Found {tweets.count()} tweets related to the game")
            tweet_contents = [tweet.content_id for tweet in tweets]

            serializer = SingleContentSerializer(tweet_contents, many=True)
            predictions = [0, 0]
            for tweet in serializer.data:
                prediction = model_manager.predict(home_team_name, away_team_name, tweet['content'])
                predictions[prediction] += 1
            outcome = 0 if predictions[0] > predictions[1] else 1
            return Response({
                'prediction': f"Predicted winner: {home_team_name if outcome == 0 else away_team_name} [{(predictions[outcome] / tweets.count()) * 100}%]"
            }, status=status.HTTP_200_OK)