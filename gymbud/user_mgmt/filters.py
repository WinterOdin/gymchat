import django_filters 
from .models import Profile


class ProfileFilter(django_filters.FilterSet):

    class Meta:
        model = Profile
        fields = {
            'date_updated':['icontains','lte','gte'],
            'date_created':['icontains','lte','gte'],
            'gender':['iexact'],
            'user__is_active':['iexact'],
            'user__is_staff':['iexact'],
            'user__search_range':['iexact'],
            'user__current_location__id':['iexact'],
            'user__current_location__city':['iexact'],
            'user__current_location__state':['iexact'],
            'user__current_location__country':['iexact'],
            'gym__id':['iexact'],
            'gym__name':['icontains'],
            'gym__place__id':['iexact'],
            'gym__place__city':['iexact'],
            'gym__place__street':['iexact'],
            'gym__place__state':['iexact'],
            'gym__place__country':['iexact']
        }
