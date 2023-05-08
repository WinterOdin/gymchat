from datetime import date
from rest_framework import serializers
from .models import User, Profile, UserSwipe, Matches, NotMatches, UserPhoto, Blocked, Gym, Location, Exercise, FavoriteExercise
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from drf_writable_nested import WritableNestedModelSerializer
from locations.serializers import GymSerializer, LocationSerializer


class RegisterUserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True,  validators=[validate_password])
    password2 = serializers.CharField(write_only=True)


    class Meta:
        model = User
        fields=('email', 'first_name', 'birthday', 'password', 'password2')

    def validate(self, attrs):

        password=attrs.get('password')
        password2=attrs.pop('password2')

        if password != password2:
            raise serializer.ValidationError("Password and Confirm Password Does not match")
        return attrs


    def create(self, validated_data):
        dob = validated_data['birthday']
        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        if age >= 18:
            user = User.objects.create(
                first_name = validated_data['first_name'],
                email = validated_data['email'],
                birthday = dob,
                age = age
            )
            user.set_password(validated_data['password'])
            user.save()

            return user        

        raise serializers.ValidationError("You are not eligible to use our app.")
    

class UserRangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('search_range',)


class UserSerializer(serializers.ModelSerializer):

    location = LocationSerializer(read_only=True)
    class Meta:
        model = User
        exclude = ('password', 'is_superuser', 'is_staff', 'groups', 'user_permissions')
        depth = 1

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPhoto
        fields = ('id', 'order', 'url')


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ('name', 'category', 'authorized')


class ProfileSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    
    fav_exercise = serializers.SerializerMethodField(read_only=True)
    images = serializers.SerializerMethodField(read_only=True)
    user = UserSerializer(read_only=True)
    gym = GymSerializer(read_only=True)
    

    def get_images(self, obj):
        return PhotoSerializer(UserPhoto.objects.filter(user=obj.user.id), many=True).data

    def get_fav_exercise(self, obj):
        fav_exercise = FavoriteExercise.objects.get(user=obj.user.id).exercise
        
        return {
            "id": fav_exercise.id,
            "name": fav_exercise.name,
            "category": fav_exercise.category,
        }

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


