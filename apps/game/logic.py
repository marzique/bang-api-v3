"""All game logic"""

import json
import random

from django.db import transaction

from game.models import Game, Player, Card, Hand, Effects, Gun, Deck, Discard


class GameLogic:
    """"""

    @staticmethod
    @transaction.atomic
    def player_join_game(player, game):
        """Add player to game, create card storages for him"""

        player.game = game
        player.save()
        Hand(player=player).save()
        Effects(player=player).save()
        Gun(player=player).save()
    
    @staticmethod
    @transaction.atomic
    def create_game(name):
        """Create game and it's decks"""

        game = Game(name=name)
        game.save()
        deck = Deck(game=game)
        deck.save()
        deck.fill_deck()
        Discard(game=game).save()
        return game

game_logic = GameLogic()
