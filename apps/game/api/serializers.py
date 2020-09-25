from rest_framework import serializers

from game.models import Player


class PlayerAPISerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Player
        fields = '__all__'
