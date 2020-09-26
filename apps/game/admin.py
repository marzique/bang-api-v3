from django.contrib import admin
from game.models import Game, Player


@admin.register(Player)
class Player(admin.ModelAdmin):
    list_display = ('name', 'role', 'character', 'health')


@admin.register(Game)
class Player(admin.ModelAdmin):
    pass
