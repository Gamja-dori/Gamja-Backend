from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class SeniorRegisterSerializer(serializers.ModelSerializer):       
    def create(self, validated_data):
        name = validated_data.get('name')
        username = validated_data.get('username')
        password = validated_data.get('password')
        email = validated_data.get('email')
        phone_number = validated_data.get('phone_number')
        user = User(
            name=name,
            username=username,
            email=email,
            phone_number=phone_number,
        )
        user.set_password(password)
        user.save()
        return user
    
    class Meta:
        model = SeniorUser
        fields = ['name', 'username', 'password', 'email', 'phone_number']
        
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username

        return token