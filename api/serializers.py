from rest_framework import serializers
from rest_framework.authentication import authenticate
from django.contrib.auth.models import User
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)

    def validate_username(self, data):
        if User.objects.filter(username=data).exists():
            raise serializers.ValidationError("Username is taken")
        else:
            return data
    
    def validate_email(self, data):
        if User.objects.filter(email=data).exists():
            raise serializers.ValidationError("An account with this email has already been created")
        else:
            return data
    
    def validate_password(self, data):
        if len(data) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long")
        else:
            return data
        

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']