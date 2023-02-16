from rest_framework import serializers
from .models import User, Profile

from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class RegisterUserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True,  validators=[validate_password])
    password2=serializers.CharField(write_only=True)

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

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'
        depth = 1
        