from django.db import models
from Matches.models import GameData

# Create your models here.
class TweetContent(models.Model):
    content_id = models.AutoField(primary_key=True)
    content = models.TextField()

    class Meta:
        db_table = 'Tweets_contents'

class TweetData(models.Model):
    _id = models.AutoField(primary_key=True)
    tweet_date = models.DateField()
    content_id = models.OneToOneField(TweetContent, related_name="tweet_with_contents", on_delete=models.CASCADE,db_column="content_id")
    created_at = models.DateTimeField(auto_now=True)
    replyies = models.IntegerField(blank=True)
    retweets = models.IntegerField(blank=True)
    likes = models.IntegerField(blank=True)
    views = models.IntegerField(blank=True)
    related_game = models.ForeignKey(GameData, on_delete=models.CASCADE, db_column="related_game")

    class Meta:
        db_table = 'tweets_data'
    
    @staticmethod
    def get_content_outcome_pairs():
        return TweetData.objects.select_related('content_id', 'related_game').values('content_id__content', 'related_game__outcome')
    
