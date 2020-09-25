from django.urls import path

from game.api import endpoints


urlpatterns = [
    path('players/', endpoints.PlayerAPIView.as_view()),
]
