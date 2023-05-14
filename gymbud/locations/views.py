from django.shortcuts import render
from rest_framework import status, viewsets
from django.http import JsonResponse
from .serializers import LocationSerializer, GymSerializer, ExerciseSerializer
from user_mgmt.models import Gym, Location, Exercise
from .permissions import GymLocationPermission
from rest_framework.response import Response
from .mixins import EnablePartialUpdateMixin
from .filters import ExerciseFilter, GymFilter
# Create your views here.

class ExerciseViewSet(EnablePartialUpdateMixin, viewsets.ModelViewSet):
    serializer_class = ExerciseSerializer
    get_queryset = Exercise.objects.all()
    filterset_class = ExerciseFilter

    def get_queryset(self):
        return Exercise.objects.all()

    def create(self, request):
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LocationViewSet(EnablePartialUpdateMixin, viewsets.ModelViewSet):
    #permission_classes = [GymLocationPermission]
    serializer_class = LocationSerializer

    def get_queryset(self):
        return Location.objects.all()

    def create(self, request):
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class GymViewSet(EnablePartialUpdateMixin, viewsets.ModelViewSet):
    #permission_classes = [GymLocationPermission]
    serializer_class = GymSerializer
    filterset_class = GymFilter

    def get_queryset(self):
        return Gym.objects.all()

    def create(self, request):
        serializer = GymSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
