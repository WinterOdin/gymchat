from django_filters import rest_framework as filters
from .models import Profile


class ProfileFilter(filters.FilterSet):

    gym__id = filters.CharFilter(field_name='user__gym__id', label="Gym ID")
    gym__name = filters.CharFilter(field_name='user__gym__name', label="Gym Name")
    gym__place__id = filters.CharFilter(field_name='user__gym__place__id', label='Gym Place ID' )
    gym__place__city = filters.CharFilter(field_name='user__gym__place__city', label='Gym Place City')
    gym__place__state = filters.CharFilter(field_name='user__gym__place__state', label='Gym Place State')
    gym__place__street = filters.CharFilter(field_name='user__gym__place__street', label='Gym Place Street')
    gym__place__country = filters.CharFilter(field_name='user__gym__place__country', label='Gym Place Country')
    gym__place__placeId = filters.CharFilter(field_name='user__gym__place__placeId', label='Gym Place PlaceID')
    
    user__age_gte = filters.NumberFilter(field_name='user__age', label='User Search Age GTE', lookup_expr='gte')
    user__age_lte = filters.NumberFilter(field_name='user__age', label='User Search Age LTE', lookup_expr='lte')
    search_range_gte = filters.NumberFilter(field_name='user__search_range', label='User Search Range GTE', lookup_expr='gte')
    search_range_lte = filters.NumberFilter(field_name='user__search_range', label='User Search Range LTE', lookup_expr='lte')

    class Meta:
        model = Profile
        fields = {
            'date_updated':['icontains','lte','gte'],
            'date_created':['icontains','lte','gte'],
            'gender':['iexact'],
            'user__is_active':['iexact'],
            'user__is_staff':['iexact'],
            'user__current_location__id':['iexact'],
            'user__current_location__city':['iexact'],
            'user__current_location__state':['iexact'],
            'user__current_location__country':['iexact'],
        }

