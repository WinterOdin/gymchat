from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from rest_framework.routers import DefaultRouter
from .views import UserAPIView, ProfileViewSet, CustomUserCreate, BlacklistTokenView, MatchesViewSet, SwipeApi, BlockedViewSet
from locations.views import LocationViewSet, GymViewSet, ExerciseViewSet
import debug_toolbar


router = DefaultRouter()
router.register('profile', ProfileViewSet, basename='profile')
router.register('match', MatchesViewSet, basename='match')
router.register('block', BlockedViewSet, basename='block')
router.register('places', LocationViewSet, basename="places")
router.register('gym', GymViewSet, basename="gym")
router.register('exercises', ExerciseViewSet, basename="exercises_list")


urlpatterns = [
    
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', CustomUserCreate.as_view(), name='create_user'),
    path('logout/blacklist/', BlacklistTokenView.as_view(), name='blacklist'),
    path('user/', UserAPIView.as_view(), name='user_info'),
    path('swipe/', SwipeApi.as_view(), name='swipe_user'),

] + router.urls