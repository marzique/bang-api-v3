import random

from django.db import models

from game.models import Player, Game
from game.constants import effects, actions, guns


class CardStorage(models.Model):
    player = models.OneToOneField(Player, on_delete=models.CASCADE)
    game = models.OneToOneField(Game, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class PlayerCardStorage(CardStorage):
    game = None

    class Meta:
        abstract = True

    def __str__(self):
        return self.player.name


class GameCardStorage(CardStorage):
    player = None

    class Meta:
        abstract = True

    def __str__(self):
        return self.game.name


class Hand(PlayerCardStorage):
    pass


class Effects(PlayerCardStorage):
    pass


class Gun(PlayerCardStorage):
    pass


class Deck(GameCardStorage):

    SUITS = ['SP', 'HE', 'DI', 'CL']
    VALUES = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

    def fill_deck(self):
        """Fill game's deck with 80 cards, actions, guns, effects. 
        Values and suits assigned randomly. Deck is shuffled"""

        all_cards = []

        for card_type, card_type_dict in enumerate([actions, effects, guns]):
            for cardname, values in card_type_dict.items():
                for _ in range(values['max']):
                    card = {
                        'name': cardname, 
                        'suit': random.choice(self.SUITS),
                        'value': random.choice(self.VALUES),
                        'action': values['action'],
                        'description': values['description'],
                        'deck': self
                    }
                    if card_type == 1:  # effect
                        card['card_type'] = 'EF'
                        card['checkable'] = values['checkable']
                    elif card_type == 2:  # gun
                        card['card_type'] = 'GU'
                        card['distance'] = values['distance']
                        card['unlimited'] = values['unlimited']
                    else: 
                        card['card_type'] = 'AC'
                    all_cards.append(card)

        random.shuffle(all_cards)
        for dic in all_cards:
            card = Card(**dic)
            card.save()


class Discard(GameCardStorage):
    pass


class Card(models.Model):

    class Suit(models.TextChoices):
        DIAMONDS = 'DI', 'Diamonds'
        HEARTS = 'HE', 'Hearts'
        CLUBS = 'CL', 'Clubs'
        SPADES = 'SP', 'Spades'

    class Value(models.TextChoices):
        TWO = '2', 'Two'
        THREE = '3', 'Three'
        FOUR = '4', 'Four'
        FIVE = '5', 'Five'
        SIX = '6', 'Six'
        SEVEN = '7', 'Seven'
        EIGHT = '8', 'Eight'
        NINE = '9', 'Nine'
        TEN = '10', 'Ten'
        JACK = 'J', 'Jack'
        QUEEN = 'Q', 'Queen'
        KING = 'K', 'King'
        ACE = 'A', 'Ace'

    class Action(models.TextChoices):
        SELF = 'SE', 'Self'
        PLAYER = 'PL', 'Player'
        ALL = 'AL', 'All'
    
    class CardType(models.TextChoices):
        GUN = 'GU', 'Gun'
        EFFECT = 'EF', 'Effect'
        ACTION = 'AC', 'Action'

    name = models.CharField(max_length=50)
    card_type = models.CharField(max_length=2, choices=CardType.choices)
    suit = models.CharField(max_length=2, choices=Suit.choices)
    value = models.CharField(max_length=2, choices=Value.choices)
    action = models.CharField(max_length=2, choices=Action.choices)
    description = models.TextField(blank=True)
    updated = models.DateTimeField(auto_now=True)
    selected = models.BooleanField(default=False)
    # if gun
    distance = models.PositiveIntegerField(blank=True, null=True)
    unlimited = models.BooleanField(null=True, default=None)
    # if effect
    checkable = models.BooleanField(null=True, default=None)
    # one of player storages
    hand = models.ForeignKey(Hand, related_name='cards', on_delete=models.CASCADE, null=True, blank=True)
    effects = models.ForeignKey(Effects, related_name='cards', on_delete=models.CASCADE, null=True, blank=True)
    gun = models.OneToOneField(Gun, on_delete=models.CASCADE, null=True, blank=True)
    # one of game storages
    deck = models.ForeignKey(Deck, related_name='cards', on_delete=models.CASCADE, null=True, blank=True)
    discard = models.ForeignKey(Discard, related_name='cards', on_delete=models.CASCADE, null=True, blank=True)
    

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ['-updated']

    def get_storage(self):
        return self.hand or self.gun or self.effects or self.deck or self.discard

    def to_discard(self):
        storage = self.get_storage()
        if storage.game:
            game = storage.game
        else:
            game = storage.player.game
        self.hand = None
        self.gun = None
        self.effects = None
        self.deck = None
        self.discard = game.discard
        self.selected = False
        self.save()