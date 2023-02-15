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
from django.contrib.auth.mixins import LoginRequiredMixin

UserModel = get_user_model()


class UsersListView(LoginRequiredMixin, ListView):
    http_method_names = ['get', ]

    def get_queryset(self):
        return UserModel.objects.all().exclude(id=self.request.user.id)

    def render_to_response(self, context, **response_kwargs):
        users: List[AbstractBaseUser] = context['object_list']

        data = [{
            "username": user.get_short_name(),
            "pk": str(user.pk)
        } for user in users]
        return JsonResponse(data, safe=False, **response_kwargs)


# Create your views here.
class UserCreate(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        
        reg_serializer = RegisterUserSerializer(data=request.data)
        if reg_serializer.is_valid():
            new_user =reg_serializer.save()

            if new_user:
                return Response(status=status.HTTP_201_CREATED)

        return Response(reg_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlacklistTokenView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)