from rest_framework import serializers
from user_mgmt.models import Gym, Location, Exercise
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class LocationSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = Location
        geo_field = 'point'
        exclude = ('test', )
        depth = 1
    

class GymSerializer(serializers.ModelSerializer):

    place = LocationSerializer(read_only=True)

    class Meta:
        model = Gym
        fields = '__all__'


class ExerciseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Exercise
        fields = '__all__'