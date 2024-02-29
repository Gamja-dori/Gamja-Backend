from django.shortcuts import render
from .serializers import SeniorRegisterSerializer, MyTokenObtainPairSerializer
from .models import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import re

class SeniorUserCreate(APIView):
    permission_classes = [AllowAny] # 로그인하지 않아도 접근 가능

    def post(self, request):
        # 비밀번호 유효성 검사
        pw = request.data.get('password')
        regex_pw = '[A-Za-z0-9!@##$%^&+=]{8,25}'
        if not re.match(regex_pw, pw):
            raise ValidationError("8자 이상의 영문 대/소문자, 숫자, 특수문자 조합을 입력해주세요.")
        if not re.search(r"[a-zA-Z]", pw):
            raise ValidationError("비밀번호는 하나 이상의 영문이 포함되어야 합니다.")
        if not re.search(r"\d", pw):
            raise ValidationError("비밀번호는 하나 이상의 숫자가 포함되어야 합니다.")
        
        serializer = SeniorRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
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
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer