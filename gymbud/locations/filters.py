from django_filters import rest_framework as filters
from user_mgmt.models import Gym, Exercise


class GymFilter(filters.FilterSet):

    class Meta:
        model = Gym
        fields = {
            'name':['icontains'],
            'place__id':['iexact'],
            'place__city':['iexact'],
            'place__street':['iexact'],
            'place__state':['iexact'],
            'place__country':['iexact']
        }

class ExerciseFilter(filters.FilterSet):

    class Meta:
        model = Exercise
        fields = {
            'name':['icontains'],
            'category':['icontains'],
            'authorized':['iexact'],
        }