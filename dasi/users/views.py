from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.core.files.storage import default_storage 
from django.core.files.base import ContentFile
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import *
from .models import *
import base64
import json
import re

def validate_password(pw):
    regex_pw = '[A-Za-z0-9!@##$%^&+=]{8,12}'
    if not re.match(regex_pw, pw):
        raise ValidationError("8자 이상의 영문 대/소문자, 숫자, 특수문자 조합을 입력해주세요.")
    
    combinations_cnt = 0 # 영문, 숫자, 특수기호 중 2종류 포함했는지 체크
    if re.search(r"[a-zA-Z]", pw):
        combinations_cnt += 1
    if re.search(r"\d", pw):
        combinations_cnt += 1
    if re.search(r"[!@##$%^&+=]", pw):
        combinations_cnt += 1
    if combinations_cnt < 2:
        raise ValidationError("비밀번호는 영문, 숫자, 특수기호 중 2종류 이상 조합되어야 합니다.")
    

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
            res = Response(
                {
                    "username": member.user.username,
                    "message": "회원가입이 완료되었습니다.",
                },
                status=status.HTTP_201_CREATED,
            )
            return res
        return Response(token_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class SeniorUserCreateView(APIView):
    permission_classes = [AllowAny] 
    
    @swagger_auto_schema(tags=['시니어 사용자 데이터를 생성합니다.'], request_body=SeniorSerializer)
    def post(self, request):
        # 비밀번호 유효성 검사
        pw = request.data.get('user').get('password')
        validate_password(pw)
        
        # 유저 생성
        response = create_user(data=request.data, user_type=1)
        return response  
    
    
class EnterpriseUserCreateView(APIView):
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
                    "profile_image": "https://api.dasi-expert.com" + user.profile_image.url,
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


class UserView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_user(self, id):
        try:
            user = User.objects.get(id=id)
            return user
        except ObjectDoesNotExist:
            return None


    def get_member(self, user):
        if user.is_senior:
            member = SeniorUser.objects.get(user=user)
        elif user.is_enterprise:
            member = EnterpriseUser.objects.get(user=user)
        return member


    @swagger_auto_schema(tags=['사용자의 정보를 조회합니다.'])
    def get(self, request, id):
        user = self.get_user(id)        
        if user is None:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        member = self.get_member(user)
        
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
    
    
    @swagger_auto_schema(tags=['사용자 정보를 수정합니다.'])
    def put(self, request, id):
        user = self.get_user(id)        
        if user is None:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        member = self.get_member(user)
        
        if user.is_senior:
            serializer = SeniorSerializer(member, data=request.data, partial=True)
        else:
            serializer = EnterpriseSerializer(member, data=request.data, partial=True)
       
        if serializer.is_valid():
            member = serializer.update(member, validated_data=serializer.validated_data)
            member.save()
            res = Response(
                {
                    "user_id": member.user_id,
                    "user": serializer.data,
                    "message": "사용자 정보가 성공적으로 수정되었습니다."
                },
                status=status.HTTP_200_OK,
            )
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    @swagger_auto_schema(tags=['사용자를 삭제합니다.'])
    def delete(self, request, id):
        user = self.get_user(id)
        if user is None:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        user.delete()
        res = Response(
            {
                "message": "사용자가 성공적으로 삭제되었습니다."
            },
            status=status.HTTP_200_OK,
        )
        return res


class ProfileImageView(APIView):
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(tags=['사용자의 프로필 사진을 조회합니다.'])
    def get(self, request, id):
        try:
            user = User.objects.get(id=id)
        except ObjectDoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            res = {
                "message": "회원 프로필 사진을 성공적으로 조회했습니다.",
                "profile_image": "https://api.dasi-expert.com" + user.profile_image.url,
            }
            return Response(res, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        

    @swagger_auto_schema(tags=['사용자의 프로필 사진을 변경합니다.'])
    def post(self, request, id):
        try:
            user = User.objects.get(id=id)
        except ObjectDoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            image = request.FILES["image"]
            if ('uploads/profile/' + user.username + '/') in user.profile_image.name:
                default_storage.delete(user.profile_image.name) # 기존 이미지 삭제
            image_path = default_storage.save('uploads/profile/' + user.username + '/' + image.name, ContentFile(image.read()))
            
            user.profile_image = image_path
            user.save()

            return Response(
                {
                    "message": "회원 프로필 사진이 성공적으로 변경되었습니다.",
                    "profile_image": "https://api.dasi-expert.com" + user.profile_image.url,
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class UserSecretView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(tags=['채용 성사 후 시니어 사용자의 개인정보를 조회합니다.'])
    def get(self, request, id):
        try:
            user = User.objects.get(id=id)
            senior = SeniorUser.objects.get(user_id=id)
        except ObjectDoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND) 
        
        return Response(
            {
                "name": senior.name,
                "phone_number": senior.phone_number,
                "email": user.email
            },
            status=status.HTTP_200_OK
        )
    
    
class CheckDuplicateView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(tags=['중복된 아이디 여부를 조회합니다.'])
    def get(self, request, username):
        try:
            User.objects.get(username=username)
            return Response({True}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({False}, status=status.HTTP_200_OK)
        
def checkUserExistence(user_id):
    try:
        user = SeniorUser.objects.get(user_id=user_id)
    except ObjectDoesNotExist:
        return False
    return user

def checkReviewExistence(user_id, review_id):
    user = checkUserExistence(user_id)
    if user:
        try:
            review = Review.objects.get(id=review_id, senior=user)
        except ObjectDoesNotExist:
            return False
        return review
    return False


class GetReviewListView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(tags=['사용자의 리뷰 목록을 조회합니다.'])
    def get(self, request, senior_id):
        senior = checkUserExistence(senior_id)
        if senior:
            reviews = Review.objects.filter(senior=senior)
            review_list = []
            avg_score = 0
            for r in reviews:
                user = User.objects.get(id=r.reviewer.user_id)
                reviewer = EnterpriseUser.objects.get(user=user)
                suggest = Suggest.objects.get(id=r.suggest.id)
                resume = Resume.objects.get(id=suggest.resume.id)
                avg_score += r.score
                review_list.append({
                    "review_id": r.id,
                    "reviewer_id": r.reviewer.user_id,
                    "reviewer_name": reviewer.company,
                    "reviewer_image": "https://api.dasi-expert.com" + user.profile_image.url,
                    "job_group": resume.job_group,
                    "job_role": resume.job_role,
                    "start_year_month": suggest.start_year_month,
                    "end_year_month": suggest.end_year_month,
                    "score": r.score,
                    "created_at": r.created_at,
                    "comment": r.comment,
                    "tags": r.tags
                })
            if len(reviews) != 0:
                avg_score = round(avg_score / len(reviews), 1)
            else:
                avg_score = 0
            res = Response(
                {
                    "senior_id": senior_id,
                    "reviews": review_list,
                    "average_score": avg_score,
                    "message": "리뷰 목록을 성공적으로 조회했습니다."
                },
                status=status.HTTP_200_OK,
            )
            return res
        return Response({"error": "Senior not found"}, status=status.HTTP_404_NOT_FOUND)
    
class CreateReviewView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(tags=['새 리뷰를 작성합니다.'], request_body=ReviewSerializer)
    def post(self, request):
        senior_id = request.data.get('senior')
        user = checkUserExistence(senior_id)
        if user:
            serializer = ReviewSerializer(data=request.data)
            if serializer.is_valid():
                review = serializer.create(validated_data=request.data)
                res = Response(
                    {
                        "review_id": review.id,
                        "message": "리뷰가 성공적으로 생성되었습니다."
                    },
                    status=status.HTTP_200_OK,
                )
                return res
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Senior not found"}, status=status.HTTP_404_NOT_FOUND)

class DeleteReviewView(APIView):
    permission_classes = [AllowAny] 

    @swagger_auto_schema(tags=['리뷰를 삭제합니다.'])
    def delete(self, request, senior_id, review_id):
        review = checkReviewExistence(senior_id, review_id)
        if review:
            review.delete()
            res = Response(
                {
                    "message": "리뷰가 성공적으로 삭제되었습니다."
                },
                status=status.HTTP_200_OK,
            )
            return res
        return Response({"error": "Review not found"}, status=status.HTTP_404_NOT_FOUND)