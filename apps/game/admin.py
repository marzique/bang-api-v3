from django.contrib import admin
from game.models import (Game, Player, Card, Hand, 
                         Effects, Gun, Deck, Discard)


class PlayerInline(admin.TabularInline):
    model = Player


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'slot', 'game', 'role', 'alive', 'ready')


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'players', 'started')

    inlines = [
        PlayerInline,
    ]

    def name(self, obj):
        return obj

    def players(self, obj):
        players = [player.name for player in obj.players.all()]
        return str(players)
    
    players.short_description = "Players"


cards_emojis = {
    'Spades': '♠',
    'Clubs': '♣',
    'Hearts': '♥',
    'Diamonds': '♦'
}

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('name', 'value_of_suit', 'card_type', 'storage')

    def value_of_suit(self, obj):
        emoji = cards_emojis[obj.get_suit_display()]
        return f'{obj.value} of {emoji}'

    def storage(self, obj):
        if obj.deck:
            return f'DECK: {obj.deck}'
        elif obj.discard:
            return f'DISCARD: {obj.discard}'
        elif obj.hand:
            return f'HAND: {obj.hand}'
        elif obj.effects:
            return f'HAND: {obj.effects}'
        elif obj.gun:
            return f'GUN: {obj.gun}'


admin.site.register(Hand)
admin.site.register(Effects)
admin.site.register(Gun)
admin.site.register(Deck)
admin.site.register(Discard)
