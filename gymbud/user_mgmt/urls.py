from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet, CustomUserCreate, BlacklistTokenView,MatchesViewSet, SwipeApi


router = DefaultRouter()
router.register('profile', ProfileViewSet, basename="profile")
router.register('matches', MatchesViewSet, basename="matches")

urlpatterns = [
    
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', CustomUserCreate.as_view(), name='create_user'),
    path('logout/blacklist/', BlacklistTokenView.as_view(), name='blacklist'),


    path('swipe/', SwipeApi.as_view(), name='swipe_user'),

] + router.urls