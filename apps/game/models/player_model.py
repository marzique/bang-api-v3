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
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=2, choices=Role.choices, blank=True)
    slot = models.PositiveIntegerField(blank=True, null=True)
    character = models.CharField(max_length=2, choices=Character.choices, blank=True)
    health = models.PositiveIntegerField(
        blank=True, 
        null=True, 
        validators=[MaxValueValidator(5)]
    )


    def __str__(self):
        return f'[{self.role}] {self.name} ({self.health})'
