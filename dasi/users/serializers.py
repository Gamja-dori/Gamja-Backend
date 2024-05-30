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

    def update(self, user, validated_data):
        user.email = validated_data.get('email', user.email)
        password = validated_data.get('password')
        if password:
            user.set_password(password)
        user.save()
        return user


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        
        
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
    
    def update(self, senior, validated_data):
        if "user" in validated_data:
            user_data = validated_data.pop('user')
            user = senior.user
        
            # user 업데이트
            user_serializer = UserRegisterSerializer()
            user_serializer.update(user, user_data)

        # senioruser 업데이트
        senior.name = validated_data.get('name', senior.name)
        senior.phone_number = validated_data.get('phone_number', senior.phone_number)
        senior.save()

        return senior
    

class EnterpriseSerializer(serializers.ModelSerializer):
    user = UserRegisterSerializer(required=True)
    
    class Meta:
        model = EnterpriseUser
        fields = ['name', 'phone_number', 'business_number', 'is_certified', 'user', 'company']
           
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserRegisterSerializer.create(UserRegisterSerializer(), validated_data=user_data, user_type=2)
        enterprise = EnterpriseUser.objects.create(
            user=user,
            name=validated_data.pop('name'),
            phone_number=validated_data.pop('phone_number'),
            business_number=validated_data.pop('business_number'),
            company=validated_data.pop('company'),
            is_certified=False
        )
        return enterprise
    
    def update(self, enterprise, validated_data):
        if "user" in validated_data:
            user_data = validated_data.pop('user')
            user = enterprise.user
        
            # user 업데이트
            user_serializer = UserRegisterSerializer()
            user_serializer.update(user, user_data)

        # enterpriseuser 업데이트
        enterprise.name = validated_data.get('name', enterprise.name)
        enterprise.phone_number = validated_data.get('phone_number', enterprise.phone_number)
        enterprise.name = validated_data.get('company', enterprise.company)
        enterprise.phone_number = validated_data.get('business_number', enterprise.business_number)
        enterprise.save()

        return enterprise
    
    
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'suggest', 'senior', 'reviewer', 'score', 'tags', 'comment']

    def create(self, validated_data):
        suggest_id = validated_data.get('suggest')
        suggest = Suggest.objects.filter(id=suggest_id)[0]
        senior_id = validated_data.get('senior')
        senior = SeniorUser.objects.filter(user_id=senior_id)[0]
        reviewer_id = validated_data.get('reviewer')
        reviewer = EnterpriseUser.objects.filter(user_id=reviewer_id)[0]
        review = Review.objects.create(suggest=suggest, senior=senior, reviewer=reviewer, score=validated_data.pop('score'), tags=validated_data.pop('tags'), comment=validated_data.pop('comment'))
        review.save()
        return review