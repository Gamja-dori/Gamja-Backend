from .models import *
from .serializers import CreateResumeSerializer, ChangeResumeTitleSerializer, FindResumeSerializer, ResumeSerializer, PriorResumeSerializer, CareerSerializer, EducationSerializer, ResumeCardSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from users.models import SeniorUser
from django.core.exceptions import ObjectDoesNotExist

def checkUserExistence(user_id):
    try:
        user = SeniorUser.objects.get(user_id=user_id)
    except ObjectDoesNotExist:
        return False
    return user

def checkResumeExistence(user_id, resume_id):
    user = checkUserExistence(user_id)
    if user:
        try:
            resume = Resume.objects.get(id=resume_id, user=user)
        except ObjectDoesNotExist:
            return False
        return resume
    return False

class CreateResumeAPIView(APIView):
    permission_classes = [AllowAny] 

    @swagger_auto_schema(tags=['새 이력서를 생성합니다.'], request_body=CreateResumeSerializer)
    def post(self, request):
        user_id = request.data.get('user_id')
        user = checkUserExistence(user_id)
        if user:
            serializer = CreateResumeSerializer(data=request.data)
            if serializer.is_valid():
                resume = serializer.create(validated_data=request.data)
                res = Response(
                    {
                        "user_id": user_id,
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
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    
class DeleteResumeAPIView(APIView):
    permission_classes = [AllowAny] 

    @swagger_auto_schema(tags=['이력서를 삭제합니다.'])
    def delete(self, request, user_id, resume_id):
        resume = checkResumeExistence(user_id, resume_id)
        if resume:
            resume.delete()
            res = Response(
                {
                    "message": "이력서가 성공적으로 삭제되었습니다."
                },
                status=status.HTTP_200_OK,
            )
            return res
        return Response({"error": "Resume not found"}, status=status.HTTP_404_NOT_FOUND)
    
class ChangeResumeTitleAPIView(APIView):
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(tags=['이력서 제목을 변경합니다.'], request_body=ChangeResumeTitleSerializer)
    def patch(self, request):
        user_id = request.data.get('user_id')
        resume_id = request.data.get('resume_id')
        resume = checkResumeExistence(user_id, resume_id)
        if resume:
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
        return Response({"error": "Resume not found"}, status=status.HTTP_404_NOT_FOUND)

class SetDefaultResumeAPIView(APIView):
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(tags=['해당 이력서를 기본 이력서로 설정합니다.'], request_body=FindResumeSerializer)
    def patch(self, request):
        user_id = request.data.get('user_id')
        resume_id = request.data.get('resume_id')
        resume = checkResumeExistence(user_id, resume_id)
        if resume:
            serializer = FindResumeSerializer(resume, data=request.data, partial=True)
            if serializer.is_valid():
                prior_default_resume = Resume.objects.filter(is_default=True)
                if len(prior_default_resume) > 0:
                    for p in prior_default_resume:
                        p.is_default = False
                        p.save()
                resume.is_default = True
                serializer.save()
                res = Response(
                    {
                        "resume_id": resume.id,
                        "is_default": resume.is_default,
                        "message": "기본 이력서가 성공적으로 변경되었습니다."
                    },
                    status=status.HTTP_200_OK,
                )
                return res
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Resume not found"}, status=status.HTTP_404_NOT_FOUND)
    
class SubmitResumeAPIView(APIView):
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(tags=['이력서를 인재풀에 등록합니다.'], request_body=FindResumeSerializer)
    def patch(self, request):
        user_id = request.data.get('user_id')
        resume_id = request.data.get('resume_id')
        resume = checkResumeExistence(user_id, resume_id)
        if resume:
            serializer = FindResumeSerializer(resume, data=request.data, partial=True)
            if serializer.is_valid():
                resume.is_submitted = True
                serializer.save()
                res = Response(
                    {
                        "resume_id": resume.id,
                        "is_submitted": resume.is_submitted,
                        "message": "이력서가 성공적으로 인재풀에 등록되었습니다."
                    },
                    status=status.HTTP_200_OK,
                )
                return res
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Resume not found"}, status=status.HTTP_404_NOT_FOUND)

class EditResumeAPIView(APIView):
    permission_classes = [AllowAny] 

    @swagger_auto_schema(tags=['이력서를 수정합니다.'], request_body=ResumeSerializer)
    def put(self, request, user_id, resume_id):
        resume = checkResumeExistence(user_id, resume_id)
        if resume:
            serializer = ResumeSerializer(resume, data=request.data)
            if serializer.is_valid():
                resume = serializer.update(resume, validated_data=request.data)
                resume.save()
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
        return Response({"error": "Resume not found"}, status=status.HTTP_404_NOT_FOUND)
    
class GetResumeAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(tags=['이력서 상세 내용을 조회합니다.'])
    def get(self, request, user_id, resume_id):
        resume = checkResumeExistence(user_id, resume_id)
        if resume:
            serializer = ResumeSerializer(resume)
            res = Response(
                {
                    "resume_id": resume_id,
                    "is_submitted": resume.is_submitted,
                    "resume": serializer.data,
                    "message": "이력서를 성공적으로 조회했습니다."
                },
                status=status.HTTP_200_OK,
            )
            return res
        return Response({"error": "Resume not found"}, status=status.HTTP_404_NOT_FOUND)

class CreateResumeDetailAPIView(APIView):
    permission_classes = [AllowAny] 

    @swagger_auto_schema(tags=['이력서 상세 항목을 생성합니다.'])
    def post(self, request):
        user_id = request.data.get('user_id')
        resume_id = request.data.get('resume_id')
        resume = checkResumeExistence(user_id, resume_id)
        if resume:
            detail_type = request.data.get('detail_type')
            if detail_type == "career":
                detail = Career.objects.create(resume=resume)
            elif detail_type == "education":
                detail = Education.objects.create(resume=resume)
            elif detail_type == "project":
                detail = Project.objects.create(resume=resume)
            elif detail_type == "portfolio":
                detail = Portfolio.objects.create(resume=resume)
            elif detail_type == "performance":
                try: 
                    career_id = request.data.get('career_id')    
                    career = Career.objects.get(id=career_id, resume=resume)
                except ObjectDoesNotExist:
                    return Response({"error": "Career not found"}, status=status.HTTP_404_NOT_FOUND)
                detail = Performance.objects.create(career=career)
            res = Response(
                {
                    "resume_id": resume_id,
                    "detail_type": detail_type,
                    "detail_id": detail.id,
                    "message": "상세 항목이 성공적으로 생성되었습니다."
                },
                status=status.HTTP_200_OK,
            )
            return res
        return Response({"error": "Resume not found"}, status=status.HTTP_404_NOT_FOUND)

class DeleteResumeDetailAPIView(APIView):
    permission_classes = [AllowAny] 

    @swagger_auto_schema(tags=['이력서 상세 항목을 삭제합니다.'])
    def delete(self, request):
        user_id = request.data.get('user_id')
        resume_id = request.data.get('resume_id')
        resume = checkResumeExistence(user_id, resume_id)
        if resume:
            detail_type = request.data.get('detail_type')
            detail_id = request.data.get('detail_id')
            try:
                if detail_type == "career":
                    detail = Career.objects.get(id=detail_id, resume=resume)
                elif detail_type == "education":
                    detail = Education.objects.get(id=detail_id, resume=resume)
                elif detail_type == "project":
                    detail = Project.objects.get(id=detail_id, resume=resume)
                elif detail_type == "portfolio":
                    detail = Portfolio.objects.get(id=detail_id, resume=resume)
                elif detail_type == "performance":
                    career_id = request.data.get('career_id')
                    career = Career.objects.get(id=career_id, resume=resume)
                    detail = Performance.objects.get(id=detail_id, career=career)
            except ObjectDoesNotExist:
                return Response({"error": "Detail not found"}, status=status.HTTP_404_NOT_FOUND)
            detail.delete()
            res = Response(
                {
                    "resume_id": resume_id,
                    "detail_type": detail_type,
                    "detail_id": detail_id,
                    "message": "상세 항목이 성공적으로 삭제되었습니다."
                },
                status=status.HTTP_200_OK,
            )
            return res
        return Response({"error": "Resume not found"}, status=status.HTTP_404_NOT_FOUND)

class GetResumeListAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(tags=['사용자의 이력서 목록을 조회합니다.'])
    def get(self, request, user_id):
        user = checkUserExistence(user_id)
        if user:
            resumes = ResumeCardSerializer(Resume.objects.filter(user=user), many=True)
            res = Response(
                {
                    "user_id": user_id,
                    "resumes": resumes.data,
                    "message": "이력서 목록을 성공적으로 조회했습니다."
                },
                status=status.HTTP_200_OK,
            )
            return res
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    
class ExtractPriorResumeAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(tags=['기존 이력서에서 정보를 추출합니다.'], request_body=PriorResumeSerializer)
    def post(self, request, user_id, resume_id):
        resume = checkResumeExistence(user_id, resume_id)
        if resume:
            serializer = PriorResumeSerializer(data=request.data)
            if serializer.is_valid():
                careers, educations = serializer.create(validated_data=request.data, resume=resume)
                career_serializer = CareerSerializer(careers, many=True)
                education_serializer = EducationSerializer(educations, many=True)
                res = Response(
                    {
                        "user_id": user_id,
                        "resume_id": resume.id,
                        "careers": career_serializer.data,
                        "educations": education_serializer.data,
                        "message": "이력서 정보가 성공적으로 추출되었습니다."
                    },
                    status=status.HTTP_200_OK,
                )
                return res
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Resume not found"}, status=status.HTTP_404_NOT_FOUND)
            
class GetDefaultResumeAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(tags=['기본 이력서 정보를 조회합니다.'])
    def get(self, request, user_id):
        user = checkUserExistence(user_id)
        if user: 
            default_resume = Resume.objects.filter(user=user, is_default=True)
            if not default_resume:
                res = Response(
                    {
                        "user_id": user_id,
                        "resume": {},
                        "message": "등록된 기본 이력서가 없습니다."
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                serializer = ResumeCardSerializer(default_resume[0])
                res = Response(
                    {
                        "user_id": user_id,
                        "resume": serializer.data,
                        "message": "기본 이력서 정보가 성공적으로 조회되었습니다."
                    },
                    status=status.HTTP_200_OK,
                )
            return res
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)