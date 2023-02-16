from django.shortcuts import render
from rest_framework.response import Response 
from rest_framework.views import APIView
from .serializers import RegisterUserSerializer
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser
from django.http import JsonResponse
from django.views.generic import TemplateView, ListView
from rest_framework import permissions
from .models import Profile
from .serializers import ProfileSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .permissions import ProfilePermission
from .paginators import ProfilePagination

UserModel = get_user_model()


class ProfileViewset(viewsets.ModelViewSet):
    permission_classes = [ProfilePermission]
    serializer_class = ProfileSerializer
    pagination_class = ProfilePagination

    def get_queryset(self):
        return Profile.objects.all().exclude(id=self.request.user.id)


class CustomUserCreate(APIView):

    permission_classes = (AllowAny,)

    def post(self, request):
        
        reg_serializer = RegisterUserSerializer(data=request.data)
        
        if reg_serializer.is_valid():
            new_user =reg_serializer.save()

            if new_user:
                return Response(status=status.HTTP_201_CREATED)

        return Response(reg_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlacklistTokenView(APIView):

    permission_classes = (AllowAny,)
    def post(self, request):

        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


