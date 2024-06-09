from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import  TweetContentViewSet, TweetDataViewSet, ContentOutcomeViewSet
router = DefaultRouter()
router.register(r'tweets', TweetDataViewSet)
router.register(r'tweet-contents', TweetContentViewSet)
router.register(r'dataset', ContentOutcomeViewSet, basename='dataset')

urlpatterns = [
    path('', include(router.urls)),
]