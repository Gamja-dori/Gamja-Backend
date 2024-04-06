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
        resume_num = len(Resume.objects.filter(user=user))
        resume.title = "이력서 " + str(resume_num)
        if len(Resume.objects.filter(user=user)) == 1:
            resume.is_default = True
        resume.save()
        return resume
        
class ChangeResumeTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ['user', 'id', 'title']

class FindResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ['user', 'id']