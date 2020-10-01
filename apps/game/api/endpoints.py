
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
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView
)

from game.api.serializers import (
    PlayerSerializer, 
    GameStateSerializer,
    CreateUpdatePlayerSerializer
)
from game.models import Player, Game, Hand, Effects, Gun


class GameStateAPIView(RetrieveAPIView):
    """Main game endpoint for updating game information"""

    serializer_class = GameStateSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Game.objects.all()

class PlayerAPIView(CreateAPIView, UpdateAPIView):
    serializer_class = CreateUpdatePlayerSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        return Player.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError:
            content = {'error': 'Player with the same name already exists'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)