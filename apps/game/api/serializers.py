from rest_framework import serializers

from game.models import Player, Game


class GameStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game

class PlayerAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'
