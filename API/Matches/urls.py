from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TeamViewSet, GameDataViewSet

router = DefaultRouter()
router.register(r'games', GameDataViewSet)
router.register(r'teams', TeamViewSet)

urlpatterns = [
    path('', include(router.urls)),
]