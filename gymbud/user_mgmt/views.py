from django.shortcuts import render
from rest_framework.response import Response 
from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser
from django.http import JsonResponse
from django.views.generic import TemplateView, ListView
from .models import Profile, User, UserSwipe,Matches
from .serializers import ProfileSerializer, DisplayMatchedUsers, UserSwipeSerializer, RegisterUserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import ProfilePermission, DisplayMatchesPermission
from .paginators import ProfilePagination
from django.db.models import Q
from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema


UserModel = get_user_model()


class ProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [ProfilePermission]
    serializer_class = ProfileSerializer
    pagination_class = ProfilePagination

    def get_queryset(self):
        return Profile.objects.all()#.exclude(user__id=self.request.user.id)


class MatchesViewSet(viewsets.ModelViewSet):
    permission_classes = [DisplayMatchesPermission]
    serializer_class = DisplayMatchedUsers
    
    def get_queryset(self):
        return Matches.objects.filter(user__id=self.request.user.id)



class SwipeApi(APIView):
    permission_classes = [IsAuthenticated]


    @swagger_auto_schema(request_body=UserSwipeSerializer)
    def post(self, request):
     
        swipe_ser = UserSwipeSerializer(data=request.data)
        if swipe_ser.is_valid():
            
            swipe_ser.save()
         
            if swipe_ser.data["swipe"] == "dislike":
                if matched_router(request.data):
                    return JsonResponse({'message':'not matched'}, status=status.HTTP_200_OK)

            elif swipe_ser.data["swipe"] == "like":
                
                criterion1 = Q(swiped_user__id__contains = swipe_ser.data['swiped_user'])
                criterion2 = Q(user__id__contains= swipe_ser.data['user'])
                get_swiped_user = UserSwipe.objects.filter(criterion1 & criterion2).first()
                
                #like this becouse we want to know if we have match 
                #need to refactor this
            
                if get_swiped_user:
                    if get_swiped_user.swipe == "like":
                        if matched_router(request.data):
                            JsonResponse({'message':'matched'}, status=status.HTTP_201_CREATED)
                    elif get_swiped_user.swipe == "dislike":
                        if matched_router(request.data):
                            JsonResponse({'message':'not matched'}, status=status.HTTP_201_CREATED)
                else:
                    if matched_router(request.data):
                        JsonResponse({'message':'matched'}, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({'message':swipe_ser.errors}, status=status.HTTP_404_NOT_FOUND)

        
        return Response(status=status.HTTP_200_OK)

        

class CustomUserCreate(APIView):

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


