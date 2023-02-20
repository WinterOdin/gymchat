from django.shortcuts import get_object_or_404
from .serializers import MatchesSerializer, NotMatchesSerializer



def get_or_none(model_or_qs, **kwargs):
    try:
        return get_object_or_404(model_or_qs, **kwargs)
    except:
        return None


def matched_router(model_obj):

    choice = model_obj['swipe']
    
    matched_data = {
        "user":model_obj['user'],
        "matched_user":model_obj['swiped_user']
    }

    if choice == "like":
        licked = MatchesSerializer(data=matched_data)
        if licked.is_valid():
            licked.save()
            return True

    elif choice == "dislike":
        not_licked = NotMatchesSerializer(data=matched_data)
        if not_licked.is_valid():
            not_licked.save()
            return True