from django.urls import path

from game.api import endpoints


urlpatterns = [
    # API ENDPOINT URLS
    path('players/', endpoints.PlayerAPIView.as_view()),
]
