from .models import Gym, Places
from rest_framework import serializers

class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Places
        exclude = '__all__'

class GymSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gym
        exclude = '__all__'