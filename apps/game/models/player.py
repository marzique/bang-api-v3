from django.conf import settings
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from game.models import Game


class Player(models.Model):

    # CHOICES 
    class Role(models.TextChoices):
        SHERIFF = 'SH', 'Sheriff'
        RENEGADE = 'RE', 'Renegade'
        OUTLAW = 'OL', 'Outlaw'
        DEPUTY = 'DE', 'Deputy'
    
    class Character(models.TextChoices):
        BART = 'BC', 'Bart Cassidy'
        BLACK = 'BJ', 'Black Jack'
        CALAMITY = 'CJ', 'Calamity Janet'
        EL = 'EG', 'El Gringo'
        JESSE = 'JJ', 'Jesse Jones'
        JOURDONNAIS = 'JD', 'Jourdonnais'
        KIT = 'KC', 'Kit Carlson'
        LUCKY = 'LD', 'Lucky Duke'
        PAUL = 'PL', 'Paul Regret'
        PEDRO = 'PR', 'Pedro Ramirez'
        ROSE = 'RD', 'Rose Doolan'
        SID = 'SK', 'Sid Ketchum'
        SLAB = 'TK', 'Slab the Killer'
        SUZY = 'SL', 'Suzy Lafayette'
        VULTURE = 'VS', 'Vulture Sam'
        WILLY = 'WK', 'Willy the Kid'
    
    # FIELDS
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='players')
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=100)
    ready = models.BooleanField(default=False)
    role = models.CharField(max_length=2, choices=Role.choices, blank=True)
    character = models.CharField(max_length=2, choices=Character.choices, blank=True)
    slot = models.PositiveIntegerField(blank=True, null=True)
    health = models.PositiveIntegerField(
        blank=True, 
        null=True, 
        validators=[MaxValueValidator(5)]
    )
    alive = models.BooleanField(default=True)
    turn = models.BooleanField(default=False)
    action_needed = models.BooleanField(default=False)
    fired = models.BooleanField(default=False)


    def __str__(self):
        return f'[{self.role}] {self.name} ({self.health})'

    def assign_turn(self):
        prev_player = self.game.players.get(turn=True)
        prev_player.turn = False
        prev_player.action_needed = False
        prev_player.save()
        self.turn = True
        self.action_needed = True
        self.fired = False
        self.save()
        self.game.give_cards(self, 2)
    
    def get_enemies(self, alive=True):
        """Return list of enemies ordered by slot, first one is the one after you
        and last one is the one before."""

        room = self.room
        if alive:
            all_players = list(self.room.players.filter(alive=True).order_by('slot'))
        else:
            all_players = list(self.room.players.order_by('slot'))
        self_index = all_players.index(self)
        enemies_ordered = all_players[self_index+1:] + all_players[:self_index]
        return enemies_ordered

    def get_distance(self, enemy):
        """Return minimum distance between player and enemy, excluding dead enemies"""

        alive_players = list(self.room.players.filter(alive=True).order_by('slot'))
        idx1 = alive_players.index(self)
        idx2 = alive_players.index(enemy)
        distance = abs(idx1 - idx2)
        return min(len(alive_players) - distance, distance)
    
    @property
    def is_sheriff(self):
        return self.role == 'SH'
    
    def get_gun(self):
        try:
            return self.gun.card
        except ObjectDoesNotExist: 
            # enemy has no gun yet
            return None
    
    def heal(self, beer=True):
        """Add +1 to health if player has less then max possible health points,
        and more than 2 alive players in game for beer"""

        max_health_character = 4 # TODO: get from data.py
        max_health = max_health_character + 1 if self.is_sheriff else max_health_character
        if beer:
            can_heal = len(self.get_enemies(alive=True)) > 1
        else:
            can_heal = True
        if can_heal and self.health < max_health:
            self.health += 1
            self.save()