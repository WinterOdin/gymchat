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
            'user__current_location_id':['iexact'],
            'user__current_location_city':['iexact'],
        }