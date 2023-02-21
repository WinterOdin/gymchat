from django.shortcuts import render
from rest_framework import status, viewsets
from django.http import JsonResponse
from .serializers import PlaceSerializer, GymSerializer
from .models import Gym, Places
from .permissions import GymLocationPermission
# Create your views here.


class PlaceViewSet(viewsets.ViewSet):
    permission_classes = [GymLocationPermission]
    serializer_class = PlaceSerializer
    get_queryset = Places.objects.all()


class GymViewSet(viewsets.ViewSet):
    permission_classes = [GymLocationPermission]
    serializer_class = GymSerializer
    get_queryset = Places.objects.all()
