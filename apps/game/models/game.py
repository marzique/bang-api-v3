import random 

from django.db import models, transaction
from django.db.models import Q

from game.constants import ROLES


class Game(models.Model):
    name = models.CharField(max_length=100, unique=True)
    started = models.BooleanField(default=False)

    def __str__(self):
        return f'Game #{self.pk}'

    @transaction.atomic
    def start_game(self):
        """Place players in table slots, give them random role & character.
        Set their health accordingly, sheriff gets +1 health and +2 cards for turn.
        TODO: get char health from dict, maybe sheriff will get +2 cards in other method"""

        # bypass circular import
        from game.models import Player
        
        players = list(self.players.all())
        random.shuffle(players)
        players_count = len(players)

        characters = random.sample([choice[0] for choice in Player.Character.choices], players_count)
        roles = ROLES[players_count]

        for i, player in enumerate(players):
            player.role = roles[i]
            player.character = characters[i]
            player.health = 4  # get from data.py later
            player.slot = i
            self.give_cards(player, player.health)
            if player.is_sheriff:
                player.health += 1
                player.turn = True
                player.action_needed = True
                player.reset_tab()
                self.give_cards(player, 2)
            player.save()
        
        self.started = True
        self.save()

    @transaction.atomic
    def give_cards(self, player, amount):
        """Transfer <amount> of top cards from room deck to player hand.
        refill_deck if needed."""

        deck_cards = self.deck.cards.all()
        if deck_cards.count() <= amount:
            self.refill_deck()
            deck_cards = self.deck.cards.all()

        cards = deck_cards[:amount]
        for card in cards:
            card.deck = None
            card.hand = player.hand
            card.save()

    @transaction.atomic
    def refill_deck(self):
        """Transfer all cards to deck except last"""

        last_of_discard = self.get_last_discard()
        if last_of_discard:
            discarded_except_last = self.discard.cards.exclude(id=last_of_discard.id).order_by('slot')
        else:
            discarded_except_last = self.discard.cards.all().order_by('slot')
        for card in discarded_except_last:
            card.discard = None
            card.deck = self.deck
            card.save()

    
    def get_last_discard(self):
        try:
            return self.discard.cards.latest('updated')
        except:
            return None
    
    def is_gameover(self):
        """Check if game is finished. Return queryset with winner/s,
        or False"""

        alive = self.players.filter(alive=True)
        if not alive.filter(role='SH').exists(): # sheriff dead
            if alive.count() == 1 and alive.filter(role='RE').exists(): # only renegade left
                return Player.objects.filter(role='RE')
            else:
                return Player.objects.filter(role='OL')
        # all bad guys dead:
        elif not alive.filter(role='OL').exists() and not alive.filter(role='RE').exists():
            return Player.objects.filter(Q(role='SH') | Q(role='DE'))
        else:
            return False
    
    def next_after(self, player):
        """Return alive player that is next after the one passed.
        for last player it's gonna be the first one in array of alive players.
        """

        alive = list(self.players.filter(alive=True).order_by('slot'))
        current_index = alive.index(player)
        next_index = (current_index + 1) % len(alive)
        return alive[next_index]
                