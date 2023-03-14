from rest_framework import serializers
from .models import User, Profile, UserSwipe, Matches, NotMatches, UserPhoto, Blocked, Gym, Location, Exercise

from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class RegisterUserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True,  validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields=('email', 'first_name', 'password','password2')

    def validate(self, attrs):

        password=attrs.get('password')
        password2=attrs.pop('password2')

        if password != password2:
            raise serializer.ValidationError("Password and Confirm Password Does not match")
        return attrs


    def create(self, validated_data):
        user = User.objects.create(
            first_name=validated_data['first_name'],
            email=validated_data['email'],
        )

        
        user.set_password(validated_data['password'])
        user.save()

        return user


class UserRangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('search_range',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', 'is_superuser', 'is_staff', 'groups', 'user_permissions')


class ProfileSerializer(serializers.ModelSerializer):

    user = UserSerializer()

    class Meta:
        model = Profile
        fields = '__all__'
        depth = 1





class DisplayMatchedUsers(serializers.ModelSerializer):
    matched_user = serializers.SerializerMethodField()
    
    def get_matched_user(self, obj):
        user = obj.matched_user
        photo = user.userphoto_set.first()
        
        return {
            "username": user.first_name,
            "pk": str(user.id),
            "url": photo.url if photo else None
        }

    class Meta:
        model = Matches
        fields = ("matched_user",)


class UserSwipeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserSwipe
        fields = ('user', 'swiped_user', 'date', 'swipe')


class MatchesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Matches
        fields = ('user', 'matched_user', 'date')


class NotMatchesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = NotMatches
        fields = ('user', 'matched_user', 'date')


class BlockedSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Blocked
        fields = ('user', 'blocked_user')


