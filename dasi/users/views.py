from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import re
from drf_yasg.utils import swagger_auto_schema

def validate_password(pw):
    regex_pw = '[A-Za-z0-9!@##$%^&+=]{8,25}'
    if not re.match(regex_pw, pw):
        raise ValidationError("8자 이상의 영문 대/소문자, 숫자, 특수문자 조합을 입력해주세요.")
    if not re.search(r"[a-zA-Z]", pw):
        raise ValidationError("비밀번호는 하나 이상의 영문이 포함되어야 합니다.")
    if not re.search(r"\d", pw):
        raise ValidationError("비밀번호는 하나 이상의 숫자가 포함되어야 합니다.")


def create_user(data, user_type):
    if user_type == 1:
        serializer = SeniorSerializer(data=data)
    elif user_type == 2:
        serializer = EnterpriseSerializer(data=data)
    password = data.get('user', {}).get('password')

    if serializer.is_valid(raise_exception=ValueError):
        member = serializer.create(validated_data=data)
        # 토큰 생성
        token_serializer = TokenObtainPairSerializer(data={'username': member.user.username, 'password': password})
        if token_serializer.is_valid():
            access_token = str(token_serializer.validated_data['access'])
            refresh_token = str(token_serializer.validated_data['refresh'])

            res = Response(
                {
                    "username": member.user.username,
                    "message": "회원가입이 완료되었습니다.",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_201_CREATED,
            )
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            return res
        return Response(token_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class SeniorUserCreate(APIView):
    permission_classes = [AllowAny] 
    
    @swagger_auto_schema(tags=['시니어 사용자 데이터를 생성합니다.'], request_body=SeniorSerializer)
    def post(self, request):
        # 비밀번호 유효성 검사
        pw = request.data.get('user').get('password')
        validate_password(pw)
        
        # 유저 생성
        response = create_user(data=request.data, user_type=1)
        return response  
    
    
class EnterpriseUserCreate(APIView):
    permission_classes = [AllowAny] 
    
    @swagger_auto_schema(tags=['기업 사용자 데이터를 생성합니다.'], request_body=EnterpriseSerializer)
    def post(self, request):
        # 비밀번호 유효성 검사
        pw = request.data.get('user').get('password')
        validate_password(pw)
        
        # 유저 생성
        response = create_user(data=request.data, user_type=2)
        return response  
    

class LoginView(APIView):
    permission_classes = [AllowAny] 

    @swagger_auto_schema(tags=['사용자가 로그인합니다.'], request_body=UserLoginSerializer)
    def post(self, request):
        token_serializer = TokenObtainPairSerializer(data=request.data)
        if token_serializer.is_valid():
            user = token_serializer.user
            if user.is_senior:
                member = SeniorUser.objects.filter(user=user)[0]
            elif user.is_enterprise:
                member = EnterpriseUser.objects.filter(user=user)[0]
                
            serializer = UserLoginSerializer(user)
            access_token = str(token_serializer.validated_data['access'])
            refresh_token = str(token_serializer.validated_data['refresh'])
            res = Response(
                {
                    "id": user.id,
                    "name": member.name,
                    "is_senior": user.is_senior,
                    "is_enterprise": user.is_enterprise,
                    "message": "로그인에 성공했습니다.",
                    "access": access_token,
                    "refresh": refresh_token
                },
                status=status.HTTP_200_OK,
            )
            res.set_cookie("refresh", refresh_token, httponly=True)
            return res
        return Response(token_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LogoutView(APIView):
    @swagger_auto_schema(tags=['사용자가 로그아웃합니다.'])
    def post(self, request):
        response = Response({
            "message": "로그아웃이 완료되었습니다."
        }, status=status.HTTP_202_ACCEPTED)

        response.delete_cookie('refresh')
        response.delete_cookie('access') 

        return response


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=['사용자의 정보를 조회합니다.'])
    def get(self, request, id):
        try:
            user = User.objects.get(id=id)
        except ObjectDoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if user.is_senior:
            member = SeniorUser.objects.get(user=user)
        elif user.is_enterprise:
            member = EnterpriseUser.objects.get(user=user)
        else:
            return Response({"error": "Invalid user type"}, status=status.HTTP_400_BAD_REQUEST)
        
        response_data = {
            "id": user.id,
            "username": user.username,
            "name": member.name,
            "phone_number": member.phone_number,
            "email": user.email,
            "is_senior": user.is_senior,
            "is_enterprise": user.is_enterprise,
            "message": "회원 정보 조회에 성공했습니다.",
        }
        
        if user.is_senior:
            response_data['default_resume'] = member.default_resume
        else:
            response_data['business_number'] = member.business_number
            response_data['is_certified'] = member.is_certified   
        
        return Response(response_data, status=status.HTTP_200_OK)