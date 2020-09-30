from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from game.models import Game


@login_required
def lobby(request):
    context = {
        'games': Game.objects.all()
    }
    user = request.user
    if hasattr(user, 'player'):
        context['player'] = user.player
    
    return render(request, 'lobby.html', context)


@login_required
def game(request, id):
    return HttpResponse(f'TODO: GAME #{id}')
