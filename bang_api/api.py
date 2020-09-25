from django.urls import path, include


urlpatterns = [
    path('players/', include('game.api.urls')),
]