from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework import status
from django.core.serializers import serialize, deserialize

class UserRegisterSerializer(serializers.ModelSerializer):   
    class Meta:
        model = User
        fields = "__all__"
        
    def create(self, validated_data, user_type):
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        email = validated_data.pop('email')
        if user_type == 1:
            is_senior = True
            is_enterprise = False
        elif user_type == 2:
            is_senior = False
            is_enterprise = True
            
        user = User.objects.create(
            username=username,
            email=email,
            is_senior=is_senior,
            is_enterprise=is_enterprise,
        )
        user.set_password(password)
        user.save()
        return user

class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        
        
class SeniorSerializer(serializers.ModelSerializer):
    user = UserRegisterSerializer(required=True)
    
    class Meta:
        model = SeniorUser
        fields = ['name', 'phone_number', 'user']
           
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserRegisterSerializer.create(UserRegisterSerializer(), validated_data=user_data, user_type=1)
        senior = SeniorUser.objects.create(
            user=user,
            name=validated_data.pop('name'),
            phone_number=validated_data.pop('phone_number'),
        )
        return senior


class EnterpriseSerializer(serializers.ModelSerializer):
    user = UserRegisterSerializer(required=True)
    
    class Meta:
        model = EnterpriseUser
        fields = ['name', 'phone_number', 'business_number', 'is_certified', 'user']
           
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserRegisterSerializer.create(UserRegisterSerializer(), validated_data=user_data, user_type=2)
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
