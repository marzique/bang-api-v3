
import io
import csv
import datetime
# from dateutil import parser

from django.db.models import Sum
from django.http import HttpResponse
from django.db import IntegrityError, transaction
from django.db.models import Q, Prefetch
from django.db.models.functions import Coalesce
from rest_framework.exceptions import MethodNotAllowed
from rest_framework import filters, status
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView
from rest_framework.generics import (
    ListCreateAPIView,
    ListAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
    UpdateAPIView,
    CreateAPIView,
    DestroyAPIView,
    GenericAPIView
)

from game.api.serializers import PlayerAPISerializer
from game.models import Player

class PlayerAPIView(ListAPIView):
    serializer_class = PlayerAPISerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Player.objects.all()
        return queryset

