from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import PlaceViewSet, GymViewSet

router = DefaultRouter()
router.register('places', PlaceViewSet, basename="places")
router.register('gym', GymViewSet, basename="gym")

urlpatterns = [
    
] + router.urls
