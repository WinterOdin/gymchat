from django.shortcuts import render
from rest_framework import status, viewsets
from django.http import JsonResponse
from .serializers import LocationSerializer, GymSerializer, ExerciseSerializer
from user_mgmt.models import Gym, Location, Exercise
from .permissions import GymLocationPermission
# Create your views here.

class ExerciseViewSet(viewsets.ModelViewSet):
    serializer_class = ExerciseSerializer

    def get_queryset(self):
        return Exercise.objects.all()

class LocationViewSet(viewsets.ViewSet):
    permission_classes = [GymLocationPermission]
    serializer_class = LocationSerializer
    get_queryset = Location.objects.all()

    def partial_update(self, request, slug):
        
        user = User.objects.get(id=self.request.id)
        location = Location.objects.get(id=user__current_location_id)
        serializer = LocationSerializer(location, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)



class GymViewSet(viewsets.ViewSet):
    permission_classes = [GymLocationPermission]
    serializer_class = GymSerializer
    get_queryset = Gym.objects.all()
