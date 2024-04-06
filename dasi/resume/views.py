from .models import *
from .serializers import CreateResumeSerializer, ChangeResumeTitleSerializer, FindResumeSerializer, ResumeSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from users.models import SeniorUser
from django.core.exceptions import ObjectDoesNotExist

class CreateResumeAPIView(APIView):
    permission_classes = [AllowAny] 

    @swagger_auto_schema(tags=['새 이력서를 생성합니다.'], request_body=CreateResumeSerializer)
    def post(self, request):
        serializer = CreateResumeSerializer(data=request.data)
        if serializer.is_valid():
            resume = serializer.create(validated_data=request.data)
            res = Response(
                {
                    "user_id": resume.user.user_id,
                    "resume_id": resume.id,
                    "title": resume.title,
                    "is_default": resume.is_default,
                    "created_at": resume.created_at,
                    "message": "이력서가 성공적으로 생성되었습니다."
                },
                status=status.HTTP_200_OK,
            )
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DeleteResumeAPIView(APIView):
    permission_classes = [AllowAny] 

    @swagger_auto_schema(tags=['이력서를 삭제합니다.'])
    def delete(self, request, user_id, resume_id):
        try:
            user = SeniorUser.objects.get(user_id=user_id)
        except ObjectDoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            delete_resume = Resume.objects.get(id=resume_id, user=user)
        except ObjectDoesNotExist:
            return Response({"error": "Resume not found"}, status=status.HTTP_404_NOT_FOUND)
        
        delete_resume.delete()
        res = Response(
            {
                "message": "이력서가 성공적으로 삭제되었습니다."
            },
            status=status.HTTP_200_OK,
        )
        return res
    
class ChangeResumeTitleAPIView(APIView):
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(tags=['이력서 제목을 변경합니다.'], request_body=ChangeResumeTitleSerializer)
    def patch(self, request):
        try:
            resume_id = request.data.get('resume_id')
            resume = Resume.objects.get(id=resume_id)
        except ObjectDoesNotExist:
            return Response({"error": "Resume not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ChangeResumeTitleSerializer(resume, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            res = Response(
                {
                    "resume_id": resume.id,
                    "title": resume.title,
                    "message": "이력서 제목이 성공적으로 변경되었습니다."
                },
                status=status.HTTP_200_OK,
            )
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SetDefaultResumeAPIView(APIView):
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(tags=['해당 이력서를 기본 이력서로 설정합니다.'], request_body=FindResumeSerializer)
    def patch(self, request):
        try:
            resume_id = request.data.get('resume_id')
            target_resume = Resume.objects.get(id=resume_id)
        except ObjectDoesNotExist:
            return Response({"error": "Resume not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = FindResumeSerializer(target_resume, data=request.data, partial=True)
        if serializer.is_valid():
            prior_default_resume = Resume.objects.get(is_default=True)
            prior_default_resume.is_default = False
            prior_default_resume.save()
            target_resume.is_default = True
            serializer.save()
            res = Response(
                {
                    "resume_id": target_resume.id,
                    "is_default": target_resume.is_default,
                    "message": "기본 이력서가 성공적으로 변경되었습니다."
                },
                status=status.HTTP_200_OK,
            )
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SubmitResumeAPIView(APIView):
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(tags=['이력서를 인재풀에 등록합니다.'], request_body=FindResumeSerializer)
    def patch(self, request):
        try:
            resume_id = request.data.get('resume_id')
            target_resume = Resume.objects.get(id=resume_id)
        except ObjectDoesNotExist:
            return Response({"error": "Resume not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = FindResumeSerializer(target_resume, data=request.data, partial=True)
        if serializer.is_valid():
            target_resume.is_submitted = True
            serializer.save()
            res = Response(
                {
                    "resume_id": target_resume.id,
                    "is_submitted": target_resume.is_submitted,
                    "message": "이력서가 성공적으로 인재풀에 등록되었습니다."
                },
                status=status.HTTP_200_OK,
            )
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EditResumeAPIView(APIView):
    permission_classes = [AllowAny] 

    @swagger_auto_schema(tags=['이력서를 수정합니다.'], request_body=ResumeSerializer)
    def put(self, request, user_id, resume_id):
        try:
            user = SeniorUser.objects.get(user_id=user_id)
        except ObjectDoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            target_resume = Resume.objects.get(id=resume_id, user=user)
        except ObjectDoesNotExist:
            return Response({"error": "Resume not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ResumeSerializer(target_resume, data=request.data)
        if serializer.is_valid():
            target_resume.is_submitted = False
            target_resume = serializer.update(target_resume, validated_data=request.data)
            target_resume.save()
            res = Response(
                {
                    "resume_id": resume_id,
                    "resume": serializer.data,
                    "message": "이력서가 성공적으로 수정되었습니다."
                },
                status=status.HTTP_200_OK,
            )
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GetResumeAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(tags=['이력서 상세 내용을 조회합니다.'])
    def get(self, request, user_id, resume_id):
        try:
            user = SeniorUser.objects.get(user_id=user_id)
        except ObjectDoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            target_resume = Resume.objects.get(id=resume_id, user=user)
        except ObjectDoesNotExist:
            return Response({"error": "Resume not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ResumeSerializer(target_resume)
        res = Response(
            {
                "resume_id": resume_id,
                "resume": serializer.data,
                "message": "이력서를 성공적으로 조회했습니다."
            },
            status=status.HTTP_200_OK,
        )
        return res

class GetResumeListAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(tags=['사용자의 이력서 목록을 조회합니다.'])
    def get(self, request, user_id):
        try:
            user = SeniorUser.objects.get(user_id=user_id)
        except ObjectDoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        resumes = [{
            "resume_id": resume.id,
            "is_default": resume.is_default,
            "is_verified": resume.is_verified,
            "career_year": resume.career_year,
            "commute_type": resume.commute_type,
            "title": resume.title,
            "job_group": resume.job_group,
            "job_role": resume.job_role,
            "updated_at": resume.updated_at
        } for resume in Resume.objects.filter(user=user)]

        res = Response(
            {
                "user_id": user_id,
                "resumes": resumes,
                "message": "이력서 목록을 성공적으로 조회했습니다."
            },
            status=status.HTTP_200_OK,
        )
        return res