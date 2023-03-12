from rest_framework import serializers
from user_mgmt.models import Gym, Location, Exercise

from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = '__all__'

class GymSerializer(serializers.ModelSerializer):

    class Meta:
        model = Gym
        fields = '__all__'


class ExerciseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Exercise
        fields = '__all__'