from django.shortcuts import render
from rest_framework import status, viewsets
from django.http import JsonResponse
from user_mgmt.serializers import PlaceSerializer, GymSerializer, ExerciseSerializer
from user_mgmt.models import Gym, Places, Exercise
from .permissions import GymLocationPermission
# Create your views here.

class ExerciseViewSet(viewsets.ModelViewSet):
    serializer_class = ExerciseSerializer

    def get_queryset(self):
        return Exercise.objects.all()

class PlaceViewSet(viewsets.ViewSet):
    permission_classes = [GymLocationPermission]
    serializer_class = PlaceSerializer
    get_queryset = Places.objects.all()


class GymViewSet(viewsets.ViewSet):
    permission_classes = [GymLocationPermission]
    serializer_class = GymSerializer
    get_queryset = Places.objects.all()
