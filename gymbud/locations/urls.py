from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import PlaceViewSet, GymViewSet, ExerciseViewSet

router = DefaultRouter()
router.register('places', PlaceViewSet, basename="places")
router.register('gym', GymViewSet, basename="gym")
router.register('exercises', ExerciseViewSet, basename="exercises_list")

urlpatterns = [
    
] + router.urls
