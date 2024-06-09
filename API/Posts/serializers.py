from rest_framework import serializers
from .models import TweetContent, TweetData, GameData

class TweetContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TweetContent
        fields = '__all__'

class TweetDataSerializer(serializers.ModelSerializer):
    content_id = serializers.CharField()
    related_game = serializers.PrimaryKeyRelatedField(queryset=GameData.objects.all())

    class Meta:
        model = TweetData
        fields = '__all__'


    def create(self, validated_data):
        content = validated_data.pop('content_id')
        tweet_content, created = TweetContent.objects.get_or_create(content=content)
        tweet_data = TweetData.objects.create(content_id=tweet_content, **validated_data)
        return tweet_data

class ContentOutcomeSerializer(serializers.Serializer):
    content = serializers.CharField()
    outcome = serializers.IntegerField()
    home = serializers.CharField()
    away = serializers.CharField()

class SingleContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TweetContent
        fields = ['content']