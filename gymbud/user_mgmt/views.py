from django.shortcuts import render
from rest_framework.response import Response 
from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser
from django.http import JsonResponse
from django.views.generic import TemplateView, ListView
from .models import Profile, User, UserSwipe, Matches, Blocked
from .serializers import UserRangeSerializer, UserSerializer, ProfileSerializer, DisplayMatchedUsers, UserSwipeSerializer, RegisterUserSerializer, BlockedSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import ProfilePermission
from chat.permissions import DisplayMatchesPermission
from .paginators import ProfilePagination
from django.db.models import Q
from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from .helpers import matched_router
from .filters import ProfileFilter

UserModel = get_user_model()

class UserAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request):
        serializer = UserSerializer(User.objects.get(id=self.request.user.id))
        return Response(serializer.data)

    def patch(self, request):
        
        serializer = UserRangeSerializer(User.objects.get(id=self.request.user.id), data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class ProfileViewSet(viewsets.ModelViewSet):
    #permission_classes = [ProfilePermission]
    serializer_class = ProfileSerializer
    pagination_class = ProfilePagination
    filterset_class  = ProfileFilter

    def get_queryset(self):

        current_id = self.request.user.id
        blocked_users = Blocked.objects.filter(user__id=current_id).values('blocked_user')

        users_taken_action = UserSwipe.objects.filter(user__id=current_id).values('swiped_user')

        users_not_taken_action = Profile.objects.exclude(user__in=users_taken_action) \
            .exclude(user__in=blocked_users).exclude(user__id=current_id)

        
        return users_not_taken_action

    def create(self, request):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MatchesViewSet(viewsets.ModelViewSet):
    permission_classes = [DisplayMatchesPermission]
    serializer_class = DisplayMatchedUsers
    
    def get_queryset(self):
        return Matches.objects.filter(user__id=self.request.user.id)



class BlockedViewSet(viewsets.ModelViewSet):
    serializer_class = BlockedSerializer

    def get_queryset(self):
        return Blocked.objects.filter(user__id=self.request.user.id)
        


class SwipeApi(APIView):
    permission_classes = [IsAuthenticated]


    @swagger_auto_schema(request_body=UserSwipeSerializer)
    def post(self, request):
        
        if request.data['user'] == request.user.id:
            swipe_ser = UserSwipeSerializer(data=request.data)
            if swipe_ser.is_valid():
                
            
                if request.data["swipe"] == "dislike":
                    if matched_router(request.data):
                        return JsonResponse({'message':'not matched'}, status=status.HTTP_201_CREATED)

                elif request.data["swipe"] == "like":
                    
                    criterion1 = Q(swiped_user__id__contains = request.data['user'] )
                    criterion2 = Q(user__id__contains = request.data['swiped_user'])
                    
                    get_swiped_user = UserSwipe.objects.filter(criterion1 & criterion2).first()
                    
                    #need to refactor this
                
                    if get_swiped_user:
                        if matched_router(request.data):
                            if get_swiped_user.swipe == "like":
                                JsonResponse({'message':'matched'}, status=status.HTTP_201_CREATED)
                            elif get_swiped_user.swipe == "dislike":
                                JsonResponse({'message':'not matched'}, status=status.HTTP_201_CREATED)

                swipe_ser.save()
                if swipe_ser:
                    JsonResponse({'message':'swiped'}, status=status.HTTP_201_CREATED)

            else:
                return JsonResponse({'message':swipe_ser.errors}, status=status.HTTP_404_NOT_FOUND)
        else:
            #add to blacklist
            return JsonResponse({'message':"blacklisted"}, status=status.HTTP_404_NOT_FOUND)

        
        return Response(status=status.HTTP_200_OK)



class CustomUserCreate(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        
        reg_serializer = RegisterUserSerializer(data=request.data)
        if reg_serializer.is_valid():
            new_user = reg_serializer.save()
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


