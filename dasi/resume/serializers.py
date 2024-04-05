from rest_framework import serializers
from .models import *
from users.models import SeniorUser

class CreateResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ['user']
        
    def create(self, validated_data):
        user_id = validated_data.get('user_id')
        user = SeniorUser.objects.filter(user_id=user_id)[0]
        resume = Resume.objects.create(user=user)
        return resume
    
