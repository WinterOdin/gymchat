from django.urls import path
from . import views


urlpatterns = [
    path("room", views.index, name="index"),
    path("join/<str:id>/", views.room, name="room"),
]