from rest_framework import serializers

from django.core.exceptions import ObjectDoesNotExist

from game.models import Player, Game, Card


class PlayerSerializer(serializers.ModelSerializer):
    hand = serializers.SerializerMethodField()
    effects = serializers.SerializerMethodField()
    gun = serializers.SerializerMethodField()

    class Meta:
        model = Player
        exclude = ('game', 'user', )

    def get_hand(self, obj):
        return CardSerializer(obj.hand.cards.all(), many=True).data

    def get_effects(self, obj):
        return CardSerializer(obj.effects.cards.all(), many=True).data

    def get_gun(self, obj):
        try:
            return CardSerializer(obj.gun.card).data
        except ObjectDoesNotExist:
            return None


class EnemySerializer(PlayerSerializer):
    hand = None
    
    class Meta:
        model = Player
        exclude = ('game', 'user', )


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        exclude = ('hand', 'discard', 'effects', 'gun', 'deck')


class GameStateSerializer(serializers.ModelSerializer):

    player = serializers.SerializerMethodField()
    enemies = serializers.SerializerMethodField()
    discard = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = '__all__'

    def get_player(self, obj):
        player = self._get_current_player()
        return PlayerSerializer(player).data

    def get_enemies(self, obj):
        player = self._get_current_player()
        enemies = player.get_enemies()
        return EnemySerializer(enemies, many=True).data

    def get_discard(self, obj):
        discard = obj.discard.cards.first()
        if discard:
            return CardSerializer(discard).data

    def _get_current_player(self):
        user = self.context['request'].user
        return user.player


class CreateUpdatePlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'name', )