from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, UserConfig

class UserConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserConfig
        fields = ['font_size', 'high_contrast', 'voice_guidance']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['phone', 'avatar_url']

class UserDetailSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(source='profile.phone', read_only=True)
    avatar_url = serializers.CharField(source='profile.avatar_url', read_only=True)
    config = UserConfigSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'avatar_url', 'config']

class LoginRequestSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

class LoginResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    token = serializers.CharField()
    user = UserDetailSerializer()

class RegisterRequestSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    email = serializers.EmailField(required=True)
    phone = serializers.CharField(required=False, allow_blank=True, default='')
    avatar_url = serializers.CharField(required=False, allow_blank=True, default='')
    font_size = serializers.ChoiceField(choices=['SMALL', 'MEDIUM', 'LARGE'], required=False, default='MEDIUM')
    high_contrast = serializers.BooleanField(required=False, default=False)
    voice_guidance = serializers.BooleanField(required=False, default=False)

class RegisterResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    token = serializers.CharField()
    user = UserDetailSerializer()

class ProfileUpdateSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    phone = serializers.CharField(required=False, allow_blank=True)
    avatar_url = serializers.CharField(required=False, allow_blank=True)
    font_size = serializers.ChoiceField(choices=['SMALL', 'MEDIUM', 'LARGE'], required=False)
    high_contrast = serializers.BooleanField(required=False)
    voice_guidance = serializers.BooleanField(required=False)

class ProfileUpdateResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    user = UserDetailSerializer()

class LogoutResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
