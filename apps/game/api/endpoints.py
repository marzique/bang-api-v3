
import io
import csv
import datetime
from dateutil import parser

from django.db.models import Sum
from django.http import HttpResponse
from django.db import IntegrityError, transaction
from django.db.models import Q, Prefetch
from django.db.models.functions import Coalesce
from rest_framework.exceptions import MethodNotAllowed
from rest_framework import filters, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView
)

from game.api.serializers import PlayerSerializer, GameStateSerializer
from game.models import Player, Game, Hand, Effects, Gun


class GameStateAPIView(RetrieveAPIView):
    """Main game endpoint for updating game information"""

    serializer_class = GameStateSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Game.objects.all()

class PlayerAPIView(ListAPIView):
    serializer_class = PlayerSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Player.objects.all()
