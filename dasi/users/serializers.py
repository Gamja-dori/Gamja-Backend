from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework import status
from django.core.serializers import serialize, deserialize

class UserSerializer(serializers.ModelSerializer):   
    class Meta:
        model = User
        fields = "__all__"
        
    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        email = validated_data.pop('email')
        user = User.objects.create(
            username=username,
            email=email,
            is_senior=True,
            is_enterprise=False,
        )
        user.set_password(password)
        user.save()
        return user
    
        
class SeniorSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    
    class Meta:
        model = SeniorUser
        fields = ['name', 'phone_number', 'user']
           
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        senior = SeniorUser.objects.create(
            user=user,
            name=validated_data.pop('name'),
            phone_number=validated_data.pop('phone_number'),
        )
        return senior


class EnterpriseSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    
    class Meta:
        model = EnterpriseUser
        fields = ['name', 'phone_number', 'business_number', 'is_certified', 'user']
           
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        enterprise = EnterpriseUser.objects.create(
            user=user,
            name=validated_data.pop('name'),
            phone_number=validated_data.pop('phone_number'),
            business_number=validated_data.pop('business_number'),
            is_certified=False
        )
        return enterprise


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user, username):
        token = super().get_token(user)
        token['username'] = username 

        return token
